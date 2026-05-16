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
)

# Re-import rendering constants that extraction code also uses
from render import (
    SCRIPTURE_BOOK_RE, SCRIPTURE_REF_RE, SCRIPTURE_CONTINUATION_TRAIL_RE,
    FOOTNOTE_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE, FOOTNOTE_PLACEHOLDER_RE,
    FT_MARKER_RE, EMPTY_BRACKET_RE,
    STRUCTURAL_START_RE, CITATION_ABBREV_TRAIL_RE,
    CITATION_ABBREV_START_RE, CITATION_AUTHOR_TRAIL_RE,
    MARKDOWN_STRUCTURAL_START_RE, ROMAN_LIST_TOKEN, PLAIN_CHAPTER_RE,
    INLINE_STRUCTURAL_MARKER_RE, ROMAN_HEADING_RE, ROMAN_ONLY_RE,
    _is_scripture_ref_fragment, _scripture_ref_tokens,
    _split_inline_structural_markers, _repair_known_catechism_ghosts,
    _trim_duplicate_reference_prefix, _norm_for_dedupe,
    _normalize_spaced_caps, _normalize_i_will, _repair_owen_ocr_errors,
    title_case, nav_display_title,
)

try:
    import fitz
except ImportError:
    sys.exit("Error: PyMuPDF (fitz) not installed. Run: pip install pymupdf4llm")
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

GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}

# ================================================================
# AGES VERSE MARKER TRANSLATION
# ================================================================

# AGES Software encodes Bible references as <BBCCVV> or <BBBCCVV> where
# BB/BBB = book code (1-based), CC = chapter (zero-padded), VV = verse.
_AGES_BOOK_NAMES = {
    1: 'Genesis', 2: 'Exodus', 3: 'Leviticus', 4: 'Numbers',
    5: 'Deuteronomy', 6: 'Joshua', 7: 'Judges', 8: 'Ruth',
    9: '1 Samuel', 10: '2 Samuel', 11: '1 Kings', 12: '2 Kings',
    13: '1 Chronicles', 14: '2 Chronicles', 15: 'Ezra', 16: 'Nehemiah',
    17: 'Esther', 18: 'Job', 19: 'Psalms', 20: 'Proverbs',
    21: 'Ecclesiastes', 22: 'Song of Solomon', 23: 'Isaiah', 24: 'Jeremiah',
    25: 'Lamentations', 26: 'Ezekiel', 27: 'Daniel', 28: 'Hosea',
    29: 'Joel', 30: 'Amos', 31: 'Obadiah', 32: 'Jonah', 33: 'Micah',
    34: 'Nahum', 35: 'Habakkuk', 36: 'Zephaniah', 37: 'Haggai',
    38: 'Zechariah', 39: 'Malachi',
    40: 'Matthew', 41: 'Mark', 42: 'Luke', 43: 'John', 44: 'Acts',
    45: 'Romans', 46: '1 Corinthians', 47: '2 Corinthians', 48: 'Galatians',
    49: 'Ephesians', 50: 'Philippians', 51: 'Colossians',
    52: '1 Thessalonians', 53: '2 Thessalonians',
    54: '1 Timothy', 55: '2 Timothy', 56: 'Titus', 57: 'Philemon',
    58: 'Hebrews', 59: 'James', 60: '1 Peter', 61: '2 Peter',
    62: '1 John', 63: '2 John', 64: '3 John', 65: 'Jude', 66: 'Revelation',
}

# Matches standard decimal AGES codes (6-9 digits) AND the Psalms hex-chapter
# variant where chapters 100-159 are encoded with a hex letter at position 2:
#   <19A225> = Psalms 102:25  (A=10 → ch = 10*10+2 = 102, v = 25)
#   <19B822> = Psalms 118:22  (B=11 → ch = 11*10+8 = 118, v = 22)
#   <19D504> = Psalms 135:4   (D=13 → ch = 13*10+5 = 135, v = 4)
# The hex letter appears only at position 2 of the code (after the 2-digit book).
_AGES_MARKER_RE = re.compile(r'<(\d{2}[0-9A-Fa-f]\d{3,6})>')

# Context-aware pattern: captures the code AND any immediately-following
# book+chapter:verse text so we can detect when the PDF already has the
# human-readable form right after the numeric code (both layers present).
# Group 1 = code (may include a hex letter), Group 2 = optional following ref text.
_AGES_MARKER_CONTEXT_RE = re.compile(
    r'<(\d{2}[0-9A-Fa-f]\d{3,6})>(\s*(?:[1-3]?\s*[A-Z][a-zA-Z ]{1,30}?\s+)?\d+:\d+(?:[-,]\s*\d+)*)?'
)

# Hex-letter → century value for the Psalms chapter encoding.
_HEX_CHAPTER_MAP = {
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
}


