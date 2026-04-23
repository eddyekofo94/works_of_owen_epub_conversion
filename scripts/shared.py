"""
Shared constants for John Owen Works PDF → EPUB conversion.
All conversion scripts import from here — single source of truth for
volume metadata, Greek Beta Code maps, Hebrew Gideon maps, and styles.
"""

import unicodedata

# ============================================================================
# VOLUME METADATA
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


# ============================================================================
# GREEK BETA CODE CONVERTER
# ============================================================================
# AGES Koine-Medium font maps ASCII characters to Greek glyphs.
# We reverse that mapping back to proper Unicode polytonic Greek.

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

SMOOTH = '\u0313'
ROUGH = '\u0314'
ACUTE = '\u0301'
GRAVE = '\u0300'
CIRCUMFLEX = '\u0342'
IOTASUB = '\u0345'

DIACRITIC_CHARS = set('><=~]J[j}|{=')
DIACRITIC_MAP = {
    'j': (SMOOTH,),
    'J': (ROUGH,),
    '>': (ACUTE,),
    '<': (GRAVE,),
    '~': (CIRCUMFLEX,),
    '=': (CIRCUMFLEX,),
    ']': (SMOOTH, ACUTE),
    '}': (SMOOTH, ACUTE),
    '[': (ROUGH, ACUTE),
    '{': (ROUGH, ACUTE),
    '|': (IOTASUB,),
}


def convert_greek_word(word):
    """Convert a Beta Code word to Unicode Greek."""
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
        elif ch == 'v':
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
        while i < len(word) and word[i] in DIACRITIC_CHARS:
            d = word[i]
            if d in DIACRITIC_MAP:
                for c in DIACRITIC_MAP[d]:
                    result.append(c)
            i += 1
    return unicodedata.normalize('NFC', ''.join(result))


# ============================================================================
# HEBREW GIDEON FONT CONVERTER
# ============================================================================
# AGES Gideon-Medium font maps ASCII characters to Hebrew glyphs.
# Text is stored in visual L→R order (reversed from Hebrew reading direction).
# Each consonant may be followed by its vowel mark.

GIDEON_CHAR_MAP = {
    'a': '\u05D0', 'b': '\u05D1', 'c': '\u05E1', 'd': '\u05D3',
    'f': '\u05D8', 'g': '\u05D2', 'h': '\u05D4', 'j': '\u05D7',
    'k': '\u05DB', 'l': '\u05DC', 'm': '\u05DE', 'n': '\u05E0',
    'q': '\u05E7', 'r': '\u05E8', 't': '\u05EA', 'v': '\u05E9\u05C1',
    'w': '\u05D5', 'x': '\u05E6', 'y': '\u05D9', '[': '\u05E2',
    'A': '\u05D0',       'B': '\u05D1\u05BC', 'D': '\u05D3\u05BC',
    'G': '\u05D2\u05BC', 'K': '\u05DB\u05BC', 'M': '\u05DD',
    'N': '\u05DF',       'P': '\u05E3',       'Q': '\u05E7\u05BC',
    'T': '\u05EA\u05BC', 'W': '\u05D5\u05BC',
    ';': '\u05B8',   '}' : '\u05B2',   ']' : '\u05B0',
    '1': '\u05B7',   'e': '\u05B5',   'i': '\u05B4',
    'o': '\u05B9',   'O': '\u05B9',
    ',': ',', ' ': ' ',
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
    """Convert Gideon font-encoded text to Unicode Hebrew."""
    import re
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
            mapped_chars.append('\u05BE')
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
    return ''.join(result)


# ============================================================================
# EPUB STYLESHEET
# ============================================================================

EPUB_STYLESHEET = r"""
/* Banner of Truth style — clean serif, elegant hierarchy */
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.65;
    color: #1a1a1a;
    margin: 1em 1.2em;
    -webkit-hyphens: auto;
    hyphens: auto;
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

h2 {
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
}

h3 {
    font-size: 1.05em;
    font-weight: bold;
    margin: 1.2em 0 0.4em;
}

p {
    text-indent: 1.5em;
    margin: 0.3em 0;
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
    margin: 0.3em 0 0.3em 1.5em;
    font-size: 0.9em;
}

a.footnote-ref {
    text-decoration: none;
    color: inherit;
    vertical-align: super;
    font-size: 0.75em;
}

/* Title page */
.title-page {
    text-align: center;
    margin-top: 20%;
    page-break-after: always;
}
.title-page h1 {
    font-size: 1.8em;
    margin-bottom: 0.3em;
    text-align: center;
}
.title-page .subtitle {
    font-size: 1.2em;
    font-style: italic;
    margin: 0.8em 0 2em;
}
.title-page .author {
    font-size: 1.1em;
    margin-top: 2em;
}
.title-page .publisher {
    margin-top: 3em;
    font-size: 0.9em;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* Treatise title pages */
.treatise-title {
    text-align: center;
    margin: 2em 1em;
    page-break-after: always;
}
.treatise-title h1, .treatise-title h2 {
    text-align: center;
    margin-bottom: 1em;
}
.treatise-title p {
    text-indent: 0;
    text-align: center;
    margin: 0.3em 0;
}
.treatise-title .connector {
    font-weight: bold;
    font-size: 0.85em;
    letter-spacing: 0.1em;
    margin: 1em 0;
    text-indent: 0;
    text-align: center;
}
.treatise-title .desc {
    font-style: italic;
    font-size: 0.95em;
    margin: 0.4em 2em;
    text-indent: 0;
    text-align: center;
}
.treatise-title .epigraph {
    font-size: 0.9em;
    margin: 2em 2em 1em;
    text-indent: 0;
    text-align: center;
}
"""