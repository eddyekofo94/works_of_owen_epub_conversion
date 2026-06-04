#!/usr/bin/env python3
"""
extract.py — Stage 1: PDF → cleaned paragraph text.

Responsible for:
  - AGES verse marker translation (including Psalms hex-chapter variant)
  - PyMuPDF PDF extraction (coordinate_redactor, structural page extractor)
  - Footnote extraction and ThML enrichment
  - Chapter structure from PDF TOC
  - Text cleaning and paragraph healing (clean_text, reconstruct_paragraphs)
  - JSON intermediate writing (extract_volume)

Imported by converter.py (legacy orchestrator) and volumes/vN/convert.py.
Issue 91: Extracted from converter.py as part of the two-stage modular refactor.
"""

import sys, os, re, json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from html import escape as _html_escape

_EXTRACT_DIR = Path(__file__).parent.resolve()
if str(_EXTRACT_DIR) not in sys.path:
    sys.path.insert(0, str(_EXTRACT_DIR))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    convert_greek_word, clean_greek_text, convert_gideon_hebrew,
    normalize_characters,
    is_greek_font, is_hebrew_font, contains_greek, contains_hebrew,
    # Pipeline constants (previously required importing render — now in shared)
    SCRIPTURE_BOOK_RE, SCRIPTURE_REF_RE, SCRIPTURE_CONTINUATION_TRAIL_RE,
    FOOTNOTE_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE, FOOTNOTE_PLACEHOLDER_RE,
    FT_MARKER_RE, EMPTY_BRACKET_RE,
    STRUCTURAL_START_RE, CITATION_ABBREV_TRAIL_RE,
    CITATION_ABBREV_START_RE, CITATION_AUTHOR_TRAIL_RE,
    MARKDOWN_STRUCTURAL_START_RE, ROMAN_LIST_TOKEN, PLAIN_CHAPTER_RE,
    INLINE_STRUCTURAL_MARKER_RE, ROMAN_HEADING_RE, ROMAN_ONLY_RE,
    _is_scripture_ref_fragment, _scripture_ref_tokens,
    _split_inline_structural_markers,
    _trim_duplicate_reference_prefix, _norm_for_dedupe,
    _normalize_spaced_caps, _normalize_i_will, _repair_owen_ocr_errors,
    title_case, nav_display_title,
)
from scripts.pdf_coordinates import (
    _append_blockquote_aware,
    _compute_page_text_bounds,
    _flush_blockquote_lines,
    _join_blockquote_lines,
    _line_is_blockquote_candidate,
    _line_text_from_spans,
    _merge_adjacent_blockquote_paragraphs,
    _repair_glued_scripture_book_references,
    _text_block_is_blockquote,
    _text_block_lines,
    _page_starts_with_blockquote_continuation,
    _quote_run_is_open,
    _quote_run_expects_reference_tail,
    _blockquote_content,
    _blockquote_has_sentence_terminal,
    _split_leading_scripture_reference_tail,
    _paragraph_expects_scripture_reference_tail,
    convert_span_text,
    coordinate_redactor,
    extract_ages_nav,
    page_has_blockquote_geometry,
    CONNECTOR_STARTERS_RE,
    SCRIPTURE_TAIL_RE,
    DANGLING_CONNECTOR_RE,
)
from scripts.ages_verse_translator import (
    translate_ages_verse_markers,
    _has_repeated_ages_marker_cluster,
)
from scripts.footnote_extractor import (
    Footnote,
    extract_footnotes_from_pdf,
    parse_thml_footnotes,
    merge_footnotes,
    find_footnote_refs_in_text,
    _normalize_extracted_footnote_markers,
)
from scripts.greek_hebrew_dedupe import (
    _remove_adjacent_duplicates,
    _remove_adjacent_line_overlaps,
)

try:
    import fitz
except ImportError:
    sys.exit("Error: PyMuPDF (fitz) not installed. Run: pip install pymupdf4llm")
os.environ.setdefault("PYMUPDF_SUGGEST_LAYOUT_ANALYZER", "0")
try:
    import pymupdf4llm
except ImportError:
    sys.exit("Error: PyMuPDF4LLM not installed. Run: pip install pymupdf4llm")

# ─── Extraction-stage constants ──────────────────────────────────
TOP_MARGIN = 35
BOTTOM_MARGIN = 20
PAGE_W = 410
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



# ================================================================
# STAGE 5: Chapter Building from TOC
# ================================================================


@dataclass
class Chapter:
    cid: str
    title: str
    level: int          # 1=treatise, 2=chapter, 3=subsection
    body_html: str = ''
    raw_text: str = ''  # Precisely truncated raw text from build_chapters_from_toc
    page_start: int = 0
    page_end: int = 0
    is_treatise: bool = False
    is_endnotes: bool = False
    footnote_refs: list = field(default_factory=list)


def _trim_to_matching_structural_marker(raw_text: str, title: str) -> str:
    """Drop carried-over page text before the marker for the current TOC entry."""
    if not raw_text or not title:
        return raw_text

    def norm(value: str) -> str:
        value = re.sub(r'\[\[[A-Z_]+\]\]', ' ', value)
        value = re.sub(r'[^A-Z0-9]+', ' ', value.upper())
        return re.sub(r'\s+', ' ', value).strip()

    title_norm = norm(title)
    if not title_norm:
        return raw_text
    markers = list(re.finditer(
        r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]\s*([^\n]*)',
        raw_text,
        re.I,
    ))
    if not markers:
        return raw_text
    for marker in markers:
        if marker.start() == 0:
            continue
        marker_text = norm(marker.group(1))
        if marker_text and (title_norm in marker_text or marker_text in title_norm):
            return raw_text[marker.start():].strip()
    return raw_text


def _keep_only_prerendered_treatise_title_page(raw_text: str) -> str:
    """Keep a pre-rendered title section without same-page body spillover."""
    if not raw_text:
        return raw_text
    match = re.match(
        r'(?P<section>\s*<section\b[^>]*class="[^"]*\btreatise-title-page\b.*?</section>)',
        raw_text,
        re.I | re.S,
    )
    if not match:
        return raw_text
    return match.group('section').strip()