def _translate_ages_marker(code_str: str) -> str:
    """Translate an AGES verse code to a readable Bible reference.

    Standard format: BBCCVV (6 digits) or BBBCCVV (7 digits) where
      BB/BBB = book number (decimal), CC = chapter, VV = verse.

    Psalms hex-chapter variant: 19XDVV where X is a hex letter A-F
      encoding the hundreds-of-chapter digit:
        19A225 → Psalms 102:25  (A=10, ch = 10*10+2 = 102)
        19B822 → Psalms 118:22  (B=11, ch = 11*10+8 = 118)
        19D504 → Psalms 135:4   (D=13, ch = 13*10+5 = 135)

    Example: 430316 → John 3:16  (43 = John, 03 = ch 3, 16 = v 16)
    Example: 1842077 → Job 42:7  (18 = Job, 42 = ch 42, 07 = v 7)
    """
    if not code_str:
        return f'[{code_str}]'

    # Detect Psalms hex-chapter encoding: 2 decimal digits + 1 hex letter + 3 digits
    # e.g. "19B822" — positions: [0:2]=book, [2]=hex_letter, [3]=ch_units, [4:6]=verse
    if len(code_str) == 6 and code_str[2].upper() in _HEX_CHAPTER_MAP:
        try:
            book_n = int(code_str[:2])
            hex_val = _HEX_CHAPTER_MAP[code_str[2]]
            ch_n = hex_val * 10 + int(code_str[3])
            v_n = int(code_str[4:6])
            book_name = _AGES_BOOK_NAMES.get(book_n)
            if book_name:
                if ch_n == 0 and v_n == 0:
                    return book_name
                if v_n == 0:
                    return f'{book_name} {ch_n}'
                return f'{book_name} {ch_n}:{v_n}'
        except (ValueError, IndexError):
            pass
        return f'[{code_str}]'

    # Standard all-decimal path
    s = code_str.lstrip('0')
    if not s:
        return f'[{code_str}]'

    try:
        # 7+ digit split: BBB CC VV  (or BB CCC VV for large chapters)
        if len(code_str) >= 7:
            book_n = int(code_str[:-4])
            ch_n = int(code_str[-4:-2])
            v_n = int(code_str[-2:])
        else:
            # 6-digit split: BB CC VV
            book_n = int(code_str[:-4])
            ch_n = int(code_str[-4:-2])
            v_n = int(code_str[-2:])
    except ValueError:
        return f'[{code_str}]'

    book_name = _AGES_BOOK_NAMES.get(book_n)
    if not book_name:
        # Unknown book code — preserve escaped form so audit catches it
        return f'[{code_str}]'
    if ch_n == 0 and v_n == 0:
        return book_name
    if v_n == 0:
        return f'{book_name} {ch_n}'
    return f'{book_name} {ch_n}:{v_n}'


def translate_ages_verse_markers(text: str) -> str:
    """Replace all AGES verse marker codes with readable Bible references.

    <430316> → John 3:16
    Unknown codes are preserved as [NNNNNN] so the audit can flag them.

    Context-aware: AGES PDFs sometimes encode a reference as both a numeric
    code AND the already-decoded human-readable text immediately following it
    (two layers in the same PDF text stream). When the following text starts
    with the same reference as the translated code — possibly with a richer
    verse range like "1 Peter 2:6-8" vs bare "1 Peter 2:6" — the code is
    suppressed and only the already-present text is kept, preventing doubling
    such as "Isaiah 9:6Isaiah 9:6".
    """
    def _norm_for_cmp(s: str) -> str:
        """Normalise a reference string for dedup comparison.

        Collapses whitespace, lowercases, and strips a trailing 's' from the
        book name so that 'Psalm'/'Psalms' and 'Samuel'/'Samuels' etc. compare
        equal regardless of which form the PDF uses.
        """
        s = re.sub(r'\s+', ' ', s).lower().strip()
        # Strip trailing 's' from the book-name portion (before the chapter number)
        s = re.sub(r's\b(?=\s+\d)', '', s, count=1)
        return s

    def _repl(m: re.Match) -> str:
        code = m.group(1)
        following = m.group(2) or ''
        translated = _translate_ages_marker(code)
        
        # Check if 'chap.' or 'chapter' precedes the match in the full text
        # by looking at the characters before m.start()
        start_idx = m.start()
        # Look back for book name to avoid doubling (Issue 108/Audit)
        preceding_full = text[max(0, start_idx-60):start_idx].lower()
        has_chap_prefix = bool(re.search(r'\b(?:chap|chapter)\.?\s*$', preceding_full))
        
        # Extract book name from translation for comparison
        book_match = re.match(r'([1-3]?\s*[A-Z][a-zA-Z ]{1,30}?)[\s,;.]+\d', translated)
        book_name = book_match.group(1).strip() if book_match else ''
        book_norm = _norm_for_cmp(book_name) if book_name else ''
        
        # If the book name already appears right before the marker, don't prepend it
        # Handle cases like "Romans 8:29 <450829>" (Issue 108/Audit)
        already_has_book = book_norm and (book_norm in preceding_full)

        if following:
            norm_following = _norm_for_cmp(following)

            # If following already starts with the book name, it's a duplicate (Issue 108/Audit)
            if book_norm and book_norm in norm_following:
                return following

            norm_translated = _norm_for_cmp(translated)            
            # Match the first reference coordinate in the following text
            # Allow optional punctuation after book name (Issue 108/Audit)
            match = re.match(r'((?:[1-3]?\s*[a-z][a-z ]{1,30}?)[,;.]?\s+)?(\d+:\d+|\d+)', norm_following)
            if match:
                base_following = match.group(0).strip()
                
                # Check for internal repetition in the following layer (Issue 26)
                # e.g. "16:1516:15" or "John 16:15John 16:15"
                if len(norm_following) >= 10:
                    half = len(norm_following) // 2
                    if norm_following[:half] == norm_following[half:]:
                        following = following[:half]
                        norm_following = norm_following[:half]
                        match = re.match(r'((?:[1-3]?\s*[a-z][a-z ]{1,30}?)[,;.]?\s+)?(\d+:\d+|\d+)', norm_following)
                        if match:
                             base_following = match.group(0).strip()

                if norm_translated.startswith(base_following) or norm_translated.endswith(base_following):
                    # It's a duplicate. We keep the `following` text.
                    # If the following text didn't have a book name, prepend the book name from the translation
                    # ONLY IF 'chap.' wasn't already there.
                    if not match.group(1) and not has_chap_prefix and not already_has_book:
                        if book_name:
                            return book_name + ' ' + following
                    return following
        # If the book name already appears right before the marker, don't prepend it
        if already_has_book:
            # Extract just the chapter:verse from translated
            coord_match = re.search(r'\d+:\d+', translated)
            if coord_match:
                coord = coord_match.group(0)
                # If following already starts with the coordinate, it's a duplicate (Issue 108/Audit)
                # e.g. "Romans 8:29 <450829>8:29, 30" -> "Romans 8:29, 30"
                follow_strip = following.lstrip()
                if follow_strip.startswith(coord):
                    return follow_strip[len(coord):]
                if follow_strip.startswith(',' + coord):
                    return follow_strip[len(coord)+1:]
                if follow_strip.startswith(';' + coord):
                    return follow_strip[len(coord)+1:]
                
                # Return only the coordinate if book name is already present
                return coord_match.group(0) + following
            # If no coordinate match, but book is already there, return following as is
            return following

        return translated + following

    return _AGES_MARKER_CONTEXT_RE.sub(_repl, text)

