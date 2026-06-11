#!/usr/bin/env python3
"""
Volume 2 — The Works of John Owen, Volume 2: Communion with God
Per-volume converter script.

Usage:
    python3 volumes/v2/convert.py                   # full pipeline (extract + render)
    python3 volumes/v2/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v2/convert.py --render-only     # Stage 2 only (JSON → EPUB)

The OVERRIDES dict is the place for any Volume 2-specific tweaks.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 2

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v2/intermediate/volume_2.json (including punctuation).
# ---------------------------------------------------------------------------

_V2_COMMUNION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Communion with God</p>
<p class="title-connector">the Father, Son, and Holy Ghost,</p>
<p class="title-connector">Each Person Distinctly, in</p>
<p class="title-line-medium">Love, Grace, and Consolation;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Saint's Fellowship with the Father,</p>
<p class="title-line-medium">Son, and Holy Ghost,</p>
<p class="title-connector">Unfolded.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Truly our fellowship is with the Father, and with his Son Jesus Christ." — 1 John 1:3.</p></div>
</section>'''

_V2_VINDICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Vindication</p>
<p class="title-connector">of Some Passages in a Discourse Concerning</p>
<p class="title-line-medium">Communion with God,</p>
<p class="title-connector">from the Exceptions of</p>
<p class="title-line-medium">William Sherlock.</p>
</section>'''

_V2_TRINITY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Brief Declaration</p>
<p class="title-connector">and</p>
<p class="title-line-major">Vindication</p>
<p class="title-connector">of the Doctrine of the</p>
<p class="title-line-medium">Holy Trinity;</p>
<p class="title-connector">as also of the</p>
<p class="title-line-medium">Person and Satisfaction of Christ:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Accommodated to the Capacity and Use of Such as May Be in Danger to Be Seduced, and the Direction of Plain Believers.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost." — Matthew 28:19.</p></div>
</section>'''

_V2_CONTENTS_PAGE = """<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 2.</h1>

<p class="contents-general-preface"><a href="ch001.xhtml">Preface</a></p>
<p class="contents-general-preface"><a href="ch002.xhtml">To the Reader</a></p>

<h2 class="contents-treatise-title">I. COMMUNION WITH GOD THE FATHER, SON, AND HOLY GHOST</h2>
<p class="contents-item"><a href="ch004.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch005.xhtml">Analysis.</a></p>
<h3 class="contents-part-title">Part I</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch007.xhtml">That the saints have communion with God — 1 John 1:3 considered to that purpose — ...</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch008.xhtml">That the saints have this communion distinctly with the Father, Son, and Spirit — ...</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch009.xhtml">Of the peculiar and distinct communion which the saints have with the Father — Obs...</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch010.xhtml">Inferences on the former doctrine concerning communion with the Father in love.</a></p>
<h3 class="contents-part-title">Part II. — Of Communion With the Son Jesus Christ</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch012.xhtml">Of the fellowship which the saints have with Jesus Christ the Son of God — That th...</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch013.xhtml">What it is wherein we have peculiar fellowship with the Lord Christ — This is in g...</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch014.xhtml">Of the way and manner whereby the saints hold communion with the Lord Christ as to...</a></p>
<p class="contents-item"><a href="ch015.xhtml">Digression 1.</a></p>
<p class="contents-item"><a href="ch016.xhtml">Digression 2.</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch017.xhtml">Of communion with Christ in a conjugal relation in respect of consequential affect...</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch018.xhtml">Other consequential affections: — 1 On the part of Christ — He values his saints —...</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch019.xhtml">Of communion with Christ in purchased grace — considered in respect of its rise an...</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch020.xhtml">The nature of purchased grace; referred to three heads: —</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch021.xhtml">How the saints hold communion with Christ as to their acceptation with God — What ...</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch022.xhtml">Of communion with Christ in holiness — The several acts ascribed unto the Lord Chr...</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch023.xhtml">Of communion with Christ in privileges — Of adoption; the nature of it, the conseq...</a></p>
<h3 class="contents-part-title">Part III. — Of Communion With the Holy Ghost.</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch025.xhtml">The foundation of our communion with the Holy ghost (John 16:1-7) opened at large ...</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch026.xhtml">Of the acting of the Holy Ghost in us, being bestowed on us — He worketh effectual...</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch027.xhtml">Of the things wherein we have communion with the Holy Ghost — He brings to remembr...</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch028.xhtml">The general consequences in the hearts of believers of the effects of the Holy Gho...</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch029.xhtml">Some observations and inferences from discourses foregoing concerning the Spirit —...</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch030.xhtml">Of particular communion with the Holy Ghost — Of preparation thereunto — Valuation...</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch031.xhtml">The general ways of the saints' acting in communion with the Holy Ghost.</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch032.xhtml">Particular directions for communion with the Holy Ghost.</a></p>

