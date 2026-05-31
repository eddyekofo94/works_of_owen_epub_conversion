#!/usr/bin/env python3
"""
Volume 7 — The Works of John Owen, Volume 7: Apostasy, Spiritually-Mindedness, Dominion of Sin
Per-volume converter script.

Usage:
    python3 volumes/v7/convert.py                   # full pipeline (extract + render)
    python3 volumes/v7/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v7/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Note: The chapter title for "Nature of Apostasy" is truncated at 60 characters in the
JSON intermediate file. The key below must match that truncated string exactly.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 7

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v7/intermediate/volume_7.json (including punctuation).
# NB: "Apostasy" title is truncated at 60 chars in the JSON.
# ---------------------------------------------------------------------------

_V7_APOSTASY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Nature of</p>
<p class="title-line-major">Apostasy</p>
<p class="title-connector">from the Profession of the Gospel</p>
<p class="title-connector">and the Punishment of Apostates Declared,</p>
<p class="title-connector">in an Exposition of</p>
<p class="title-line-medium">Hebrews 6:4–6.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For it is impossible for those who were once enlightened, and have tasted of the heavenly gift, and were made partakers of the Holy Ghost, and have tasted the good word of God, and the powers of the world to come, if they shall fall away, to renew them again unto repentance." — Hebrews 6:4–6.</p></div>
</section>'''

_V7_SPIRITUALLY_MINDED_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Grace and Duty of Being</p>
<p class="title-line-major">Spiritually Minded,</p>
<p class="title-connector">Declared and Practically Improved.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For to be carnally minded is death; but to be spiritually minded is life and peace." — Romans 8:6.</p></div>
</section>'''

_V7_DOMINION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Treatise</p>
<p class="title-connector">of the</p>
<p class="title-line-medium">Dominion of Sin and Grace.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For sin shall not have dominion over you: for ye are not under the law, but under grace." — Romans 6:14.</p></div>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        # Truncated at 60 chars in JSON — match exactly
        'The Nature of Apostasy From the Profession of the Gospel and Th': _V7_APOSTASY_TITLE_PAGE,
        'Grace and Duty of Being Spiritually Minded': _V7_SPIRITUALLY_MINDED_TITLE_PAGE,
        'A Treatise Of The Dominion of Sin and Grace': _V7_DOMINION_TITLE_PAGE,
    },
    'text_replacements': {
        'apostaey': 'apostasy',
        'apostate.s': 'apostates',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
