#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   John Owen Works — PDF to EPUB Converter                    ║
║   Banner of Truth Edition                                    ║
╚══════════════════════════════════════════════════════════════╝

Converts the AGES Digital Library PDFs of John Owen's 16-volume
Works into clean, modern EPUBs with:

  • Unicode Greek (converted from AGES Koine-Medium Beta Code)
  • Hebrew passages preserved as-is (not garbled)
  • Footnotes extracted and linked (FT/ft markers → endnotes)
  • Quoted passages italicised
  • Proper paragraph flow (PDF page breaks merged)
  • Banner of Truth cover images
  • Embedded Lora font for elegant reading

USAGE:
    python3 convert_owen_to_epub.py [folder_path]

    folder_path  — path to the folder containing the PDFs.
                   Defaults to the current directory.

FOLDER STRUCTURE EXPECTED:
    folder/
    ├── [John_Owen]_Works_of_John_Owen_vol_01.pdf
    ├── [John_Owen]_Works_of_John_Owen_vol_02.pdf
    ├── ...
    ├── covers/
    │   ├── v1.jpg      (or .png)
    │   ├── v2.jpg
    │   └── ...v16.jpg
    └── (output EPUBs will be written here)

FONT:
    The script looks for Google's Lora font in common system locations.
    If not found, it falls back to a CSS-only font stack (Georgia, serif).
    To embed Lora, install it:
      • macOS:  brew install --cask font-lora
      • Linux:  sudo apt install fonts-lora  (or download from Google Fonts)
      • Or place Lora-Variable.ttf and Lora-Italic-Variable.ttf in a
        "fonts/" folder next to this script.

REQUIREMENTS:
    pip install pypdf ebooklib
