import re
from html import escape as _html_escape, unescape as _html_unescape
import render
from shared import convert_greek_word, VOLUME_SUBTITLES, clean_greek_text

_AGES_HEADERS = {'THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION',
                 'Books For The Ages', 'AGES Software', 'Version 1.0',
                 'B o o k s F o r T h e A g e s'}

_TITLE_CONNECTORS = {
    'OR', 'OF', 'ON', 'IN', 'WITH', 'ALSO', 'AS ALSO,', 'AND', 'WHEREIN',
    'ARE', 'BY',
}

def _polish_contents_page_html(html: str) -> str:
    """Normalize extracted contents pages into a consistent, reader-friendly TOC."""
    if 'epub:type="toc"' not in html:
        return html

    # Translate known legacy Beta Code in TOC to premium Greek Unicode
    html = html.replace('Qemoci&gt;av Aujtexousiastikh~v SPECIMEN', '<span lang="el" xml:lang="el">Θεομαχίας Αὐτεξουσιαστικῆς</span> Specimen')
    html = html.replace('QEOMACIA ATTEXOUSIASTIKH', '<span lang="el" xml:lang="el">ΘΕΟΜΑΧΙΑ ΑΥΤΕΞΟΥΣΙΑΣΤΙΚΗ</span>')

    html = re.sub(r'<section([^>]*)epub:type="toc"([^>]*)>', '<section class="contents-page" epub:type="toc">', html, count=1)
    seen_volume_title = False

    def _heading_repl(match):
        nonlocal seen_volume_title
        text_html = match.group(1).strip()
        plain = re.sub(r'<br\s*/?>', ' ', text_html, flags=re.I)
        plain = re.sub(r'<[^>]+>', '', plain).strip()
        plain_upper = plain.upper()
        if re.match(r'^CONTENTS\s+OF\s+VOL(?:UME)?\.?\s*\d+', plain_upper) or plain_upper == 'CONTENTS':
            seen_volume_title = True
            return f'<h1 class="contents-volume-title">{text_html}</h1>'
        if re.fullmatch(r'(?:PREFATORY NOTE|PREFACE|PREFACE TO THE READER|ORIGINAL PREFACE|GENERAL PREFACE|TO THE READER|NOTE TO THE READER|ADVERTISEMENT)(?:\s+(?:BY THE EDITOR|TO THE READER|BY D\.?\s+BURGESS))?(?:\s+(?:PREFATORY NOTE|PREFACE|PREFACE TO THE READER|ORIGINAL PREFACE|GENERAL PREFACE|TO THE READER|NOTE TO THE READER|ADVERTISEMENT)(?:\s+(?:BY THE EDITOR|TO THE READER|BY D\.?\s+BURGESS))?)*', plain_upper):
            return f'<p class="contents-frontmatter-line">{text_html}</p>'
        cls = 'contents-treatise-title' if seen_volume_title else 'contents-section-title'
        return f'<h2 class="{cls}">{text_html}</h2>'

    html = re.sub(r'<h[23][^>]*>\s*(.*?)\s*</h[23]>', _heading_repl, html, flags=re.I | re.S)
    html = re.sub(r'<p class="ContentsItem">', '<p class="contents-item">', html)
    html = re.sub(r'<span class="ContentsDescWrap">', '<span class="contents-desc-wrap">', html)

    # Normalize contents-desc starting with ordinals or Roman numerals to contents-item
    def _desc_to_item_repl(m):
        content = m.group(1)
        clean_content = re.sub(r'<[^>]+>', '', content).strip()
        is_ordinal_or_roman = bool(re.match(
            r'^(?:(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)(?:ly)?,?|'
            r'[IVXLCDM]+(?:\s+|\.|$))',
            clean_content,
            re.I
        ))
        if is_ordinal_or_roman:
            return f'<p class="contents-item">{content}</p>'
        return m.group(0)

    html = re.sub(r'<p class="contents-desc">\s*(.*?)\s*</p>', _desc_to_item_repl, html, flags=re.I | re.S)

    item_re = re.compile(r'<p class="contents-item">\s*(.*?)\s*</p>', re.I | re.S)
    rebuilt = []
    cursor = 0
    pending_item = None

    def _plain_contents(inner: str) -> str:
        inner = re.sub(r'<br\s*/?>', ' ', inner, flags=re.I)
        inner = re.sub(r'<[^>]+>', '', inner)
        inner = _html_unescape(inner)
        inner = re.sub(r'\s+', ' ', inner).strip()
        inner = re.sub(r'\b(Chapter|Part|Digression)\s+([0-9IVXLCDM]+)\s+\.', r'\1 \2.', inner, flags=re.I)
        inner = re.sub(r'\b(Chapter|Part|Digression)\s+([0-9IVXLCDM]+)(?=\s+[A-Z])', r'\1 \2.', inner, flags=re.I)
        inner = re.sub(r'\b(\d+)\.\s*—\s*', r'\1. — ', inner)
        inner = re.sub(r'\s+([,.;:])', r'\1', inner)
        return inner

    def _entry_starts(text: str):
        return list(re.finditer(r'(?<!\w)(?:Part|Chapter|Digression)\s+[0-9IVXLCDM]+\.?', text, re.I))

    def _split_entries(text: str) -> list[str]:
        starts = _entry_starts(text)
        if not starts:
            return [text] if text else []
        entries = []
        if starts[0].start() > 0 and text[:starts[0].start()].strip():
            entries.append(text[:starts[0].start()].strip())
        for idx, start in enumerate(starts):
            end = starts[idx + 1].start() if idx + 1 < len(starts) else len(text)
            entries.append(text[start.start():end].strip())
        return [entry for entry in entries if entry]

    def _render_contents_entry(text: str) -> str:
        part = re.fullmatch(r'(Part\s+[0-9IVXLCDM]+\.?)', text, re.I)
        if part:
            label = re.sub(r'\s+\.', '.', part.group(1))
            return f'<h2 class="contents-part-title">{_html_escape(label)}</h2>'

        match = re.match(
            r'(?P<label>'
            r'(?:Chapter|Digression)\s+[0-9IVXLCDM]+\.?|'
            r'[0-9]+\.?\s*—|'
            r'(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)(?:ly)?,?|'
            r'[IVXLCDM]+\.?'
            r')\s*(?P<desc>.*)$',
            text,
            re.I | re.S,
        )
        if match:
            label = re.sub(r'\s+\.', '.', match.group('label').strip())
            label = re.sub(r'\s*—\s*$', ' —', label)
            desc = match.group('desc').strip()
            if desc.startswith('—'):
                desc = desc[1:].strip()
            desc = re.sub(r'\s+', ' ', desc)
            desc = clean_greek_text(desc)
            return (
                f'<p class="contents-item"><span class="contents-label">'
                f'{_html_escape(label)}</span>'
                f'{(" " + render.tag_unicode_ranges(_html_escape(desc))) if desc else ""}</p>'
            )

        if text.upper() == text and len(re.findall(r'[A-Z]', text)) >= 12:
            return f'<h2 class="contents-treatise-title">{render.tag_unicode_ranges(_html_escape(text))}</h2>'

        return f'<p class="contents-item">{render.tag_unicode_ranges(_html_escape(text))}</p>'

    def _flush_pending():
        nonlocal pending_item
        if pending_item is None:
            return ''
        rendered = _render_contents_entry(pending_item)
        pending_item = None
        return rendered

    for match in item_re.finditer(html):
        pending_str = ''
        if re.search(r'<h[1-6]\b', html[cursor:match.start()], re.I):
            pending_str = _flush_pending()
        if pending_str:
            rebuilt.append(pending_str)
        rebuilt.append(html[cursor:match.start()])
        text = _plain_contents(match.group(1))
        entries = _split_entries(text)
        if not entries:
            cursor = match.end()
            continue

        rendered_here = []
        for entry in entries:
            if re.fullmatch(r'Part\s+[0-9IVXLCDM]+\.?', entry, re.I):
                rendered_here.append(_flush_pending())
                rendered_here.append(_render_contents_entry(entry))
                continue
            if _entry_starts(entry):
                rendered_here.append(_flush_pending())
                pending_item = entry
                continue
            if pending_item is not None and re.match(r'^[a-z(]', entry):
                pending_item = pending_item.rstrip() + ' ' + entry
                continue
            rendered_here.append(_flush_pending())
            pending_item = entry
        rebuilt.append(''.join(part for part in rendered_here if part))
        cursor = match.end()

    rebuilt.append(_flush_pending())
    rebuilt.append(html[cursor:])
    return ''.join(rebuilt)


