import re
import os
import zipfile
import shutil
import xml.etree.ElementTree as ET
from shared import _repair_owen_ocr_errors, nav_display_title, VOLUME_SUBTITLES, FOOTNOTE_MARKER_RE
from html import escape as _html_escape, unescape as _html_unescape
from ebooklib import epub
from scripts.epub_pages import _TITLE_CONNECTORS

def _escape_xml(text):
    if text is None:
        return ""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def _make_xhtml(title, body_html, css_href='style/main.css'):
    safe_title = _escape_xml(title)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        f'lang="en" xml:lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8"/>\n'
        f'  <title>{safe_title}</title>\n'
        f'  <link rel="stylesheet" type="text/css" href="{css_href}"/>\n'
        '</head>\n'
        f'<body>{body_html}</body>\n'
        '</html>'
    )


def _build_title_page(vol_num, title, subtitle):
    return f'''<div class="title-page">
<p class="ornament">❧</p>
<h1 class="primary">The Works of<br/>John Owen</h1>
<hr class="rule"/>
<h2 class="secondary">Volume {vol_num}</h2>
<h2 class="secondary">{_escape_xml(subtitle)}</h2>
<p class="author"><span class="by">by</span>John Owen</p>
<p class="editor">Edited by William H. Goold</p>
<p class="publisher">Eduardus Ekofius</p>
</div>'''





def _polish_treatise_title_page_html(html: str, seen_footnote_refs=None) -> str:
    """Normalize pre-rendered treatise title pages into one elegant title sheet."""
    if not re.search(r'<section\b[^>]*class="[^"]*\btreatise-title-page\b', html):
        return html

    if seen_footnote_refs is not None:
        def footnote_marker_repl(match):
            fn_num = match.group(1)
            if fn_num in seen_footnote_refs:
                return ''
            seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'
        html = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, html)

    # Fix "title-line -major" -> "title-line-major", handles -minor, -small, -medium too
    html = re.sub(r'class="title-line\s+-(\w+)"', r'class="title-line-\1"', html)
    
    # Also handle the case where it was already partially fixed or has multiple classes
    html = re.sub(r'class="title-line\s+title-line-(\w+)"', r'class="title-line-\1"', html)

    html = re.sub(
        r'<p class="title-line-medium">\s*(' + '|'.join(re.escape(item) for item in sorted(_TITLE_CONNECTORS, key=len, reverse=True)) + r')\s*</p>',
        lambda m: f'<p class="title-connector">{m.group(1)}</p>',
        html,
        flags=re.I,
    )

    def _connector_repl(match):
        attrs = match.group(1)
        if 'greek-title' in attrs:
            return f'<p class="greek-title">{match.group(2).strip()}</p>'
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if text.upper() not in _TITLE_CONNECTORS:
            return match.group(0)
        return f'<p class="title-connector">{match.group(2).strip()}</p>'

    html = re.sub(r'<h2([^>]*)>\s*(.*?)\s*</h2>', _connector_repl, html, flags=re.I | re.S)
    html = re.sub(
        r'<h2([^>]*)>\s*(.*?)\s*</h2>',
        lambda m: f'<p class="title-line title-line-medium">{m.group(2).strip()}</p>',
        html,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'<h1([^>]*)>\s*(.*?)\s*</h1>',
        lambda m: f'<p class="title-line title-line-major">{m.group(2).strip()}</p>',
        html,
        flags=re.I | re.S,
    )

    if seen_footnote_refs is not None:
        from render import _restore_footnote_placeholders
        html = _restore_footnote_placeholders(html)

    return html


