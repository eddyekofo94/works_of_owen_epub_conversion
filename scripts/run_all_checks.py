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

from cli_utils import bold, cyan, dim, green, red, status_icon, yellow

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


def print_summary(results: dict[int, dict], pytest_result: dict) -> None:
    sep = dim("\u2500" * 72)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{bold('=' * 72)}")
    print(f"  {bold('FULL CHECK SUMMARY')} \u2014 {now}")
    print(f"{bold('=' * 72)}\n")

    has_issues = False

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
            has_issues = True
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

        print(f"    {sep}")

    pt_icon = green("PASS") if pytest_result["ok"] else red("FAIL")
    print(f"\n  {dim('\u2500' * 68)}")
    print(f"  Pytest:  {pt_icon}  "
          f"{pytest_result['summary']}  {dim(_fmt_dur(pytest_result['elapsed']))}")
    print(f"  {dim('\u2500' * 68)}\n")

    _print_issue_list(results)

    if not has_issues and pytest_result["ok"]:
        print(f"  {green(bold('All checks passed — no issues found.'))}\n")

    print(f"  {dim('Detailed reports: volumes/v{n}/bugs_fixes/')}\n")


def _print_issue_list(results: dict[int, dict]) -> None:
    """Print a detailed issue list grouped by volume."""
    all_issues: list[tuple[int, str, str]] = []

    for vol in sorted(results):
        r = results[vol]

        if not r["converter"]["ok"]:
            tail = r["converter"]["output"].split("\n")[-1][:120]
            all_issues.append((vol, "Converter", tail))

        ea = r["epub_audit"]
        if ea:
            for ed in ea.get("error_details", []):
                msg = ed.get("message", str(ed))
                all_issues.append((vol, "EPUB Error", msg))
            for wd in ea.get("warning_details", []):
                msg = wd.get("message", str(wd))
                all_issues.append((vol, "EPUB Warning", msg))

        ti = r["text_integrity"]
        if ti:
            for wd in ti.get("warning_details", []):
                msg = wd.get("message", str(wd))
                all_issues.append((vol, "Integrity Warning", msg))

        br = r["bug_regression"]
        if br:
            for rd in br.get("regression_details", []):
                label = rd.get("label", "?")
                actual = rd.get("actual", "?")
                budget = rd.get("budget", "?")
                all_issues.append((vol, "Bug Regression", f"{label} (actual={actual}, budget={budget})"))
                for sample in rd.get("samples", [])[:3]:
                    s = str(sample)[:150]
                    all_issues.append((vol, "  Sample", s))

    if not all_issues:
        return

    print(f"  {bold(red('Issues Found'))}\n")
    for vol, kind, msg in all_issues:
        vol_tag = dim(f"v{vol}")
        if kind.startswith("EPUB Error") or kind == "Converter":
            kind_tag = red(kind)
        elif kind.startswith("Bug Regression"):
            kind_tag = red(kind)
        elif kind == "  Sample":
            kind_tag = dim("  Sample")
        else:
            kind_tag = yellow(kind)
        print(f"  {vol_tag} {kind_tag}: {msg}")


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
    args = parser.parse_args()

    volumes = resolve_volumes(args.volumes)
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