"""

import re
import os
import sys
import glob
import unicodedata
from html import escape

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("ERROR: 'pypdf' is required. Install with:  pip install pypdf")

try:
    from ebooklib import epub
except ImportError:
    sys.exit("ERROR: 'ebooklib' is required. Install with:  pip install ebooklib")


# ╔══════════════════════════════════════════════════════════════╗
# ║  VOLUME METADATA                                            ║
# ╚══════════════════════════════════════════════════════════════╝

VOLUME_SUBTITLES = {
    1:  "The Glory of Christ",
    2:  "Communion with God",
    3:  "The Holy Spirit",
    4:  "The Work of the Spirit",
    5:  "Faith and Its Evidences",
    6:  "Temptation and Sin",
    7:  "Sin and Grace",
    8:  "Sermons to the Nation",
    9:  "Sermons to the Church",
    10: "The Death of Christ",
    11: "Continuing in the Faith",
    12: "The Gospel Defended",
    13: "Ministry and Fellowship",
    14: "True and False Religion",
    15: "Church Purity and Unity",
    16: "The Church and the Bible",
}


# ╔══════════════════════════════════════════════════════════════╗
# ║  AGES BETA CODE → UNICODE GREEK CONVERTER                  ║
# ╚══════════════════════════════════════════════════════════════╝
#
# The AGES Digital Library used a font called "Koine-Medium" that
# maps ASCII characters to Greek glyphs. This converter turns that
# encoding back into proper Unicode polytonic Greek.

GREEK_LOWER = {
    'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε',
    'z': 'ζ', 'h': 'η', 'q': 'θ', 'i': 'ι', 'k': 'κ',
    'l': 'λ', 'm': 'μ', 'n': 'ν', 'x': 'ξ', 'o': 'ο',
    'p': 'π', 'r': 'ρ', 's': 'σ', 't': 'τ',
    'u': 'υ', 'f': 'φ', 'c': 'χ', 'y': 'ψ', 'w': 'ω',
}
GREEK_UPPER = {
    'A': 'Α', 'B': 'Β', 'G': 'Γ', 'D': 'Δ', 'E': 'Ε',
    'Z': 'Ζ', 'H': 'Η', 'Q': 'Θ', 'I': 'Ι', 'K': 'Κ',
    'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'X': 'Ξ', 'O': 'Ο',
    'P': 'Π', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ',
    'U': 'Υ', 'F': 'Φ', 'C': 'Χ', 'Y': 'Ψ', 'W': 'Ω',
}
ALL_GREEK = {**GREEK_LOWER, **GREEK_UPPER}

# Unicode combining diacritical marks
SMOOTH     = '\u0313'   # smooth breathing  (psili)
ROUGH      = '\u0314'   # rough breathing   (dasia)
ACUTE      = '\u0301'   # acute accent
GRAVE      = '\u0300'   # grave accent
CIRCUMFLEX = '\u0342'   # circumflex        (perispomeni)
IOTASUB    = '\u0345'   # iota subscript

# How AGES diacritic characters map to Unicode combining marks:
#   j = smooth breathing         J = rough breathing
#   > = acute accent             < = grave accent
#   ~ = circumflex               = = circumflex (alternate)
#   ] = smooth + acute           } = smooth + acute (alternate)
#   [ = rough + acute            { = rough + acute  (alternate)
#   | = iota subscript
DIACRITIC_CHARS = set('><=~]J[j}|{=')
DIACRITIC_MAP = {
    'j': (SMOOTH,),       'J': (ROUGH,),
    '>': (ACUTE,),        '<': (GRAVE,),
    '~': (CIRCUMFLEX,),   '=': (CIRCUMFLEX,),
    ']': (SMOOTH, ACUTE), '}': (SMOOTH, ACUTE),
    '[': (ROUGH, ACUTE),  '{': (ROUGH, ACUTE),
    '|': (IOTASUB,),
}


def _convert_greek_word(word):
    """Convert a single AGES Beta Code word to Unicode Greek."""
    result = []
    i = 0
    while i < len(word):
        ch = word[i]
        if ch in GREEK_LOWER:
            result.append(GREEK_LOWER[ch])
            i += 1
        elif ch in GREEK_UPPER:
            result.append(GREEK_UPPER[ch])
            i += 1
        elif ch == 'v':                        # final sigma ς
            result.append('ς')
            i += 1
        elif ch in DIACRITIC_CHARS and result:
            if ch in DIACRITIC_MAP:
                for c in DIACRITIC_MAP[ch]:
                    result.append(c)
            i += 1
            continue
        else:
            result.append(ch)
            i += 1
            continue
        # Consume any diacritics immediately following the letter
        while i < len(word) and word[i] in DIACRITIC_CHARS:
            d = word[i]
            if d in DIACRITIC_MAP:
                for c in DIACRITIC_MAP[d]:
                    result.append(c)
            i += 1
    return unicodedata.normalize('NFC', ''.join(result))


def _has_ages_diacritics(word):
    """Does this word contain AGES Beta Code diacritics (i.e., is it Greek)?"""
    # Hebrew uses digits and semicolons — skip those
    if re.search(r'[\d;]', word):
        return False
    # Non-ASCII characters (µ, Õ, etc.) are Hebrew font artefacts, not Greek
    if re.search(r'[^\x00-\x7f]', word):
        return False
    # The word stripped of diacritics must consist entirely of Beta Code
    # letters.  This catches Hebrew tokens that contain }, { etc. but
    # have non-Beta-Code letter sequences (e.g. "µyh}loaÕAlK").
    cleaned = re.sub(r'[><=~\]\[\}\{|Jj]', '', word)
    if cleaned and not all(c in ALL_GREEK or c == 'v' for c in cleaned):
        return False
    # Strong indicators that never appear in English prose
    # ~ and = are both circumflex markers, | is iota subscript
    if re.search(r'[~|=]', word):
        return True
    # ] [ } { are Greek ONLY when BETWEEN a vowel and a letter within
    # a word (not at the end — that's an English bracket).
    # e.g. a]sarkov ✓   also] ✗   e[n ✓
    if re.search(r'[aehiouw][\]\[\}\{][a-zA-Z]', word):
        return True
    # > after a lowercase letter = acute accent
    if re.search(r'[a-z]>', word):
        return True
    # < after a vowel = grave accent
    if re.search(r'[aehiouw]<', word):
        return True
    # J after a vowel = rough breathing, but only if the whole word
    # is plausible Beta Code (avoids "prejudice", "project", etc.)
    if re.search(r'[aehiouw]J', word):
        if cleaned and all(c in ALL_GREEK or c == 'v' for c in cleaned):
            return True
    return False


# Common Greek particles that appear without any diacritics
_GREEK_COMMON = frozenset({
    'kai', 'de', 'te', 'men', 'gar', 'dia', 'ek', 'en', 'epi',
    'kata', 'meta', 'para', 'peri', 'pro', 'sun', 'anti',
    'tou', 'ton', 'thn', 'twn', 'tov', 'toi', 'to', 'ta',
    'estin', 'einai', 'esti', 'mh', 'ou', 'ouk', 'ouc',
    'oti', 'alla', 'autov',
})

# Common short English words whose letters all happen to map to Greek
_ENGLISH_COMMON = frozenset({
    'a', 'an', 'at', 'be', 'but', 'can', 'do', 'for', 'get', 'go',
    'got', 'had', 'has', 'he', 'held', 'her', 'him', 'his', 'hot',
    'if', 'in', 'is', 'it', 'its', 'let', 'man', 'me', 'met', 'mine',
    'must', 'no', 'nor', 'not', 'of', 'on', 'one', 'or', 'our',
    'out', 'own', 'put', 'ran', 'run', 'set', 'so', 'sum', 'sun',
    'ten', 'that', 'the', 'them', 'then', 'this', 'thus', 'till',
    'time', 'tin', 'tip', 'tone', 'too', 'top', 'tub', 'turn',
    'up', 'upon', 'us', 'use', 'using', 'vast', 'was', 'we',
    'went', 'were', 'will', 'win', 'with', 'won', 'work', 'bore',
    'come', 'done', 'even', 'ever', 'from', 'give', 'have', 'here',
    'into', 'just', 'like', 'long', 'make', 'more', 'much', 'name',
    'once', 'over', 'same', 'some', 'take', 'than', 'very', 'what',
    'when', 'whom', 'been', 'also', 'book', 'both', 'each', 'good',
    'great', 'keep', 'last', 'life', 'look', 'most', 'next', 'other',
    'part', 'place', 'see', 'seem', 'sent', 'since', 'still',
    'such', 'tell', 'them', 'true', 'under', 'well', 'which',
    'while', 'about', 'after', 'before', 'being', 'could', 'first',
    'given', 'know', 'made', 'might', 'mind', 'never', 'other',
    'right', 'said', 'shall', 'should', 'state', 'their', 'these',
    'thing', 'think', 'those', 'three', 'under', 'until', 'where',
    'whole', 'whose', 'would', 'write', 'psalm', 'god', 'lord',
    'sin', 'son', 'word', 'grace', 'faith', 'hope', 'love',
})


def _is_plausible_greek(word):
    """Could this plain word (no diacritics) be Greek in context?"""
    wl = word.lower()
    if wl in _ENGLISH_COMMON:
        return False
    if all(c in ALL_GREEK or c == 'v' for c in word):
        if wl in _GREEK_COMMON:
            return True
    return False


def convert_greek(text):
    """Convert AGES Beta Code Greek in mixed English/Greek text to Unicode."""
    # Remove AGES scripture reference codes: <401616>, <19D001>, etc.
    text = re.sub(r'<[\dA-Z]{5,8}>', '', text)

    # --- Pre-process AGES font artefacts ---
    # The AGES Koine-Medium font sometimes produces non-ASCII characters
    # when the PDF is extracted.  Map known Greek-context artefacts back
    # to their ASCII Beta Code equivalents so the converter can handle them.
    # Ò (U+00D2) = capital O with opening quote-like mark → O (omicron)
    # Ó (U+00D3) = closing quote mark artefact → strip (punctuation)
    # Õ (U+00D5) = appears mid-Greek-word → strip (ligature artefact)
    # Ñ (U+00D1) = dash-like separator in Greek → — (em-dash)
    text = text.replace('\u00d2', 'O')    # Ò → O
    text = text.replace('\u00d3', '')      # Ó → remove
    text = text.replace('\u00d5', '')      # Õ → remove
    text = text.replace('\u00d1', '—')     # Ñ → em-dash

    # Remove Private Use Area characters (e.g. U+F8E7 renders as ||||
    # in EPUB readers — it's an AGES font glyph with no Unicode meaning)
    text = re.sub(r'[\uE000-\uF8FF]', '', text)

    # Strip AGES font-change marker '+' before a Greek/Latin letter
    # (e.g. "+W" at the start of a Greek passage → "W")
    text = re.sub(r'\+(?=[A-Za-z])', '', text)
    # Separate brackets that are English punctuation from adjacent text,
    # while preserving brackets that are AGES Greek diacritics.
    # Greek diacritics: ] [ } { appear BETWEEN a vowel and a consonant
    # WITHIN a word (e.g. a]sarkov, e[n).  English brackets appear at
    # word boundaries (e.g. [also], [but]).
    #
    # '[' before a letter: separate unless preceded by a Beta Code vowel
    text = re.sub(r'(?<![aehiouwAEHIOUW])\[([A-Za-z])', r'[ \1', text)
    # ']' after a letter: separate unless followed by a letter (Greek
    # diacritics are always mid-word, never at word end)
    text = re.sub(r'([A-Za-z])\](?![A-Za-z])', r'\1 ]', text)

    tokens = re.split(r'(\s+|[,;:\.!?\(\)"""\'—\-–]+)', text)
    result = []
    in_greek = False

    for idx, token in enumerate(tokens):
        if not token:
            result.append(token)
            continue
        if re.match(r'^[\s,;:\.!?\(\)"""\'—\-–]+$', token):
            result.append(token)
            if re.search(r'[\.!?]', token):
                in_greek = False
            continue

        if _has_ages_diacritics(token):
            result.append(_convert_greek_word(token))
            in_greek = True
        elif re.match(r'^[a-zA-Z]+$', token) and len(token) <= 15:
            # Look for Greek neighbors even when in_greek is False
            # (catches words at the START of a Greek passage)
            has_greek_neighbor = any(
                0 <= idx + off < len(tokens) and _has_ages_diacritics(tokens[idx + off])
                for off in (-4, -3, -2, -1, 1, 2, 3, 4)
            )
            if has_greek_neighbor and (in_greek or _is_plausible_greek(token)):
                result.append(_convert_greek_word(token))
                in_greek = True
            elif in_greek and _is_plausible_greek(token):
                result.append(_convert_greek_word(token))
            else:
                result.append(token)
                in_greek = False
        else:
            result.append(token)
            in_greek = False

    # --- Second pass: convert straggler Latin words near Greek text ---
    # After the first pass, some words at the very start/end of a Greek
    # quote may still be unconverted.  Scan the joined text for Latin-
    # alphabet words that have Greek Unicode characters nearby.
    joined = ''.join(result)
    _greek_range = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')

    # Quote characters that indicate a language boundary (Greek ↔ English)
    _quote_chars = set('"\u201c\u201d\u0022')

    def _fix_straggler(m):
        word = m.group(0)
        # Skip words that aren't valid Beta Code characters
        if not all(c in ALL_GREEK or c == 'v' for c in word):
            return word
        wl = word.lower()
        # Never convert known English words in this pass
        if wl in _ENGLISH_COMMON:
            return word
        # Never convert long words (>5 letters) — real Greek stragglers
        # are short articles/particles at passage edges
        if len(word) > 5:
            return word

        # Use a TIGHT window — only the immediately adjacent characters
        before_txt = joined[max(0, m.start() - 8):m.start()]
        after_txt  = joined[m.end():m.end() + 8]
        greek_before = bool(_greek_range.search(before_txt))
        greek_after  = bool(_greek_range.search(after_txt))

        # Check for quote boundaries — if a quote character sits between
        # this word and the nearby Greek, we're in a different language zone
        quote_before = any(c in _quote_chars for c in before_txt)
        quote_after  = any(c in _quote_chars for c in after_txt)

        if greek_before and greek_after:
            # Only convert if no quote boundary on either side
            if quote_before or quote_after:
                return word    # English word between Greek quotes
            return _convert_greek_word(word)

        if greek_after and not greek_before:
            # At the START of a Greek passage — preceded by quote/punct
            before_stripped = before_txt.rstrip()
            if not before_stripped or before_stripped[-1] in '"\u201c\u201d:;,({':
                return _convert_greek_word(word)

        if greek_before and not greek_after:
            # At the END of a Greek passage — followed by quote/punct
            after_stripped = after_txt.lstrip()
            if not after_stripped or after_stripped[0] in '"\u201c\u201d.;,)}':
                return _convert_greek_word(word)

        return word

    joined = re.sub(r'\b[a-zA-Z]{1,12}\b', _fix_straggler, joined)

    # --- Third pass: rejoin Greek fragments split by stray periods ---
    # PDF extraction sometimes inserts a period mid-word (e.g. "ἀναι.δειαν").
    # If a Greek word fragment is followed by '.' and then another Greek
    # fragment (no space), stitch them back together.
    joined = re.sub(
        r'([\u0370-\u03FF\u1F00-\u1FFF]+)\.([\u0370-\u03FF\u1F00-\u1FFF]+)',
        r'\1\2',
        joined
    )

    return joined


