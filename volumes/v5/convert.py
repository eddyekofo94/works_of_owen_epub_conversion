#!/usr/bin/env python3
"""
Volume 5 — The Works of John Owen, Volume 5: Justification by Faith
Per-volume converter script.

Source type: ages_pdf

Usage:
    python3 volumes/v5/convert.py                   # full pipeline (extract + render)
    python3 volumes/v5/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v5/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 5

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v5/intermediate/volume_5.json (including punctuation).
# ---------------------------------------------------------------------------

_V5_JUSTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Doctrine of</p>
<p class="title-line-major">Justification by Faith</p>
<p class="title-connector">through the Imputation of the</p>
<p class="title-line-medium">Righteousness of Christ,</p>
<p class="title-connector">Explained, Confirmed, and Vindicated.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Therefore being justified by faith, we have peace with God through our Lord Jesus Christ." — Romans 5:1.</p></div>
</section>'''

_V5_GOSPEL_GROUNDS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Gospel Grounds and Evidences</p>
<p class="title-connector">of the</p>
<p class="title-line-major">Faith of God's Elect.</p>
</section>'''

OVERRIDES = {
    'text_replacements': {
        # PDF OCR errors in 'To the Reader' preface
        'far although sunder': 'for although sundry',
        'consequent of it, yet': 'consequents of it, yet',
        'get the main weight': 'yet the main weight',
        'may books published': 'many books published',
        'artificial seasonings': 'artificial reasonings',
        'seasonings of carnal minds': 'reasonings of carnal minds',
        'well enough, find sufficiently': 'well enough, and sufficiently',
        'nulla pietatis commendatione, nulla': 'nulla pietatis commendatione, nullo',
        'prerumque': 'plerumque',
        'graneis': 'ganeis',
        'another writings of mine': 'any other writings of mine',
        'that is declared only': 'that it is declared only',
    },
    'treatise_title_overrides': {
        'The Doctrine of Justification By Faith,': _V5_JUSTIFICATION_TITLE_PAGE,
        "Gospel Grounds & Evidences of the Faith of God's Elect": _V5_GOSPEL_GROUNDS_TITLE_PAGE,
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
