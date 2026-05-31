#!/usr/bin/env python3
"""
Volume 6 — The Works of John Owen, Volume 6: Mortification, Temptation, and Psalm 130
Per-volume converter script.

Usage:
    python3 volumes/v6/convert.py                   # full pipeline (extract + render)
    python3 volumes/v6/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v6/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 6

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v6/intermediate/volume_6.json (including punctuation).
# ---------------------------------------------------------------------------

_V6_MORTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Of the</p>
<p class="title-line-major">Mortification of Sin</p>
<p class="title-connector">in Believers;</p>
<p class="title-line-medium">The Necessity, Nature, and Means of It:</p>
<p class="title-connector">with a Short Discourse of the</p>
<p class="title-line-medium">Dominion of Sin and Grace.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For if ye live after the flesh, ye shall die: but if ye through the Spirit do mortify the deeds of the body, ye shall live." — Romans 8:13.</p></div>
</section>'''

_V6_TEMPTATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Of Temptation:</p>
<p class="title-line-medium">The Nature and Power of It;</p>
<p class="title-line-medium">The Danger of Entering into It;</p>
<p class="title-connector">and the</p>
<p class="title-line-medium">Means of Preventing That Danger.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Watch and pray, that ye enter not into temptation: the spirit indeed is willing, but the flesh is weak." — Matthew 26:41.</p></div>
</section>'''

_V6_INDWELLING_SIN_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Nature, Power, Deceit,</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Prevalency</p>
<p class="title-connector">of the Remainders of</p>
<p class="title-line-major">Indwelling Sin</p>
<p class="title-connector">in Believers.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For I know that in me (that is, in my flesh,) dwelleth no good thing: for to will is present with me; but how to perform that which is good I find not." — Romans 7:18.</p></div>
</section>'''

_V6_PSALM_130_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Practical Exposition</p>
<p class="title-connector">upon</p>
<p class="title-line-major">Psalm 130;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Nature and Encouragement of Trust in God</p>
<p class="title-connector">in Depths of Affliction, Sin, and Desertion.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Out of the depths have I cried unto thee, O Lord." — Psalm 130:1.</p></div>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'Mortification of Sin in Believers;': _V6_MORTIFICATION_TITLE_PAGE,
        'Of Temptation:': _V6_TEMPTATION_TITLE_PAGE,
        'The Nature, Power, Deceit, and Prevalency': _V6_INDWELLING_SIN_TITLE_PAGE,
        'Practical Exposition Upon Psalm 130.;': _V6_PSALM_130_TITLE_PAGE,
    },
    'text_replacements': {
        'mortifled': 'mortified',
        'sanctifled': 'sanctified',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