# ╔══════════════════════════════════════════════════════════════╗
# ║  PDF TEXT EXTRACTION                                        ║
# ╚══════════════════════════════════════════════════════════════╝

def extract_footnotes(reader, total_pages):
    """Find the footnote section at the end of the PDF and parse it.

    Scans backwards from the end to find ALL pages containing FT markers,
    even if there are gaps (pages without FT markers interspersed).  The
    body-end boundary is the first FT-bearing page found.
    """
    # Scan backwards to find all footnote pages in the tail of the PDF.
    # We allow gaps of up to 5 non-FT pages within the footnote section
    # (some AGES volumes interleave blank/title pages).
    ft_pages = []
    gap = 0
    max_gap = 5  # allow up to 5 consecutive non-FT pages within the section

    for pg in range(total_pages - 1, max(total_pages - 80, 0), -1):
        text = reader.pages[pg].extract_text() or ""
        if re.search(r'^(?:FT|ft)\d+\s', text, re.MULTILINE) or 'FOOTNOTES' in text:
            ft_pages.append(pg)
            gap = 0
        else:
            if ft_pages:
                gap += 1
                if gap > max_gap:
                    break  # too many consecutive non-FT pages — we've left the section

    if not ft_pages:
        return {}, total_pages

    ft_start = min(ft_pages)

    # Gather text from all pages from ft_start to the end
    ft_text = ""
    for pg in range(ft_start, total_pages):
        ft_text += "\n" + (reader.pages[pg].extract_text() or "")

    footnotes = {}
    for m in re.finditer(r'(?:FT|ft)(\d+)\s+(.*?)(?=\n(?:FT|ft)\d+|\Z)', ft_text, re.DOTALL):
        num = m.group(1)
        footnotes[num] = convert_greek(m.group(2).strip())

    return footnotes, ft_start


