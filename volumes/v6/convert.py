#!/usr/bin/env python3
"""
Volume 6 — The Works of John Owen, Volume 6: Mortification, Temptation, and Psalm 130
Per-volume converter script.

Usage:
    python3 volumes/v6/convert.py                   # full pipeline (extract + render)
    python3 volumes/v6/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v6/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 6

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v6/intermediate/volume_6.json (including punctuation).
# ---------------------------------------------------------------------------

_V6_MORTIFICATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Of the</p>
<p class="title-line-major">Mortification of Sin</p>
<p class="title-connector">in Believers;</p>
<p class="title-line-medium">The Necessity, Nature, and Means of It:</p>
<p class="title-connector">with a Short Discourse of the</p>
<p class="title-line-medium">Dominion of Sin and Grace.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For if ye live after the flesh, ye shall die: but if ye through the Spirit do mortify the deeds of the body, ye shall live." — Romans 8:13.</p></div>
</section>'''

_V6_TEMPTATION_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Of Temptation:</p>
<p class="title-line-medium">The Nature and Power of It;</p>
<p class="title-line-medium">The Danger of Entering into It;</p>
<p class="title-connector">and the</p>
<p class="title-line-medium">Means of Preventing That Danger.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Watch and pray, that ye enter not into temptation: the spirit indeed is willing, but the flesh is weak." — Matthew 26:41.</p></div>
</section>'''

_V6_INDWELLING_SIN_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Nature, Power, Deceit,</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Prevalency</p>
<p class="title-connector">of the Remainders of</p>
<p class="title-line-major">Indwelling Sin</p>
<p class="title-connector">in Believers.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For I know that in me (that is, in my flesh,) dwelleth no good thing: for to will is present with me; but how to perform that which is good I find not." — Romans 7:18.</p></div>
</section>'''

_V6_PSALM_130_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Practical Exposition</p>
<p class="title-connector">upon</p>
<p class="title-line-major">Psalm 130;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Nature and Encouragement of Trust in God</p>
<p class="title-connector">in Depths of Affliction, Sin, and Desertion.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Out of the depths have I cried unto thee, O Lord." — Psalm 130:1.</p></div>
</section>'''
_V6_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 6.</h1>

<h2 class="contents-treatise-title">I. OF THE MORTIFICATION OF SIN IN BELIEVERS</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch003.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch004.xhtml">The foundation of the whole ensuing discourse (Romans 8:13)</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch005.xhtml">The necessity of mortification</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch006.xhtml">The means of mortification: the Spirit</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch007.xhtml">The vigor and comfort of our spiritual life depend on mortification</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch008.xhtml">The first main case of conscience: a lust perplexing</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch009.xhtml">The nature of mortification: what it is not, and what it is</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch010.xhtml">General rules: no mortification without an interest in Christ</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch011.xhtml">The second general rule: without universal sincerity, no lust will be mortified</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch012.xhtml">Particular directions: first, consider the dangerous symptoms of any lust</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch013.xhtml">Get a clear sense of the guilt of the perplexing lust</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch014.xhtml">Load thy conscience with the guilt of it</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch015.xhtml">Thoughtfulness of the majesty and holiness of God</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch016.xhtml">Speak no peace to the heart until God speaks it</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch017.xhtml">The great direction: act faith on Christ</a></p>

<h2 class="contents-treatise-title">II. OF TEMPTATION: THE NATURE AND POWER OF IT</h2>
<p class="contents-item"><a href="ch019.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch020.xhtml">The foundation laid in Matthew 26:41</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch021.xhtml">What it is to "enter into temptation"</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch022.xhtml">The great doctrine: entering into temptation is a highly dangerous state</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch023.xhtml">Particular cases proposed: the first case resolved</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch024.xhtml">The second case proposed: directions to those who are entered into temptation</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch025.xhtml">Of watching that we enter not into temptation</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch026.xhtml">Several acts of watchfulness: watch the heart</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch027.xhtml">Watch against temptation by constant abiding in the hour of trial</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch028.xhtml">General exhortation to watchfulness</a></p>

<h2 class="contents-treatise-title">III. INDWELLING SIN IN BELIEVERS</h2>
<p class="contents-item"><a href="ch030.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch031.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch032.xhtml">Indwelling sin treated of in Romans 7:21</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch033.xhtml">Indwelling sin a law: in what sense</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch034.xhtml">The seat or subject of the law of sin: the heart</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch035.xhtml">Indwelling sin enmity against God</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch036.xhtml">Nature of sin farther discovered as enmity</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch037.xhtml">The work of this enmity: it lusteth</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch038.xhtml">The captivating power of indwelling sin</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch039.xhtml">Indwelling sin proved powerful from its deceit</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch040.xhtml">Deceit in drawing off the mind from duties</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch041.xhtml">Deceit in drawing off the mind from particular duties</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch042.xhtml">The working of sin to entangle the affections</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch043.xhtml">The conception of sin through its deceit</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch044.xhtml">Several ways whereby conceived sin is obstructed</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch045.xhtml">The power of sin demonstrated by its effects in believers</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch046.xhtml">Decays in degrees of grace caused by indwelling sin</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch047.xhtml">The strength of indwelling sin in persons unregenerate</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch048.xhtml">Strength of sin evidenced from its resistance to the law</a></p>

<h2 class="contents-treatise-title">IV. A PRACTICAL EXPOSITION UPON PSALM 130</h2>
<p class="contents-item"><a href="ch050.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch051.xhtml">To the Reader</a></p>
<p class="contents-item"><a href="ch052.xhtml">A Paraphrase on the Psalm</a></p>
<p class="contents-item"><a href="ch053.xhtml">General Scope of the Whole Psalm</a></p>
<p class="contents-item"><b>Verses 1, 2.</b> <a href="ch054.xhtml">The State and Condition of the Soul</a></p>
<p class="contents-item"><a href="ch055.xhtml">Spiritual Depths and Distresses</a></p>
<p class="contents-item"><b>Verse 3.</b> <a href="ch060.xhtml">The Words Explained</a></p>
<p class="contents-item"><b>Verse 4.</b> <a href="ch065.xhtml">The Words Explained: Gospel Forgiveness</a></p>
<p class="contents-item"><b>Verses 5, 6.</b> <a href="ch102.xhtml">The Soul's Waiting in Distresses</a></p>
<p class="contents-item"><b>Verses 7, 8.</b> <a href="ch106.xhtml">Plenteous Redemption</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V6_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V6_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'Mortification of Sin in Believers;': _V6_MORTIFICATION_TITLE_PAGE,
        'Of Temptation:': _V6_TEMPTATION_TITLE_PAGE,
        'The Nature, Power, Deceit, and Prevalency': _V6_INDWELLING_SIN_TITLE_PAGE,
        'Practical Exposition Upon Psalm 130.;': _V6_PSALM_130_TITLE_PAGE,
    },
    'text_replacements': {
        'mortifled': 'mortified',
        'sanctifled': 'sanctified',
        'in in the inward man': 'in the inward man',
        'unto it it hath not': 'unto it, it hath not',
        'in in the business': 'in the business',
        'in in secret': 'is in secret',
        'Proper-ties': 'Properties',
        'fiuctibus': 'fluctibus',
        'legera': 'legem',
        'axe come in': 'are come in',
        'east into': 'cast into',
        'suaxum': 'suarum',
        'seasonlHow': 'season! How',
        'Adam)were': 'Adam) were',
        'the]east': 'the least',
        'the]ate': 'the late',
        'cries to Samuel, "Come in, thou blessed of the Lord; "I have': 'cries to Samuel, "Come in, thou blessed of the Lord; I have',
    },
}


def post_extract_hook(data):
    chapters = data.get("chapters", [])
    
    # Helper to move tail
    def move_tail(idx_a, idx_b, suffix):
        if idx_a >= len(chapters) or idx_b >= len(chapters):
            return
        text_a = chapters[idx_a]['raw_text'].strip()
        text_b = chapters[idx_b]['raw_text'].strip()
        
        if text_a.endswith(suffix):
            chapters[idx_a]['raw_text'] = text_a[:-len(suffix)].strip()
            chapters[idx_b]['raw_text'] = (suffix + " " + text_b).strip()
            print(f"Healed transition {idx_a}->{idx_b} for suffix: '{suffix}'")
        else:
            print(f"WARNING: Transition {idx_a}->{idx_b} failed, suffix '{suffix}' not found at end")

    # Apply transitions on original indices
    move_tail(72, 73, '"Why," saith he, "he')
    move_tail(78, 79, 'forgiveness')
    move_tail(79, 80, 'by invitations,')
    move_tail(80, 81, 'how he should come')
    
    # First set of rules
    move_tail(84, 85, 'temptations,')
    move_tail(85, 86, 'and have no')
    move_tail(86, 87, 'and')
    move_tail(87, 88, 'soul unto more')
    move_tail(88, 89, 'conclude, that')
    move_tail(89, 90, 'adhere to, mere')
    move_tail(90, 91, 'person that he')
    move_tail(91, 92, 'will insensibly')
    move_tail(92, 93, 'do but to')
    
    # Transition 94->95
    move_tail(94, 95, 'So, you')
    
    # Move prefix 96->95
    prefix_96 = 'interest in that forgiveness that is with God; nor dare we, on that account, admit of the consolation that is tendered on the truth insisted on."'
    if 96 < len(chapters):
        text_96 = chapters[96]['raw_text'].strip()
        if text_96.startswith(prefix_96):
            chapters[96]['raw_text'] = text_96[len(prefix_96):].strip()
            chapters[95]['raw_text'] = (chapters[95]['raw_text'].strip() + " " + prefix_96).strip()
            print("Successfully moved prefix from Chapter 96 to Chapter 95!")
        else:
            print("WARNING: Failed to move prefix from Chapter 96!")
            
    # Split Rule 1 and Rule 2 of the second set
    if 96 < len(chapters) and 97 < len(chapters):
        raw_96 = chapters[96]['raw_text']
        parts = raw_96.split('RULE 2.', 1)
        if len(parts) == 2:
            chapters[96]['raw_text'] = parts[0].strip()
            chapters[97]['raw_text'] = ('RULE 2.' + parts[1]).strip()
            print("Successfully split Rule 1 and Rule 2 of second set!")
        else:
            print("WARNING: Failed to split Rule 1 and Rule 2!")
            
    # Move transitions of second set
    move_tail(97, 98, 'he hath left the nature of')
    move_tail(98, 99, 'in')
    move_tail(99, 100, 'doth not')
    move_tail(101, 102, 'faint, and to')
    
    # Delete Chapter 82 (duplicate prefix)
    new_chapters = []
    for ch in chapters:
        if ch.get('title') == 'Rules to Be Observed by Them Who Would Come to Stability in Obedience.':
            print("Deleted Chapter 82 (duplicate prefix)")
            continue
        new_chapters.append(ch)
    data['chapters'] = new_chapters
    
    return data


# Add post_extract_hook to OVERRIDES
OVERRIDES['post_extract_hook'] = post_extract_hook


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