def format_treatise_title_page(page, limit_to_title=False):
    """Build specialized inner treatise title page (e.g. Christologia) with PDF-accurate layout.
    
    Handles:
      - Centered Greek markers
      - Big centered main title
      - Grouped centered sub-elements
      - Grouped italic descriptive blocks
      - Quote block at the bottom
    """
    blocks = page.get_text('dict')['blocks']
    lines_data = []
    
    # 1. Gather lines with metadata
    for b in blocks:
        if b.get('type') != 0: continue
        for line in b['lines']:
            spans = line['spans']
            max_size = max(s['size'] for s in spans)
            text = "".join(s['text'] for s in spans).strip()
            text = re.sub(r'<[0-9A-Fa-f]{6}>', '', text).strip()
            if not text or text.isdigit(): continue
            if any(h in text for h in _AGES_HEADERS): continue
            
            has_koine = any('Koine' in s['font'] for s in spans)
            has_italic = any('Italic' in s['font'] for s in spans)
            has_bold = any('Bold' in s['font'] for s in spans)
            
            lines_data.append({
                'text': text,
                'size': max_size,
                'has_koine': has_koine,
                'has_italic': has_italic,
                'has_bold': has_bold,
                'bbox': line['bbox']
            })

    if not lines_data: return ""

    parts = ['<section class="treatise-title-page" epub:type="titlepage">']
    body_remainder = []
    
    def starts_body_or_chapter(line_text):
        normalized = re.sub(r'\s+', ' ', line_text).strip()
        return bool(re.match(
            r'^(?:CHAPTER\s+\d+\.?|Ques\.?\s+\d+\.|Q\.\s*\d+\.|Ans\.?\s+\d+\.|A\.\s*\d+\.)\b',
            normalized,
            re.I,
        ))

    def looks_like_body_run(index):
        """Detect same-page prose after an inner title without swallowing subtitles."""
        if not limit_to_title or index < 3:
            return False
        sample = lines_data[index:index + 3]
        if len(sample) < 2:
            return False
        current_text = re.sub(r'\s+', ' ', sample[0]['text']).strip()
        current_words = re.findall(r"[A-Za-z']+", current_text)
        current_is_prose = (
            bool(re.search(r'[a-z]', current_text))
            and current_text.upper() != current_text
            and len(current_words) >= 7
            and sample[0]['size'] < 15
        )
        if not current_is_prose:
            return False
        prose_like = 0
        for item in sample:
            item_text = re.sub(r'\s+', ' ', item['text']).strip()
            words = re.findall(r"[A-Za-z']+", item_text)
            has_lower = bool(re.search(r'[a-z]', item_text))
            mostly_caps = item_text.upper() == item_text and len(words) >= 3
            if has_lower and not mostly_caps and len(words) >= 7 and item['size'] < 15:
                prose_like += 1
        return prose_like >= 2

    # 2. Process groups with lookahead for merging
    i = 0
    while i < len(lines_data):
        line = lines_data[i]
        text = line['text']
        y_pos = line['bbox'][1]

        if limit_to_title and (starts_body_or_chapter(text) or looks_like_body_run(i)):
            for item in lines_data[i:]:
                remainder_text = item['text']
                if item['has_koine']:
                    remainder_text = convert_greek_word(remainder_text)
                body_remainder.append(remainder_text)
            break
        
        # Detect Quote block at bottom (usually y > 500 on 792pt page)
        if (text.startswith(('“', '"')) or y_pos > 500) and i >= len(lines_data) - 6:
            quote_lines = []
            while i < len(lines_data):
                l_text = lines_data[i]['text']
                if lines_data[i]['has_koine']:
                    l_text = convert_greek_word(l_text)
                quote_lines.append(_html_escape(l_text))
                i += 1
            full_quote = " ".join(quote_lines)
            parts.append(f'<div class="quote-block">{render.tag_unicode_ranges(full_quote)}</div>')
            break

        # Greek Markers (often used as titles, e.g. ΧΡΙΣΤΟΛΟΓΙΑ)
        if line['has_koine']:
            greek_text = convert_greek_word(text)
            parts.append(f'<h2 class="greek-title"><span lang="el" xml:lang="el">{_html_escape(greek_text)}</span></h2>')
            i += 1
            continue

        # Main Title (Big text)
        if line['size'] > 15 or line['has_bold']:
            cls = 'title-line-major' if line['size'] > 18 else 'title-line-medium'
            parts.append(f'<p class="title-line {cls}">{_html_escape(text)}</p>')
            i += 1
            continue
            
        # Separators (OR, WITH, OF)
        if text.upper() in _TITLE_CONNECTORS:
            parts.append(f'<p class="title-connector">{_html_escape(text)}</p>')
            i += 1
            continue

        # Descriptive/Italic - MERGE CONSECUTIVE LINES
        if line['has_italic']:
            italic_parts = [_html_escape(text)]
            j = i + 1
            while j < len(lines_data):
                next_line = lines_data[j]
                if next_line['has_italic'] and not next_line['has_bold'] and next_line['size'] < 15:
                    italic_parts.append(_html_escape(next_line['text']))
                    j += 1
                else:
                    break
            joined_italic = " ".join(italic_parts)
            parts.append(f'<p class="descriptive">{joined_italic}</p>')
            i = j
            continue

        # Standard descriptive
        parts.append(f'<p class="descriptive">{_html_escape(text)}</p>')
        i += 1

    parts.append('</section>')
    result = "\n".join(parts)
    if body_remainder:
        result += "\n\n" + "\n".join(body_remainder)
    return result


