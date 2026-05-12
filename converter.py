#!/usr/bin/env python3
"""
John Owen Works — PyMuPDF EPUB3 Converter
Replaces legacy pdftohtml pipeline with PyMuPDF + PyMuPDF4LLM.
"""

import sys, os, re, uuid, shutil, zipfile, tempfile, hashlib, json, subprocess
from datetime import datetime
from html import escape as _html_escape
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

_SCRIPT_DIR = Path(__file__).parent.resolve()
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    convert_greek_word, convert_gideon_hebrew
)

try:
    import fitz
except ImportError:
    sys.exit("Error: PyMuPDF (fitz) not installed. Run: pip install pymupdf4llm")
try:
    import pymupdf4llm
except ImportError:
    sys.exit("Error: PyMuPDF4LLM not installed. Run: pip install pymupdf4llm")
try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed.")

FONT_BASE = os.path.join(_SCRIPT_DIR, 'fonts')

# ─── Coordinate Constants ─────────────────────────────────────
TOP_MARGIN = 40        # Redact text blocks above this y (pts)
BOTTOM_MARGIN = 25     # Redact text blocks below page_height - this
PAGE_W = 410           # Standard page width for Owen PDFs
PAGE_H = 626           # Standard page height for Owen PDFs

# ─── Font Detection ────────────────────────────────────────────
GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}

# Regex for detecting Beta Code words that missed font tagging.
# Keep this conservative: the fallback runs after ordinary prose has been
# escaped, so broad markers like apostrophe or leading j/J corrupt English
# words such as "author's", "Jesus", "John", and "justification".
BETA_CODE_RE = re.compile(
    r"(?<!\S)(?![^æ;]*[æ;])(?:"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+[><=~|{}\[\]+]+"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
    r"[><=~|{}\[\]+]+[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
    r"pneu'ma"
    r")\.?(?!\S)"
)

# Regex for detecting Gideon Hebrew words that missed font tagging.
# Matches words containing unambiguous Gideon-only marks. Plain semicolon,
# bracket, and digit 1 are ordinary English/list punctuation and caused major
# false positives ("grace;" and "vol. 1" became Hebrew).
GIDEON_HEBREW_RE = re.compile(r'(?<!\S)[a-zA-Z\[\];1]*(?:[æ}])[a-zA-Zæ}\];1\[]*\.?(?!\S)')

FOOTNOTE_MARKER_RE = re.compile(r'\[f(\d+)\]')
LOOSE_FOOTNOTE_MARKER_RE = re.compile(
    r'\[\s*f\s*(\d{1,3})\s*\]|(?<![A-Za-z])f\s*(\d{1,3})\b',
    re.I,
)
FOOTNOTE_PLACEHOLDER_RE = re.compile(r'FNREFTOKEN(\d+)TOKEN')
FT_MARKER_RE = re.compile(r'^ft(\d+)\s*', re.I)
EMPTY_BRACKET_RE = re.compile(r'\[\s*\]')
STRUCTURAL_START_RE = re.compile(
    r'^(?:'
    r'(?!\d{4}\.)\d{1,3}\.\s+|'                         # 5. Mankind...
    r'\((?!\d{4}\))\d+\.?\)\s+|'                    # (1.) There... / (1) There...
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\s+|'  # (1st,) Such...
    r'\[\d+\.?\]\s+|'                    # [1.] There...
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\s+|'  # [1st,] There...
    r'[IVXLCDM]+\.\s+|'                  # I. / II.
    r'[A-Z]\.\s+|'                       # Q. / A. catechism lines
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]\s+|'  # 1st, 2nd, 3rd, 4th,
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?\s+|'  # 2ndly, 3rdly
    r'(?:First|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly|Again|But)\b[,.]?\s+'
    r')'
)
STRUCTURAL_PREFIX_HTML_RE = re.compile(
    r'^(?P<marker>'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
    r'[IVXLCDM]+\.|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<space>\s+)'
)
INLINE_STRUCTURAL_MARKER_RE = re.compile(
    r'(?<!^)(?P<lead>\s+)'
    r'(?P<marker>'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
    r'\*\*\d+\.\*\*|'
    r'\*\*\((?!\d{4}\))\d+\.?\)\*\*|'
    r'\*\*\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\*\*|'
    r'\*\*\[\d+\.?\]\*\*|'
    r'\*\*\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\*\*|'
    r'\*\*\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)\*\*\s*[,.;]?|'
    r'\*\*[IVXLCDM]+\.\*\*|'
    r'[IVXLCDM]+\.|'
    r'(?<![:\d-])(?!\d{4}\.)\d+\.|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<trail>\s+)'
)
ROMAN_HEADING_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?\s+(?P<rest>.+)$')
ROMAN_ONLY_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$')
PLAIN_CHAPTER_RE = re.compile(r'^(CHAPTER\s+\d+\.?)(?:\s+(.+))?$')
CITATION_ABBREV_TRAIL_RE = re.compile(
    r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|q|a|p)\.?\s*$',
    re.I,
)
CITATION_ABBREV_START_RE = re.compile(
    r'^(?:Lib|Serm|Sermo|Epist|Ep|Cap|Chap|Orat|Tract|Homil|Haer|Dial)\.\s+',
    re.I,
)
CITATION_AUTHOR_TRAIL_RE = re.compile(
    r'\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|'
    r'Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan)\.?\s*$',
    re.I,
)
ROMAN_LIST_TOKEN = '@@ROMAN_LIST@@'
MARKDOWN_STRUCTURAL_START_RE = re.compile(
    r'^\*\*(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
    r'\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\*\*\s*[,.;]?\s+'
)


def _repair_owen_ocr_errors(text: str) -> str:
    """
    Repair known OCR character misreads specific to Owen/AGES extraction.
    Separate from _repair_known_source_losses() which handles source loss patterns.
    """
    corrections = {
        'Charneck': 'Charnock',
        'storage': 'strange',
        'whoso': 'whose',
        'se largely': 'so largely',
        'prevailing task': 'prevailing taste',
        'whoso name': 'whose name',
        'whoso human': 'whose human',
        'secretes': 'secrets',
        'on]y': 'only',
        'name]y': 'namely',
        r'(\w+)]y\b': r'\1ly',
        # Add more as they are discovered
    }
    result = text
    for wrong, right in corrections.items():
        if wrong.startswith('(') or wrong.endswith('\\b'):
             result = re.sub(wrong, right, result)
        else:
             result = re.sub(r'\b' + re.escape(wrong) + r'\b', right, result)
    return result
SCRIPTURE_BOOK_RE = (
    r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|'
    r'Proverbs|Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|'
    r'Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|'
    r'Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|'
    r'Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|'
    r'Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|'
    r'Revelation)'
)
SCRIPTURE_REF_RE = re.compile(
    rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*|\b\d+:\d+(?:[-,]\s*\d+)*',
    re.I,
)
SCRIPTURE_CONTINUATION_TRAIL_RE = re.compile(
    rf'(?:\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+)?\d+:\d+(?:[-,;]\s*\d+)*[,:;]?\s*$|'
    rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+(?:[-,;]\s*\d+)*,\s*$|'
    r'\b(?:verse|verses|chap|chapter)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$|'
    r'\b(?:cap|lib)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$',
    re.I,
)

# ================================================================
# STAGE 1: Coordinate-Based Redaction
# ================================================================

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
            
            # Bottom safety: Owen's footnotes or low body lines often sit at y=580-595
            if y_center > page_height - 65 and not is_header_footer and len(line_text) > 15:
                keep_lines.append(line)
                continue

            if y_center < top_margin and not is_header_footer:
                # Top safety: don't clip lines that might be part of a chapter head
                if y_center > 30 and len(line_text) > 30:
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


# ================================================================
# STAGE 2: AGES Navigation Extraction
# ================================================================

def extract_ages_nav(doc):
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
            return _parse_visual_toc(doc, pg)
    return []


