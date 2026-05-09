#!/usr/bin/env python3
"""
John Owen Works — PDF → pdftohtml → EPUB3 Converter

Uses pdftohtml (poppler) as an intermediate instead of ThML XML.
Keeps all styling, fonts, and EPUB3 features from the existing pipeline.

Usage:
  .venv/bin/python3 converter_pdftohtml.py <volume_number>
  .venv/bin/python3 converter_pdftohtml.py          # volume 1 default

Output: volumes/v{N}/output_pdftohtml/volume_{N}.epub
"""

import sys
import os
import re
import uuid
import shutil
import zipfile
import tempfile
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from html import escape as html_escape
from pathlib import Path
from collections import defaultdict

_SCRIPT_DIR = Path(__file__).parent.resolve()
_WORKSPACE = _SCRIPT_DIR
_Parent = _SCRIPT_DIR.parent
if str(_Parent) not in sys.path:
    sys.path.insert(0, str(_Parent))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    convert_greek_word, convert_gideon_hebrew
)

from converter import (
    title_case, _split_nav_title, _is_treatise_title_page,
    _extract_chapter_subtitle, _build_normal_chapter, _build_treatise_title,
    _elem_to_html, _escape_xml
)

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed.")

FONT_BASE = os.path.join(_WORKSPACE, 'fonts')


# ===========================================================================
# DATA STRUCTURES
# ===========================================================================

class TextRun:
    __slots__ = ('text', 'top', 'left', 'width', 'height', 'font_id', 'page_num', 'is_bold', 'is_italic')
    def __init__(self, text, top, left, width, height, font_id, page_num, is_bold=False, is_italic=False):
        self.text = text
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.font_id = font_id
        self.page_num = page_num
        self.is_bold = is_bold
        self.is_italic = is_italic


class FontSpec:
    __slots__ = ('fid', 'size', 'family', 'color', 'is_bold', 'is_italic', 'is_greek', 'is_hebrew')
    def __init__(self, fid, size, family, color):
        self.fid = fid
        self.size = size
        self.family = family
        self.color = color
        self.is_bold = 'Bold' in family
        self.is_italic = 'Italic' in family
        self.is_greek = 'Koine' in family
        self.is_hebrew = 'Gideon' in family


class Line:
    __slots__ = ('segments', 'top', 'page_num', 'left')
    def __init__(self, segments, top, page_num, left=0):
        self.segments = segments        # list of (text, font_spec)
        self.top = top
        self.page_num = page_num
        self.left = left


class Paragraph:
    __slots__ = ('lines', 'page_num', 'kind')
    def __init__(self, lines, page_num):
        self.lines = lines
        self.page_num = page_num
        self.kind = 'body'   # body | heading_1 | heading_2 | chapter_heading | list_item | treatise_title


class Chapter:
    __slots__ = ('title', 'id', 'heading_level', 'paragraphs', 'subtitle', 'is_treatise', 'synthetic_html', 'toc_level')
    def __init__(self, title, cid, heading_level='h1'):
        self.title = title
        self.id = cid
        self.heading_level = heading_level
        self.paragraphs = []
        self.subtitle = ''
        self.is_treatise = False
        self.synthetic_html = None    # set for chapters rendered from ThML (no pdftohtml match)
        self.toc_level = 2            # 1=treatise, 2=chapter, 3=subsection


# ===========================================================================
# PDFTOHTML XML PARSER
# ===========================================================================

def run_pdftohtml(pdf_path):
    pdf_path = str(pdf_path)
    result = subprocess.run(
        ['pdftohtml', '-xml', '-stdout', '-q', pdf_path],
        capture_output=True, text=True, timeout=300
    )
    if result.returncode != 0:
        print(f"  Error running pdftohtml: {result.stderr.strip()}")
        return None
    return result.stdout


def _parse_text_element(text_elem):
    """Extract plain text and detect bold/italic from a pdftohtml <text> element.
    Handles nested tags like <i><b>...</b></i>.
    """
    is_bold = False
    is_italic = False
    
    # Check for bold/italic anywhere in the element or its descendants
    if text_elem.find('.//b') is not None: is_bold = True
    if text_elem.find('.//i') is not None: is_italic = True
    
    # Extract all text in order
    text = "".join(text_elem.itertext())
    return text, is_bold, is_italic


def parse_pdftohtml_xml(xml_text):
    root = ET.fromstring(xml_text)

    # Accumulate all fontspecs across all pages into a global dict
    global_fontspecs = {}
    for page_elem in root.findall('page'):
        for fs in page_elem.findall('fontspec'):
            fid = int(fs.get('id', 0))
            if fid not in global_fontspecs:
                global_fontspecs[fid] = FontSpec(
                    fid=fid,
                    size=float(fs.get('size', 0)),
                    family=fs.get('family', ''),
                    color=fs.get('color', '#000000')
                )

    pages = []
    for page_elem in root.findall('page'):
        page_num = int(page_elem.get('number', 0))
        page_height = int(page_elem.get('height', 0))
        page_width = int(page_elem.get('width', 0))

        runs = []
        for text_elem in page_elem.findall('text'):
            font_id = int(text_elem.get('font', 0))
            text, is_bold, is_italic = _parse_text_element(text_elem)
            if not text.strip():
                continue
            runs.append(TextRun(
                text=text,
                top=int(text_elem.get('top', 0)),
                left=int(text_elem.get('left', 0)),
                width=int(text_elem.get('width', 0)),
                height=int(text_elem.get('height', 0)),
                font_id=font_id,
                page_num=page_num,
                is_bold=is_bold,
                is_italic=is_italic
            ))

        pages.append({
            'num': page_num,
            'height': page_height,
            'width': page_width,
            'fontspecs': global_fontspecs,
            'runs': runs
        })

    return pages


# ===========================================================================
# NOISE FILTERING
# ===========================================================================

AGES_HEADERS = {
    'THE WORKS OF JOHN OWEN',
    'THE AGES DIGITAL LIBRARY',
    'JOHN OWEN COLLECTION',
    'AGES SOFTWARE',
    'ALBANY, OR',
    'WWW.AGESLIBRARY.COM',
    'VERSION',
    'BOOKS FOR THE AGES',
}

SCRIPTURE_CODE_RE = re.compile(r'^<[A-Z0-9]{5,8}>$')
PAGE_NUM_RE = re.compile(r'^\d{1,3}$')


def is_boilerplate(run, fontspec):
    text_upper = run.text.strip().upper()

    # Aggressively catch Scripture codes like <19D001> even if partial
    if '<' in text_upper and '>' in text_upper:
        if SCRIPTURE_CODE_RE.search(text_upper):
            return True

    if text_upper in AGES_HEADERS:
        return True

    if SCRIPTURE_CODE_RE.match(text_upper):
        return True

    if fontspec is not None:
        if len(run.text.strip()) <= 3 and fontspec.size is not None and run.top < 60:
            return True

    return False


