#!/usr/bin/env python3
"""
Volume 2 — The Works of John Owen, Volume 2: Communion with God
Per-volume converter script.

Usage:
    python3 volumes/v2/convert.py                   # full pipeline (extract + render)
    python3 volumes/v2/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v2/convert.py --render-only     # Stage 2 only (JSON → EPUB)

The OVERRIDES dict is the place for any Volume 2-specific tweaks.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 2

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v2/intermediate/volume_2.json (including punctuation).
# ---------------------------------------------------------------------------

_V2_COMMUNION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Communion with God</p>
<p class="title-connector">the Father, Son, and Holy Ghost,</p>
<p class="title-connector">Each Person Distinctly, in</p>
<p class="title-line-medium">Love, Grace, and Consolation;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Saint's Fellowship with the Father,</p>
<p class="title-line-medium">Son, and Holy Ghost,</p>
<p class="title-connector">Unfolded.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Truly our fellowship is with the Father, and with his Son Jesus Christ." — 1 John 1:3.</p></div>
</section>'''

_V2_VINDICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Vindication</p>
<p class="title-connector">of Some Passages in a Discourse Concerning</p>
<p class="title-line-medium">Communion with God,</p>
<p class="title-connector">from the Exceptions of</p>
<p class="title-line-medium">William Sherlock.</p>
</section>'''

_V2_TRINITY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Brief Declaration</p>
<p class="title-connector">and</p>
<p class="title-line-major">Vindication</p>
<p class="title-connector">of the Doctrine of the</p>
<p class="title-line-medium">Holy Trinity;</p>
<p class="title-connector">as also of the</p>
<p class="title-line-medium">Person and Satisfaction of Christ:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Accommodated to the Capacity and Use of Such as May Be in Danger to Be Seduced, and the Direction of Plain Believers.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost." — Matthew 28:19.</p></div>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'Communion With God the Father, Son, and Holy Ghost,': _V2_COMMUNION_TITLE_PAGE,
        'A Vindication of Some Passages in a Discourse Concerning Communion': _V2_VINDICATION_TITLE_PAGE,
        'A Brief Declaration and Vindication of the Doctrine of the Trinity': _V2_TRINITY_TITLE_PAGE,
    },
    'text_replacements': {
        'Sherloclc': 'Sherlock',
        'Sherlok': 'Sherlock',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
