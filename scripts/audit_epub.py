#!/usr/bin/env python3
"""Audit generated Owen EPUB3 files.

The checks here are intentionally conservative: they flag packaging,
navigation, language-tagging, footnote, boilerplate, and duplication risks
without mutating the EPUB or the converter.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urldefrag

from lxml import etree


NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "epub": "http://www.idpf.org/2007/ops",
}

GREEK_RE = re.compile(r"[\u0370-\u03ff\u1f00-\u1fff]")
HEBREW_RE = re.compile(r"[\u0590-\u05ff]")
HTML_TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
WORD_RE = re.compile(r"\b[\w\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff'-]+\b", re.UNICODE)

EMPTY_BRACKET_RE = re.compile(r"\[\s*\]")
CHAPTER_HEADING_RE = re.compile(
    r'<h1[^>]*class="[^"]*\bchapter-heading\b[^"]*"[^>]*>.*?</h1>',
    re.I | re.S,
)
CHAPTER_INITIALIZER_RE = re.compile(
    r'^\s*<(?:p class="(?:chapter-opening|chapter-argument)"|h3 class="chapter-summary")>',
    re.I | re.S,
)
LEADING_CHAPTER_SUBTITLE_RE = re.compile(
    r'^\s*<h4[^>]*class="[^"]*\b(?:chapter-subtitle|roman-subheading)\b[^"]*"[^>]*>.*?</h4>',
    re.I | re.S,
)
LEADING_CHAPTER_FRONT_LIST_RE = re.compile(
    r'^\s*<p>\s*(?:<b>)?\d{1,2}\.(?:</b>)?\s+[^<]{8,180}</p>',
    re.I | re.S,
)

EMPTY_BRACKET_RE = re.compile(r"\[\s*\]")

BOILERPLATE_PATTERNS = [
    "THE AGES DIGITAL LIBRARY",
    "JOHN OWEN COLLECTION",
    "B o o k s F o r T h e A g e s",
    "Books For The Ages",
    "AGES Software",
    "Version 1.0",
]

BETA_CODE_RESIDUE_RE = re.compile(
    r"\b(?:[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW][><=~|{}\[\]jJ+]+"
    r"|[><=~|{}\[\]jJ+]+[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW])\b"
)


class Audit:
    def __init__(self, epub_path: Path, out_dir: Path | None = None) -> None:
        self.epub_path = epub_path
        self.out_dir = out_dir
        self.errors: list[dict[str, Any]] = []
        self.warnings: list[dict[str, Any]] = []
        self.info: dict[str, Any] = {}
        self.files: set[str] = set()
        self.opf_path: str | None = None
        self.opf_dir = ""
        self.manifest: dict[str, dict[str, str]] = {}
        self.spine_idrefs: list[str] = []
        self.xhtml_files: list[str] = []
        self.nav_files: list[str] = []

    def error(self, code: str, message: str, **data: Any) -> None:
        self.errors.append({"code": code, "message": message, **data})

    def warn(self, code: str, message: str, **data: Any) -> None:
        self.warnings.append({"code": code, "message": message, **data})

    def run(self) -> dict[str, Any]:
        if not self.epub_path.exists():
            self.error("missing_epub", "EPUB file does not exist", path=str(self.epub_path))
            return self.result()

        try:
            with zipfile.ZipFile(self.epub_path) as zf:
                self.files = set(zf.namelist())
                self.info["file_count"] = len(self.files)
                self.info["epub_size_bytes"] = self.epub_path.stat().st_size
                self.check_zip_basics(zf)
                self.load_opf(zf)
                if self.opf_path:
                    self.check_opf(zf)
                    self.check_xhtml(zf)
                    self.check_nav_links(zf)
                    self.check_apple_options()
        except zipfile.BadZipFile:
            self.error("bad_zip", "EPUB is not a valid ZIP archive")

        return self.result()

    def check_zip_basics(self, zf: zipfile.ZipFile) -> None:
        names = zf.namelist()
        if not names:
            self.error("empty_zip", "EPUB archive has no files")
            return

        if names[0] != "mimetype":
            self.error("mimetype_not_first", "The mimetype file must be the first ZIP entry", first=names[0])
        if "mimetype" not in self.files:
            self.error("missing_mimetype", "Missing mimetype file")
        else:
            content = zf.read("mimetype").decode("utf-8", "replace")
            if content != "application/epub+zip":
                self.error("bad_mimetype", "mimetype has unexpected content", content=content)
            info = zf.getinfo("mimetype")
            if info.compress_type != zipfile.ZIP_STORED:
                self.warn("mimetype_compressed", "mimetype should be stored uncompressed")

        if "META-INF/container.xml" not in self.files:
            self.error("missing_container", "Missing META-INF/container.xml")

    def load_opf(self, zf: zipfile.ZipFile) -> None:
        if "META-INF/container.xml" not in self.files:
            return
        try:
            root = parse_xml(zf.read("META-INF/container.xml"))
            rootfile = root.find(".//container:rootfile", namespaces=NS)
            if rootfile is None:
                self.error("missing_rootfile", "container.xml has no rootfile entry")
                return
            opf_path = rootfile.get("full-path")
            if not opf_path:
                self.error("missing_opf_path", "container rootfile has no full-path")
                return
            if opf_path not in self.files:
                self.error("opf_not_found", "OPF path from container is missing from EPUB", opf_path=opf_path)
                return
            self.opf_path = opf_path
            self.opf_dir = posixpath.dirname(opf_path)
            self.info["opf_path"] = opf_path
        except etree.XMLSyntaxError as exc:
            self.error("container_xml_invalid", "container.xml is not valid XML", detail=str(exc))

    def check_opf(self, zf: zipfile.ZipFile) -> None:
        assert self.opf_path is not None
        try:
            root = parse_xml(zf.read(self.opf_path))
        except etree.XMLSyntaxError as exc:
            self.error("opf_xml_invalid", "OPF is not valid XML", detail=str(exc))
            return

        version = root.get("version")
        self.info["opf_version"] = version
        if version != "3.0":
            self.error("opf_not_epub3", "OPF package version is not 3.0", version=version)

        titles = [clean_text(el.text or "") for el in root.xpath(".//dc:title", namespaces=NS)]
        creators = [clean_text(el.text or "") for el in root.xpath(".//dc:creator", namespaces=NS)]
        self.info["titles"] = titles
        self.info["creators"] = creators
        if not titles:
            self.error("missing_title", "OPF metadata has no dc:title")
        if not creators:
            self.warn("missing_creator", "OPF metadata has no dc:creator")

        for item in root.xpath(".//opf:manifest/opf:item", namespaces=NS):
            item_id = item.get("id")
            href = item.get("href")
            media_type = item.get("media-type", "")
            if not item_id or not href:
                self.warn("manifest_item_incomplete", "Manifest item missing id or href")
                continue
            full_href = norm_join(self.opf_dir, href)
            props = item.get("properties", "")
            self.manifest[item_id] = {
                "href": full_href,
                "media_type": media_type,
                "properties": props,
            }
            if full_href not in self.files:
                self.error("manifest_file_missing", "Manifest href does not exist in EPUB", id=item_id, href=full_href)
            if media_type in ("application/xhtml+xml", "text/html") or full_href.endswith((".xhtml", ".html")):
                self.xhtml_files.append(full_href)
            if "nav" in props.split():
                self.nav_files.append(full_href)

        self.spine_idrefs = [
            itemref.get("idref", "")
            for itemref in root.xpath(".//opf:spine/opf:itemref", namespaces=NS)
            if itemref.get("idref")
        ]
        for idref in self.spine_idrefs:
            if idref not in self.manifest:
                self.error("spine_idref_missing", "Spine idref is not present in manifest", idref=idref)

        self.info["manifest_count"] = len(self.manifest)
        self.info["spine_count"] = len(self.spine_idrefs)
        self.info["xhtml_count"] = len(set(self.xhtml_files))
        self.info["nav_files"] = self.nav_files
        self.info["font_count"] = sum(1 for item in self.manifest.values() if "font" in item["media_type"])

        if not self.nav_files:
            self.error("missing_nav_property", "No manifest item has properties='nav'")
        nav_idrefs_in_spine = [
            idref for idref in self.spine_idrefs
            if "nav" in self.manifest.get(idref, {}).get("properties", "").split()
        ]
        if nav_idrefs_in_spine:
            self.error(
                "nav_in_spine",
                "EPUB navigation document is in the reading-order spine",
                idrefs=nav_idrefs_in_spine,
            )
        if not any(item["href"].endswith("toc.ncx") for item in self.manifest.values()):
            self.warn("missing_ncx", "No NCX file found in manifest")
        if not any(item["href"].lower().endswith((".ttf", ".otf")) for item in self.manifest.values()):
            self.error("missing_fonts", "No embedded font files found in manifest")
        if not any("cover" in item["properties"].split() or item_id == "cover-img" for item_id, item in self.manifest.items()):
            self.warn("missing_cover_manifest_hint", "No obvious cover image manifest hint found")

    def check_xhtml(self, zf: zipfile.ZipFile) -> None:
        totals = Counter()
        samples: dict[str, list[dict[str, Any]]] = {
            "boilerplate": [],
            "beta_code": [],
            "escaped_lang_tag": [],
            "untagged_greek": [],
            "untagged_hebrew": [],
            "hebrew_integrity": [],
            "repeated_phrase": [],
            "literal_footnote_marker": [],
            "empty_bracket_noise": [],
            "noteref_without_class": [],
            "missing_chapter_initialization": [],
            # New checks — populated below
            "unprocessed_ages_marker": [],
            "page_reference_split": [],
            "chapter_heading_in_paragraph": [],
            "overlong_heading_body": [],
            "fragmented_greek_span_run": [],
            "scripture_blockquote": [],
            "orphan_scripture_bracket": [],
            "glued_ordinal": [],
            "structural_bold_leak": [],
            "repeated_structural_marker": [],
            "scholastic_bold_leak": [],
            "inline_scholastic_label": [],
            "trailing_scholastic_label": [],
            "digression_not_h3": [],
            "cross_chapter_continuation": [],
            "nav_overlong_entry": [],
            "nav_duplicate_text": [],
            "spaced_caps": [],
            "lowercase_paragraph_start": [],
            "noteref_leading_space": [],
            "greek_span_legacy_accent": [],
            "quote_prose_join": [],
            "i_will_mangle": [],
        }
        noteref_targets: list[str] = []
        endnote_ids: set[str] = set()
        all_text_parts: list[str] = []

        for path in sorted(set(self.xhtml_files)):
            if path not in self.files:
                continue
            raw = zf.read(path).decode("utf-8", "replace")
            if "xmlns:epub=" not in raw:
                self.warn("xhtml_missing_epub_namespace", "XHTML file is missing xmlns:epub", file=path)
                totals["xhtml_missing_epub_namespace"] += 1

            text = html_to_text(raw)
            all_text_parts.append(text)

            upper = text.upper()
            for pattern in BOILERPLATE_PATTERNS:
                if pattern.upper() in upper:
                    add_sample(samples["boilerplate"], path, pattern)
                    totals["boilerplate_hits"] += 1

            beta_hits = BETA_CODE_RESIDUE_RE.findall(text)
            if beta_hits:
                add_sample(samples["beta_code"], path, beta_hits[0])
                totals["beta_code_files"] += 1

            literal_fn_hits = re.findall(r'(?:\[\s*f\s*\d{1,3}\s*\]|\bf\s*\d{1,3}\b)', text, flags=re.I)
            if literal_fn_hits:
                add_sample(samples["literal_footnote_marker"], path, literal_fn_hits[0])
                totals["literal_footnote_marker_files"] += 1

            if EMPTY_BRACKET_RE.search(text):
                add_sample(samples["empty_bracket_noise"], path, text)
                totals["empty_bracket_noise_files"] += 1

            escaped_lang_hits = re.findall(r"&lt;span\s+lang=&quot;(?:el|he)&quot;.*?&gt;", raw)
            if not escaped_lang_hits:
                escaped_lang_hits = re.findall(r"&lt;span\s+lang=\"(?:el|he)\".*?&gt;", raw)
            if escaped_lang_hits:
                add_sample(samples["escaped_lang_tag"], path, escaped_lang_hits[0])
                totals["escaped_lang_tag_files"] += 1

            try:
                root = parse_xml(raw.encode("utf-8"))
            except etree.XMLSyntaxError as exc:
                self.error("xhtml_xml_invalid", "XHTML is not valid XML", file=path, detail=str(exc))
                continue

            stats = inspect_language_tagging(root, path, samples)
            missing_chapter_initializers = 0
            for chapter_match in CHAPTER_HEADING_RE.finditer(raw):
                heading_text = HTML_TAG_RE.sub('', chapter_match.group(0))
                # Only check initialization for start of Part/Volume (usually Chapter 1 or I)
                # Sub-chapters (Chapter 2, 3, etc.) are allowed to start with plain body text.
                chapter_num_match = re.search(r'CHAPTER\s+([IVXLCDM\d]+)', heading_text, re.I)
                if chapter_num_match:
                    num = chapter_num_match.group(1).upper()
                    if num not in ('1', 'I'):
                        continue

                after_heading = raw[chapter_match.end():]
                previous_after = None
                while previous_after != after_heading:
                    previous_after = after_heading
                    after_heading = LEADING_CHAPTER_SUBTITLE_RE.sub('', after_heading, count=1)
                    after_heading = LEADING_CHAPTER_FRONT_LIST_RE.sub('', after_heading, count=1)
                    
                while True:
                    new_after = re.sub(r"^\s*<p>[^a-z<]+</p>", "", after_heading, count=1, flags=re.S)
                    if new_after == after_heading:
                        break
                    after_heading = new_after

                    after_heading = re.sub(r"^\s*<p>OF COMMUNION .*?</p>", "", after_heading, flags=re.I | re.S)

                if not re.search(r"<(?:p class=\"(?:chapter-opening|chapter-argument)\"|h3 class=\"chapter-summary\")>", after_heading[:2000], re.I | re.S):
                    missing_chapter_initializers += 1
            if missing_chapter_initializers:
                add_sample(samples["missing_chapter_initialization"], path, "chapter starts with plain body text")
                totals["missing_chapter_initialization_files"] += 1

            totals.update(stats)

            # ── New content scan checks ──────────────────────────────────────

            # Unprocessed AGES verse markers: <[0-9]+ > in rendered text
            ages_hits = re.findall(r"<\d{6,9}>", text)
            if ages_hits:
                add_sample(samples["unprocessed_ages_marker"], path, ages_hits[0])
                totals["unprocessed_ages_marker_files"] += 1

            # Page-reference splits: "p. NNN." at end of paragraph (false split)
            pref_hits = re.findall(r"\bp\.\s+\d{1,4}\.\s*$", text, re.MULTILINE)
            if pref_hits:
                add_sample(samples["page_reference_split"], path, pref_hits[0])
                totals["page_reference_split_files"] += 1

            # Chapter heading rendered inside <p> (not in <h1>/<h2>)
            ch_para_hits = re.findall(r"<p[^>]*>(?:[^<]|\n){0,30}CHAPTER\s+[IVXLCDM\d]+", raw, re.I | re.S)
            if ch_para_hits:
                add_sample(samples["chapter_heading_in_paragraph"], path, HTML_TAG_RE.sub("", ch_para_hits[0])[:160])
                totals["chapter_heading_in_paragraph_files"] += 1

            # Overlong heading: h1/h2/h3 containing >40 words (body prose swallowed)
            overlong_hits = re.findall(r"<h[123][^>]*>(.*?)</h[123]>", raw, re.I | re.S)
            for oh in overlong_hits:
                oh_text = HTML_TAG_RE.sub(" ", oh).strip()
                if len(oh_text.split()) > 40:
                    add_sample(samples["overlong_heading_body"], path, oh_text[:180])
                    totals["overlong_heading_body_files"] += 1
                    break

            # Fragmented Greek span runs: adjacent Greek spans with only whitespace between
            frag_greek = re.findall(
                r'<span[^>]+lang=["\']el["\'][^>]*>[^<]{1,5}</span>\s{0,3}<span[^>]+lang=["\']el["\'][^>]*>',
                raw, re.I
            )
            if frag_greek:
                add_sample(samples["fragmented_greek_span_run"], path, frag_greek[0][:160])
                totals["fragmented_greek_span_run_files"] += 1

            # Glued ordinals: e.g. ")1." or "2.3." stuck to adjacent text
            glued_hits = re.findall(r"[)\]]\d{1,2}\.\S", text)
            if glued_hits:
                add_sample(samples["glued_ordinal"], path, glued_hits[0])
                totals["glued_ordinal_files"] += 1

            # Structural bold leaks: entire <p> is bold (>85% of text is in <b>)
            p_blocks = re.findall(r"<p[^>]*>(.*?)</p>", raw, re.I | re.S)
            for pb in p_blocks[:300]:  # limit to first 300 paragraphs for speed
                pb_plain = HTML_TAG_RE.sub("", pb).strip()
                if len(pb_plain) < 40:
                    continue
                bold_text = "".join(re.findall(r"<b[^>]*>(.*?)</b>", pb, re.I | re.S))
                bold_plain = HTML_TAG_RE.sub("", bold_text).strip()
                if bold_plain and len(bold_plain) > 0.85 * len(pb_plain) and len(pb_plain) > 60:
                    add_sample(samples["structural_bold_leak"], path, pb_plain[:160])
                    totals["structural_bold_leak_files"] += 1
                    break

            # Repeated structural markers: e.g. [1.] [1.] in same paragraph
            rep_struct = re.findall(r"(\[\d{1,2}\.\])\s+\1", text)
            if rep_struct:
                add_sample(samples["repeated_structural_marker"], path, rep_struct[0])
                totals["repeated_structural_marker_files"] += 1

            # Scholastic bold leaks: >3 bold words after Obj./Ans./Use label
            schol_leak_hits = re.findall(
                r"<b[^>]*>(?:Obj(?:ection)?|Ans(?:wer)?|Use\s+\d+|Usus\s+\d+)\.[^<]{30,}</b>",
                raw, re.I
            )
            if schol_leak_hits:
                add_sample(samples["scholastic_bold_leak"], path, HTML_TAG_RE.sub("", schol_leak_hits[0])[:160])
                totals["scholastic_bold_leak_files"] += 1

            # Inline scholastic labels: Obj./Ans. appearing mid-paragraph (not at start)
            inline_schol = re.findall(
                r"[a-z,;]\s+(?:Obj(?:ection)?|Ans(?:wer)?|Use\s+\d+|Usus\s+\d+)\.",
                text
            )
            if inline_schol:
                add_sample(samples["inline_scholastic_label"], path, inline_schol[0])
                totals["inline_scholastic_label_files"] += 1

            # Trailing scholastic labels: paragraph ends with Obj./Ans. (must break before)
            trailing_schol = re.findall(
                r"(?:Obj(?:ection)?|Ans(?:wer)?)\.\s*$",
                text, re.MULTILINE
            )
            if trailing_schol:
                add_sample(samples["trailing_scholastic_label"], path, trailing_schol[0])
                totals["trailing_scholastic_label_files"] += 1

            # DIGRESSION headings not promoted to h3
            digr_in_para = re.findall(r"<p[^>]*>\s*DIGRESSION\b", raw, re.I)
            if digr_in_para:
                add_sample(samples["digression_not_h3"], path, "DIGRESSION found in <p> not <h3>")
                totals["digression_not_h3_files"] += 1

            # Spaced-caps OCR: single capital letters separated by spaces (M E, T H E)
            spaced_caps_hits = re.findall(r"\b(?:[A-Z]\s){2,}[A-Z]\b", text)
            if spaced_caps_hits:
                add_sample(samples["spaced_caps"], path, spaced_caps_hits[0])
                totals["spaced_caps_files"] += 1

            # Lowercase paragraph start (failed page-join)
            lc_para_starts = re.findall(r"<p[^>]*>\s*[a-z]", raw)
            # Exclude list-continuation patterns like "(2." starting with digit
            lc_real = [h for h in lc_para_starts if not re.match(r"<p[^>]*>\s*[a-z]{1,2}\.", h)]
            if lc_real:
                add_sample(samples["lowercase_paragraph_start"], path, HTML_TAG_RE.sub("", lc_real[0])[:100])
                totals["lowercase_paragraph_start_files"] += 1

            # Noteref leading space: space character before superscript footnote marker
            nref_space_hits = re.findall(r"\s<[^>]+epub:type=['\"]noteref['\"]", raw)
            if nref_space_hits:
                add_sample(samples["noteref_leading_space"], path, nref_space_hits[0][:100])
                totals["noteref_leading_space_files"] += 1

            # Greek span legacy accents: ~, >, < inside a Greek-tagged span
            greek_spans = re.findall(r'<span[^>]+lang=["\']el["\'][^>]*>(.*?)</span>', raw, re.I | re.S)
            for gs in greek_spans:
                gs_text = HTML_TAG_RE.sub("", gs)
                if re.search(r"[~><]", gs_text):
                    add_sample(samples["greek_span_legacy_accent"], path, gs_text[:120])
                    totals["greek_span_legacy_accent_files"] += 1
                    break

            # I WILL / I AM mangles: IWILL or e will or i will (lower)
            mangle_hits = re.findall(r"\bIWILL\b|\be will\b|\bIAM\b", text)
            if mangle_hits:
                add_sample(samples["i_will_mangle"], path, mangle_hits[0])
                totals["i_will_mangle_files"] += 1

            for el in root.iter():
                epub_type = attr(el, "epub:type")
                if epub_type and "noteref" in epub_type.split():
                    href = el.get("href") or el.get("{http://www.w3.org/1999/xlink}href")
                    if href:
                        noteref_targets.append(resolve_href(path, href))
                    if "noteref" not in (el.get("class") or "").split():
                        add_sample(samples["noteref_without_class"], path, etree.tostring(el, encoding="unicode")[:160])
                        totals["noteref_without_class"] += 1
                el_id = el.get("id")
                if el_id and el_id.startswith("fn"):
                    role = el.get("role", "")
                    if "doc-endnote" in role or "endnote" in (epub_type or ""):
                        endnote_ids.add(resolve_href(path, f"#{el_id}"))

        repeated = find_repeated_phrases("\n".join(all_text_parts))
        for item in repeated:
            add_sample(samples["repeated_phrase"], "combined_text", item["phrase"], count=item["count"])
        totals["repeated_phrase_count"] = len(repeated)

        noteref_set = set(noteref_targets)
        missing_endnotes = sorted(noteref_set - endnote_ids)[:25]
        orphan_endnotes = sorted(endnote_ids - noteref_set)[:25]

        self.info["language"] = {
            "greek_chars": totals["greek_chars"],
            "greek_untagged_chars": totals["greek_untagged_chars"],
            "hebrew_chars": totals["hebrew_chars"],
            "hebrew_untagged_chars": totals["hebrew_untagged_chars"],
            "files_with_untagged_greek": totals["files_with_untagged_greek"],
            "files_with_untagged_hebrew": totals["files_with_untagged_hebrew"],
            # Hebrew integrity: RTL+lang="he" both required
            "hebrew_integrity_failures": totals["hebrew_untagged_chars"],
        }
        self.info["footnotes"] = {
            "noteref_count": len(noteref_targets),
            "unique_noteref_targets": len(noteref_set),
            "endnote_anchor_count": len(endnote_ids),
            "missing_endnote_targets": missing_endnotes,
            "orphan_endnotes": orphan_endnotes,
        }
        self.info["content_scan"] = {
            "boilerplate_hits": totals["boilerplate_hits"],
            "beta_code_files": totals["beta_code_files"],
            "escaped_lang_tag_files": totals["escaped_lang_tag_files"],
            "literal_footnote_marker_files": totals["literal_footnote_marker_files"],
            "empty_bracket_noise_files": totals["empty_bracket_noise_files"],
            "missing_chapter_initialization_files": totals["missing_chapter_initialization_files"],
            "noteref_without_class": totals["noteref_without_class"],
            "repeated_phrase_count": totals["repeated_phrase_count"],
            # Extended checks
            "unprocessed_ages_marker_files": totals["unprocessed_ages_marker_files"],
            "page_reference_split_files": totals["page_reference_split_files"],
            "chapter_heading_in_paragraph_files": totals["chapter_heading_in_paragraph_files"],
            "overlong_heading_body_files": totals["overlong_heading_body_files"],
            "fragmented_greek_span_run_files": totals["fragmented_greek_span_run_files"],
            "glued_ordinal_files": totals["glued_ordinal_files"],
            "structural_bold_leak_files": totals["structural_bold_leak_files"],
            "repeated_structural_marker_files": totals["repeated_structural_marker_files"],
            "scholastic_bold_leak_files": totals["scholastic_bold_leak_files"],
            "inline_scholastic_label_files": totals["inline_scholastic_label_files"],
            "trailing_scholastic_label_files": totals["trailing_scholastic_label_files"],
            "digression_not_h3_files": totals["digression_not_h3_files"],
            "spaced_caps_files": totals["spaced_caps_files"],
            "lowercase_paragraph_start_files": totals["lowercase_paragraph_start_files"],
            "noteref_leading_space_files": totals["noteref_leading_space_files"],
            "greek_span_legacy_accent_files": totals["greek_span_legacy_accent_files"],
            "i_will_mangle_files": totals["i_will_mangle_files"],
            "samples": samples,
        }

        if totals["greek_untagged_chars"]:
            self.warn("untagged_greek", "Greek characters appear outside lang='el' context", chars=totals["greek_untagged_chars"])
        if totals["hebrew_untagged_chars"]:
            self.warn("untagged_hebrew", "Hebrew characters appear outside lang='he' context", chars=totals["hebrew_untagged_chars"])
        if totals["boilerplate_hits"]:
            self.warn("boilerplate_residue", "AGES boilerplate text appears in XHTML", hits=totals["boilerplate_hits"])
        if totals["beta_code_files"]:
            self.warn("possible_beta_code_residue", "Possible Beta Code residue detected", files=totals["beta_code_files"])
        if totals["escaped_lang_tag_files"]:
            self.warn("escaped_lang_tags", "Escaped language span markup appears in XHTML text", files=totals["escaped_lang_tag_files"])
        if totals["literal_footnote_marker_files"]:
            self.error("literal_footnote_markers", "Literal fN footnote markers appear in rendered text", files=totals["literal_footnote_marker_files"])
        if totals["empty_bracket_noise_files"]:
            self.error("empty_bracket_noise", "Empty bracket residue appears in rendered text", files=totals["empty_bracket_noise_files"])
        if totals["noteref_without_class"]:
            self.error("noteref_without_spacing_class", "Some noteref links lack the spacing class", count=totals["noteref_without_class"])
        if repeated:
            self.warn("repeated_phrases", "Potential repeated phrases detected", count=len(repeated))
        if missing_endnotes:
            self.error("noteref_targets_missing", "Some noteref targets do not have matching endnote anchors", examples=missing_endnotes)
        if orphan_endnotes:
            self.warn("orphan_endnotes", "Some endnote anchors have no matching noteref", examples=orphan_endnotes)

    def check_nav_links(self, zf: zipfile.ZipFile) -> None:
        link_count = 0
        missing: list[dict[str, str]] = []
        for nav_path in self.nav_files:
            if nav_path not in self.files:
                continue
            try:
                root = parse_xml(zf.read(nav_path))
            except etree.XMLSyntaxError:
                continue
            for el in root.xpath(".//xhtml:a[@href]", namespaces=NS):
                href = el.get("href", "")
                if href.startswith(("http:", "https:", "mailto:")):
                    continue
                link_count += 1
                target = resolve_href(nav_path, href)
                target_file, _frag = urldefrag(target)
                if target_file not in self.files:
                    missing.append({"nav": nav_path, "href": href, "target": target_file})
        self.info["nav_link_count"] = link_count
        if missing:
            self.error("nav_link_missing", "NAV contains links to missing files", examples=missing[:25], count=len(missing))

    def check_apple_options(self) -> None:
        expected = "META-INF/com.apple.ibooks.display-options.xml"
        if expected not in self.files:
            self.warn("missing_apple_options", "Missing Apple Books display-options file")
            return
        self.info["apple_options"] = expected

    def result(self) -> dict[str, Any]:
        return {
            "epub": str(self.epub_path),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "fail" if self.errors else ("warn" if self.warnings else "pass"),
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info,
        }


def parse_xml(data: bytes) -> etree._Element:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    return etree.fromstring(data, parser=parser)


def clean_text(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text or "").strip()


def html_to_text(raw: str) -> str:
    no_tags = HTML_TAG_RE.sub(" ", raw)
    return clean_text(no_tags)


def norm_join(base_dir: str, href: str) -> str:
    href = unquote(href)
    joined = posixpath.normpath(posixpath.join(base_dir, href)) if base_dir else posixpath.normpath(href)
    return joined.lstrip("./")


def resolve_href(source_path: str, href: str) -> str:
    href = unquote(href)
    href_no_query = href.split("?", 1)[0]
    if href_no_query.startswith("#"):
        return source_path + href_no_query
    base = posixpath.dirname(source_path)
    target, frag = urldefrag(href_no_query)
    resolved = norm_join(base, target)
    return resolved + (f"#{frag}" if frag else "")


def attr(el: etree._Element, name: str) -> str | None:
    if name == "epub:type":
        return el.get(f"{{{NS['epub']}}}type") or el.get("epub:type")
    return el.get(name)


def add_sample(samples: list[dict[str, Any]], file_path: str, text: str, **data: Any) -> None:
    if len(samples) >= 10:
        return
    samples.append({"file": file_path, "text": clean_text(str(text))[:220], **data})


def inspect_language_tagging(root: etree._Element, path: str, samples: dict[str, list[dict[str, Any]]]) -> Counter:
    stats = Counter()
    file_has_untagged_greek = False
    file_has_untagged_hebrew = False

    def visit(el: etree._Element, inherited_lang: str | None, inherited_dir: str | None) -> None:
        nonlocal file_has_untagged_greek, file_has_untagged_hebrew

        lang = el.get("lang") or el.get("{http://www.w3.org/XML/1998/namespace}lang") or inherited_lang
        direction = el.get("dir") or inherited_dir

        if el.text:
            check_text(el.text, lang, direction)
        for child in el:
            visit(child, lang, direction)
            if child.tail:
                check_text(child.tail, lang, direction)

    def check_text(text: str, lang: str | None, direction: str | None) -> None:
        nonlocal file_has_untagged_greek, file_has_untagged_hebrew
        greek_count = len(GREEK_RE.findall(text))
        hebrew_count = len(HEBREW_RE.findall(text))
        stats["greek_chars"] += greek_count
        stats["hebrew_chars"] += hebrew_count
        if greek_count and lang != "el":
            stats["greek_untagged_chars"] += greek_count
            file_has_untagged_greek = True
            add_sample(samples["untagged_greek"], path, text)
        if hebrew_count and not (lang == "he" and direction == "rtl"):
            stats["hebrew_untagged_chars"] += hebrew_count
            file_has_untagged_hebrew = True
            add_sample(samples["untagged_hebrew"], path, text)

    visit(root, None, None)
    if file_has_untagged_greek:
        stats["files_with_untagged_greek"] += 1
    if file_has_untagged_hebrew:
        stats["files_with_untagged_hebrew"] += 1
    return stats


def find_repeated_phrases(text: str, ngram_size: int = 8, max_results: int = 10) -> list[dict[str, Any]]:
    words = [w.lower() for w in WORD_RE.findall(text)]
    repeated: Counter[str] = Counter()

    i = 0
    while i + (2 * ngram_size) <= len(words):
        first = words[i : i + ngram_size]
        second = words[i + ngram_size : i + (2 * ngram_size)]
        if first == second:
            repeated[" ".join(first)] += 1
            i += ngram_size
        else:
            i += 1

    return [
        {"phrase": phrase, "count": count}
        for phrase, count in repeated.most_common(max_results)
    ]


def write_reports(result: dict[str, Any], out_dir: Path, stem: str) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{stem}_audit.json"
    md_path = out_dir / f"{stem}_audit.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    return json_path, md_path


def infer_output_dir(epub_path: Path) -> Path:
    parts = epub_path.parts
    for i, part in enumerate(parts):
        if part == "volumes" and i + 3 < len(parts):
            vol_dir = Path(*parts[: i + 2])
            if parts[i + 2] == "output":
                return vol_dir / "bugs_fixes"
    return Path("qa/reports")


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# EPUB Audit: {Path(result['epub']).name}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- Errors: {result['error_count']}",
        f"- Warnings: {result['warning_count']}",
        "",
    ]

    info = result.get("info", {})
    lines.extend([
        "## Summary",
        "",
        f"- OPF: {info.get('opf_path', 'not found')}",
        f"- OPF version: {info.get('opf_version', 'unknown')}",
        f"- Files: {info.get('file_count', 0)}",
        f"- Manifest items: {info.get('manifest_count', 0)}",
        f"- Spine items: {info.get('spine_count', 0)}",
        f"- XHTML files: {info.get('xhtml_count', 0)}",
        f"- Embedded fonts: {info.get('font_count', 0)}",
        f"- NAV links: {info.get('nav_link_count', 0)}",
        "",
    ])

    lang = info.get("language", {})
    footnotes = info.get("footnotes", {})
    scan = info.get("content_scan", {})
    lines.extend([
        "## Content Checks",
        "",
        f"- Greek chars: {lang.get('greek_chars', 0)}",
        f"- Untagged Greek chars: {lang.get('greek_untagged_chars', 0)}",
        f"- Hebrew chars: {lang.get('hebrew_chars', 0)}",
        f"- Untagged Hebrew chars: {lang.get('hebrew_untagged_chars', 0)}",
        f"- Noteref links: {footnotes.get('noteref_count', 0)}",
        f"- Endnote anchors: {footnotes.get('endnote_anchor_count', 0)}",
        f"- Boilerplate hits: {scan.get('boilerplate_hits', 0)}",
        f"- Possible Beta Code files: {scan.get('beta_code_files', 0)}",
        f"- Escaped language-tag files: {scan.get('escaped_lang_tag_files', 0)}",
        f"- Empty bracket noise files: {scan.get('empty_bracket_noise_files', 0)}",
        f"- Missing chapter initialization files: {scan.get('missing_chapter_initialization_files', 0)}",
        f"- Repeated phrase hits: {scan.get('repeated_phrase_count', 0)}",
        "",
    ])

    if result["errors"]:
        lines.extend(["## Errors", ""])
        for item in result["errors"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    if result["warnings"]:
        lines.extend(["## Warnings", ""])
        for item in result["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    samples = scan.get("samples", {})
    sample_lines = []
    for name, entries in samples.items():
        if not entries:
            continue
        sample_lines.extend([f"### {name}", ""])
        for entry in entries[:5]:
            text = entry.get("text", "")
            file_path = entry.get("file", "")
            sample_lines.append(f"- `{file_path}`: {text}")
        sample_lines.append("")
    if sample_lines:
        lines.extend(["## Samples", "", *sample_lines])

    return "\n".join(lines).rstrip() + "\n"


def render_bug_log_section(result: dict[str, Any], json_path: Path, md_path: Path) -> str:
    info = result.get("info", {})
    lang = info.get("language", {})
    footnotes = info.get("footnotes", {})
    scan = info.get("content_scan", {})

    lines = [
        "<!-- AUTO_AUDIT_START -->",
        "## Automated EPUB Audit",
        "",
        f"**Last run:** {result['generated_at']}",
        f"**EPUB:** `{result['epub']}`",
        f"**Status:** {result['status'].upper()} ({result['error_count']} errors, {result['warning_count']} warnings)",
        "",
        "Reports:",
        f"- `{json_path.name}`",
        f"- `{md_path.name}`",
        "",
        "| Check | Result |",
        "|-------|--------|",
        f"| OPF version | {info.get('opf_version', 'unknown')} |",
        f"| XHTML files | {info.get('xhtml_count', 0)} |",
        f"| Spine items | {info.get('spine_count', 0)} |",
        f"| Embedded fonts | {info.get('font_count', 0)} |",
        f"| NAV links | {info.get('nav_link_count', 0)} |",
        f"| Greek chars / untagged | {lang.get('greek_chars', 0)} / {lang.get('greek_untagged_chars', 0)} |",
        f"| Hebrew chars / untagged | {lang.get('hebrew_chars', 0)} / {lang.get('hebrew_untagged_chars', 0)} |",
        f"| Noteref links / endnote anchors | {footnotes.get('noteref_count', 0)} / {footnotes.get('endnote_anchor_count', 0)} |",
        f"| AGES boilerplate hits | {scan.get('boilerplate_hits', 0)} |",
        f"| Possible Beta Code files | {scan.get('beta_code_files', 0)} |",
        f"| Escaped language-tag files | {scan.get('escaped_lang_tag_files', 0)} |",
        f"| Empty bracket noise files | {scan.get('empty_bracket_noise_files', 0)} |",
        f"| Repeated phrase hits | {scan.get('repeated_phrase_count', 0)} |",
        "",
    ]

    if result["warnings"]:
        lines.extend(["Warnings requiring triage:", ""])
        for item in result["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    if result["errors"]:
        lines.extend(["Errors requiring correction:", ""])
        for item in result["errors"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")

    lines.extend([
        "**Status note:** Automated audit findings are not user validation. Keep related fixes as `IMPLEMENTED (AWAITING VALIDATION)` until explicitly approved.",
        "<!-- AUTO_AUDIT_END -->",
        "",
    ])
    return "\n".join(lines)


def update_bug_log(result: dict[str, Any], json_path: Path, md_path: Path) -> Path | None:
    out_dir = md_path.parent
    bug_log = out_dir / "BUGS_AND_FIXES.md"
    if not bug_log.exists():
        return None

    content = bug_log.read_text(encoding="utf-8")
    section = render_bug_log_section(result, json_path, md_path).rstrip()
    pattern = re.compile(r"\n?<!-- AUTO_AUDIT_START -->.*?<!-- AUTO_AUDIT_END -->\n?", re.S)

    if pattern.search(content):
        updated = pattern.sub("\n\n" + section + "\n", content).rstrip() + "\n"
    else:
        updated = content.rstrip() + "\n\n---\n\n" + section + "\n"

    bug_log.write_text(updated, encoding="utf-8")
    return bug_log


def infer_report_stem(epub_path: Path) -> str:
    match = re.search(r"volume_(\d+)\.epub$", epub_path.name)
    if match:
        return f"volume_{match.group(1)}"
    return epub_path.stem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a generated Owen EPUB3 file")
    parser.add_argument("epub", type=Path, help="Path to .epub file")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Directory for JSON/Markdown reports; defaults to the volume's bugs_fixes directory when possible",
    )
    parser.add_argument("--no-bug-log", action="store_true", help="Do not update BUGS_AND_FIXES.md")
    parser.add_argument("--fail-on-warning", action="store_true", help="Exit non-zero when warnings are present")
    args = parser.parse_args(argv)

    audit = Audit(args.epub)
    result = audit.run()
    out_dir = args.out_dir or infer_output_dir(args.epub)
    json_path, md_path = write_reports(result, out_dir, infer_report_stem(args.epub))
    bug_log = None if args.no_bug_log else update_bug_log(result, json_path, md_path)

    print(render_markdown(result))
    print(f"Reports written:\n- {json_path}\n- {md_path}")
    if bug_log:
        print(f"Bug log updated:\n- {bug_log}")

    if result["error_count"]:
        return 1
    if args.fail_on_warning and result["warning_count"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())