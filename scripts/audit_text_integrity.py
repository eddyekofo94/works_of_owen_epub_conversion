#!/usr/bin/env python3
"""Audit textual integrity between an Owen source PDF and generated EPUB.

This is not a proofreader. It is a conservative tripwire for the failure modes
that matter most in this project: missing source text, duplicated ghost text,
faulty paragraph breaks, and suspicious extraction residue.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import unicodedata
import zipfile
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import fitz
from lxml import etree

# Set up path to import shared logic
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from shared import (
        convert_greek_word, convert_gideon_hebrew, clean_greek_text,
        is_greek_font, is_hebrew_font,
    )
except ImportError:
    convert_greek_word = lambda x: x
    convert_gideon_hebrew = lambda x: x
    clean_greek_text = lambda x: x
    is_greek_font = lambda x: False
    is_hebrew_font = lambda x: False

NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

WORD_RE = re.compile(r"[\w\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff'’-]+", re.UNICODE)
SPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")
HEADER_RE = re.compile(
    r"\b(?:THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|JOHN OWEN COLLECTION|"
    r"BOOKS FOR THE AGES|AGES SOFTWARE|VERSION 1\.0|VOLUME \d+)\b",
    re.I,
)
TERMINAL_RE = re.compile(r"""[.!?:;]["')\]]?$""")
HARD_STRUCTURAL_START_RE = re.compile(
    r"^(?:[0-9]+\.\s+|\([0-9]+\.?\)\s+|\[[0-9]+\.?\]\s+|[IVXLCDM]+\.\s+|"
    r"[0-9]+(?:st|nd|rd|th)\b\s*[,.;]\s+|[0-9]+(?:(?:st|nd|rd|th)ly|dly|ly)\b\s*[,.]?\s+)",
    re.I,
)
INLINE_STRUCTURAL_RE = re.compile(
    r".{8,}?[,:;—-]\s+(?P<marker>"
    r"(?<![:\d-])[0-9]+\.\s+|\([0-9]+\.?\)\s+|\[[0-9]+\.?\]\s+|[IVXLCDM]+\.\s+|"
    r"[0-9]+(?:st|nd|rd|th)\b\s*[,.;]\s+|[0-9]+(?:(?:st|nd|rd|th)ly|dly|ly)\b\s*[,.]?\s+)"
)
INLINE_RENDERED_STRUCTURAL_RE = re.compile(
    r"<b>\s*(?P<marker>"
    r"[0-9]{1,2}\.|"
    r"\([0-9]{1,2}\.?\)|"
    r"\[[0-9]{1,2}(?:st|nd|rd|th|dly|ly)?[,.]?\]|"
    r"[IVXLCDM]{2,}\.|"
    r"[0-9]{1,2}(?:st|nd|rd|th)\b\s*[,.;]|"
    r"[0-9]{1,2}(?:(?:st|nd|rd|th)ly|dly|ly)\b\s*[,.]?"
    r")\s*</b>",
    re.I,
)
SCRIPTURE_TRAIL_RE = re.compile(
    r"(?:\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|"
    r"Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|Proverbs|"
    r"Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|"
    r"Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|"
    r"Malachi|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|"
    r"Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Philemon|"
    r"Hebrews|James|Peter|Jude|Revelation)\s+)?"
    r"\d+:\d+(?:[-,;]\s*\d+)*[,:;]?\s*$|"
    r"\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|"
    r"Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|Proverbs|"
    r"Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|"
    r"Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|"
    r"Malachi|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|"
    r"Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Philemon|"
    r"Hebrews|James|Peter|Jude|Revelation)\s+\d+(?:[-,;]\s*\d+)*,\s*$",
    re.I,
)
VERSE_TRAIL_RE = re.compile(r"\b(?:verse|verses|chap|chapter)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$", re.I)
REFERENCE_STEM_RE = re.compile(r"\b(?:verse|verses|chap|chapter)[.,]?\s*$", re.I)
REFERENCE_CONTINUATION_START_RE = re.compile(r"^\d{1,3}(?::\d+)?(?:[-,;]\s*\d+)*[,:;]?\b")
CITATION_TRAIL_RE = re.compile(r"\b(?:cap|lib|sect|dist|part|vol|p|q|a|m|ad)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$", re.I)
CITATION_AUTHOR_TRAIL_RE = re.compile(
    r"\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|"
    r"Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan|Aquin|Alexand|Alens)\.?\s*$",
    re.I,
)
CITATION_ABBREV_START_RE = re.compile(
    r"^(?:Lib|Serm|Sermo|Epist|Ep|Cap|Chap|Orat|Tract|Homil|Haer|Dial|Quest|Art|Dist|Part|Vol)\.?\s+",
    re.I,
)
ROMAN_PROSE_START_RE = re.compile(r"^[IVXLCDM]+\.\s+\S+", re.I)
ROMAN_PROSE_MARKER_RE = re.compile(r"^(?P<roman>[IVXLCDM]+)\.\s+(?P<rest>.+)", re.I)
LIST_OR_LABEL_RE = re.compile(
    r"^(?:"
    r"[0-9]+\.\s+|"                         # 5. Mankind...
    r"\([0-9]+\.?\)\s+|"                    # (1.) There... / (1) There...
    r"\([0-9]+(?:st|nd|rd|th|dly|ly)[,.;]?\)\s+|"  # (1st,) Such...
    r"\[[0-9]+\.?\]\s+|"                    # [1.] There...
    r"\[[0-9]+(?:st|nd|rd|th|dly|ly)[,.;]?\]\s+|"  # [1st,] There...
    r"[IVXLCDM]+\.\s+|"                     # I. / II.
    r"[A-Z]\.\s+|"                          # Q. / A. catechism answers
    r"[0-9]+(?:st|nd|rd|th|dly|ly)\b[,.]?\s*|"  # 1st, 2ndly, 3rdly
    r"(?:First|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly|Again|But)\b[,.]?\s+|"
    r"CHAPTER\b|BOOK\b|PART\b|SECTION\b|PREFACE\b|PREFATORY\b"
    r")",
    re.I,
)


def is_source_footnotes_page(text: str) -> bool:
    """True when the source PDF page is the back-matter footnote section."""
    return bool(re.match(r"^\s*(?:\d+\s+)?FOOTNOTES\b", clean_text(text), re.I))
ENUMERATOR_RE = re.compile(
    r"(?<!\w)(?P<marker>"
    r"\[(?P<bracket_num>[0-9]{1,2})(?P<bracket_suffix>st|nd|rd|th|dly|ly)?[,.]?\]|"
    r"\((?P<paren_num>[0-9]{1,2})(?P<paren_suffix>st|nd|rd|th|dly|ly)?[,.]?\)|"
    r"\b(?P<bare_num>[0-9]{1,2})(?P<bare_suffix>st|nd|rd|th|dly|ly)\b[,.]?"
    r")",
    re.I,
)

MIN_WORD_LEN = 2
COMMON_WORDS = {
    "that", "this", "with", "from", "have", "which", "unto", "they", "them",
    "there", "their", "shall", "were", "been", "being", "upon", "when",
    "what", "where", "would", "could", "should", "into", "than", "then",
    "also", "only", "these", "those", "such", "some", "more", "most",
    "very", "will", "christ", "god", "lord", "john", "owen",
    "span", "lang", "xml", "rtl",
}


@dataclass
class Paragraph:
    file: str
    text: str
    tag: str
    index: int
    classes: str = ""
    html: str = ""


@dataclass
class Enumerator:
    marker: str
    family: str
    number: int
    suffix: str
    location: str
    context: str


def clean_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    text = re.sub(r"</?span\b[^>]*>", " ", text)
    text = HEADER_RE.sub(" ", text)
    text = re.sub(r"<\d[A-Za-z0-9]{5}>", " ", text)
    text = re.sub(r"(?<=[A-Za-z])f\d+\b", " ", text)
    text = re.sub(r"^\s*\d{1,4}\s*$", " ", text, flags=re.M)
    return SPACE_RE.sub(" ", text).strip()


def strip_greek_diacritics(text: str) -> str:
    """Remove polytonic diacritics for easier comparison."""
    # 1. Normalize to NFD to separate base chars from combining marks
    nfd = unicodedata.normalize("NFD", text)
    # 2. Filter out combining marks in the common Greek ranges
    # 0300-036F is Combining Diacritical Marks
    # 1DC0-1DFF is Combining Diacritical Marks Supplement
    # Also include the ancient Greek block marks (1F00-1FFF) if they are decomposed
    filtered = "".join(
        c for c in nfd 
        if not (unicodedata.category(c) == "Mn" and (0x0300 <= ord(c) <= 0x036F or 0x1DC0 <= ord(c) <= 0x1DFF))
    )
    # 3. Normalize back to NFC
    return unicodedata.normalize("NFC", filtered)


