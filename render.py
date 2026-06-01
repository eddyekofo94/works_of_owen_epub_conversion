#!/usr/bin/env python3
# v3
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
from html import escape as _html_escape, unescape as _html_unescape
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

_RENDER_DIR = Path(__file__).parent.resolve()
if str(_RENDER_DIR) not in sys.path:
    sys.path.insert(0, str(_RENDER_DIR))

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES, TITLE_PAGE_FONTS, PROXIMA_NOVA_FILES,
    convert_greek_word, clean_greek_text, convert_gideon_hebrew,
    normalize_characters, polytonic_sweep,
    # Pipeline constants — moved to shared.py so extract.py no longer imports render
    FOOTNOTE_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE, FOOTNOTE_PLACEHOLDER_RE,
    FT_MARKER_RE, EMPTY_BRACKET_RE,
    STRUCTURAL_START_RE, INLINE_STRUCTURAL_MARKER_RE,
    ROMAN_HEADING_RE, ROMAN_ONLY_RE, PLAIN_CHAPTER_RE,
    CITATION_ABBREV_TRAIL_RE, CITATION_ABBREV_START_RE, CITATION_AUTHOR_TRAIL_RE,
    ROMAN_LIST_TOKEN, MARKDOWN_STRUCTURAL_START_RE,
    SCRIPTURE_BOOK_RE, SCRIPTURE_REF_RE, SCRIPTURE_CONTINUATION_TRAIL_RE,
    _normalize_spaced_caps, _normalize_i_will,
    _normalize_scholarly_citation_artifacts, _repair_owen_ocr_errors,
    title_case, nav_display_title, _norm_for_dedupe,
    _is_scripture_ref_fragment, _scripture_ref_tokens,
    _split_inline_structural_markers, _repair_known_catechism_ghosts,
    _trim_duplicate_reference_prefix,
)

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed.")

FONT_BASE = os.path.join(_RENDER_DIR, 'fonts')


# ================================================================
# RENDER-ONLY CONSTANTS (not used by extract.py)
# ================================================================

# Regex for detecting Beta Code words that missed font tagging.
# Keep this conservative: the fallback runs after ordinary prose has been
# escaped, so broad markers like apostrophe or leading j/J corrupt English
# words such as "author’s", "Jesus", "John", and "justification".
BETA_CODE_RE = re.compile(
    r"(?<!\S)(?![^æ;]*[æ;])(?:"
    r"[abgdezhqiklmnxoprstufcyvwjABGDEZHQIKLMNXOPRSTUFCYVWJ]+[><=~|{}+]+"
    r"[abgdezhqiklmnxoprstufcyvwjABGDEZHQIKLMNXOPRSTUFCYVWJ><=~|{}\[\]+’]*|"
    r"[><=~|{}+]+[abgdezhqiklmnxoprstufcyvwjABGDEZHQIKLMNXOPRSTUFCYVWJ]+"
    r"[abgdezhqiklmnxoprstufcyvwjABGDEZHQIKLMNXOPRSTUFCYVWJ><=~|{}\[\]+’]*|"
    r"pneu’ma"
    r")\.?(?!\S)"
)

# Regex for detecting Gideon Hebrew words that missed font tagging.
# Matches words containing unambiguous Gideon-only marks. Plain semicolon,
# bracket, and digit 1 are ordinary English/list punctuation and caused major
# false positives ("grace;" and "vol. 1" became Hebrew).
GIDEON_HEBREW_RE = re.compile(
    r"(?<!\S)[a-zA-Z0-9\[\];,`=/\’’’µËÚãæçˆ˚≈}]*"
    r"(?:[µËÚãæçˆ˚≈}])"
    r"[a-zA-Z0-9\[\];,`=/\’’’µËÚãæçˆ˚≈}]*\.?(?!\S)"
)

STRUCTURAL_PREFIX_HTML_RE = re.compile(
    r'^(?P<marker>'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]\.?|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\.?|'
    r'\[(?:FIRST|SECONDLY|SECOND|THIRDLY|THIRD|FOURTHLY|FOURTH|FIFTHLY|FIFTH|'
    r'SIXTHLY|SIXTH|SEVENTHLY|SEVENTH|EIGHTHLY|EIGHTH|NINTHLY|NINTH|LASTLY|LAST)\][,.;]?|'
    r'(?!(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\.)[IVXLCDM]+\.|'
    r'(?:Q\.|Ques\.|Ans\.|A\.\s*\d+\.)|'
    r'(?:Obj(?:ection)?\.?\s*\d*\.?|Ans(?:wer)?\.?\s*\d*\.?|Sol(?:ution)?\.?\s*\d*\.?|Use\.?\s*\d+\.)|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?|'
    r'(?:First|Firstly|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Seventhly|Eighthly|Ninthly|Lastly)\b[,.]'
    r')(?P<space>\s+)'
)
# ================================================================
# SCHOLASTIC ANCHOR POST-PROCESSOR
# ================================================================

# Raw string used in _SCHOLASTIC_ANCHOR_SPLIT_RE and apply_scholastic_anchor_protocol
_SCHOLASTIC_LABEL_RE = (
    r'(?:Obj(?:ection)?\.?\s*\d*\.?|Ans(?:wer)?\.?\s*\d*\.?|'
    r'Sol(?:ution)?\.?\s*\d*\.?|Use\.?\s*\d+\.?|Usus\.?\s*\d+\.?|'
    r'Application\.?\s*\d+\.?)'
)

_SCHOLASTIC_ANCHOR_SPLIT_RE = re.compile(
    r'([.!?"\u201d])\s+'           # closing punctuation / quote
    r'(?P<label>'
    + _SCHOLASTIC_LABEL_RE +
    r')\s',
    re.I,
)

# Pattern to detect "Objection ." (space before period) — OCR artifact
_SCHOLASTIC_SPACE_DOT_RE = re.compile(
    r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application)\s+\.',
    re.I,
)


def _get_scholastic_subclass(label_text: str) -> str:
    label_upper = label_text.upper()
    if any(w in label_upper for w in ['OBJ', 'USE', 'USUS', 'APPLICATION', 'INQUIRY']):
        return 'scholastic-anchor-parent'
    if any(w in label_upper for w in ['ANS', 'SOL', 'RESPONSE']):
        return 'scholastic-anchor-child'
    return 'scholastic-anchor-child'  # default fallback is child


def _nest_scholastic_in_divs(html: str) -> str:
    """Group consecutive scholastic-anchor-child paragraphs and nest them in a <div class="owen-branch owen-level-2">
    container under their preceding introducing paragraph/objection, ensuring proper vertical border and indentation.
    """
    import re
    # 1. Promote level-1 divs that start with a scholastic child anchor to level-2
    html = re.sub(
        r'<div class="owen-branch owen-level-1">\s*(<p\b[^>]*class="[^"]*scholastic-anchor-child[^"]*")',
        r'<div class="owen-branch owen-level-2">\n\1',
        html,
        flags=re.I
    )

    # 2. Token-based wrapping for any remaining top-level scholastic child anchors
    token_re = re.compile(
        r'(<div\b[^>]*>|</div>|<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )
    
    tokens = []
    last_idx = 0
    for m in token_re.finditer(html):
        inter = html[last_idx:m.start()]
        if inter:
            tokens.append(inter)
        tokens.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:]
    if tail:
        tokens.append(tail)

    def is_scholastic_child(t: str) -> bool:
        if not t.startswith('<p') or not t.endswith('</p>'):
            return False
        m = re.match(r'^<p\b[^>]*class="([^"]*)"', t)
        if m:
            classes = m.group(1).split()
            return 'scholastic-anchor-child' in classes
        return False

    def is_whitespace(t: str) -> bool:
        return not t.strip()

    output_tokens = []
    active_divs = []
    i = 0
    n = len(tokens)
    while i < n:
        token = tokens[i]
        if token.startswith('<div'):
            m_div = re.match(r'^<div\b[^>]*class="([^"]*)"', token)
            div_classes = m_div.group(1).split() if m_div else []
            level = 0
            for c in div_classes:
                if c.startswith('owen-level-'):
                    try:
                        level = int(c.split('-')[-1])
                    except ValueError:
                        pass
            active_divs.append(level)
            output_tokens.append(token)
            i += 1
        elif token == '</div>':
            if active_divs:
                active_divs.pop()
            output_tokens.append(token)
            i += 1
        elif is_scholastic_child(token):
            current_level = active_divs[-1] if active_divs else 0
            if current_level >= 2:
                output_tokens.append(token)
                i += 1
            else:
                seq_indices = [i]
                j = i + 1
                while j < n:
                    if is_scholastic_child(tokens[j]):
                        seq_indices.append(j)
                        j += 1
                    elif is_whitespace(tokens[j]):
                        j += 1
                    else:
                        break
                
                end_idx = seq_indices[-1]
                output_tokens.append('<div class="owen-branch owen-level-2">')
                for idx in range(i, end_idx + 1):
                    output_tokens.append(tokens[idx])
                output_tokens.append('</div>')
                i = end_idx + 1
        else:
            output_tokens.append(token)
            i += 1
            
    return "".join(output_tokens)


def apply_scholastic_anchor_protocol(html: str) -> str:
    """Post-processor: ensure Obj./Ans./Use. labels start their own paragraphs
    and sequentially chain bare ordinals following a starting scholastic label.

    Runs on the assembled chapter XHTML string after markdown_to_html().
    """
    # 1. Remove stray space before period in scholastic labels
    html = _SCHOLASTIC_SPACE_DOT_RE.sub(lambda m: m.group(1) + '.', html)

    # 2. Force paragraph break before scholastic labels that appear mid-paragraph
    def _split_before_label(m: re.Match) -> str:
        return f'{m.group(1)}</p>\n<p class="scholastic-anchor"><b>{m.group("label")}</b> '

    html = _SCHOLASTIC_ANCHOR_SPLIT_RE.sub(_split_before_label, html)

    # 3. Clean up leading <b> tags around Obj./Ans. abbreviations to expose them as plain text
    # e.g., <b>Ans.</b> 1. -> Ans. 1.
    def _strip_b_tags(m: re.Match) -> str:
        label_word = m.group(2)
        digit_part = m.group(3)
        return f'{m.group(1)}{label_word} {digit_part} '

    _STRIP_B_RE = re.compile(
        r'(<p(?:\s[^>]*)?>)\s*<b>\s*(Obj(?:ection)?\.?|Ans(?:wer)?\.?|Sol(?:ution)?\.?|Use\.?|Usus\.?|Application\.?)\s*</b>\s*(\d+\.?)\s*',
        re.I
    )
    html = _STRIP_B_RE.sub(_strip_b_tags, html)

    # 4. Bold all scholastic labels at paragraph start (improved original step)
    def _clean_scholastic_label(label: str) -> str:
        label = re.sub(r'\s+', ' ', label).strip()
        label = re.sub(r'\s+\.', '.', label)
        label = re.sub(r'\.(?=\d)', '. ', label)
        return label

    html = re.sub(
        r'(<p(?:\s[^>]*)?>)\s*'
        r'(?P<label>' + _SCHOLASTIC_LABEL_RE + r')\s',
        lambda m: f'{m.group(1)}<b class="scholastic-label">{_clean_scholastic_label(m.group("label"))}</b> ',
        html,
        flags=re.I,
    )

    # 5. Standardize paragraph class to "scholastic-anchor" for all scholastic labels
    _SCHOLASTIC_ANCHOR_PARA_RE = re.compile(
        r'<p\s+class="([^"]*)"([^>]*)>\s*(<b class="scholastic-label">.*?</b>)',
        re.I
    )
    def _add_anchor_class(m: re.Match) -> str:
        classes = m.group(1).split()
        filtered = [c for c in classes if not (c.startswith('list-') or c == 'roman-list-item')]
        if 'scholastic-anchor' not in filtered:
            filtered.append('scholastic-anchor')
            
        label_content = re.sub(r'<[^>]+>', '', m.group(3))
        subclass = _get_scholastic_subclass(label_content)
        if subclass not in filtered:
            filtered.append(subclass)
            
        return f'<p class="{" ".join(filtered)}"{m.group(2)}>{m.group(3)}'

    html = _SCHOLASTIC_ANCHOR_PARA_RE.sub(_add_anchor_class, html)

    # Add class to bare paragraphs starting with a scholastic label
    def _add_bare_anchor_class(m: re.Match) -> str:
        label_content = re.sub(r'<[^>]+>', '', m.group(1))
        subclass = _get_scholastic_subclass(label_content)
        return f'<p class="scholastic-anchor {subclass}">{m.group(1)}'

    html = re.sub(
        r'<p>\s*(<b class="scholastic-label">.*?</b>)',
        _add_bare_anchor_class,
        html,
        flags=re.I
    )

    # 6. Smart Scholastic Chain State Machine
    lines = html.split('\n')
    out = []
    active_prefix = None
    expected_idx = None

    for line in lines:
        stripped = line.strip()
        
        m_label = re.search(
            r'<p[^>]*class="[^"]*scholastic-anchor[^"]*"[^>]*>\s*<b class="scholastic-label">(Obj|Ans|Sol|Use|Usus|Application)\.\s*(\d+)\.</b>',
            stripped,
            re.I
        )
        if m_label:
            active_prefix = m_label.group(1)
            expected_idx = int(m_label.group(2)) + 1
            out.append(line)
            continue

        if active_prefix and expected_idx is not None:
            m_digit = re.search(
                r'(<p\s+class=")([^"]*)("[^>]*>\s*)<b>(\d+)\.</b>\s*(.*)',
                line,
                re.I
            )
            if m_digit:
                digit_val = int(m_digit.group(4))
                if digit_val == expected_idx:
                    classes = m_digit.group(2).split()
                    filtered = [c for c in classes if not (c.startswith('list-') or c == 'roman-list-item')]
                    subclass = _get_scholastic_subclass(active_prefix)
                    if 'scholastic-anchor' not in filtered:
                        filtered.append('scholastic-anchor')
                    if subclass not in filtered:
                        filtered.append(subclass)

                    rewritten_line = (
                        f'{m_digit.group(1)}{" ".join(filtered)}{m_digit.group(3)}'
                        f'<b class="scholastic-label">{active_prefix.capitalize()}. {digit_val}.</b> {m_digit.group(5)}'
                    )
                    out.append(rewritten_line)
                    expected_idx += 1
                    continue

        if '<h' in stripped or '<hr' in stripped:
            active_prefix = None
            expected_idx = None

        out.append(line)

    combined_html = '\n'.join(out)
    return _nest_scholastic_in_divs(combined_html)


def normalize_footnote_markers(text):
    """Normalize AGES inline footnote markers like f2 or [ f2] to [f2]."""
    def repl(match):
        fn = next(group for group in match.groups() if group)
        return f'[f{fn}]'

    text = LOOSE_FOOTNOTE_MARKER_RE.sub(repl, text)
    return re.sub(r'(\[f\d+\])(?=[A-Za-z])', r'\1 ', text)


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
    - Tag every Unicode Greek run, including one-letter grammatical notes such
      as "ὅ", because these are already Unicode Greek and are not Beta-Code
      guesses.
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

    # 2. Tag Greek Unicode runs, including single-letter grammatical notes.
    def tag_greek(m):
        content = m.group(1)
        # Apply polytonic sweep to remove legacy accent artifacts
        clean = polytonic_sweep(content)
        if not clean.strip():
            return content
        return f'<span lang="el" xml:lang="el">{clean}</span>'

    text = re.sub(r'([\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\u0300-\u036F]*)', tag_greek, text)

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

    def _split_hebrew_inside_greek(m):
        content = m.group(1)
        parts = re.split(
            r'([\u0590-\u05FF\u0300-\u036F]*[\u0590-\u05FF][\u0590-\u05FF\u0300-\u036F]*(?:\s+[\u0590-\u05FF\u0300-\u036F]*[\u0590-\u05FF][\u0590-\u05FF\u0300-\u036F]*)*)',
            content,
        )
        out = []
        for part in parts:
            if not part:
                continue
            if re.search(r'[\u0590-\u05FF]', part):
                out.append(f'<span lang="he" xml:lang="he" dir="rtl">{part}</span>')
            else:
                out.append(f'<span lang="el" xml:lang="el">{part}</span>')
        return ''.join(out)

    text = re.sub(
        r'<span lang="el" xml:lang="el">([^<]*[\u0590-\u05FF][^<]*)</span>',
        _split_hebrew_inside_greek,
        text,
    )

    return text


def emphasize_structural_prefix(text):
    """Bold visible paragraph/list markers that survive the PDF extraction."""
    if not text or text.startswith('<b>'):
        return text
    return STRUCTURAL_PREFIX_HTML_RE.sub(r'<b>\g<marker></b>\g<space>', text, count=1)


def _detect_signature(plain: str, is_front_matter: bool) -> bool:
    """Return True if *plain* (HTML-stripped paragraph text) looks like an author signature.

    Patterns covered:
      1. Dash/equals prefix + title-case name   — "= John Owen", "— Thomas Goodwin"
      2. Bare initials                           — "J. O.", "W. H. G."
      3. Initials + study phrase                 — "J.O. From my study, ..."
      4. Goold/Edinburgh editor                  — "W. H. G. Edinburgh, 1850."
      5. Date-only (month + year)                — "May 11, 1677", "September the last, 1645"
      6. Place + year                            — "Edinburgh, 1682.", "London, 1682"
      7. ALL-CAPS name (front-matter only)       — "JOHN OWEN", "DANIEL BURGESS"
         Restricted to front-matter so that short chapter headings in body text
         (e.g. "THE HOLY SPIRIT") are never false-positives.
    """
    # Pattern 1 — dash/equals + title-case name (1–4 words), no sentence content
    if re.match(r'^[=—–-]\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\.?$', plain):
        if not re.search(r'\b(?:Chapter|Vol\.|p\.|pp\.|the|of|in|and)\b', plain, re.I):
            return True
    # Pattern 2 — bare initials only: "J. O." or "W. H. G."
    if re.match(r'^[A-Z]\.\s*[A-Z]\.(?:\s*[A-Z]\.)?\.?$', plain):
        return True
    # Pattern 3 — initials + "From my study …"
    if re.match(r'^[A-Z]\.[A-Z]\.\s+From\s+my\s+study', plain, re.I):
        return True
    # Pattern 3b — standalone "From my study"
    if re.match(r'^From\s+my\s+study\b', plain, re.I) and len(plain) < 40:
        return True
    # Pattern 4 — Goold header (initials + optional city + 18xx date)
    if re.match(r'^W\.\s*H\.\s*G\.', plain):
        return True
    # Pattern 5 — date-only: "May 11, 1677", "September the last, [1645]"
    if re.match(
        r'^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?'
        r'|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
        r'\s+(?:the\s+)?\w+,?\s*\[?\d{4}\]?\.?$',
        plain,
    ):
        return True
    # Pattern 6 — place + year: "Edinburgh, 1682", "London, 1677."
    if re.match(r'^[A-Z][a-z]+,\s*\d{4}\.?$', plain):
        return True
    # Pattern 6b — place + month + year: "Edinburgh, August 1850."
    _months = r'(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    if re.match(rf'^[A-Z][a-z]+,\s+{_months}\s+\d{{4}}\.?$', plain, re.I):
        return True
    # Pattern 7 — ALL-CAPS name (front-matter only to avoid heading false positives)
    if is_front_matter:
        words = plain.rstrip('.').split()
        if (
            2 <= len(words) <= 4
            and len(plain) < 50
            and all(re.match(r'^[A-Z]+$', w) for w in words)
            and not re.search(r'\b(?:THE|AND|FOR|NOT|BUT|ALL|GOD|HIS|ITS)\b', plain)
        ):
            return True
    return False


RENDERED_INLINE_STRUCTURAL_RE = re.compile(
    r'(?P<marker><b>(?:'
    r'(?!\d{4}\.)\d{1,3}\.|'
    r'\[(?:\d+\.?|\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\]\.?|'
    r'\[(?:FIRST|SECONDLY|SECOND|THIRDLY|THIRD|FOURTHLY|FOURTH|FIFTHLY|FIFTH|'
    r'SIXTHLY|SIXTH|SEVENTHLY|SEVENTH|EIGHTHLY|EIGHTH|NINTHLY|NINTH|LASTLY|LAST)\][,.;]?|'
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
        if CITATION_ABBREV_TRAIL_RE.search(before_text):
            continue
        # Issue 9: Prevent splitting after a book name + reference (e.g. Romans 1:1)
        if SCRIPTURE_REF_RE.search(before_text) and re.search(rf'\b{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*\s*$', before_text, re.I):
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


def _roman_head_match(text):
    # Exclude well-known scholarly abbreviations that are composed entirely of
    # Roman-numeral letters (LXX, MT, OT, NT, DV, KJV, AV, NIV, ESV, NRSV).
    # Also exclude any Roman value > L (50) in body text — large values like LXX (70)
    # are virtually never section headings in Owen; they are abbreviations.
    _EXCLUSION = r'(?!\*{0,2}(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\*{0,2}[.\s])'
    m = re.match(
        _EXCLUSION + r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?(?:\s+(?P<rest>.*))?$',
        (text or '').strip(),
    )
    if m and _roman_to_int(m.group('roman')) > 50:
        return None
    return m


def _roman_decimal_marker_match(text):
    """Match combined outline markers such as "I. 1." without splitting them."""
    return re.match(
        r'^(?P<marker>(?:\*\*)?[IVXLCDM]+\.(?:\*\*)?\s+\d+\.)(?:\s+(?P<rest>.+))?$',
        (text or '').strip(),
    )


def _starts_roman_outline(previous_text, roman_number):
    if roman_number != 1:
        return False
    return bool(
        re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
        or re.search(r'(?:[—-]|,)\s*$', previous_text)
    )


def _is_roman_outline_entry(roman_text, previous_text, expected_roman_number):
    match = _roman_head_match(roman_text)
    if not match:
        return False, None
    roman_number = _roman_to_int(match.group('roman'))
    rest = (match.group('rest') or '').strip()
    if not rest:
        return False, None
    if (
        (_starts_roman_outline(previous_text, roman_number) or expected_roman_number == roman_number)
        and _is_roman_list_item(rest)
    ):
        return True, roman_number + 1
    return False, None


def _render_simple_roman_heading_content(raw_content):
    match = _roman_head_match(raw_content)
    if not match:
        return tag_unicode_ranges(_html_escape(_clean_heading_text(raw_content)))
    roman_html = f'<b>{_html_escape(match.group("roman"))}</b>'
    rest = _clean_heading_text(match.group('rest') or '')
    if not rest:
        return roman_html
    return f'{roman_html} {tag_unicode_ranges(_html_escape(rest))}'


def _split_roman_section_opening(text):
    match = _roman_head_match(text)
    if not match:
        return None
    rest = (match.group('rest') or '').strip()
    if len(re.findall(r'\w+', rest)) < 12:
        return None
    heading = match.group("roman")
    body = rest
    return heading, body


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
                roman_number == 1
                and (
                    re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                    or re.search(r'(?:[—-]|,)\s*$', previous_text)
                )
            )
            continues_list = expected_roman_number == roman_number

            if (starts_list and _is_roman_list_item(paragraphs[i + 1])) or continues_list:
                out.append(f'{ROMAN_LIST_TOKEN} {roman_match.group("roman")} {paragraphs[i + 1].strip()}')
                expected_roman_number = roman_number + 1
                i += 2
                continue

        if roman_match:
            expected_roman_number = None
        out.append(paragraphs[i])
        i += 1

    return out


