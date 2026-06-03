#!/usr/bin/env python3
"""
Volume 7 — The Works of John Owen, Volume 7: Apostasy, Spiritually-Mindedness, Dominion of Sin
Per-volume converter script.

Usage:
    python3 volumes/v7/convert.py                   # full pipeline (extract + render)
    python3 volumes/v7/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v7/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Note: The chapter title for "Nature of Apostasy" is truncated at 60 characters in the
JSON intermediate file. The key below must match that truncated string exactly.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 7

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v7/intermediate/volume_7.json (including punctuation).
# NB: "Apostasy" title is truncated at 60 chars in the JSON.
# ---------------------------------------------------------------------------

_V7_APOSTASY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Nature of</p>
<p class="title-line-major">Apostasy</p>
<p class="title-connector">from the Profession of the Gospel</p>
<p class="title-connector">and the Punishment of Apostates Declared,</p>
<p class="title-connector">in an Exposition of</p>
<p class="title-line-medium">Hebrews 6:4–6.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For it is impossible for those who were once enlightened, and have tasted of the heavenly gift, and were made partakers of the Holy Ghost, and have tasted the good word of God, and the powers of the world to come, if they shall fall away, to renew them again unto repentance." — Hebrews 6:4–6.</p></div>
</section>'''

_V7_SPIRITUALLY_MINDED_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Grace and Duty of Being</p>
<p class="title-line-major">Spiritually Minded,</p>
<p class="title-connector">Declared and Practically Improved.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For to be carnally minded is death; but to be spiritually minded is life and peace." — Romans 8:6.</p></div>
</section>'''

_V7_DOMINION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Treatise</p>
<p class="title-connector">of the</p>
<p class="title-line-medium">Dominion of Sin and Grace.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For sin shall not have dominion over you: for ye are not under the law, but under grace." — Romans 6:14.</p></div>
</section>'''
_V7_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 7.</h1>

<h2 class="contents-treatise-title">I. THE NATURE AND CAUSES OF APOSTASY</h2>
<p class="contents-item"><a href="ch003.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch004.xhtml">Analysis</a></p>
<p class="contents-item"><a href="ch005.xhtml">To the Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch006.xhtml">The nature of apostasy from the gospel declared</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch007.xhtml">Partial apostasy from the gospel</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch008.xhtml">Apostasy from the mystery, truth, or doctrine of the gospel</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch009.xhtml">The reasons and causes of apostasy from the truth</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch010.xhtml">Darkness and ignorance another cause of apostasy</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch011.xhtml">Pride and vanity of mind a cause of apostasy</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch012.xhtml">Defection from the truth of the gospel</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch013.xhtml">Apostasy from the holiness of the gospel</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch014.xhtml">Apostasy into profaneness and sensuality of life</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch015.xhtml">Other causes and occasions of the decay of holiness</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch016.xhtml">Apostasy from evangelical worship</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch017.xhtml">Inferences from the foregoing discourses</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch018.xhtml">Directions to avoid the power of a prevailing apostasy</a></p>

<h2 class="contents-treatise-title">II. THE GRACE AND DUTY OF BEING SPIRITUALLY MINDED</h2>
<p class="contents-item"><a href="ch020.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch021.xhtml">Analysis</a></p>
<h3 class="contents-part-title">Part I</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch026.xhtml">The words of the text (Romans 8:6) explained</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch027.xhtml">A particular account of the nature of this grace and duty</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch028.xhtml">Outward means and occasions of spiritual thoughts</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch029.xhtml">Thoughts about spiritual things arising from renovation</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch030.xhtml">The objects of spiritual thoughts: Christ's person and glory</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch031.xhtml">Especial objects of spiritual thoughts: the mediation of Christ</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch032.xhtml">Especial objects: the glorious state of the church above</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch033.xhtml">Spiritual thoughts of God himself: opposition and remedies</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch034.xhtml">What of God or in God we are to think and meditate upon</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch035.xhtml">Meditation on God's omnipresence and omniscience</a></p>
<h3 class="contents-part-title">Part II</h3>
<p class="contents-item"><a href="ch024.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch037.xhtml">The seat of spiritual mindedness in the affections</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch038.xhtml">What is required in and unto our affections</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch039.xhtml">The work of the renovation of our affections</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch040.xhtml">Renovated affections distinguished from natural affections</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch041.xhtml">Delight of believers in the holy institutions of divine worship</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch042.xhtml">Assimilation unto things heavenly and spiritual in affections</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch043.xhtml">Decays in spiritual affections, with the causes and dangers</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch044.xhtml">The state of spiritual affections</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch045.xhtml">The true notion and consideration of spiritual things</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch046.xhtml">The application of the soul unto spiritual objects</a></p>
<p class="contents-item"><b>Chapter XXI.</b> <a href="ch047.xhtml">Spiritual mindedness life and peace</a></p>

<h2 class="contents-treatise-title">III. A TREATISE OF THE DOMINION OF SIN AND GRACE</h2>
<p class="contents-item"><a href="ch049.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch050.xhtml">Analysis</a></p>
<p class="contents-item"><a href="ch051.xhtml">To the Serious Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch052.xhtml">What sin is consistent with the state of grace</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch053.xhtml">Whether sin hath dominion in us</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch054.xhtml">Whether sin hath dominion in unregenerate persons</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch055.xhtml">Practical signs of the dominion of sin</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch056.xhtml">Assurances that sin shall not have dominion (Romans 6:14)</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch057.xhtml">Practical directions how to be preserved from the dominion of sin</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V7_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V7_CONTENTS_PAGE,
    },
    'exclude_chapters': [
        'The Works of John Owen Vol. 7',
    ],
    'treatise_title_overrides': {
        # Truncated at 60 chars in JSON — match exactly
        'The Nature of Apostasy From the Profession of the Gospel and Th': _V7_APOSTASY_TITLE_PAGE,
        'Grace and Duty of Being Spiritually Minded': _V7_SPIRITUALLY_MINDED_TITLE_PAGE,
        'A Treatise Of The Dominion of Sin and Grace': _V7_DOMINION_TITLE_PAGE,
    },
    'text_replacements': {
        'apostaey': 'apostasy',
        'apostate.s': 'apostates',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
