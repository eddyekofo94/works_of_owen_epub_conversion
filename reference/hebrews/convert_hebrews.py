#!/usr/bin/env python3
"""
Convert John Owen Hebrews Commentary EPUBs from EPUB 2 → EPUB 3.
- Reads source NCX for TOC entries (no hardcoded titles)
- Builds hierarchical TOC: PART/CHAPTER headings become parents
- Generates both nav.xhtml (EPUB3) and toc.ncx (EPUB2 fallback)
- Proper EPUB3 spine, cover, and modern CSS
- Works for all 7 volumes
"""

import os
import sys
import re
import uuid
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET
from html import escape
from collections import namedtuple

try:
    import ebooklib.epub as epub
except ImportError:
    sys.exit("Error: ebooklib not installed. Run: pip install ebooklib")


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

TocEntry = namedtuple('TocEntry', ['label', 'href', 'children'])


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

MODERN_CSS = """\
* { box-sizing: border-box; }
body {
    font-family: Georgia, Palatino, "Palatino Linotype", "Book Antiqua", serif;
    font-size: 1rem; line-height: 1.75; color: #1a1a1a;
    margin: 0 0.5em; text-align: justify; hyphens: auto;
    -webkit-hyphens: auto; epub-hyphens: auto;
}
h1 { font-size: 1.6em; font-weight: bold; text-align: center;
     margin: 1.5em 0 0.75em; page-break-before: always; }
h2 { font-size: 1.3em; font-weight: bold; text-align: center;
     margin: 1.5em 0 0.5em; }
h3 { font-size: 1.1em; font-weight: bold; text-align: center;
     margin: 1.25em 0 0.5em; font-style: italic; }
p, div { margin: 0.5em 0; text-indent: 1.25em; }
section p:first-of-type { text-indent: 0; }
.title-page { text-align: center; margin-top: 25%; page-break-after: always; }
.title-page h1 { font-size: 1.8em; margin-bottom: 0.5em; }
.title-page h2 { font-size: 1.2em; font-style: italic; font-weight: normal;
                  margin: 1em 0 2em; }
.title-page p { text-indent: 0; margin: 0.5em 0; }
.portrait-page { text-align: center; margin-top: 15%; page-break-after: always; }
.portrait-page img { max-width: 65%; height: auto; }
.portrait-page p { text-indent: 0; text-align: center; margin-top: 1em;
                    font-style: italic; font-size: 0.9em; }
nav#toc { text-align: left; }
nav#toc h1 { text-align: left; font-size: 1.4em; margin-bottom: 0.75em;
             page-break-before: avoid; }
nav#toc ol { list-style: none; padding: 0; margin: 0; }
nav#toc > ol > li { margin: 0.6em 0; }
nav#toc > ol > li > a { font-weight: bold; font-size: 1.05em; }
nav#toc > ol > li > ol { margin-top: 0.3em; }
nav#toc > ol > li > ol > li { margin: 0.25em 0; padding-left: 1.5em; }
nav#toc > ol > li > ol > li > a { font-weight: normal; font-size: 0.95em; }
nav#toc a { text-decoration: none; }
"""


# ---------------------------------------------------------------------------
# Source EPUB reading
# ---------------------------------------------------------------------------