def format_title_page(page, section_class="title-page", epub_type="titlepage", limit_to_title=False):
    """Build Goold-style centered title page XHTML from PDF blocks with premium styling.

    Preserves PDF line breaks with <br/>, maps font-size hierarchy to h1/h2/h3.
    Applies colors and italics based on content heuristics.
    """
    blocks = page.get_text('dict')['blocks']
    lines_data = []
    for b in blocks:
        if b.get('type') != 0:
            continue
        for line in b['lines']:
            spans = line['spans']
            max_size = max(s['size'] for s in spans)
            font_names = [s['font'] for s in spans]
            text = ''.join(s['text'] for s in spans).strip()
            text = re.sub(r'<[0-9A-Fa-f]{6}>', '', text).strip()
            if not text or text.isdigit():
                continue
            if any(h in text for h in _AGES_HEADERS):
                continue
            
            # Stop if we hit a chapter marker and limit_to_title is active
            if limit_to_title and text.upper().startswith('CHAPTER'):
                break
                
            has_koine = any('Koine' in f for f in font_names)
            has_italic = any('Italic' in f for f in font_names)
            has_bold = any('Bold' in f for f in font_names)
            lines_data.append((max_size, has_koine, has_italic, has_bold, text))
        else:
            continue
        break 

    if not lines_data:
        return ''

    # Absolute font thresholds
    h1_threshold = 20.0
    h2_threshold = 15.0

    groups = []
    for size, has_koine, has_italic, has_bold, text in lines_data:
        if has_koine:
            text = convert_greek_word(text)
        safe = _html_escape(text)
        if has_koine:
            safe = f'<span lang="el" xml:lang="el">{safe}</span>'

        # Class heuristics
        cls = ""
        if size >= h1_threshold or (size >= h2_threshold and len(text) < 20):
            lvl = 'h1'
            cls = ' class="primary"'
        elif size >= h2_threshold:
            lvl = 'h2'
            cls = ' class="secondary"'
        elif text.upper() in _TITLE_CONNECTORS:
            lvl = 'p'
            cls = ' class="title-connector"'
        elif len(text) > 40 or has_italic:
            lvl = 'p'
            cls = ' class="descriptive"'
        elif has_bold:
            lvl = 'h3'
        else:
            lvl = 'p'

        if groups and groups[-1][0] == lvl and groups[-1][1] == cls:
            groups[-1][2].append(safe)
        else:
            groups.append((lvl, cls, [safe]))

    parts = [f'<section class="{section_class}" epub:type="{epub_type}">']
    # Add ornament at top
    parts.append('<p class="ornament">❧</p>')
    
    for lvl, cls, texts in groups:
        content = '<br/>'.join(texts)
        parts.append(f'<{lvl}{cls}>{content}</{lvl}>')
    parts.append('</section>')
    return '\n'.join(parts)


def restore_dropped_title_noteref(title_html, chap, vol_num):
    """Restore title-page noterefs that PyMuPDF omits from sparse title pages."""
    if (
        vol_num == 1
        and chap.cid == 'ch025'
        and 'endnotes.xhtml#fn18' not in title_html
        and 'THE GLORY OF CHRIST' in title_html
    ):
        title_html = re.sub(
            r'(THE GLORY OF CHRIST,)',
            lambda m: m.group(1) + render._noteref_link(18),
            title_html,
            count=1,
        )
    return title_html


def build_toc_page_xhtml(pages):
    """Build a formatted CONTENTS page from one or more PDF pages.
    
    Uses block metadata to identify headings vs items and apply styling.
    """
    if not isinstance(pages, list):
        pages = [pages]
        
    parts = ['<section class="contents-page" epub:type="toc">']
    
    for page in pages:
        blocks = page.get_text('dict')['blocks']
        text_blocks = [b for b in blocks if b.get('type') == 0]
        
        for b in text_blocks:
            lines_data = []
            max_size = 0
            has_bold = False
            has_color = False
            
            for line in b['lines']:
                spans = line['spans']
                l_size = max(s['size'] for s in spans)
                max_size = max(max_size, l_size)
                if any(s['flags'] & 2 for s in spans): # 2 is bold
                    has_bold = True
                
                # Check for colors (non-black)
                for s in spans:
                    if s['color'] != 0:
                        has_color = True
                
                l_text = "".join(s['text'] for s in spans).strip()
                l_text = re.sub(r'<[0-9A-Fa-f]{6}>', '', l_text).strip()
                # Skip standalone page numbers
                if l_text.isdigit() and len(l_text) <= 4:
                    continue
                if l_text:
                    lines_data.append(l_text)
            
            if not lines_data:
                continue
                
            full_text = " ".join(lines_data)
            safe_text = "<br/>".join(_html_escape(l) for l in lines_data)
            
            # Heuristics based on John Owen Volume 1 layout
            # 1. Main Titles (Large, usually bold/colored)
            if max_size > 13 or (full_text.isupper() and len(full_text) < 60 and not "CHAPTER" in full_text.upper()):
                if full_text.upper().startswith('CONTENTS OF VOLUME'):
                    parts.append(f'<h1 class="contents-volume-title">{safe_text}</h1>')
                else:
                    parts.append(f'<h2 class="contents-treatise-title">{safe_text}</h2>')
            # 2. Section Headers (PREFATORY NOTE, PREFACE, etc.)
            elif full_text.isupper() and len(full_text) < 40:
                parts.append(f'<p class="contents-frontmatter-line">{safe_text}</p>')
            # 3. TOC Items (CHAPTER 1, 1. -, etc.)
            else:
                # Use .ContentsItem for hanging indent
                # We want to bold the label part if possible
                # Refined regex for labels like "1. —" or "CHAPTER 1."
                match = re.match(r'^((?:CHAPTER\s+\d+|[IVXLC]+\.|[0-9]+[\.\-\s]*[—\-]?)\s*)(.*)', full_text, re.I | re.S)
                if match:
                    label, desc = match.groups()
                    desc_safe = _html_escape(desc.strip())
                    parts.append(f'<p class="contents-item"><b>{_html_escape(label)}</b> {desc_safe}</p>')
                else:
                    continuation = _html_escape(re.sub(r'\s+', ' ', full_text).strip())
                    if (
                        parts
                        and 'class="contents-item"' in parts[-1]
                        and re.search(r'[;—-]\s*</p>$', parts[-1])
                    ):
                        # Sparse TOC style: merge continuation into previous entry
                        parts[-1] = parts[-1].replace('</p>', f' {continuation}</p>')
                    elif continuation:
                        # Analytical TOC style: descriptive paragraph after a heading
                        parts.append(f'<p class="contents-desc">{continuation}</p>')

    parts.append('</section>')
    return '\n'.join(parts)


