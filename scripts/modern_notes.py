#!/usr/bin/env python3
"""Manifest-driven modern translation and reference notes for Owen volumes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from html import escape as html_escape, unescape as html_unescape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


LATIN_SIGNAL_WORDS = {
    "ad", "aut", "autem", "cap", "cum", "de", "dei", "deus", "enim",
    "erat", "esse", "est", "et", "hoc", "id", "igitur", "in", "ipse",
    "ipsum", "lib", "nec", "non", "per", "quae", "quam", "qui", "quia",
    "quid", "quo", "quod", "sed", "sine", "sunt", "super", "ut", "vel",
}

FOREIGN_RE = re.compile(
    r"[\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]|"
    r"\b(?:lib|cap|epist|orat|homil|tract|dist|quaest|art)\.\s*\w+",
    re.I,
)

TAG_RE = re.compile(r"<[^>]+>")
BARE_LOCATION_RE = re.compile(
    r"^\(?\s*(?:(?:lib|cap|chap|tract|epist|ep|homil|orat|serm)\."
    r"\s*(?:[0-9IVXLCDM]+|ult\.?)(?:\s*(?:[:,;.]|ad)?\s*)?)+\)?$",
    re.I,
)


def _plain(text: str) -> str:
    text = re.sub(r"\[\[(?:CHAPTER|SUMMARY|BLOCKQUOTE|PART)\]\]", " ", text)
    text = re.sub(r"\[f\d+\]", " ", text)
    text = TAG_RE.sub(" ", text)
    text = html_unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+\b", _plain(text)))


def _looks_latin(text: str) -> bool:
    words = re.findall(r"\b[A-Za-z][A-Za-z.'’-]*\b", text)
    if len(words) < 5:
        return False
    hits = [w for w in words if w.lower().strip(".'’-") in LATIN_SIGNAL_WORDS]
    strong_hits = [
        w for w in hits
        if w.lower().strip(".'’-") not in {"in", "ad", "id"}
    ]
    return bool(strong_hits) and len(hits) >= 3 and (len(hits) / len(words)) >= 0.10


def note_type(note_html: str) -> str:
    """Return translation when note text contains a translation payload."""
    if re.search(r"(?:<strong>\s*)?(?:Modern\s+)?Translation(?:\s+Summary)?\s*:", note_html, re.I):
        return "translation"
    if not re.search(r"(?:<strong>\s*)?(?:Modern Citation|Editorial Note)\s*:", note_html, re.I):
        return "translation"
    return "citation"


def citation_only(note_html: str) -> str | None:
    """Extract a citation-only note from a combined citation+translation entry."""
    match = re.search(
        r"((?:<strong>\s*)?Modern Citation(?:\s*</strong>)?\s*:.*?)(?:<br\s*/?>\s*<strong>\s*(?:Modern\s+)?Translation|\Z)",
        note_html,
        re.I | re.S,
    )
    if not match:
        return None
    citation = match.group(1).strip()
    if re.search(r"\b(?:Latin|Greek|Hebrew|term|phrase)\b", _plain(citation), re.I):
        return None
    if not re.search(r"<em>[^<]+</em>|\b(?:Book|Chapter|Homily|Epistle|Oration|line|ST|Sentences|NPNF|ANF|PG|PL)\b", citation):
        return None
    return citation


def sanitize_note_html(note_html: str) -> str:
    """Remove vague legacy source claims from reader-facing modern notes."""
    note_html = re.sub(
        r"\s*\((?:Unknown|unknown),\s*<em>Unknown Work</em>,\s*Unknown Location\)",
        "",
        note_html,
    )
    note_html = re.sub(
        r"\s*\((?:Unknown|unknown)(?:\s+Work|\s+Location)?\)",
        "",
        note_html,
    )
    return note_html


def _anchorable_citation_phrase(phrase: str) -> bool:
    """Reject fragment-only citation keys; contextual resolver may still add them."""
    plain = _plain(phrase)
    if re.match(r"^[1-3]\s+Epist\.\s*\d+:\d+$", plain, re.I):
        return False
    if BARE_LOCATION_RE.match(plain):
        return False
    if _word_count(plain) >= 4:
        return True
    return bool(re.search(r"\b[A-Z][a-z]{3,}\.?\b|\bDe\s+[A-Z][A-Za-z]+\b", plain))


def _owen_translation_nearby(current: str, following: str) -> bool:
    tail = _plain((current[-180:] + " " + following[:900]).strip())
    after_quote = re.split(r'["”]\s*', tail, maxsplit=1)
    if len(after_quote) > 1:
        tail = after_quote[-1].strip()
    return bool(re.match(
        r'(?i)^(?:—|-)\s*["“][A-Z]|^(?:that is|that is to say|which is|namely|or,? that is|that means)\b',
        tail,
    ))


def _candidate_key(scope: str, chapter: str, exact: str, note: str | None = None) -> str:
    seed = f"{scope}|{chapter}|{_plain(exact).lower()}|{_plain(note or '').lower()}"
    import hashlib
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]


def _chapter_paragraphs(chapter: dict[str, Any]) -> list[str]:
    return [p.strip() for p in chapter.get("raw_text", "").split("\n\n") if p.strip()]


def _find_translation_db_items(chapter: dict[str, Any], seen: set[str]) -> list[dict[str, Any]]:
    from scripts.translation_db import BODY_TRANSLATIONS
    from scripts.audit_text_integrity import normalized_word_string

    title = chapter.get("title", "")
    raw_text = chapter.get("raw_text", "")
    norm_raw = normalized_word_string(raw_text)
    paragraphs = _chapter_paragraphs(chapter)
    items: list[dict[str, Any]] = []

    for phrase, note_html in sorted(BODY_TRANSLATIONS.items(), key=lambda kv: len(kv[0]), reverse=True):
        norm_phrase = normalized_word_string(phrase)
        if not norm_phrase or norm_phrase not in norm_raw:
            continue
        if phrase in seen:
            continue

        kind = note_type(note_html)
        note_html = sanitize_note_html(note_html)
        words = _word_count(phrase)
        if kind == "translation" and words < 5:
            continue
        if kind == "citation" and not _anchorable_citation_phrase(phrase):
            continue

        para_index = -1
        owen_translated = False
        for idx, para in enumerate(paragraphs):
            if norm_phrase in normalized_word_string(para):
                para_index = idx
                following = "\n\n".join(paragraphs[idx + 1:idx + 3])
                owen_translated = _owen_translation_nearby(para, following)
                break

        modern_reference = citation_only(note_html)
        if kind == "translation" and owen_translated:
            if modern_reference:
                action = "citation_popup"
                payload = modern_reference
                reason = "Owen appears to translate or paraphrase this passage nearby; suppress duplicate translation."
            else:
                action = "none"
                payload = None
                reason = "Owen appears to translate or paraphrase this passage nearby and no high-confidence modern reference was isolated."
        elif kind == "translation":
            action = "translation_popup"
            payload = note_html
            reason = "Curated quote-level modern translation entry."
        else:
            action = "citation_popup"
            payload = note_html
            reason = "Curated high-confidence modern reference entry."

        item = {
            "id": _candidate_key("body", title, phrase, payload),
            "scope": "body",
            "chapter": title,
            "cid": chapter.get("cid"),
            "paragraph_index": para_index,
            "action": action,
            "confidence": "high" if action != "none" else "medium",
            "source": "BODY_TRANSLATIONS",
            "exact_text": phrase,
            "owen_translated_or_paraphrased": owen_translated,
            "modern_reference": modern_reference if action == "citation_popup" else None,
            "translation_text": payload if action == "translation_popup" else None,
            "note_html": payload,
            "reason": reason,
            "word_count": words,
        }
        items.append(item)
        seen.add(phrase)
    return items


def _find_patristic_items(chapter: dict[str, Any], used_texts: set[str]) -> list[dict[str, Any]]:
    from scripts.patristic_refs import (
        PATRISTIC_CITATION_RE,
        SELF_REF_PATTERNS,
        _citation_tail_continues_source_title,
        _strip_tags,
        build_citation_note,
    )

    title = chapter.get("title", "")
    raw_text = chapter.get("raw_text", "")
    items: list[dict[str, Any]] = []
    for match in PATRISTIC_CITATION_RE.finditer(raw_text):
        cite = match.group(0)
        if len(cite.strip()) < 6:
            continue
        if cite in used_texts:
            continue
        if _citation_tail_continues_source_title(raw_text, match.end()):
            continue
        ctx_start = max(0, match.start() - 220)
        ctx_end = min(len(raw_text), match.end() + 120)
        plain_ctx_before = _strip_tags(raw_text[ctx_start:match.start()])
        plain_ctx_after = _strip_tags(raw_text[match.end():ctx_end])
        if SELF_REF_PATTERNS.search(plain_ctx_before):
            continue
        note = build_citation_note(cite, plain_ctx_before + " | " + plain_ctx_after)
        if note is None:
            continue
        items.append({
            "id": _candidate_key("body-citation", title, cite, note),
            "scope": "body",
            "chapter": title,
            "cid": chapter.get("cid"),
            "paragraph_index": None,
            "action": "citation_popup",
            "confidence": "high",
            "source": "patristic_refs",
            "exact_text": cite,
            "owen_translated_or_paraphrased": False,
            "modern_reference": note,
            "translation_text": None,
            "note_html": note,
            "reason": "Resolved by author + work + location reference map.",
            "word_count": _word_count(cite),
        })
        used_texts.add(cite)
    return items


def _find_footnote_items(vol_num: int, intermediate: dict[str, Any]) -> list[dict[str, Any]]:
    from scripts.translation_db import FOOTNOTE_TRANSLATIONS
    from scripts.patristic_refs import PATRISTIC_CITATION_RE, build_citation_note

    items: list[dict[str, Any]] = []
    for raw_num, data in intermediate.get("footnotes", {}).items():
        fnum = int(raw_num)
        text = data.get("text", "")
        key = f"v{vol_num}_fn{fnum}"
        curated = FOOTNOTE_TRANSLATIONS.get(key)
        note_html = sanitize_note_html(curated) if curated else None
        reason = "Curated existing-footnote enrichment."
        confidence = "high"

        if note_html is None:
            for match in PATRISTIC_CITATION_RE.finditer(text):
                ctx_start = max(0, match.start() - 220)
                note_html = build_citation_note(match.group(0), text[ctx_start:match.start()])
                if note_html:
                    reason = "Existing footnote contains a high-confidence archaic reference."
                    break

        needs_review = bool(FOREIGN_RE.search(text) or _looks_latin(_plain(text)))
        if note_html:
            items.append({
                "id": _candidate_key("footnote", f"fn{fnum}", text, note_html),
                "scope": "footnote",
                "footnote": fnum,
                "action": "enrich_existing_footnote",
                "confidence": confidence,
                "source": "FOOTNOTE_TRANSLATIONS" if curated else "patristic_refs",
                "exact_text": text,
                "owen_translated_or_paraphrased": False,
                "modern_reference": citation_only(note_html) or note_html,
                "translation_text": note_html if note_type(note_html) == "translation" else None,
                "note_html": note_html,
                "reason": reason,
                "word_count": _word_count(text),
            })
        elif needs_review:
            items.append({
                "id": _candidate_key("footnote-review", f"fn{fnum}", text),
                "scope": "footnote",
                "footnote": fnum,
                "action": "none",
                "confidence": "low",
                "source": "heuristic",
                "exact_text": text,
                "owen_translated_or_paraphrased": False,
                "modern_reference": None,
                "translation_text": None,
                "note_html": None,
                "reason": "Existing footnote appears to contain foreign text or an archaic reference, but no high-confidence enrichment is available.",
                "word_count": _word_count(text),
            })
    return items


def generate_manifest(vol_num: int, intermediate: dict[str, Any]) -> dict[str, Any]:
    seen_translation_phrases: set[str] = set()
    seen_patristic_texts: set[str] = set()
    items: list[dict[str, Any]] = []
    for chapter in intermediate.get("chapters", []):
        if chapter.get("is_endnotes"):
            continue
        body_items = _find_translation_db_items(chapter, seen_translation_phrases)
        items.extend(body_items)
        seen_patristic_texts.update(i["exact_text"] for i in body_items if i["action"] != "none")
        items.extend(_find_patristic_items(chapter, seen_patristic_texts))
    items.extend(_find_footnote_items(vol_num, intermediate))

    summary = {
        "total_items": len(items),
        "body_translation_popups": sum(1 for i in items if i["action"] == "translation_popup"),
        "body_citation_popups": sum(1 for i in items if i["action"] == "citation_popup"),
        "footnote_enrichments": sum(1 for i in items if i["action"] == "enrich_existing_footnote"),
        "unresolved_modern_references": sum(1 for i in items if i["scope"] == "body" and i["action"] == "none"),
        "untranslated_substantial_foreign_passages": sum(
            1 for i in items
            if i["scope"] == "body" and i["action"] == "none" and i.get("word_count", 0) >= 5
        ),
        "unenriched_legacy_footnotes": sum(1 for i in items if i["scope"] == "footnote" and i["action"] == "none"),
    }
    return {
        "volume": vol_num,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "schema_version": 1,
        "summary": summary,
        "items": items,
    }


def footnote_enrichment_map(manifest: dict[str, Any]) -> dict[int, str]:
    return {
        int(item["footnote"]): item["note_html"]
        for item in manifest.get("items", [])
        if item.get("scope") == "footnote"
        and item.get("action") == "enrich_existing_footnote"
        and item.get("confidence") == "high"
        and item.get("note_html")
    }


def _clean_and_map(orig_str: str) -> tuple[str, list[int], list[int]]:
    stripped_chars: list[str] = []
    map_to_orig_start: list[int] = []
    map_to_orig_end: list[int] = []
    i = 0
    while i < len(orig_str):
        if orig_str[i] == "<":
            while i < len(orig_str) and orig_str[i] != ">":
                i += 1
            i += 1
        elif orig_str[i] == "&":
            j = i + 1
            while j < len(orig_str) and orig_str[j] != ";" and (j - i) < 12:
                j += 1
            if j < len(orig_str) and orig_str[j] == ";":
                decoded = html_unescape(orig_str[i:j + 1])
                for char in decoded:
                    stripped_chars.append(char)
                    map_to_orig_start.append(i)
                    map_to_orig_end.append(j + 1)
                i = j + 1
            else:
                stripped_chars.append(orig_str[i])
                map_to_orig_start.append(i)
                map_to_orig_end.append(i + 1)
                i += 1
        else:
            stripped_chars.append(orig_str[i])
            map_to_orig_start.append(i)
            map_to_orig_end.append(i + 1)
            i += 1
    return "".join(stripped_chars), map_to_orig_start, map_to_orig_end


def _quote_agnostic_regex(text: str) -> str:
    words = text.split()
    escaped_words = []
    for word in words:
        escaped = re.escape(word)
        escaped = escaped.replace(r"\'", "'").replace("'", r"['’‘]")
        escaped = escaped.replace(r'\"', '"').replace('"', r'["“”]')
        escaped_words.append(escaped)
    return r"\s+".join(escaped_words)


def apply_modern_body_notes(
    body_html: str,
    chapter_title: str,
    cid: str,
    manifest: dict[str, Any],
    note_counter: int,
) -> tuple[str, list[dict[str, Any]], int]:
    """Insert high-confidence manifest body markers into rendered chapter HTML."""
    chapter_items = [
        item for item in manifest.get("items", [])
        if item.get("scope") == "body"
        and item.get("chapter") == chapter_title
        and item.get("action") in {"translation_popup", "citation_popup"}
        and item.get("confidence") == "high"
        and item.get("note_html")
        and item.get("exact_text")
    ]
    chapter_items.sort(key=lambda item: len(item["exact_text"]), reverse=True)

    notes: list[dict[str, Any]] = []
    clean_text, map_start, map_end = _clean_and_map(body_html)
    used_clean_spans: list[tuple[int, int]] = []
    selected: list[dict[str, Any]] = []

    for item in chapter_items:
        exact = item["exact_text"]
        if not exact.strip():
            continue
        pattern = re.compile(_quote_agnostic_regex(exact), re.I)
        match = pattern.search(clean_text)
        if not match:
            continue
        clean_start = match.start()
        clean_end = match.end()
        if any(not (clean_end <= start or clean_start >= end) for start, end in used_clean_spans):
            continue

        used_clean_spans.append((clean_start, clean_end))
        orig_start = map_start[clean_start]
        orig_end = map_end[clean_end - 1]
        punc_match = re.match(
            r'^((?:</(?!p\b|li\b|ul\b|ol\b|div\b|blockquote\b|h[1-6]\b|section\b|aside\b|body\b|html\b|dt\b|dd\b|table\b|tr\b|td\b|th\b)[a-zA-Z]+>)*)([\.,\?!:;\'"“”’)\]]*)',
            body_html[orig_end:],
        )
        trailing_tags = punc_match.group(1) if punc_match else ""
        trailing_punc = punc_match.group(2) if punc_match else ""
        insert_at = orig_end + len(trailing_tags) + len(trailing_punc)
        selected.append({
            "item": item,
            "insert_at": insert_at,
        })

    selected.sort(key=lambda entry: entry["insert_at"])
    replacements: list[tuple[int, str]] = []
    for entry in selected:
        item = entry["item"]
        note_counter += 1
        note_type_value = "translation" if item["action"] == "translation_popup" else "citation"
        note_class = "noteref-trans" if note_type_value == "translation" else "noteref-citation"
        symbol = "†" if note_type_value == "translation" else "◇"
        fn_id = f"fnmodern_{cid}_{note_counter}"
        fn_link = (
            f'<a class="noteref {note_class}" epub:type="noteref" '
            f'role="doc-noteref" href="endnotes.xhtml#{fn_id}"><sup>{symbol}</sup></a>'
        )
        replacements.append((entry["insert_at"], fn_link))
        notes.append({
            "id": fn_id,
            "num": note_counter,
            "phrase": item["exact_text"],
            "translation": item["note_html"],
            "type": note_type_value,
            "manifest_id": item["id"],
        })

    for insert_at, fn_link in sorted(replacements, key=lambda entry: entry[0], reverse=True):
        body_html = body_html[:insert_at] + fn_link + body_html[insert_at:]

    return body_html, notes, note_counter


def write_manifest_reports(manifest: dict[str, Any], report_dir: Path) -> tuple[Path, Path]:
    vol_num = manifest["volume"]
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / f"volume_{vol_num}_modern_notes_manifest.json"
    md_path = report_dir / f"volume_{vol_num}_modern_notes_manifest.md"
    json_path.unlink(missing_ok=True)
    md_path.unlink(missing_ok=True)
    json_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = manifest["summary"]
    lines = [
        f"# Volume {vol_num} Modern Notes Manifest",
        "",
        f"- Generated: {manifest['generated_at']}",
        f"- Total items: {summary['total_items']}",
        f"- Body translation popups: {summary['body_translation_popups']}",
        f"- Body reference popups: {summary['body_citation_popups']}",
        f"- Existing footnote enrichments: {summary['footnote_enrichments']}",
        f"- Unresolved modern references: {summary['unresolved_modern_references']}",
        f"- Untranslated substantial foreign passages: {summary['untranslated_substantial_foreign_passages']}",
        f"- Unenriched legacy footnotes: {summary['unenriched_legacy_footnotes']}",
        "",
        "## Items",
        "",
    ]
    for item in manifest["items"]:
        label = item.get("chapter") or f"fn{item.get('footnote')}"
        lines.extend([
            f"### {item['action']} — {label}",
            "",
            f"- ID: `{item['id']}`",
            f"- Confidence: {item['confidence']}",
            f"- Source: {item['source']}",
            f"- Owen translated/paraphrased: {'yes' if item.get('owen_translated_or_paraphrased') else 'no'}",
            f"- Reason: {item['reason']}",
            "",
            "```text",
            _plain(item.get("exact_text", ""))[:900],
            "```",
            "",
        ])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def latest_manifest(vol_num: int) -> dict[str, Any] | None:
    reports = sorted((ROOT / "volumes" / f"v{vol_num}" / "reports").glob("*/volume_*_modern_notes_manifest.json"))
    if not reports:
        return None
    return json.loads(reports[-1].read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("volume", type=int)
    args = parser.parse_args()
    json_path = ROOT / "volumes" / f"v{args.volume}" / "intermediate" / f"volume_{args.volume}.json"
    intermediate = json.loads(json_path.read_text(encoding="utf-8"))
    manifest = generate_manifest(args.volume, intermediate)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_modern_notes")
    out_dir = ROOT / "volumes" / f"v{args.volume}" / "reports" / stamp
    paths = write_manifest_reports(manifest, out_dir)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