def content_words(text: str, include_common: bool = False) -> list[str]:
    words = []
    # Normalize Greek diacritics for more robust comparison
    text = strip_greek_diacritics(text)
    for raw in WORD_RE.findall(clean_text(text).lower()):
        word = raw.strip("'’-")
        if len(word) < MIN_WORD_LEN:
            continue
        if not include_common and word in COMMON_WORDS:
            continue
        words.append(word)
    return words


def normalized_word_string(text: str) -> str:
    """A very robust normalization for fuzzy phrase matching."""
    # First strip diacritics to make Greek/Hebrew matching robust
    text = strip_greek_diacritics(text)
    return " ".join(content_words(text, include_common=True))


def contiguous_script_runs(text: str, word_re: re.Pattern, min_words: int = 5) -> list[list[str]]:
    """Return contiguous Greek/Hebrew word runs without crossing prose gaps."""
    matches = list(word_re.finditer(text))
    runs: list[list[str]] = []
    current: list[str] = []
    previous_end = None

    for match in matches:
        word = match.group(0).lower()
        if len(word) < 2:
            if len(current) >= min_words:
                runs.append(current)
            current = []
            previous_end = match.end()
            continue

        if previous_end is not None:
            gap = text[previous_end:match.start()]
            # Punctuation and whitespace can separate words in the same Greek
            # quotation. Latin letters/digits mean prose intervened, so this is
            # a new run rather than one long synthetic clause.
            if re.search(r"[A-Za-z0-9]", gap):
                if len(current) >= min_words:
                    runs.append(current)
                current = []

        current.append(word)
        previous_end = match.end()

    if len(current) >= min_words:
        runs.append(current)
    return runs


def parse_xml(data: bytes) -> etree._Element:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    return etree.fromstring(data, parser=parser)


def norm_join(base_dir: str, href: str) -> str:
    href = unquote(href)
    joined = posixpath.normpath(posixpath.join(base_dir, href)) if base_dir else posixpath.normpath(href)
    return joined.lstrip("./")


def extract_epub_paragraphs(epub_path: Path) -> tuple[list[Paragraph], dict[str, Any]]:
    paragraphs: list[Paragraph] = []
    meta: dict[str, Any] = {}

    with zipfile.ZipFile(epub_path) as zf:
        root = parse_xml(zf.read("META-INF/container.xml"))
        rootfile = root.find(".//container:rootfile", namespaces=NS)
        if rootfile is None or not rootfile.get("full-path"):
            raise RuntimeError("container.xml has no OPF rootfile")

        opf_path = rootfile.get("full-path")
        assert opf_path is not None
        opf_dir = posixpath.dirname(opf_path)
        opf = parse_xml(zf.read(opf_path))

        manifest: dict[str, dict[str, str]] = {}
        for item in opf.xpath(".//opf:manifest/opf:item", namespaces=NS):
            item_id = item.get("id")
            href = item.get("href")
            if not item_id or not href:
                continue
            manifest[item_id] = {
                "href": norm_join(opf_dir, href),
                "properties": item.get("properties", ""),
                "media_type": item.get("media-type", ""),
            }

        spine_files: list[str] = []
        for itemref in opf.xpath(".//opf:spine/opf:itemref", namespaces=NS):
            idref = itemref.get("idref")
            if not idref or idref not in manifest:
                continue
            href = manifest[idref]["href"]
            props = manifest[idref]["properties"].split()
            if "nav" in props:
                continue
            if href.endswith((".xhtml", ".html")):
                spine_files.append(href)

        meta["spine_text_files"] = len(spine_files)
        idx = 0
        for href in spine_files:
            if href not in zf.namelist():
                continue
            try:
                doc = parse_xml(zf.read(href))
            except etree.XMLSyntaxError:
                continue
            for el in doc.xpath(".//xhtml:p|.//xhtml:h1|.//xhtml:h2|.//xhtml:h3|.//xhtml:h4", namespaces=NS):
                text = clean_text(" ".join(el.itertext()))
                if not text:
                    continue
                ancestor_classes = " ".join(
                    ancestor.get("class", "")
                    for ancestor in el.xpath("ancestor::*[@class]")
                )
                semantic_context = []
                if el.xpath("ancestor::xhtml:blockquote", namespaces=NS):
                    semantic_context.append("blockquote")
                if ancestor_classes:
                    semantic_context.append(ancestor_classes)
                paragraphs.append(Paragraph(
                    file=href,
                    text=text,
                    tag=etree.QName(el).localname,
                    index=idx,
                    classes=" ".join(part for part in [el.get("class", ""), *semantic_context] if part),
                    html=etree.tostring(el, encoding="unicode", method="xml"),
                ))
                idx += 1

    meta["paragraph_count"] = len(paragraphs)
    return paragraphs, meta


def extract_pdf_pages(pdf_path: Path) -> tuple[list[str], dict[str, Any]]:
    pages: list[str] = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            page_content = []
            for b in blocks:
                if b["type"] != 0:
                    continue
                for line in b["lines"]:
                    line_text = []
                    for span in line["spans"]:
                        text = span["text"]
                        font = span.get("font", "")
                        if is_greek_font(font):
                            text = clean_greek_text(convert_greek_word(text))
                        elif is_hebrew_font(font):
                            text = convert_gideon_hebrew(text)
                        line_text.append(text)
                    page_content.append("".join(line_text))
            page_text = " ".join(page_content)
            if is_source_footnotes_page(page_text):
                break
            pages.append(page_text)
    return pages, {"page_count": len(pages)}


def compare_word_coverage(pdf_text: str, epub_text: str) -> dict[str, Any]:
    pdf_counts = Counter(content_words(pdf_text))
    epub_counts = Counter(content_words(epub_text))

    missing = []
    excess = []
    for word, count in pdf_counts.items():
        epub_count = epub_counts.get(word, 0)
        if count >= 3 and epub_count < count * 0.5:
            missing.append({"word": word, "pdf": count, "epub": epub_count})
    for word, count in epub_counts.items():
        pdf_count = pdf_counts.get(word, 0)
        if count >= 5 and count > max(pdf_count * 1.8, pdf_count + 5):
            excess.append({"word": word, "pdf": pdf_count, "epub": count})

    missing.sort(key=lambda item: (item["pdf"] - item["epub"], item["pdf"]), reverse=True)
    excess.sort(key=lambda item: (item["epub"] - item["pdf"], item["epub"]), reverse=True)

    pdf_total = sum(pdf_counts.values())
    overlap = sum(min(count, epub_counts.get(word, 0)) for word, count in pdf_counts.items())
    coverage = overlap / pdf_total if pdf_total else 1.0

    return {
        "pdf_content_tokens": pdf_total,
        "epub_content_tokens": sum(epub_counts.values()),
        "coverage_ratio": round(coverage, 4),
        "missing_word_samples": missing[:25],
        "excess_word_samples": excess[:25],
    }


