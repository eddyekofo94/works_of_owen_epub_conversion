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
<div class="title-line-medium">The Nature of</div>
<div class="title-line-major">Apostasy</div>
<div class="title-connector">from the Profession of the Gospel</div>
<div class="title-connector">and the Punishment of Apostates Declared,</div>
<div class="title-connector">in an Exposition of</div>
<div class="title-line-medium">Hebrews 6:4–6.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"For it is impossible for those who were once enlightened, and have tasted of the heavenly gift, and were made partakers of the Holy Ghost, and have tasted the good word of God, and the powers of the world to come, if they shall fall away, to renew them again unto repentance." — Hebrews 6:4–6.</div></div>
</section>'''

_V7_SPIRITUALLY_MINDED_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-medium">The Grace and Duty of Being</div>
<div class="title-line-major">Spiritually Minded,</div>
<div class="title-connector">Declared and Practically Improved.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"For to be carnally minded is death; but to be spiritually minded is life and peace." — Romans 8:6.</div></div>
</section>'''

_V7_DOMINION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">A Treatise</div>
<div class="title-connector">of the</div>
<div class="title-line-medium">Dominion of Sin and Grace.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"For sin shall not have dominion over you: for ye are not under the law, but under grace." — Romans 6:14.</div></div>
</section>'''
_V7_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 7.</h1>

<h2 class="contents-treatise-title">I. THE NATURE AND CAUSES OF APOSTASY FROM THE GOSPEL</h2>
<p class="contents-item"><a href="ch003.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch004.xhtml">Analysis</a></p>
<p class="contents-item"><a href="ch005.xhtml">To the Reader</a></p>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch006.xhtml">The nature of apostasy from the gospel declared, in an exposition of Hebrews 6:4–6</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch007.xhtml">Partial apostasy from the gospel</a></p>
<p class="contents-desc">Pretences of the church of Rome against the charge of this evil examined and rejected</p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch008.xhtml">Apostasy from the mystery, truth, or doctrine of the gospel</a></p>
<p class="contents-desc">Proneness of persons and churches thereunto — Proved by all sorts of instances</p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch009.xhtml">The reasons and causes of apostasy from the truth or doctrine of the gospel</a></p>
<p class="contents-desc">And the inclination of all sorts of persons thereunto in all ages, inquired into and declared — Uncured enmity in the minds of many against spiritual things, and the effects of it in a wicked conversation, the first cause of apostasy</p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch010.xhtml">Darkness and ignorance another cause of apostasy</a></p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch011.xhtml">Pride and vanity of mind, sloth and negligence, love of the world, causes of apostasy</a></p>
<p class="contents-desc">The work of Satan and judgments of God in this matter</p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch012.xhtml">Instance of a peculiar defection from the truth of the gospel; with the reasons of it</a></p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch013.xhtml">Apostasy from the holiness of the gospel; the occasion and cause of it</a></p>
<p class="contents-desc">Of that which is gradual, on the pretence of somewhat else in its room</p>
<p class="contents-item"><strong>Chapter IX.</strong> <a href="ch014.xhtml">Apostasy into profaneness and sensuality of life — The causes and occasions of it</a></p>
<p class="contents-desc">Defects in public teachers and guides in religion</p>
<p class="contents-item"><strong>Chapter X.</strong> <a href="ch015.xhtml">Other causes and occasions of the decay of holiness</a></p>
<p class="contents-item"><strong>Chapter XI.</strong> <a href="ch016.xhtml">Apostasy from evangelical worship</a></p>
<p class="contents-item"><strong>Chapter XII.</strong> <a href="ch017.xhtml">Inferences from the foregoing discourses</a></p>
<p class="contents-desc">The present danger of all sorts of persons, in the prevalency of apostasy from the truth and decays in the practice of evangelical holiness</p>
<p class="contents-item"><strong>Chapter XIII.</strong> <a href="ch018.xhtml">Directions to avoid the power of a prevailing apostasy</a></p>

<h2 class="contents-treatise-title">II. THE GRACE AND DUTY OF BEING SPIRITUALLY MINDED</h2>
<p class="contents-item"><a href="ch020.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch024.xhtml">Preface</a></p>

<h3 class="contents-part-title">Part I</h3>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch026.xhtml">The words of the text explained</a></p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch027.xhtml">A particular account of the nature of this grace and duty of being spiritually minded</a></p>
<p class="contents-desc">How it is stated in and evidenced by our thoughts</p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch028.xhtml">Outward means and occasions of such thoughts of spiritual things as do not prove men to be spiritually minded</a></p>
<p class="contents-desc">Preaching of the word — Exercise of gifts — Prayer — How we may know whether our thoughts of spiritual things in prayer are truly spiritual thoughts, proving us to be spiritually minded</p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch029.xhtml">Other evidences of thoughts about spiritual things arising from an internal principle of grace, whereby they are an evidence of our being spiritually minded</a></p>
<p class="contents-desc">The abounding of these thoughts, how far, and wherein, such an evidence</p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch030.xhtml">The objects of spiritual thoughts, or what they are conversant about; evidencing them in whom they are to be spiritually minded</a></p>
<p class="contents-desc">Rules directing unto steadiness in the contemplation of heavenly things — Motives to fix our thoughts with steadiness on them</p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch031.xhtml">Directions unto the exercise of our thoughts on things above, things future, invisible, and eternal; on God himself; with the difficulties of it, and oppositions unto it, and the way of their removal</a></p>
<p class="contents-desc">Right notions of future glory stated</p>
<p class="contents-item"><strong>Chapter VII.</strong> <a href="ch032.xhtml">Especial objects of spiritual thoughts on the glorious state of heaven, and what belongs thereunto</a></p>
<p class="contents-desc">First, of Christ himself — Thoughts of heavenly glory in opposition unto thoughts of eternal misery — The use of such thoughts — Advantage in sufferings</p>
<p class="contents-item"><strong>Chapter VIII.</strong> <a href="ch033.xhtml">Spiritual thoughts of God himself</a></p>
<p class="contents-desc">The opposition unto them and neglect of them, with their causes and the way of their prevalency — Predominant corruptions expelling due thoughts of God, how to be discovered, etc. — Thoughts of God, of what nature, and what they are to be accompanied withal, etc.</p>
<p class="contents-item"><strong>Chapter IX.</strong> <a href="ch034.xhtml">What of God or in God we are to think and meditate upon</a></p>
<p class="contents-desc">His being — Reasons of it: oppositions to it; the way of their conquest — Thoughts of the omnipresence and omniscience of God peculiarly necessary — The reasons hereof — As also of his omnipotence — The use and benefit of such thoughts</p>
<p class="contents-item"><strong>Chapter X.</strong> <a href="ch035.xhtml">Sundry things tendered unto such as complain that, they know not how, they are not able to abide in holy thoughts of God and spiritual, or heavenly things, for their relief, instruction, and direction</a></p>
<p class="contents-desc">Rules concerning stated spiritual meditation</p>

<h3 class="contents-part-title">Part II</h3>
<p class="contents-item"><strong>Chapter XI.</strong> <a href="ch037.xhtml">The seat of spiritual mindedness in the affections</a></p>
<p class="contents-desc">The nature and use of them — The ways and means used by God himself to call the affections of men from the world</p>
<p class="contents-item"><strong>Chapter XII.</strong> <a href="ch038.xhtml">What is required in and unto our affections that they may be spiritual</a></p>
<p class="contents-desc">A threefold work on the affections described</p>
<p class="contents-item"><strong>Chapter XIII.</strong> <a href="ch039.xhtml">The work of the renovation of our affections</a></p>
<p class="contents-desc">How differenced from any other impression on or change wrought in them; and how it is evidenced so to be — The first instance, in the universality accompanying of affections spiritually renewed — The order of the exercise of our affections with respect unto their objects</p>
<p class="contents-item"><strong>Chapter XIV.</strong> <a href="ch040.xhtml">The second difference between affections spiritually renewed and those which have been only changed by light and conviction</a></p>
<p class="contents-desc">Grounds and reasons of men’s delight in duties of divine worship, and of their diligence in their performance, whose minds are not spiritually renewed</p>
<p class="contents-item"><strong>Chapter XV.</strong> <a href="ch041.xhtml">Delight of believers in the holy institutions of divine worship</a></p>
<p class="contents-desc">The grounds and reasons thereof — The evidence of being spiritually minded thereby, etc.</p>
<p class="contents-item"><strong>Chapter XVI.</strong> <a href="ch042.xhtml">Assimilation unto things heavenly and spiritual in affections spiritually renewed</a></p>
<p class="contents-desc">This assimilation the work of faith; how, and whereby — Reasons of the want of growth in our spiritual affections as unto this assimilation</p>
<p class="contents-item"><strong>Chapter XVII.</strong> <a href="ch043.xhtml">Decays in spiritual affections, with the causes and danger of them</a></p>
<p class="contents-desc">Advice unto them who are sensible of the evil of spiritual decays</p>
<p class="contents-item"><strong>Chapter XVIII.</strong> <a href="ch044.xhtml">The state of spiritual affections</a></p>
<p class="contents-item"><strong>Chapter XIX.</strong> <a href="ch045.xhtml">The true notion and consideration of spiritual and heavenly things</a></p>
<p class="contents-item"><strong>Chapter XX.</strong> <a href="ch046.xhtml">The application of the soul unto spiritual objects</a></p>
<p class="contents-item"><strong>Chapter XXI.</strong> <a href="ch047.xhtml">Spiritual mindedness life and peace</a></p>

<h2 class="contents-treatise-title">III. A TREATISE OF THE DOMINION OF SIN AND GRACE</h2>
<p class="contents-item"><a href="ch049.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch051.xhtml">To the serious reader</a></p>
<p class="contents-item"><strong>Chapter I.</strong> <a href="ch052.xhtml">What sin is consistent with the state of grace, and what not</a></p>
<p class="contents-desc">Sin’s great design in all to obtain dominion: it hath it in unbelievers, and contends for it in believers — The ways by which it acts</p>
<p class="contents-item"><strong>Chapter II.</strong> <a href="ch053.xhtml">The inquiries for understanding the text proposed</a></p>
<p class="contents-desc">The first spoken to, namely, What is the dominion of sin, which we are freed from and discharged of by grace</p>
<p class="contents-item"><strong>Chapter III.</strong> <a href="ch054.xhtml">The second inquiry spoken to, Whether sin hath dominion in us or not</a></p>
<p class="contents-desc">In answer to which it is showed that some wear sin’s livery, and they are the professed servants thereof — There are many in which the case is dubious, where sin’s service is not so discernible — Several exceptions are put in against its dominion where it seems to prevail — Some certain signs of its dominion — Graces and duties to be exercised for its mortification</p>
<p class="contents-item"><strong>Chapter IV.</strong> <a href="ch055.xhtml">Hardness of heart spoken to as an eminent sign of sin’s dominion</a></p>
<p class="contents-desc">And it is shown that it ought to be considered as total or partial</p>
<p class="contents-item"><strong>Chapter V.</strong> <a href="ch056.xhtml">The third inquiry handled, namely, What is the assurance given us, and what are the grounds thereof, that sin shall not have dominion over us</a></p>
<p class="contents-desc">The ground of this assurance is, that we are “not under the law, but under grace” — The force of this reason shown, namely, How the law doth not destroy the dominion of sin, and how grace dethrones sin and gives dominion over it</p>
<p class="contents-item"><strong>Chapter VI.</strong> <a href="ch057.xhtml">The practical observations drawn from, end application made of, the whole text</a></p>
</section>'''

