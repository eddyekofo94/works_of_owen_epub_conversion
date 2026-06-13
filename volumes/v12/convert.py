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
        'Plato de Legib.\n\n12. And that may be the sense': 'Plato de Legib. 12. And that may be the sense',
        'true )': 'true)',
        'True ,': 'True,',
        'of .our sins': 'of our sins',
        'enemies )': 'enemies)',
        'Ezekiel ( 5:13': 'Ezekiel (5:13',
        'is ,': 'is,',
        'also .': 'also.',
        '1 . His birth': '1. His birth',
        'and .personality': 'and personality',
        'came ,': 'came,',
        '2 . To translate': '2. To translate',
        'ejus ;': 'ejus;',
        'est ,': 'est,',
        'office . 2. The title': 'office. 2. The title',
        'Mohammedanism )': 'Mohammedanism)',
        'confess .that': 'confess that',
        'Ans . That': 'Ans. That',
        'were .priests': 'were priests',
        '1 )': '1)',
        '2dly . The': '2dly. The',
        'comeliness ;': 'comeliness;',
        'the .providence': 'the providence',
        't )': 't)',
        'two .ways': 'two ways',
        '1st . The': '1st. The',
        '2dly . That': '2dly. That',
        'name .of the': 'name of the',
        'doing them.. These': 'doing them. These',
        'A . It is': 'A. It is',
        'spiritual .redemption': 'spiritual redemption',
        'there .is': 'there is',
        'fieri ,': 'fieri,',
        'exact .perfection': 'exact perfection',
        'is not in us . \\"': 'is not in us.\\"',
        'curse of the law .for us': 'curse of the law for us',
        'not ,': 'not,',
        'jus . But': 'jus. But',
        'labores necessaria . Mihi': 'labores necessaria. Mihi',
        'say)millions': 'say, millions',
        'know]edge': 'knowledge',
        'say)we': 'say, we',
        'part)by': 'part) by',
        'myself(with': 'myself (with',
        'inScripturis': 'in Scripturis',
        'chimerA': 'chimera',
        'InsTitus': 'Instit.',
        'Zephaniah 23:14': '23:14',
        'Colossians 5. 2, 3': 'Colossians 2:2, 3',
        'Ephesians 11:10': 'Ephesians 2:10',
        'de verb. signif, Titus 16:': 'de verb. signif. tit. 16:',
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
        r'(— Thes\.\n\nFrancisci)': '— Thes. Francisci',
        '"De Christo,\'': '"De Christo,"',
        'Hist. Ecclesiastes lib. 5': 'Hist. Eccles. lib. 5',
        'Euseb. Hist. Ecclesiastes lib. 7 cap. 29, 30': 'Euseb. Hist. Eccles. lib. 7 cap. 29, 30',
        'Socrat. Ecclesiastes Hist. lib. 2 cap. 24, 25': 'Socrat. Eccles. Hist. lib. 2 cap. 24, 25',
        'in in odum': 'in modum',
        'put to to give': 'put to, to give',
        'discourse is is evident': 'discourse is, is evident',
        'asserts it it is': 'asserts it, it is',
        'for for that end': 'for that end',
        'which it is is inconsistent': 'which it is, is inconsistent',
        'ca]Ties': 'carries',
        'co]our': 'colour',
        'giguitur in nobis tides': 'gignitur in nobis fides',
        'quae deinde tides': 'quae deinde fides',
        'Isaiah 3:13chap. 3': 'Isaiah 52:13; chap. 52',
        'peculiar to Christ. But, 2. These gentlemen': 'peculiar to Christ. But,\n\n2. These gentlemen',
        'To affirm, on the other side, — (1.)': 'To affirm, on the other side, —\n\n(1.)',
        '; (2.) That he hath': ';\n\n(2.) That he hath',
        '; and, (4.) That he sits': ';\n\n(4.) That he sits',
        r'(\(8\.\)) By this prerogative of certain predictions': '(3.) By this prerogative of certain predictions',
        r"(family of Christ\.')(?!\s*(?:\[f285\]|FNREFTOKEN|<a))": r"\1 [f285]",
        "on that subject [f445]": "on that subject [f446]",
        r"(another apology\.)(?!\s*(?:\[f489\]|FNREFTOKEN|<a))": r"\1[f489]",
        "hosae iin re": "hac in re",
        "Statorii mgenium": "Statorii ingenium",
        "ne ja,": "ne jam,",
        "definite time Ans.": "definite time? Ans.",
        "**Ques. 1.** _What is God_ **Ans.**": "**Ques. 1.** _What is God?_ **Ans.**",
    },
    'regex_replacements': {
        r'divines,\s*—\s*Bull,\s*Waterland,\s*Horsley,\s*Magee,\s*Fuller,\s*Pye\s+Smith,\s*and\s*Wardlaw,\s*—\s*by':
        'divines, — George Bull, Daniel Waterland, Samuel Horsley, William Magee, Andrew Fuller, John Pye Smith, and Ralph Wardlaw, — by',
        r',,': ',',
        r'xauni~am': 'familiam',
        r'con~erendls': 'conferendis',
        # Format the Chapter 3 summary and fix "drape" -> "shape" typo
        r'\[\[SUMMARY\]\] Of the drape and bodily visible figure of God\.\s+MR BIDDLE\'S question:\s*—\s+\[\[SUMMARY\]\] Is God in the Scripture said to have any likeness, similitude, person, shape\?':
        r"[[SUMMARY]] Of the shape and bodily visible figure of God.\n\n[[SUMMARY]] Mr Biddle's question: — Is God in the Scripture said to have any likeness, similitude, person, shape?",
        # Format the Chapter 49 summary and fix "CONCENRING" -> "CONCERNING" typo and stray closing bracket
        r'\[\[SUMMARY\]\] THE DOCTRINE CONCENRING THEM FORMERLY DELIVERED VINDICATED FROM THE ANIMADVERSIONS OF MR\. R\. BAXTER\.\](?=\s+\[f\d+\])':
        r'[[SUMMARY]] THE DOCTRINE CONCERNING THEM FORMERLY DELIVERED VINDICATED FROM THE ANIMADVERSIONS OF MR. R. BAXTER.',
        # Translate the Mercurius Greek quote, using negative lookahead
        r'(serm\. 78: )(Θεὸν μὲν νοῆσαι .*? τοῦτο ἐστιν ὁ Θεός)(?!\s*\[Translated:)':
        r'\1\2 [Translated: “To understand God is difficult, to speak of him is impossible. For the incorporeal cannot be expressed by the corporeal, and the perfect cannot be comprehended by the imperfect, and it is hard for the eternal to associate with the short-lived. For the one is always, but the other passes away; and the one is truth, but the other is shadowed by imagination. The weaker is separated from the stronger, and the smaller from the greater, by as much as the mortal is distant from the divine. The intervening distance dims the vision of the beautiful. For bodies are visible to eyes, and things seen are speakable by the tongue, but that which is incorporeal, invisible, shapeless, and not underlying any matter, cannot be grasped by our senses. I understand, O Tat, I understand what cannot be spoken: this is God.”]',
        # Translate the Calicratides Greek quote, using negative lookahead
        r'(Serm\. 83: )(Τὸ δὲ ἕν ἐστιν .*? διακοσμάσιος)(?!\s*\[Translated:)':
        r'\1\2 [Translated: “But the One is the best, which is, according to our conception, a heavenly, incorruptible living being, the beginning and cause of the ordering of all things.”]',
        # Correct citation typos in Chapter 8
        r'Theodoret, Lib\. 4 Ecclesiastes Hist\., cap\. 10': 'Theodoret, Lib. 4 Eccles. Hist., cap. 10',
        r'Socrat\. Ecclesiastes Hist\. lib\. 6:cap\. 7\.': 'Socrat. Eccles. Hist. lib. 6:cap. 7.',
        r'De Nat\. Deer\.': 'De Nat. Deor.',
        # Correct and translate Rutherford citation and quote in Chapter 49
        r'exercit\. 1, cap\. 2, Titus, \"Quomodo': 'exercit. 1, cap. 2, titulus, "Quomodo',
        # Translate the Racovian Catechism, Smalcius, Schlichting, Faustus Socinus quote (Paragraph 46) in Chapter 49
        r'(Deo obtemperemus,\"\s+etc\..*? Faust\.\s+Socin\.\s+Opusc\.\s+p\.\s+115\.)(?!\s*\[Translated:)':
        r'\1 [Translated: “...we obey God,” etc. — Racovian Catechism, chapter 9, on faith; Volkel, On True Religion, book 4, chapter 3, pp. 179, 180; Smalcius, Refutation of the Theses of Franz, disputation 4, p. 103, and disputation 6, p. 184. “To believe in Christ is nothing else than to trust in him, that is, to obey him under the hope of the promises made to us by him,” etc. — Smalcius, Refutation of the Theses of Franz, disputation 7, p. 209. “Faith in Christ is to place trust in him, and to believe that he is the cause of eternal salvation to all who obey him. If taken properly and strictly, it differs from obedience. But by a certain metonymy or synecdoche it is often taken so broadly as to comprehend all works of piety and justice.” — Schlichting, Commentary on chapter 11 to the Hebrews, p. 519. “What is it to believe in the name of Christ? Answer: To receive him, to have faith in his words, to trust in him, and finally to obey him.” — Anonymous Dialogue on Justification, p. 4. “From these things which have been said so far, it can be sufficiently understood that, although it is most true, as Scripture most openly testifies, that we are saved through the death of Christ and through the shedding of his blood, and our sins are blotted out, yet to believe this very thing is not that faith in Christ by which, as the holy Scriptures teach, we are justified, which many both in the past and today have thought, and so similarly believe; for it is far other to believe that, and under the hope of obtaining eternal life from him, to obey Christ, which was previously said and demonstrated by us to be necessarily required for our justification.” — Fragment on Justification; Faustus Socinus, Minor Works, p. 115.]',
        # Translate Meisner quote (Paragraph 47) in Chapter 49
        r'(\"Patet quam inepte Meisnerus .*? tanquam instrumentum vel manum,\"\s+etc\.\s+—)(?!\s*\[Translated:)':
        r'\1 [Translated: “It is clear how foolishly Meisner calls faith an instrumental cause by which we apprehend or receive justification (or righteousness); it is clear, finally, how falsely (which error follows from the former) he denies that faith, which is a virtue or work, justifies. What could be said more perverse and contrary to the holy Scriptures? It had been too little for us to exclude all other virtues and pious works from obtaining salvation for us, if he had not also branded with so foul an ignominy faith itself in God, the mother and queen of all virtues, after dethroning it from its seat. You understand faith altogether perversely, for you do not consider it as a condition for obtaining justification, but as an instrument or hand,” etc.]',
        # Translate Schlichting and Smalcius quote (Paragraph 48) in Chapter 49
        r'(Jo\.\s+Schlichting\.\s+Disput\.\s+pro\s+Faust\.\s+Socin\.\s+ad\s+Meisner\.\s+p\.\s+129-131\..*? justificationis nostrae\.\"\s+—\s+Smalc\.\s+Refut\.\s+Thes\.\s+Franz\.\s+disp\.\s+4,\s+p\.\s+103\.)(?!\s*\[Translated:)':
        r'\1 [Translated: “Concerning the fact that man receives righteousness, nothing is read in the sacred Scriptures; and if it is explained according to the mind of our adversaries, it is a ridiculous fable.” — Jo. Schlichting, Disputation on behalf of Faustus Socinus against Meisner, pp. 129-131. “But faith is not, accurately speaking, an instrumental cause, but a cause without which not (an efficient cause) of our justification.” — Smalcius, Refutation of the Theses of Franz, disputation 4, p. 103.]',
        # Correct and translate Crellius quote (Paragraph 8) in Chapter 49
        r'\"Causa impulsiva externa sunt peccata nostra, quod itidem aperte sacrae literae docent, dum aiunt, Christum propter peccata nostra percussum, vulneratum, et traditum esse\.\" — Crell, de Calls\. Mort\. Christi, p\. 2\.':
        r'"Causa impulsiva externa sunt peccata nostra, quod itidem aperte sacrae literae docent, dum aiunt, Christum propter peccata nostra percussum, vulneratum, et traditum esse." — Crell, de Causis Mort. Christi, p. 2. [Translated: “The external impulsive cause is our sins, which the holy Scriptures likewise openly teach when they say that Christ was smitten, wounded, and delivered for our sins.”]',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