def extract_epub_metadata(epub_path):
    """Read DC metadata from source content.opf."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        # Find the OPF file (might be in a subdirectory)
        opf_candidates = [n for n in zf.namelist()
                          if n.endswith('.opf')]
        if not opf_candidates:
            return {'title': 'Hebrews', 'creator': 'John Owen',
                    'language': 'en', 'publisher': 'Monergism Books'}
        content_opf = zf.read(opf_candidates[0]).decode('utf-8')

    root = ET.fromstring(content_opf)
    result = {'title': None, 'creator': None,
              'language': 'en', 'publisher': None}
    ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
    for elem in root.findall('.//dc:*', ns):
        tag = elem.tag.split('}')[-1]
        if tag in result:
            result[tag] = elem.text

    return {
        'title': result['title'] or 'An Exposition of the Epistle to the Hebrews',
        'creator': result['creator'] or 'John Owen',
        'language': result['language'],
        'publisher': result['publisher'] or 'Monergism Books',
    }


def extract_html_chapters(epub_path):
    """Return list of (filename, html_content) for split chapter files."""
    chapters = []
    with zipfile.ZipFile(epub_path, 'r') as zf:
        html_files = sorted(
            n for n in zf.namelist()
            if 'split' in n and (n.endswith('.html') or n.endswith('.xhtml'))
        )
        for fname in html_files:
            content = zf.read(fname).decode('utf-8')
            chapters.append((fname, content))
    return chapters


# ---------------------------------------------------------------------------
# TOC extraction from source NCX
# ---------------------------------------------------------------------------

def read_source_ncx(epub_path):
    """Parse the source toc.ncx and return a flat list of (label, href)."""
    with zipfile.ZipFile(epub_path, 'r') as zf:
        ncx_files = [n for n in zf.namelist() if n.endswith('.ncx')]
        if not ncx_files:
            return []
        ncx_xml = zf.read(ncx_files[0]).decode('utf-8')

    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
    root = ET.fromstring(ncx_xml)
    nav_map = root.find('ncx:navMap', ns)
    if nav_map is None:
        return []

    entries = []

    def walk(parent):
        for np in parent.findall('ncx:navPoint', ns):
            label_el = np.find('ncx:navLabel/ncx:text', ns)
            content_el = np.find('ncx:content', ns)
            label = label_el.text.strip() if label_el is not None and label_el.text else ''
            href = content_el.get('src', '') if content_el is not None else ''
            if label:
                entries.append((label, href))
            # Recurse into nested navPoints (some NCXs may already nest)
            walk(np)

    walk(nav_map)
    return entries


def _is_parent_entry(label):
    """Detect whether a TOC label is a group header (PART / CHAPTER)."""
    stripped = label.strip()
    # PART headers
    if re.match(r'^PART\s+[IVXLC]+', stripped, re.IGNORECASE):
        return True
    # CHAPTER headers
    if re.match(r'^CHAPTER\s+\d+', stripped, re.IGNORECASE):
        return True
    return False


def _is_front_matter(label):
    """Detect prefatory / front-matter entries."""
    low = label.strip().lower()
    return any(low.startswith(k) for k in (
        'general preface', 'preface', 'the epistle dedicatory',
        'epistle dedicatory', 'prefatory', 'editor',
    ))


def fix_broken_toc_hrefs(flat_entries, chapters_data):
    """Fix TOC entries whose anchors sit at the tail of an HTML file.

    The source EPUBs sometimes split a section so that the heading anchor
    (e.g. EXERCITATION VI) lands at the very end of one HTML file while
    the actual body content (e.g. ONENESS OF THE CHURCH) starts at the
    top of the next file.  Clicking the TOC entry drops the reader at a
    nearly-empty stub instead of the real content.

    Fix: for each TOC href that points to a file#anchor, check whether
    the anchor appears in the last portion of the file with < 150 chars
    of real text after it.  If so, redirect the href to the next
    sequential HTML file (no fragment).
    """
    # Build ordered list of chapter filenames
    filenames = [os.path.basename(fn) for fn, _ in chapters_data]
    # Build content lookup
    content_by_name = {}
    for fn, html in chapters_data:
        content_by_name[os.path.basename(fn)] = html

    fixed = []
    num_fixed = 0
    for label, href in flat_entries:
        if '#' in href:
            fname, anchor = href.split('#', 1)
            html = content_by_name.get(fname, '')
            if html:
                # Find the anchor position in the raw HTML
                anchor_pattern = f'id="{re.escape(anchor)}"'
                m = re.search(anchor_pattern, html)
                if m:
                    after = html[m.end():]
                    text_after = re.sub(r'<[^>]+>', '', after).strip()
                    if len(text_after) < 150:
                        # Redirect to next file
                        try:
                            idx = filenames.index(fname)
                            if idx + 1 < len(filenames):
                                new_href = filenames[idx + 1]
                                fixed.append((label, new_href))
                                num_fixed += 1
                                continue
                        except ValueError:
                            pass
        fixed.append((label, href))

    if num_fixed:
        print(f"  Fixed {num_fixed} broken TOC link(s)")
    return fixed


def build_toc_hierarchy(flat_entries):
    """Convert a flat list of (label, href) into a nested TocEntry tree.

    Returns a list of top-level TocEntry objects.  PART and CHAPTER
    entries become parents; subsequent entries become their children
    until the next parent or front-matter item.
    """
    tree = []
    current_parent = None
    children = []

    def flush():
        nonlocal current_parent, children
        if current_parent is not None:
            tree.append(TocEntry(
                label=current_parent[0],
                href=current_parent[1],
                children=[TocEntry(l, h, []) for l, h in children],
            ))
        current_parent = None
        children = []

    for label, href in flat_entries:
        if _is_parent_entry(label):
            flush()
            current_parent = (label, href)
            children = []
        elif _is_front_matter(label):
            flush()
            tree.append(TocEntry(label, href, []))
        else:
            if current_parent is not None:
                children.append((label, href))
            else:
                tree.append(TocEntry(label, href, []))

    flush()
    return tree


# ---------------------------------------------------------------------------
# TOC generators (NCX + nav.xhtml)
# ---------------------------------------------------------------------------

def generate_ncx(vol_title, book_uid, toc_tree):
    """Generate a hierarchical toc.ncx from the TOC tree."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">',
        '  <head>',
        f'    <meta content="{escape(book_uid)}" name="dtb:uid"/>',
        '    <meta content="2" name="dtb:depth"/>',
        '    <meta content="0" name="dtb:totalPageCount"/>',
        '    <meta content="0" name="dtb:maxPageNumber"/>',
        '  </head>',
        '  <docTitle>',
        f'    <text>{escape(vol_title)}</text>',
        '  </docTitle>',
        '  <navMap>',
    ]

    order = [0]

    def emit(entry, indent):
        order[0] += 1
        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', entry.href or f'item_{order[0]}')
        pad = '  ' * indent
        lines.append(f'{pad}<navPoint id="nav_{safe_id}" playOrder="{order[0]}">')
        lines.append(f'{pad}  <navLabel><text>{escape(entry.label)}</text></navLabel>')
        lines.append(f'{pad}  <content src="{entry.href}"/>')
        for child in entry.children:
            emit(child, indent + 1)
        lines.append(f'{pad}</navPoint>')

    for entry in toc_tree:
        emit(entry, 2)

    lines.append('  </navMap>')
    lines.append('</ncx>')
    return '\n'.join(lines)


