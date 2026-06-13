#!/usr/bin/env python3
"""
Volume 10 — The Works of John Owen, Volume 10: Arminianism and the Death of Christ
Per-volume converter script.

Source type: ages_pdf

Usage:
    python3 volumes/v10/convert.py                   # full pipeline (extract + render)
    python3 volumes/v10/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v10/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 10

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V10_ARMINIANISM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Display of Arminianism:</p>
<p class="title-connector">Being a Discovery of the Old</p>
<p class="title-line-medium">Pelagian Idol, Free-Will,</p>
<p class="title-connector">with the New Goddess</p>
<p class="title-line-medium">Contingency,</p>
<p class="title-connector">Advancing Themselves into the Throne of God in Heaven, and Deposing His Sacred Providence from the Government of the World.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Known unto God are all his works from the beginning of the world." — Acts 15:18.</p></div>
</section>'''

_V10_DEATH_OF_DEATH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">The Death of Death</p>
<p class="title-connector">in the</p>
<p class="title-line-major">Death of Christ:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">A Treatise in Which the Whole Controversy about Universal Redemption Is Fully Discussed; the Reality and Efficacy of the Satisfaction of Christ Vindicated; and the Doctrine of Particular Redemption Confirmed and Established.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"He shall see of the travail of his soul, and shall be satisfied." — Isaiah 53:11.</p></div>
</section>'''

_V10_DEATH_OF_CHRIST_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">The Death of Christ;</p>
<p class="title-connector">the Price He Paid,</p>
<p class="title-connector">and the Purchase He Made.</p>
</section>'''

_V10_DIVINE_JUSTICE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Dissertation</p>
<p class="title-connector">on</p>
<p class="title-line-medium">Divine Justice;</p>
<p class="title-connector">or, the Claims of</p>
<p class="title-line-medium">Vindicatory Justice.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Wherein the Necessity of Punishing Sin Is Asserted, the Satisfaction of Christ Founded Thereon, and the Remission of Sins Through Him Vindicated.</p>
</section>'''

_V10_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 10.</h1>

<h2 class="contents-treatise-title">I. A DISPLAY OF ARMINIANISM</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch003.xhtml">To the Committee for Religion</a></p>
<p class="contents-item"><a href="ch004.xhtml">To the Christian Reader</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <b>Chapters:</b>
  <a href="ch005.xhtml">1. Arminian Ends</a> | 
  <a href="ch006.xhtml">2. Divine Decrees</a> | 
  <a href="ch007.xhtml">3. Prescience of God</a> | 
  <a href="ch008.xhtml">4. Providence</a> | 
  <a href="ch009.xhtml">5. Resisting God’s Will</a> | 
  <a href="ch010.xhtml">6. Predestination</a> | 
  <a href="ch011.xhtml">7. Original Sin</a> | 
  <a href="ch012.xhtml">8. Adam before the Fall</a> | 
  <a href="ch013.xhtml">9. Death of Christ</a> | 
  <a href="ch014.xhtml">10. Cause of Grace</a> | 
  <a href="ch015.xhtml">11. Salvation apart from Knowledge</a> | 
  <a href="ch016.xhtml">12. Free-Will</a> | 
  <a href="ch017.xhtml">13. Power of Free-Will</a> | 
  <a href="ch018.xhtml">14. Conversion</a>
</div>

<h2 class="contents-treatise-title">II. THE DEATH OF DEATH IN THE DEATH OF CHRIST</h2>
<p class="contents-item"><a href="ch020.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch021.xhtml">Analysis of the Work</a></p>
<p class="contents-item"><a href="ch022.xhtml">To Robert, Earl of Warwick</a></p>

<p class="contents-item"><b>Book I.</b> <a href="ch023.xhtml">Redemption, Its Agents and Work</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch024.xhtml">1</a> | <a href="ch025.xhtml">2</a> | <a href="ch026.xhtml">3</a> | <a href="ch027.xhtml">4</a> | <a href="ch028.xhtml">5</a> | <a href="ch029.xhtml">6</a> | <a href="ch030.xhtml">7</a> | <a href="ch031.xhtml">8</a>
</p>

<p class="contents-item"><b>Book II.</b> <a href="ch032.xhtml">The End of the Death of Christ Stated</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch033.xhtml">1</a> | <a href="ch034.xhtml">2</a> | <a href="ch035.xhtml">3</a> | <a href="ch036.xhtml">4</a> | <a href="ch037.xhtml">5</a>
</p>

<p class="contents-item"><b>Book III.</b> <a href="ch038.xhtml">Arguments Against Universal Redemption</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch039.xhtml">1</a> | <a href="ch040.xhtml">2</a> | <a href="ch041.xhtml">3</a> | <a href="ch042.xhtml">4</a> | <a href="ch043.xhtml">5</a> | <a href="ch044.xhtml">6</a> | <a href="ch045.xhtml">7</a> | <a href="ch046.xhtml">8</a> | <a href="ch047.xhtml">9</a> | <a href="ch048.xhtml">10</a> | <a href="ch049.xhtml">11</a>
</p>

<p class="contents-item"><b>Book IV.</b> <a href="ch050.xhtml">Objections Answered and Ancient Testimonies</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch051.xhtml">1</a> | <a href="ch052.xhtml">2</a> | <a href="ch053.xhtml">3</a> | <a href="ch054.xhtml">4</a> | <a href="ch055.xhtml">5</a> | <a href="ch056.xhtml">6</a> | <a href="ch057.xhtml">7</a> | <a href="ch058.xhtml">Ancient Testimonies</a>
</p>

<h2 class="contents-treatise-title">III. OF THE DEATH OF CHRIST (REPLY TO BAXTER)</h2>
<p class="contents-item"><a href="ch061.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch062.xhtml">To the Reader</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <b>Chapters:</b>
  <a href="ch063.xhtml">1. Occasion</a> | 
  <a href="ch064.xhtml">2. Entrance</a> | 
  <a href="ch065.xhtml">3. Grotius and Baxter</a> | 
  <a href="ch066.xhtml">4. Satisfaction</a> | 
  <a href="ch067.xhtml">5. Justification before Faith</a> | 
  <a href="ch068.xhtml">6. Acts of God’s Will</a> | 
  <a href="ch069.xhtml">7. State of the Elect</a> | 
  <a href="ch070.xhtml">8. Efficacy of Christ’s Death</a> | 
  <a href="ch071.xhtml">9. Immediate Effect</a> | 
  <a href="ch072.xhtml">10. Merit of Christ</a> | 
  <a href="ch073.xhtml">11. State before Believing</a> | 
  <a href="ch074.xhtml">12. Attaining Faith</a> | 
  <a href="ch075.xhtml">13. Conclusion</a>
</div>

<h2 class="contents-treatise-title">IV. A DISSERTATION ON DIVINE JUSTICE</h2>
<p class="contents-item"><a href="ch077.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch078.xhtml">To the Public</a></p>
<p class="contents-item"><a href="ch079.xhtml">To Lord Oliver Cromwell</a></p>
<p class="contents-item"><a href="ch080.xhtml">Preface to the Reader</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <b>Chapters:</b>
  <a href="ch081.xhtml">1. Design</a> | 
  <a href="ch082.xhtml">2. Universal Justice</a> | 
  <a href="ch083.xhtml">3. Vindicatory Justice</a> | 
  <a href="ch084.xhtml">4. Human Sacrifices</a> | 
  <a href="ch085.xhtml">5. Providence</a> | 
  <a href="ch086.xhtml">6. Punitory Justice</a> | 
  <a href="ch087.xhtml">7. God’s Glory</a> | 
  <a href="ch088.xhtml">8. Necessity of Punishment</a> | 
  <a href="ch089.xhtml">9. Crellius Examined</a> | 
  <a href="ch090.xhtml">10. Socinus Examined</a> | 
  <a href="ch091.xhtml">11. Socinian Arguments</a> | 
  <a href="ch092.xhtml">12. Domestic Controversy</a> | 
  <a href="ch093.xhtml">13. Twisse First Argument</a> | 
  <a href="ch094.xhtml">14. Twisse Third Argument</a> | 
  <a href="ch095.xhtml">15. Lubbertus defended</a> | 
  <a href="ch096.xhtml">16. Piscator Review</a> | 
  <a href="ch097.xhtml">17. Rutherford Review</a> | 
  <a href="ch098.xhtml">18. Spiritual Utility</a>
</div>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _V10_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V10_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        'A Display of Arminianism:': _V10_ARMINIANISM_TITLE_PAGE,
        'The Death of Death in the Death of Christ': _V10_DEATH_OF_DEATH_TITLE_PAGE,
        'The Death of Christ,': _V10_DEATH_OF_CHRIST_TITLE_PAGE,
        'A Dissertation on Divine Justice:': _V10_DIVINE_JUSTICE_TITLE_PAGE,
    },
    'text_replacements': {
        'Arminlan': 'Arminian',
        'Arminlanism': 'Arminianism',
        'Pelaglan': 'Pelagian',
        '119 "Infants': '"Infants',
        '120 "Neither': '"Neither',
        '134 "Whether': '"Whether',
        '169 " Can': '"Can',
        '202 "Herein': '"Herein',
        '206 "In': '"In',
        'suit{rig': 'suiting',
        'years)in': 'years) in',
        'licenser)is': 'licenser) is',
        'pro iIlis tan-turn': 'pro illis tantum',
        'lXXXvii': 'LXXXVII',
        'OdysSey': 'Odyssey',
        'ViceChancelor': 'Vice-Chancellor',
        'LoRD': 'LORD',
        'Jude 1:4 4, "Ordained': 'Jude 1:4, "Ordained',
        'no t to': 'not to',
        'w _hole_': 'whole',
        'not of t he': 'not of the',
        'gloW of the divine': 'glory of the divine',
        'his own glow,': 'his own glory,',
        'vindicate his glow,': 'vindicate his glory,',
        'his own gloW': 'his own glory',
        'Christs-coming': "Christ's coming",
        'hunt Mediato-rem': 'hunc Mediatorem',
        'JOHN WHITE .': 'JOHN WHITE.',
        'STANLEY GOWER .': 'STANLEY GOWER.',
        '(as they do )': '(as they do)',
        'knoweth not :': 'knoweth not:',
        'Ephesians 1:4 ,': 'Ephesians 1:4,',
        'therewith ;': 'therewith;',
        'concerning it :': 'concerning it:',
        'etc. Ans .': 'etc. Ans.',
        'saved ;': 'saved;',
        'world ;': 'world;',
        'Grotius !': 'Grotius!',
        'compensation ;': 'compensation;',
        'Luke 12:32 ;': 'Luke 12:32;',
        'obligation: — 1st ,': 'obligation: — 1st,',
        'deos ?': 'deos?',
        'commentaries ;': 'commentaries;',
        'lash ?': 'lash?',
        'wickedness ;': 'wickedness;',
        'universe ?': 'universe?',
        'viz.: — 1 . Of': 'viz.: — 1. Of',
        'natural sense; 2 . In': 'natural sense; 2. In',
        'Arg. 5 . From': 'Arg. 5. From',
        'Arg. 6 . From': 'Arg. 6. From',
    },
    'regex_replacements': {
        '(?s)unworthiest laborer in his vineyard, _J\\.O\\._\\s*<section class="treatise-title-page"[^>]*>.*?</section>': 'unworthiest laborer in his vineyard, _J.O._',
        'T\\. M\\[ore(\\.?)\\]': 'T. More\\1',
        r'fore-ordained\. 2\.\n\nHis prescience,': r'fore-ordained.\n\n2. His prescience,',
    },
}


def post_extract_hook(data):
    chapters = data.get("chapters", [])
    
    # 1. Clean Chapter 1 title (index 80)
    if 80 < len(chapters):
        ch = chapters[80]
        if 'prolepsis' in ch.get('title', '').lower():
            ch['title'] = 'Chapter 1 - The introduction — The design of the work — Atheists — The prolepsis of divine justice in general'
            print("Successfully updated Volume 10 Chapter 1 title!")

    # 2. Clean Chapter 10 title (index 89)
    if 89 < len(chapters):
        ch = chapters[89]
        if 'socinus' in ch.get('title', '').lower():
            ch['title'] = 'Chapter 10 - The opinion of Socinus considered — What he thought of our present question'
            print("Successfully updated Volume 10 Chapter 10 title!")

    # 3. Merge bad split in Chapter 3 (index 34)
    if 34 < len(chapters):
        ch = chapters[34]
        old_txt = "Now, having thus gaily Matthew 20:28, Mark 10:45.\n\ntrimmed and set up"
        new_txt = "Now, having thus gaily Matthew 20:28, Mark 10:45. trimmed and set up"
        if old_txt in ch.get('raw_text', ''):
            ch['raw_text'] = ch['raw_text'].replace(old_txt, new_txt)
            print("Successfully merged scripture paragraph split in Volume 10 Chapter 3!")
        else:
            print("WARNING: Scripture split text not found in Volume 10 Chapter 3!")

    return data


# Add post_extract_hook to OVERRIDES
OVERRIDES['post_extract_hook'] = post_extract_hook


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
