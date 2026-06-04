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

from scripts.epub_pages import (
    _polish_contents_page_html,
    format_treatise_title_page,
    format_title_page,
    build_toc_page_xhtml,
    generate_copyright_xhtml,
    restore_dropped_title_noteref,
    _AGES_HEADERS,
    _TITLE_CONNECTORS
)
from scripts.scholastic_parser import apply_scholastic_anchor_protocol, _nest_scholastic_in_divs
from scripts.polish import _apply_premium_signatures, _apply_premium_chapter_endings, _apply_premium_salutations
from scripts.analysis_parser import (
    _polish_analysis_html,
    _prepare_analysis_raw_text,
    _repair_analysis_spillover_chapters,
)

_RENDER_DIR = Path(__file__).parent.resolve()
if str(_RENDER_DIR) not in sys.path:
    sys.path.insert(0, str(_RENDER_DIR))

from scripts.epub_builder import (
    _make_xhtml,
    _polish_treatise_title_page_html,
    _polish_volume_title_page_html,
    build_endnotes_chapter,
    build_hierarchical_toc,
    generate_frontispiece_xhtml,
    generate_nav_xhtml,
    repackage_canonical,
    _add_cover_manifest_properties,
    _inject_apple_books_options,
)

from shared import (
    VOLUME_CONFIG, VOLUME_SUBTITLES,
    EPUB_STYLESHEET, generate_font_styles,
    select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES, TITLE_PAGE_FONTS, PROXIMA_NOVA_FILES, GFS_PORSON_FILES,
    CARDO_FILES, GENTIUM_PLUS_FILES, tag_latin_words,
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
    _split_inline_structural_markers,
    _trim_duplicate_reference_prefix,
)

from scripts.owen_lists import (
    _attach_em_dash_flat_list,
    _owen_marker_level,
    _add_owen_list_level_classes,
    _nest_owen_list_hierarchies,
    _merge_short_inline_lists,
)

from scripts.markdown_parser import markdown_to_html, _repair_markdown_tables
from scripts.roman_parser import _roman_head_match

try:
    from ebooklib import epub
except ImportError:
    sys.exit("Error: ebooklib not installed.")

FONT_BASE = os.path.join(_RENDER_DIR, 'fonts')


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

    text = tag_latin_words(text)
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
        before_text = re.sub(r'\s+([.,;:?!])', r'\1', before_text)
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



def _strip_inline_structural_tokens(text):
    """Remove any structural tokens that leaked into paragraphs (e.g. [[SUMMARY]])."""
    return re.sub(r'\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*', '', text)


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
    import unicodedata

    def _strip_diacritics(text):
        normalized = unicodedata.normalize('NFD', text)
        return "".join(c for c in normalized if not unicodedata.combining(c))

    def _clean_for_compare(text):
        cleaned = _strip_diacritics(text).lower()
        cleaned = _re.sub(r'[^a-z\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff]', '', cleaned)
        return cleaned

    override_clean = _clean_for_compare(override)

    for frag in fragments:
        plain_frag = _re.sub(r'<[^>]+>', '', frag).strip()
        if not plain_frag:
            continue
        
        # If this plain text is already present in the override, skip it
        if plain_frag in override or _clean_for_compare(plain_frag) in override_clean:
            continue
            
        # Append before the closing </section>
        override = _re.sub(
            r'(</section>\s*$)',
            '\n' + frag + '\n' + r'\1',
            override,
            flags=_re.I
        )
        override_clean = _clean_for_compare(override)
        
    return override