def coordinate_redactor(blocks, page_height=PAGE_H, top_margin=TOP_MARGIN, bottom_margin=BOTTOM_MARGIN):
    """
    Filter out text blocks that overlap the top `top_margin` pts
    or bottom `bottom_margin` pts of the page.

    Uses LINE-level filtering within blocks: only keeps lines whose
    vertical midpoint is inside the safe reading zone [top_margin, page_h - bottom_margin].
    This preserves content like 'CONTENTS OF VOLUME 1' (y≈62) while removing
    page numbers (y≈30) and AGES header blocks (y≈26-75).
    """
    keep = []
    for b in blocks:
        if b.get('type') != 0:
            continue
        keep_lines = []
        for line in b['lines']:
            y_center = (line['bbox'][1] + line['bbox'][3]) / 2
            line_text = ''.join(span.get('text', '') for span in line.get('spans', [])).strip()
            
            # PROTECTIVE MARGINS: If a line is in the margin zone but looks like 
            # substantial body text (not a header/footer), keep it.
            is_header_footer = (
                re.fullmatch(r'\d{1,4}', line_text)
                or re.search(
                    r'THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|'
                    r'JOHN OWEN COLLECTION|BOOKS FOR THE AGES|AGES SOFTWARE|'
                    r'VERSION \d\.\d|VOLUME \d+',
                    line_text,
                    re.I,
                )
            )
            
            # Bottom safety: Owen's footnotes or low body lines often sit at y=580-605
            if y_center > page_height - 70 and not is_header_footer and len(line_text) > 10:
                keep_lines.append(line)
                continue

            if y_center < top_margin and not is_header_footer:
                # Top safety: don't clip lines that might be part of a chapter head
                if y_center > 25 and len(line_text) > 20:
                    keep_lines.append(line)
                    continue
                continue
            
            if is_header_footer and (y_center < 75 or y_center > page_height - 75):
                continue

            if top_margin <= y_center <= page_height - bottom_margin:
                keep_lines.append(line)
        if keep_lines:
            # Rebuild block with only kept lines
            new_block = dict(b)
            new_block['lines'] = keep_lines
            # Recalculate bbox from kept lines
            if keep_lines:
                x0 = min(l['bbox'][0] for l in keep_lines)
                y0 = min(l['bbox'][1] for l in keep_lines)
                x1 = max(l['bbox'][2] for l in keep_lines)
                y1 = max(l['bbox'][3] for l in keep_lines)
            new_block['bbox'] = (x0, y0, x1, y1)
            keep.append(new_block)
    return keep