<h2 class="contents-treatise-title">II. A VINDICATION OF SOME PASSAGES IN A DISCOURSE CONCERNING COMMUNION</h2>
<p class="contents-item"><a href="ch034.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch035.xhtml">A Vindication</a></p>

<h2 class="contents-treatise-title">III. A BRIEF DECLARATION AND VINDICATION OF THE DOCTRINE OF THE TRINITY</h2>
<p class="contents-item"><a href="ch037.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch038.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch039.xhtml">Preface</a></p>
<p class="contents-item"><a href="ch040.xhtml">The Doctrine of the Holy Trinity Explained and Vindicated</a></p>
<p class="contents-item"><a href="ch041.xhtml">Of the Person of Christ</a></p>
<p class="contents-item"><a href="ch042.xhtml">Of the Satisfaction of Christ</a></p>
<p class="contents-item"><a href="ch043.xhtml">An Appendix</a></p>
</section>"""

OVERRIDES = {
    'contents_page_overrides': _V2_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V2_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'Communion With God the Father, Son, and Holy Ghost,': _V2_COMMUNION_TITLE_PAGE,
        'A Vindication of Some Passages in a Discourse Concerning Communion': _V2_VINDICATION_TITLE_PAGE,
        'A Brief Declaration and Vindication of the Doctrine of the Trinity': _V2_TRINITY_TITLE_PAGE,
    },
    'text_replacements': {
        'Sherloclc': 'Sherlock',
        'Sherlok': 'Sherlock',
        'soul. e is': 'soul. He is',
        '"ejusdem doloris socii.\'': '"ejusdem doloris socii."',
        'love of the Splint': 'love of the Spirit',
        'I a will': 'I will',
        'John 24:19': 'Joshua 24:19',
        '1 John 14:21': 'John 14:21',

        # Punctuation spacing fixes
        'Daniel Burgess . [f1]': 'Daniel Burgess. [f1]',
        'Part II . —': 'Part II. —',
        'distinguish,,': 'distinguish,',
        'Answer . ': 'Answer. ',
        'Objection . ': 'Objection. ',
        'Obj . ': 'Obj. ',
        '**1** . "How': '**1**. "How',

        # Volume 2 Biographical Expansions (Idempotent)
        'been Sherlock\'s': 'been William Sherlock\'s',
        'Tritheism. Sherlock': 'Tritheism. William Sherlock',
        'Sherlock\'s work against Owen': 'William Sherlock\'s work against Owen',
        'appeared in 1678, and Sherlock': 'appeared in 1678, and William Sherlock',
        'Vindication of Mr. Sherlock against': 'Vindication of William Sherlock against',
        'Mr. William Sherlock': 'William Sherlock',
        'Mr. Danson\'s': 'Thomas Danson\'s',
        'Mr. Danson': 'Thomas Danson',
        'Cavils of Mr. Danson.': 'Cavils of Thomas Danson.',
        'Mr. Lewis Stuckley': 'Lewis Stucley',
        'Mr Lewis Stuckley': 'Lewis Stucley',
        '_**DANIEL BURGESS**_': 'Daniel Burgess',
        'reading Quintus Curtius:': 'reading Quintus Curtius Rufus:',
        'Mr. Hooker, and that': 'Richard Hooker, and that',
        'Mr Hooker. Why do': 'Richard Hooker. Why do',
        'Reynolds, Whitaker, Hooker, Sutcliffe': 'John Rainolds, William Whitaker, Richard Hooker, Matthew Sutcliffe',
        'judgement of Hooker we': 'judgement of Richard Hooker we',
        'replied to Mr. Hooker, Dr. Jackson': 'replied to Richard Hooker, Thomas Jackson',
        'answering of Bishop Downham on': 'answering of George Downham on',
        'Mr Polwheil\'s book': 'Theophilus Polwhele\'s book',
        'Mr Polwheil': 'Theophilus Polwhele',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
