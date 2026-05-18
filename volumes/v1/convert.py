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

# Ensure the project root is on the path regardless of where this is invoked from
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from extract import extract_volume
from render import render_volume

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

    label = _format_v1_catechism_label(label_match.group('label'), label_num)
    return f'<p class="catechism-item"><b>{label}</b> {rest}</p>'


def _group_v1_catechism_pairs(html):
    qa_pair_re = re.compile(
        r'(?P<q><p class="catechism-item"><b>(?:Ques|Q)\.(?:\s+\d+\.)?</b>.*?</p>)\s*\n\s*'
        r'(?P<a><p class="catechism-item"><b>(?:Ans|A)\.(?:\s+\d+\.)?</b>.*?</p>)',
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
    margin: 1em 0 1.25em;
    break-inside: avoid;
    page-break-inside: avoid;
}

.v1-catechism-pair .catechism-item {
    margin: 0.12em 0 0.2em;
    text-align: left;
    text-indent: 0 !important;
}

.v1-catechism-pair .catechism-item + .catechism-item {
    margin-top: 0.28em;
}

p.catechism-item {
    text-align: left;
    text-indent: 0 !important;
}

.catechism-item b {
    font-weight: 700;
}
"""

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
        'considered?"': 'considered?',
        'Objection .': 'Objection.',
        'Ans .': 'Ans.',
        'Q .': 'Q.',
        'To object of Dr. Owen in this treatise': 'The object of Dr. Owen in this treatise',
        'simple vague and defective': 'simply vague and defective',
        'these apprehensions of Own.': 'these apprehensions of Owen.',
        'The Christology of Owens has always been highly valued': 'The Christology of Owen has always been highly valued',
        'They were among the firsts as the other treatises': 'They were among the first, as the other treatises',
        'publish all the treatises of ushered under their auspices into public notice': 'publish all the treatises of Owen in volumes corresponding in size and appearance with the one ushered under their auspices into public notice',
        'This being the [f8] [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
        'This being the [f9] declare wherein he placed': 'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    },
    'regex_replacements': {
        r'\bknow\.\?': 'know?',
    },
    # Volume 1 Hook: Specialized paragraph merging for Catechisms
    'paragraph_coalesce_hook': _coalesce_v1_catechism_paragraphs,
    'html_postprocess_hook': _postprocess_v1_catechism_html,
    'extra_css': _V1_CATECHISM_CSS,
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
    import argparse
    parser = argparse.ArgumentParser(
        description=f'Convert Owen Works Volume {VOL}',
    )
    parser.add_argument(
        '--extract-only', action='store_true',
        help='Run Stage 1 only (PDF → JSON intermediate)',
    )
    parser.add_argument(
        '--render-only', action='store_true',
        help='Run Stage 2 only (JSON → EPUB, requires existing intermediate)',
    )
    args = parser.parse_args()

    if args.render_only and args.extract_only:
        parser.error('Cannot use both --extract-only and --render-only')

    if not args.render_only:
        print(f'=== Volume {VOL}: Stage 1 — Extract ===')
        extract_volume(VOL, overrides=OVERRIDES)

    if not args.extract_only:
        print(f'=== Volume {VOL}: Stage 2 — Render ===')
        render_volume(VOL, overrides=OVERRIDES)

    print(f'=== Volume {VOL}: Done ===')


if __name__ == '__main__':
    main()
