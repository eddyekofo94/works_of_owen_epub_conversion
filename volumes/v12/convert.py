#!/usr/bin/env python3
"""
Volume 12 — The Works of John Owen, Volume 12: Vindiciae Evangelicae; Hugo Grotius
Per-volume converter script.

Usage:
    python3 volumes/v12/convert.py                   # full pipeline (extract + render)
    python3 volumes/v12/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v12/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 12

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V12_VINDICIAE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Vindiciae Evangelicae;</p>
<p class="title-connector">Or, the</p>
<p class="title-line-medium">Mystery of the Gospel Vindicated</p>
<p class="title-connector">And</p>
<p class="title-line-medium">Socinianism Examined,</p>
<p class="title-connector">In the Consideration and Refutation of a</p>
<p class="title-line-medium">Catechism,</p>
<p class="title-connector">Published by John Biddle, M.A.;</p>
<p class="title-connector">And the Catechism of Valentinus Smalcius, commonly called</p>
<p class="title-line-medium">The Racovian Catechism;</p>
<p class="title-connector">With the Vindication of the Testimonies of Scripture concerning the Deity and Satisfaction of Jesus Christ from the perverse Expositions and Interpretations of them by Hugo Grotius, in his Annotations on the Bible.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block" style="text-align: center;">
<p lang="el" style="font-family: 'SBL Greek', 'Cardo', serif; font-size: 1.15em; line-height: 1.45; margin-bottom: 0.5em;">Μηδὲ ἐμοὶ τῷ ταῦτα λέγοντι ἁπλῶς πιστεύσῃς, ἐὰν τὴν ἀπόδειξιν τῶν καταγγελλομένων ἀπὸ θείων μὴ λάβῃς γραφῶν<a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="#fn_cyril"><sup>[1]</sup></a></p>
<p class="title-source" style="font-size: 0.9em; margin-top: 0;">— CYRIL, HIEROS., Catech. 4.</p>
</div>
<aside epub:type="footnote" id="fn_cyril" class="footnote" role="doc-endnote">
<p class="footnote"><span class="fn-link">[1]</span> “Believe not even me simply in these things, unless you receive the proof of what I declare from the divine Scriptures.” — Cyril of Jerusalem, <i>Catechetical Lectures</i>, Lecture 4, Section 17 [NPNF2, 7:23; PG 33.476].</p>
</aside>
</section>'''

_V12_DEATH_JUSTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Of the Death of Christ,</p>
<p class="title-connector">and of</p>
<p class="title-line-major">Justification:</p>
<p class="title-connector">Being a Full Answer to Mr Richard Baxter's Exceptions</p>
<p class="title-connector">in His Treatise of</p>
<p class="title-line-medium">Redemption.</p>
</section>'''

_V12_GROTIUS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Review of the Annotations of</p>
<p class="title-line-major">Hugo Grotius,</p>
<p class="title-connector">in Reference to the Doctrine of the</p>
<p class="title-line-medium">Deity and Satisfaction of Christ.</p>
</section>'''

_V12_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 12.</h1>

<h2 class="contents-treatise-title">VINDICIAE EVANGELICAE; OR, THE MYSTERY OF THE GOSPEL VINDICATED AND SOCINIANISM EXAMINED</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch003.xhtml">Epistle Dedicatory</a></p>
<p class="contents-item"><a href="ch004.xhtml">Preface to the Reader</a></p>
<p class="contents-item"><a href="ch005.xhtml">Mr Biddle's Preface to His Catechism</a></p>
<p class="contents-item"><a href="ch006.xhtml">Mr Biddle's Preface Briefly Examined</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch007.xhtml">Mr Biddle's first chapter examined — Of the Scriptures</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch008.xhtml">Of the nature of God</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch009.xhtml">Of the shape and bodily visible figure of God</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch010.xhtml">Of the attribution of passions and affections, anger, fear, repentance, unto God — In what sense it is done in the Scripture</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch011.xhtml">Of God's prescience or foreknowledge</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch012.xhtml">Of the creation, and condition of man before and after the fall</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch015.xhtml">Of the person of Jesus Christ, and on what account he is the Son of God</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch018.xhtml">An entrance into the examination of the Racovian Catechism in the business of the deity of Christ — Their arguments against it answered; and testimonies of the eternity of Christ vindicated</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch019.xhtml">The pre-eternity of Christ farther evinced — Sundry texts of Scripture vindicated</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch020.xhtml">Of the names of God given unto Christ</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch021.xhtml">Of the work of creation assigned to Jesus Christ, etc. — The confirmation of his eternal deity from thence</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch022.xhtml">All-ruling and disposing providence assigned unto Christ, and his eternal Godhead thence farther confirmed, with other testimonies thereof</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch023.xhtml">Of the incarnation of Christ, and his pre-existence thereunto</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch024.xhtml">Sundry other testimonies given to the deity of Christ vindicated</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch025.xhtml">Of the Holy Ghost, his deity, graces, and operations</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch028.xhtml">Of salvation by Christ</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch030.xhtml">Of the mediation of Christ</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch031.xhtml">Of Christ's prophetical office</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch032.xhtml">Of the kingly office of Jesus Christ, and of the worship that is ascribed and due to him</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch033.xhtml">Of the priestly office of Christ — How he was a priest — When he entered on his office — And how he dischargeth it</a></p>
<p class="contents-item"><b>Chapter XXI.</b> <a href="ch035.xhtml">Of the death of Christ, the causes, ends, and fruits thereof, with an entrance into the doctrine of his satisfaction thereby</a></p>
<p class="contents-item"><b>Chapter XXII.</b> <a href="ch036.xhtml">The several considerations of the death of Christ as to the expiation of our sins thereby, and the satisfaction made therein — First, Of it as a price; secondly, As a sacrifice</a></p>
<p class="contents-item"><b>Chapter XXIII.</b> <a href="ch037.xhtml">Of the death of Christ as it was a punishment, and the satisfaction made thereby</a></p>
<p class="contents-item"><b>Chapter XXIV.</b> <a href="ch038.xhtml">Some particular testimonies evincing the death of Christ to be a punishment, properly so called</a></p>
<p class="contents-item"><b>Chapter XXV.</b> <a href="ch039.xhtml">A digression concerning the 53d chapter of Isaiah, and the vindication of it from the perverse interpretation of HUGO GROTIUS</a></p>
<p class="contents-item"><b>Chapter XXVI.</b> <a href="ch040.xhtml">Of the matter of the punishment that Christ underwent, or what he suffered</a></p>
<p class="contents-item"><b>Chapter XXVII.</b> <a href="ch041.xhtml">Of the covenant between the Father and the Son, the ground and foundation of this dispensation of Christ’s being punished for us and in our stead</a></p>
<p class="contents-item"><b>Chapter XXVIII.</b> <a href="ch042.xhtml">Of redemption by the death of Christ as it was a price or ransom</a></p>
<p class="contents-item"><b>Chapter XXIX.</b> <a href="ch043.xhtml">Of reconciliation by the death of Christ as it is a sacrifice</a></p>
<p class="contents-item"><b>Chapter XXX.</b> <a href="ch044.xhtml">The satisfaction of Christ, on the consideration of his death being a punishment, farther evinced, and vindicated from the exceptions of Smalcius</a></p>
<p class="contents-item"><b>Chapter XXXI.</b> <a href="ch045.xhtml">Of election and universal grace — Of the resurrection of Christ from the dead</a></p>
<p class="contents-item"><b>Chapter XXXII.</b> <a href="ch046.xhtml">Of justification and faith</a></p>
<p class="contents-item"><b>Chapter XXXIII.</b> <a href="ch047.xhtml">Of keeping the commandments of God, and of perfection of obedience — How attainable in this life</a></p>
<p class="contents-item"><b>Chapter XXXIV.</b> <a href="ch048.xhtml">Of prayer; and whether Christ prescribed a form of prayer to be used by believers; and of praying unto him and in his name under the old testament</a></p>
<p class="contents-item"><b>Chapter XXXV.</b> <a href="ch049.xhtml">Of the resurrection of the dead and the state of the wicked at the last day</a></p>

<h2 class="contents-treatise-title">OF THE DEATH OF CHRIST, AND OF JUSTIFICATION</h2>
<p class="contents-item"><a href="ch050.xhtml">Of the Death of Christ, and of Justification (Answer to Richard Baxter)</a></p>

<h2 class="contents-treatise-title">A REVIEW OF THE ANNOTATIONS OF HUGO GROTIUS</h2>
<p class="contents-item"><a href="ch052.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch053.xhtml">A Second Consideration of the Annotations of Hugo Grotius</a></p>
</section>'''

def post_extract_hook(intermediate):
    # Insert the modern curated Contents page as the first TOC item in front_matter_items
    fm_items = intermediate.get('front_matter_items', [])
    
    # Find the original printed contents page and rename its title to distinguish it
    original_toc = None
    insert_idx = 0
    for idx, item in enumerate(fm_items):
        if item.get('type') == 'toc':
            original_toc = item
            insert_idx = idx
            break
            
    if original_toc:
        original_toc['title'] = 'Original Printed Contents'
        
    modern_toc = {
        'type': 'toc',
        'file_name': 'contents.xhtml',
        'title': 'Contents',
        'page': 2,
        'html': _V12_CONTENTS_PAGE
    }
    fm_items.insert(insert_idx, modern_toc)
    intermediate['front_matter_items'] = fm_items
    return intermediate


OVERRIDES = {
    'post_extract_hook': post_extract_hook,
    'front_matter_overrides': {
        'Contents': _V12_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'Vindiciae Evangelicae;': _V12_VINDICIAE_TITLE_PAGE,
        'Of the Death of Christ, and of Justification:': _V12_DEATH_JUSTIFICATION_TITLE_PAGE,
        'A Review of the Annotations of Hugo Grotius.': _V12_GROTIUS_TITLE_PAGE,
    },
    'text_replacements': {
        'Socimanism': 'Socinianism',
        'Sociman': 'Socinian',
        'Blddle': 'Biddle',
        'Grotiua': 'Grotius',
        'Peta-vius': 'Petavius',
        'Soci-nians': 'Socinians',
        'So-cinians': 'Socinians',
        'So-cinus': 'Socinus',
        'Geor-gius': 'Georgius',
        'Cra-covia': 'Cracovia',
        'iraFated': 'imputed',
        'B[AXTER': 'BAXTER',
        'Francisei': 'Francisci',
        'Virglnique': 'Virginique',
        'Virgln': 'Virgin',
        'Clarke': 'Clarae',
        'Voss. Rasp': 'Voss. Resp',
        r'(— Thes\.\n\nFrancisci)': '— Thes. Francisci',
        'sod': 'sed',
        '"De Christo,\'': '"De Christo,"',
        'remain': 'veniam',
        'Hist. Ecclesiastes lib. 5': 'Hist. Eccles. lib. 5',
        'Euseb. Hist. Ecclesiastes lib. 7 cap. 29, 30': 'Euseb. Hist. Eccles. lib. 7 cap. 29, 30',
        'Socrat. Ecclesiastes Hist. lib. 2 cap. 24, 25': 'Socrat. Eccles. Hist. lib. 2 cap. 24, 25',
        'in in odum': 'in modum',
        'put to to give': 'put to, to give',
        'discourse is is evident': 'discourse is, is evident',
        'asserts it it is': 'asserts it, it is',
        'for for that end': 'for that end',
        'queastum facere solitua': 'quaestum facere solitus',
        'which it is is inconsistent': 'which it is, is inconsistent',
    },
    'regex_replacements': {
        r',,': ',',
        r'xauni~am': 'familiam',
        r'con~erendls': 'conferendis',
        # Translate the George Blandrata Latin dedication, using negative lookahead to prevent double replacement
        r'whose inscription is, "Amplissimo clarissimoque viro Georgio Blandratae Stephani invictissimi regis Poloniae, etc\., archiatro et conciliario intimo, domino, ae patrono suo perpetua observantia colendo; et subscribitur, Tibi in Domino Jesu deditissimus cliens tuus F\. S\."(?! \[Translated:)':
        r'whose inscription is, "Amplissimo clarissimoque viro Georgio Blandratae Stephani invictissimi regis Poloniae, etc., archiatro et conciliario intimo, domino, ae patrono suo perpetua observantia colendo; et subscribitur, Tibi in Domino Jesu deditissimus cliens tuus F. S." [Translated: “To the most distinguished and renowned George Blandrata, physician-in-chief and intimate counselor of Stephen, the most unconquered king of Poland, etc., his lord and patron to be cherished with perpetual respect; and it is subscribed, Your most devoted client in the Lord Jesus, F. S.”]',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
