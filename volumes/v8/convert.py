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

_V8_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 8.</h1>

<h2 class="contents-treatise-title">SERMONS TO THE NATION</h2>
<p class="contents-item"><a href="ch001.xhtml">Preface</a></p>

<p class="contents-item"><b>Sermon I.</b> <a href="ch004.xhtml">A Vision of Unchangeable, Free Mercy in Sending the Means of Grace</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch003.xhtml">Prefatory Note</a> | <a href="ch005.xhtml">A Short Defensative</a> | <a href="ch006.xhtml">A Country Essay</a></p>

<p class="contents-item"><b>Sermon II.</b> <a href="ch010.xhtml">A Memorial of the Deliverance of Essex County, and Committee</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch008.xhtml">Prefatory Note</a> | <a href="ch009.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon III.</b> <a href="ch014.xhtml">Righteous Zeal Encouraged by Divine Protection</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch012.xhtml">Prefatory Note</a> | <a href="ch013.xhtml">Dedicatory Epistle</a> | <a href="ch015.xhtml">Of Toleration</a></p>

<p class="contents-item"><b>Sermon IV.</b> <a href="ch019.xhtml">The Steadfastness of the Promises, and the Sinfulness of Staggering</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch017.xhtml">Prefatory Note</a> | <a href="ch018.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon V.</b> <a href="ch023.xhtml">The Shaking and Translating of Heaven and Earth</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch021.xhtml">Prefatory Note</a> | <a href="ch022.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon VI.</b> <a href="ch027.xhtml">The Branch of the Lord the Beauty of Zion</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch025.xhtml">Prefatory Note</a> | <a href="ch026.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon VII.</b> <a href="ch031.xhtml">Advantage of the Kingdom of Christ</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch029.xhtml">Prefatory Note</a> | <a href="ch030.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon VIII.</b> <a href="ch035.xhtml">The Laboring Saint's Dismission to Rest</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch033.xhtml">Prefatory Note</a> | <a href="ch034.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon IX.</b> <a href="ch038.xhtml">Christ's Kingdom and the Magistrate's Power</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch037.xhtml">Prefatory Note</a></p>

<p class="contents-item"><b>Sermon X.</b> <a href="ch042.xhtml">God's Work in Founding Zion, and His People’s Duty Thereupon</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch040.xhtml">Prefatory Note</a> | <a href="ch041.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon XI.</b> <a href="ch046.xhtml">God's Presence With a People the Spring of Their Prosperity</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch044.xhtml">Prefatory Note</a> | <a href="ch045.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon XII.</b> <a href="ch050.xhtml">The Glory and Interest of Nations Professing the Gospel</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch048.xhtml">Prefatory Note</a> | <a href="ch049.xhtml">Dedicatory Epistle</a></p>

<p class="contents-item"><b>Sermon XIII.</b> <a href="ch053.xhtml">How We May Bring Our Hearts to Bear Reproofs</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch052.xhtml">Prefatory Note</a></p>

<p class="contents-item"><b>Sermon XIV.</b> <a href="ch055.xhtml">The Testimony of the Church Is Not the Only Nor the Chief Reason of Our Believing</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  <a href="ch056.xhtml">Exception I</a> | 
  <a href="ch057.xhtml">Exception II</a> | 
  <a href="ch058.xhtml">Exception III</a> | 
  <a href="ch059.xhtml">Exception IV</a> | 
  <a href="ch060.xhtml">Exception V</a>
</p>

<p class="contents-item"><b>Sermon XV.</b> <a href="ch062.xhtml">The Chamber of Imagery in the Church of Rome Laid Open</a></p>

<p class="contents-item"><b>Sermon XVI.</b> <a href="ch066.xhtml">An Humble Testimony Unto the Goodness and Severity of God</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;"><a href="ch064.xhtml">Prefatory Note</a> | <a href="ch065.xhtml">To the Reader</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V8_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V8_CONTENTS_PAGE,
    },
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