def extract_pages(reader, end_page):
    """Extract raw text from each body page."""
    return [(i + 1, reader.pages[i].extract_text() or "") for i in range(end_page)]


def detect_chapters(pages):
    """Detect chapter/section boundaries from extracted pages."""
    chapters = []
    current_title = "Front Matter"
    current_text = []

    chapter_re = re.compile(
        r'^((?:CHAPTER|SERMON|DISCOURSE|EXERCITATION)\s+\d+[^\n]*)$',
        re.MULTILINE
    )

    # Major work divisions found across all 16 Owen volumes
    major_titles = [
        r'CRISTOLOGIA\s*:?\s*(?:OR\b)?',
        r'CHRISTOLOGIA\b',
        r'MEDITATIONS AND DISCOURSES',
        r'A BRIEF DECLARATION AND VINDICATION',
        r'TWO SHORT CATECHISMS',
        r'THE DIVINE ORIGINAL',
        r'OF COMMUNION WITH GOD',
        r'A DISCOURSE OF THE',
        r'A DISCOURSE CONCERNING',
        r'VINDICIAE EVANGELICAE',
        r'OF THE DEATH OF CHRIST',
        r'A REVIEW OF THE',
        r'AN EXPOSITION OF',
        r'THE DOCTRINE OF',
        r'ON THE MORTIFICATION',
        r'OF THE NATURE.*SIN',
        r'THE GRACE AND DUTY',
        r'PNEUMATOLOGIA',
        r'A TREATISE OF',
        r'THE REASON OF FAITH',
        r'THE CAUSES.*WAYS.*MEANS',
        r'AN INQUIRY INTO',
        r'EXERCITATIONS',
        r'GENERAL PREFACE',
        r'CONTENTS OF VOL',
    ]
    major_re = re.compile(
        r'^(' + '|'.join(major_titles) + r').*$',
        re.MULTILINE | re.IGNORECASE
    )

    section_re = re.compile(
        r'^((?:PREFACE|DEDICATION|EPISTLE DEDICATORY|PREFATORY NOTE|'
        r'THE EPISTLE TO THE READER|TO THE READER|NOTE TO THE READER|'
        r'AN INTRODUCTORY|APPENDIX|SUPPLEMENT|'
        r'Digression\s+\d+|Part\s+\d+)[\.\s]?.*)$',
        re.MULTILINE
    )

    for page_num, text in pages:
        if page_num <= 2:
            continue

        lines = text.split('\n')
        # Strip leading page number
        if lines and re.match(r'^\d+\s*$', lines[0].strip()):
            lines = lines[1:]

        page_text = '\n'.join(lines).strip()
        if not page_text:
            continue

        first_lines = '\n'.join(lines[:5])
        found = False

        for regex in (major_re, chapter_re, section_re):
            m = regex.search(first_lines)
            if m:
                if current_text:
                    chapters.append((current_title, '\n\n'.join(current_text)))
                current_title = re.sub(r'\s+F\d+\s*$', '', m.group(1).strip())[:120]
                current_text = [page_text]
                found = True
                break

        if not found:
            current_text.append(page_text)

    if current_text:
        chapters.append((current_title, '\n\n'.join(current_text)))

    return chapters