def page_coverage(pdf_pages: list[str], epub_text: str) -> dict[str, Any]:
    epub_norm = normalized_word_string(epub_text)
    weak_pages = []
    checked = 0

    for idx, page_text in enumerate(pdf_pages, start=1):
        words = content_words(page_text, include_common=True)
        if len(words) < 40:
            continue
        checked += 1
        windows = []
        if len(words) <= 16:
            windows = [words]
        else:
            positions = sorted({0, max(0, len(words) // 2 - 8), max(0, len(words) - 16)})
            windows = [words[pos : pos + 16] for pos in positions if len(words[pos : pos + 16]) >= 10]
        hits = sum(1 for window in windows if " ".join(window) in epub_norm)
        ratio = hits / len(windows) if windows else 1.0
        if ratio < 0.34:
            weak_pages.append({
                "page": idx,
                "hit_ratio": round(ratio, 3),
                "sample": " ".join(words[:24]),
            })

    return {
        "pages_checked": checked,
        "weak_page_count": len(weak_pages),
        "weak_pages": weak_pages[:30],
    }


def dense_source_window_integrity(pdf_pages: list[str], epub_text: str) -> dict[str, Any]:
    """Scan dense Latin word windows so sliced sentence interiors are visible."""
    epub_norm = normalized_word_string(epub_text)
    missing = []
    checked = 0
    for page_no, page_text in enumerate(pdf_pages, start=1):
        raw = clean_text(page_text)
        if re.search(r"[<>~|}]", raw):
            continue
        words = content_words(raw, include_common=True)
        if len(words) < 80:
            continue
        for start in range(0, len(words) - 13, 8):
            window = words[start:start + 14]
            if len(window) < 14:
                continue
            checked += 1
            phrase = " ".join(window)
            if phrase not in epub_norm:
                missing.append({
                    "page": page_no,
                    "sample": phrase,
                })
                break
    return {
        "dense_windows_checked": checked,
        "missing_dense_window_pages": len(missing),
        "missing_dense_windows": missing[:40],
    }


def looks_like_front_toc_continuation(text: str) -> bool:
    upper = text.upper()
    if re.match(r"^\d*\s*(?:GENERAL PREFACE|PREFACE|PREFATORY NOTE|TO THE READER)\b", upper):
        return False
    chapter_hits = len(re.findall(r"\bCHAPTER\s+\d+", upper))
    part_hits = len(re.findall(r"\bPART\s+\d+", upper))
    numbered_hits = len(re.findall(r"(?:^|\s)(?:[IVXLCDM]+\.|\d+\.)\s+[—A-Z]", text, re.I))
    return (chapter_hits + part_hits + numbered_hits) >= 1


def front_matter_toc_integrity(pdf_pages: list[str], epub_text: str) -> dict[str, Any]:
    """Strictly check early CONTENTS pages; global coverage hides these losses."""
    epub_norm = normalized_word_string(epub_text)
    toc_pages = []
    in_toc = False
    for page_no, page_text in enumerate(pdf_pages[:8], start=1):
        upper = page_text.upper()
        if "CONTENTS" in upper:
            in_toc = True
            toc_pages.append((page_no, page_text))
            continue
        if in_toc and looks_like_front_toc_continuation(page_text):
            toc_pages.append((page_no, page_text))
            continue
        if in_toc:
            break

    missing = []
    checked_windows = 0
    for page_no, page_text in toc_pages:
        words = content_words(page_text, include_common=True)
        if len(words) < 30:
            continue
        starts = sorted({0, max(0, len(words) // 3), max(0, (len(words) * 2) // 3), max(0, len(words) - 12)})
        windows = [words[start:start + 12] for start in starts if len(words[start:start + 12]) >= 10]
        checked_windows += len(windows)
        hits = sum(1 for window in windows if " ".join(window) in epub_norm)
        ratio = hits / len(windows) if windows else 1.0
        if ratio < 0.75:
            missing.append({
                "page": page_no,
                "hit_ratio": round(ratio, 3),
                "sample": " ".join(words[:28]),
            })

    return {
        "front_toc_pages_checked": len(toc_pages),
        "front_toc_windows_checked": checked_windows,
        "missing_front_toc_pages": len(missing),
        "missing_front_toc_samples": missing,
    }


def is_running_header_or_page_number(text: str) -> bool:
    stripped = clean_text(text)
    if not stripped:
        return True
    if re.fullmatch(r"\d{1,4}", stripped):
        return True
    return bool(HEADER_RE.search(stripped))


def extract_top_body_windows(pdf_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Extract first real body text from each PDF page for top-clipping checks."""
    windows: list[dict[str, Any]] = []
    checked = 0

    with fitz.open(pdf_path) as doc:
        for page_no, page in enumerate(doc, start=1):
            if is_source_footnotes_page(page.get_text("text")):
                break
            lines: list[tuple[float, str]] = []
            for block in page.get_text("dict").get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    y_center = (line["bbox"][1] + line["bbox"][3]) / 2
                    if y_center < 35 or y_center > 145:
                        continue
                    text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                    if is_running_header_or_page_number(text):
                        continue
                    lines.append((line["bbox"][1], text))

            if not lines:
                continue
            checked += 1
            lines.sort(key=lambda item: item[0])
            sample = clean_text(" ".join(text for _, text in lines[:2]))
            words = content_words(sample, include_common=True)
            if len(words) < 8:
                continue
            windows.append({
                "page": page_no,
                "window": " ".join(words[:14]),
                "sample": sample,
            })

    return windows, {"top_windows_checked": checked, "top_windows_usable": len(windows)}


def top_of_page_integrity(pdf_path: Path, epub_text: str) -> dict[str, Any]:
    """Catch body text lost by aggressive top-margin filtering."""
    epub_norm = normalized_word_string(epub_text)
    windows, meta = extract_top_body_windows(pdf_path)
    missing = []
    skipped = []

    for item in windows:
        sample = item["sample"]
        if re.match(r"^FT\d+\b", sample):
            skipped.append({**item, "reason": "source footnote block"})
            continue
        if re.search(r"[<>\]~|}]", sample):
            skipped.append({**item, "reason": "font-encoded Greek/Hebrew window"})
            continue

        words = item["window"].split()
        if len(words) < 8:
            skipped.append({**item, "reason": "too few stable words"})
            continue

        candidates = []
        for size in (14, 12, 10, 8):
            if len(words) < size:
                continue
            candidates.extend(" ".join(words[i:i + size]) for i in range(0, len(words) - size + 1))
        if not any(candidate and candidate in epub_norm for candidate in candidates):
            missing.append(item)

    return {
        **meta,
        "skipped_top_window_count": len(skipped),
        "skipped_top_windows": skipped[:40],
        "missing_top_window_count": len(missing),
        "missing_top_windows": missing[:40],
    }


def extract_bottom_body_windows(pdf_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Extract last real body text from each PDF page for bottom-clipping checks."""
    windows: list[dict[str, Any]] = []
    checked = 0

    with fitz.open(pdf_path) as doc:
        for page_no, page in enumerate(doc, start=1):
            if is_source_footnotes_page(page.get_text("text")):
                break
            page_height = page.rect.height
            lines: list[tuple[float, str]] = []
            for block in page.get_text("dict").get("blocks", []):
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    y_center = (line["bbox"][1] + line["bbox"][3]) / 2
                    # Bottom zone: above typical footer but below main body midpoint
                    if y_center < page_height - 145 or y_center > page_height - 30:
                        continue
                    text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
                    if is_running_header_or_page_number(text):
                        continue
                    lines.append((line["bbox"][1], text))

            if not lines:
                continue
            checked += 1
            lines.sort(key=lambda item: item[0], reverse=True)
            # Take the last 2 lines of the body block
            sample = clean_text(" ".join(text for _, text in reversed(lines[:2])))
            norm_sample = normalized_word_string(sample)
            words = norm_sample.split()
            if len(words) < 8:
                continue
            windows.append({
                "page": page_no,
                "window": " ".join(words[-14:]),
                "sample": sample,
            })

    return windows, {"bottom_windows_checked": checked, "bottom_windows_usable": len(windows)}


def bottom_of_page_integrity(pdf_path: Path, epub_text: str) -> dict[str, Any]:
    """Catch body text lost by aggressive bottom-margin filtering or footnote overlaps."""
    epub_norm = normalized_word_string(epub_text)
    windows, meta = extract_bottom_body_windows(pdf_path)
    missing = []
    skipped = []

    for item in windows:
        words = item["window"].split()
        if len(words) < 8:
            skipped.append({**item, "reason": "too few stable words"})
            continue

        candidates = []
        for size in (14, 12, 10, 8):
            if len(words) < size:
                continue
            candidates.extend(" ".join(words[i:i + size]) for i in range(0, len(words) - size + 1))
        if not any(candidate and candidate in epub_norm for candidate in candidates):
            missing.append(item)

    return {
        **meta,
        "skipped_bottom_window_count": len(skipped),
        "skipped_bottom_windows": skipped[:40],
        "missing_bottom_window_count": len(missing),
        "missing_bottom_windows": missing[:40],
    }


def paragraph_integrity(paragraphs: list[Paragraph]) -> dict[str, Any]:
    split_candidates = []
    short_fragments = []
    adjacent_duplicates = []
    inline_structural_candidates = []
    reference_continuation_splits = []
    citation_continuation_splits = []
    suspicious_large_number_starts = []
    roman_heading_candidates = []
    overlong_heading_candidates = []
    frontmatter_heading_body_candidates = []
    structural_start_exclusions = 0

    split_excluded_class_re = re.compile(
        r"\b(?:blockquote|treatise-title-page|volume-title-page|contents-page|"
        r"title-line|title-connector|descriptive|greek-title|quote-block|chapter-summary)\b"
    )
    body_paras = [
        p for p in paragraphs
        if p.tag == "p"
        and re.search(r"/ch\d+\.xhtml$", p.file)
        and not split_excluded_class_re.search(p.classes)
    ]
    frontmatter_heading_re = re.compile(r"^(PREFACE|PREFATORY NOTE|ORIGINAL PREFACE)\.?\b", re.I)

    for para in paragraphs:
        if not re.search(r"/ch\d+\.xhtml$", para.file):
            continue
        if para.tag not in {"h1", "h2", "h3", "h4"}:
            continue
        text = para.text.strip()
        if len(text) > 180 or len(re.findall(r"\w+", text)) > 28:
            overlong_heading_candidates.append({
                "file": para.file,
                "tag": para.tag,
                "text": text[:260],
            })
        if not frontmatter_heading_re.match(text):
            continue
        words = re.findall(r"\w+", text)
        if len(words) > 6 or re.search(r"[.!?;]\s+\w", text):
            frontmatter_heading_body_candidates.append({
                "file": para.file,
                "tag": para.tag,
                "text": text[:260],
            })

    for prev, nxt in zip(body_paras, body_paras[1:]):
        if prev.file != nxt.file:
            continue
        prev_text = prev.text.strip()
        next_text = nxt.text.strip()
        if not prev_text or not next_text:
            continue

        prev_terminal = bool(TERMINAL_RE.search(prev_text))
        next_is_structural_start = bool(LIST_OR_LABEL_RE.match(next_text) or HARD_STRUCTURAL_START_RE.match(next_text))
        if (
            REFERENCE_STEM_RE.search(prev_text)
            and REFERENCE_CONTINUATION_START_RE.match(next_text)
            and not next_is_structural_start
        ):
            reference_continuation_splits.append({
                "file": prev.file,
                "previous": prev_text[-180:],
                "next": next_text[:180],
            })
        if CITATION_AUTHOR_TRAIL_RE.search(prev_text) and CITATION_ABBREV_START_RE.match(next_text):
            citation_continuation_splits.append({
                "file": prev.file,
                "previous": prev_text[-180:],
                "next": next_text[:180],
            })
        if not prev_terminal:
            if HARD_STRUCTURAL_START_RE.match(next_text):
                structural_start_exclusions += 1
            else:
                split_candidates.append({
                    "file": prev.file,
                    "previous": prev_text[-180:],
                    "next": next_text[:180],
                })

        if similar_text(prev_text, next_text) > 0.92 and len(prev_text) > 40:
            adjacent_duplicates.append({
                "file": prev.file,
                "previous": prev_text[:180],
                "next": next_text[:180],
            })

    for para in body_paras:
        text = para.text.strip()
        if len(text) >= 35:
            continue
        if LIST_OR_LABEL_RE.match(text):
            continue
        if re.fullmatch(r"[-–—*\s]+", text):
            continue
        short_fragments.append({"file": para.file, "text": text})

    # Suspicious large-number starts: catch "Psalm 42" being split into "Psalm" and "42."
    all_numbered_starts = []
    for idx, para in enumerate(body_paras):
        match = re.match(r"^(\d{1,3})\.?\s+\S+", para.text.strip())
        if match:
            all_numbered_starts.append((idx, para.file, int(match.group(1)), para.text.strip()))

    suspicious_large_number_starts = []
    for i, (idx, file_name, number, text) in enumerate(all_numbered_starts):
        if number < 10:
            continue

        # 1. Punctuation check: if previous para in same file didn't end in punctuation,
        # it's a split/continuation (already caught by split_candidates), not a suspicious start.
        if idx > 0:
            prev_p = body_paras[idx - 1]
            if prev_p.file == file_name and not TERMINAL_RE.search(prev_p.text.strip()):
                continue

        # 2. Sequence check: if it's part of a numbered list (has neighbor N-1 or N+1 nearby),
        # it is a valid intentional start.
        # Look wider (10 paras) for points in long discourses.
        nearby = all_numbered_starts[max(0, i - 10):i + 11]
        has_neighbor = any(
            other_idx != idx
            and other_file == file_name
            and abs(other_number - number) == 1
            and abs(other_idx - idx) <= 10
            for other_idx, other_file, other_number, _ in nearby
        )
        if not has_neighbor:
            suspicious_large_number_starts.append({
                "file": file_name,
                "text": text[:220],
            })

    def context_is_reference_or_citation(context: str) -> bool:
        return bool(
            SCRIPTURE_TRAIL_RE.search(context)
            or VERSE_TRAIL_RE.search(context)
            or REFERENCE_STEM_RE.search(context)
            or CITATION_TRAIL_RE.search(context)
            or re.search(r"\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|distinct)\.?\s*$", context, re.I)
            or re.search(r"\b(?:see|cf)\s*$", context, re.I)
        )

    def has_inline_structural_marker(text: str, html: str = "") -> bool:
        for match in INLINE_STRUCTURAL_RE.finditer(text):
            marker_start = match.start("marker")
            if marker_start <= 2:
                continue
            marker = match.group("marker").strip()
            after_marker = text[match.end("marker"):match.end("marker") + 40]
            if re.fullmatch(r"[IVXLCDM]+\.", marker, re.I) and re.match(r"\s*[—-]\s*[IVXLCDM]+\.", after_marker, re.I):
                continue
            context = text[max(0, marker_start - 90):marker_start]
            if context_is_reference_or_citation(context) and not re.match(r"\s*(?:\([0-9]+\.?\)|\[[0-9]+\.?\])", match.group("marker")):
                continue
            # Skip markers inside quoted passages
            before_marker = text[:marker_start]
            if before_marker.count('"') % 2 != 0 or before_marker.count('\u201c') > before_marker.count('\u201d'):
                continue
            return True

        for match in INLINE_RENDERED_STRUCTURAL_RE.finditer(html or ""):
            before_html = html[:match.start()]
            before_text = clean_text(TAG_RE.sub(" ", before_html))
            if len(before_text) < 35:
                continue
            context = before_text[-120:]
            if context_is_reference_or_citation(context):
                continue
            return True
        return False

    def roman_to_int(roman: str) -> int:
        values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
        total = 0
        previous = 0
        for char in reversed(roman.upper()):
            value = values.get(char, 0)
            if value < previous:
                total -= value
            else:
                total += value
                previous = value
        return total

    def is_allowed_roman_list_item(text: str, previous_text: str, expected: int | None) -> tuple[bool, int | None]:
        match = ROMAN_PROSE_MARKER_RE.match(text)
        if not match:
            return False, None
        number = roman_to_int(match.group("roman"))
        rest = match.group("rest").strip()
        starts_list = (
            number in (1, 2)
            and (
                re.search(r"\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?(?:\d+\s*)?$", previous_text, re.I)
                or re.search(r"(?:[—-]|,)\s*$", previous_text)
            )
        )
        continues_list = expected == number
        short_enough = len(re.findall(r"\w+", rest)) <= 28
        terminal = bool(TERMINAL_RE.search(rest))
        if (starts_list or continues_list) and short_enough and terminal:
            return True, number + 1
        return False, None

    expected_roman_list_number = None
    previous_body_text = ""
    for para in body_paras:
        text = para.text.strip()
        if "roman-list-item" in para.classes.split():
            continue
        if ROMAN_PROSE_START_RE.match(text):
            # To reduce false positives (like "ill." being part of "will" after a break),
            # only flag if previous paragraph was empty or ended with punctuation.
            if previous_body_text and not TERMINAL_RE.search(previous_body_text):
                # Probably a continuation, ignore Roman marker
                pass
            else:
                allowed, next_expected = is_allowed_roman_list_item(
                    text,
                    previous_body_text,
                    expected_roman_list_number,
                )
                if allowed:
                    expected_roman_list_number = next_expected
                else:
                    expected_roman_list_number = None
                    roman_heading_candidates.append({
                        "file": para.file,
                        "text": text[:220],
                    })
        elif text:
            expected_roman_list_number = expected_roman_list_number
        if has_inline_structural_marker(text, para.html):
            inline_structural_candidates.append({
                "file": para.file,
                "text": text[:260],
            })
        if text:
            previous_body_text = text

    return {
        "paragraphs_checked": len(body_paras),
        "split_candidate_count": len(split_candidates),
        "split_candidates": split_candidates[:40],
        "structural_start_exclusions": structural_start_exclusions,
        "short_fragment_count": len(short_fragments),
        "short_fragments": short_fragments[:40],
        "adjacent_duplicate_count": len(adjacent_duplicates),
        "adjacent_duplicates": adjacent_duplicates[:30],
        "inline_structural_candidate_count": len(inline_structural_candidates),
        "inline_structural_candidates": inline_structural_candidates[:40],
        "reference_continuation_split_count": len(reference_continuation_splits),
        "reference_continuation_splits": reference_continuation_splits[:40],
        "citation_continuation_split_count": len(citation_continuation_splits),
        "citation_continuation_splits": citation_continuation_splits[:40],
        "suspicious_large_number_start_count": len(suspicious_large_number_starts),
        "suspicious_large_number_starts": suspicious_large_number_starts[:40],
        "roman_heading_candidate_count": len(roman_heading_candidates),
        "roman_heading_candidates": roman_heading_candidates[:40],
        "overlong_heading_candidate_count": len(overlong_heading_candidates),
        "overlong_heading_candidates": overlong_heading_candidates[:30],
        "frontmatter_heading_body_candidate_count": len(frontmatter_heading_body_candidates),
        "frontmatter_heading_body_candidates": frontmatter_heading_body_candidates[:20],
    }


def iter_enumerators(text: str, location: str) -> list[Enumerator]:
    markers: list[Enumerator] = []
    for match in ENUMERATOR_RE.finditer(text):
        if match.group("bracket_num"):
            family = "bracket_ordinal" if match.group("bracket_suffix") else "bracket_decimal"
            number = int(match.group("bracket_num"))
            suffix = (match.group("bracket_suffix") or "").lower()
        elif match.group("paren_num"):
            family = "paren_ordinal" if match.group("paren_suffix") else "paren_decimal"
            number = int(match.group("paren_num"))
            suffix = (match.group("paren_suffix") or "").lower()
        else:
            family = "bare_ordinal"
            number = int(match.group("bare_num"))
            suffix = (match.group("bare_suffix") or "").lower()

        start, end = match.span()
        context = clean_text(text[max(0, start - 90): min(len(text), end + 180)])
        markers.append(Enumerator(
            marker=match.group("marker"),
            family=family,
            number=number,
            suffix=suffix,
            location=location,
            context=context,
        ))
    return markers


def enumerator_integrity(pdf_pages: list[str], paragraphs: list[Paragraph]) -> dict[str, Any]:
    pdf_markers: list[Enumerator] = []
    for page_no, page_text in enumerate(pdf_pages, start=1):
        pdf_markers.extend(iter_enumerators(page_text, f"pdf:p{page_no}"))

    epub_markers: list[Enumerator] = []
    for para in paragraphs:
        epub_markers.extend(iter_enumerators(para.text, f"{para.file}#p{para.index}"))

    def is_front_matter_toc_marker(marker: Enumerator) -> bool:
        match = re.match(r"pdf:p(\d+)$", marker.location)
        return bool(match and int(match.group(1)) <= 6)

    comparable_pdf = [
        m for m in pdf_markers
        if m.family != "bare_ordinal" and not is_front_matter_toc_marker(m)
    ]
    comparable_epub = [m for m in epub_markers if m.family != "bare_ordinal"]
    pdf_counts = Counter(m.marker for m in comparable_pdf)
    epub_counts = Counter(m.marker for m in comparable_epub)

    missing = []
    for marker, count in sorted(pdf_counts.items()):
        epub_count = epub_counts.get(marker, 0)
        if epub_count < count:
            examples = [m for m in comparable_pdf if m.marker == marker][:3]
            missing.append({
                "marker": marker,
                "pdf": count,
                "epub": epub_count,
                "examples": [
                    {"location": ex.location, "context": ex.context}
                    for ex in examples
                ],
            })

    excess = []
    for marker, count in sorted(epub_counts.items()):
        pdf_count = pdf_counts.get(marker, 0)
        if count > pdf_count:
            examples = [m for m in comparable_epub if m.marker == marker][:3]
            excess.append({
                "marker": marker,
                "pdf": pdf_count,
                "epub": count,
                "examples": [
                    {"location": ex.location, "context": ex.context}
                    for ex in examples
                ],
            })

    orphan_candidates = []
    by_file: dict[str, list[Enumerator]] = {}
    for marker in epub_markers:
        if not marker.location.endswith("#p" + marker.location.rsplit("#p", 1)[-1]):
            continue
        file_name = marker.location.split("#p", 1)[0]
        by_file.setdefault(file_name, []).append(marker)

    for file_name, markers in by_file.items():
        for idx, marker in enumerate(markers):
            if marker.number <= 1:
                continue
            recent = markers[max(0, idx - 20):idx]
            if any(prev.family == marker.family and prev.number == marker.number - 1 for prev in recent):
                continue
            # Bare ordinals often restart after prose labels; exact PDF-vs-EPUB
            # counts are the primary guard for those.
            if marker.family == "bare_ordinal":
                continue
            orphan_candidates.append({
                "file": file_name,
                "marker": marker.marker,
                "family": marker.family,
                "context": marker.context,
            })

    return {
        "pdf_marker_count": len(pdf_markers),
        "epub_marker_count": len(epub_markers),
        "missing_marker_count": len(missing),
        "missing_markers": missing[:40],
        "excess_marker_count": len(excess),
        "excess_markers": excess[:40],
        "orphan_candidate_count": len(orphan_candidates),
        "orphan_candidates": orphan_candidates[:40],
    }


def similar_text(a: str, b: str) -> float:
    aw = content_words(a, include_common=True)
    bw = content_words(b, include_common=True)
    if not aw or not bw:
        return 0.0
    aset = set(aw)
    bset = set(bw)
    return len(aset & bset) / max(len(aset | bset), 1)


def repeated_windows(text: str, size: int = 10) -> list[dict[str, Any]]:
    """Detect non-consecutive n-gram repetitions across the entire text.
    Ghost layers often inject duplicates out of order or with slight variations.
    """
    words = content_words(text, include_common=True)
    if len(words) < size:
        return []

    ngrams = Counter()
    for i in range(len(words) - size + 1):
        ngram = " ".join(words[i : i + size])
        ngrams[ngram] += 1

    # Filter for n-grams that appear multiple times
    # and try to coalesce adjacent or overlapping hits
    hits = []
    for phrase, count in ngrams.most_common(50):
        if count > 1:
            hits.append({"phrase": phrase, "count": count})

    # Return top 25 suspicious repetitions
    return hits[:25]


GREEK_WORD_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]+")
HEBREW_WORD_RE = re.compile(r"[\u0590-\u05ff]+")
GREEK_HEBREW_WORD_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff]+")


def greek_hebrew_word_coverage(pdf_pages: list[str], paragraphs: list[Paragraph]) -> dict[str, Any]:
    """Compare Greek and Hebrew word counts between PDF and EPUB.

    Uses font-aware PDF extraction (already done in extract_pdf_pages)
    and EPUB text (stripped of HTML tags).
    """
    pdf_text = "\n".join(pdf_pages)
    epub_text = "\n".join(p.text for p in paragraphs)

    pdf_greek = GREEK_WORD_RE.findall(pdf_text)
    epub_greek = GREEK_WORD_RE.findall(epub_text)
    pdf_hebrew = HEBREW_WORD_RE.findall(pdf_text)
    epub_hebrew = HEBREW_WORD_RE.findall(epub_text)

    # Build word frequency maps for more nuanced comparison
    pdf_greek_counts = Counter(w.lower() for w in pdf_greek if len(w) >= 2)
    epub_greek_counts = Counter(w.lower() for w in epub_greek if len(w) >= 2)
    pdf_hebrew_counts = Counter(w for w in pdf_hebrew if len(w) >= 2)
    epub_hebrew_counts = Counter(w for w in epub_hebrew if len(w) >= 2)

    # Greek coverage
    greek_total = sum(pdf_greek_counts.values())
    greek_overlap = sum(min(c, epub_greek_counts.get(w, 0)) for w, c in pdf_greek_counts.items())
    greek_coverage = greek_overlap / greek_total if greek_total else 1.0

    # Hebrew coverage
    hebrew_total = sum(pdf_hebrew_counts.values())
    hebrew_overlap = sum(min(c, epub_hebrew_counts.get(w, 0)) for w, c in pdf_hebrew_counts.items())
    hebrew_coverage = hebrew_overlap / hebrew_total if hebrew_total else 1.0

    # Find significantly missing Greek words (present ≥3 times in PDF, <50% in EPUB)
    missing_greek = []
    for word, count in pdf_greek_counts.items():
        if count >= 3 and epub_greek_counts.get(word, 0) < count * 0.5:
            missing_greek.append({
                "word": word,
                "pdf": count,
                "epub": epub_greek_counts.get(word, 0),
            })
    missing_greek.sort(key=lambda x: x["pdf"] - x["epub"], reverse=True)

    # Find significantly missing Hebrew words
    missing_hebrew = []
    for word, count in pdf_hebrew_counts.items():
        if count >= 2 and epub_hebrew_counts.get(word, 0) < count * 0.5:
            missing_hebrew.append({
                "word": word,
                "pdf": count,
                "epub": epub_hebrew_counts.get(word, 0),
            })
    missing_hebrew.sort(key=lambda x: x["pdf"] - x["epub"], reverse=True)

    return {
        "pdf_greek_word_count": len(pdf_greek),
        "epub_greek_word_count": len(epub_greek),
        "pdf_greek_unique_words": len(pdf_greek_counts),
        "epub_greek_unique_words": len(epub_greek_counts),
        "greek_word_coverage_ratio": round(greek_coverage, 4),
        "pdf_hebrew_word_count": len(pdf_hebrew),
        "epub_hebrew_word_count": len(epub_hebrew),
        "pdf_hebrew_unique_words": len(pdf_hebrew_counts),
        "epub_hebrew_unique_words": len(epub_hebrew_counts),
        "hebrew_word_coverage_ratio": round(hebrew_coverage, 4),
        "missing_greek_word_samples": missing_greek[:25],
        "missing_hebrew_word_samples": missing_hebrew[:25],
    }


def greek_hebrew_clause_fidelity(pdf_pages: list[str], epub_text: str) -> dict[str, Any]:
    """Verify dense Greek/Hebrew passages from PDF are preserved in EPUB.

    A 'dense passage' is a sequence of ≥ 5 consecutive Greek or Hebrew words
    on a single PDF page. These are checked as normalized word strings
    against the EPUB text.
    """
    epub_norm = normalized_word_string(epub_text)
    missing_greek_clauses = []
    missing_hebrew_clauses = []
    checked_greek = 0
    checked_hebrew = 0

    for page_no, page_text in enumerate(pdf_pages, start=1):
        # Find Greek word sequences
        # Strip diacritics before finding sequences to make it robust
        page_text_stripped = strip_greek_diacritics(page_text)
        # Strip 'j'/'J' artifacts common in AGES Greek extraction
        page_text_stripped = re.sub(r'\b[jJ](?=[\u0370-\u03FF\u1F00-\u1FFF])', '', page_text_stripped)
        for current_seq in contiguous_script_runs(page_text_stripped, GREEK_WORD_RE):
            checked_greek += 1
            phrase = " ".join(current_seq)
            if phrase not in epub_norm:
                window_size = max(5, int(len(current_seq) * 0.8))
                found = any(
                    " ".join(current_seq[i:i + window_size]) in epub_norm
                    for i in range(len(current_seq) - window_size + 1)
                )
                if not found:
                    missing_greek_clauses.append({
                        "page": page_no,
                        "word_count": len(current_seq),
                        "sample": " ".join(current_seq[:12]),
                    })

        for current_seq in contiguous_script_runs(page_text, HEBREW_WORD_RE, min_words=3):
            checked_hebrew += 1
            phrase = " ".join(current_seq)
            if phrase not in epub_norm:
                window_size = max(3, int(len(current_seq) * 0.8))
                found = any(
                    " ".join(current_seq[i:i + window_size]) in epub_norm
                    for i in range(len(current_seq) - window_size + 1)
                )
                if not found:
                    missing_hebrew_clauses.append({
                        "page": page_no,
                        "word_count": len(current_seq),
                        "sample": " ".join(current_seq[:10]),
                    })

    return {
        "greek_clauses_checked": checked_greek,
        "missing_greek_clause_count": len(missing_greek_clauses),
        "missing_greek_clauses": missing_greek_clauses[:30],
        "hebrew_clauses_checked": checked_hebrew,
        "missing_hebrew_clause_count": len(missing_hebrew_clauses),
        "missing_hebrew_clauses": missing_hebrew_clauses[:30],
    }


def infer_paths(volume: int, root: Path) -> tuple[Path, Path, Path]:
    vol_dir = root / "volumes" / f"v{volume}"
    return (
        vol_dir / "input" / f"owen-v{volume}.pdf",
        vol_dir / "output" / f"volume_{volume}.epub",
        vol_dir / "bugs_fixes",
    )


def run_audit(volume: int, pdf_path: Path, epub_path: Path) -> dict[str, Any]:
    pdf_pages, pdf_meta = extract_pdf_pages(pdf_path)
    paragraphs, epub_meta = extract_epub_paragraphs(epub_path)

    pdf_text = "\n".join(pdf_pages)
    epub_text = "\n".join(p.text for p in paragraphs)

    word_coverage = compare_word_coverage(pdf_text, epub_text)
    page_scan = page_coverage(pdf_pages, epub_text)
    dense_scan = dense_source_window_integrity(pdf_pages, epub_text)
    front_toc_scan = front_matter_toc_integrity(pdf_pages, epub_text)
    top_scan = top_of_page_integrity(pdf_path, epub_text)
    bottom_scan = bottom_of_page_integrity(pdf_path, epub_text)
    para_scan = paragraph_integrity(paragraphs)
    enum_scan = enumerator_integrity(pdf_pages, paragraphs)
    repeats = repeated_windows(epub_text)
    gh_word_cov = greek_hebrew_word_coverage(pdf_pages, paragraphs)
    gh_clause_fid = greek_hebrew_clause_fidelity(pdf_pages, epub_text)

    warnings = []
    if word_coverage["coverage_ratio"] < 0.86:
        warnings.append({
            "code": "low_word_coverage",
            "message": "EPUB content word coverage against PDF extraction is lower than expected",
        })
    if page_scan["weak_page_count"]:
        warnings.append({
            "code": "weak_page_coverage",
            "message": "Some PDF pages have no strong text-window match in the EPUB",
        })
    if dense_scan["missing_dense_window_pages"]:
        warnings.append({
            "code": "dense_source_window_loss",
            "message": "Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors",
        })
    if front_toc_scan["missing_front_toc_pages"]:
        warnings.append({
            "code": "front_matter_toc_loss",
            "message": "Some early CONTENTS pages have no strong text-window match in the EPUB",
        })
    if top_scan["missing_top_window_count"]:
        warnings.append({
            "code": "top_of_page_text_loss",
            "message": "Some first body lines near the top of PDF pages are not found in the EPUB",
        })
    if bottom_scan["missing_bottom_window_count"]:
        warnings.append({
            "code": "bottom_of_page_text_loss",
            "message": "Some last body lines near the bottom of PDF pages are not found in the EPUB",
        })
    if para_scan["split_candidate_count"]:
        warnings.append({
            "code": "paragraph_split_candidates",
            "message": "Some adjacent EPUB paragraphs look like possible faulty line or page breaks",
        })
    if para_scan["adjacent_duplicate_count"]:
        warnings.append({
            "code": "adjacent_duplicate_paragraphs",
            "message": "Some adjacent EPUB paragraphs are near duplicates",
        })
    if para_scan["inline_structural_candidate_count"]:
        warnings.append({
            "code": "inline_structural_markers",
            "message": "Some list or roman markers appear embedded in prose instead of starting their own paragraph",
        })
    if para_scan["reference_continuation_split_count"]:
        warnings.append({
            "code": "reference_continuation_splits",
            "message": "Some scripture or chapter references are split across paragraph boundaries",
        })
    if para_scan["citation_continuation_split_count"]:
        warnings.append({
            "code": "citation_continuation_splits",
            "message": "Some scholarly citation chains are split across paragraph boundaries",
        })
    if para_scan["suspicious_large_number_start_count"]:
        warnings.append({
            "code": "suspicious_large_number_starts",
            "message": "Some paragraphs begin with large bare numbers that may be broken reference continuations",
        })
    if para_scan["roman_heading_candidate_count"]:
        warnings.append({
            "code": "roman_heading_candidates",
            "message": "Some roman numeral headings appear in body paragraphs instead of centered heading elements",
        })
    if para_scan["overlong_heading_candidate_count"]:
        warnings.append({
            "code": "overlong_heading_candidates",
            "message": "Some chapter headings are long enough to suggest swallowed body text",
        })
    if para_scan["frontmatter_heading_body_candidate_count"]:
        warnings.append({
            "code": "frontmatter_heading_body_candidates",
            "message": "Some front-matter headings appear to contain body text",
        })
    if enum_scan["missing_marker_count"]:
        warnings.append({
            "code": "missing_enumerator_markers",
            "message": "Some bracketed/parenthesized/ordinal markers present in the PDF are missing from the EPUB",
        })
    if enum_scan["orphan_candidate_count"]:
        warnings.append({
            "code": "enumerator_sequence_candidates",
            "message": "Some EPUB enumerators look like possible sequence jumps and need triage",
        })
    if repeats:
        warnings.append({
            "code": "repeated_windows",
            "message": "Repeated word windows may indicate ghost-layer duplication",
        })
    if gh_word_cov["pdf_greek_word_count"] >= 20 and gh_word_cov["greek_word_coverage_ratio"] < 0.80:
        warnings.append({
            "code": "low_greek_word_coverage",
            "message": "EPUB Greek word coverage against PDF extraction is lower than expected",
        })
    if gh_word_cov["pdf_hebrew_word_count"] >= 10 and gh_word_cov["hebrew_word_coverage_ratio"] < 0.80:
        warnings.append({
            "code": "low_hebrew_word_coverage",
            "message": "EPUB Hebrew word coverage against PDF extraction is lower than expected",
        })
    if gh_clause_fid["missing_greek_clause_count"]:
        warnings.append({
            "code": "missing_greek_clauses",
            "message": "Some dense Greek passages from the PDF are missing from the EPUB",
        })
    if gh_clause_fid["missing_hebrew_clause_count"]:
        warnings.append({
            "code": "missing_hebrew_clauses",
            "message": "Some dense Hebrew passages from the PDF are missing from the EPUB",
        })

    return {
        "volume": volume,
        "pdf_path": str(pdf_path),
        "epub_path": str(epub_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "warn" if warnings else "pass",
        "warning_count": len(warnings),
        "warnings": warnings,
        "pdf": pdf_meta,
        "epub": epub_meta,
        "word_coverage": word_coverage,
        "page_coverage": page_scan,
        "dense_source_window_integrity": dense_scan,
        "front_matter_toc_integrity": front_toc_scan,
        "top_of_page_integrity": top_scan,
        "bottom_of_page_integrity": bottom_scan,
        "paragraph_integrity": para_scan,
        "enumerator_integrity": enum_scan,
        "repeated_windows": repeats,
        "greek_hebrew_word_coverage": gh_word_cov,
        "greek_hebrew_clause_fidelity": gh_clause_fid,
        "limits": {
            "note": "Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.",
        },
    }


def write_reports(result: dict[str, Any], out_dir: Path, stem: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{stem}_text_integrity.json"
    md_path = out_dir / f"{stem}_text_integrity.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    return json_path, md_path


def render_markdown(result: dict[str, Any]) -> str:
    wc = result["word_coverage"]
    pc = result["page_coverage"]
    ds = result["dense_source_window_integrity"]
    ft = result["front_matter_toc_integrity"]
    tp = result["top_of_page_integrity"]
    bp = result["bottom_of_page_integrity"]
    pi = result["paragraph_integrity"]
    ei = result["enumerator_integrity"]
    gh = result["greek_hebrew_word_coverage"]
    ghf = result["greek_hebrew_clause_fidelity"]
    lines = [
        f"# Text Integrity Audit: Volume {result['volume']}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- Warnings: {result['warning_count']}",
        f"- PDF pages: {result['pdf']['page_count']}",
        f"- EPUB text files: {result['epub']['spine_text_files']}",
        f"- EPUB paragraphs/headings: {result['epub']['paragraph_count']}",
        "",
        "## Coverage",
        "",
        f"- PDF content tokens: {wc['pdf_content_tokens']}",
        f"- EPUB content tokens: {wc['epub_content_tokens']}",
        f"- Approximate PDF-to-EPUB coverage ratio: {wc['coverage_ratio']}",
        f"- Pages checked: {pc['pages_checked']}",
        f"- Weak page matches: {pc['weak_page_count']}",
        f"- Dense source windows checked: {ds['dense_windows_checked']}",
        f"- Missing dense source-window pages: {ds['missing_dense_window_pages']}",
        f"- Front CONTENTS pages checked: {ft['front_toc_pages_checked']}",
        f"- Missing front CONTENTS pages: {ft['missing_front_toc_pages']}",
        f"- Top-of-page body windows checked: {tp['top_windows_usable']}",
        f"- Top-of-page windows skipped as unstable: {tp['skipped_top_window_count']}",
        f"- Missing top-of-page body windows: {tp['missing_top_window_count']}",
        f"- Bottom-of-page body windows checked: {bp['bottom_windows_usable']}",
        f"- Bottom-of-page windows skipped as unstable: {bp['skipped_bottom_window_count']}",
        f"- Missing bottom-of-page body windows: {bp['missing_bottom_window_count']}",
        "",
        "## Paragraphs",
        "",
        f"- Body paragraphs checked: {pi['paragraphs_checked']}",
        f"- Possible faulty paragraph splits: {pi['split_candidate_count']}",
        f"- Structural starts excluded from split warnings: {pi['structural_start_exclusions']}",
        f"- Short fragments: {pi['short_fragment_count']}",
        f"- Adjacent duplicate paragraphs: {pi['adjacent_duplicate_count']}",
        f"- Inline structural marker candidates: {pi['inline_structural_candidate_count']}",
        f"- Reference continuation splits: {pi['reference_continuation_split_count']}",
        f"- Citation continuation splits: {pi['citation_continuation_split_count']}",
        f"- Suspicious large-number starts: {pi['suspicious_large_number_start_count']}",
        f"- Roman heading candidates: {pi['roman_heading_candidate_count']}",
        f"- Overlong heading candidates: {pi['overlong_heading_candidate_count']}",
        f"- Front-matter heading/body candidates: {pi['frontmatter_heading_body_candidate_count']}",
        f"- Repeated word windows: {len(result['repeated_windows'])}",
        f"- PDF enumerator markers: {ei['pdf_marker_count']}",
        f"- EPUB enumerator markers: {ei['epub_marker_count']}",
        f"- Missing enumerator marker forms: {ei['missing_marker_count']}",
        f"- Enumerator sequence candidates: {ei['orphan_candidate_count']}",
        "",
        "## Greek / Hebrew",
        "",
        f"- PDF Greek words: {gh['pdf_greek_word_count']}",
        f"- EPUB Greek words: {gh['epub_greek_word_count']}",
        f"- Greek word coverage ratio: {gh['greek_word_coverage_ratio']}",
        f"- PDF Hebrew words: {gh['pdf_hebrew_word_count']}",
        f"- EPUB Hebrew words: {gh['epub_hebrew_word_count']}",
        f"- Hebrew word coverage ratio: {gh['hebrew_word_coverage_ratio']}",
        f"- Greek clauses checked: {ghf['greek_clauses_checked']}",
        f"- Missing Greek clauses: {ghf['missing_greek_clause_count']}",
        f"- Hebrew clauses checked: {ghf['hebrew_clauses_checked']}",
        f"- Missing Hebrew clauses: {ghf['missing_hebrew_clause_count']}",
        "",
    ]

    if result["warnings"]:
        lines.extend(["## Warnings", ""])
        for item in result["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    add_sample_section(lines, "Missing Dense Source Windows", ds["missing_dense_windows"], ["page", "sample"])
    add_sample_section(lines, "Missing Front CONTENTS Pages", ft["missing_front_toc_samples"], ["page", "hit_ratio", "sample"])
    add_sample_section(lines, "Missing Top-Of-Page Body Windows", tp["missing_top_windows"], ["page", "sample"])
    add_sample_section(lines, "Missing Bottom-Of-Page Body Windows", bp["missing_bottom_windows"], ["page", "sample"])
    add_sample_section(lines, "Possible Paragraph Splits", pi["split_candidates"], ["file", "previous", "next"])
    add_sample_section(lines, "Adjacent Duplicate Paragraphs", pi["adjacent_duplicates"], ["file", "previous", "next"])
    add_sample_section(lines, "Inline Structural Marker Candidates", pi["inline_structural_candidates"], ["file", "text"])
    add_sample_section(lines, "Reference Continuation Splits", pi["reference_continuation_splits"], ["file", "previous", "next"])
    add_sample_section(lines, "Citation Continuation Splits", pi["citation_continuation_splits"], ["file", "previous", "next"])
    add_sample_section(lines, "Suspicious Large-Number Starts", pi["suspicious_large_number_starts"], ["file", "text"])
    add_sample_section(lines, "Roman Heading Candidates", pi["roman_heading_candidates"], ["file", "text"])
    add_sample_section(lines, "Overlong Heading Candidates", pi["overlong_heading_candidates"], ["file", "tag", "text"])
    add_sample_section(lines, "Front-Matter Heading Body Candidates", pi["frontmatter_heading_body_candidates"], ["file", "tag", "text"])
    add_sample_section(lines, "Short Fragments", pi["short_fragments"], ["file", "text"])
    add_sample_section(lines, "Missing Enumerator Markers", ei["missing_markers"], ["marker", "pdf", "epub", "examples"])
    add_sample_section(lines, "Enumerator Sequence Candidates", ei["orphan_candidates"], ["file", "marker", "family", "context"])
    add_sample_section(lines, "Repeated Windows", result["repeated_windows"], ["phrase", "count"])
    add_sample_section(lines, "Missing Word Samples", wc["missing_word_samples"], ["word", "pdf", "epub"])
    add_sample_section(lines, "Excess Word Samples", wc["excess_word_samples"], ["word", "pdf", "epub"])
    add_sample_section(lines, "Missing Greek Word Samples", gh["missing_greek_word_samples"], ["word", "pdf", "epub"])
    add_sample_section(lines, "Missing Hebrew Word Samples", gh["missing_hebrew_word_samples"], ["word", "pdf", "epub"])
    add_sample_section(lines, "Missing Greek Clauses", ghf["missing_greek_clauses"], ["page", "word_count", "sample"])
    add_sample_section(lines, "Missing Hebrew Clauses", ghf["missing_hebrew_clauses"], ["page", "word_count", "sample"])

    lines.extend([
        "## Limits",
        "",
        result["limits"]["note"],
        "",
    ])
    return "\n".join(lines).rstrip() + "\n"


def add_sample_section(lines: list[str], title: str, rows: list[dict[str, Any]], fields: list[str], limit: int = 10) -> None:
    if not rows:
        return
    lines.extend([f"## {title}", ""])
    for row in rows[:limit]:
        parts = []
        for field in fields:
            value = display_value(row.get(field, ""))
            if len(value) > 240:
                value = value[:237] + "..."
            parts.append(f"{field}: {value}")
        lines.append("- " + "; ".join(parts))
    lines.append("")


def display_value(value: Any) -> str:
    if isinstance(value, (int, float)):
        return str(value)
    return clean_text(str(value))


def render_bug_log_section(result: dict[str, Any], json_path: Path, md_path: Path) -> str:
    wc = result["word_coverage"]
    pc = result["page_coverage"]
    ds = result["dense_source_window_integrity"]
    ft = result["front_matter_toc_integrity"]
    tp = result["top_of_page_integrity"]
    bp = result["bottom_of_page_integrity"]
    pi = result["paragraph_integrity"]
    ei = result["enumerator_integrity"]
    gh = result["greek_hebrew_word_coverage"]
    ghf = result["greek_hebrew_clause_fidelity"]
    lines = [
        "<!-- TEXT_INTEGRITY_START -->",
        "## Automated Textual Integrity Audit",
        "",
        f"**Last run:** {result['generated_at']}",
        f"**Status:** {result['status'].upper()} ({result['warning_count']} warnings)",
        "",
        "Reports:",
        f"- `{json_path.name}`",
        f"- `{md_path.name}`",
        "",
        "| Check | Result |",
        "|-------|--------|",
        f"| PDF pages | {result['pdf']['page_count']} |",
        f"| EPUB text files | {result['epub']['spine_text_files']} |",
        f"| EPUB paragraphs/headings | {result['epub']['paragraph_count']} |",
        f"| Approximate PDF-to-EPUB word coverage | {wc['coverage_ratio']} |",
        f"| Weak page matches | {pc['weak_page_count']} |",
        f"| Dense source windows checked | {ds['dense_windows_checked']} |",
        f"| Missing dense source-window pages | {ds['missing_dense_window_pages']} |",
        f"| Front CONTENTS pages checked | {ft['front_toc_pages_checked']} |",
        f"| Missing front CONTENTS pages | {ft['missing_front_toc_pages']} |",
        f"| Top-of-page body windows checked | {tp['top_windows_usable']} |",
        f"| Top-of-page windows skipped as unstable | {tp['skipped_top_window_count']} |",
        f"| Missing top-of-page body windows | {tp['missing_top_window_count']} |",
        f"| Bottom-of-page body windows checked | {bp['bottom_windows_usable']} |",
        f"| Bottom-of-page windows skipped as unstable | {bp['skipped_bottom_window_count']} |",
        f"| Missing bottom-of-page body windows | {bp['missing_bottom_window_count']} |",
        f"| Possible faulty paragraph splits | {pi['split_candidate_count']} |",
        f"| Structural starts excluded from split warnings | {pi['structural_start_exclusions']} |",
        f"| Short fragments | {pi['short_fragment_count']} |",
        f"| Adjacent duplicate paragraphs | {pi['adjacent_duplicate_count']} |",
        f"| Inline structural marker candidates | {pi['inline_structural_candidate_count']} |",
        f"| Reference continuation splits | {pi['reference_continuation_split_count']} |",
        f"| Citation continuation splits | {pi['citation_continuation_split_count']} |",
        f"| Suspicious large-number starts | {pi['suspicious_large_number_start_count']} |",
        f"| Roman heading candidates | {pi['roman_heading_candidate_count']} |",
        f"| Overlong heading candidates | {pi['overlong_heading_candidate_count']} |",
        f"| Front-matter heading/body candidates | {pi['frontmatter_heading_body_candidate_count']} |",
        f"| Repeated word windows | {len(result['repeated_windows'])} |",
        f"| PDF enumerator markers | {ei['pdf_marker_count']} |",
        f"| EPUB enumerator markers | {ei['epub_marker_count']} |",
        f"| Missing enumerator marker forms | {ei['missing_marker_count']} |",
        f"| Enumerator sequence candidates | {ei['orphan_candidate_count']} |",
        f"| PDF Greek words / EPUB Greek words | {gh['pdf_greek_word_count']} / {gh['epub_greek_word_count']} |",
        f"| Greek word coverage ratio | {gh['greek_word_coverage_ratio']} |",
        f"| PDF Hebrew words / EPUB Hebrew words | {gh['pdf_hebrew_word_count']} / {gh['epub_hebrew_word_count']} |",
        f"| Hebrew word coverage ratio | {gh['hebrew_word_coverage_ratio']} |",
        f"| Missing Greek clauses | {ghf['missing_greek_clause_count']} |",
        f"| Missing Hebrew clauses | {ghf['missing_hebrew_clause_count']} |",
        "",
    ]

    if result["warnings"]:
        lines.extend(["Warnings requiring triage:", ""])
        for item in result["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    lines.extend([
        "**Status note:** This audit is a mechanical integrity screen, not final proofreading or user validation.",
        "<!-- TEXT_INTEGRITY_END -->",
        "",
    ])
    return "\n".join(lines)


def update_bug_log(result: dict[str, Any], json_path: Path, md_path: Path) -> Path | None:
    bug_log = md_path.parent / "BUGS_AND_FIXES.md"
    if not bug_log.exists():
        return None
    content = bug_log.read_text(encoding="utf-8")
    section = render_bug_log_section(result, json_path, md_path).rstrip()
    pattern = re.compile(r"\n?<!-- TEXT_INTEGRITY_START -->.*?<!-- TEXT_INTEGRITY_END -->\n?", re.S)
    if pattern.search(content):
        updated = pattern.sub("\n\n" + section + "\n", content).rstrip() + "\n"
    else:
        updated = content.rstrip() + "\n\n---\n\n" + section + "\n"
    bug_log.write_text(updated, encoding="utf-8")
    return bug_log


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit textual integrity between an Owen PDF and EPUB")
    parser.add_argument("volume", type=int, help="Owen volume number")
    parser.add_argument("--pdf", type=Path, default=None, help="Override source PDF path")
    parser.add_argument("--epub", type=Path, default=None, help="Override generated EPUB path")
    parser.add_argument("--out-dir", type=Path, default=None, help="Override report output directory")
    parser.add_argument("--no-bug-log", action="store_true", help="Do not update BUGS_AND_FIXES.md")
    args = parser.parse_args(argv)

    root = Path.cwd()
    default_pdf, default_epub, default_out = infer_paths(args.volume, root)
    pdf_path = args.pdf or default_pdf
    epub_path = args.epub or default_epub
    out_dir = args.out_dir or default_out

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1
    if not epub_path.exists():
        print(f"EPUB not found: {epub_path}", file=sys.stderr)
        return 1

    result = run_audit(args.volume, pdf_path, epub_path)
    stem = f"volume_{args.volume}"
    json_path, md_path = write_reports(result, out_dir, stem)
    bug_log = None if args.no_bug_log else update_bug_log(result, json_path, md_path)

    print(render_markdown(result))
    print(f"Reports written:\n- {json_path}\n- {md_path}")
    if bug_log:
        print(f"Bug log updated:\n- {bug_log}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
