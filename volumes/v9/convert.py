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

_V9_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 9.</h1>

<h2 class="contents-treatise-title">I. POSTHUMOUS SERMONS — PART I</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note</a></p>
<p class="contents-item"><b>Sermon.</b> <a href="ch003.xhtml">Seasonable Words for English Protestants</a></p>

<h2 class="contents-treatise-title">II. POSTHUMOUS SERMONS — PART II</h2>
<p class="contents-item"><a href="ch005.xhtml">Prefatory Note</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <b>Sermons:</b>
  <a href="ch006.xhtml">I</a>, <a href="ch007.xhtml">II</a>, <a href="ch008.xhtml">III</a>, <a href="ch009.xhtml">IV</a>, <a href="ch010.xhtml">V</a>, <a href="ch011.xhtml">VI</a>, <a href="ch012.xhtml">VII</a>, <a href="ch013.xhtml">VIII</a>, <a href="ch014.xhtml">IX</a>, <a href="ch015.xhtml">X</a>, <a href="ch016.xhtml">XI</a>, <a href="ch017.xhtml">XII</a>, <a href="ch018.xhtml">XIII</a>, <a href="ch019.xhtml">XIV</a>, <a href="ch020.xhtml">XV</a>, <a href="ch021.xhtml">XVI</a>, <a href="ch022.xhtml">XVII</a>, <a href="ch023.xhtml">XVIII</a>, <a href="ch024.xhtml">XIX</a>, <a href="ch025.xhtml">XX</a>, <a href="ch026.xhtml">XXI</a>, <a href="ch027.xhtml">XXII</a>, <a href="ch028.xhtml">XXIII</a>, <a href="ch029.xhtml">XXIV</a>, <a href="ch030.xhtml">XXV</a>, <a href="ch031.xhtml">XXVI</a>, <a href="ch032.xhtml">XXVII</a>, <a href="ch033.xhtml">XXVIII</a>, <a href="ch034.xhtml">XXIX</a>, <a href="ch035.xhtml">XXX</a>
</div>

<h2 class="contents-treatise-title">III. SEVERAL PRACTICAL CASES OF CONSCIENCE RESOLVED</h2>
<p class="contents-item"><a href="ch037.xhtml">Prefatory Note</a></p>
<p class="contents-item" style="font-size: 0.9em; margin-bottom: 0.4em;"><b>Discourses:</b></p>
<div style="font-size: 0.88em; line-height: 1.5; margin-left: 1.5em; color: #555; margin-bottom: 1.5em;">
  <a href="ch038.xhtml">I. Inner Peace</a> | 
  <a href="ch039.xhtml">II. Self-Examination</a> | 
  <a href="ch040.xhtml">III. Backsliding</a> | 
  <a href="ch041.xhtml">IV. Spiritual Decays</a> | 
  <a href="ch042.xhtml">V. Heart-Purging</a> | 
  <a href="ch043.xhtml">VI. Coldness in Duty</a> | 
  <a href="ch044.xhtml">VII. Spiritual Mindedness</a> | 
  <a href="ch045.xhtml">VIII. Temptations</a> | 
  <a href="ch046.xhtml">IX. Family Worship</a> | 
  <a href="ch047.xhtml">X. Ministerial Duties</a> | 
  <a href="ch048.xhtml">XI. Church Fellowship</a> | 
  <a href="ch049.xhtml">XII. Lord’s Supper</a> | 
  <a href="ch050.xhtml">XIII. Brotherly Love</a> | 
  <a href="ch051.xhtml">XIV. Perseverance</a>
</div>

<h2 class="contents-treatise-title">IV. POSTHUMOUS SERMONS — PART III</h2>
<p class="contents-item"><a href="ch053.xhtml">Prefatory Note</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <b>Sermons:</b>
  <a href="ch054.xhtml">I</a>, <a href="ch055.xhtml">II</a>, <a href="ch056.xhtml">III</a>, <a href="ch057.xhtml">IV</a>, <a href="ch058.xhtml">V</a>, <a href="ch059.xhtml">VI</a>, <a href="ch060.xhtml">VII</a>, <a href="ch061.xhtml">VIII</a>, <a href="ch062.xhtml">IX</a>, <a href="ch063.xhtml">X</a>, <a href="ch064.xhtml">XI</a>, <a href="ch065.xhtml">XII</a>, <a href="ch066.xhtml">XIII</a>
</div>

<h2 class="contents-treatise-title">V. DISCOURSES SUITABLE TO THE LORD’S SUPPER (PART IV)</h2>
<p class="contents-item"><a href="ch068.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch069.xhtml">To Mrs Cooke of Stoke Newington</a></p>
<p class="contents-item"><a href="ch070.xhtml">Preface</a></p>
<p class="contents-item" style="font-size: 0.9em; margin-bottom: 0.4em;"><b>Sacramental Discourses:</b></p>
<div style="font-size: 0.88em; line-height: 1.6; margin-left: 1.5em; color: #555; margin-bottom: 1.5em;">
  <a href="ch071.xhtml">Discourse 1</a>, <a href="ch072.xhtml">Discourse 2</a>, <a href="ch073.xhtml">Discourse 3</a>, <a href="ch074.xhtml">Discourse 4</a>, <a href="ch075.xhtml">Discourse 5</a>, <a href="ch076.xhtml">Discourse 6</a>, <a href="ch077.xhtml">Discourse 7</a>, <a href="ch078.xhtml">Discourse 8</a>, <a href="ch079.xhtml">Discourse 9</a>, <a href="ch080.xhtml">Discourse 10</a>, <a href="ch081.xhtml">Discourse 11</a>, <a href="ch082.xhtml">Discourse 12</a>, <a href="ch083.xhtml">Discourse 13</a>, <a href="ch084.xhtml">Discourse 14</a>, <a href="ch085.xhtml">Discourse 15</a>, <a href="ch086.xhtml">Discourse 16</a>, <a href="ch087.xhtml">Discourse 17</a>, <a href="ch088.xhtml">Discourse 18</a>, <a href="ch089.xhtml">Discourse 19</a>, <a href="ch090.xhtml">Discourse 20</a>, <a href="ch091.xhtml">Discourse 21</a>, <a href="ch092.xhtml">Discourse 22</a>, <a href="ch093.xhtml">Discourse 23</a>, <a href="ch094.xhtml">Discourse 24</a>, <a href="ch095.xhtml">Discourse 25</a>
</div>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V9_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V9_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'Posthumous Sermons — Part 1': _V9_PART1_TITLE_PAGE,
        'Posthumous Sermons — Part 2': _V9_PART2_TITLE_PAGE,
        'Posthumous Sermons — Part 3': _V9_PART3_TITLE_PAGE,
        'Posthumous Sermons — Part 4': _V9_PART4_TITLE_PAGE,
        'Several Practical Cases of Conscience Resolved.': _V9_CASES_TITLE_PAGE,
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