# ╔══════════════════════════════════════════════════════════════╗
# ║  TEXT → HTML CONVERSION                                     ║
# ╚══════════════════════════════════════════════════════════════╝

def _merge_page_breaks(text):
    """Join text that was split across PDF page boundaries.

    A real paragraph break is: sentence-ending punctuation + blank line +
    capital letter.  Everything else is a mid-sentence page break that
    should be merged.
    """
    chunks = re.split(r'\n\s*\n', text)
    if len(chunks) <= 1:
        return text

    merged = [chunks[0]]

    # Common abbreviations that end with '.' but are NOT sentence ends.
    # When the previous chunk ends with one of these, always merge.
    _abbrev_tail = re.compile(
        r'\b(?:chap|vol|ver|sect|art|pt|fig|no|cf|viz|etc'
        r'|Gen|Exod|Lev|Num|Deut|Josh|Judg|Sam|Kgs|Chron'
        r'|Neh|Esth|Ps|Prov|Eccles|Isa|Jer|Lam|Ezek|Dan'
        r'|Hos|Obad|Mic|Nah|Hab|Zeph|Hag|Zech|Mal'
        r'|Matt|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Heb|Rev'
        r'|ibid|loc|cit|op)\.\s*$',
        re.IGNORECASE
    )

    # Next chunk starts with a verse reference like "10:14." or "1:3."
    _verse_start = re.compile(r'^\d{1,3}:\d')

    # Next chunk starts with a Bible book name (possibly preceded by a number
    # like "1 Corinthians") followed by a chapter:verse reference or a digit.
    # This catches Scripture reference lists split across page breaks.
    _bible_book = re.compile(
        r'^(?:[12]\s*)?(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy'
        r'|Joshua|Judges|Ruth|Samuel|Kings|Chronicles|Ezra|Nehemiah'
        r'|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song'
        r'|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel'
        r'|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum'
        r'|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi'
        r'|Matthew|Mark|Luke|John|Acts|Romans|Corinthians'
        r'|Galatians|Ephesians|Philippians|Colossians'
        r'|Thessalonians|Timothy|Titus|Philemon|Hebrews'
        r'|James|Peter|Jude|Revelation)\s*\d'
    )

    for chunk in chunks[1:]:
        chunk = chunk.strip()
        if not chunk:
            continue

        prev = merged[-1].rstrip()
        prev_ends_sentence = bool(re.search(r'[\.!?;:"\)]\s*$', prev))
        prev_is_abbrev     = bool(_abbrev_tail.search(prev))
        next_starts_upper  = bool(re.match(r'[A-Z""\(]', chunk))
        next_starts_verse  = bool(_verse_start.match(chunk))
        next_starts_bible  = bool(_bible_book.match(chunk))
        next_is_heading    = bool(re.match(
            r'(?:CHAPTER|SERMON|DISCOURSE|EXERCITATION|PREFACE|SECTION|Part\s+\d|Digression)',
            chunk
        ))

        if prev_is_abbrev or next_starts_verse or next_starts_bible:
            merged[-1] = prev + ' ' + chunk          # abbreviation, verse ref, or Bible ref → always join
        elif not prev_ends_sentence:
            merged[-1] = prev + ' ' + chunk          # mid-sentence → join
        elif next_is_heading:
            merged.append(chunk)                       # heading
        elif prev_ends_sentence and next_starts_upper:
            merged.append(chunk)                       # real paragraph
        elif prev_ends_sentence and not next_starts_upper:
            merged[-1] = prev + ' ' + chunk           # lowercase continuation
        else:
            merged.append(chunk)

    return '\n\n'.join(merged)


