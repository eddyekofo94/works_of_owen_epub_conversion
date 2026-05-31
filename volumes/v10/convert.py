#!/usr/bin/env python3
"""
Volume 10 — The Works of John Owen, Volume 10: Arminianism and the Death of Christ
Per-volume converter script.

Source type: ages_pdf

Usage:
    python3 volumes/v10/convert.py                   # full pipeline (extract + render)
    python3 volumes/v10/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v10/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 10

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V10_ARMINIANISM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Display of Arminianism:</p>
<p class="title-connector">Being a Discovery of the Old</p>
<p class="title-line-medium">Pelagian Idol, Free-Will,</p>
<p class="title-connector">with the New Goddess</p>
<p class="title-line-medium">Contingency,</p>
<p class="title-connector">Advancing Themselves into the Throne of God in Heaven, and Deposing His Sacred Providence from the Government of the World.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Known unto God are all his works from the beginning of the world." — Acts 15:18.</p></div>
</section>'''

_V10_DEATH_OF_DEATH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">The Death of Death</p>
<p class="title-connector">in the</p>
<p class="title-line-major">Death of Christ:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">A Treatise in Which the Whole Controversy about Universal Redemption Is Fully Discussed; the Reality and Efficacy of the Satisfaction of Christ Vindicated; and the Doctrine of Particular Redemption Confirmed and Established.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"He shall see of the travail of his soul, and shall be satisfied." — Isaiah 53:11.</p></div>
</section>'''

_V10_DEATH_OF_CHRIST_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">The Death of Christ;</p>
<p class="title-connector">the Price He Paid,</p>
<p class="title-connector">and the Purchase He Made.</p>
</section>'''

_V10_DIVINE_JUSTICE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Dissertation</p>
<p class="title-connector">on</p>
<p class="title-line-medium">Divine Justice;</p>
<p class="title-connector">or, the Claims of</p>
<p class="title-line-medium">Vindicatory Justice.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Wherein the Necessity of Punishing Sin Is Asserted, the Satisfaction of Christ Founded Thereon, and the Remission of Sins Through Him Vindicated.</p>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'A Display of Arminianism:': _V10_ARMINIANISM_TITLE_PAGE,
        'The Death of Death in the Death of Christ': _V10_DEATH_OF_DEATH_TITLE_PAGE,
        'The Death of Christ,': _V10_DEATH_OF_CHRIST_TITLE_PAGE,
        'A Dissertation on Divine Justice:': _V10_DIVINE_JUSTICE_TITLE_PAGE,
    },
    'text_replacements': {
        'Arminlan': 'Arminian',
        'Arminlanism': 'Arminianism',
        'Pelaglan': 'Pelagian',
        '119 "Infants': '"Infants',
        '120 "Neither': '"Neither',
        '134 "Whether': '"Whether',
        '169 " Can': '"Can',
        '202 "Herein': '"Herein',
        '206 "In': '"In',
    },
    'regex_replacements': {
        r'T\. M\[ore(\.?)\]': r'T. More\1',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
