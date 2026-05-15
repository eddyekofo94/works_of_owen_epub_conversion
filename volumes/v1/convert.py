#!/usr/bin/env python3
"""
Volume 1 — The Works of John Owen, Volume 1: The Glory of Christ
Per-volume converter script.

Usage:
    python3 volumes/v1/convert.py                   # full pipeline (extract + render)
    python3 volumes/v1/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v1/convert.py --render-only     # Stage 2 only (JSON → EPUB)

The OVERRIDES dict below is the place for any Volume 1-specific tweaks.
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

from extract import extract_volume
from render import render_volume

VOL = 1

OVERRIDES = {
    # Volume 1 works correctly with all defaults.
    # Add keys here as v1-specific issues are discovered, for example:
    #   'front_matter_pages': 12,   # if auto-detection scans too many/few pages
    #   'body_start_hint': 7,       # override healer page detection
}


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description=f'Convert Owen Works Volume {VOL}',
    )
    parser.add_argument(
        '--extract-only', action='store_true',
        help='Run Stage 1 only (PDF → JSON intermediate)',
    )
    parser.add_argument(
        '--render-only', action='store_true',
        help='Run Stage 2 only (JSON → EPUB, requires existing intermediate)',
    )
    args = parser.parse_args()

    if args.render_only and args.extract_only:
        parser.error('Cannot use both --extract-only and --render-only')

    if not args.render_only:
        print(f'=== Volume {VOL}: Stage 1 — Extract ===')
        extract_volume(VOL, overrides=OVERRIDES)

    if not args.extract_only:
        print(f'=== Volume {VOL}: Stage 2 — Render ===')
        render_volume(VOL, overrides=OVERRIDES)

    print(f'=== Volume {VOL}: Done ===')


if __name__ == '__main__':
    main()
