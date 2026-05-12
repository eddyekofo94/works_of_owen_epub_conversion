#!/usr/bin/env python3
"""Summarize known Owen bug-class regressions from generated audit reports.

This script is intended for the #test workflow: run the converter, run the
EPUB and text-integrity audits, then turn those reports into a repair queue for
known recurring bug classes.
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "qa" / "bug_regression_baselines.json"


TEXT_CHECKS = [
    (
        "Possible faulty paragraph splits",
        ("paragraph_integrity", "split_candidate_count"),
        ("text_integrity", "max_split_candidate_count"),
        ("paragraph_integrity", "split_candidates"),
    ),
    (
        "Inline structural marker candidates",
        ("paragraph_integrity", "inline_structural_candidate_count"),
        ("text_integrity", "max_inline_structural_candidate_count"),
        ("paragraph_integrity", "inline_structural_candidates"),
    ),
    (
        "Repeated word windows",
        ("repeated_windows",),
        ("text_integrity", "max_repeated_window_count"),
        ("repeated_windows",),
    ),
    (
        "Missing front CONTENTS pages",
        ("front_matter_toc_integrity", "missing_front_toc_pages"),
        ("text_integrity", "max_front_toc_missing_pages"),
        ("front_matter_toc_integrity", "missing_front_toc_samples"),
    ),
    (
        "Reference continuation splits",
        ("paragraph_integrity", "reference_continuation_split_count"),
        ("text_integrity", "max_reference_continuation_split_count"),
        ("paragraph_integrity", "reference_continuation_splits"),
    ),
    (
        "Citation continuation splits",
        ("paragraph_integrity", "citation_continuation_split_count"),
        ("text_integrity", "max_citation_continuation_split_count"),
        ("paragraph_integrity", "citation_continuation_splits"),
    ),
    (
        "Adjacent duplicate paragraphs",
        ("paragraph_integrity", "adjacent_duplicate_count"),
        ("text_integrity", "max_adjacent_duplicate_count"),
        ("paragraph_integrity", "adjacent_duplicates"),
    ),
    (
        "Missing enumerator markers",
        ("enumerator_integrity", "missing_marker_count"),
        ("text_integrity", "max_missing_marker_count"),
        ("enumerator_integrity", "missing_markers"),
    ),
]


EPUB_CHECKS = [
    (
        "EPUB packaging errors",
        ("error_count",),
        ("epub", "max_error_count"),
        ("errors",),
    ),
    (
        "Untagged Greek characters",
        ("info", "language", "greek_untagged_chars"),
        ("epub", "max_greek_untagged_chars"),
        ("info", "content_scan", "samples", "untagged_greek"),
    ),
    (
        "Untagged Hebrew characters",
        ("info", "language", "hebrew_untagged_chars"),
        ("epub", "max_hebrew_untagged_chars"),
        ("info", "content_scan", "samples", "untagged_hebrew"),
    ),
    (
        "Repeated phrase hits",
        ("info", "content_scan", "repeated_phrase_count"),
        ("epub", "max_repeated_phrase_count"),
        ("info", "content_scan", "samples", "repeated_phrase"),
    ),
    (
        "Possible Beta Code residue files",
        ("info", "content_scan", "beta_code_files"),
        ("epub", "max_beta_code_files"),
        ("info", "content_scan", "samples", "beta_code"),
    ),
    (
        "Escaped language-tag files",
        ("info", "content_scan", "escaped_lang_tag_files"),
        ("epub", "max_escaped_lang_tag_files"),
        ("info", "content_scan", "samples", "escaped_lang_tag"),
    ),
    (
        "Literal footnote marker files",
        ("info", "content_scan", "literal_footnote_marker_files"),
        ("epub", "max_literal_footnote_marker_files"),
        ("info", "content_scan", "samples", "literal_footnote_marker"),
    ),
    (
        "Empty bracket noise files",
        ("info", "content_scan", "empty_bracket_noise_files"),
        ("epub", "max_empty_bracket_noise_files"),
        ("info", "content_scan", "samples", "empty_bracket_noise"),
    ),
    (
        "Noteref links without spacing class",
        ("info", "content_scan", "noteref_without_class"),
        ("epub", "max_noteref_without_class"),
        ("info", "content_scan", "samples", "noteref_without_class"),
    ),
]


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def nested_get(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    value: Any = data
    for key in path:
        value = value[key]
    return value


def observed_value(data: dict[str, Any], path: tuple[str, ...]) -> int:
    value = nested_get(data, path)
    if isinstance(value, list):
        return len(value)
    return int(value)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing report: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_budget(volume: int, baseline_path: Path) -> dict[str, Any]:
    data = load_json(baseline_path)
    return deep_merge(data["default"], data.get("volumes", {}).get(str(volume), {}))


def report_paths(root: Path, volume: int) -> tuple[Path, Path, Path, Path]:
    bug_dir = root / "volumes" / f"v{volume}" / "bugs_fixes"
    return (
        bug_dir / f"volume_{volume}_audit.json",
        bug_dir / f"volume_{volume}_text_integrity.json",
        bug_dir / f"volume_{volume}_bug_regressions.json",
        bug_dir / f"volume_{volume}_bug_regressions.md",
    )


def warning_codes(result: dict[str, Any]) -> set[str]:
    return {item["code"] for item in result.get("warnings", [])}


def build_check_rows(
    result: dict[str, Any],
    budget: dict[str, Any],
    checks: list[tuple[str, tuple[str, ...], tuple[str, ...], tuple[str, ...]]],
) -> list[dict[str, Any]]:
    rows = []
    for label, observed_path, budget_path, sample_path in checks:
        observed = observed_value(result, observed_path)
        limit = observed_value(budget, budget_path)
        samples = nested_get(result, sample_path)
        rows.append({
            "label": label,
            "observed": observed,
            "budget": limit,
            "status": "regression" if observed > limit else "ok",
            "samples": samples[:10] if isinstance(samples, list) else [],
        })
    return rows


def build_result(volume: int, root: Path, baseline_path: Path) -> dict[str, Any]:
    epub_json, text_json, out_json, out_md = report_paths(root, volume)
    epub = load_json(epub_json)
    text = load_json(text_json)
    budget = load_budget(volume, baseline_path)

    text_rows = build_check_rows(text, budget, TEXT_CHECKS)
    epub_rows = build_check_rows(epub, budget, EPUB_CHECKS)

    text_extra = sorted(warning_codes(text) - set(budget["text_integrity"]["allowed_warning_codes"]))
    epub_extra = sorted(warning_codes(epub) - set(budget["epub"]["allowed_warning_codes"]))
    regressions = [row for row in text_rows + epub_rows if row["status"] == "regression"]

    return {
        "volume": volume,
        "status": "warn" if regressions or text_extra or epub_extra else "pass",
        "epub_audit": str(epub_json),
        "text_integrity_audit": str(text_json),
        "output_json": str(out_json),
        "output_markdown": str(out_md),
        "extra_warning_codes": {
            "text_integrity": text_extra,
            "epub": epub_extra,
        },
        "text_integrity_checks": text_rows,
        "epub_checks": epub_rows,
    }


def render_sample(sample: dict[str, Any]) -> str:
    parts = []
    for key in ("file", "page", "marker", "phrase", "text", "previous", "next", "sample"):
        if key in sample and sample[key]:
            value = str(sample[key]).replace("\n", " ")
            parts.append(f"{key}: {value[:220]}")
    return "; ".join(parts) if parts else str(sample)[:260]


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Bug Regression Report: Volume {result['volume']}",
        "",
        f"- Status: **{result['status'].upper()}**",
        f"- EPUB audit: `{Path(result['epub_audit']).name}`",
        f"- Text integrity audit: `{Path(result['text_integrity_audit']).name}`",
        "",
        "## Regression Budget",
        "",
        "| Check | Observed | Budget | Status |",
        "|-------|----------|--------|--------|",
    ]

    for row in result["text_integrity_checks"] + result["epub_checks"]:
        lines.append(
            f"| {row['label']} | {row['observed']} | {row['budget']} | {row['status'].upper()} |"
        )

    extras = result["extra_warning_codes"]
    if extras["text_integrity"] or extras["epub"]:
        lines.extend(["", "## New Warning Codes", ""])
        if extras["text_integrity"]:
            lines.append(f"- Text integrity: {', '.join(extras['text_integrity'])}")
        if extras["epub"]:
            lines.append(f"- EPUB: {', '.join(extras['epub'])}")

    lines.extend(["", "## Triage Samples", ""])
    for row in result["text_integrity_checks"] + result["epub_checks"]:
        if row["status"] != "regression" and not row["samples"]:
            continue
        lines.extend([f"### {row['label']}", ""])
        if not row["samples"]:
            lines.append("- No samples reported.")
        for sample in row["samples"][:5]:
            lines.append(f"- {render_sample(sample)}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_result(result: dict[str, Any]) -> None:
    out_json = Path(result["output_json"])
    out_md = Path(result["output_markdown"])
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    out_md.write_text(render_markdown(result), encoding="utf-8")


def parse_volumes(args: list[str]) -> list[int]:
    if len(args) == 1 and args[0].lower() == "all":
        return list(range(1, 17))
    return [int(arg) for arg in args]


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize known bug-class regressions from Owen audit reports")
    parser.add_argument("volumes", nargs="+", help="Volume number(s), or all")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--baseline", type=Path, default=BASELINE_PATH)
    parser.add_argument("--strict", action="store_true", help="Return non-zero when regressions are present")
    args = parser.parse_args()

    failed = False
    for volume in parse_volumes(args.volumes):
        result = build_result(volume, args.root, args.baseline)
        write_result(result)
        failed = failed or result["status"] != "pass"
        print(
            f"Volume {volume}: {result['status'].upper()} "
            f"({Path(result['output_markdown']).relative_to(args.root)})"
        )

    return 1 if args.strict and failed else 0


if __name__ == "__main__":
    sys.exit(main())