def _italicise_quotes(html_text):
    """Wrap quoted passages ("...") in <em> tags for italics."""
    # Match "..." and "..." style quotes (but not single words)
    html_text = re.sub(
        r'(\u201c)(.*?)(\u201d)',        # "smart quotes"
        r'\1<em>\2</em>\3',
        html_text,
        flags=re.DOTALL
    )
    # Also handle straight quotes used as block quotes (multi-word)
    html_text = re.sub(
        r'&quot;((?:[^&]|&(?!quot;)){10,}?)&quot;',
        r'&quot;<em>\1</em>&quot;',
        html_text,
        flags=re.DOTALL
    )
    return html_text


def text_to_html(title, text, footnotes):
    """Convert extracted text to XHTML with footnotes and formatting."""
    text = convert_greek(text)
    text = _merge_page_breaks(text)

    # Clean up square-bracket numbering [1. ] → [1.]
    text = re.sub(r'\[(\d{1,3})\.\s*\]', r'[\1.]', text)

    # Remove extra space after '(' in scripture references: ( Romans → (Romans
    text = re.sub(r'\(\s+', '(', text)

    text_escaped = escape(text)
    title_escaped = escape(title)

    # Footnote references: f1, f2, etc. → superscript links
    def fn_replace(m):
        num = m.group(1)
        if num in footnotes:
            return f'<sup><a href="#fn{num}" id="fnref{num}">[{num}]</a></sup>'
        return m.group(0)

    text_escaped = re.sub(r'\bf(\d+)\b', fn_replace, text_escaped)

    # Italicise quoted passages
    text_escaped = _italicise_quotes(text_escaped)

    # Build paragraphs
    paragraphs = re.split(r'\n\s*\n', text_escaped)
    html_parts = [f'<h2>{title_escaped}</h2>']

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para = re.sub(r'\n', ' ', para)
        para = re.sub(r'  +', ' ', para)
        html_parts.append(f'<p>{para}</p>')

    # Append footnotes used in this chapter
    fn_nums = re.findall(r'id="fnref(\d+)"', '\n'.join(html_parts))
    if fn_nums:
        html_parts.append('<hr/><section class="footnotes"><h3>Notes</h3>')
        for num in fn_nums:
            if num in footnotes:
                fn_text = re.sub(r'\n', ' ', escape(footnotes[num]))
                html_parts.append(
                    f'<p class="footnote" id="fn{num}">'
                    f'<a href="#fnref{num}">[{num}]</a> {fn_text}</p>'
                )
        html_parts.append('</section>')

    return '\n'.join(html_parts)


# ╔══════════════════════════════════════════════════════════════╗
# ║  FONT DISCOVERY                                             ║
# ╚══════════════════════════════════════════════════════════════╝

def _find_lora_fonts(script_dir):
    """Try to locate Lora font files on the system."""
    search_paths = [
        # 1. fonts/ folder next to this script
        os.path.join(script_dir, 'fonts'),
        # 2. Common Linux locations
        '/usr/share/fonts/truetype/google-fonts',
        '/usr/share/fonts/truetype/lora',
        '/usr/share/fonts/opentype/lora',
        # 3. macOS
        os.path.expanduser('~/Library/Fonts'),
        '/Library/Fonts',
        '/System/Library/Fonts',
        # 4. Windows
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Fonts'),
        r'C:\Windows\Fonts',
    ]

    regular = italic = None
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        for f in os.listdir(base):
            fl = f.lower()
            if 'lora' in fl and fl.endswith(('.ttf', '.otf')):
                full = os.path.join(base, f)
                if 'italic' in fl:
                    italic = italic or full
                elif 'variable' in fl or 'regular' in fl or fl == 'lora.ttf':
                    regular = regular or full
        if regular:
            break

    return regular, italic


# ╔══════════════════════════════════════════════════════════════╗
# ║  CSS                                                        ║
# ╚══════════════════════════════════════════════════════════════╝

