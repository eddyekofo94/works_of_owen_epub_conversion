#!/usr/bin/env python3
"""
Volume 15 — The Works of John Owen, Volume 15: Liturgies, Evangelical Churches, Catechism
Per-volume converter script.

Usage:
    python3 volumes/v15/convert.py                   # full pipeline (extract + render)
    python3 volumes/v15/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v15/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 15 contains:
  - Discourse Concerning Liturgies, and Their Imposition
  - A Discourse Concerning Evangelical Love, Church Peace, and Unity
  - An Inquiry of Evangelical Churches
  - An Answer to Dr Stillingfleet's Book of the Unreasonableness of Separation
    (including: Worship of God and Discipline of the Churches — a sub-treatise)
  - A Short Catechism (with An Explanation upon the Same)

The catechism section (A Short Catechism + Questions 1–53) receives specialised
CSS and postprocessing similar to v1, adapted for v15's chapter-per-question
structure where each "Question N" chapter contains the Q and A inline.

Note: The JSON title "An Axplanation Upon the Same - Questions" is an OCR
corruption of "An Explanation Upon the Same." The key below matches the
corrupted form; text_replacements repairs it in the rendered body.
"""

import os
import sys
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 15

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V15_LITURGIES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Discourse</p>
<p class="title-connector">Concerning</p>
<p class="title-line-medium">Liturgies,</p>
<p class="title-connector">and Their Imposition.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"God is a Spirit: and they that worship him must worship him in spirit and in truth." — John 4:24.</p></div>
</section>'''

_V15_EVANGELICAL_LOVE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Discourse</p>
<p class="title-connector">Concerning</p>
<p class="title-line-medium">Evangelical Love,</p>
<p class="title-line-medium">Church Peace, and Unity;</p>
<p class="title-connector">with the Occasions and Reasons of</p>
<p class="title-line-medium">Present Differences and Divisions</p>
<p class="title-connector">About Things Sacred and Religious.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"<span lang="la" xml:lang="la">Speciosum quidem nomen est pacis, et pulchra opinio unitatis; sed quis ambigat eam solam unicam ecclesiae pacem esse quae Christi est</span>."</p></div>
</section>'''

_V15_INQUIRY_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">An Inquiry</p>
<p class="title-connector">into the Original, Nature, Institution, Power,</p>
<p class="title-connector">Order, and Communion of</p>
<p class="title-line-major">Evangelical Churches.</p>
</section>'''

_V15_STILLINGFLEET_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">An Answer</p>
<p class="title-connector">to</p>
<p class="title-line-medium">Dr Stillingfleet's Book</p>
<p class="title-connector">of the</p>
<p class="title-line-major">Unreasonableness of Separation.</p>
</section>'''

