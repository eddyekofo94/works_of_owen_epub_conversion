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

import re

# Re-import rendering constants that Catechism logic uses
from render import SCRIPTURE_BOOK_RE

VOL = 1

def _coalesce_v1_catechism_paragraphs(paragraphs):
    """V1-specific: Merge scripture reference paragraphs into the preceding Catechism answer."""
    if not paragraphs:
        return []
    out = []
    for para in paragraphs:
        stripped = para.strip()
        # If this paragraph looks like a bare scripture proof list and the 
        # previous paragraph was an Answer, merge them.
        # Allow leading digits/item markers (Issue 26)
        is_proof = re.match(rf'^(?:\d{{1,3}}\.?\s+)?(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b', stripped, re.I)
        if is_proof and out and re.match(r'^(?:\*\*)?(?:A\.|Ans\.)', out[-1].strip(), re.I):
            # Join with a space (Issue 16)
            out[-1] = out[-1].rstrip() + " " + stripped
        else:
            out.append(para)
    return out

OVERRIDES = {
    'text_replacements': {
        'Charneck': 'Charnock',
        'storage': 'strange',
        'whoso': 'whose',
        'se largely': 'so largely',
        'prevailing task': 'prevailing taste',
        'whoso name': 'whose name',
        'whoso human': 'whose human',
        'secretes': 'secrets',
        'on]y': 'only',
        'name]y': 'namely',
        'learned': 'learned',
        'learnt': 'learnt',
        'learning': 'learning',
        'faithfullness': 'faithfulness',
        '( 8)': ', 8',
        'John 16:1516:15': 'John 16:15',
        '1 John 5:205:20': '1 John 5:20',
        'Romans 1:1Romans': 'Romans 1:1',
        'Matthew 4:1Matthew 4': 'Matthew 4:1',
        'considered?”': 'considered?',
        'Objection .': 'Objection.',
        'Ans .': 'Ans.',
        'Q .': 'Q.',
        'To object of Dr. Owen in this treatise': 'The object of Dr. Owen in this treatise',
        'simple vague and defective': 'simply vague and defective',
        'these apprehensions of Own.': 'these apprehensions of Owen.',
        'The Christology of Owens has always been highly valued': 'The Christology of Owen has always been highly valued',
        'They were among the firsts as the other treatises': 'They were among the first, as the other treatises',
        'publish all the treatises of ushered under their auspices into public notice': 'publish all the treatises of Owen in volumes corresponding in size and appearance with the one ushered under their auspices into public notice',
        'This being the [f8] [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
        'This being the [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    },
    # Volume 1 Hook: Specialized paragraph merging for Catechisms
    'paragraph_coalesce_hook': _coalesce_v1_catechism_paragraphs,
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