def _split_raw_title_body(raw_text: str) -> tuple[str, str]:
    """
    Splits raw_text into (title_block, body_text).
    The title_block is the leading part containing headings, summary, etc.
    The body_text is the subsequent actual content.
    If no body text is found, body_text will be empty.
    """
    if not raw_text:
        return "", ""

    # If the raw_text is already an HTML section (e.g. standalone title page),
    # then it doesn't have a separate body text to preserve.
    if raw_text.strip().startswith('<section') and '</section>' in raw_text:
        return raw_text, ""

    paragraphs = raw_text.split('\n\n')
    title_paras = []
    body_paras = []
    in_body = False

    for p in paragraphs:
        p_strip = p.strip()
        if not p_strip:
            continue
        if in_body:
            body_paras.append(p)
        else:
            # Check if this paragraph is part of the title page metadata/headings.
            is_title_tag = (
                p_strip.startswith('[[CHAPTER]]') or
                p_strip.startswith('[[SUMMARY]]') or
                p_strip.startswith('[[TITLE]]') or
                p_strip.startswith('[[PART]]') or
                p_strip.startswith('[[AUTHOR]]') or
                p_strip.startswith('[[EPIGRAPH]]')
            )
            if is_title_tag:
                title_paras.append(p)
            else:
                in_body = True
                body_paras.append(p)

    return '\n\n'.join(title_paras), '\n\n'.join(body_paras)



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


# ================================================================
# MAIN PIPELINE
# ================================================================

# ================================================================
# FRONT MATTER HANDLING
# ================================================================




def detect_page_type(page, page_num=None):
    """Detect if a page is TOC, Title, or Body text based on visual structure."""
    text_upper = page.get_text().upper()
    is_volume_title = bool(re.search(r'THE\s+WORKS\s+OF\s+JOHN\s+OWEN', text_upper))
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if b.get('type') == 0]
    n_blocks = len(text_blocks)

    # TOC detection: any CONTENTS page OR pages with many numbered/chapter items
    if 'CONTENTS' in text_upper and (n_blocks > 5 or 'CONTENTS OF VOLUME' in text_upper):
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


def generate_abbreviations_guide_html(vol_num: int) -> str:
    """Generate a premium Table of Abbreviations & Citations Guide page for the front matter."""
    return f'''<section class="front-matter-section abbreviations-guide-page">
<h2 class="front-matter-heading">Abbreviations &amp; Scholarly Citations Guide</h2>

<p class="front-matter-prose first">To preserve the flow of John Owen’s theological treatises while providing modern readers with standard academic context, this digital edition employs standardized abbreviation codes in all editorial footnotes. Below is a comprehensive guide to these references, matching the standards found in modern Reformed theological scholarship (such as the <em>Institutes of Elenctic Theology</em> and <em>Reformed Systematic Theology</em>):</p>

<table class="abbreviations-table">
  <tr class="abbr-row">
    <td class="abbr-code">NPNF1</td>
    <td class="abbr-desc"><strong>Nicene and Post-Nicene Fathers, First Series</strong> (Philip Schaff, ed., 14 vols.). Standard English translation of Augustine and John Chrysostom.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">NPNF2</td>
    <td class="abbr-desc"><strong>Nicene and Post-Nicene Fathers, Second Series</strong> (Philip Schaff and Henry Wace, eds., 14 vols.). Standard English translation of Ambrose, Basil, Gregory of Nyssa, Gregory the Great, and Jerome.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">ANF</td>
    <td class="abbr-desc"><strong>Ante-Nicene Fathers</strong> (Alexander Roberts and James Donaldson, eds., 10 vols.). English translation of early patristics prior to Nicea (e.g., Justin Martyr, Irenaeus, Tertullian, Origen, Cyprian).</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">PL</td>
    <td class="abbr-desc"><strong>Patrologia Latina</strong> (Jacques-Paul Migne, ed., 221 vols.). The authoritative compilation of Latin patristic and medieval writers, including Augustine, Ambrose, Prosper of Aquitaine, Fulgentius, and Bernard of Clairvaux.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">PG</td>
    <td class="abbr-desc"><strong>Patrologia Graeca</strong> (Jacques-Paul Migne, ed., 161 vols.). The authoritative compilation of Greek patristic writers, including John Chrysostom, Basil of Caesarea, Athanasius of Alexandria, and Gregory of Nyssa.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">ST</td>
    <td class="abbr-desc"><strong>Summa Theologiae</strong> (Thomas Aquinas). Reference coordinates denote Part (e.g., I, I-II, II-II, III), Question (Q.), Article (Art.), and Reply (ad).</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">LCC</td>
    <td class="abbr-desc"><strong>Library of Christian Classics</strong> (Westminster Press). Volumes 20–21 comprise the standard English edition of John Calvin’s <em>Institutes of the Christian Religion</em>.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">Battles</td>
    <td class="abbr-desc">Ford Lewis Battles, translator of the definitive 1960 English edition of John Calvin’s <em>Institutes of the Christian Religion</em>.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">LXX</td>
    <td class="abbr-desc"><strong>Septuagint</strong>. The ancient Greek translation of the Hebrew Scriptures (Old Testament), frequently cited by early Christian authors.</td>
  </tr>
  <tr class="abbr-row">
    <td class="abbr-code">ED</td>
    <td class="abbr-desc"><strong>Editor’s Note</strong>. Indicates annotations added by William H. Goold, the definitive 19th-century editor of Owen's Works, or the modern editorial team.</td>
  </tr>
</table>

<p class="front-matter-prose" style="margin-top: 1.5em;"><strong>Note on Bible Translations:</strong> Scripture citations followed by the designation <em>“margin”</em> denote alternative readings or explanatory notes found in the margins of the 1611 Authorized Version (King James Bible), which Owen and his contemporaries frequently consulted.</p>
</section>
'''