def extract_ages_nav(doc, config=None):
    """
    Extract navigation hierarchy from the PDF's internal outline/bookmarks.
    Returns list of (level, title, page_num_0indexed).
    
    Falls back to parsing the visual 'CONTENTS OF VOLUME' page if outline is empty.
    """
    toc = doc.get_toc()
    if toc:
        nav = []
        for item in toc:
            level, title, page = item
            if page < 1:
                continue  # skip entries with no page (-1)
            nav.append((level, title.strip(), page - 1))  # convert to 0-indexed
        if nav:
            return nav

    # Fallback: parse the visual TOC from the CONTENTS page
    for pg in range(len(doc)):
        page = doc[pg]
        text = page.get_text()
        if 'CONTENTS OF VOLUME' in text:
            return _parse_visual_toc(doc, pg, config=config)
    return []


def _parse_visual_toc(doc, toc_page_num, config=None):
    """
    Parse the visual 'CONTENTS OF VOLUME' page to extract chapter titles
    and map them to PDF page numbers.
    """
    from collections import OrderedDict
    nav = []
    page = doc[toc_page_num]
    blocks = page.get_text('dict')['blocks']
    
    lines = []
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            text = ''.join(s['text'] for s in line['spans']).strip()
            if text:
                lines.append(text)
    
    # Try to find page numbers for each chapter by scanning through pages
    toc_entries = []
    current_treatise = None
    configured_treatises = (config or {}).get('treatises', [])
    
    for text in lines:
        text_upper = text.upper()
        if 'CONTENTS OF VOLUME' in text_upper:
            continue
        # Match chapter patterns
        ch_match = re.match(r'^(CHAPTER\s+\d+)\.?\s*(.*)', text, re.I)
        if ch_match:
            toc_entries.append((2, ch_match.group(1).strip(), ''))
            continue
        # Roman numeral subsections
        roman_match = re.match(r'^([IVXLCDM]+)\.\s+(.*)', text)
        if roman_match:
            toc_entries.append((3, text.strip(), ''))
            continue
        
        # Match against configured treatises (Issue 108)
        matched_treatise = None
        for t in configured_treatises:
            if t.upper() in text_upper or text_upper in t.upper():
                matched_treatise = t
                break
        
        if matched_treatise or (text_upper == text and len(text) > 5 and len(text) < 60):
            toc_entries.append((1, text.strip(), ''))
            current_treatise = text
            continue
        
        # Prefatory notes, prefaces
        if text_upper in ('PREFATORY NOTE', 'PREFACE', 'ORIGINAL PREFACE') or 'PREFATORY' in text_upper:
            toc_entries.append((2, text.strip(), ''))
            continue
    
    # Map entries to pages by scanning document
    for i, entry in enumerate(toc_entries):
        level, title, _ = entry
        # Find the page this title appears on
        search_title = re.sub(r'[—–:]', '', title).strip()
        for pg in range(len(doc)):
            pg_text = doc[pg].get_text()
            if search_title.upper() in pg_text.upper():
                nav.append((level, title, pg))
                break
    
    return nav


# ================================================================
# STAGE 3: Font-Aware Text Extraction + Greek/Hebrew Conversion
# ================================================================

def page_has_special_fonts(page):
    """Check if a PyMuPDF page contains Greek or Hebrew font spans."""
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if b['type'] != 0:
            continue
        for line in b['lines']:
            for span in line['spans']:
                font = span.get('font', '')
                if any(gf in font for gf in GREEK_FONTS):
                    return 'greek'
                if any(hf in font for hf in HEBREW_FONTS):
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
    return False


def extract_structural_page(page, page_height=PAGE_H):
    """
    Robust extraction for pages with structural elements (Part/Chapter starts).
    Groups same-type lines to avoid fragmentation and uses explicit tokens.
    """
    blocks = page.get_text('dict')['blocks']
    blocks = coordinate_redactor(blocks, page_height)
    
    output_lines = []
    current_kind = None
    current_text_parts = []
    in_heading_section = True
    waiting_for_summary = False  # Track if we just hit a CHAPTER (Issue 108/Audit)

    def flush():
        nonlocal current_kind, current_text_parts
        if not current_text_parts:
            return
            
        # Join major structural elements with space to keep them unified (Issue 108/Audit)
        if current_kind in ('PART', 'CHAPTER', 'SUMMARY', 'SUBTITLE', 'DIGRESSION'):
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

    for b in blocks:
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
                elif (color == COLOR_GREEN or color == 0) and 13.5 <= size <= 14.5:
                    # Specific pattern for Roman heads to avoid catching body lines
                    # ONLY match standalone Roman numerals as headings (Issue 12/19)
                    if re.match(r'^[IVXLCDM]+\.?$', text.strip()):
                        line_is_roman_head = True
                elif color == COLOR_RED and size > 15:
                    line_is_volume = True

            line_text = ''.join(spans_text).strip()
            if not line_text:
                continue

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
                
            # Roman head detection: must be a standalone Roman numeral (Issue 12/19)
            if line_is_roman_head and not re.match(r'^[IVXLCDM]+\.?$', line_text):
                line_is_roman_head = False
                
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
            elif line_is_roman_head: 
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
            
            if kind != 'PLAIN':
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
            
            if kind != current_kind:
                # Always flush on kind change in structural pages to preserve 
                # explicit formatting intent.
                if current_text_parts:
                    flush()
                current_kind = kind
            current_text_parts.append(line_text)
                
    flush()
    return '\n'.join(output_lines)

