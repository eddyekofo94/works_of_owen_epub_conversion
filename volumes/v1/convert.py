#!/usr/bin/env python3
"""
Volume 1 — The Works of John Owen, Volume 1: The Glory of Christ
Per-volume converter script.

Usage:
    python3 volumes/v1/convert.py                   # full pipeline (extract + render)
    python3 volumes/v1/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v1/convert.py --render-only     # Stage 2 only (JSON → EPUB)

The OVERRIDES dict below is the place for any Volume 1-specific tweaks.
Most volumes start with an empty dict and grow only when a genuine
volume-specific issue is discovered.
"""

import sys
import os
import html as html_lib

# Ensure the project root is on the path regardless of where this is invoked from
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

import re

# Re-import rendering constants that Catechism logic uses
from render import SCRIPTURE_BOOK_RE

VOL = 1

_V1_CATECHISM_DENSE_RE = re.compile(
    r'<p[^>]*>\s*(?:<b>)?(?:Ques|Ans|Q|A)\.?\b',
    re.I,
)

_V1_CATECHISM_P_RE = re.compile(
    r'<p(?P<attrs>[^>]*)>(?P<body>.*?)</p>',
    re.S,
)

_V1_CATECHISM_BOLD_LABEL_RE = re.compile(
    r'^\s*<b>(?P<label>Ques|Ans|Q|A)\.?(?:\s*(?P<num>\d+)\s*\.?)?</b>\s*',
    re.I | re.S,
)

_V1_CATECHISM_PLAIN_LABEL_RE = re.compile(
    r'^\s*(?P<label>Ques|Ans|Q|A)\.?(?:\s*(?P<num>\d+)\s*\.?)?(?=\s+)\s+',
    re.I | re.S,
)


_V1_CATECHISM_PROOFS_RE = re.compile(
    rf'(?P<pre>.*?)(?P<proof>\b(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b\s+\d+(?::\d+|(?:\s*,\s*\d+)+)?\b.*)$',
    re.I | re.S,
)


def _format_v1_catechism_label(label, num=None):
    canonical = {'q': 'Q', 'ques': 'Ques', 'a': 'A', 'ans': 'Ans'}[label.lower()]
    formatted = f'{canonical}.'
    if num:
        formatted += f' {num}.'
    return formatted


def _normalize_v1_catechism_paragraph(match):
    """V1-only rendered cleanup for Catechism Q/A anchors."""
    body = match.group('body').strip()

    label_match = _V1_CATECHISM_BOLD_LABEL_RE.match(body)
    if label_match:
        rest = body[label_match.end():].strip()
        # Handles OCR/render split forms such as <b>Q.</b> 2 . What...
        trailing_num = re.match(r'^(?P<num>\d+)\s*\.\s+', rest)
        label_num = label_match.group('num')
        if trailing_num and not label_num:
            label_num = trailing_num.group('num')
            rest = rest[trailing_num.end():].strip()
    else:
        label_match = _V1_CATECHISM_PLAIN_LABEL_RE.match(body)
        if not label_match:
            return match.group(0)
        rest = body[label_match.end():].strip()
        label_num = label_match.group('num')

    if not rest:
        return match.group(0)

    label_text = label_match.group('label').lower()
    is_q = label_text in ('q', 'ques')
    item_cls = 'catechism-question' if is_q else 'catechism-answer'

    # Extract and wrap scripture proofs from the end of the answer
    if not is_q:
        proofs_match = _V1_CATECHISM_PROOFS_RE.match(rest)
        if proofs_match:
            pre_text = proofs_match.group('pre').strip()
            proof_text = proofs_match.group('proof').strip()
            pre_text = re.sub(r'\s*[—-]\s*$', '', pre_text).strip()
            rest = f'{pre_text} <span class="catechism-proofs">{proof_text}</span>'

    label = _format_v1_catechism_label(label_match.group('label'), label_num)
    return f'<p class="catechism-item {item_cls}"><b>{label}</b> {rest}</p>'


def _group_v1_catechism_pairs(html):
    # Matches consecutive Question and Answer blocks (taking classes into account)
    qa_pair_re = re.compile(
        r'(?P<q><p class="catechism-item catechism-question"><b>(?:Ques|Q)\.(?:\s+\d+\.)?</b>.*?</p>)\s*\n\s*'
        r'(?P<a><p class="catechism-item catechism-answer"><b>(?:Ans|A)\.(?:\s+\d+\.)?</b>.*?</p>)',
        re.S,
    )
    return qa_pair_re.sub(
        lambda m: (
            '<div class="v1-catechism-pair">\n'
            f'{m.group("q")}\n'
            f'{m.group("a")}\n'
            '</div>'
        ),
        html,
    )