def generate_nav_xhtml(toc_tree):
    """Generate an EPUB3 nav.xhtml from the TOC tree."""
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml"'
        ' xmlns:epub="http://www.idpf.org/2007/ops"'
        ' epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#"'
        ' lang="en" xml:lang="en">',
        '<head>',
        '  <title>Table of Contents</title>',
        '  <link href="stylesheet.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        '<nav epub:type="toc" id="toc">',
        '<h1>Table of Contents</h1>',
        '<ol>',
    ]

    def emit(entry, indent):
        pad = '  ' * indent
        if entry.children:
            lines.append(f'{pad}<li>')
            lines.append(f'{pad}  <a href="{entry.href}">{escape(entry.label)}</a>')
            lines.append(f'{pad}  <ol>')
            for child in entry.children:
                emit(child, indent + 2)
            lines.append(f'{pad}  </ol>')
            lines.append(f'{pad}</li>')
        else:
            lines.append(
                f'{pad}<li><a href="{entry.href}">'
                f'{escape(entry.label)}</a></li>'
            )

    for entry in toc_tree:
        emit(entry, 1)

    lines.append('</ol>')
    lines.append('</nav>')
    lines.append('</body>')
    lines.append('</html>')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def clean_html(html_content):
    """Strip calibre artifacts and old headers from chapter HTML."""
    clean = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)
    clean = re.sub(r'class="calibre\d+"', '', clean)
    clean = re.sub(r'<html[^>]*>|<body[^>]*>|</body>|</html>', '', clean)
    # Strip all old cover/header images (hebrews800.jpg, hebrews_v2.jpg, etc.)
    clean = re.sub(r'<img[^>]*src="hebrews[^"]*\.jpg"[^>]*/?\s*>', '',
                   clean, flags=re.IGNORECASE)

    # Move anchor IDs onto their parent heading element.
    # Source has: <h3><a id="X"></a>TEXT</h3> or <h3><a id="X"/>TEXT</h3>
    # Apple Books is unreliable with self-closing <a> navigation targets.
    # Convert to: <h3 id="X">TEXT</h3>  (EPUB3 best practice)
    clean = re.sub(
        r'(<h[1-6])([^>]*)>\s*<a\s[^>]*id="([^"]+)"[^>]*/?\s*>\s*(?:</a>)?\s*',
        r'\1\2 id="\3">',
        clean,
    )
    return clean