def generate_copyright_xhtml(vol_num, config, primary_font_name):
    """Generate visual and detailed Publication Metadata (colophon/copyright) page."""
    from scripts.epub_builder import _escape_xml
    publisher = config.get('publisher') or 'Eduardus Ekofius'
    editors = config.get('editors') or ['William H. Goold']
    editor = editors[0] if editors else 'William H. Goold'
    subtitle = VOLUME_SUBTITLES.get(vol_num, '')
    
    ages_info = (
        "The text of this digital edition was originally transcribed and prepared by "
        "<strong>A.G.E.S. Software</strong> (Albany, Oregon) as part of their landmark "
        "<strong>A.G.E.S. Digital Library</strong>, active during the late 1990s and early 2000s. "
        "Their monumental CD-ROM collection, particularly \"The Master Christian Library\" "
        "and \"the digital Owen collection,\" was pioneering in digital theological publishing—preserving "
        "classic, out-of-print Puritan and Reformed literature, making these historic writings "
        "inexpensively accessible to students, ministers, and scholars worldwide."
    )
    
    historical_info = (
        f"This digital volume reproduces the text of the authoritative 16-volume standard edition "
        f"of the <i>Works of John Owen</i>, edited by the Reverend William H. Goold, originally "
        f"published between 1850 and 1853 by Johnstone & Hunter in Edinburgh. The treatises "
        f"and sermons in this volume cover core elements of Reformed and Puritan theology, "
        f"dogmatics, and biblical exposition."
    )
    
    conversion_info = (
        "This EPUB 3.0 publication is the result of a modern agentic conversion pipeline "
        "specifically optimized for high-fidelity rendering on mobile devices, tablets, and e-readers. "
        "It features holistic paragraph healing across page boundaries, automatic language tagging "
        "for Greek and Hebrew Unicode scripts, continuous blockquote styling, easy-tap footnote controls, "
        "and complete typographic consistency tailored for Apple Books."
    )

    fonts_list_html = f"""
    <ul class="colophon-metadata-list">
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Primary Body:</span>
        <span class="colophon-metadata-value">{_escape_xml(primary_font_name)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Greek Script:</span>
        <span class="colophon-metadata-value">SBL Greek / SBL BibLit</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Hebrew Script:</span>
        <span class="colophon-metadata-value">SBL Hebrew / Ezra SIL</span>
      </li>
    </ul>
    """
    
    subtitle_escaped = _escape_xml(subtitle)
    metadata_list_html = f"""
    <ul class="colophon-metadata-list">
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Title:</span>
        <span class="colophon-metadata-value">The Works of John Owen, Volume {vol_num}</span>
      </li>
      {f'<li class="colophon-metadata-item"><span class="colophon-metadata-label">Subtitle:</span><span class="colophon-metadata-value">{subtitle_escaped}</span></li>' if subtitle else ''}
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Author:</span>
        <span class="colophon-metadata-value">John Owen (1616–1683)</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Editor:</span>
        <span class="colophon-metadata-value">{_escape_xml(editor)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Publisher:</span>
        <span class="colophon-metadata-value">{_escape_xml(publisher)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Release Year:</span>
        <span class="colophon-metadata-value">2026</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Format:</span>
        <span class="colophon-metadata-value">EPUB 3.0 (Digital Edition)</span>
      </li>
    </ul>
    """

    html = f"""<section class="colophon-page" epub:type="colophon">
  <h1 class="colophon-title">Publication Metadata</h1>
  
  <p class="colophon-ornament">❧</p>
  
  <div class="colophon-section">
    <h2 class="colophon-section-title">Edition Details</h2>
    {metadata_list_html}
  </div>
  
  <div class="colophon-section">
    <h2 class="colophon-section-title">Theological Glossary &amp; Biographical Notes</h2>
    <p class="colophon-text">
      Throughout the text of this volume, archaic theological or historical terms (e.g., <i>Socinians</i>, <i>Pelagians</i>, <i>Sublapsarian</i>) are marked with a section sign (<sup>§</sup>), and key historical figures (e.g., <i>Calvin</i>, <i>Cyril</i>, <i>Charnock</i>) are marked with a double dagger (<sup>‡</sup>) upon their first occurrence in the book. Tapping these symbols opens contextual definitions and brief biographical details in a pop-up footnote.
    </p>
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Historical Source</h2>
    <p>{historical_info}</p>
    <p>{ages_info}</p>
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Typography &amp; Fonts</h2>
    <p>This volume is styled with a premium collection of typography designed specifically for legibility and aesthetic excellence on narrow screens and e-ink displays. The following fonts are embedded or referenced within this package:</p>
    {fonts_list_html}
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Scholarly Footnote Architecture</h2>
    <p>This digital edition features a five-track footnote architecture designed for high readability and premium scholarly utility:</p>
    <ul>
      <li><strong>Original Historical Footnotes <code>1, 2, ...</code></strong>: Original historical footnotes remain intact, numbered sequentially. Where these footnotes contain untranslated Greek/Latin quotes or abbreviated patristic references, a dedicated modernization block has been appended directly beneath them showing full modern translations and standard academic source citations.</li>
      <li><strong>Word Translation Footnotes <code>†</code></strong>: Indicated by a superscript dagger, these represent modern editorial translations of foreign-language words and phrases (Latin, Greek, and Hebrew) appearing in the main text. They are kept entirely distinct from the original historical footnotes.</li>
      <li><strong>Reference &amp; Citation Footnotes <code>*</code></strong>: Indicated by a superscript asterisk, these provide modern academic citations for inline patristic, classical, or scholastic references.</li>
      <li><strong>Theological Glossary <code>§</code></strong>: Indicated by a superscript section sign, these provide brief, contextual definitions of technical theological and historical terms upon their first mention in the book.</li>
      <li><strong>Biographical Notes <code>‡</code></strong>: Indicated by a superscript double dagger, these provide brief biographical details for key historical figures upon their first mention in the book.</li>
    </ul>
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Conversion Technology</h2>
    <p>{conversion_info}</p>
  </div>
</section>"""
    return html


def _init_render_paths_and_json(vol_num: int, overrides: dict = None, intermediate: dict = None):
    """Initialize paths, merge configuration, and load/repair intermediate JSON data."""
    import json
    from shared import merge_volume_config
    from scripts.analysis_parser import _repair_analysis_spillover_chapters
    from render import _repair_owen_ocr_errors, _RENDER_DIR
    
    config = merge_volume_config(vol_num, overrides)
    
    vol_dir = _RENDER_DIR / 'volumes' / f'v{vol_num}'
    json_path = vol_dir / 'intermediate' / f'volume_{vol_num}.json'
    out_dir = vol_dir / 'output'
    out_dir.mkdir(parents=True, exist_ok=True)
    epub_path = str(out_dir / f'volume_{vol_num}.epub')
    
    if intermediate is None:
        with open(json_path, encoding='utf-8') as f:
            intermediate = json.load(f)
            
    intermediate = _repair_analysis_spillover_chapters(intermediate)
    for ch in intermediate.get('chapters', []):
        if 'title' in ch:
            ch['title'] = _repair_owen_ocr_errors(ch['title'], config=config)
            
    return config, epub_path, intermediate