def _postprocess_v1_catechism_html(html, chapter):
    """Polish V1 Lesser/Greater Catechism Q&A rendering after generic HTML output."""
    if not chapter.get('is_catechism_context'):
        return html

    # These chapters have dense Q/A runs. The guard avoids touching ordinary prose
    # paragraphs elsewhere in Volume 1 that happen to start with "A."
    if len(_V1_CATECHISM_DENSE_RE.findall(html)) < 2:
        return html

    html = _V1_CATECHISM_P_RE.sub(_normalize_v1_catechism_paragraph, html)
    return _group_v1_catechism_pairs(html)


_V1_CATECHISM_CSS = """
/* Volume 1-only Catechism polish */
.v1-catechism-pair {
    margin: 1.6em 0;
    padding: 0.9em 1.1em;
    background-color: rgba(42, 85, 160, 0.02) !important; /* Soft Owen Blue background tint */
    border-left: 3px solid rgba(42, 85, 160, 0.35) !important; /* Primary accent line */
    border-radius: 4px;
    break-inside: avoid;
    page-break-inside: avoid;
}

.v1-catechism-pair .catechism-item {
    margin: 0;
    text-align: left;
    text-indent: 0 !important;
}

.v1-catechism-pair .catechism-question {
    color: #111;
    font-weight: 500;
    font-size: 0.98em;
}

.v1-catechism-pair .catechism-question b {
    color: #2a55a0 !important; /* Owen Blue Question Label */
    font-weight: bold;
    margin-right: 0.3em;
}

.v1-catechism-pair .catechism-answer {
    margin-top: 0.6em !important;
    color: #222;
    font-size: 0.96em;
    line-height: 1.55;
}

.v1-catechism-pair .catechism-answer b {
    color: #b08d2d !important; /* Muted Gold Answer Label */
    font-weight: bold;
    margin-right: 0.3em;
}

.v1-catechism-pair .catechism-proofs {
    display: block; /* Sits on its own line below the answer */
    margin-top: 0.55em;
    font-size: 0.85em;
    color: #555;
    font-style: italic;
    line-height: 1.5;
    padding-left: 0.8em;
    border-left: 1.5px solid rgba(0, 0, 0, 0.08); /* Tiny hairline grouping */
}
"""

_V1_CHRISTOLOGIA_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="greek-title"><span lang="el" xml:lang="el">Χριστολογία</span></p>
<p class="title-line-major">Christologia</p>
<p class="title-connector">Or,</p>
<p class="title-line-medium">A Declaration of the Glorious Mystery</p>
<p class="title-connector">of</p>
<p class="title-line-medium">The Person of Christ — God and Man:</p>
<p class="title-connector">with</p>
<p class="descriptive">The Infinite Wisdom, Love, and Power of God in the Contrivance and Constitution Thereof; as also, of the Grounds and Reasons of His Incarnation; the Nature of His Ministry in Heaven; the Present State of the Church Above Thereon; and the Use of His Person in Religion.</p>
<p class="title-connector">with</p>
<p class="descriptive">An Account and Vindication of the Honor, Worship, Faith, Love, and Obedience Due Unto Him, in and from the Church.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Yea doubtless, and I count all things but loss for the excellency of the knowledge of Christ Jesus my Lord: for whom I have suffered the loss of all things, and do count them but dung, that I may win Christ." — Philippians 3:8.</p></div>
</section>'''

_V1_MEDITATIONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Meditations and Discourses</p>
<p class="title-connector">on</p>
<p class="title-line-major">The Glory of Christ,</p>
<p class="title-connector">in</p>
<p class="title-line-medium">His Person, Office, and Grace:</p>
<p class="title-connector">with</p>
<p class="title-line-medium">The Differences Between Faith and Sight;</p>
<p class="title-line-medium">Applied Unto the Use of Them That Believe.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Father, I will that they also, whom thou hast given me, be with me where I am; that they may behold my glory, which thou hast given me: for thou lovedst me before the foundation of the world." — John 17:24.</p></div>
</section>'''