def html_postprocess_hook(html, ch_context):
    title = ch_context.get('title', '')
    
    # Priority 4: Promote Roman Heading Candidates
    if 'Chapter XX' in title or 'ch046' in ch_context.get('cid', ''):
        old_str = '<p class="list-item list-level-1"><strong>I. 1.</strong> That spiritual life whereof we are made partakers in this world is threefold, or there are three gospel privileges or graces so expressed: —</p>'
        new_str = '<h2 class="roman-subheading"><strong>I. 1.</strong> That spiritual life whereof we are made partakers in this world is threefold, or there are three gospel privileges or graces so expressed: —</h2>'
        html = html.replace(old_str, new_str)
        
    elif 'Prefatory Note' in title and 'Dominion' in title or 'ch049' in ch_context.get('cid', ''):
        old_str1 = '<p class="list-item list-level-1"><strong>I.</strong> As to the <em>nature</em> of this dominion, —</p>'
        new_str1 = '<h3 class="roman-subheading"><strong>I.</strong> As to the <em>nature</em> of this dominion, —</h3>'
        old_str2 = '<p class="list-item list-level-1"><strong>II.</strong> As to the evidence of this dominion, —</p>'
        new_str2 = '<h3 class="roman-subheading"><strong>II.</strong> As to the evidence of this dominion, —</h3>'
        html = html.replace(old_str1, new_str1).replace(old_str2, new_str2)
        
    return html


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
    'regex_replacements': {
        r'\b\s+([.,;:?!])': r'\1',
        r'\(\s+': '(',
        r'\b\s+\)': ')',
        # Collapse double periods and spaced periods inside list markers (Priority 2 & 3)
        r'\*\*(\w+)(\.?)\*\*(\s*)_._': r'**\1.**',
        r'\.{2,}': '.',
    },
    'text_replacements': {
        'sal_ vation': 'salvation',
        'of_ S _atan': 'of Satan',
        'T _he_': 'The',
        'Adul-lam': 'Adullam',
        'so u that': 'so that',
        'them)is': 'them) is',
        'menlHow': 'men! How',
        'it it be under the power': 'if it be under the power',
        'delight in in the': 'delight in, in the',
        'yet to to be': 'yet to be',
        'unto it It is': 'unto it. It is',
        'apostaey': 'apostasy',
        'apostate.s': 'apostates',
        'predomi-nancy': 'predominancy',
        '2dly..': '2dly.',
        '1st..': '1st.',
        'l st .': '1st.',
        'l st.': '1st.',
        '**l** _st_.': '1st.',
        '**l** _st_': '1st',
        'the r own': 'their own',
        ',,': ',',
        '..': '.',
        # Latin tagging (Priority 1) — Regex protected from nested wrapping
        r'(\bsui juris\b(?!</span>))': '<span lang="la">sui juris</span>',
        r'(\bamor patriae, laudumque immensam cupido\b(?!</span>))': '<span lang="la">amor patriae, laudumque immensam cupido</span>',
        r'(\bAmmianus Marcellinus\b(?!</span>))': '<span lang="la">Ammianus Marcellinus</span>',
        r'(\banimae vehicula\b(?!</span>))': '<span lang="la">animae vehicula</span>',
        r'(\bNemo moritur in declinatione morbi\b(?!</span>))': '<span lang="la">Nemo moritur in declinatione morbi</span>',
        r'(\bApostata est osor sui ordinis\b(?!</span>))': '<span lang="la">Apostata est osor sui ordinis</span>',
        r'(\bSolis nosse Deos et coeli Numina vobis Aut solis nescire datum\b(?!</span>))': '<span lang="la">Solis nosse Deos et coeli Numina vobis Aut solis nescire datum</span>',
        r'(\bPrudentia, sapientia, intelligentia, mens, cogitatio, discretio, id quod Spiritus sapit\b(?!</span>))': '<span lang="la">Prudentia, sapientia, intelligentia, mens, cogitatio, discretio, id quod Spiritus sapit</span>',
        r'(\bvox naturae clamantis ad Dominum naturae\b(?!</span>))': '<span lang="la">vox naturae clamantis ad Dominum naturae</span>',
        r'(\bignis fatuus\b(?!</span>))': '<span lang="la">ignis fatuus</span>',
        # OCR fix (Priority 6)
        'conrained': 'contained',
        'con rained': 'contained',
        'The temple of the LORD, The temple of the LORD, are these': 'The temple of the LORD, The temple of the LORD, The temple of the LORD, are these',
    },
    'html_postprocess_hook': html_postprocess_hook,
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