def _build_css(has_fonts):
    font_faces = ""
    if has_fonts:
        font_faces = """
@font-face {
    font-family: 'Lora';
    src: url('../fonts/Lora-Regular.ttf') format('truetype');
    font-weight: 100 900;
    font-style: normal;
}
@font-face {
    font-family: 'Lora';
    src: url('../fonts/Lora-Italic.ttf') format('truetype');
    font-weight: 100 900;
    font-style: italic;
}
"""

    font_family = "'Lora', " if has_fonts else ""

    return font_faces + f"""
body {{
    font-family: {font_family}Georgia, 'Palatino Linotype', serif;
    margin: 1.2em;
    line-height: 1.7;
    color: #1a1a1a;
}}
h1 {{
    text-align: center;
    font-size: 1.8em;
    margin-bottom: 0.5em;
    font-weight: 600;
    letter-spacing: 0.02em;
}}
h2 {{
    font-size: 1.25em;
    margin-top: 1.8em;
    margin-bottom: 0.6em;
    font-weight: 600;
    letter-spacing: 0.01em;
}}
h3 {{ font-size: 1.05em; margin-top: 1.2em; font-weight: 600; }}
p {{
    text-indent: 1.5em;
    margin: 0.4em 0;
    text-align: justify;
}}
sup {{ font-size: 0.7em; line-height: 0; }}
sup a {{ text-decoration: none; color: #6b2d2d; }}
.footnotes {{ font-size: 0.88em; margin-top: 2.5em; color: #333; }}
.footnotes p {{ text-indent: 0; margin: 0.6em 0; }}
.footnotes a {{ text-decoration: none; color: #6b2d2d; font-weight: 600; }}
.title-page {{ text-align: center; margin-top: 4em; }}
.title-page h1 {{ font-size: 2em; font-weight: 700; letter-spacing: 0.03em; }}
.title-page h2 {{ font-size: 1.2em; font-style: italic; font-weight: normal; }}
hr {{ border: none; border-top: 1px solid #ccc; margin: 2em 0 1em; }}
"""


# ╔══════════════════════════════════════════════════════════════╗
# ║  EPUB BUILDER                                               ║
# ╚══════════════════════════════════════════════════════════════╝

def create_epub(pdf_path, cover_path, title, subtitle, output_path,
                vol_num, font_regular, font_italic, css_text):
    """Create one EPUB file from a PDF volume."""
    print(f"\n{'='*60}")
    print(f"  Processing: {title}")
    print(f"{'='*60}")

    reader = PdfReader(pdf_path)
    total = len(reader.pages)

    # Footnotes
    print("  Extracting footnotes...")
    footnotes, body_end = extract_footnotes(reader, total)
    print(f"  Found {len(footnotes)} footnotes (body ends at page {body_end})")

    # Body text
    print("  Extracting text...")
    pages = extract_pages(reader, body_end)

    # Chapters
    print("  Detecting chapters...")
    chapters = detect_chapters(pages)
    print(f"  Found {len(chapters)} sections")

    # --- Build EPUB ---
    book = epub.EpubBook()
    book.set_identifier(f'john-owen-works-vol-{vol_num:02d}-bot')
    book.set_title(title)
    book.set_language('en')
    book.add_author('John Owen')
    book.add_metadata('DC', 'publisher', 'Banner of Truth Trust')
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'description', f'{title} — {subtitle}')

    # Cover image
    print("  Adding cover...")
    ext = os.path.splitext(cover_path)[1].lower()
    media = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
    with open(cover_path, 'rb') as f:
        cover_data = f.read()

    book.add_item(epub.EpubItem(
        uid='cover-image', file_name='images/cover' + ext,
        media_type=media, content=cover_data
    ))
    book.add_metadata(None, 'meta', '', {'name': 'cover', 'content': 'cover-image'})

    cover_page = epub.EpubHtml(title='Cover', file_name='cover.xhtml', lang='en')
    cover_page.set_content(
        f'<html xmlns="http://www.w3.org/1999/xhtml">'
        f'<head><title>Cover</title></head>'
        f'<body style="margin:0;padding:0;text-align:center;">'
        f'<img src="../images/cover{ext}" alt="Cover" '
        f'style="max-width:100%;max-height:100%;"/>'
        f'</body></html>'
    )
    book.add_item(cover_page)

    # Fonts (optional)
    if font_regular:
        print("  Embedding Lora font...")
        for fpath, fname in [(font_regular, 'Lora-Regular.ttf'),
                              (font_italic, 'Lora-Italic.ttf')]:
            if fpath and os.path.isfile(fpath):
                with open(fpath, 'rb') as f:
                    book.add_item(epub.EpubItem(
                        uid=fname.replace('.', '-'),
                        file_name=f'fonts/{fname}',
                        media_type='font/ttf',
                        content=f.read()
                    ))

    # CSS
    css_item = epub.EpubItem(
        uid='style', file_name='style/default.css',
        media_type='text/css', content=css_text
    )
    book.add_item(css_item)

    # Title page
    title_ch = epub.EpubHtml(title='Title Page', file_name='title.xhtml', lang='en')
    title_ch.set_content(
        f'<html xmlns="http://www.w3.org/1999/xhtml">'
        f'<head><link rel="stylesheet" href="../style/default.css" /></head>'
        f'<body><div class="title-page">'
        f'<h1>{escape(title)}</h1>'
        f'<h2>{escape(subtitle)}</h2>'
        f'<p style="text-indent:0;text-align:center;margin-top:2em;">by John Owen</p>'
        f'<p style="text-indent:0;text-align:center;">Edited by William H. Goold</p>'
        f'<p style="text-indent:0;text-align:center;margin-top:2em;">'
        f'Banner of Truth Trust</p>'
        f'</div></body></html>'
    )
    title_ch.add_item(css_item)
    book.add_item(title_ch)

    # Content chapters
    epub_chapters = [title_ch]
    toc = []

    print("  Building chapters...")
    for i, (ch_title, ch_text) in enumerate(chapters):
        html_content = text_to_html(ch_title, ch_text, footnotes)
        ch = epub.EpubHtml(
            title=ch_title[:80],
            file_name=f'chapter_{i:03d}.xhtml',
            lang='en'
        )
        ch.set_content(
            f'<html xmlns="http://www.w3.org/1999/xhtml">'
            f'<head><link rel="stylesheet" href="../style/default.css" /></head>'
            f'<body>{html_content}</body></html>'
        )
        ch.add_item(css_item)
        book.add_item(ch)
        epub_chapters.append(ch)
        toc.append(ch)

        if (i + 1) % 20 == 0:
            print(f"    ...{i+1}/{len(chapters)} chapters")

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = [cover_page, 'nav'] + epub_chapters

    print("  Writing EPUB...")
    epub.write_epub(output_path, book)
    size = os.path.getsize(output_path)
    print(f"  ✓ {os.path.basename(output_path)}  "
          f"({size / 1024:.0f} KB, {len(chapters)} sections, "
          f"{len(footnotes)} footnotes)")