def convert_span_text(text, font):
    """Convert text based on font encoding."""
    font_upper = font.upper()
    if any(gf.upper() in font_upper for gf in GREEK_FONTS):
        return convert_greek_word(text)
    if any(hf.upper() in font_upper for hf in HEBREW_FONTS):
        return convert_gideon_hebrew(text)
    return text


def extract_page_text_with_fonts(page, page_height=PAGE_H):
    """
    Extract text from a page using raw PyMuPDF, filtering by coordinates
    and converting Greek/Hebrew font spans.
    """
    blocks = page.get_text('dict')['blocks']
    blocks = coordinate_redactor(blocks, page_height)
    
    lines = []
    for b in blocks:
        for line in b['lines']:
            spans_text = []
            for span in line['spans']:
                text = span['text']
                font = span.get('font', '')
                converted = convert_span_text(text, font)
                spans_text.append(converted)
            line_text = ''.join(spans_text).strip()
            if line_text:
                lines.append(line_text)
    
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


def get_merged_page_text(doc, pages_md, page_idx):
    """
    Get text for a page:
    - For structural pages (Part/Chapter starts): use specialized extraction.
    - For inner treatise title pages: use specialized formatting.
    - For Greek/Hebrew pages: use font-aware extraction.
    - For regular pages: use PyMuPDF4LLM Markdown.
    """
    from render import (
        detect_page_type, format_treatise_title_page,
    )
    page = doc[page_idx]
    ptype = detect_page_type(page, page_idx + 1)
    
    if ptype == 'treatise_title_page':
        return format_treatise_title_page(page)

    is_struct = page_is_structural(page)
    font_type = page_has_special_fonts(page)
    md_text = extract_page_markdown(pages_md, page_idx)
    
    if is_struct:
        return extract_structural_page(page)
    
    if font_type:
        raw_text = extract_page_text_with_fonts(page)
        # Preserve [fN] markers from Markdown that might be lost in raw text
        fn_markers = FOOTNOTE_MARKER_RE.findall(md_text)
        # Also check for standalone [fN] markers on their own lines
        for fn in fn_markers:
            marker = f'[f{fn}]'
            if marker not in raw_text:
                raw_text += f' {marker}'
        return raw_text
    else:
        return md_text

@dataclass
class Footnote:
    fnum: int
    text: str
    source: str = 'pdf'       # 'pdf' or 'thml'
    pages: list = field(default_factory=list)  # PDF pages where referenced

def _converted_pdf_line(line):
    converted_parts = []
    for span in line['spans']:
        span_text = span['text']
        font = span.get('font', '')
        if any(gf in font for gf in GREEK_FONTS):
            span_text = convert_greek_word(span_text)
        elif any(hf in font for hf in HEBREW_FONTS):
            span_text = convert_gideon_hebrew(span_text)
        converted_parts.append(span_text)
    return ''.join(converted_parts).strip()


def _page_has_ages_footnote_marker(page):
    for block in page.get_text('dict').get('blocks', []):
        if block.get('type') != 0:
            continue
        for line in block.get('lines', []):
            line_text = ''.join(s['text'] for s in line.get('spans', [])).strip()
            if FT_MARKER_RE.match(line_text):
                return True
    return False


def _find_ages_footnote_start_page(doc):
    """Find the AGES back-matter footnote section, with a marker fallback."""
    heading_pages = [
        pg for pg in range(len(doc))
        if 'FOOTNOTES' in doc[pg].get_text().upper()
    ]
    if heading_pages:
        return heading_pages[0]

    # Some AGES PDFs omit or garble the heading but still use ftN markers in
    # the back matter. Limit the fallback to the tail of the book so inline
    # prose cannot be mistaken for note text.
    tail_start = max(0, len(doc) - 20)
    for pg in range(tail_start, len(doc)):
        if _page_has_ages_footnote_marker(doc[pg]):
            return pg
    return None


def extract_footnotes_from_pdf(doc):
    """
    Extract AGES footnotes from the PDF back matter.

    The normal AGES scheme is a FOOTNOTES section whose notes begin with
    ftN/FTN markers. A fallback also recognizes those markers in the final
    pages when the section heading is missing or damaged.
    """
    footnotes = {}
    current_fn = None
    current_text = []
    start_page = _find_ages_footnote_start_page(doc)
    
    if start_page is None:
        return footnotes

    for pg in range(start_page, len(doc)):
        page = doc[pg]
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if b['type'] != 0:
                continue
            for line in b['lines']:
                line_text = ''.join(s['text'] for s in line['spans'])
                line_text = line_text.strip()
                
                if not line_text:
                    continue
                
                line_text_converted = _converted_pdf_line(line)
                if not line_text_converted:
                    continue
                
                # Check for FT marker in raw text (before conversion might mess it up)
                line_text_raw = ''.join(s['text'] for s in line['spans']).strip()
                ft_match = FT_MARKER_RE.match(line_text_raw)
                
                if ft_match:
                    # Save previous footnote
                    if current_fn is not None and current_text:
                        footnotes[current_fn] = ' '.join(current_text).strip()
                    
                    current_fn = int(ft_match.group(1))
                    # Use converted text for the content part
                    rest = line_text_converted[ft_match.end():].strip()
                    current_text = [rest] if rest else []
                elif current_fn is not None:
                    current_text.append(line_text_converted)
    
    # Save last footnote
    if current_fn is not None and current_text:
        combined = ' '.join(current_text).strip()
        if combined:
            footnotes[current_fn] = combined
    
    return footnotes