def _polish_volume_title_page_html(html: str, vol_num: int, config: dict) -> str:
    """Ensure generated/extracted volume title pages carry edition metadata."""
    if 'class="title-page"' not in html:
        return html
    publisher = _escape_xml(config.get('publisher') or 'Eduardus Ekofius')
    editors = config.get('editors') or ['William H. Goold']
    editor = _escape_xml(editors[0])
    subtitle = _escape_xml(VOLUME_SUBTITLES.get(vol_num, ''))
    if re.search(r'THE\s+WORKS\s+OF(?:<br\s*/?>|\s)+JOHN\s+OWEN', html, re.I):
        subtitle_html = f'<p class="title-volume-subtitle">{subtitle}</p>' if subtitle else ''
        return f'''<section class="title-page volume-title-page" epub:type="titlepage">
<div class="emblem-container">
<img class="title-emblem-seal" src="images/emblem_seal.png" alt="Emblem Seal of Dr. John Owen"/>
</div>
<p class="title-work-top">The Works of</p>
<h1 class="title-author-main">John Owen</h1>
<div class="title-divider-double" aria-hidden="true"></div>
<p class="title-volume-number">Volume {vol_num}</p>
{subtitle_html}
<div class="title-meta-divider" aria-hidden="true"></div>
<div class="title-meta">
<p class="editor">Edited by {editor}</p>
<p class="publisher-brand">{publisher}</p>
<p class="publisher-loc">Parentis-en-Born</p>
<p class="edition-year">MMXXVI</p>
</div>
</section>'''
    meta_bits = []
    if 'Edited by' not in html and 'EDITED BY' not in html:
        meta_bits.append(f'<p class="editor">Edited by {editor}</p>')
    if publisher not in html:
        meta_bits.append(f'<p class="publisher-brand">{publisher}</p>')
        meta_bits.append('<p class="publisher-loc">Parentis-en-Born</p>')
    if '2026' not in html and 'MMXXVI' not in html:
        meta_bits.append('<p class="edition-year">MMXXVI</p>')
    if not meta_bits:
        return html
    meta = '<div class="title-meta">' + ''.join(meta_bits) + '</div>'
    return re.sub(r'</section>\s*$', meta + '</section>', html, flags=re.S)




def generate_frontispiece_xhtml(portrait_filename):
    return f'<div class="frontispiece"><img src="images/{portrait_filename}" alt="Portrait of John Owen"/><p class="caption">John Owen (1616&#x2013;1683)</p></div>'


