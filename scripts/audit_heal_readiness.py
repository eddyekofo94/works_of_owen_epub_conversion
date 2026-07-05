#!/usr/bin/env python3
"""Audit whether a healed volume is strictly ready for by-eye review."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.heal_readiness import build_readiness_report, write_readiness_reports
from scripts.report_volume_state import gather_volume_data, score_volume


def _normalize_volume(value: str) -> str:
    value = value.strip().lower()
    return value[1:] if value.startswith("v") and value[1:].isdigit() else value


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a strict heal-readiness report for one volume.")
    parser.add_argument("volume", help="Volume number, e.g. 10 or v10")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero unless strict readiness passes.")
    args = parser.parse_args()

    volume = _normalize_volume(args.volume)
    state_data = gather_volume_data(volume)
    need = float(score_volume(state_data))
    vol_dir = ROOT / "volumes" / f"v{volume}"
    epub_path = vol_dir / "output" / f"volume_{volume}.epub"
    report = build_readiness_report(volume, state_data, need, epub_path)
    json_path, md_path = write_readiness_reports(report, vol_dir / "bugs_fixes")

    status = "PASS" if report["strict_ready"] else "FAIL"
    print(f"Heal readiness {status}: volume {volume} Need {need:.1f}, blockers={report['blocker_count']}, review_debt={report['review_debt_count']}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")

    if args.strict and not report["strict_ready"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
