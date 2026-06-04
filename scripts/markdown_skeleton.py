import re
from shared import (
    ROMAN_HEADING_RE, ROMAN_ONLY_RE, FOOTNOTE_MARKER_RE,
    clean_greek_text, is_greek_font, is_hebrew_font,
    convert_greek_word, convert_gideon_hebrew,
    contains_greek, contains_hebrew
)
from scripts.pdf_coordinates import (
    coordinate_redactor, _compute_page_text_bounds, _text_block_lines,
    _text_block_is_blockquote, page_has_blockquote_geometry,
    _page_starts_with_blockquote_continuation, _flush_blockquote_lines,
    _append_blockquote_aware, _join_blockquote_lines, _quote_run_is_open,
    _quote_run_expects_reference_tail, convert_span_text,
    _line_text_from_spans
)
from scripts.ages_verse_translator import _has_repeated_ages_marker_cluster
PAGE_H = 626

COLOR_BLUE = 212
COLOR_GREEN = 25617
COLOR_RED = 8388608


# ================================================================
# STAGE 3: Font-Aware Text Extraction + Greek/Hebrew Conversion
# ================================================================

def page_has_special_fonts(page):
    """Check if a PyMuPDF page contains Greek/Hebrew font or Unicode spans."""
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            for span in line['spans']:
                font = span.get('font', '')
                text = span.get('text', '')
                if is_greek_font(font) or contains_greek(text):
                    return 'greek'
                if is_hebrew_font(font) or contains_hebrew(text):
                    return 'hebrew'
    return None


def page_is_structural(page):
    """Check if a page contains Blue/Green/Red structural headings or Digressions."""
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            line_text = "".join(s['text'] for s in line['spans']).strip()
            for span in line['spans']:
                color = span.get('color', 0)
                size = span.get('size', 0)
                flags = span.get('flags', 0)
                # Parts (Blue > 20), Chapters (Green > 15), Volumes (Red > 15)
                if (color == COLOR_BLUE and size > 20) or \
                   (color == COLOR_GREEN and size > 15) or \
                   (color == COLOR_RED and size > 15):
                    return True
                # Digressions (Bold black starting with DIGRESSION)
                if color == 0 and size == 12 and (flags & 16) and line_text.startswith('DIGRESSION'):
                    return True
            
            # Roman Heads (Issue 1)
            if ROMAN_HEADING_RE.match(line_text) or ROMAN_ONLY_RE.match(line_text):
                return True
    return False


