#!/usr/bin/env python3
"""
render.py — Stage 2: Rendering and EPUB3 assembly.

Responsible for:
  - markdown_to_html() and all paragraph/inline rendering helpers
  - Catechism Q&A rendering
  - Greek/Hebrew Unicode tagging (tag_unicode_ranges, force_polyglot_mapping)
  - EPUB3 assembly: nav, ncx, title page, endnotes, cover, frontispiece
  - find_cover(), find_portrait(), generate_nav_xhtml(), etc.
  - Scholastic anchor post-processor

Imported by converter.py (legacy orchestrator) and volumes/vN/convert.py.
Issue 91: Extracted from converter.py as part of the two-stage modular refactor.
"""

import sys, os, re, uuid, shutil, zipfile, tempfile, hashlib, json, subprocess
from datetime import datetime
from html import escape as _html_escape
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

_RENDER_DIR = Path(__file__).parent.resolve()
if str(_RENDER_DIR) not in sys.path:
    sys.path.insert(0, str(_RENDER_DIR))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    convert_greek_word,
    clean_greek_text, convert_gideon_hebrew, polytonic_sweep,
)

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed.")

FONT_BASE = os.path.join(_RENDER_DIR, 'fonts')


# ================================================================
# SHARED CONSTANTS (also used by extract.py)
# ================================================================

# ─── Font Detection ────────────────────────────────────────────
GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}

# Regex for detecting Beta Code words that missed font tagging.
# Keep this conservative: the fallback runs after ordinary prose has been
# escaped, so broad markers like apostrophe or leading j/J corrupt English
# words such as "author's", "Jesus", "John", and "justification".
BETA_CODE_RE = re.compile(
    r"(?<!\S)(?![^æ;]*[æ;])(?:"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+[><=~|{}\[\]+]+"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
    r"[><=~|{}\[\]+]+[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+"
    r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
    r"pneu'ma"
    r")\.?(?!\S)"
)

# Regex for detecting Gideon Hebrew words that missed font tagging.
# Matches words containing unambiguous Gideon-only marks. Plain semicolon,
# bracket, and digit 1 are ordinary English/list punctuation and caused major
# false positives ("grace;" and "vol. 1" became Hebrew).
GIDEON_HEBREW_RE = re.compile(r'(?<!\S)[a-zA-Z\[\];1]*(?:[æ}])[a-zA-Zæ}\];1\[]*\.?(?!\S)')

FOOTNOTE_MARKER_RE = re.compile(r'\[f(\d+)\]')
LOOSE_FOOTNOTE_MARKER_RE = re.compile(
    r'\[\s*f\s*(\d{1,3})\s*\]|(?<![A-Za-z])f\s*(\d{1,3})\b',
    re.I,
)
FOOTNOTE_PLACEHOLDER_RE = re.compile(r'FNREFTOKEN(\d+)TOKEN')
FT_MARKER_RE = re.compile(r'^ft(\d+)\s*', re.I)
EMPTY_BRACKET_RE = re.compile(r'\[\s*\]')
STRUCTURAL_START_RE = re.compile(
    r'^(?:'
    r'(?!\d{4}\.)\d{1,3}\.\s+|'                         # 5. Mankind...
    r'\((?!\d{4}\))\d+\.?\)\s+|'                    # (1.) There... / (1) There...
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\s+|'  # (1st,) Such...
    r'\[\d+\.?\]\s+|'                    # [1.] There...
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\s+|'  # [1st,] There...
    r'[IVXLCDM]+\.\s+|'                  # I. / II.
    r'[A-Z]\.\s+|'                       # Q. / A. catechism lines
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]\s+|'  # 1st, 2nd, 3rd, 4th,
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?\s+|'  # 2ndly, 3rdly
    r'(?:First|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly|Again|But)\b[,.]?\s+'
    r')'
)
STRUCTURAL_PREFIX_HTML_RE = re.compile(
    r'^(?P<marker>'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
    r'[IVXLCDM]+\.|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<space>\s+)'
)
INLINE_STRUCTURAL_MARKER_RE = re.compile(
    r'(?<!^)(?P<lead>\s+)'
    r'(?P<marker>'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
    r'\*\*\d+\.\*\*|'
    r'\*\*\((?!\d{4}\))\d+\.?\)\*\*|'
    r'\*\*\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\*\*|'
    r'\*\*\[\d+\.?\]\*\*|'
    r'\*\*\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\*\*|'
    r'\*\*\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)\*\*\s*[,.;]?|'
    r'\*\*[IVXLCDM]+\.\*\*|'
    r'[IVXLCDM]+\.|'
    r'(?<![:\d-])(?!\d{4}\.)\d+\.|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<trail>\s+)'
)
ROMAN_HEADING_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?\s+(?P<rest>.+)$')
ROMAN_ONLY_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$')
PLAIN_CHAPTER_RE = re.compile(r'^(CHAPTER\s+\d+\.?)(?:\s+(.+))?$')
CITATION_ABBREV_TRAIL_RE = re.compile(
    r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|q|a|p)\.?\s*$'
    r'|'
    # Page references: "p. 43" or "pp. 43" — should not be sentence ends
    r'\bp+\.\s+\d{1,4}\s*$'
    r'|'
    # Scripture book abbreviations before chapter:verse — e.g. "Cant. 5:10"
    r'\b(?:Cant|Prov|Eccl|Sol|Isa|Jer|Lam|Ezek|Dan|Hos|Zeph|Zech|Mal|'
    r'Matt|Mk|Lk|Jn|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Rev)\.\s*$',
    re.I,
)
CITATION_ABBREV_START_RE = re.compile(
    r'^(?:Lib|Serm|Sermo|Epist|Ep|Cap|Chap|Orat|Tract|Homil|Haer|Dial)\.\s+',
    re.I,
)
CITATION_AUTHOR_TRAIL_RE = re.compile(
    r'\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|'
    r'Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan)\.?\s*$',
    re.I,
)
ROMAN_LIST_TOKEN = '@@ROMAN_LIST@@'
MARKDOWN_STRUCTURAL_START_RE = re.compile(
    r'^\*\*(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
    r'\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\*\*\s*[,.;]?\s+'
)
# ================================================================
# SCHOLASTIC ANCHOR POST-PROCESSOR
# ================================================================

_SCHOLASTIC_LABEL_RE = re.compile(
    r'(?<![A-Z])'           # Not mid-word all-caps
    r'(?P<label>'
    r'(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.'
    r')'
    r'(?P<rest>\s)',
    re.I,
)

_SCHOLASTIC_ANCHOR_SPLIT_RE = re.compile(
    r'([.!?"\u201d])\s+'           # closing punctuation / quote
    r'(?P<label>'
    r'(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.'
    r')\s',
    re.I,
)

# Pattern to detect "Objection ." (space before period) — OCR artifact
_SCHOLASTIC_SPACE_DOT_RE = re.compile(
    r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application)\s+\.',
    re.I,
)


def apply_scholastic_anchor_protocol(html: str) -> str:
    """Post-processor: ensure Obj./Ans./Use. labels start their own paragraphs.

    Runs on the assembled chapter XHTML string after markdown_to_html().
    Three transformations:
      1. Normalize "Objection ." → "Objection." (stray space OCR artifact).
      2. Force </p><p> break before any Obj./Ans./Use. label that appears
         mid-paragraph after closing punctuation.
      3. Wrap the label itself in <b> and assign class="scholastic-anchor".
    """
    # 1. Remove stray space before period in scholastic labels
    html = _SCHOLASTIC_SPACE_DOT_RE.sub(lambda m: m.group(1) + '.', html)

    # 2. Force paragraph break before scholastic labels that appear mid-paragraph
    def _split_before_label(m: re.Match) -> str:
        return f'{m.group(1)}</p>\n<p class="scholastic-anchor"><b>{m.group("label")}</b> '

    html = _SCHOLASTIC_ANCHOR_SPLIT_RE.sub(_split_before_label, html)

    # 3. Ensure labels at paragraph start are bold
    html = re.sub(
        r'(<p(?:\s[^>]*)?>)\s*'
        r'(?P<label>(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.)\s',
        lambda m: f'{m.group(1)}<b class="scholastic-label">{m.group("label")}</b> ',
        html,
        flags=re.I,
    )

    return html


# ================================================================
# SPACED-CAPS AND I WILL OCR NORMALIZATION
# ================================================================

_SPACED_CAPS_RE = re.compile(r'\b([A-Z](?:\s[A-Z]){2,})\b')
_I_WILL_RE = re.compile(r'\bI\s*WILL\b|\bIWILL\b', re.I)
_I_AM_RE = re.compile(r'\bI\s*AM\b|\bIAM\b', re.I)


def _normalize_spaced_caps(text: str) -> str:
    """Collapse M E → ME, T H E → THE for all-caps spaced sequences."""
    def _join(m: re.Match) -> str:
        return m.group(1).replace(' ', '')
    return _SPACED_CAPS_RE.sub(_join, text)


def _normalize_i_will(text: str) -> str:
    """Normalize IWILL → I WILL, i am → I AM etc."""
    text = _I_WILL_RE.sub('I WILL', text)
    text = _I_AM_RE.sub('I AM', text)
    return text


def _repair_owen_ocr_errors(text: str) -> str:
    """
    Repair known OCR character misreads specific to Owen/AGES extraction.
    Separate from _repair_known_source_losses() which handles source loss patterns.
    """
    corrections = {
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
        r'(\w+)]y\b': r'\1ly',
        # Add more as they are discovered
    }
    result = text
    for wrong, right in corrections.items():
        if wrong.startswith('(') or wrong.endswith('\\b'):
             result = re.sub(wrong, right, result)
        else:
             result = re.sub(r'\b' + re.escape(wrong) + r'\b', right, result)
    return result