def filter_noise(pages):
    for page in pages:
        fontspecs = page['fontspecs']
        filtered = []
        for run in page['runs']:
            fs = fontspecs.get(run.font_id)
            if is_boilerplate(run, fs):
                continue
            filtered.append(run)
        page['runs'] = filtered
    return pages


# ===========================================================================
# FLOW RECONSTRUCTION
# ===========================================================================

def group_runs_into_lines(runs, fontspecs, line_tolerance=5):
    sorted_runs = sorted(runs, key=lambda r: (r.top, r.left))
    lines = []
    current = []
    for run in sorted_runs:
        if not current:
            current.append(run)
        elif abs(run.top - current[-1].top) <= line_tolerance:
            current.append(run)
        else:
            lines.append(current)
            current = [run]
    if current:
        lines.append(current)

    result = []
    for line_runs in lines:
        line_runs.sort(key=lambda r: r.left)
        segments = []
        for run in line_runs:
            fs = fontspecs.get(run.font_id)
            if fs is None:
                fs = FontSpec(fid=run.font_id, size=0, family='?', color='#000000')
            # Override FontSpec bold/italic flags with run-level formatting detected
            # from <b>/<i> tags inside pdftohtml <text> elements.
            if run.is_bold or run.is_italic:
                fs = FontSpec(fid=fs.fid, size=fs.size, family=fs.family, color=fs.color)
                fs.is_bold = run.is_bold or fs.is_bold
                fs.is_italic = run.is_italic or fs.is_italic
            segments.append((run.text, fs))
        if segments:
            result.append(Line(segments, line_runs[0].top, line_runs[0].page_num, left=line_runs[0].left))

    return result


def is_ages_boilerplate_line(line):
    joined = ''.join(s[0] for s in line.segments).strip().upper().replace(' ', '')
    if 'AGESDIGITALLIBRARY' in joined or 'AGES' in joined and 'LIBRARY' in joined:
        return True
    return False


def group_lines_into_paragraphs(lines, page_width):
    if not lines:
        return []

    paras = []
    current_lines = [lines[0]]

    for i in range(1, len(lines)):
        prev = lines[i - 1]
        curr = lines[i]

        curr_text = "".join(s[0] for s in curr.segments).strip().upper()
        
        # Detect centering for current line
        page_mid = page_width / 2
        # Max size in current line for center estimation
        max_s = max((s[1].size for s in curr.segments), default=14)
        est_w = len(curr_text) * (max_s * 0.45)
        line_center = curr.left + (est_w / 2)
        is_centered = abs(line_center - page_mid) < page_width * 0.1
        
        # Force break for common TOC/Chapter markers OR centered lines (titles)
        if curr_text.startswith('CHAPTER') or curr_text.startswith('PART') or curr_text.startswith('BOOK') or is_centered:
            paras.append(Paragraph(current_lines, current_lines[0].page_num))
            current_lines = [curr]
            continue

        line_height = max((s[1].size for s in curr.segments), default=14)
        gap = curr.top - prev.top
        gap_threshold_narrow = line_height * 0.6
        gap_threshold_new = line_height * 1.8

        if gap > gap_threshold_new:
            paras.append(Paragraph(current_lines, current_lines[0].page_num))
            current_lines = [curr]
        elif gap > gap_threshold_narrow:
            curr_left = curr.left
            page_mid = page_width / 2
            is_centered = abs(curr_left - page_mid) < page_width * 0.15
            if curr_left > page_width * 0.15 and not is_centered:
                paras.append(Paragraph(current_lines, current_lines[0].page_num))
                current_lines = [curr]
            else:
                current_lines.append(curr)
        else:
            current_lines.append(curr)

    if current_lines:
        paras.append(Paragraph(current_lines, current_lines[0].page_num))

    return paras


def classify_paragraph(para_lines, page_width):
    first_line = para_lines[0]
    page_mid = page_width / 2
    line_left = first_line.left

    sizes = []
    is_bold = False
    is_greek = False
    is_hebrew = False
    full_text = ""
    for line in para_lines:
        for text, fs in line.segments:
            sizes.append(fs.size)
            if fs.is_bold: is_bold = True
            if fs.is_greek: is_greek = True
            if fs.is_hebrew: is_hebrew = True
            full_text += text

    if not sizes: return 'body'

    max_size = max(sizes)
    first_line_text = "".join(s[0] for s in first_line.segments).strip()
    
    # Estimate line width and center
    est_width = len(first_line_text) * (max_size * 0.45)
    line_center = line_left + (est_width / 2)
    is_centered = abs(line_center - page_mid) < page_width * 0.1
    
    # Large headings (>19) can be a bit more off-center
    if max_size >= 20:
        is_centered = abs(line_center - page_mid) < page_width * 0.15

    # Check if the entire line is bold or if it's short
    is_short = len(first_line_text) < 40
    all_bold = all(fs.is_bold for _, fs in first_line.segments)

    # heading_1: Large, centered, and EITHER all bold OR short (not a long TOC line)
    if max_size >= 20 and is_centered and (all_bold or is_short):
        return 'heading_1'
    
    # heading_2: Medium-large, centered, and EITHER all bold OR short
    if max_size >= 16 and is_centered and (all_bold or is_short):
        return 'heading_2'

    if is_greek: return 'greek'
    if is_hebrew: return 'hebrew'

    text = full_text.strip().upper()
    chapter_pattern = re.compile(
        r'^(CHAPTER|SERMON|DISCOURSE|EXERCITATION|PREFACE|PREFATORY|'
        r'DEDICATION|APPENDIX|SECTION|PART)\b'
    )

    # chapter_heading: must be bold, not indented, and short (to avoid TOC lines)
    is_indented = line_left > page_width * 0.1
    if is_bold and not is_indented and chapter_pattern.match(text) and is_short:
        return 'chapter_heading'

    roman_pattern = re.compile(r'^[IVXLCDM]+\d*\.?')
    if is_bold and is_indented and roman_pattern.match(text):
        return 'list_item'

    return 'body'


def build_paragraph_xhtml(para, fontspecs):
    line_parts = []
    for line in para.lines:
        parts = []
        for text, fs in line.segments:
            if fs.is_greek:
                converted = ' '.join(convert_greek_word(w) for w in text.split())
                parts.append(f'<span lang="el" xml:lang="el">{html_escape(converted)}</span>')
            elif fs.is_hebrew:
                converted = convert_gideon_hebrew(text)
                parts.append(f'<span lang="he" xml:lang="he" dir="rtl">{html_escape(converted)}</span>')
            else:
                # Cleanup common AGES noise in text segments
                text = text.replace('THEGLORIOUS', 'THE GLORIOUS').replace('OFCHRIST', 'OF CHRIST')
                fmt = html_escape(text)
                if fs.is_bold and fs.is_italic:
                    fmt = f'<b><i>{fmt}</i></b>'
                elif fs.is_bold:
                    fmt = f'<b>{fmt}</b>'
                elif fs.is_italic:
                    fmt = f'<i>{fmt}</i>'
                parts.append(fmt)
        line_parts.append(''.join(parts))
    return ' '.join(line_parts)


