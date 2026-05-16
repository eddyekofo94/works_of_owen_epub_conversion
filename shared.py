"""
Shared constants for John Owen Works PDF → EPUB conversion.
All conversion scripts import from here — single source of truth for
volume metadata, Greek Beta Code maps, Hebrew Gideon maps, font pools,
and EPUB3 stylesheets.
"""

import unicodedata
import re

# ============================================================================
# VOLUME METADATA — Owen Works (16 volumes)
# ============================================================================

VOLUME_SUBTITLES = {
    1: "The Glory of Christ",
    2: "Communion with God",
    3: "The Holy Spirit",
    4: "The Work of the Spirit",
    5: "Faith and Its Evidences",
    6: "Temptation and Sin",
    7: "Sin and Grace",
    8: "Sermons to the Nation",
    9: "Sermons to the Church",
    10: "The Death of Christ",
    11: "Continuing in the Faith",
    12: "The Gospel Defended",
    13: "Ministry and Fellowship",
    14: "True and False Religion",
    15: "Church Purity and Unity",
    16: "The Church and the Bible",
}

VOLUME_CONFIG = {
    1: {
        'title': 'The Works of John Owen, Volume 1: The Glory of Christ',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'front_matter_skip': 3,
    },
    2: {
        'title': 'The Works of John Owen, Volume 2: Communion with God',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    3: {
        'title': 'The Works of John Owen, Volume 3: The Holy Spirit',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    4: {
        'title': 'The Works of John Owen, Volume 4: The Work of the Spirit',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    5: {
        'title': 'The Works of John Owen, Volume 5: Faith and Its Evidences',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Brill_font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ccel_xml',
        'ccel_file': 'special_sources/owen-v5-justification.xml',
    },
    6: {
        'title': 'The Works of John Owen, Volume 6: Temptation and Sin',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    7: {
        'title': 'The Works of John Owen, Volume 7: Sin and Grace',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    8: {
        'title': 'The Works of John Owen, Volume 8: Sermons to the Nation',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    9: {
        'title': 'The Works of John Owen, Volume 9: Sermons to the Church',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    10: {
        'title': 'The Works of John Owen, Volume 10: The Death of Christ',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Brill_font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ccel_xml',
        'ccel_file': 'special_sources/owen-10-deathofdeath.xml',
    },
    11: {
        'title': 'The Works of John Owen, Volume 11: Continuing in the Faith',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    12: {
        'title': 'The Works of John Owen, Volume 12: The Gospel Defended',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    13: {
        'title': 'The Works of John Owen, Volume 13: Ministry and Fellowship',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    14: {
        'title': 'The Works of John Owen, Volume 14: True and False Religion',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Brill_font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    15: {
        'title': 'The Works of John Owen, Volume 15: Church Purity and Unity',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
    16: {
        'title': 'The Works of John Owen, Volume 16: The Church and the Bible',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
    },
}

# ============================================================================
# VOLUME METADATA — Hebrews Commentary (7 volumes)
# ============================================================================

HEBREWS_VOLUME_CONFIG = {
    1: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 1',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    2: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 2',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    3: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 3',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    4: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 4',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    5: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 5',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    6: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 6',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
    7: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 7',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
    },
}

# ============================================================================
# GREEK BETA CODE CONVERTER
# ============================================================================

GREEK_LOWER = {
    'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε',
    'z': 'ζ', 'h': 'η', 'q': 'θ', 'i': 'ι', 'k': 'κ',
    'l': 'λ', 'm': 'μ', 'n': 'ν', 'x': 'ξ', 'o': 'ο',
    'p': 'π', 'r': 'ρ', 's': 'σ', 't': 'τ',
    'u': 'υ', 'f': 'φ', 'c': 'χ', 'y': 'ψ', 'v': 'ς', 'w': 'ω',
}

GREEK_UPPER = {
    'A': 'Α', 'B': 'Β', 'G': 'Γ', 'D': 'Δ', 'E': 'Ε',
    'Z': 'Ζ', 'H': 'Η', 'Q': 'Θ', 'I': 'Ι', 'K': 'Κ',
    'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'X': 'Ξ', 'O': 'Ο',
    'P': 'Π', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ',
    'U': 'Υ', 'F': 'Φ', 'C': 'Χ', 'Y': 'Ψ', 'V': 'Σ', 'W': 'Ω',
}
ALL_GREEK = {**GREEK_LOWER, **GREEK_UPPER}

SMOOTH = '\u0313'
ROUGH = '\u0314'
ACUTE = '\u0301'
GRAVE = '\u0300'
CIRCUMFLEX = '\u0342'
IOTASUB = '\u0345'

DIACRITIC_CHARS = set('><=~]J[j}|{=+\'')
DIACRITIC_MAP = {
    'j': (SMOOTH,),
    'J': (ROUGH,),
    '>': (ACUTE,),
    '<': (GRAVE,),
    '\'': (ACUTE,),
    '~': (CIRCUMFLEX,),
    '=': (CIRCUMFLEX,),
    '+': (CIRCUMFLEX,),
    ']': (SMOOTH, ACUTE),
    '}': (SMOOTH, CIRCUMFLEX),
    '[': (ROUGH, ACUTE),
    '{': (ROUGH, CIRCUMFLEX),
    '|': (IOTASUB,),
}


def clean_greek_text(text):
    """
    User-mandated Greek cleaning:
    1. Strip "j" artifact prepended to Greek characters (handling optional spaces).
    2. Normalize to NFC.
    """
    if not text:
        return ""
    # 1. Strip the "j" artifact prepended to Greek characters.
    # Handle both "jΕ" and "j Ε" patterns found in PDF extraction.
    text = re.sub(r'\b[jJ]\s*([\u0370-\u03FF\u1F00-\u1FFF])', r'\1', text)
    # 2. Normalize to NFC
    text = unicodedata.normalize('NFC', text)
    return text


def convert_greek_word(word):
    """Convert a Beta Code / AGES-Koine word to Unicode Greek.

    Sigma rules (AGES encoding for Owen volumes):
      - 's' at the very end of a word → final sigma ς
      - 's' elsewhere → medial sigma σ
      - 'v' → final sigma ς (explicitly typed by AGES/Graeca)
      - 'y' → psi ψ

    Note: The previous assumption that 'v' was psi was incorrect. AGES uses Graeca/WinGreek layout where 'v' = ς and 'y' = ψ.
    """
    result = []
    i = 0
    while i < len(word):
        ch = word[i]
        # Determine the next non-diacritic character for sigma-end detection
        if ch in GREEK_LOWER:
            # Check for final sigma: 's' is final only when it is the last
            # alphabetic character in the word (all remaining chars are diacritics).
            if ch == 's':
                rest_alpha = [c for c in word[i + 1:] if c not in DIACRITIC_CHARS]
                if not rest_alpha:
                    result.append('ς')
                else:
                    result.append('σ')
            else:
                result.append(GREEK_LOWER[ch])
            i += 1
            while i < len(word) and word[i] in DIACRITIC_CHARS:
                d = word[i]
                if d in DIACRITIC_MAP:
                    for c in DIACRITIC_MAP[d]:
                        result.append(c)
                i += 1
        elif ch in GREEK_UPPER:
            if ch == 'S':
                result.append('Σ')
            else:
                result.append(GREEK_UPPER[ch])
            i += 1
            while i < len(word) and word[i] in DIACRITIC_CHARS:
                d = word[i]
                if d in DIACRITIC_MAP:
                    for c in DIACRITIC_MAP[d]:
                        result.append(c)
                i += 1
        else:
            result.append(ch)
            i += 1
    return unicodedata.normalize('NFC', ''.join(result))


# Legacy accent characters that should not appear inside a Unicode Greek span.
_GREEK_LEGACY_ACCENT_RE = re.compile(r'[~><jJ\[\]{}\|\'=+]+')


def polytonic_sweep(text: str) -> str:
    """Remove any surviving legacy Beta Code accent/breathing characters from text.

    This is a safety net — after convert_greek_word() has run, no span of Greek
    text should contain '~', '>', '<', 'j', 'J', etc.  We strip them here so
    they never reach the EPUB.
    """
    return _GREEK_LEGACY_ACCENT_RE.sub('', text)


# ============================================================================
# HEBREW GIDEON FONT CONVERTER
# ============================================================================

GIDEON_CHAR_MAP = {
    # ── Consonants (Gideon AGES legacy encoding) ──────────────────────────
    'a': '\u05D0',  # א Alef
    'b': '\u05D1',  # ב Bet
    'c': '\u05E1',  # ס Samekh (AGES maps 'c' to Samekh)
    'd': '\u05D3',  # ד Dalet
    'f': '\u05D8',  # ט Tet
    'g': '\u05D2',  # ג Gimel
    'h': '\u05D4',  # ה He
    'j': '\u05D7',  # ח Het
    'k': '\u05DB',  # כ Kaf
    'l': '\u05DC',  # ל Lamed
    'm': '\u05DE',  # מ Mem
    'n': '\u05E0',  # נ Nun
    'p': '\u05E4',  # פ Pe
    'q': '\u05E7',  # ק Qof
    'r': '\u05E8',  # ר Resh
    's': '\u05E1',  # ס Samekh (alternate; same as 'c')
    't': '\u05EA',  # ת Tav
    'v': '\u05E9\u05C1',  # שׁ Shin (Shin + Shin dot)
    'w': '\u05D5',  # ו Vav
    'x': '\u05E6',  # צ Tsadi
    'y': '\u05D9',  # י Yod
    'z': '\u05D6',  # ז Zayin
    '[': '\u05E2',  # ע Ayin
    'i': '\u05E2',  # ע Ayin (alternate)
    # ── Final forms ────────────────────────────────────────────────────────
    'A': '\u05D0',        # א Alef (uppercase alternate)
    'B': '\u05D1\u05BC',  # בּ Bet + Dagesh
    'D': '\u05D3\u05BC',  # דּ Dalet + Dagesh
    'G': '\u05D2\u05BC',  # גּ Gimel + Dagesh
    'K': '\u05DB\u05BC',  # כּ Kaf + Dagesh
    'M': '\u05DD',        # ם Mem Final
    'N': '\u05DF',        # ן Nun Final
    'P': '\u05E3',        # ף Pe Final
    'Q': '\u05E7\u05BC',  # קּ Qof + Dagesh
    'T': '\u05EA\u05BC',  # תּ Tav + Dagesh
    'W': '\u05D5\u05BC',  # וּ Vav + Dagesh (Shureq)
    'X': '\u05E5',        # ץ Tsadi Final
    'Y': '\u05D9',        # י Yod (uppercase alternate, common in Vol 2)
    '\u00B5': '\u05DD',   # µ (U+00B5 micro sign) → ם Mem Final (Vol 2 failure)
    '\u00E7': '\u05E6',   # ç → צ Tsadi (Vol 2 font artifact)
    '\u02DA': '\u05BC',   # ˚ → ּ Dagesh (Vol 2 font artifact)
    '\u02C6': '\u05B4',   # ˆ → ִ Hiriq (Vol 2 font artifact)
    '\u00DA': '\u05D5',   # Ú → ו Vav (Vol 2 font artifact)
    '\u2019': '\u05BE',   # ' → ־ Maqef (Vol 1 font artifact — curly apostrophe)
    '\u2248': '\u05C1',   # ≈ → ׁ Shin dot (Vol 1 font artifact)
    # ── Vowel points / diacritics ──────────────────────────────────────────
    ';': '\u05B8',   # ָ Qamats
    '}': '\u05B2',   # ֲ Hataf Patah
    ']': '\u05B0',   # ְ Sheva
    '1': '\u05B7',   # ַ Patah
    'e': '\u05B5',   # ֵ Tsere
    'o': '\u05B9',   # ֹ Holam
    'O': '\u05B9',   # ֹ Holam (alternate)
    # ── Alternate vowel mappings ───────────────────────────────────────────
    'æ': '\u05B7',   # ַ Patah (Latin ae ligature used as AGES artifact)
    # ── Punctuation / spacing ──────────────────────────────────────────────
    ',': ',',
    ' ': ' ',
}

GIDEON_CID_MAP = {
    181: '\u05DD',   190: '\u05B7',   213: '\u05BE',
    246: '\u05DF',   242: '\u05E3',   141: '\u05B8',
    139: '\u05B8',   197: '\u05BC',   212: '\u05BF',
    232: '\u05BC',   251: '\u05C2',
}


def is_hebrew_vowel(ch):
    if len(ch) != 1:
        return False
    cp = ord(ch)
    return (0x05B0 <= cp <= 0x05BD) or cp == 0x05BF or (0x05C1 <= cp <= 0x05C2)


def convert_gideon_hebrew(encoded):
    """Convert Gideon font-encoded text to Unicode Hebrew.

    Text is stored in visual L→R order; reverses per word and reverses
    word order to produce logical R→L Hebrew.

    Unknown Gideon characters are logged to stderr (once per character per
    session) so gaps in GIDEON_CHAR_MAP can be identified and filled.
    """
    import re
    import sys
    _warned_chars: set = getattr(convert_gideon_hebrew, '_warned_chars', set())
    convert_gideon_hebrew._warned_chars = _warned_chars

    text = re.sub(
        r'\(cid:(\d+)\)',
        lambda m: GIDEON_CID_MAP.get(int(m.group(1)), ''),
        encoded
    )
    mapped_chars = []
    for ch in text:
        if ch in GIDEON_CHAR_MAP:
            mapped_chars.append(GIDEON_CHAR_MAP[ch])
        elif ch == '\u00AF':
            mapped_chars.append('\u05BE')  # Maqef
        elif ord(ch) > 127 and ch not in _warned_chars:
            # Non-ASCII character not in map — log once
            _warned_chars.add(ch)
            print(f"[GIDEON WARNING] Unmapped character U+{ord(ch):04X} ({repr(ch)}) — add to GIDEON_CHAR_MAP", file=sys.stderr)
            mapped_chars.append(ch)
        else:
            mapped_chars.append(ch)
    flat = ''.join(mapped_chars)

    tokens = []
    current = ''
    for ch in flat:
        if is_hebrew_vowel(ch):
            current += ch
        elif ch == ' ' or ch == '\u05BE' or ch == ',':
            if current:
                tokens.append(current)
                current = ''
            tokens.append(ch)
        else:
            if current:
                tokens.append(current)
            current = ch
    if current:
        tokens.append(current)

    words = []
    current_word = []
    for tok in tokens:
        if tok == ' ':
            if current_word:
                words.append(list(reversed(current_word)))
            words.append([' '])
            current_word = []
        elif tok == '\u05BE':
            current_word.append(tok)
        else:
            current_word.append(tok)
    if current_word:
        words.append(list(reversed(current_word)))
    words.reverse()

    result = []
    for word in words:
        result.extend(word)
    return unicodedata.normalize('NFC', ''.join(result))


# ============================================================================
# FONT POOLS
# ============================================================================

def select_primary_font(body_font_name):
    """Select a primary font by name and scan its directory for associated files.
    
    Looks in fonts/<body_font_name>/ for .ttf and .otf files.
    Returns a dict: {'name': body_font_name, 'files': {basename: relative_path}}.
    """
    import os
    
    # Base directory for fonts (shared.py is in project root)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(base_dir, 'fonts', body_font_name)
    
    # Fallback to SBL_BLit if directory doesn't exist
    if not os.path.isdir(font_dir):
        body_font_name = 'SBL_BLit'
        font_dir = os.path.join(base_dir, 'fonts', body_font_name)
    
    files = {}
    if os.path.isdir(font_dir):
        for f in os.listdir(font_dir):
            if f.lower().endswith(('.ttf', '.otf')):
                files[f] = f"{body_font_name}/{f}"
                
    return {
        'name': body_font_name,
        'files': files
    }


SBL_SUPPLEMENTS = {
    'SBL_BLit.ttf': 'SBL_BLit/SBL_BLit.ttf',
    'SBL_grk.ttf': 'SBL_BLit/SBL_grk.ttf',
    'SBL_Hbrw.ttf': 'SBL_BLit/SBL_Hbrw.ttf',
}

EZRA_SIL_FILES = {
    'SILEOT.ttf': 'EzraSIL2.51/SILEOT.ttf',
}


# ============================================================================
# EPUB STYLESHEET (GEMINI.md compliant)
# ============================================================================

EPUB_STYLESHEET = r"""
/* Eduardus Ekofius style — clean serif, elegant hierarchy */
body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 1.1em;
    line-height: 1.65;
    color: #000;
    margin: 1em 1.2em;
    -webkit-font-smoothing: antialiased;
    -webkit-hyphens: auto;
    hyphens: auto;
}

/* Title Page Majesty */
.titlepage,
.title-page {
    text-align: center;
    padding: 12% 6% 10%;
    max-width: 36em;
    margin: 0 auto;
    page-break-before: always;
    -webkit-column-break-before: always;
}
.titlepage .ornament,
.title-page .ornament {
    display: block;
    text-align: center;
    font-size: 1.15em;
    line-height: 1;
    margin: 0 auto 1.5em;
    color: #b08d2d;
    text-indent: 0;
}
.titlepage h1,
.title-page h1 {
    font-variant: small-caps;
    font-size: 1.9em;
    line-height: 1.18;
    margin: 0 0 1.35em;
    page-break-before: avoid;
}
.titlepage h2,
.title-page h2 {
    font-weight: bold;
    font-size: 1.25em;
    line-height: 1.35;
    margin: 1.2em 0;
    page-break-before: avoid;
    -webkit-column-break-before: avoid;
}
.titlepage h3,
.title-page h3 {
    text-align: center;
    font-size: 1.05em;
    line-height: 1.35;
    margin: 1.15em 0;
    page-break-before: avoid;
    -webkit-column-break-before: avoid;
}
.titlepage .subtitle,
.title-page .subtitle {
    font-size: 1.1em;
    margin-top: 1em;
}
.titlepage .descriptive,
.title-page .descriptive {
    text-align: center;
    font-style: italic;
    line-height: 1.45;
    margin: 1.8em auto 0;
    max-width: 31em;
    text-indent: 0;
}
.titlepage .author,
.titlepage .editor,
.titlepage .publisher,
.title-page .author,
.title-page .editor,
.title-page .publisher {
    text-align: center;
    text-indent: 0;
    margin: 0.2em auto;
}
.titlepage .author,
.title-page .author {
    margin-top: 2em;
}
.titlepage .by,
.title-page .by {
    font-style: italic;
    margin-right: 0.25em;
}

h1 {
    text-align: center;
    font-size: 1.6em;
    font-weight: bold;
    letter-spacing: 0.03em;
    margin: 1.8em 0 0.6em;
    page-break-before: always;
    -webkit-column-break-before: always;
}

h1.primary {
    font-size: 1.7em;
    text-align: center;
    border-bottom: 1px solid #000;
    padding-bottom: 0.2em;
}

h2 {
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
}

h2.secondary, h3.secondary, h1.secondary {
    font-size: 1.35em;
    text-align: center;
    margin: 1.5em 0 0.5em;
    border: none;
    padding: 0;
}

h3 {
    text-align: center;
    font-size: 1.05em;
    font-weight: bold;
    margin: 1.2em 0 0.4em;
}

p.chapter-summary {
    font-style: italic;
    font-size: 0.95em;
    text-align: center;
    margin: 1.2em 12% 2.2em;
    text-indent: 0;
    line-height: 1.45;
}

h4.chapter-subtitle {
    text-align: center;
    font-size: 1.05em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    line-height: 1.35;
    margin: 0.4em 0 1em;
    text-indent: 0;
}

.digression-heading {
    text-align: center;
    font-size: 1.3em;
    color: #000;
    margin: 2em 0 0.5em;
    font-weight: bold;
    page-break-before: always;
}

.roman-subheading {
    text-align: center;
    font-weight: bold;
    text-indent: 0;
    margin: 1.2em 0 0.8em;
    break-after: avoid;
    page-break-after: avoid;
    break-inside: avoid;
    page-break-inside: avoid;
}

.roman-list-item {
    text-align: center;
    text-indent: 0;
    margin: 1.1em 0;
}

.roman-list-item b {
    display: block;
    margin-bottom: 0.35em;
}

/* Front Matter Styling (Issue 107 / Issue 89) */

/* Decorative blurb title — used for 1-3 line ornamental headings on
   title-adjacent pages (e.g. "PREFACE" as a standalone centered line
   in blurb style). */
.front-matter-title {
    font-size: 1.35em;
    text-align: center;
    margin: 2em 0 1em;
    font-weight: bold;
    text-transform: uppercase;
}

/* Section heading for prose-heavy front matter (General Preface,
   Prefatory Notes, Prefaces, Analyses). h2-level, uppercase, centered — same visual weight as front-matter-title
   but semantically a heading element. */
.front-matter-heading {
    font-size: 1.45em;
    text-align: center;
    margin: 2em 0 1.2em;
    font-weight: bold;
    text-transform: uppercase;
    text-indent: 0;
}

/* Decorative blurb body — for 2-5 line centered ornamental paragraphs
   on title-adjacent pages (author name, dedications, publisher info). */
.front-matter-body {
    text-align: center;
    font-style: italic;
    margin: 1.2em 10%;
    line-height: 1.6;
    text-indent: 0;
}

/* Running prose body — for editorial prefaces, prefatory notes,
   analyses. Identical to normal chapter body paragraphs so long
   prose reads naturally. */
.front-matter-prose {
    text-align: justify;
    text-indent: 1.5em;
    margin: 0;
    font-style: normal;
    line-height: 1.6;
    orphans: 2;
    widows: 2;
}

.front-matter-prose.first {
    text-indent: 0;
}

/* Body Flow */
p {
    text-indent: 1.5em;
    margin: 0;
    text-align: justify;
    orphans: 2;
    widows: 2;
}

p.first, p.noindent {
    text-indent: 0;
}

blockquote {
    margin: 0.8em 2em;
    font-size: 0.95em;
}

/* Frontispiece / Portrait */
.frontispiece {
    text-align: center;
    margin-top: 15%;
    page-break-after: always;
}
.frontispiece img {
    max-width: 65%;
    height: auto;
}
.frontispiece .caption {
    text-indent: 0;
    text-align: center;
    margin-top: 1em;
    font-style: italic;
}

.verse {
    text-align: center;
    font-style: italic;
    margin: 1.2em 0;
    text-indent: 0 !important;
}

.greek {
    font-family: Georgia, "Times New Roman", serif;
    font-style: italic;
}

.hebrew {
    font-family: Georgia, "Times New Roman", serif;
}

.small-caps {
    font-variant: small-caps;
}

sup {
    font-size: 0.75em;
    line-height: 0;
    vertical-align: super;
}

.footnote {
    font-size: 0.9em;
    text-indent: 0;
    margin: 0.3em 0;
}

a.footnote-ref {
    text-decoration: none;
    color: #0000EE;
    vertical-align: super;
    font-size: 1em;
}

a.fn-link {
    color: #0000EE;
    text-decoration: none;
    font-size: 0.9em;
    margin-right: 0.3em;
}

/* Proper TOC Alignment */
.toc-line {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3em;
    padding-left: 2em;
    text-indent: -2em;
}
.toc-line .toc-title {
    flex-grow: 1;
    text-align: left;
}
.toc-line .toc-page {
    margin-left: 1em;
    text-align: right;
    white-space: nowrap;
}

/* EPUB3 footnote styles */
.noteref {
    color: #0000EE;
    text-decoration: none;
    vertical-align: super;
    font-size: 0.95em;
    display: inline-block;
    line-height: 1;
    margin-left: 0.18em;
    padding-right: 0.25em;
    text-indent: 0;
}

/* Consecutive noterefs: keep them visually separated */
.noteref + .noteref {
    margin-left: 0;
}

.noteref sup {
    font-size: 1em;
    line-height: 1;
}

.doxology {
    text-align: center;
    text-indent: 0;
    margin: 2em 0 1.2em;
}

/* Scholastic anchor: Obj. / Ans. / Use N. — each on its own paragraph */
p.scholastic-anchor {
    margin-top: 1.5em;
    text-indent: 0;
}
p.scholastic-anchor b,
b.scholastic-label {
    font-weight: bold;
}

/* Author signatures: "= John Owen" at end of prefaces */
p.signature {
    text-align: right;
    font-style: italic;
    text-indent: 0;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
}

/* Catechism formatting */
.catechism-item {
    text-indent: 0 !important;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}

/* Inner Treatise Title Pages (e.g. Christologia) */
.treatise-title-page {
    text-align: center;
    padding: 5% 5% 8%;
    max-width: 38em;
    margin: 0 auto;
    page-break-before: always;
}
.treatise-title-page .greek-title {
    text-align: center;
    font-size: 1.25em;
    margin-bottom: 2.5em;
    text-indent: 0;
    font-weight: bold;
}
.treatise-title-page h1 {
    font-size: 2.2em;
    margin: 1.2em 0 0.8em;
    text-transform: uppercase;
    line-height: 1.15;
    font-weight: bold;
}
.treatise-title-page h2 {
    font-size: 1.45em;
    margin: 0.8em 0;
    line-height: 1.3;
    font-weight: bold;
    text-transform: uppercase;
}
.treatise-title-page p {
    text-align: center;
    text-indent: 0;
    margin: 0.6em 0;
    line-height: 1.4;
}
.treatise-title-page .separator {
    margin: 1.2em 0;
    text-transform: uppercase;
    font-size: 1em;
}
.treatise-title-page .descriptive {
    font-style: italic;
    font-size: 1.1em;
    margin: 1.5em auto;
    max-width: 32em;
}
.treatise-title-page .quote-block {
    text-align: left;
    margin: 5em 8% 2em;
    font-size: 1em;
    line-height: 1.55;
    text-indent: 0;
    font-style: italic;
    border-top: 1px solid #ccc;
    padding-top: 1.5em;
}

aside[epub\:type~="footnote"] {
    display: block;
}

aside[epub\:type~="endnote"] {
    margin-bottom: 0.8em;
    padding-left: 1.8em;
    text-indent: -1.8em;
}

/* Contents Item */
.ContentsItem {
    margin: 0.8em 0 0.2em;
    padding-left: 6.5em;
    text-indent: -6.5em;
    text-align: left;
    color: #000;
    font-size: 0.95em;
    line-height: 1.45;
}

.ContentsDescWrap {
    margin: 0 0 0.2em 6.5em;
    text-indent: 0;
    text-align: left;
    font-size: 0.95em;
    display: block;
}
"""


# ============================================================================
# EPUB3 INLINE FONT INJECTION STYLES
# ============================================================================

EPUB3_FONT_STYLES = r"""
/* Injected font-face declarations and language-specific overrides */
/* Primary font: {primary_font} */
@font-face {{
    font-family: "{primary_font}";
    src: url("Fonts/{primary_file}");
}}
{bold_face}
{italic_face}
{bold_italic_face}
/* SBL BibLit — universal biblical fallback */
@font-face {{
    font-family: "SBL BibLit";
    src: url("Fonts/SBL_BLit.ttf");
}}
/* SBL Greek — polytonic Greek */
@font-face {{
    font-family: "SBL Greek";
    src: url("Fonts/SBL_grk.ttf");
}}
/* SBL Hebrew — fully pointed Hebrew */
@font-face {{
    font-family: "SBL Hebrew";
    src: url("Fonts/SBL_Hbrw.ttf");
}}
/* Ezra SIL — BHS-style Hebrew fallback */
@font-face {{
    font-family: "Ezra SIL";
    src: url("Fonts/SILEOT.ttf");
}}
/* Language overrides (GEMINI.md Section 4.2) */
body, div, p, span, h1, h2, h3, h4, h5, h6 {{
    font-family: "{primary_font}", "SBL BibLit", "Gentium Plus", serif !important;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
}}
[lang="el"], [lang="el"] *, .greek, .greek * {{
    font-family: "SBL Greek", "SBL BibLit", serif !important;
    font-size: 1.15em;
}}
[lang="he"], [lang="he"] *, .hebrew, .hebrew * {{
    direction: rtl;
    unicode-bidi: embed;
    font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", serif !important;
    font-size: 1.5em;
    line-height: 1.24;
}}
[lang="he"], [lang="he"] p,
[lang="he"], [lang="he"] div {{
    text-align: left;
}}
"""


def generate_font_styles(primary_font_name, primary_font_files):
    """Generate per-XHTML inline <style> block with @font-face declarations.
    
    Font files are stored flat in Fonts/ (no subdirectories), so we use
    os.path.basename() to flatten paths like 'Brill/Brill-Roman.ttf' → 'Brill-Roman.ttf'.
    
    Returns the complete <style> element content as a string.
    """
    import os as _os
    
    # 1. Identify primary, bold, italic, and bold-italic files using robust heuristics
    primary_file = None
    bold_file = None
    italic_file = None
    bold_italic_file = None
    
    # Sort files to ensure deterministic results (prefer shorter names or 'Regular')
    sorted_files = sorted(primary_font_files.values(), key=lambda x: (len(x), x))
    
    for font_file in sorted_files:
        fname = _os.path.basename(font_file).lower()
        
        is_bold = 'bold' in fname or '-b.' in fname or '_b.' in fname
        is_italic = 'italic' in fname or 'ital' in fname or '-i.' in fname or '_i.' in fname
        is_regular = 'regular' in fname or 'roman' in fname or '-r.' in fname or '_r.' in fname or (not is_bold and not is_italic)
        
        if is_bold and is_italic:
            if not bold_italic_file: bold_italic_file = _os.path.basename(font_file)
        elif is_bold:
            if not bold_file: bold_file = _os.path.basename(font_file)
        elif is_italic:
            if not italic_file: italic_file = _os.path.basename(font_file)
        elif is_regular:
            if not primary_file: primary_file = _os.path.basename(font_file)

    # Fallback for primary_file if no "Regular" found
    if not primary_file and primary_font_files:
        primary_file = _os.path.basename(list(primary_font_files.values())[0])
    
    bold_face = ''
    if bold_file:
        bold_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    src: url("Fonts/{bold_file}");\n}}'
    
    italic_face = ''
    if italic_file:
        italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-style: italic;\n    src: url("Fonts/{italic_file}");\n}}'
    
    bold_italic_face = ''
    if bold_italic_file:
        bold_italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    font-style: italic;\n    src: url("Fonts/{bold_italic_file}");\n}}'
    
    return EPUB3_FONT_STYLES.format(
        primary_font=primary_font_name,
        primary_file=primary_file,
        bold_face=bold_face,
        italic_face=italic_face,
        bold_italic_face=bold_italic_face,
    )
