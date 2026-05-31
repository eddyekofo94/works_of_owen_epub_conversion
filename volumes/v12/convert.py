#!/usr/bin/env python3
"""
Volume 12 — The Works of John Owen, Volume 12: Vindiciae Evangelicae; Hugo Grotius
Per-volume converter script.

Usage:
    python3 volumes/v12/convert.py                   # full pipeline (extract + render)
    python3 volumes/v12/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v12/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 12

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V12_VINDICIAE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Vindiciae Evangelicae;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Mystery of the Gospel Vindicated</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Socinianism Examined,</p>
<p class="title-connector">in the Consideration and Refutation of a</p>
<p class="title-line-medium">Catechism,</p>
<p class="title-connector">Published by John Biddle, M.A.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"But though we, or an angel from heaven, preach any other gospel unto you than that which we have preached unto you, let him be accursed." — Galatians 1:8.</p></div>
</section>'''

_V12_DEATH_JUSTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Of the Death of Christ,</p>
<p class="title-connector">and of</p>
<p class="title-line-major">Justification:</p>
<p class="title-connector">Being a Full Answer to Mr Richard Baxter's Exceptions</p>
<p class="title-connector">in His Treatise of</p>
<p class="title-line-medium">Redemption.</p>
</section>'''

_V12_GROTIUS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Review of the Annotations of</p>
<p class="title-line-major">Hugo Grotius,</p>
<p class="title-connector">in Reference to the Doctrine of the</p>
<p class="title-line-medium">Deity and Satisfaction of Christ.</p>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'Vindiciae Evangelicae;': _V12_VINDICIAE_TITLE_PAGE,
        'Of the Death of Christ, and of Justification:': _V12_DEATH_JUSTIFICATION_TITLE_PAGE,
        'A Review of the Annotations of Hugo Grotius.': _V12_GROTIUS_TITLE_PAGE,
    },
    'text_replacements': {
        'Socimanism': 'Socinianism',
        'Sociman': 'Socinian',
        'Blddle': 'Biddle',
        'Grotiua': 'Grotius',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
