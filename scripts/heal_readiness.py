#!/usr/bin/env python3
"""Shared heal-readiness classification helpers."""

from __future__ import annotations

import html
import json
import re
import subprocess
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

WORD_COVERAGE_THRESHOLD = 0.995
POLYGLOT_COVERAGE_THRESHOLD = 0.990
LATIN_REVIEW_THRESHOLD = 0.990

TEXT_WARNING_BLOCKERS = {
    "dense_source_window_loss",
    "paragraph_split_candidates",
    "missing_clauses",
    "bottom_of_page_text_loss",
    "top_of_page_text_loss",
    "repeated_windows",
    "missing_enumerators",
    "untagged_greek",
    "untagged_hebrew",
}

TEXT_WARNING_REVIEW_DEBT = {
    "syllabus_anchor_candidates",
    "inline_structural_markers",
    "low_latin_tagging",
    "low_latin_translation_coverage",
}

INLINE_NOTE_PATTERNS = (
    "Modern Translation:",
    "Modern Citation:",
)


@dataclass
class ReadinessItem:
    code: str
    message: str
    severity: str
    value: Any = None
    samples: list[Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v not in (None, [])}


def _pct(value: float | None) -> str:
    if value is None:
        return "?"
    return f"{value * 100:.2f}%"


def _sample_limit(samples: Any, limit: int = 5) -> list[Any]:
    if not samples:
        return []
    if isinstance(samples, list):
        return samples[:limit]
    return [samples]


def classify_state_data(data: dict[str, Any]) -> dict[str, Any]:
    """Classify gathered volume-state data into blockers and review debt."""

    blockers: list[ReadinessItem] = []
    review_debt: list[ReadinessItem] = []

    if data.get("qa_level") == "NONE":
        blockers.append(ReadinessItem(
            "missing_qa_reports",
            "No QA reports are available for this volume.",
            "blocker",
        ))
        return _classification_result(blockers, review_debt)

    if data.get("audit_status") is None:
        blockers.append(ReadinessItem("missing_epub_audit", "Missing EPUB audit report.", "blocker"))
    if data.get("coverage") is None:
        blockers.append(ReadinessItem("missing_text_integrity", "Missing text-integrity report.", "blocker"))
    if data.get("regressions") is None:
        blockers.append(ReadinessItem("missing_bug_regression", "Missing bug-regression report.", "blocker"))

    audit_errors = data.get("audit_errors")
    if audit_errors:
        blockers.append(ReadinessItem("epub_audit_errors", "EPUB audit errors remain.", "blocker", audit_errors))

    audit_warnings = data.get("audit_warnings")
    if audit_warnings:
        blockers.append(ReadinessItem("epub_audit_warnings", "EPUB audit warnings remain.", "blocker", audit_warnings))

    coverage = data.get("coverage")
    if coverage is not None and coverage < WORD_COVERAGE_THRESHOLD:
        blockers.append(ReadinessItem(
            "word_coverage_below_threshold",
            f"Word coverage {_pct(coverage)} is below {_pct(WORD_COVERAGE_THRESHOLD)}.",
            "blocker",
            coverage,
        ))

    for key, label in (("greek_coverage", "Greek"), ("hebrew_coverage", "Hebrew")):
        value = data.get(key)
        if value is not None and value < POLYGLOT_COVERAGE_THRESHOLD:
            blockers.append(ReadinessItem(
                f"{key}_below_threshold",
                f"{label} coverage {_pct(value)} is below {_pct(POLYGLOT_COVERAGE_THRESHOLD)}.",
                "blocker",
                value,
            ))

    latin_coverage = data.get("latin_coverage")
    if latin_coverage is not None and latin_coverage < POLYGLOT_COVERAGE_THRESHOLD:
        blockers.append(ReadinessItem(
            "latin_coverage_below_threshold",
            f"Latin word coverage {_pct(latin_coverage)} is below {_pct(POLYGLOT_COVERAGE_THRESHOLD)}.",
            "blocker",
            latin_coverage,
        ))

    if data.get("unresolved_citations", 0):
        blockers.append(ReadinessItem(
            "unresolved_citations",
            "Unresolved patristic/classical citations remain.",
            "blocker",
            data.get("unresolved_citations"),
        ))

    for key, label in (
        ("unresolved_modern_references", "Unresolved modern references remain."),
        ("untranslated_substantial_foreign_passages", "Substantial foreign passages remain untranslated."),
        ("unenriched_legacy_footnotes", "Legacy footnotes remain unenriched."),
    ):
        if data.get(key, 0):
            blockers.append(ReadinessItem(key, label, "blocker", data.get(key)))

    if data.get("anomalies_count"):
        blockers.append(ReadinessItem(
            "unresolved_anomalies",
            "Text anomalies remain unless specifically verified and whitelisted.",
            "blocker",
            data.get("anomalies_count"),
        ))

    if data.get("unmatched_quotes"):
        blockers.append(ReadinessItem(
            "unmatched_quotes",
            "Unmatched quotation-mark findings remain unless specifically verified and whitelisted.",
            "blocker",
            data.get("unmatched_quotes"),
        ))

    for warning in data.get("text_warning_details", []):
        code = warning.get("code", "text_integrity_warning")
        message = warning.get("message") or f"Text-integrity warning remains: {code}."
        if code in TEXT_WARNING_REVIEW_DEBT:
            review_debt.append(ReadinessItem(code, message, "review_debt"))
        elif code in TEXT_WARNING_BLOCKERS or code:
            blockers.append(ReadinessItem(code, message, "blocker"))

    for regression in data.get("regression_details", []):
        label = regression.get("label", "Bug regression")
        blockers.append(ReadinessItem(
            "bug_regression_over_budget",
            f"{label} exceeds its budget.",
            "blocker",
            {"observed": regression.get("observed", regression.get("actual")), "budget": regression.get("budget")},
            _sample_limit(regression.get("samples")),
        ))

    for key, label in (("latin_tagging", "Latin tagging"), ("latin_translation", "Latin translation")):
        value = data.get(key)
        if value is not None and value < LATIN_REVIEW_THRESHOLD:
            review_debt.append(ReadinessItem(
                f"low_{key}",
                f"{label} ratio {_pct(value)} is below {_pct(LATIN_REVIEW_THRESHOLD)}; verify no Latin text is missing.",
                "review_debt",
                value,
                _sample_limit(data.get(f"{key}_samples")),
            ))

    for entry in data.get("stale_whitelist_entries", []):
        review_debt.append(ReadinessItem(
            "stale_whitelist_entry",
            "Stale whitelist entry remains and should be cleaned when safe.",
            "review_debt",
            entry,
        ))

    return _classification_result(blockers, review_debt)


