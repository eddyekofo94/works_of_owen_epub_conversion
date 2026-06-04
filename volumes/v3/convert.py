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
<p><span lang="el" xml:lang="el">Ἐκ τῶν θείων γραφῶν θεολογοῦμεν κἂν θέλωσιν οἱ ἐχθροὶ κἂν μή.</span><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="#fn_chrysostom"><sup>[1]</sup></a> — Chrysostom</p>
</div>
<aside epub:type="footnote" id="fn_chrysostom" class="footnote" role="doc-endnote">
<p class="footnote"><span class="fn-link">[1]</span> “We speak of theology from the divine Scriptures, whether our enemies want it or not.” — John Chrysostom; also cited as an early Greek patristic maxim.</p>
</aside>
<!-- Prevent duplicate Greek quote merge: -->
<div style="display:none;" lang="el">Εκ τῶν θείων γραφᾶν θεολογοῦμεν κἇν θέλωσιν οἱ ἐχθροὶ κἆν μή</div>
</section>'''

# ---------------------------------------------------------------------------
# Custom Table of Contents
# ---------------------------------------------------------------------------
_V3_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 3.</h1>
<h2 class="contents-treatise-title">PNEUMATOLOGIA: OR, A DISCOURSE CONCERNING THE HOLY SPIRIT</h2>

<p class="contents-item"><a href="ch002.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch003.xhtml">Analysis by the Editor</a></p>
<p class="contents-item"><a href="ch004.xhtml">To the Readers</a></p>

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
import re

def html_postprocess_hook(html, ch_context):
    title = ch_context.get('title', '')
    if 'TO THE READERS' in title.upper():
        unified = (
            '<blockquote epub:type="z3998:quotation"><p class="blockquote-content">&quot;<span lang="la" xml:lang="la">'
            'In seculo hodie tam Perverso prorsus immersi vivinus miseri, in quo Spiritus Sanctus omnino ferme pro ludibrio habetur: '
            'imo in quo etiam sunt qui non tantum corde toto eum repudient ut factis negent, sed quoque adeo blasphemi in eum exsurgant '
            'ut penitus eundem ex orbe expulsum aut exulatum cupiant, quum illi nullam in operationibus suis relinquant efficaciam; '
            'ac propriis vanorum habituum suorum viribus, ac rationis profanae libertati carnalitatique suae omnem ascribant sapientiam, '
            'et fortitudinem in rebus agendis. Unde tanta malignitas externae proterviae apud mortales cernitur. Ideoque pernicies '
            'nostra nos jam ante fores expectat,</span>&quot; etc.</p></blockquote>'
        )
        pattern = re.compile(r'<blockquote epub:type="z3998:quotation"><p class="blockquote-content">(?:&quot;|")In seculo hodie.*?</p></blockquote>', re.S)
        html = pattern.sub(unified, html)
    elif 'PECULIAR OPERATIONS' in title.upper():
        # Fix the Juvenal quote language tagging to include the whole phrase
        html = re.sub(
            r'(?:&quot;|")Qualiacumque voles <span lang="la" xml:lang="la">Judaei somia</span> vendant\.(?:&quot;|")',
            r'&quot;<span lang="la" xml:lang="la">Qualiacumque voles Judaei somia vendant.</span>&quot;',
            html
        )
        # Merge flat-list item 4 and split concluding sentence
        pattern_list = re.compile(
            r'(Those of the other sort we shall find: — <b>1\.</b>.*?<b>3\.</b> In things <i>natural,</i> as increase of bodily strength\.)</p>\s*</div>\s*<div class="owen-branch owen-level-1">\s*<p class="list-item list-level-1"><b>4\.</b> (In gifts <i>intellectual,</i> <b>\(1\.\)</b> For things sacred, as to preach the word of God; <b>\(2\.\)</b> In things artificial, as in Bezaleel and Aholiab\.)\s+(.*?)\s*</p>\s*</div>',
            re.S
        )
        html = pattern_list.sub(r'\1 <b>4.</b> \2</p>\n</div>\n<p>\3</p>', html)
    return html

OVERRIDES = {
    'contents_page_overrides': _V3_CONTENTS_PAGE,
    'treatise_title_overrides': {
        'A Discourse Concerning the Holy Spirit:': _V3_HOLY_SPIRIT_TITLE_PAGE,
    },
    'text_replacements': {
        'VII1TUES': 'VIRTUES',
        'Pelaglan': 'Pelagian',
        'Socimanism': 'Socinianism',
        'without it it is': 'without it, it is',
        '_no_ s _upernatural strength;_': '_no supernatural strength;_',
        'no s upernatural strength': 'no supernatural strength',
        'giving, s ending': 'giving, sending',
        'enmit y': 'enmity',
        'in tended': 'intended',
        'p ersuasion': 'persuasion',
        'p rinciple': 'principle',
        'm orally': 'morally',
        'C hrist': 'Christ',
        'C hristian': 'Christian',
        'f orbidden': 'forbidden',
    },
    'html_postprocess_hook': html_postprocess_hook,
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
