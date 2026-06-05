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
    _text_block_is_fully_inset,
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
from scripts.markdown_skeleton import (
    page_has_special_fonts,
    page_is_structural,
    extract_structural_page,
    extract_page_text_with_fonts,
    extract_page_markdown,
    get_merged_page_text,
)
from scripts.chapter_builder import Chapter, build_chapters_from_toc
from scripts.text_cleaner import (
    clean_text, reconstruct_paragraphs, strip_false_ocr_bolds, 
    _is_terminal, get_pages_text, post_process_paragraphs,
    _remove_interrupted_duplicate_clause,
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