def build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map, config=None,
                            vol_num=None, progress_callback=None):
    """
    Build chapters by grouping pages based on PDF TOC entries.
    Merges consecutive same-level entries and handles hierarchy.
    """
    if not nav_entries:
        # Fallback: treat each page as a chapter
        return _build_flat_chapters(doc, pages_md, footnote_map)
    
    chapters = []
    seen_titles = set()
    cid_counter = 0
    
    # Filter out metadata entries (book-level entries, contents pages)
    # Also skip all children of filtered-out entries (tree-aware)
    filtered_nav = []
    skip_level = None  # level of the currently skipped metadata entry
    metadata_patterns = re.compile(
        r'^(Owen Librarian|The Works of John Owen|Contents|The Works of John Owen Vol\.\s*\d+)$|'
        r'^The Works of John Owen\s*[-–]|'
        r'^Contents\s+of\b', re.I
    )
    for level, title, page in nav_entries:
        title_stripped = title.strip()
        is_meta = bool(metadata_patterns.match(title_stripped))
        
        if is_meta:
            skip_level = level
            continue
        
        if skip_level is not None:
            if level <= skip_level:
                skip_level = None  # back to sibling level, stop skipping
            else:
                continue  # still a child of a skipped entry
        
        filtered_nav.append((level, title_stripped, page))
    
    nav_entries = filtered_nav
    
    if not nav_entries:
        return _build_flat_chapters(doc, pages_md, footnote_map)
    
    # Process TOC entries
    current_treatise = ""
    configured_treatises = (config or {}).get('treatises', [])
    
    for i, (level, title, page_0idx) in enumerate(nav_entries):
        if re.fullmatch(r'\s*FOOTNOTES\.?\s*', title, re.I):
            continue
        # Determine if this is a treatise title page
        title_upper = title.upper()
        
        # Use relative matching against configured treatises (Issue 108)
        # We check if the TOC title contains any of our configured treatise titles
        matched_treatise = None
        for t in configured_treatises:
            if t.upper() in title_upper or title_upper in t.upper():
                matched_treatise = t
                break
                
        standalone_catechism_title = bool(re.match(
            r'^(?:THE\s+)?(?:GREATER|LESSER)\s+CATECHISM\.?$',
            title_upper,
        ))
        is_treatise = (
            bool(matched_treatise)
            or any(kw in title_upper for kw in ['PART', 'BOOK'])
            or standalone_catechism_title
        )
        
        if is_treatise:
            if matched_treatise:
                current_treatise = matched_treatise
            else:
                current_treatise = title_case(title)

        # Determine end page (next entry's page - 1, or end of doc)
        if i + 1 < len(nav_entries):
            end_page = nav_entries[i + 1][2] - 1
        else:
            end_page = len(doc) - 1
        
        if end_page < page_0idx:
            end_page = page_0idx
        
        # Skip if bookends/empty
        shares_previous_start = bool(chapters and chapters[-1].page_end == page_0idx)
        allow_treatise_title_page = not (shares_previous_start and not is_treatise)
        raw_text = get_pages_text(
            doc,
            pages_md,
            page_0idx,
            end_page,
            title=title,
            config=config,
            allow_treatise_title_page=allow_treatise_title_page,
        )
        raw_text = _trim_to_matching_structural_marker(raw_text, title)
        
        # Handle shared start page: if this chapter starts on a page shared with previous,
        # extract only from the heading onwards.
        if chapters and chapters[-1].page_end == page_0idx:
            # If this is a chapter starting on the same page as a treatise/part,
            # we must start at the CHAPTER marker, not the PART marker.
            if not is_treatise:
                marker = re.search(r'\[\[CHAPTER\]\]', raw_text)
                if marker:
                    raw_text = raw_text[marker.start():]
            else:
                marker = re.search(r'\[\[(?:PART|CHAPTER|DIGRESSION)\]\]', raw_text)
                if marker:
                    raw_text = raw_text[marker.start():]

        # Handle shared end page: if the NEXT chapter starts on the same page this one ends,
        # OR if it starts on the very same page (shared start), truncate this one.
        if i + 1 < len(nav_entries):
            next_start_page = nav_entries[i + 1][2]
            if page_0idx == next_start_page:
                # This entry and the next one share the SAME START PAGE.
                # We must truncate THIS entry before the next one's heading.
                # Usually happens for Treatise title pages that are followed immediately by Chapter 1.
                if is_treatise:
                    raw_text = _keep_only_prerendered_treatise_title_page(raw_text)
                
                # Find all markers
                markers = list(re.finditer(r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]\s*([^\n]*)', raw_text))
                if len(markers) > 1:
                    # Find the first 'major' marker after the initial one to truncate at.
                    # If current is PART/TREATISE, we stop at the next CHAPTER or PART.
                    truncate_at = len(raw_text)
                    next_title_norm = re.sub(r'[^A-Z0-9]+', ' ', nav_entries[i + 1][1].upper()).strip()
                    for m in markers[1:]:
                        marker_token = re.match(r'\[\[([A-Z_]+)\]\]', m.group(0)).group(1)
                        marker_text_norm = re.sub(r'[^A-Z0-9]+', ' ', (m.group(1) or '').upper()).strip()
                        matches_next_title = bool(
                            marker_text_norm
                            and next_title_norm
                            and (next_title_norm in marker_text_norm or marker_text_norm in next_title_norm)
                        )
                        if marker_token in ('PART', 'CHAPTER', 'DIGRESSION') or matches_next_title:
                            truncate_at = m.start()
                            break
                    raw_text = raw_text[:truncate_at].strip()
            elif end_page == next_start_page - 1:
                # We need to check the actual start page of the next entry.
                # If it has content before the heading, it belongs here.
                next_page_raw = get_merged_page_text(doc, pages_md, next_start_page)
                marker = re.search(r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]', next_page_raw)
                if marker:
                    pre_heading = next_page_raw[:marker.start()].strip()
                    if pre_heading:
                        # Only join if it doesn't look like a standalone title (Issue 99/11)
                        # and if the current text didn't end with a signature
                        if (len(pre_heading) > 40 or not pre_heading.isupper()) and \
                           not re.search(r'_\*\*J\.O\.\*\*|_August_ 18\d{2}', raw_text):
                            raw_text = raw_text + "\n\n" + pre_heading
        
        if not raw_text.strip():
            continue
        
        cid_counter += 1
        cid = f'ch{cid_counter:03d}'
        
        display_title = title_case(title) if not is_treatise else title
        if not is_treatise and current_treatise:
            # Differentiate Prefatory Notes and Prefaces
            # Match titles like "Prefatory Note", "Preface", "The Preface", "To the Reader"
            normalized_title = title.strip().rstrip('.').upper()
            if any(kw in normalized_title for kw in {
                'PREFATORY NOTE', 'PREFACE', 'TO THE READER'
            }):
                # Keep it concise: "Prefatory Note (Treatise Name)"
                # Extract the base name (e.g. "THE PREFACE" -> "Preface")
                base = "Prefatory Note" if "PREFATORY" in normalized_title else \
                       "Preface" if "PREFACE" in normalized_title else \
                       "To the Reader"
                display_title = f"{base} ({current_treatise})"

        chap = Chapter(
            cid=cid,
            title=display_title,
            level=level,
            raw_text=raw_text,
            page_start=page_0idx,
            page_end=end_page,
            is_treatise=is_treatise,
        )
        chapters.append(chap)

        if progress_callback:
            progress_callback(i + 1, len(nav_entries),
                              f"[extract] Volume {vol_num}")

    return chapters



def strip_false_ocr_bolds(text):
    """Strip false OCR bold markers (**word**) that are not structural list or heading elements."""
    if not text:
        return text

    def replace_bold(match):
        full_match = match.group(0)
        content = match.group(1)
        clean_content = content.strip()

        # Preserve structural list markers: e.g. "1.", "(1)", "[1]", "I.", "Q.", "Ans.", "First.", "1stly", "[1st.]"
        # Handles optional brackets or parentheses around digit/ordinal/Roman/Letter
        if re.match(
            r'^[\(\[]?(?:(?!\d{4}\.)\d{1,4}(?:st|nd|rd|th)?(?:ly|dly)?|[IVXLCDM]+|[A-Z])\.?[\)\]]?$',
            clean_content,
            re.I
        ):
            return full_match
        if re.match(r'^(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?$', clean_content, re.I):
            return full_match
        if re.match(r'^(?:First|Secondly|Thirdly|Fourthly|Fifthly|Lastly)\.?$', clean_content, re.I):
            return full_match

        # Otherwise, if it is a random word or phrase in the text, it is likely false OCR bold.
        return content

    # Use re.sub with a non-greedy match for **content**
    return re.sub(r'\*\*(?!\*)([^\n*]+?)\*\*', replace_bold, text)


def _is_terminal(text):
    """Check if the text ends in a terminal punctuation, excluding abbreviations."""
    if not text:
        return False
    text_clean = text.strip()
    if not re.search(r'[.!?]"?\s*$', text_clean):
        return False
    # If it ends with a citation abbreviation, it's not a true terminal period
    if CITATION_ABBREV_TRAIL_RE.search(text_clean):
        return False
    # Also check other common theological/patristic/Bible abbreviations
    abbrevs = (
        r'\b(?:Dr|Mr|Mrs|St|viz|i\.e|e\.g|[A-Z])\.\s*$'
        r'|'
        # Bible books
        r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kings|Chron|Ezra|Neh|Esth|Job|Ps|Prov|Eccl|Cant|'
        r'Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|'
        r'Matt|Mk|Lk|Jn|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Pet|Jude|Rev)\.\s*$'
        r'|'
        # Patristic / Scholastic authors
        r'\b(?:Aug|August|Austin|Chrys|Chrysost|Hierom|Jerome|Clem|Clement|Tertull|Orig|Origen|Cyp|Cyprian|'
        r'Euseb|Athan|Athanas|Basil|Naz|Nazianz|Nyss|Ambr|Ambrose|Theod|Theodoret|Cyril|Hilar|Hilary|Leo|Bern|'
        r'Bernard|Bell|Bellar|Soc|Socin|Faust|Faustus|Calv|Calvin|Epiph|Epiphan|Greg|Gregory|Plut|Cic|Sen|Tac|'
        r'Plin|Arist|Plat|Justin|Iren|Alex|Alexand|Mart)\.\s*$'
    )
    if re.search(abbrevs, text_clean, re.I):
        return False
    return True


def clean_text(text, config=None):
    """Sanitize extracted text before paragraph reconstruction."""
    if not text:
        return ''

    # 0. Character normalization (Issue: Gideon/AGES legacy encoding)
    text = normalize_characters(text)

    # 0a. Owen-specific OCR repairs (Issue 75/108)
    text = _repair_owen_ocr_errors(text, config=config)
    text = _normalize_extracted_footnote_markers(text)
    # Normalize loose bracketed footnote letters: [ a] or [ a[ -> [a]
    text = re.sub(r'\[\s*([a-z])\s*[\]\[]', r'[\1]', text, flags=re.I)

    # 0b. Normalize spaced-caps OCR and I WILL / I AM mangles
    text = _normalize_spaced_caps(text)
    text = _normalize_i_will(text)
    
    # 0c. Scripture range OCR repairs (Issue 108)
    # Handles "7 ( 8)" -> "7, 8" misreads
    text = re.sub(r'(\d)\s+\(\s*(\d+)\s*\)', r'\1, \2', text)
    text = _normalize_scholarly_citation_artifacts(text)

    # 1. Translate AGES scripture reference codes to readable citations.
    #    <430316> → John 3:16. Must run BEFORE EMPTY_BRACKET_RE so we don't
    #    clobber the translated output.
    text = translate_ages_verse_markers(text)
    text = _repair_glued_scripture_book_references(text)
    text = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', text, flags=re.I)
    # General enough for "( John" while avoiding global "** Text" corruption.
    text = re.sub(r'\(\s+([A-Z])', r'(\1', text)
    text = EMPTY_BRACKET_RE.sub('', text)
    # 2. Remove AGES running headers (whole-line removal)
    text = re.sub(
        r'^.*(?:THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|'
        r'BOOKS FOR THE AGES|AGES SOFTWARE|VERSION \d\.\d|'
        r'VOLUME \d+|JOHN OWEN COLLECTION|Books For The Ages).*$',
        '', text, flags=re.MULTILINE | re.IGNORECASE
    )
    # 3. Collapse multiple spaces → single space
    text = re.sub(r' {2,}', ' ', text)
    # Normalize Q/A labels that are clearly structural (Issue 26)
    # Strictly case-sensitive and anchored to start of line to avoid corrupting prose
    text = re.sub(r'\bAns\s+\.\s+(\d+)\b\.?', r'Ans. \1.', text)
    text = re.sub(r'(?m)^([QA])\s*[\., ]+\s*(\d+)\s*\.?', r'\1. \2.', text)
    text = re.sub(r'(?m)^([QA])\s*[\., ]+\s*', r'\1. ', text)
    text = re.sub(r'(?m)^(A)\s*\.\s*,\s*', r'\1. ', text) # A. , -> A.
    
    # Fix ordinal spacing: "1st ." -> "1st.", "**1st** ." -> "**1st**.", "2ndly ," -> "2ndly,"
    # Handles both plain and bold-wrapped ordinals, including adverbial forms
    text = re.sub(
        r'(\*\*)?(\d+(?:(?:st|nd|rd|th)ly|dly|ly|st|nd|rd|th))(\*\*)?\s+([,.;])',
        r'\1\2\3\4',
        text
    )
    
    # 4. Strip leading/trailing whitespace per line
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    # 4a. Ensure space between Greek/Hebrew and English (Issue 108/Audit)
    # Handles cases like “ἰσάγγελοι”like -> “ἰσάγγελοι” like
    # Includes common trailing punctuation/quotes in the junction check
    text = re.sub(r'([\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF][”"’)]?)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])([“"‘(]?[\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF])', r'\1 \2', text)

    # 4b. Aggressive remove leading Latin artifact noise before Greek (Issue: j jEgw)
    # Standalone 'j' or 'J' followed by space or before Greek is noise.
    text = re.sub(r'(?i)\b[jJ]\s+', '', text)
    text = re.sub(r'(?i)\b[jJ](?=[\u0370-\u03FF\u1F00-\u1FFF])', '', text)
    
    # 5. Remove adjacent ghost-layer duplicates and repeated line tails
    text = _remove_adjacent_duplicates(text)
    text = _remove_adjacent_line_overlaps(text)
    text = strip_false_ocr_bolds(text)
    return clean_greek_text(text.strip())


def _normalize_scholarly_citation_artifacts(text):
    """Repair OCR punctuation that breaks patristic/scholastic citations.

    AGES extraction sometimes turns citation abbreviations into forms like
    "cap., 8" or splits "Chapter, 8." across lines. Those commas make the
    paragraph healer treat the following number as a list item instead of a
    citation continuation.
    """
    if not text:
        return text

    # "cap., 8" / "q. , 81" -> "cap. 8" / "q. 81"
    text = re.sub(
        r'\b(?P<label>cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|'
        r'dial|enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\s*\.\s*,\s*(?=\d)',
        lambda m: f'{m.group("label")}. ',
        text,
        flags=re.I,
    )

    # "Chapter,\n8." / "Chap., 8." -> "Chapter 8." / "Chap. 8."
    text = re.sub(
        r'\b(?P<label>chapter|chap)\s*(?:\.\s*)?,\s*(?=\d)',
        lambda m: f'{m.group("label")} ' if m.group("label").lower() == 'chapter' else f'{m.group("label")}. ',
        text,
        flags=re.I,
    )

    return text


# Short introductory connectors that should be merged with previous text (Issue 1)
SEMANTIC_CONNECTOR_RE = re.compile(
    r'^(?:For|As|Wherefore|And|Or|Yea|Yet|So|Thus|Hence|Moreover)\s*[,;—\-]\s*$',
    re.I
)

# Terms where a hyphen at EOL should be preserved (Issue 1)
OWEN_HARD_HYPHENS = {
    'Spiritual-mindedness', 'spiritually-minded', 'heavenly-mindedness',
    'self-denial', 'faith-fulness', 'church-state', 'fellow-creature',
    'well-pleased', 'good-will', 'soul-satisfying'
}


def reconstruct_paragraphs(text):
    """Heal broken lines into proper, reflowable paragraphs."""
    if not text:
        return []

    lines = text.split('\n')
    paragraphs = []
    current = []
    _bracket_continuation = False  # Issue 8: flag when last structural token has unbalanced [

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Issue 8: if previous structural token had unclosed bracket, join this line to it
        if _bracket_continuation and stripped:
            _bracket_continuation = False
            if paragraphs:
                paragraphs[-1] = paragraphs[-1] + ' ' + stripped
            continue

        if not stripped:
            if current:
                prev = current[-1]
                ends_terminal = _is_terminal(prev)
                # Look ahead: if next non-empty line starts with connector, don't break
                next_nonempty = None
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        next_nonempty = lines[j].strip()
                        break
                
                starts_with_connector = (
                    next_nonempty is not None and
                    bool(CONNECTOR_STARTERS_RE.match(next_nonempty))
                )
                starts_with_scripture = (
                    next_nonempty is not None and
                    bool(re.match(rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b', next_nonempty, re.I))
                )
                starts_with_bare_ref = (
                    next_nonempty is not None and
                    bool(re.match(r'^\d+:\d+', next_nonempty))
                )
                
                # Issue 108/Blemish 8: Reference continuation awareness across blank lines
                ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
                prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
                next_starts_with_ref_number = next_nonempty and bool(re.match(r'^\d{1,4}\b', next_nonempty))
                
                if ends_terminal and not starts_with_connector:
                    if starts_with_scripture or starts_with_bare_ref:
                        continue
                    if prev_is_ref_abbrev and next_starts_with_ref_number:
                        # Reference continuation (p.\n\n280) -> join
                        continue
                    paragraphs.append(' '.join(current))
                    current = []
            continue

        # Preserve heading markers and structural tokens as standalone paragraphs
        is_structural_token = stripped.startswith('[[') and ']]' in stripped
        if stripped.startswith('#') or is_structural_token:
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append(stripped)
            # Issue 8: check for unbalanced '[' after stripping [[TOKEN]] markers.
            # If content after the markers has more '[' than ']', the next line
            # (e.g. "6. 546.]") belongs to this paragraph (e.g. "[Juv.,\n6. 546.]").
            _token_stripped = re.sub(r'\[\[[A-Z_]+\]\]\s*', '', stripped)
            _bracket_continuation = _token_stripped.count('[') > _token_stripped.count(']')
            continue

        # Preserve numbered/list-like starts as real paragraph breaks.
        if STRUCTURAL_START_RE.match(stripped):
            if current:
                prev = current[-1]

                # Blemish fix: numeric range hyphen — "Romans 1:19-" + "21. This..."
                # The continuation digit matches STRUCTURAL_START_RE but it's a verse
                # range continuation, not a new list item.  Join and preserve hyphen.
                if re.search(r'\d+-$', prev):
                    current[-1] = prev + stripped
                    continue

                ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
                prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
                starts_with_ref_number = bool(re.match(r'^\d{1,4}\.\s+', stripped))
                if prev_is_ref_abbrev and starts_with_ref_number:
                    current.append(stripped)
                    continue

                # Hard structural: markers that are nearly always paragraph starts
                # Q./A./Ques./Ans. must be UPPERCASE to avoid scholastic citations (Issue 17/26)
                hard_structural = re.match(
                    r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
                    r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
                    r'\d+(?:st|nd|rd|th)\b[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)',
                    stripped
                )
                if not hard_structural:
                     # Fallback for case-insensitive Roman numerals but NOT Q/A
                     hard_structural = re.match(
                        r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
                        r'\d+(?:st|nd|rd|th)\b[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)',
                        stripped,
                        re.I
                    )
                
                # Blemish 11: Classical/Scholarly reference tail detection: "Liv. viii." -> "9."
                prev_is_classical_ref = bool(re.search(
                    r'\b(?:liv|aen|hist|tac|plut|cic|sen|aug)\.?\s+(?:hist\.?\s+)?[ivxlcdm]+\.\s*$',
                    prev, re.I
                ))
                is_bare_decimal = bool(re.match(r'^\d{1,2}\.\s+[A-Z]', stripped))
                if prev_is_classical_ref and is_bare_decimal:
                    current.append(stripped)
                    continue

                # Bible book abbreviation followed by Roman or Arabic chapter/verse marker
                prev_is_book_abbrev = bool(re.search(
                    r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kings|Chron|Ezra|Neh|Esth|Job|Ps|Prov|Eccl|Cant|'
                    r'Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|'
                    r'Matt|Mk|Lk|Jn|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Pet|Jude|Rev)\.\s*$',
                    prev, re.I
                ))
                is_ref_start = bool(re.match(r'^(?:[ivxlcdm]+|\d+)\b', stripped, re.I))
                if prev_is_book_abbrev and is_ref_start:
                    current.append(stripped)
                    continue

                ends_terminal = _is_terminal(prev)
                is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))
                is_comma_continuation = bool(re.search(r',\s*$', prev))

                # Blemish fix: a line ending with a dangling connector word (e.g. "the",
                # "of", "from") or a comma must ALWAYS join the next line, even if that next line
                # superficially matches hard_structural (e.g. "the\n11th, which we…").
                # "11th," looks like an ordinal list marker but it's mid-sentence here.
                # However, if the next line starts with a clear structural list marker (like "(2.)" or "2."),
                # it should NOT be merged since lists can end items with commas.
                is_clear_list_marker = bool(re.match(
                    r'^(?:\(\d+\.?\)|\(\w+\.?\)|\[\d+\.?\]|\[\w+\.?\]|\b\d+\.\s+[A-Z]|\b[IVXLCDM]+\.\s+[A-Z])',
                    stripped
                ))
                if (is_dangling or is_comma_continuation) and not is_clear_list_marker:
                    current.append(stripped)
                    continue

                if (not ends_terminal) and not hard_structural:
                    current.append(stripped)
                    continue
            if current:
                paragraphs.append(' '.join(current))
            current = [stripped]
            continue

        # De-hyphenation: strip trailing hyphen, merge with no space
        if current and current[-1].endswith('-'):
            prev_tail = current[-1]
            candidate = prev_tail + stripped
            # Blemish fix: numeric range hyphens (e.g. "1:19-" / "19-") must be
            # preserved as-is — they are verse/chapter range delimiters, NOT
            # word-break hyphens.  "Romans 1:19-\n21" → "Romans 1:19-21".
            if re.search(r'\d+-$', prev_tail):
                current[-1] = prev_tail + stripped
                continue
            # If the resulting word is a known hard-hyphenated term, keep the hyphen (Issue 1)
            if any(term.lower() == candidate.lower() for term in OWEN_HARD_HYPHENS):
                current[-1] = prev_tail + " " + stripped
            else:
                current[-1] = prev_tail[:-1] + stripped
            continue

        if current:
            prev = current[-1]
            ends_terminal = _is_terminal(prev)
            starts_lower = bool(re.match(r'^[a-z0-9({\[\'"\u201c\u2018]', stripped))
            is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))
            is_semantic_connector = bool(SEMANTIC_CONNECTOR_RE.match(stripped))
            starts_with_connector = bool(CONNECTOR_STARTERS_RE.match(stripped))

            # Blemish 5, 8, 10: Reference and Scripture continuation awareness
            starts_with_scripture = bool(re.match(rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b', stripped, re.I))
            starts_with_bare_ref = bool(re.match(r'^\d+:\d+', stripped))
            
            ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
            prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
            starts_with_ref_number = bool(re.match(r'^\d{1,4}\b', stripped))
            prev_ends_with_number_period = bool(re.search(r'\d+\.\s*$', prev))

            # Issue 76: Multiline block quote preservation
            all_current_text = ' '.join(current)
            is_inside_quote = (
                (all_current_text.count('\u201c') > all_current_text.count('\u201d')) or
                (all_current_text.count('"') % 2 != 0)
            )
            # Blemish fix: unclosed parenthetical \u2014 if the accumulated paragraph
            # has more open parens than closing parens we are inside a parenthetical
            # expression (e.g. a Latin citation like "(Crell. de Natur. Spir.\nSanc.)")
            # and must always join the continuation, regardless of terminal punctuation.
            is_inside_paren = all_current_text.count('(') > all_current_text.count(')')

            if not ends_terminal or is_dangling or is_semantic_connector:
                # Line does not end with terminal punctuation or ends with a connector
                # OR the current line is a semantic connector ("For,", "As,") → join
                current.append(stripped)
            elif starts_lower:
                # Starts lowercase after terminal (e.g. middle of quotation) → join
                current.append(stripped)
            elif is_inside_quote or is_inside_paren:
                # Inside an unclosed quote or parenthetical → join
                current.append(stripped)
            elif starts_with_connector:
                # Next starts with connector word ("Wherefore", "But", "And", etc.) → join
                current.append(stripped)
            elif starts_with_scripture or starts_with_bare_ref:
                # Blemish 5: Scripture continuation → join
                current.append(stripped)
            elif prev_is_ref_abbrev and (starts_with_ref_number or prev_ends_with_number_period):
                # Blemish 8/10: Reference number continuation (p. 280, Aen. 10.) → join
                current.append(stripped)
            else:
                # Terminal punctuation + uppercase start → new paragraph
                paragraphs.append(' '.join(current))
                current = [stripped]
        else:
            current = [stripped]

    if current:
        paragraphs.append(' '.join(current))

    paragraphs = _merge_adjacent_blockquote_paragraphs(paragraphs)
    return post_process_paragraphs(paragraphs)






def _paragraph_needs_numeric_continuation(prev, current):
    """Return True when a numeric-looking paragraph is really a reference tail."""
    if not prev or not current:
        return False

    current_clean = current.strip()
    current_clean = re.sub(r'^\*\*(\d{1,3}[,.;]?)\*\*', r'\1', current_clean)
    if not re.match(r'^\d{1,3}[,.;]?\s+', current_clean):
        return False

    prev_clean = prev.strip()
    
    # Mid-sentence dangling connectors, commas, or hyphens always indicate continuation
    if (
        bool(DANGLING_CONNECTOR_RE.search(prev_clean))
        or bool(re.search(r',\s*$', prev_clean))
        or bool(re.search(r'-\s*$', prev_clean))
    ):
        return True
    if re.search(
        r'\b(?:p|pp|sec|chap|vol|cf|see|ibid|id|op|cit|fol|col|liv|aen|hist)\.?\s*$',
        prev_clean,
        re.I,
    ):
        return True
    if re.search(r'\b(?:Aen|Liv|Hist)\.?\s+\d+\.\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b(?:Liv|Tac|Plut|Cic|Sen|Aug)\.?,?\s+Hist\.?\s+[ivxlcdm]+\.\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+\s*$', prev_clean, re.I):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean, re.I):
        return True
    if _is_scholarly_citation_tail(prev_clean):
        return True
    return False


def _join_numeric_continuation(prev, current):
    """Join numeric continuations, preserving verse ranges where possible."""
    if re.search(r'\b\d+:\d+\s*$', prev.strip()) and re.match(r'^\d{1,3}\.?\s+', current.strip()):
        current = re.sub(r'^(\d{1,3})\.?\s+', r'\1. ', current.strip(), count=1)
        return f"{prev.rstrip()}-{current}"
    return f"{prev} {current}".strip()


def _is_reference_continuation(prev, current):
    """Return True for broken reference tails such as `chap.` / `7:26`."""
    if not prev or not current:
        return False
    prev_clean = prev.strip()
    current_clean = current.strip()
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev_clean, re.I):
        return bool(re.match(r'^\d{1,3}(?::\d+)?(?:[-,;]\s*\d+)*[,:;]?\b', current_clean))
    if SCRIPTURE_CONTINUATION_TRAIL_RE.search(prev_clean):
        return bool(re.match(r'^\d{1,3}(?:[-,;]\s*\d+)*[,:;]?\s+', current_clean))
    return False


