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
        <span class="colophon-metadata-value">{render._escape_xml(primary_font_name)}</span>
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
    
    subtitle_escaped = render._escape_xml(subtitle)
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
        <span class="colophon-metadata-value">{render._escape_xml(editor)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Publisher:</span>
        <span class="colophon-metadata-value">{render._escape_xml(publisher)}</span>
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