def _classification_result(blockers: list[ReadinessItem], review_debt: list[ReadinessItem]) -> dict[str, Any]:
    return {
        "blockers": [item.to_dict() for item in blockers],
        "review_debt": [item.to_dict() for item in review_debt],
        "blocker_count": len(blockers),
        "review_debt_count": len(review_debt),
        "ready": not blockers,
    }


def blocker_penalty(data: dict[str, Any]) -> float:
    """Conservative score penalty shared by the global Need report."""

    classification = classify_state_data(data)
    penalty = classification["blocker_count"] * 2.0
    penalty += classification["review_debt_count"] * 0.4
    return min(penalty, 12.0)


def scan_inline_modern_note_leaks(epub_path: Path) -> list[dict[str, str]]:
    """Find modern note content rendered inline in body XHTML."""

    if not epub_path.exists():
        return []

    leaks: list[dict[str, str]] = []
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            lower = name.lower()
            if not lower.endswith((".xhtml", ".html")):
                continue
            basename = Path(name).name.lower()
            if basename in {"endnotes.xhtml", "nav.xhtml", "toc.xhtml"}:
                continue
            text = zf.read(name).decode("utf-8", errors="replace")
            for pattern in INLINE_NOTE_PATTERNS:
                if pattern in text:
                    leaks.append({
                        "file": name,
                        "pattern": pattern,
                        "snippet": _snippet(text, pattern),
                    })
    return leaks


def _snippet(text: str, needle: str, radius: int = 90) -> str:
    idx = text.find(needle)
    start = max(0, idx - radius)
    end = min(len(text), idx + len(needle) + radius)
    raw = re.sub(r"\s+", " ", text[start:end]).strip()
    return html.unescape(raw)