def _is_citation_abbrev_continuation(prev, current):
    """Return True for scholarly citation chains split after an author cue."""
    if not prev or not current:
        return False
    prev_clean = prev.strip()
    current_clean = current.strip()
    if not CITATION_ABBREV_START_RE.match(current_clean):
        return False
    if CITATION_AUTHOR_TRAIL_RE.search(prev_clean):
        return True
    if re.search(r'\b(?:see|apud|contra|adv|ad)\s*$', prev_clean, re.I):
        return True
    return False


def _is_scholarly_citation_tail(text):
    """Return True when text ends inside a scholarly citation number chain."""
    if not text:
        return False
    return bool(re.search(
        r'\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*,?\s*$',
        text.strip(),
        re.I,
    ))


def _is_scholarly_citation_fragment(text):
    """Return True for short paragraphs that are only citation tail fragments."""
    if not text:
        return False
    clean = text.strip()
    if len(clean) > 140:
        return False
    return bool(re.fullmatch(
        r'(?:'
        r'(?:and\s+)?(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*|'
        r'ad\s+(?:prim|tert|secund)\.?'
        r')'
        r'(?:[,;]\s*(?:and\s+)?(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*|[,;]\s*ad\s+(?:prim|tert|secund)\.?)*'
        r'\.?',
        clean,
        re.I,
    ))


