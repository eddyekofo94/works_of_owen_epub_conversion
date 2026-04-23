#!/usr/bin/env python3
"""
Stage 2: ThML XML → EPUB for John Owen Works.

Converts ThML XML files (produced by pdf_to_thml.py) to EPUB 3.0.
Run from the directory containing the ThML XML files.

Usage:
    python3 thml_to_epub.py [work_dir]

Outputs one volume_N.epub per ThML XML found.
Skips volumes where the .epub already exists (delete to reconvert).

Requirements:
    pip install ebooklib
"""

import sys
import os
import re
import uuid
from pathlib import Path

_SCRIPT_DIR = Path(__file__).parent
_WORKSPACE = _SCRIPT_DIR.parent
if str(_WORKSPACE) not in sys.path:
    sys.path.insert(0, str(_WORKSPACE))

from scripts.shared import VOLUME_SUBTITLES, EPUB_STYLESHEET

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed. Run: pip install ebooklib")


# ============================================================================
# XML/XHTML HELPERS
# ============================================================================

def _escape_xml(text):
    return (
        text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
    )


def _make_xhtml(title, body_html, css_href='style/main.css'):
    safe_title = _escape_xml(title)
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">'
        '<head>'
        '<meta charset="utf-8"/>'
        f'<title>{safe_title}</title>'
        f'<link rel="stylesheet" type="text/css" href="{css_href}"/>'
        '</head>'
        f'<body>{body_html}</body>'
        '</html>'
    )


def _elem_to_html(elem):
    html_parts = []
    if elem.text:
        html_parts.append(_escape_xml(elem.text))
    for child in elem:
        if child.tag == 'span':
            lang = child.get('lang', '')
            cls = child.get('class', '')
            style = child.get('style', '')
            attrs = ''
            if lang:
                attrs += f' lang="{lang}"'
            if cls:
                attrs += f' class="{cls}"'
            if style:
                attrs += f' style="{style}"'
            inner = _elem_to_html(child)
            html_parts.append(f'<span{attrs}>{inner}</span>')
        elif child.tag in ('i', 'b', 'em', 'strong'):
            inner = _elem_to_html(child)
            html_parts.append(f'<{child.tag}>{inner}</{child.tag}>')
        else:
            inner = _elem_to_html(child)
            html_parts.append(inner)
        if child.tail:
            html_parts.append(_escape_xml(child.tail))
    return ''.join(html_parts)


# ============================================================================
# TREATISE TITLE PAGE DETECTION AND BUILDING
# ============================================================================

def _is_treatise_title_page(div1):
    paras = div1.findall('p')
    if not paras:
        return False

    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|'
        r'WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )

    connectors = 0
    total_body_text = 0
    leading_connectors = 0
    leading_done = False

    for p in paras:
        text = _elem_to_html(p).strip()
        plain = re.sub(r'<[^>]+>', '', text).strip()
        total_body_text += len(plain)

        is_connector = False
        if re.match(r'^<b>[^<]{1,20}</b>$', text):
            bold_text = re.sub(r'</?b>', '', text).strip()
            if connector_re.match(bold_text):
                connectors += 1
                is_connector = True
        elif connector_re.match(plain) and len(plain) < 15:
            connectors += 1
            is_connector = True

        if not leading_done:
            if is_connector:
                leading_connectors += 1
            else:
                leading_done = True

    if connectors >= 2 and total_body_text < 2000:
        return True
    if leading_connectors >= 2:
        return True
    return False


