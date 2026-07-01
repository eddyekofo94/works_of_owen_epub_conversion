#!/usr/bin/env python3
"""Generate a volume-scoped Latin translation/citation research report."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_text_integrity import normalized_word_string
from scripts.translation_db import BODY_TRANSLATIONS

LATIN_SIGNAL_WORDS = {
    "ad", "aut", "autem", "cum", "dei", "deus", "enim", "erat", "esse",
    "est", "et", "hoc", "id", "igitur", "in", "ipse", "ipsum", "lib",
    "nec", "non", "per", "quae", "quam", "qui", "quia", "quid", "quo",
    "quod", "sed", "sine", "sunt", "super", "ut", "vel",
}


def _entry_type(note: str) -> str:
    if re.search(r'(?:<strong>\s*)?Translation(?:\s+Summary)?\s*:', note, re.I):
        return "translation"
    if re.search(r'(?:<strong>\s*)?(?:Modern Citation|Editorial Note)\s*:', note, re.I):
        return "citation"
    return "translation"


TRANSLATION_KEYS = {
    normalized_word_string(k): k
    for k, v in BODY_TRANSLATIONS.items()
    if _entry_type(v) == "translation"
}
CITATION_KEYS = {
    normalized_word_string(k): k
    for k, v in BODY_TRANSLATIONS.items()
    if _entry_type(v) == "citation"
}


def _plain(text: str) -> str:
    text = re.sub(r"\[\[(?:CHAPTER|SUMMARY|BLOCKQUOTE)\]\]", " ", text)
    text = re.sub(r"\[f\d+\]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _latin_score(text: str) -> tuple[int, int, float]:
    words = re.findall(r"\b[A-Za-z][A-Za-z.'’-]*\b", text)
    latin_hits = [w for w in words if w.lower().strip(".'’-") in LATIN_SIGNAL_WORDS]
    ratio = len(latin_hits) / len(words) if words else 0.0
    return len(words), len(latin_hits), ratio


def _looks_latin(text: str) -> bool:
    words, hits, ratio = _latin_score(text)
    if words < 5:
        return False
    if hits >= 4 and ratio >= 0.12:
        return True
    return bool(re.search(r"\b(?:lib|cap|tract|epist|orat|homil)\.\s*\d", text, re.I)) and hits >= 2


def _owen_translation_follows(current: str, following: str) -> bool:
    tail = _plain((current[-120:] + " " + following[:700]).strip())
    after_quote = re.split(r'["”]\s*', tail, maxsplit=1)
    if len(after_quote) > 1:
        tail = after_quote[-1].strip()
    return bool(re.match(
        r'(?i)^(?:—|-)\s*["“][A-Z]|^(?:that is|that is to say|which is|namely|or,? that is)\b',
        tail,
    ))


def _find_known(norm: str, keys: dict[str, str]) -> str | None:
    if not norm:
        return None
    for key_norm, original in keys.items():
        if not key_norm:
            continue
        if key_norm in norm or norm in key_norm:
            return original
    return None


def scan_volume(vol_num: int) -> dict:
    json_path = ROOT / "volumes" / f"v{vol_num}" / "intermediate" / f"volume_{vol_num}.json"
    data = json.loads(json_path.read_text(encoding="utf-8"))
    candidates = []

    for ch in data.get("chapters", []):
        title = ch.get("title", "")
        paragraphs = [p.strip() for p in ch.get("raw_text", "").split("\n\n") if p.strip()]
        for idx, para in enumerate(paragraphs):
            plain = _plain(para)
            if not _looks_latin(plain):
                continue
            norm = normalized_word_string(plain)
            translation_key = _find_known(norm, TRANSLATION_KEYS)
            citation_key = _find_known(norm, CITATION_KEYS)
            following = "\n\n".join(paragraphs[idx + 1:idx + 3])
            owen_translated = _owen_translation_follows(para, following)
            if translation_key:
                status = "curated_translation"
            elif owen_translated:
                status = "owen_translates_nearby"
            else:
                status = "needs_translation_research"
            candidates.append({
                "chapter": title,
                "paragraph_index": idx,
                "status": status,
                "has_curated_translation": bool(translation_key),
                "has_modern_citation": bool(citation_key),
                "curated_translation_key": translation_key,
                "citation_key": citation_key,
                "owen_translation_detected": owen_translated,
                "word_count": _latin_score(plain)[0],
                "latin_signal_count": _latin_score(plain)[1],
                "sample": plain[:700],
            })

    return {
        "volume": vol_num,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "candidate_count": len(candidates),
        "needs_translation_research_count": sum(1 for c in candidates if c["status"] == "needs_translation_research"),
        "owen_translates_nearby_count": sum(1 for c in candidates if c["status"] == "owen_translates_nearby"),
        "curated_translation_count": sum(1 for c in candidates if c["status"] == "curated_translation"),
        "candidates": candidates,
    }


def write_reports(result: dict) -> tuple[Path, Path]:
    vol_num = result["volume"]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_latin_research")
    report_dir = ROOT / "volumes" / f"v{vol_num}" / "reports" / stamp
    report_dir.mkdir(parents=True, exist_ok=True)
    json_path = report_dir / f"volume_{vol_num}_latin_research.json"
    md_path = report_dir / f"volume_{vol_num}_latin_research.md"
    json_path.unlink(missing_ok=True)
    md_path.unlink(missing_ok=True)
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"# Volume {vol_num} Latin Translation Research",
        "",
        f"- Generated: {result['generated_at']}",
        f"- Latin candidates: {result['candidate_count']}",
        f"- Curated translation entries: {result['curated_translation_count']}",
        f"- Owen-translated nearby: {result['owen_translates_nearby_count']}",
        f"- Needs translation research: {result['needs_translation_research_count']}",
        "",
        "## Candidates",
        "",
    ]
    for item in result["candidates"]:
        lines.extend([
            f"### {item['status']} — {item['chapter']} ¶{item['paragraph_index']}",
            "",
            f"- Modern citation known: {'yes' if item['has_modern_citation'] else 'no'}",
            f"- Curated translation known: {'yes' if item['has_curated_translation'] else 'no'}",
            f"- Owen translation detected nearby: {'yes' if item['owen_translation_detected'] else 'no'}",
            "",
            "```text",
            item["sample"],
            "```",
            "",
        ])
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("volume", type=int)
    args = parser.parse_args()
    result = scan_volume(args.volume)
    json_path, md_path = write_reports(result)
    print(json_path)
    print(md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
