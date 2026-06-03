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


_V14_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 14.</h1>

<h2 class="contents-treatise-title">ANIMADVERSIONS ON A TREATISE ENTITLED "FIAT LUX"</h2>
<p class="contents-item"><a href="ch003.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch004.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch005.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch006.xhtml">Our author's preface, and his method</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch007.xhtml">Heathen pleas — General principles</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch008.xhtml">Motive, matter, and method of our author's book</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch009.xhtml">Contests about religion and reformation, schoolmen, etc.</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch010.xhtml">Obscurity of God, etc.</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch011.xhtml">Scripture vindicated</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch012.xhtml">Use of reason</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch013.xhtml">Jews' objections</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch014.xhtml">Protestant pleas</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch015.xhtml">Scripture, and new principles</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch016.xhtml">Story of religion</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch017.xhtml">Reformation</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch018.xhtml">Popish contradictions</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch019.xhtml">Mass</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch020.xhtml">Blessed Virgin</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch021.xhtml">Images</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch022.xhtml">Latin service</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch023.xhtml">Communion</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch024.xhtml">Saints</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch025.xhtml">Purgatory</a></p>
<p class="contents-item"><b>Chapter XXI.</b> <a href="ch026.xhtml">Pope</a></p>
<p class="contents-item"><b>Chapter XXII.</b> <a href="ch027.xhtml">Popery</a></p>

<h2 class="contents-treatise-title">A VINDICATION OF THE ANIMADVERSIONS ON "FIAT LUX"</h2>
<p class="contents-item"><a href="ch029.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch030.xhtml">To the Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch031.xhtml">Introductory considerations</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch032.xhtml">Vindication of the first chapter of the "Animadversions"</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch033.xhtml">A defense of the second chapter of the "Animadversions"</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch034.xhtml">Farther vindication of second chapter of the "Animadversions"</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch035.xhtml">Other principles of "Fiat Lux" re-examined</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch036.xhtml">Farther vindication of the second chapter of the "Animadversions"</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch037.xhtml">Unity of faith, wherein it consists</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch038.xhtml">Principles of Papists, whereon they proceed in religion</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch039.xhtml">Proposals from protestant principles tending unto moderation and unity</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch040.xhtml">Farther vindication of the second chapter of the "Animadversions"</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch041.xhtml">Judicious readers — Schoolmen the forgers of Popery</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch042.xhtml">False suppositions, causing false and absurd consequences</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch043.xhtml">Faith and charity of Roman Catholics</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch044.xhtml">Of reason — Jews' objections against Christ</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch045.xhtml">Pleas of Prelate Protestants — Christ the supreme head of the church</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch046.xhtml">The power assigned by Papists and Protestants unto kings</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch047.xhtml">Scripture — Story of the progress and declension of religion vindicated</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch048.xhtml">Reformation of religion — Papal contradictions</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch049.xhtml">Of preaching — The mass and the sacrifice of it</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch050.xhtml">Of the blessed Virgin</a></p>
<p class="contents-item"><b>Chapter XXI.</b> <a href="ch051.xhtml">Images — Doctrine of the Council of Trent</a></p>
<p class="contents-item"><b>Chapter XXII.</b> <a href="ch052.xhtml">Of Latin service</a></p>
<p class="contents-item"><b>Chapter XXIII.</b> <a href="ch053.xhtml">Communion</a></p>
<p class="contents-item"><b>Chapter XXIV.</b> <a href="ch054.xhtml">Heroes — Of the ass's head</a></p>

<h2 class="contents-treatise-title">THE CHURCH OF ROME NO SAFE GUIDE</h2>
<p class="contents-item"><a href="ch056.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch057.xhtml">Preface</a></p>
<p class="contents-item"><a href="ch058.xhtml">The Church of Rome No Safe Guide</a></p>

<h2 class="contents-treatise-title">SOME CONSIDERATIONS ABOUT UNION AMONG PROTESTANTS</h2>
<p class="contents-item"><a href="ch060.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch061.xhtml">Some Considerations About Union Among Protestants</a></p>

<h2 class="contents-treatise-title">THE STATE AND FATE OF THE PROTESTANT RELIGION</h2>
<p class="contents-item"><a href="ch063.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch064.xhtml">The State and Fate of the Protestant Religion</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V14_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V14_CONTENTS_PAGE,
    },
    'exclude_chapters': [
        'The Works of John Owen Vol. 14',
    ],
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