def build_readiness_report(volume: str, state_data: dict[str, Any], need: float, epub_path: Path) -> dict[str, Any]:
    classification = classify_state_data(state_data)
    inline_leaks = scan_inline_modern_note_leaks(epub_path)
    source_changes = detect_source_text_changes(volume)
    if inline_leaks:
        classification["blockers"].append({
            "code": "inline_modern_note_content",
            "message": "Modern translation/citation note content appears inline in body XHTML.",
            "severity": "blocker",
            "value": len(inline_leaks),
            "samples": inline_leaks[:5],
        })
        classification["blocker_count"] += 1
        classification["ready"] = False
    if source_changes:
        branch = _current_branch()
        item = {
            "code": "source_text_or_conversion_changes",
            "value": len(source_changes),
            "samples": source_changes[:10],
        }
        if branch not in (None, "master"):
            # In-progress heal-branch work is disclosed review debt, not a blocker;
            # it only blocks readiness when the worktree is dirty on master.
            item["message"] = (
                f"Conversion-affecting files have uncommitted changes on branch '{branch}'; "
                "disclose and commit them on the heal branch before merging."
            )
            item["severity"] = "review"
            classification["review_debt"].append(item)
            classification["review_debt_count"] += 1
        else:
            item["message"] = (
                "Source-text or conversion-affecting files have uncommitted changes "
                "and must be explicitly reported before readiness."
            )
            item["severity"] = "blocker"
            classification["blockers"].append(item)
            classification["blocker_count"] += 1
            classification["ready"] = False

    strict_ready = need < 1.0 and classification["ready"]
    return {
        "volume": str(volume),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "need": need,
        "need_gate": need < 1.0,
        "strict_ready": strict_ready,
        "blocker_count": classification["blocker_count"],
        "review_debt_count": classification["review_debt_count"],
        "blockers": classification["blockers"],
        "review_debt": classification["review_debt"],
        "inline_modern_note_leaks": inline_leaks,
        "source_text_or_conversion_changes": source_changes,
    }


def _current_branch() -> str | None:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return None
    return proc.stdout.strip() or None


def detect_source_text_changes(volume: str) -> list[dict[str, str]]:
    """Return dirty files that can affect source text or conversion output."""

    watched = [
        "extract.py",
        "render.py",
        "shared.py",
        "scripts/patristic_refs.py",
        "scripts/translation_db.py",
        f"volumes/v{volume}/convert.py",
        f"volumes/v{volume}/intermediate/volume_{volume}.json",
    ]
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain", "--", *watched],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return []
    changes = []
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        changes.append({"status": line[:2].strip(), "path": line[3:].strip()})
    return changes


def write_readiness_reports(report: dict[str, Any], bugs_dir: Path) -> tuple[Path, Path]:
    volume = report["volume"]
    json_path = bugs_dir / f"volume_{volume}_heal_readiness.json"
    md_path = bugs_dir / f"volume_{volume}_heal_readiness.md"
    json_path.unlink(missing_ok=True)
    md_path.unlink(missing_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(render_readiness_markdown(report), encoding="utf-8")
    return json_path, md_path


def render_readiness_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Volume {report['volume']} Heal Readiness",
        "",
        f"Generated: {report['generated_at']}",
        "",
        f"- Need: {report['need']:.1f}",
        f"- Need gate `<1.0`: {'PASS' if report['need_gate'] else 'FAIL'}",
        f"- Strict ready for by-eye review: {'PASS' if report['strict_ready'] else 'FAIL'}",
        f"- Blockers: {report['blocker_count']}",
        f"- Review debt: {report['review_debt_count']}",
        "",
    ]
    lines.extend(_items_section("Blockers", report["blockers"]))
    lines.extend(_items_section("Review Debt", report["review_debt"]))
    if report.get("inline_modern_note_leaks"):
        lines.extend(_items_section("Inline Modern Note Leaks", report["inline_modern_note_leaks"]))
    return "\n".join(lines).rstrip() + "\n"


def _items_section(title: str, items: list[dict[str, Any]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not items:
        lines.extend(["None.", ""])
        return lines
    for item in items:
        code = item.get("code") or item.get("pattern", "item")
        message = item.get("message") or item.get("snippet") or ""
        lines.append(f"- `{code}`: {message}")
        if "value" in item:
            lines.append(f"  - Value: `{item['value']}`")
        samples = item.get("samples")
        if samples:
            lines.append(f"  - Samples: `{json.dumps(samples[:3], ensure_ascii=False)}`")
    lines.append("")
    return lines
