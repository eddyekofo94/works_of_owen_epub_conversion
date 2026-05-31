#!/usr/bin/env python3
"""
Volume 11 — The Works of John Owen, Volume 11: The Saints' Perseverance
Per-volume converter script.

Usage:
    python3 volumes/v11/convert.py                   # full pipeline (extract + render)
    python3 volumes/v11/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v11/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Note: The JSON chapter title reads "The Doctrine of the Saints Perseverance" —
the apostrophe in "Saints'" is missing due to OCR. The title page uses the
correct form; the text_replacement below also repairs it in the body text.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 11

# ---------------------------------------------------------------------------
# Treatise title pages
# The key must match the EXACT (OCR-corrupted) chapter title from the JSON.
# ---------------------------------------------------------------------------

_V11_PERSEVERANCE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Doctrine of the</p>
<p class="title-line-major">Saints' Perseverance,</p>
<p class="title-connector">Explained and Confirmed;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Certain Permanency of Their</p>
<p class="title-line-medium">Acceptance with God</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Sanctification Considered and Proved.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ." — Philippians 1:6.</p></div>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        # Key matches the OCR-corrupted JSON title (no apostrophe)
        'The Doctrine of the Saints Perseverance': _V11_PERSEVERANCE_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair missing apostrophe where it appears in body text
        "Saints Perseverance": "Saints' Perseverance",
        "saints perseverance": "saints' perseverance",
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
