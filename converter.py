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
    convert_greek_word,
    clean_greek_text, convert_gideon_hebrew, polytonic_sweep
)

# Issue 91: extract.py owns all PDF extraction, text cleaning, and paragraph healing.
from extract import (
    # AGES translation
    _AGES_BOOK_NAMES, _AGES_MARKER_RE, _AGES_MARKER_CONTEXT_RE, _HEX_CHAPTER_MAP,
    _translate_ages_marker, translate_ages_verse_markers,
    # PDF extraction
    coordinate_redactor,
    extract_ages_nav, _parse_visual_toc,
    page_has_special_fonts, page_is_structural,
    extract_structural_page, convert_span_text,
    extract_page_text_with_fonts, extract_page_markdown, get_merged_page_text,
    # Footnotes
    Footnote, _converted_pdf_line, _page_has_ages_footnote_marker,
    _find_ages_footnote_start_page, extract_footnotes_from_pdf,
    parse_thml_footnotes, merge_footnotes, find_footnote_refs_in_text,
    # Chapter building
    Chapter, build_chapters_from_toc,
    # Text cleaning and paragraph healing
    _remove_adjacent_duplicates, _remove_adjacent_line_overlaps,
    clean_text, reconstruct_paragraphs,
    _paragraph_needs_numeric_continuation, _join_numeric_continuation,
    _is_reference_continuation, _is_citation_abbrev_continuation,
    _trim_overlapping_prefix, _paragraph_needs_text_continuation,
    _is_probable_duplicate_fragment,
    _remove_repeated_opening_clause,
    _collapse_adjacent_duplicate_refs,
    _remove_duplicate_scripture_tail, _remove_interrupted_duplicate_clause,
    _remove_adjacent_repeated_word_runs,
    post_process_paragraphs, _remove_global_ngram_duplicates,
    deduplicate_junction, get_pages_text, _build_flat_chapters,
)

# Issue 91: render.py now owns all rendering + EPUB assembly functions.
# Import everything from it so the rest of converter.py continues to work
# unchanged during the gradual migration.
from render import (
    # Constants
    FOOTNOTE_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE, FOOTNOTE_PLACEHOLDER_RE,
    FT_MARKER_RE, EMPTY_BRACKET_RE,
    BETA_CODE_RE, GIDEON_HEBREW_RE,
    STRUCTURAL_START_RE, STRUCTURAL_PREFIX_HTML_RE, INLINE_STRUCTURAL_MARKER_RE,
    ROMAN_HEADING_RE, ROMAN_ONLY_RE, PLAIN_CHAPTER_RE,
    CITATION_ABBREV_TRAIL_RE, CITATION_ABBREV_START_RE, CITATION_AUTHOR_TRAIL_RE,
    ROMAN_LIST_TOKEN, MARKDOWN_STRUCTURAL_START_RE,
    SCRIPTURE_BOOK_RE, SCRIPTURE_REF_RE, SCRIPTURE_CONTINUATION_TRAIL_RE,
    RENDERED_INLINE_STRUCTURAL_RE, PLAIN_INLINE_STRUCTURAL_HTML_RE,
    # Footnote helpers
    normalize_footnote_markers, _noteref_link,
    _restore_footnote_placeholders, _strip_footnote_placeholders,
    # OCR/text normalization (called by clean_text in converter.py)
    _normalize_spaced_caps, _normalize_i_will, _repair_owen_ocr_errors,
    # Text helpers used by both stages
    title_case, nav_display_title,
    _norm_for_dedupe, _is_scripture_ref_fragment, _scripture_ref_tokens,
    _split_inline_structural_markers,
    _repair_known_catechism_ghosts,
    _trim_duplicate_reference_prefix,
    # Rendering
    apply_scholastic_anchor_protocol,
    force_polyglot_mapping, tag_unicode_ranges, emphasize_structural_prefix,
    _split_rendered_inline_structural_html,
    markdown_to_html,
    # EPUB assembly
    _escape_xml, _make_xhtml,
    _split_leading_chapter_subtitle, _clean_heading_text,
    _roman_to_int, _is_roman_list_item, _strip_markdown_heading_marker,
    _coalesce_roman_list_paragraphs,
    _split_inline_catechism_questions, _is_catechism_scripture_spill,
    _answer_head,
    find_cover, find_portrait, _build_title_page,
    generate_frontispiece_xhtml, generate_nav_xhtml, generate_ncx,
    repackage_canonical, _inject_apple_books_options,
    build_endnotes_chapter,
    detect_page_type, is_toc_continuation_page,
    format_title_page, restore_dropped_title_noteref,
    build_toc_page_xhtml,
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

# ─── Structural Colors (AGES PDF specific) ──────────────────────
COLOR_BLUE = 212       # 0x0000D4 (Parts)
COLOR_GREEN = 25617    # 0x006411 (Chapters)
COLOR_RED = 8388608    # 0x800000 (Volumes)

# ─── Font Detection (extraction-stage constants) ─────────────────
GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}

