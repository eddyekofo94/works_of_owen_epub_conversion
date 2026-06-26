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
<div class="greek-title"><span lang="el" xml:lang="el">ΠΝΕΥΜΑΤΟΛΟΓΙΑ:</span></div>
<div class="title-connector">Or,</div>
<div class="title-line-major">A Discourse</div>
<div class="title-connector">Concerning the</div>
<div class="title-line-major">Holy Spirit:</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive">The Nature, Office, Work, Gifts, and Operations of the Holy Spirit Revealed and Vindicated.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="title-source">"He shall glorify me: for he shall receive of mine, and shall shew it unto you." — John 16:14.</div>
<div class="quote-block">
<p><span lang="el" xml:lang="el">Ἐκ τῶν θείων γραφῶν θεολογοῦμεν κἂν θέλωσιν οἱ ἐχθροὶ κἂν μή.</span><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="#fn_chrysostom"><sup>[1]</sup></a> — Chrysostom</div>
</div>
<aside epub:type="footnote endnote" id="fn_chrysostom" role="doc-footnote doc-endnote">
<p class="footnote" style="line-height: 1.30 !important;"><span class="fn-link">[1]</span> “We speak of theology from the divine Scriptures, whether our enemies want it or not.” — John Chrysostom; also cited as an early Greek patristic maxim.</p>
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
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch006.xhtml">General Principles Concerning the Holy Spirit and His Work</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch007.xhtml">The Name and Titles of the Holy Spirit</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch008.xhtml">Divine Nature and Personality of the Holy Spirit Proved and Vindicated</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch009.xhtml">Peculiar Works of the Holy Spirit in the First or Old Creation</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch010.xhtml">Way and Manner of the Divine Dispensation of the Holy Spirit</a></p>

<h3 class="contents-part-title">BOOK II. — PREPARATORY OPERATIONS OF THE HOLY SPIRIT</h3>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch012.xhtml">Peculiar Operations of the Holy Spirit Under the Old Testament Preparatory for the New</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch013.xhtml">General Dispensation of the Holy Spirit with Respect unto the New Creation</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch014.xhtml">Work of the Holy Spirit with Respect unto the Head of the New Creation — The Human Nature of Christ</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch015.xhtml">Work of the Holy Spirit in and on the Human Nature of Christ</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch016.xhtml">The General Work of the Holy Spirit in the New Creation with Respect unto the Members of That Body</a></p>

<h3 class="contents-part-title">BOOK III. — THE WORK OF THE HOLY SPIRIT IN REGENERATION</h3>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch018.xhtml">Work of the Holy Spirit in the New Creation by Regeneration</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch019.xhtml">Works of the Holy Spirit Preparatory unto Regeneration</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch020.xhtml">Corruption or Depravation of the Mind by Sin</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch021.xhtml">Life and Death, Natural and Spiritual, Compared</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch022.xhtml">The Nature, Causes, and Means of Regeneration</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch023.xhtml">The Manner of Conversion Explained in the Instance of Augustine</a></p>

<h3 class="contents-part-title">BOOK IV. — THE WORK OF THE HOLY SPIRIT IN SANCTIFICATION</h3>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch025.xhtml">The Nature of Sanctification and Gospel Holiness Explained</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch026.xhtml">Sanctification a Progressive Work</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch027.xhtml">Believers the Only Object of Sanctification</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch028.xhtml">The Defilement of Sin, Wherein It Consists, with Its Purification</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch029.xhtml">The Filth of Sin Purged by the Spirit and Blood of Christ</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch030.xhtml">The Positive Work of the Spirit in the Sanctification of Believers</a></p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch031.xhtml">Of the Acts and Duties of Holiness</a></p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch032.xhtml">Mortification of Sin, the Nature and Causes of It</a></p>