_V15_CATECHISM_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Short Catechism</p>
<p class="title-connector">for the Instruction of the Ignorant</p>
<p class="title-connector">in the Necessary Principles of</p>
<p class="title-line-medium">Christian Religion.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Train up a child in the way he should go: and when he is old, he will not depart from it." — Proverbs 22:6.</p></div>
</section>'''

# ---------------------------------------------------------------------------
# Catechism CSS
# ---------------------------------------------------------------------------

_V15_CATECHISM_CSS = """
/* Volume 15 Catechism polish */
.v15-catechism-question {
    margin: 0.8em 0 0.2em;
    font-weight: 700;
    text-indent: 0 !important;
    text-align: left;
}

.v15-catechism-answer {
    margin: 0.1em 0 0.8em;
    padding-left: 1.2em;
    text-indent: 0 !important;
    text-align: left;
}
"""

# ---------------------------------------------------------------------------
# Catechism postprocessor
# v15 catechism chapters have Q and A inline within each "Question N" chapter.
# We detect the Q./A. labels and apply styled classes.
# ---------------------------------------------------------------------------

_V15_QA_RE = re.compile(
    r'<p(?P<attrs>[^>]*)>\s*(?P<body>(?:<[^>]+>)*\s*(?:Q(?:uestion)?|A(?:ns(?:wer)?)?|Explication)\b.*?)</p>',
    re.S | re.I,
)

def _postprocess_v15_catechism_html(html, chapter):
    """Style Q/A paragraphs in v15 Short Catechism chapters."""
    title = chapter.get('title', '')
    # Only act on catechism chapters
    if not any(t in title for t in ('Catechism', 'Question', 'Questions', 'Axplanation', 'Explanation')):
        return html

    def _style_qa(m):
        body = m.group('body').strip()
        text = re.sub(r'<[^>]+>', '', body)
        if re.match(r'Q(?:uestion)?\b', text, re.I):
            return f'<p class="catechism-item v15-catechism-question">{body}</p>'
        elif re.match(r'(?:A(?:ns(?:wer)?)?|Explication)\b', text, re.I):
            return f'<p class="catechism-item v15-catechism-answer">{body}</p>'
        return m.group(0)

    return _V15_QA_RE.sub(_style_qa, html)


def post_extract_hook(intermediate: dict) -> dict:
    import re
    # Process chapters for sequence split and OCR footnote corruptions
    for ch in intermediate.get('chapters', []):
        text = ch.get('raw_text', '')
        # Fix A. D. 912. 5, 8
        text = text.replace('A. D.\n\n912. 5, 8', 'A. D. 912, sections 5, 8')
        # Fix OCR footnote corruptions (often in Prefaces/Prefatory notes which are processed as chapters)
        text = text.replace('o [f186] to 180', 'of 186 to 180')
        text = text.replace('o [f347] pages', 'of 347 pages')
        text = text.replace('_A_ Elurus', 'Aelurus')
        # Heal faulty paragraph split and match quotes in Chapter 5 (Clemens/Clement)
        text = text.replace(
            'without blame.\n\nBlessed are the elders',
            'without blame. Blessed are the elders'
        )
        # Philippians verse corruptions
        text = text.replace('Philippians 5:2 2:2', 'Philippians 2:2')
        text = text.replace('Philippians 74:25 2:25-28', 'Philippians 2:25-28')
        text = text.replace('Philippians 50:17 2:17', 'Philippians 2:17')
        text = text.replace('Philippians 44:15 2:15', 'Philippians 2:15')
        text = text.replace('Philippians 47:16 2:16', 'Philippians 2:16')
        
        # Heal broken reference continuations causing suspicious large number starts
        text = text.replace('Apol., cap.\n\n30. again', 'Apol., cap. 30. again')
        text = text.replace('Epiphan. Haeres.\n\n42. Montanus', 'Epiphan. Haeres. 42. Montanus')
        text = text.replace('lib. 3 cap.\n\n12. If the reader', 'lib. 3 cap. 12. If the reader')
        text = text.replace('Euseb. lib. 4 cap.\n\n15. So in the excellent', 'Euseb. lib. 4 cap. 15. So in the excellent')

        # Remove leaked AGES scripture tags (e.g. <490416>)
        text = re.sub(r'<\d{6,}>', '', text)
        
        # Unresolved citations fixes
        text = text.replace('Deorum [[BLOCKQUOTE]] comprecatio', 'Deorum comprecatio')
        text = text.replace('opinion with him, lib. 4 cap. 10.', 'opinion with him, Theodoret, lib. 4 cap. 10.')
        text = text.replace('religion as were then fallen out, lib. 39:15:', 'religion as were then fallen out, lib. 39, cap. 15:')
        
        # Spacing and OCR fixes
        text = text.replace('heads _:', 'heads:')
        text = text.replace('efficacy_ ;', 'efficacy;')
        text = text.replace('**2dly** _._', '**2dly.**')
        text = text.replace('**3dly** _._', '**3dly.**')
        text = text.replace('**4thly** _._', '**4thly.**')
        text = text.replace('**1** _._ _Particular', '**1.** _Particular')
        text = text.replace('**1st.**_._', '**1st.**')
        text = text.replace('acqui-escency', 'acquiescency')
        
        # Wrap the Hilary quote in a Latin span and fix the 'earn' -> 'eam' typo
        text = text.replace(
            'Speciosum quidem est nomen pacis, et pulchra opinio unitatis, sed quis ambigat earn solam, unicam, ecclesiae pacem esse, quae Christi est',
            '<span lang="la" xml:lang="la">Speciosum quidem est nomen pacis, et pulchra opinio unitatis, sed quis ambigat eam solam, unicam, ecclesiae pacem esse, quae Christi est</span>'
        )
        # Capitalise 'saith Hilary' to prevent it from merging into the preceding blockquote paragraph
        text = text.replace('saith Hilary. Suppose', 'Saith Hilary. Suppose')
        
        # Priority 2 OCR misreads
        text = text.replace('theft the ', 'that the ')
        text = text.replace('theft it ', 'that it ')
        text = text.replace('theft sentence', 'that sentence')
        text = text.replace('theft numbers', 'that numbers')
        text = text.replace('parochisl', 'parochial')
        text = text.replace('cougregational', 'congregational')
        text = text.replace('ms infinite', 'his infinite')
        text = text.replace('Hobart alarms', 'Hobart affirms')
        text = text.replace('aider Christ', 'after Christ')
        text = text.replace('afar the apostles', 'after the apostles')
        
        ch['raw_text'] = text
        
    # Process front matter items for OCR footnote corruptions
    for fm in intermediate.get('front_matter_items', []):
        for key in ('raw_text', 'html'):
            if key in fm and fm[key]:
                fm[key] = fm[key].replace('o [f186] to 180', 'of 186 to 180')
                fm[key] = fm[key].replace('o [f347] pages', 'of 347 pages')
                fm[key] = fm[key].replace('_A_ Elurus', 'Aelurus')
    return intermediate


OVERRIDES = {
    'post_extract_hook': post_extract_hook,
    'treatise_title_overrides': {
        'Discourse Concerning Liturgies, and Their Imposition.': _V15_LITURGIES_TITLE_PAGE,
        'A Discourse Concerning Evangelical Love, Church Peace, and Unity;': _V15_EVANGELICAL_LOVE_TITLE_PAGE,
        'An Inquiry of Evangelical Churches.': _V15_INQUIRY_TITLE_PAGE,
        "An Answer To Dr Stillingfleet's Book of the Unreasonableness of Separation": _V15_STILLINGFLEET_TITLE_PAGE,
        'A Short Catechism': _V15_CATECHISM_TITLE_PAGE,
    },
    'text_replacements': {
        # Compound word merging fixes (extract.py drops hyphen at line breaks)
        'churchcommunion': 'church-communion',
        'preeminence': 'pre-eminence',
        'churchrule': 'church-rule',
        'churchpower': 'church-power',
        'churchaffairs': 'church-affairs',
        # churchofficers must be processed before churchofficer because it is a superstring.
        # Python 3.7+ preserves dict insertion order.
        'churchofficers': 'church-officers',
        'churchofficer': 'church-officer',
        'churchorder': 'church-order',
        'churchstate': 'church-state',
        'churchsocieties': 'church-societies',
        # OCR corruption in JSON title and body
        'Axplanation': 'Explanation',
        # Repair possessive OCR artifact (shared with v14 pattern)
        "Stillingfleetìs": "Stillingfleet's",
        # Fix consecutive duplicate words
        'the the things': 'the things',
        'is is now': 'is now',
        # Quote matching and OCR repairs
        'is "written for our admonition, 1 Corinthians 10:11;': 'is "written for our admonition," 1 Corinthians 10:11;',
        '"Igitur,!\'': '"Igitur,"!',
        "To which he replies, This is the apostle's rule,": 'To which he replies, "This is the apostle\'s rule,',
        'single congregation? Why so?': 'single congregation?" Why so?',
        'giving us caution not to lose those things which we have wrought,"': 'giving us caution "not to lose those things which we have wrought,"',
        "inheritance,''": 'inheritance,"',
        "''Wherefore did": '"Wherefore did',
        'Either, then, he must quit': '"Either, then, he must quit',
        '"But, saith he, "I': '"But," saith he, "I',
        'the presbyters or elders of the church,"': 'the presbyters or elders of the church,',
        # Spelling and spacing repairs
        'lieS': 'lies',
        'thiS': 'this',
        'mahLtain': 'maintain',
        'heads :': 'heads:',
        ',,': ',',
        'it ?': 'it?',
        'infected ?': 'infected?',
        'efficacy ;': 'efficacy;',
    },
    'regex_replacements': {
        # Fix doubled punctuation sequence where word boundary would fail
        'murder!!': 'murder!',
    },
    'extra_css': _V15_CATECHISM_CSS,
    'html_postprocess_hook': _postprocess_v15_catechism_html,
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()