def generate_nav_xhtml(toc_entries, volume_title=None, has_cover=False, has_frontispiece=False, first_content_href=None):
    from render import tag_unicode_ranges
    """Generate 3-level NAV XHTML with EPUB3 landmarks."""
    display_title = _html_escape(volume_title or 'Table of Contents')
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">',
        '<head>',
        '  <title>Table of Contents</title>',
        '  <link href="style/main.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        '<nav epub:type="toc" id="toc" role="doc-toc">',
        '<h2>Table of Contents</h2>',
    ]
    
    current_level = 0
    stack = []
    for level, text, href in toc_entries:
        # Normalize level to 1-3 range based on relative depth
        # Volume 1 often has [2, 3, 4] as levels.
        # Find the minimum level in toc_entries to use as base
        min_level = min(e[0] for e in toc_entries)
        level = (level - min_level) + 1
        level = max(1, min(level, 3))
        
        if level > current_level:
            for _ in range(level - current_level):
                lines.append('<ol>')
                stack.append('ol')
        elif level < current_level:
            lines.append('</li>')
            stack.pop()
            for _ in range(current_level - level):
                lines.extend(['</ol>', '</li>'])
                stack.pop()
                stack.pop()
        elif current_level > 0:
            lines.append('</li>')
            stack.pop()
        
        display_text = nav_display_title(text)
        lines.append(f'<li><a href="{_html_escape(href)}">{tag_unicode_ranges(_html_escape(display_text))}</a>')
        stack.append('li')
        current_level = level

    while stack:
        lines.append(f'</{stack.pop()}>')

    lines.append('</nav>')
    
    # Landmarks
    lines.append('<nav epub:type="landmarks">\n<h2>Guide</h2>\n<ol>')
    if has_cover:
        lines.append('  <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    lines.append('  <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')
    if has_frontispiece:
        lines.append('  <li><a epub:type="frontispiece" href="frontispiece.xhtml">Frontispiece</a></li>')
    if first_content_href:
        lines.append(f'  <li><a epub:type="bodymatter" href="{first_content_href}">Start of Content</a></li>')
    lines.extend(['</ol>', '</nav>', '</body>', '</html>'])
    
    return '\n'.join(lines)


def build_hierarchical_toc(toc_entries):
    """Convert flat (level, title, href) entries into nested ebooklib structure."""
    if not toc_entries:
        return []
        
    min_level = min(e[0] for e in toc_entries)
    
    def _nest(entries, base_level):
        result = []
        i = 0
        while i < len(entries):
            level, title, href = entries[i]
            # Normalize level
            rel_level = (level - min_level) + 1
            
            if rel_level == base_level:
                # Look ahead for children
                children_entries = []
                j = i + 1
                while j < len(entries):
                    next_level = (entries[j][0] - min_level) + 1
                    if next_level > base_level:
                        children_entries.append(entries[j])
                        j += 1
                    else:
                        break
                
                link = epub.Link(href, title, href.replace('.xhtml', ''))
                if children_entries:
                    result.append((link, _nest(children_entries, base_level + 1)))
                else:
                    result.append(link)
                i = j
            else:
                # Should not happen with well-formed TOC, but skip if it does
                i += 1
        return result

    return _nest(toc_entries, 1)


def generate_ncx(title, uid, toc_entries):
    """Generate NCX for backward compatibility."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
        f'  <head><meta content="{_html_escape(uid)}" name="dtb:uid"/></head>',
        f'  <docTitle><text>{_html_escape(title)}</text></docTitle>',
        '  <navMap>',
    ]
    for i, (level, text, href) in enumerate(toc_entries):
        lines.append(
            f'    <navPoint id="nav_{i}" playOrder="{i+1}">'
            f'<navLabel><text>{_html_escape(text)}</text></navLabel>'
            f'<content src="{_html_escape(href)}"/>'
            f'</navPoint>'
        )
    lines.extend(['  </navMap>', '</ncx>'])
    return '\n'.join(lines)


def repackage_canonical(epub_path, src_dir):
    """Repackage as canonical EPUB3 (mimetype first, no compression).

    Builds the zip in a system temp file, then copies it over the
    destination.  Using a temp-then-copy strategy avoids PermissionError
    on read-only or sandbox-mounted output directories where in-place
    deletion or creation of new files is blocked but overwriting existing
    file bytes (via shutil.copy2) is permitted.
    """
    import tempfile, shutil, subprocess
    fd, tmp_path = tempfile.mkstemp(suffix='.epub')
    os.close(fd)
    os.remove(tmp_path)   # zip must create the file itself; it fails on an empty pre-existing file
    try:
        with open(os.path.join(src_dir, 'mimetype'), 'wb') as f:
            f.write(b'application/epub+zip')
        subprocess.run(['zip', '-0Xq', tmp_path, 'mimetype'],
                       cwd=src_dir, check=True)
        subprocess.run(['zip', '-r9q', tmp_path, '.', '-x',
                        'mimetype', '-x', '*.DS_Store'],
                       cwd=src_dir, check=True)
        # shutil.copy2 overwrites existing files without needing to delete them
        shutil.copy2(tmp_path, epub_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def _add_cover_manifest_properties(tmp_dir):
    """Add properties='cover-image' to the cover manifest item in OPF."""
    import lxml.etree as et
    opf_path = os.path.join(tmp_dir, 'EPUB', 'content.opf')
    if not os.path.exists(opf_path):
        return
    tree = et.parse(opf_path)
    ns = {'opf': 'http://www.idpf.org/2007/opf'}
    manifest = tree.find('.//opf:manifest', ns)
    if manifest is None:
        return
    for item in manifest.findall('opf:item', ns):
        uid = item.get('id', '')
        if uid == 'cover-image':
            props = item.get('properties', '')
            if 'cover-image' not in props:
                item.set('properties', props + ' cover-image' if props else 'cover-image')
    tree.write(opf_path, xml_declaration=True, encoding='UTF-8')


def _inject_apple_books_options(epub_path):
    """Post-process EPUB to add the Apple Books display-options file in META-INF."""
    tmp = epub_path + '.tmp'
    apple_opts_path = 'META-INF/com.apple.ibooks.display-options.xml'
    
    apple_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<display-options xmlns="http://www.apple.com/itunes/vbook/display-options">
  <platform name="*">
    <option name="specified-fonts">true</option>
  </platform>
</display-options>
"""
    
    with zipfile.ZipFile(epub_path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            # Copy all existing items
            for item in zin.infolist():
                if item.filename == apple_opts_path:
                    continue # Will overwrite
                zout.writestr(item, zin.read(item.filename))
            
            # Add Apple options file
            zout.writestr(apple_opts_path, apple_xml)
            
    shutil.move(tmp, epub_path)


def build_endnotes_chapter(footnotes, style_item=None, valid_fnums=None, vol_num=None, trans_notes=None, glossary_notes=None, config=None, biographical_notes=None):
    from scripts.translation_db import FOOTNOTE_TRANSLATIONS
    from render import tag_unicode_ranges
    fn_map = {f.fnum: f for f in footnotes.values()}
    parts = ['<section epub:type="footnotes" role="doc-endnotes" hidden="hidden">']
    for fnum in sorted(fn_map.keys()):
        fn = fn_map[fnum]
        repaired_text = _repair_owen_ocr_errors(fn.text, config=config)
        fn_text = tag_unicode_ranges(_html_escape(repaired_text))
        
        # Look up translation and modernized patristic citation
        trans_key = f"v{vol_num}_fn{fnum}" if vol_num else f"v3_fn{fnum}"
        trans_info = FOOTNOTE_TRANSLATIONS.get(trans_key)
        
        extra_html = ""
        if trans_info:
            extra_html = f'<p class="footnote-modern-translation">{trans_info}</p>'
            
        parts.append(
            f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="fn{fnum}">'
            f'<p class="footnote">'
            f'<span class="fn-link">{fnum}</span> '
            f'{fn_text}'
            f'</p>'
            f'{extra_html}'
            f'</aside>'
        )
        
    if trans_notes:
        parts.append(
            f'<div class="translation-notes-header">'
            f'<h2 class="endnotes-section-title">Modern Translations &amp; Citations</h2>'
            f'<p style="font-size: 0.9em; color: #666; text-align: center; font-style: italic; margin-top: 0.5em;">Translations of Latin, Greek, and Hebrew phrases, and modern academic citations of historical sources.</p>'
            f'</div>'
        )
        for note in trans_notes:
            note_type = note.get('type', 'translation')
            symbol = '†' if note_type == 'translation' else '*'
            parts.append(
                f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="{note["id"]}">'
                f'<p class="footnote">'
                f'<span class="fn-link">{symbol}</span> '
                f'<span class="original-phrase">{tag_unicode_ranges(_html_escape(note["phrase"]))}</span>: '
                f'{note["translation"]}'
                f'</p>'
                f'</aside>'
            )
            
    if glossary_notes:
        parts.append(
            f'<div class="translation-notes-header">'
            f'<h2 class="endnotes-section-title">Theological Glossary</h2>'
            f'<p style="font-size: 0.9em; color: #666; text-align: center; font-style: italic; margin-top: 0.5em;">Definitions of technical theological and historical terms.</p>'
            f'</div>'
        )
        for note in glossary_notes:
            parts.append(
                f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="{note["id"]}">'
                f'<p class="footnote">'
                f'<span class="fn-link">§</span> '
                f'<strong>{note["term"]}</strong>: '
                f'{note["definition"]}'
                f'</p>'
                f'</aside>'
            )

    if biographical_notes:
        parts.append(
            f'<div class="translation-notes-header">'
            f'<h2 class="endnotes-section-title">Biographical Notes</h2>'
            f'<p style="font-size: 0.9em; color: #666; text-align: center; font-style: italic; margin-top: 0.5em;">Brief biographical details of key historical figures.</p>'
            f'</div>'
        )
        for note in biographical_notes:
            parts.append(
                f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="{note["id"]}">'
                f'<p class="footnote">'
                f'<span class="fn-link">‡</span> '
                f'<strong>{note["term"]}</strong>: '
                f'{note["definition"]}'
                f'</p>'
                f'</aside>'
            )

    parts.append('</section>')
    html = ''.join(parts)
    return _make_xhtml('Footnotes', html)


