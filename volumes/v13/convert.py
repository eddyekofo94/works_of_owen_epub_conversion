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

OVERRIDES = {
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
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