def build_treatise_title_xhtml(para, fontspecs):
    text = ''.join(s[0] for line in para.lines for s in line.segments).strip()
    return f'<h1>{html_escape(text)}</h1>'


def build_body_paragraph(para, fontspecs):
    html = build_paragraph_xhtml(para, fontspecs)
    return f'<p class="Body">{html}</p>'


# ===========================================================================
# LATIN DETECTION
# ===========================================================================

LATIN_MARKERS = {
    'sola', 'fide', 'gratia', 'christus', 'ecclesia', 'spiritus', 'sanctus',
    'veritas', 'dominus', 'deus', 'jesus', 'gloria', 'etiam', 'quod', 'cum',
    'sed', 'autem', 'enim', 'sunt', 'esse', 'hoc', 'haec', 'homo', 'virtus',
    'opera', 'opus', 'lex', 'salus', 'peccatum', 'coram', 'extra', 'contra',
    'supra', 'infra', 'intra', 'per', 'pro', 'sub', 'sine', 'vel', 'nec',
    'neque', 'sive', 'quia', 'quam', 'nisi', 'tamen', 'quoque', 'atque',
    'igitur', 'ergo', 'nam', 'propter', 'secundum', 'juxta', 'circa',
    'apud', 'adversus', 'usque', 'versus', 'videlicet', 'scilicet',
    'idem', 'eadem', 'id ipsum', 'a priori', 'a posteriori', 'a fortiori',
    'de facto', 'de jure', 'in re', 'in situ', 'in toto', 'in vacuo',
    'prima facie', 'bona fide', 'caveat', 'etc.', '&c', 'ibid.', 'op. cit.',
    'infra', 'supra', 'passim', 'circa', 'fl.', 'q.v.', 'viz.',
}

LATIN_SUFFIXES = {'-que', '-ve', '-ne', '-cum', '-dam', '-piam', '-nam'}


def contains_latin(text):
    lower = text.lower().strip().rstrip('.,;:!?\'"»«()[]{}')
    if lower in LATIN_MARKERS:
        return True
    for suffix in LATIN_SUFFIXES:
        if lower.endswith(suffix):
            return True
    return False


def detect_latin_spans(html):
    def replace_callback(m):
        word = m.group(0)
        if contains_latin(word):
            stripped = word.rstrip('.,;:!?\'"»«)')
            punct = word[len(stripped):]
            return f'<span lang="la" xml:lang="la">{html_escape(stripped)}</span>{punct}'
        return word
    return re.sub(r'\b[a-zA-Z][a-zA-Z.\-]+\b', replace_callback, html)


# ===========================================================================
# CHAPTER DETECTION AND BUILDING
# ===========================================================================

CHAPTER_KEYWORD_RE = re.compile(
    r'^(CHAPTER|SERMON|DISCOURSE|EXERCITATION|PREFACE|PREFATORY|'
    r'DEDICATION|APPENDIX|SECTION|PART)\b', re.IGNORECASE
)


# ===========================================================================
# THML-HYBRID CHAPTER BUILDING
# ===========================================================================

def parse_thml_chapter_list(vol_num):
    """Parse ThML XML and return ordered list of (title, id, div1_elem)
    excluding FOOTNOTES.

    This is the authoritative chapter list: every div1 becomes a chapter
    in the output EPUB spine.
    """
    thml_path = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}',
                             'intermediate', f'volume_{vol_num}.thml.xml')
    if not os.path.exists(thml_path):
        print(f"  Warning: ThML not found at {thml_path}")
        return []
    tree = ET.parse(thml_path)
    root = tree.getroot()
    chapters = []
    for div1 in root.findall('.//div1'):
        title = (div1.get('title') or '').strip()
        if title.upper() == 'FOOTNOTES':
            continue
        cid = div1.get('id', '')
        chapters.append((title, cid, div1))
    print(f"  ThML chapter list: {len(chapters)} chapters parsed")
    return chapters


def _normalize_title(t):
    """Normalize a title for comparison (ThML ↔ pdftohtml matching)."""
    t = re.sub(r'\s+', ' ', t.strip().upper())
    # Remove common AGES noise from titles
    t = t.replace('THEGLORIOUS', 'THE GLORIOUS').replace('OFCHRIST', 'OF CHRIST')
    t = t.replace('CRISTOLOGIA', 'CHRISTOLOGIA')
    t = t.rstrip('.')
    return t


# Map pdftohtml titles (keys) to ThML titles (values) for known mismatches
TITLE_MAP = {
    'PREFACE': 'GENERAL PREFACE.',
    'CHAPTER 1.': 'CHAPTER 1',
    'CHAPTER 2.': 'CHAPTER 2',
    'CHAPTER 3.': 'CHAPTER 3.',
    'CHAPTER 4.': 'CHAPTER 4',
    'CHAPTER 5.': 'CHAPTER 5.',
    'CHAPTER 6.': 'CHAPTER 6',
    'CHAPTER 8.': 'CHAPTER 8.',
    'CHAPTER 12.': 'CHAPTER 12.',
}


def _find_matching_pdf_chapter(thml_title, pdf_chapters):
    """Find a pdftohtml Chapter whose title matches the given ThML title."""
    thml_norm = _normalize_title(thml_title)
    for pdf_ch in pdf_chapters:
        pdf_norm = _normalize_title(pdf_ch.title)
        if pdf_norm == thml_norm:
            return pdf_ch
        
        # Fuzzy match for long titles
        if len(thml_norm) > 20 and (thml_norm in pdf_norm or pdf_norm in thml_norm):
            return pdf_ch
            
        mapped = TITLE_MAP.get(pdf_ch.title.strip(), pdf_ch.title.strip())
        if _normalize_title(mapped) == thml_norm:
            return pdf_ch
    return None


