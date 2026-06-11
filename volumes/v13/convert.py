#!/usr/bin/env python3
"""
Volume 13 — The Works of John Owen, Volume 13: Pastors, Schism, and Church Tracts
Per-volume converter script.

Usage:
    python3 volumes/v13/convert.py                   # full pipeline (extract + render)
    python3 volumes/v13/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v13/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 13 is a collection of shorter polemical and pastoral tracts on church
order, schism, nonconformity, toleration, and civil religion. Major works:
  - The Duty of Pastors and People Distinguished
  - Eshcol: A Cluster of the Fruit of Canaan
  - Of Schism / A Review of the True Nature of Schism
  - An Answer to a Late Treatise of Mr Cawdrey
  - A Brief Vindication of the Nonconformists
  - Truth and Innocence Vindicated
  - Two Questions Concerning the Power of the Supreme Magistrate
  - Indulgence and Toleration Considered
  - A Peace-offering
  - I. An Account of the Grounds and Reasons
  - II. The Case of Present Distresses
  - I. The State of the Kingdom / II. A Word of Advice to the Citizens of London
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 13

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V13_DUTY_PASTORS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Duty of</p>
<p class="title-line-major">Pastors and People</p>
<p class="title-line-major">Distinguished:</p>
<p class="title-connector">with a Further Vindication of the</p>
<p class="title-line-medium">Petitionary Confession of Faith</p>
<p class="title-connector">Against the Exceptions of</p>
<p class="title-line-medium">Mr D. Cawdrey.</p>
</section>'''

_V13_ESHCOL_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Eshcol:</p>
<p class="title-connector">A Cluster of the Fruit of Canaan,</p>
<p class="title-connector">Brought to the Borders of Israel;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Present State of the Gospel-Church</p>
<p class="title-line-medium">of Christ</p>
<p class="title-connector">Considered.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"And they came unto the brook of Eshcol, and cut down from thence a branch with one cluster of grapes." — Numbers 13:23.</p></div>
</section>'''

_V13_SCHISM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Of Schism:</p>
<p class="title-line-medium">The True Nature of It</p>
<p class="title-connector">Discovered and Considered,</p>
<p class="title-connector">with Reference to the</p>
<p class="title-line-medium">Present Differences in Religion.</p>
</section>'''

_V13_REVIEW_SCHISM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Review</p>
<p class="title-connector">of the</p>
<p class="title-line-medium">True Nature of Schism;</p>
<p class="title-connector">with a Vindication of the</p>
<p class="title-line-medium">Congregational Churches in England</p>
<p class="title-connector">from the Imputation Thereof.</p>
</section>'''

_V13_ANSWER_CAWDREY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">An Answer to a Late Treatise</p>
<p class="title-connector">of</p>
<p class="title-line-major">Mr Cawdrey</p>
<p class="title-connector">About the Nature of Schism.</p>
</section>'''

_V13_VINDICATION_NONCONFORMISTS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Brief Vindication</p>
<p class="title-connector">of the</p>
<p class="title-line-major">Nonconformists</p>
<p class="title-connector">from the Charge of Schism.</p>
</section>'''

_V13_TRUTH_INNOCENCE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Truth and Innocence</p>
<p class="title-line-major">Vindicated;</p>
<p class="title-connector">in a Survey of a Discourse Concerning</p>
<p class="title-line-medium">Ecclesiastical Polity,</p>
<p class="title-connector">and the Authority of the</p>
<p class="title-line-medium">Civil Magistrate Over the Consciences</p>
<p class="title-line-medium">of Men in Matters of Religion.</p>
</section>'''

_V13_TWO_QUESTIONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Two Questions Concerning</p>
<p class="title-line-medium">the Power of the</p>
<p class="title-line-major">Supreme Magistrate</p>
<p class="title-connector">About Religion,</p>
<p class="title-connector">and the Worship of God.</p>
</section>'''

_V13_INDULGENCE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Indulgence and Toleration</p>
<p class="title-line-major">Considered:</p>
<p class="title-connector">in a Letter unto a Person of Honour.</p>
</section>'''

_V13_PEACE_OFFERING_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Peace-offering,</p>
<p class="title-connector">in an Apology and Humble Plea for</p>
<p class="title-line-medium">Indulgence and Liberty of Conscience.</p>
</section>'''

_V13_GROUNDS_REASONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">I. An Account of the Grounds and Reasons</p>
<p class="title-connector">on Which</p>
<p class="title-line-medium">Protestant Dissenters Desire Their</p>
<p class="title-line-medium">Relief.</p>
</section>'''

_V13_PRESENT_DISTRESSES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">II. The Case of</p>
<p class="title-line-major">Present Distresses</p>
<p class="title-connector">on Nonconformists</p>
<p class="title-line-medium">Examined.</p>
</section>'''

_V13_STATE_KINGDOM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">I. The State of the Kingdom</p>
<p class="title-connector">with Respect to the</p>
<p class="title-line-medium">Present Bill Against Nonconformists.</p>
</section>'''

_V13_WORD_OF_ADVICE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">II. A Word of Advice</p>
<p class="title-connector">to the</p>
<p class="title-line-major">Citizens of London.</p>
</section>'''

_V13_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 13.</h1>

<h2 class="contents-treatise-title">THE DUTY OF PASTORS AND PEOPLE DISTINGUISHED</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch003.xhtml">Epistle Dedicatory to Sir Edward Scot</a></p>
<p class="contents-item"><a href="ch004.xhtml">Preface to the Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch005.xhtml">Of the administration of holy things among the patriarchs before the law</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch006.xhtml">Of the same among the Jews, and of the duty of that people distinct from their church-state</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch007.xhtml">Containing a digression concerning the name of "priests," the right of Christians to that title, etc.</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch008.xhtml">Of the duty of God's people in cases extraordinary concerning his worship</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch009.xhtml">Of the several ways of extraordinary calling to the teaching of others</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch010.xhtml">What assurance men extraordinarily called can give to others that they are so called</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch011.xhtml">The second way whereby a man may be called extraordinarily</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch012.xhtml">Of the liberty and duty of gifted uncalled Christians in the exercise of divers acts of God's worship</a></p>

<h2 class="contents-treatise-title">ESHCOL: A CLUSTER OF THE FRUIT OF CANAAN</h2>
<p class="contents-item"><a href="ch014.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch015.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch016.xhtml">Rules for Church Fellowship (Eshcol; a Cluster of the Fruit of Canaan)</a></p>

<h2 class="contents-treatise-title">OF SCHISM: THE TRUE NATURE OF IT STATED</h2>
<p class="contents-item"><a href="ch018.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch019.xhtml">Aggravations of the evil of schism, from the authority of the ancients</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch020.xhtml">The nature of schism to be determined from Scripture only</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch021.xhtml">Objections against the former discourse proposed to consideration</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch022.xhtml">Several acceptations in the Scripture of the name "church" — Of the church catholic, etc.</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch023.xhtml">Of the catholic church visible — Of the nature thereof</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch024.xhtml">Romanists' charge of schism on the account of separation from the church catholic examined</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch025.xhtml">Of a particular church; its nature — Frequently mentioned in Scripture</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch026.xhtml">Of the church of England — The charge of schism in the name thereof proposed and considered</a></p>

<h2 class="contents-treatise-title">A REVIEW OF THE TRUE NATURE OF SCHISM</h2>
<p class="contents-item"><a href="ch028.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch029.xhtml">To the Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch030.xhtml">Introductory observations</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch031.xhtml">An answer to the appendix of Mr. Cawdrey's charge</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch032.xhtml">A review of the charger's preface</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch033.xhtml">Of the nature of schism</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch034.xhtml">The scripture meaning of schism farther considered</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch035.xhtml">Of the church catholic visible, and separation from it</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch036.xhtml">Of the congregational church-state and separation</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch037.xhtml">Of Independentism and Donatism</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch038.xhtml">Of the charge of schism against congregational churches</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch039.xhtml">Independency no schism</a></p>

<h2 class="contents-treatise-title">AN ANSWER TO A LATE TREATISE ABOUT THE NATURE OF SCHISM</h2>
<p class="contents-item"><a href="ch041.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch042.xhtml">An Answer to Mr. Cawdrey's Book About Schism</a></p>

<h2 class="contents-treatise-title">A BRIEF VINDICATION OF THE NONCONFORMISTS FROM THE CHARGE OF SCHISM</h2>
<p class="contents-item"><a href="ch044.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch045.xhtml">A Brief Vindication of the Nonconformists</a></p>

<h2 class="contents-treatise-title">TRUTH AND INNOCENCE VINDICATED</h2>
<p class="contents-item"><a href="ch047.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch048.xhtml">A Survey of a Discourse Concerning Ecclesiastical Polity</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch049.xhtml">A survey of the first chapter</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch050.xhtml">A survey of the second chapter</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch051.xhtml">A survey of the third chapter</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch052.xhtml">A survey of the fourth chapter</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch053.xhtml">A survey of the fifth chapter</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch054.xhtml">A survey of the sixth chapter</a></p>

<h2 class="contents-treatise-title">TWO QUESTIONS CONCERNING THE POWER OF THE SUPREME MAGISTRATE</h2>
<p class="contents-item"><a href="ch056.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><b>Question I.</b> <a href="ch057.xhtml">First question considered</a></p>
<p class="contents-item"><b>Question II.</b> <a href="ch058.xhtml">Second question considered</a></p>
<p class="contents-item"><b>Question III.</b> <a href="ch059.xhtml">Third question considered</a></p>

<h2 class="contents-treatise-title">INDULGENCE AND TOLERATION CONSIDERED</h2>
<p class="contents-item"><a href="ch061.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch062.xhtml">Indulgence and Toleration Considered (A Letter to a Person of Honour)</a></p>

<h2 class="contents-treatise-title">A PEACE-OFFERING</h2>
<p class="contents-item"><a href="ch064.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch065.xhtml">A Peace-offering in an Apology for Indulgence</a></p>

<h2 class="contents-treatise-title">THE GROUNDS AND REASONS ON WHICH PROTESTANT DISSENTERS DESIRE TOLERATION</h2>
<p class="contents-item"><a href="ch067.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch068.xhtml">I. An Account of the Grounds and Reasons on Which Protestant Dissenters Desire Relief</a></p>
<p class="contents-item"><a href="ch070.xhtml">Prefatory Note: The Case of Present Distresses</a></p>
<p class="contents-item"><a href="ch071.xhtml">II. The Case of Present Distresses on Nonconformists Examined</a></p>

<h2 class="contents-treatise-title">THE STATE OF THE KINGDOM WITH RESPECT TO THE BILL AGAINST NONCONFORMISTS</h2>
<p class="contents-item"><a href="ch073.xhtml">Prefatory Note: Posthumous Tracts</a></p>
<p class="contents-item"><a href="ch074.xhtml">I. The State of the Kingdom with Respect to the Bill Against Nonconformists</a></p>
<p class="contents-item"><a href="ch076.xhtml">Prefatory Note: Advice to the Citizens of London</a></p>
<p class="contents-item"><a href="ch077.xhtml">II. A Word of Advice to the Citizens of London</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V13_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V13_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'The Duty of Pastors and People Distinguished:': _V13_DUTY_PASTORS_TITLE_PAGE,
        # Two JSON entries for Eshcol (one with comma, one with period)
        'Eshcol; a Cluster of the Fruit of Canaan,': _V13_ESHCOL_TITLE_PAGE,
        'Eshcol; a Cluster of the Fruit of Canaan.': _V13_ESHCOL_TITLE_PAGE,
        'Of Schism:': _V13_SCHISM_TITLE_PAGE,
        'A Review of the True Nature of Schism,': _V13_REVIEW_SCHISM_TITLE_PAGE,
        # OCR typo in JSON: "Treaties" instead of "Treatise"
        'An Answer to a Late Treaties of Mr. Cawdrey': _V13_ANSWER_CAWDREY_TITLE_PAGE,
        # Truncated at ~60 chars in JSON
        'A Brief Vindication of the Nonconformists From the Charge of Sc': _V13_VINDICATION_NONCONFORMISTS_TITLE_PAGE,
        'Truth and Innocence Vindicated;': _V13_TRUTH_INNOCENCE_TITLE_PAGE,
        'Two Questions Concerning the Power of the Supreme Magistrate': _V13_TWO_QUESTIONS_TITLE_PAGE,
        'Indulgence and Toleration Considered:': _V13_INDULGENCE_TITLE_PAGE,
        'A Peace-offering,': _V13_PEACE_OFFERING_TITLE_PAGE,
        'I. an Account of the Grounds and Reasons, Etc.': _V13_GROUNDS_REASONS_TITLE_PAGE,
        'II. the Case of Present Distresses, Etc.': _V13_PRESENT_DISTRESSES_TITLE_PAGE,
        'I. the State of the Kingdom, Etc,': _V13_STATE_KINGDOM_TITLE_PAGE,
        'II. a Word of Advice to the Citizens of London.': _V13_WORD_OF_ADVICE_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair OCR typo in body text
        'Late Treaties of Mr': 'Late Treatise of Mr',
        'Eccleslastical': 'Ecclesiastical',
        'Objects of the the same': 'Objects of the same',
        'principles of of human': 'principles of human',
        'increase and and love': 'increase and love',
        'put in in bar': 'put in bar',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