def apply_inline_translations(body_html: str) -> str:
    """Scan and substitute centralized inline translations in body HTML."""
    from scripts.translation_db import INLINE_TRANSLATIONS
    for phrase, trans in INLINE_TRANSLATIONS.items():
        words = phrase.split()
        if not words:
            continue
        phrase_pat = r'\s+'.join(re.escape(w) for w in words)
        pattern = re.compile(
            rf'(<span\s+lang="la"[^>]*>\s*{phrase_pat}\s*</span>|{phrase_pat})(?!\s*(?:[\.,\?!:;\'"“”’]*\s*)?\[Translated:)([\.,\?!:;\'"“”’]*)',
            re.DOTALL
        )
        if pattern.search(body_html):
            body_html = pattern.sub(rf'\1\2 [Translated: {trans}]', body_html)
    return body_html


def replace_first_outside_tags_and_comments(body_html: str, pattern: re.Pattern, replace_fn) -> tuple[str, bool]:
    """Search for all matches of pattern, replacing the first occurrence that does not fall inside HTML tags or comments."""
    exclusion_spans = []
    for m_ex in re.finditer(r'<!--.*?-->|<[^>]+>', body_html, re.S):
        exclusion_spans.append(m_ex.span())

    def is_excluded(pos):
        return any(start <= pos < end for start, end in exclusion_spans)

    for m in pattern.finditer(body_html):
        term_pos = m.start(1)
        if not is_excluded(term_pos):
            replacement = replace_fn(m)
            body_html = body_html[:m.start()] + replacement + body_html[m.end():]
            return body_html, True

    return body_html, False


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
        SBL_SUPPLEMENTS, EZRA_SIL_FILES, TITLE_PAGE_FONTS, GFS_PORSON_FILES,
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
    for ch in intermediate.get('chapters', []):
        if 'title' in ch:
            ch['title'] = _repair_owen_ocr_errors(ch['title'], config=config)

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
    for _font_dict in (SBL_SUPPLEMENTS, EZRA_SIL_FILES, PROXIMA_NOVA_FILES, TITLE_PAGE_FONTS, GFS_PORSON_FILES, CARDO_FILES, GENTIUM_PLUS_FILES):
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
    added_abbreviations_guide = False
    for fm in intermediate.get('front_matter_items', []):
        if fm['title'] == _last_fm_title:
            continue
        _last_fm_title = fm['title']

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
        if fm.get('type') == 'toc' and fm.get('file_name', '').startswith('contents_'):
            fm['title'] = 'Original Printed Contents'

        fm_item.set_content(
            _make_xhtml(fm['title'], fm_html).encode('utf-8')
        )
        fm_item.add_item(style_item)
        book.add_item(fm_item)
        front_matter_epub_items.append(fm_item)

        # Relocate Publication Metadata (copyright/colophon page) immediately after the main Title Page
        if fm.get('type') == 'title_page' and not copyright_added:
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

        if fm.get('type') == 'toc' and not added_abbreviations_guide:
            abbr_item = epub.EpubHtml(
                title='Abbreviations & Scholarly Citations',
                file_name='abbreviations_guide.xhtml',
                lang='en',
            )
            abbr_html = generate_abbreviations_guide_html(vol_num)
            abbr_item.set_content(_make_xhtml('Abbreviations & Scholarly Citations', abbr_html).encode('utf-8'))
            abbr_item.add_item(style_item)
            book.add_item(abbr_item)
            front_matter_epub_items.append(abbr_item)
            added_abbreviations_guide = True

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

    if not added_abbreviations_guide:
        abbr_item = epub.EpubHtml(
            title='Abbreviations & Scholarly Citations',
            file_name='abbreviations_guide.xhtml',
            lang='en',
        )
        abbr_html = generate_abbreviations_guide_html(vol_num)
        abbr_item.set_content(_make_xhtml('Abbreviations & Scholarly Citations', abbr_html).encode('utf-8'))
        abbr_item.add_item(style_item)
        book.add_item(abbr_item)
        front_matter_epub_items.append(abbr_item)
        added_abbreviations_guide = True

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
    all_glossary_notes = []
    all_biographical_notes = []
    seen_body_translations = set()
    seen_glossary_terms = set()
    seen_biographical_terms = set()
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

        # Skip explicitly excluded chapters (e.g. raw printed Table of Contents pages)
        if ch_dict['title'] in config.get('exclude_chapters', []):
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
            title_block, body_text = _split_raw_title_body(raw_text)
            foreign_frags = _foreign_fragments_in_section(title_block or raw_text)
            overridden_title = _merge_titlepage_override(titlepage_override, foreign_frags)
            if body_text:
                raw_text = f"{overridden_title}\n\n{body_text}"
            else:
                raw_text = overridden_title
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

        # Centralized inline translations scanning and substitution
        body_html = apply_inline_translations(body_html)

        # Dynamic translation notes scanning and substitution
        from scripts.translation_db import BODY_TRANSLATIONS
        from scripts.patristic_refs import expand_inline_citations
        import html
        sorted_phrases = sorted(BODY_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
        local_notes = []
        placeholders = {}
        placeholder_counter = 0
        trans_counter = 0
        cid = ch_dict['cid']

        # Clean and map helper for tag-agnostic matching
        def clean_and_map(orig_str):
            stripped_chars = []
            map_to_orig = []
            i = 0
            n = len(orig_str)
            while i < n:
                if orig_str[i] == '<':
                    # Skip tag
                    while i < n and orig_str[i] != '>':
                        i += 1
                    i += 1 # skip '>'
                elif orig_str[i] == '&':
                    # Find end of entity
                    j = i + 1
                    while j < n and orig_str[j] != ';' and (j - i) < 10:
                        j += 1
                    if j < n and orig_str[j] == ';':
                        entity = orig_str[i:j+1]
                        decoded = html.unescape(entity)
                        for char in decoded:
                            stripped_chars.append(char)
                            map_to_orig.append(i) # map to start of entity
                        i = j + 1
                    else:
                        stripped_chars.append(orig_str[i])
                        map_to_orig.append(i)
                        i += 1
                else:
                    stripped_chars.append(orig_str[i])
                    map_to_orig.append(i)
                    i += 1
            return "".join(stripped_chars), map_to_orig

        def make_quote_agnostic(phrase):
            words = phrase.split()
            escaped_words = []
            for w in words:
                escaped = re.escape(w)
                escaped = escaped.replace(r"\'", "'").replace("'", r"['’‘]")
                escaped = escaped.replace(r'\"', '"').replace('"', r'["“”]')
                escaped_words.append(escaped)
            return r'\s+'.join(escaped_words)

        # Initialize clean text and mapping once per chapter
        clean_text, mapping = clean_and_map(body_html)
        dirty = False

        for phrase, trans in sorted_phrases:
            if phrase in seen_body_translations:
                continue

            if dirty:
                clean_text, mapping = clean_and_map(body_html)
                dirty = False

            first_char = phrase[0]
            last_char = phrase[-1]
            lb = ""
            la = ""
            if '\u0590' <= first_char <= '\u05ff':
                lb = r'(?<![\u0590-\u05ff־-])'
            elif ('\u0370' <= first_char <= '\u03ff' or '\u1f00' <= first_char <= '\u1fff'):
                lb = r'(?<![\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f־-])'
            elif first_char.isalnum():
                lb = r'(?<![a-zA-Z0-9\u0300-\u036f])'

            if '\u0590' <= last_char <= '\u05ff':
                la = r'(?![\u0590-\u05ff־-])'
            elif ('\u0370' <= last_char <= '\u03ff' or '\u1f00' <= last_char <= '\u1fff'):
                la = r'(?![\u0370-\u03ff\u1f00-\u1fff\u0300-\u036f־-])'
            elif last_char.isalnum():
                la = r'(?![a-zA-Z0-9\u0300-\u036f])'

            phrase_regex = make_quote_agnostic(phrase)
            pattern = re.compile(rf'{lb}{phrase_regex}{la}', re.I)

            match = pattern.search(clean_text)
            if match:
                start_idx = match.start()
                end_idx = match.end()

                orig_start = mapping[start_idx]
                orig_end = mapping[end_idx] if end_idx < len(mapping) else len(body_html)

                punc_match = re.match(r'^((?:</[a-zA-Z]+>)*)([\.,\?!:;\'"“”’]*)', body_html[orig_end:])
                if punc_match:
                    trailing_tags = punc_match.group(1)
                    trailing_punc = punc_match.group(2)
                else:
                    trailing_tags = ""
                    trailing_punc = ""
                orig_end_with_punc = orig_end + len(trailing_tags) + len(trailing_punc)

                matched_str = body_html[orig_start:orig_end]

                trans_counter += 1
                placeholder_counter += 1

                fn_link = f'<sup><a class="noteref noteref-trans" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fntrans_{cid}_{trans_counter}">†</a></sup>'
                local_notes.append({
                    'id': f"fntrans_{cid}_{trans_counter}",
                    'num': trans_counter,
                    'phrase': phrase,
                    'translation': trans,
                    'type': 'translation'
                })

                placeholder_key = f"__BODY_TRANS_PH_{placeholder_counter}__"
                placeholders[placeholder_key] = (matched_str, trailing_tags, trailing_punc, fn_link)
                replacement = placeholder_key

                body_html = body_html[:orig_start] + replacement + body_html[orig_end_with_punc:]
                seen_body_translations.add(phrase)
                dirty = True

        # Call patristic citation resolution fallback while placeholders are active (prevents matching inside translated phrases)
        body_html, citation_notes, trans_counter = expand_inline_citations(
            body_html,
            cid=cid,
            trans_notes=local_notes,
            trans_counter=trans_counter
        )

        if local_notes:
            all_translation_notes.extend(local_notes)

        # Dynamic Glossary Notes scanning (First Occurrence Only in the book)
        from scripts.technical_glossary import apply_glossary_footnotes
        body_html, local_glossary, seen_glossary_terms = apply_glossary_footnotes(
            body_html, cid, seen_glossary_terms, replace_first_outside_tags_and_comments
        )

        if local_glossary:
            all_glossary_notes.extend(local_glossary)

        # Dynamic Biographical Notes scanning (First Occurrence Only in the book)
        from scripts.biography_db import BIOGRAPHICAL_DB
        local_biographical = []
        biographical_counter = 0

        sorted_biog_terms = sorted(BIOGRAPHICAL_DB.items(), key=lambda x: len(x[0]), reverse=True)
        for term, definition in sorted_biog_terms:
            if term in seen_biographical_terms:
                continue

            pattern = re.compile(
                rf'(?<![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
                rf'({re.escape(term)}(?:s|es)?)'
                rf'(?![a-zA-Z0-9\u0370-\u03ff\u1f00-\u1fff\u0590-\u05ff\u0300-\u036f־-])'
                rf'((?:</[a-zA-Z]+>)*)'
                rf'([\.,\?!:;\'"“”’]*)',
                re.I
            )
            def replace_biographical(m):
                nonlocal biographical_counter
                biographical_counter += 1
                matched_str = m.group(1)
                trailing_tags = m.group(2)
                trailing_punc = m.group(3)
                # Double dagger symbol (‡) for biographical notes (Rule 11)
                fn_link = f'<sup><a class="noteref noteref-biographical" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fnbiog_{cid}_{biographical_counter}">‡</a></sup>'
                local_biographical.append({
                    'id': f"fnbiog_{cid}_{biographical_counter}",
                    'term': term,
                    'definition': definition
                })
                return f"{matched_str}{trailing_tags}{trailing_punc}{fn_link}"

            body_html, replaced = replace_first_outside_tags_and_comments(body_html, pattern, replace_biographical)
            if replaced:
                seen_biographical_terms.add(term)

        if local_biographical:
            all_biographical_notes.extend(local_biographical)

        # Restore all translation placeholders, placing their footnote links after punctuation (Rule 11)
        for ph_key, (matched_str, trailing_tags, trailing_punc, fn_link) in placeholders.items():
            body_html = body_html.replace(ph_key, f"{matched_str}{trailing_tags}{trailing_punc}{fn_link}")

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
    if footnote_map or all_translation_notes or all_glossary_notes or all_biographical_notes:
        endnotes_html = build_endnotes_chapter(footnote_map, style_item, vol_num=vol_num, trans_notes=all_translation_notes, glossary_notes=all_glossary_notes, config=config, biographical_notes=all_biographical_notes)
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
    _nav_seen_files: set = set()
    _nav_prefix: list = []
    if cover_page:
        _nav_prefix.append((1, 'Cover', 'cover.xhtml'))
        _nav_seen_titles.add('Cover')
        _nav_seen_files.add('cover.xhtml')
    for _fm in intermediate.get('front_matter_items', []):
        _fm_title = _fm.get('title', '')
        _fm_html = _fm.get('html')
        _fm_fn = _fm.get('file_name', '')
        if _fm_html is None:
            continue
        if _fm_title and _fm_title not in _nav_seen_titles and _fm_fn not in _nav_seen_files:
            _nav_prefix.append((1, _fm_title, _fm_fn))
            _nav_seen_titles.add(_fm_title)
            _nav_seen_files.add(_fm_fn)
    # Also add any prose front-matter items (Preface, Analysis, etc.) not yet listed
    for _fm_item in front_matter_epub_items:
        _fmt = getattr(_fm_item, 'title', None) or ''
        _fmf = getattr(_fm_item, 'file_name', None) or ''
        if _fmt and _fmt not in _nav_seen_titles and _fmf and _fmf not in _nav_seen_files:
            _nav_prefix.append((1, _fmt, _fmf))
            _nav_seen_titles.add(_fmt)
            _nav_seen_files.add(_fmf)
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
    nav_item.set_content(nav_html.encode('utf-8'))
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
    spine.append(nav_item)  # Insert the perfectly linked, interactive TOC into the reading flow!
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