def build_hybrid_chapters(thml_chapters, pdf_chapters):
    """Build a hybrid chapter list: iterate ThML chapters in order,
    matching pdftohtml content where available, falling back to ThML rendering.
    
    CRITICAL: Preserves ALL pdftohtml content by attaching unmatched PDF
    segments to the preceding matched chapter. Forces monotonic matching
    to avoid picking up early TOC entries instead of real content.
    """
    # 1. Map ThML chapters to PDF chapters (MONOTONIC)
    thml_to_pdf = {}
    last_pdf_idx = -1
    
    for i, (thml_title, cid, div1) in enumerate(thml_chapters):
        pdf_ch_idx = -1
        thml_norm = _normalize_title(thml_title)
        
        # Search PDF chapters starting AFTER the last match
        for j in range(last_pdf_idx + 1, len(pdf_chapters)):
            pdf_ch = pdf_chapters[j]
            pdf_norm = _normalize_title(pdf_ch.title)
            
            if pdf_norm == thml_norm:
                pdf_ch_idx = j; break
            
            # Fuzzy match for long titles
            if len(thml_norm) > 20 and (thml_norm in pdf_norm or pdf_norm in thml_norm):
                pdf_ch_idx = j; break
                
            mapped = TITLE_MAP.get(pdf_ch.title.strip(), pdf_ch.title.strip())
            if _normalize_title(mapped) == thml_norm:
                pdf_ch_idx = j; break
        
        if pdf_ch_idx != -1:
            thml_to_pdf[i] = pdf_ch_idx
            last_pdf_idx = pdf_ch_idx

    # 2. Build result by iterating ThML chapters and collecting ranges
    hybrid = []
    pdf_count = len(pdf_chapters)
    
    for i, (thml_title, cid, div1) in enumerate(thml_chapters):
        subtitle = _extract_chapter_subtitle(div1)
        is_treatise = _is_treatise_title_page(div1)
        ch = Chapter(title=thml_title, cid=cid)
        ch.subtitle = subtitle
        ch.is_treatise = is_treatise

        if i in thml_to_pdf:
            start_idx = thml_to_pdf[i]
            # Find the end of this range: up to the next matched PDF chapter
            next_match_idx = pdf_count
            for k in range(i + 1, len(thml_chapters)):
                if k in thml_to_pdf:
                    next_match_idx = thml_to_pdf[k]
                    break
            
            # Collect all paragraphs from start_idx up to next_match_idx
            all_paras = []
            for j in range(start_idx, next_match_idx):
                pdf_seg = pdf_chapters[j]
                # If it's a new PDF segment (not the first one in range), 
                # add its title as a bold paragraph if it's not "Untitled"
                if j > start_idx and pdf_seg.title != 'Untitled' and len(pdf_seg.title) > 3:
                    title_para = Paragraph([], pdf_seg.paragraphs[0].page_num if pdf_seg.paragraphs else 0)
                    title_para.kind = 'body'
                    fs = FontSpec(0, 18, 'TimesNewRomanPS-BoldMT', '#000000')
                    fs.is_bold = True
                    title_para.lines = [Line([(pdf_seg.title, fs)], 0, 0)]
                    all_paras.append(title_para)
                
                all_paras.extend(pdf_seg.paragraphs)
            
            ch.paragraphs = all_paras
            ch.heading_level = pdf_chapters[start_idx].heading_level
            if is_treatise:
                ch.synthetic_html = _build_treatise_title(div1)
        elif is_treatise:
            ch.synthetic_html = _build_treatise_title(div1)
        else:
            ch.synthetic_html = _build_normal_chapter(div1)

        hybrid.append(ch)

    print(f"  Hybrid chapters: {len(hybrid)} ({sum(1 for c in hybrid if not c.synthetic_html)} matched range, {sum(1 for c in hybrid if c.synthetic_html is not None)} synthetic)")
    return hybrid


def build_chapters(paragraphs, page_width):
    chapters = []
    chapter_counter = 0
    current = None

    for para in paragraphs:
        kind = para.kind
        text = ''.join(s[0] for line in para.lines for s in line.segments).strip()

        if kind in ('heading_1', 'heading_2', 'chapter_heading'):
            if current is not None:
                chapters.append(current)
            chapter_counter += 1
            cid = f'ch{chapter_counter:03d}'
            h_level = 'h1' if kind == 'heading_1' else 'h2'
            current = Chapter(text, cid, h_level)
            current.is_treatise = (kind == 'heading_1')

        elif kind == 'list_item' and current is not None:
            current.paragraphs.append(para)

        elif kind in ('body', 'greek', 'hebrew'):
            if current is None:
                chapter_counter += 1
                cid = f'ch{chapter_counter:03d}'
                current = Chapter('Untitled', cid, 'h1')

            if not current.paragraphs and not current.is_treatise:
                first_text = text.upper()
                if current.title == 'Untitled' and not CHAPTER_KEYWORD_RE.match(first_text):
                    current.title = first_text[:80]

            current.paragraphs.append(para)

    if current is not None:
        chapters.append(current)

    return chapters


# ===========================================================================
# FOOTNOTE PROCESSING
# ===========================================================================


def parse_footnotes_from_thml(vol_num):
    """Parse FOOTNOTES section from ThML intermediate."""
    thml_path = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}',
                             'intermediate', f'volume_{vol_num}.thml.xml')
    if not os.path.exists(thml_path):
        return []

    tree = ET.parse(thml_path)
    root = tree.getroot()
    FN_MARKER_RE = re.compile(
        r'<a\s+class="fnmarker"\s+data-fn="(\d+)"[^>]*?/?>'
    )

    for div1 in root.findall('.//div1'):
        title = (div1.get('title') or '').upper().strip()
        if title == 'FOOTNOTES':
            footnotes = []
            for p in div1.findall('p'):
                p_html = ET.tostring(p, encoding='unicode', method='html')
                segments = FN_MARKER_RE.split(p_html)
                for i in range(1, len(segments), 2):
                    fn_num = int(segments[i])
                    raw = segments[i + 1]
                    # fnmarker has <a>...</a> form, strip closing </a>
                    if raw.startswith('</a>'):
                        raw = raw[4:]
                    raw = raw.replace('</p>', '')
                    raw = re.sub(r'\s+', ' ', raw).strip()
                    footnotes.append((fn_num, raw))
            footnotes.sort(key=lambda x: x[0])
            return footnotes

    return []


def parse_thml_fnrefs(vol_num):
    """Parse ThML body fnref markers to map chapters to footnote numbers."""
    thml_path = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}',
                             'intermediate', f'volume_{vol_num}.thml.xml')
    if not os.path.exists(thml_path):
        return {}

    tree = ET.parse(thml_path)
    root = tree.getroot()
    chapter_fnrefs = {}

    for div1 in root.findall('.//div1'):
        ch_id = div1.get('id', '')
        if not ch_id:
            continue
        title = (div1.get('title') or '').upper().strip()
        if title == 'FOOTNOTES':
            continue
        fns = []
        for fnref in div1.findall('.//a[@class="fnref"]'):
            href = fnref.get('href', '')
            m = re.match(r'#fn(\d+)', href)
            if m:
                fns.append(int(m.group(1)))
        if fns:
            chapter_fnrefs[ch_id] = fns

    return chapter_fnrefs