_V1_TWO_CATECHISMS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Two Short Catechisms:</p>
<p class="title-connector">Wherein the</p>
<p class="title-line-medium">Principles of the Doctrine of Christ,</p>
<p class="title-connector">are</p>
<p class="title-line-medium">Unfolded and Explained.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Proper for all Persons to Learn Before They be Admitted to the Sacrament of the Lord's Supper; and Composed for the Use of all Congregations in General.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Come, ye children, hearken to me; I will teach you the fear of the Lord." — Psalm 34:11.</p></div>
</section>'''

_V1_PART_2_TITLE_PAGE = '''<section class="treatise-title-page v1-applied-glory-title" epub:type="titlepage">
<p class="title-line-medium">Meditations and Discourses</p>
<p class="title-connector">Concerning</p>
<p class="title-line-major">The Glory of Christ;</p>
<p class="title-connector">Applied Unto</p>
<p class="title-line-medium">Unconverted Sinners</p>
<p class="title-connector">And</p>
<p class="title-line-medium">Saints Under Spiritual Decays.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">In Two Chapters, from John XVII. 24.</p>
<div class="quote-block"><p>"Father, I will that they also, whom thou hast given me, be with me where I am; that they may behold my glory, which thou hast given me." — John 17:24.</p></div>
</section>'''


_V1_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 1.</h1>
<h2 class="contents-treatise-title">CHRISTOLOGIA: OR, A DECLARATION OF THE<br/>GLORIOUS MYSTERY OF THE PERSON OF<br/>CHRIST.</h2>
<p class="contents-frontmatter-line">PREFATORY NOTE<br/>PREFACE</p>
<p class="contents-item"><b>CHAPTER 1</b> . Peter’s Confession; Matthew 16:16 — Conceits of the Papists thereon — The Substance and Excellency of that Confession.</p>
<p class="contents-item"><b>CHAPTER 2</b> . Opposition made unto the Church as built upon the Person of Christ.</p>
<p class="contents-item"><b>CHAPTER 3</b> . The Person of Christ the most ineffable Effect of Divine Wisdom and Goodness — Thence the next Cause of all True Religion — In what sense it is so.</p>
<p class="contents-item"><b>CHAPTER 4</b> . To Person of Christ the Foundation of all the Counsels of God.</p>
<p class="contents-item"><b>CHAPTER 5</b> . The Person of Christ the great Representative of God and his Will.</p>
<p class="contents-item"><b>CHAPTER 6</b> . The Person of Christ the great Repository of Sacred Truth — Its Relation thereunto.</p>
<p class="contents-item"><b>CHAPTER 7</b> . Power and Efficacy Communicated unto the Office of Christ, for the Salvation of the Church, from his Person.</p>
<p class="contents-item"><b>CHAPTER 8</b> . The Faith of the Church under the Old Testament in and concerning the Person of Christ.</p>
<p class="contents-item"><b>CHAPTER 9</b> . Honor due to the Person of Christ — The nature and Causes of it.</p>
<p class="contents-item"><b>CHAPTER 10</b> . The Principle of the Assignation of Divine Honor unto the Person of Christ, in both the Branches of it; with is Faith in Him.</p>
<p class="contents-item"><b>CHAPTER 11</b> . Obedience unto Christ — The Nature and Causes of it.</p>
<p class="contents-item"><b>CHAPTER 12</b> . The especial Principle of Obedience unto the Person of Christ; which is Love — Its Truth and Reality Vindicated.</p>
<p class="contents-item"><b>CHAPTER 13</b> . The Nature, Operations, and Causes of Divine Love, as it respects the Person of Christ.</p>
<p class="contents-item"><b>CHAPTER 14</b> . Motives unto the Love of Christ.</p>
<p class="contents-item"><b>CHAPTER 15</b> . Conformity unto Christ, and Following his Example.</p>
<p class="contents-item"><b>CHAPTER 16</b> . An humble Inquiry into, and Prospect of, the infinite Wisdom of God, in the Constitution of the Person of Christ, and the Way of Salvation thereby.</p>
<p class="contents-item"><b>CHAPTER 17</b> . Other Evidences of Divine Wisdom in the Contrivance of the Work of Redemption in and by the Person of Christ, in Effects Evidencing a Condecency thereunto.</p>
<p class="contents-item"><b>CHAPTER 18</b> . The Nature of the Person of Christ, and the Hypostatical Union of his Natures Declared.</p>
<p class="contents-item"><b>CHAPTER 19</b> . The Exaltation of Christ, with his Present state and Condition in Glory during the Continuance of his Mediatory Office.</p>
<p class="contents-item"><b>CHAPTER 20</b> . The Exercise of the Mediatory Office of Christ in Heaven.</p>
<h2 class="contents-treatise-title">MEDITATIONS AND DISCOURSES ON THE<br/>GLORY OF CHRIST.</h2>
<p class="contents-frontmatter-line">PREFATORY NOTE BY THE EDITOR<br/>PREFACE TO THE READER</p>
<p class="contents-item"><b>1. — </b> The Explication of the Text; John 17:24</p>
<p class="contents-item"><b>2. — </b> The Glory of the Person of Christ, as the only Representative of God unto the Church</p>
<p class="contents-item"><b>3. — </b> The Glory of Christ in the mysterious Constitution of his Person</p>
<p class="contents-item"><b>4. — </b> The Glory of Christ in his susception of the Office of a Mediator. — First, in his Condescension</p>
<p class="contents-item"><b>5. — </b> The Glory of Christ in his Love</p>
<p class="contents-item"><b>6. — </b> The Glory of Christ in the Discharge of his Mediatory Office</p>
<p class="contents-item"><b>7. — </b> The Glory of Christ in his Exaltation, after the accomplishment of the Work of Mediation in this World</p>
<p class="contents-item"><b>8. — </b> Representations of the Glory of Christ under the Old Testament</p>
<p class="contents-item"><b>9. — </b> The Glory of Christ in his intimate Conjunction with the Church</p>
<p class="contents-item"><b>10. — </b> The Glory of Christ in the Communication of himself unto Believers</p>
<p class="contents-item"><b>11. — </b> The Glory of Christ in the Recapitulation of all things in him</p>
<p class="contents-item"><b>12. — </b> Differences between our Beholding the Glory of Christ by Faith in this World and by Sight in Heaven — The First of them Explained .</p>
<p class="contents-item"><b>13. — </b> The Second Difference between our Beholding the Glory of Christ by Faith in this World and by Sight in Heaven</p>
<p class="contents-item"><b>14. — </b> Other Difference between our Beholding the Glory of Christ by Faith in this World and by Sight in Heaven</p>
<h2 class="contents-treatise-title">MEDITATIONS AND DISCOURSES CONCERNING<br/>THE GLORY OF CHRIST, APPLIED, ETC.</h2>
<p class="contents-frontmatter-line">ORIGINAL PREFACE</p>
<p class="contents-item"><b>1. — </b> Application of the foregoing Meditations concerning the Glory of Christ — First, in an Exhortation unto such as are not yet Partakers of him</p>
<p class="contents-item"><b>2. — </b> The Way and Means of the Recovery of Spiritual Decays, and of Obtaining fresh Springs of Grace</p>
<h2 class="contents-treatise-title">TWO SHORT CATECHISMS.</h2>
<p class="contents-frontmatter-line">PREFATORY NOTE BY THE EDITOR<br/>THE EPISTLE DEDICATORY<br/>THE LESSER CATECHISM</p>
<h2 class="contents-treatise-title">THE GREATER CATECHISM</h2>
<p class="contents-item"><b>1.— </b> Of the Scripture</p>
<p class="contents-item"><b>2. — </b> Of God</p>
<p class="contents-item"><b>3. — </b> Of the Holy Trinity</p>
<p class="contents-item"><b>4. — </b> Of the Works of God; and, first, of those that are Internal and Immanent</p>
<p class="contents-item"><b>5. — </b> Of the Works of God that outwardly are of him</p>
<p class="contents-item"><b>6. — </b> Of God’s actual Providence</p>
<p class="contents-item"><b>7. — </b> Of the Law of God</p>
<p class="contents-item"><b>8. — </b> Of the State of Corrupted Nature</p>
<p class="contents-item"><b>9. — </b> Of the Incarnation of Christ</p>
<p class="contents-item"><b>10. — </b> Of the Person of Jesus Christ</p>
<p class="contents-item"><b>11. — </b> Of the Offices of Christ; and first, of his Kingly</p>
<p class="contents-item"><b>12. — </b> Of Christ’s Priestly Office</p>
<p class="contents-item"><b>13. — </b> Of Christ’s Prophetical Office</p>
<p class="contents-item"><b>14. — </b> Of the Twofold Estate of Christ</p>
<p class="contents-item"><b>15. — </b> Of the Persons to whom the Benefits of Christ’s Offices do belong</p>
<p class="contents-item"><b>16. — </b> Of the Church</p>
<p class="contents-item"><b>17. — </b> Of Faith</p>
<p class="contents-item"><b>18. — </b> Of our Vocation, or God’s Calling us</p>
<p class="contents-item"><b>19. — </b> Of Justification</p>
<p class="contents-item"><b>20. — </b> Of Sanctification</p>
<p class="contents-item"><b>21. — </b> Of the Privileges of Believers</p>
<p class="contents-item"><b>22. — </b> Of the Sacraments of the New Covenant in particular; a holy right whereunto is the Fourth Privilege of Believers</p>
<p class="contents-item"><b>23. — </b> Of Baptism</p>
<p class="contents-item"><b>24. — </b> Of the Lord’s Supper.</p>
<p class="contents-item"><b>25. — </b> Of the Communion of Saints — the Fifth Privilege of Believers</p>
<p class="contents-item"><b>26. — </b> Of Particular Churches</p>
<p class="contents-item"><b>27. — </b> Of the Last Privilege of Believers, — being the Door of Entrance into Glory</p>
</section>'''

