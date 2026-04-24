#!/usr/bin/env python3
"""
Convert John Owen Hebrew Commentary EPUBs to EPUB 3.0 with OLD structure.
- Keep original file names: hebrews_v1_split_000.html, titlepage.xhtml
- Use toc.ncx only (no nav.xhtml)
- Match old EPUB structure exactly
"""

import os
import sys
import re
import uuid
import zipfile
import tempfile
import shutil
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
.title-page { text-align: center; margin-top: 25%; page-break-after: always; }
.title-page h1 { font-size: 1.8em; margin-bottom: 0.5em; }
.title-page h2 { font-size: 1.2em; font-style: italic; font-weight: normal; margin: 1em 0 2em; }
.title-page p { text-indent: 0; margin: 0.5em 0; }
"""


def extract_epub_metadata(epub_path):
    with zipfile.ZipFile(epub_path, 'r') as zf:
        content_opf = zf.read('content.opf').decode('utf-8')
    
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(content_opf)
    result = {'title': None, 'creator': None, 'language': 'en', 'publisher': None}
    
    ns = {'opf': 'http://www.idpf.org/2007/opf', 'dc': 'http://purl.org/dc/elements/1.1/'}
    for elem in tree.findall('.//dc:*', ns):
        tag = elem.tag.split('}')[-1]
        if tag in result:
            result[tag] = elem.text
    
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
        html_files = sorted([n for n in names if 'split' in n and (n.endswith('.html') or n.endswith('.xhtml'))])
        for fname in html_files:
            content = zf.read(fname).decode('utf-8')
            chapters.append((fname, content))
    return chapters


def titlecase_text(text):
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


def find_cover_for_volume(work_dir, vol_num):
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
    # Remove old decorative header image reference (not needed - we have proper cover)
    clean = re.sub(r'<img[^>]*hebrews800\.jpg[^>]*>', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'src="hebrews800\.jpg"', '', clean, flags=re.IGNORECASE)
    return clean


def preserve_anchors(html_content, anchor_ids):
    for anchor_id in anchor_ids:
        pattern = r'(<h[1-4][^>]*>)'
        replacement = rf'\1<a id="{anchor_id}"></a>'
        html_content = re.sub(pattern, replacement, html_content, count=1)
    return html_content


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
    """Extract ALL TOC anchors from the EPUB including special markers."""
    all_anchors = []
    seen_anchors = set()
    anchor_skip = {'calibre_pb', 'calibre_link'}
    
    with zipfile.ZipFile(epub_path, 'r') as zf:
        names = zf.namelist()
        
        for fname in sorted(names):
            if 'split' in fname and (fname.endswith('.html') or fname.endswith('.xhtml')):
                content = zf.read(fname).decode('utf-8')
                
                # Find all anchors in <a id="..."></a> format
                for match in re.finditer(r'<a[^>]*\bid="([^"#]+)"[^>]*></a>', content):
                    anchor_id = match.group(1)
                    
                    if anchor_id in anchor_skip or anchor_id in seen_anchors:
                        continue
                    
                    seen_anchors.add(anchor_id)
                    
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
                    
                    if len(anchor_text) < 3:
                        continue
                    
                    if anchor_text and len(anchor_text) > 2:
                        all_anchors.append((fname, anchor_id, anchor_text))
    
    return all_anchors


def group_anchors_by_chapter(anchors):
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


def generate_ncx_old(vol_title, chapters_map):
    """Generate NCX with proper nesting for left-aligned hierarchy."""
    
    # Title mappings
    EXACT_TITLE = {
        'pre': 'GENERAL PREFACE BY THE EDITOR',
        'note': 'The Epistle Dedicatory',
        'pref': 'Prefatory Notices',
        'p1': 'PART I: CONCERNING THE EPISTLE TO THE HEBREWS',
        'canon': 'I. —The canonical authority of the Epistle to the Hebrews',
        'e2': 'II. —Of the penman of the Epistle to the Hebrews',
        'e3': 'III. —The time [and occasion] of the writing of the Epistle to the Hebrews',
        'e4': 'IV. —The language wherein the Epistle to the Hebrews was originally written',
        'e5': 'V. —Testimonies cited by the apostle out of the Old Testament',
        'e6': 'VI. —Oneness of the church',
        'e7': 'VII. —Of the Judaical distribution of the Old Testament',
        'p2': 'PART II: CONCERNING THE MESSIAH',
        'e8': 'VIII. —The first dissertation concerning the Messiah, proving him to be promised of old',
        'e9': 'IX. —Promises of the Messiah vindicated',
        'ex': 'X. —Appearances of the Son of God under the old Testament',
        'e11': 'XI. —Faith of the ancient church of the Jews concerning the Messiah',
        'e12': 'XII. —[Second dissertation]—The promised Messiah long since come',
        'e13': 'XIII. —Other testimonies proving the Messiah to be come',
        'e14': 'XIV. —Daniel\'s prophecy vindicated',
        'e15': 'XV. —Computation of Daniel\'s weeks',
        'e16': 'XVI. —The exposition of the Psalm',
        'e17': 'XVII. —The doctrinal part of the Epistle',
        'e18': 'XVIII. —The sundry types and shadows',
        'e19': 'XIX. —The nature of Gospel obedience',
        'e20': 'XX. —The witness of the Spirit',
        'e21': 'XXI. —The saintsâ€™ communion with Christ',
        'e22': 'XXII. —The way of salvation opened',
        'e23': 'XXIII. —The gospel method of salvation',
        'e24': 'XXIV. —The conclusion of the whole',
        'p3': 'PART III: CONCERNING THE OFFICE OF THE MESSIAH',
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
    
    # Collect all items with their file references
    all_items = []
    for ch_num in sorted(chapters_map.keys()):
        for anchor_id, anchor_text in chapters_map[ch_num]:
            if ch_num == 1 and anchor_id in ['pre', 'note', 'pref']:
                fname = 'hebrews_v1_split_000.html'
            else:
                fname = f'hebrews_v1_split_{ch_num-1:03d}.html'
            all_items.append((anchor_id, fname))
    
    play_order = 1
    in_part1 = False
    in_part2 = False
    
    for anchor_id, fname in all_items:
        display = EXACT_TITLE.get(anchor_id, anchor_id)
        
        # Handle preface items (no nesting)
        if anchor_id in ['pre', 'note', 'pref']:
            ncx += f'    <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
            ncx += f'      <navLabel><text>{escape(display)}</text></navLabel>\n'
            ncx += f'      <content src="{fname}#{anchor_id}"/>\n'
            ncx += f'    </navPoint>\n'
            play_order += 1
            continue
        
        # PART I header
        if anchor_id == 'p1':
            ncx += f'    <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
            ncx += f'      <navLabel><text>{escape(display)}</text></navLabel>\n'
            ncx += f'      <content src="{fname}#{anchor_id}"/>\n'
            play_order += 1
            in_part1 = True
            continue
        
        # Exercises under PART I (nested)
        if in_part1 and anchor_id.startswith('e') and not anchor_id.startswith('e1') or in_part1 and anchor_id in ['canon']:
            ncx += f'      <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
            ncx += f'        <navLabel><text>{escape(display)}</text></navLabel>\n'
            ncx += f'        <content src="{fname}#{anchor_id}"/>\n'
            ncx += f'      </navPoint>\n'
            play_order += 1
            continue
        
        # PART II header - close PART I first
        if in_part1 and anchor_id == 'p2':
            ncx += f'    </navPoint>\n'  # Close PART I parent
            ncx += f'    <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
            ncx += f'      <navLabel><text>{escape(display)}</text></navLabel>\n'
            ncx += f'      <content src="{fname}#{anchor_id}"/>\n'
            play_order += 1
            in_part1 = False
            in_part2 = True
            continue
        
        # Exercises under PART II (nested)
        if in_part2 and anchor_id.startswith('e'):
            ncx += f'      <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
            ncx += f'        <navLabel><text>{escape(display)}</text></navLabel>\n'
            ncx += f'        <content src="{fname}#{anchor_id}"/>\n'
            ncx += f'      </navPoint>\n'
            play_order += 1
            continue
        
        # Default - top level
        ncx += f'    <navPoint id="nav_{anchor_id}" playOrder="{play_order}">\n'
        ncx += f'      <navLabel><text>{escape(display)}</text></navLabel>\n'
        ncx += f'      <content src="{fname}#{anchor_id}"/>\n'
        ncx += f'    </navPoint>\n'
        play_order += 1
    
    # Close any open tags
    if in_part1:
        ncx += f'    </navPoint>\n'
    if in_part2:
        ncx += f'    </navPoint>\n'
    
    ncx += '''  </navMap>
</ncx>
'''
    
    return ncx


def convert_epub(input_path, output_path, work_dir, vol_num):
    """Convert EPUB with OLD structure."""
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
        file_name='stylesheet.css',
        media_type='text/css',
        content=MODERN_CSS.encode('utf-8')
    )
    book.add_item(style)
    
    cover_path = find_cover_for_volume(work_dir, vol_num)
    if cover_path and os.path.exists(cover_path):
        with open(cover_path, 'rb') as f:
            cover_data = f.read()
        book.set_cover('cover.jpeg', cover_data, create_page=False)
        print(f"  Cover: {os.path.basename(cover_path)}")
    
    # Create titlepage showing cover image (like old EPUB)
    titlepage = epub.EpubHtml(title='Cover', file_name='titlepage.xhtml', lang='en')
    titlepage.set_content(b'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Cover</title></head>
<body>
<div><img src="cover.jpeg" alt="Cover"/></div>
</body>
</html>''')
    book.add_item(titlepage)
    
    # Create elegant text title page (old EPUB simple style)
    title_text = f"An Exposition of the Epistle to the Hebrews, Vol. {vol_num}"
    author_text = "by John Owen"
    text_title = epub.EpubHtml(title='Title', file_name='text_title.xhtml', lang='en')
    text_title.set_content(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Title</title></head>
<body>
<h2>{escape(title_text)}</h2>
<h3>{escape(author_text)}</h3>
</body>
</html>'''.encode('utf-8'))
    book.add_item(text_title)
    
    epub_chapters = []
    
    for i, (fname, content) in enumerate(chapters_data):
        old_fname = os.path.basename(fname)
        
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        body_content = body_match.group(1) if body_match else content
        
        ch_title = extract_chapter_title(body_content, f'Part {i+1}')
        if not ch_title or ch_title == f'Part {i+1}':
            ch_title = f'Part {i+1}'
        
        clean_content = clean_html(body_content)
        
        chapter_anchor_ids = [a[0] for a in chapters_map.get(i+1, [])]
        if chapter_anchor_ids:
            clean_content = preserve_anchors(clean_content, chapter_anchor_ids)
        
        full_html = (
            f'<?xml version="1.0" encoding="utf-8"?>'
            f'<html xmlns="http://www.w3.org/1999/xhtml" lang="en">'
            f'<head><link rel="stylesheet" href="stylesheet.css"/></head>'
            f'<body>{clean_content}</body></html>'
        )
        
        ch = epub.EpubHtml(title=ch_title[:200], file_name=old_fname, lang='en')
        ch.set_content(full_html.encode('utf-8'))
        ch.add_item(style)
        book.add_item(ch)
        
        epub_chapters.append((ch, ch_title, i+1, old_fname))
        print(f"    Chapter {i+1}/{len(chapters_data)}: {old_fname}")
    
    toc_ncx = generate_ncx_old(metadata['title'], chapters_map)
    toc_item = epub.EpubItem(
        uid='ncx',
        file_name='toc.ncx',
        media_type='application/x-dtbncx+xml',
        content=toc_ncx.encode('utf-8')
    )
    book.add_item(toc_item)
    
    book.spine = [titlepage, text_title] + [ch[0] for ch in epub_chapters]
    
    temp_epub = output_path.replace('.epub', '_temp.epub')
    epub.write_epub(temp_epub, book, {})
    
    post_process_epub_simple(temp_epub)
    
    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(temp_epub, output_path)
    
    size = os.path.getsize(output_path)
    print(f"  Saved: {os.path.basename(output_path)} ({size/1024:.0f} KB)")
    return True


def post_process_epub_simple(epub_path):
    """Fix up the EPUB: ensure spine has toc='ncx'."""
    tmp_dir = tempfile.mkdtemp()
    extract_dir = os.path.join(tmp_dir, 'epub_extracted')
    
    try:
        os.makedirs(extract_dir, exist_ok=True)
        
        with zipfile.ZipFile(epub_path, 'r') as zf:
            zf.extractall(extract_dir)
        
        opf_path = os.path.join(extract_dir, 'content.opf')
        if os.path.exists(opf_path):
            with open(opf_path, 'r', encoding='utf-8') as f:
                opf_content = f.read()
            
            opf_content = opf_content.replace('<spine>', '<spine toc="ncx">')
            
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