<h3 class="contents-part-title">BOOK V. — THE NECESSITY OF HOLINESS</h3>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch034.xhtml">Necessity of Holiness from the Consideration of the Nature of God</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch035.xhtml">Eternal Election a Cause of and Motive unto Holiness</a></p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch036.xhtml">Necessity of Holiness from the Commands of God</a></p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch037.xhtml">Necessity of Holiness from God's Sending Jesus Christ</a></p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch038.xhtml">Necessity of Holiness from Our Condition in This World</a></p>
</section>'''

# ---------------------------------------------------------------------------
# Overrides and replacements
# ---------------------------------------------------------------------------
import re

def post_extract_hook(intermediate):
    for ch in intermediate.get('chapters', []):
        if 'raw_text' in ch:
            ch['raw_text'] = re.sub(
                r'—\s*\n\n(Schlichting\.|עָרָה|\*\*1\*\*|1\.|Psalm 31|That the will|There are two|Philippians 1|Sanctification, as|Sanctification is|It is the universal)',
                r'— \1',
                ch['raw_text']
            )
            ch['raw_text'] = re.sub(
                r'person of Christ; for,\s*—\s*\n\nIt is by all confessed',
                r'person of Christ; for, — It is by all confessed',
                ch['raw_text']
            )
            ch['raw_text'] = re.sub(
                r'offered for us,\s*—\s*\n\nRevelation 1:5, it is not only',
                r'offered for us, — Revelation 1:5, it is not only',
                ch['raw_text']
            )
    return intermediate

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
            r'(Those of the other sort we shall find: — <strong>1\.</strong>.*?<strong>3\.</strong> In things <em>natural,</em> as increase of bodily strength\.)</p>\s*</div>\s*<div class="owen-branch owen-level-1">\s*<p class="list-item list-level-1"><strong>4\.</strong> (In gifts <em>intellectual,</em> <strong>\(1\.\)</strong> For things sacred, as to preach the word of God; <strong>\(2\.\)</strong> In things artificial, as in Bezaleel and Aholiab\.)\s+(.*?)\s*</p>\s*</div>',
            re.S
        )
        html = pattern_list.sub(r'\1 <strong>4.</strong> \2</p>\n</div>\n<p>\3</p>', html)
    return html

OVERRIDES = {
    'contents_page_overrides': _V3_CONTENTS_PAGE,
    'treatise_title_overrides': {
        'A Discourse Concerning the Holy Spirit:': _V3_HOLY_SPIRIT_TITLE_PAGE,
    },
    'text_replacements': {
        '1 .': '1.',
        '2dly .': '2dly.',
        '3dly .': '3dly.',
        '4thly .': '4thly.',
        'Ans .': 'Ans.',
        'end .': 'end.',
        'idem .': 'idem.',
        'habit .': 'habit.',
        'Assimilation :': 'Assimilation:',
        'transgression :': 'transgression:',
        'free ;': 'free;',
        'n )': 'n)',
        'sin :': 'sin:',
        'spirits ;': 'spirits;',
        'received .': 'received.',
        'Jehovah .': 'Jehovah.',
        'of ,': 'of,',
        'sacrifice .': 'sacrifice.',
        'our .': 'our.',
        'easy ,': 'easy,',
        '..': '.',
        'holiness .': 'holiness.',
        
        # Latin Translations and OCR Fixes
        'Malus bonum cure simulat, tune est pessimus': 'Malus bonum cum simulat, tunc est pessimus',

        'VII1TUES': 'VIRTUES',
        'Pelaglan': 'Pelagian',
        'Socimanism': 'Socinianism',
        'without it it is': 'without it, it is',
        '_no_ s _upernatural strength;_': '_no supernatural strength;_',
        'no s upernatural strength': 'no supernatural strength',
        'Philippians 14:5 2:5-8': 'Philippians 2:5-8',
        'Philippians 17:6 2:6, 7': 'Philippians 2:6, 7',
        'Philippians 23:8 2:8': 'Philippians 2:8',
        'Philippians 26:9 2:9, 10': 'Philippians 2:9, 10',
        'Philippians 38:13 2:13': 'Philippians 2:13',
        'Hebrews 19:12-14': 'Hebrews 9:12-14',
        # Punctuation formatting fixes
        '**1** .': '**1**.',
        '_Ans_ .': '_Ans_.',
        '_ad idem_ .': '_ad idem_.',
        '_habit_ .': '_habit_.',
        '_Assimilation_ :': '_Assimilation_:',
        '_transgression_ :': '_transgression_:',
        '_free_ ;': '_free_;',
        '_own_ )': '_own_)',
        '_sin_ )': '_sin_)',
        'sin_ :': 'sin_:',
        'end _._': 'end_._',
        '**1st** _._': '**1st**_._',
        '**2dly** _._': '**2dly**_._',
        '**3dly** _._': '**3dly**_._',
        '**4thly** _._': '**4thly**_._',
        # Compound word merging fixes (extract.py drops hyphen at line breaks)
        'preeminence': 'pre-eminence',
        'selfabasement': 'self-abasement',
        'selfdenial': 'self-denial',
    },
    'regex_replacements': {
        r'\b_enmit_ y\b': 'enmity',
        r'\btestimon\*\*y against\*\*': 'testimony against',
        r'\benmit \*\*y against\*\*': 'enmity against',
        r'_giving,_ s _ending_': '_giving, sending_',
        r'\bp\s+(_?)ersuasion(_?)\b': r'\1persuasion\2',
        r'\bp\s+(_?)rinciple(_?)\b': r'\1principle\2',
        r'\bm\s+(_?)orally(_?)\b': r'\1morally\2',
        r'\bC\s+(_?)hristian(_?)\b': r'\1Christian\2',
        r'\bC\s+(_?)hrist(_?)\b': r'\1Christ\2',
        r'\bf\s+(_?)orbidden(_?)\b': r'\1forbidden\2',
        r'\bin_?\s+tended\b': 'intended',
    },
    'post_extract_hook': post_extract_hook,
    'html_postprocess_hook': html_postprocess_hook,
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