SCRIPTURE_BOOK_RE = (
    r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|'
    r'Proverbs|Ecclesiastes|Song|Isaiah|Jeremiah|Lamentations|Ezekiel|'
    r'Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|'
    r'Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|'
    r'Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|'
    r'Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|'
    r'Revelation)'
)
SCRIPTURE_REF_RE = re.compile(
    rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*|\b\d+:\d+(?:[-,]\s*\d+)*',
    re.I,
)
SCRIPTURE_CONTINUATION_TRAIL_RE = re.compile(
    rf'(?:\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+)?\d+:\d+(?:[-,;]\s*\d+)*[,:;]?\s*$|'
    rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+(?:[-,;]\s*\d+)*,\s*$|'
    r'\b(?:verse|verses|chap|chapter)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$|'
    r'\b(?:cap|lib)\.?\s+\d+(?:[-,;]\s*\d+)*,\s*$',
    re.I,
)
def normalize_footnote_markers(text):
    """Normalize AGES inline footnote markers like f2 or [ f2] to [f2]."""
    def repl(match):
        return f'[f{match.group(1) or match.group(2)}]'

    return LOOSE_FOOTNOTE_MARKER_RE.sub(repl, text)


def _noteref_link(fn_num):
    return (
        f'<a class="noteref" epub:type="noteref" role="doc-noteref" '
        f'href="endnotes.xhtml#fn{fn_num}"><sup>{fn_num}</sup></a>'
    )


def _restore_footnote_placeholders(text):
    # Remove any space immediately before the noteref token so spacing is
    # handled purely by CSS (margin-right on .footnote-marker) rather than
    # a literal space character — this avoids "noteref leading space" blemish.
    text = re.sub(r'\s+(FNREFTOKEN\d+TOKEN)', r'\1', text)
    return FOOTNOTE_PLACEHOLDER_RE.sub(lambda m: _noteref_link(m.group(1)), text)


def _strip_footnote_placeholders(text):
    return FOOTNOTE_PLACEHOLDER_RE.sub(' ', text)
def title_case(text):
    """Convert text to Title Case, preserving Roman numerals and small words."""
    if not text:
        return ""
    small_words = {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'en', 'for',
                   'if', 'in', 'of', 'on', 'or', 'the', 'to', 'v', 'via', 'vs'}
    words = text.split()
    res = []
    for i, w in enumerate(words):
        clean_w = w.strip('.,:;()[]"').upper()
        if re.match(r'^[IVXLCDM]+$', clean_w):
            res.append(w.upper())
        elif i > 0 and w.lower() in small_words:
            res.append(w.lower())
        else:
            res.append(w.capitalize())
    return " ".join(res)


def nav_display_title(text):
    """Display front-matter labels in NAV as they appear in the PDF."""
    stripped = (text or '').strip()
    normalized = stripped.rstrip('.').upper()
    if normalized in {
        'GENERAL PREFACE',
        'PREFATORY NOTE',
        'PREFACE',
        'PREFACE TO THE READER',
        'ORIGINAL PREFACE',
    }:
        return normalized + ('.' if stripped.endswith('.') else '')
    return title_case(stripped)
def _norm_for_dedupe(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\[f\d+\]', ' ', text)
    text = text.lower()
    text = re.sub(r'[^a-z0-9:]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _is_scripture_ref_fragment(text):
    """Return True when a paragraph is almost entirely a scripture reference list."""
    clean = re.sub(r'\[f\d+\]', '', text).strip()
    if len(clean) > 220:
        return False
    if not SCRIPTURE_REF_RE.search(clean):
        return False
    leftovers = SCRIPTURE_REF_RE.sub('', clean)
    leftovers = re.sub(r'[;:,.()\-\s]', '', leftovers)
    return len(leftovers) <= 12


def _scripture_ref_tokens(text):
    """Return a normalised list of all scripture reference strings in text."""
    tokens = []
    for m in SCRIPTURE_REF_RE.finditer(text):
        token = re.sub(r'\s+', ' ', m.group(0).lower())
        token = re.sub(r'^(?:[1-3]\s+)?', '', token)
        tokens.append(token)
    return tokens
def _split_inline_structural_markers(para):
    """Promote inline Owen list markers to paragraph starts."""
    pieces = []
    pos = 0
    for match in INLINE_STRUCTURAL_MARKER_RE.finditer(para):
        before = para[pos:match.start()].strip()
        marker = match.group('marker')
        after_start = match.start('marker')

        marker_is_wrapped = marker.startswith(('(', '[', '**(', '**['))
        has_list_intro_before_reference = bool(re.search(
            r'\b(?:here\s+is|here\s+are|as\s+follows|following)\b.{0,320}$',
            before,
            re.I,
        ))
        # Skip roman numeral ranges like "III. — VI."
        if (
            re.match(r'^[IVXLCDM]+\.$', marker, re.I)
            and re.match(r'\s*[—–-]\s*[IVXLCDM]+\.', para[match.end():])
        ):
            continue
        if (
            (
                SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
                or CITATION_ABBREV_TRAIL_RE.search(before[-80:])
                or re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
                or re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
                or (para[:match.start()].count('"') % 2 != 0)
                or (para[:match.start()].count('\u201c') > para[:match.start()].count('\u201d'))
            )
            and not marker_is_wrapped
            and not has_list_intro_before_reference
        ):
            continue

        before_ends_structural = bool(re.search(r'[,;:—-]\s*$', before))
        before_ends_terminal = bool(re.search(r'[.!?]["”’)\]]?\s*$', before))
        before_ends_lead_word = bool(re.search(
            r'\b(?:wherefore|therefore|for|but|and|or|as)\s*$',
            before,
            re.I,
        ))
        before_ends_objection = bool(re.search(r'\b(?:Objection|Obj)\b\.?\s*$', before, re.I))
        if len(before) < 12 and not (before_ends_structural or before_ends_lead_word or before_ends_objection):
            continue
        marker_clean = re.sub(r'[\*\[\]\(\),;.\s]', '', marker).lower()
        marker_is_bare_decimal = bool(re.match(r'^(?:\*\*)?\d+\.(?:\*\*)?$', marker.strip()))
        marker_is_bare_roman = bool(re.match(r'^(?:\*\*)?[IVXLCDM]+\.(?:\*\*)?$', marker.strip(), re.I))
        marker_is_bare_ordinal = bool(re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b,?\s*(?:\*\*)?$', marker.strip(), re.I))
        after_preview = para[match.end():match.end() + 80].lstrip()
        after_starts_like_heading = bool(re.match(r'[A-Z“"‘]', after_preview))
        strong_source_like_marker = (
            (marker_is_bare_decimal or marker_is_bare_roman or marker_is_bare_ordinal)
            and len(before) >= 35
            and after_starts_like_heading
            and not SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
            and not CITATION_ABBREV_TRAIL_RE.search(before[-80:])
            and not re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', before, re.I)
            and not re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
            and not re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
            and marker_clean not in {'i', 'v', 'x', 'l', 'c', 'd', 'm'}
        )
        if not (re.search(r'[.,;:—-]\s*$', before) or before_ends_terminal or before_ends_lead_word or before_ends_objection):
            if not (marker_is_wrapped or strong_source_like_marker):
                continue

        if before:
            pieces.append(before)
        pos = after_start

    if not pieces:
        return [para]

    tail = para[pos:].strip()
    if tail:
        pieces.append(tail)
    return pieces
def _repair_known_catechism_ghosts(text):
    """Repair source-confirmed catechism phrases damaged by AGES footnote columns."""
    text = re.sub(
        rf'\s*\*\*\s*\]\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)',
        ' ',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bby the mighty, effectual working of his preaching of the Word\b',
        'by the mighty, effectual working of his Spirit in the preaching of the Word',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bNothing at all, being merely(?P<fn>\s+\[f\d+\])?\s+in ourselves\b',
        lambda match: (
            'Nothing at all, being merely wrought upon by the free grace '
            f'and Spirit of God, when in ourselves{match.group("fn") or ""}'
        ),
        text,
        flags=re.I,
    )
    return text
def _trim_duplicate_reference_prefix(prev, current):
    """Drop a leading scripture-reference run when the same refs just appeared."""
    if not prev or not current:
        return current
    pos = 0
    refs = []
    while pos < len(current):
        while pos < len(current) and current[pos].isspace():
            pos += 1
        match = SCRIPTURE_REF_RE.match(current, pos)
        if not match:
            break
        refs.append(re.sub(r'\s+', ' ', match.group(0).lower()))
        pos = match.end()
        while pos < len(current) and current[pos] in ' ;,.:':
            pos += 1

    if not refs:
        return current

    prev_refs = set(_scripture_ref_tokens(prev))
    normalized_refs = {re.sub(r'^(?:[1-3]\s+)?', '', ref) for ref in refs}
    if normalized_refs and normalized_refs <= prev_refs:
        return current[pos:].lstrip()
    return current
def force_polyglot_mapping(text):
    """
    Aggressive regex fallback to convert Beta Code and Gideon Hebrew that
    missed font detection. Splits by tags to avoid corrupting HTML.
    """
    if not text:
        return ""
    
    # Pass 1: Hebrew Gideon (Higher priority due to unique characters)
    parts = re.split(r'(<[^>]+>)', text)
    temp_parts = []
    for part in parts:
        if part.startswith('<'):
            temp_parts.append(part)
        else:
            temp_parts.append(GIDEON_HEBREW_RE.sub(
                lambda m: f'<span class="hebrew" lang="he" xml:lang="he" dir="rtl">{convert_gideon_hebrew(m.group(0))}</span>',
                part
            ))
    text = ''.join(temp_parts)

    # Pass 2: Greek Beta Code
    parts = re.split(r'(<[^>]+>)', text)
    temp_parts = []
    for part in parts:
        if part.startswith('<'):
            temp_parts.append(part)
        else:
            temp_parts.append(BETA_CODE_RE.sub(
                lambda m: f'<span class="greek" lang="el" xml:lang="el">{convert_greek_word(m.group(0))}</span>',
                part
            ))
    text = ''.join(temp_parts)
        
    return text


def tag_unicode_ranges(text):
    """Wrap untagged Greek and Hebrew Unicode runs in language-tagged spans.

    Guards:
    - Minimum 3 Greek codepoints before tagging (prevents English false positives
      like single letters from erroneously becoming Greek spans).
    - Applies polytonic_sweep() inside every Greek span to remove any surviving
      legacy Beta Code accent characters (~, >, <, j, J, etc.).
    - Adjacent Greek / Hebrew spans with only whitespace between them are merged
      into a single span to reduce fragmentation.
    """
    if not text:
        return ""

    # 1. Force mapping of any raw Beta Code or Gideon residue, then clean
    text = force_polyglot_mapping(text)
    text = clean_greek_text(text)

    # 2. Tag Greek runs — minimum 3 codepoints to avoid false positives
    def tag_greek(m):
        content = m.group(1)
        # Guard: skip very short runs (1-2 chars) that are likely OCR noise
        greek_chars = re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]', content)
        if len(greek_chars) < 3:
            return content
        # Apply polytonic sweep to remove legacy accent artifacts
        clean = polytonic_sweep(content)
        if not clean.strip():
            return content
        return f'<span lang="el" xml:lang="el">{clean}</span>'

    text = re.sub(r'([\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\u0300-\u036F\u0020]*[\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\u0300-\u036F]*)', tag_greek, text)

    # 3. Tag Hebrew runs (all lengths — Hebrew words are identifiable even at 1-2 chars)
    def tag_hebrew(m):
        content = m.group(1)
        return f'<span lang="he" xml:lang="he" dir="rtl">{content}</span>'

    text = re.sub(r'([\u0590-\u05FF\u0300-\u036F]*[\u0590-\u05FF][\u0590-\u05FF\u0300-\u036F]*)', tag_hebrew, text)

    # 4. Merge adjacent same-language spans separated only by optional whitespace.
    # Pattern: </span>SPACE<span same-lang> → SPACE  (space stays inside merged span)
    # Repeat until stable to handle chains of 3+ adjacent spans.
    _el_join = re.compile(r'</span>(\s*)<span lang="el" xml:lang="el">')
    _he_join = re.compile(r'</span>(\s*)<span lang="he" xml:lang="he" dir="rtl">')
    prev = None
    while prev != text:
        prev = text
        text = _el_join.sub(r'\1', text)
        text = _he_join.sub(r'\1', text)

    return text


def emphasize_structural_prefix(text):
    """Bold visible paragraph/list markers that survive the PDF extraction."""
    if not text or text.startswith('<b>'):
        return text
    return STRUCTURAL_PREFIX_HTML_RE.sub(r'<b>\g<marker></b>\g<space>', text, count=1)


RENDERED_INLINE_STRUCTURAL_RE = re.compile(
    r'(?P<marker><b>(?:'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\[(?:\d+\.?|\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\]|'
    r'\((?:\d+\.?|\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\)|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')</b>\s+)'
)
PLAIN_INLINE_STRUCTURAL_HTML_RE = re.compile(
    r'(?P<marker>(?<![:\d-])(?!\d{4}\.)\d{1,3}\.\s+)'
)

def _split_rendered_inline_structural_html(text_html):
    """Split paragraphs where a rendered bold list marker remains inline."""
    pieces = []
    pos = 0
    matches = sorted(
        list(RENDERED_INLINE_STRUCTURAL_RE.finditer(text_html))
        + list(PLAIN_INLINE_STRUCTURAL_HTML_RE.finditer(text_html)),
        key=lambda item: item.start(),
    )
    for match in matches:
        if match.start() < pos:
            continue
        before_html = text_html[pos:match.start()].strip()
        before_text = re.sub(r'<[^>]+>', ' ', before_html)
        before_text = re.sub(r'\s+', ' ', before_text).strip()
        if not before_text or len(before_text) < 35:
            continue
        if re.search(r'\b(?:verse|verses|chap|chapter|john|romans|corinthians|timothy|peter)\.?\s*$', before_text, re.I):
            continue
        if not re.search(r'[.!?:;—-]\s*$', before_text):
            continue
        pieces.append(before_html)
        pos = match.start()
    if not pieces:
        return [text_html]
    pieces.append(text_html[pos:].strip())
    return [piece for piece in pieces if piece]


def _escape_xml(text):
    if text is None:
        return ""
    return (text.replace('&', '&amp;').replace('<', '&lt;')
                .replace('>', '&gt;').replace('"', '&quot;'))


def _make_xhtml(title, body_html, css_href='style/main.css'):
    safe_title = _escape_xml(title)
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<!DOCTYPE html>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        f'lang="en" xml:lang="en">\n'
        '<head>\n'
        '  <meta charset="utf-8"/>\n'
        f'  <title>{safe_title}</title>\n'
        f'  <link rel="stylesheet" type="text/css" href="{css_href}"/>\n'
        '</head>\n'
        f'<body>{body_html}</body>\n'
        '</html>'
    )


