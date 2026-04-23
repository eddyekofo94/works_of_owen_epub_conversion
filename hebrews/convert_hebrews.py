#!/usr/bin/env python3
"""
Convert John Owen Hebrew Commentary EPUBs to EPUB 3.0 with full hierarchical TOC.
"""

import os
import sys
import re
import uuid
import zipfile
import tempfile
import shutil
from xml.etree import ElementTree as ET
from html import escape

try:
    import ebooklib.epub as epub
except ImportError:
    sys.exit("Error: ebooklib not installed. Run: pip install ebooklib")


MODERN_CSS = """\
* { box-sizing: border-box; }
body {
    font-family: Georgia, Palatino, "Palatino Linotype", "Book Antiqua", serif;
    font-size: 1rem; line-height: 1.75; color: #1a1a1a;
    margin: 0 0.5em; text-align: justify; hyphens: auto;
    -webkit-hyphens: auto; epub-hyphens: auto;
}
h1 { font-size: 1.6em; font-weight: bold; text-align: center; margin: 1.5em 0 0.75em; page-break-before: always; }
h2 { font-size: 1.3em; font-weight: bold; text-align: center; margin: 1.5em 0 0.5em; }
h3 { font-size: 1.1em; font-weight: bold; text-align: center; margin: 1.25em 0 0.5em; font-style: italic; }
p, div { margin: 0.5em 0; text-indent: 1.25em; }
section p:first-of-type { text-indent: 0; }
a { text-decoration: none; color: #0000EE; }
.title-page { text-align: center; margin-top: 25%; page-break-after: always; }
.title-page h1 { font-size: 1.8em; margin-bottom: 0.5em; }
.title-page h2 { font-size: 1.2em; font-style: italic; font-weight: normal; margin: 1em 0 2em; }
.title-page p { text-indent: 0; margin: 0.5em 0; }
nav h2 { display: none; }
nav ol { padding-left: 1em; list-style: none; }
nav li { margin: 0.5em 0; }
nav a { text-decoration: none; color: #0000EE; }
"""


def extract_epub_metadata(epub_path):
    with zipfile.ZipFile(epub_path, 'r') as zf:
        content_opf = zf.read('content.opf').decode('utf-8')
    
    tree = ET.fromstring(content_opf)
    result = {'title': None, 'creator': None, 'language': 'en', 'publisher': None}
    
    for elem in tree.iter():
        tag = elem.tag.split('}')[-1]
        if tag == 'title':
            result['title'] = elem.text
        elif tag == 'creator':
            result['creator'] = elem.text
        elif tag == 'language':
            result['language'] = elem.text
        elif tag == 'publisher':
            result['publisher'] = elem.text
    
    return {
        'title': result['title'] or 'An Exposition of the Epistle to the Hebrews',
        'creator': result['creator'] or 'John Owen',
        'language': result['language'],
        'publisher': result['publisher'] or 'Monergism Books'
    }


def extract_html_chapters(epub_path):
    chapters = []
    with zipfile.ZipFile(epub_path, 'r') as zf:
        names = zf.namelist()
        html_files = sorted([n for n in names if n.endswith('.html') or n.endswith('.xhtml')])
        for fname in html_files:
            if 'split' in fname:
                content = zf.read(fname).decode('utf-8')
                chapters.append((fname, content))
    return chapters


def titlecase_text(text):
    """Convert ALL CAPS to Title Case."""
    if not text or len(text) < 3:
        return text
    if text.isupper():
        lower_words = {'of', 'the', 'and', 'in', 'to', 'a', 'an', 'is', 'it', 'for', 'on', 'at', 'by', 'with', 'from', 'be', 'as'}
        words = text.split()
        result = []
        for i, word in enumerate(words):
            if word.lower() in lower_words and i > 0:
                result.append(word.lower())
            else:
                result.append(word.capitalize())
        return ' '.join(result)
    return text


def find_portraits(work_dir):
    """Find portrait images in portraits folder."""
    portraits_dir = os.path.join(work_dir, '..', 'portraits')
    if not os.path.isdir(portraits_dir):
        return []
    portraits = []
    for f in sorted(os.listdir(portraits_dir)):
        if f.lower().endswith(('.jpeg', '.jpg', '.png')):
            portraits.append(os.path.join(portraits_dir, f))
    return portraits


def find_cover_for_volume(work_dir, vol_num):
    """Find the cover image for a volume."""
    covers_dir = os.path.join(work_dir, 'covers')
    if not os.path.isdir(covers_dir):
        return None
    patterns = [f'hb{vol_num}.png', f'hb{vol_num}.jpeg', f'hb{vol_num}.jpg',
                f'Hb{vol_num}.png', f'Hb{vol_num}.jpeg', f'Hb{vol_num}.jpg']
    for pattern in patterns:
        candidate = os.path.join(covers_dir, pattern)
        if os.path.exists(candidate):
            return candidate
    return None