def _split_inline_catechism_questions(paragraphs, allow_bare_a=False):
    out = []
    # Split on space followed by Q./Ques. or A./Ans. markers
    # Supports optional bold ** markers.
    # NOTE: Case-sensitive to avoid catching scholarly citations like 'q. 81' (Issue 17)
    answer_marker = r'A\.|' if allow_bare_a else ''
    pattern = re.compile(
        rf'(?<!^)\s+(?=(?:\*\*)?(?:Q\.|Ques\.|{answer_marker}Ans\.)\s*(?:\d+\.)?\s*(?:\*\*)?)'
    )
    for para_idx, para in enumerate(paragraphs):
        parts = [part.strip() for part in pattern.split(para) if part.strip()]
        out.extend(parts or [para])
    return out


def _is_catechism_scripture_spill(text):
    clean = re.sub(r'\[f\d+\]', ' ', text)
    if re.match(r'^(?:\*\*)?[QA]\.', clean.strip()):
        return False
    has_ref_code = bool(re.search(r'<[0-9A-Fa-f]{6}>', clean))
    has_ref = bool(SCRIPTURE_REF_RE.search(clean))
    if not (has_ref_code or has_ref):
        return False
    clean = re.sub(r'<[0-9A-Fa-f]{6}>', ' ', clean)
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
    clean = re.sub(r'<[0-9A-Fa-f]{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    match = re.match(r'^(?:\*\*)?A\.(?:\*\*)?\s+(.{5,120}?[.!?;])', clean, re.I)
    return _norm_for_dedupe(match.group(1)) if match else ''


def _clean_catechism_footnote_spill(paragraphs):
    out = []
    in_catechism = False
    last_answer_head = ''
    for para_idx, para in enumerate(paragraphs):
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
    """Remove text that was pulled forward from following paragraphs (AGES ghosting)."""
    cleaned = list(paragraphs)
    for idx, para in enumerate(cleaned[:-1]):
        # Look ahead up to 6 paragraphs for ghosting
        for offset in range(1, min(7, len(cleaned) - idx)):
            next_para = cleaned[idx + offset].strip()
            if not next_para:
                continue

            curr_words = [
                (m.group(0).lower(), m.start(), m.end())
                for m in re.finditer(r"[A-Za-z0-9:]+", para)
            ]
            next_words = [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9:]+", next_para)]
            if len(curr_words) < 8 or len(next_words) < 6:
                continue

            best = None
            max_size = min(18, len(curr_words), len(next_words))
            for size in range(max_size, 5, -1):
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
                para = re.sub(r'\s{2,}', ' ', (para[:start] + ' ' + para[end:]).strip())
                cleaned[idx] = para
    return cleaned


def _remove_duplicate_catechism_answer_opening(text):
    """Collapse ghosted catechism answer openings inside one paragraph."""
    # Pattern: A. Body text. A. Body text.
    pattern = re.compile(
        r'^(?P<label>(?:\*\*)?(?:A\.|Ans\.|Q\.|Ques\.)(?:\*\*)?\s*(?:\d+\.)?\s*)'
        r'(?P<body>.{6,180}?[.!?;])\s+'
        r'(?:\*\*)?(?:A\.|Ans\.|Q\.|Ques\.)(?:\*\*)?\s*(?:\d+\.)?\s*(?P=body)',
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
def _coalesce_catechism_paragraphs(paragraphs):
    """Merge scripture reference paragraphs into the preceding Catechism answer."""
    if not paragraphs:
        return []
    out = []
    for para in paragraphs:
        stripped = para.strip()
        # If this paragraph looks like a bare scripture proof list and the 
        # previous paragraph was an Answer, merge them.
        # Allow leading digits/item markers (Issue 26)
        is_proof = re.match(rf'^(?:\d{{1,3}}\.?\s+)?(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b', stripped, re.I)
        if is_proof and out and re.match(r'^(?:\*\*)?(?:A\.|Ans\.)', out[-1].strip(), re.I):
            # Join with a space (Issue 16)
            out[-1] = out[-1].rstrip() + " " + stripped
        else:
            out.append(para)
    return out


def _strip_inline_structural_tokens(text):
    """Remove any structural tokens that leaked into paragraphs (e.g. [[SUMMARY]])."""
    return re.sub(r'\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*', '', text)


_SCHOLASTIC_QUOTED_OBJECTION_RE = re.compile(
    r'(?P<intro>\b(?:Obj(?:ection)?\.?\s*\d+\.?)\s+But\s+some\s+may\s+say,)\s*'
    r'(?P<quote>["“][^\n]+?)\n\n'
    r'\[\[BLOCKQUOTE\]\]\s*(?P<rest>.*?["”])',
    re.I | re.S,
)


def _repair_scholastic_blockquote_boundaries(text):
    """Move blockquote markers back over quoted Objection/Obj. openings."""
    if not text:
        return text

    def repl(match):
        quote = match.group("quote").strip()
        rest = re.sub(r'\s+', ' ', match.group("rest").strip())
        return f'{match.group("intro")}\n\n[[BLOCKQUOTE]] {quote} {rest}'

    return _SCHOLASTIC_QUOTED_OBJECTION_RE.sub(repl, text)


def _repair_markdown_tables(text: str) -> str:
    """Convert Markdown pipe-table paragraphs into [[BLOCKQUOTE]] / plain paragraph pairs."""
    if not text or ('|---|' not in text and '|--' not in text):
        return text

    paras = text.split('\n\n')
    out: list[str] = []

    for para in paras:
        stripped = para.strip()

        # Quick bail — paragraph has no table separator row
        if not re.search(r'\|[\-]+\|', stripped):
            out.append(para)
            continue

        # Normalise <br> tags → space so cell text reads as a single line
        normalised = re.sub(r'<br\s*/?>', ' ', stripped)

        # Split inline-concatenated rows. Each row ends with '|' and the next
        # starts with '|' with only whitespace between them.
        row_texts = re.split(r'(?<=\|)\s+(?=\|)', normalised)

        first_row = True
        for rt in row_texts:
            rt = rt.strip()
            if not rt:
                continue

            # Split cells by '|' and strip them.
            cells = [c.strip() for c in rt.split('|')]
            if cells and not cells[0]:
                cells.pop(0)
            if cells and not cells[-1]:
                cells.pop()

            if not cells:
                continue

            # Check if this is the separator row
            if all(re.match(r'^[\-]+$', c) for c in cells):
                continue

            if len(cells) >= 2:
                left = cells[0]
                right = cells[1]

                # Special case: unclosed preceding blockquote
                if first_row and out and out[-1].strip().startswith('[[BLOCKQUOTE]]') and out[-1].strip().endswith(','):
                    out[-1] = out[-1] + ' ' + right
                    out.append(left)
                else:
                    out.append('[[BLOCKQUOTE]] ' + right)
                    out.append(left)
                first_row = False

    return '\n\n'.join(out)


def _repair_fused_word_ordinals(text: str) -> str:
    """Split paragraphs at fused capitalised word ordinals (e.g. Secondly, Thirdly) that follow terminal punctuation."""
    if not text:
        return text

    paras = text.split('\n\n')
    out = []
    for para in paras:
        stripped = para.strip()
        # If it starts with a blockquote marker, do not split it.
        if stripped.startswith('[[BLOCKQUOTE]]'):
            out.append(para)
            continue

        # Otherwise, split at space before Thirdly/Secondly/etc. following terminal punctuation.
        pattern = r'(?<=[.!?])\s+(?=(?:Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Seventhly|Eighthly|Ninthly|Lastly|Finally),\s)'
        para_fixed = re.sub(pattern, '\n\n', para)
        out.append(para_fixed)

    return '\n\n'.join(out)


def _repair_mid_sentence_blockquote_splits(text: str) -> str:
    """Join paragraphs split mid-sentence before a [[BLOCKQUOTE]] marker."""
    if not text or '[[BLOCKQUOTE]]' not in text:
        return text

    paras = text.split('\n\n')
    out: list[str] = []
    i = 0
    n = len(paras)

    while i < n:
        para = paras[i]
        stripped = para.strip()

        if i == n - 1:
            out.append(para)
            i += 1
            continue

        next_para = paras[i+1].strip()
        if next_para.startswith('[[BLOCKQUOTE]]'):
            clean_end = stripped.rstrip('\"\' \t\r\n')
            if clean_end and not clean_end.endswith(('.', ',', ';', ':', '?', '!', '—', '-')):
                blockquote_content = next_para[len('[[BLOCKQUOTE]]'):].strip()
                merged_para = stripped + ' ' + blockquote_content
                paras[i+1] = merged_para
                i += 1
                continue

        out.append(para)
        i += 1

    return '\n\n'.join(out)



_TOKEN_STRIP_RE = re.compile(r'\[\[[A-Z_]+\]\]\s*')


def _repair_unbalanced_bracket_splits(text):
    """Rejoin paragraph fragments split across a \n\n where the previous
    paragraph has an unclosed '[' that isn't part of a [[TOKEN]] marker.

    This commonly occurs when a citation like '[Juv., 6. 546.]' gets broken
    across paragraphs during extraction: the structural token ends with '[Juv.,'
    and the continuation '6. 546.]' lands in its own paragraph.
    """
    if not text or '[' not in text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        # Strip [[TOKEN]] markers to count only content brackets
        content = _TOKEN_STRIP_RE.sub('', para)
        if content.count('[') > content.count(']') and i + 1 < len(paragraphs):
            # Absorb the next paragraph (the continuation of the unclosed bracket)
            paragraphs[i + 1] = para + ' ' + paragraphs[i + 1]
            i += 1
            continue
        result.append(para)
        i += 1
    return '\n\n'.join(result)


_DOC_STRUCTURE_TOKENS_RE = re.compile(
    r'^\[\[(?:CHAPTER|PART|SUBTITLE|DIGRESSION|BLOCKQUOTE)\]\]'
)


def _repair_lowercase_continuation_splits(text: str) -> str:
    """Rejoin paragraphs that open with a lowercase letter.

    Owen never begins a fresh paragraph with a lowercase letter.  When a
    paragraph starts with one it is a PDF page-boundary split: the sentence was
    cut mid-stream at a page turn and the continuation was left as a separate
    paragraph in the intermediate JSON.

    Structural document tokens ([[CHAPTER]], [[SUMMARY]], [[PART]], etc.) are
    never lowercased, so they are never affected.  [[BLOCKQUOTE]] text CAN be
    extended (the quote itself may have split across a page).

    Skipped when the previous paragraph is a bare document-structure header
    (those have no trailing prose that could be incomplete).
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and stripped
            and stripped[0].islower()
            and not _DOC_STRUCTURE_TOKENS_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            result[-1] = result[-1].rstrip() + ' ' + stripped
        else:
            result.append(para)
    return '\n\n'.join(result)


_CONNECTOR_END_RE = re.compile(
    r'(?:'
    r'[,;:—–-]\s*|'
    r'\b(?:and|or|but|as|to|into|unto|of|in|by|with|that|which|is|are|were|was|be|been)\b\s*'
    r')[”"\'’]*\s*$',
    re.I
)

_LIST_MARKER_START_RE = re.compile(
    r'^\s*(?:'
    r'[\(\[]?(?:1st|2nd(?:ly)?|2dly|3rd(?:ly)?|3dly|4th(?:ly)?|5th(?:ly)?|first|secondly|thirdly|fourthly|fifthly|lastly)\b'
    r')\s*',
    re.I
)


def _repair_flat_list_continuation_splits(text: str) -> str:
    """Rejoin paragraphs that open with a list marker when the previous paragraph
    ends with a connector or punctuation (e.g. comma, semicolon, colon, or connector word).
    This ensures that short inline lists that flow with the sentence are elegantly joined
    into a single paragraph instead of being broken into vertical block fragments.
    """
    if not text:
        return text
def _repair_flat_list_continuation_splits(text: str) -> str:
    """Rejoin paragraphs that open with a list marker when the previous paragraph
    ends with a connector or punctuation (e.g. comma, semicolon, colon, or connector word).
    This ensures that short inline lists that flow with the sentence are elegantly joined
    into a single paragraph, wrapping the inline markers in bold formatting (**marker**)
    to preserve their visual distinction.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        match = _LIST_MARKER_START_RE.match(stripped)
        if (
            result
            and stripped
            and match
            and _CONNECTOR_END_RE.search(result[-1].strip())
            and not _DOC_STRUCTURE_TOKENS_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            marker = match.group(0)
            marker_stripped = marker.strip()
            # Wrap marker in markdown bold asterisks if not already bolded
            if not (marker_stripped.startswith('**') and marker_stripped.endswith('**')):
                trailing_space = marker[len(marker_stripped):]
                bold_marker = f"**{marker_stripped}**{trailing_space}"
                stripped_bolded = bold_marker + stripped[match.end():]
            else:
                stripped_bolded = stripped
            
            result[-1] = result[-1].rstrip() + ' ' + stripped_bolded
        else:
            result.append(para)
    return '\n\n'.join(result)



_TRANSITIONAL_WORD_RE = re.compile(
    r'^(Therefore|Wherefore|Hence|Again|Moreover|Accordingly|Furthermore|'
    r'Nevertheless|Notwithstanding|Howbeit|Howsoever|Whence|Hereupon|'
    r'Herein|Hereby|Hereof|Hereto|Hereunto|Herewith|Therein|Thereby|'
    r'Thereof|Thereto|Thereunto|Therewith|But|So|Now|As|For)[,;.—\s]*$',
    re.I,
)
_SCHOLASTIC_CONTINUATION_RE = re.compile(
    r'^\d{1,3}\.\s+(?:q|a|p|pp|vol|sec|lib|cap|chap|serm|art|dist|part|num)\.',
    re.I,
)


def _repair_transitional_word_isolation(text: str) -> str:
    """Merge lone transitional words back onto their preceding paragraph.

    Owen sometimes had sentences like "...these things are inseparable.
    Therefore, 3. The difference..." which PDF extraction splits into three
    separate paragraphs. The middle "Therefore," fragment has no prose on its
    own and must be appended to the preceding paragraph.

    Only words known to function as sentence connectors are merged; proper
    nouns, names, and structural tokens are never touched.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and _TRANSITIONAL_WORD_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            # Append transitional fragment with a space
            trail = stripped.rstrip()
            result[-1] = result[-1].rstrip() + ' ' + trail
        else:
            result.append(para)
    return '\n\n'.join(result)


def _repair_scholastic_anchor_splits(text: str) -> str:
    """Rejoin scholastic citation tails split from their introducing clause.

    Pattern: paragraph ending with a comma after an author name, followed by a
    paragraph that begins with a two-or-more-digit number and a lowercase
    abbreviation (e.g. "22. q. 174, a. 1" — a Thomistic q./a. reference).
    These are never list items; they are inlined citation locators.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and _SCHOLASTIC_CONTINUATION_RE.match(stripped)
            and result[-1].rstrip().endswith(',')
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            result[-1] = result[-1].rstrip() + ' ' + stripped
        else:
            result.append(para)
    return '\n\n'.join(result)


# ---------------------------------------------------------------------------
# Dangling single-letter initial repair (Issue 21)
# ---------------------------------------------------------------------------
_DANGLING_INITIAL_END_RE = re.compile(
    r'(?<!\S)([A-Z])\.\s*$'   # bare single capital + period at end of paragraph
)
_CITATION_ABBREV_BEFORE_INITIAL_RE = re.compile(
    r'\b(?:chap|cap|lib|part|sect|num|vol|art|op|cit|ibid|serm)\.\s+[A-Z]\.\s*$',
    re.I,
)
_STRUCTURAL_DASH_BEFORE_INITIAL_RE = re.compile(
    r'[—–]\s*[A-Z]\.\s*$'
)
_COMMA_BEFORE_INITIAL_RE = re.compile(
    r',\s*[A-Z]\.\s*$'
)


def _repair_dangling_initial_splits(text: str) -> str:
    """Join a paragraph ending with a bare single-letter initial to the next.

    When a PDF line break falls in the middle of an author-initials citation
    (e.g. "S. P."), extract.py emits one paragraph ending with "S." and the
    next paragraph starting with "P. do sufficiently…".  This function merges
    them back into one paragraph.

    Guards — these endings are NOT merged (false positives):
    - Citation abbreviation before initial: "chap. I.", "cap. V.", etc.
    - Structural dash before initial:       "— I.", "– V." (numbered observations)
    - Doc-structure token at para start:    "[[ROMAN_HEAD]]", "[[CHAPTER]]", etc.
    - Comma immediately before initial:     ", V." (Roman numeral list entries)
    - Standalone initial paragraph:         "I." alone (Roman numeral heading)
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result: list = []
    for para in paragraphs:
        stripped = para.strip()
        if result:
            prev_stripped = result[-1].rstrip()
            m = _DANGLING_INITIAL_END_RE.search(prev_stripped)
            if m:
                text_before = prev_stripped[:m.start()].strip()
                if text_before:  # skip standalone initials (would be Roman headings)
                    is_citation = bool(_CITATION_ABBREV_BEFORE_INITIAL_RE.search(prev_stripped))
                    is_dash = bool(_STRUCTURAL_DASH_BEFORE_INITIAL_RE.search(prev_stripped))
                    is_doc_token = bool(re.match(r'^\[\[', prev_stripped))
                    is_comma = bool(_COMMA_BEFORE_INITIAL_RE.search(prev_stripped))
                    if not any([is_citation, is_dash, is_doc_token, is_comma]):
                        result[-1] = result[-1].rstrip() + ' ' + stripped
                        continue
        result.append(para)
    return '\n\n'.join(result)


def _repair_sermon_prefatory_note_splits(text: str) -> str:
    """Heal sermon prefatory note split by summary tag and page boundary.
    
    Pattern:
      Paragraph 1: 'THIS sermon, from'
      Paragraph 2: '[[SUMMARY]] Hebrews 12:27, was preached before Parliament on a'
      Paragraph 3: 'day set apart for extraordinary humiliation.'
    """
    if not text:
        return text
    pattern = re.compile(
        r'(THIS\s+sermon,\s+from)\s*\n\n\s*\[\[SUMMARY\]\]\s*([^A-Z\n]*[A-Z][^\n]*?)\s*\n\n\s*([a-z][^\n]*?)(?=\n\n|$)',
        re.S | re.I
    )
    return pattern.sub(r'\1 \2 \3', text)


def _split_tail_signature(text: str) -> str:
    """Split J.O. signature fused at the end of a body paragraph into its own paragraph."""
    if not text:
        return text
    pattern = re.compile(
        r'([.!?”"])\s+'
        r'(?P<sig>'
        r'J\.?\s*O\.?\s+From\s+my\s+Study.*|'
        r'J\.?\s*O\.?\s+September\s+the\s+last.*'
        r')$',
        re.I
    )
    return pattern.sub(r'\1\n\n\g<sig>', text)


def markdown_to_html(md_text, current_mode="BODY_TEXT", pending_drop_cap=False,
                     front_matter_style="blurb", config=None):
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
    
    # 0. Character normalization (Issue: Gideon/AGES legacy encoding)
    md_text = normalize_characters(md_text)

    # Apply replacements (Issue 108)
    md_text = _split_tail_signature(md_text)
    md_text = _repair_sermon_prefatory_note_splits(md_text)
    md_text = _repair_owen_ocr_errors(md_text, config=config)
    md_text = _repair_markdown_tables(md_text)
    md_text = _repair_fused_word_ordinals(md_text)
    md_text = _repair_mid_sentence_blockquote_splits(md_text)
    md_text = _repair_scholastic_blockquote_boundaries(md_text)
    # Strip stray '+' line-continuation OCR artifacts (e.g. ",+using" → ",using")
    md_text = re.sub(r'(?<=[,;.!?\s])\+(?=[a-z])', '', md_text)

    md_text = _repair_unbalanced_bracket_splits(md_text)
    md_text = _repair_lowercase_continuation_splits(md_text)
    md_text = _repair_transitional_word_isolation(md_text)
    md_text = _repair_scholastic_anchor_splits(md_text)
    md_text = _repair_dangling_initial_splits(md_text)
    md_text = _repair_flat_list_continuation_splits(md_text)

    normalized_paragraphs = [
        normalize_footnote_markers(para)
        for para in _merge_reference_continuation_paragraphs(md_text.split('\n\n'))
    ]
    
    # Apply volume-specific coalesce hook if provided (Issue 26)
    coalesce_hook = config.get('paragraph_coalesce_hook') if config else None
    is_catechism_context = bool(config.get('is_catechism_context')) if config else False
    if coalesce_hook:
        paragraphs = coalesce_hook(
            _split_inline_catechism_questions(
                _coalesce_roman_list_paragraphs(normalized_paragraphs),
                allow_bare_a=is_catechism_context,
            )
        )
    else:
        paragraphs = _split_inline_catechism_questions(
            _coalesce_roman_list_paragraphs(normalized_paragraphs),
            allow_bare_a=is_catechism_context,
        )
        
    expanded_paragraphs = []
    for para in paragraphs:
        expanded_paragraphs.extend(
            _split_inline_structural_markers(
                para,
                allow_bare_a=is_catechism_context,
            )
        )
    paragraphs = expanded_paragraphs
    paragraphs = [_repair_known_catechism_ghosts(para) for para in paragraphs]
    recent_plain = []
    roman_list_expected = None
    roman_sequence_choice = None
    pending_chapter_subtitle = False
    summary_continuation_active = False
    seen_footnote_refs = set()
    _fm_prose_started = False  # tracks first paragraph in a prose FM section
    _is_sermon_volume = bool(config.get('suppress_prefatory_note_heading')) if config else False
    _next_blockquote_is_opening = False  # reset per chapter in sermon volumes

    # Mode and drop cap state are passed in to preserve continuity across files
    
    for para_idx, para in enumerate(paragraphs):
        stripped = para.strip()
        if not stripped:
            continue
            
        # Detect pre-rendered HTML sections (Issue 106)
        if re.match(r'<section\b[^>]*class="[^"]*\btreatise-title-page\b', stripped):
            section_match = re.match(r'(?P<section><section\b[^>]*class="[^"]*\btreatise-title-page\b.*?</section>)(?P<trailing>.*)$', stripped, re.I | re.S)
            if section_match:
                html_parts.append(_polish_treatise_title_page_html(section_match.group('section'), seen_footnote_refs=seen_footnote_refs))
                trailing = section_match.group('trailing').strip()
                if trailing:
                    paragraphs.insert(para_idx + 1, trailing)
            else:
                html_parts.append(_polish_treatise_title_page_html(stripped, seen_footnote_refs=seen_footnote_refs))
            continue

        if stripped.startswith('>'):
            quote_content = re.sub(r'(?:^|\n)\s*>\s?', ' ', stripped).strip()
            stripped = f'[[BLOCKQUOTE]] {quote_content}'

        h_tag = None
        subtitle_md = None
        roman_heading = None
        is_centered_roman_list = False

        # State Transitions (Issue 107 Refinement)
        # We strip structural tokens for trigger detection
        clean_upper = re.sub(r'^\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*', '', stripped.upper()).strip()
        
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
        token_match = re.match(r'^\[\[(PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*(.*)$', stripped, re.S)
        if token_match:
            kind = token_match.group(1)
            content = token_match.group(2).strip()

            def _render_heading_content(raw_content: str) -> str:
                """Escape content for use in a heading, converting [fN] markers to noteref links."""
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'
                
                content_clean = _strip_inline_structural_tokens(raw_content)
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            def _render_blockquote_content(raw_content: str) -> str:
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'

                content_clean = _strip_inline_structural_tokens(raw_content)
                # Issue 26: strip a trailing open/left quotation mark that has no
                # matching close — the blockquote itself is the container, so an
                # unclosed opening quote at the end is always an OCR artifact.
                # Strip trailing unclosed opening quotes (Issue 26)
                content_clean = content_clean.rstrip()
                if content_clean.endswith(('“', '‘')):
                    content_clean = content_clean[:-1].rstrip()
                elif content_clean.endswith('"'):
                    if len(content_clean) <= 1 or content_clean[-2].isspace():
                        content_clean = content_clean[:-1].rstrip()
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            if kind == 'BLOCKQUOTE':
                if not content.strip():
                    continue
                
                # Blemish 9: Extract leading scripture from blockquote content
                # e.g., "[[BLOCKQUOTE]] 1 Corinthians 10:9, \"Neither...\""
                scripture_match = re.match(
                    rf'^((?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\s+\d+:\d+(?:[-,]\s*\d+)*),\s+(.*)$',
                    content, re.I | re.S
                )
                if scripture_match:
                    ref = scripture_match.group(1)
                    content = scripture_match.group(2)
                    html_parts.append(f'<p class="scripture-ref-introduction">{tag_unicode_ranges(_html_escape(ref))},</p>')

                if _next_blockquote_is_opening:
                    bq_class = ' class="sermon-opening-scripture"'
                    _next_blockquote_is_opening = False
                else:
                    bq_class = ''
                html_parts.append(f'<blockquote{bq_class} epub:type="z3998:quotation"><p class="blockquote-content">{_render_blockquote_content(content)}</p></blockquote>')
                pending_drop_cap = False
                roman_list_expected = None
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            
            # Zone A (Front Matter) Immunity: Treat all structural components as
            # simple items until we hit the Body transition.
            if current_mode == "FRONT_MATTER" and not is_major_trigger:
                _escaped = _render_heading_content(content)
                if front_matter_style == "prose":
                    if kind == 'PART':
                        part_match = re.match(r'^(Part\s+[IVXLCDM]+\.?)(.*)$', content, re.I | re.S)
                        if part_match:
                            lead = _html_escape(part_match.group(1).rstrip('.'))
                            rest = _render_heading_content(part_match.group(2).strip())
                            html_parts.append(f'<p class="analysis-part"><b>{lead}.</b> {rest}</p>')
                        else:
                            html_parts.append(f'<p class="analysis-part"><b>{_escaped}</b></p>')
                        _fm_prose_started = False
                        pending_drop_cap = False
                        continue
                    if kind == 'ROMAN_HEAD':
                        roman_match = re.match(r'^([IVXLCDM]+\.)\s*(.*)$', content, re.I | re.S)
                        if roman_match:
                            numeral = _html_escape(roman_match.group(1))
                            rest = _render_heading_content(roman_match.group(2).strip())
                            html_parts.append(f'<p class="roman-list-item"><b>{numeral}</b> {rest}</p>')
                        else:
                            html_parts.append(f'<p class="roman-list-item">{_escaped}</p>')
                        _fm_prose_started = False
                        pending_drop_cap = False
                        continue
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
                            f'{_render_heading_content(title_text)}'
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



            def _render_summary_content(raw_content: str) -> str:
                """Render chapter-summary text without body list/scholastic styling."""
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'

                content_clean = _strip_inline_structural_tokens(raw_content)
                content_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', content_clean)
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            def _render_roman_heading_content(raw_content: str) -> str:
                """Render a Roman heading with only the numeral bolded."""
                content_clean = _strip_inline_structural_tokens(raw_content)
                match = _roman_head_match(content_clean)
                if not match:
                    return _render_heading_content(content_clean)
                roman_html = f'<b>{_html_escape(match.group("roman"))}</b>'
                rest = (match.group('rest') or '').strip()
                if not rest:
                    return roman_html
                return f'{roman_html} {_render_heading_content(rest)}'

            if kind == 'PART':
                summary_continuation_active = False
                html_parts.append(f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">{_render_heading_content(content)}</h1>')
                # Only trigger BODY_START/drop cap if it matches the pattern (Issue 107 Refinement)
                if is_major_trigger:
                    pending_drop_cap = True
                    current_mode = "BODY_START"
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'CHAPTER':
                summary_continuation_active = False
                html_parts.append(f'<h1 class="secondary">{_render_heading_content(content)}</h1>')
                # In sermon volumes, the first blockquote after each chapter heading is the opening scripture
                if _is_sermon_volume:
                    _next_blockquote_is_opening = True
                # CHAPTER does not trigger or reset pending_drop_cap (Issue 107)
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'ROMAN_HEAD':
                summary_continuation_active = False
                previous_text = recent_plain[-1] if recent_plain else ''
                
                roman_match = _roman_head_match(content)
                roman_number = _roman_to_int(roman_match.group('roman')) if roman_match else None
                
                is_roman_list = False
                if roman_number == 1:
                    is_roman_list, next_roman = _is_roman_outline_entry(
                        content,
                        previous_text,
                        roman_list_expected,
                    )
                    roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                elif roman_number is not None and roman_number > 1:
                    if roman_sequence_choice == 'list-item':
                        is_roman_list = True
                    elif roman_sequence_choice == 'roman-subheading':
                        is_roman_list = False
                    else:
                        is_roman_list, next_roman = _is_roman_outline_entry(
                            content,
                            previous_text,
                            roman_list_expected,
                        )
                else:
                    is_roman_list, next_roman = _is_roman_outline_entry(
                        content,
                        previous_text,
                        roman_list_expected,
                    )

                if current_mode == "FRONT_MATTER":
                    html_parts.append(f'<p class="roman-list-item">{_render_roman_heading_content(content)}</p>')
                    roman_list_expected = roman_number + 1 if (is_roman_list and roman_number is not None) else None
                elif is_roman_list:
                    html_parts.append(f'<p class="roman-list-item">{_render_roman_heading_content(content)}</p>')
                    roman_list_expected = roman_number + 1 if roman_number is not None else None
                else:
                    html_parts.append(f'<h4 class="roman-subheading">{_render_roman_heading_content(content)}</h4>')
                    roman_list_expected = None
                pending_drop_cap = False
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'SUBTITLE':
                summary_continuation_active = False
                # Catechism protection: don't render Q./A. as subtitles (Issue 102)
                if re.match(r'^(?:\*\*)?(?:Q\.|Ques\.|A\.|Ans\.)\s*(?:\d+\.)?\s*(?:\*\*)?', content, re.I):
                    stripped = content
                    # Fall through to normal paragraph rendering
                else:
                    html_parts.append(f'<h4 class="chapter-subtitle">{_render_heading_content(content)}</h4>')
                    recent_plain.append(_strip_footnote_placeholders(content))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            elif kind == 'SUMMARY':
                # Blemish 7: Some chapter summaries begin with an all-caps titled
                # heading (the sub-topic title of the treatise) followed by a mixed-
                # case synopsis sentence.  Detect this and render the heading as
                # <h3 class="chapter-heading"> (slightly smaller than the chapter
                # title, larger than the synopsis) and the synopsis separately.
                #
                # Heuristic: content starts with ≥10-char all-caps run ending in
                # sentence punctuation, immediately followed by a mixed-case sentence.
                # Pure Roman-numeral tokens are excluded (handled by ROMAN_HEAD).
                _summary_heading_re = re.compile(
                    r"^(?P<heading>[A-Z][A-Z\s,;:'\u2018\u2019\u2014\-]{9,}[.!?])\s+"
                    r"(?P<synopsis>[\dA-Z\"\u201c\u2018(].{10,})$",
                    re.S,
                )
                # Issue 28: a footnote number immediately after sentence punctuation
                # (e.g. "AUGUSTINE.133") prevents the heading/synopsis split because
                # digits are not in the heading character class.  Strip inline
                # footnote refs (digits following [.!?] before a space) so the
                # heuristic sees clean all-caps heading text.
                _content_for_split = re.sub(
                    r'([.!?])(\d{1,4})(?=\s+[A-Z\"\u201c\u2018(])', r'\1', content.strip()
                )
                _smatch = _summary_heading_re.match(_content_for_split)
                # Synopsis must contain lowercase letters to confirm it's genuinely
                # mixed-case (avoids splitting a second all-caps run as heading+synopsis).
                _synopsis_has_lower = (
                    _smatch and bool(re.search(r'[a-z]', _smatch.group('synopsis')[:80]))
                )
                if _smatch and _synopsis_has_lower and not ROMAN_ONLY_RE.match(
                    _smatch.group('heading').rstrip('.!? ').strip()
                ):
                    # Case 2: All-caps heading + mixed-case synopsis in same paragraph.
                    # The synopsis may continue into the next paragraph (e.g. long
                    # outlines split across PDF pages), so keep continuation active.
                    h_text = _smatch.group('heading').strip()
                    s_text = _smatch.group('synopsis').strip()
                    html_parts.append(
                        f'<h3 class="chapter-heading">{_render_heading_content(h_text)}</h3>'
                    )
                    html_parts.append(
                        f'<p class="chapter-summary">{_render_summary_content(s_text)}</p>'
                    )
                    summary_continuation_active = True
                else:
                    # Distinguish Case 1 (entirely all-caps) from Case 3 (mixed-case synopsis).
                    # Owen chapter sub-headings are all-caps outline entries; synopses are prose.
                    _content_letters = [c for c in content if c.isalpha()]
                    _upper_ratio = (
                        sum(1 for c in _content_letters if c.isupper()) / len(_content_letters)
                        if _content_letters else 0
                    )
                    _is_all_caps_heading = (
                        _upper_ratio >= 0.92
                        and not ROMAN_ONLY_RE.match(content.strip().rstrip('.!? ').strip())
                    )
                    if _is_all_caps_heading:
                        # Case 1: Entirely all-caps → chapter sub-heading, body text follows.
                        html_parts.append(
                            f'<h3 class="chapter-heading">{_render_heading_content(content)}</h3>'
                        )
                        summary_continuation_active = False
                    else:
                        # Case 3: Mixed-case synopsis paragraph; continuation may follow.
                        html_parts.append(
                            f'<p class="chapter-summary">{_render_summary_content(content)}</p>'
                        )
                        summary_continuation_active = True
                # SUMMARY does not trigger or reset pending_drop_cap (Issue 107)
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'DIGRESSION':
                summary_continuation_active = False
                # Generate unique ID for Digressions
                num_match = re.search(r'\d+', content)
                d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
                html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{_render_heading_content(content.upper().rstrip("."))}</h3>')
                pending_drop_cap = False
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

            # Fall through for non-structural content or protected Q/A
            # (continue not called above)
            pass
        
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
        content_no_refs = _strip_inline_structural_tokens(content_no_refs)
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
                summary_continuation_active = False
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
                marker = f'{part_book_match.group(1).title()} {part_book_match.group(2).upper()}.'
                rest = (part_book_match.group(3) or '').strip()
                if rest and len(rest) > 18:
                    content_no_refs = f'**{marker}** {rest}'
                else:
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
                if subtitle:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    pending_chapter_subtitle = False
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            pending_chapter_subtitle = False

        if not h_tag:
            if summary_continuation_active:
                plain_summary_candidate = re.sub(r'\*\*(.+?)\*\*', r'\1', content_no_refs).strip()
                if _looks_like_summary_continuation(plain_summary_candidate):
                    summary_piece = _render_summary_content(content_no_refs)
                    if html_parts and html_parts[-1].startswith('<p class="chapter-summary">'):
                        html_parts[-1] = html_parts[-1][:-4] + f' {summary_piece}</p>'
                    else:
                        html_parts.append(f'<p class="chapter-summary">{summary_piece}</p>')
                    recent_plain.append(_strip_footnote_placeholders(plain_summary_candidate))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
                summary_continuation_active = False

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

        if not h_tag:
            subtitle_md, content_no_refs = _split_leading_chapter_subtitle(content_no_refs)

        if not h_tag and not subtitle_md:
            roman_decimal = _roman_decimal_marker_match(content_no_refs)
            if roman_decimal and roman_decimal.group('rest'):
                content_no_refs = f'**{_clean_heading_text(roman_decimal.group("marker"))}** {roman_decimal.group("rest").strip()}'
                roman_list_expected = None
            else:
                roman_match = ROMAN_HEADING_RE.match(content_no_refs)
                if roman_match:
                    roman_number = _roman_to_int(roman_match.group('roman'))
                    rest_after_roman = roman_match.group('rest').strip()
                    previous_text = recent_plain[-1] if recent_plain else ''
                    
                    is_roman_list = False
                    if roman_number == 1:
                        starts_roman_list = (
                            re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                            or re.search(r'(?:[—-]|,)\s*$', previous_text)
                        )
                        if starts_roman_list and _is_roman_list_item(rest_after_roman):
                            is_roman_list = True
                        roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                    elif roman_number > 1:
                        if roman_sequence_choice == 'list-item':
                            is_roman_list = True
                        elif roman_sequence_choice == 'roman-subheading':
                            is_roman_list = False
                        else:
                            is_roman_list = roman_list_expected == roman_number
                    
                    if is_roman_list or current_mode == "FRONT_MATTER":
                        content_no_refs = f'**{roman_match.group("roman")}** {rest_after_roman}'
                        is_centered_roman_list = True
                        roman_list_expected = roman_number + 1 if (is_roman_list or current_mode == "FRONT_MATTER") else None
                    else:
                        roman_heading = _render_simple_roman_heading_content(roman_match.group('roman'))
                        content_no_refs = rest_after_roman
                        roman_list_expected = None
                else:
                    roman_section = None
                    roman_head_start = _roman_head_match(content_no_refs)
                    if roman_head_start:
                        roman_number = _roman_to_int(roman_head_start.group('roman'))
                        rest_after_roman = (roman_head_start.group('rest') or '').strip()
                        previous_text = recent_plain[-1] if recent_plain else ''
                        
                        is_roman_list = False
                        if roman_number == 1:
                            if _starts_roman_outline(previous_text, roman_number):
                                is_roman_list = True
                            roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                        elif roman_number > 1:
                            if roman_sequence_choice == 'list-item':
                                is_roman_list = True
                            elif roman_sequence_choice == 'roman-subheading':
                                is_roman_list = False
                            else:
                                is_roman_list = roman_list_expected == roman_number
                        
                        if is_roman_list:
                            content_no_refs = f'**{roman_head_start.group("roman")}** {rest_after_roman}'
                            is_centered_roman_list = True
                            roman_list_expected = roman_number + 1
                        else:
                            roman_section = _split_roman_section_opening(content_no_refs)
                    if roman_section:
                        roman_heading = _render_simple_roman_heading_content(roman_section[0])
                        content_no_refs = roman_section[1]
                        roman_list_expected = None
                    elif not roman_head_start:
                        roman_list_expected = None
        
        # Clean up Catechism artifacts (Issue 26)
        text_html = content_no_refs
        
        # 1. Standardize Q/A labels: "Q. , , 8 ." -> "Q. 8."
        # CASE-SENSITIVE and strictly anchored to start of paragraph (Issue 26)
        text_html = re.sub(r'^([QA])\.\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        text_html = re.sub(r'^(Q)\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        # Handle "Q., 8." (Issue 26)
        text_html = re.sub(r'^(Q)\.,\s*(\d+)\.', r'\1. \2.', text_html)
        
        # 2. Cleanup leading/trailing bold artifacts
        if not MARKDOWN_STRUCTURAL_START_RE.match(text_html):
            text_html = re.sub(r'^\*\*(?:\*\*)?', '', text_html)
            text_html = re.sub(r'\*\*(?:\*\*)?$', '', text_html)
        # Specifically remove surviving .** artifact (Issue 91/107)
        text_html = re.sub(r'(?<!\*)\b(\d+)\.\*\*(?=\s+)', r'\1.', text_html)
        
        # Standardize Q/A labels for bolding (CASE-SENSITIVE, anchored)
        # Only allow A if followed by period or Ans/Ques (Issue 26)
        text_html = re.sub(r'^(Q\.|Ans\.|Ques\.|A\.\s*\d+\.)\s+', r'**\1** ', text_html)
        # For Q. N. form
        text_html = re.sub(r'^(Q\.\s*\d+\.|A\.\s*\d+\.|Ques\.\s*\d+\.|Ans\.\s*\d+\.)\s+', r'**\1** ', text_html)

        # Apply replacements again on the standard markers (Issue 108)
        text_html = _repair_owen_ocr_errors(text_html, config=config)

        # Cleanup unbalanced bold markers (Issue 26)
        if text_html.count('**') % 2 != 0:
            text_html = text_html.replace('**', '')
            
        def _repair_bold_marker(m):
            # Check if there is an unclosed ** before this match (Issue 91/107)
            if text_html[:m.start()].count('**') % 2 != 0:
                return m.group(0)
            return f"**{m.group(1)}**"
            
        text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', _repair_bold_marker, text_html)
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)
        
        # Clean up bolding on Q/A numbers
        text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(A\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(Q\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(A\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(\d+\.)\s+', r'<b>\1 \2</b> ', text_html)
        
        # Specific comma artifact cleanup (Issue 26)
        text_html = re.sub(r'<b>([QA])\.</b>\s*,\s*', r'<b>\1.</b> ', text_html)

        text_html = re.sub(
            r'^(<b>A\.</b>\s+)([^<]{6,180}?[.!?;])\s+<b>A\.</b>\s+\2',
            r'\1\2',
            text_html,
            flags=re.I,
        )
        text_html = emphasize_structural_prefix(text_html)
        text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(?:<b>)?(\d+\.)(?:</b>)?\s+', r'<b>\1 \2</b> ', text_html)
        text_html = re.sub(r'(\b(?:verse|verses|chap|chapter)\.?\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html, flags=re.I)
        text_html = re.sub(r'(\b\d+:\d+(?:[-,]\s*\d+)*,\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html)
        text_html = re.sub(r'<b>(\d+(?:st|nd|rd|th))</b>(\s+(?:Psalm|Psalms)\b)', r'\1\2', text_html)
        # Issue 27: if the paragraph STARTS with a bare bold number (e.g. <b>9.</b>) and
        # the previous paragraph ended with a scripture reference trailing comma or
        # a bare comma (suggesting a verse-range continuation split across lines),
        # the bold is spurious — undo it.
        _prev_plain = recent_plain[-1] if recent_plain else ''
        if (
            re.match(r'^<b>\d+[.;]?</b>\s', text_html)
            and re.search(r'(?:\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+)\s*,\s*$', _prev_plain)
            and not _TRANSITIONAL_WORD_RE.match(_prev_plain.strip())
        ):
            text_html = re.sub(r'^<b>(\d+[.;]?)</b>\s', r'\1 ', text_html)
        
        # Tag Unicode Greek/Hebrew ranges
        text_html = tag_unicode_ranges(text_html)
        text_html = _restore_footnote_placeholders(text_html)
        
        # Final punctuation normalization (Issue 26)
        text_html = re.sub(r',[\s,]+,', ',', text_html)
        text_html = re.sub(r',+', ',', text_html)
        text_html = re.sub(r'\.+', '.', text_html)
        text_html = re.sub(r', \.', r'.', text_html)
        
        # Ensure Q/A bolding includes the number
        text_html = re.sub(r'<b>([QA])\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)
        text_html = re.sub(r'<b>(Ques|Ans)\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)

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
                if not subtitle_html:
                    pass
                else:
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
                    
                    # Signature detection — consolidated helper (replaces fragmented patterns)
                    _sig_plain = re.sub(r'<[^>]+>', '', paragraph_html).strip()
                    _is_signature = _detect_signature(
                        _sig_plain,
                        is_front_matter=(current_mode == "FRONT_MATTER"),
                    )
                    if _is_signature:
                        # Strip trailing Greek residue if it was pulled in (Issue 26)
                        paragraph_html = re.sub(r'\s*[\u0370-\u03FF\u1F00-\u1FFF].*$', '', paragraph_html)
                        
                        # Split Goold signature into two lines (Issue 99)
                        m_sig = re.match(r'^((?:<i>|<b>)*W\.\s*H\.\s*G\.(?:</i>|</b>)*)\s+((?:<i>|<b>)*[A-Z][a-z]+,.*18\d{2}\.?(?:</i>|</b>)*)\s*$', paragraph_html)
                        if m_sig:
                            paragraph_html = f'{m_sig.group(1)}<br/>{m_sig.group(2)}'
                        
                        # Split J.O. study signature: "J.O. From my study, September..."
                        m_study = re.match(
                            r'^((?:<i>|<b>)*[A-Z]\.[A-Z]\.(?:</i>|</b>)*)\s+'
                            r'(From\s+my\s+study\b.*?),\s*'
                            r'([A-Z][a-z]+(?:\s+the\s+last)?,\s*\[?\d{4}\]?\.?)$',
                            paragraph_html,
                            re.I
                        )
                        if m_study:
                            paragraph_html = f'{m_study.group(1)}<br/>{m_study.group(2)}<br/>{m_study.group(3)}'
                        else:
                            m_study2 = re.match(r'^((?:<i>|<b>)*[A-Z]\.[A-Z]\.(?:</i>|</b>)*)\s+(From\s+my\s+study.*)$', paragraph_html, re.I)
                            if m_study2:
                                paragraph_html = f'{m_study2.group(1)}<br/>{m_study2.group(2)}'
                        
                        html_parts.append(f'<p class="signature">{paragraph_html}</p>')
                        pending_drop_cap = False
                        continue

                    # Rule 1: FRONT_MATTER rules
                    if current_mode == "FRONT_MATTER":
                        if front_matter_style == "prose":
                            # Check for embedded signature at end of paragraph (e.g., "...DANIEL BURGESS</b></i>")
                            _emb_sig = re.search(
                                r'(,\s*|\.\s*)(<i><b>|<b><i>|<i>|<b>)([A-Z][A-Z\s]+)(</b></i>|</i></b>|</i>|</b>)\s*\.?\s*(<a[^>]*noteref[^>]*>.*?</a>)?\s*$',
                                paragraph_html,
                            )
                            if _emb_sig:
                                sig_name = _emb_sig.group(3).strip()
                                sig_words = sig_name.split()
                                # Only treat as signature if 2-4 all-caps words (name)
                                if 2 <= len(sig_words) <= 4:
                                    prefix = paragraph_html[:_emb_sig.start()]
                                    # Remove trailing comma/space from prefix
                                    prefix = re.sub(r'[,.\s]+$', '', prefix)
                                    if prefix:
                                        html_parts.append(f'<p class="front-matter-prose">{prefix}</p>')
                                    html_parts.append(f'<p class="signature">{sig_name}</p>')
                                    pending_drop_cap = False
                                    continue
                            
                            # Running editorial prose: justify like normal body text.
                            if not _fm_prose_started:
                                p_cls = "front-matter-prose first"
                                _fm_prose_started = True
                            else:
                                p_cls = "front-matter-prose"
                            # Run prefix bolding on front-matter prose lists
                            paragraph_html = emphasize_structural_prefix(paragraph_html)
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
                                p_class = ' class="first"'
                                pending_drop_cap = False
                                current_mode = "BODY_TEXT" # Transition to State 3
                            # If is_subpoint or doesn't start with letter, we stay in BODY_START/pending_drop_cap=True
                        
                        # Catechism or List styling
                        if not p_class:
                            is_qa = (
                                re.match(r'^(?:<b>)?(?:Q\.|Ques\.|Ans\.)', paragraph_html, re.I)
                                or (
                                    is_catechism_context
                                    and re.match(r'^(?:<b>)?A\.', paragraph_html, re.I)
                                )
                            )
                            is_proof = re.match(rf'^(?:<b>)?(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b', paragraph_html, re.I)
                            roman_plain_match = _roman_head_match(plain_for_class)
                            is_combined_roman_decimal = bool(_roman_decimal_marker_match(plain_for_class))
                            is_continued_roman_outline = False
                            if roman_plain_match and not is_combined_roman_decimal:
                                roman_number = _roman_to_int(roman_plain_match.group('roman'))
                                rest_after_roman = (roman_plain_match.group('rest') or '').strip()
                                is_continued_roman_outline = (
                                    roman_list_expected == roman_number
                                    and _is_roman_list_item(rest_after_roman)
                                )
                                is_long_roman_section = (
                                    current_mode != "FRONT_MATTER"
                                    and
                                    not is_continued_roman_outline
                                    and len(re.findall(r'\w+', rest_after_roman)) >= 12
                                )
                                if is_long_roman_section:
                                    html_parts.append(f'<h4 class="roman-subheading">{paragraph_html}</h4>')
                                    pending_drop_cap = False
                                    continue
                            if is_qa or is_proof:
                                p_class = ' class="catechism-item"'
                            elif is_combined_roman_decimal:
                                p_class = ' class="list-item"'
                            elif is_continued_roman_outline:
                                p_class = ' class="roman-list-item"'
                                roman_list_expected = roman_number + 1
                            elif STRUCTURAL_START_RE.match(plain_for_class):
                                 # Numbered/lettered lists (Issue 23/26)
                                 p_class = ' class="list-item"'
                            elif re.match(r'^(?:<b>)?Part\s+[IVXLCDM]+\.', paragraph_html, re.I):
                                 p_class = ' class="list-item"'
                                
                            html_parts.append(f'<p{p_class}>{paragraph_html}</p>')
                        else:
                            html_parts.append(f'<p{p_class}>{paragraph_html}</p>')


        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
        if len(recent_plain) > 5:
            recent_plain = recent_plain[-5:]
    
    result_html = '\n'.join(html_parts)
    result_html = _attach_colon_introduced_list(result_html)
    result_html = _attach_em_dash_flat_list(result_html, config=config)
    result_html = _coalesce_adjacent_signatures(result_html)
    result_html = _merge_short_inline_lists(result_html)
    result_html = _add_owen_list_level_classes(result_html)
    result_html = _nest_owen_list_hierarchies(result_html)
    return result_html, current_mode, pending_drop_cap


# ---------------------------------------------------------------------------
# Issue #48 — colon-introduced list merging
# ---------------------------------------------------------------------------
def _attach_colon_introduced_list(html: str) -> str:
    """Merge a colon-terminated paragraph inline with the following list-item."""
    if not html:
        return html

    import re as _re

    # Case A: any non-list-item <p> ending in ':'
    html = _re.sub(
        r'(<p(?:(?! class="list-item")[^>])*>)'
        r'((?:(?!</p>).)*:)\s*</p>'
        r'\s*<p class="list-item">',
        r'<p class="list-item">\2 ',
        html,
        flags=_re.S,
    )

    # Case B: list-item whose bold marker is NOT parenthesised (e.g. "4." not "(1.)")
    # and whose next sibling IS a parenthesised sub-item "(N.)"
    html = _re.sub(
        r'(<p class="list-item">(?!<b>\())'   # intro: list-item, marker not starting "(…"
        r'((?:(?!</p>).)*:)\s*</p>'            # content ending ':'
        r'\s*<p class="list-item">(<b>\([^)]+\)</b>)', # next sibling starting with parenthesized bold marker
        r'\1\2 \3',
        html,
        flags=_re.S,
    )

    return html


# ---------------------------------------------------------------------------
# Helper: join split flat-list ordinal markers across consecutive paragraphs
# ---------------------------------------------------------------------------
def _join_orphaned_flat_list_marker_paragraphs(html: str) -> str:
    """Join paragraphs where a flat-list ordinal marker is orphaned at end of a <p>.

    E.g. '<p>heads: — <b>1.</b> Temptations. 2.</p>\\n<p>Afflictions.</p>'
    →    '<p>heads: — <b>1.</b> Temptations. <b>2.</b> Afflictions.</p>'
    """
    import re as _re
    pattern = _re.compile(
        r'(<p(?:\s[^>]*)?>)((?:(?!</p>).)*?)\s+(\d+\.)\s*</p>\s*\n\s*<p(?:\s[^>]*)?>((?:(?!</p>).)*?)</p>',
        _re.S,
    )
    def _replacer(m: '_re.Match') -> str:
        return f'{m.group(1)}{m.group(2)} <b>{m.group(3)}</b> {m.group(4)}</p>'
    return pattern.sub(_replacer, html)


# ---------------------------------------------------------------------------
# Helper: split a list-item that embeds an ordinal sub-sequence after '—'
# ---------------------------------------------------------------------------
def _split_ordinal_inline_expansions(html: str) -> str:
    """Split a list-item containing an embedded '— (ordinal)' expansion.

    Only fires when the intro before '—' is ≥ 8 plain words.
    E.g. '<p class="list-item"><b>(3rdly.)</b> His excellency…men: — (1st.) fitness…</p>'
    →    two separate list-item paragraphs, second one with bolded (1st.) marker.
    """
    import re as _re

    def _wc_plain(text: str) -> int:
        return len(_re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', text)).strip().split())

    # Matches '— (ordinal)' embedded inside a list-item body
    _EMBEDDED_ORDINAL_RE = _re.compile(
        r'(.*?—\s*)(\((?:1st|2nd(?:ly)?|2dly|3rd(?:ly)?|3dly|4th(?:ly)?|5th(?:ly)?)\.\))',
        _re.I | _re.S,
    )
    _LIST_ITEM_FULL_RE = _re.compile(
        r'^(<p class="list-item">)(<b>[^<]{1,30}</b>\s*)(.*)(</p>)$',
        _re.S,
    )

    out: list[str] = []
    for line in html.split('\n'):
        m = _LIST_ITEM_FULL_RE.match(line.strip())
        if not m:
            out.append(line)
            continue
        tag_open, bold_marker, body, _ = m.group(1), m.group(2), m.group(3), m.group(4)
        sm = _EMBEDDED_ORDINAL_RE.search(body)
        if not sm:
            out.append(line)
            continue
        intro_html = bold_marker + body[:sm.start(2)].rstrip()
        if _wc_plain(intro_html) < 8:
            out.append(line)
            continue
        ordinal = sm.group(2)                        # '(1st.)'
        remainder = body[sm.start(2) + len(ordinal):]  # ' His fitness…'
        out.append(f'{tag_open}{intro_html}</p>')
        out.append(f'{tag_open}<b>{ordinal}</b>{remainder}</p>')
    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Issue #16 — em-dash / open-punctuation flat syllabus flattening
# ---------------------------------------------------------------------------
def _attach_em_dash_flat_list(html: str, config: dict = None) -> str:
    """Absorb short Owenian flat-list prefixes into a preceding em-dash anchor.

    Signals
    -------
    F  — announced count exactly matches run length, ≤20 w per item
    H  — ≥3 items, all end '.', all ≤25 w
    G  — single-item ordinal that continues an existing inline ordinal sequence
    all_non_final_semi — every non-final item ends ';', non-final ≤20 w
    cont-comma — non-final item ends ',' → final item joins regardless of length
    cont-connector — non-final item ends 'and'/'or' → same
    A  — non-final item ends ';' or ',', ≤12 w (hard cap, Bug #6 raised from 8)
    B  — any item ends 'and'/'or', ≤12 w
    C  — all items ≤3 w
    D  — ≥3 items, all ≤7 w
    """
    if not html:
        return html

    if config and config.get('chapter_title') in config.get('flat_list_exclude_chapters', []):
        return html

    import re as _re

    def _parse_roman(s: str) -> int:
        s = s.upper().strip('.,:;()[]')
        if not s or not _re.match(r'^[IVXLCDM]+$', s):
            return 0
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        val = 0
        prev_val = 0
        for char in reversed(s):
            curr_val = roman_map.get(char, 0)
            if curr_val >= prev_val:
                val += curr_val
            else:
                val -= curr_val
            prev_val = curr_val
        return val

    def _get_marker_val_and_type(marker_text: str) -> tuple[str, int]:
        clean = _re.sub(r'<[^>]+>', '', marker_text).strip()
        clean = clean.strip('.,:; \t\n\r*')
        if not clean:
            return ('empty', 0)
        
        clean_upper = clean.upper()
        
        if clean.startswith('(') and clean.endswith(')'):
            inner = clean[1:-1].strip('.,:; ')
            if inner.isdigit():
                return ('arabic_paren', int(inner))
            if len(inner) == 1 and inner.isalpha():
                return ('alpha_paren', ord(inner.lower()) - ord('a') + 1)
            roman_val = _parse_roman(inner)
            if roman_val > 0:
                return ('roman_paren', roman_val)
                
        if clean.startswith('[') and clean.endswith(']'):
            inner = clean[1:-1].strip('.,:; ')
            if inner.isdigit():
                return ('arabic_bracket', int(inner))
            if len(inner) == 1 and inner.isalpha():
                return ('alpha_bracket', ord(inner.lower()) - ord('a') + 1)
            roman_val = _parse_roman(inner)
            if roman_val > 0:
                return ('roman_bracket', roman_val)

        w = clean_upper
        if 'FIRST' in w or '1ST' in w: return ('ordinal', 1)
        if 'SECOND' in w or '2ND' in w or '2DLY' in w: return ('ordinal', 2)
        if 'THIRD' in w or '3RD' in w or '3DLY' in w: return ('ordinal', 3)
        if 'FOURTH' in w or '4TH' in w or '4THLY' in w: return ('ordinal', 4)
        if 'FIFTH' in w or '5TH' in w or '5THLY' in w: return ('ordinal', 5)
        if 'SIXTH' in w or '6TH' in w: return ('ordinal', 6)
        if 'SEVENTH' in w or '7TH' in w: return ('ordinal', 7)
        if 'EIGHTH' in w or '8TH' in w: return ('ordinal', 8)
        if 'NINTH' in w or '9TH' in w: return ('ordinal', 9)
        if 'TENTH' in w or '10TH' in w: return ('ordinal', 10)

        if clean.isdigit():
            return ('arabic_bare', int(clean))
            
        roman_val = _parse_roman(clean)
        if roman_val > 0:
            return ('roman_bare', roman_val)
            
        if len(clean) == 1 and clean.isalpha():
            return ('alpha_bare', ord(clean.lower()) - ord('a') + 1)
            
        return ('unknown', 0)

    def _is_sequential_sequence(pairs) -> bool:
        parsed = [_get_marker_val_and_type(mk) for mk, _ in pairs]
        known_parsed = [(t, v) for t, v in parsed if t != 'unknown' and t != 'empty' and v > 0]
        if len(known_parsed) < 2:
            return True
            
        first_type = known_parsed[0][0]
        if not all(t == first_type for t, _ in known_parsed):
            return False
            
        for idx in range(1, len(known_parsed)):
            if known_parsed[idx][1] <= known_parsed[idx-1][1]:
                return False
        return True


    # ── caps ─────────────────────────────────────────────────────────────────
    _HARD_CAP     = 12   # base cap raised from 8 (Bug #6)
    _SIGNAL_F_CAP = config.get('list_item_merge_cap', 20) if config else 20   # exact announced-count match (tightened 2026-05-27)
    _SIGNAL_H_CAP = 25   # preview-syllabus: ≥3 items, all end '.', all ≤25 w
    _ALL_SEMI_CAP = 20   # all_non_final_semi: non-final items must be ≤20 w
    _ANCHOR_LIMIT = 80   # max plain words in a list-item anchor for auto-attach

    # ── patterns ─────────────────────────────────────────────────────────────
    _EXPLICIT_COUNT_RE = _re.compile(
        r'\b(?:I\s+understand\s+)?(?:two|three|four|five|six|seven|'
        r'eight|nine|ten|twofold|threefold|fourfold|\d+)\b.{0,120}'
        r'\b(?:things?|ways?|heads?|accounts?|regards?|parts?|'
        r'sorts?|considerations?|observations?|particulars?|'
        r'respects?|instances?)\b.{0,100}[—\-:,;.]\s*$',
        _re.I,
    )
    _FORMULA_TAIL_RE = _re.compile(
        r'\b(?:these?\s+following|as\s+follows?|following\s+particulars?|'
        r'(?:may|to)\s+be\s+(?:observed|noted|considered|mentioned)|'
        r'I\s+shall\s+(?:observe|note|propose|mention|consider)|'
        r'in\s+particular|are\s+these|namely\s+these|namely,\s+these)\b.{0,60}[—\-:,;.]\s*$',
        _re.I,
    )
    _LIST_ITEM_RE = _re.compile(
        r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
        _re.S,
    )
    # Ordinal markers: (1st.), (2ndly.), 3rdly., etc.
    _ORDINAL_MK_RE = _re.compile(
        r'^\(?(?:\d+(?:(?:st|nd|rd|th)ly?|dly|ly)|1st|2nd(?:ly)?|'
        r'3rd(?:ly)?|4th(?:ly)?)\.?\)?\.?$',
        _re.I,
    )
    # Detect inline ordinals already embedded in a preceding paragraph
    _HAS_INLINE_ORDINAL_RE = _re.compile(
        r'\((?:1st|2nd(?:ly|dly)?|3rd(?:ly|dly)?|4th(?:ly)?|5th(?:ly)?)\.\)',
        _re.I,
    )

    # ── helpers ───────────────────────────────────────────────────────────────
    def _plain(frag: str) -> str:
        return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', frag)).strip()

    def _wc(frag: str) -> int:
        return len(_plain(frag).split())

    def _strip_marker(text: str) -> str:
        text = _re.sub(r'^\s*(?:[IVXLCDM]+|\d+)\s*[\).:]\s*', '', text, flags=_re.I)
        text = _re.sub(r'^\s*\(\s*(?:[IVXLCDM]+|\d+)\.?\s*\)\s*', '', text, flags=_re.I)
        return text.strip()

    def _extract_count(text: str) -> int:
        """Return announced count only when text matches _EXPLICIT_COUNT_RE."""
        if not _EXPLICIT_COUNT_RE.search(text):
            return 0
        cleaned = _strip_marker(text)
        m = _re.search(
            r'\b(two|three|four|five|six|seven|eight|nine|ten|'
            r'twofold|threefold|fourfold|\d+)\b',
            cleaned, _re.I,
        )
        if not m:
            return 0
        w = m.group(1).lower()
        if w.isdigit():
            return int(w)
        return {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
                'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                'twofold': 2, 'threefold': 3, 'fourfold': 4}.get(w, 0)

    def _allows_attach(plain: str, is_list_item: bool = False) -> bool:
        plain = plain.strip()
        if not plain:
            return False
        if _re.search(r'\bwhereby\b', plain, _re.I):
            return False
        if is_list_item:
            body_wc = len(_strip_marker(plain).split())
            if body_wc > _ANCHOR_LIMIT:
                if not (_EXPLICIT_COUNT_RE.search(plain) or _FORMULA_TAIL_RE.search(plain)):
                    return False
        last = plain.rstrip('\"\'').strip()
        if not last:
            return False
        if last[-1] in ('—', ',', ';', ':'):
            return True
        if last[-1] == '.':
            return bool(_EXPLICIT_COUNT_RE.search(plain) or _FORMULA_TAIL_RE.search(plain))
        return False

    def _add_anchor_class(para_html: str) -> str:
        if 'syllabus-anchor' in para_html:
            return para_html
        if _re.match(r'<p\s+class="([^"]*)"', para_html):
            return _re.sub(
                r'<p\s+class="([^"]*)"',
                lambda mm: f'<p class="{mm.group(1)} syllabus-anchor"',
                para_html, count=1,
            )
        if para_html.startswith('<p>'):
            return '<p class="syllabus-anchor">' + para_html[3:]
        return para_html

    def _absorb(preceding: str, pairs: list, count: int) -> str:
        parts = [((mk or '') + ' ' + ct).strip() for mk, ct in pairs[:count]]
        inline = _re.sub(r'\s+', ' ', ' '.join(parts))
        merged = _re.sub(r'</p>\s*$', ' ' + inline + '</p>', preceding, count=1)
        return _add_anchor_class(merged)

    # ── main loop ─────────────────────────────────────────────────────────────
    paras = html.split('\n')
    out: list[str] = []
    i = 0
    n = len(paras)

    while i < n:
        para = paras[i]
        stripped = para.strip()

        m_item = _LIST_ITEM_RE.match(stripped)
        if not m_item:
            out.append(para)
            i += 1
            continue

        # Collect consecutive list-item run
        run_indices: list[int] = []
        j = i
        while j < n:
            curr = paras[j].strip()
            if not curr:
                j += 1
                continue
            if _LIST_ITEM_RE.match(curr):
                run_indices.append(j)
                j += 1
            else:
                break

        # ── Signal G: single-item ordinal continuation ───────────────────────
        if len(run_indices) == 1:
            pm = _LIST_ITEM_RE.match(stripped)
            mk_plain = _plain(pm.group(2) or '').strip() if pm else ''
            if pm and _ORDINAL_MK_RE.match(mk_plain):
                prev_idx = next(
                    (k for k in range(len(out) - 1, -1, -1) if out[k].strip()), -1
                )
                if prev_idx >= 0 and _HAS_INLINE_ORDINAL_RE.search(_plain(out[prev_idx])):
                    # Ensure the next ordinal is a numerical continuation (Issue 91/107)
                    def _parse_val(marker_text: str) -> int:
                        m = _re.search(r'\d+', marker_text)
                        if m: return int(m.group(0))
                        w = marker_text.lower()
                        if 'first' in w or '1st' in w: return 1
                        if 'second' in w or '2nd' in w or '2dly' in w: return 2
                        if 'third' in w or '3rd' in w or '3dly' in w: return 3
                        if 'fourth' in w or '4th' in w: return 4
                        if 'fifth' in w or '5th' in w: return 5
                        return 0
                    
                    preceding_plain = _plain(out[prev_idx])
                    matches = list(_re.finditer(r'\((?:\d+(?:st|nd|rd|th|ly|dly)?|1st|2nd(?:ly)?|3rd(?:ly)?|4th(?:ly)?)\.?\)', preceding_plain, _re.I))
                    is_continuation = True
                    if matches:
                        last_val = _parse_val(matches[-1].group(0))
                        next_val = _parse_val(mk_plain)
                        if next_val != last_val + 1:
                            is_continuation = False
                    
                    if is_continuation:
                        ct = pm.group(3) or ''
                        out[prev_idx] = _absorb(out[prev_idx], [(pm.group(2) or '', ct)], 1)
                        i = j
                        continue
            out.append(para)
            i += 1
            continue

        if len(run_indices) < 2:
            out.append(para)
            i += 1
            continue

        # ── is_case_2: first list-item ends '—' (nested sub-list anchor) ─────
        is_case_2 = False
        first_plain = _plain(para)
        if first_plain.rstrip('\"\'').strip().endswith('—'):
            is_li = bool(_re.match(r'<p class="(?:list-item|roman-list-item)">', stripped))
            if is_li and _allows_attach(first_plain, is_list_item=True):
                is_case_2 = True

        if is_case_2:
            preceding      = para
            preceding_plain = first_plain
            candidate_idx  = run_indices[1:]
        else:
            prev_idx = next(
                (k for k in range(len(out) - 1, -1, -1) if out[k].strip()), -1
            )
            if prev_idx == -1:
                out.append(para)
                i += 1
                continue
            preceding      = out[prev_idx]
            preceding_plain = _plain(preceding)
            is_prec_li = bool(_re.match(
                r'<p class="(?:list-item|roman-list-item)">', preceding.strip()
            ))
            if not _allows_attach(preceding_plain, is_list_item=is_prec_li):
                out.append(para)
                i += 1
                continue
            candidate_idx = run_indices

        # Build item pairs
        item_pairs: list[tuple[str, str]] = []
        for idx in candidate_idx:
            pm = _LIST_ITEM_RE.match(paras[idx].strip())
            item_pairs.append((pm.group(2) or '', pm.group(3) or ''))

        announced = _extract_count(preceding_plain)

        # ── determine flat prefix length ──────────────────────────────────────
        flat_prefix_len = 0

        for L in range(len(item_pairs), 1, -1):
            sub   = item_pairs[:L]
            if not _is_sequential_sequence(sub):
                continue
            wcs   = [_wc(ct) for _, ct in sub]
            nf    = sub[:-1]      # non-final items

            # Signal F: exact announced count, ≤20 w each
            if announced == L and all(wc <= _SIGNAL_F_CAP for wc in wcs):
                flat_prefix_len = L
                break

            # Signal H: ≥3 items, all end '.', all ≤25 w
            if (L >= 3
                    and all(ct.rstrip('\"\'').strip().endswith('.') for _, ct in sub)
                    and all(wc <= _SIGNAL_H_CAP for wc in wcs)):
                flat_prefix_len = L
                break

            # all_non_final_semi: every non-final item ends ';', non-final ≤20 w
            if (nf
                    and all(ct.rstrip('\"\'').strip().endswith(';') for _, ct in nf)
                    and all(wcs[k] <= _ALL_SEMI_CAP for k in range(len(nf)))):
                flat_prefix_len = L
                break

            # Continuation comma: non-final item ends ',' → final joins
            if nf and any(ct.rstrip('\"\'').strip().endswith(',') for _, ct in nf):
                flat_prefix_len = L
                break

            # Continuation connector: non-final ends 'and'/'or' → final joins
            if nf and any(
                _re.search(r'\b(?:and|or)\s*$', ct.rstrip('\"\'').strip(), _re.I)
                for _, ct in nf
            ):
                flat_prefix_len = L
                break

            # Standard hard cap
            if any(wc > _HARD_CAP for wc in wcs):
                continue

            # Standard signals A/B/C/D
            sig_a = any(ct.rstrip('\"\'').strip().endswith((';', ',')) for _, ct in nf)
            sig_b = any(
                _re.search(r'\b(?:and|or)\s*$', ct.rstrip('\"\'').strip(), _re.I)
                for _, ct in sub
            )
            sig_c = all(wc <= 3 for wc in wcs)
            sig_d = L >= 3 and all(wc <= 7 for wc in wcs)

            if sig_a or sig_b or sig_c or sig_d:
                flat_prefix_len = L
                break

        if flat_prefix_len == 0:
            out.append(para)
            i += 1
            continue

        # ── absorb ───────────────────────────────────────────────────────────
        new_preceding = _absorb(preceding, item_pairs, flat_prefix_len)

        if is_case_2:
            out.append(new_preceding)
        else:
            out[prev_idx] = new_preceding

        # Re-emit remaining expansion items (recurse)
        remaining = [paras[idx] for idx in candidate_idx[flat_prefix_len:]]
        if remaining:
            out.extend(_attach_em_dash_flat_list('\n'.join(remaining)).split('\n'))

        i = j
        continue

    return '\n'.join(out)


def _owen_marker_level(marker_text: str, previous_marker_family: str = None) -> tuple[str, str]:
    """Classify an Owenian structural list marker into a reader level.
    
    Returns (level_class, marker_family).
    """
    marker_text = re.sub(r'<[^>]+>', '', marker_text).strip()
    if not marker_text:
        return 'list-level-1', previous_marker_family or 'other'

    # Strip bold tags and normalize casing
    clean = marker_text.strip('.,:; \t\n\r*')
    clean_upper = clean.upper()

    # 1. Level 3: Ordinals (1st., 2dly., 3dly., [SECONDLY], [3dly.])
    is_digit_ordinal = bool(re.search(r'\d(?:ST|ND|RD|TH|DLY|LY)', clean_upper))
    is_bracketed_word_ordinal = clean_upper.startswith('[') and clean_upper.endswith(']') and any(
        w in clean_upper for w in [
            'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH', 'SEVENTH',
            'EIGHTH', 'NINTH', 'LAST', 'LY'
        ]
    )
    is_local_ordinal = any(clean_upper.startswith(w) for w in ['1ST', '2DLY', '3DLY', '4THLY'])
    
    if is_digit_ordinal or is_bracketed_word_ordinal or is_local_ordinal:
        return 'list-level-3', 'ordinal'

    # 2. Level 2: Bracketed markers (e.g., [1.], [1], [a]) that are NOT word ordinals
    if clean.startswith('[') and clean.endswith(']'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return 'list-level-2', 'arabic_bracket'
        elif len(inner) == 1 and inner.isalpha():
            return 'list-level-2', 'alpha_bracket'
        else:
            return 'list-level-2', 'other_bracket'
    if clean.startswith('[') or re.match(r'^\[\d+\]\.?$', clean):
        return 'list-level-2', 'arabic_bracket'

    # 3. Level 2: Parenthesized markers (1.), (a.) (subordinate to main points)
    if clean.startswith('(') and clean.endswith(')'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return 'list-level-2', 'arabic_paren'
        elif len(inner) == 1 and inner.isalpha():
            return 'list-level-2', 'alpha_paren'
        else:
            return 'list-level-2', 'other_paren'

    if clean.isdigit() or re.match(r'^\d+$', clean):
        return 'list-level-1', 'arabic'
        
    if any(w in clean_upper for w in ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'OBJECTION', 'ANSWER', 'USE', 'SOL']):
        return 'list-level-1', 'word'

    if re.search(r'[IVXLCDM]+\.?\s+\d+', clean):
        return 'list-level-1', 'roman_decimal'

    return 'list-level-1', previous_marker_family or 'other'


def _add_owen_list_level_classes(html: str) -> str:
    """Add modest reader-facing hierarchy classes to remaining block lists,
    dynamically adjusting nesting levels based on count-phrase triggers in parent paragraphs.
    """
    if not html:
        return html

    import re

    # Trigger patterns
    COUNT_TRIGGER_RE = re.compile(
        r'\b(?:two|three|four|five|six|seven|eight|nine|ten|sundry|several|twofold|threefold|fourfold|ensuing|following)\s+'
        r'(?:ways|reasons|things|respects|accounts|causes|parts|points|arguments|properties|instances|ends|acts|observations|propositions|heads)\b',
        re.I
    )
    ENDS_WITH_INTRO_RE = re.compile(r'[:—\-]\s*$', re.I)

    # Helper to check if a block contains a list trigger
    def has_list_trigger(text: str) -> bool:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        return bool(COUNT_TRIGGER_RE.search(clean)) and bool(ENDS_WITH_INTRO_RE.search(clean))

    # Helper to convert Roman to Int
    def roman_to_int(s: str) -> int:
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        val = 0
        prev_val = 0
        for char in reversed(s.upper()):
            curr_val = roman_map.get(char, 0)
            if curr_val == 0:
                return None
            if curr_val >= prev_val:
                val += curr_val
            else:
                val -= curr_val
            prev_val = curr_val
        return val

    # Block regex to split the XHTML safely
    block_re = re.compile(
        r'(<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )

    blocks = []
    last_idx = 0
    for m in block_re.finditer(html):
        inter = html[last_idx:m.start()]
        if inter.strip():
            blocks.append(inter)
        blocks.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:]
    if tail.strip():
        blocks.append(tail)

    output_blocks = []
    active_override_level = None
    previous_family = None

    last_digit_at_level = {1: None, 2: None, 3: None}
    last_family_at_level = {1: None, 2: None, 3: None}

    for block in blocks:
        # Check if it's a list item
        p_match = re.match(r'^<p class="(?P<classes>[^"]*)">(?P<inner>.*?)</p>$', block, re.S)
        if p_match:
            classes_list = p_match.group('classes').split()
            if 'list-item' in classes_list or 'roman-list-item' in classes_list:
                cls = 'roman-list-item' if 'roman-list-item' in classes_list else 'list-item'
                inner = p_match.group('inner')
                marker_match = re.match(r'\s*(<b>[^<]{1,40}</b>)', inner, re.S)
                marker_raw = marker_match.group(1) if marker_match else ''
                
                # Determine base level and family
                if cls == 'roman-list-item':
                    base_level_class = 'list-level-1'
                    family = 'roman'
                else:
                    base_level_class, family = _owen_marker_level(marker_raw, previous_family)
                
                previous_family = family
                
                try:
                    base_level = int(base_level_class.split('-')[-1])
                except ValueError:
                    base_level = 1
                
                # Extract decimal / Roman integer value if available
                clean_marker = re.sub(r'<[^>]+>', '', marker_raw).strip('.,:; \t\n\r*()[]')
                val = None
                if clean_marker.isdigit():
                    val = int(clean_marker)
                elif re.match(r'^[IVXLCDM]+$', clean_marker, re.I):
                    val = roman_to_int(clean_marker)

                # Determine dynamic context-aware level
                assigned_level = base_level

                if val is not None:
                    # 1. Check if it continues Level 1 sequence (resets overrides)
                    if last_digit_at_level[1] is not None and val == last_digit_at_level[1] + 1 and family == last_family_at_level[1]:
                        active_override_level = None
                        assigned_level = 1
                    # 2. Check if it continues Level 2 sequence
                    elif last_digit_at_level[2] is not None and val == last_digit_at_level[2] + 1 and family == last_family_at_level[2]:
                        assigned_level = 2
                    # 3. Check if it continues Level 3 sequence
                    elif last_digit_at_level[3] is not None and val == last_digit_at_level[3] + 1 and (family == last_family_at_level[3] or active_override_level == 3):
                        assigned_level = 3
                    # 4. Check if it is starting a new nested sequence (val == 1)
                    elif val == 1:
                        if active_override_level is not None:
                            assigned_level = active_override_level
                        else:
                            assigned_level = base_level
                    # 5. Fallback for non-sequential but numeric items
                    else:
                        if active_override_level is not None:
                            assigned_level = max(base_level, active_override_level)
                        else:
                            assigned_level = base_level
                else:
                    # Non-numeric items (e.g. scholastic anchors, ordinals)
                    if active_override_level is not None:
                        assigned_level = max(base_level, active_override_level)
                    else:
                        assigned_level = base_level

                # Update sequence trackers
                if val is not None:
                    last_digit_at_level[assigned_level] = val
                    last_family_at_level[assigned_level] = family

                # Reconstruct the list item paragraph preserving other classes (like syllabus-anchor)
                other_classes = [c for c in classes_list if c not in ('list-item', 'roman-list-item') and not c.startswith('list-level-')]
                new_classes = [cls, f'list-level-{assigned_level}'] + other_classes
                block = f'<p class="{" ".join(new_classes)}">{inner}</p>'
                
                # Check if this list item itself acts as an introducing trigger for a sub-list
                if has_list_trigger(inner):
                    active_override_level = min(3, assigned_level + 1)
                
                output_blocks.append(block)
            else:
                output_blocks.append(block)
        elif re.match(r'^<h[1-6]\b', block):
            output_blocks.append(block)
            active_override_level = None
        else:
            output_blocks.append(block)
            
            # Check if it acts as a list trigger
            if has_list_trigger(block):
                active_override_level = 2
            else:
                # Non-list paragraph with no trigger resets overrides
                active_override_level = None

    return "".join(output_blocks)


def _nest_owen_list_hierarchies(html: str) -> str:
    """Reconstruct flat list-item paragraphs into a nested <div> tree.
    
    This function processes top-level block elements (paragraphs, blockquotes, headings)
    and wraps them in <div class="owen-branch owen-level-X"> containers based on their
    list-level markings. Continuation prose and quotes automatically nest inside the
    active leaf container.
    """
    import re
    block_re = re.compile(
        r'(<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<div\b[^>]*>.*?</div>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )
    
    blocks = []
    last_idx = 0
    for m in block_re.finditer(html):
        inter = html[last_idx:m.start()].strip()
        if inter:
            blocks.append(inter)
        blocks.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:].strip()
    if tail:
        blocks.append(tail)
        
    if not blocks:
        return html
        
    output_parts = []
    active_levels = []  # Stack of currently open levels (e.g. [1, 2])
    
    def close_levels_down_to(target_level: int):
        """Close all open divs deeper than or equal to target_level."""
        while active_levels and active_levels[-1] >= target_level:
            output_parts.append("</div>")
            active_levels.pop()

    for block in blocks:
        explicit_level = None
        
        p_match = re.match(r'^<p\b([^>]*)>', block)
        if p_match:
            attrs = p_match.group(1)
            if 'list-level-3' in attrs:
                explicit_level = 3
            elif 'list-level-2' in attrs:
                explicit_level = 2
            elif 'list-level-1' in attrs:
                explicit_level = 1
            elif 'signature' in attrs or 'front-matter' in attrs:
                explicit_level = 0
        elif re.match(r'^<h[1-6]\b', block):
            explicit_level = 0
        elif re.match(r'^<aside\b', block):
            explicit_level = 0
            
        if explicit_level is not None:
            if explicit_level == 0:
                close_levels_down_to(1)
                output_parts.append(block)
            else:
                current_active = active_levels[-1] if active_levels else 0
                
                if explicit_level > current_active:
                    for level in range(current_active + 1, explicit_level + 1):
                        output_parts.append(f'<div class="owen-branch owen-level-{level}">')
                        active_levels.append(level)
                    output_parts.append(block)
                    
                elif explicit_level == current_active:
                    output_parts.append("</div>")
                    active_levels.pop()
                    output_parts.append(f'<div class="owen-branch owen-level-{explicit_level}">')
                    active_levels.append(explicit_level)
                    output_parts.append(block)
                    
                else:  # explicit_level < current_active
                    close_levels_down_to(explicit_level)
                    output_parts.append(f'<div class="owen-branch owen-level-{explicit_level}">')
                    active_levels.append(explicit_level)
                    output_parts.append(block)
        else:
            output_parts.append(block)
            
    close_levels_down_to(1)
    
    return "\n".join(output_parts)



# ---------------------------------------------------------------------------
# Issue #49 — coalesce consecutive signature paragraphs
# ---------------------------------------------------------------------------
def _coalesce_adjacent_signatures(html: str) -> str:
    """Merge consecutive <p class="signature"> elements into one, joined by <br/>."""
    if not html:
        return html

    import re as _re

    paras = html.split('\n')
    out: list[str] = []
    i = 0
    n = len(paras)

    while i < n:
        para = paras[i]
        stripped = para.strip()

        m = _re.match(r'<p\s+class="signature">(.*?)</p>', stripped)
        if not m:
            out.append(para)
            i += 1
            continue

        sig_contents = [m.group(1).strip()]
        j = i + 1
        while j < n:
            curr = paras[j].strip()
            if not curr:
                j += 1
                continue
            m_curr = _re.match(r'<p\s+class="signature">(.*?)</p>', curr)
            if m_curr:
                sig_contents.append(m_curr.group(1).strip())
                j += 1
            else:
                break

        if len(sig_contents) > 1:
            merged_content = '<br/>'.join(sig_contents)
            out.append(f'<p class="signature">{merged_content}</p>')
        else:
            out.append(para)

        i = j

    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Treatise title page override helper: preserve foreign script (Greek/Hebrew) epigraphs
# ---------------------------------------------------------------------------
def _foreign_fragments_in_section(html: str) -> list[str]:
    """Extract elements containing Greek or Hebrew characters from an HTML section."""
    if not html:
        return []

    import re as _re

    # Find tags: blockquote, p, span, h1-6
    pattern = r'(<(blockquote|p|span|h[1-6])\b[^>]*>.*?</\2>)'
    matches = _re.findall(pattern, html, _re.S | _re.I)
    
    fragments = []
    for match_tuple in matches:
        full_tag = match_tuple[0]
        # Strip HTML tags to check only the text content
        plain_text = _re.sub(r'<[^>]+>', '', full_tag)
        # Check for Greek range (\u0370-\u03FF, \u1F00-\u1FFF) or Hebrew range (\u0590-\u05FF)
        if _re.search(r'[\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]', plain_text):
            fragments.append(full_tag)
            
    return fragments


def _merge_titlepage_override(override: str, fragments: list[str]) -> str:
    """Merge missing Greek/Hebrew fragments into the override section before the closing </section>."""
    if not override or not fragments:
        return override

    import re as _re

    for frag in fragments:
        plain_frag = _re.sub(r'<[^>]+>', '', frag).strip()
        if not plain_frag:
            continue
        
        # If this plain text is already present in the override, skip it
        if plain_frag in override:
            continue
            
        # Append before the closing </section>
        override = _re.sub(
            r'(</section>\s*$)',
            '\n' + frag + '\n' + r'\1',
            override,
            flags=_re.I
        )
        
    return override


# ---------------------------------------------------------------------------
# Issue 19: Inline list merging
# ---------------------------------------------------------------------------
_LIST_ITEM_CONTENT_RE = re.compile(
    r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
    re.S,
)


def _merge_short_inline_lists(html: str) -> str:
    """Merge consecutive list items into continuous prose when appropriate.

    Two complementary rules:

    Rule A — short-item run (Issue 13 / Issue 19.b):
      If every item in the entire run has very short plain-text content
      (≤ _SHORT_ITEM_WORD_LIMIT words after stripping the bold marker),
      the whole run is a "pseudo-list" — really an inline enumeration —
      and is merged unconditionally into a single prose paragraph,
      regardless of terminal punctuation.
      Examples: "1. Complacency; 2. Permanency."
                "1. Illumination; 2. Conviction; 3. Reformation."

    Rule B — semicolon sub-run:
      An item whose content ends with ';' or ',' is accumulated into the
      current sub-run.  When a terminating item (ends with anything else) is
      reached, the accumulated sub-run (≥ 2 items) is merged.  Items that
      stand alone remain on their own line.

      Handles heterogeneous runs naturally: a long 'Secondly,…' paragraph
      ending with '.' stays separate while short ';' items are merged.
    """
    import re as _re

    _SHORT_ITEM_WORD_LIMIT = 4   # items with ≤ this many words are "not really list items"

    def _plain_text(html_frag: str) -> str:
        return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', html_frag)).strip()

    def _content_word_count(plain: str) -> int:
        return len(plain.split())

    def _is_non_terminating_item(html_frag: str) -> bool:
        plain = _plain_text(html_frag).rstrip()
        if plain.endswith((';', ',')):
            return True
        if _re.search(r'\b(and|or)\b\s*$', plain, _re.I):
            return True
        return False

    # Split on both list-item and roman-list-item paragraphs
    parts = _re.split(r'(<p class="(?:list-item|roman-list-item)">.*?</p>)', html, flags=_re.S)

    def _item_class(frag: str) -> str:
        """Return the CSS class of a list-item paragraph fragment."""
        m2 = _re.match(r'<p class="(list-item|roman-list-item)">', frag)
        return m2.group(1) if m2 else 'list-item'

    out = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if not _re.match(r'<p class="(?:list-item|roman-list-item)">', token):
            out.append(token)
            i += 1
            continue

        # Collect a run of consecutive list-item paragraphs of the SAME class
        run_cls = _item_class(token)
        run = [token]
        j = i + 1
        while j < len(parts):
            if parts[j].strip() == '':
                j += 1
                continue
            if _re.match(rf'<p class="{run_cls}">', parts[j]):
                run.append(parts[j])
                j += 1
            else:
                break

        # Extract (marker, content) pairs — bold group is optional
        item_contents = []
        for item in run:
            m = _LIST_ITEM_CONTENT_RE.match(item)
            if m:
                # group(1)=class, group(2)=optional bold marker, group(3)=content
                item_contents.append((m.group(2) or '', m.group(3)))
            else:
                # Fallback: strip outer <p> tags to get inner HTML
                inner = _re.sub(
                    r'^<p class="(?:list-item|roman-list-item)">(.*?)</p>$',
                    r'\1', item, flags=_re.S,
                )
                item_contents.append(('', inner))

        # ── Rule A: all items are very short AND at least one non-final item
        #    ends with ';' or ',' or a connector → merge the entire run.
        #
        #    The semicolon/comma guard prevents period-terminated standalone
        #    statements ("God is sovereign. God is holy.") from merging, while
        #    still catching short pseudo-lists ("1. Complacency; 2. Permanency.")
        #    that Rule B would also handle.
        if len(item_contents) >= 2:
            all_short = all(
                _content_word_count(_plain_text(ct)) <= _SHORT_ITEM_WORD_LIMIT
                for _mk, ct in item_contents
            )
            any_non_final_has_semi = any(
                _is_non_terminating_item(ct)
                for _mk, ct in item_contents[:-1]
            )
            if all_short and any_non_final_has_semi:
                merged = ' '.join(mk2 + ct2 for mk2, ct2 in item_contents)
                out.append(f'<p class="{run_cls}">{merged}</p>')
                i = j
                continue

        # ── Rule B: semicolon/comma sub-run accumulation ──────────────────────
        run_out = []
        current_subrun = []

        for mk, ct in item_contents:
            current_subrun.append((mk, ct))
            if not _is_non_terminating_item(ct):
                # Terminating item — flush the accumulated sub-run
                if len(current_subrun) >= 2:
                    merged = ' '.join(mk2 + ct2 for mk2, ct2 in current_subrun)
                    run_out.append(f'<p class="{run_cls}">{merged}</p>')
                else:
                    mk2, ct2 = current_subrun[0]
                    run_out.append(f'<p class="{run_cls}">{mk2}{ct2}</p>')
                current_subrun = []

        # Flush any remaining items (run where every item ends with ; or ,)
        if current_subrun:
            if len(current_subrun) >= 2:
                merged = ' '.join(mk2 + ct2 for mk2, ct2 in current_subrun)
                run_out.append(f'<p class="{run_cls}">{merged}</p>')
            else:
                mk2, ct2 = current_subrun[0]
                run_out.append(f'<p class="{run_cls}">{mk2}{ct2}</p>')

        out.append('\n'.join(run_out))
        i = j

    return ''.join(out)


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


_TITLE_CONNECTORS = {
    'OR', 'OF', 'ON', 'IN', 'WITH', 'ALSO', 'AS ALSO,', 'AND', 'WHEREIN',
    'ARE', 'BY',
}


def _polish_treatise_title_page_html(html: str, seen_footnote_refs=None) -> str:
    """Normalize pre-rendered treatise title pages into one elegant title sheet."""
    if not re.search(r'<section\b[^>]*class="[^"]*\btreatise-title-page\b', html):
        return html

    if seen_footnote_refs is not None:
        def footnote_marker_repl(match):
            fn_num = match.group(1)
            if fn_num in seen_footnote_refs:
                return ''
            seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'
        html = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, html)

    # Fix "title-line -major" -> "title-line-major", handles -minor, -small, -medium too
    html = re.sub(r'class="title-line\s+-(\w+)"', r'class="title-line-\1"', html)
    
    # Also handle the case where it was already partially fixed or has multiple classes
    html = re.sub(r'class="title-line\s+title-line-(\w+)"', r'class="title-line-\1"', html)

    html = re.sub(
        r'<p class="title-line-medium">\s*(' + '|'.join(re.escape(item) for item in sorted(_TITLE_CONNECTORS, key=len, reverse=True)) + r')\s*</p>',
        lambda m: f'<p class="title-connector">{m.group(1)}</p>',
        html,
        flags=re.I,
    )

    def _connector_repl(match):
        attrs = match.group(1)
        if 'greek-title' in attrs:
            return f'<p class="greek-title">{match.group(2).strip()}</p>'
        text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
        if text.upper() not in _TITLE_CONNECTORS:
            return match.group(0)
        return f'<p class="title-connector">{match.group(2).strip()}</p>'

    html = re.sub(r'<h2([^>]*)>\s*(.*?)\s*</h2>', _connector_repl, html, flags=re.I | re.S)
    html = re.sub(
        r'<h2([^>]*)>\s*(.*?)\s*</h2>',
        lambda m: f'<p class="title-line title-line-medium">{m.group(2).strip()}</p>',
        html,
        flags=re.I | re.S,
    )
    html = re.sub(
        r'<h1([^>]*)>\s*(.*?)\s*</h1>',
        lambda m: f'<p class="title-line title-line-major">{m.group(2).strip()}</p>',
        html,
        flags=re.I | re.S,
    )

    if seen_footnote_refs is not None:
        html = _restore_footnote_placeholders(html)

    return html


def _polish_volume_title_page_html(html: str, vol_num: int, config: dict) -> str:
    """Ensure generated/extracted volume title pages carry edition metadata."""
    if 'class="title-page"' not in html:
        return html
    publisher = _escape_xml(config.get('publisher') or 'Eduardus Ekofius')
    editors = config.get('editors') or ['William H. Goold']
    editor = _escape_xml(editors[0])
    subtitle = _escape_xml(VOLUME_SUBTITLES.get(vol_num, ''))
    if re.search(r'THE\s+WORKS\s+OF(?:<br\s*/?>|\s)+JOHN\s+OWEN', html, re.I):
        subtitle_html = f'<p class="title-volume-subtitle">{subtitle}</p>' if subtitle else ''
        return f'''<section class="title-page volume-title-page" epub:type="titlepage">
<div class="emblem-container">
<img class="title-emblem-seal" src="images/emblem_seal.png" alt="Emblem Seal of Dr. John Owen"/>
</div>
<p class="title-work-top">The Works of</p>
<h1 class="title-author-main">John Owen</h1>
<div class="title-divider-double" aria-hidden="true"></div>
<p class="title-volume-number">Volume {vol_num}</p>
{subtitle_html}
<div class="title-meta-divider" aria-hidden="true"></div>
<div class="title-meta">
<p class="editor">Edited by {editor}</p>
<p class="publisher-brand">{publisher}</p>
<p class="publisher-loc">Parentis-en-Born</p>
<p class="edition-year">MMXXVI</p>
</div>
</section>'''
    meta_bits = []
    if 'Edited by' not in html and 'EDITED BY' not in html:
        meta_bits.append(f'<p class="editor">Edited by {editor}</p>')
    if publisher not in html:
        meta_bits.append(f'<p class="publisher-brand">{publisher}</p>')
        meta_bits.append('<p class="publisher-loc">Parentis-en-Born</p>')
    if '2026' not in html and 'MMXXVI' not in html:
        meta_bits.append('<p class="edition-year">MMXXVI</p>')
    if not meta_bits:
        return html
    meta = '<div class="title-meta">' + ''.join(meta_bits) + '</div>'
    return re.sub(r'</section>\s*$', meta + '</section>', html, flags=re.S)


def _polish_contents_page_html(html: str) -> str:
    """Normalize extracted contents pages into a consistent, reader-friendly TOC."""
    if 'epub:type="toc"' not in html:
        return html

    # Translate known legacy Beta Code in TOC to premium Greek Unicode
    html = html.replace('Qemoci&gt;av Aujtexousiastikh~v SPECIMEN', '<span lang="el" xml:lang="el">Θεομαχίας Αὐτεξουσιαστικῆς</span> Specimen')
    html = html.replace('QEOMACIA ATTEXOUSIASTIKH', '<span lang="el" xml:lang="el">ΘΕΟΜΑΧΙΑ ΑΥΤΕΞΟΥΣΙΑΣΤΙΚΗ</span>')

    html = re.sub(r'<section([^>]*)epub:type="toc"([^>]*)>', '<section class="contents-page" epub:type="toc">', html, count=1)
    seen_volume_title = False

    def _heading_repl(match):
        nonlocal seen_volume_title
        text_html = match.group(1).strip()
        plain = re.sub(r'<br\s*/?>', ' ', text_html, flags=re.I)
        plain = re.sub(r'<[^>]+>', '', plain).strip()
        plain_upper = plain.upper()
        if re.match(r'^CONTENTS\s+OF\s+VOL(?:UME)?\.?\s*\d+', plain_upper) or plain_upper == 'CONTENTS':
            seen_volume_title = True
            return f'<h1 class="contents-volume-title">{text_html}</h1>'
        if re.fullmatch(r'(?:PREFATORY NOTE|PREFACE|PREFACE TO THE READER|ORIGINAL PREFACE|GENERAL PREFACE|TO THE READER|NOTE TO THE READER|ADVERTISEMENT)(?:\s+(?:BY THE EDITOR|TO THE READER|BY D\.?\s+BURGESS))?(?:\s+(?:PREFATORY NOTE|PREFACE|PREFACE TO THE READER|ORIGINAL PREFACE|GENERAL PREFACE|TO THE READER|NOTE TO THE READER|ADVERTISEMENT)(?:\s+(?:BY THE EDITOR|TO THE READER|BY D\.?\s+BURGESS))?)*', plain_upper):
            return f'<p class="contents-frontmatter-line">{text_html}</p>'
        cls = 'contents-treatise-title' if seen_volume_title else 'contents-section-title'
        return f'<h2 class="{cls}">{text_html}</h2>'

    html = re.sub(r'<h[23][^>]*>\s*(.*?)\s*</h[23]>', _heading_repl, html, flags=re.I | re.S)
    html = re.sub(r'<p class="ContentsItem">', '<p class="contents-item">', html)
    html = re.sub(r'<span class="ContentsDescWrap">', '<span class="contents-desc-wrap">', html)

    # Normalize contents-desc starting with ordinals or Roman numerals to contents-item
    def _desc_to_item_repl(m):
        content = m.group(1)
        clean_content = re.sub(r'<[^>]+>', '', content).strip()
        is_ordinal_or_roman = bool(re.match(
            r'^(?:(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)(?:ly)?,?|'
            r'[IVXLCDM]+(?:\s+|\.|$))',
            clean_content,
            re.I
        ))
        if is_ordinal_or_roman:
            return f'<p class="contents-item">{content}</p>'
        return m.group(0)

    html = re.sub(r'<p class="contents-desc">\s*(.*?)\s*</p>', _desc_to_item_repl, html, flags=re.I | re.S)

    item_re = re.compile(r'<p class="contents-item">\s*(.*?)\s*</p>', re.I | re.S)
    rebuilt = []
    cursor = 0
    pending_item = None

    def _plain_contents(inner: str) -> str:
        inner = re.sub(r'<br\s*/?>', ' ', inner, flags=re.I)
        inner = re.sub(r'<[^>]+>', '', inner)
        inner = _html_unescape(inner)
        inner = re.sub(r'\s+', ' ', inner).strip()
        inner = re.sub(r'\b(Chapter|Part|Digression)\s+([0-9IVXLCDM]+)\s+\.', r'\1 \2.', inner, flags=re.I)
        inner = re.sub(r'\b(Chapter|Part|Digression)\s+([0-9IVXLCDM]+)(?=\s+[A-Z])', r'\1 \2.', inner, flags=re.I)
        inner = re.sub(r'\b(\d+)\.\s*—\s*', r'\1. — ', inner)
        inner = re.sub(r'\s+([,.;:])', r'\1', inner)
        return inner

    def _entry_starts(text: str):
        return list(re.finditer(r'(?<!\w)(?:Part|Chapter|Digression)\s+[0-9IVXLCDM]+\.?', text, re.I))

    def _split_entries(text: str) -> list[str]:
        starts = _entry_starts(text)
        if not starts:
            return [text] if text else []
        entries = []
        if starts[0].start() > 0 and text[:starts[0].start()].strip():
            entries.append(text[:starts[0].start()].strip())
        for idx, start in enumerate(starts):
            end = starts[idx + 1].start() if idx + 1 < len(starts) else len(text)
            entries.append(text[start.start():end].strip())
        return [entry for entry in entries if entry]

    def _render_contents_entry(text: str) -> str:
        part = re.fullmatch(r'(Part\s+[0-9IVXLCDM]+\.?)', text, re.I)
        if part:
            label = re.sub(r'\s+\.', '.', part.group(1))
            return f'<h2 class="contents-part-title">{_html_escape(label)}</h2>'

        match = re.match(
            r'(?P<label>'
            r'(?:Chapter|Digression)\s+[0-9IVXLCDM]+\.?|'
            r'[0-9]+\.?\s*—|'
            r'(?:First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)(?:ly)?,?|'
            r'[IVXLCDM]+\.?'
            r')\s*(?P<desc>.*)$',
            text,
            re.I | re.S,
        )
        if match:
            label = re.sub(r'\s+\.', '.', match.group('label').strip())
            label = re.sub(r'\s*—\s*$', ' —', label)
            desc = match.group('desc').strip()
            if desc.startswith('—'):
                desc = desc[1:].strip()
            desc = re.sub(r'\s+', ' ', desc)
            desc = clean_greek_text(desc)
            return (
                f'<p class="contents-item"><span class="contents-label">'
                f'{_html_escape(label)}</span>'
                f'{(" " + tag_unicode_ranges(_html_escape(desc))) if desc else ""}</p>'
            )

        if text.upper() == text and len(re.findall(r'[A-Z]', text)) >= 12:
            return f'<h2 class="contents-treatise-title">{tag_unicode_ranges(_html_escape(text))}</h2>'

        return f'<p class="contents-item">{tag_unicode_ranges(_html_escape(text))}</p>'

    def _flush_pending():
        nonlocal pending_item
        if pending_item is None:
            return ''
        rendered = _render_contents_entry(pending_item)
        pending_item = None
        return rendered

    for match in item_re.finditer(html):
        pending_str = ''
        if re.search(r'<h[1-6]\b', html[cursor:match.start()], re.I):
            pending_str = _flush_pending()
        if pending_str:
            rebuilt.append(pending_str)
        rebuilt.append(html[cursor:match.start()])
        text = _plain_contents(match.group(1))
        entries = _split_entries(text)
        if not entries:
            cursor = match.end()
            continue

        rendered_here = []
        for entry in entries:
            if re.fullmatch(r'Part\s+[0-9IVXLCDM]+\.?', entry, re.I):
                rendered_here.append(_flush_pending())
                rendered_here.append(_render_contents_entry(entry))
                continue
            if _entry_starts(entry):
                rendered_here.append(_flush_pending())
                pending_item = entry
                continue
            if pending_item is not None and re.match(r'^[a-z(]', entry):
                pending_item = pending_item.rstrip() + ' ' + entry
                continue
            rendered_here.append(_flush_pending())
            pending_item = entry
        rebuilt.append(''.join(part for part in rendered_here if part))
        cursor = match.end()

    rebuilt.append(_flush_pending())
    rebuilt.append(html[cursor:])
    return ''.join(rebuilt)


def _polish_analysis_html(html: str) -> str:
    """Keep front-matter analysis outlines compact instead of heading-heavy."""
    if not html:
        return html
    return re.sub(
        r'<h4 class="roman-subheading">(.*?)</h4>',
        r'<p class="roman-list-item">\1</p>',
        html,
        flags=re.I | re.S,
    )


def _apply_premium_signatures(html: str, ch_title: str) -> str:
    """Detect signature paragraphs in prefaces/introductions and format them as premium signature blocks."""
    if not html:
        return html
        
    def replacer(match):
        p_html = match.group(0)
        p_content = match.group(1).strip()
        
        # Skip if already part of an epub-signature or pre-formatted signature class
        if 'class="signature-' in p_html or 'epub-signature' in p_html:
            return p_html
            
        parsed = parse_signature_paragraph(p_content)
        if parsed:
            return format_signature_html(parsed)
        return p_html
        
    def parse_signature_paragraph(content):
        # Strip HTML tags and markdown symbols to look for a signature name
        cleaned = re.sub(r'<[^>]+>', '', content).strip()
        cleaned = re.sub(r'[\*_]+', '', cleaned).strip()
        
        name_patterns = [
            r"\bJOHN\s+OWEN\b", r"\bJohn\s+Owen\b", r"\bJ\.\s*O\.", 
            r"\bWILLIAM\s+H\.\s+GOOLD\b", r"\bWilliam\s+H\.\s+Goold\b", r"\bW\.\s*H\.\s*G\.",
            r"\bSir\s+John\s+Hartopp\b", r"\bMrs\s+Cooke\b", r"\bDANIEL\s+BURGESS\b"
        ]
        
        matched_name = None
        for pattern in name_patterns:
            m = re.search(pattern, cleaned, re.I)
            if m:
                matched_name = m.group(0)
                break
                
        if not matched_name:
            return None
            
        name_plain = matched_name.strip()
        
        # Find where it occurs in the plain text
        m = re.search(re.escape(name_plain), cleaned)
        start_idx, end_idx = m.start(), m.end()
        
        # ── Strict Signature Criteria ─────────────────────────────
        # A paragraph is a signature ONLY if:
        # 1. It is short (under 200 characters total).
        # 2. OR, the name is near the very end of a longer paragraph (within the last 120 characters).
        total_len = len(cleaned)
        dist_from_end = total_len - start_idx
        
        is_short = total_len < 200
        is_near_end = dist_from_end <= 120
        
        if not (is_short or is_near_end):
            return None  # Standard body prose mentioning the name
            
        prefix = cleaned[:start_idx].strip()
        suffix = cleaned[end_idx:].strip()
        
        def clean_block(t):
            t = re.sub(r'^[\s,.\—\-_—\-]+|[\s,.\—\-_—\-]+$', '', t)
            t = t.strip()
            return t
            
        intro = clean_block(prefix)
        date_loc = clean_block(suffix)
        body_text = ""
        
        split_patterns = [
            r"\bYour\s+(?:devoted|humble|humblest|obedient|loving)?\s*Servant\b",
            r"\bSo\s+prays\b",
            r"\bunworthy\s+author\b",
            r"\bloving\s+brother\b",
            r"\bYour\s+Excellency's\s+Most\s+humble\s+and\s+devoted\s*Servant\b"
        ]
        
        found_split_idx = -1
        for sp in split_patterns:
            m_sp = re.search(sp, intro, re.I)
            if m_sp:
                if found_split_idx == -1 or m_sp.start() > found_split_idx:
                    found_split_idx = m_sp.start()
                    
        # If it's a long paragraph and we didn't find an explicit valediction split,
        # reject it to prevent body text false positives
        if total_len >= 200 and found_split_idx == -1:
            return None
            
        # If it is a shorter paragraph but:
        # - Has no valediction split
        # - Has no date/location
        # - The text before the name is a long sentence (> 20 characters)
        # Reject it as it's a standard sentence (e.g., "...preached by Dr John Owen.")
        if found_split_idx == -1 and not date_loc and len(intro) > 20:
            return None
            
        if found_split_idx != -1:
            body_text = intro[:found_split_idx].strip()
            intro = intro[found_split_idx:].strip()
            body_text = re.sub(r'[\s,.\—\-_—\-]+$', '', body_text).strip()
            intro = re.sub(r'^[\s,.\—\-_—\-]+', '', intro).strip()
            
        name = name_plain
        # Normalize name casing
        if name.lower() in ("john owen", "john owen."):
            name = "John Owen"
        elif name.lower() in ("j.o.", "j. o.", "j.o", "j. o"):
            name = "J.O."
        elif name.lower() in ("william h. goold", "william h. goold."):
            name = "William H. Goold"
            
        return {
            "body_text": body_text,
            "intro": intro,
            "name": name,
            "date_loc": date_loc
        }

    def format_signature_html(sig):
        parts = []
        if sig["body_text"]:
            parts.append(f'<p class="front-matter-prose">{sig["body_text"]}</p>')
        parts.append('<div class="epub-signature">')
        if sig["intro"]:
            parts.append(f'  <p class="signature-intro">{sig["intro"]}</p>')
        parts.append(f'  <p class="signature-name">{sig["name"]}</p>')
        if sig["date_loc"]:
            parts.append(f'  <p class="signature-date">{sig["date_loc"]}</p>')
        parts.append('</div>')
        return "\n".join(parts)
        
    return re.sub(r'<p\b[^>]*>(.*?)</p>', replacer, html, flags=re.I | re.S)


def _apply_premium_chapter_endings(html: str) -> str:
    """Detect 'END', 'THE END', or 'END OF PART...' at the end of chapters and format them as distinct, centered bold markers."""
    if not html:
        return html
        
    end_pattern = re.compile(
        r'(?:,\s*|\.\s*|;\s*|\s+)?'
        r'(?:<[^>]+>|[\*_]|\s)*'
        r'\b(THE\s+END|END\s+OF\s+(?:THE\s+)?(?:(?:PART|BOOK|VOLUME|TREATISE)\s+(?:FIRST|SECOND|THIRD|FOURTH|V\w+|[IVXLCDM\d\s]+)|(?:FIRST|SECOND|THIRD|FOURTH|V\w+|[IVXLCDM\d\s]+)\s*(?:PART|BOOK|VOLUME|TREATISE)|PART|BOOK|VOLUME|TREATISE)|END)\b'
        r'(?:<[^>]+>|[\*_]|\s|[,.\—\-_—\-])*$',
        re.I
    )

    def replacer(match):
        p_html = match.group(0)
        p_attrs = match.group(1)
        p_content = match.group(2).strip()
        
        m_end = end_pattern.search(p_content)
        if m_end:
            matched_txt = m_end.group(1)
            
            is_uppercase = matched_txt.isupper()
            has_formatting = '<' in p_content[m_end.start():] or '*' in p_content[m_end.start():] or '_' in p_content[m_end.start():]
            is_standalone = m_end.start() == 0 or p_content[:m_end.start()].strip() == ""
            
            if not (is_uppercase or has_formatting or is_standalone):
                return p_html
                
            prefix = p_content[:m_end.start()].strip()
            prefix = re.sub(r'[\s,.\—\-_—\-]+$', '', prefix).strip()
            
            clean_txt = re.sub(r'<[^>]+>', '', matched_txt).strip()
            clean_txt = re.sub(r'[\*_]+', '', clean_txt).strip()
            clean_txt = re.sub(r'[^a-zA-Z\d\s]', '', clean_txt).strip()
            formatted_marker = f'<p class="chapter-end-marker"><b>{clean_txt.upper()}.</b></p>'
            
            if prefix:
                return f'<p{p_attrs}>{prefix}.</p>\n{formatted_marker}'
            else:
                return formatted_marker
                
        return p_html

    return re.sub(r'<p(\b[^>]*)>(.*?)</p>', replacer, html, flags=re.I | re.S)


def _apply_premium_salutations(html: str) -> str:
    """Detect 'Christian Reader,', 'To the Christian Reader,', etc. and format them as elegant left-aligned salutations."""
    if not html:
        return html
        
    salutation_pattern = re.compile(
        r'<(p|h[1-6])(\b[^>]*)>(?:<[^>]+>)*\s*'
        r'\b((?:To\s+the\s+)?(?:Christian\s+)?Reader\b\s*[,.\—\-_—\-]*)\s*'
        r'(?:<[^>]+>)*\s*</\1>',
        re.I
    )

    def replacer(match):
        p_html = match.group(0)
        p_text = match.group(3).strip()
        
        if len(p_text) > 60:
            return p_html
            
        return f'<p class="prefatory-salutation">{p_text}</p>'

    return salutation_pattern.sub(replacer, html)


def _looks_like_summary_body_start(text: str) -> bool:
    """Detect the first real body paragraph after a chapter summary."""
    if not text:
        return False
    plain = re.sub(r'\*\*(.+?)\*\*', r'\1', text).strip()
    plain = re.sub(r'\s+', ' ', plain)
    # Owen chapters commonly begin with a drop-cap all-caps word followed by
    # ordinary prose.  Keep this strict so all-caps summary fragments survive.
    if re.match(r'^(?:THE|WE|I|THIS|THAT|THERE|BEING|HAVING)\b\s+[a-zA-Z]', plain):
        return True
    # Some body sections begin with an outline word followed by the all-caps
    # drop word from the source page: "Secondly, THE human nature..."
    if re.match(
        r'^(?:First|Firstly|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly),?\s+THE\b',
        plain,
        re.I,
    ):
        return True
    return False


def _looks_like_summary_continuation(text: str) -> bool:
    """Return True for summary fragments that continue after a [[SUMMARY]] tag."""
    if not text:
        return False
    plain = re.sub(r'\*\*(.+?)\*\*', r'\1', text).strip()
    if not plain or _looks_like_summary_body_start(plain):
        return False
    if plain.startswith(('—', '–', '-')):
        # Explicit continuation marker — synopsis fragments that overflow onto
        # the next PDF page always begin with an em/en-dash in Owen.
        return True
    if re.match(r'^[\u0370-\u03FF\u1F00-\u1FFF]', plain):
        return True
    if STRUCTURAL_START_RE.match(plain):
        return not bool(
            _roman_head_match(plain)
            and len(re.findall(r'\w+', (_roman_head_match(plain).group('rest') or ''))) >= 8
        )
    # Long synopsis continuations often contain em-dash-separated clauses but
    # are not outline/body paragraphs yet.  Require mostly uppercase — Owen
    # synopses are all-caps; mixed-case body prose with em-dashes must not be
    # absorbed (e.g. "Our blessed Savior — as he was usually...").
    if '—' in plain:
        _letters = [c for c in plain if c.isalpha()]
        _upper_ratio = (
            sum(1 for c in _letters if c.isupper()) / len(_letters)
            if _letters else 0
        )
        return len(re.findall(r'\w+', plain)) >= 8 and _upper_ratio >= 0.65
    return False


def _prepare_analysis_raw_text(raw_text: str) -> str:
    """Normalize Analysis chapters into a stable outline before rendering.

    The AGES PDFs often flatten front-matter analysis pages into prose. This
    keeps the fix shared across volumes instead of relying on v2-only JSON
    rewrites.
    """
    if not raw_text:
        return raw_text

    text = raw_text
    text = re.sub(r'\*\*(Part\s+[IVXLCDM]+)\*\*\s*\.', r'[[PART]] \1.', text, flags=re.I)
    text = re.sub(r'\*\*(Part\s+[IVXLCDM]+\.)\*\*', r'[[PART]] \1', text, flags=re.I)
    text = re.sub(r'(?m)^(?!\[\[PART\]\]\s*)(Part\s+[IVXLCDM]+\.?\s*[—\-])', r'[[PART]] \1', text, flags=re.I)
    text = re.sub(r'(?<!\n)(\s+)(\[\[PART\]\]\s*Part\s+[IVXLCDM]+\.?)', r'\n\n\2', text, flags=re.I)
    text = re.sub(
        r'(?m)^(?!\[\[)([IVXLCDM]{1,8}\.\s+(?:Communion|It\s+is\s+shown|and\s+practical|'
        r'The\s+foundation|His\s+gracious|The\s+elements|The\s+effects|General\s+inferences)\b)',
        r'[[ROMAN_HEAD]] \1',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'([,;])\s+([IVXLCDM]{1,8}\.\s+(?:Communion|It\s+is\s+shown|and\s+practical)\b)',
        r'\1\n\n[[ROMAN_HEAD]] \2',
        text,
        flags=re.I,
    )
    return text


def _repair_analysis_spillover_chapters(intermediate: dict) -> dict:
    """Move prose accidentally captured before ANALYSIS back to the prior chapter.

    AGES occasionally cuts a front-matter paragraph at the page where the
    ANALYSIS title begins, producing one chapter that starts with the previous
    sentence tail and only later says "ANALYSIS".  Rendering can repair this
    without rewriting the cached JSON.
    """
    chapters = intermediate.get('chapters') or []
    for index, chapter in enumerate(chapters):
        if index == 0 or 'ANALYSIS' not in (chapter.get('title') or '').upper():
            continue
        raw_text = chapter.get('raw_text') or ''
        if not raw_text or raw_text.lstrip().startswith('[['):
            continue
        match = re.search(r'\bANALYSIS\.?\s*', raw_text, re.I)
        if not match or match.start() < 80:
            continue
        spill = raw_text[:match.start()].strip()
        analysis_body = raw_text[match.end():].strip()
        if not spill or not analysis_body:
            continue

        previous = chapters[index - 1]
        previous_raw = (previous.get('raw_text') or '').rstrip()
        separator = ' ' if previous_raw and not re.search(r'[.!?]["”\')\]]?\s*$', previous_raw) else '\n\n'
        previous['raw_text'] = f'{previous_raw}{separator}{spill}'.strip()
        chapter['raw_text'] = f'[[SUBTITLE]] ANALYSIS.\n\n{analysis_body}'
    return intermediate


def _merge_reference_continuation_paragraphs(paragraphs: list[str]) -> list[str]:
    """Heal paragraph breaks inserted between "chap." and a following locator."""
    merged: list[str] = []
    for para in paragraphs:
        current = para.strip()
        if not current:
            continue
        if (
            merged
            and re.search(r'\b(?:chap|chapter)\.?\s*$', merged[-1], re.I)
            and re.match(r'^\d{1,3}:\d+(?:[-,]\s*\d+)*[,:;]?\b', current)
        ):
            merged[-1] = f'{merged[-1].rstrip()} {current}'
        else:
            merged.append(current)
    return merged


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
        '  <title>Table of Contents</title>',
        '  <link href="style/main.css" rel="stylesheet" type="text/css"/>',
        '</head>',
        '<body>',
        '<nav epub:type="toc" id="toc" role="doc-toc">',
        '<h2>Table of Contents</h2>',
    ]
    
    current_level = 0
    stack = []
    for level, text, href in toc_entries:
        # Normalize level to 1-3 range based on relative depth
        # Volume 1 often has [2, 3, 4] as levels.
        # Find the minimum level in toc_entries to use as base
        min_level = min(e[0] for e in toc_entries)
        level = (level - min_level) + 1
        level = max(1, min(level, 3))
        
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
        
        display_text = nav_display_title(text)
        lines.append(f'<li><a href="{_html_escape(href)}">{_html_escape(display_text)}</a>')
        stack.append('li')
        current_level = level

    while stack:
        lines.append(f'</{stack.pop()}>')

    lines.append('</nav>')
    
    # Landmarks
    lines.append('<nav epub:type="landmarks">\n<h2>Guide</h2>\n<ol>')
    if has_cover:
        lines.append('  <li><a epub:type="cover" href="cover.xhtml">Cover</a></li>')
    lines.append('  <li><a epub:type="toc" href="nav.xhtml">Table of Contents</a></li>')
    if has_frontispiece:
        lines.append('  <li><a epub:type="frontispiece" href="frontispiece.xhtml">Frontispiece</a></li>')
    if first_content_href:
        lines.append(f'  <li><a epub:type="bodymatter" href="{first_content_href}">Start of Content</a></li>')
    lines.extend(['</ol>', '</nav>', '</body>', '</html>'])
    
    return '\n'.join(lines)


def build_hierarchical_toc(toc_entries):
    """Convert flat (level, title, href) entries into nested ebooklib structure."""
    if not toc_entries:
        return []
        
    min_level = min(e[0] for e in toc_entries)
    
    def _nest(entries, base_level):
        result = []
        i = 0
        while i < len(entries):
            level, title, href = entries[i]
            # Normalize level
            rel_level = (level - min_level) + 1
            
            if rel_level == base_level:
                # Look ahead for children
                children_entries = []
                j = i + 1
                while j < len(entries):
                    next_level = (entries[j][0] - min_level) + 1
                    if next_level > base_level:
                        children_entries.append(entries[j])
                        j += 1
                    else:
                        break
                
                link = epub.Link(href, title, href.replace('.xhtml', ''))
                if children_entries:
                    result.append((link, _nest(children_entries, base_level + 1)))
                else:
                    result.append(link)
                i = j
            else:
                # Should not happen with well-formed TOC, but skip if it does
                i += 1
        return result

    return _nest(toc_entries, 1)


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
    """Repackage as canonical EPUB3 (mimetype first, no compression).

    Builds the zip in a system temp file, then copies it over the
    destination.  Using a temp-then-copy strategy avoids PermissionError
    on read-only or sandbox-mounted output directories where in-place
    deletion or creation of new files is blocked but overwriting existing
    file bytes (via shutil.copy2) is permitted.
    """
    import tempfile, shutil
    fd, tmp_path = tempfile.mkstemp(suffix='.epub')
    os.close(fd)
    os.remove(tmp_path)   # zip must create the file itself; it fails on an empty pre-existing file
    try:
        with open(os.path.join(src_dir, 'mimetype'), 'wb') as f:
            f.write(b'application/epub+zip')
        subprocess.run(['zip', '-0Xq', tmp_path, 'mimetype'],
                       cwd=src_dir, check=True)
        subprocess.run(['zip', '-r9q', tmp_path, '.', '-x',
                        'mimetype', '-x', '*.DS_Store'],
                       cwd=src_dir, check=True)
        # shutil.copy2 overwrites existing files without needing to delete them
        shutil.copy2(tmp_path, epub_path)
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def _add_cover_manifest_properties(tmp_dir):
    """Add properties='cover-image' to the cover manifest item in OPF."""
    import lxml.etree as et
    opf_path = os.path.join(tmp_dir, 'EPUB', 'content.opf')
    if not os.path.exists(opf_path):
        return
    tree = et.parse(opf_path)
    ns = {'opf': 'http://www.idpf.org/2007/opf'}
    manifest = tree.find('.//opf:manifest', ns)
    if manifest is None:
        return
    for item in manifest.findall('opf:item', ns):
        uid = item.get('id', '')
        if uid == 'cover-image':
            props = item.get('properties', '')
            if 'cover-image' not in props:
                item.set('properties', props + ' cover-image' if props else 'cover-image')
    tree.write(opf_path, xml_declaration=True, encoding='UTF-8')


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

def build_endnotes_chapter(footnotes, style_item=None, valid_fnums=None, vol_num=None, trans_notes=None):
    from translation_db import FOOTNOTE_TRANSLATIONS
    fn_map = {f.fnum: f for f in footnotes.values()}
    parts = ['<section epub:type="footnotes" role="doc-endnotes" hidden="hidden">']
    for fnum in sorted(fn_map.keys()):
        fn = fn_map[fnum]
        fn_text = tag_unicode_ranges(_html_escape(fn.text))
        
        # Look up translation and modernized patristic citation
        trans_key = f"v{vol_num}_fn{fnum}" if vol_num else f"v3_fn{fnum}"
        trans_info = FOOTNOTE_TRANSLATIONS.get(trans_key)
        
        extra_html = ""
        if trans_info:
            extra_html = f'<p class="footnote-modern-translation">{trans_info}</p>'
            
        parts.append(
            f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="fn{fnum}">'
            f'<p class="footnote">'
            f'<span class="fn-link">{fnum}</span> '
            f'{fn_text}'
            f'</p>'
            f'{extra_html}'
            f'</aside>'
        )
        
    if trans_notes:
        parts.append(
            f'<div class="translation-notes-header">'
            f'<h2 class="endnotes-section-title">Modern Editorial Translations</h2>'
            f'<p style="font-size: 0.9em; color: #666; text-align: center; font-style: italic; margin-top: 0.5em;">Translations of Latin, Greek, and Hebrew phrases appearing in the main text of this volume.</p>'
            f'</div>'
        )
        for note in trans_notes:
            parts.append(
                f'<aside epub:type="footnote endnote" role="doc-footnote doc-endnote" id="{note["id"]}">'
                f'<p class="footnote">'
                f'<span class="fn-link">[{note["num"]}]</span> '
                f'<span class="original-phrase">{tag_unicode_ranges(_html_escape(note["phrase"]))}</span>: '
                f'{note["translation"]}'
                f'</p>'
                f'</aside>'
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
    is_volume_title = bool(re.search(r'THE\s+WORKS\s+OF\s+JOHN\s+OWEN', text_upper))
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
        return 'title_page' if is_volume_title else 'treatise_title_page'

    # Beyond very sparse: char-count based title page detection (mid-volume)
    if total_chars < 1200 and large_chars >= 40:
        return 'title_page' if is_volume_title else 'treatise_title_page'

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
                return 'title_page' if is_volume_title else 'treatise_title_page'
            # If we hit a normal block first, it's a body page
            break

    return 'body_page'


def is_toc_continuation_page(page, page_num=None):
    """Detect continuation pages after a visual CONTENTS page.

    No hardcoded page-number cutoff — the caller (extract.py) stops the scan
    at the first known chapter page, which is the authoritative bound.
    Two complementary signals:
      1. Structural labels: CHAPTER N, PART N, numbered/Roman list items.
      2. Em-dash density: analytical TOC styles use em-dashes as topic
         separators (40–70 per page); body prose rarely exceeds ~5.
    """
    text = page.get_text()
    clean = re.sub(r'\s+', ' ', text).strip()
    if not clean:
        return False
    upper = clean.upper()
    # A page opening with a named section header is body content, not TOC
    if re.match(r'^\d*\s*(?:GENERAL PREFACE|PREFACE|PREFATORY NOTE|TO THE READER)\b', upper):
        return False
    chapter_hits = len(re.findall(r'\bCHAPTER\s+\d+', upper))
    part_hits = len(re.findall(r'\bPART\s+\d+', upper))
    numbered_hits = len(re.findall(r'(?:^|\s)(?:[IVXLCDM]+\.|\d+\.)\s+[—A-Z]', clean, re.I))
    em_dash_hits = text.count('—')
    return (chapter_hits + part_hits + numbered_hits) >= 1 or em_dash_hits >= 5


def format_treatise_title_page(page, limit_to_title=False):
    """Build specialized inner treatise title page (e.g. Christologia) with PDF-accurate layout.
    
    Handles:
      - Centered Greek markers
      - Big centered main title
      - Grouped centered sub-elements
      - Grouped italic descriptive blocks
      - Quote block at the bottom
    """
    blocks = page.get_text('dict')['blocks']
    lines_data = []
    
    # 1. Gather lines with metadata
    for b in blocks:
        if b.get('type') != 0: continue
        for line in b['lines']:
            spans = line['spans']
            max_size = max(s['size'] for s in spans)
            text = "".join(s['text'] for s in spans).strip()
            text = re.sub(r'<[0-9A-Fa-f]{6}>', '', text).strip()
            if not text or text.isdigit(): continue
            if any(h in text for h in _AGES_HEADERS): continue
            
            has_koine = any('Koine' in s['font'] for s in spans)
            has_italic = any('Italic' in s['font'] for s in spans)
            has_bold = any('Bold' in s['font'] for s in spans)
            
            lines_data.append({
                'text': text,
                'size': max_size,
                'has_koine': has_koine,
                'has_italic': has_italic,
                'has_bold': has_bold,
                'bbox': line['bbox']
            })

    if not lines_data: return ""

    parts = ['<section class="treatise-title-page" epub:type="titlepage">']
    body_remainder = []
    
    def starts_body_or_chapter(line_text):
        normalized = re.sub(r'\s+', ' ', line_text).strip()
        return bool(re.match(
            r'^(?:CHAPTER\s+\d+\.?|Ques\.?\s+\d+\.|Q\.\s*\d+\.|Ans\.?\s+\d+\.|A\.\s*\d+\.)\b',
            normalized,
            re.I,
        ))

    def looks_like_body_run(index):
        """Detect same-page prose after an inner title without swallowing subtitles."""
        if not limit_to_title or index < 3:
            return False
        sample = lines_data[index:index + 3]
        if len(sample) < 2:
            return False
        current_text = re.sub(r'\s+', ' ', sample[0]['text']).strip()
        current_words = re.findall(r"[A-Za-z']+", current_text)
        current_is_prose = (
            bool(re.search(r'[a-z]', current_text))
            and current_text.upper() != current_text
            and len(current_words) >= 7
            and sample[0]['size'] < 15
        )
        if not current_is_prose:
            return False
        prose_like = 0
        for item in sample:
            item_text = re.sub(r'\s+', ' ', item['text']).strip()
            words = re.findall(r"[A-Za-z']+", item_text)
            has_lower = bool(re.search(r'[a-z]', item_text))
            mostly_caps = item_text.upper() == item_text and len(words) >= 3
            if has_lower and not mostly_caps and len(words) >= 7 and item['size'] < 15:
                prose_like += 1
        return prose_like >= 2

    # 2. Process groups with lookahead for merging
    i = 0
    while i < len(lines_data):
        line = lines_data[i]
        text = line['text']
        y_pos = line['bbox'][1]

        if limit_to_title and (starts_body_or_chapter(text) or looks_like_body_run(i)):
            for item in lines_data[i:]:
                remainder_text = item['text']
                if item['has_koine']:
                    remainder_text = convert_greek_word(remainder_text)
                body_remainder.append(remainder_text)
            break
        
        # Detect Quote block at bottom (usually y > 500 on 792pt page)
        if (text.startswith(('“', '"')) or y_pos > 500) and i >= len(lines_data) - 6:
            quote_lines = []
            while i < len(lines_data):
                l_text = lines_data[i]['text']
                if lines_data[i]['has_koine']:
                    l_text = convert_greek_word(l_text)
                quote_lines.append(_html_escape(l_text))
                i += 1
            full_quote = " ".join(quote_lines)
            parts.append(f'<div class="quote-block">{tag_unicode_ranges(full_quote)}</div>')
            break

        # Greek Markers (often used as titles, e.g. ΧΡΙΣΤΟΛΟΓΙΑ)
        if line['has_koine']:
            greek_text = convert_greek_word(text)
            parts.append(f'<h2 class="greek-title"><span lang="el" xml:lang="el">{_html_escape(greek_text)}</span></h2>')
            i += 1
            continue

        # Main Title (Big text)
        if line['size'] > 15 or line['has_bold']:
            cls = 'title-line-major' if line['size'] > 18 else 'title-line-medium'
            parts.append(f'<p class="title-line {cls}">{_html_escape(text)}</p>')
            i += 1
            continue
            
        # Separators (OR, WITH, OF)
        if text.upper() in _TITLE_CONNECTORS:
            parts.append(f'<p class="title-connector">{_html_escape(text)}</p>')
            i += 1
            continue

        # Descriptive/Italic - MERGE CONSECUTIVE LINES
        if line['has_italic']:
            italic_parts = [_html_escape(text)]
            j = i + 1
            while j < len(lines_data):
                next_line = lines_data[j]
                if next_line['has_italic'] and not next_line['has_bold'] and next_line['size'] < 15:
                    italic_parts.append(_html_escape(next_line['text']))
                    j += 1
                else:
                    break
            joined_italic = " ".join(italic_parts)
            parts.append(f'<p class="descriptive">{joined_italic}</p>')
            i = j
            continue

        # Standard descriptive
        parts.append(f'<p class="descriptive">{_html_escape(text)}</p>')
        i += 1

    parts.append('</section>')
    result = "\n".join(parts)
    if body_remainder:
        result += "\n\n" + "\n".join(body_remainder)
    return result


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
            text = re.sub(r'<[0-9A-Fa-f]{6}>', '', text).strip()
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
        elif text.upper() in _TITLE_CONNECTORS:
            lvl = 'p'
            cls = ' class="title-connector"'
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
        
    parts = ['<section class="contents-page" epub:type="toc">']
    
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
                l_text = re.sub(r'<[0-9A-Fa-f]{6}>', '', l_text).strip()
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
                if full_text.upper().startswith('CONTENTS OF VOLUME'):
                    parts.append(f'<h1 class="contents-volume-title">{safe_text}</h1>')
                else:
                    parts.append(f'<h2 class="contents-treatise-title">{safe_text}</h2>')
            # 2. Section Headers (PREFATORY NOTE, PREFACE, etc.)
            elif full_text.isupper() and len(full_text) < 40:
                parts.append(f'<p class="contents-frontmatter-line">{safe_text}</p>')
            # 3. TOC Items (CHAPTER 1, 1. -, etc.)
            else:
                # Use .ContentsItem for hanging indent
                # We want to bold the label part if possible
                # Refined regex for labels like "1. —" or "CHAPTER 1."
                match = re.match(r'^((?:CHAPTER\s+\d+|[IVXLC]+\.|[0-9]+[\.\-\s]*[—\-]?)\s*)(.*)', full_text, re.I | re.S)
                if match:
                    label, desc = match.groups()
                    desc_safe = _html_escape(desc.strip())
                    parts.append(f'<p class="contents-item"><b>{_html_escape(label)}</b> {desc_safe}</p>')
                else:
                    continuation = _html_escape(re.sub(r'\s+', ' ', full_text).strip())
                    if (
                        parts
                        and 'class="contents-item"' in parts[-1]
                        and re.search(r'[;—-]\s*</p>$', parts[-1])
                    ):
                        # Sparse TOC style: merge continuation into previous entry
                        parts[-1] = parts[-1].replace('</p>', f' {continuation}</p>')
                    elif continuation:
                        # Analytical TOC style: descriptive paragraph after a heading
                        parts.append(f'<p class="contents-desc">{continuation}</p>')

    parts.append('</section>')
    return '\n'.join(parts)


def generate_copyright_xhtml(vol_num, config, primary_font_name):
    """Generate visual and detailed Publication Metadata (colophon/copyright) page."""
    publisher = config.get('publisher') or 'Eduardus Ekofius'
    editors = config.get('editors') or ['William H. Goold']
    editor = editors[0] if editors else 'William H. Goold'
    subtitle = VOLUME_SUBTITLES.get(vol_num, '')
    
    ages_info = (
        "The text of this digital edition was originally transcribed and prepared by "
        "<strong>A.G.E.S. Software</strong> (Albany, Oregon) as part of their landmark "
        "<strong>A.G.E.S. Digital Library</strong>, active during the late 1990s and early 2000s. "
        "Their monumental CD-ROM collection, particularly \"The Master Christian Library\" "
        "and \"the digital Owen collection,\" was pioneering in digital theological publishing—preserving "
        "classic, out-of-print Puritan and Reformed literature, making these historic writings "
        "inexpensively accessible to students, ministers, and scholars worldwide."
    )
    
    historical_info = (
        f"This digital volume reproduces the text of the authoritative 16-volume standard edition "
        f"of the <i>Works of John Owen</i>, edited by the Reverend William H. Goold, originally "
        f"published between 1850 and 1853 by Johnstone & Hunter in Edinburgh. The treatises "
        f"and sermons in this volume cover core elements of Reformed and Puritan theology, "
        f"dogmatics, and biblical exposition."
    )
    
    conversion_info = (
        "This EPUB 3.0 publication is the result of a modern agentic conversion pipeline "
        "specifically optimized for high-fidelity rendering on mobile devices, tablets, and e-readers. "
        "It features holistic paragraph healing across page boundaries, automatic language tagging "
        "for Greek and Hebrew Unicode scripts, continuous blockquote styling, easy-tap footnote controls, "
        "and complete typographic consistency tailored for Apple Books."
    )

    fonts_list_html = f"""
    <ul class="colophon-metadata-list">
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Primary Body:</span>
        <span class="colophon-metadata-value">{_escape_xml(primary_font_name)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Greek Script:</span>
        <span class="colophon-metadata-value">SBL Greek / SBL BibLit</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Hebrew Script:</span>
        <span class="colophon-metadata-value">SBL Hebrew / Ezra SIL</span>
      </li>
    </ul>
    """
    
    subtitle_escaped = _escape_xml(subtitle)
    metadata_list_html = f"""
    <ul class="colophon-metadata-list">
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Title:</span>
        <span class="colophon-metadata-value">The Works of John Owen, Volume {vol_num}</span>
      </li>
      {f'<li class="colophon-metadata-item"><span class="colophon-metadata-label">Subtitle:</span><span class="colophon-metadata-value">{subtitle_escaped}</span></li>' if subtitle else ''}
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Author:</span>
        <span class="colophon-metadata-value">John Owen (1616–1683)</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Editor:</span>
        <span class="colophon-metadata-value">{_escape_xml(editor)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Publisher:</span>
        <span class="colophon-metadata-value">{_escape_xml(publisher)}</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Release Year:</span>
        <span class="colophon-metadata-value">2026</span>
      </li>
      <li class="colophon-metadata-item">
        <span class="colophon-metadata-label">Format:</span>
        <span class="colophon-metadata-value">EPUB 3.0 (Digital Edition)</span>
      </li>
    </ul>
    """

    html = f"""<section class="colophon-page" epub:type="colophon">
  <h1 class="colophon-title">Publication Metadata</h1>
  
  <p class="colophon-ornament">❧</p>
  
  <div class="colophon-section">
    <h2 class="colophon-section-title">Edition Details</h2>
    {metadata_list_html}
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Historical Source</h2>
    <p>{historical_info}</p>
    <p>{ages_info}</p>
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Typography &amp; Fonts</h2>
    <p>This volume is styled with a premium collection of typography designed specifically for legibility and aesthetic excellence on narrow screens and e-ink displays. The following fonts are embedded or referenced within this package:</p>
    {fonts_list_html}
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Modern Translations &amp; Patristic Citations</h2>
    <p>This digital edition features premium scholarly enhancements for modern readers. Because John Owen frequently utilized Greek, Hebrew, and Latin without translation, this volume implements a double-track footnote architecture:</p>
    <ul>
      <li><strong>Bracketed Footnotes <code>[1], [2], ...</code></strong>: These represent modern editorial translations of inline Latin, Greek, and Hebrew phrases and verified modern patristic citations. They are kept entirely distinct from the original authorial/historical footnotes and reset starting at <code>[1]</code> for each chapter.</li>
      <li><strong>Enhanced Original Footnotes <code>1, 2, ...</code></strong>: Original historical footnotes remain intact, numbered sequentially. Where these footnotes contain untranslated Greek/Latin quotes or abbreviated patristic references, a dedicated modernization block has been appended directly beneath them showing full modern translations and standard academic source citations.</li>
    </ul>
  </div>

  <div class="colophon-section">
    <h2 class="colophon-section-title">Conversion Technology</h2>
    <p>{conversion_info}</p>
  </div>
</section>"""
    return html


def generate_structural_guide_html(vol_num: int) -> str:
    """Generate a premium, mobile-first Structural Guide page for the front matter."""
    return f'''<section class="front-matter-section structural-guide-page">
<h2 class="front-matter-heading">Note on the Structural Formatting</h2>

<p class="front-matter-prose first">In common with other scholastic theological works of the seventeenth century, the treatises of Dr. John Owen feature an incredibly rich, complex, and deeply layered hierarchy of divisions, subdivisions, and nested rhetorical arguments. In early editions, these nested numeral systems (I, 1, (1), [1], 1st) frequently fell into typographical confusion, bewildering the reader in a labyrinthine maze of outlines.</p>

<p class="front-matter-prose">To restore Goold’s original logical clarity while ensuring a premium, seamless reading experience on modern mobile devices, this digital edition adopts a standardized, highly readable <strong>Three-Level Visual Hierarchy</strong> designed specifically for Apple Books and iPhone:</p>

<div class="structural-guide-levels" style="margin: 1.8em 5%; padding: 0.5em 0.8em; border-left: 2.5px solid #2a55a0; background-color: rgba(42, 85, 160, 0.03);">
  <p style="margin: 0.6em 0; text-indent: 0; line-height: 1.5; font-size: 0.95em;">
    <strong style="color: #2a55a0;">Level 1 — Major Expository Divisions</strong><br/>
    Marked by bare Arabic decimals (e.g., <strong>1., 2.</strong>) or uppercase Roman numerals (e.g., <strong>I., II.</strong>). These serve as the main anchors of Owen’s discourse and are positioned flush against the left margin.
  </p>
  <p style="margin: 0.8em 0 0.6em; text-indent: 0; line-height: 1.5; font-size: 0.95em;">
    <strong style="color: #2a55a0;">Level 2 — Nested Proofs &amp; Subdivisions</strong><br/>
    Marked by parenthesized Arabic numbers (e.g., <strong>(1.), (2.)</strong>) or bracketed Arabic numbers (e.g., <strong>[1.], [2.]</strong>). These represent secondary theological proofs and are indented with a subtle, thin vertical blue hairline on the left.
  </p>
  <p style="margin: 0.8em 0 0.6em; text-indent: 0; line-height: 1.5; font-size: 0.95em;">
    <strong style="color: #2a55a0;">Level 3 — Local Rhetorical Subpoints</strong><br/>
    Marked by digit-based ordinals (e.g., <strong>1st., 2dly., 3dly.</strong>) or bracketed word ordinals (e.g., <strong>[FIRSTLY]</strong>). These represent rapid logical chains or local lists, and are modestly indented without double vertical lines to prevent layout crushing on narrow screens.
  </p>
</div>

<p class="front-matter-prose"><strong>Dynamic Outline Formatting (Inline vs. Block)</strong></p>
<p class="front-matter-prose">To optimize the display for narrow smartphone screens, the outline rendering is determined dynamically by rhetorical length:</p>
<ul style="margin: 0.8em 8% 1.2em; padding-left: 1.2em; line-height: 1.6; font-size: 0.95em; color: #333; list-style-type: square;">
  <li style="margin-bottom: 0.6em;"><strong>Inline Flat Syllabus:</strong> Short, compact summary lists (e.g., <em>“reduced unto two heads: 1st, Adoration; 2ndly, Invocation”</em>) are elegant, flat, and inline. This prevents long, distracting vertical stacks of short words or phrases.</li>
  <li><strong>Indented Block Paragraphs:</strong> When an outline ordinal introduces a substantial paragraph of expository prose or a detailed theological argument, it is kept as a distinct block paragraph with clear indents to preserve paragraph continuity and reading comfort.</li>
</ul>

<p class="front-matter-prose"><strong>Polyglot Typographical Integration</strong></p>
<p class="front-matter-prose">Every Greek and Hebrew citation in this work is automatically isolated and wrapped in specialized, highly legible fonts (<em>SBL Greek</em> and <em>SBL Hebrew</em> or <em>Ezra SIL</em>) to ensure that the ancient languages render with premium clarity and correct right-to-left layout alignment across all digital platforms.</p>
</section>
'''


# ================================================================
# STAGE 2 ENTRY POINT — render_volume()
# ================================================================


def render_volume(vol_num: int, overrides: dict = None,
                  intermediate: dict = None, progress_callback=None) -> str:
    """Run Stage 2 for a single Owen volume: JSON intermediate → EPUB3.

    Reads volumes/vN/intermediate/volume_N.json (or uses supplied dict),
    assembles the EPUB3, and writes volumes/vN/output/volume_N.epub.
    Returns the path to the written EPUB.

    overrides: optional per-volume config additions (see volumes/vN/convert.py).
    intermediate: if supplied, use this dict instead of reading from disk.
    """
    # Import here to avoid circular import at module level
    from shared import (
        merge_volume_config,
        EPUB_STYLESHEET, generate_font_styles, select_primary_font,
        SBL_SUPPLEMENTS, EZRA_SIL_FILES, TITLE_PAGE_FONTS,
    )
    try:
        from ebooklib import epub
    except ImportError:
        import sys; sys.exit("Error: ebooklib not installed.")

    config = merge_volume_config(vol_num, overrides)

    vol_dir = _RENDER_DIR / 'volumes' / f'v{vol_num}'
    json_path = vol_dir / 'intermediate' / f'volume_{vol_num}.json'
    out_dir = vol_dir / 'output'
    out_dir.mkdir(parents=True, exist_ok=True)
    epub_path = str(out_dir / f'volume_{vol_num}.epub')

    if intermediate is None:
        with open(json_path, encoding='utf-8') as f:
            intermediate = json.load(f)
    intermediate = _repair_analysis_spillover_chapters(intermediate)

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
    extra_css = config.get('extra_css', '')
    full_css = EPUB_STYLESHEET + '\n' + font_css
    if extra_css:
        full_css += '\n' + extra_css
    style_item = epub.EpubItem(
        uid='style', file_name='style/main.css',
        media_type='text/css', content=full_css.encode('utf-8'),
    )
    book.add_item(style_item)

    font_fnames = set()
    font_base = os.path.join(_RENDER_DIR, 'fonts')

    def _font_media_type(filename):
        ext = os.path.splitext(filename)[1].lower()
        if ext == '.otf':
            return 'font/otf'
        if ext == '.ttf':
            return 'font/ttf'
        if ext == '.woff':
            return 'font/woff'
        if ext == '.woff2':
            return 'font/woff2'
        return 'application/font-sfnt'

    # Primary font files (from select_primary_font dict)
    for _variant, _rel_path in primary_font.get('files', {}).items():
        _fbase = os.path.basename(_rel_path)
        if _fbase in font_fnames:
            continue
        _src = os.path.join(font_base, _rel_path)
        if os.path.exists(_src):
            book.add_item(epub.EpubItem(
                uid=f'f_{_fbase.replace(".","_")}',
                file_name=f'Fonts/{_fbase}', media_type=_font_media_type(_fbase),
                content=open(_src, 'rb').read(),
            ))
            font_fnames.add(_fbase)

    # Supplemental biblical fonts, heading font, and the embedded title display face
    for _font_dict in (SBL_SUPPLEMENTS, EZRA_SIL_FILES, PROXIMA_NOVA_FILES, TITLE_PAGE_FONTS):
        for _fname, _fpath in _font_dict.items():
            _fbase = os.path.basename(_fpath)
            if _fbase in font_fnames:
                continue
            _src = os.path.join(font_base, _fpath)
            if os.path.exists(_src):
                book.add_item(epub.EpubItem(
                    uid=f'f_{_fbase.replace(".","_")}',
                    file_name=f'Fonts/{_fbase}',
                    media_type=_font_media_type(_fbase),
                    content=open(_src, 'rb').read(),
                ))
                font_fnames.add(_fbase)

    # ── Cover ────────────────────────────────────────────────────
    cover_path = find_cover(vol_num)
    cover_page = None
    cover_item = None
    if cover_path and os.path.exists(cover_path):
        ext = os.path.splitext(cover_path)[1].lower()
        mt = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
        with open(cover_path, 'rb') as f:
            cover_item = epub.EpubItem(
                uid='cover-image', file_name=f'images/cover{ext}',
                media_type=mt, content=f.read(),
            )
        book.add_item(cover_item)
        book.add_metadata(None, 'meta', '', {'name': 'cover', 'content': 'cover-image'})
        
        # Create manual cover page for spine control
        cover_page = epub.EpubHtml(title='Cover', file_name='cover.xhtml', lang='en')
        cover_html = f'<div class="cover"><img src="images/cover{ext}" alt="Cover"/></div>'
        cover_page.set_content(_make_xhtml('Cover', cover_html).encode('utf-8'))
        book.add_item(cover_page)

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
        
        # Use the relative path in the EPUB (images/portrait.ext)
        fi_html = generate_frontispiece_xhtml(os.path.basename(port_fn))
        frontispiece_item = epub.EpubHtml(
            title='Frontispiece', file_name='frontispiece.xhtml', lang='en',
        )
        frontispiece_item.set_content(
            _make_xhtml('Frontispiece', fi_html).encode('utf-8')
        )
        frontispiece_item.add_item(style_item)
        book.add_item(frontispiece_item)

    # ── Emblem Seal ──────────────────────────────────────────────
    emblem_path = _RENDER_DIR / 'covers' / 'emblem_seal.png'
    if emblem_path.exists():
        with open(emblem_path, 'rb') as f:
            emblem_item = epub.EpubItem(
                file_name='images/emblem_seal.png',
                media_type='image/png',
                content=f.read()
            )
        book.add_item(emblem_item)

    # ── PDF-extracted front matter (title pages, TOC) ────────────
    front_matter_epub_items = []
    _last_fm_title = None
    copyright_added = False
    added_structural_guide = False
    for fm in intermediate.get('front_matter_items', []):
        if fm['title'] == _last_fm_title:
            continue
        _last_fm_title = fm['title']
        
        if fm.get('type') == 'toc' and not copyright_added:
            cop_title = 'Publication Metadata'
            cop_fn = 'colophon.xhtml'
            cop_html = generate_copyright_xhtml(vol_num, config, primary_font['name'])
            cop_item = epub.EpubHtml(
                title=cop_title, file_name=cop_fn, lang='en',
            )
            cop_item.set_content(
                _make_xhtml(cop_title, cop_html).encode('utf-8')
            )
            cop_item.add_item(style_item)
            book.add_item(cop_item)
            front_matter_epub_items.append(cop_item)
            copyright_added = True

        fm_item = epub.EpubHtml(
            title=fm['title'], file_name=fm['file_name'], lang='en',
        )
        fm_html = fm['html']
        if fm_html is None:
            continue
        fm_overrides = config.get('front_matter_overrides', {})
        if fm['title'] in fm_overrides:
            fm_html = fm_overrides[fm['title']]
        elif fm.get('type') == 'title_page':
            fm_html = _polish_volume_title_page_html(fm_html, vol_num, config)
        elif fm.get('type') == 'treatise_title_page':
            fm_html = _polish_treatise_title_page_html(fm_html)
        elif fm.get('type') == 'toc':
            toc_override = config.get('contents_page_overrides')
            if toc_override:
                fm_html = toc_override
            else:
                fm_html = _polish_contents_page_html(fm_html)
        fm_item.set_content(
            _make_xhtml(fm['title'], fm_html).encode('utf-8')
        )
        fm_item.add_item(style_item)
        book.add_item(fm_item)
        front_matter_epub_items.append(fm_item)

        # Dynamic insertion of the Note on Structural Formatting after TOC page
        if fm.get('type') == 'toc' and not added_structural_guide:
            note_item = epub.EpubHtml(
                title='Note on Structural Formatting',
                file_name='structural_guide.xhtml',
                lang='en',
            )
            note_html = generate_structural_guide_html(vol_num)
            note_item.set_content(_make_xhtml('Note on Structural Formatting', note_html).encode('utf-8'))
            note_item.add_item(style_item)
            book.add_item(note_item)
            front_matter_epub_items.append(note_item)
            added_structural_guide = True

    if not added_structural_guide:
        note_item = epub.EpubHtml(
            title='Note on Structural Formatting',
            file_name='structural_guide.xhtml',
            lang='en',
        )
        note_html = generate_structural_guide_html(vol_num)
        note_item.set_content(_make_xhtml('Note on Structural Formatting', note_html).encode('utf-8'))
        note_item.add_item(style_item)
        book.add_item(note_item)
        front_matter_epub_items.append(note_item)
        added_structural_guide = True

    if not copyright_added:
        cop_title = 'Publication Metadata'
        cop_fn = 'colophon.xhtml'
        cop_html = generate_copyright_xhtml(vol_num, config, primary_font['name'])
        cop_item = epub.EpubHtml(
            title=cop_title, file_name=cop_fn, lang='en',
        )
        cop_item.set_content(
            _make_xhtml(cop_title, cop_html).encode('utf-8')
        )
        cop_item.add_item(style_item)
        book.add_item(cop_item)
        front_matter_epub_items.append(cop_item)
        copyright_added = True

    # ── Chapters ─────────────────────────────────────────────────
    toc_entries = []
    epub_chapters = []
    all_translation_notes = []
    guide_landmarks = [] # was [('Title Page', 'title.xhtml')]

    conv_mode = 'FRONT_MATTER'
    conv_drop_cap = False
    conv_fm_style = 'blurb'

    _FM_PROSE_KEYWORDS = [
        'PREFACE', 'PREFATORY NOTE', 'PREFATORY', 'ANALYSIS',
        'TO THE READER', 'ADVERTISEMENT', 'GENERAL PREFACE',
    ]

    for ch_dict in intermediate['chapters']:
        title_upper = ch_dict['title'].upper()
        if ch_dict.get('is_endnotes') or title_upper == 'FOOTNOTES':
            continue

        fm_style = ch_dict.get('front_matter_style')

        if any(kw in title_upper for kw in ['ANALYSIS', 'PREFATORY NOTE', 'PREFACE', 'CONTENTS']):
            conv_mode = 'FRONT_MATTER'
            conv_drop_cap = False
            conv_fm_style = 'prose'
        elif ch_dict.get('is_treatise'):
            conv_mode = 'BODY_START'
            conv_drop_cap = True
            conv_fm_style = 'blurb'
        elif re.search(r'\bCHAPTER\s+\d+\b|\bSERMON\s+\d+\b|\bDISCOURSE\s+\d+\b', title_upper):
            if conv_mode == 'FRONT_MATTER':
                conv_mode = 'BODY_START'
                conv_drop_cap = True
            conv_fm_style = 'blurb'

        raw_text = ch_dict.get('raw_text', '')
        titlepage_override = config.get('treatise_title_overrides', {}).get(ch_dict['title'])
        if titlepage_override:
            foreign_frags = _foreign_fragments_in_section(raw_text)
            raw_text = _merge_titlepage_override(titlepage_override, foreign_frags)
        if not raw_text:
            continue
        if 'ANALYSIS' in title_upper:
            raw_text = _prepare_analysis_raw_text(raw_text)
        part_match = re.search(r'\bPart\s+([0-9IVXLCDM]+)\b', ch_dict.get('title', ''), re.I)
        if (
            ch_dict.get('is_treatise')
            and part_match
            and not re.search(r'\[\[PART\]\]|\bPART\s+[0-9IVXLCDM]+\.?', raw_text[:400], re.I)
        ):
            raw_text = f'[[PART]] PART {part_match.group(1)}.\n\n{raw_text}'

        # Issue 41: Some chapters are missing their [[CHAPTER]] token because the
        # PDF page for that chapter starts with the summary text and the chapter
        # heading line was not detected during extraction.  When the metadata title
        # says "Chapter N - …" but the raw_text has no [[CHAPTER]] token, inject it.
        _chapter_num_match = re.match(
            r'^Chapter\s+(\d+)\b', ch_dict.get('title', ''), re.I
        )
        if (
            _chapter_num_match
            and not re.search(r'\[\[CHAPTER\]\]', raw_text[:200])
            and not re.search(r'\[\[PART\]\]', raw_text[:200])
            and not ch_dict.get('is_treatise')
        ):
            _ch_num = _chapter_num_match.group(1)
            raw_text = f'[[CHAPTER]] CHAPTER {_ch_num}.\n\n{raw_text}'

        # Catechism context is per-chapter only — never sticky.
        # A chapter qualifies when its title contains "CATECHISM" OR its
        # raw_text contains actual Q./Ques./Ans. Q&A markers.  This prevents
        # the flag from bleeding into any prose chapter that follows the
        # catechism block (Issue #30 v1).
        in_catechism_context = (
            'CATECHISM' in title_upper
            or bool(re.search(
                r'^\s*(?:Q\.|Ques\.\s*\d|Ans\.\s*[A-Z])',
                raw_text[:3000],
                re.MULTILINE,
            ))
        )
        chapter_config = {
            **config,
            'is_catechism_context': in_catechism_context,
            'chapter_title': ch_dict.get('title'),
        }
        body_html, conv_mode, conv_drop_cap = markdown_to_html(
            raw_text,
            current_mode=conv_mode,
            pending_drop_cap=conv_drop_cap,
            front_matter_style=conv_fm_style,
            config=chapter_config
        )
        if 'ANALYSIS' in title_upper:
            body_html = _polish_analysis_html(body_html)
        body_html = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', body_html, flags=re.I)
        body_html = apply_scholastic_anchor_protocol(body_html)
        html_postprocess_hook = config.get('html_postprocess_hook')
        if html_postprocess_hook:
            ch_context = {**ch_dict, 'is_catechism_context': in_catechism_context}
            body_html = html_postprocess_hook(body_html, ch_context)
        body_html = _apply_premium_signatures(body_html, ch_dict.get('title', ''))
        body_html = _apply_premium_chapter_endings(body_html)
        body_html = _apply_premium_salutations(body_html)
        inline_replacements = config.get('inline_html_replacements', {})
        if inline_replacements:
            for old, new in inline_replacements.items():
                body_html = body_html.replace(old, new)
        if not body_html.strip():
            continue

        # Dynamic translation notes scanning and substitution
        from translation_db import BODY_TRANSLATIONS
        sorted_phrases = sorted(BODY_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
        local_notes = []
        placeholders = {}
        trans_counter = 0
        cid = ch_dict['cid']

        for idx, (phrase, trans) in enumerate(sorted_phrases):
            # Match the phrase, optionally wrapped in language spans
            pattern = re.compile(
                rf'(<span\s+lang="(?:el|he)"[^>]*>\s*{re.escape(phrase)}\s*</span>|{re.escape(phrase)})'
            )
            if pattern.search(body_html):
                trans_counter += 1
                placeholder = f"___TRANSPHRASE_PLACEHOLDER_{idx}___"
                matched_str = pattern.search(body_html).group(0)
                fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{trans_counter}">[{trans_counter}]</a></sup>'
                placeholders[placeholder] = f"{matched_str}{fn_link}"
                local_notes.append({
                    'id': f"fntrans_{cid}_{trans_counter}",
                    'num': trans_counter,
                    'phrase': phrase,
                    'translation': trans
                })
                body_html = pattern.sub(placeholder, body_html)

        for placeholder, replacement in placeholders.items():
            body_html = body_html.replace(placeholder, replacement)

        if local_notes:
            all_translation_notes.extend(local_notes)

        body = f'<section>{body_html}</section>'
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
    if footnote_map or all_translation_notes:
        endnotes_html = build_endnotes_chapter(footnote_map, style_item, vol_num=vol_num, trans_notes=all_translation_notes)
        endnotes_item = epub.EpubHtml(
            title='Footnotes', file_name='endnotes.xhtml', lang='en',
        )
        endnotes_item.set_content(endnotes_html.encode('utf-8'))
        endnotes_item.add_item(style_item)
        book.add_item(endnotes_item)

    # ── NAV, NCX, spine ──────────────────────────────────────────
    # Blemish fix (Issue 2): Cover and "Contents of Volume N" must appear in the
    # main nav <nav epub:type="toc"> so Apple Books and all readers show them in
    # the navigation panel.  Prepend them at level 1 ahead of chapter entries.
    _nav_seen_titles: set = set()
    _nav_prefix: list = []
    if cover_page:
        _nav_prefix.append((1, 'Cover', 'cover.xhtml'))
        _nav_seen_titles.add('Cover')
    for _fm in intermediate.get('front_matter_items', []):
        _fm_title = _fm.get('title', '')
        _fm_html = _fm.get('html')
        if _fm_html is None:
            continue
        if _fm_title and _fm_title not in _nav_seen_titles:
            _nav_prefix.append((1, _fm_title, _fm['file_name']))
            _nav_seen_titles.add(_fm_title)
    # Also add any prose front-matter items (Preface, Analysis, etc.) not yet listed
    for _fm_item in front_matter_epub_items:
        _fmt = getattr(_fm_item, 'title', None) or ''
        _fmf = getattr(_fm_item, 'file_name', None) or ''
        if _fmt and _fmt not in _nav_seen_titles and _fmf:
            _nav_prefix.append((1, _fmt, _fmf))
            _nav_seen_titles.add(_fmt)
    nav_entries = _nav_prefix + toc_entries  # already (level, title, href)
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
    nav_item.properties = ['nav']
    nav_item.set_content(_make_xhtml('Table of Contents', nav_html).encode('utf-8'))
    nav_item.add_item(style_item)
    book.add_item(nav_item)
    
    # Set hierarchical TOC for ebooklib (affects NCX and device menus)
    book.toc = build_hierarchical_toc(nav_entries)

    ncx_uid = uid
    ncx = epub.EpubNcx()
    book.add_item(ncx)

    spine = []
    if cover_page:
        spine.append(cover_page)
    spine.extend(front_matter_epub_items)
    if frontispiece_item:
        spine.append(frontispiece_item)
    spine += epub_chapters
    book.spine = spine

    # ── Write and repackage ──────────────────────────────────────
    import tempfile as _tempfile
    import zipfile as _zf
    # ebooklib writes a valid EPUB but not in canonical form (mimetype must be
    # first and uncompressed). Write to a temp path, extract, repackage.
    temp_epub = epub_path + '.tmp_build'
    epub.write_epub(temp_epub, book)
    with _tempfile.TemporaryDirectory() as tmp:
        with _zf.ZipFile(temp_epub, 'r') as z:
            z.extractall(tmp)
        _add_cover_manifest_properties(tmp)
        repackage_canonical(epub_path, tmp)
    if os.path.exists(temp_epub):
        try:
            os.remove(temp_epub)
        except OSError:
            pass  # sandbox/read-only mount — stale .tmp_build is harmless
    _inject_apple_books_options(epub_path)
    print(f'[render] ✓ EPUB saved: {epub_path}')
    return epub_path


if __name__ == '__main__':
    import sys
    vol = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    render_volume(vol)
