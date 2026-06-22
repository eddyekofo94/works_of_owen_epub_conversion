#!/usr/bin/env python3
"""
Volume 4 — The Works of John Owen, Volume 4: The Reason of Faith; Holy Spirit (Books 5–7)
Per-volume converter script.

Usage:
    python3 volumes/v4/convert.py                   # full pipeline (extract + render)
    python3 volumes/v4/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v4/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 4

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v4/intermediate/volume_4.json (including punctuation).
# ---------------------------------------------------------------------------

_V4_HS_CONTINUED_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="greek-title"><span lang="el" xml:lang="el">ΠΝΕΥΜΑΤΟΛΟΓΙΑ</span></div>
<div class="title-line-major">A Discourse</div>
<div class="title-connector">Concerning the</div>
<div class="title-line-major">Holy Spirit:</div>
<div class="title-connector">Continued.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive">Books V, VI, and VII: Treating of the Work of the Holy Spirit in the Illumination of the Mind, the Sanctification of the Will, and the Renovation of the Whole Soul.</div>
</section>'''

_V4_REASON_OF_FAITH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">The Reason of Faith;</div>
<div class="title-connector">Or,</div>
<div class="title-line-medium">An Answer Unto That Inquiry,</div>
<div class="title-line-medium">"Wherefore We Believe the Scripture to Be the Word of God;"</div>
<div class="title-connector">With</div>
<div class="title-line-medium">The Causes and Nature of That Faith Wherewith We Do So:</div>
<div class="title-connector">Wherein</div>
<div class="descriptive">The Grounds Whereon the Holy Scripture Is Believed to Be the Word of God with Faith Divine and Supernatural Are Declared and Vindicated.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"If they hear not Moses and the prophets, neither will they be persuaded, though one rose from the dead." — Luke 16:31.</div></div>
</section>'''

_V4_CAUSES_WAYS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="greek-title"><span lang="el" xml:lang="el">ΣΥΝΕΣΙΣ ΠΝΕΥΜΑΤΙΚΗ</span></div>
<div class="title-line-medium">The Causes, Ways, and Means</div>
<div class="title-connector">of</div>
<div class="title-line-medium">Understanding the Mind of God</div>
<div class="title-connector">as Revealed in His Word,</div>
<div class="title-line-medium">with Assurance Therein.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive">And a Declaration of the Perspicuity of the Scriptures, with the External Means of the Interpretation of Them.</div>
</section>'''

_V4_HS_PRAYER_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">A Discourse</div>
<div class="title-connector">of the Work of the</div>
<div class="title-line-medium">Holy Spirit in Prayer;</div>
<div class="title-connector">with a Brief Inquiry into the Nature and Use of</div>
<div class="title-line-medium">Mental Prayer and Forms.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"Likewise the Spirit also helpeth our infirmities: for we know not what we should pray for as we ought: but the Spirit itself maketh intercession for us with groanings which cannot be uttered." — Romans 8:26.</div></div>
</section>'''

_V4_TWO_DISCOURSES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">Two Discourses</div>
<div class="title-connector">Concerning the</div>
<div class="title-line-medium">Holy Spirit and His Work:</div>
<div class="title-connector">The First, of</div>
<div class="title-line-medium">The Spirit as a Comforter;</div>
<div class="title-connector">The Second, of</div>
<div class="title-line-medium">The Work of the Holy Spirit</div>
<div class="title-line-medium">in the New Creation.</div>
</section>'''

_V4_SPIRITUAL_GIFTS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">A Discourse</div>
<div class="title-connector">Concerning the</div>
<div class="title-line-medium">Holy Spirit,</div>
<div class="title-connector">His Gifts:</div>
<div class="title-line-medium">Their Nature, Distributions,</div>
<div class="title-line-medium">Excellency, Use, and Abuse.</div>
</section>'''

_V4_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 4.</h1>

<p class="contents-general-preface"><a href="ch002.xhtml">A Discourse Concerning the Holy Spirit, Continued</a></p>

<h2 class="contents-treatise-title">THE REASON OF FAITH</h2>
<p class="contents-item"><a href="ch004.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch005.xhtml">Preface</a></p>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch006.xhtml">The Subject Stated — Preliminary Remarks</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch007.xhtml">What It Is to Believe the Scripture to Be the Word of God</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch008.xhtml">Convincing Arguments for Divine Revelation</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch009.xhtml">Moral Certainty</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch010.xhtml">Divine Revelation Itself the Only Foundation</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch011.xhtml">The Nature of Divine Revelations</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch012.xhtml">Inferences From the Whole</a></p>
<p class="contents-item"><a href="ch013.xhtml">Appendix</a></p>

<h2 class="contents-treatise-title">THE CAUSES, WAYS, AND MEANS OF UNDERSTANDING THE MIND OF GOD</h2>
<p class="contents-item"><a href="ch015.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch016.xhtml">Analysis</a></p>
<p class="contents-item"><a href="ch017.xhtml">Preface</a></p>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch018.xhtml">Usurpation of the church of Rome with reference unto the interpretation of the Scripture</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch019.xhtml">The general assertion confirmed with testimonies of the Scripture</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch020.xhtml">Other testimonies pleaded in confirmation of the same truth</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch021.xhtml">The especial work of the Holy Spirit in the illumination of our minds</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch022.xhtml">Causes of the ignorance of the mind of God revealed in the Scripture</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch023.xhtml">The work of the Holy Spirit in the composing and disposal of the Scripture</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch024.xhtml">Means to be used for the right understanding of the mind of God</a></p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch025.xhtml">Further Rules</a></p>
<p class="contents-item"><strong>Chapter IX.</strong> <a href="ch026.xhtml">Helps ecclesiastical in the interpretation of the Scripture</a></p>

<h2 class="contents-treatise-title">A DISCOURSE OF THE WORK OF THE HOLY SPIRIT IN PRAYER</h2>
<p class="contents-item"><a href="ch028.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch029.xhtml">Analysis</a></p>
<p class="contents-item"><a href="ch030.xhtml">Preface</a></p>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch031.xhtml">The Use of Prayer, and the Work</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch032.xhtml">Zechariah 12:10 Opened and Vindicated</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch033.xhtml">Galatians 4:6 Opened and Vindicated</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch034.xhtml">The Nature of Prayer</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch035.xhtml">The Work of the Holy Spirit</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch036.xhtml">The Due Manner of Prayer</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch037.xhtml">The Nature of Prayer in General</a></p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch038.xhtml">Duty of Prayer by Virtue of a Spiritual Gift Explained</a></p>
<p class="contents-item"><strong>Chapter IX.</strong> <a href="ch039.xhtml">Duties Inferred From the Preceding Discourse</a></p>
<p class="contents-item"><strong>Chapter X.</strong> <a href="ch040.xhtml">Of Mental Prayer as Pretended Unto by Some</a></p>
<p class="contents-item"><strong>Chapter XI.</strong> <a href="ch041.xhtml">Prescribed Forms of Prayer Examined</a></p>

<h2 class="contents-treatise-title">OF THE HOLY SPIRIT AS A COMFORTER</h2>
<p class="contents-item"><a href="ch043.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch044.xhtml">Analysis of the First Treatise</a></p>
<p class="contents-item"><a href="ch045.xhtml">Analysis of the Second Treatise</a></p>
<p class="contents-item"><a href="ch046.xhtml">Preface</a></p>
<div class="contents-part-divider">
  <span class="divider-ornament">❦</span>
  <h3 class="contents-part-title">OF THE SPIRIT AS A COMFORTER</h3>
</div>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch048.xhtml">The Holy Ghost the comforter of the church by way of office</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch049.xhtml">General Adjuncts or Properties of the Office of a Comforter</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch050.xhtml">Unto Whom the Holy Spirit Is Promised and Given as a Comforter</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch051.xhtml">Inhabitation of the Spirit</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch052.xhtml">Particular Actings of the Holy Spirit As A Comforter</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch053.xhtml">The Spirit a Seal, and How</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch054.xhtml">The Spirit an Earnest, and How</a></p>
<p class="contents-item"><a href="ch055.xhtml">The Application of the Foregoing Discourse</a></p>

<h2 class="contents-treatise-title">A DISCOURSE OF SPIRITUAL GIFTS</h2>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch057.xhtml">Spiritual Gifts, Their Names and Signification</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch058.xhtml">Differences Between Spiritual Gifts and Saving Grace</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch059.xhtml">Of Gifts and Offices Extraordinary</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch060.xhtml">Extraordinary Spiritual Gifts</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch061.xhtml">Extraordinary Spiritual Gifts</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch062.xhtml">Of Ordinary Gifts of the Spirit</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch063.xhtml">Of Spiritual Gifts Enabling the Ministry</a></p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch064.xhtml">Of the Gifts of the Spirit With Respect Unto Doctrine, Worship, & Rule</a></p>
</section>'''

def post_extract_hook(intermediate: dict) -> dict:
    """Post-extraction adjustments for Volume 4."""
    for ch in intermediate.get('chapters', []):
        if ch['cid'] == 'ch048':
            ch['raw_text'] = ch['raw_text'].replace('13:112 Epist. 13:11', '13:11')
    return intermediate


OVERRIDES = {
    'post_extract_hook': post_extract_hook,
    'contents_page_overrides': _V4_CONTENTS_PAGE,
    'exclude_chapters': [
        'The Works of John Owen Vol. 4',
    ],
    'treatise_title_overrides': {
        'A Discourse Concerning the Holy Spirit, Continued:': _V4_HS_CONTINUED_TITLE_PAGE,
        'The Reason of Faith;': _V4_REASON_OF_FAITH_TITLE_PAGE,
        'The Causes, Ways, and Means of Understanding the Mind of God as': _V4_CAUSES_WAYS_TITLE_PAGE,
        'A Discourse of the Work of the Holy Spirit in Prayer': _V4_HS_PRAYER_TITLE_PAGE,
        'Two Discourses Concerning the Holy Spirit and His Work:': _V4_TWO_DISCOURSES_TITLE_PAGE,
        # OCR typo in JSON: "Glfts" instead of "Gifts" — keep the key exactly as it appears in JSON
        'A Discourse of Spiritual Glfts.': _V4_SPIRITUAL_GIFTS_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair OCR chapter-title typo so it renders correctly in the body
        'Spiritual Glfts': 'Spiritual Gifts',
        'Glfts': 'Gifts',
        '13:112 Epist. 13:11': '13:11',
        'com-prebends': 'comprehends',
        'hac-tenus': 'hactenus',
        'limi-rations': 'limitations',
        'ma-nagery': 'managery',
        'a0y': 'any',
        'Co1ossians': 'Colossians',
        'pIeasure': 'pleasure',
        'shalI': 'shall',
        '2 ndly .': '2ndly.',
        '4 thly .': '4thly.',
        '5 thly .': '5thly.',
        '2dly .': '2dly.',
        '3dly .': '3dly.',
        '1st..': '1st.',
        '2dly..': '2dly.',
        'perfect,,': 'perfect,',
        'them,,': 'them,',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
