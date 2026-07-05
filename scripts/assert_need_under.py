#!/usr/bin/env python3
"""Fail-closed Need score gate for heal workflows.

Usage:
  .venv/bin/python3 scripts/assert_need_under.py 10 1.0
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.report_volume_state import gather_volume_data, score_volume


def _normalize_volume(value: str) -> str:
    value = value.strip().lower()
    return value[1:] if value.startswith("v") and value[1:].isdigit() else value


def _read_need(volume: str) -> float:
    data = gather_volume_data(volume)
    if data.get("qa_level") == "NONE":
        raise SystemExit(f"Volume {volume} has no QA reports; cannot assert Need score")
    return float(score_volume(data))


def main() -> int:
    parser = argparse.ArgumentParser(description="Assert a volume Need score is below a threshold.")
    parser.add_argument("volume", help="Volume number, e.g. 10 or v10")
    parser.add_argument("threshold", type=float, help="Exclusive upper bound, e.g. 1.0")
    args = parser.parse_args()

    volume = _normalize_volume(args.volume)
    need = _read_need(volume)
    if need < args.threshold:
        print(f"Need gate PASS: volume {volume} Need {need:.1f} < {args.threshold:g}")
        return 0

    print(
        f"Need gate FAIL: volume {volume} Need {need:.1f} >= {args.threshold:g}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