def parse_thml_footnotes(thml_path):
    """Parse existing ThML XML FOOTNOTES section for enriched footnote text."""
    from lxml import etree
    footnotes = {}

    if not os.path.exists(thml_path):
        return footnotes

    try:
        parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=True)
        root = etree.parse(thml_path, parser).getroot()

        # Find all fnmarkers anywhere in the document
        markers = root.xpath('.//a[@class="fnmarker"]')
        for i, marker in enumerate(markers):
            fn_num = int(marker.get('data-fn', '0') or 0)
            if not fn_num:
                continue

            parts = []
            # Use a stateful approach: collect everything until the next marker
            # We look for all text nodes and other elements between this marker and the next
            # We'll use the markers list to define boundaries

            # Start collecting from this marker's position
            next_marker = markers[i+1] if i + 1 < len(markers) else None

            def get_all_text_between(start_node, end_node):
                collected = []

                # 1. Start with start_node's tail
                if start_node.tail:
                    collected.append(start_node.tail)

                # 2. Iterate through siblings and their descendants
                curr = start_node
                while curr is not None:
                    # Move to next sibling
                    sibling = curr.getnext()
                    if sibling is None:
                        # Go up to parent's next sibling
                        curr = curr.getparent()
                        if curr is None or curr == root:
                            break
                        # When moving to a new paragraph/div, add a newline
                        if curr.tag in ('p', 'div', 'div1', 'div2'):
                            collected.append('\n\n')
                        continue

                    if sibling == end_node:
                        break

                    # Does this sibling contain the end_node?
                    if end_node is not None and end_node in sibling.xpath('.//*'):
                        # Need to recurse into this sibling to find exact boundary
                        # But simpler: just get text until end_node
                        for sub_node in sibling.xpath('.//text() | .//*'):
                             if sub_node == end_node:
                                 break
                             # (This is getting complex, let's use a simpler approach)
                             pass
                        break

                    # Add all text from this sibling
                    collected.append(''.join(sibling.itertext()))
                    if sibling.tail:
                        collected.append(sibling.tail)
                    curr = sibling

                return ''.join(collected)

            # Simpler approach: use xpath to get all following text/elements
            # and stop when we see the next marker.
            # Actually, let's use a very simple paragraph-based heuristic again
            # but fix the "sibling" vs "descendant" issue.

            parts = []
            if marker.tail:
                parts.append(marker.tail)

            # Collect following siblings in same parent
            curr = marker.getnext()
            found_next = False
            while curr is not None:
                if curr.tag == 'a' and curr.get('class') == 'fnmarker':
                    found_next = True
                    break
                parts.append(''.join(curr.itertext()))
                if curr.tail:
                    parts.append(curr.tail)
                curr = curr.getnext()

            # If we didn't hit a marker in the same paragraph, check following paragraphs
            if not found_next:
                p = marker.getparent()
                while p is not None:
                    next_p = p.getnext()
                    if next_p is None:
                        break
                    # If this paragraph has a marker, stop.
                    # IMPORTANT: it might have multiple markers, we stop at the first one.
                    m_in_next = next_p.xpath('.//a[@class="fnmarker"]')
                    if m_in_next:
                        # Add text BEFORE the first marker in this paragraph
                        first_m = m_in_next[0]
                        # This part is tricky. Let's just take the whole paragraph if
                        # the marker is at the very end, or if it's the marker we want?
                        # No, if it has ANY marker, it belongs to the next footnote.
                        break

                    parts.append('\n\n' + ''.join(next_p.itertext()))
                    p = next_p

            text = re.sub(r'[ \t]+', ' ', ''.join(parts)).strip()
            if text:
                footnotes[fn_num] = text
    except Exception as e:
        print(f"  Warning: Could not parse ThML footnotes: {e}")

    return footnotes
def merge_footnotes(pdf_footnotes, thml_footnotes):
    """
    Merge footnotes from PDF and ThML, preferring ThML for quality.
    """
    all_nums = set(pdf_footnotes.keys()) | set(thml_footnotes.keys())
    merged = {}
    for num in sorted(all_nums):
        text = thml_footnotes.get(num) or pdf_footnotes.get(num) or ''
        merged[num] = Footnote(
            fnum=num,
            text=text,
            source='thml' if num in thml_footnotes else 'pdf'
        )
    return merged