def _parse_visual_toc(doc, toc_page_num):
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
        # Treatise titles (all caps, short)
        if text_upper == text and len(text) > 5 and len(text) < 60:
            if any(kw in text_upper for kw in ('CHRISTOLOGIA', 'MEDITATIONS', 'CATECHISMS')):
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
    - For regular pages: use PyMuPDF4LLM Markdown (cleaned)
    - For Greek/Hebrew pages: use font-aware extraction to convert Beta Code/Gideon,
      but preserve [fN] footnote markers from the Markdown.
    """
    page = doc[page_idx]
    font_type = page_has_special_fonts(page)
    md_text = extract_page_markdown(pages_md, page_idx)
    
    if font_type:
        raw_text = extract_page_text_with_fonts(page)
        # Preserve [fN] markers from Markdown that might be lost in raw text
        fn_markers = FOOTNOTE_MARKER_RE.findall(md_text)
        # Also check for standalone [fN] markers on their own lines
        for fn in fn_markers:
            marker = f'[f{fn}]'
            if marker not in raw_text:
                raw_text += f' [f{fn}]'
        return raw_text
    else:
        return md_text


# ================================================================
# STAGE 4: Footnote Stitching
# ================================================================

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


def normalize_footnote_markers(text):
    """Normalize AGES inline footnote markers like f2 or [ f2] to [f2]."""
    def repl(match):
        return f'[f{match.group(1) or match.group(2)}]'

    return LOOSE_FOOTNOTE_MARKER_RE.sub(repl, text)


def _noteref_link(fn_num):
    return (
        f'<a class="noteref" epub:type="noteref" role="doc-noteref" '
        f'href="endnotes.xhtml#fn{fn_num}"><sup>{fn_num}</sup></a>'
    )


def _restore_footnote_placeholders(text):
    return FOOTNOTE_PLACEHOLDER_RE.sub(lambda m: _noteref_link(m.group(1)), text)


def _strip_footnote_placeholders(text):
    return FOOTNOTE_PLACEHOLDER_RE.sub(' ', text)


# ================================================================
# STAGE 5: Chapter Building from TOC
# ================================================================

@dataclass
class Chapter:
    cid: str
    title: str
    level: int          # 1=treatise, 2=chapter, 3=subsection
    body_html: str = ''
    page_start: int = 0
    page_end: int = 0
    is_treatise: bool = False
    is_endnotes: bool = False
    footnote_refs: list = field(default_factory=list)


def title_case(text):
    """Convert text to Title Case, preserving Roman numerals and small words."""
    if not text:
        return ""
    small_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'en', 'for',
                   'if', 'in', 'of', 'on', 'or', 'the', 'to', 'v', 'via', 'vs'}
    words = text.split()
    res = []
    for i, w in enumerate(words):
        clean_w = w.strip('.,:;()[]"').upper()
        if re.match(r'^[IVXLCDM]+$', clean_w):
            res.append(w.upper())
        elif i > 0 and w.lower() in small_words:
            res.append(w.lower())
        else:
            res.append(w.capitalize())
    return " ".join(res)


def nav_display_title(text):
    """Display front-matter labels in NAV as they appear in the PDF."""
    stripped = (text or '').strip()
    normalized = stripped.rstrip('.').upper()
    if normalized in {
        'GENERAL PREFACE',
        'PREFATORY NOTE',
        'PREFACE',
        'PREFACE TO THE READER',
        'ORIGINAL PREFACE',
    }:
        return normalized + ('.' if stripped.endswith('.') else '')
    return title_case(stripped)


def build_chapters_from_toc(doc, pages_md, nav_entries, footnote_map):
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
    for i, (level, title, page_0idx) in enumerate(nav_entries):
        # Determine if this is a treatise title page
        title_upper = title.upper()
        is_treatise = any(kw in title_upper for kw in [
            'CHRISTOLOGIA', 'MEDITATIONS AND DISCOURSES', 'TWO SHORT CATECHISMS',
            'DECLARATION OF THE GLORIOUS', 'A DECLARATION', 'A VINDICATION',
            'COMMUNION WITH GOD', 'THE DOCTRINE OF THE TRINITY'
        ])
        
        if is_treatise:
            # Clean up the treatise name for parenthetical use
            if 'BRIEF DECLARATION' in title_upper or 'DOCTRINE OF THE TRINITY' in title_upper:
                current_treatise = 'Doctrine of the Trinity'
            elif 'VINDICATION' in title_upper:
                current_treatise = 'Vindication'
            elif 'COMMUNION' in title_upper:
                current_treatise = 'Communion with God'
            elif 'CHRISTOLOGIA' in title_upper:
                current_treatise = 'Christologia'
            elif 'GLORY OF CHRIST' in title_upper:
                current_treatise = 'Glory of Christ'
            elif 'CATECHISMS' in title_upper:
                current_treatise = 'Catechisms'
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
        raw_text = get_pages_text(doc, pages_md, page_0idx, end_page)
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


def clean_text(text):
    """Sanitize extracted text before paragraph reconstruction."""
    if not text:
        return ''
    
    # 0. Owen-specific OCR repairs (Issue 75)
    text = _repair_owen_ocr_errors(text)
    
    # 1. Remove CCEL/AGES scripture reference codes: <450503>
    text = re.sub(r'<\d[A-Za-z0-9]{5}>', '', text)
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
    # 5. Remove adjacent ghost-layer duplicates and repeated line tails
    text = _remove_adjacent_duplicates(text)
    text = _remove_adjacent_line_overlaps(text)
    return text.strip()


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
        
        # Preserve heading markers as standalone paragraphs
        if stripped.startswith('#'):
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append(stripped)
            continue

        # Preserve numbered/list-like starts as real paragraph breaks. Owen's
        # PDFs use bold "5." and "(1.)" heads at paragraph starts; these are
        # not faulty extraction splits even if the preceding line lacks final
        # punctuation.
        if STRUCTURAL_START_RE.match(stripped):
            if current:
                prev = current[-1]
                hard_structural = re.match(
                    r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
                    r'\d+(?:st|nd|rd|th)\b[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)',
                    stripped,
                )
                if not re.search(r'[.!?]"?\s*$', prev) and not hard_structural:
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
            
            # Issue 76: Multiline block quote preservation
            all_current_text = ' '.join(current)
            is_inside_quote = (
                (all_current_text.count('\u201c') > all_current_text.count('\u201d')) or
                (all_current_text.count('"') % 2 != 0)
            )
            
            if not ends_terminal:
                # Line does not end with terminal punctuation → join
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


def _norm_for_dedupe(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\[f\d+\]', ' ', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9:]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _is_scripture_ref_fragment(text):
    clean = re.sub(r'\[f\d+\]', '', text).strip()
    if len(clean) > 220:
        return False
    if not SCRIPTURE_REF_RE.search(clean):
        return False
    leftovers = SCRIPTURE_REF_RE.sub('', clean)
    leftovers = re.sub(r'[;:,.()\-\s]', '', leftovers)
    return len(leftovers) <= 12


def _scripture_ref_tokens(text):
    tokens = []
    for m in SCRIPTURE_REF_RE.finditer(text):
        token = re.sub(r'\s+', ' ', m.group(0).lower())
        token = re.sub(r'^(?:[1-3]\s+)?', '', token)
        tokens.append(token)
    return tokens


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
    if current.startswith('#'):
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
    """Drop short ghost fragments whose words already occur in the previous paragraph."""
    if not prev or not current or len(current) > 260:
        return False
    prev_words = set(re.findall(r"[a-z0-9:]+", _norm_for_dedupe(prev)))
    current_words = re.findall(r"[a-z0-9:]+", _norm_for_dedupe(current))
    useful = [w for w in current_words if len(w) > 2]
    if len(useful) < 8:
        return False
    overlap = sum(1 for w in useful if w in prev_words)
    return overlap / len(useful) >= 0.82


def _split_inline_structural_markers(para):
    """Promote inline Owen list markers to paragraph starts."""
    pieces = []
    pos = 0
    for match in INLINE_STRUCTURAL_MARKER_RE.finditer(para):
        before = para[pos:match.start()].strip()
        marker = match.group('marker')
        after_start = match.start('marker')

        marker_is_wrapped = marker.startswith(('(', '[', '**(', '**['))
        has_list_intro_before_reference = bool(re.search(
            r'\b(?:here\s+is|here\s+are|as\s+follows|following)\b.{0,320}$',
            before,
            re.I,
        ))
        # Skip roman numeral ranges like "III. — VI."
        if (
            re.match(r'^[IVXLCDM]+\.$', marker, re.I)
            and re.match(r'\s*[—–-]\s*[IVXLCDM]+\.', para[match.end():])
        ):
            continue
        if (
            (
                SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
                or CITATION_ABBREV_TRAIL_RE.search(before[-80:])
                or re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
                or re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
                or (para[:match.start()].count('"') % 2 != 0)
                or (para[:match.start()].count('\u201c') > para[:match.start()].count('\u201d'))
            )
            and not marker_is_wrapped
            and not has_list_intro_before_reference
        ):
            continue

        before_ends_structural = bool(re.search(r'[,;:—-]\s*$', before))
        before_ends_terminal = bool(re.search(r'[.!?]["”’)\]]?\s*$', before))
        before_ends_lead_word = bool(re.search(
            r'\b(?:wherefore|therefore|for|but|and|or|as)\s*$',
            before,
            re.I,
        ))
        before_ends_objection = bool(re.search(r'\b(?:Objection|Obj)\b\.?\s*$', before, re.I))
        if len(before) < 12 and not (before_ends_structural or before_ends_lead_word or before_ends_objection):
            continue
        marker_clean = re.sub(r'[\*\[\]\(\),;.\s]', '', marker).lower()
        marker_is_bare_decimal = bool(re.match(r'^(?:\*\*)?\d+\.(?:\*\*)?$', marker.strip()))
        marker_is_bare_roman = bool(re.match(r'^(?:\*\*)?[IVXLCDM]+\.(?:\*\*)?$', marker.strip(), re.I))
        marker_is_bare_ordinal = bool(re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b,?\s*(?:\*\*)?$', marker.strip(), re.I))
        after_preview = para[match.end():match.end() + 80].lstrip()
        after_starts_like_heading = bool(re.match(r'[A-Z“"‘]', after_preview))
        strong_source_like_marker = (
            (marker_is_bare_decimal or marker_is_bare_roman or marker_is_bare_ordinal)
            and len(before) >= 35
            and after_starts_like_heading
            and not SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
            and not CITATION_ABBREV_TRAIL_RE.search(before[-80:])
            and not re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', before, re.I)
            and not re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
            and not re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
            and marker_clean not in {'i', 'v', 'x', 'l', 'c', 'd', 'm'}
        )
        if not (re.search(r'[.,;:—-]\s*$', before) or before_ends_terminal or before_ends_lead_word or before_ends_objection):
            if not (marker_is_wrapped or strong_source_like_marker):
                continue

        if before:
            pieces.append(before)
        pos = after_start

    if not pieces:
        return [para]

    tail = para[pos:].strip()
    if tail:
        pieces.append(tail)
    return pieces


def _remove_repeated_opening_clause(text):
    """Remove duplicated opening clauses like 'So we are said ...: So we are said ...:'."""
    pattern = re.compile(r'^(.{25,220}?[.:;])\s+\1', re.I)
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub(r'\1 ', text)
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


def _repair_known_catechism_ghosts(text):
    """Repair source-confirmed catechism phrases damaged by AGES footnote columns."""
    text = re.sub(
        rf'\s*\*\*\s*\]\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)',
        ' ',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bby the mighty, effectual working of his preaching of the Word\b',
        'by the mighty, effectual working of his Spirit in the preaching of the Word',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bNothing at all, being merely(?P<fn>\s+\[f\d+\])?\s+in ourselves\b',
        lambda match: (
            'Nothing at all, being merely wrought upon by the free grace '
            f'and Spirit of God, when in ourselves{match.group("fn") or ""}'
        ),
        text,
        flags=re.I,
    )
    return text


def _trim_duplicate_reference_prefix(prev, current):
    """Drop a leading scripture-reference run when the same refs just appeared."""
    if not prev or not current:
        return current
    pos = 0
    refs = []
    while pos < len(current):
        while pos < len(current) and current[pos].isspace():
            pos += 1
        match = SCRIPTURE_REF_RE.match(current, pos)
        if not match:
            break
        refs.append(re.sub(r'\s+', ' ', match.group(0).lower()))
        pos = match.end()
        while pos < len(current) and current[pos] in ' ;,.:':
            pos += 1

    if not refs:
        return current

    prev_refs = set(_scripture_ref_tokens(prev))
    normalized_refs = {re.sub(r'^(?:[1-3]\s+)?', '', ref) for ref in refs}
    if normalized_refs and normalized_refs <= prev_refs:
        return current[pos:].lstrip()
    return current


def post_process_paragraphs(paragraphs):
    """Clean paragraph-level artifacts after line healing."""
    cleaned = []
    for para in paragraphs:
        para = _remove_repeated_opening_clause(para.strip())
        para = _remove_interrupted_duplicate_clause(para)
        para = _remove_duplicate_scripture_tail(para)
        para = _remove_adjacent_repeated_word_runs(para)
        para = _repair_known_catechism_ghosts(para)
        para = _repair_known_source_losses(para)
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


def _remove_global_ngram_duplicates(paragraphs, size=12):
    """
    Remove non-consecutive paragraph-level duplicates using n-gram anchors.
    This catches 'interrupted' ghost layers that sequential de-duplication misses.
    """
    seen_ngrams = set()
    cleaned = []
    for para in paragraphs:
        words = [w.lower() for w in re.findall(r"[A-Za-z0-9]+", para)]
        if len(words) < size:
            cleaned.append(para)
            continue

        # Check first and last n-gram of the paragraph
        first_anchor = tuple(words[:size])
        last_anchor = tuple(words[-size:])

        # If it's a long paragraph, also check a middle anchor
        middle_anchor = None
        if len(words) > size * 3:
            mid = len(words) // 2
            middle_anchor = tuple(words[mid:mid + size])

        if first_anchor in seen_ngrams or last_anchor in seen_ngrams:
            # Ghost layers are almost always exact paragraph repeats
            # We limit the check to size 12+ to avoid common short phrases
            continue

        seen_ngrams.add(first_anchor)
        seen_ngrams.add(last_anchor)
        if middle_anchor:
            seen_ngrams.add(middle_anchor)
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


def get_pages_text(doc, pages_md, start_page, end_page, healer_mode=True):
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
    cleaned = clean_text('\n'.join(raw_parts))
    if not cleaned:
        return ''

    if not healer_mode:
        return cleaned

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
# STAGE 6: EPUB3 Assembly
# ================================================================

def force_polyglot_mapping(text):
    """
    Aggressive regex fallback to convert Beta Code and Gideon Hebrew that
    missed font detection. Splits by tags to avoid corrupting HTML.
    """
    if not text:
        return ""
    
    # Pass 1: Hebrew Gideon (Higher priority due to unique characters)
    parts = re.split(r'(<[^>]+>)', text)
    temp_parts = []
    for part in parts:
        if part.startswith('<'):
            temp_parts.append(part)
        else:
            temp_parts.append(GIDEON_HEBREW_RE.sub(
                lambda m: f'<span class="hebrew" lang="he" xml:lang="he" dir="rtl">{convert_gideon_hebrew(m.group(0))}</span>',
                part
            ))
    text = ''.join(temp_parts)

    # Pass 2: Greek Beta Code
    parts = re.split(r'(<[^>]+>)', text)
    temp_parts = []
    for part in parts:
        if part.startswith('<'):
            temp_parts.append(part)
        else:
            temp_parts.append(BETA_CODE_RE.sub(
                lambda m: f'<span class="greek" lang="el" xml:lang="el">{convert_greek_word(m.group(0))}</span>',
                part
            ))
    text = ''.join(temp_parts)
        
    return text


def tag_unicode_ranges(text):
    """Wrap untagged Greek and Hebrew Unicode runs in spans."""
    if not text:
        return ""
    
    # 1. Force mapping of any raw Beta Code or Gideon residue
    text = force_polyglot_mapping(text)
    
    # 2. Tag any existing Unicode that wasn't wrapped
    def tag_greek(m):
        content = m.group(1)
        before = text[:m.start()]
        if '<span' in before and before.rfind('<span') > before.rfind('</span>'):
            return content
        return f'<span lang="el" xml:lang="el">{content}</span>'

    text = re.sub(r'([\u0370-\u03FF\u1F00-\u1FFF]+)', tag_greek, text)

    def tag_hebrew(m):
        content = m.group(1)
        before = text[:m.start()]
        if '<span' in before and before.rfind('<span') > before.rfind('</span>'):
            return content
        return f'<span lang="he" xml:lang="he" dir="rtl">{content}</span>'

    text = re.sub(r'([\u0590-\u05FF]+)', tag_hebrew, text)

    text = text.replace('</span><span lang="el" xml:lang="el">', '')
    text = text.replace('</span><span lang="he" xml:lang="he" dir="rtl">', '')
    return text


def emphasize_structural_prefix(text):
    """Bold visible paragraph/list markers that survive the PDF extraction."""
    if not text or text.startswith('<b>'):
        return text
    return STRUCTURAL_PREFIX_HTML_RE.sub(r'<b>\g<marker></b>\g<space>', text, count=1)


RENDERED_INLINE_STRUCTURAL_RE = re.compile(
    r'(?P<marker><b>(?:'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\[(?:\d+\.?|\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\]|'
    r'\((?:\d+\.?|\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\)|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')</b>\s+)'
)
PLAIN_INLINE_STRUCTURAL_HTML_RE = re.compile(
    r'(?P<marker>(?<![:\d-])(?!\d{4}\.)\d{1,3}\.\s+)'
)


def _split_rendered_inline_structural_html(text_html):
    """Split paragraphs where a rendered bold list marker remains inline."""
    pieces = []
    pos = 0
    matches = sorted(
        list(RENDERED_INLINE_STRUCTURAL_RE.finditer(text_html))
        + list(PLAIN_INLINE_STRUCTURAL_HTML_RE.finditer(text_html)),
        key=lambda item: item.start(),
    )
    for match in matches:
        if match.start() < pos:
            continue
        before_html = text_html[pos:match.start()].strip()
        before_text = re.sub(r'<[^>]+>', ' ', before_html)
        before_text = re.sub(r'\s+', ' ', before_text).strip()
        if not before_text or len(before_text) < 35:
            continue
        if re.search(r'\b(?:verse|verses|chap|chapter|john|romans|corinthians|timothy|peter)\.?\s*$', before_text, re.I):
            continue
        if not re.search(r'[.!?:;—-]\s*$', before_text):
            continue
        pieces.append(before_html)
        pos = match.start()
    if not pieces:
        return [text_html]
    pieces.append(text_html[pos:].strip())
    return [piece for piece in pieces if piece]


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


def _split_leading_chapter_subtitle(text):
    """Split bold all-caps chapter subtitles from following prose."""
    match = re.match(r'^((?:\*\*[^*]+\*\*\s*){1,5})(.+)$', text, flags=re.S)
    if not match:
        return None, text

    subtitle_md = match.group(1).strip()
    rest = match.group(2).strip()
    subtitle_plain = re.sub(r'\*\*', '', subtitle_md)
    letters = [c for c in subtitle_plain if c.isalpha()]
    if not letters:
        return None, text
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    if upper_ratio < 0.72 or len(subtitle_plain) < 18:
        return None, text
    if not rest:
        return None, text
    return subtitle_md, rest


def _clean_heading_text(text):
    """Remove stray markdown emphasis markers from extracted heading text."""
    text = (text or '').replace('*', '')
    return re.sub(r'\s+', ' ', text).strip()


def _roman_to_int(roman):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    previous = 0
    for char in reversed(roman.rstrip('.').upper()):
        value = values.get(char, 0)
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def _is_roman_list_item(text):
    stripped = text.strip()
    if not stripped or stripped.startswith('#') or ROMAN_ONLY_RE.match(stripped):
        return False
    if len(re.findall(r'\w+', stripped)) > 28:
        return False
    return bool(re.search(r'[.!?:;]"?\s*$', stripped))


def _strip_markdown_heading_marker(text):
    return re.sub(r'^\s*#{1,6}\s+', '', text.strip())


def _coalesce_roman_list_paragraphs(paragraphs):
    """Join outline-like roman list labels with their short item text."""
    out = []
    expected_roman_number = None
    i = 0

    while i < len(paragraphs):
        stripped = paragraphs[i].strip()
        roman_source = _strip_markdown_heading_marker(stripped)
        roman_match = ROMAN_ONLY_RE.match(roman_source)
        if roman_match and i + 1 < len(paragraphs):
            roman_number = _roman_to_int(roman_match.group('roman'))
            previous_text = out[-1].strip() if out else ''
            starts_list = (
                roman_number in (1, 2)
                and (
                    re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                    or re.search(r'(?:[—-]|,)\s*$', previous_text)
                )
            )
            continues_list = expected_roman_number == roman_number

            if (starts_list or continues_list) and _is_roman_list_item(paragraphs[i + 1]):
                out.append(f'{ROMAN_LIST_TOKEN} {roman_match.group("roman")} {paragraphs[i + 1].strip()}')
                expected_roman_number = roman_number + 1
                i += 2
                continue

        if roman_match:
            expected_roman_number = None
        out.append(paragraphs[i])
        i += 1

    return out


def _split_inline_catechism_questions(paragraphs):
    out = []
    pattern = re.compile(r'(?<!^)\s+(?=(?:\*\*)?Q\.\s*\d+\.(?:\*\*)?\s+)')
    for para in paragraphs:
        parts = [part.strip() for part in pattern.split(para) if part.strip()]
        out.extend(parts or [para])
    return out


def _is_catechism_scripture_spill(text):
    clean = re.sub(r'\[f\d+\]', ' ', text)
    if re.match(r'^(?:\*\*)?[QA]\.', clean.strip()):
        return False
    has_ref_code = bool(re.search(r'<\d{6}>', clean))
    has_ref = bool(SCRIPTURE_REF_RE.search(clean))
    if not (has_ref_code or has_ref):
        return False
    clean = re.sub(r'<\d{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(
        rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b|\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+\b',
        ' ',
        clean,
        flags=re.I,
    )
    leftovers = re.sub(r'[;:,.()\-\s]', '', clean)
    return len(leftovers) <= 20


def _answer_head(text):
    clean = FOOTNOTE_MARKER_RE.sub(' ', text)
    clean = re.sub(r'<\d{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    match = re.match(r'^(?:\*\*)?A\.(?:\*\*)?\s+(.{5,120}?[.!?;])', clean, re.I)
    return _norm_for_dedupe(match.group(1)) if match else ''


def _clean_catechism_footnote_spill(paragraphs):
    out = []
    in_catechism = False
    last_answer_head = ''
    for para in paragraphs:
        stripped = para.strip()
        if re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            in_catechism = True
            last_answer_head = ''
        if in_catechism and _is_catechism_scripture_spill(stripped):
            continue
        current_answer_head = _answer_head(stripped)
        if in_catechism and current_answer_head and current_answer_head == last_answer_head:
            continue
        out.append(para)
        if current_answer_head:
            last_answer_head = current_answer_head
        elif re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            last_answer_head = ''
    return out


def _remove_catechism_lookahead_ghosts(paragraphs):
    """Remove answer text that was pulled forward from the following answer."""
    cleaned = list(paragraphs)
    for idx, para in enumerate(cleaned[:-1]):
        if not re.match(r'^(?:\*\*)?A\.', para.strip(), re.I):
            continue
        next_answer = ''
        for following in cleaned[idx + 1:idx + 4]:
            if re.match(r'^(?:\*\*)?A\.', following.strip(), re.I):
                next_answer = following
                break
        if not next_answer:
            continue

        curr_words = [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:]+", para)
        ]
        next_words = [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9:]+", next_answer)]
        if len(curr_words) < 10 or len(next_words) < 8:
            continue

        best = None
        max_size = min(18, len(curr_words), len(next_words))
        for size in range(max_size, 6, -1):
            next_runs = {tuple(next_words[j:j + size]) for j in range(len(next_words) - size + 1)}
            for i in range(1, len(curr_words) - size + 1):
                run = tuple(w for w, _, _ in curr_words[i:i + size])
                if run in next_runs:
                    best = (curr_words[i][1], curr_words[i + size - 1][2])
                    break
            if best:
                break

        if best:
            start, end = best
            while start > 0 and para[start - 1] in ' \t,;:':
                start -= 1
            while end < len(para) and para[end] in ' \t,;:.':
                end += 1
            cleaned[idx] = re.sub(r'\s{2,}', ' ', (para[:start] + ' ' + para[end:]).strip())
    return cleaned


def _remove_duplicate_catechism_answer_opening(text):
    """Collapse ghosted catechism answer openings inside one paragraph."""
    pattern = re.compile(
        r'^(?P<label>(?:\*\*)?A\.(?:\*\*)?\s+)'
        r'(?P<body>.{6,180}?[.!?;])\s+'
        r'(?:\*\*)?A\.(?:\*\*)?\s+(?P=body)',
        re.I,
    )
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(r'\g<label>\g<body>', text)
    return text


def _repair_known_front_matter_text(text):
    """Repair front-matter phrases lost when PDF footnote overlays interrupt text."""
    text = text.replace(
        'To object of Dr. Owen in this treatise',
        'The object of Dr. Owen in this treatise',
    )
    text = text.replace(
        'simple vague and defective',
        'simply vague and defective',
    )
    text = text.replace(
        'these apprehensions of Own.',
        'these apprehensions of Owen.',
    )
    text = text.replace(
        'The Christology of Owens has always been highly valued',
        'The Christology of Owen has always been highly valued',
    )
    text = text.replace(
        'They were among the firsts as the other treatises',
        'They were among the first, as the other treatises',
    )
    text = text.replace(
        'publish all the treatises of ushered under their auspices into public notice',
        'publish all the treatises of Owen in volumes corresponding in size and appearance with the one ushered under their auspices into public notice',
    )
    return text


def _repair_known_source_losses(text):
    """Restore source text lost by font-aware extraction around PDF overlays."""
    text = text.replace(
        'This being the [f8] [f9] declare wherein he placed',
        'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    )
    text = text.replace(
        'This being the [f9] declare wherein he placed',
        'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    )
    return text


def markdown_to_html(md_text):
    """
    Convert paragraph-healed text to clean XHTML.
    Input is paragraphs separated by double newlines.
    Handles headings, bold, italic, and footnote refs.
    """
    if not md_text:
        return ''
    
    html_parts = []
    normalized_paragraphs = [normalize_footnote_markers(para) for para in md_text.split('\n\n')]
    paragraphs = _clean_catechism_footnote_spill(
        _split_inline_catechism_questions(
            _coalesce_roman_list_paragraphs(normalized_paragraphs)
        )
    )
    expanded_paragraphs = []
    for para in paragraphs:
        expanded_paragraphs.extend(_split_inline_structural_markers(para))
    paragraphs = expanded_paragraphs
    paragraphs = _remove_catechism_lookahead_ghosts(paragraphs)
    paragraphs = [_repair_known_catechism_ghosts(para) for para in paragraphs]
    recent_plain = []
    roman_list_expected = None
    pending_chapter_subtitle = False
    seen_footnote_refs = set()
    
    for para in paragraphs:
        stripped = para.strip()
        if not stripped:
            continue
        
        # Detect heading level from leading #
        h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        
        if h_match:
            level = len(h_match.group(1))
            content = h_match.group(2)
            h_tag = 'h1' if level <= 2 else ('h2' if level <= 4 else 'h3')
        else:
            content = stripped
            h_tag = None

        frontmatter_inline = None
        if h_tag:
            frontmatter_inline = re.match(
                r'^(?:THE\s+)?(PREFACE|PREFATORY NOTE|ORIGINAL PREFACE)(\.?)\s+(.{40,})$',
                content,
                re.S,
            )
        if frontmatter_inline:
            heading = f'{frontmatter_inline.group(1)}{frontmatter_inline.group(2)}'
            html_parts.append(f'<h3 class="secondary">{heading}</h3>')
            content = frontmatter_inline.group(3).strip()
            h_tag = None
        
        # Process footnote markers [fN]
        roman_list_match = re.match(rf'^{re.escape(ROMAN_LIST_TOKEN)}\s+([IVXLCDM]+\.?)\s+(.+)$', content)
        is_centered_roman_list = False
        if roman_list_match:
            is_centered_roman_list = True
            content = f'**{roman_list_match.group(1)}** {roman_list_match.group(2).strip()}'
            h_tag = None

        def footnote_marker_repl(match):
            fn_num = match.group(1)
            if fn_num in seen_footnote_refs:
                return ''
            seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'

        content_no_refs = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, content).strip()
        content_no_refs = re.sub(r'\s{2,}', ' ', content_no_refs)
        content_no_refs = _remove_duplicate_catechism_answer_opening(content_no_refs)
        content_no_refs = _repair_known_front_matter_text(content_no_refs)
        if recent_plain:
            content_no_refs = _trim_duplicate_reference_prefix(' '.join(recent_plain[-3:]), content_no_refs)
            if not content_no_refs:
                continue

        if h_tag:
            chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
            if chapter_match:
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_rest = (chapter_match.group(2) or '').strip()
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if not chapter_rest:
                    pending_chapter_subtitle = True
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

                subtitle_md, body_after_subtitle = _split_leading_chapter_subtitle(chapter_rest)
                if subtitle_md:
                    subtitle = _clean_heading_text(subtitle_md)
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    content_no_refs = body_after_subtitle.strip()
                    h_tag = None
                    pending_chapter_subtitle = False
                else:
                    letters = [c for c in chapter_rest if c.isalpha()]
                    upper_ratio = (
                        sum(1 for c in letters if c.isupper()) / len(letters)
                        if letters else 0
                    )
                    if upper_ratio >= 0.72 and len(re.findall(r'\w+', chapter_rest)) <= 24:
                        subtitle = _clean_heading_text(chapter_rest)
                        html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                        pending_chapter_subtitle = False
                        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                        if len(recent_plain) > 5:
                            recent_plain = recent_plain[-5:]
                        continue
                    content_no_refs = chapter_rest
                    h_tag = None
                    pending_chapter_subtitle = False

        if h_tag:
            # Generic all-caps heading absorption split:
            # e.g. "THE DOCTRINE...VINDICATED The doctrine of..."
            ac_match = re.match(
                r'^([A-Z][A-Z\s,;:\u2013\u2014\-\(\)\']{18,}?)'
                r'\s+([A-Z][a-z].{40,})$',
                content_no_refs.strip(),
                re.S,
            )
            if ac_match:
                h_text = ac_match.group(1).strip().rstrip('.')
                b_text = ac_match.group(2).strip()
                letters = [c for c in h_text if c.isalpha()]
                upper_ratio = (
                    sum(1 for c in letters if c.isupper()) / len(letters)
                    if letters else 0
                )
                if upper_ratio >= 0.72 and len(re.findall(r'\w+', h_text)) >= 4:
                    cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
                    html_parts.append(f'<{h_tag}{cls}>{h_text}</{h_tag}>')
                    content_no_refs = b_text
                    h_tag = None

        if not h_tag:
            chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
            if chapter_match:
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_subtitle = _clean_heading_text(chapter_match.group(2) or '')
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if chapter_subtitle:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(chapter_subtitle))}</h4>')
                    pending_chapter_subtitle = False
                else:
                    pending_chapter_subtitle = True
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

            # PART/BOOK/SECTION headings → premium title-page style
            part_book_match = re.match(
                r'^(PART|BOOK|SECTION)\s+([IVXLCDM\d]+)(?:\s*[.—–-]\s*(.*))?$',
                content_no_refs.strip(),
                re.I,
            )
            if part_book_match:
                part_label = part_book_match.group(0).strip()
                html_parts.append(
                    f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">'
                    f'{part_label}</h1>'
                )
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

        if pending_chapter_subtitle and not h_tag:
            # Detect italic chapter subtitles (Volume 2 pattern)
            italic_subtitle = re.match(
                r'^_(.+)_\s*$', content_no_refs.strip(), re.S
            )
            if italic_subtitle:
                sub_text = italic_subtitle.group(1).strip()
                sub_text = re.sub(r'\s+', ' ', sub_text)
                if len(sub_text) >= 18 and len(re.findall(r'\w+', sub_text)) <= 40:
                    html_parts.append(
                        f'<h4 class="chapter-subtitle">'
                        f'{tag_unicode_ranges(_html_escape(sub_text))}'
                        f'</h4>'
                    )
                    pending_chapter_subtitle = False
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            plain_letters = [c for c in content_no_refs if c.isalpha()]
            upper_ratio = (
                sum(1 for c in plain_letters if c.isupper()) / len(plain_letters)
                if plain_letters else 0
            )
            if len(content_no_refs) >= 18 and upper_ratio >= 0.72:
                subtitle = _clean_heading_text(content_no_refs)
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                pending_chapter_subtitle = False
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            pending_chapter_subtitle = False

        if not h_tag:
            standalone_bold = re.fullmatch(r'\*\*(.+?)\*\*', content_no_refs.strip(), re.S)
            if standalone_bold:
                bold_plain = standalone_bold.group(1).strip()
                letters = [c for c in bold_plain if c.isalpha()]
                upper_ratio = (
                    sum(1 for c in letters if c.isupper()) / len(letters)
                    if letters else 0
                )
                if len(bold_plain) >= 12 and upper_ratio >= 0.72:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(_clean_heading_text(bold_plain)))}</h4>')
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

        subtitle_md = None
        if not h_tag:
            subtitle_md, content_no_refs = _split_leading_chapter_subtitle(content_no_refs)

        roman_heading = None
        if not h_tag and not subtitle_md:
            roman_match = ROMAN_HEADING_RE.match(content_no_refs)
            if roman_match:
                roman_number = _roman_to_int(roman_match.group('roman'))
                rest_after_roman = roman_match.group('rest').strip()
                previous_text = recent_plain[-1] if recent_plain else ''
                starts_roman_list = (
                    roman_number in (1, 2)
                    and (
                        re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                        or re.search(r'(?:[—-]|,)\s*$', previous_text)
                    )
                )
                continues_roman_list = roman_list_expected == roman_number
                if (starts_roman_list or continues_roman_list) and _is_roman_list_item(rest_after_roman):
                    content_no_refs = f'**{roman_match.group("roman")}** {rest_after_roman}'
                    is_centered_roman_list = True
                    roman_list_expected = roman_number + 1
                else:
                    roman_heading = roman_match.group('roman')
                    content_no_refs = rest_after_roman
                    roman_list_expected = None
            else:
                roman_list_expected = None
        
        # Convert **bold** → <b>, _italic_ → <i>
        text_html = content_no_refs
        text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', r'**\1**', text_html)
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)
        text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(
            r'^(<b>A\.</b>\s+)([^<]{6,180}?[.!?;])\s+<b>A\.</b>\s+\2',
            r'\1\2',
            text_html,
            flags=re.I,
        )
        text_html = emphasize_structural_prefix(text_html)
        text_html = re.sub(r'(\b(?:verse|verses|chap|chapter)\.?\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html, flags=re.I)
        text_html = re.sub(r'(\b\d+:\d+(?:[-,]\s*\d+)*,\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html)
        text_html = re.sub(r'<b>(\d+(?:st|nd|rd|th))</b>(\s+(?:Psalm|Psalms)\b)', r'\1\2', text_html)
        
        # Tag Unicode Greek/Hebrew ranges
        text_html = tag_unicode_ranges(text_html)
        text_html = _restore_footnote_placeholders(text_html)

        plain_for_class = re.sub(r'<[^>]+>', '', text_html)
        plain_for_class = re.sub(r'\s+', ' ', plain_for_class).strip()
        
        if h_tag:
            cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
            html_parts.append(f'<{h_tag}{cls}>{text_html}</{h_tag}>')
        elif text_html.startswith('---') or text_html.startswith('***'):
            html_parts.append('<hr/>')
        elif is_centered_roman_list:
            html_parts.append(f'<p class="roman-list-item">{text_html}</p>')
        else:
            if subtitle_md:
                subtitle_html = _clean_heading_text(subtitle_md)
                subtitle_html = tag_unicode_ranges(subtitle_html)
                roman_match = re.match(r'^(?P<title>.+?)\s+(?P<roman>[IVXLCDM]+\.?)$', subtitle_html)
                if roman_match and len(roman_match.group('title')) >= 18:
                    html_parts.append(f'<h4 class="chapter-subtitle">{roman_match.group("title")}</h4>')
                    html_parts.append(f'<h4 class="chapter-subtitle roman-subheading">{roman_match.group("roman")}</h4>')
                else:
                    html_parts.append(f'<h4 class="chapter-subtitle">{subtitle_html}</h4>')
            if roman_heading:
                html_parts.append(f'<h4 class="roman-subheading">{roman_heading}</h4>')
            if plain_for_class in {
                'Glory be to God on high!',
                'To Him be all glory and honor for evermore! Amen.',
            }:
                html_parts.append(f'<p class="doxology">{text_html}</p>')
            else:
                for paragraph_html in _split_rendered_inline_structural_html(text_html):
                    html_parts.append(f'<p>{paragraph_html}</p>')

        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
        if len(recent_plain) > 5:
            recent_plain = recent_plain[-5:]
    
    return '\n'.join(html_parts)


def find_cover(vol_num):
    """Find cover image for a volume."""
    covers_dir = os.path.join(_SCRIPT_DIR, 'covers')
    for ext in ('.jpeg', '.jpg', '.png'):
        path = os.path.join(covers_dir, f'v{vol_num}{ext}')
        if os.path.exists(path):
            return path
    return None


def find_portrait(vol_num=None):
    """Find a portrait image."""
    p_dir = os.path.join(_SCRIPT_DIR, 'portraits')
    if not os.path.isdir(p_dir):
        return None
    files = sorted([f for f in os.listdir(p_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))])
    if not files:
        return None
    idx = int(hashlib.md5(f'owen-v{vol_num}'.encode()).hexdigest(), 16) % len(files)
    return os.path.join(p_dir, files[idx])


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


def generate_frontispiece_xhtml(portrait_filename):
    return f'<div class="frontispiece"><img src="images/{portrait_filename}" alt="Portrait of John Owen"/><p class="caption">John Owen (1616&#x2013;1683)</p></div>'


def generate_nav_xhtml(toc_entries, volume_title=None, has_cover=False, has_frontispiece=False, first_content_href=None):
    """Generate 3-level NAV XHTML with EPUB3 landmarks."""
    display_title = _html_escape(volume_title or 'Table of Contents')
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">',
        '<head>',
        f'  <title>{display_title}</title>',
        '  <link href="style/main.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        f'<nav epub:type="toc" id="toc" role="doc-toc">',
        f'<h2>{display_title}</h2>',
    ]
    
    current_level = 0
    stack = []
    for level, text, href in toc_entries:
        level = max(1, min(level, 3))
        if level > current_level + 1:
            level = current_level + 1
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
        
        lines.append(f'<li><a href="{_html_escape(href)}">{_html_escape(text)}</a>')
        stack.append('li')
        current_level = level
    
    while stack:
        lines.append(f'</{stack.pop()}>')
    
    lines.append('</nav>')
    
    # Landmarks
    lines.append('<nav epub:type="landmarks">\n<h2>Guide</h2>\n<ol>')
    if has_cover:
        lines.append('  <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    lines.append('  <li><a epub:type="titlepage" href="title.xhtml">Title Page</a></li>')
    lines.append('  <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')
    if has_frontispiece:
        lines.append('  <li><a epub:type="frontispiece" href="frontispiece.xhtml">Frontispiece</a></li>')
    if first_content_href:
        lines.append(f'  <li><a epub:type="bodymatter" href="{first_content_href}">Start of Content</a></li>')
    lines.extend(['</ol>', '</nav>', '</body>', '</html>'])
    
    return '\n'.join(lines)


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
    """Repackage as canonical EPUB3 (mimetype first, no compression)."""
    if os.path.exists(epub_path):
        os.remove(epub_path)
    with open(os.path.join(src_dir, 'mimetype'), 'wb') as f:
        f.write(b'application/epub+zip')
    subprocess.run(['zip', '-0Xq', epub_path, 'mimetype'],
                   cwd=src_dir, check=True)
    subprocess.run(['zip', '-r9q', epub_path, '.', '-x',
                    'mimetype', '-x', '*.DS_Store'],
                   cwd=src_dir, check=True)


def _inject_apple_books_options(epub_path):
    """Post-process EPUB to enable Apple Books specified-fonts option."""
    tmp = epub_path + '.tmp'
    with zipfile.ZipFile(epub_path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename.endswith('.opf'):
                    text = data.decode('utf-8')
                    opts = (
                        '\n<display-options xmlns="http://www.apple.com/itunes/vbook/display-options">\n'
                        '  <platform name="*">\n'
                        '    <option name="specified-fonts">true</option>\n'
                        '  </platform>\n'
                        '</display-options>\n'
                    )
                    text = text.replace('</metadata>', '</metadata>' + opts)
                    data = text.encode('utf-8')
                zout.writestr(item, data)
    shutil.move(tmp, epub_path)


# ================================================================
# MAIN PIPELINE
# ================================================================

def build_endnotes_chapter(footnotes, style_item=None):
    fn_map = {f.fnum: f for f in footnotes.values()}
    parts = ['<section epub:type="footnotes" role="doc-endnotes" hidden="hidden">']
    for fnum in sorted(fn_map.keys()):
        fn = fn_map[fnum]
        fn_text = tag_unicode_ranges(_html_escape(fn.text))
        parts.append(
            f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="fn{fnum}">'
            f'<p class="footnote">'
            f'<span class="fn-link">{fnum}</span> '
            f'{fn_text}'
            f'</p></aside>'
        )
    parts.append('</section>')
    html = ''.join(parts)
    return _make_xhtml('Footnotes', html)


# ================================================================
# FRONT MATTER HANDLING
# ================================================================

_AGES_HEADERS = {'THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION',
                 'Books For The Ages', 'AGES Software', 'Version 1.0',
                 'B o o k s F o r T h e A g e s'}


def detect_page_type(page, page_num=None):
    text_upper = page.get_text().upper()
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if b.get('type') == 0]
    n_blocks = len(text_blocks)

    # TOC detection: any CONTENTS page OR pages with many numbered/chapter items
    if 'CONTENTS' in text_upper and n_blocks > 5:
        return 'toc_page'
    
    # Heuristic for multi-page TOC (pages with high count of "CHAPTER X" or numbered items)
    if n_blocks > 10:
        items_count = 0
        for b in text_blocks:
            b_text = "".join(s['text'] for line in b['lines'] for s in line['spans']).strip()
            # Match "CHAPTER 1", "1. ", "I. ", etc.
            if re.match(r'^(CHAPTER\s+\d+|[IVXLC]+\.|\d+[\.\-])', b_text, re.I):
                items_count += 1
        if items_count > 8:
            return 'toc_page'

    # For first 10 pages: structural detection (sparse blocks + large font)
    if page_num is not None and page_num <= 10:
        if n_blocks < 15:
            max_font = 0
            total_chars = 0
            for b in text_blocks:
                for line in b['lines']:
                    for s in line['spans']:
                        max_font = max(max_font, s['size'])
                        total_chars += len(s['text'])
            if max_font > 14 and total_chars < 800:
                return 'title_page'
        # Body text: too many chars or many blocks → not a structural page
        total_chars = 0
        for b in text_blocks:
            for line in b['lines']:
                for s in line['spans']:
                    total_chars += len(s['text'])
        if total_chars > 800 or n_blocks >= 10:
            return 'body_page'
        return 'preserve_page'

    # Beyond page 10: char-count based title page detection (mid-volume)
    total_chars = 0
    large_chars = 0
    for b in text_blocks:
        for line in b['lines']:
            for s in line['spans']:
                c = len(s['text'])
                total_chars += c
                if s['size'] > 14:
                    large_chars += c
    if total_chars < 1200 and large_chars >= 40:
        return 'title_page'

    # Fallback for mixed title+body pages (e.g. Part titles starting mid-page)
    # ONLY if the total characters are relatively low and font is very large (PART/BOOK)
    if total_chars < 2000:
        for b in text_blocks:
            b_text = "".join(s['text'] for line in b['lines'] for s in line['spans']).strip()
            # Skip page numbers and running headers
            if b_text.isdigit() and len(b_text) <= 4: continue
            if any(h in b_text for h in _AGES_HEADERS): continue
            
            b_max = max(s['size'] for line in b['lines'] for s in line['spans'])
            # Only trigger if we find a very large-font line (e.g. PART X, BOOK X)
            if b_max > 18 and len(b_text) < 40 and not b_text.upper().startswith('CHAPTER'):
                return 'title_page'
            # If we hit a normal block first, it's a body page
            break

    return 'body_page'


def is_toc_continuation_page(page, page_num=None):
    """Detect sparse continuation pages after a visual CONTENTS page."""
    if page_num is not None and page_num > 8:
        return False
    text = page.get_text()
    clean = re.sub(r'\s+', ' ', text).strip()
    if not clean:
        return False
    upper = clean.upper()
    if re.match(r'^\d*\s*(?:GENERAL PREFACE|PREFACE|PREFATORY NOTE|TO THE READER)\b', upper):
        return False
    chapter_hits = len(re.findall(r'\bCHAPTER\s+\d+', upper))
    part_hits = len(re.findall(r'\bPART\s+\d+', upper))
    numbered_hits = len(re.findall(r'(?:^|\s)(?:[IVXLCDM]+\.|\d+\.)\s+[—A-Z]', clean, re.I))
    return (chapter_hits + part_hits + numbered_hits) >= 1


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
            text = re.sub(r'<\d{6}>', '', text).strip()
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
        elif text.upper() in {'OR', 'OF', 'WITH', 'AS ALSO,'}:
            lvl = 'h3'
            cls = ' class="separator"'
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
            lambda m: m.group(1) + _noteref_link(18),
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
        
    parts = ['<section epub:type="toc">']
    
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
                l_text = re.sub(r'<\d{6}>', '', l_text).strip()
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
                parts.append(f'<h2 style="text-align: center;">{safe_text}</h2>')
            # 2. Section Headers (PREFATORY NOTE, PREFACE, etc.)
            elif full_text.isupper() and len(full_text) < 40:
                parts.append(f'<h3 style="text-align: center;">{safe_text}</h3>')
            # 3. TOC Items (CHAPTER 1, 1. -, etc.)
            else:
                # Use .ContentsItem for hanging indent
                # We want to bold the label part if possible
                # Refined regex for labels like "1. —" or "CHAPTER 1."
                match = re.match(r'^((?:CHAPTER\s+\d+|[IVXLC]+\.|[0-9]+[\.\-\s]*[—\-]?)\s*)(.*)', full_text, re.I | re.S)
                if match:
                    label, desc = match.groups()
                    desc_safe = _html_escape(desc.strip())
                    parts.append(f'<p class="ContentsItem"><b>{_html_escape(label)}</b> {desc_safe}</p>')
                else:
                    continuation = _html_escape(re.sub(r'\s+', ' ', full_text).strip())
                    if (
                        parts
                        and 'class="ContentsItem"' in parts[-1]
                        and re.search(r'[;—-]\s*</p>$', parts[-1])
                    ):
                        parts[-1] = parts[-1].replace('</p>', f' {continuation}</p>')
                    else:
                        parts.append(f'<p class="ContentsItem">{safe_text}</p>')
                    
    parts.append('</section>')
    return '\n'.join(parts)


def process_owen_volume(vol_num):
    """Process a single Owen volume from PDF to EPUB3."""
    config = VOLUME_CONFIG.get(vol_num)
    if not config:
        print(f"Error: Unknown volume {vol_num}")
        return False
    
    vol_dir = os.path.join(_SCRIPT_DIR, 'volumes', f'v{vol_num}')
    pdf_path = os.path.join(vol_dir, 'input', f'owen-v{vol_num}.pdf')
    output_dir = os.path.join(vol_dir, 'output')
    intermediate_dir = os.path.join(vol_dir, 'intermediate')
    thml_path = os.path.join(intermediate_dir, f'volume_{vol_num}.thml.xml')
    os.makedirs(output_dir, exist_ok=True)
    
    epub_path = os.path.join(output_dir, f'volume_{vol_num}.epub')
    
    print(f"\n{'='*60}")
    print(f"Volume {vol_num}: {config['title']}")
    print(f"{'='*60}")
    
    if not os.path.exists(pdf_path):
        print(f"  Error: PDF not found at {pdf_path}")
        return False
    
    # ── Open PDF ──
    doc = fitz.open(pdf_path)
    print(f"  Pages: {len(doc)}")
    
    # ── Stage 1-2: Dual Extraction ──
    print(f"  Extracting Markdown skeleton via PyMuPDF4LLM...")
    pages_md = pymupdf4llm.to_markdown(
        pdf_path,
        page_chunks=True,
        show_progress=False
    )
    print(f"  Extracted {len(pages_md)} pages")
    
    # ── Stage 2: AGES Navigation ──
    print(f"  Extracting navigation from PDF outline...")
    nav = extract_ages_nav(doc)
    print(f"  Found {len(nav)} TOC entries")
    
    # ── Stage 4: Footnotes ──
    print(f"  Extracting footnotes...")
    pdf_footnotes = extract_footnotes_from_pdf(doc)
    thml_footnotes = parse_thml_footnotes(thml_path)
    footnotes = merge_footnotes(pdf_footnotes, thml_footnotes)
    print(f"  Footnotes: {len(pdf_footnotes)} PDF + {len(thml_footnotes)} ThML = {len(footnotes)} total")
    
    # ── Stage 5: Build Chapters ──
    print(f"  Building chapters...")
    chapters = build_chapters_from_toc(doc, pages_md, nav, footnotes)
    print(f"  Created {len(chapters)} chapters")
    
    # ── Stage 6: EPUB3 Assembly ──
    print(f"  Assembling EPUB3...")
    
    body_font = config.get('body_font', 'SBL_BLit')
    primary = select_primary_font(body_font)
    font_styles = generate_font_styles(primary['name'], primary['files'])
    
    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-pymupdf-v{vol_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(config['title'])
    book.set_language('en')
    book.set_direction('ltr')
    
    # Primary Author
    for i, author in enumerate(config.get('authors', [])):
        uid = 'creator' if i == 0 else f'aut_{i}'
        book.add_author(author, role='aut', uid=uid)
        
    # Editor as Contributor
    for i, editor in enumerate(config.get('editors', [])):
        book.add_author(editor, role='edt', uid=f'edt_{i}')

        
    # Secondary Languages
    for lang in config.get('secondary_languages', []):
        book.add_metadata('DC', 'language', lang)
    
    book.add_metadata('DC', 'publisher', config.get('publisher', 'Eduardus Ekofius'))
    
    # CSS — merge @font-face into main.css (ebooklib strips inline <style>)
    combined_css = EPUB_STYLESHEET.rstrip('\n') + '\n' + font_styles.lstrip('\n')
    style_item = epub.EpubItem(
        uid="css",
        file_name="style/main.css",
        media_type="text/css",
        content=combined_css.encode('utf-8')
    )
    book.add_item(style_item)
    
    # Fonts — track by filename to avoid duplicates
    font_fnames = set()
    for f_file in primary['files'].values():
        fname = os.path.basename(f_file)
        if fname in font_fnames:
            continue
        src = os.path.join(FONT_BASE, f_file)
        if os.path.exists(src):
            uid = f'f_{fname.replace(".","_")}'
            book.add_item(epub.EpubItem(
                uid=uid,
                file_name=f'Fonts/{fname}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            font_fnames.add(fname)
    
    for fname, fpath in SBL_SUPPLEMENTS.items():
        fbase = os.path.basename(fpath)
        if fbase in font_fnames:
            continue
        src = os.path.join(FONT_BASE, fpath)
        if os.path.exists(src):
            uid = f'f_{fbase.replace(".","_")}'
            book.add_item(epub.EpubItem(
                uid=uid,
                file_name=f'Fonts/{fbase}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            font_fnames.add(fbase)
    
    for fname, fpath in EZRA_SIL_FILES.items():
        fbase = os.path.basename(fpath)
        if fbase in font_fnames:
            continue
        src = os.path.join(FONT_BASE, fpath)
        if os.path.exists(src):
            uid = f'f_{fbase.replace(".","_")}'
            book.add_item(epub.EpubItem(
                uid=uid,
                file_name=f'Fonts/{fbase}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            font_fnames.add(fbase)
    
    # Cover
    cover_file = find_cover(vol_num)
    cover_item = None
    if cover_file:
        ext = os.path.splitext(cover_file)[1].lower()
        cover_fname = f'images/cover{ext}'
        mime = 'image/png' if ext == '.png' else 'image/jpeg'
        with open(cover_file, 'rb') as fh:
            book.add_item(epub.EpubItem(
                uid="cover-img",
                file_name=cover_fname,
                media_type=mime,
                content=fh.read()
            ))
        cover_item = epub.EpubHtml(title="Cover", file_name="cover.xhtml", lang='en')
        cover_item.set_content(
            _make_xhtml("Cover",
                f'<div style="text-align:center; margin:0; padding:0;">'
                f'<img src="{cover_fname}" alt="Cover" style="max-width:100%; max-height:100%;"/>'
                f'</div>'
            ).encode('utf-8')
        )
        cover_item.add_item(style_item)
        book.add_item(cover_item)
    
    # Portrait
    portrait_file = find_portrait(vol_num)
    frontispiece_item = None
    if portrait_file:
        p_fn = f"portrait{os.path.splitext(portrait_file)[1]}"
        book.add_item(epub.EpubItem(
            uid="portrait-img",
            file_name=f"images/{p_fn}",
            media_type="image/jpeg",
            content=open(portrait_file, 'rb').read()
        ))
        frontispiece_item = epub.EpubHtml(title="Frontispiece", file_name="frontispiece.xhtml", lang="en")
        frontispiece_item.set_content(
            _make_xhtml("Frontispiece", generate_frontispiece_xhtml(p_fn)).encode('utf-8')
        )
        frontispiece_item.add_item(style_item)
        book.add_item(frontispiece_item)
    
    # ── Front Matter: Detect title/TOC pages from PDF ──
    print(f"  Detecting front matter pages...")
    front_matter_items = []
    healer_page = None
    scan_limit = min(15, len(doc))
    
    # Build set of page indices covered by any chapter (for dedup)
    chapter_pages = set()
    for ch in chapters:
        for p in range(ch.page_start, ch.page_end + 1):
            chapter_pages.add(p)
    
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
            if html_body:
                # Try to extract a more specific title from the first h1 or h2
                title_match = re.search(r'<h[12]>(.*?)</h[12]>', html_body, re.S)
                if title_match:
                    fm_title = title_match.group(1).replace('<br/>', ' ').strip()
                    # Clean up title
                    fm_title = re.sub(r'\s+', ' ', fm_title)
                    if len(fm_title) > 50:
                        fm_title = fm_title[:47] + "..."
                else:
                    fm_title = "Title Page"
                    
                fm = epub.EpubHtml(title=fm_title, file_name=f"title_{pg}.xhtml", lang='en')
                fm.set_content(_make_xhtml(fm_title, html_body).encode('utf-8'))
                fm.add_item(style_item)
                book.add_item(fm)
                front_matter_items.append(fm)
        
        elif ptype == 'toc_page':
            # Collect all consecutive toc_pages
            toc_pages = [page]
            next_pg = pg + 1
            while next_pg < scan_limit:
                if (
                    detect_page_type(doc[next_pg], next_pg + 1) == 'toc_page'
                    or is_toc_continuation_page(doc[next_pg], next_pg + 1)
                ):
                    toc_pages.append(doc[next_pg])
                    next_pg += 1
                else:
                    break
                    
            html_body = build_toc_page_xhtml(toc_pages)
            if html_body:
                fm = epub.EpubHtml(title="Contents", file_name=f"contents_{pg}.xhtml", lang='en')
                fm.set_content(_make_xhtml("Contents", html_body).encode('utf-8'))
                fm.add_item(style_item)
                book.add_item(fm)
                front_matter_items.append(fm)
            pg = next_pg
            continue
        
        elif ptype == 'preserve_page':
            # Use same logic as format_title_page to preserve structure, but different class
            html_body = format_title_page(page, section_class="preserved-layout", epub_type="frontmatter")
            if html_body:
                fm = epub.EpubHtml(title=f"Page {pg+1}", file_name=f"front_{pg}.xhtml", lang='en')
                fm.set_content(_make_xhtml(f"Page {pg+1}", html_body).encode('utf-8'))
                fm.add_item(style_item)
                book.add_item(fm)
                front_matter_items.append(fm)
        
        else:
            # body_page — check for healer-mode transition
            # Require common section markers AND reasonable text density
            has_indicator = any(kw in text_upper for kw in ['PREFACE', 'CHAPTER', 'TREATISE', 'CATECHISM', 'DISCOURSE'])
            if has_indicator and n_blocks > 10:
                if healer_page is None:
                    healer_page = pg
                    break
        pg += 1
    
    if healer_page is None:
        healer_page = scan_limit
    
    # Template-based title page (clean fallback)
    subtitle_val = VOLUME_SUBTITLES.get(vol_num, "")
    tp_item = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang="en")
    tp_item.set_content(
        _make_xhtml("Title Page", _build_title_page(vol_num, config['title'], subtitle_val)).encode('utf-8')
    )
    tp_item.add_item(style_item)
    book.add_item(tp_item)
    
    # Chapters
    toc_entries = []
    epub_chapters = []
    last_l1_text = None
    guide_landmarks = [("Title Page", "title.xhtml")]
    chapter_subtitles = {}  # cid -> subtitle text for NAV enrichment
    
    for i, chap in enumerate(chapters):
        if chap.is_endnotes or chap.title.strip().lower() == 'footnotes':
            continue
        
        # Chapter body text should always use the paragraph healer. The
        # front-matter preservation path handles title/TOC pages separately;
        # disabling the healer for early chapters causes false paragraph
        # breaks in sections like the General Preface.
        healer_active = True
        
        # Detect mid-volume title pages (book/treatise titles)
        first_page = doc[chap.page_start]
        
        # Skip title detection if this chapter starts on the same page as the previous one
        # (prevents duplicate title pages when a title and chapter start together)
        if i > 0 and chapters[i].page_start == chapters[i-1].page_start:
            ptype = 'body_page'
        else:
            ptype = detect_page_type(first_page, chap.page_start + 1)
        
        if ptype == 'title_page':
            # If the next chapter starts on this same page, then this is a structural
            # entry (e.g. PART 2). We limit title extraction and skip separate body.
            shares_page = (i + 1 < len(chapters) and chapters[i+1].page_start == chap.page_start)
            title_html = restore_dropped_title_noteref(
                format_title_page(first_page, limit_to_title=shares_page),
                chap,
                vol_num,
            )
            
            xhtml_title = chap.title
            tp_fn = f'{chap.cid}_title.xhtml'
            tp_ch = epub.EpubHtml(title=xhtml_title, file_name=tp_fn, lang='en')
            tp_ch.set_content(_make_xhtml(xhtml_title, title_html).encode('utf-8'))
            tp_ch.add_item(style_item)
            book.add_item(tp_ch)
            epub_chapters.append(tp_ch)
            guide_landmarks.append((xhtml_title, tp_fn))
            
            if shares_page:
                has_content = False
            else:
                body_start_page = chap.page_start + 1
                has_content = chap.page_end >= body_start_page
                if has_content:
                    md_text = get_pages_text(doc, pages_md, body_start_page, chap.page_end, healer_mode=healer_active)
                    body_html = markdown_to_html(md_text)
                    has_content = bool(body_html.strip())
                    if has_content:
                        body = f'<section>{body_html}</section>'
                        ch = epub.EpubHtml(title=xhtml_title, file_name=f'{chap.cid}.xhtml', lang='en')
                        ch.set_content(_make_xhtml(xhtml_title, body).encode('utf-8'))
                        ch.add_item(style_item)
                        book.add_item(ch)
                        epub_chapters.append(ch)
                        subtitle_m = re.search(
                            r'<h4 class="chapter-subtitle">([^<]+)</h4>',
                            body_html,
                        )
                        if subtitle_m:
                            chapter_subtitles[chap.cid] = subtitle_m.group(1).strip()
            
            # TOC href: title page if no body content, content file otherwise
            toc_href = tp_fn if not has_content else f'{chap.cid}.xhtml'
        else:
            body_end = chap.page_end
            if i + 1 < len(chapters):
                next_start = chapters[i+1].page_start
                if next_start > chap.page_start and next_start <= body_end:
                    body_end = next_start - 1
            md_text = get_pages_text(doc, pages_md, chap.page_start, body_end, healer_mode=healer_active)
            body_html = markdown_to_html(md_text)
            if not body_html.strip():
                continue
            xhtml_title = chap.title
            body = f'<section>{body_html}</section>'
            ch = epub.EpubHtml(title=xhtml_title, file_name=f'{chap.cid}.xhtml', lang='en')
            ch.set_content(_make_xhtml(xhtml_title, body).encode('utf-8'))
            ch.add_item(style_item)
            book.add_item(ch)
            epub_chapters.append(ch)
            toc_href = f'{chap.cid}.xhtml'
            subtitle_m = re.search(
                r'<h4 class="chapter-subtitle">([^<]+)</h4>',
                body_html,
            )
            if subtitle_m:
                chapter_subtitles[chap.cid] = subtitle_m.group(1).strip()
        
        clean_t = chap.title
        # Enrich NAV display title with chapter subtitle
        sub_text = chapter_subtitles.get(chap.cid, '')
        if sub_text and clean_t.upper().startswith('CHAPTER'):
            subtitle_display = _clean_heading_text(sub_text)
            clean_t = f'{clean_t} — {subtitle_display}'
        epub_level = chap.level
        if epub_level <= 2:
            epub_level = 1
        elif epub_level == 3:
            epub_level = 2
        else:
            epub_level = 3
        
        if epub_level == 1:
            if clean_t != last_l1_text:
                toc_entries.append((1, nav_display_title(clean_t), toc_href))
                last_l1_text = clean_t
        elif epub_level == 2:
            lvl = 2 if last_l1_text else 1
            toc_entries.append((lvl, nav_display_title(clean_t), toc_href))
        else:
            toc_entries.append((3, clean_t, toc_href))
    
    # Endnotes chapter
    if footnotes:
        endnotes_html = build_endnotes_chapter(footnotes, style_item)
        en = epub.EpubHtml(title="Footnotes", file_name="endnotes.xhtml", lang='en')
        en.set_content(endnotes_html.encode('utf-8'))
        en.add_item(style_item)
        book.add_item(en)
    
    # Front matter NAV entries (skip generic "Page N" preserve entries and deduplicate)
    fm_entries = []
    seen_titles = set()
    for fm in front_matter_items:
        fm_title = getattr(fm, 'title', 'Front Matter') or 'Front Matter'
        fm_fn = getattr(fm, 'file_name', '')
        if fm_fn and not fm_title.startswith('Page ') and fm_title not in seen_titles:
            fm_entries.append((1, fm_title, fm_fn))
            seen_titles.add(fm_title)
    
    toc_entries = fm_entries + toc_entries
    
    # NAV
    full_t = f"The Works of John Owen, Vol. {vol_num} — {VOLUME_SUBTITLES.get(vol_num, '')}"
    first_href = toc_entries[len(fm_entries)][2] if len(toc_entries) > len(fm_entries) else None
    nav_html = generate_nav_xhtml(
        toc_entries, full_t,
        has_cover=cover_file is not None,
        has_frontispiece=portrait_file is not None,
        first_content_href=first_href
    )
    nav_item = epub.EpubHtml(title='Table of Contents', file_name='nav.xhtml', lang='en')
    nav_item.id = 'nav'
    nav_item.set_content(nav_html.encode('utf-8'))
    nav_item.properties = ['nav']
    nav_item.add_item(style_item)
    book.add_item(nav_item)
    
    # Spine: cover → title → frontispiece → front matter → chapters.
    # Keep nav.xhtml as the EPUB3 navigation document, but do not expose it as
    # a reading-order chapter; Apple Books otherwise opens with the redundant
    # Guide/Table-of-Contents page.
    spine_items = []
    if cover_item:
        spine_items.append(cover_item)
    spine_items.append(tp_item)
    if frontispiece_item:
        spine_items.append(frontispiece_item)
    spine_items.extend(front_matter_items)
    spine_items.extend(epub_chapters)
    book.spine = spine_items
    
    # Write EPUB
    temp_epub = epub_path + '.tmp'
    epub.write_epub(temp_epub, book, {})
    
    # Repackage with proper EPUB3 structure
    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(temp_epub, 'r') as zf:
        zf.extractall(tmp)
    
    # Find OEBPS directory
    oebps = None
    for root, dirs, files in os.walk(tmp):
        if any(f.endswith('.opf') for f in files):
            oebps = root
            break
    
    if oebps:
        # Fix NAV
        with open(os.path.join(oebps, 'nav.xhtml'), 'w') as f:
            f.write(nav_html)
        
        # NCX
        with open(os.path.join(oebps, 'toc.ncx'), 'w') as f:
            f.write(generate_ncx(full_t, str(vol_uuid), toc_entries))
        
        # Fix OPF
        opf_path = os.path.join(oebps, 'content.opf')
        if os.path.exists(opf_path):
            with open(opf_path, 'r') as f:
                opf = f.read()
            opf = opf.replace('version="2.0"', 'version="3.0"')
            opf = opf.replace('.html"', '.xhtml"')
            opf = re.sub(r'\s+properties="nav"', '', opf)
            opf = re.sub(r'(href="nav\.xhtml"[^>]*?)/?>', r'\1 properties="nav"/>', opf)
            # Cover meta
            if cover_file and '<meta name="cover"' not in opf:
                opf = opf.replace('</metadata>', '  <meta name="cover" content="cover-img"/>\n  </metadata>')
            if 'href="toc.ncx"' not in opf:
                opf = opf.replace(
                    '</manifest>',
                    '  <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n  </manifest>'
                )
            if '<spine' in opf and 'toc="ncx"' not in opf:
                opf = opf.replace('<spine', '<spine toc="ncx"')
            if guide_landmarks:
                guide_entries = '\n'.join(
                    f'    <reference type="title-page" title="{_escape_xml(t)}" href="{h}"/>'
                    for t, h in guide_landmarks
                )
                guide_block = f'\n  <guide>\n{guide_entries}\n  </guide>'
                if '<guide>' not in opf:
                    opf = opf.replace('</package>', guide_block + '\n</package>')
            with open(opf_path, 'w') as f:
                f.write(opf)
    
    repackage_canonical(epub_path, tmp)
    shutil.rmtree(tmp)
    if os.path.exists(temp_epub):
        os.remove(temp_epub)
    
    _inject_apple_books_options(epub_path)
    
    doc.close()
    print(f"  ✓ EPUB saved: {epub_path}")
    return True


def process_all_volumes():
    """Process all 16 Owen volumes."""
    for vol_num in range(1, 17):
        process_owen_volume(vol_num)


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Owen Works PyMuPDF EPUB3 Converter')
    parser.add_argument('volumes', nargs='*', type=int,
                       help='Volume numbers to process (default: all 16)')
    parser.add_argument('--hebrews', action='store_true',
                       help='Process Hebrews commentary volumes')
    parser.add_argument('--test', action='store_true',
                       help='Test mode: process volume 1 only')
    
    args = parser.parse_args()
    
    if args.test:
        process_owen_volume(1)
    elif args.hebrews:
        print("Hebrews pipeline not yet implemented")
    elif args.volumes:
        for v in args.volumes:
            process_owen_volume(v)
    else:
        process_all_volumes()