def clean_html(html_content):
    clean = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)
    clean = re.sub(r'class="calibre\d+"', '', clean)
    clean = re.sub(r'<html[^>]*>|<body[^>]*>|</body>|</html>', '', clean)
    return clean


def extract_chapter_title(html_content, default_title):
    title = default_title
    heading_match = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_content, re.DOTALL)
    if heading_match:
        raw_title = heading_match.group(1)
        clean_title = re.sub(r'<[^>]+>', '', raw_title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        if len(clean_title) > 3 and len(clean_title) < 150:
            title = clean_title
    return title[:200]


def extract_toc_anchors(epub_path):
    """Extract ALL TOC anchors from the EPUB with their locations."""
    all_anchors = []
    anchor_skip = {'calibre_pb', 'calibre_link'}
    special_titles = {'pre': 'GENERAL PREFACE BY THE EDITOR', 
                     'note': 'The Epistle Dedicatory',
                     'pref': 'Prefatory Notices'}
    
    with zipfile.ZipFile(epub_path, 'r') as zf:
        names = zf.namelist()
        
        for fname in sorted(names):
            if 'split' in fname and (fname.endswith('.html') or fname.endswith('.xhtml')):
                content = zf.read(fname).decode('utf-8')
                
                for match in re.finditer(r'<a[^>]*\bid="([^"#]+)"[^>]*></a>', content):
                    anchor_id = match.group(1)
                    
                    if anchor_id in anchor_skip:
                        continue
                    
                    anchor_pos = match.end()
                    after_text = content[anchor_pos:anchor_pos+800]
                    
                    h_tags = list(re.finditer(r'<h[1-4][^>]*>(.*?)</h[1-4]>', after_text, re.DOTALL))
                    
                    if h_tags:
                        anchor_text = h_tags[0].group(1).strip()
                        if len(h_tags) > 1:
                            second_text = h_tags[1].group(1).strip()
                            if len(second_text) > len(anchor_text):
                                anchor_text = second_text
                    else:
                        text_only = re.search(r'([^<]{3,200})', after_text)
                        anchor_text = text_only.group(1).strip() if text_only else ''
                    
                    anchor_text = re.sub(r'\s+', ' ', anchor_text).strip()
                    
                    anchor_text = titlecase_text(anchor_text)
                    
                    if len(anchor_text) < 3:
                        continue
                    
                    if anchor_id in special_titles:
                        anchor_text = special_titles[anchor_id]
                    
                    if anchor_text and len(anchor_text) > 2:
                        all_anchors.append((fname, anchor_id, anchor_text))
    
    return all_anchors


def group_anchors_by_chapter(anchors):
    """Group anchors by chapter file."""
    chapters_map = {}
    num_pattern = re.compile(r'_(\d+)\.')
    
    for fname, anchor_id, anchor_text in anchors:
        match = num_pattern.search(fname)
        if match:
            ch_num = int(match.group(1)) + 1
            if ch_num not in chapters_map:
                chapters_map[ch_num] = []
            chapters_map[ch_num].append((anchor_id, anchor_text))
    
    return chapters_map


def generate_ncx(vol_title, epub_chapters, chapters_map):
    """Generate NCX XML with hierarchical TOC."""
    special_titles = {
        'pre': 'GENERAL PREFACE BY THE EDITOR', 
        'note': 'The Epistle Dedicatory',
        'pref': 'Prefatory Notices',
        'canon': 'I. —The canonical authority of the Epistle to the Hebrews',
        'e2': 'II. —Of the penman of the Epistle to the Hebrews',
        'p1': 'PART I: CONCERNING THE EPISTLE TO THE HEBREWS',
    }
    
    ncx = '''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="eng">
  <head>
    <meta content="owen-hebrews-ncx" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>{}</text>
  </docTitle>
  <navMap>
'''.format(escape(vol_title))
    
    ncx += '    <navPoint id="chapter_title">\n'
    ncx += '      <navLabel><text>Title Page</text></navLabel>\n'
    ncx += '      <content src="title.xhtml"/>\n'
    ncx += '    </navPoint>\n'
    
    first_ch_fname = None
    if epub_chapters:
        first_ch_fname = epub_chapters[0][3]
        
        for aid in ['pre', 'note', 'pref']:
            for anchor_id, anchor_text in chapters_map.get(1, []):
                if anchor_id == aid:
                    ncx += f'    <navPoint id="nav_{aid}">\n'
                    ncx += f'      <navLabel><text>{escape(special_titles.get(aid, anchor_text))}</text></navLabel>\n'
                    ncx += f'      <content src="{first_ch_fname}#{aid}"/>\n'
                    ncx += f'    </navPoint>\n'
                    break
    
    prefice_anchor_ids = {'pre', 'note', 'pref'}
    
    nav_counter = 1
    for ch_obj, ch_title, ch_num, ch_fname in epub_chapters:
        ncx += f'    <navPoint id="chapter_{nav_counter}">\n'
        ncx += f'      <navLabel><text>{escape(ch_title)}</text></navLabel>\n'
        ncx += f'      <content src="{ch_fname}"/>\n'
        
        section_list = chapters_map.get(ch_num, [])
        for anchor_id, anchor_text in section_list:
            if anchor_id in prefice_anchor_ids:
                continue
            display_text = special_titles.get(anchor_id, anchor_text)
            nav_counter += 1
            ncx += f'      <navPoint id="chapter_{nav_counter}">\n'
            ncx += f'        <navLabel><text>{escape(display_text)}</text></navLabel>\n'
            ncx += f'        <content src="{ch_fname}#{escape(anchor_id)}"/>\n'
            ncx += f'      </navPoint>\n'
        
        nav_counter += 1
        ncx += f'    </navPoint>\n'
    
    ncx += '''  </navMap>
</ncx>
'''
    
    return ncx


def generate_nav_xhtml(vol_title, epub_chapters, chapters_map, has_portrait=False):
    """Generate nav.xhtml with hierarchical TOC for EPUB3."""
    special_titles = {
        'pre': 'GENERAL PREFACE BY THE EDITOR', 
        'note': 'The Epistle Dedicatory',
        'pref': 'Prefatory Notices',
        'canon': 'I. —The canonical authority of the Epistle to the Hebrews',
        'e2': 'II. —Of the penman of the Epistle to the Hebrews',
        'p1': 'PART I: CONCERNING THE EPISTLE TO THE HEBREWS',
    }
    
    html = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
  <head>
    <title>{escape(vol_title)}</title>
    <link href="style/main.css" rel="stylesheet" type="text/css"/>
  </head>
  <body>
    <nav epub:type="toc" id="id" role="doc-toc">
      <h2>{escape(vol_title)}</h2>
      <ol>
        <li><a href="title.xhtml">Title Page</a></li>
'''
    
    if has_portrait:
        html += '        <li><a href="portrait.xhtml">Portrait</a></li>\n'
    
    preface_anchor_ids = {'pre', 'note', 'pref'}
    
    first_ch_fname = None
    if epub_chapters:
        first_ch_fname = epub_chapters[0][3]
        
        for aid in ['pre', 'note', 'pref']:
            for anchor_id, anchor_text in chapters_map.get(1, []):
                if anchor_id == aid:
                    display_text = special_titles.get(aid, anchor_text)
                    html += f'        <li><a href="{first_ch_fname}#{aid}">{escape(display_text)}</a></li>\n'
                    break
    
    for ch_obj, ch_title, ch_num, ch_fname in epub_chapters:
        html += f'        <li><a href="{ch_fname}">{escape(ch_title)}</a>\n'
        
        section_list = chapters_map.get(ch_num, [])
        if section_list:
            html += '          <ol>\n'
            for anchor_id, anchor_text in section_list:
                if anchor_id in preface_anchor_ids:
                    continue
                display_text = special_titles.get(anchor_id, anchor_text)
                html += f'            <li><a href="{ch_fname}#{escape(anchor_id)}">{escape(display_text)}</a></li>\n'
            html += '          </ol>\n'
        
        html += '        </li>\n'
    
    html += '''      </ol>
    </nav>
  </body>
</html>
'''
    
    return html


def post_process_epub(epub_path, vol_title, epub_chapters, chapters_map, has_portrait=False):
    """Post-process EPUB to add hierarchical TOC (nav.xhtml only for EPUB3)."""
    tmp_dir = tempfile.mkdtemp()
    extract_dir = os.path.join(tmp_dir, 'epub_extracted')
    
    try:
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(epub_path, 'r') as zf:
            zf.extractall(extract_dir)
        
        nav_content = generate_nav_xhtml(vol_title, epub_chapters, chapters_map, has_portrait=has_portrait)
        with open(os.path.join(extract_dir, 'EPUB', 'nav.xhtml'), 'w', encoding='utf-8') as f:
            f.write(nav_content)
        
        # Generate toc.ncx for Apple Books backward compatibility
        ncx_content = generate_ncx(vol_title, epub_chapters, chapters_map)
        with open(os.path.join(extract_dir, 'EPUB', 'toc.ncx'), 'w', encoding='utf-8') as f:
            f.write(ncx_content)
        
        # Add toc.ncx to content.opf manifest and add properties="nav" to nav.xhtml
        opf_path = os.path.join(extract_dir, 'EPUB', 'content.opf')
        if os.path.exists(opf_path):
            with open(opf_path, 'r', encoding='utf-8') as f:
                opf_content = f.read()
            # Add toc.ncx item and properties="nav" to nav.xhtml entry
            if 'href="nav.xhtml"' in opf_content and 'id="ncx"' not in opf_content:
                opf_content = opf_content.replace(
                    '<item href="nav.xhtml"',
                    '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n    <item href="nav.xhtml"'
                )
                opf_content = opf_content.replace(
                    'media-type="application/xhtml+xml"/>',
                    'media-type="application/xhtml+xml" properties="nav"/>'
                )
            with open(opf_path, 'w', encoding='utf-8') as f:
                f.write(opf_content)
        
        temp_zip = epub_path.replace('.epub', '_fixed.zip')
        
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zf.write(file_path, arcname)
        
        os.remove(epub_path)
        os.rename(temp_zip, epub_path)
    
    finally:
        shutil.rmtree(tmp_dir)


def convert_epub(input_path, output_path, work_dir, vol_num):
    """Convert one EPUB to EPUB 3.0 with full hierarchical TOC."""
    print(f"Converting Volume {vol_num}...")
    
    metadata = extract_epub_metadata(input_path)
    print(f"  Title: {metadata['title']}")
    
    chapters_data = extract_html_chapters(input_path)
    anchors = extract_toc_anchors(input_path)
    chapters_map = group_anchors_by_chapter(anchors)
    
    print(f"  Found {len(anchors)} TOC anchors")
    
    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-hebrews-vol-{vol_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(metadata['title'])
    book.set_language(metadata.get('language', 'en'))
    book.add_author(metadata.get('creator', 'John Owen'))
    book.add_metadata('DC', 'publisher', metadata.get('publisher', 'Monergism Books'))
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata('DC', 'subject', 'Hebrews')
    book.add_metadata('DC', 'description', f"John Owen's Commentary on the Epistle to the Hebrews, Volume {vol_num}")
    
    style = epub.EpubItem(
        uid='main-css',
        file_name='style/main.css',
        media_type='text/css',
        content=MODERN_CSS.encode('utf-8')
    )
    book.add_item(style)
    
    cover_path = find_cover_for_volume(work_dir, vol_num)
    if cover_path and os.path.exists(cover_path):
        with open(cover_path, 'rb') as f:
            cover_data = f.read()
        ext = os.path.splitext(cover_path)[1].lower()
        if ext == '.jpeg':
            ext = '.jpg'
        book.set_cover(f'images/cover{ext}', cover_data, create_page=False)
        print(f"  Cover: {os.path.basename(cover_path)}")
    
    title = metadata['title']
    title_body = (
        f'<div class="title-page">'
        f'<h1>{escape(title)}</h1>'
        f'<p>by {escape(metadata.get("creator", "John Owen"))}</p>'
        f'<p>Monergism Books</p>'
        f'</div>'
    )
    
    title_page = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
    title_page.set_content(
        f'<?xml version="1.0" encoding="utf-8"?>'
        f'<html xmlns="http://www.w3.org/1999/xhtml" lang="en">'
        f'<head><link rel="stylesheet" href="style/main.css"/></head>'
        f'<body>{title_body}</body></html>'.encode('utf-8')
    )
    title_page.add_item(style)
    book.add_item(title_page)
    
    portraits = find_portraits(work_dir)
    portrait_page = None
    if portraits:
        print(f"  Portraits: {len(portraits)} found")
        portrait_items = []
        for i, portrait_path in enumerate(portraits):
            with open(portrait_path, 'rb') as f:
                img_data = f.read()
            img_ext = os.path.splitext(portrait_path)[1].lower()
            img_name = f'portrait_{i+1}.jpeg'
            
            portrait_item = epub.EpubItem(
                uid=f'portrait-{i+1}',
                file_name=f'images/{img_name}',
                media_type='image/jpeg',
                content=img_data
            )
            book.add_item(portrait_item)
            portrait_items.append((img_name, os.path.basename(portrait_path)))
        
        if portrait_items:
            portrait_html = '<div class="portrait-page">'
            for img_name, orig_name in portrait_items:
                portrait_html += f'<p><img src="images/{img_name}" alt="Portrait" style="max-width:100%;height:auto;"/></p>'
            portrait_html += '</div>'
            
            portrait_page = epub.EpubHtml(title='Portrait', file_name='portrait.xhtml', lang='en')
            portrait_page.set_content(
                f'<?xml version="1.0" encoding="utf-8"?>'
                f'<html xmlns="http://www.w3.org/1999/xhtml" lang="en">'
                f'<head><link rel="stylesheet" href="style/main.css"/></head>'
                f'<body>{portrait_html}</body></html>'.encode('utf-8')
            )
            portrait_page.add_item(style)
            book.add_item(portrait_page)
            print(f"  Portrait page added")
    
    epub_chapters = []
    
    for i, (fname, content) in enumerate(chapters_data):
        ch_id = f'chapter_{i+1:03d}'
        
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        body_content = body_match.group(1) if body_match else content
        
        ch_title = extract_chapter_title(body_content, f'Part {i+1}')
        if not ch_title or ch_title == f'Part {i+1}':
            ch_title = f'Part {i+1}'
        
        clean_content = clean_html(body_content)
        
        full_html = (
            f'<?xml version="1.0" encoding="utf-8"?>'
            f'<html xmlns="http://www.w3.org/1999/xhtml" lang="en">'
            f'<head><link rel="stylesheet" href="../style/main.css"/></head>'
            f'<body><section>{clean_content}</section></body></html>'
        )
        
        ch = epub.EpubHtml(title=ch_title[:200], file_name=f'{ch_id}.xhtml', lang='en')
        ch.set_content(full_html.encode('utf-8'))
        ch.add_item(style)
        book.add_item(ch)
        
        epub_chapters.append((ch, ch_title, i+1, f'{ch_id}.xhtml'))
        print(f"    Chapter {i+1}/{len(chapters_data)}")
    
    # nav.xhtml with thorough TOC is generated in post_process_epub()
    # EPUB3 only needs nav.xhtml - no need for book.toc (causes duplicate)
    
    # EPUB3 uses thorough nav.xhtml added in post_process
    # Create minimal nav for spine; content replaced by post_process_epub
    nav = epub.EpubHtml(title='Table of Contents', file_name='nav.xhtml', lang='en')
    nav.set_content(b'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en">
<head><link rel="stylesheet" href="style/main.css"/></head>
<body><nav epub:type="toc" id="toc"><ol></ol></nav></body></html>''')
    nav.add_item(style)
    book.add_item(nav)
    
    if portrait_page:
        spine_items = ['nav', title_page, portrait_page] + [ch[0] for ch in epub_chapters]
    else:
        spine_items = ['nav', title_page] + [ch[0] for ch in epub_chapters]
    book.spine = spine_items
    
    has_portrait = portrait_page is not None
    
    temp_epub = output_path.replace('.epub', '_temp.epub')
    epub.write_epub(temp_epub, book, {})
    
    post_process_epub(temp_epub, metadata['title'], epub_chapters, chapters_map, has_portrait)
    
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(temp_epub, output_path)
    
    size = os.path.getsize(output_path)
    print(f"  Saved: {os.path.basename(output_path)} ({size/1024:.0f} KB)")
    return True