def _ends_with_scholarly_citation_sentence(text):
    """Return True when a paragraph ends with a scholarly citation sentence."""
    if not text:
        return False
    clean = text.strip()
    if len(clean) > 500:
        clean = clean[-500:]
    return bool(re.search(
        r'\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*\.\s*$',
        clean,
        re.I,
    ))


def _trim_overlapping_prefix(prev, current):
    """Return current with a duplicated prefix removed when it repeats prev's tail."""
    prev_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", prev)]
    curr_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", current)]
    max_overlap = min(10, len(prev_words), len(curr_words))
    for size in range(max_overlap, 1, -1):
        if [w for w, _, _ in prev_words[-size:]] == [w for w, _, _ in curr_words[:size]]:
            cut = curr_words[size - 1][2]
            return current[cut:].lstrip(' ,;:.')
    return current


def _paragraph_needs_text_continuation(prev, current):
    if not prev or not current:
        return False
    if current.startswith('#') or '[[' in current:
        return False
    if '[[' in prev:
        return False
    
    # Check for continuation contexts FIRST (Issues 71, 72)
    # Book + reference (e.g. "1 Corinthians" + "1. Wherefore...")
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', prev, re.I) and \
       re.match(r'^\d{1,3}[,.;]?\s+', current):
        return True
    
    # Chapter range continuation (e.g. "Chapter 9 to" + "15. It is followed...")
    if re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', prev, re.I) and \
       re.match(r'^\d{1,3}[,.;]?\s+', current):
        return True


    hard_structural = re.match(r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|\d+(?:st|nd|rd|th)\b\s*[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)', current)
    if hard_structural or MARKDOWN_STRUCTURAL_START_RE.match(current):
        return False

    # Issue 76: Quote continuation
    if (prev.count('\u201c') > prev.count('\u201d')) or (prev.count('"') % 2 != 0):
        return True

    if not _is_terminal(prev):
        return True
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev, re.I):
        return True
    if re.search(r'\b(?:of|the|and|or|to|in|with|from|unto|for)\s*$', prev, re.I):
        return True
    return False