def extract_chapter_title(html_content, default_title):
    """Pull the first heading from a chapter's body HTML."""
    m = re.search(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_content, re.DOTALL)
    if m:
        raw = re.sub(r'<[^>]+>', '', m.group(1))
        raw = re.sub(r'\s+', ' ', raw).strip()
        if 3 < len(raw) < 150:
            return raw
    return default_title


def find_cover_for_volume(work_dir, vol_num):
    """Look for hbN.png / .jpeg / .jpg in covers/."""
    covers_dir = os.path.join(work_dir, 'covers')
    if not os.path.isdir(covers_dir):
        return None
    for ext in ('png', 'jpeg', 'jpg'):
        for prefix in (f'hb{vol_num}', f'Hb{vol_num}'):
            candidate = os.path.join(covers_dir, f'{prefix}.{ext}')
            if os.path.exists(candidate):
                return candidate
    return None


def find_portrait(work_dir):
    """Find a John Owen portrait image, checking multiple locations."""
    # Check hebrews/portraits, then parent portraits/
    for base in (work_dir, os.path.dirname(work_dir)):
        portraits_dir = os.path.join(base, 'portraits')
        if os.path.isdir(portraits_dir):
            for f in sorted(os.listdir(portraits_dir)):
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    return os.path.join(portraits_dir, f)
    return None


# ---------------------------------------------------------------------------
# EPUB3 post-processing
# ---------------------------------------------------------------------------