def _setup_epub_book(vol_num: int, config: dict, title: str):
    """Set up the EpubBook object and apply metadata."""
    import uuid
    from ebooklib import epub
    
    book = epub.EpubBook()
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-works-vol-{vol_num}'))
    book.set_identifier(uid)
    book.set_title(title)
    book.set_language('en')
    book.add_author(config.get('authors', ['John Owen'])[0])
    for ed in config.get('editors', []):
        book.add_metadata('DC', 'contributor', ed, {'role': 'edt', 'id': 'editor'})
    book.add_metadata('DC', 'publisher', config.get('publisher', ''))
    book.add_metadata('DC', 'rights', 'Public Domain')
    return book, uid


def _inject_fonts_and_css(book, config: dict):
    """Generate stylesheet and copy font assets into the EPUB book."""
    import os
    from ebooklib import epub
    from render import _RENDER_DIR
    from shared import (
        EPUB_STYLESHEET, generate_font_styles, select_primary_font,
        SBL_SUPPLEMENTS, EZRA_SIL_FILES, TITLE_PAGE_FONTS, GFS_PORSON_FILES,
        PROXIMA_NOVA_FILES, CARDO_FILES, GENTIUM_PLUS_FILES,
    )
    
    body_font_name = config.get('body_font', 'SBL_BLit')
    primary_font = select_primary_font(body_font_name)
    font_css = generate_font_styles(primary_font['name'], primary_font['files'])
    extra_css = config.get('extra_css', '')
    full_css = EPUB_STYLESHEET + '\n' + font_css
    if extra_css:
        full_css += '\n' + extra_css
        
    style_item = epub.EpubItem(
        uid='style', file_name='style/main.css',
        media_type='text/css', content=full_css.encode('utf-8'),
    )
    book.add_item(style_item)
    
    font_fnames = set()
    font_base = os.path.join(_RENDER_DIR, 'fonts')
    
    def _font_media_type(filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.otf': return 'font/otf'
        if ext == '.ttf': return 'font/ttf'
        if ext == '.woff': return 'font/woff'
        if ext == '.woff2': return 'font/woff2'
        return 'application/font-sfnt'
        
    # Primary font files
    for _variant, _rel_path in primary_font.get('files', {}).items():
        _fbase = os.path.basename(_rel_path)
        if _fbase in font_fnames:
            continue
        _src = os.path.join(font_base, _rel_path)
        if os.path.exists(_src):
            book.add_item(epub.EpubItem(
                uid=f'f_{_fbase.replace(".","_")}',
                file_name=f'Fonts/{_fbase}', media_type=_font_media_type(_fbase),
                content=open(_src, 'rb').read(),
            ))
            font_fnames.add(_fbase)
            
    # Supplemental fonts
    for _font_dict in (SBL_SUPPLEMENTS, EZRA_SIL_FILES, PROXIMA_NOVA_FILES, TITLE_PAGE_FONTS, GFS_PORSON_FILES, CARDO_FILES, GENTIUM_PLUS_FILES):
        for _fname, _fpath in _font_dict.items():
            _fbase = os.path.basename(_fpath)
            if _fbase in font_fnames:
                continue
            _src = os.path.join(font_base, _fpath)
            if os.path.exists(_src):
                book.add_item(epub.EpubItem(
                    uid=f'f_{_fbase.replace(".","_")}',
                    file_name=f'Fonts/{_fbase}',
                    media_type=_font_media_type(_fbase),
                    content=open(_src, 'rb').read(),
                ))
                font_fnames.add(_fbase)
                
    return style_item, primary_font


def _add_cover_and_portrait(book, vol_num: int, style_item):
    """Add cover image, cover XHTML page, portrait, and emblem assets if present."""
    import os
    from ebooklib import epub
    from render import _RENDER_DIR, find_cover, find_portrait
    from scripts.epub_builder import _make_xhtml, generate_frontispiece_xhtml
    
    cover_path = find_cover(vol_num)
    cover_page = None
    cover_item = None
    if cover_path and os.path.exists(cover_path):
        ext = os.path.splitext(cover_path)[1].lower()
        mt = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
        with open(cover_path, 'rb') as f:
            cover_item = epub.EpubItem(
                uid='cover-image', file_name=f'images/cover{ext}',
                media_type=mt, content=f.read(),
            )
        book.add_item(cover_item)
        book.add_metadata(None, 'meta', '', {'name': 'cover', 'content': 'cover-image'})
        
        cover_page = epub.EpubHtml(title='Cover', file_name='cover.xhtml', lang='en')
        cover_html = f'<div class="cover"><img src="images/cover{ext}" alt="Cover"/></div>'
        cover_page.set_content(_make_xhtml('Cover', cover_html).encode('utf-8'))
        book.add_item(cover_page)
        
    portrait_path = find_portrait(vol_num)
    frontispiece_item = None
    if portrait_path and os.path.exists(portrait_path):
        ext = os.path.splitext(portrait_path)[1].lower()
        mt = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
        port_fn = f'images/portrait{ext}'
        with open(portrait_path, 'rb') as f:
            port_item = epub.EpubItem(file_name=port_fn, media_type=mt, content=f.read())
        book.add_item(port_item)
        
        fi_html = generate_frontispiece_xhtml(os.path.basename(port_fn))
        frontispiece_item = epub.EpubHtml(
            title='Frontispiece', file_name='frontispiece.xhtml', lang='en',
        )
        frontispiece_item.set_content(
            _make_xhtml('Frontispiece', fi_html).encode('utf-8')
        )
        frontispiece_item.add_item(style_item)
        book.add_item(frontispiece_item)
        
    emblem_path = _RENDER_DIR / 'covers' / 'emblem_seal.png'
    if emblem_path.exists():
        with open(emblem_path, 'rb') as f:
            emblem_item = epub.EpubItem(
                file_name='images/emblem_seal.png',
                media_type='image/png',
                content=f.read()
            )
        book.add_item(emblem_item)
        
    return cover_page, frontispiece_item, cover_item


def _add_front_matter(book, vol_num: int, config: dict, primary_font: dict, style_item, intermediate: dict):
    """Add PDF-extracted front matter items (title page, copyright, TOC, formatting/abbreviation guides)."""
    from ebooklib import epub
    from scripts.epub_builder import (
        _make_xhtml, _polish_volume_title_page_html, _polish_treatise_title_page_html,
        generate_frontispiece_xhtml,
    )
    from render import (
        generate_structural_guide_html, generate_abbreviations_guide_html
    )
    
    front_matter_epub_items = []
    _last_fm_title = None
    copyright_added = False
    added_structural_guide = False
    added_abbreviations_guide = False
    
    for fm in intermediate.get('front_matter_items', []):
        if fm['title'] == _last_fm_title:
            continue
        _last_fm_title = fm['title']
        
        fm_item = epub.EpubHtml(
            title=fm['title'], file_name=fm['file_name'], lang='en',
        )
        fm_html = fm['html']
        if fm_html is None:
            continue
            
        fm_overrides = config.get('front_matter_overrides', {})
        if fm['title'] in fm_overrides:
            fm_html = fm_overrides[fm['title']]
        elif fm.get('type') == 'title_page':
            fm_html = _polish_volume_title_page_html(fm_html, vol_num, config)
        elif fm.get('type') == 'treatise_title_page':
            fm_html = _polish_treatise_title_page_html(fm_html)
        elif fm.get('type') == 'toc':
            toc_override = config.get('contents_page_overrides')
            if toc_override:
                fm_html = toc_override
            else:
                fm_html = _polish_contents_page_html(fm_html)
                
        if fm.get('type') == 'toc' and fm.get('file_name', '').startswith('contents_'):
            fm['title'] = 'Original Printed Contents'
            
        fm_item.set_content(
            _make_xhtml(fm['title'], fm_html).encode('utf-8')
        )
        fm_item.add_item(style_item)
        book.add_item(fm_item)
        front_matter_epub_items.append(fm_item)
        
        if fm.get('type') == 'title_page' and not copyright_added:
            cop_title = 'Publication Metadata'
            cop_fn = 'colophon.xhtml'
            cop_html = generate_copyright_xhtml(vol_num, config, primary_font['name'])
            cop_item = epub.EpubHtml(title=cop_title, file_name=cop_fn, lang='en')
            cop_item.set_content(_make_xhtml(cop_title, cop_html).encode('utf-8'))
            cop_item.add_item(style_item)
            book.add_item(cop_item)
            front_matter_epub_items.append(cop_item)
            copyright_added = True
            
        if fm.get('type') == 'toc' and not added_structural_guide:
            note_item = epub.EpubHtml(title='Note on Structural Formatting', file_name='structural_guide.xhtml', lang='en')
            note_html = generate_structural_guide_html(vol_num)
            note_item.set_content(_make_xhtml('Note on Structural Formatting', note_html).encode('utf-8'))
            note_item.add_item(style_item)
            book.add_item(note_item)
            front_matter_epub_items.append(note_item)
            added_structural_guide = True
            
        if fm.get('type') == 'toc' and not added_abbreviations_guide:
            abbr_item = epub.EpubHtml(title='Abbreviations & Scholarly Citations', file_name='abbreviations_guide.xhtml', lang='en')
            abbr_html = generate_abbreviations_guide_html(vol_num)
            abbr_item.set_content(_make_xhtml('Abbreviations & Scholarly Citations', abbr_html).encode('utf-8'))
            abbr_item.add_item(style_item)
            book.add_item(abbr_item)
            front_matter_epub_items.append(abbr_item)
            added_abbreviations_guide = True
            
    if not added_structural_guide:
        note_item = epub.EpubHtml(title='Note on Structural Formatting', file_name='structural_guide.xhtml', lang='en')
        note_html = generate_structural_guide_html(vol_num)
        note_item.set_content(_make_xhtml('Note on Structural Formatting', note_html).encode('utf-8'))
        note_item.add_item(style_item)
        book.add_item(note_item)
        front_matter_epub_items.append(note_item)
        
    if not added_abbreviations_guide:
        abbr_item = epub.EpubHtml(title='Abbreviations & Scholarly Citations', file_name='abbreviations_guide.xhtml', lang='en')
        abbr_html = generate_abbreviations_guide_html(vol_num)
        abbr_item.set_content(_make_xhtml('Abbreviations & Scholarly Citations', abbr_html).encode('utf-8'))
        abbr_item.add_item(style_item)
        book.add_item(abbr_item)
        front_matter_epub_items.append(abbr_item)
        
    if not copyright_added:
        cop_title = 'Publication Metadata'
        cop_fn = 'colophon.xhtml'
        cop_html = generate_copyright_xhtml(vol_num, config, primary_font['name'])
        cop_item = epub.EpubHtml(title=cop_title, file_name=cop_fn, lang='en')
        cop_item.set_content(_make_xhtml(cop_title, cop_html).encode('utf-8'))
        cop_item.add_item(style_item)
        book.add_item(cop_item)
        front_matter_epub_items.append(cop_item)
        
    return front_matter_epub_items


def _render_single_chapter(
    ch_dict: dict,
    config: dict,
    conv_mode: str,
    conv_drop_cap: bool,
    conv_fm_style: str,
    style_item,
    book,
    seen_body_translations: set,
    seen_glossary_terms: set,
    seen_biographical_terms: set,
    all_translation_notes: list,
    all_glossary_notes: list,
    all_biographical_notes: list
):
    """Processes, scans/tags, and builds the XHTML file for a single chapter."""
    import re
    import html
    from ebooklib import epub
    from shared import SCRIPTURE_BOOK_RE
    from render import (
        markdown_to_html, _split_raw_title_body, _foreign_fragments_in_section,
        _merge_titlepage_override, _prepare_analysis_raw_text, apply_inline_translations,
        replace_first_outside_tags_and_comments
    )
    from scripts.analysis_parser import _polish_analysis_html
    from scripts.scholastic_parser import apply_scholastic_anchor_protocol
    from scripts.polish import _apply_premium_signatures, _apply_premium_chapter_endings, _apply_premium_salutations
    from scripts.epub_builder import _make_xhtml
    
    title_upper = ch_dict['title'].upper()
    
    if any(kw in title_upper for kw in ['ANALYSIS', 'PREFATORY NOTE', 'PREFACE', 'CONTENTS']):
        conv_mode = 'FRONT_MATTER'
        conv_drop_cap = False
        conv_fm_style = 'prose'
    elif ch_dict.get('is_treatise'):
        conv_mode = 'BODY_START'
        conv_drop_cap = True
        conv_fm_style = 'blurb'
    elif re.search(r'\bCHAPTER\s+\d+\b|\bSERMON\s+\d+\b|\bDISCOURSE\s+\d+\b', title_upper):
        if conv_mode == 'FRONT_MATTER':
            conv_mode = 'BODY_START'
            conv_drop_cap = True
        conv_fm_style = 'blurb'
        
    raw_text = ch_dict.get('raw_text', '')
    titlepage_override = config.get('treatise_title_overrides', {}).get(ch_dict['title'])
    if titlepage_override:
        title_block, body_text = _split_raw_title_body(raw_text)
        foreign_frags = _foreign_fragments_in_section(title_block or raw_text)
        overridden_title = _merge_titlepage_override(titlepage_override, foreign_frags)
        if body_text:
            raw_text = f"{overridden_title}\n\n{body_text}"
        else:
            raw_text = overridden_title
            
    if not raw_text:
        return None, None, conv_mode, conv_drop_cap, conv_fm_style
        
    if 'ANALYSIS' in title_upper:
        raw_text = _prepare_analysis_raw_text(raw_text)
        
    part_match = re.search(r'\bPart\s+([0-9IVXLCDM]+)\b', ch_dict.get('title', ''), re.I)
    if (
        ch_dict.get('is_treatise')
        and part_match
        and not re.search(r'\[\[PART\]\]|\bPART\s+[0-9IVXLCDM]+\.?', raw_text[:400], re.I)
    ):
        raw_text = f'[[PART]] PART {part_match.group(1)}.\n\n{raw_text}'
        
    _chapter_num_match = re.match(r'^Chapter\s+(\d+)\b', ch_dict.get('title', ''), re.I)
    if (
        _chapter_num_match
        and not re.search(r'\[\[CHAPTER\]\]', raw_text[:200])
        and not re.search(r'\[\[PART\]\]', raw_text[:200])
        and not ch_dict.get('is_treatise')
    ):
        _ch_num = _chapter_num_match.group(1)
        raw_text = f'[[CHAPTER]] CHAPTER {_ch_num}.\n\n{raw_text}'
        
    in_catechism_context = (
        'CATECHISM' in title_upper
        or bool(re.search(r'^\s*(?:Q\.|Ques\.\s*\d|Ans\.\s*[A-Z])', raw_text[:3000], re.MULTILINE))
    )
    
    chapter_config = {
        **config,
        'is_catechism_context': in_catechism_context,
        'chapter_title': ch_dict.get('title'),
    }
    
    body_html, conv_mode, conv_drop_cap = markdown_to_html(
        raw_text,
        current_mode=conv_mode,
        pending_drop_cap=conv_drop_cap,
        front_matter_style=conv_fm_style,
        config=chapter_config
    )
    
    if 'ANALYSIS' in title_upper:
        body_html = _polish_analysis_html(body_html)
        
    body_html = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', body_html, flags=re.I)
    body_html = apply_scholastic_anchor_protocol(body_html)
    
    html_postprocess_hook = config.get('html_postprocess_hook')
    if html_postprocess_hook:
        ch_context = {**ch_dict, 'is_catechism_context': in_catechism_context}
        body_html = html_postprocess_hook(body_html, ch_context)
        
    body_html = _apply_premium_signatures(body_html, ch_dict.get('title', ''))
    body_html = _apply_premium_chapter_endings(body_html)
    body_html = _apply_premium_salutations(body_html)
    
    inline_replacements = config.get('inline_html_replacements', {})
    if inline_replacements:
        for old, new in inline_replacements.items():
            body_html = body_html.replace(old, new)
            
    if not body_html.strip():
        return None, None, conv_mode, conv_drop_cap, conv_fm_style
        
    body_html = apply_inline_translations(body_html)
    
    from scripts.translation_db import BODY_TRANSLATIONS
    from scripts.patristic_refs import expand_inline_citations
    
    sorted_phrases = sorted(BODY_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    local_notes = []
    placeholders = {}
    placeholder_counter = 0
    trans_counter = 0
    cid = ch_dict['cid']
    
    def clean_and_map(orig_str):
        stripped_chars = []
        map_to_orig = []
        i = 0
        n = len(orig_str)
        while i < n:
            if orig_str[i] == '<':
                while i < n and orig_str[i] != '>': i += 1
                i += 1
            elif orig_str[i] == '&':
                j = i + 1
                while j < n and orig_str[j] != ';' and (j - i) < 10: j += 1
                if j < n and orig_str[j] == ';':
                    entity = orig_str[i:j+1]
                    decoded = html.unescape(entity)
                    for char in decoded:
                        stripped_chars.append(char)
                        map_to_orig.append(i)
                    i = j + 1
                else:
                    stripped_chars.append(orig_str[i])
                    map_to_orig.append(i)
                    i += 1
            else:
                stripped_chars.append(orig_str[i])
                map_to_orig.append(i)
                i += 1
        return "".join(stripped_chars), map_to_orig
        
    def make_quote_agnostic(phrase):
        words = phrase.split()
        escaped_words = []
        for w in words:
            escaped = re.escape(w)
            escaped = escaped.replace(r"\'", "'").replace("'", r"['’‘]")
            escaped = escaped.replace(r'\"', '"').replace('"', r'["“”]')
            escaped_words.append(escaped)
        return r'\s+'.join(escaped_words)
        
    clean_text, mapping = clean_and_map(body_html)
    dirty = False
    
    for phrase, trans in sorted_phrases:
        if phrase in seen_body_translations:
            continue
            
        if dirty:
            clean_text, mapping = clean_and_map(body_html)
            dirty = False
            
        first_char = phrase[0]
        last_char = phrase[-1]
        lb = ""
        la = ""
        if '\u0590' <= first_char <= '\u05ff':
            lb = r'(?<![\u0590-\u05ff־-])'
        elif ('\u0370' <= first_char <= '\u03ff' or '\u1f00' <= first_char <= '\u1fff'):
            lb = r'(?<![\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f־-])'
        elif first_char.isalnum():
            lb = r'(?<![a-zA-Z0-9\u0300-\u036f])'
            
        if '\u0590' <= last_char <= '\u05ff':
            la = r'(?![\u0590-\u05ff־-])'
        elif ('\u0370' <= last_char <= '\u03ff' or '\u1f00' <= last_char <= '\u1fff'):
            la = r'(?![\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f־-])'
        elif last_char.isalnum():
            la = r'(?![a-zA-Z0-9\u0300-\u036f])'
            
        phrase_regex = make_quote_agnostic(phrase)
        pattern = re.compile(rf'{lb}{phrase_regex}{la}', re.I)
        
        match = pattern.search(clean_text)
        if match:
            start_idx = match.start()
            end_idx = match.end()
            orig_start = mapping[start_idx]
            orig_end = mapping[end_idx] if end_idx < len(mapping) else len(body_html)
            
            punc_match = re.match(r'^((?:</[a-zA-Z]+>)*)([\.,\?!:;\'"“”’]*)', body_html[orig_end:])
            if punc_match:
                trailing_tags = punc_match.group(1)
                trailing_punc = punc_match.group(2)
            else:
                trailing_tags = ""
                trailing_punc = ""
            orig_end_with_punc = orig_end + len(trailing_tags) + len(trailing_punc)
            
            matched_str = body_html[orig_start:orig_end]
            trans_counter += 1
            placeholder_counter += 1
            
            fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{trans_counter}">†</a></sup>'
            local_notes.append({
                'id': f"fntrans_{cid}_{trans_counter}",
                'num': trans_counter,
                'phrase': phrase,
                'translation': trans,
                'type': 'translation'
            })
            
            placeholder_key = f"__BODY_TRANS_PH_{placeholder_counter}__"
            placeholders[placeholder_key] = (matched_str, trailing_tags, trailing_punc, fn_link)
            replacement = placeholder_key
            body_html = body_html[:orig_start] + replacement + body_html[orig_end_with_punc:]
            seen_body_translations.add(phrase)
            dirty = True
            
    body_html, citation_notes, trans_counter = expand_inline_citations(
        body_html,
        cid=cid,
        trans_notes=local_notes,
        trans_counter=trans_counter
    )
    
    if local_notes:
        all_translation_notes.extend(local_notes)
        
    from scripts.technical_glossary import apply_glossary_footnotes
    body_html, local_glossary, seen_glossary_terms = apply_glossary_footnotes(
        body_html, cid, seen_glossary_terms, replace_first_outside_tags_and_comments
    )
    if local_glossary:
        all_glossary_notes.extend(local_glossary)
        
    from scripts.biography_db import BIOGRAPHICAL_DB
    local_biographical = []
    biographical_counter = 0
    sorted_biog_terms = sorted(BIOGRAPHICAL_DB.items(), key=lambda x: len(x[0]), reverse=True)
    for term, definition in sorted_biog_terms:
        if term in seen_biographical_terms:
            continue
            
        pattern = re.compile(
            rf'(?<![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
            rf'({re.escape(term)}(?:s|es)?)'
            rf'(?![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
            rf'((?:</[a-zA-Z]+>)*)'
            rf'([\.,\?!:;\'"“”’]*)',
            re.I
        )
        def replace_biographical(m):
            nonlocal biographical_counter
            biographical_counter += 1
            matched_str = m.group(1)
            trailing_tags = m.group(2)
            trailing_punc = m.group(3)
            fn_link = f'<sup><a class="noteref noteref-biographical" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fnbiog_{cid}_{biographical_counter}">‡</a></sup>'
            local_biographical.append({
                'id': f"fnbiog_{cid}_{biographical_counter}",
                'term': term,
                'definition': definition
            })
            return f"{matched_str}{trailing_tags}{trailing_punc}{fn_link}"
            
        body_html, replaced = replace_first_outside_tags_and_comments(body_html, pattern, replace_biographical)
        if replaced:
            seen_biographical_terms.add(term)
            
    if local_biographical:
        all_biographical_notes.extend(local_biographical)
        
    for ph_key, (matched_str, trailing_tags, trailing_punc, fn_link) in placeholders.items():
        body_html = body_html.replace(ph_key, f"{matched_str}{trailing_tags}{trailing_punc}{fn_link}")
        
    body = f'<section>{body_html}</section>'
    ch_item = epub.EpubHtml(title=ch_dict['title'], file_name=f'{cid}.xhtml', lang='en')
    ch_item.set_content(_make_xhtml(ch_dict['title'], body).encode('utf-8'))
    ch_item.add_item(style_item)
    book.add_item(ch_item)
    
    toc_entry = (ch_dict['level'], ch_dict['title'], f'{cid}.xhtml')
    return ch_item, toc_entry, conv_mode, conv_drop_cap, conv_fm_style


def _finalize_epub_and_write(
    book,
    vol_num: int,
    epub_path: str,
    uid: str,
    epub_chapters: list,
    front_matter_epub_items: list,
    cover_page,
    frontispiece_item,
    endnotes_item,
    toc_entries: list,
    intermediate: dict,
    cover_item
):
    """Write EPUB to disk, construct navigation indices, and repackage canonically."""
    import os
    import tempfile as _tempfile
    import zipfile as _zf
    from ebooklib import epub
    from scripts.epub_builder import (
        generate_nav_xhtml, build_hierarchical_toc,
        _add_cover_manifest_properties, repackage_canonical, _inject_apple_books_options
    )
    
    _nav_seen_titles = set()
    _nav_seen_files = set()
    _nav_prefix = []
    if cover_page:
        _nav_prefix.append((1, 'Cover', 'cover.xhtml'))
        _nav_seen_titles.add('Cover')
        _nav_seen_files.add('cover.xhtml')
        
    for _fm in intermediate.get('front_matter_items', []):
        _fm_title = _fm.get('title', '')
        _fm_html = _fm.get('html')
        _fm_fn = _fm.get('file_name', '')
        if _fm_html is None:
            continue
        if _fm_title and _fm_title not in _nav_seen_titles and _fm_fn not in _nav_seen_files:
            _nav_prefix.append((1, _fm_title, _fm_fn))
            _nav_seen_titles.add(_fm_title)
            _nav_seen_files.add(_fm_fn)
            
    for _fm_item in front_matter_epub_items:
        _fmt = getattr(_fm_item, 'title', None) or ''
        _fmf = getattr(_fm_item, 'file_name', None) or ''
        if _fmt and _fmt not in _nav_seen_titles and _fmf and _fmf not in _nav_seen_files:
            _nav_prefix.append((1, _fmt, _fmf))
            _nav_seen_titles.add(_fmt)
            _nav_seen_files.add(_fmf)
            
    nav_entries = _nav_prefix + toc_entries
    
    style_item = book.get_item_with_id('style')
    nav_html = generate_nav_xhtml(
        nav_entries,
        volume_title=intermediate['title'],
        has_cover=cover_item is not None,
        has_frontispiece=frontispiece_item is not None,
        first_content_href=epub_chapters[0].file_name if epub_chapters else None,
    )
    nav_item = epub.EpubHtml(title='Table of Contents', file_name='nav.xhtml', media_type='application/xhtml+xml', lang='en')
    nav_item.properties = ['nav']
    nav_item.set_content(nav_html.encode('utf-8'))
    if style_item:
        nav_item.add_item(style_item)
    book.add_item(nav_item)
    
    book.toc = build_hierarchical_toc(nav_entries)
    
    ncx = epub.EpubNcx()
    book.add_item(ncx)
    
    spine = []
    if cover_page:
        spine.append(cover_page)
    spine.extend(front_matter_epub_items)
    spine.append(nav_item)
    if frontispiece_item:
        spine.append(frontispiece_item)
    spine += epub_chapters
    if endnotes_item:
        spine.append(endnotes_item)
    book.spine = spine
    
    temp_epub = epub_path + '.tmp_build'
    epub.write_epub(temp_epub, book)
    with _tempfile.TemporaryDirectory() as tmp:
        with _zf.ZipFile(temp_epub, 'r') as z:
            z.extractall(tmp)
        _add_cover_manifest_properties(tmp)
        repackage_canonical(epub_path, tmp)
        
    if os.path.exists(temp_epub):
        try:
            os.remove(temp_epub)
        except OSError:
            pass
            
    _inject_apple_books_options(epub_path)
    return epub_path

