#!/usr/bin/env python3
"""
Volume 2 — The Works of John Owen, Volume 2: Communion with God
Per-volume converter script.

Usage:
    python3 volumes/v2/convert.py                   # full pipeline (extract + render)
    python3 volumes/v2/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v2/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Add Volume 2-specific fixes to OVERRIDES only when a real V2 issue is found.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli


VOL = 2

OVERRIDES = {}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