def build_endnotes_xhtml(footnotes, endnotes_file='ch120.xhtml'):
    """Build the endnotes <section> XHTML."""
    if not footnotes:
        return None
    parts = [
        '<section epub:type="endnotes" role="doc-endnotes">',
        '<h1>Footnotes</h1>',
    ]
    for fn_num, fn_text in footnotes:
        tagged = tag_unicode_ranges(fn_text)
        parts.append(
            f'<aside epub:type="endnote" role="doc-endnote" id="fn{fn_num}">'
            f'<p class="footnote">'
            f'<a href="#fn{fn_num}" class="fn-link">{fn_num}</a> {tagged}'
            f'</p></aside>'
        )
    parts.append('</section>')
    return '\n'.join(parts)


def parse_thml_fnrefs_by_chapter(vol_num):
    """Parse ThML fnrefs mapped by chapter title instead of id.

    Returns: {chapter_title: [fn_number, ...]}
    """
    thml_path = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}',
                             'intermediate', f'volume_{vol_num}.thml.xml')
    if not os.path.exists(thml_path):
        return {}

    tree = ET.parse(thml_path)
    root = tree.getroot()
    result = {}

    for div1 in root.findall('.//div1'):
        title = (div1.get('title') or '').strip().upper()
        if title == 'FOOTNOTES':
            continue
        fns = []
        for fnref in div1.findall('.//a[@class="fnref"]'):
            href = fnref.get('href', '')
            m = re.match(r'#fn(\d+)', href)
            if m:
                fns.append(int(m.group(1)))
        if fns:
            result[title] = fns

    return result


def inject_footnote_links(html_text, chapter_fn_nums, endnotes_file='ch120.xhtml'):
    """Find occurrences of each fn number in body HTML and wrap in noteref.
    Strictly requires 'f' prefix (e.g. f1) to avoid false positives.
    """
    if not chapter_fn_nums:
        return html_text

    para_matches = list(re.finditer(r'<p[^>]*>(.*?)</p>', html_text, re.DOTALL))
    if not para_matches:
        return html_text

    para_info = []
    for m in para_matches:
        content = m.group(1)
        plain = re.sub(r'<[^>]+>', ' ', content)
        plain = re.sub(r'\s+', ' ', plain).strip()
        para_info.append({
            'content': content,
            'plain': plain,
            'start': m.start(),
            'end': m.end(),
            'attr': m.group(0)[:m.group(0).find('>') + 1]
        })

    sorted_fns = sorted(set(chapter_fn_nums), reverse=True)
    para_replacements = {}

    for fn_num in sorted_fns:
        num_str = str(fn_num)
        found_pi = -1
        found_pos = -1
        match_len = 0
        
        # AGES PDFs use 'f' prefix for genuine footnote markers
        patterns = [rf'f{num_str}\b']
        
        for pi in range(len(para_info) - 1, -1, -1):
            p = para_info[pi]
            for pat in patterns:
                matches = list(re.finditer(pat, p['plain']))
                if matches:
                    last_match = matches[-1]
                    already_used = False
                    for used_pos, used_len, _ in para_replacements.get(pi, []):
                        if last_match.start() < used_pos + used_len and last_match.end() > used_pos:
                            already_used = True; break
                    if already_used: continue

                    found_pi = pi
                    found_pos = last_match.start()
                    match_len = last_match.end() - last_match.start()
                    break
            if found_pi != -1: break

        if found_pi != -1:
            if found_pi not in para_replacements: para_replacements[found_pi] = []
            para_replacements[found_pi].append((found_pos, match_len, fn_num))

    new_html_parts = []
    last_idx = 0
    for pi, replacements in sorted(para_replacements.items()):
        p = para_info[pi]
        replacements.sort(key=lambda x: x[0], reverse=True)
        content = p['content']
        
        for pos, length, fn_num in replacements:
            search_key = p['plain'][pos : pos + length] # e.g. "f1"
            html_pat = r'(<[^>]+>)*'.join(re.escape(c) for c in search_key)
            matches = list(re.finditer(html_pat, content))
            if matches:
                m = matches[-1]
                link = f'<a epub:type="noteref" role="doc-noteref" href="{endnotes_file}#fn{fn_num}" class="footnote-ref"><sup>{fn_num}</sup></a>'
                content = content[:m.start()] + link + content[m.end():]
        
        new_html_parts.append(html_text[last_idx:p['start']])
        new_html_parts.append(f"{p['attr']}{content}</p>")
        last_idx = p['end']
    
    new_html_parts.append(html_text[last_idx:])
    return "".join(new_html_parts)


def tag_unicode_ranges(text):
    """Wrap untagged Greek and Hebrew Unicode runs in spans."""
    if not text:
        return ""
    text = re.sub(
        r'([\u0370-\u03FF\u1F00-\u1FFF\s]{2,})',
        lambda m: f'<span lang="el" xml:lang="el">{m.group(1)}</span>'
        if any(c.strip() for c in m.group(1)) else m.group(1),
        text
    )
    text = re.sub(
        r'([\u0590-\u05FF\s]{2,})',
        lambda m: f'<span lang="he" xml:lang="he" dir="rtl">{m.group(1)}</span>'
        if any(c.strip() for c in m.group(1)) else m.group(1),
        text
    )
    text = text.replace(
        '</span><span lang="el" xml:lang="el">', ''
    ).replace(
        '</span><span lang="he" xml:lang="he" dir="rtl">', ''
    )
    return text


def escape_xml(text):
    if text is None:
        return ''
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                 .replace('>', '&gt;').replace('"', '&quot;'))


# ===========================================================================
# EPUB ASSEMBLY (mirrors converter.py)
# ===========================================================================

def make_xhtml(title, body_html, css_href='style/main.css', font_styles=None):
    safe_title = escape_xml(title)
    style_block = f'\n<style type="text/css">{font_styles}</style>\n' if font_styles else ''
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        'epub:prefix="z3998: http://www.daisy.org/z3998/2012/vocab/structure/#" '
        'lang="en" xml:lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8"/>\n'
        f'  <title>{safe_title}</title>\n'
        f'  <link rel="stylesheet" type="text/css" href="{css_href}"/>\n'
        f'  {style_block}\n'
        '</head>\n'
        f'<body>{body_html}</body>\n'
        '</html>'
    )


def _title_case_headings(html):
    """Apply title_case to <h1> and <h2> text content."""
    return re.sub(
        r'(<(?:h1|h2)[^>]*>)(.*?)(</(?:h1|h2)>)',
        lambda m: m.group(1) + title_case(m.group(2)) + m.group(3),
        html, flags=re.DOTALL
    )


