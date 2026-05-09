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
TOP_MARGIN = 65        # Redact text blocks above this y (pts)
BOTTOM_MARGIN = 50     # Redact text blocks below page_height - this
PAGE_W = 410           # Standard page width for Owen PDFs
PAGE_H = 626           # Standard page height for Owen PDFs

# ─── Font Detection ────────────────────────────────────────────
GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}
FOOTNOTE_MARKER_RE = re.compile(r'\[f(\d+)\]')
FT_MARKER_RE = re.compile(r'^FT(\d+)\s*')

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

def extract_footnotes_from_pdf(doc):
    """
    Extract footnotes from the FOOTNOTES section of the PDF.
    Each footnote has an FT{N} marker followed by text.
    """
    footnotes = {}
    in_footnotes = False
    current_fn = None
    current_text = []
    
    for pg in range(len(doc)):
        page = doc[pg]
        text = page.get_text()
        
        if 'FOOTNOTES' in text and not in_footnotes:
            in_footnotes = True
        
        if not in_footnotes:
            continue
        
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if b['type'] != 0:
                continue
            for line in b['lines']:
                line_text = ''.join(s['text'] for s in line['spans'])
                line_text = line_text.strip()
                
                if not line_text:
                    continue
                
                # Check for FT marker
                ft_match = FT_MARKER_RE.match(line_text)
                if ft_match:
                    # Save previous footnote
                    if current_fn is not None and current_text:
                        combined = ' '.join(current_text).strip()
                        combined = combined.strip()
                        if combined:
                            text_clean = combined
                            # Convert any Greek in footnote text
                            for span in line['spans']:
                                font = span.get('font', '')
                                if any(gf in font for gf in GREEK_FONTS):
                                    text_clean = convert_greek_word(text_clean)
                            footnotes[current_fn] = text_clean
                    
                    current_fn = int(ft_match.group(1))
                    rest = line_text[ft_match.end():].strip()
                    current_text = [rest] if rest else []
                elif current_fn is not None:
                    current_text.append(line_text)
        
        # End of footnotes - check if we've moved past
        if in_footnotes:
            # Check if this is the last page of footnotes
            if pg == len(doc) - 1 or 'FOOTNOTES' not in doc[pg + 1].get_text():
                pass  # continue to next page within footnotes
    
    # Save last footnote
    if current_fn is not None and current_text:
        combined = ' '.join(current_text).strip()
        if combined:
            footnotes[current_fn] = combined
    
    return footnotes


def parse_thml_footnotes(thml_path):
    """Parse existing ThML XML FOOTNOTES section for enriched footnote text."""
    import xml.etree.ElementTree as ET
    footnotes = {}
    
    if not os.path.exists(thml_path):
        return footnotes
    
    try:
        tree = ET.parse(thml_path)
        root = tree.getroot()
        
        # Find the footnotes div
        for div1 in root.findall('.//div1'):
            title = (div1.get('title') or '').upper()
            if title == 'FOOTNOTES':
                fn_num = None
                fn_parts = []
                
                for elem in div1.iter():
                    if elem.tag == 'a' and elem.get('class') == 'fnmarker':
                        # Save previous footnote
                        if fn_num is not None and fn_parts:
                            text = ''.join(fn_parts).strip()
                            if text:
                                footnotes[fn_num] = text
                        
                        fn_num = int(elem.get('data-fn', '0'))
                        fn_parts = []
                    elif fn_num is not None and elem.text:
                        fn_parts.append(elem.text)
                    elif fn_num is not None and elem.tail:
                        fn_parts.append(elem.tail)
                
                # Save last footnote
                if fn_num is not None and fn_parts:
                    text = ''.join(fn_parts).strip()
                    if text:
                        footnotes[fn_num] = text
                break
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
    for i, (level, title, page_0idx) in enumerate(nav_entries):
        # Determine if this is a treatise title page
        title_upper = title.upper()
        is_treatise = any(kw in title_upper for kw in [
            'CHRISTOLOGIA', 'MEDITATIONS AND DISCOURSES', 'TWO SHORT CATECHISMS',
            'DECLARATION OF THE GLORIOUS', 'A DECLARATION', 'A VINDICATION'
        ])
        
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
        
        chap = Chapter(
            cid=cid,
            title=title_case(title) if not is_treatise else title,
            level=level,
            page_start=page_0idx,
            page_end=end_page,
            is_treatise=is_treatise,
        )
        chapters.append(chap)
    
    return chapters


