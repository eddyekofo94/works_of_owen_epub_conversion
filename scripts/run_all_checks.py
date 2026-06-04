#!/usr/bin/env python3
"""
Run the full check pipeline for Owen volumes.

For each volume: converter -> EPUB audit -> text integrity audit -> bug regression report.
Then runs all pytest tests across the selected volumes.

Usage:
  .venv/bin/python3 scripts/run_all_checks.py             all volumes
  .venv/bin/python3 scripts/run_all_checks.py 3            volume 3
  .venv/bin/python3 scripts/run_all_checks.py 1 2 5        volumes 1, 2, 5
  .venv/bin/python3 scripts/run_all_checks.py --no-rebuild skip converter, audit existing EPUBs
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cli_utils import bold, cyan, dim, green, red, status_icon, yellow

PYTHON = sys.executable
OWEN_VOLUME_RANGE = range(1, 17)


def resolve_volumes(args: list[str]) -> list[int]:
    if not args:
        return list(OWEN_VOLUME_RANGE)
    if len(args) == 1 and args[0].lower() in ("all", "--all"):
        return list(OWEN_VOLUME_RANGE)
    seen: set[int] = set()
    result: list[int] = []
    for arg in args:
        try:
            vol = int(arg)
        except ValueError:
            continue
        if vol in OWEN_VOLUME_RANGE and vol not in seen:
            seen.add(vol)
            result.append(vol)
    return result


def _run(cmd: list[str], label: str, timeout: int = 7200) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        lines = (r.stdout + r.stderr).strip().split("\n")
        tail = "\n".join(lines[-6:]).strip()
        return r.returncode, tail
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except FileNotFoundError:
        return -1, "command not found"


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _fmt_dur(secs: float) -> str:
    if secs < 60:
        return f"{secs:.0f}s"
    m = int(secs // 60)
    s = int(secs % 60)
    return f"{m}m{s:02d}s" if m < 60 else f"{m // 60}h{m % 60}m"


def run_volume_pipeline(vol_num: int, no_rebuild: bool = False) -> dict:
    start = datetime.now()
    bugs_dir = ROOT / "volumes" / f"v{vol_num}" / "bugs_fixes"
    bugs_dir.mkdir(parents=True, exist_ok=True)
    epub_path = ROOT / "volumes" / f"v{vol_num}" / "output" / f"volume_{vol_num}.epub"

    summary: dict = {
        "volume": vol_num,
        "elapsed": 0,
        "converter": None,
        "epub_audit": None,
        "text_integrity": None,
        "bug_regression": None,
        "anomalies_audit": None,
    }

    if not no_rebuild:
        print(f"  [{vol_num}] converter.py ...", end=" ", flush=True)
        code, out = _run(
            [PYTHON, str(ROOT / "converter.py"), str(vol_num)],
            f"v{vol_num} converter",
        )
        ok = code == 0
        print(status_icon(ok))
        summary["converter"] = {"ok": ok, "output": out}
        if not ok:
            summary["elapsed"] = (datetime.now() - start).total_seconds()
            return summary
    else:
        summary["converter"] = {"ok": True, "output": "skipped (--no-rebuild)"}
        if not epub_path.exists():
            summary["converter"] = {"ok": False, "output": f"EPUB not found: {epub_path}"}
            summary["elapsed"] = (datetime.now() - start).total_seconds()
            return summary

    print(f"  [{vol_num}] audit_epub.py ...", end=" ", flush=True)
    code, out = _run(
        [PYTHON, str(ROOT / "scripts" / "audit_epub.py"), str(epub_path)],
        f"v{vol_num} epub audit",
    )
    ok = code == 0
    print(status_icon(ok))
    aj = _read_json(bugs_dir / f"volume_{vol_num}_audit.json")
    summary["epub_audit"] = {
        "ok": ok,
        "errors": aj.get("error_count", "?"),
        "warnings": aj.get("warning_count", "?"),
        "footnotes": aj.get("footnote_count", "?"),
        "error_details": aj.get("errors", []),
        "warning_details": aj.get("warnings", []),
        "output": out,
    }

    print(f"  [{vol_num}] audit_text_integrity.py ...", end=" ", flush=True)
    code, out = _run(
        [PYTHON, str(ROOT / "scripts" / "audit_text_integrity.py"), str(vol_num)],
        f"v{vol_num} text integrity",
    )
    ok = code == 0
    print(status_icon(ok))
    tj = _read_json(bugs_dir / f"volume_{vol_num}_text_integrity.json")
    wc = tj.get("word_coverage", {})
    pi = tj.get("paragraph_integrity", {})
    summary["text_integrity"] = {
        "ok": ok,
        "word_coverage": wc.get("latin_word_coverage_pct", "?"),
        "splits": pi.get("split_candidate_count", 0),
        "warning_details": tj.get("warnings", []),
        "output": out,
    }

    print(f"  [{vol_num}] audit_bug_regressions.py ...", end=" ", flush=True)
    code, out = _run(
        [PYTHON, str(ROOT / "scripts" / "audit_bug_regressions.py"), str(vol_num)],
        f"v{vol_num} bug regressions",
    )
    ok = code == 0
    print(status_icon(ok))
    bj = _read_json(bugs_dir / f"volume_{vol_num}_bug_regressions.json")
    checks = bj.get("text_integrity_checks", []) + bj.get("epub_checks", [])
    regression_details = [
        {"label": c.get("label"), "actual": c.get("actual"), "budget": c.get("budget"), "samples": c.get("samples", [])}
        for c in checks if c.get("status") == "regression"
    ]
    summary["bug_regression"] = {
        "ok": ok,
        "regressions": len(regression_details),
        "regression_details": regression_details,
        "output": out,
    }

    print(f"  [{vol_num}] audit_anomalies.py ...", end=" ", flush=True)
    code, out = _run(
        [PYTHON, str(ROOT / "scripts" / "audit_anomalies.py"), str(vol_num)],
        f"v{vol_num} anomalies audit",
    )
    ok = code == 0
    print(status_icon(ok))
    anj = _read_json(bugs_dir / f"volume_{vol_num}_anomalies.json")
    summary["anomalies_audit"] = {
        "ok": ok,
        "count": anj.get("total_anomalies_count", "?"),
        "output": out,
    }

    summary["elapsed"] = (datetime.now() - start).total_seconds()
    return summary


def run_pytest(volumes: list[int]) -> dict:
    test_files = sorted((ROOT / "tests").glob("test_*.py"))
    vol_str = "all" if len(volumes) >= 16 else " ".join(str(v) for v in volumes)
    env = {**os.environ, "OWEN_REGRESSION_VOLUMES": vol_str}

    start = datetime.now()
    try:
        r = subprocess.run(
            [PYTHON, "-m", "pytest", "-v"] + [str(f) for f in test_files],
            capture_output=True, text=True, timeout=7200, env=env,
        )
        lines = (r.stdout + r.stderr).strip().split("\n")
        summary_line = next(
            (ln.strip() for ln in reversed(lines) if "passed" in ln and "failed" in ln),
            "",
        )
        return {
            "ok": r.returncode == 0,
            "summary": summary_line,
            "output": "\n".join(lines[-5:]).strip(),
            "elapsed": (datetime.now() - start).total_seconds(),
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "summary": "TIMEOUT", "output": "", "elapsed": 0}
    except FileNotFoundError:
        return {"ok": False, "summary": "pytest not found", "output": "", "elapsed": 0}


def _collect_issues_for_volume(vol_num: int, result: dict) -> list[tuple[str, str, str, str]]:
    """Return [(kind_label, code, message, extra_context), ...] for one volume."""
    issues: list[tuple[str, str, str, str]] = []

    if not result["converter"]["ok"]:
        tail = result["converter"]["output"].split("\n")[-1][:200]
        issues.append(("Converter", "", tail, ""))

    ea = result.get("epub_audit")
    if ea:
        for ed in ea.get("error_details", []):
            extra = _fmt_extra_fields(ed)
            issues.append(("EPUB Error", ed.get("code", ""), ed.get("message", ""), extra))
        for wd in ea.get("warning_details", []):
            extra = _fmt_extra_fields(wd)
            issues.append(("EPUB Warning", wd.get("code", ""), wd.get("message", ""), extra))

    ti = result.get("text_integrity")
    if ti:
        ti_raw = _read_json(ROOT / "volumes" / f"v{vol_num}" / "bugs_fixes" / f"volume_{vol_num}_text_integrity.json")
        for wd in ti.get("warning_details", []):
            code = wd.get("code", "")
            extra = _fmt_text_integrity_extra(ti_raw, code)
            issues.append(("Integrity Warn", code, wd.get("message", ""), extra))

    br = result.get("bug_regression")
    if br:
        for rd in br.get("regression_details", []):
            label = rd.get("label", "?")
            actual = rd.get("actual", "?")
            budget = rd.get("budget", "?")
            msg = f"{label} (actual={actual}, budget={budget})"
            samples = rd.get("samples", [])
            extra_parts = []
            for s in samples[:2]:
                if isinstance(s, dict) and "file" in s:
                    t = str(s.get("text", ""))[:120]
                    extra_parts.append(f"{s['file']}: {t}" if t else s['file'])
                else:
                    extra_parts.append(str(s)[:150])
            issues.append(("Bug Regression", label, msg, "  " + "\n       ".join(extra_parts) if extra_parts else ""))

    return issues


def _fmt_extra_fields(d: dict) -> str:
    """Format extra context fields from an audit error/warning dict."""
    skip = {"code", "message"}
    parts = []
    for k, v in d.items():
        if k in skip:
            continue
        if isinstance(v, list):
            if len(v) > 3:
                parts.append(f"{k}={', '.join(str(x) for x in v[:3])}…")
            else:
                parts.append(f"{k}={', '.join(str(x) for x in v)}")
        elif isinstance(v, (int, float)):
            parts.append(f"{k}={v}")
        elif isinstance(v, str) and v:
            parts.append(f"{k}={v}")
    return "  " + "  ".join(parts) if parts else ""


def _fmt_text_integrity_extra(tj: dict, code: str) -> str:
    """Pull sample file/page references from text integrity data for a warning code."""
    lookup = {
        "weak_page_coverage": ("page_coverage", "weak_pages", "page"),
        "dense_source_window_loss": ("dense_source_window_integrity", "missing_windows", "page"),
        "front_matter_toc_loss": ("front_matter_toc_integrity", "missing_pages", "page"),
        "top_of_page_text_loss": ("top_of_page_integrity", "missing_pages", "page"),
        "bottom_of_page_text_loss": ("bottom_of_page_integrity", "missing_pages", "page"),
        "paragraph_split_candidates": ("paragraph_integrity", "split_candidates", "file"),
        "inline_structural_markers": ("paragraph_integrity", "inline_structural_candidates", "file"),
        "reference_continuation_splits": ("paragraph_integrity", "reference_continuation_splits", "file"),
        "citation_continuation_splits": ("paragraph_integrity", "citation_continuation_splits", "file"),
        "paragraph_duplicates": ("paragraph_integrity", "adjacent_duplicates", "file"),
        "roman_heading_candidates": ("paragraph_integrity", "roman_heading_candidates", "file"),
        "overlong_heading_candidates": ("paragraph_integrity", "overlong_heading_candidates", "file"),
        "suspicious_large_number_starts": ("paragraph_integrity", "suspicious_large_number_starts", "file"),
        "enumerator_discrepancies": ("enumerator_integrity", "missing_markers", "file"),
        "missing_enumerator_markers": ("enumerator_integrity", "missing_markers", "file"),
        "missing_greek_clauses": ("greek_hebrew_clause_fidelity", "missing_greek_clauses", "page"),
    }
    if code not in lookup:
        return ""

    section, subkey, file_field = lookup[code]
    data = tj.get(section, {}).get(subkey, [])
    if not data:
        return ""

    seen: set[str] = set()
    samples: list[str] = []
    for item in data:
        ref = str(item.get(file_field, item.get("file", "")))
        if ref and ref not in seen:
            seen.add(ref)
            if file_field == "page":
                samples.append(f"page {ref}")
            else:
                text = str(item.get("text", ""))[:80] if "text" in item else ""
                samples.append(f"{ref}: {text}" if text else ref)
        if len(samples) >= 2:
            break

    if samples:
        return "  " + "\n       ".join(samples)
    return ""


def _print_volume_issues(vol_num: int, result: dict) -> None:
    """Print numbered issues for a single volume inline after its pipeline."""
    issues = _collect_issues_for_volume(vol_num, result)
    if not issues:
        return

    sep = dim("\u2500" * 72)
    print()
    print(f"  {bold(red(f'Volume {vol_num} — {len(issues)} issue{"s" if len(issues) > 1 else ""}'))}")
    print(f"  {dim('\u2500' * 50)}")

    for i, (kind, code, msg, extra) in enumerate(issues, 1):
        if kind == "Converter":
            tag = red("Converter")
        elif kind.startswith("EPUB Error"):
            tag = red("EPUB Error")
        elif kind.startswith("Bug Regression"):
            tag = red("Bug Regression")
        elif kind.startswith("EPUB Warning"):
            tag = yellow("EPUB Warn ")
        else:
            tag = yellow("Integrity ")

        code_str = f" [{code}]" if code else ""
        print(f"  {i:>2}. {tag}{code_str}")
        print(f"       {msg}")
        if extra:
            print(f"       {extra}")

    print(f"  {dim('\u2500' * 72)}")


def print_summary(results: dict[int, dict], pytest_result: dict) -> None:
    sep = dim("\u2500" * 72)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{bold('=' * 72)}")
    print(f"  {bold('FULL CHECK SUMMARY')} \u2014 {now}")
    print(f"{bold('=' * 72)}\n")

    any_fail = False

    for vol in sorted(results):
        r = results[vol]
        dur = _fmt_dur(r.get("elapsed", 0))
        all_ok = (
            r["converter"]["ok"]
            and (r["epub_audit"] is None or r["epub_audit"]["ok"])
            and (r["text_integrity"] is None or r["text_integrity"]["ok"])
            and (r["bug_regression"] is None or r["bug_regression"]["ok"])
        )
        if not all_ok:
            any_fail = True
        vol_label = bold(f"Volume {vol}") if all_ok else bold(red(f"Volume {vol}"))
        print(f"  {vol_label}  {dim(dur)}")

        c = r["converter"]
        print(f"    Converter:       {status_icon(c['ok'])}")

        ea = r["epub_audit"]
        if ea:
            err = ea["errors"]
            warn = ea["warnings"]
            fn = ea["footnotes"]
            err_s = red(str(err)) if isinstance(err, int) and err > 0 else str(err)
            warn_s = yellow(str(warn)) if isinstance(warn, int) and warn > 0 else str(warn)
            print(f"    EPUB Audit:      {status_icon(ea['ok'])}  "
                  f"Errors: {err_s}  Warnings: {warn_s}  "
                  f"Footnotes: {fn}")

        ti = r["text_integrity"]
        if ti:
            wc = ti["word_coverage"]
            wc_s = f"{wc:.1f}%" if isinstance(wc, (int, float)) else str(wc)
            if isinstance(wc, (int, float)) and wc < 95:
                wc_s = yellow(wc_s)
            print(f"    Text Integrity:  {status_icon(ti['ok'])}  "
                  f"Coverage: {wc_s}  Splits: {ti['splits']}")

        br = r["bug_regression"]
        if br:
            reg = br["regressions"]
            reg_s = red(str(reg)) if reg > 0 else green(str(reg))
            print(f"    Bug Regressions: {status_icon(br['ok'])}  "
                  f"Over budget: {reg_s}")

        an = r.get("anomalies_audit")
        if an:
            an_count = an["count"]
            print(f"    Text Anomalies:  {status_icon(an['ok'])}  "
                  f"Flagged: {an_count}")

        print(f"    {sep}")

    pt_icon = green("PASS") if pytest_result["ok"] else red("FAIL")
    print(f"\n  {dim('\u2500' * 68)}")
    print(f"  Pytest:  {pt_icon}  "
          f"{pytest_result['summary']}  {dim(_fmt_dur(pytest_result['elapsed']))}")
    print(f"  {dim('\u2500' * 68)}\n")

    if not any_fail and pytest_result["ok"]:
        print(f"  {green(bold('All checks passed — no issues found.'))}\n")

    print(f"  {dim('Detailed reports: volumes/v{n}/bugs_fixes/')}\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Full check pipeline for Owen volumes",
    )
    parser.add_argument(
        "volumes", nargs="*",
        help="Volume numbers (default: all 16)",
    )
    parser.add_argument(
        "--no-rebuild", action="store_true",
        help="Skip converter.py, audit existing EPUBs only",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process all 16 volumes",
    )
    args = parser.parse_args()

    volumes = list(OWEN_VOLUME_RANGE) if args.all else resolve_volumes(args.volumes)
    if not volumes:
        print("No valid volumes specified.", file=sys.stderr)
        return 1

    vol_list = ", ".join(str(v) for v in volumes)
    rebuild_note = dim("  (--no-rebuild)") if args.no_rebuild else ""
    print(f"Full check for volume(s): {bold(vol_list)}{rebuild_note}")

    results: dict[int, dict] = {}
    for v in volumes:
        print(f"\n{cyan(f'=== Volume {v} ===')}")
        results[v] = run_volume_pipeline(v, no_rebuild=args.no_rebuild)
        _print_volume_issues(v, results[v])

    print(f"\n{cyan('=== Pytest ===')}")
    pt = run_pytest(volumes)
    print(pt["summary"] or pt["output"])

    print_summary(results, pt)

    any_fail = (
        any(r.get("converter") and not r["converter"]["ok"] for r in results.values())
        or any(r.get("epub_audit") and not r["epub_audit"]["ok"] for r in results.values())
        or any(r.get("text_integrity") and not r["text_integrity"]["ok"] for r in results.values())
        or any(r.get("bug_regression") and not r["bug_regression"]["ok"] for r in results.values())
        or not pt["ok"]
    )
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