_V1_TITLE_SMALL_WORDS = {
    'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'from', 'in', 'into',
    'nor', 'of', 'on', 'or', 'the', 'to', 'unto', 'with', 'within',
}


def _v1_heading_caps_text(text):
    letter_text = ''.join(re.findall(r'[A-Za-z]', text))
    if not letter_text or letter_text != letter_text.upper():
        return text
    tokens = re.split(r'(\s+|—|–|-|:|;|,|\.)', text.lower())
    result = []
    word_index = 0
    force_next_cap = True
    for token in tokens:
        if not token:
            continue
        if re.fullmatch(r'\s+|—|–|-|:|;|,|\.', token):
            result.append(token)
            if token in {'—', '–', '-', ':'}:
                force_next_cap = True
            continue
        if re.search(r'[a-z]', token):
            if token in _V1_TITLE_SMALL_WORDS and word_index > 0 and not force_next_cap:
                result.append(token)
            else:
                result.append(token[:1].upper() + token[1:])
            word_index += 1
            force_next_cap = False
        else:
            result.append(token)
    return ''.join(result)


def _postprocess_v1_chapter_summaries(html):
    """Convert ALL-CAPS chapter summaries/headings to title case.

    [[SUMMARY]] tags may render as either <p class="chapter-summary"> or
    <h3 class="chapter-heading"> depending on context. Both are converted.
    """
    def _convert_caps(text, tag, cls):
        if '<' in text:
            return f'<{tag} class="{cls}">{text}</{tag}>'
        polished = _v1_heading_caps_text(html_lib.unescape(text))
        return f'<{tag} class="{cls}">{html_lib.escape(polished, quote=False)}</{tag}>'

    # Handle <p class="chapter-summary">
    html = re.sub(
        r'<p class="chapter-summary">\s*(.*?)\s*</p>',
        lambda m: _convert_caps(m.group(1).strip(), 'p', 'chapter-summary'),
        html, flags=re.S,
    )
    # Handle <h3 class="chapter-heading">
    html = re.sub(
        r'<h3 class="chapter-heading">\s*(.*?)\s*</h3>',
        lambda m: _convert_caps(m.group(1).strip(), 'h3', 'chapter-heading'),
        html, flags=re.S,
    )
    return html