def _split_leading_chapter_subtitle(text):
    """Split bold all-caps chapter subtitles from following prose."""
    match = re.match(r'^((?:\*\*[^*]+\*\*\s*){1,5})(.+)$', text, flags=re.S)
    if not match:
        return None, text

    subtitle_md = match.group(1).strip()
    rest = match.group(2).strip()
    subtitle_plain = re.sub(r'\*\*', '', subtitle_md)
    letters = [c for c in subtitle_plain if c.isalpha()]
    if not letters:
        return None, text
    upper_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
    if upper_ratio < 0.72 or len(subtitle_plain) < 18:
        return None, text
    if not rest:
        return None, text
    return subtitle_md, rest


def _clean_heading_text(text):
    """Remove stray markdown emphasis markers from extracted heading text."""
    text = (text or '').replace('*', '')
    return re.sub(r'\s+', ' ', text).strip()


def _roman_to_int(roman):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    previous = 0
    for char in reversed(roman.rstrip('.').upper()):
        value = values.get(char, 0)
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def _is_roman_list_item(text):
    stripped = text.strip()
    if not stripped or stripped.startswith('#') or ROMAN_ONLY_RE.match(stripped):
        return False
    if len(re.findall(r'\w+', stripped)) > 28:
        return False
    return bool(re.search(r'[.!?:;]"?\s*$', stripped))


def _strip_markdown_heading_marker(text):
    return re.sub(r'^\s*#{1,6}\s+', '', text.strip())


def _coalesce_roman_list_paragraphs(paragraphs):
    """Join outline-like roman list labels with their short item text."""
    out = []
    expected_roman_number = None
    i = 0

    while i < len(paragraphs):
        stripped = paragraphs[i].strip()
        roman_source = _strip_markdown_heading_marker(stripped)
        roman_match = ROMAN_ONLY_RE.match(roman_source)
        if roman_match and i + 1 < len(paragraphs):
            roman_number = _roman_to_int(roman_match.group('roman'))
            previous_text = out[-1].strip() if out else ''
            starts_list = (
                roman_number in (1, 2)
                and (
                    re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                    or re.search(r'(?:[—-]|,)\s*$', previous_text)
                )
            )
            continues_list = expected_roman_number == roman_number

            if (starts_list or continues_list) and _is_roman_list_item(paragraphs[i + 1]):
                out.append(f'{ROMAN_LIST_TOKEN} {roman_match.group("roman")} {paragraphs[i + 1].strip()}')
                expected_roman_number = roman_number + 1
                i += 2
                continue

        if roman_match:
            expected_roman_number = None
        out.append(paragraphs[i])
        i += 1

    return out


def _split_inline_catechism_questions(paragraphs):
    out = []
    pattern = re.compile(r'(?<!^)\s+(?=(?:\*\*)?Q\.\s*\d+\.(?:\*\*)?\s+)')
    for para in paragraphs:
        parts = [part.strip() for part in pattern.split(para) if part.strip()]
        out.extend(parts or [para])
    return out


def _is_catechism_scripture_spill(text):
    clean = re.sub(r'\[f\d+\]', ' ', text)
    if re.match(r'^(?:\*\*)?[QA]\.', clean.strip()):
        return False
    has_ref_code = bool(re.search(r'<\d{6}>', clean))
    has_ref = bool(SCRIPTURE_REF_RE.search(clean))
    if not (has_ref_code or has_ref):
        return False
    clean = re.sub(r'<\d{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(
        rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b|\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+\b',
        ' ',
        clean,
        flags=re.I,
    )
    leftovers = re.sub(r'[;:,.()\-\s]', '', clean)
    return len(leftovers) <= 20


def _answer_head(text):
    clean = FOOTNOTE_MARKER_RE.sub(' ', text)
    clean = re.sub(r'<\d{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    match = re.match(r'^(?:\*\*)?A\.(?:\*\*)?\s+(.{5,120}?[.!?;])', clean, re.I)
    return _norm_for_dedupe(match.group(1)) if match else ''


def _clean_catechism_footnote_spill(paragraphs):
    out = []
    in_catechism = False
    last_answer_head = ''
    for para in paragraphs:
        stripped = para.strip()
        if re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            in_catechism = True
            last_answer_head = ''
        if in_catechism and _is_catechism_scripture_spill(stripped):
            continue
        current_answer_head = _answer_head(stripped)
        if in_catechism and current_answer_head and current_answer_head == last_answer_head:
            continue
        out.append(para)
        if current_answer_head:
            last_answer_head = current_answer_head
        elif re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            last_answer_head = ''
    return out


def _remove_catechism_lookahead_ghosts(paragraphs):
    """Remove answer text that was pulled forward from the following answer."""
    cleaned = list(paragraphs)
    for idx, para in enumerate(cleaned[:-1]):
        if not re.match(r'^(?:\*\*)?A\.', para.strip(), re.I):
            continue
        next_answer = ''
        for following in cleaned[idx + 1:idx + 4]:
            if re.match(r'^(?:\*\*)?A\.', following.strip(), re.I):
                next_answer = following
                break
        if not next_answer:
            continue

        curr_words = [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:]+", para)
        ]
        next_words = [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9:]+", next_answer)]
        if len(curr_words) < 10 or len(next_words) < 8:
            continue

        best = None
        max_size = min(18, len(curr_words), len(next_words))
        for size in range(max_size, 6, -1):
            next_runs = {tuple(next_words[j:j + size]) for j in range(len(next_words) - size + 1)}
            for i in range(1, len(curr_words) - size + 1):
                run = tuple(w for w, _, _ in curr_words[i:i + size])
                if run in next_runs:
                    best = (curr_words[i][1], curr_words[i + size - 1][2])
                    break
            if best:
                break

        if best:
            start, end = best
            while start > 0 and para[start - 1] in ' \t,;:':
                start -= 1
            while end < len(para) and para[end] in ' \t,;:.':
                end += 1
            cleaned[idx] = re.sub(r'\s{2,}', ' ', (para[:start] + ' ' + para[end:]).strip())
    return cleaned


def _remove_duplicate_catechism_answer_opening(text):
    """Collapse ghosted catechism answer openings inside one paragraph."""
    pattern = re.compile(
        r'^(?P<label>(?:\*\*)?A\.(?:\*\*)?\s+)'
        r'(?P<body>.{6,180}?[.!?;])\s+'
        r'(?:\*\*)?A\.(?:\*\*)?\s+(?P=body)',
        re.I,
    )
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(r'\g<label>\g<body>', text)
    return text


