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
<div class="title-line-major">A Display of Arminianism:</div>
<div class="title-connector">Being a Discovery of the Old</div>
<div class="title-line-medium">Pelagian Idol, Free-Will,</div>
<div class="title-connector">with the New Goddess</div>
<div class="title-line-medium">Contingency,</div>
<div class="title-connector">Advancing Themselves into the Throne of God in Heaven, and Deposing His Sacred Providence from the Government of the World.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="quote-block"><p>"Known unto God are all his works from the beginning of the world." — Acts 15:18.</div></div>
</section>'''

_V10_DEATH_OF_DEATH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">Salus Electorum, Sanguis Jesu;</div>
<div class="title-connector">Or,</div>
<div class="title-line-major">The Death of Death</div>
<div class="title-connector">in the</div>
<div class="title-line-major">Death of Christ:</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive">A Treatise of the Redemption and Reconciliation that is in the Blood of Christ; the Merit Thereof, and the Satisfaction Wrought Thereby. Wherein the Proper End of the Death of Christ is Asserted; the Immediate Effects and Fruits Thereof Assigned, with Their Extent in Respect of its Object; and the Whole Controversy about Universal Redemption Fully Discussed.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive" style="text-align: left;">
<strong>In Four Parts.</strong><br/>
1. Declaring the eternal counsel and distinct actual concurrence of the Holy Trinity unto the work of redemption in the blood of Christ; with the covenanted intendment and accomplished end of God therein.<br/>
2. Removing false and supposed ends of the death of Christ, with the distinctions invented to solve the manifold contradictions of the pretended universal atonement; rightly stating the controversy.<br/>
3. Containing arguments against universal redemption from the word of God; with an assertion of the satisfaction and merit of Christ.<br/>
4. Answering all considerable objections as yet brought to light, either by the Arminians or others (their late followers as to this point), in the behalf of universal redemption; with a large unfolding of all the texts of Scripture by any produced and wrested to that purpose.
</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="title-source">"The Son of man came not to be ministered unto, but to minister, and to give his life a ransom for many." — Matthew 20:28.</div>
<div class="title-source">"In whom we have redemption through his blood, the forgiveness of sins, according to the riches of his grace." — Ephesians 1:7.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="title-source">Imprimatur, Jan. 22, 1647. — JOHN CRANFORD.</div>
</section>'''

_V10_DEATH_OF_CHRIST_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-major">The Death of Christ;</div>
<div class="title-connector">the Price He Paid,</div>
<div class="title-connector">and the Purchase He Made.</div>
</section>'''

_V10_DIVINE_JUSTICE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<div class="title-line-medium">A</div>
<div class="title-line-major">Dissertation on Divine Justice:</div>
<div class="title-connector">Or,</div>
<div class="title-line-major">The Claims of Vindicatory Justice</div>
<div class="title-line-medium">Vindicated;</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="descriptive">Wherein that essential property of the divine nature is demonstrated from the sacred writings, and defended against Socinians, particularly the authors of the Racovian Catechism, John Crellius, and F. Socinus himself;</div>
<div class="title-line-medium">Likewise the Necessary Exercise Thereof;</div>
<div class="descriptive">Together with the indispensable necessity of the satisfaction of Christ for the salvation of sinners is established against the objections of certain very learned men, G. Twisse, G. Vossius, Samuel Rutherford, and others.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="title-line-medium">By John Owen,</div>
<div class="title-line-medium">Dean of Christ Church College, Oxford.</div>
<div class="title-rule" aria-hidden="true"></div>
<div class="title-source">"Is God unrighteous who taketh vengeance? God forbid: for then how shall God judge the world?" — Romans 3:5, 6.</div>
<div class="title-source">Oxford: Thomas Robinson. 1653.</div>
</section>'''

_V10_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 10.</h1>

<h2 class="contents-treatise-title">I. A DISPLAY OF ARMINIANISM</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch003.xhtml">To the Committee for Religion</a></p>
<p class="contents-item"><a href="ch004.xhtml">To the Christian Reader</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <strong>Chapters:</strong>
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

<p class="contents-item"><strong>Book I.</strong> <a href="ch023.xhtml">Redemption, Its Agents and Work</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch024.xhtml">1</a> | <a href="ch025.xhtml">2</a> | <a href="ch026.xhtml">3</a> | <a href="ch027.xhtml">4</a> | <a href="ch028.xhtml">5</a> | <a href="ch029.xhtml">6</a> | <a href="ch030.xhtml">7</a> | <a href="ch031.xhtml">8</a>
</p>

<p class="contents-item"><strong>Book II.</strong> <a href="ch032.xhtml">The End of the Death of Christ Stated</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch033.xhtml">1</a> | <a href="ch034.xhtml">2</a> | <a href="ch035.xhtml">3</a> | <a href="ch036.xhtml">4</a> | <a href="ch037.xhtml">5</a>
</p>

<p class="contents-item"><strong>Book III.</strong> <a href="ch038.xhtml">Arguments Against Universal Redemption</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch039.xhtml">1</a> | <a href="ch040.xhtml">2</a> | <a href="ch041.xhtml">3</a> | <a href="ch042.xhtml">4</a> | <a href="ch043.xhtml">5</a> | <a href="ch044.xhtml">6</a> | <a href="ch045.xhtml">7</a> | <a href="ch046.xhtml">8</a> | <a href="ch047.xhtml">9</a> | <a href="ch048.xhtml">10</a> | <a href="ch049.xhtml">11</a>
</p>