def build_chapter_xhtml(chapter, font_styles=None):
    if chapter.synthetic_html is not None:
        return chapter.synthetic_html

    body_parts = ['<section>']

    # Special handling for CONTENTS pages to preserve PDF-like formatting
    is_contents = chapter.title.upper().startswith('CONTENTS')

    if not chapter.is_treatise:
        if chapter.heading_level == 'h1':
            body_parts.append(f'<h1>{escape_xml(chapter.title)}</h1>')
        else:
            body_parts.append(f'<h2>{escape_xml(chapter.title)}</h2>')
    else:
        # Treatise titles are already formatted by _build_treatise_title
        # and would fall into the synthetic_html block above if matched.
        # This part handles pdftohtml chapters identified as treatises.
        body_parts.append(f'<h1>{escape_xml(chapter.title)}</h1>')

    fontspecs = {}
    for para in chapter.paragraphs:
        for line in para.lines:
            for _, fs in line.segments:
                fontspecs[id(fs)] = fs

    for para in chapter.paragraphs:
        if is_contents:
            html = build_paragraph_xhtml(para, fontspecs)
            first_line = para.lines[0] if para.lines else None
            first_text = "".join(s[0] for s in first_line.segments).strip().upper() if first_line else ""
            is_bold = any(fs.is_bold for l in para.lines for _, fs in l.segments)
            
            # Identify chapter markers (flush left or starts with CHAPTER)
            is_chapter_marker = "CHAPTER" in first_text or "BOOK" in first_text or "PART" in first_text or re.match(r'^\d+\.', first_text)
            
            # Identify titles (centered or bold and not a chapter marker)
            # Centered if left margin > 50 and it's bold
            line_left = first_line.left if first_line else 0
            is_likely_title = is_bold and line_left > 50 and not is_chapter_marker
            
            if is_likely_title:
                cls = 'ContentsTitle'
            elif is_chapter_marker:
                cls = 'ContentsItem'
            else:
                cls = 'ContentsDescWrap'
            
            body_parts.append(f'<p class="{cls}">{html}</p>')
        else:
            html = build_body_paragraph(para, fontspecs)
            if chapter.is_treatise and para == chapter.paragraphs[0]:
                pass
            body_parts.append(html)

    body_parts.append('</section>')
    return '\n'.join(body_parts)


def build_treatise_title_xhtml_page(chapter, font_styles=None):
    body = '<div class="treatise-title">'
    body += f'<h1>{escape_xml(chapter.title)}</h1>'
    body += '</div>'
    return make_xhtml(chapter.title, body, font_styles=font_styles)


def find_cover(vol_num):
    covers_dir = os.path.join(_WORKSPACE, 'covers')
    for ext in ('.jpeg', '.jpg', '.png'):
        path = os.path.join(covers_dir, f'v{vol_num}{ext}')
        if os.path.exists(path):
            return path
    return None


def find_portrait(vol_num=None):
    p_dir = os.path.join(_WORKSPACE, 'portraits')
    if not os.path.isdir(p_dir):
        return None
    files = sorted([f for f in os.listdir(p_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))])
    if not files:
        return None
    idx = int(hashlib.md5(f'owen-v{vol_num}'.encode()).hexdigest(), 16) % len(files)
    return os.path.join(p_dir, files[idx])


def build_title_page(vol_num, title, subtitle):
    return f'''<div class="title-page"><p class="ornament">â§</p><h1>The Works of<br/>John Owen</h1><hr class="rule"/><p class="subtitle">Volume {vol_num}</p><p class="subtitle">{escape_xml(subtitle)}</p><p class="author"><span class="by">by</span>John Owen</p><p class="editor">Edited by William H. Goold</p><p class="publisher">Banner of Truth Trust</p></div>'''


def generate_frontispiece_xhtml(portrait_filename):
    return f'''<?xml version="1.0" encoding="utf-8"?><!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en"><head><title>Frontispiece</title><link href="style/main.css" rel="stylesheet" type="text/css"/></head><body><div class="frontispiece"><img src="images/{portrait_filename}" alt="Portrait"/><p class="caption">John Owen (1616&#x2013;1683)</p></div></body></html>'''


def generate_nav_xhtml(toc_entries, volume_title=None):
    display_title = html_escape(volume_title or 'Table of Contents')
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

        lines.append(f'<li><a href="{html_escape(href)}">{html_escape(text)}</a>')
        stack.append('li')
        current_level = level

    while stack:
        lines.append(f'</{stack.pop()}>')

    lines.extend(['</nav>', '</body>', '</html>'])
    return '\n'.join(lines)


def generate_ncx(title, uid, toc_entries):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
        f'  <head><meta content="{html_escape(uid)}" name="dtb:uid"/></head>',
        f'  <docTitle><text>{html_escape(title)}</text></docTitle>',
        '  <navMap>',
    ]
    for i, (level, text, href) in enumerate(toc_entries):
        lines.append(
            f'    <navPoint id="nav_{i}" playOrder="{i+1}">'
            f'<navLabel><text>{html_escape(text)}</text></navLabel>'
            f'<content src="{html_escape(href)}"/>'
            f'</navPoint>'
        )
    lines.extend(['  </navMap>', '</ncx>'])
    return '\n'.join(lines)


def repackage_canonical(epub_path, src_dir):
    if os.path.exists(epub_path):
        os.remove(epub_path)
    with open(os.path.join(src_dir, 'mimetype'), 'wb') as f:
        f.write(b'application/epub+zip')
    subprocess.run(['zip', '-0Xq', epub_path, 'mimetype'], cwd=src_dir, check=True)
    subprocess.run(
        ['zip', '-r9q', epub_path, '.', '-x', 'mimetype', '-x', '*.DS_Store'],
        cwd=src_dir, check=True
    )


