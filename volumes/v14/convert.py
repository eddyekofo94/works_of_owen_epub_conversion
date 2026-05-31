#!/usr/bin/env python3
"""
Volume 14 — The Works of John Owen, Volume 14: The Fiat Lux Controversy
Per-volume converter script.

Usage:
    python3 volumes/v14/convert.py                   # full pipeline (extract + render)
    python3 volumes/v14/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v14/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 14 contains Owen's anti-Roman Catholic writings:
  - Animadversions on "Fiat Lux" (and its Vindication)
  - The Church of Rome No Safe Guide
  - Some Considerations About Union Among Protestants
  - The State and Fate of the Protestant Religion

Note: The JSON chapter title uses "fiat Lux" (lowercase f) due to OCR;
the title page renders the correct capitalisation "Fiat Lux".
The OCR artifact "Ì" (capital I with grave accent) appears in place of
apostrophes in some possessives — e.g. "AuthorÌs" for "Author's".
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

import re

VOL = 14

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V14_ANIMADVERSIONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Animadversions</p>
<p class="title-connector">on a Treatise Entitled</p>
<p class="title-line-medium">"Fiat Lux":</p>
<p class="title-connector">or, an Examination of the Seasonableness, Usefulness,</p>
<p class="title-connector">Tendency, and Reasonableness of a Book Written by</p>
<p class="title-line-medium">Ν. N.</p>
<p class="title-connector">and Entitled "Fiat Lux."</p>
</section>'''

_V14_VINDICATION_ANIMADVERSIONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Vindication</p>
<p class="title-connector">of the</p>
<p class="title-line-medium">Animadversions on "Fiat Lux,"</p>
<p class="title-connector">from the Exceptions and Reasonings of J. V. in His Book</p>
<p class="title-connector">Entitled</p>
<p class="title-line-medium">Veteris Ecclesiae Vindiciae.</p>
</section>'''

_V14_ROME_NO_GUIDE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Church of Rome</p>
<p class="title-line-major">No Safe Guide;</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Or, Reasons to Prove That No Rational Man Who Considers the Inconsistency of Its Doctrine About Scripture, Tradition, and Interpretation Can with Safety Be Led by It.</p>
</section>'''

_V14_UNION_PROTESTANTS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Some Considerations</p>
<p class="title-connector">About</p>
<p class="title-line-major">Union Among Protestants,</p>
<p class="title-connector">and the Preservation of the</p>
<p class="title-line-medium">Interest of the Protestant Religion</p>
<p class="title-connector">in This Nation.</p>
</section>'''

_V14_PROTESTANT_RELIGION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The State and Fate of the</p>
<p class="title-line-major">Protestant Religion.</p>
</section>'''


def _postprocess_v14_ocr_apostrophes(html, chapter):
    """Replace OCR artifact Ì (I-grave) used in place of apostrophes in possessives."""
    # Pattern: word-character + Ì + s (e.g. "AuthorÌs" → "Author's")
    html = re.sub(r'(\w)Ìs\b', r"\1's", html)
    # Also handle ì (lowercase i-grave) in the same position
    html = re.sub(r'(\w)ìs\b', r"\1's", html)
    return html


OVERRIDES = {
    'treatise_title_overrides': {
        # Key matches exact (OCR-lowercase) JSON title
        'Animadversions on Treatise Entitled "fiat Lux"': _V14_ANIMADVERSIONS_TITLE_PAGE,
        'A Vindication of the Animadversions on "fiat Lux"': _V14_VINDICATION_ANIMADVERSIONS_TITLE_PAGE,
        'The Church of Rome No Safe Guide': _V14_ROME_NO_GUIDE_TITLE_PAGE,
        'Some Considerations About Union Among Protestants,': _V14_UNION_PROTESTANTS_TITLE_PAGE,
        'Nature of the Protestant Religion;': _V14_PROTESTANT_RELIGION_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair OCR lowercase in body text where "fiat Lux" appears
        '"fiat Lux"': '"Fiat Lux"',
        'fiat lux': 'Fiat Lux',
        # Repair the volume-level chapter header OCR corruption
        'The Works of John Owen Vol. 14': 'The Works of John Owen, Volume 14',
    },
    'html_postprocess_hook': _postprocess_v14_ocr_apostrophes,
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