def extract_structural_page(page, page_height=PAGE_H):
    """
    Robust extraction for pages with structural elements (Part/Chapter starts).
    Groups same-type lines to avoid fragmentation and uses explicit tokens.
    """
    blocks = page.get_text('dict')['blocks']
    blocks = coordinate_redactor(blocks, page_height)
    body_left, body_right = _compute_page_text_bounds(blocks)
    
    output_lines = []
    current_kind = None
    current_text_parts = []
    pending_blockquote_lines = []
    in_heading_section = True
    waiting_for_summary = False  # Track if we just hit a CHAPTER (Issue 108/Audit)

    def flush():
        nonlocal current_kind, current_text_parts
        if not current_text_parts:
            return
            
        # Join major structural elements with space to keep them unified (Issue 108/Audit)
        if current_kind in ('PART', 'CHAPTER', 'SUMMARY', 'SUBTITLE', 'DIGRESSION', 'ROMAN_HEAD'):
            joined = ' '.join(current_text_parts).strip()
        else:
            joined = '\n'.join(current_text_parts).strip()
            
        if not joined:
            return
        if current_kind and current_kind != 'PLAIN':
            output_lines.append(f"[[{current_kind}]] {joined}")
        else:
            output_lines.append(joined)
        current_text_parts = []

    def flush_blockquote():
        nonlocal pending_blockquote_lines
        pending_blockquote_lines = _flush_blockquote_lines(output_lines, pending_blockquote_lines)

    blockquote_continuation_allowed = _page_starts_with_blockquote_continuation(blocks, body_left, body_right)
    blockquote_quote_buffer = ''
    for b in blocks:
        block_lines = _text_block_lines(b)
        block_is_blockquote = _text_block_is_blockquote(
            b,
            body_left,
            body_right,
            blockquote_continuation_allowed,
        )
        for line in b['lines']:
            spans_text = []
            line_is_part = False
            line_is_chapter = False
            line_is_volume = False
            line_is_roman_head = False
            line_is_subtitle = False
            
            first_span = line['spans'][0]
            first_flags = first_span.get('flags', 0)
            first_size = first_span.get('size', 0)
            
            all_italic = True
            for span in line['spans']:
                if not (span.get('flags', 0) & 2):
                    all_italic = False
                
                text = span['text']
                converted = convert_span_text(text, span.get('font', ''))
                spans_text.append(converted)
                
                color = span.get('color', 0)
                size = span.get('size', 0)
                flags = span.get('flags', 0)
                
                if color == COLOR_BLUE and size > 20:
                    line_is_part = True
                elif color == COLOR_GREEN and size > 15:
                    line_is_chapter = True
                elif color == COLOR_RED and size > 15:
                    line_is_volume = True

            line_text = ''.join(spans_text).strip()
            if not line_text:
                continue

            # Roman head detection (Issue 1)
            # Catch standalone Roman numerals OR those followed by text
            if ROMAN_HEADING_RE.match(line_text) or ROMAN_ONLY_RE.match(line_text):
                line_is_roman_head = True

            # Summary Criteria (Issue 108/25):
            # 1. Direct follow-up to CHAPTER: any All-Caps block is a summary.
            # We prioritize SUMMARY over SUBTITLE when waiting_for_summary.
            line_is_summary = False
            if waiting_for_summary:
                if line_text.isupper() and len(line_text) > 4:
                    line_is_summary = True
                elif line_text:
                     # If we hit non-all-caps text, summary section is over.
                     waiting_for_summary = False

            # Subtitle: All-caps bold, or specific Title Case keywords (even if not bold) (Issue 108)
            # Use line_text for keyword check to avoid span-split issues
            is_reader = any(kw in line_text for kw in ['To The Reader', 'Christian Reader', 'To the Reader'])
            if (11.5 <= first_size <= 12.5) and not line_is_summary:
                is_bold = bool(first_flags & 16)
                is_all_caps = line_text.isupper()
                if (is_bold and is_all_caps) or is_reader:
                    line_is_subtitle = True
            
            # Subtitle detection: whole line must be uppercase (Issue 102/103)
            # EXCEPT for specific keywords like 'To The Reader'
            if line_is_subtitle and not line_text.isupper() and not is_reader:
                line_is_subtitle = False
                
            line_is_summary = False
            if in_heading_section:
                # Summary Criteria (Issue 108):
                # 1. Direct follow-up to CHAPTER: any All-Caps block is a summary.
                if waiting_for_summary and line_text.isupper() and len(line_text) > 4:
                    line_is_summary = True
                # 2. Traditional italic/small text summaries.
                elif (first_flags & 2 or first_size < 10) and first_size <= 13.5:
                    if len(line_text) < 300: # Summaries aren't usually huge paragraphs
                        line_is_summary = True

            kind = 'PLAIN'
            if line_is_part or line_is_volume: 
                kind = 'PART'
                in_heading_section = True
                waiting_for_summary = False
            elif line_text.startswith('DIGRESSION') and 11 <= first_size <= 13:
                kind = 'DIGRESSION'
                in_heading_section = True
                waiting_for_summary = False
            elif line_is_chapter: 
                kind = 'CHAPTER'
                in_heading_section = True
                waiting_for_summary = True # Now we wait for the all-caps summary
            elif ROMAN_HEADING_RE.match(line_text) or line_is_roman_head:
                kind = 'ROMAN_HEAD'
                # A Roman head ends the heading/summary block
                in_heading_section = False
                waiting_for_summary = False
            elif line_is_summary: 
                # Group multi-line all-caps summaries (Issue 108/Audit)
                if current_kind != 'SUMMARY':
                    if current_text_parts:
                        flush()
                    current_kind = 'SUMMARY'
                current_text_parts.append(line_text)
                continue
            elif line_is_subtitle: 
                kind = 'SUBTITLE'
                waiting_for_summary = False
            
            if kind == 'PLAIN' and in_heading_section:
                # We hit substantial body text that isn't italic, stop looking for headers/summaries
                if not (first_flags & 2) and len(line_text) > 25:
                    in_heading_section = False
                    waiting_for_summary = False

            if kind == 'PLAIN' and current_kind == 'ROMAN_HEAD' and current_text_parts:
                current_heading = ' '.join(current_text_parts).strip()
                heading_is_open = not re.search(r'[.!?;:]"?\s*$', current_heading)
                continues_heading = bool(re.match(r'^[a-z]', line_text))
                if heading_is_open and continues_heading:
                    current_text_parts.append(line_text)
                    continue
            
            if kind != 'PLAIN':
                flush_blockquote()
                # Structural lines should be joined if they are the SAME kind and adjacent
                # (Issue 26: avoid fragmented <h2> for multi-line subtitles)
                if kind != current_kind:
                    if current_text_parts:
                        flush()
                    current_kind = kind
                
                current_text_parts.append(line_text)
                # We no longer flush immediately for major kinds to allow multi-line headers
                # but we will flush if we hit a different kind or plain text.
                continue

            is_blockquote = block_is_blockquote and kind == 'PLAIN'
            if is_blockquote:
                if current_text_parts:
                    flush()
                pending_blockquote_lines.append(line_text)
                continue

            flush_blockquote()
            
            if kind != current_kind:
                # Always flush on kind change in structural pages to preserve 
                # explicit formatting intent.
                if current_text_parts:
                    flush()
                current_kind = kind
            current_text_parts.append(line_text)
        if block_is_blockquote:
            joined_block = _join_blockquote_lines([text for _, text in block_lines])
            if blockquote_continuation_allowed:
                blockquote_quote_buffer = (blockquote_quote_buffer + ' ' + joined_block).strip()
            else:
                blockquote_quote_buffer = joined_block
            if blockquote_continuation_allowed and not re.search(r'[“”"]', joined_block):
                blockquote_continuation_allowed = True
            else:
                blockquote_continuation_allowed = (
                    _quote_run_is_open(blockquote_quote_buffer) or
                    _quote_run_expects_reference_tail(blockquote_quote_buffer)
                )
            if not blockquote_continuation_allowed:
                flush_blockquote()
        elif block_lines:
            flush_blockquote()
            blockquote_continuation_allowed = False
            blockquote_quote_buffer = ''
                
    flush_blockquote()
    flush()
    return '\n'.join(output_lines)



