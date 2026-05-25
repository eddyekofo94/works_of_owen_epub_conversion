#!/usr/bin/env python3
"""
Volume 3 — The Works of John Owen, Volume 3: The Holy Spirit
Per-volume converter script.

Usage:
    python3 volumes/v3/convert.py                   # full pipeline (extract + render)
    python3 volumes/v3/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v3/convert.py --render-only     # Stage 2 only (JSON → EPUB)

The OVERRIDES dict below is the place for any Volume 3-specific tweaks.
Most volumes start with an empty dict and grow only when a genuine
volume-specific issue is discovered.
"""

import sys
import os

# Ensure the project root is on the path regardless of where this is invoked from
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 3

OVERRIDES = {}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()