def _build_treatise_title(div1):
    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|'
        r'WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )

    parts = ['<div class="treatise-title">']

    heading_text = ''
    heading_tag = 'h1'
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            heading_text = _elem_to_html(h_elem).strip()
            heading_tag = h_tag
            break

    heading_lines = [h.strip() for h in heading_text.split(' — ') if h.strip()]

    body_paras = []
    connectors_list = []
    for p_elem in div1.findall('p'):
        html = _elem_to_html(p_elem)
        trimmed = html.strip()
        if not trimmed:
            continue
        plain = re.sub(r'<[^>]+>', '', trimmed).strip()

        is_conn = False
        if re.match(r'^<b>[^<]{1,20}</b>$', trimmed):
            bold_text = re.sub(r'</?b>', '', trimmed).strip()
            if connector_re.match(bold_text):
                connectors_list.append(bold_text)
                body_paras.append(('connector', bold_text))
                is_conn = True
        elif connector_re.match(plain) and len(plain) < 15:
            connectors_list.append(plain)
            body_paras.append(('connector', plain))
            is_conn = True

        if not is_conn:
            body_paras.append(('other', trimmed, plain))

    if len(heading_lines) > 1 and connectors_list:
        parts.append(f'<h1>{_escape_xml(heading_lines[0])}</h1>')
        conn_idx = 0
        for i, line in enumerate(heading_lines[1:]):
            if conn_idx < len(connectors_list):
                parts.append(
                    f'<p class="connector">'
                    f'{_escape_xml(connectors_list[conn_idx])}</p>'
                )
                conn_idx += 1
            parts.append(f'<h2>{_escape_xml(line)}</h2>')
        used_connectors = conn_idx
    else:
        parts.append(f'<{heading_tag}>{heading_text}</{heading_tag}>')
        used_connectors = 0

    connector_skip = 0
    for item in body_paras:
        if item[0] == 'connector':
            if connector_skip < used_connectors:
                connector_skip += 1
                continue
            bold_text = item[1]
            parts.append(f'<p class="connector">{_escape_xml(bold_text)}</p>')
            continue

        trimmed = item[1]
        plain = item[2]

        if trimmed.startswith('<i>'):
            parts.append(f'<p class="desc">{trimmed}</p>')
            continue

        if plain.startswith(('"', '\u201c', "'", '\u2018')):
            parts.append(f'<p class="epigraph">{trimmed}</p>')
            continue

        parts.append(f'<p>{trimmed}</p>')

    parts.append('</div>')
    return ''.join(parts)


def _build_normal_chapter(div1):
    body_parts = ['<section>']

    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            body_parts.append(
                f'<{h_tag}>{_elem_to_html(h_elem)}</{h_tag}>'
            )
            break

    para_count = 0
    for p_elem in div1.findall('p'):
        p_html = _elem_to_html(p_elem)
        if not p_html.strip():
            continue
        css_class = ' class="first"' if para_count == 0 else ''
        body_parts.append(f'<p{css_class}>{p_html}</p>')
        para_count += 1

    body_parts.append('</section>')
    return ''.join(body_parts)


# ============================================================================
# ThML → EPUB CONVERSION
# ============================================================================