def _coalesce_v1_catechism_paragraphs(paragraphs):
    """V1-specific: Merge scripture reference paragraphs into the preceding Catechism answer."""
    if not paragraphs:
        return []
    out = []
    for para in paragraphs:
        stripped = para.strip()
        # If this paragraph looks like a bare scripture proof list and the 
        # previous paragraph was an Answer, merge them.
        # Allow leading digits/item markers (Issue 26)
        is_proof = re.match(rf'^(?:\d{{1,3}}\.?\s+)?(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b', stripped, re.I)
        is_catechism_chapter_ref = re.match(r'^[—-]\s*Chap(?:ter)?\.?\s+\d+\b', stripped, re.I)
        if (is_proof or is_catechism_chapter_ref) and out and re.match(r'^(?:\*\*)?(?:A\.|Ans\.)', out[-1].strip(), re.I):
            if is_catechism_chapter_ref:
                stripped = re.sub(r'^[—-]\s*', '— ', stripped)
            # Join with a space (Issue 16)
            out[-1] = out[-1].rstrip() + " " + stripped
        else:
            out.append(para)
    return out

OVERRIDES = {
    'text_replacements': {
        'Origin': 'Origen',
        'εηκκλησίαν': 'ἐκκλησίαν',
        'eccleaism': 'ecclesiam',
        'Charneck': 'Charnock',
        'storage': 'strange',
        'whoso': 'whose',
        'se largely': 'so largely',
        'prevailing task': 'prevailing taste',
        'whoso name': 'whose name',
        'whoso human': 'whose human',
        'secretes': 'secrets',
        'on]y': 'only',
        'name]y': 'namely',
        'learned': 'learned',
        'learnt': 'learnt',
        'learning': 'learning',
        'faithfullness': 'faithfulness',
        r'\(\s+': '(',
        r'\(\s*8\)': ', 8',
        'John 16:1516:15': 'John 16:15',
        '1 John 5:205:20': '1 John 5:20',
        'Romans 1:1Romans': 'Romans 1:1',
        'Matthew 4:1Matthew 4': 'Matthew 4:1',
        # Issue 46: "15:211 Corinthians" — verse fused with next book reference
        '1 Corinthians 15:211 Corinthians': '1 Corinthians 15:21',
        'considered?"': 'considered?',
        'To object of Dr. Owen in this treatise': 'The object of Dr. Owen in this treatise',
        'simple vague and defective': 'simply vague and defective',
        'these apprehensions of Own.': 'these apprehensions of Owen.',
        'The Christology of Owens has always been highly valued': 'The Christology of Owen has always been highly valued',
        'They were among the firsts as the other treatises': 'They were among the first, as the other treatises',
        'publish all the treatises of ushered under their auspices into public notice': 'publish all the treatises of Owen in volumes corresponding in size and appearance with the one ushered under their auspices into public notice',
        'This being the [f8] [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
        'This being the [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
        'open the door, I WILL come in to him, and will sup with him': 'open the door, I will come in to him, and will sup with him',
    },
    'regex_replacements': {
        r'\bknow\.\?': 'know?',

        # Issue 46: AGES ghost duplication — "15:21<ghost>. So he affirms again, 15:21,"
        # The ghost inserts "reparation and recovery from sin. So he affirms again, 1 Cor 15:21,"
        # between the verse ref and its actual continuation.  Strip the ghost clause.
        r'(1 Corinthians 15:21)\s+reparation and recovery from sin\.\s+So he affirms again,\s+1 Corinthians 15:21,': r'\1,',
        # Issue 49: Ch 20 (Chapter 17) para 45 — OCR dropped the terminal period.
        # "...essentially in himself" ends the sentence; must close with a period.
        # Negative lookahead prevents doubling if the period is ever added to the JSON.
        r'essentially in himself(?=["”]?\s*(?:\n|$))': 'essentially in himself.',
    },
    'list_item_merge_cap': 40,
    # Volume 1 Hook: Specialized paragraph merging for Catechisms
    'paragraph_coalesce_hook': _coalesce_v1_catechism_paragraphs,
    'html_postprocess_hook': lambda html, chapter: _postprocess_v1_chapter_summaries(
        _postprocess_v1_catechism_html(html, chapter)
    ),
    'extra_css': _V1_CATECHISM_CSS,
    'contents_page_overrides': _V1_CONTENTS_PAGE,
    'treatise_title_overrides': {
        # All v1 treatise title pages defined here — do NOT put these in render.py or shared.py.
        # Title strings must match the exact chapter title from volumes/v1/intermediate/volume_1.json.
        'Christologia - a Declaration of the Glorious Mystery': _V1_CHRISTOLOGIA_TITLE_PAGE,
        'Meditations and Discourses On The Glory of Christ': _V1_MEDITATIONS_TITLE_PAGE,
        'Part 2 - Meditations and Discourses Concerning The Glory of Christ': _V1_PART_2_TITLE_PAGE,
        'Two Short Catechisms:': _V1_TWO_CATECHISMS_TITLE_PAGE,
    },
    # Volume 1: Tag Greek abbreviations that fall below the 3-codepoint minimum
    # in tag_unicode_ranges(). Also repairs damaged OCR form ".τ. λ." → "κ.τ.λ.".
    # Order matters: normal case first, damaged case second (so its inserted
    # κ.τ.λ. won't be re-matched).
    'inline_html_replacements': {
        'κ.τ.λ.': '<span lang="el" xml:lang="el">κ.τ.λ.</span>',
        '</span>.τ. λ.': '</span><span lang="el" xml:lang="el">κ.τ.λ.</span>',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
