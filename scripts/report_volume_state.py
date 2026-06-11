#!/usr/bin/env python3
"""Inventory QA state for all Owen volumes, rank by severity, write report.

Usage:
  .venv/bin/python3 scripts/report_volume_state.py                    # read existing reports
  .venv/bin/python3 scripts/report_volume_state.py --audit-missing    # run audits for missing volumes
  .venv/bin/python3 scripts/report_volume_state.py --volumes 4 5 7    # target specific volumes
  .venv/bin/python3 scripts/report_volume_state.py --no-readme        # skip README update
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cli_utils import bold, cyan, dim, green, magenta, red, yellow

from shared import get_volume_dir, get_volume_label

PYTHON = sys.executable
OWEN_VOLUMES = [str(i) for i in range(1, 17)]
HEBREWS_VOLUMES = [f"h{i}" for i in range(1, 8)]
ALL_VOLUMES = OWEN_VOLUMES + HEBREWS_VOLUMES

QA_LEVELS = {"PRISTINE": 4, "FULL": 3, "STANDARD": 2, "BASIC": 1, "NONE": 0}


# ── helpers ──────────────────────────────────────────────────────────────────

def _vol_path(vol) -> Path:
    return get_volume_dir(vol)


def _bugs_path(vol) -> Path:
    return _vol_path(vol) / "bugs_fixes"


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _pct(val: float | None, decimals: int = 2) -> str:
    if val is None:
        return "?"
    return f"{val * 100:.{decimals}f}"


def _maybe_pct(val: float | None) -> str | None:
    if val is None:
        return None
    return round(val * 100, 2)


# ── data gathering ───────────────────────────────────────────────────────────

def gather_volume_data(vol: int) -> dict:
    bugs = _bugs_path(vol)

    audit = _read_json(bugs / f"volume_{vol}_audit.json")
    text_int = _read_json(bugs / f"volume_{vol}_text_integrity.json")
    bug_reg = _read_json(bugs / f"volume_{vol}_bug_regressions.json")
    anom = _read_json(bugs / f"volume_{vol}_anomalies.json")
    unmatched_q_json = _read_json(bugs / f"volume_{vol}_unmatched_quotes.json")
    whitelist = _read_json(bugs / f"volume_{vol}_whitelist.json")

    # metadata from shared.py
    try:
        from shared import VOLUME_CONFIG
        cfg = VOLUME_CONFIG.get(vol, {})
    except ImportError:
        cfg = {}

    # convert.py
    convert_py = _vol_path(vol) / "convert.py"
    has_convert = convert_py.exists()
    convert_lines = len(convert_py.read_text().splitlines()) if has_convert else 0

    # count text_replacements in convert.py (coarse: count "text_replacements" key in file)
    text_repl_count = 0
    if has_convert:
        text_repl_count = convert_py.read_text().count("text_replacements")

    # extract data from reports
    wc = text_int.get("word_coverage", {})
    pi = text_int.get("paragraph_integrity", {})
    gh = text_int.get("greek_hebrew_word_coverage", {})
    lat_cov_info = text_int.get("latin_word_coverage", {})
    lat_trans_info = text_int.get("latin_translation_coverage", {})

    # citations from scan_citations.py
    total_citations = 0
    unresolved_citations = 0
    try:
        from scripts.scan_citations import load_volume, scan_volume
        vol_data = load_volume(vol)
        if vol_data:
            hits = scan_volume(vol, vol_data)
            total_citations = len(hits)
            unresolved_citations = sum(1 for h in hits if not h['already_resolved'] and not h['is_self_ref'])
    except Exception:
        pass

    data: dict[str, Any] = {
        "vol": vol,
        "font": cfg.get("body_font", "?"),
        "source_type": cfg.get("source_type", "?"),
        "treatises": len(cfg.get("treatises", [])),
        "has_convert_py": has_convert,
        "convert_py_lines": convert_lines,
        "text_replacements": text_repl_count,
        "anomalies_count": anom.get("total_anomalies_count"),
        "total_citations": total_citations,
        "unresolved_citations": unresolved_citations,
        "unmatched_quotes": unmatched_q_json.get("unmatched_quotes_count"),
        "ignored_warnings": whitelist.get("text_integrity", {}).get("ignored_warnings", []),
    }

    # audit report
    if audit:
        data["audit_status"] = audit.get("status", "?")
        data["audit_errors"] = audit.get("error_count", 0)
        data["audit_warnings"] = audit.get("warning_count", 0)
        data["footnote_count"] = audit.get("footnote_count")
    else:
        data["audit_status"] = None
        data["audit_errors"] = None
        data["audit_warnings"] = None
        data["footnote_count"] = None

    # text integrity report
    if text_int:
        coverage = wc.get("coverage_ratio")
        greek_cov = gh.get("greek_word_coverage_ratio")
        hebrew_cov = gh.get("hebrew_word_coverage_ratio")
        splits = pi.get("split_candidate_count", 0)

        data["coverage"] = coverage
        data["greek_coverage"] = greek_cov
        data["hebrew_coverage"] = hebrew_cov
        data["latin_coverage"] = lat_cov_info.get("latin_word_coverage_ratio")
        data["latin_tagging"] = lat_cov_info.get("latin_tagging_ratio")
        data["latin_translation"] = lat_trans_info.get("latin_translation_ratio")
        data["splits"] = splits
        data["text_warnings"] = text_int.get("warning_count", 0)
    else:
        data["coverage"] = None
        data["greek_coverage"] = None
        data["hebrew_coverage"] = None
        data["latin_coverage"] = None
        data["latin_tagging"] = None
        data["latin_translation"] = None
        data["splits"] = None
        data["text_warnings"] = None

    # bug regression report
    if bug_reg:
        checks = (
            bug_reg.get("text_integrity_checks", [])
            + bug_reg.get("epub_checks", [])
        )
        regressions = [c for c in checks if c.get("status") == "regression"]
        data["regressions"] = len(regressions)
        data["regression_details"] = [
            {"label": c.get("label"), "actual": c.get("actual"), "budget": c.get("budget")}
            for c in regressions
        ]
    else:
        data["regressions"] = None
        data["regression_details"] = []

    # derive QA level
    has_audit = audit != {}
    has_text = text_int != {}
    has_bug = bug_reg != {}
    if has_audit and has_text and has_bug:
        cov = data.get("coverage")
        greek_cov = data.get("greek_coverage")
        hebrew_cov = data.get("hebrew_coverage")
        latin_cov = data.get("latin_coverage")
        unres = data.get("unresolved_citations", 0)
        unmatched_quotes = data.get("unmatched_quotes")

        is_hebrews = str(vol).lower().startswith('h')
        is_pristine = (
            cov is not None and cov >= 0.995 and
            greek_cov is not None and greek_cov >= 0.990 and
            hebrew_cov is not None and hebrew_cov >= 0.990 and
            (is_hebrews or (latin_cov is not None and latin_cov >= 0.990)) and
            unres == 0 and
            (unmatched_quotes is None or unmatched_quotes == 0)
        )
        if is_pristine:
            data["qa_level"] = "PRISTINE"
        else:
            data["qa_level"] = "FULL"
    elif has_audit and has_text:
        data["qa_level"] = "STANDARD"
    elif has_audit:
        data["qa_level"] = "BASIC"
    else:
        data["qa_level"] = "NONE"

    # recommended actions
    actions: list[str] = []
    unmatched_quotes = data.get("unmatched_quotes")
    if unmatched_quotes is not None and unmatched_quotes > 0:
        actions.append("resolve_unmatched_quotes")
    if not has_audit:
        actions.append("run_epub_audit")
    if not has_text:
        actions.append("run_text_integrity_audit")
    if not has_bug:
        actions.append("run_bug_regression_report")
    if has_text:
        c = data.get("coverage")
        if c is not None and c < 0.90:
            actions.append("investigate_low_coverage")
        gc = data.get("greek_coverage")
        if gc is not None and gc < 0.90:
            actions.append("investigate_greek_extraction")
        hc = data.get("hebrew_coverage")
        if hc is not None and hc < 0.90:
            actions.append("investigate_hebrew_extraction")
        lat_c = data.get("latin_coverage")
        if lat_c is not None and lat_c < 0.90:
            actions.append("investigate_latin_extraction")
        if unresolved_citations > 0:
            actions.append("translate_unresolved_citations")
    if not has_convert:
        actions.append("create_per_volume_script")
    anom_count = data.get("anomalies_count")
    if anom_count is not None and anom_count > 20:
        actions.append("review_ocr_anomalies")
    data["recommended_actions"] = actions

    return data


# ── scoring ──────────────────────────────────────────────────────────────────

def score_volume(d: dict) -> float:
    score = 0.0
    ignored_warnings = d.get("ignored_warnings", [])

    if d["qa_level"] == "NONE":
        score += 40.0  # big penalty for no QA at all
    else:
        if d["audit_status"] is None:
            score += 15.0
        if d.get("coverage") is None:
            score += 15.0
        if d.get("regressions") is None:
            score += 10.0

    # coverage
    cov = d.get("coverage")
    if cov is not None:
        score += min((1.0 - cov) * 4000, 20.0)

    # Greek coverage
    gc = d.get("greek_coverage")
    if gc is not None:
        score += min((1.0 - gc) * 3000, 15.0)

    # Hebrew coverage
    hc = d.get("hebrew_coverage")
    if hc is not None:
        score += min((1.0 - hc) * 3000, 15.0)

    # Latin scoring (skipped for Hebrews)
    is_hebrews = str(d["vol"]).lower().startswith('h')
    if not is_hebrews:
        # Latin coverage
        if "low_latin_word_coverage" not in ignored_warnings:
            lat_cov = d.get("latin_coverage")
            if lat_cov is not None:
                score += min((1.0 - lat_cov) * 2000, 10.0)
            elif d["qa_level"] != "NONE":
                score += 5.0

        # Latin tagging
        if "low_latin_tagging" not in ignored_warnings:
            lat_tag = d.get("latin_tagging")
            if lat_tag is not None:
                score += min((1.0 - lat_tag) * 10, 5.0)
            elif d["qa_level"] != "NONE":
                score += 2.0

        # Latin translation
        if "low_latin_translation_coverage" not in ignored_warnings:
            lat_trans = d.get("latin_translation")
            if lat_trans is not None:
                score += min((1.0 - lat_trans) * 10, 5.0)
            elif d["qa_level"] != "NONE":
                score += 2.0

    # Unresolved citations ratio penalty
    total_cite = d.get("total_citations", 0)
    unresolved_cite = d.get("unresolved_citations", 0)
    if total_cite > 0:
        cite_ratio = unresolved_cite / total_cite
        score += cite_ratio * 15.0

    # splits
    splits = d.get("splits")
    if splits is not None:
        score += min(splits * 0.5, 10.0)

    # audit warnings
    aw = d.get("audit_warnings")
    if aw is not None:
        score += min(aw * 2, 10.0)

    # audit errors
    ae = d.get("audit_errors")
    if ae is not None:
        score += min(ae * 5, 5.0)

    # anomalies
    anom_c = d.get("anomalies_count")
    if anom_c is not None:
        score += min(anom_c * 0.1, 10.0)

    # unmatched quotes
    unmatched_quotes = d.get("unmatched_quotes")
    if unmatched_quotes is not None:
        score += min(unmatched_quotes * 0.5, 10.0)

    return round(score, 1)


# ── stdout table ─────────────────────────────────────────────────────────────

def _fmt(val: Any, width: int = 8) -> str:
    s = str(val) if val is not None else "?"
    return s.rjust(width)


def _score_color(score: float) -> str:
    if score < 20:
        return green(f"{score:>6.1f}")
    elif score < 40:
        return yellow(f"{score:>6.1f}")
    elif score < 60:
        return magenta(f"{score:>6.1f}")
    return red(f"{score:>6.1f}")


def vol_sort_key(vol_id):
    v_str = str(vol_id).lower()
    if v_str.startswith('h'):
        try:
            return (1, int(v_str[1:]))
        except ValueError:
            return (1, v_str)
    else:
        v_num = v_str[1:] if v_str.startswith('v') else v_str
        try:
            return (0, int(v_num))
        except ValueError:
            return (0, v_str)


def render_single_stdout_table(sub_ranked: list[dict], title: str) -> str:
    lines = []
    sep = dim("\u2500" * 78)
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    title_text = f"{title} — QA State Ranking  {now_str}"
    pad = max(0, (78 - len(title_text)) // 2)
    lines.append("")
    lines.append(f"{' ' * pad}{bold(title_text)}")
    lines.append(sep)
    header = (
        f"  {'Rank':>4}  {'Vol':>3}  {'Need':>6}  "
        f"{'Cov%':>6}  {'Greek':>6}  {'Heb':>6}  {'Lat%':>6}  "
        f"{'Splits':>6}  {'Unres':>5}  {'QA Level':>9}"
    )
    lines.append(header)
    lines.append(dim("\u2500" * 78))

    for i, d in enumerate(sub_ranked, 1):
        vol = d["vol"]
        score = d["score"]

        cov = _maybe_pct(d.get("coverage"))
        greek = _maybe_pct(d.get("greek_coverage"))
        hebrew = _maybe_pct(d.get("hebrew_coverage"))
        lat_cov = _maybe_pct(d.get("latin_coverage"))

        splits = d.get("splits")
        splits_s = str(splits) if splits is not None else "?"
        
        unres = d.get("unresolved_citations")
        unres_s = str(unres) if unres is not None else "?"

        ql = d["qa_level"]
        if ql == "PRISTINE":
            ql_s = bold(green("PRISTINE"))
        elif ql == "FULL":
            ql_s = green("FULL")
        elif ql == "STANDARD":
            ql_s = cyan("STANDARD")
        elif ql == "BASIC":
            ql_s = yellow("BASIC")
        else:
            ql_s = red("NONE")

        rank_str = red(f"{i:>4}") if ql == "NONE" else f"{i:>4}"

        lines.append(
            f"  {rank_str}  {vol:>3}  {_score_color(score)}  "
            f"{_fmt(cov, 6)}  {_fmt(greek, 6)}  {_fmt(hebrew, 6)}  {_fmt(lat_cov, 6)}  "
            f"{_fmt(splits_s, 6)}  {_fmt(unres_s, 5)}  {ql_s:>9}"
        )

    lines.append(sep)
    lines.append(f"  {dim('Need: lower = better (0 best, 100 worst). Green <20, Yellow <40, Pink <60, Red ≥60.')}")
    lines.append(f"  {dim('Red rank = No QA data — need is a placeholder penalty.')}")
    lines.append("")
    return "\n".join(lines)


def _format_table(ranked: list[dict]) -> str:
    works_ranked = [d for d in ranked if not str(d["vol"]).lower().startswith('h')]
    hebrews_ranked = [d for d in ranked if str(d["vol"]).lower().startswith('h')]

    lines = []
    if works_ranked:
        works_by_need = sorted(works_ranked, key=lambda x: (-x["score"], vol_sort_key(x["vol"])))
        lines.append(render_single_stdout_table(works_by_need, "Works of John Owen (16 Volumes)"))
    if hebrews_ranked:
        hebrews_by_need = sorted(hebrews_ranked, key=lambda x: (-x["score"], vol_sort_key(x["vol"])))
        lines.append(render_single_stdout_table(hebrews_by_need, "Hebrews Commentary (7 Volumes)"))

    return "\n".join(lines)


# ── markdown report ──────────────────────────────────────────────────────────

def _actions_to_text(actions: list[str]) -> str:
    icons = {
        "run_epub_audit": "📋 Run EPUB audit",
        "run_text_integrity_audit": "📝 Run text integrity audit",
        "run_bug_regression_report": "🐛 Run bug regression report",
        "investigate_low_coverage": "⚠️ Investigate low word coverage",
        "investigate_greek_extraction": "🔤 Investigate Greek extraction",
        "investigate_hebrew_extraction": "🔤 Investigate Hebrew extraction",
        "create_per_volume_script": "📄 Create per-volume script",
        "review_ocr_anomalies": "🔍 Review OCR anomalies",
        "resolve_unmatched_quotes": "❓ Resolve unmatched quotation marks",
    }
    return "; ".join(icons.get(a, a) for a in actions)


def write_markdown_report(ranked: list[dict], path: Path) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = []
    lines.append("# Owen Volumes — QA State Report")
    lines.append("")
    lines.append(f"Generated: {now}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("**Need** (0–100): lower is better. Combines coverage, Greek/Hebrew/Latin health, unresolved citations, splits, warnings, and QA completeness into a single score. Volumes ranked worst first.")
    lines.append("")

    works_ranked = [d for d in ranked if not str(d["vol"]).lower().startswith('h')]
    hebrews_ranked = [d for d in ranked if str(d["vol"]).lower().startswith('h')]

    if works_ranked:
        works_by_need = sorted(works_ranked, key=lambda x: (-x["score"], vol_sort_key(x["vol"])))
        lines.append("### Works of John Owen (16 Volumes)")
        lines.append("")
        lines.append("| Rank | Vol | Need | Font | Treatises | Coverage | Greek | Hebrew | Latin | Unres | Quotes | QA Level |")
        lines.append("|------|-----|------|------|-----------|----------|-------|--------|-------|-------|--------|----------|")
        for i, d in enumerate(works_by_need, 1):
            lines.append(
                f"| {i} | {d['vol']} | {d['score']} "
                f"| {d['font']} | {d['treatises']} "
                f"| {_fmt(_maybe_pct(d.get('coverage')), 6)} "
                f"| {_fmt(_maybe_pct(d.get('greek_coverage')), 6)} "
                f"| {_fmt(_maybe_pct(d.get('hebrew_coverage')), 6)} "
                f"| {_fmt(_maybe_pct(d.get('latin_coverage')), 6)} "
                f"| {d.get('unresolved_citations', '?')} "
                f"| {d.get('unmatched_quotes', '?')} "
                f"| {d['qa_level']} |"
            )
        lines.append("")

    if hebrews_ranked:
        hebrews_by_need = sorted(hebrews_ranked, key=lambda x: (-x["score"], vol_sort_key(x["vol"])))
        lines.append("### Hebrews Commentary (7 Volumes)")
        lines.append("")
        lines.append("| Rank | Vol | Need | Font | Treatises | Coverage | Greek | Hebrew | Unres | Quotes | QA Level |")
        lines.append("|------|-----|------|------|-----------|----------|-------|--------|-------|--------|----------|")
        for i, d in enumerate(hebrews_by_need, 1):
            lines.append(
                f"| {i} | {d['vol']} | {d['score']} "
                f"| {d['font']} | {d['treatises']} "
                f"| {_fmt(_maybe_pct(d.get('coverage')), 6)} "
                f"| {_fmt(_maybe_pct(d.get('greek_coverage')), 6)} "
                f"| {_fmt(_maybe_pct(d.get('hebrew_coverage')), 6)} "
                f"| {d.get('unresolved_citations', '?')} "
                f"| {d.get('unmatched_quotes', '?')} "
                f"| {d['qa_level']} |"
            )
        lines.append("")
    lines.append("## Per-Volume Details")
    lines.append("")

    for d in ranked:
        v = d["vol"]
        s = d["score"]
        if s < 20:
            need_label = "✅ Good"
        elif s < 40:
            need_label = "👌 Fair"
        elif s < 60:
            need_label = "🩷 Needs work"
        else:
            need_label = "❌ Poor"
        lines.append(f"### Volume {v} — Need: {d['score']} ({need_label}) — Rank {ranked.index(d) + 1}")
        lines.append("")
        lines.append(f"- **Body font:** {d['font']}")
        lines.append(f"- **Source type:** {d['source_type']}")
        lines.append(f"- **Treatises:** {d['treatises']}")
        lines.append(f"- **QA level:** {d['qa_level']}")
        lines.append(f"- **convert.py:** {'Yes' if d['has_convert_py'] else 'No'} ({d['convert_py_lines']} lines, {d['text_replacements']} text_replacements)")
        lines.append(f"- **Audit:** errors={d.get('audit_errors', '?')}, warnings={d.get('audit_warnings', '?')}, footnotes={d.get('footnote_count', '?')}")
        lines.append(f"- **Word coverage:** {_pct(d.get('coverage')) if d.get('coverage') is not None else '?'}")
        lines.append(f"- **Greek coverage:** {_pct(d.get('greek_coverage')) if d.get('greek_coverage') is not None else '?'}")
        lines.append(f"- **Hebrew coverage:** {_pct(d.get('hebrew_coverage')) if d.get('hebrew_coverage') is not None else '?'}")
        lines.append(f"- **Latin coverage:** {_pct(d.get('latin_coverage')) if d.get('latin_coverage') is not None else '?'}")
        lines.append(f"- **Latin tagging:** {_pct(d.get('latin_tagging')) if d.get('latin_tagging') is not None else '?'}")
        lines.append(f"- **Latin translation:** {_pct(d.get('latin_translation')) if d.get('latin_translation') is not None else '?'}")
        lines.append(f"- **Citations:** total={d.get('total_citations', 0)}, unresolved={d.get('unresolved_citations', 0)}")
        lines.append(f"- **Splits:** {d.get('splits', '?')}")
        lines.append(f"- **Regressions:** {d.get('regressions', '?')}")
        lines.append(f"- **Suspected anomalies:** {d.get('anomalies_count', '?')}")
        lines.append(f"- **Unmatched quotes:** {d.get('unmatched_quotes', '?')}")
        lines.append(f"- **Recommended:** {_actions_to_text(d['recommended_actions'])}")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_json_report(ranked: list[dict], path: Path) -> None:
    export = []
    for d in ranked:
        s = d["score"]
        if s < 20:
            grade = "good"
        elif s < 40:
            grade = "fair"
        elif s < 60:
            grade = "needs_work"
        else:
            grade = "poor"
        export.append({
            "vol": d["vol"],
            "rank": ranked.index(d) + 1,
            "score": d["score"],
            "need": d["score"],
            "grade": grade,
            "qa_level": d["qa_level"],
            "coverage": _maybe_pct(d.get("coverage")),
            "greek_coverage": _maybe_pct(d.get("greek_coverage")),
            "hebrew_coverage": _maybe_pct(d.get("hebrew_coverage")),
            "latin_coverage": _maybe_pct(d.get("latin_coverage")),
            "latin_tagging": _maybe_pct(d.get("latin_tagging")),
            "latin_translation": _maybe_pct(d.get("latin_translation")),
            "total_citations": d.get("total_citations", 0),
            "unresolved_citations": d.get("unresolved_citations", 0),
            "splits": d.get("splits"),
            "warnings": d.get("audit_warnings"),
            "errors": d.get("audit_errors"),
            "regressions": d.get("regressions"),
            "anomalies_count": d.get("anomalies_count"),
            "unmatched_quotes": d.get("unmatched_quotes"),
            "font": d["font"],
            "treatises": d["treatises"],
            "has_convert_py": d["has_convert_py"],
            "text_replacements": d["text_replacements"],
            "recommended_actions": d["recommended_actions"],
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(export, indent=2), encoding="utf-8")


# ── README updater ──────────────────────────────────────────────────────────

def _table_line(d: dict) -> str:
    v = d["vol"]
    v_str = str(v).lower()
    if v_str.startswith('h'):
        convert = v_str if d["has_convert_py"] else "—"
    else:
        convert = f"v{v}" if d["has_convert_py"] else "—"
    overrides = "Populated" if d["text_replacements"] > 0 else ("Empty" if d["has_convert_py"] else "—")
    ql = d["qa_level"]
    notes = ""
    if d["qa_level"] == "NONE":
        notes = "No QA reports"
    elif d["qa_level"] == "BASIC":
        notes = "Audit only"
    elif d["qa_level"] == "STANDARD":
        notes = "Audit + text integrity"
    else:
        cov = d.get("coverage")
        greek = d.get("greek_coverage")
        hebrew = d.get("hebrew_coverage")
        lat = d.get("latin_coverage")
        unres = d.get("unresolved_citations", 0)
        unmatched = d.get("unmatched_quotes")
        
        cov_s = f"{_pct(cov)}" if cov is not None else "?"
        greek_s = f"{_pct(greek)}" if greek is not None else "?"
        hebrew_s = f"{_pct(hebrew)}" if hebrew is not None else "?"
        lat_s = f"{_pct(lat)}" if lat is not None else "?"
        unres_s = f" Unres {unres}" if unres else ""
        unmatched_s = f" Quotes {unmatched}" if unmatched else ""
        
        is_hebrews = v_str.startswith('h')
        if is_hebrews:
            notes = f"Cov {cov_s} Greek {greek_s} Heb {hebrew_s}{unres_s}{unmatched_s}"
        else:
            notes = f"Cov {cov_s} Greek {greek_s} Heb {hebrew_s} Lat {lat_s}{unres_s}{unmatched_s}"

    return f"| {v} | {convert} | {overrides} | {ql} | {notes} |"


def _update_section_table(text: str, heading: str, new_table_rows: list[str]) -> str:
    lines = text.split("\n")
    try:
        heading_idx = next(i for i, ln in enumerate(lines) if heading in ln)
    except StopIteration:
        return text

    table_start_idx = None
    for i in range(heading_idx + 1, len(lines)):
        if lines[i].strip().startswith("|"):
            table_start_idx = i
            break
        if lines[i].strip().startswith("#"):
            break

    if table_start_idx is None:
        return text

    table_end_idx = table_start_idx
    while table_end_idx < len(lines) and lines[table_end_idx].strip().startswith("|"):
        table_end_idx += 1

    new_lines = lines[:table_start_idx] + new_table_rows + lines[table_end_idx:]
    return "\n".join(new_lines)


def update_readme(ranked: list[dict]) -> None:
    readme_path = ROOT / "README.md"
    text = readme_path.read_text(encoding="utf-8")

    works_ranked = [d for d in ranked if not str(d["vol"]).lower().startswith('h')]
    hebrews_ranked = [d for d in ranked if str(d["vol"]).lower().startswith('h')]

    if works_ranked:
        sorted_works = sorted(works_ranked, key=lambda x: vol_sort_key(x["vol"]))
        works_rows = [
            "| Volume | convert.py | OVERRIDES | QA Level | Notes |",
            "|---|---|---|---|---|",
        ]
        for d in sorted_works:
            works_rows.append(_table_line(d))
        text = _update_section_table(text, "## Per-Volume Script Status", works_rows)

    if hebrews_ranked:
        sorted_hebrews = sorted(hebrews_ranked, key=lambda x: vol_sort_key(x["vol"]))
        hebrews_rows = [
            "| Volume | convert.py | OVERRIDES | QA Level | Notes |",
            "|---|---|---|---|---|",
        ]
        for d in sorted_hebrews:
            hebrews_rows.append(_table_line(d))
        text = _update_section_table(text, "## Hebrews Commentary Script Status", hebrews_rows)

    readme_path.write_text(text, encoding="utf-8")
    print(f"  {green('README.md tables updated')}")


# ── audit missing ────────────────────────────────────────────────────────────

def run_audit_for_volume(vol: int) -> dict:
    """Run audit scripts for a volume that's missing reports."""
    results: dict[str, bool] = {}

    bugs = _bugs_path(vol)
    bugs.mkdir(parents=True, exist_ok=True)

    epub_path = _vol_path(vol) / "output" / f"volume_{vol}.epub"

    # EPUB audit
    audit_json = bugs / f"volume_{vol}_audit.json"
    if not audit_json.exists():
        if epub_path.exists():
            print(f"    [{vol}] Running audit_epub.py ...", end=" ", flush=True)
            r = subprocess.run(
                [PYTHON, str(ROOT / "scripts" / "audit_epub.py"), str(epub_path)],
                capture_output=True, text=True, timeout=600,
            )
            ok = r.returncode == 0
            print(green("done") if ok else red(f"failed ({r.returncode})"))
            results["audit"] = ok
        else:
            print(f"    [{vol}] {yellow('EPUB not found — skipping audit')}")
            results["audit"] = False
    else:
        results["audit"] = True

    # Text integrity
    text_json = bugs / f"volume_{vol}_text_integrity.json"
    if not text_json.exists():
        print(f"    [{vol}] Running audit_text_integrity.py ...", end=" ", flush=True)
        r = subprocess.run(
            [PYTHON, str(ROOT / "scripts" / "audit_text_integrity.py"), str(vol)],
            capture_output=True, text=True, timeout=600,
        )
        ok = r.returncode == 0
        print(green("done") if ok else red(f"failed ({r.returncode})"))
        results["text_integrity"] = ok
    else:
        results["text_integrity"] = True

    # Bug regression
    bug_json = bugs / f"volume_{vol}_bug_regressions.json"
    if not bug_json.exists():
        if text_json.exists() or results.get("text_integrity"):
            print(f"    [{vol}] Running audit_bug_regressions.py ...", end=" ", flush=True)
            r = subprocess.run(
                [PYTHON, str(ROOT / "scripts" / "audit_bug_regressions.py"), str(vol)],
                capture_output=True, text=True, timeout=300,
            )
            ok = r.returncode == 0
            print(green("done") if ok else red(f"failed ({r.returncode})"))
            results["bug_regression"] = ok
        else:
            print(f"    [{vol}] {yellow('Skipping bug regression (text integrity missing)')}")
            results["bug_regression"] = False
    else:
        results["bug_regression"] = True

    # Anomalies
    anom_json = bugs / f"volume_{vol}_anomalies.json"
    if not anom_json.exists():
        print(f"    [{vol}] Running audit_anomalies.py ...", end=" ", flush=True)
        r = subprocess.run(
            [PYTHON, str(ROOT / "scripts" / "audit_anomalies.py"), str(vol)],
            capture_output=True, text=True, timeout=300,
        )
        ok = r.returncode == 0
        print(green("done") if ok else red(f"failed ({r.returncode})"))
        results["anomalies"] = ok
    else:
        results["anomalies"] = True

    return results


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory and rank QA state for all Owen volumes",
    )
    parser.add_argument(
        "--volumes", type=str, nargs="*",
        help="Volume numbers/identifiers (e.g. 1, h1)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process all volumes",
    )
    parser.add_argument(
        "--audit-missing", action="store_true",
        help="Run audit scripts for volumes missing reports",
    )
    parser.add_argument(
        "--no-readme", action="store_true",
        help="Skip README.md update",
    )
    args = parser.parse_args()

    volumes = ALL_VOLUMES if args.all else (args.volumes or ALL_VOLUMES)

    if args.audit_missing:
        print(f"{bold('Running audits for missing reports...')}")
        for vol in volumes:
            d = gather_volume_data(vol)
            if d["qa_level"] == "NONE" or d["audit_status"] is None:
                print(f"  {cyan(f'Volume {vol}:')} {d['qa_level']} — running audits")
                run_audit_for_volume(vol)
    else:
        print(f"{bold('Reading existing QA reports...')}")

    # Gather data (after possible audits)
    all_data = [gather_volume_data(v) for v in volumes]

    # Score and rank (worst first)
    for d in all_data:
        d["score"] = score_volume(d)
        
    ranked = sorted(all_data, key=lambda x: (-x["score"], vol_sort_key(x["vol"])))

    # Outputs
    print(_format_table(ranked))

    md_path = ROOT / "qa" / "reports" / "volume_state_report.md"
    write_markdown_report(ranked, md_path)
    print(f"  Report: {green(str(md_path))}")

    json_path = ROOT / "qa" / "reports" / "volume_state_report.json"
    write_json_report(ranked, json_path)
    print(f"  JSON:   {green(str(json_path))}")

    if not args.no_readme:
        update_readme(ranked)

    return 0


if __name__ == "__main__":
    sys.exit(main())