def generate_landmarks_nav(title_href):
    return (
        '<nav epub:type="landmarks" id="landmarks">\n'
        '<h1>Guide</h1>\n'
        '<ol>\n'
        f'  <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>\n'
        f'  <li><a epub:type="bodymatter" href="{title_href}">Start of Content</a></li>\n'
        '</ol>\n'
        '</nav>'
    )


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def process_volume(vol_num):
    config = VOLUME_CONFIG.get(vol_num)
    if config is None:
        print(f"Error: No config for volume {vol_num}")
        return False

    source_type = config.get('source_type', '')
    if source_type != 'ages_pdf':
        print(f"  Skipping volume {vol_num} (source: {source_type})")
        return False

    vol_dir = os.path.join(_WORKSPACE, 'volumes', f'v{vol_num}')
    pdf_dir = os.path.join(_WORKSPACE, 'pdfs')
    intermediate_dir = os.path.join(vol_dir, 'intermediate')
    output_dir = os.path.join(vol_dir, 'output_pdftohtml')
    os.makedirs(output_dir, exist_ok=True)

    pdf_path = os.path.join(pdf_dir, f'owen-v{vol_num}.pdf')
    if not os.path.exists(pdf_path):
        print(f"  Error: PDF not found: {pdf_path}")
        return False

    intermediate_xml = os.path.join(intermediate_dir, f'volume_{vol_num}.pdftohtml.xml')
    epub_path = os.path.join(output_dir, f'volume_{vol_num}.epub')

    # --- Stage 1: Run pdftohtml ---
    if os.path.exists(intermediate_xml):
        print(f"  Using cached pdftohtml XML: {intermediate_xml}")
        with open(intermediate_xml, 'r') as f:
            xml_text = f.read()
    else:
        print(f"  Running pdftohtml on {os.path.basename(pdf_path)}...")
        xml_text = run_pdftohtml(pdf_path)
        if xml_text is None:
            return False
        with open(intermediate_xml, 'w') as f:
            f.write(xml_text)
        print(f"  Saved pdftohtml XML: {intermediate_xml} ({len(xml_text) // 1024} KB)")

    # --- Stage 2: Parse XML ---
    pages = parse_pdftohtml_xml(xml_text)

    # --- Stage 3: Filter noise ---
    pages = filter_noise(pages)

    # --- Stage 4: Flow reconstruction ---
    page_height = pages[0]['height'] if pages else 939
    all_lines = []
    for page in pages:
        lines = group_runs_into_lines(page['runs'], page['fontspecs'])
        page_num = page['num']
        for line in lines:
            if is_ages_boilerplate_line(line):
                continue
            joined = ''.join(s[0] for s in line.segments).strip()
            if joined.isdigit() and len(joined) <= 3 and (line.top < 60 or line.top > 870):
                continue
            line.top = line.top + (page_num - 1) * page_height
            all_lines.append(line)

    paragraphs = group_lines_into_paragraphs(all_lines, pages[0]['width'] if pages else 600)

    # --- Stage 5: Classify paragraphs ---
    for para in paragraphs:
        page_width = pages[0]['width'] if pages else 600
        para.kind = classify_paragraph(para.lines, page_width)

    # --- Stage 6: Build chapters ---
    chapters = build_chapters(paragraphs, pages[0]['width'] if pages else 600)

    # --- Stage 6b: Footnote processing ---
    footnotes = parse_footnotes_from_thml(vol_num)
    thml_fnrefs_by_title = parse_thml_fnrefs_by_chapter(vol_num)
    endnotes_html = build_endnotes_xhtml(footnotes) if footnotes else None

    # Separate footnotes chapter from main chapters
    main_chapters = []
    footnotes_chapter = None
    for ch in chapters:
        clean_title = ch.title.strip().upper()
        if clean_title == 'FOOTNOTES':
            footnotes_chapter = ch
        else:
            main_chapters.append(ch)
    chapters = main_chapters

    if footnotes_chapter:
        print(f"  Detected FOOTNOTES chapter ({len(footnotes)} notes via ThML)")

    # --- Stage 6c: Build hybrid chapters from ThML + pdftohtml ---
    thml_chapters = parse_thml_chapter_list(vol_num)
    if thml_chapters:
        chapters = build_hybrid_chapters(thml_chapters, chapters)
    else:
        print(f"  Warning: No ThML chapters loaded (ThML file missing or empty)")

    # --- Stage 7: EPUB assembly ---
    print(f"  Assembling EPUB...")
    vol_name = f'owen-v{vol_num}'
    primary = select_primary_font(vol_name)
    font_styles = generate_font_styles(primary['name'], primary['files'])

    book = epub.EpubBook()
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-bot-v{vol_num}-pdftohtml')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(config['title'])
    book.set_language('en')
    for a in config.get('authors', ['John Owen']):
        book.add_author(a)

    style_item = epub.EpubItem(
        uid="css", file_name="style/main.css",
        media_type="text/css",
        content=EPUB_STYLESHEET.encode('utf-8')
    )
    book.add_item(style_item)

    seen_fonts = set()
    for f_file in primary['files'].values():
        fname = os.path.basename(f_file)
        if fname in seen_fonts:
            continue
        src = os.path.join(FONT_BASE, f_file)
        if os.path.exists(src):
            book.add_item(epub.EpubItem(
                uid=f'f_{fname.replace(".","_")}',
                file_name=f'Fonts/{fname}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            seen_fonts.add(fname)

    for fname, fpath in SBL_SUPPLEMENTS.items():
        if fname in seen_fonts:
            continue
        src = os.path.join(FONT_BASE, fpath)
        if os.path.exists(src):
            book.add_item(epub.EpubItem(
                uid=f'f_{fname.replace(".","_")}',
                file_name=f'Fonts/{fname}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            seen_fonts.add(fname)

    for fname, fpath in EZRA_SIL_FILES.items():
        if fname in seen_fonts:
            continue
        src = os.path.join(FONT_BASE, fpath)
        if os.path.exists(src):
            book.add_item(epub.EpubItem(
                uid=f'f_{fname.replace(".","_")}',
                file_name=f'Fonts/{fname}',
                media_type='application/font-sfnt',
                content=open(src, 'rb').read()
            ))
            seen_fonts.add(fname)

    cover_file = find_cover(vol_num)
    if cover_file:
        book.set_cover("images/cover.png", open(cover_file, 'rb').read())

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
            make_xhtml("Frontispiece", generate_frontispiece_xhtml(p_fn), font_styles=font_styles).encode('utf-8')
        )
        frontispiece_item.add_item(style_item)
        book.add_item(frontispiece_item)

    subtitle_val = VOLUME_SUBTITLES.get(vol_num, "")
    tp_item = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang="en")
    tp_item.set_content(
        make_xhtml("Title Page", build_title_page(vol_num, config['title'], subtitle_val), font_styles=font_styles).encode('utf-8')
    )
    tp_item.add_item(style_item)
    book.add_item(tp_item)

    toc_entries = []
    epub_chapters = []
    last_l1_text = None

    def _is_same_treatise(new_t, last_t):
        if not last_t: return False
        n = new_t.upper().strip()
        l = last_t.upper().strip()
        if n in l or l in n: return True
        n_words = set(re.findall(r'\w{4,}', n))
        l_words = set(re.findall(r'\w{4,}', l))
        if len(n_words & l_words) >= 2: return True
        return False

    print(f"  Converting {len(chapters)} chapters to XHTML...")
    for ch in chapters:
        cid = ch.id
        clean_t = ch.title.strip()
        
        # Roman numerals are always L3 if we have an L2 parent, otherwise L2
        is_roman = bool(re.match(r'^[IVXLCDM]+\.?$', clean_t, re.IGNORECASE))

        # --- Determine TOC entry ---
        major_front_matter = ('CONTENTS', 'GENERAL PREFACE', 'DEDICATION', 'ADVERTISEMENT')
        is_major = any(clean_t.upper().startswith(m) for m in major_front_matter)

        split = _split_nav_title(clean_t)
        if is_major:
            # Major front matter is always L1 and resets the active treatise
            toc_entries.append((1, title_case(clean_t), f'{cid}.xhtml'))
            last_l1_text = None
        elif split:
            treatise_text, chapter_text = split
            # For split titles, merge with active L1 if it matches
            if not _is_same_treatise(treatise_text, last_l1_text):
                toc_entries.append((1, title_case(treatise_text), f'{cid}.xhtml'))
                last_l1_text = title_case(treatise_text)
            disp = title_case(chapter_text)
            if ch.subtitle:
                disp = f"{disp} - {title_case(ch.subtitle)}"
            toc_entries.append((2, disp, f'{cid}.xhtml'))
        elif ch.is_treatise:
            # For actual title pages, always start a new L1 unless it's virtually identical
            # to the previous L1 (to avoid immediate duplicates)
            if clean_t.upper() != (last_l1_text or "").upper():
                toc_entries.append((1, title_case(clean_t), f'{cid}.xhtml'))
                last_l1_text = title_case(clean_t)
        elif is_roman:
            # Roman numerals (I., II., etc.) are nested at L3
            toc_entries.append((3, clean_t, f'{cid}.xhtml'))
        else:
            # General chapters, Prefatory Notes, Parts
            lvl = 2 if last_l1_text else 1
            disp = title_case(clean_t)
            if ch.subtitle:
                disp = f"{disp} - {title_case(ch.subtitle)}"
            toc_entries.append((lvl, disp, f'{cid}.xhtml'))

        # --- Build body XHTML ---
        body = build_chapter_xhtml(ch, font_styles)

        # Inject footnote references using ThML fnref data matched by title
        def _norm_for_fn(t):
            return re.sub(r'\s+', ' ', t.strip()).upper().rstrip('.')
        pdf_norm = _norm_for_fn(clean_t)
        mapped_key = TITLE_MAP.get(clean_t.strip(), clean_t.strip())
        mapped_norm = _norm_for_fn(mapped_key)
        chapter_fn_nums = []
        for thml_title, fns in thml_fnrefs_by_title.items():
            if _norm_for_fn(thml_title) == mapped_norm:
                chapter_fn_nums = fns
                break
        if chapter_fn_nums:
            body = inject_footnote_links(body, chapter_fn_nums)

        ch_item = epub.EpubHtml(title=title_case(clean_t), file_name=f'{cid}.xhtml', lang='en')
        ch_item.set_content(make_xhtml(title_case(clean_t), body, font_styles=font_styles).encode('utf-8'))
        ch_item.add_item(style_item)
        book.add_item(ch_item)
        epub_chapters.append(ch_item)

    # Add endnotes chapter
    if endnotes_html:
        print(f"  Adding endnotes chapter ({len(footnotes)} footnotes)...")
        en = epub.EpubHtml(title="Footnotes", file_name="ch120.xhtml", lang='en')
        en.set_content(
            make_xhtml("Footnotes", endnotes_html, font_styles=font_styles).encode('utf-8')
        )
        en.add_item(style_item)
        book.add_item(en)
        epub_chapters.append(en)
        toc_entries.append((1, "Footnotes", "ch120.xhtml"))

    full_t = f"The Works of John Owen, Vol. {vol_num} \u2014 {VOLUME_SUBTITLES.get(vol_num, '')}"
    nav_xhtml = generate_nav_xhtml(toc_entries, full_t)

    landmarks_nav = generate_landmarks_nav('title.xhtml')
    nav_html_full = nav_xhtml.replace('</nav>', f'{landmarks_nav}\n</nav>')

    nav_item = epub.EpubHtml(title='Table of Contents', file_name='nav.xhtml', lang='en')
    nav_item.set_content(nav_html_full.encode('utf-8'))
    nav_item.properties = ['nav']
    nav_item.add_item(style_item)
    book.add_item(nav_item)

    book.spine = ['nav', tp_item]
    if frontispiece_item:
        book.spine.insert(1, frontispiece_item)
    book.spine.extend(epub_chapters)

    temp_epub = epub_path + '.tmp'
    epub.write_epub(temp_epub, book, {})

    tmp = tempfile.mkdtemp()
    zipfile.ZipFile(temp_epub, 'r').extractall(tmp)

    oebps = None
    for r, d, f_names in os.walk(tmp):
        if any(fn.endswith('.opf') for fn in f_names):
            oebps = r
            break

    if oebps is None:
        print("  Error: OPF not found in extracted EPUB")
        shutil.rmtree(tmp)
        return False

    with open(os.path.join(oebps, 'nav.xhtml'), 'w') as f:
        f.write(nav_html_full)

    with open(os.path.join(oebps, 'toc.ncx'), 'w') as f:
        f.write(generate_ncx(full_t, str(vol_uuid), toc_entries))

    opf_p = os.path.join(oebps, 'content.opf')
    with open(opf_p, 'r') as f:
        opf = f.read()

    opf = opf.replace('version="2.0"', 'version="3.0"').replace('.html"', '.xhtml"')
    opf = re.sub(r'\s+properties="nav"', '', opf)
    opf = re.sub(r'(href="nav\.xhtml"[^>]*?)/?>', r'\1 properties="nav"/>', opf)

    if 'href="toc.ncx"' not in opf:
        opf = opf.replace(
            '</manifest>',
            '  <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n  </manifest>'
        )
    if '<spine' in opf and 'toc="ncx"' not in opf:
        opf = opf.replace('<spine', '<spine toc="ncx"')

    with open(opf_p, 'w') as f:
        f.write(opf)

    meta_inf = os.path.join(tmp, 'META-INF')
    os.makedirs(meta_inf, exist_ok=True)
    display_opts = '''<?xml version="1.0" encoding="UTF-8"?>
<display-options xmlns="http://www.apple.com/itunes/vbook/display-options">
  <platform name="*">
    <option name="specified-fonts">true</option>
  </platform>
</display-options>
'''
    with open(os.path.join(meta_inf, 'com.apple.ibooks.display-options.xml'), 'w') as f:
        f.write(display_opts)

    repackage_canonical(epub_path, tmp)
    shutil.rmtree(tmp)

    if os.path.exists(temp_epub):
        os.remove(temp_epub)

    file_size = os.path.getsize(epub_path)
    print(f"  Saved EPUB: {epub_path} ({file_size // 1024} KB)")
    return True


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    valid_volumes = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16]

    if len(sys.argv) > 1:
        try:
            vol_num = int(sys.argv[1])
            volumes = [vol_num] if vol_num in valid_volumes else []
        except ValueError:
            volumes = valid_volumes
    else:
        volumes = [1]

    if not volumes:
        print(f"Usage: {sys.argv[0]} <volume_number>")
        print(f"Valid volumes (PDF-only): {valid_volumes}")
        sys.exit(1)

    print(f"John Owen Works — pdftohtml → EPUB3 Converter")
    print(f"{'=' * 60}")

    results = []
    for v in volumes:
        print(f"\nVolume {v}:")
        success = process_volume(v)
        results.append((v, success))

    print(f"\n{'=' * 60}")
    success_count = sum(1 for _, s in results if s)
    print(f"Results: {success_count}/{len(results)} succeeded")
    for v, s in results:
        status = "OK" if s else "FAIL"
        print(f"  Volume {v}: {status}")


if __name__ == '__main__':
    main()