def extract_page_text_with_fonts(page, page_height=PAGE_H):
    """
    Extract text from a page using raw PyMuPDF, filtering by coordinates
    and converting Greek/Hebrew font spans.
    """
    blocks = page.get_text('dict')['blocks']
    blocks = coordinate_redactor(blocks, page_height)
    body_left, body_right = _compute_page_text_bounds(blocks)
    
    lines = []
    pending_blockquote_lines = []
    blockquote_continuation_allowed = _page_starts_with_blockquote_continuation(blocks, body_left, body_right)
    blockquote_quote_buffer = ''
    for b in blocks:
        block_lines = _text_block_lines(b)
        block_is_blockquote = _text_block_is_blockquote(
            b,
            body_left,
            body_right,
            blockquote_continuation_allowed,
        )
        for line in b['lines']:
            line_text = _line_text_from_spans(line)
            if line_text:
                is_blockquote = block_is_blockquote
                pending_blockquote_lines = _append_blockquote_aware(
                    lines,
                    pending_blockquote_lines,
                    line_text,
                    is_blockquote,
                )
        if block_is_blockquote:
            joined_block = _join_blockquote_lines([text for _, text in block_lines])
            if blockquote_continuation_allowed:
                blockquote_quote_buffer = (blockquote_quote_buffer + ' ' + joined_block).strip()
            else:
                blockquote_quote_buffer = joined_block
            if blockquote_continuation_allowed and not re.search(r'[“”"]', joined_block):
                blockquote_continuation_allowed = True
            else:
                blockquote_continuation_allowed = (
                    _quote_run_is_open(blockquote_quote_buffer) or
                    _quote_run_expects_reference_tail(blockquote_quote_buffer)
                )
            if not blockquote_continuation_allowed:
                pending_blockquote_lines = _append_blockquote_aware(lines, pending_blockquote_lines, '', False)
        elif block_lines:
            pending_blockquote_lines = _append_blockquote_aware(lines, pending_blockquote_lines, '', False)
            blockquote_continuation_allowed = False
            blockquote_quote_buffer = ''

    if pending_blockquote_lines:
        _append_blockquote_aware(lines, pending_blockquote_lines, '', False)
    
    return '\n'.join(lines)


