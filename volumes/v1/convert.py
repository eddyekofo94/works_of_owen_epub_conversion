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


def _postprocess_v1_html(html, chapter):
    """Holistic post-processing for Volume 1, handling Catechisms, chapter summaries, signatures, and Part dividers."""
    # 1. Catechism formatting
    html = _postprocess_v1_catechism_html(html, chapter)

    # 2. Chapter summaries formatting
    html = _postprocess_v1_chapter_summaries(html)

    # 3. Signature block parsing and layout styling (Issue 48)
    sig_pattern = r'<p class="front-matter-prose">Your servant in the work of the Lord,\s*<i>\s*<b>\s*J\.O\.\s*</b>\s*</i>\s*From my Study,\s*September the last,\s*\[1645\]\.</p>'
    sig_replacement = """<div class="epub-signature">
  <p class="signature-intro">Your servant in the work of the Lord,</p>
  <p class="signature-name">J.O.</p>
  <p class="signature-date">From my Study, September the last, [1645].</p>
</div>"""
    html = re.sub(sig_pattern, sig_replacement, html, flags=re.I)

    # 4. Part Title formatting (e.g. Chapter 43 - Part 2 Title Page)
    html = html.replace(
        '<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">PART 2.</h1>',
        '<div class="contents-part-divider"><span class="divider-ornament">❦</span><h3 class="contents-part-title">PART II</h3></div>'
    )

    return html



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