def thml_to_epub(thml_path, epub_path, volume_num, cover_image=None):
    print(f"  Parsing ThML XML...")
    try:
        from xml.etree import ElementTree as ET
        tree = ET.parse(thml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"  Error parsing ThML: {e}")
        return False

    dc_title = root.find('.//DC.Title')
    dc_creator = root.find('.//DC.Creator')
    title = dc_title.text if dc_title is not None else f"The Works of John Owen, Vol. {volume_num}"
    author = dc_creator.text if dc_creator is not None else "John Owen"
    subtitle = VOLUME_SUBTITLES.get(volume_num, "")

    print(f"  Creating EPUB 3 structure...")

    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-works-bot-vol-{volume_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)
    book.add_metadata('DC', 'publisher', 'Banner of Truth Trust')
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata(
        'DC', 'description',
        f'Volume {volume_num} of The Works of John Owen, '
        f'edited by William H. Goold.'
    )

    style = epub.EpubItem(
        uid='main-css',
        file_name='style/main.css',
        media_type='text/css',
        content=EPUB_STYLESHEET.encode('utf-8')
    )
    book.add_item(style)

    cover_item = None
    if cover_image and os.path.exists(cover_image):
        try:
            with open(cover_image, 'rb') as f:
                cover_data = f.read()
            ext = os.path.splitext(cover_image)[1].lower()
            book.set_cover(f'images/cover{ext}', cover_data)
            print(f"  Added cover image")
        except Exception as e:
            print(f"  Warning: Could not add cover: {e}")

    title_body = (
        '<div class="title-page">'
        f'<h1>{_escape_xml(title)}</h1>'
        f'<p class="subtitle">{_escape_xml(subtitle)}</p>'
        f'<p class="author">by<br/>{_escape_xml(author)}</p>'
        '<p class="publisher">Banner of Truth Trust</p>'
        '</div>'
    )
    title_page = epub.EpubHtml(
        title='Title Page', file_name='title.xhtml', lang='en'
    )
    title_page.set_content(
        _make_xhtml('Title Page', title_body).encode('utf-8')
    )
    title_page.add_item(style)
    book.add_item(title_page)

    print(f"  Converting chapters...")
    epub_chapters = []
    div1_elements = root.findall('.//div1')

    for div_idx, div1 in enumerate(div1_elements):
        chapter_title = div1.get('title', f'Chapter {div_idx + 1}')
        chapter_id = div1.get('id', f'ch{div_idx + 1:03d}')

        is_treatise_title = _is_treatise_title_page(div1)

        if is_treatise_title:
            body_html = _build_treatise_title(div1)
        else:
            body_html = _build_normal_chapter(div1)

        ch_item = epub.EpubHtml(
            title=chapter_title[:200],
            file_name=f'{chapter_id}.xhtml',
            lang='en'
        )
        ch_item.set_content(
            _make_xhtml(chapter_title, body_html).encode('utf-8')
        )
        ch_item.add_item(style)
        book.add_item(ch_item)
        epub_chapters.append((ch_item, chapter_title))

    print(f"  {len(epub_chapters)} chapters created")

    toc_entries = [ch[0] for ch in epub_chapters]
    book.toc = [title_page] + toc_entries

    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    nav.add_item(style)
    book.add_item(nav)

    spine_items = ['nav', title_page] + [ch[0] for ch in epub_chapters]
    book.spine = spine_items

    print(f"  Writing EPUB file...")
    try:
        epub.write_epub(epub_path, book, {})
        file_size = os.path.getsize(epub_path)
        print(f"  Saved EPUB: {epub_path} ({file_size / 1024:.0f} KB)")
        return True
    except Exception as e:
        print(f"  Error writing EPUB: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================================
# FILE DISCOVERY
# ============================================================================

def extract_volume_number_from_path(path):
    import re
    filename = os.path.basename(path)
    match = re.search(r'vol[_\s]*(\d{1,2})', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'[-_]v(\d{1,2})[-_.]', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d{1,2})', filename)
    if match:
        num = int(match.group(1))
        if 1 <= num <= 16:
            return num
    return None


def find_cover(work_dir, volume_num):
    covers_dir = os.path.join(work_dir, 'covers')
    if not os.path.isdir(covers_dir):
        return None
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        cover_path = os.path.join(covers_dir, f'v{volume_num}{ext}')
        if os.path.exists(cover_path):
            return cover_path
    return None


def discover_thml(work_dir):
    thml_files = []
    for file in os.listdir(work_dir):
        if not file.endswith('.thml.xml'):
            continue
        pdf_path = os.path.join(work_dir, file)
        volume_num = extract_volume_number_from_path(file)
        if volume_num and 1 <= volume_num <= 16:
            thml_files.append((volume_num, pdf_path, file))
    return sorted(thml_files, key=lambda x: x[0])


# ============================================================================
# MAIN CONVERSION
# ============================================================================

def process_volume(thml_path, work_dir, volume_num):
    basename = os.path.basename(thml_path)
    print(f"\nProcessing Volume {volume_num}: {basename}")

    epub_path = os.path.join(work_dir, f'volume_{volume_num}.epub')

    if os.path.exists(epub_path):
        print(f"  Skipping (EPUB already exists: {epub_path})")
        return True, epub_path

    cover_image = find_cover(work_dir, volume_num)

    if not thml_to_epub(thml_path, epub_path, volume_num, cover_image):
        return False, None

    return True, epub_path


def main():
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]
    else:
        work_dir = os.getcwd()

    work_dir = os.path.abspath(work_dir)

    print(f"John Owen Works — ThML XML → EPUB")
    print(f"Working directory: {work_dir}\n")

    if not os.path.isdir(work_dir):
        print(f"Error: Directory not found: {work_dir}")
        sys.exit(1)

    thml_files = discover_thml(work_dir)
    if not thml_files:
        print(f"No ThML XML files found in {work_dir}")
        sys.exit(1)

    print(f"Found {len(thml_files)} ThML XML file(s):\n")
    for vol_num, _, filename in thml_files:
        print(f"  Vol {vol_num}: {filename}")

    print(f"\n{'=' * 70}\n")
    results = []

    for vol_num, thml_path, filename in thml_files:
        success, epub_path = process_volume(thml_path, work_dir, vol_num)
        results.append((vol_num, success, epub_path))

    print(f"\n{'=' * 70}")
    print(f"SUMMARY\n")
    succeeded = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    print(f"Succeeded: {len(succeeded)}/{len(results)}")
    for vol_num, _, epub_path in succeeded:
        print(f"  Vol {vol_num}: {epub_path}")
    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for vol_num, _, _ in failed:
            print(f"  Vol {vol_num}")
    print(f"\n{'=' * 70}")


if __name__ == '__main__':
    main()