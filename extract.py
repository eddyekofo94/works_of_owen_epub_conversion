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

def extract_volume(vol_num, overrides: dict = None,
                   progress_callback=None) -> dict:
    """Run Stage 1 for a single Owen volume: PDF → JSON intermediate.

    Writes volumes/vN/intermediate/volume_N.json and returns the dict.
    The JSON is the contract between Stage 1 (extract) and Stage 2 (render).

    overrides: optional per-volume config additions (see volumes/vN/convert.py).
    """
    import pymupdf4llm
    from shared import merge_volume_config, get_volume_dir
    from render import (
        detect_page_type, is_toc_continuation_page,
        format_title_page, build_toc_page_xhtml,
    )

    config = merge_volume_config(vol_num, overrides)
    vol_dir = get_volume_dir(vol_num)
    
    if config.get('source_type') == 'epub2':
        return extract_epub2_volume(vol_num, overrides=overrides, progress_callback=progress_callback)

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


def clean_html_to_markdown(soup_segment) -> str:
    """Convert a BeautifulSoup tag or list of elements into Markdown-like text."""
    from bs4 import Comment, NavigableString
    markdown_lines = []
    
    for elem in soup_segment:
        if isinstance(elem, Comment):
            continue
        if isinstance(elem, NavigableString):
            text = str(elem).strip()
            if text:
                markdown_lines.append(text)
            continue
            
        tag = elem.name
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            text = elem.get_text().strip()
            if text:
                level = int(tag[1])
                markdown_lines.append(f"\n\n{'#' * level} {text}\n\n")
        elif tag == 'blockquote':
            text = elem.get_text().strip()
            if text:
                lines = [f"> {line.strip()}" for line in text.split('\n') if line.strip()]
                markdown_lines.append("\n\n" + "\n".join(lines) + "\n\n")
        elif tag in ('ul', 'ol'):
            for li in elem.find_all('li', recursive=False):
                li_text = li.get_text().strip()
                if li_text:
                    markdown_lines.append(f"\n- {li_text}")
            markdown_lines.append("\n")
        elif tag == 'p':
            p_html = ""
            for child in elem.children:
                if isinstance(child, NavigableString):
                    p_html += str(child)
                elif child.name in ('b', 'strong'):
                    p_html += f"**{child.get_text()}**"
                elif child.name in ('i', 'em'):
                    p_html += f"*{child.get_text()}*"
                else:
                    p_html += child.get_text()
            p_text = re.sub(r'\s+', ' ', p_html).strip()
            if p_text:
                markdown_lines.append(f"\n\n{p_text}\n\n")
        elif tag == 'hr':
            markdown_lines.append("\n\n---\n\n")
        else:
            text = elem.get_text().strip()
            if text:
                markdown_lines.append(text)
                
    raw_markdown = "".join(markdown_lines)
    raw_markdown = re.sub(r'\n{3,}', '\n\n', raw_markdown)
    return raw_markdown.strip()