def _repair_known_front_matter_text(text):
    """Repair front-matter phrases lost when PDF footnote overlays interrupt text."""
    text = text.replace(
        'To object of Dr. Owen in this treatise',
        'The object of Dr. Owen in this treatise',
    )
    text = text.replace(
        'simple vague and defective',
        'simply vague and defective',
    )
    text = text.replace(
        'these apprehensions of Own.',
        'these apprehensions of Owen.',
    )
    text = text.replace(
        'The Christology of Owens has always been highly valued',
        'The Christology of Owen has always been highly valued',
    )
    text = text.replace(
        'They were among the firsts as the other treatises',
        'They were among the first, as the other treatises',
    )
    text = text.replace(
        'publish all the treatises of ushered under their auspices into public notice',
        'publish all the treatises of Owen in volumes corresponding in size and appearance with the one ushered under their auspices into public notice',
    )
    return text


def _repair_known_source_losses(text):
    """Restore source text lost by font-aware extraction around PDF overlays."""
    text = text.replace(
        'This being the [f8] [f9] declare wherein he placed',
        'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    )
    text = text.replace(
        'This being the [f9] declare wherein he placed',
        'This being the opinion of Nestorius, [f9] revived again in the days wherein we live, I shall declare wherein he placed',
    )
    return text
def markdown_to_html(md_text, current_mode="BODY_TEXT", pending_drop_cap=False,
                     front_matter_style="blurb"):
    """
    Convert paragraph-healed text to clean XHTML.
    Input is paragraphs separated by double newlines.
    Handles headings, bold, italic, and footnote refs.
    Issue 107: Tracks three structural states (FRONT_MATTER, BODY_START, BODY_TEXT).
    Issue 89: front_matter_style controls rendering inside FRONT_MATTER mode:
      "prose" — running editorial text (prefaces, prefatory notes, analyses):
               justified body paragraphs with a proper h2 heading.
      "blurb" — decorative title-page-adjacent content: centered italic paragraphs.
    """
    if not md_text:
        return '', current_mode, pending_drop_cap
    
    html_parts = []
    normalized_paragraphs = [normalize_footnote_markers(para) for para in md_text.split('\n\n')]
    paragraphs = _clean_catechism_footnote_spill(
        _split_inline_catechism_questions(
            _coalesce_roman_list_paragraphs(normalized_paragraphs)
        )
    )
    expanded_paragraphs = []
    for para in paragraphs:
        expanded_paragraphs.extend(_split_inline_structural_markers(para))
    paragraphs = expanded_paragraphs
    paragraphs = _remove_catechism_lookahead_ghosts(paragraphs)
    paragraphs = [_repair_known_catechism_ghosts(para) for para in paragraphs]
    recent_plain = []
    roman_list_expected = None
    pending_chapter_subtitle = False
    seen_footnote_refs = set()
    _fm_prose_started = False  # tracks first paragraph in a prose FM section

    # Mode and drop cap state are passed in to preserve continuity across files
    
    for para in paragraphs:
        stripped = para.strip()
        if not stripped:
            continue

        # State Transitions (Issue 107 Refinement)
        # We strip structural tokens for trigger detection
        clean_upper = re.sub(r'^\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION)\]\]\s*', '', stripped.upper()).strip()
        
        # Rule 1: Reset to FRONT_MATTER upon editorial keywords (Issue 107)
        # Match standalone keywords or those with optional trailing dot
        if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in
               ["PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
                "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"]):
            current_mode = "FRONT_MATTER"
            pending_drop_cap = False
            _fm_prose_started = False  # new section → first paragraph gets .first
        
        # Rule 2: Leave FRONT_MATTER ONLY upon Major Heading (Issue 107)
        # Supports PART 1, BOOK I, specific Owen titles, and any short all-caps
        # standalone line that signals a section beginning (for sermon volumes etc.).
        is_major_trigger = False
        if re.match(r'^(?:PART|BOOK)\s+[0-9IVXLCDM]+\.?$', clean_upper):
            is_major_trigger = True
        elif len(clean_upper) < 60 and any(kw == clean_upper.rstrip('.') for kw in [
            "CHRISTOLOGIA", "MEDITATIONS", "TWO SHORT CATECHISMS",
            "A DISCOURSE", "A TREATISE", "OF COMMUNION", "OF TEMPTATION",
            "THE NATURE", "THE DOCTRINE", "THE MORTIFICATION",
            "SERMON", "SERMONS", "INTRODUCTION",
        ]):
            is_major_trigger = True
        elif (
            # Generic: short all-caps line that is not a known front-matter keyword
            # and not a TOC entry (those contain dots or page numbers)
            len(clean_upper) >= 4 and len(clean_upper) < 55
            and clean_upper == clean_upper.upper()
            and not any(kw in clean_upper for kw in ["PREFACE", "CONTENTS", "ANALYSIS", "PREFATORY", "ADVERTISEMENT"])
            and not re.search(r'\d', clean_upper)
            and not re.search(r'\.{3}|,\s*\d+$', clean_upper)
            and current_mode == "FRONT_MATTER"
            and len(recent_plain) >= 3  # Must be past the first 3 paragraphs
        ):
            is_major_trigger = True
        
        if is_major_trigger:
            current_mode = "BODY_START"
            pending_drop_cap = True
        
        # While in FRONT_MATTER, detect special titles for styling
        if current_mode == "FRONT_MATTER":
            # If it's a standalone title line, style it and continue
            _fm_title_kws = ["PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
                             "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"]
            if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in _fm_title_kws):
                if front_matter_style == "prose":
                    # h2 heading, AGES green, uppercase — proper section heading
                    html_parts.append(
                        f'<h2 class="front-matter-heading">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.rstrip(".").title()))}'
                        f'</h2>'
                    )
                    _fm_prose_started = False  # next paragraph gets .first
                else:
                    html_parts.append(
                        f'<h3 class="front-matter-title">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.title()))}'
                        f'</h3>'
                    )
                pending_drop_cap = False
                continue

        # Detect explicit structural tokens from robust extractor
        token_match = re.match(r'^\[\[(PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION)\]\]\s*(.*)$', stripped, re.S)
        if token_match:
            kind = token_match.group(1)
            content = token_match.group(2).strip()
            
            # Zone A (Front Matter) Immunity: Treat all structural components as
            # simple items until we hit the Body transition.
            if current_mode == "FRONT_MATTER" and not is_major_trigger:
                _escaped = tag_unicode_ranges(_html_escape(content))
                if front_matter_style == "prose":
                    # In prose mode, structural tokens that carry a section title
                    # (PREFACE, PREFATORY NOTE, ORIGINAL PREFACE, TO THE READER,
                    # etc.) become the h2 section heading; other tokens (e.g.
                    # "Christian Reader," salutations) become h3 subheadings.
                    _content_upper = content.upper().strip().rstrip('.')
                    _is_fm_section_title = any(
                        re.match(rf'^(?:THE\s+)?{kw}\.?$', _content_upper)
                        for kw in [
                            "PREFATORY NOTE", "ANALYSIS", "PREFACE",
                            "ORIGINAL PREFACE", "PREFACE TO THE READER",
                            "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT",
                        ]
                    )
                    if _is_fm_section_title:
                        title_text = content.rstrip('.').title()
                        html_parts.append(
                            f'<h2 class="front-matter-heading">'
                            f'{tag_unicode_ranges(_html_escape(title_text))}'
                            f'</h2>'
                        )
                    else:
                        html_parts.append(f'<h3 class="secondary">{_escaped}</h3>')
                    _fm_prose_started = False
                else:
                    # In blurb mode render as a bold centered paragraph
                    html_parts.append(f'<p class="front-matter-body"><b>{_escaped}</b></p>')
                pending_drop_cap = False
                continue

            def _render_heading_content(raw_content: str) -> str:
                """Escape content for use in a heading, converting [fN] markers to noteref links."""
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, raw_content)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            if kind == 'PART':
                html_parts.append(f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">{_render_heading_content(content)}</h1>')
                # Only trigger BODY_START/drop cap if it matches the pattern (Issue 107 Refinement)
                if is_major_trigger:
                    pending_drop_cap = True
                    current_mode = "BODY_START"
            elif kind == 'CHAPTER':
                html_parts.append(f'<h1 class="secondary">{_render_heading_content(content)}</h1>')
                # CHAPTER does not trigger or reset pending_drop_cap (Issue 107)
            elif kind == 'ROMAN_HEAD':
                html_parts.append(f'<h4 class="roman-subheading">{_render_heading_content(content)}</h4>')
                pending_drop_cap = False
            elif kind == 'SUBTITLE':
                html_parts.append(f'<h4 class="chapter-subtitle">{_render_heading_content(content)}</h4>')
            elif kind == 'SUMMARY':
                html_parts.append(f'<p class="chapter-summary">{_render_heading_content(content)}</p>')
                # SUMMARY does not trigger or reset pending_drop_cap (Issue 107)
            elif kind == 'DIGRESSION':
                # Generate unique ID for Digressions
                num_match = re.search(r'\d+', content)
                d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
                html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{_render_heading_content(content.upper().rstrip("."))}</h3>')
                pending_drop_cap = False

            recent_plain.append(_strip_footnote_placeholders(content))
            if len(recent_plain) > 5:
                recent_plain = recent_plain[-5:]
            continue
        
        # Detect heading level from leading #
        h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        
        if h_match:
            level = len(h_match.group(1))
            content = h_match.group(2)
            # Standard markdown Digression handling
            if 'DIGRESSION' in content.upper():
                num_match = re.search(r'\d+', content)
                d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
                html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{tag_unicode_ranges(_html_escape(content.upper().rstrip(".")))}</h3>')
                pending_drop_cap = False
                continue
            h_tag = 'h1' if level <= 2 else ('h2' if level <= 4 else 'h3')
        else:
            content = stripped
            h_tag = None

        # Fix floating letter issue by stripping leading whitespace
        content = content.lstrip()

        frontmatter_inline = None
        if h_tag:
            frontmatter_inline = re.match(
                r'^(?:THE\s+)?(PREFACE|PREFATORY NOTE|ORIGINAL PREFACE)(\.?)\s+(.{40,})$',
                content,
                re.S,
            )
        if frontmatter_inline:
            heading = f'{frontmatter_inline.group(1)}{frontmatter_inline.group(2)}'
            html_parts.append(f'<h3 class="secondary">{heading}</h3>')
            content = frontmatter_inline.group(3).strip()
            h_tag = None
        
        # Process footnote markers [fN]
        roman_list_match = re.match(rf'^{re.escape(ROMAN_LIST_TOKEN)}\s+([IVXLCDM]+\.?)\s+(.+)$', content)
        is_centered_roman_list = False
        if roman_list_match:
            is_centered_roman_list = True
            content = f'**{roman_list_match.group(1)}** {roman_list_match.group(2).strip()}'
            h_tag = None

        def footnote_marker_repl(match):
            fn_num = match.group(1)
            if fn_num in seen_footnote_refs:
                return ''
            seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'

        content_no_refs = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, content).strip()
        content_no_refs = re.sub(r'\s{2,}', ' ', content_no_refs)
        content_no_refs = _remove_duplicate_catechism_answer_opening(content_no_refs)
        content_no_refs = _repair_known_front_matter_text(content_no_refs)
        if recent_plain:
            content_no_refs = _trim_duplicate_reference_prefix(' '.join(recent_plain[-3:]), content_no_refs)
            if not content_no_refs:
                continue

        if h_tag:
            if current_mode == "FRONT_MATTER":
                if front_matter_style == "prose":
                    # In prose mode, let the heading fall through to normal
                    # heading rendering below (h2/h3 as appropriate).
                    pass
                else:
                    # Blurb mode: suppress markdown headings into bold centered
                    # paragraphs to avoid oversized numerals on title-adjacent pages.
                    html_parts.append(
                        f'<p class="front-matter-body">'
                        f'<b>{tag_unicode_ranges(_html_escape(content_no_refs))}</b>'
                        f'</p>'
                    )
                    pending_drop_cap = False
                    continue

            chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
            if chapter_match:
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_rest = (chapter_match.group(2) or '').strip()
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if not chapter_rest:
                    pending_chapter_subtitle = True
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

                subtitle_md, body_after_subtitle = _split_leading_chapter_subtitle(chapter_rest)
                if subtitle_md:
                    subtitle = _clean_heading_text(subtitle_md)
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    content_no_refs = body_after_subtitle.strip()
                    h_tag = None
                    pending_chapter_subtitle = False
                else:
                    letters = [c for c in chapter_rest if c.isalpha()]
                    upper_ratio = (
                        sum(1 for c in letters if c.isupper()) / len(letters)
                        if letters else 0
                    )
                    if upper_ratio >= 0.72 and len(re.findall(r'\w+', chapter_rest)) <= 24:
                        subtitle = _clean_heading_text(chapter_rest)
                        html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                        pending_chapter_subtitle = False
                        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                        if len(recent_plain) > 5:
                            recent_plain = recent_plain[-5:]
                        continue
                    content_no_refs = chapter_rest
                    h_tag = None
                    pending_chapter_subtitle = False

        if h_tag:
            # Generic all-caps heading absorption split:
            # e.g. "THE DOCTRINE...VINDICATED The doctrine of..."
            ac_match = re.match(
                r'^([A-Z][A-Z\s,;:\u2013\u2014\-\(\)\']{18,}?)'
                r'\s+([A-Z][a-z].{40,})$',
                content_no_refs.strip(),
                re.S,
            )
            if ac_match:
                h_text = ac_match.group(1).strip().rstrip('.')
                b_text = ac_match.group(2).strip()
                letters = [c for c in h_text if c.isalpha()]
                upper_ratio = (
                    sum(1 for c in letters if c.isupper()) / len(letters)
                    if letters else 0
                )
                if upper_ratio >= 0.72 and len(re.findall(r'\w+', h_text)) >= 4:
                    cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
                    html_parts.append(f'<{h_tag}{cls}>{h_text}</{h_tag}>')
                    content_no_refs = b_text
                    h_tag = None

        if not h_tag:
            chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
            if chapter_match:
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_subtitle = _clean_heading_text(chapter_match.group(2) or '')
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if chapter_subtitle:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(chapter_subtitle))}</h4>')
                    pending_chapter_subtitle = False
                else:
                    pending_chapter_subtitle = True
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

            # PART/BOOK/SECTION headings → premium title-page style
            part_book_match = re.match(
                r'^(PART|BOOK|SECTION)\s+([IVXLCDM\d]+)(?:\s*[.—–-]\s*(.*))?$',
                content_no_refs.strip(),
                re.I,
            )
            if part_book_match:
                part_label = part_book_match.group(0).strip()
                html_parts.append(
                    f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">'
                    f'{part_label}</h1>'
                )
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

        if pending_chapter_subtitle and not h_tag:
            # Detect italic chapter subtitles (Volume 2 pattern)
            italic_subtitle = re.match(
                r'^_(.+)_\s*$', content_no_refs.strip(), re.S
            )
            if italic_subtitle:
                sub_text = italic_subtitle.group(1).strip()
                sub_text = re.sub(r'\s+', ' ', sub_text)
                if len(sub_text) >= 18 and len(re.findall(r'\w+', sub_text)) <= 40:
                    html_parts.append(
                        f'<h4 class="chapter-subtitle">'
                        f'{tag_unicode_ranges(_html_escape(sub_text))}'
                        f'</h4>'
                    )
                    pending_chapter_subtitle = False
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            plain_letters = [c for c in content_no_refs if c.isalpha()]
            upper_ratio = (
                sum(1 for c in plain_letters if c.isupper()) / len(plain_letters)
                if plain_letters else 0
            )
            if len(content_no_refs) >= 18 and upper_ratio >= 0.72:
                subtitle = _clean_heading_text(content_no_refs)
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                pending_chapter_subtitle = False
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            pending_chapter_subtitle = False

        if not h_tag:
            standalone_bold = re.fullmatch(r'\*\*(.+?)\*\*', content_no_refs.strip(), re.S)
            if standalone_bold:
                bold_plain = standalone_bold.group(1).strip()
                letters = [c for c in bold_plain if c.isalpha()]
                upper_ratio = (
                    sum(1 for c in letters if c.isupper()) / len(letters)
                    if letters else 0
                )
                if len(bold_plain) >= 12 and upper_ratio >= 0.72:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(_clean_heading_text(bold_plain)))}</h4>')
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

        subtitle_md = None
        if not h_tag:
            subtitle_md, content_no_refs = _split_leading_chapter_subtitle(content_no_refs)

        roman_heading = None
        if not h_tag and not subtitle_md:
            roman_match = ROMAN_HEADING_RE.match(content_no_refs)
            if roman_match:
                roman_number = _roman_to_int(roman_match.group('roman'))
                rest_after_roman = roman_match.group('rest').strip()
                previous_text = recent_plain[-1] if recent_plain else ''
                starts_roman_list = (
                    roman_number in (1, 2)
                    and (
                        re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                        or re.search(r'(?:[—-]|,)\s*$', previous_text)
                    )
                )
                continues_roman_list = roman_list_expected == roman_number
                if (starts_roman_list or continues_roman_list) and _is_roman_list_item(rest_after_roman):
                    content_no_refs = f'**{roman_match.group("roman")}** {rest_after_roman}'
                    is_centered_roman_list = True
                    roman_list_expected = roman_number + 1
                else:
                    roman_heading = roman_match.group('roman')
                    content_no_refs = rest_after_roman
                    roman_list_expected = None
            else:
                roman_list_expected = None
        
        # Convert **bold** → <b>, _italic_ → <i>
        text_html = content_no_refs
        text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', r'**\1**', text_html)
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)
        text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(
            r'^(<b>A\.</b>\s+)([^<]{6,180}?[.!?;])\s+<b>A\.</b>\s+\2',
            r'\1\2',
            text_html,
            flags=re.I,
        )
        text_html = emphasize_structural_prefix(text_html)
        text_html = re.sub(r'(\b(?:verse|verses|chap|chapter)\.?\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html, flags=re.I)
        text_html = re.sub(r'(\b\d+:\d+(?:[-,]\s*\d+)*,\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html)
        text_html = re.sub(r'<b>(\d+(?:st|nd|rd|th))</b>(\s+(?:Psalm|Psalms)\b)', r'\1\2', text_html)
        
        # Tag Unicode Greek/Hebrew ranges
        text_html = tag_unicode_ranges(text_html)
        text_html = _restore_footnote_placeholders(text_html)

        plain_for_class = re.sub(r'<[^>]+>', '', text_html)
        plain_for_class = re.sub(r'\s+', ' ', plain_for_class).strip()
        
        if h_tag:
            cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
            html_parts.append(f'<{h_tag}{cls}>{text_html}</{h_tag}>')
        elif text_html.startswith('---') or text_html.startswith('***'):
            html_parts.append('<hr/>')
        elif is_centered_roman_list:
            html_parts.append(f'<p class="roman-list-item">{text_html}</p>')
        else:
            if subtitle_md:
                subtitle_html = _clean_heading_text(subtitle_md)
                subtitle_html = tag_unicode_ranges(subtitle_html)
                roman_match = re.match(r'^(?P<title>.+?)\s+(?P<roman>[IVXLCDM]+\.?)$', subtitle_html)
                if roman_match and len(roman_match.group('title')) >= 18:
                    html_parts.append(f'<h4 class="chapter-subtitle">{roman_match.group("title")}</h4>')
                    html_parts.append(f'<h4 class="chapter-subtitle roman-subheading">{roman_match.group("roman")}</h4>')
                else:
                    html_parts.append(f'<h4 class="chapter-subtitle">{subtitle_html}</h4>')
            if roman_heading:
                html_parts.append(f'<h4 class="roman-subheading">{roman_heading}</h4>')
            if plain_for_class in {
                'Glory be to God on high!',
                'To Him be all glory and honor for evermore! Amen.',
            }:
                html_parts.append(f'<p class="doxology">{text_html}</p>')
            else:
                for paragraph_html in _split_rendered_inline_structural_html(text_html):
                    # Strip leading whitespace/hidden chars to fix the "floating letter" issue
                    paragraph_html = paragraph_html.lstrip()
                    if not paragraph_html:
                        continue
                    
                    # Signature detection: "= John Owen" or "— John Owen" etc.
                    _sig_plain = re.sub(r'<[^>]+>', '', paragraph_html).strip()
                    _is_signature = bool(re.match(
                        r'^[=—–-]\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3}\.?\s*$',
                        _sig_plain,
                    ))

                    # Rule 1: FRONT_MATTER rules
                    if current_mode == "FRONT_MATTER":
                        if _is_signature:
                            html_parts.append(f'<p class="signature">{paragraph_html}</p>')
                        elif front_matter_style == "prose":
                            # Running editorial prose: justify like normal body text.
                            if not _fm_prose_started:
                                p_cls = "front-matter-prose first"
                                _fm_prose_started = True
                            else:
                                p_cls = "front-matter-prose"
                            html_parts.append(f'<p class="{p_cls}">{paragraph_html}</p>')
                        else:
                            # Blurb: centered italic for decorative title-page content.
                            html_parts.append(f'<p class="front-matter-body">{paragraph_html}</p>')
                        pending_drop_cap = False
                    else:
                        # User-mandated Drop Cap Constraint (States 2 and 3)
                        p_class = ""
                        if pending_drop_cap and current_mode == "BODY_START":
                            # Exclude sub-points from drop caps (e.g. '(2.)', '1.', 'I.', 'Ans.')
                            # User: Never turn a character into a drop cap if it is a parenthesis ( or a number 1.
                            is_subpoint = re.match(
                                r'^(?:<b>)?(?:\([0-9IVXLCDM]+\.?\)|[0-9]+\.|[IVXLCDM]+\.|Ans\.|Sol\.|Obj\.|Objection|Answer|Solution|Use\s+\d+)', 
                                paragraph_html, re.I
                            )
                            # Also ensure the paragraph starts with a letter if we are to drop-cap it
                            starts_with_letter = re.match(r'^(?:<b>)?[A-Z]', paragraph_html, re.I)
                            
                            if not is_subpoint and starts_with_letter:
                                p_class = ' class="chapter-opening"'
                                pending_drop_cap = False
                                current_mode = "BODY_TEXT" # Transition to State 3
                            # If is_subpoint or doesn't start with letter, we stay in BODY_START/pending_drop_cap=True
                        
                        if _is_signature:
                            html_parts.append(f'<p class="signature">{paragraph_html}</p>')
                        else:
                            html_parts.append(f'<p{p_class}>{paragraph_html}</p>')


        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
        if len(recent_plain) > 5:
            recent_plain = recent_plain[-5:]
    
    return '\n'.join(html_parts), current_mode, pending_drop_cap
def find_cover(vol_num):
    """Find cover image for a volume."""
    covers_dir = os.path.join(_RENDER_DIR, 'covers')
    for ext in ('.jpeg', '.jpg', '.png'):
        path = os.path.join(covers_dir, f'v{vol_num}{ext}')
        if os.path.exists(path):
            return path
    return None


def find_portrait(vol_num=None):
    """Find a portrait image."""
    p_dir = os.path.join(_RENDER_DIR, 'portraits')
    if not os.path.isdir(p_dir):
        return None
    files = sorted([f for f in os.listdir(p_dir) if f.lower().endswith(('.jpeg', '.jpg', '.png'))])
    if not files:
        return None
    idx = int(hashlib.md5(f'owen-v{vol_num}'.encode()).hexdigest(), 16) % len(files)
    return os.path.join(p_dir, files[idx])


def _build_title_page(vol_num, title, subtitle):
    return f'''<div class="title-page">
<p class="ornament">❧</p>
<h1 class="primary">The Works of<br/>John Owen</h1>
<hr class="rule"/>
<h2 class="secondary">Volume {vol_num}</h2>
<h2 class="secondary">{_escape_xml(subtitle)}</h2>
<p class="author"><span class="by">by</span>John Owen</p>
<p class="editor">Edited by William H. Goold</p>
<p class="publisher">Eduardus Ekofius</p>
</div>'''


def generate_frontispiece_xhtml(portrait_filename):
    return f'<div class="frontispiece"><img src="images/{portrait_filename}" alt="Portrait of John Owen"/><p class="caption">John Owen (1616&#x2013;1683)</p></div>'


def generate_nav_xhtml(toc_entries, volume_title=None, has_cover=False, has_frontispiece=False, first_content_href=None):
    """Generate 3-level NAV XHTML with EPUB3 landmarks."""
    display_title = _html_escape(volume_title or 'Table of Contents')
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<!DOCTYPE html>',
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">',
        '<head>',
        f'  <title>{display_title}</title>',
        '  <link href="style/main.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        f'<nav epub:type="toc" id="toc" role="doc-toc">',
        f'<h2>{display_title}</h2>',
    ]
    
    current_level = 0
    stack = []
    for level, text, href in toc_entries:
        level = max(1, min(level, 3))
        if level > current_level + 1:
            level = current_level + 1
        if level > current_level:
            for _ in range(level - current_level):
                lines.append('<ol>')
                stack.append('ol')
        elif level < current_level:
            lines.append('</li>')
            stack.pop()
            for _ in range(current_level - level):
                lines.extend(['</ol>', '</li>'])
                stack.pop()
                stack.pop()
        elif current_level > 0:
            lines.append('</li>')
            stack.pop()
        
        lines.append(f'<li><a href="{_html_escape(href)}">{_html_escape(text)}</a>')
        stack.append('li')
        current_level = level
    
    while stack:
        lines.append(f'</{stack.pop()}>')
    
    lines.append('</nav>')
    
    # Landmarks
    lines.append('<nav epub:type="landmarks">\n<h2>Guide</h2>\n<ol>')
    if has_cover:
        lines.append('  <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    lines.append('  <li><a epub:type="titlepage" href="title.xhtml">Title Page</a></li>')
    lines.append('  <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')
    if has_frontispiece:
        lines.append('  <li><a epub:type="frontispiece" href="frontispiece.xhtml">Frontispiece</a></li>')
    if first_content_href:
        lines.append(f'  <li><a epub:type="bodymatter" href="{first_content_href}">Start of Content</a></li>')
    lines.extend(['</ol>', '</nav>', '</body>', '</html>'])
    
    return '\n'.join(lines)


def generate_ncx(title, uid, toc_entries):
    """Generate NCX for backward compatibility."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">',
        f'  <head><meta content="{_html_escape(uid)}" name="dtb:uid"/></head>',
        f'  <docTitle><text>{_html_escape(title)}</text></docTitle>',
        '  <navMap>',
    ]
    for i, (level, text, href) in enumerate(toc_entries):
        lines.append(
            f'    <navPoint id="nav_{i}" playOrder="{i+1}">'
            f'<navLabel><text>{_html_escape(text)}</text></navLabel>'
            f'<content src="{_html_escape(href)}"/>'
            f'</navPoint>'
        )
    lines.extend(['  </navMap>', '</ncx>'])
    return '\n'.join(lines)


def repackage_canonical(epub_path, src_dir):
    """Repackage as canonical EPUB3 (mimetype first, no compression)."""
    if os.path.exists(epub_path):
        os.remove(epub_path)
    with open(os.path.join(src_dir, 'mimetype'), 'wb') as f:
        f.write(b'application/epub+zip')
    subprocess.run(['zip', '-0Xq', epub_path, 'mimetype'],
                   cwd=src_dir, check=True)
    subprocess.run(['zip', '-r9q', epub_path, '.', '-x',
                    'mimetype', '-x', '*.DS_Store'],
                   cwd=src_dir, check=True)


def _inject_apple_books_options(epub_path):
    """Post-process EPUB to add the Apple Books display-options file in META-INF."""
    tmp = epub_path + '.tmp'
    apple_opts_path = 'META-INF/com.apple.ibooks.display-options.xml'
    
    apple_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<display-options xmlns="http://www.apple.com/itunes/vbook/display-options">
  <platform name="*">
    <option name="specified-fonts">true</option>
  </platform>
</display-options>
"""
    
    with zipfile.ZipFile(epub_path, 'r') as zin:
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
            # Copy all existing items
            for item in zin.infolist():
                if item.filename == apple_opts_path:
                    continue # Will overwrite
                zout.writestr(item, zin.read(item.filename))
            
            # Add Apple options file
            zout.writestr(apple_opts_path, apple_xml)
            
    shutil.move(tmp, epub_path)


# ================================================================
# MAIN PIPELINE
# ================================================================

def build_endnotes_chapter(footnotes, style_item=None):
    fn_map = {f.fnum: f for f in footnotes.values()}
    parts = ['<section epub:type="footnotes" role="doc-endnotes" hidden="hidden">']
    for fnum in sorted(fn_map.keys()):
        fn = fn_map[fnum]
        fn_text = tag_unicode_ranges(_html_escape(fn.text))
        parts.append(
            f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="fn{fnum}">'
            f'<p class="footnote">'
            f'<span class="fn-link">{fnum}</span> '
            f'{fn_text}'
            f'</p></aside>'
        )
    parts.append('</section>')
    html = ''.join(parts)
    return _make_xhtml('Footnotes', html)


# ================================================================
# FRONT MATTER HANDLING
# ================================================================

_AGES_HEADERS = {'THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION',
                 'Books For The Ages', 'AGES Software', 'Version 1.0',
                 'B o o k s F o r T h e A g e s'}


def detect_page_type(page, page_num=None):
    """Detect if a page is TOC, Title, or Body text based on visual structure."""
    text_upper = page.get_text().upper()
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if b.get('type') == 0]
    n_blocks = len(text_blocks)

    # TOC detection: any CONTENTS page OR pages with many numbered/chapter items
    if 'CONTENTS' in text_upper and n_blocks > 5:
        return 'toc_page'
    
    # Heuristic for multi-page TOC (pages with high count of "CHAPTER X" or numbered items)
    if n_blocks > 10:
        items_count = 0
        for b in text_blocks:
            b_text = "".join(s['text'] for line in b['lines'] for s in line['spans']).strip()
            # Match "CHAPTER 1", "1. ", "I. ", etc.
            if re.match(r'^(CHAPTER\s+\d+|[IVXLC]+\.|\d+[\.\-])', b_text, re.I):
                items_count += 1
        if items_count > 8:
            return 'toc_page'

    # Universal structural page detection (Stop using page numbers - Issue 107)
    total_chars = 0
    large_chars = 0
    max_font = 0
    for b in text_blocks:
        for line in b['lines']:
            for s in line['spans']:
                c = len(s['text'])
                total_chars += c
                max_font = max(max_font, s['size'])
                if s['size'] > 14:
                    large_chars += c
                    
    # Strict structural criteria (sparse blocks + large font)
    if max_font > 14 and total_chars < 800 and n_blocks < 15:
        return 'title_page'

    # Beyond very sparse: char-count based title page detection (mid-volume)
    if total_chars < 1200 and large_chars >= 40:
        return 'title_page'

    # Fallback for mixed title+body pages (e.g. Part titles starting mid-page)
    if total_chars < 2000:
        for b in text_blocks:
            b_text = "".join(s['text'] for line in b['lines'] for s in line['spans']).strip()
            # Skip page numbers and running headers
            if b_text.isdigit() and len(b_text) <= 4: continue
            if any(h in b_text for h in _AGES_HEADERS): continue
            
            # Check font size in this block
            b_max = 0
            for line in b['lines']:
                for s in line['spans']:
                    b_max = max(b_max, s['size'])
                    
            # Only trigger if we find a very large-font line (e.g. PART X, BOOK X)
            if b_max > 18 and len(b_text) < 40 and not b_text.upper().startswith('CHAPTER'):
                return 'title_page'
            # If we hit a normal block first, it's a body page
            break

    return 'body_page'


def is_toc_continuation_page(page, page_num=None):
    """Detect sparse continuation pages after a visual CONTENTS page."""
    if page_num is not None and page_num > 8:
        return False
    text = page.get_text()
    clean = re.sub(r'\s+', ' ', text).strip()
    if not clean:
        return False
    upper = clean.upper()
    if re.match(r'^\d*\s*(?:GENERAL PREFACE|PREFACE|PREFATORY NOTE|TO THE READER)\b', upper):
        return False
    chapter_hits = len(re.findall(r'\bCHAPTER\s+\d+', upper))
    part_hits = len(re.findall(r'\bPART\s+\d+', upper))
    numbered_hits = len(re.findall(r'(?:^|\s)(?:[IVXLCDM]+\.|\d+\.)\s+[—A-Z]', clean, re.I))
    return (chapter_hits + part_hits + numbered_hits) >= 1


def format_title_page(page, section_class="title-page", epub_type="titlepage", limit_to_title=False):
    """Build Goold-style centered title page XHTML from PDF blocks with premium styling.

    Preserves PDF line breaks with <br/>, maps font-size hierarchy to h1/h2/h3.
    Applies colors and italics based on content heuristics.
    """
    blocks = page.get_text('dict')['blocks']
    lines_data = []
    for b in blocks:
        if b.get('type') != 0:
            continue
        for line in b['lines']:
            spans = line['spans']
            max_size = max(s['size'] for s in spans)
            font_names = [s['font'] for s in spans]
            text = ''.join(s['text'] for s in spans).strip()
            text = re.sub(r'<\d{6}>', '', text).strip()
            if not text or text.isdigit():
                continue
            if any(h in text for h in _AGES_HEADERS):
                continue
            
            # Stop if we hit a chapter marker and limit_to_title is active
            if limit_to_title and text.upper().startswith('CHAPTER'):
                break
                
            has_koine = any('Koine' in f for f in font_names)
            has_italic = any('Italic' in f for f in font_names)
            has_bold = any('Bold' in f for f in font_names)
            lines_data.append((max_size, has_koine, has_italic, has_bold, text))
        else:
            continue
        break 

    if not lines_data:
        return ''

    # Absolute font thresholds
    h1_threshold = 20.0
    h2_threshold = 15.0

    groups = []
    for size, has_koine, has_italic, has_bold, text in lines_data:
        if has_koine:
            text = convert_greek_word(text)
        safe = _html_escape(text)
        if has_koine:
            safe = f'<span lang="el" xml:lang="el">{safe}</span>'

        # Class heuristics
        cls = ""
        if size >= h1_threshold or (size >= h2_threshold and len(text) < 20):
            lvl = 'h1'
            cls = ' class="primary"'
        elif size >= h2_threshold:
            lvl = 'h2'
            cls = ' class="secondary"'
        elif text.upper() in {'OR', 'OF', 'WITH', 'AS ALSO,'}:
            lvl = 'h3'
            cls = ' class="separator"'
        elif len(text) > 40 or has_italic:
            lvl = 'p'
            cls = ' class="descriptive"'
        elif has_bold:
            lvl = 'h3'
        else:
            lvl = 'p'

        if groups and groups[-1][0] == lvl and groups[-1][1] == cls:
            groups[-1][2].append(safe)
        else:
            groups.append((lvl, cls, [safe]))

    parts = [f'<section class="{section_class}" epub:type="{epub_type}">']
    # Add ornament at top
    parts.append('<p class="ornament">❧</p>')
    
    for lvl, cls, texts in groups:
        content = '<br/>'.join(texts)
        parts.append(f'<{lvl}{cls}>{content}</{lvl}>')
    parts.append('</section>')
    return '\n'.join(parts)


def restore_dropped_title_noteref(title_html, chap, vol_num):
    """Restore title-page noterefs that PyMuPDF omits from sparse title pages."""
    if (
        vol_num == 1
        and chap.cid == 'ch025'
        and 'endnotes.xhtml#fn18' not in title_html
        and 'THE GLORY OF CHRIST' in title_html
    ):
        title_html = re.sub(
            r'(THE GLORY OF CHRIST,)',
            lambda m: m.group(1) + _noteref_link(18),
            title_html,
            count=1,
        )
    return title_html


def build_toc_page_xhtml(pages):
    """Build a formatted CONTENTS page from one or more PDF pages.
    
    Uses block metadata to identify headings vs items and apply styling.
    """
    if not isinstance(pages, list):
        pages = [pages]
        
    parts = ['<section epub:type="toc">']
    
    for page in pages:
        blocks = page.get_text('dict')['blocks']
        text_blocks = [b for b in blocks if b.get('type') == 0]
        
        for b in text_blocks:
            lines_data = []
            max_size = 0
            has_bold = False
            has_color = False
            
            for line in b['lines']:
                spans = line['spans']
                l_size = max(s['size'] for s in spans)
                max_size = max(max_size, l_size)
                if any(s['flags'] & 2 for s in spans): # 2 is bold
                    has_bold = True
                
                # Check for colors (non-black)
                for s in spans:
                    if s['color'] != 0:
                        has_color = True
                
                l_text = "".join(s['text'] for s in spans).strip()
                l_text = re.sub(r'<\d{6}>', '', l_text).strip()
                # Skip standalone page numbers
                if l_text.isdigit() and len(l_text) <= 4:
                    continue
                if l_text:
                    lines_data.append(l_text)
            
            if not lines_data:
                continue
                
            full_text = " ".join(lines_data)
            safe_text = "<br/>".join(_html_escape(l) for l in lines_data)
            
            # Heuristics based on John Owen Volume 1 layout
            # 1. Main Titles (Large, usually bold/colored)
            if max_size > 13 or (full_text.isupper() and len(full_text) < 60 and not "CHAPTER" in full_text.upper()):
                parts.append(f'<h2 style="text-align: center;">{safe_text}</h2>')
            # 2. Section Headers (PREFATORY NOTE, PREFACE, etc.)
            elif full_text.isupper() and len(full_text) < 40:
                parts.append(f'<h3 style="text-align: center;">{safe_text}</h3>')
            # 3. TOC Items (CHAPTER 1, 1. -, etc.)
            else:
                # Use .ContentsItem for hanging indent
                # We want to bold the label part if possible
                # Refined regex for labels like "1. —" or "CHAPTER 1."
                match = re.match(r'^((?:CHAPTER\s+\d+|[IVXLC]+\.|[0-9]+[\.\-\s]*[—\-]?)\s*)(.*)', full_text, re.I | re.S)
                if match:
                    label, desc = match.groups()
                    desc_safe = _html_escape(desc.strip())
                    parts.append(f'<p class="ContentsItem"><b>{_html_escape(label)}</b> {desc_safe}</p>')
                else:
                    continuation = _html_escape(re.sub(r'\s+', ' ', full_text).strip())
                    if (
                        parts
                        and 'class="ContentsItem"' in parts[-1]
                        and re.search(r'[;—-]\s*</p>$', parts[-1])
                    ):
                        parts[-1] = parts[-1].replace('</p>', f' {continuation}</p>')
                    else:
                        parts.append(f'<p class="ContentsItem">{safe_text}</p>')
                    
    parts.append('</section>')
    return '\n'.join(parts)


# ================================================================
# STAGE 2 ENTRY POINT — render_volume()
# ================================================================

def render_volume(vol_num: int, overrides: dict = None,
                  intermediate: dict = None) -> str:
    """Run Stage 2 for a single Owen volume: JSON intermediate → EPUB3.

    Reads volumes/vN/intermediate/volume_N.json (or uses supplied dict),
    assembles the EPUB3, and writes volumes/vN/output/volume_N.epub.
    Returns the path to the written EPUB.

    overrides: optional per-volume config additions (see volumes/vN/convert.py).
    intermediate: if supplied, use this dict instead of reading from disk.
    """
    # Import here to avoid circular import at module level
    from shared import (
        VOLUME_CONFIG, VOLUME_SUBTITLES,
        EPUB_STYLESHEET, generate_font_styles, select_primary_font,
        SBL_SUPPLEMENTS, EZRA_SIL_FILES,
    )
    try:
        from ebooklib import epub
    except ImportError:
        import sys; sys.exit("Error: ebooklib not installed.")

    overrides = overrides or {}
    config = {**VOLUME_CONFIG.get(vol_num, {}), **overrides}

    vol_dir = _RENDER_DIR / 'volumes' / f'v{vol_num}'
    json_path = vol_dir / 'intermediate' / f'volume_{vol_num}.json'
    out_dir = vol_dir / 'output'
    out_dir.mkdir(parents=True, exist_ok=True)
    epub_path = str(out_dir / f'volume_{vol_num}.epub')

    if intermediate is None:
        with open(json_path, encoding='utf-8') as f:
            intermediate = json.load(f)

    print(f'[render] Volume {vol_num}: {len(intermediate["chapters"])} chapters, '
          f'{len(intermediate["footnotes"])} footnotes')

    # Reconstruct Footnote-like objects from JSON
    from dataclasses import dataclass as _dc, field as _field

    @_dc
    class _Fn:
        fnum: int
        text: str
        source: str = 'pdf'
        pages: list = _field(default_factory=list)

    footnote_map = {
        int(k): _Fn(fnum=int(k), text=v['text'], source=v['source'])
        for k, v in intermediate['footnotes'].items()
    }

    # ── EPUB book setup ──────────────────────────────────────────
    book = epub.EpubBook()
    uid = str(uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-works-vol-{vol_num}'))
    book.set_identifier(uid)
    book.set_title(intermediate['title'])
    book.set_language('en')
    book.add_author(config.get('authors', ['John Owen'])[0])
    for ed in config.get('editors', []):
        book.add_metadata('DC', 'contributor', ed,
                          {'role': 'edt', 'id': 'editor'})
    book.add_metadata('DC', 'publisher', config.get('publisher', ''))
    book.add_metadata('DC', 'rights', 'Public Domain')

    # ── CSS and fonts ────────────────────────────────────────────
    body_font_name = config.get('body_font', 'SBL_BLit')
    primary_font = select_primary_font(body_font_name)
    font_css = generate_font_styles(primary_font['name'], primary_font['files'])
    full_css = EPUB_STYLESHEET + '\n' + font_css
    style_item = epub.EpubItem(
        uid='style', file_name='style/main.css',
        media_type='text/css', content=full_css.encode('utf-8'),
    )
    book.add_item(style_item)

    font_fnames = set()
    font_base = os.path.join(_RENDER_DIR, 'fonts')

    # Primary font files (from select_primary_font dict)
    for _variant, _rel_path in primary_font.get('files', {}).items():
        _fbase = os.path.basename(_rel_path)
        if _fbase in font_fnames:
            continue
        _src = os.path.join(font_base, _rel_path)
        if os.path.exists(_src):
            _ext = os.path.splitext(_fbase)[1].lower()
            _mt = ('font/otf' if _ext == '.otf' else
                   'font/ttf' if _ext == '.ttf' else 'application/font-sfnt')
            book.add_item(epub.EpubItem(
                uid=f'f_{_fbase.replace(".","_")}',
                file_name=f'Fonts/{_fbase}', media_type=_mt,
                content=open(_src, 'rb').read(),
            ))
            font_fnames.add(_fbase)

    # SBL supplement fonts and Ezra SIL
    for _font_dict in (SBL_SUPPLEMENTS, EZRA_SIL_FILES):
        for _fname, _fpath in _font_dict.items():
            _fbase = os.path.basename(_fpath)
            if _fbase in font_fnames:
                continue
            _src = os.path.join(font_base, _fpath)
            if os.path.exists(_src):
                book.add_item(epub.EpubItem(
                    uid=f'f_{_fbase.replace(".","_")}',
                    file_name=f'Fonts/{_fbase}',
                    media_type='application/font-sfnt',
                    content=open(_src, 'rb').read(),
                ))
                font_fnames.add(_fbase)

    # ── Cover ────────────────────────────────────────────────────
    cover_path = find_cover(vol_num)
    cover_item = None
    if cover_path and os.path.exists(cover_path):
        ext = os.path.splitext(cover_path)[1].lower()
        mt = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
        with open(cover_path, 'rb') as f:
            cover_item = epub.EpubItem(
                file_name=f'images/cover{ext}', media_type=mt, content=f.read(),
            )
        book.add_item(cover_item)
        # Don't call set_cover — it duplicates the item already added above

    # ── Frontispiece ─────────────────────────────────────────────
    portrait_path = find_portrait(vol_num)
    frontispiece_item = None
    if portrait_path and os.path.exists(portrait_path):
        ext = os.path.splitext(portrait_path)[1].lower()
        mt = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
        port_fn = f'images/portrait{ext}'
        with open(portrait_path, 'rb') as f:
            port_item = epub.EpubItem(file_name=port_fn, media_type=mt, content=f.read())
        book.add_item(port_item)
        fi_html = generate_frontispiece_xhtml(os.path.basename(portrait_path))
        frontispiece_item = epub.EpubHtml(
            title='Frontispiece', file_name='frontispiece.xhtml', lang='en',
        )
        frontispiece_item.set_content(
            _make_xhtml('Frontispiece', fi_html).encode('utf-8')
        )
        frontispiece_item.add_item(style_item)
        book.add_item(frontispiece_item)

    # ── Template title page ──────────────────────────────────────
    subtitle_val = VOLUME_SUBTITLES.get(vol_num, '')
    tp_item = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
    tp_item.set_content(
        _make_xhtml('Title Page',
                    _build_title_page(vol_num, intermediate['title'], subtitle_val)
                    ).encode('utf-8')
    )
    tp_item.add_item(style_item)
    book.add_item(tp_item)

    # ── PDF-extracted front matter (title pages, TOC) ────────────
    front_matter_epub_items = []
    for fm in intermediate.get('front_matter_items', []):
        fm_item = epub.EpubHtml(
            title=fm['title'], file_name=fm['file_name'], lang='en',
        )
        fm_item.set_content(
            _make_xhtml(fm['title'], fm['html']).encode('utf-8')
        )
        fm_item.add_item(style_item)
        book.add_item(fm_item)
        front_matter_epub_items.append(fm_item)

    # ── Chapters ─────────────────────────────────────────────────
    toc_entries = []
    epub_chapters = []
    guide_landmarks = [('Title Page', 'title.xhtml')]

    conv_mode = 'FRONT_MATTER'
    conv_drop_cap = False
    conv_fm_style = 'blurb'

    _FM_PROSE_KEYWORDS = [
        'PREFACE', 'PREFATORY NOTE', 'PREFATORY', 'ANALYSIS',
        'TO THE READER', 'ADVERTISEMENT', 'GENERAL PREFACE',
    ]

    for ch_dict in intermediate['chapters']:
        if ch_dict.get('is_endnotes'):
            continue

        title_upper = ch_dict['title'].upper()
        fm_style = ch_dict.get('front_matter_style')

        if any(kw in title_upper for kw in ['ANALYSIS', 'PREFATORY NOTE', 'PREFACE', 'CONTENTS']):
            conv_mode = 'FRONT_MATTER'
            conv_drop_cap = False
            conv_fm_style = 'prose'
        elif ch_dict.get('is_treatise') and re.search(
            r'\b(?:PART|BOOK)\s+[0-9IVXLCDM]+\b|\b(?:CHRISTOLOGIA|MEDITATIONS|TWO SHORT CATECHISMS)\b',
            title_upper,
        ):
            conv_mode = 'BODY_START'
            conv_drop_cap = True
            conv_fm_style = 'blurb'
        elif re.search(r'\bCHAPTER\s+\d+\b|\bSERMON\s+\d+\b|\bDISCOURSE\s+\d+\b', title_upper):
            if conv_mode == 'FRONT_MATTER':
                conv_mode = 'BODY_START'
                conv_drop_cap = True
            conv_fm_style = 'blurb'

        raw_text = ch_dict.get('raw_text', '')
        if not raw_text:
            continue

        body_html, conv_mode, conv_drop_cap = markdown_to_html(
            raw_text,
            current_mode=conv_mode,
            pending_drop_cap=conv_drop_cap,
            front_matter_style=conv_fm_style,
        )
        body_html = apply_scholastic_anchor_protocol(body_html)
        if not body_html.strip():
            continue

        body = f'<section>{body_html}</section>'
        cid = ch_dict['cid']
        ch_item = epub.EpubHtml(
            title=ch_dict['title'], file_name=f'{cid}.xhtml', lang='en',
        )
        ch_item.set_content(_make_xhtml(ch_dict['title'], body).encode('utf-8'))
        ch_item.add_item(style_item)
        book.add_item(ch_item)
        epub_chapters.append(ch_item)

        toc_entries.append((
            ch_dict['level'], ch_dict['title'], f'{cid}.xhtml',
        ))

    # ── Endnotes ─────────────────────────────────────────────────
    endnotes_item = None
    if footnote_map:
        endnotes_html = build_endnotes_chapter(footnote_map, style_item)
        endnotes_item = epub.EpubHtml(
            title='Footnotes', file_name='endnotes.xhtml', lang='en',
        )
        endnotes_item.set_content(endnotes_html.encode('utf-8'))
        endnotes_item.add_item(style_item)
        book.add_item(endnotes_item)

    # ── NAV, NCX, spine ──────────────────────────────────────────
    nav_entries = toc_entries  # already (level, title, href)
    nav_html = generate_nav_xhtml(
        nav_entries,
        volume_title=intermediate['title'],
        has_cover=cover_item is not None,
        has_frontispiece=frontispiece_item is not None,
        first_content_href=epub_chapters[0].file_name if epub_chapters else None,
    )
    nav_item = epub.EpubHtml(
        title='Table of Contents', file_name='nav.xhtml',
        media_type='application/xhtml+xml', lang='en',
    )
    nav_item.set_content(_make_xhtml('Table of Contents', nav_html).encode('utf-8'))
    nav_item.add_item(style_item)
    book.add_item(nav_item)
    book.toc = tuple(
        epub.Link(href, title, '') for _, title, href in nav_entries
    )

    ncx_uid = uid
    ncx = epub.EpubNcx()
    book.add_item(ncx)

    spine = ['nav', tp_item] + front_matter_epub_items
    if frontispiece_item:
        spine.append(frontispiece_item)
    spine += epub_chapters
    if endnotes_item:
        spine.append(endnotes_item)
    book.spine = spine

    # ── Write and repackage ──────────────────────────────────────
    import tempfile as _tempfile
    # ebooklib writes a valid EPUB but not in canonical form (mimetype must be
    # first and uncompressed). Write to a temp path, extract, repackage.
    temp_epub = epub_path + '.tmp_build'
    epub.write_epub(temp_epub, book)
    with _tempfile.TemporaryDirectory() as tmp:
        import zipfile as _zf
        with _zf.ZipFile(temp_epub, 'r') as z:
            z.extractall(tmp)
        repackage_canonical(epub_path, tmp)
    if os.path.exists(temp_epub):
        os.remove(temp_epub)
    _inject_apple_books_options(epub_path)
    print(f'[render] ✓ EPUB saved: {epub_path}')
    return epub_path


if __name__ == '__main__':
    import sys
    vol = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    render_volume(vol)