def _is_probable_duplicate_fragment(prev, current):
    """Drop ghost fragments whose words already occur in the previous paragraph."""
    if not prev or not current:
        return False
    
    # Increase threshold for Owen volumes (Issue 108/Audit)
    if len(current) > 1200: 
        return False
        
    prev_norm = _norm_for_dedupe(prev)
    current_norm = _norm_for_dedupe(current)
    
    # 1. Prefix match (Issue 108/Audit ch032): 
    # If the current paragraph is a prefix of the previous one, it is a ghost.
    if prev_norm.startswith(current_norm) and len(current_norm) > 30:
        return True

    # 2. Word overlap match
    prev_words = set(re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", prev_norm))
    current_words = re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", current_norm)
    
    useful = [w for w in current_words if len(w) > 2]
    if len(useful) < 8:
        return False
        
    overlap = sum(1 for w in useful if w in prev_words)
    ratio = overlap / len(useful)
    
    # High confidence for short runs, very high for longer ones
    if len(useful) < 25:
        return ratio >= 0.90
    return ratio >= 0.95


def _remove_repeated_opening_clause(text):
    """Remove duplicated opening clauses like 'So we are said ...: So we are said ...:'."""
    pattern = re.compile(r'^(.{25,220}?[.:;])\s+\1', re.I)
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub(r'\1 ', text)
    return text


def _collapse_adjacent_duplicate_refs(text):
    """Collapse directly-concatenated duplicate scripture references."""
    def _dedup_repl(m):
        first = m.group(1)
        second = m.group(2)
        # Normalize for comparison (Issue 108/Audit)
        f_norm = re.sub(r'[^a-z0-9:]', '', first.lower())
        s_norm = re.sub(r'[^a-z0-9:]', '', second.lower())
        
        if f_norm == s_norm or f_norm.endswith(s_norm) or s_norm.endswith(f_norm):
             return first if len(first) >= len(second) else second
        return m.group(0)

    # Pattern: Book Ch:v followed by optional punctuation and potentially a repeat.
    # Allow zero or more punctuation/spaces between them (Issue 108/Audit)
    _ADJ_DUP_RE = re.compile(
        r'(\b(?:[1-3]\s+)?[A-Z][a-zA-Z ]{1,30}?\s+\d+:\d+(?:[-,]\s*\d+)*)'
        r'[\s,;.]*'
        r'((?:(?:[1-3]\s+)?[A-Z][a-zA-Z, ]{1,30}?\s+)?\d+:\d+(?:[-,]\s*\d+)*)',
    )
    previous = None
    while previous != text:
        previous = text
        text = _ADJ_DUP_RE.sub(_dedup_repl, text)
    return text


def _remove_duplicate_scripture_tail(text):
    """Trim repeated scripture-reference tails inside one paragraph."""
    previous = None
    while previous != text:
        previous = text
        refs = list(SCRIPTURE_REF_RE.finditer(text))
        if len(refs) < 4:
            return text

        # Compare normalized reference tokens and cut if the same tail starts over.
        norm_refs = []
        for m in refs:
            token = re.sub(r'\s+', ' ', m.group(0).lower())
            token = re.sub(r'^(?:[1-3]\s+)?', '', token)
            norm_refs.append((token, m.start(), m.end()))

        changed = False
        for i in range(len(norm_refs)):
            for j in range(i + 2, len(norm_refs)):
                if norm_refs[i][0] != norm_refs[j][0]:
                    continue
                run = 0
                while (
                    i + run < len(norm_refs)
                    and j + run < len(norm_refs)
                    and norm_refs[i + run][0] == norm_refs[j + run][0]
                ):
                    run += 1
                if run >= 2:
                    cut_start = norm_refs[j][1]
                    cut_end = norm_refs[j + run - 1][2]
                    while cut_start > 0 and text[cut_start - 1] in ' \t':
                        cut_start -= 1
                    while cut_end < len(text) and text[cut_end] in ' ;,.:':
                        cut_end += 1
                    # AGES sometimes leaves a bare verse number between duplicated
                    # reference runs, such as "Ezekiel 36:26; 26; John 1:13".
                    bare_verse = re.match(r'\s*\d{1,3}\s*[;,]\s*', text[cut_end:])
                    if bare_verse:
                        cut_end += bare_verse.end()
                    text = re.sub(r'\s{2,}', ' ', (text[:cut_start] + ' ' + text[cut_end:]).strip())
                    changed = True
                    break
            if changed:
                break
        if not changed:
            return text
    return text


def _remove_interrupted_duplicate_clause(text):
    """Remove reference-list ghosts that interrupt and restart the same clause."""
    words = [
        (re.sub(r'[^a-z0-9\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+', '', m.group(0).lower()), m.start(), m.end())
        for m in re.finditer(r"[A-Za-z0-9'\u2019\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF-]+", text)
    ]
    words = [item for item in words if item[0]]
    size = 6
    for i in range(0, max(0, len(words) - (size * 2))):
        first = [w for w, _, _ in words[i:i + size]]
        if sum(1 for w in first if re.search(r'[a-z]', w)) < 4:
            continue
        for j in range(i + size, min(len(words) - size + 1, i + 80)):
            if first != [w for w, _, _ in words[j:j + size]]:
                continue
            gap = text[words[i + size - 1][2]:words[j][1]]
            if len(SCRIPTURE_REF_RE.findall(gap)) < 2:
                continue
            # Guard 1 — never delete a span carrying source-language text. A true
            # AGES ghost is an English clause restarting after a bare reference
            # list; it never contains Greek/Hebrew. If the gap holds any Greek or
            # Hebrew, the repeated phrase is coincidental (two distinct sentences
            # that happen to share a 6-word run) and the Greek is genuine content
            # that must not be dropped. (v16: "that spake in the name of" recurs
            # around 2 Peter 2:1, ἐγένοντο ψευδοπροφῆται ἐν τῷ λαῷ.)
            if re.search(r'[Ͱ-Ͽἀ-῿֐-׿]', gap):
                continue
            # Guard 2 — a genuine ghost interruption is essentially just the
            # reference list. If, after removing the scripture references, the gap
            # still carries substantive prose (more than a few words), the two
            # occurrences are separate sentences, not a ghost restart — keep both.
            residual = SCRIPTURE_REF_RE.sub(' ', gap)
            residual_words = [w for w in re.findall(r"[A-Za-z]{2,}", residual)]
            if len(residual_words) > 3:
                continue
            cut_start = words[i + size - 1][2]
            cut_end = words[j + size - 1][2]
            return (text[:cut_start] + text[cut_end:]).strip()
    return text


def _remove_adjacent_repeated_word_runs(text):
    """Collapse adjacent ghost repeats inside a paragraph."""
    if not text or len(text) < 20:
        return text

    def tokens(value):
        return [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", value)
        ]

    previous = None
    while previous != text:
        previous = text
        words = tokens(text)
        changed = False
        max_size = min(14, len(words) // 2)
        for size in range(max_size, 1, -1):
            for i in range(0, len(words) - (size * 2) + 1):
                first = [w for w, _, _ in words[i:i + size]]
                second = [w for w, _, _ in words[i + size:i + (size * 2)]]
                if first != second:
                    continue
                useful = [w for w in first if len(w) > 2 or ':' in w]
                if len(useful) < 2:
                    continue
                cut_start = words[i + size][1]
                cut_end = words[i + (size * 2) - 1][2]
                while cut_start > 0 and text[cut_start - 1] in ' \t':
                    cut_start -= 1
                while cut_end < len(text) and text[cut_end] in ' \t,;:.':
                    cut_end += 1
                text = (text[:cut_start] + ' ' + text[cut_end:]).strip()
                changed = True
                break
            if changed:
                break
        if changed:
            continue
        text = re.sub(r'\b([A-Z][a-z]{3,})\s+\1\b', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text)


def post_process_paragraphs(paragraphs):
    """Clean paragraph-level artifacts after line healing."""
    # 1. Primary cleanup of OCR artifacts and noise
    pre_cleaned = []
    for para in paragraphs:
        stripped = para.strip()
        # Sweep 'stray letter' paragraphs (Issue 1)
        # standalone lowercase letters (often from Christ -> i, or headers)
        if re.match(r'^[a-z]\s*$', stripped):
            continue
        pre_cleaned.append(para)
    paragraphs = pre_cleaned

    cleaned = []
    for para in paragraphs:
        para = _remove_repeated_opening_clause(para.strip())
        para = _collapse_adjacent_duplicate_refs(para)
        
        # Aggressive book doubling fix (Issue 108/Audit)
        # Handles "Romans 8:29Romans" or "Hebrews 9:14Hebrews"
        para = re.sub(r'(\b(?:[1-3]\s+)?[A-Z][a-z]{3,}\s+\d+:\d+(?:[-,]\s*\d+)*)\s*([A-Z][a-z]{3,})\b', 
                      lambda m: m.group(1) if m.group(1).startswith(m.group(2)) else m.group(0), para)
        
        # Aggressive coordinate doubling fix (Issue 108/Audit)
        # Handles "Romans 8:29, 8:29" or "Romans 8:29 8:29"
        para = re.sub(r'(\b(?:[1-3]\s+)?[A-Z][a-z]{3,}\s+\d+:\d+(?:[-,]\s*\d+)*)[\s,;.]+(\d+:\d+(?:[-,]\s*\d+)*)\b',
                      lambda m: m.group(1) if m.group(1).endswith(m.group(2)) else m.group(0), para)
        
        para = _remove_interrupted_duplicate_clause(para)
        para = _repair_glued_scripture_book_references(para)
        para = _remove_duplicate_scripture_tail(para)
        para = _remove_adjacent_repeated_word_runs(para)
        # Catechism ghosts repaired in v1 overrides during rendering
        if not para:
            continue

        for part in _split_inline_structural_markers(para):
            if not part:
                continue

            if (
                cleaned
                and re.fullmatch(r'(?:Objection|Obj\.?|Answer|Ans\.?|Solution|Sol\.?)', cleaned[-1].strip(), re.I)
                and re.match(r'^\d+\.?\s+', part)
            ):
                label = cleaned[-1].strip()
                cleaned[-1] = f"{label} {part}".strip()
                continue

            if cleaned and _paragraph_needs_numeric_continuation(cleaned[-1], part):
                cleaned[-1] = _join_numeric_continuation(cleaned[-1], part)
                continue

            if cleaned and _is_citation_abbrev_continuation(cleaned[-1], part):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            if cleaned:
                recent_context = ' '.join(cleaned[-3:])
                part = _trim_duplicate_reference_prefix(recent_context, part)
                if not part:
                    continue

            if cleaned and _paragraph_needs_text_continuation(cleaned[-1], part):
                trimmed = _trim_overlapping_prefix(cleaned[-1], part)
                if (
                    trimmed != part
                    or _is_reference_continuation(cleaned[-1], part)
                    or not _is_terminal(cleaned[-1])
                    or re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b\s+', part)
                ):
                    cleaned[-1] = f"{cleaned[-1]} {trimmed}".strip()
                    continue

            if (
                cleaned
                and (
                    _is_scholarly_citation_fragment(cleaned[-1])
                    or _ends_with_scholarly_citation_sentence(cleaned[-1])
                )
                and re.match(r'^(?:But|And|For|Yea|Yet|So|Herein|Wherefore)\b', part)
            ):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            if cleaned and _is_probable_duplicate_fragment(cleaned[-1], part):
                continue

            if cleaned and _is_scripture_ref_fragment(part):
                para_norm = _norm_for_dedupe(part)
                prev_norm = _norm_for_dedupe(cleaned[-1])
                if para_norm and para_norm in prev_norm[-500:]:
                    continue
                para_refs = _scripture_ref_tokens(part)
                prev_refs = set(_scripture_ref_tokens(cleaned[-1]))
                if para_refs and prev_refs:
                    overlap = sum(1 for ref in para_refs if ref in prev_refs)
                    if overlap / len(para_refs) >= 0.6:
                        continue
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            # Owen-specific: Join short transitional paragraphs with the next one (Issue 1)
            # Match "But —", "For —", "And —", "Or —", etc.
            # Don't join if the next part is structural (Issue 1 Refinement)
            is_structural = part.startswith('[[')
            if cleaned and not is_structural and re.match(r'^(?:But|For|And|Or|Yea|Yet|So|Wherefore)\s*[—\-]\s*$', cleaned[-1].strip()):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            cleaned.append(part)
    return _remove_global_ngram_duplicates(cleaned)


def _remove_global_ngram_duplicates(paragraphs, size=14):
    """
    Remove non-consecutive paragraph-level duplicates using n-gram anchors.
    This catches 'interrupted' ghost layers that sequential de-duplication misses.
    """
    seen_anchor_pairs = set()
    cleaned = []
    for para in paragraphs:
        # Normalize for dedupe to avoid minor spacing/punctuation differences
        para_norm = _norm_for_dedupe(para)
        words = [w for w in re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", para_norm)]
        if len(words) < size:
            cleaned.append(para)
            continue

        # Check first and last n-gram of the paragraph
        first_anchor = tuple(words[:size])
        last_anchor = tuple(words[-size:])
        anchor_pair = (first_anchor, last_anchor)

        # Require BOTH anchors as a pair to match to be considered a ghost-layer duplicate (Issue 108/Audit)
        if anchor_pair in seen_anchor_pairs:
            continue

        seen_anchor_pairs.add(anchor_pair)
        cleaned.append(para)
    return cleaned


def deduplicate_junction(prev_text, next_text, threshold=0.85):
    """Lookback buffer: remove duplicate text at page junctions."""
    if not prev_text or not next_text:
        return next_text
    
    overlap_len = min(60, len(prev_text), len(next_text))
    if overlap_len < 15:
        return next_text
    
    prev_tail = prev_text[-overlap_len:].lower().strip()
    next_head = next_text[:overlap_len].lower().strip()
    
    matches = sum(1 for a, b in zip(prev_tail, next_head) if a == b)
    ratio = matches / max(len(prev_tail), len(next_head))
    
    if ratio >= threshold:
        cut = overlap_len
        while cut < len(next_text) and cut < overlap_len + 40:
            if next_text[:cut].lower().strip() == prev_tail:
                return next_text[cut:]
            cut += 1
        return next_text[overlap_len:].lstrip()
    
    return next_text


def get_pages_text(
    doc,
    pages_md,
    start_page,
    end_page,
    healer_mode=True,
    title="",
    chapter_id="",
    config=None,
    allow_treatise_title_page=True,
):
    """Get merged text for a range of pages with optional paragraph healing.

    Paragraph healing must be holistic across the full page range. Running
    reconstruction page-by-page forces false breaks at page boundaries.

    When healer_mode=False, returns clean raw text without paragraph
    reconstruction (used for layout-preserved front matter pages).
    """
    _page_h = (config or {}).get('page_height', None)
    raw_parts = []

    for pg in range(start_page, min(end_page + 1, len(doc))):
        raw = get_merged_page_text(
            doc,
            pages_md,
            pg,
            allow_treatise_title_page=allow_treatise_title_page,
            page_height=_page_h,
        )
        if not raw.strip():
            continue
        raw_parts.append(raw)
    
    if not raw_parts:
        return ''

    # Clean and heal the whole chapter/range at once so sentences that cross
    # PDF page boundaries stay inside the same EPUB paragraph.
    cleaned = clean_text('\n'.join(raw_parts), config=config)
    if not cleaned:
        return ''

    return '\n\n'.join(reconstruct_paragraphs(cleaned))


def _build_flat_chapters(doc, pages_md, footnote_map):
    """Fallback: create one chapter per PDF page."""
    chapters = []
    for pg in range(len(doc)):
        text = get_merged_page_text(doc, pages_md, pg)
        if not text.strip():
            continue
        page_num = pg + 1
        chapters.append(Chapter(
            cid=f'page{page_num:04d}',
            title=f'Page {page_num}',
            level=2,
            raw_text=text,
            body_html=f'<p>{_html_escape(text.strip())}</p>',
            page_start=pg,
            page_end=pg,
        ))
    return chapters


# ================================================================
# STAGE 1 ENTRY POINT — extract_volume()
# ================================================================

def extract_volume(vol_num: int, overrides: dict = None,
                   progress_callback=None) -> dict:
    """Run Stage 1 for a single Owen volume: PDF → JSON intermediate.

    Writes volumes/vN/intermediate/volume_N.json and returns the dict.
    The JSON is the contract between Stage 1 (extract) and Stage 2 (render).

    overrides: optional per-volume config additions (see volumes/vN/convert.py).
    """
    import pymupdf4llm
    from shared import merge_volume_config
    from render import (
        detect_page_type, is_toc_continuation_page,
        format_title_page, build_toc_page_xhtml,
    )

    config = merge_volume_config(vol_num, overrides)
    vol_dir = _EXTRACT_DIR / 'volumes' / f'v{vol_num}'
    pdf_path = vol_dir / 'input' / f'owen-v{vol_num}.pdf'
    thml_path = vol_dir / 'intermediate' / f'volume_{vol_num}.thml.xml'
    out_json = vol_dir / 'intermediate' / f'volume_{vol_num}.json'

    print(f'[extract] Volume {vol_num}: opening {pdf_path.name}')
    doc = fitz.open(str(pdf_path))
    pages_md = pymupdf4llm.to_markdown(doc, page_chunks=True)

    # Footnotes
    pdf_footnotes = extract_footnotes_from_pdf(doc)
    thml_footnotes = parse_thml_footnotes(str(thml_path)) if thml_path.exists() else {}
    footnote_map = merge_footnotes(pdf_footnotes, thml_footnotes)

    # Chapter structure from TOC
    nav_entries = extract_ages_nav(doc, config=config)
    chapters = build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map,
                                       config=config, vol_num=vol_num,
                                       progress_callback=progress_callback)

    # Determine front-matter prose style per chapter
    _FM_PROSE_KEYWORDS = [
        'PREFACE', 'PREFATORY NOTE', 'PREFATORY', 'ANALYSIS',
        'TO THE READER', 'ADVERTISEMENT', 'GENERAL PREFACE',
    ]
    chapter_dicts = []
    for ch in chapters:
        title_upper = ch.title.upper()
        if any(kw in title_upper for kw in _FM_PROSE_KEYWORDS):
            fm_style = 'prose'
        else:
            fm_style = None  # body chapter — no FM styling
        chapter_dicts.append({
            'cid': ch.cid,
            'title': ch.title,
            'level': ch.level,
            'page_start': ch.page_start,
            'page_end': ch.page_end,
            'is_treatise': ch.is_treatise,
            'is_endnotes': ch.is_endnotes,
            'front_matter_style': fm_style,
            'raw_text': ch.raw_text or '',
        })

    # Front matter pages (title pages, TOC pages)
    scan_limit = min(config.get('front_matter_pages', 25), len(doc))
    chapter_pages = {p for ch in chapters
                     for p in range(ch.page_start, ch.page_end + 1)}
    front_matter_items = []
    pg = 0
    while pg < scan_limit:
        page = doc[pg]
        ptype = detect_page_type(page, pg + 1)
        toc_like = ptype == 'toc_page'  # continuation detection runs only in the inner loop
        if pg in chapter_pages:
            pg += 1
            continue
        text_upper = page.get_text().upper()
        blocks = page.get_text('dict')['blocks']
        text_blocks = [b for b in blocks if b.get('type') == 0]
        n_blocks = len(text_blocks)
        if ptype == 'title_page':
            html_body = format_title_page(page)
            front_matter_items.append({
                'type': 'title_page',
                'file_name': f'title_{pg}.xhtml',
                'title': f'Title Page',
                'page': pg,
                'html': html_body,
            })
        elif toc_like:
            toc_pages = [doc[pg]]
            j = pg + 1
            while j < scan_limit and j not in chapter_pages:
                if is_toc_continuation_page(doc[j], j + 1):
                    toc_pages.append(doc[j])
                    j += 1
                else:
                    break
            html_body = build_toc_page_xhtml(toc_pages)
            front_matter_items.append({
                'type': 'toc',
                'file_name': f'contents_{pg}.xhtml',
                'title': 'Contents',
                'page': pg,
                'html': html_body,
            })
            pg = j
            continue
        else:
            has_indicator = any(kw in text_upper for kw in
                                ['PREFACE', 'CHAPTER', 'TREATISE', 'CATECHISM', 'DISCOURSE'])
            if has_indicator and n_blocks > 10:
                break
        pg += 1

    # Footnote map → serialisable dict
    fn_dict = {
        str(f.fnum): {'text': f.text, 'source': f.source}
        for f in footnote_map.values()
    }

    intermediate = {
        'volume': vol_num,
        'title': config.get('title', f'The Works of John Owen, Volume {vol_num}'),
        'meta': {
            'pages': len(doc),
            'chapters_count': len(chapter_dicts),
            'extracted_at': datetime.now().isoformat(),
        },
        'chapters': chapter_dicts,
        'footnotes': fn_dict,
        'front_matter_items': front_matter_items,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(intermediate, f, ensure_ascii=False, indent=2)
    print(f'[extract] Written: {out_json}')
    return intermediate


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Stage 1: PDF → JSON intermediate for Owen volumes")
    parser.add_argument("volumes", nargs="*", type=int, help="Volume number(s) to extract")
    parser.add_argument("--all", action="store_true", help="Extract all 16 volumes")
    args = parser.parse_args()

    vols = list(range(1, 17)) if args.all else (args.volumes or [1])
    for v in vols:
        extract_volume(v)