def extract_epub2_volume(vol_num, overrides: dict = None,
                         progress_callback=None) -> dict:
    """Run Stage 1 for a Hebrews volume: EPUB2 -> JSON intermediate.
    
    Reads from volumes/hN/input/volume_hN.epub and outputs to volumes/hN/intermediate/volume_hN.json.
    """
    import zipfile
    from xml.etree import ElementTree
    from bs4 import BeautifulSoup
    from shared import merge_volume_config, get_volume_dir
    
    config = merge_volume_config(vol_num, overrides)
    vol_dir = get_volume_dir(vol_num)
    epub_path = vol_dir / 'input' / f'volume_{vol_num}.epub'
    out_json = vol_dir / 'intermediate' / f'volume_{vol_num}.json'
    
    print(f'[extract] Volume {vol_num}: opening {epub_path.name}')
    
    if not epub_path.exists():
        raise FileNotFoundError(f"Source EPUB2 file not found: {epub_path}")
        
    with zipfile.ZipFile(epub_path) as z:
        # 1. Read container.xml to find OPF path
        container_xml = z.read("META-INF/container.xml")
        root = ElementTree.fromstring(container_xml)
        ns_container = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
        opf_path = root.find(".//c:rootfile", ns_container).attrib["full-path"]
        
        opf_dir = os.path.dirname(opf_path)
        opf_content = z.read(opf_path)
        opf_root = ElementTree.fromstring(opf_content)
        
        # 2. Parse OPF manifest and spine
        ns_opf = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
        manifest_items = {}
        for item in opf_root.findall(".//opf:item", ns_opf):
            manifest_items[item.attrib["id"]] = item.attrib["href"]
            
        spine_itemrefs = []
        for itemref in opf_root.findall(".//opf:itemref", ns_opf):
            spine_itemrefs.append(itemref.attrib["idref"])
            
        spine_files = []
        for idref in spine_itemrefs:
            href = manifest_items[idref]
            path = os.path.join(opf_dir, href) if opf_dir else href
            spine_files.append(path)
            
        # 3. Locate and parse NCX
        ncx_id = opf_root.find(".//opf:spine", ns_opf).attrib["toc"]
        ncx_href = manifest_items[ncx_id]
        ncx_path = os.path.join(opf_dir, ncx_href) if opf_dir else ncx_href
        
        ncx_content = z.read(ncx_path)
        ncx_root = ElementTree.fromstring(ncx_content)
        
        ncx_ns = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}
        nav_points = []
        
        def parse_nav_point(elem, level=1):
            title = elem.find("./ncx:navLabel/ncx:text", ncx_ns).text
            src = elem.find("./ncx:content", ncx_ns).attrib["src"]
            nav_points.append({
                "title": title.strip() if title else "",
                "src": src,
                "level": level
            })
            for sub in elem.findall("./ncx:navPoint", ncx_ns):
                parse_nav_point(sub, level + 1)
                
        for np in ncx_root.findall("./ncx:navMap/ncx:navPoint", ncx_ns):
            parse_nav_point(np)
            
        # Resolve target files and anchors for each navPoint
        for np in nav_points:
            src_parts = np["src"].split('#')
            file_href = src_parts[0]
            anchor = src_parts[1] if len(src_parts) > 1 else None
            file_path = os.path.join(opf_dir, file_href) if opf_dir else file_href
            np["file_path"] = file_path
            np["anchor"] = anchor
            
        # 4. Extract chapters
        chapter_dicts = []
        _FM_PROSE_KEYWORDS = [
            'PREFACE', 'PREFATORY NOTE', 'PREFATORY', 'ANALYSIS',
            'TO THE READER', 'ADVERTISEMENT', 'GENERAL PREFACE',
            'DEDICATORY', 'DEDICATION'
        ]
        
        total_ch = len(nav_points)
        for i, np in enumerate(nav_points):
            if progress_callback:
                progress_callback(i, total_ch, f"Extracting Chapter {i+1}/{total_ch}")
                
            title = np["title"]
            file_path = np["file_path"]
            anchor = np["anchor"]
            level = np["level"]
            
            # Boundary calculation
            next_file_path = None
            next_anchor = None
            if i + 1 < len(nav_points):
                next_file_path = nav_points[i+1]["file_path"]
                next_anchor = nav_points[i+1]["anchor"]
                
            content = z.read(file_path).decode('utf-8')
            soup = BeautifulSoup(content, 'xml')
            
            body_children = list(soup.find('body').children) if soup.find('body') else list(soup.children)
            
            start_idx = 0
            if anchor:
                start_elem = soup.find(id=anchor)
                if not start_elem:
                    start_elem = soup.find(attrs={"name": anchor})
                    
                if start_elem:
                    parent = start_elem.parent
                    while parent and parent.name not in ('body', 'html', '[document]'):
                        start_elem = parent
                        parent = start_elem.parent
                    try:
                        start_idx = list(parent.children).index(start_elem)
                    except ValueError:
                        start_idx = 0
                        
            extracted_elements = []
            current_file_idx = spine_files.index(file_path)
            
            end_file_idx = current_file_idx
            if next_file_path and next_file_path in spine_files:
                end_file_idx = spine_files.index(next_file_path)
                
            for idx in range(current_file_idx, end_file_idx + 1):
                f_path = spine_files[idx]
                if idx > current_file_idx:
                    f_content = z.read(f_path).decode('utf-8')
                    f_soup = BeautifulSoup(f_content, 'xml')
                    f_children = list(f_soup.find('body').children) if f_soup.find('body') else list(f_soup.children)
                    f_start_idx = 0
                else:
                    f_children = body_children
                    f_start_idx = start_idx
                    
                f_end_idx = len(f_children)
                if idx == end_file_idx and next_anchor:
                    end_content = z.read(next_file_path).decode('utf-8')
                    end_soup = BeautifulSoup(end_content, 'xml')
                    end_elem = end_soup.find(id=next_anchor)
                    if not end_elem:
                        end_elem = end_soup.find(attrs={"name": next_anchor})
                    if end_elem:
                        local_end_elem = f_children[0].parent.find(id=next_anchor)
                        if not local_end_elem:
                            local_end_elem = f_children[0].parent.find(attrs={"name": next_anchor})
                        if local_end_elem:
                            parent = local_end_elem.parent
                            while parent and parent != f_children[0].parent:
                                local_end_elem = parent
                                parent = local_end_elem.parent
                            try:
                                f_end_idx = list(parent.children).index(local_end_elem)
                            except ValueError:
                                f_end_idx = len(f_children)
                                
                for j in range(f_start_idx, f_end_idx):
                    extracted_elements.append(f_children[j])
                    
            raw_text = clean_html_to_markdown(extracted_elements)
            
            title_upper = title.upper()
            fm_style = 'prose' if any(kw in title_upper for kw in _FM_PROSE_KEYWORDS) else None
            
            is_treatise = False
            for t_title in config.get('treatises', []):
                if t_title.lower() in title.lower() or title.lower() in t_title.lower():
                    is_treatise = True
                    break
            if 'PART ' in title_upper or 'BOOK ' in title_upper:
                is_treatise = True
                
            cid = f"ch{i+1:03d}"
            
            chapter_dicts.append({
                'cid': cid,
                'title': title,
                'level': level,
                'page_start': current_file_idx,
                'page_end': end_file_idx,
                'is_treatise': is_treatise,
                'is_endnotes': False,
                'front_matter_style': fm_style,
                'raw_text': raw_text,
            })
            
        front_matter_items = []
        if "titlepage.xhtml" in z.namelist():
            tp_content = z.read("titlepage.xhtml").decode('utf-8')
            tp_soup = BeautifulSoup(tp_content, 'xml')
            tp_body = tp_soup.find('body')
            tp_html = "".join(str(c) for c in tp_body.children) if tp_body else tp_content
            front_matter_items.append({
                'type': 'title_page',
                'file_name': 'titlepage.xhtml',
                'title': 'Title Page',
                'page': 0,
                'html': tp_html,
            })
            
        # Add a placeholder Contents page
        front_matter_items.append({
            'type': 'toc',
            'file_name': 'contents.xhtml',
            'title': 'Contents',
            'page': 0,
            'html': '<h1>Contents</h1>',
        })
            
        intermediate = {
            'volume': vol_num,
            'title': config.get('title', f'An Exposition of the Epistle to the Hebrews, Volume {vol_num}'),
            'meta': {
                'pages': len(spine_files),
                'chapters_count': len(chapter_dicts),
                'extracted_at': datetime.now().isoformat(),
            },
            'chapters': chapter_dicts,
            'footnotes': {},
            'front_matter_items': front_matter_items,
        }
        
        out_json.parent.mkdir(parents=True, exist_ok=True)
        with open(out_json, 'w', encoding='utf-8') as f:
            json.dump(intermediate, f, ensure_ascii=False, indent=2)
            
        print(f'[extract] Written: {out_json}')
        if progress_callback:
            progress_callback(total_ch, total_ch, f"Completed extracting Volume {vol_num}")
            
        return intermediate


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Stage 1: PDF → JSON intermediate for Owen volumes")
    parser.add_argument("volumes", nargs="*", help="Volume identifier(s) to extract (e.g. 1, h1)")
    parser.add_argument("--all", action="store_true", help="Extract all volumes")
    args = parser.parse_args()

    vols = list(range(1, 17)) if args.all else (args.volumes or ['1'])
    for v in vols:
        extract_volume(v)