# ╔══════════════════════════════════════════════════════════════╗
# ║  MAIN — AUTO-DISCOVERY                                     ║
# ╚══════════════════════════════════════════════════════════════╝

def main():
    # Determine working folder
    if len(sys.argv) > 1:
        work_dir = sys.argv[1]
    else:
        work_dir = os.getcwd()

    work_dir = os.path.abspath(work_dir)
    covers_dir = os.path.join(work_dir, 'covers')

    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  John Owen Works — PDF → EPUB Converter                 ║")
    print(f"╚══════════════════════════════════════════════════════════╝")
    print(f"  Folder:  {work_dir}")
    print(f"  Covers:  {covers_dir}")

    # --- Find PDFs ---
    pdf_pattern = os.path.join(work_dir, '*.pdf')
    pdfs = sorted(glob.glob(pdf_pattern))

    if not pdfs:
        sys.exit(f"\n  ERROR: No PDF files found in {work_dir}")

    # --- Find covers ---
    if not os.path.isdir(covers_dir):
        print(f"\n  WARNING: No 'covers' folder found at {covers_dir}")
        print(f"           EPUBs will be created without cover images.\n")

    # --- Find fonts ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_regular, font_italic = _find_lora_fonts(script_dir)
    has_fonts = font_regular is not None
    if has_fonts:
        print(f"  Font:    Lora (embedded)")
    else:
        print(f"  Font:    Georgia / system serif (Lora not found)")

    css_text = _build_css(has_fonts)

    # --- Match PDFs to volumes ---
    print(f"\n  Found {len(pdfs)} PDF(s):\n")

    converted = 0
    skipped = 0

    for pdf_path in pdfs:
        pdf_name = os.path.basename(pdf_path)

        # Extract volume number from filename
        vol_match = re.search(r'vol[_\s]*(\d{1,2})', pdf_name, re.IGNORECASE)
        if not vol_match:
            vol_match = re.search(r'[-_]v(\d{1,2})[-_]', pdf_name, re.IGNORECASE)
        if not vol_match:
            vol_match = re.search(r'(\d{1,2})', pdf_name)
        if not vol_match:
            print(f"  SKIP: {pdf_name} (can't determine volume number)")
            skipped += 1
            continue

        vol_num = int(vol_match.group(1))

        # Check if EPUB already exists
        epub_name = f'Works_of_John_Owen_Vol_{vol_num:02d}.epub'
        epub_path = os.path.join(work_dir, epub_name)
        if os.path.exists(epub_path):
            print(f"  SKIP: Vol {vol_num:2d} — {epub_name} already exists")
            skipped += 1
            continue

        # Find matching cover
        cover_path = None
        if os.path.isdir(covers_dir):
            for ext in ('.jpg', '.jpeg', '.png', '.webp'):
                candidate = os.path.join(covers_dir, f'v{vol_num}{ext}')
                if os.path.exists(candidate):
                    cover_path = candidate
                    break

        if not cover_path:
            print(f"  WARNING: No cover found for vol {vol_num} "
                  f"(looked for covers/v{vol_num}.jpg/.png)")

        # Volume metadata
        subtitle = VOLUME_SUBTITLES.get(vol_num, f"Volume {vol_num}")
        title = f"The Works of John Owen, Vol. {vol_num}"

        # Convert!
        try:
            create_epub(
                pdf_path=pdf_path,
                cover_path=cover_path,
                title=title,
                subtitle=subtitle,
                output_path=epub_path,
                vol_num=vol_num,
                font_regular=font_regular,
                font_italic=font_italic,
                css_text=css_text,
            )
            converted += 1
        except Exception as e:
            print(f"\n  ERROR converting vol {vol_num}: {e}")
            import traceback
            traceback.print_exc()

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"  DONE — {converted} converted, {skipped} skipped")
    print(f"{'='*60}")

    if skipped > 0:
        print(f"\n  To reconvert an existing EPUB, delete it first and re-run.")


if __name__ == '__main__':
    main()