# Regex for detecting Beta Code words that missed font tagging.
# Keep this conservative: the fallback runs after ordinary prose has been
# escaped, so broad markers like apostrophe or leading j/J corrupt English
# words such as "author's", "Jesus", "John", and "justification".

# Regex for detecting Gideon Hebrew words that missed font tagging.
# Matches words containing unambiguous Gideon-only marks. Plain semicolon,
# bracket, and digit 1 are ordinary English/list punctuation and caused major
# false positives ("grace;" and "vol. 1" became Hebrew).

LOOSE_FOOTNOTE_MARKER_RE = re.compile(
    r'\[\s*f\s*(\d{1,3})\s*\]|(?<![A-Za-z])f\s*(\d{1,3})\b',
    re.I,
)
FT_MARKER_RE = re.compile(r'^ft(\d+)\s*', re.I)
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
ROMAN_ONLY_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$')
CITATION_ABBREV_TRAIL_RE = re.compile(
    r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|q|a|p)\.?\s*$'
    r'|'
    # Page references: "p. 43" or "pp. 43" — should not be sentence ends
    r'\bp+\.\s+\d{1,4}\s*$'
    r'|'
    # Scripture book abbreviations before chapter:verse — e.g. "Cant. 5:10"
    r'\b(?:Cant|Prov|Eccl|Sol|Isa|Jer|Lam|Ezek|Dan|Hos|Zeph|Zech|Mal|'
    r'Matt|Mk|Lk|Jn|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Rev)\.\s*$',
    re.I,
)
CITATION_AUTHOR_TRAIL_RE = re.compile(
    r'\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|'
    r'Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan)\.?\s*$',
    re.I,
)
MARKDOWN_STRUCTURAL_START_RE = re.compile(
    r'^\*\*(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
    r'\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\*\*\s*[,.;]?\s+'
)


# ================================================================
# AGES VERSE MARKER TRANSLATION
# ================================================================

# AGES Software encodes Bible references as <BBCCVV> or <BBBCCVV> where
# BB/BBB = book code (1-based), CC = chapter (zero-padded), VV = verse.

# Matches standard decimal AGES codes (6-9 digits) AND the Psalms hex-chapter
# variant where chapters 100-159 are encoded with a hex letter at position 2:
#   <19A225> = Psalms 102:25  (A=10 → ch = 10*10+2 = 102, v = 25)
#   <19B822> = Psalms 118:22  (B=11 → ch = 11*10+8 = 118, v = 22)
#   <19D504> = Psalms 135:4   (D=13 → ch = 13*10+5 = 135, v = 4)
# The hex letter appears only at position 2 of the code (after the 2-digit book).

# Context-aware pattern: captures the code AND any immediately-following
# book+chapter:verse text so we can detect when the PDF already has the
# human-readable form right after the numeric code (both layers present).
# Group 1 = code (may include a hex letter), Group 2 = optional following ref text.

# Hex-letter → century value for the Psalms chapter encoding.


# ================================================================
# SCHOLASTIC ANCHOR POST-PROCESSOR
# ================================================================


# Pattern to detect "Objection ." (space before period) — OCR artifact


# ================================================================
# SPACED-CAPS AND I WILL OCR NORMALIZATION
# ================================================================

_I_WILL_RE = re.compile(r'\bI\s*WILL\b|\bIWILL\b', re.I)


SCRIPTURE_REF_RE = re.compile(
    rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*|\b\d+:\d+(?:[-,]\s*\d+)*',
    re.I,
)

# ================================================================
# STAGE 1: Coordinate-Based Redaction
# ================================================================


# ================================================================
# STAGE 2: AGES Navigation Extraction
# ================================================================


# ================================================================
# STAGE 3: Font-Aware Text Extraction + Greek/Hebrew Conversion
# ================================================================


# ================================================================
# STAGE 4: Footnote Stitching
# ================================================================


# ================================================================
# STAGE 5: Chapter Building from TOC
# ================================================================


# ================================================================
# STAGE 6: EPUB3 Assembly
# ================================================================


PLAIN_INLINE_STRUCTURAL_HTML_RE = re.compile(
    r'(?P<marker>(?<![:\d-])(?!\d{4}\.)\d{1,3}\.\s+)'
)


# ================================================================
# MAIN PIPELINE
# ================================================================


# ================================================================
# FRONT MATTER HANDLING
# ================================================================