def clean_text(text):
    """Sanitize extracted text before paragraph reconstruction."""
    if not text:
        return ''
    # 1. Remove CCEL/AGES scripture reference codes: <450503>
    text = re.sub(r'<\d[A-Za-z0-9]{5}>', '', text)
    # 2. Remove AGES running headers (whole-line removal)
    text = re.sub(
        r'^.*(?:THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|'
        r'BOOKS FOR THE AGES|AGES SOFTWARE|VERSION \d\.\d|'
        r'VOLUME \d+|JOHN OWEN COLLECTION|Books For The Ages).*$',
        '', text, flags=re.MULTILINE | re.IGNORECASE
    )
    # 3. Collapse multiple spaces → single space
    text = re.sub(r' {2,}', ' ', text)
    # 4. Strip leading/trailing whitespace per line
    text = '\n'.join(line.strip() for line in text.split('\n'))
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
        
        # De-hyphenation: strip trailing hyphen, merge with no space
        if current and current[-1].endswith('-'):
            current[-1] = current[-1][:-1] + stripped
            continue
        
        if current:
            prev = current[-1]
            ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
            starts_lower = bool(re.match(r'^[a-z0-9({\[\'"\u201c\u2018]', stripped))
            
            if not ends_terminal:
                # Line does not end with terminal punctuation → join
                current.append(stripped)
            elif starts_lower:
                # Starts lowercase after terminal (e.g. middle of quotation) → join
                current.append(stripped)
            else:
                # Terminal punctuation + uppercase start → new paragraph
                paragraphs.append(' '.join(current))
                current = [stripped]
        else:
            current = [stripped]
    
    if current:
        paragraphs.append(' '.join(current))
    
    return paragraphs


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

    When healer_mode=False, returns clean raw text without paragraph
    reconstruction (used for layout-preserved front matter pages).
    """
    all_paragraphs = []
    prev_page_last = ''
    
    for pg in range(start_page, min(end_page + 1, len(doc))):
        raw = get_merged_page_text(doc, pages_md, pg)
        if not raw.strip():
            continue
        
        # Clean: strip scripture codes, headers, normalize whitespace
        cleaned = clean_text(raw)
        if not cleaned:
            continue
        
        if healer_mode:
            # Reconstruct: heal broken lines into paragraphs
            page_paras = reconstruct_paragraphs(cleaned)
            if not page_paras:
                continue
            # Deduplicate at page junction
            if prev_page_last:
                page_paras[0] = deduplicate_junction(prev_page_last, page_paras[0])
                if not page_paras[0].strip():
                    page_paras.pop(0)
            prev_page_last = page_paras[-1]
        else:
            page_paras = [cleaned]
        
        all_paragraphs.extend(page_paras)
    
    return '\n\n'.join(all_paragraphs)


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

def tag_unicode_ranges(text):
    """Wrap untagged Greek and Hebrew Unicode runs in spans."""
    if not text:
        return ""
    text = re.sub(
        r'([\u0370-\u03FF\u1F00-\u1FFF]{2,})',
        lambda m: f'<span lang="el" xml:lang="el">{m.group(1)}</span>'
        if any(c.strip() for c in m.group(1)) else m.group(1),
        text
    )
    text = re.sub(
        r'([\u0590-\u05FF]{2,})',
        lambda m: f'<span lang="he" xml:lang="he" dir="rtl">{m.group(1)}</span>'
        if any(c.strip() for c in m.group(1)) else m.group(1),
        text
    )
    text = text.replace('</span><span lang="el" xml:lang="el">', '')
    text = text.replace('</span><span lang="he" xml:lang="he" dir="rtl">', '')
    return text


def _escape_xml(text):
    if text is None:
        return ""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def _make_xhtml(title, body_html, css_href='style/main.css', font_styles=None):
    safe_title = _escape_xml(title)
    style_block = f'\n<style type="text/css">{font_styles}</style>\n' if font_styles else ''
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
        f'  {style_block}\n'
        '</head>\n'
        f'<body>{body_html}</body>\n'
        '</html>'
    )


def markdown_to_html(md_text):
    """
    Convert paragraph-healed text to clean XHTML.
    Input is paragraphs separated by double newlines.
    Handles headings, bold, italic, and footnote refs.
    """
    if not md_text:
        return ''
    
    html_parts = []
    paragraphs = md_text.split('\n\n')
    
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
        
        # Process footnote markers [fN]
        ref_nums = FOOTNOTE_MARKER_RE.findall(content)
        content_no_refs = FOOTNOTE_MARKER_RE.sub('', content).strip()
        
        # Convert **bold** → <b>, _italic_ → <i>
        text_html = content_no_refs
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        
        # Tag Unicode Greek/Hebrew ranges
        text_html = tag_unicode_ranges(text_html)
        
        # Add footnote noteref links
        fn_links = ''
        for rn in ref_nums:
            fn_links += f'<a epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fn{rn}"><sup>{rn}</sup></a>'
        
        if h_tag:
            cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
            html_parts.append(f'<{h_tag}{cls}>{text_html}{fn_links}</{h_tag}>')
        elif text_html.startswith('---') or text_html.startswith('***'):
            html_parts.append('<hr/>')
        else:
            html_parts.append(f'<p>{text_html}{fn_links}</p>')
    
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
<p class="publisher">Banner of Truth Trust</p>
</div>'''


def generate_frontispiece_xhtml(portrait_filename):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>Frontispiece</title>
<link href="style/main.css" rel="stylesheet" type="text/css"/></head>
<body><div class="frontispiece">
<img src="images/{portrait_filename}" alt="Portrait"/>
<p class="caption">John Owen (1616–1683)</p>
</div></body></html>'''


def generate_nav_xhtml(toc_entries, volume_title=None):
    """Generate 3-level NAV XHTML."""
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
    
    lines.extend(['</nav>', '</body>', '</html>'])
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


# ================================================================
# MAIN PIPELINE
# ================================================================

def build_endnotes_chapter(footnotes, style_item=None, font_styles=None):
    """
    Build the endnotes XHTML chapter from merged footnotes.
    """
    fn_map = {f.fnum: f for f in footnotes.values()}
    
    parts = ['<section epub:type="endnotes" role="doc-endnotes">',
             '<h1>Footnotes</h1>']
    for fnum in sorted(fn_map.keys()):
        fn = fn_map[fnum]
        fn_text = tag_unicode_ranges(fn.text)
        parts.append(
            f'<aside epub:type="endnote" role="doc-endnote" id="fn{fnum}">'
            f'<p class="footnote">'
            f'<a href="#fn{fnum}" class="fn-link">{fnum}</a> '
            f'{_escape_xml(fn_text)}'
            f'</p></aside>'
        )
    parts.append('</section>')
    
    html = ''.join(parts)
    return _make_xhtml('Footnotes', html, font_styles=font_styles)


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
    
    vol_name = f'owen-v{vol_num}'
    primary = select_primary_font(vol_name)
    font_styles = generate_font_styles(primary['name'], primary['files'])
    
    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-pymupdf-v{vol_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(config['title'])
    book.set_language('en')
    for author in config['authors']:
        book.add_author(author)
    
    # CSS
    style_item = epub.EpubItem(
        uid="css",
        file_name="style/main.css",
        media_type="text/css",
        content=EPUB_STYLESHEET.encode('utf-8')
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
    
    # Cover
    cover_file = find_cover(vol_num)
    if cover_file:
        book.set_cover("images/cover.png", open(cover_file, 'rb').read())
    
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
            _make_xhtml("Frontispiece", generate_frontispiece_xhtml(p_fn),
                        font_styles=font_styles).encode('utf-8')
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
        if pg in chapter_pages:
            pg += 1
            continue
            
        page = doc[pg]
        ptype = detect_page_type(page, pg + 1)
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
                fm.set_content(_make_xhtml(fm_title, html_body, font_styles=font_styles).encode('utf-8'))
                fm.add_item(style_item)
                book.add_item(fm)
                front_matter_items.append(fm)
        
        elif ptype == 'toc_page':
            # Collect all consecutive toc_pages
            toc_pages = [page]
            next_pg = pg + 1
            while next_pg < scan_limit and next_pg not in chapter_pages:
                if detect_page_type(doc[next_pg], next_pg + 1) == 'toc_page':
                    toc_pages.append(doc[next_pg])
                    next_pg += 1
                else:
                    break
                    
            html_body = build_toc_page_xhtml(toc_pages)
            if html_body:
                fm = epub.EpubHtml(title="Contents", file_name=f"contents_{pg}.xhtml", lang='en')
                fm.set_content(_make_xhtml("Contents", html_body, font_styles=font_styles).encode('utf-8'))
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
                fm.set_content(_make_xhtml(f"Page {pg+1}", html_body, font_styles=font_styles).encode('utf-8'))
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
        _make_xhtml("Title Page", _build_title_page(vol_num, config['title'], subtitle_val),
                    font_styles=font_styles).encode('utf-8')
    )
    tp_item.add_item(style_item)
    book.add_item(tp_item)
    
    # Chapters
    toc_entries = []
    epub_chapters = []
    last_l1_text = None
    guide_landmarks = []
    
    for i, chap in enumerate(chapters):
        if chap.is_endnotes or chap.title.strip().lower() == 'footnotes':
            continue
        
        healer_active = chap.page_start >= healer_page
        
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
            title_html = format_title_page(first_page, limit_to_title=shares_page)
            
            xhtml_title = chap.title
            tp_fn = f'{chap.cid}_title.xhtml'
            tp_ch = epub.EpubHtml(title=xhtml_title, file_name=tp_fn, lang='en')
            tp_ch.set_content(_make_xhtml(xhtml_title, title_html, font_styles=font_styles).encode('utf-8'))
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
                        ch.set_content(_make_xhtml(xhtml_title, body, font_styles=font_styles).encode('utf-8'))
                        ch.add_item(style_item)
                        book.add_item(ch)
                        epub_chapters.append(ch)
            
            # TOC href: title page if no body content, content file otherwise
            toc_href = tp_fn if not has_content else f'{chap.cid}.xhtml'
        else:
            md_text = get_pages_text(doc, pages_md, chap.page_start, chap.page_end, healer_mode=healer_active)
            body_html = markdown_to_html(md_text)
            if not body_html.strip():
                continue
            xhtml_title = chap.title
            body = f'<section>{body_html}</section>'
            ch = epub.EpubHtml(title=xhtml_title, file_name=f'{chap.cid}.xhtml', lang='en')
            ch.set_content(_make_xhtml(xhtml_title, body, font_styles=font_styles).encode('utf-8'))
            ch.add_item(style_item)
            book.add_item(ch)
            epub_chapters.append(ch)
            toc_href = f'{chap.cid}.xhtml'
        
        clean_t = chap.title
        epub_level = chap.level
        if epub_level <= 2:
            epub_level = 1
        elif epub_level == 3:
            epub_level = 2
        else:
            epub_level = 3
        
        if epub_level == 1:
            if clean_t != last_l1_text:
                toc_entries.append((1, title_case(clean_t), toc_href))
                last_l1_text = clean_t
        elif epub_level == 2:
            lvl = 2 if last_l1_text else 1
            toc_entries.append((lvl, title_case(clean_t), toc_href))
        else:
            toc_entries.append((3, clean_t, toc_href))
    
    # Endnotes chapter
    if footnotes:
        endnotes_html = build_endnotes_chapter(footnotes, style_item, font_styles)
        en = epub.EpubHtml(title="Footnotes", file_name="endnotes.xhtml", lang='en')
        en.set_content(endnotes_html.encode('utf-8'))
        en.add_item(style_item)
        book.add_item(en)
        epub_chapters.append(en)
        toc_entries.append((1, "Footnotes", "endnotes.xhtml"))
    
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
    nav_html = generate_nav_xhtml(toc_entries, full_t)
    nav_item = epub.EpubHtml(title='Table of Contents', file_name='nav.xhtml', lang='en')
    nav_item.set_content(nav_html.encode('utf-8'))
    nav_item.properties = ['nav']
    nav_item.add_item(style_item)
    book.add_item(nav_item)
    
    # Spine
    book.spine = ['nav', tp_item]
    if frontispiece_item:
        book.spine.insert(1, frontispiece_item)
    book.spine.extend(front_matter_items)
    book.spine.extend(epub_chapters)
    
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