.contents-general-preface {
    margin-top: 1em;
    margin-bottom: 1em;
    font-weight: bold;
    text-align: center;
}
"""

_V1_CHRISTOLOGIA_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="greek-title"><span lang="el" xml:lang="el">ΧΡΙΣΤΟΛΟΓΙΑ:</span></p>
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

<p class="contents-general-preface"><a href="ch001.xhtml">General Preface</a></p>

<h2 class="contents-treatise-title">CHRISTOLOGIA: OR, A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST</h2>
<p class="contents-item"><a href="ch003.xhtml">Prefatory Note</a></p>
<p class="contents-item"><a href="ch004.xhtml">Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch005.xhtml">Peter’s Confession; Matthew 16:16</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch006.xhtml">Opposition made unto the Church as built upon the Person of Christ</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch007.xhtml">The Person of Christ the most ineffable Effect of Divine Wisdom and Goodness</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch008.xhtml">The Person of Christ the Foundation of all the Counsels of God</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch009.xhtml">The Person of Christ the great Representative of God and his Will</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch010.xhtml">The Person of Christ the great Repository of Sacred Truth</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch011.xhtml">Power and Efficacy Communicated unto the Office of Christ, for the Salvation of the Church</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch012.xhtml">The Faith of the Church under the Old Testament in and concerning the Person of Christ</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch013.xhtml">Honor due to the Person of Christ — The nature and Causes of it</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch014.xhtml">The Principle of the Assignation of Divine Honor unto the Person of Christ</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch015.xhtml">Obedience unto Christ — The Nature and Causes of it</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch016.xhtml">The especial Principle of Obedience unto the Person of Christ; which is Love</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch017.xhtml">The Nature, Operations, and Causes of Divine Love, as it respects the Person of Christ</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch018.xhtml">Motives unto the Love of Christ</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch019.xhtml">Conformity unto Christ, and Following his Example</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch020.xhtml">An humble Inquiry into, and Prospect of, the infinite Wisdom of God</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch021.xhtml">Other Evidences of Divine Wisdom in the Contrivance of the Work of Redemption</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch022.xhtml">The Nature of the Person of Christ, and the Hypostatical Union of his Natures Declared</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch023.xhtml">The Exaltation of Christ, with his Present state and Condition in Glory</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch024.xhtml">The Exercise of the Mediatory Office of Christ in Heaven</a></p>

<h2 class="contents-treatise-title">MEDITATIONS AND DISCOURSES ON THE GLORY OF CHRIST</h2>
<p class="contents-item"><a href="ch026.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch027.xhtml">Preface to the Reader</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch028.xhtml">The Explication of the Text; John 17:24</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch029.xhtml">The Glory of the Person of Christ, as the only Representative of God unto the Church</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch030.xhtml">The Glory of Christ in the mysterious Constitution of his Person</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch031.xhtml">The Glory of Christ in his susception of the Office of a Mediator</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch032.xhtml">The Glory of Christ in his Love</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch033.xhtml">The Glory of Christ in the Discharge of his Mediatory Office</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch034.xhtml">The Glory of Christ in his Exaltation, after the accomplishment of the Work of Mediation</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch035.xhtml">Representations of the Glory of Christ under the Old Testament</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch036.xhtml">The Glory of Christ in his intimate Conjunction with the Church</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch037.xhtml">The Glory of Christ in the Communication of himself unto Believers</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch038.xhtml">The Glory of Christ in the Recapitulation of all things in him</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch039.xhtml">Differences between our Beholding the Glory of Christ by Faith and by Sight (First Difference)</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch040.xhtml">The Second Difference between our Beholding the Glory of Christ by Faith and by Sight</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch041.xhtml">Other Differences between our Beholding the Glory of Christ by Faith and by Sight</a></p>

<h2 class="contents-treatise-title">MEDITATIONS AND DISCOURSES CONCERNING THE GLORY OF CHRIST, APPLIED</h2>
<p class="contents-item"><a href="ch042.xhtml">Original Preface</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch044.xhtml">Application of the foregoing Meditations — Exhortation unto such as are not yet Partakers of him</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch045.xhtml">The Way and Means of the Recovery of Spiritual Decays, and of Obtaining fresh Springs of Grace</a></p>

<h2 class="contents-treatise-title">TWO SHORT CATECHISMS</h2>
<p class="contents-item"><a href="ch047.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch048.xhtml">To My Loving Neighbors and Christian Friends</a></p>
<p class="contents-item"><a href="ch049.xhtml">The Lesser Catechism</a></p>
<div class="contents-part-divider">
  <span class="divider-ornament">❦</span>
  <h3 class="contents-part-title">THE GREATER CATECHISM</h3>
</div>
<p class="contents-item"><b>Chapter I.</b> <a href="ch051.xhtml">Of the Scripture</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch052.xhtml">Of God</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch053.xhtml">Of the Holy Trinity</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch054.xhtml">Of the Works of God; and, first, of those that are Internal and Immanent</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch055.xhtml">Of the Works of God that outwardly are of him</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch056.xhtml">Of God’s actual Providence</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch057.xhtml">Of the Law of God</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch058.xhtml">Of the State of Corrupted Nature</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch059.xhtml">Of the Incarnation of Christ</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch060.xhtml">Of the Person of Jesus Christ</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch061.xhtml">Of the Offices of Christ; and first, of his Kingly</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch062.xhtml">Of Christ’s Priestly Office</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch063.xhtml">Of Christ’s Prophetical Office</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch064.xhtml">Of the Twofold Estate of Christ</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch065.xhtml">Of the Persons to whom the Benefits of Christ’s Offices do belong</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch066.xhtml">Of the Church</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch067.xhtml">Of Faith</a></p>
<p class="contents-item"><b>Chapter XVIII.</b> <a href="ch068.xhtml">Of our Vocation, or God’s Calling us</a></p>
<p class="contents-item"><b>Chapter XIX.</b> <a href="ch069.xhtml">Of Justification</a></p>
<p class="contents-item"><b>Chapter XX.</b> <a href="ch070.xhtml">Of Sanctification</a></p>
<p class="contents-item"><b>Chapter XXI.</b> <a href="ch071.xhtml">Of the Privileges of Believers</a></p>
<p class="contents-item"><b>Chapter XXII.</b> <a href="ch072.xhtml">Of the Sacraments of the New Covenant in particular</a></p>
<p class="contents-item"><b>Chapter XXIII.</b> <a href="ch073.xhtml">Of Baptism</a></p>
<p class="contents-item"><b>Chapter XXIV.</b> <a href="ch074.xhtml">Of the Lord’s Supper</a></p>
<p class="contents-item"><b>Chapter XXV.</b> <a href="ch075.xhtml">Of the Communion of Saints</a></p>
<p class="contents-item"><b>Chapter XXVI.</b> <a href="ch076.xhtml">Of Particular Churches</a></p>
<p class="contents-item"><b>Chapter XXVII.</b> <a href="ch077.xhtml">Of the Last Privilege of Believers, — being the Door of Entrance into Glory</a></p>
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
        'Athanasiu6': 'Athanasius',
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
        'stripping h in of his': 'stripping him of his',
        'd imaginem': 'ad imaginem',
        'by the mighty, effectual working of his preaching of the Word': 'by the mighty, effectual working of his Spirit in the preaching of the Word',
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
        
        # Catechism ghosts damaged by AGES footnote columns
        rf'\s*\*\*\s*\]\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)': ' ',
        r'\bNothing at all, being merely(?P<fn>\s+\[f\d+\])?\s+in ourselves\b': r'Nothing at all, being merely wrought upon by the free grace and Spirit of God, when in ourselves\g<fn>',
    },
    'list_item_merge_cap': 40,
    'flat_list_exclude_chapters': [
        "Chapter 1 — Peter's Confession",
    ],
    # Volume 1 Hook: Specialized paragraph merging for Catechisms
    'paragraph_coalesce_hook': _coalesce_v1_catechism_paragraphs,
    'html_postprocess_hook': _postprocess_v1_html,
    'extra_css': _V1_CATECHISM_CSS,
    'contents_page_overrides': _V1_CONTENTS_PAGE,
    'treatise_title_overrides': {
        # All v1 treatise title pages defined here — do NOT put these in render.py or shared.py.
        # Title strings must match the exact chapter title from volumes/v1/intermediate/volume_1.json.
        'Christologia — a Declaration of the Glorious Mystery': _V1_CHRISTOLOGIA_TITLE_PAGE,
        'Meditations and Discourses On The Glory of Christ': _V1_MEDITATIONS_TITLE_PAGE,
        'Part 2 — Meditations and Discourses Concerning The Glory of Christ': _V1_PART_2_TITLE_PAGE,
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