_AGES_HEADERS = {'THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION',
                 'Books For The Ages', 'AGES Software', 'Version 1.0',
                 'B o o k s F o r T h e A g e s'}


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
    # Use per-volume front_matter_pages config if available, else 25-page default
    _fm_pages = config.get('front_matter_pages', 25)
    scan_limit = min(_fm_pages, len(doc))
    
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

    # Issue 107: Global conversion state across chapters
    # Issue 89: front matter style — "prose" for running editorial text,
    #           "blurb" for decorative title-page-adjacent content.
    conv_mode = "FRONT_MATTER"
    conv_drop_cap = False
    conv_front_matter_style = "blurb"  # safe default; overridden per chapter below

    # Keywords that identify prose-heavy front matter sections (prefaces, notes,
    # analyses). Any chapter whose title contains one of these gets prose styling.
    _FM_PROSE_KEYWORDS = [
        "PREFACE", "PREFATORY NOTE", "PREFATORY", "ANALYSIS",
        "TO THE READER", "ADVERTISEMENT", "GENERAL PREFACE",
    ]

    for i, chap in enumerate(chapters):
        if chap.is_endnotes or chap.title.strip().lower() == 'footnotes':
            continue

        # If this is a structural Part/Treatise, trigger BODY_START and Drop Cap
        # ONLY if it matches the Major Heading pattern (Issue 107 Refinement)
        title_upper = chap.title.upper()
        if any(kw in title_upper for kw in ["ANALYSIS", "PREFATORY NOTE", "PREFACE", "CONTENTS"]):
            conv_mode = "FRONT_MATTER"
            conv_drop_cap = False
            # Running editorial prose: Prefaces, Prefatory Notes, Analyses,
            # "To the Reader" letters, Advertisements all carry multi-paragraph
            # prose that must be left-justified, not centered-italic.
            conv_front_matter_style = "prose"
        elif chap.is_treatise and re.search(
            r'\b(?:PART|BOOK)\s+[0-9IVXLCDM]+\b|\b(?:CHRISTOLOGIA|MEDITATIONS|TWO SHORT CATECHISMS)\b',
            title_upper,
        ):
            conv_mode = "BODY_START"
            conv_drop_cap = True
            conv_front_matter_style = "blurb"
        elif re.search(r'\bCHAPTER\s+\d+\b|\bSERMON\s+\d+\b|\bDISCOURSE\s+\d+\b|\bLECTURE\s+\d+\b', title_upper):
            # Explicitly numbered chapters, sermons, discourses are always body content.
            # Reset any lingering FRONT_MATTER state so prose styling doesn't bleed
            # from a preceding prefatory chapter into body chapters.
            if conv_mode == "FRONT_MATTER":
                conv_mode = "BODY_START"
                conv_drop_cap = True
            conv_front_matter_style = "blurb"

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
        
        # Prepare XHTML title
        xhtml_title = chap.title
        # Avoid repeated phrase warning in audit by shortening the internal title for Part pages
        if chap.is_treatise and ' - ' in xhtml_title:
            xhtml_title = xhtml_title.split(' - ')[0]

        if ptype == 'title_page':
            # If the next chapter starts on this same page, then this is a structural
            # entry (e.g. PART 2). We limit title extraction and skip separate body.
            shares_page = (i + 1 < len(chapters) and chapters[i+1].page_start == chap.page_start)
            title_html = restore_dropped_title_noteref(
                format_title_page(first_page, limit_to_title=shares_page),
                chap,
                vol_num,
            )
            
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
                    md_text = chap.raw_text
                    # If raw_text is missing or we specifically want to start from body_start_page, re-extract
                    if not md_text or chap.page_start < body_start_page:
                        md_text = get_pages_text(doc, pages_md, body_start_page, chap.page_end, healer_mode=healer_active)
                    
                    body_html, conv_mode, conv_drop_cap = markdown_to_html(
                        md_text,
                        current_mode=conv_mode,
                        pending_drop_cap=conv_drop_cap,
                        front_matter_style=conv_front_matter_style,
                    )
                    body_html = apply_scholastic_anchor_protocol(body_html)
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
            md_text = chap.raw_text
            if not md_text:
                body_end = chap.page_end
                if i + 1 < len(chapters):
                    next_start = chapters[i+1].page_start
                    if next_start > chap.page_start and next_start <= body_end:
                        body_end = next_start - 1
                md_text = get_pages_text(doc, pages_md, chap.page_start, body_end, healer_mode=healer_active)
            
            body_html, conv_mode, conv_drop_cap = markdown_to_html(
                md_text,
                current_mode=conv_mode,
                pending_drop_cap=conv_drop_cap,
                front_matter_style=conv_front_matter_style,
            )
            body_html = apply_scholastic_anchor_protocol(body_html)
            if not body_html.strip():
                continue
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