def find_footnote_refs_in_text(text):
    """
    Find [fN] footnote markers in text and return (cleaned_text, list of fn_numbers).
    """
    markers = FOOTNOTE_MARKER_RE.findall(text)
    fn_nums = [int(m) for m in markers]
    cleaned = FOOTNOTE_MARKER_RE.sub('', text)
    return cleaned, fn_nums


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


def build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map, config=None):
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
        r'^(Owen Librarian|The Works of John Owen|Contents)$|'
        r'^The Works of John Owen\s*[-–]', re.I
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
        # Determine if this is a treatise title page
        title_upper = title.upper()
        
        # Use relative matching against configured treatises (Issue 108)
        # We check if the TOC title contains any of our configured treatise titles
        matched_treatise = None
        for t in configured_treatises:
            if t.upper() in title_upper or title_upper in t.upper():
                matched_treatise = t
                break
                
        is_treatise = bool(matched_treatise) or any(kw in title_upper for kw in ['PART', 'BOOK'])
        
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
        raw_text = get_pages_text(doc, pages_md, page_0idx, end_page, title=title, config=config)
        
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
                
                # Find all markers
                markers = list(re.finditer(r'\[\[(?:PART|CHAPTER|DIGRESSION|ROMAN_HEAD|SUBTITLE|SUMMARY)\]\]', raw_text))
                if len(markers) > 1:
                    # Find the first 'major' marker after the initial one to truncate at.
                    # If current is PART/TREATISE, we stop at the next CHAPTER or PART.
                    truncate_at = len(raw_text)
                    for m in markers[1:]:
                        kind = m.group(0)[2:-2]
                        if kind in ('PART', 'CHAPTER', 'DIGRESSION'):
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
    
    return chapters

def _remove_adjacent_duplicates(text):
    """Remove ghost-layer duplicates — identical lines only (fast)."""
    if not text or len(text) < 40:
        return text
    lines = text.split('\n')
    # Single pass: remove any line that's identical to one of the
    # next 5 lines (ghost layers in pymupdf4llm are usually within
    # a few lines of each other, separated by blanks).
    out = []
    skip = set()
    for i, line in enumerate(lines):
        if i in skip:
            continue
        if len(line) >= 20:
            for j in range(i + 1, min(i + 6, len(lines))):
                if lines[j] == line:
                    skip.add(j)
        out.append(line)
    return '\n'.join(out)


def _remove_adjacent_line_overlaps(text):
    """Trim ghost-layer overlaps where the next line repeats the prior line tail."""
    if not text or len(text) < 40:
        return text

    def words_with_spans(value):
        return [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:;,'’-]+", value)
        ]

    lines = text.split('\n')
    out = []
    for line in lines:
        if not out or not line.strip():
            out.append(line)
            continue

        prev_words = words_with_spans(out[-1])
        curr_words = words_with_spans(line)
        max_overlap = min(8, len(prev_words), len(curr_words))
        trim_at = None
        for size in range(max_overlap, 1, -1):
            if [w for w, _, _ in prev_words[-size:]] != [w for w, _, _ in curr_words[:size]]:
                continue
            overlap_text = line[curr_words[0][1]:curr_words[size - 1][2]]
            if len(overlap_text) >= 12:
                trim_at = curr_words[size - 1][2]
                break

        if trim_at is not None:
            line = line[trim_at:].lstrip(' ,;:.')
        out.append(line)

    return '\n'.join(out)


def clean_text(text, config=None):
    """Sanitize extracted text before paragraph reconstruction."""
    if not text:
        return ''

    # 0. Character normalization (Issue: Gideon/AGES legacy encoding)
    text = normalize_characters(text)

    # 0a. Owen-specific OCR repairs (Issue 75/108)
    text = _repair_owen_ocr_errors(text, config=config)

    # 0b. Normalize spaced-caps OCR and I WILL / I AM mangles
    text = _normalize_spaced_caps(text)
    text = _normalize_i_will(text)
    
    # 0c. Scripture range OCR repairs (Issue 108)
    # Handles "7 ( 8)" -> "7, 8" misreads
    text = re.sub(r'(\d)\s+\(\s*(\d+)\s*\)', r'\1, \2', text)

    # 1. Translate AGES scripture reference codes to readable citations.
    #    <430316> → John 3:16. Must run BEFORE EMPTY_BRACKET_RE so we don't
    #    clobber the translated output.
    text = translate_ages_verse_markers(text)
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
    # Normalize answer labels that are split by PDF spacing.
    text = re.sub(r'\bAns\s+\.\s+(\d+)\b\.?', r'Ans. \1.', text)
    text = re.sub(r'\b(\d+(?:st|nd|rd|th))\s+([,.;])', r'\1\2', text)
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
    return clean_greek_text(text.strip())


DANGLING_CONNECTOR_RE = re.compile(
    r'\b(?:and|the|of|for|with|in|to|a|is|was|were|be|been|being|has|have|had|'
    r'by|from|as|at|or|which|who|whom|this|that|these|those)\s*$',
    re.I
)


