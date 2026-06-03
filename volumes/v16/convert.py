#!/usr/bin/env python3
"""
Volume 16 — The Works of John Owen, Volume 16: The Church and the Bible
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 16

_V16_GOSPEL_CHURCH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The True Nature</p>
<p class="title-connector">of a</p>
<p class="title-line-major">Gospel Church</p>
<p class="title-connector">and</p>
<p class="title-line-major">Its Government:</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Wherein these following particulars are distinctly handled:</p>
<p class="descriptive">The Subject-Matter of the Church; The Formal Cause of a Particular Church; The Polity, Rule, or Discipline, of the Church in General; The Officers of the Church; The Duty of Pastors of Churches; The Office of Teachers in the Church; The Rule of the Church, or of Ruling Elders; The Nature of Church Polity or Rule, with the Duty of Elders; Of Deacons; Of Excommunication; Of the Communion of Churches.</p>
</section>'''

_V16_LETTER_DISCOURSE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Letter</p>
<p class="title-connector">concerning the matter of the present</p>
<p class="title-line-major">Excommunications.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-line-medium">A Discourse</p>
<p class="title-connector">concerning the</p>
<p class="title-line-major">Administration of Church Censures.</p>
</section>'''

_V16_ANSWER_TWO_QUESTIONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">An Answer Unto</p>
<p class="title-line-major">Two Questions:</p>
<p class="title-connector">with</p>
<p class="title-line-medium">Twelve Arguments against any Conformity to</p>
<p class="title-line-medium">Worship not of Divine Institution.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">"Should ye not hear the words which the Lord hath cried by the former prophets?" — Zechariah 7:7.<br/>
"Happy is he that condemneth not himself in that thing which he alloweth." — Romans 14:22.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-line-medium">Of Marrying after Divorce in case of Adultery.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-line-medium">Of Infant Baptism and Dipping.</p>
</section>'''

_V16_TREATISES_SCRIPTURES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Treatises</p>
<p class="title-connector">Concerning</p>
<p class="title-line-major">The Scriptures.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-line-medium">I. The Divine Original of the Scripture.</p>
<p class="title-line-medium">II. Integrity and Purity of the Hebrew and Greek Text.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">"Search the scriptures; for in them ye think ye have eternal life: and they are they which testify of me." — John 5:39.</p>
</section>'''

_V16_HEBREW_GREEK_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Of the</p>
<p class="title-line-major">Integrity and Purity</p>
<p class="title-connector">of the</p>
<p class="title-line-medium">Hebrew and Greek Text of the Scripture;</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">With Considerations on the Prolegomena and Appendix to the Late</p>
<p class="descriptive">Biblia Polyglotta.</p>
</section>'''

_V16_POSTHUMOUS_SERMONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons:</p>
<p class="title-connector">Or,</p>
<p class="title-line-medium">Thirteen Sermons</p>
<p class="title-connector">Preached on</p>
<p class="title-line-medium">Various Occasions.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">First published in 1756.</p>
</section>'''

_V16_THREE_DISCOURSES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Three Discourses</p>
<p class="title-connector">Suitable to</p>
<p class="title-line-medium">The Lord's Supper.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">Delivered in 1669 and 1674.</p>
</section>'''

def post_extract_hook(intermediate: dict) -> dict:
    chapters = intermediate.get('chapters', [])
    
    # Clean up Prefatory Note titles
    for ch in chapters:
        if ch['title'].startswith('Prefatory Note (Chapter 2'):
            ch['title'] = 'Prefatory Note'
            
    # Remove fragments and duplicates
    drop_titles = {'II. and III.', 'Of Infant Baptism and Dipping.'}
    new_chapters = []
    
    for idx, ch in enumerate(chapters):
        t = ch.get('title', '')
        
        if t in drop_titles:
            continue
            
        if t == 'Answers and Questions':
            ch['title'] = 'An Answer Unto Two Questions.'
            ch['is_treatise'] = True
            
        if t == 'I.':
            ch['title'] = 'Prefatory Note'
            ch['raw_text'] = ch['raw_text'].replace('[[ROMAN_HEAD]] I.\n\n', '')

        if t == 'An Answer Unto Two Questions.' and idx > 18:
            # We already changed chapter 18 to this title. The one at idx 22 is a duplicate fragment.
            continue

        if t == 'Prefatory Note' and len(ch.get('raw_text', '')) < 50:
            continue
            
        new_chapters.append(ch)
        
    intermediate['chapters'] = new_chapters
    
    # Fix lowercase page fragments and splits caused by page boundaries
    for i, ch in enumerate(chapters):
        if ch.get('title') == 'Of Dipping.':
            # This chapter was incorrectly split by PyMuPDF4LLM. The first part belongs to the previous chapter.
            text = ch.get('raw_text', '')
            if 'OF DIPPING.\n\n' in text:
                parts = text.split('OF DIPPING.\n\n', 1)
                # Append the first part to the previous chapter
                chapters[i-1]['raw_text'] = chapters[i-1].get('raw_text', '') + '\n\n' + parts[0].strip()
                # Keep the second part for this chapter
                ch['raw_text'] = parts[1]

    # Run simple replacements on all chapters
    for ch in chapters:
        text = ch.get('raw_text', '')
        text = text.replace('Hebrews 12:23,\n\nthat is, in the Lamb', 'Hebrews 12:23, that is, in the Lamb')
        text = text.replace('the example of his age, as the\n\nwords and scope show.', 'the example of his age, as the words and scope show.')
        text = text.replace('glory and virtue;"\n\nthat is, whatsoever', 'glory and virtue;" that is, whatsoever')
        text = text.replace('Lord, how long?"\n\nhow long shall they!', 'Lord, how long?" how long shall they!')
        ch['raw_text'] = text

    
    # Fix TOC Greek/Hebrew artifacts and typos
    import re
    for fm in intermediate.get('front_matter_items', []):
        html = fm.get('html', '')
        html = html.replace('aujto&gt;grafa', '<span lang="el">αὐτόγραφα</span>')
        html = html.replace('zeopneustoi', '<span lang="el">θεόπνευστοι</span>')
        html = html.replace('ejk tw~n ajduna&gt;twn', '<span lang="el">ἐκ τῶν ἀδυνάτων</span>')
        html = html.replace('zhtei~n to&lt;n Ku&gt;rion eji a]rage yhlafh&gt;seian aujto&lt;n kai&lt;', '<span lang="el">ζητεῖν τὸν Κύριον εἰ ἄραγε ψηλαφήσειαν αὐτὸν καὶ</span>')
        html = html.replace('to&lt; loipo&lt;n ou+n', '<span lang="el">τὸ λοιπὸν οὖν</span>')
        html = html.replace('bytik]W yriq]', '<span lang="he" dir="rtl">קְרִי וּכְתִיב</span>')
        html = html.replace('putty of the originals', 'purity of the originals')
        # Fix the fragmented dash line breaks in the TOC
        html = re.sub(r'</p>\s*<p[^>]*>—</p>\s*<p[^>]*>', ' — ', html)
        fm['html'] = html

    return intermediate


OVERRIDES = {
    'post_extract_hook': post_extract_hook,
    'treatise_title_overrides': {
        'The True Nature of a Gospel Church and Its Government.': _V16_GOSPEL_CHURCH_TITLE_PAGE,
        'A Letter and a Discourse': _V16_LETTER_DISCOURSE_TITLE_PAGE,
        'An Answer Unto Two Questions.': _V16_ANSWER_TWO_QUESTIONS_TITLE_PAGE,
        'Treatises Concerning the Scriptures.': _V16_TREATISES_SCRIPTURES_TITLE_PAGE,
        'Hebrew and Greek Text of the Scripture;': _V16_HEBREW_GREEK_TITLE_PAGE,
        'Posthumous Sermons:': _V16_POSTHUMOUS_SERMONS_TITLE_PAGE,
        'Three Discourses Suitable to the Lordìs Supper.': _V16_THREE_DISCOURSES_TITLE_PAGE,
    },
    'text_replacements': {
        'Concerining': 'Concerning',
        'Lordìs Supper': "Lord's Supper",
        'lordìs supper': "lord's supper",
    },
    'regex_replacements': {
        r'for, — 1\. ': 'for, —\n\n1. ',
        r'required, — 1\. ': 'required, —\n\n1. ',
        r'as, — \[1\.\] ': 'as, —\n\n[1.] ',
        r'are intended: — 1\. ': 'are intended: —\n\n1. ',
        r'name: — 1\. ': 'name: —\n\n1. ',
        r'he, — 1\. ': 'he, —\n\n1. ',
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
