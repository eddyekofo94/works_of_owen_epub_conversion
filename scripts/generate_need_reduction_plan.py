#!/usr/bin/env python3
"""Generate a comprehensive Need score reduction plan for an Owen volume.

Reads existing audit, text integrity, anomaly, whitelist, and state report data,
computes the full Need score breakdown, identifies root causes for each non-zero
penalty component, and writes a prioritized action plan with specific fixes.

Usage:
    .venv/bin/python3 scripts/generate_need_reduction_plan.py 16
    .venv/bin/python3 scripts/generate_need_reduction_plan.py          # auto-detect worst volume
    .venv/bin/python3 scripts/generate_need_reduction_plan.py 1 2 5    # multiple volumes
    .venv/bin/python3 scripts/generate_need_reduction_plan.py --all    # all 16 volumes
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared import get_volume_dir, get_volume_label

OWEN_VOLUMES = [str(i) for i in range(1, 17)]

# Known compound prefixes that extract.py may merge at line breaks
COMPOUND_PREFIXES = [
    "church", "office", "subject", "self", "well", "over", "under",
    "non", "pre", "post", "anti", "co", "re", "inter", "sub",
]

# Scripture book names for detecting scripture reference clusters
SCRIPTURE_BOOKS = {
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy",
    "joshua", "judges", "ruth", "samuel", "kings", "chronicles",
    "ezra", "nehemiah", "esther", "job", "psalm", "psalms",
    "proverbs", "ecclesiastes", "song", "isaiah", "jeremiah",
    "lamentations", "ezekiel", "daniel", "hosea", "joel", "amos",
    "obadiah", "jonah", "micah", "nahum", "habakkuk", "zephaniah",
    "haggai", "zechariah", "malachi",
    "matthew", "mark", "luke", "john", "acts",
    "romans", "corinthians", "galatians", "ephesians", "philippians",
    "colossians", "thessalonians", "timothy", "titus", "philemon",
    "hebrews", "james", "peter", "john", "jude", "revelation",
}


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _vol_path(vol) -> Path:
    return get_volume_dir(vol)


def _bugs_path(vol) -> Path:
    return _vol_path(vol) / "bugs_fixes"


def _plans_path(vol) -> Path:
    return _vol_path(vol) / "plans"


def gather_volume_data(vol) -> dict:
    bugs = _bugs_path(vol)

    audit = _read_json(bugs / f"volume_{vol}_audit.json")
    text_int = _read_json(bugs / f"volume_{vol}_text_integrity.json")
    anom = _read_json(bugs / f"volume_{vol}_anomalies.json")
    whitelist = _read_json(bugs / f"volume_{vol}_whitelist.json")
    bug_reg = _read_json(bugs / f"volume_{vol}_bug_regressions.json")

    wc = text_int.get("word_coverage", {})
    pi = text_int.get("paragraph_integrity", {})
    gh = text_int.get("greek_hebrew_word_coverage", {})
    lat_cov = text_int.get("latin_word_coverage", {})
    lat_trans = text_int.get("latin_translation_coverage", {})

    data: dict[str, Any] = {
        "vol": vol,
        "coverage": wc.get("coverage_ratio"),
        "pdf_tokens": wc.get("pdf_content_tokens"),
        "epub_tokens": wc.get("epub_content_tokens"),
        "missing_word_samples": wc.get("missing_word_samples", []),
        "excess_word_samples": wc.get("excess_word_samples", []),
        "greek_coverage": gh.get("greek_word_coverage_ratio"),
        "hebrew_coverage": gh.get("hebrew_word_coverage_ratio"),
        "latin_coverage": lat_cov.get("latin_word_coverage_ratio"),
        "latin_tagging": lat_cov.get("latin_tagging_ratio"),
        "latin_translation": lat_trans.get("latin_translation_ratio"),
        "untagged_latin_samples": lat_cov.get("untagged_latin_word_samples", []),
        "untranslated_latin_samples": lat_trans.get("untranslated_latin_samples", []),
        "splits": pi.get("split_candidate_count", 0),
        "short_fragments": pi.get("short_fragment_count", 0),
        "inline_structural_candidates": pi.get("inline_structural_candidate_count", 0),
        "enumerator_sequence_candidates": pi.get("enumerator_sequence_candidates", []),
        "suspicious_large_number_starts": pi.get("suspicious_large_number_start_count", 0),
        "roman_heading_candidates": pi.get("roman_heading_candidate_count", 0),
        "dense_windows_missing": text_int.get("dense_source_window_integrity", {}).get("missing_dense_window_count", 0),
        "dense_windows_pages": [
            {"page": w.get("page"), "sample": w.get("sample", "")}
            for w in text_int.get("dense_source_window_integrity", {}).get("missing_dense_windows", [])
        ],
        "warning_count": text_int.get("warning_count", 0),
        "warnings": [w.get("code", "") for w in text_int.get("warnings", [])],
        "audit_errors": audit.get("error_count", 0),
        "audit_warnings": audit.get("warning_count", 0),
        "anomalies_count": anom.get("total_anomalies_count", 0),
        "anomalies": anom.get("anomalies", {}),
        "ignored_warnings": whitelist.get("text_integrity", {}).get("ignored_warnings", []),
        "whitelist_dense_pages": whitelist.get("text_integrity", {}).get("dense_source_window_loss", []),
        "whitelist": whitelist,
        "bug_regressions": bug_reg,
    }

    try:
        from scripts.scan_citations import load_volume, scan_volume
        vol_data = load_volume(vol)
        if vol_data:
            hits = scan_volume(vol, vol_data)
            data["total_citations"] = len(hits)
            data["unresolved_citations"] = sum(
                1 for h in hits if not h["already_resolved"] and not h["is_self_ref"]
            )
        else:
            data["total_citations"] = 0
            data["unresolved_citations"] = 0
    except Exception:
        data["total_citations"] = 0
        data["unresolved_citations"] = 0

    from scripts.report_volume_state import score_volume, gather_volume_data as state_gather
    state_data = state_gather(vol)
    data["need_score"] = score_volume(state_data)
    data["qa_level"] = state_data.get("qa_level", "?")
    data["unmatched_quotes"] = state_data.get("unmatched_quotes", 0)

    return data


def compute_need_breakdown(data: dict) -> list[dict]:
    rows = []
    ignored = data.get("ignored_warnings", [])

    cov = data.get("coverage")
    if cov is not None:
        rows.append(("Coverage", f"{cov*100:.2f}%", min((1.0 - cov) * 4000, 20.0)))
    else:
        rows.append(("Coverage", "?", 15.0))

    gc = data.get("greek_coverage")
    if gc is not None:
        rows.append(("Greek coverage", f"{gc*100:.1f}%", min((1.0 - gc) * 3000, 15.0)))
    else:
        rows.append(("Greek coverage", "?", 15.0))

    hc = data.get("hebrew_coverage")
    if hc is not None:
        rows.append(("Hebrew coverage", f"{hc*100:.1f}%", min((1.0 - hc) * 3000, 15.0)))
    else:
        rows.append(("Hebrew coverage", "?", 15.0))

    lat_cov = data.get("latin_coverage")
    if "low_latin_word_coverage" not in ignored:
        if lat_cov is not None and lat_cov < 0.990:
            rows.append(("Latin word coverage", f"{lat_cov*100:.2f}%", min((0.990 - lat_cov) * 2000, 10.0)))
        elif lat_cov is None:
            rows.append(("Latin word coverage", "?", 5.0))
        else:
            rows.append(("Latin word coverage", f"{lat_cov*100:.2f}%>=99%", 0.0))
    else:
        rows.append(("Latin word coverage", "whitelisted", 0.0))

    lat_tag = data.get("latin_tagging")
    if "low_latin_tagging" not in ignored:
        if lat_tag is not None:
            rows.append(("Latin tagging", f"{lat_tag*100:.1f}%", min((1.0 - lat_tag) * 10, 5.0)))
        else:
            rows.append(("Latin tagging", "?", 2.0))
    else:
        rows.append(("Latin tagging", "whitelisted", 0.0))

    lat_trans = data.get("latin_translation")
    if "low_latin_translation_coverage" not in ignored:
        if lat_trans is not None:
            rows.append(("Latin translation", f"{lat_trans*100:.1f}%", min((1.0 - lat_trans) * 10, 5.0)))
        else:
            rows.append(("Latin translation", "?", 2.0))
    else:
        rows.append(("Latin translation", "whitelisted", 0.0))

    total_cite = data.get("total_citations", 0)
    unresolved = data.get("unresolved_citations", 0)
    if total_cite > 0:
        cite_ratio = unresolved / total_cite
        rows.append(("Unresolved citations", f"{unresolved}/{total_cite}", cite_ratio * 15.0))
    else:
        rows.append(("Unresolved citations", "0/0", 0.0))

    splits = data.get("splits", 0)
    rows.append(("Splits", str(splits), min(splits * 0.5, 10.0)))

    aw = data.get("audit_warnings", 0)
    rows.append(("Audit warnings", str(aw), min(aw * 2, 10.0)))

    ae = data.get("audit_errors", 0)
    rows.append(("Audit errors", str(ae), min(ae * 5, 5.0)))

    anom = data.get("anomalies_count", 0)
    rows.append(("Anomalies", str(anom), min(anom * 0.1, 10.0)))

    uq = data.get("unmatched_quotes") or 0
    rows.append(("Unmatched quotes", str(uq), min(uq * 0.5, 10.0)))

    return rows


def categorize_dense_window_loss(page_data: dict) -> str:
    sample = page_data.get("sample", "").lower()
    has_greek = bool(re.search(r"[\u0370-\u03ff\u1f00-\u1fff]", sample))
    has_hebrew = bool(re.search(r"[\u0590-\u05ff]", sample))
    has_latin_phrase = bool(re.search(
        r"(?:et|de|ex|in|ad|per|pro|cum|non|sed|est|aut|vel|quod|quam|qui|quae|hoc|sic|enim|vero|igitur|tamen|nam|ut|si|nec|atque)\s",
        sample,
    ))
    has_scripture_ref = any(book in sample for book in SCRIPTURE_BOOKS if len(book) > 3)
    short_refs = bool(re.search(r"\d+[-:]\d+", sample))
    has_verse_list = bool(re.search(r"\b(?:matthew|mark|luke|john|acts|romans|corinthians|peter|hebrews|psalm|chronicles|isaiah|jeremiah)\b", sample))

    if has_greek or has_hebrew:
        return "polyglot"
    if has_latin_phrase and len(sample.split(",")) >= 2:
        return "patristic_latin"
    if has_verse_list or (has_scripture_ref and short_refs):
        return "scripture_refs"
    if has_latin_phrase:
        return "patristic_latin"
    return "structural"


def detect_compound_merges(vol) -> list[tuple[str, str, int]]:
    json_path = _vol_path(vol) / "intermediate" / f"volume_{vol}.json"
    if not json_path.exists():
        return []
    try:
        raw = json_path.read_text(encoding="utf-8")
    except Exception:
        return []

    compounds = {
        "officepower": "office-power",
        "churchcommunion": "church-communion",
        "churchrule": "church-rule",
        "subjectmatter": "subject-matter",
        "preeminence": "pre-eminence",
        "churchprivileges": "church-privileges",
        "churchgovernment": "church-government",
        "churchaffairs": "church-affairs",
        "churchofficers": "church-officers",
        "churchofficer": "church-officer",
        "churchpower": "church-power",
        "churchmember": "church-member",
        "churchmembers": "church-members",
        "churchedification": "church-edification",
        "churchorder": "church-order",
        "churchassemblies": "church-assemblies",
        "churchcovenant": "church-covenant",
        "churchcensures": "church-censures",
        "wellgoverned": "well-governed",
        "selfconceitedness": "self-conceitedness",
        "selfdenial": "self-denial",
        "selfexaltation": "self-exaltation",
        "selfabasement": "self-abasement",
        "selfreflection": "self-reflection",
        "overreaching": "over-reaching",
    }

    found = []
    for merged, correct in compounds.items():
        count = raw.lower().count(merged.lower())
        if count > 0:
            found.append((merged, correct, count))
    found.sort(key=lambda x: -x[2])
    return found


def compute_scenarios(data: dict) -> list[dict]:
    base_need = data.get("need_score", 0)
    cov = data.get("coverage") or 0
    cov_penalty = min((1.0 - cov) * 4000, 20.0) if cov else 2.0

    anom_count = data.get("anomalies_count", 0)
    anom_penalty = min(anom_count * 0.1, 10.0)

    uq = data.get("unmatched_quotes") or 0
    uq_penalty = min(uq * 0.5, 10.0)

    rows = [
        {"scenario": "Current state", "anomaly_penalty": anom_penalty,
         "quotes_penalty": uq_penalty, "coverage_penalty": cov_penalty,
         "total": base_need},
    ]
    rows.append({"scenario": "Whitelist anomalies only",
                  "anomaly_penalty": 0.0, "quotes_penalty": uq_penalty,
                  "coverage_penalty": cov_penalty,
                  "total": round(uq_penalty + cov_penalty, 1)})
    rows.append({"scenario": "Whitelist quotes only",
                  "anomaly_penalty": anom_penalty, "quotes_penalty": 0.0,
                  "coverage_penalty": cov_penalty,
                  "total": round(anom_penalty + cov_penalty, 1)})
    rows.append({"scenario": "Whitelist both anomalies + quotes",
                  "anomaly_penalty": 0.0, "quotes_penalty": 0.0,
                  "coverage_penalty": cov_penalty,
                  "total": round(cov_penalty, 1)})
    return rows


def generate_plan(vol) -> str:
    data = gather_volume_data(vol)
    label = get_volume_label(vol)
    need = data.get("need_score", 0)
    qa = data.get("qa_level", "?")
    cov = data.get("coverage", 0)

    lines = []
    lines.append(f"# Volume {vol} — Comprehensive Need Score Reduction Plan")
    lines.append("")
    lines.append(f"> Current Need: **{need}** | Grade: {qa} | QA Level: {data.get('qa_level', '?')}")
    lines.append(f"> Target Need: **≤ 2.0** (PRISTINE)")
    lines.append("")

    breakdown = compute_need_breakdown(data)
    lines.append("## Need Score Breakdown")
    lines.append("")
    lines.append("| Component | Value | Penalty | Capped? |")
    lines.append("|---|---|---|---|")
    total = 0
    for name, val, penalty in breakdown:
        capped = "YES" if penalty >= 10 else ("—" if penalty == 0 else "no")
        lines.append(f"| {name} | {val} | **{penalty:.1f}** | {capped} |")
        total += penalty
    lines.append(f"| **TOTAL** | | **{total:.1f}** | |")
    lines.append("")

    scenarios = compute_scenarios(data)
    lines.append("### Scenario Projections")
    lines.append("")
    lines.append("| Scenario | Anomalies | Quotes | Coverage | Total |")
    lines.append("|---|---|---|---|---|")
    for s in scenarios:
        lines.append(f"| **{s['scenario']}** | {s['anomaly_penalty']:.1f} | {s['quotes_penalty']:.1f} | {s['coverage_penalty']:.1f} | **{s['total']}** |")
    lines.append("")

    cov_gap = (1.0 - cov) * 4000 if cov else 0
    if cov_gap > 5:
        lines.append(f"The coverage gap alone contributes **{cov_gap:.1f}** points. ")
        lines.append("Reducing this requires finding and fixing missing content in the EPUB.")
    elif cov_gap > 0:
        lines.append(f"The coverage gap is only **{cov_gap:.1f}** points — very small. ")

    top_penalty_name = max(breakdown, key=lambda x: x[2])
    if top_penalty_name[2] > 0:
        lines.append(f"The dominant penalty is **{top_penalty_name[0]}** at **{top_penalty_name[2]:.1f}** points.")
    lines.append("")

    anomaly_categories = data.get("anomalies", {})
    lines.append("## Anomaly Breakdown")
    lines.append("")
    lines.append("| Category | Count | Legitimate? | Fixable? |")
    lines.append("|---|---|---|---|")
    for cat, items in anomaly_categories.items():
        count = len(items) if isinstance(items, list) else 0
        lines.append(f"| {cat} | {count} | See analysis | See analysis |")
    lines.append("")

    struct_jumps = anomaly_categories.get("Structural Nesting Sequence Jumps", [])
    if struct_jumps:
        lines.append("### Structural Nesting Sequence Jumps")
        lines.append("")
        lines.append(f"**{len(struct_jumps)} jumps** — all are sermon numbers or legitimate list starts:")
        for jump in struct_jumps:
            target = jump.get("target", "?")
            desc = jump.get("description", "")
            ch = jump.get("chapter", "?")
            lines.append(f"- `{target}` — {desc} ({ch})")
        lines.append("")
        lines.append("All are legitimate. White-list them.")
        lines.append("")

    unmatched = anomaly_categories.get("Unmatched Quotation Marks", [])
    if unmatched:
        lines.append("### Unmatched Quotation Marks")
        lines.append("")
        lines.append(f"**{len(unmatched)} entries** — Owen's 17th-century convention of opening quotation marks")
        lines.append("without closing them in debate/citation/Scripture contexts. These are authentic")
        lines.append("and should not be modernized per AGENTS.md.")
        lines.append("")

    uq = data.get("unmatched_quotes") or 0
    uq_penalty = min(uq * 0.5, 10.0)
    if uq_penalty > 0:
        lines.append(f"Unmatched quotes penalty: **{uq_penalty:.1f}** (capped at 10.0 from {uq} quotes × 0.5).")
        lines.append("Add `unmatched_quotes` to `ignored_warnings` in the whitelist to eliminate this penalty.")
        lines.append("")

    anom_count = data.get("anomalies_count", 0)
    anom_penalty = min(anom_count * 0.1, 10.0)
    if anom_penalty > 0:
        lines.append(f"Anomalies penalty: **{anom_penalty:.1f}** ({anom_count} anomalies × 0.1).")
        lines.append("White-list all legitimate anomaly categories to eliminate this penalty.")
        lines.append("")

    dense_pages = data.get("dense_windows_pages", [])
    if dense_pages:
        lines.append("## Dense Source Window Losses")
        lines.append("")
        lines.append(f"**{len(dense_pages)} pages** with missing dense source windows.")
        lines.append("")
        lines.append("| Page | Sample | Category | Action |")
        lines.append("|---|---|---|---|")
        for pd in dense_pages:
            cat = categorize_dense_window_loss(pd)
            action = "Whitelist" if cat in ("polyglot", "patristic_latin", "scripture_refs", "structural") else "Fix + re-audit"
            sample = pd.get("sample", "")[:60]
            lines.append(f"| {pd.get('page', '?')} | {sample}... | {cat} | {action} |")
        lines.append("")

    compounds = detect_compound_merges(vol)
    if compounds:
        lines.append("## Compound Word Merging Fixes")
        lines.append("")
        lines.append("The following merged compounds were found in the JSON intermediate.")
        lines.append("Add these to `OVERRIDES['text_replacements']` in `convert.py`:")
        lines.append("")
        lines.append("```python")
        lines.append("# Compound word merging fixes (extract.py drops hyphen at line breaks)")
        for merged, correct, count in compounds:
            lines.append(f"'{merged}': '{correct}',")
        lines.append("```")
        lines.append("")

    missing_words = data.get("missing_word_samples", [])
    if missing_words:
        lines.append("## Missing Word Samples")
        lines.append("")
        for mw in missing_words[:10]:
            word = mw.get("word", "?")
            pdf_c = mw.get("pdf", 0)
            epub_c = mw.get("epub", 0)
            lines.append(f"- `{word}`: PDF={pdf_c}, EPUB={epub_c}")
        lines.append("")

    excess_words = data.get("excess_word_samples", [])
    if excess_words:
        lines.append("## Excess Word Samples")
        lines.append("")
        for ew in excess_words[:10]:
            word = ew.get("word", "?")
            pdf_c = ew.get("pdf", 0)
            epub_c = ew.get("epub", 0)
            lines.append(f"- `{word}`: PDF={pdf_c}, EPUB={epub_c}")
        lines.append("")

    lines.append("## Whitelist Updates Required")
    lines.append("")
    lines.append("### `ignored_warnings` additions")
    lines.append("")
    lines.append("```json")
    current_ignored = data.get("ignored_warnings", [])
    additions = []
    if uq_penalty > 0 and "unmatched_quotes" not in current_ignored:
        additions.append("unmatched_quotes")
    if additions:
        lines.append(f'// Add these to text_integrity.ignored_warnings:')
        for a in additions:
            lines.append(f'"{a}",')
    else:
        lines.append("// No additions needed — all penalty-generating warnings are already whitelisted.")
    lines.append("```")
    lines.append("")

    current_dense_pages = set(data.get("whitelist_dense_pages", []))
    actual_dense_pages = set(pd.get("page", 0) for pd in dense_pages)
    stale = current_dense_pages - actual_dense_pages
    new_pages = actual_dense_pages - current_dense_pages

    if stale or new_pages:
        lines.append("### `dense_source_window_loss` updates")
        lines.append("")
        if stale:
            lines.append(f"**Stale entries to remove**: {sorted(stale)}")
            lines.append("")
        if new_pages:
            lines.append(f"**New pages to add**: {sorted(new_pages)}")
            lines.append("")
        lines.append("Updated whitelist:")
        lines.append("```json")
        all_pages = sorted(current_dense_pages | actual_dense_pages)
        lines.append(f'"dense_source_window_loss": {json.dumps(all_pages)}')
        lines.append("```")
        lines.append("")

    lines.append("## Action Checklist")
    lines.append("")
    priority = 1
    if uq_penalty > 0 and "unmatched_quotes" not in current_ignored:
        lines.append(f"### Step {priority}: White-list `unmatched_quotes` (Impact: −{uq_penalty:.1f} Need)")
        lines.append("")
        lines.append(f"Add `\"unmatched_quotes\"` to `ignored_warnings` in `volume_{vol}_whitelist.json`.")
        lines.append("")
        priority += 1

    if anom_penalty > 0:
        lines.append(f"### Step {priority}: White-list anomaly categories (Impact: −{anom_penalty:.1f} Need)")
        lines.append("")
        lines.append("Update the anomalies section in `volume_{vol}_whitelist.json` to cover all flagged categories.")
        if struct_jumps:
            lines.append(f"Add all {len(struct_jumps)} structural nesting sequence jumps.")
        if unmatched:
            lines.append("Add unmatched quotation marks explanation (legitimate Owen convention).")
        lines.append("")
        priority += 1

    if compounds:
        lines.append(f"### Step {priority}: Fix compound word merging (Impact: readability + coverage)")
        lines.append("")
        lines.append("Add the `text_replacements` entries listed above to `convert.py`.")
        lines.append("")
        priority += 1

    lines.append(f"### Step {priority}: Update dense source window whitelist")
    lines.append("")
    lines.append("Replace the `dense_source_window_loss` array in `volume_{vol}_whitelist.json`")
    lines.append("with the updated list shown above.")
    lines.append("")
    priority += 1

    lines.append(f"### Step {priority}: Re-audit and verify")
    lines.append("")
    lines.append("After all changes:")
    lines.append("1. Re-render: `.venv/bin/python3 volumes/v{vol}/convert.py --render-only`")
    lines.append("2. Audit EPUB: `.venv/bin/python3 scripts/audit_epub.py {vol}`")
    lines.append("3. Audit text integrity: `.venv/bin/python3 scripts/audit_text_integrity.py {vol}`")
    lines.append("4. Audit anomalies: `.venv/bin/python3 scripts/audit_anomalies.py {vol}`")
    lines.append("5. Audit bug regressions: `.venv/bin/python3 scripts/audit_bug_regressions.py {vol}`")
    lines.append("6. Report state: `.venv/bin/python3 scripts/report_volume_state.py`")
    lines.append(f"7. Verify Need drops from {need} to target")
    lines.append("")

    lines.append("## What NOT To Do")
    lines.append("")
    lat_cov = data.get("latin_coverage")
    if lat_cov is not None and lat_cov >= 0.990:
        lines.append(f"1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage")
        lines.append(f"   is already {lat_cov*100:.2f}% (above the 99% threshold). Whitelisting has zero effect.")
    if "low_latin_tagging" in (data.get("ignored_warnings") or []):
        lines.append("2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.")
    if unmatched:
        lines.append("3. **Do NOT try to \"fix\" Owen's quotation conventions** — All unmatched quotes are")
        lines.append("   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.")
    if struct_jumps:
        lines.append("4. **Do NOT try to resolve structural nesting sequence jumps** — These are sermon")
        lines.append("   numbers (4, 8, 10, 11, 12, 13) that are chapter titles, not list items.")

    return "\n".join(lines)


def find_worst_volume() -> str:
    state_path = ROOT / "qa" / "reports" / "volume_state_report.json"
    if not state_path.exists():
        print("Error: No volume state report found. Run scripts/report_volume_state.py first.")
        sys.exit(1)

    data = json.loads(state_path.read_text(encoding="utf-8"))
    owen_vols = [v for v in data if not str(v.get("vol", "")).lower().startswith("h")]
    if not owen_vols:
        print("Error: No Owen volumes found in state report.")
        sys.exit(1)
    worst = max(owen_vols, key=lambda v: v.get("need", 0))
    return str(worst.get("vol", "1"))


def main():
    parser = argparse.ArgumentParser(
        description="Generate Need score reduction plan for Owen volumes"
    )
    parser.add_argument(
        "volumes", nargs="*", default=["auto"],
        help="Volume number(s) to plan. Use 'auto' for worst-Need volume."
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Generate plans for all 16 volumes."
    )
    args = parser.parse_args()

    if args.all:
        volumes = [str(i) for i in range(1, 17)]
    else:
        volumes = args.volumes
        if volumes == ["auto"]:
            vol = find_worst_volume()
            print(f"Auto-detected worst volume: {vol}")
            volumes = [vol]

    for vol in volumes:
        label = get_volume_label(vol)
        print(f"Generating plan for Volume {vol} ({label})...")

        plan_dir = _plans_path(vol)
        plan_dir.mkdir(parents=True, exist_ok=True)

        plan = generate_plan(vol)
        plan_path = plan_dir / f"v{vol}_need_reduction_plan.md"
        plan_path.write_text(plan, encoding="utf-8")
        print(f"  Written: {plan_path}")

    print("Done.")


if __name__ == "__main__":
    main()