#!/usr/bin/env python3
"""
Volume 3 — The Works of John Owen, Volume 3: The Holy Spirit (Books 1–5)
Per-volume converter script.

Usage:
    python3 volumes/v3/convert.py                   # full pipeline (extract + render)
    python3 volumes/v3/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v3/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 3

# ---------------------------------------------------------------------------
# Treatise Title Page Override
# ---------------------------------------------------------------------------
_V3_HOLY_SPIRIT_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="greek-title"><span lang="el" xml:lang="el">ΠΝΕΥΜΑΤΟΛΟΓΙΑ:</span></p>
<p class="title-connector">Or,</p>
<p class="title-line-major">A Discourse</p>
<p class="title-connector">Concerning the</p>
<p class="title-line-major">Holy Spirit:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">The Nature, Office, Work, Gifts, and Operations of the Holy Spirit Revealed and Vindicated.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">"He shall glorify me: for he shall receive of mine, and shall shew it unto you." — John 16:14.</p>
<div class="quote-block">
<p><span lang="el" xml:lang="el">Ἐκ τῶν θείων γραφῶν θεολογοῦμεν κἂν θέλωσιν οἱ ἐχθροὶ κἂν μή.</span> — Chrysostom</p>
</div>
<!-- Prevent duplicate Greek quote merge: -->
<div style="display:none;" lang="el">Εκ τῶν θείων γραφᾶν θεολογοῦμεν κἇν θέλωσιν οἱ ἐχθροὶ κἆν μή</div>
</section>'''

# ---------------------------------------------------------------------------
# Custom Table of Contents
# ---------------------------------------------------------------------------
_V3_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 3.</h1>
<h2 class="contents-treatise-title">PNEUMATOLOGIA: OR, A DISCOURSE CONCERNING THE HOLY SPIRIT</h2>

<p class="contents-frontmatter-line">
<a href="ch002.xhtml">Prefatory Note by the Editor</a> &bull; 
<a href="ch003.xhtml">Analysis by the Editor</a> &bull; 
<a href="ch004.xhtml">To the Readers</a>
</p>

<h3 class="contents-part-title">BOOK I. — GENERAL PRINCIPLES CONCERNING THE HOLY SPIRIT AND HIS WORK</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch006.xhtml">General Principles Concerning the Holy Spirit and His Work</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch007.xhtml">The Name and Titles of the Holy Spirit</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch008.xhtml">Divine Nature and Personality of the Holy Spirit Proved and Vindicated</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch009.xhtml">Peculiar Works of the Holy Spirit in the First or Old Creation</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch010.xhtml">Way and Manner of the Divine Dispensation of the Holy Spirit</a></p>

<h3 class="contents-part-title">BOOK II. — PREPARATORY OPERATIONS OF THE HOLY SPIRIT</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch012.xhtml">Peculiar Operations of the Holy Spirit Under the Old Testament Preparatory for the New</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch013.xhtml">General Dispensation of the Holy Spirit with Respect unto the New Creation</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch014.xhtml">Work of the Holy Spirit with Respect unto the Head of the New Creation — The Human Nature of Christ</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch015.xhtml">Work of the Holy Spirit in and on the Human Nature of Christ</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch016.xhtml">The General Work of the Holy Spirit in the New Creation with Respect unto the Members of That Body</a></p>

<h3 class="contents-part-title">BOOK III. — THE WORK OF THE HOLY SPIRIT IN REGENERATION</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch018.xhtml">Work of the Holy Spirit in the New Creation by Regeneration</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch019.xhtml">Works of the Holy Spirit Preparatory unto Regeneration</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch020.xhtml">Corruption or Depravation of the Mind by Sin</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch021.xhtml">Life and Death, Natural and Spiritual, Compared</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch022.xhtml">The Nature, Causes, and Means of Regeneration</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch023.xhtml">The Manner of Conversion Explained in the Instance of Augustine</a></p>

<h3 class="contents-part-title">BOOK IV. — THE WORK OF THE HOLY SPIRIT IN SANCTIFICATION</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch025.xhtml">The Nature of Sanctification and Gospel Holiness Explained</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch026.xhtml">Sanctification a Progressive Work</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch027.xhtml">Believers the Only Object of Sanctification</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch028.xhtml">The Defilement of Sin, Wherein It Consists, with Its Purification</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch029.xhtml">The Filth of Sin Purged by the Spirit and Blood of Christ</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch030.xhtml">The Positive Work of the Spirit in the Sanctification of Believers</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch031.xhtml">Of the Acts and Duties of Holiness</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch032.xhtml">Mortification of Sin, the Nature and Causes of It</a></p>

<h3 class="contents-part-title">BOOK V. — THE NECESSITY OF HOLINESS</h3>
<p class="contents-item"><b>Chapter I.</b> <a href="ch034.xhtml">Necessity of Holiness from the Consideration of the Nature of God</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch035.xhtml">Eternal Election a Cause of and Motive unto Holiness</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch036.xhtml">Necessity of Holiness from the Commands of God</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch037.xhtml">Necessity of Holiness from God's Sending Jesus Christ</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch038.xhtml">Necessity of Holiness from Our Condition in This World</a></p>
</section>'''

# ---------------------------------------------------------------------------
# Overrides and replacements
# ---------------------------------------------------------------------------
OVERRIDES = {
    'contents_page_overrides': _V3_CONTENTS_PAGE,
    'treatise_title_overrides': {
        'A Discourse Concerning the Holy Spirit:': _V3_HOLY_SPIRIT_TITLE_PAGE,
    },
    'text_replacements': {
        'Pelaglan': 'Pelagian',
        'Socimanism': 'Socinianism',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