<p class="contents-item"><strong>Book IV.</strong> <a href="ch050.xhtml">Objections Answered and Ancient Testimonies</a></p>
<p class="contents-item" style="margin-top: -0.8em; margin-bottom: 1.2em; font-size: 0.85em; color: #555; padding-left: 1.5em;">
  Chapters: 
  <a href="ch051.xhtml">1</a> | <a href="ch052.xhtml">2</a> | <a href="ch053.xhtml">3</a> | <a href="ch054.xhtml">4</a> | <a href="ch055.xhtml">5</a> | <a href="ch056.xhtml">6</a> | <a href="ch057.xhtml">7</a> | <a href="ch058.xhtml">Ancient Testimonies</a>
</p>

<h2 class="contents-treatise-title">III. OF THE DEATH OF CHRIST (REPLY TO BAXTER)</h2>
<p class="contents-item"><a href="ch061.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch062.xhtml">To the Reader</a></p>
<div style="font-size: 0.9em; line-height: 1.6; margin-left: 1.5em; color: #444; margin-bottom: 1.5em;">
  <strong>Chapters:</strong>
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
  <strong>Chapters:</strong>
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
        'which is mostly taken from it.\n\nANALYSIS.\n\nBOOK 1. declares': 'which is mostly taken from it.\n\nBOOK 1. declares',
        'wickedness ;': 'wickedness;',
        'universe ?': 'universe?',
        'viz.: — 1 . Of': 'viz.: — 1. Of',
        'natural sense; 2 . In': 'natural sense; 2. In',
        'Arg. 5 . From': 'Arg. 5. From',
        'Arg. 6 . From': 'Arg. 6. From',
        'John in.\n\n36. To abide argueth': 'John 3:36.\n\nTo abide argueth',
        'Rem. Apol., fol. 96. All which assertions': 'Rem. Apol., fol. 96.\n\nAll which assertions',
        'Seneca, Ep.\n\n117. And again, Aristotle': 'Seneca, Ep. 117.\n\nAnd again, Aristotle',
        'Ecclesiastes 12:12Ecclesiasties 12:12': 'Ecclesiastes 12:12',
        'spritual': 'spiritual',
        'satistfaction': 'satisfaction',
        '_hyothetic': '_hypothetic',
        "Mall's Approach": "Man's Approach",
        '**1** . Of the work;': '**1**. Of the work;',
        '**2** . In a natural sense.': '**2**. In a natural sense.',
        '2 Peter 7 to 8: "': 'chap. vii. to xiii.; "',
        'do)ignorantly': 'do) ignorantly',
    },
    'regex_replacements': {
        '(?s)unworthiest laborer in his vineyard, _J\\.O\\._\\s*<section class="treatise-title-page"[^>]*>.*?</section>': 'unworthiest laborer in his vineyard, _J.O._',
        'T\\. M\\[ore(\\.?)\\]': 'T. More\\1',
        r'fore-ordained\. 2\.\n\nHis prescience,': r'fore-ordained.\n\n2. His prescience,',
        r'\n\n256\. \[f361\] Also,': r'\n\n[f361] Also,',
        r'\n\n3\. chap\. 1, etc\.': r' 3. chap. 1, etc.',
        r'book\n\n9\. "The Thracians': r'book 9.\n\n"The Thracians',
        r'sect\.\n\n8\. But from': r'sect. 8.\n\nBut from',
        r'John in\.\n\n3\. "That which': r'John 3:3.\n\n"That which',
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

    # 4. Inject missing page 91 text into Arminianism Chapter 6
    for ch in chapters:
        if ch.get('title', '').lower().startswith('chapter 6 - how the whole doctrine of predestination'):
            marker = 'his own duty, he is endued, are pleasing to God," Rem. Apol.'
            if marker in ch.get('raw_text', ''):
                missing_text = '\n\n"What hast thou that thou didst not receive?" 1 Corinthians 4:7. "Are we better than they? No, in no wise," Romans 3:9.\n\n[[BLOCKQUOTE]] But we are "predestinated to the adoption of children by Jesus Christ, according to the good pleasure of his will," Ephesians 1:5; John 6:37-39, 10:3, 13:18, 17:6; Acts 13:48; Titus 1:1; 2 Timothy 2:19; James 1:17, 18, etc.\n\nThe sum of their doctrine is: God hath appointed the obedience of faith to be the means of salvation. If men fulfill this condition, he determineth to save them, which is their election; but if, after they have entered the way of godliness, they fall from it, they lose also their predestination. If they will return again, they are chosen anew; and if they can hold out to the end, then, and for that continuance, they are peremptorily elected, or post-destinated, after they are saved. Now, whether these positions may be gathered from those places of Scripture which deliver this doctrine, let any man judge.'
                ch['raw_text'] = ch['raw_text'].replace(marker, marker + missing_text)
                print("Successfully injected missing page 91 text into Volume 10 Chapter 6!")
            break

    # 5. Fix formatting of "Opusc. 6."
    for ch in chapters:
        old_opusc = 'Opusc.\n\n6. de Just. Div. sec. 1.'
        new_opusc = 'Opusc. 6. de Just. Div. sec. 1.'
        if old_opusc in ch.get('raw_text', ''):
            ch['raw_text'] = ch['raw_text'].replace(old_opusc, new_opusc)
            print("Successfully fixed Opusc. 6. list artifact!")
            break

    return data


# Add post_extract_hook to OVERRIDES
OVERRIDES['post_extract_hook'] = post_extract_hook


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