def discover_epubs(work_dir):
    v2_dir = os.path.join(work_dir, 'epubs_v2')
    epubs = []
    for f in os.listdir(v2_dir):
        if f.endswith('.epub'):
            match = re.search(r'(\d+)\.epub', f)
            if match:
                vol_num = int(match.group(1))
                epubs.append((vol_num, os.path.join(v2_dir, f), f))
    return sorted(epubs, key=lambda x: x[0])


def main():
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]
    else:
        work_dir = os.getcwd()
    
    work_dir = os.path.abspath(work_dir)
    
    print(f"John Owen Hebrew Commentary -> EPUB 3.0 Converter")
    print(f"Working directory: {work_dir}\n")
    
    epubs = discover_epubs(work_dir)
    if not epubs:
        print(f"No EPUB files found in {work_dir}/epubs_v2/")
        sys.exit(1)
    
    print(f"Found {len(epubs)} EPUB(s):\n")
    for vol_num, path, name in epubs:
        print(f"  Vol {vol_num}: {name}")
    
    print(f"\n{'='*60}\n")
    
    for vol_num, input_path, original_name in epubs:
        output_name = original_name.replace('.epub', '_v3.epub')
        output_path = os.path.join(work_dir, output_name)
        
        convert_epub(input_path, output_path, work_dir, vol_num)
    
    print(f"\n{'='*60}")
    print(f"Done! Converted {len(epubs)} volumes to EPUB 3.0")


if __name__ == '__main__':
    main()