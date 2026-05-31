#!/usr/bin/env python3
"""
Volume 9 — The Works of John Owen, Volume 9: Posthumous Sermons and Cases of Conscience
Per-volume converter script.

Usage:
    python3 volumes/v9/convert.py                   # full pipeline (extract + render)
    python3 volumes/v9/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v9/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 9 contains:
  - Posthumous Sermons Parts 1–4 (sermons published after Owen's death)
  - Several Practical Cases of Conscience Resolved (14 discourses)

The four sermon parts and the Cases of Conscience each receive a title page.
Individual sermon numbers do not get individual title pages.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 9

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V9_PART1_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons</p>
<p class="title-connector">Part I.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Sermons Preached on Various Occasions, Published After the Author's Death.</p>
</section>'''

_V9_PART2_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons</p>
<p class="title-connector">Part II.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Including Several Practical Cases of Conscience Resolved.</p>
</section>'''

_V9_PART3_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons</p>
<p class="title-connector">Part III.</p>
</section>'''

_V9_PART4_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons</p>
<p class="title-connector">Part IV.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Dedicated to Mrs Cooke of Stoke Newington.</p>
</section>'''

_V9_CASES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Several Practical</p>
<p class="title-line-major">Cases of Conscience</p>
<p class="title-connector">Resolved.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Fourteen Discourses Wherein Difficult and Important Cases of Practical Godliness Are Considered and Determined.</p>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'Posthumous Sermons - Part 1': _V9_PART1_TITLE_PAGE,
        'Posthumous Sermons - Part 2': _V9_PART2_TITLE_PAGE,
        'Posthumous Sermons - Part 3': _V9_PART3_TITLE_PAGE,
        'Posthumous Sermons - Part 4': _V9_PART4_TITLE_PAGE,
        'Several Practical Cases of Conscience Resolved.': _V9_CASES_TITLE_PAGE,
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