def extract_page_markdown(pages_md, page_idx):
    """Get PyMuPDF4LLM Markdown for a page, with coordinate redaction applied."""
    if page_idx >= len(pages_md):
        return ''
    text = pages_md[page_idx]['text']
    # Post-process the Markdown to remove leftover header lines
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Remove AGES headers and page numbers
        if any(h in stripped for h in ['THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION',
                                         'B o o k s F o r T h e A g e s', 'AGES Software',
                                         'Version 1.0', 'Books For The Ages']):
            continue
        if stripped.isdigit() and len(stripped) <= 4:
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)




def get_merged_page_text(doc, pages_md, page_idx, allow_treatise_title_page=True, page_height=None):
    """
    Get text for a page:
    - For structural pages (Part/Chapter starts): use specialized extraction.
    - For inner treatise title pages: use specialized formatting.
    - For Greek/Hebrew pages: use font-aware extraction.
    - For regular pages: use PyMuPDF4LLM Markdown.

    page_height: override the module-level PAGE_H constant (useful when a volume's
    PDF has non-standard page dimensions, set via OVERRIDES['page_height']).
    """
    _page_h = page_height or PAGE_H
    from render import (
        detect_page_type, format_treatise_title_page,
    )
    page = doc[page_idx]
    ptype = detect_page_type(page, page_idx + 1)
    
    if ptype == 'treatise_title_page' and allow_treatise_title_page:
        return format_treatise_title_page(page, limit_to_title=True)

    is_struct = page_is_structural(page)
    font_type = page_has_special_fonts(page)
    md_text = extract_page_markdown(pages_md, page_idx)
    
    if is_struct:
        return extract_structural_page(page, page_height=_page_h)

    has_blockquotes = page_has_blockquote_geometry(page, page_height=_page_h)

    if font_type:
        raw_text = extract_page_text_with_fonts(page, page_height=_page_h)
        # Preserve [fN] markers from Markdown that might be lost in raw text
        fn_markers = FOOTNOTE_MARKER_RE.findall(md_text)
        # Also check for standalone [fN] markers on their own lines
        for fn in fn_markers:
            marker = f'[f{fn}]'
            if marker not in raw_text:
                raw_text += f' {marker}'
        return raw_text
    elif has_blockquotes or _has_repeated_ages_marker_cluster(md_text):
        raw_text = extract_page_text_with_fonts(page)
        fn_markers = FOOTNOTE_MARKER_RE.findall(md_text)
        for fn in fn_markers:
            marker = f'[f{fn}]'
            if marker not in raw_text:
                raw_text += f' {marker}'
        return raw_text
    else:
        return md_text
