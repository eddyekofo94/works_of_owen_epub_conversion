#!/usr/bin/env python3
"""
Volume 8 — The Works of John Owen, Volume 8: Sermons to the Nation
Per-volume converter script.

Usage:
    python3 volumes/v8/convert.py                   # full pipeline (extract + render)
    python3 volumes/v8/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v8/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 8 is a sermon collection: 16 sermons preached on public occasions,
each preceded by a Prefatory Note and often a dedicatory epistle.
Structure: Sermon N. → Prefatory Note → [Dedicatory Epistle] → Sermon Title → Text.

Title page overrides are applied only to the major sermon-level markers
("Sermon N.") where a distinguished title page improves navigation.
Sermon 14 is singled out because it contains a substantial standalone
theological discourse embedded within the sermon series.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 8

_V8_SERMONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Sermons to the Nation</p>
<p class="title-connector">Preached on Public Occasions</p>
<p class="title-connector">before the Parliament and the Lord Protector,</p>
<p class="title-connector">1646–1659.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Sixteen Sermons, with Prefatory Notes and Dedicatory Epistles, on Themes of National Religion, Reformation, Providence, and the Advancement of Christ's Kingdom.</p>
</section>'''

_V8_SERMON14_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Sermon XIV.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-line-medium">The Testimony of the Church Is Not the</p>
<p class="title-line-medium">Only Nor the Chief Reason of Our Believing</p>
<p class="title-line-medium">the Scripture to Be the Word of God.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"They have Moses and the prophets; let them hear them." — Luke 16:29.</p></div>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'Preface.': _V8_SERMONS_TITLE_PAGE,
        'Sermon 14.': _V8_SERMON14_TITLE_PAGE,
    },
    'text_replacements': {
        'Cromwel ': 'Cromwell ',
        'Cromwel,': 'Cromwell,',
        'Cromwel.': 'Cromwell.',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