def reconstruct_paragraphs(text):
    """Heal broken lines into proper, reflowable paragraphs."""
    if not text:
        return []

    lines = text.split('\n')
    paragraphs = []
    current = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if current:
                prev = current[-1]
                ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
                if ends_terminal:
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
            continue

        # Preserve numbered/list-like starts as real paragraph breaks.
        if STRUCTURAL_START_RE.match(stripped):
            if current:
                prev = current[-1]
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
                ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
                is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))

                if (not ends_terminal or is_dangling) and not hard_structural:
                    current.append(stripped)
                    continue
            if current:
                paragraphs.append(' '.join(current))
            current = [stripped]
            continue

        # De-hyphenation: strip trailing hyphen, merge with no space
        if current and current[-1].endswith('-'):
            current[-1] = current[-1][:-1] + stripped
            continue

        if current:
            prev = current[-1]
            ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
            starts_lower = bool(re.match(r'^[a-z0-9({\[\'"\u201c\u2018]', stripped))
            is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))

            # Issue 76: Multiline block quote preservation
            all_current_text = ' '.join(current)
            is_inside_quote = (
                (all_current_text.count('\u201c') > all_current_text.count('\u201d')) or
                (all_current_text.count('"') % 2 != 0)
            )

            if not ends_terminal or is_dangling:
                # Line does not end with terminal punctuation or ends with a connector → join
                current.append(stripped)
            elif starts_lower:
                # Starts lowercase after terminal (e.g. middle of quotation) → join
                current.append(stripped)
            elif is_inside_quote:
                # Inside an unclosed quote → join
                current.append(stripped)
            else:
                # Terminal punctuation + uppercase start → new paragraph
                paragraphs.append(' '.join(current))
                current = [stripped]
        else:
            current = [stripped]

    if current:
        paragraphs.append(' '.join(current))

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
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+\s*$', prev_clean, re.I):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean, re.I):
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


def _trim_overlapping_prefix(prev, current):
    """Return current with a duplicated prefix removed when it repeats prev's tail."""
    prev_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:]+", prev)]
    curr_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:]+", current)]
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

    if not re.search(r'[.!?]"?\s*$', prev.strip()):

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
    prev_words = set(re.findall(r"[a-z0-9:]+", prev_norm))
    current_words = re.findall(r"[a-z0-9:]+", current_norm)
    
    useful = [w for w in current_words if len(w) > 2]
    if len(useful) < 8:
        return False
        
    overlap = sum(1 for w in useful if w in prev_words)
    ratio = overlap / len(useful)
    
    # High confidence for short runs, very high for longer ones
    if len(useful) < 25:
        return ratio >= 0.85
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
        (re.sub(r'[^a-z0-9]+', '', m.group(0).lower()), m.start(), m.end())
        for m in re.finditer(r"[A-Za-z0-9'’-]+", text)
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
            for m in re.finditer(r"[A-Za-z0-9:]+", value)
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
        para = _remove_duplicate_scripture_tail(para)
        para = _remove_adjacent_repeated_word_runs(para)
        para = _repair_known_catechism_ghosts(para)
        if not para:
            continue

        for part in _split_inline_structural_markers(para):
            if not part:
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
                    or not re.search(r'[.!?]"?\s*$', cleaned[-1].strip())
                    or re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b\s+', part)
                ):
                    cleaned[-1] = f"{cleaned[-1]} {trimmed}".strip()
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
        words = [w for w in re.findall(r"[a-z0-9:]+", para_norm)]
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


def get_pages_text(doc, pages_md, start_page, end_page, healer_mode=True, title="", chapter_id="", config=None):
    """Get merged text for a range of pages with optional paragraph healing.

    Paragraph healing must be holistic across the full page range. Running
    reconstruction page-by-page forces false breaks at page boundaries.

    When healer_mode=False, returns clean raw text without paragraph
    reconstruction (used for layout-preserved front matter pages).
    """
    raw_parts = []
    
    for pg in range(start_page, min(end_page + 1, len(doc))):
        raw = get_merged_page_text(doc, pages_md, pg)
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
            body_html=f'<p>{_html_escape(text.strip())}</p>',
            page_start=pg,
            page_end=pg,
        ))
    return chapters


# ================================================================
# STAGE 1 ENTRY POINT — extract_volume()
# ================================================================

def extract_volume(vol_num: int, overrides: dict = None) -> dict:
    """Run Stage 1 for a single Owen volume: PDF → JSON intermediate.

    Writes volumes/vN/intermediate/volume_N.json and returns the dict.
    The JSON is the contract between Stage 1 (extract) and Stage 2 (render).

    overrides: optional per-volume config additions (see volumes/vN/convert.py).
    """
    import pymupdf4llm
    from shared import VOLUME_CONFIG, VOLUME_SUBTITLES
    from render import (
        detect_page_type, is_toc_continuation_page,
        format_title_page, build_toc_page_xhtml,
    )

    overrides = overrides or {}
    config = {**VOLUME_CONFIG.get(vol_num, {}), **overrides}
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
    chapters = build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map, config=config)

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
        toc_like = ptype == 'toc_page' or is_toc_continuation_page(page, pg + 1)
        if pg in chapter_pages and not toc_like:
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
            while j < scan_limit:
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
    import sys
    vol = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    extract_volume(vol)