def post_process_epub3(epub_path):
    """Rewrite the EPUB zip to ensure EPUB3 compliance.

    - Set package version="3.0"
    - Add toc="ncx" to <spine> for backwards compatibility
    - Mark nav.xhtml with properties="nav" in manifest
    - Write mimetype first and uncompressed (EPUB spec requirement)
    """
    tmp_dir = tempfile.mkdtemp()
    extract_dir = os.path.join(tmp_dir, 'epub')
    try:
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(epub_path, 'r') as zf:
            zf.extractall(extract_dir)

        # Find and patch the OPF
        opf_path = None
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.endswith('.opf'):
                    opf_path = os.path.join(root, f)
                    break

        if opf_path:
            with open(opf_path, 'r', encoding='utf-8') as f:
                opf = f.read()

            # Upgrade to EPUB 3.0
            opf = re.sub(r'version="2\.0"', 'version="3.0"', opf)

            # Add toc="ncx" to spine if missing
            if '<spine' in opf and 'toc="ncx"' not in opf:
                opf = opf.replace('<spine', '<spine toc="ncx"')

            # Ensure nav.xhtml has properties="nav"
            opf = re.sub(
                r'(<item[^>]*href="nav\.xhtml"[^>]*)/>',
                r'\1 properties="nav"/>',
                opf,
            )
            # Clean up double properties
            opf = re.sub(r'properties="nav"\s+properties="nav"',
                         'properties="nav"', opf)

            with open(opf_path, 'w', encoding='utf-8') as f:
                f.write(opf)

        # Rebuild ZIP with mimetype first and uncompressed
        temp_zip = epub_path + '.tmp'
        with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            # mimetype MUST be first and stored (not deflated)
            mt_path = os.path.join(extract_dir, 'mimetype')
            if os.path.exists(mt_path):
                zf.write(mt_path, 'mimetype',
                         compress_type=zipfile.ZIP_STORED)

            for dirpath, _, filenames in os.walk(extract_dir):
                for fn in sorted(filenames):
                    if fn == 'mimetype':
                        continue
                    full = os.path.join(dirpath, fn)
                    arcname = os.path.relpath(full, extract_dir)
                    zf.write(full, arcname)

        os.replace(temp_zip, epub_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------

def convert_epub(input_path, output_path, work_dir, vol_num):
    """Convert a single EPUB2 → EPUB3."""
    print(f"\nConverting Volume {vol_num}...")

    # --- metadata ---
    metadata = extract_epub_metadata(input_path)
    vol_title = metadata['title']
    print(f"  Title: {vol_title}")

    # --- source chapters (read before TOC so we can fix broken hrefs) ---
    chapters_data = extract_html_chapters(input_path)

    # --- source TOC ---
    flat_toc = read_source_ncx(input_path)
    # Skip the book-title entry that some NCXs include as first item
    if flat_toc and flat_toc[0][0].lower().startswith('an exposition'):
        flat_toc = flat_toc[1:]
    # Fix anchors that sit at the tail of a split file
    flat_toc = fix_broken_toc_hrefs(flat_toc, chapters_data)
    toc_tree = build_toc_hierarchy(flat_toc)
    print(f"  TOC entries: {len(flat_toc)}  (top-level groups: {len(toc_tree)})")

    # --- book setup ---
    book = epub.EpubBook()
    book_uid = f'urn:uuid:{uuid.uuid5(uuid.NAMESPACE_DNS, f"john-owen-hebrews-v{vol_num}")}'
    book.set_identifier(book_uid)
    book.set_title(vol_title)
    book.set_language(metadata.get('language', 'en'))
    book.add_author(metadata.get('creator', 'John Owen'))
    book.add_metadata('DC', 'publisher',
                      metadata.get('publisher', 'Monergism Books'))
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata('DC', 'subject', 'Hebrews')
    book.add_metadata('DC', 'description',
                      f"John Owen's Commentary on the Epistle to the Hebrews, Volume {vol_num}")

    # --- CSS ---
    style = epub.EpubItem(
        uid='main-css', file_name='stylesheet.css',
        media_type='text/css', content=MODERN_CSS.encode('utf-8'),
    )
    book.add_item(style)

    # --- cover image ---
    cover_path = find_cover_for_volume(work_dir, vol_num)
    cover_ext = 'png'
    if cover_path and os.path.exists(cover_path):
        cover_ext = os.path.splitext(cover_path)[1].lstrip('.')
        with open(cover_path, 'rb') as f:
            cover_data = f.read()
        cover_fname = f'cover.{cover_ext}'
        mime = f'image/{cover_ext}'
        if cover_ext == 'jpg':
            mime = 'image/jpeg'
        book.set_cover(cover_fname, cover_data, create_page=False)
        print(f"  Cover: {os.path.basename(cover_path)}")
    else:
        cover_fname = 'cover.png'
        print("  Cover: (none found)")

    # --- cover page ---
    coverpage = epub.EpubHtml(
        title='Cover', file_name='titlepage.xhtml', lang='en')
    coverpage.set_content(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Cover</title></head>
<body style="text-align:center; margin:0; padding:0;">
<div><img src="{cover_fname}" alt="Cover"
     style="max-width:100%; max-height:100%;"/></div>
</body>
</html>'''.encode('utf-8'))
    book.add_item(coverpage)

    # --- text title page ---
    title_text = f"An Exposition of the Epistle to the Hebrews"
    sub_text = f"Volume {vol_num}"
    text_title = epub.EpubHtml(
        title='Title Page', file_name='text_title.xhtml', lang='en')
    text_title.set_content(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Title Page</title>
<link rel="stylesheet" href="stylesheet.css"/></head>
<body>
<div class="title-page">
<h1>{escape(title_text)}</h1>
<h2>{escape(sub_text)}</h2>
<p>by John Owen</p>
</div>
</body>
</html>'''.encode('utf-8'))
    text_title.add_item(style)
    book.add_item(text_title)

    # --- portrait page ---
    portrait_page = None
    portrait_path = find_portrait(work_dir)
    if portrait_path:
        port_ext = os.path.splitext(portrait_path)[1].lstrip('.')
        port_mime = f'image/{port_ext}'
        if port_ext == 'jpg':
            port_mime = 'image/jpeg'
        port_fname = f'portrait.{port_ext}'
        with open(portrait_path, 'rb') as f:
            port_data = f.read()
        port_img = epub.EpubItem(
            uid='portrait-img', file_name=port_fname,
            media_type=port_mime, content=port_data)
        book.add_item(port_img)

        portrait_page = epub.EpubHtml(
            title='Portrait', file_name='portrait.xhtml', lang='en')
        portrait_page.set_content(f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>John Owen</title>
<link rel="stylesheet" href="stylesheet.css"/></head>
<body>
<div class="portrait-page">
<img src="{port_fname}" alt="Portrait of John Owen"/>
<p>John Owen (1616–1683)</p>
</div>
</body>
</html>'''.encode('utf-8'))
        portrait_page.add_item(style)
        book.add_item(portrait_page)
        print(f"  Portrait: {os.path.basename(portrait_path)}")

    # --- content chapters ---
    epub_chapters = []
    for i, (fname, content) in enumerate(chapters_data):
        old_fname = os.path.basename(fname)

        body_match = re.search(r'<body[^>]*>(.*?)</body>',
                               content, re.DOTALL)
        body_content = body_match.group(1) if body_match else content
        ch_title = extract_chapter_title(body_content, f'Section {i+1}')

        clean_content = clean_html(body_content)

        full_html = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" lang="en">'
            '<head><link rel="stylesheet" href="stylesheet.css"/></head>'
            f'<body>{clean_content}</body></html>'
        )

        ch = epub.EpubHtml(
            title=ch_title[:200], file_name=old_fname, lang='en')
        ch.set_content(full_html.encode('utf-8'))
        ch.add_item(style)
        book.add_item(ch)
        epub_chapters.append(ch)
        print(f"    [{i+1}/{len(chapters_data)}] {old_fname}")

    # --- nav.xhtml (EPUB3 primary navigation) ---
    nav_html = generate_nav_xhtml(toc_tree)
    nav_item = epub.EpubHtml(
        title='Table of Contents', file_name='nav.xhtml', lang='en')
    nav_item.set_content(nav_html.encode('utf-8'))
    nav_item.add_item(style)
    book.add_item(nav_item)

    # --- toc.ncx (EPUB2 fallback) ---
    ncx_xml = generate_ncx(vol_title, book_uid, toc_tree)
    ncx_item = epub.EpubItem(
        uid='ncx', file_name='toc.ncx',
        media_type='application/x-dtbncx+xml',
        content=ncx_xml.encode('utf-8'),
    )
    book.add_item(ncx_item)

    # --- ebooklib TOC (for the <guide> / toc metadata) ---
    # Build ebooklib-compatible TOC from our tree
    eb_toc = []
    for entry in toc_tree:
        if entry.children:
            section = epub.Section(entry.label, entry.href)
            kids = []
            for child in entry.children:
                link = epub.Link(child.href, child.label, child.href)
                kids.append(link)
            eb_toc.append((section, kids))
        else:
            eb_toc.append(epub.Link(entry.href, entry.label, entry.href))
    book.toc = eb_toc

    # --- spine ---
    front = [coverpage, text_title]
    if portrait_page:
        front.append(portrait_page)
    book.spine = front + epub_chapters

    # --- write ---
    temp_epub = output_path + '.tmp'
    epub.write_epub(temp_epub, book, {})

    # --- post-process for EPUB3 compliance ---
    post_process_epub3(temp_epub)

    if os.path.exists(output_path):
        os.remove(output_path)
    os.rename(temp_epub, output_path)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"  Saved: {os.path.basename(output_path)} ({size_kb:.0f} KB)")

    # Show TOC summary
    for entry in toc_tree:
        if entry.children:
            print(f"    {entry.label}  ({len(entry.children)} children)")
        else:
            print(f"    {entry.label}")

    return True


# ---------------------------------------------------------------------------
# Discovery + main
# ---------------------------------------------------------------------------

def discover_epubs(work_dir):
    """Find source EPUB2 files in epubs_v2/ subdirectory."""
    v2_dir = os.path.join(work_dir, 'epubs_v2')
    if not os.path.isdir(v2_dir):
        return []
    epubs = []
    for f in os.listdir(v2_dir):
        if f.endswith('.epub'):
            m = re.search(r'(\d+)\.epub', f)
            if m:
                vol_num = int(m.group(1))
                epubs.append((vol_num, os.path.join(v2_dir, f), f))
    return sorted(epubs, key=lambda x: x[0])


def main():
    work_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    work_dir = os.path.abspath(work_dir)

    print("John Owen Hebrews Commentary  EPUB 2 -> EPUB 3 Converter")
    print(f"Working directory: {work_dir}\n")

    epubs = discover_epubs(work_dir)
    if not epubs:
        print(f"No EPUB files found in {work_dir}/epubs_v2/")
        sys.exit(1)

    print(f"Found {len(epubs)} EPUB(s):\n")
    for vol_num, path, name in epubs:
        print(f"  Vol {vol_num}: {name}")
    print(f"\n{'='*60}")

    succeeded = 0
    for vol_num, input_path, original_name in epubs:
        output_name = original_name.replace('.epub', '_v3.epub')
        output_path = os.path.join(work_dir, output_name)
        try:
            convert_epub(input_path, output_path, work_dir, vol_num)
            succeeded += 1
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\n{'='*60}")
    print(f"Done! Converted {succeeded}/{len(epubs)} volumes to EPUB 3.0")


if __name__ == '__main__':
    main()
