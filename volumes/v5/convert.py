#!/usr/bin/env python3
"""
Volume 5 — The Works of John Owen, Volume 5: Justification by Faith
Per-volume converter script.

Source type: ages_pdf

Usage:
    python3 volumes/v5/convert.py                   # full pipeline (extract + render)
    python3 volumes/v5/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v5/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 5

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v5/intermediate/volume_5.json (including punctuation).
# ---------------------------------------------------------------------------

_V5_JUSTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Doctrine of</p>
<p class="title-line-major">Justification by Faith</p>
<p class="title-connector">through the Imputation of the</p>
<p class="title-line-medium">Righteousness of Christ,</p>
<p class="title-connector">Explained, Confirmed, and Vindicated.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Therefore being justified by faith, we have peace with God through our Lord Jesus Christ." — Romans 5:1.</p></div>
</section>'''

_V5_GOSPEL_GROUNDS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Gospel Grounds and Evidences</p>
<p class="title-connector">of the</p>
<p class="title-line-major">Faith of God's Elect.</p>
</section>'''

_V5_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 5.</h1>

<h2 class="contents-treatise-title">I. THE DOCTRINE OF JUSTIFICATION BY FAITH</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch003.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch004.xhtml">General Considerations</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch005.xhtml">Justifying Faith</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch006.xhtml">The Nature of Justifying Faith</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch007.xhtml">The Use of Faith in Justification</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch008.xhtml">Of Justification</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch009.xhtml">The Continuation of Justification</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch010.xhtml">Evangelical Personal Righteousness</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch011.xhtml">Imputation, and the Nature of It</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch012.xhtml">Imputation of the Sins of the Church Unto Christ</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch013.xhtml">The Formal Cause of Justification</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch014.xhtml">Arguments for Justification</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch015.xhtml">The Nature of the Obedience That God Requires</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch016.xhtml">The Imputation of the Obedience of Christ</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch017.xhtml">The Nature of Justification Proved</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch018.xhtml">The Exclusion of All Sorts of Works</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch019.xhtml">Faith Alone</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch020.xhtml">The Truth Pleaded Farther</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch021.xhtml">Testimonies Out of the Evangelists Considered</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch022.xhtml">The Nature of Justification (Romans 4:3-8)</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch023.xhtml">Objections Against the Doctrine of Justification</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch024.xhtml">Doctrine of the Apostle James Concerning Faith</a></p>

<h2 class="contents-treatise-title">II. GOSPEL GROUNDS AND EVIDENCES OF THE FAITH OF GOD'S ELECT</h2>
<p class="contents-item"><a href="ch026.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch027.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch028.xhtml">Evidences of the Faith of God’s Elect</a></p>
<p class="contents-item"><b>Section I.</b> <a href="ch029.xhtml">How Does Saving Faith Approve of This Way?</a></p>
<p class="contents-item"><b>Section II.</b> <a href="ch030.xhtml">The Second Evidence</a></p>
<p class="contents-item"><b>Section III.</b> <a href="ch031.xhtml">The Third Evidence</a></p>
<p class="contents-item"><b>Section IV.</b> <a href="ch032.xhtml">The Fourth Evidence</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V5_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V5_CONTENTS_PAGE,
    },
    'text_replacements': {
        # PDF OCR errors in 'To the Reader' preface
        'far although sunder': 'for although sundry',
        'consequent of it, yet': 'consequents of it, yet',
        'get the main weight': 'yet the main weight',
        'may books published': 'many books published',
        'artificial seasonings': 'artificial reasonings',
        'seasonings of carnal minds': 'reasonings of carnal minds',
        'well enough, find sufficiently': 'well enough, and sufficiently',
        'nulla pietatis commendatione, nulla': 'nulla pietatis commendatione, nullo',
        'prerumque': 'plerumque',
        'graneis': 'ganeis',
        'another writings of mine': 'any other writings of mine',
        'that is declared only': 'that it is declared only',
    },
    'treatise_title_overrides': {
        'The Doctrine of Justification By Faith,': _V5_JUSTIFICATION_TITLE_PAGE,
        "Gospel Grounds & Evidences of the Faith of God's Elect": _V5_GOSPEL_GROUNDS_TITLE_PAGE,
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
