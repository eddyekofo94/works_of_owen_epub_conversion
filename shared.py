"""
Shared constants for John Owen Works PDF → EPUB conversion.
All conversion scripts import from here — single source of truth for
volume metadata, Greek Beta Code maps, Hebrew Gideon maps, font pools,
and EPUB3 stylesheets.
"""

import unicodedata

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
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
        'front_matter_skip': 3,
    },
    2: {
        'title': 'The Works of John Owen, Volume 2: Communion with God',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    3: {
        'title': 'The Works of John Owen, Volume 3: The Holy Spirit',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    4: {
        'title': 'The Works of John Owen, Volume 4: The Work of the Spirit',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    5: {
        'title': 'The Works of John Owen, Volume 5: Faith and Its Evidences',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ccel_xml',
        'ccel_file': 'special_sources/owen-v5-justification.xml',
    },
    6: {
        'title': 'The Works of John Owen, Volume 6: Temptation and Sin',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    7: {
        'title': 'The Works of John Owen, Volume 7: Sin and Grace',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    8: {
        'title': 'The Works of John Owen, Volume 8: Sermons to the Nation',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    9: {
        'title': 'The Works of John Owen, Volume 9: Sermons to the Church',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    10: {
        'title': 'The Works of John Owen, Volume 10: The Death of Christ',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ccel_xml',
        'ccel_file': 'special_sources/owen-10-deathofdeath.xml',
    },
    11: {
        'title': 'The Works of John Owen, Volume 11: Continuing in the Faith',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    12: {
        'title': 'The Works of John Owen, Volume 12: The Gospel Defended',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    13: {
        'title': 'The Works of John Owen, Volume 13: Ministry and Fellowship',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    14: {
        'title': 'The Works of John Owen, Volume 14: True and False Religion',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    15: {
        'title': 'The Works of John Owen, Volume 15: Church Purity and Unity',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'ages_pdf',
    },
    16: {
        'title': 'The Works of John Owen, Volume 16: The Church and the Bible',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
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
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    2: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 2',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    3: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 3',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    4: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 4',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    5: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 5',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    6: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 6',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
        'source_type': 'epub2',
    },
    7: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 7',
        'authors': ['John Owen'],
        'publisher': 'Banner of Truth Trust',
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
    'u': 'υ', 'f': 'φ', 'c': 'χ', 'y': 'υ', 'v': 'ψ', 'w': 'ω',
}

GREEK_UPPER = {
    'A': 'Α', 'B': 'Β', 'G': 'Γ', 'D': 'Δ', 'E': 'Ε',
    'Z': 'Ζ', 'H': 'Η', 'Q': 'Θ', 'I': 'Ι', 'K': 'Κ',
    'L': 'Λ', 'M': 'Μ', 'N': 'Ν', 'X': 'Ξ', 'O': 'Ο',
    'P': 'Π', 'R': 'Ρ', 'S': 'Σ', 'T': 'Τ',
    'U': 'Υ', 'F': 'Φ', 'C': 'Χ', 'Y': 'Υ', 'V': 'Ψ', 'W': 'Ω',
}
ALL_GREEK = {**GREEK_LOWER, **GREEK_UPPER}

SMOOTH = '\u0313'
ROUGH = '\u0314'
ACUTE = '\u0301'
GRAVE = '\u0300'
CIRCUMFLEX = '\u0342'
IOTASUB = '\u0345'

DIACRITIC_CHARS = set('><=~]J[j}|{=+')
DIACRITIC_MAP = {
    'j': (SMOOTH,),
    'J': (ROUGH,),
    '>': (ACUTE,),
    '<': (GRAVE,),
    '~': (CIRCUMFLEX,),
    '=': (CIRCUMFLEX,),
    '+': (CIRCUMFLEX,),
    ']': (SMOOTH, ACUTE),
    '}': (SMOOTH, CIRCUMFLEX),
    '[': (ROUGH, ACUTE),
    '{': (ROUGH, CIRCUMFLEX),
    '|': (IOTASUB,),
}


def convert_greek_word(word):
    """Convert a Beta Code word to Unicode Greek.
    
    Handles sigma form: 'v' maps to ς (final sigma) at word end,
    σ (medial sigma) elsewhere.
    """
    result = []
    i = 0
    in_word = True
    while i < len(word):
        ch = word[i]
        if ch in GREEK_LOWER:
            if i == len(word) - 1 and ch == 's':
                result.append('ς')
            else:
                if ch == 'v':
                    result.append('ς')
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


# ============================================================================
# HEBREW GIDEON FONT CONVERTER
# ============================================================================

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
    ';': '\u05B8',   '}': '\u05B2',   ']': '\u05B0',
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
    """Convert Gideon font-encoded text to Unicode Hebrew.
    
    Text is stored in visual L→R order; reverses per word and reverses
    word order to produce logical R→L Hebrew.
    """
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
# FONT POOLS
# ============================================================================

FONT_POOLS = {
    'owen_primary': [
        {
            'name': 'SBL_BLit',
            'files': {'SBL_BLit.ttf': 'SBL_BLit/SBL_BLit.ttf'},
        },
        {
            'name': 'Cardo',
            'files': {
                'Cardo-Regular.ttf': 'Cardo/Cardo-Regular.ttf',
                'Cardo-Bold.ttf': 'Cardo/Cardo-Bold.ttf',
                'Cardo-Italic.ttf': 'Cardo/Cardo-Italic.ttf',
            },
        },
        {
            'name': 'Libertinus',
            'files': {
                'LibertinusSerif-Regular.otf': 'Libertinus/LibertinusSerif-Regular.otf',
                'LibertinusSerif-Bold.otf': 'Libertinus/LibertinusSerif-Bold.otf',
                'LibertinusSerif-Italic.otf': 'Libertinus/LibertinusSerif-Italic.otf',
                'LibertinusSerif-BoldItalic.otf': 'Libertinus/LibertinusSerif-BoldItalic.otf',
            },
        },
    ],
}

SBL_SUPPLEMENTS = {
    'SBL_BLit.ttf': 'SBL_BLit/SBL_BLit.ttf',
    'SBL_grk.ttf': 'SBL_BLit/SBL_grk.ttf',
    'SBL_Hbrw.ttf': 'SBL_BLit/SBL_Hbrw.ttf',
}

EZRA_SIL_FILES = {
    'SILEOT.ttf': 'EzraSIL2.51/SILEOT.ttf',
}


def select_primary_font(vol_name, pool_key='owen_primary'):
    """Select a primary font deterministically based on volume name.
    
    Uses hashlib.md5 for deterministic selection (Python's built-in hash()
    is salted per-process in Python 3.3+ and not deterministic).
    """
    import hashlib
    pool = FONT_POOLS.get(pool_key, FONT_POOLS['owen_primary'])
    idx = int(hashlib.md5(vol_name.encode()).hexdigest(), 16) % len(pool)
    return pool[idx]


# ============================================================================
# EPUB STYLESHEET (GEMINI.md compliant)
# ============================================================================

EPUB_STYLESHEET = r"""
/* Banner of Truth style — clean serif, elegant hierarchy */
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.65;
    color: #1a1a1a;
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
    color: #1a1a1a;
    page-break-before: avoid;
}
.titlepage h2,
.title-page h2 {
    font-weight: bold;
    font-size: 1.25em;
    line-height: 1.35;
    color: #1a1a1a;
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

h2 {
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
}

h3 {
    text-align: center;
    font-size: 1.05em;
    font-weight: bold;
    margin: 1.2em 0 0.4em;
}

.chapter-subtitle {
    text-align: center;
    font-size: 1.05em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    line-height: 1.35;
    margin: 0.4em 0 1em;
    text-indent: 0;
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
    color: #000080; /* Navy Blue matching PDF */
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
    font-size: 0.95em;
}

a.fn-link {
    color: #0000EE;
    text-decoration: none;
    font-size: 0.85em;
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
    font-size: 0.85rem;
    display: inline-block;
    line-height: 1;
    margin-left: 0.25em;
    margin-right: 0.08em;
    padding: 0 0.14em;
    text-indent: 0;
}

.noteref + .noteref {
    margin-left: 0.35em;
}

.noteref sup {
    line-height: 1;
}

.doxology {
    text-align: center;
    text-indent: 0;
    margin: 2em 0 1.2em;
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
[lang="el"], [lang="el"] * {{
    font-family: "SBL Greek", "Cardo", "SBL BibLit", serif !important;
    font-size: 1.15em;
}}
[lang="he"], [lang="he"] * {{
    direction: rtl;
    unicode-bidi: embed;
    font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif !important;
    font-size: 1.5em;
    line-height: 1.24;
}}
[lang="he"], [lang="he"] p,
[lang="he"], [lang="he"] div {{
    text-align: left;
}}
.noteref {{
    color: #0000EE;
    text-decoration: none;
    vertical-align: super;
    font-size: 0.85rem;
    display: inline-block;
    line-height: 1;
    margin-left: 0.25em;
    margin-right: 0.08em;
    padding: 0 0.14em;
    text-indent: 0;
}}
.noteref + .noteref {{
    margin-left: 0.35em;
}}
.noteref sup {{
    line-height: 1;
}}
.doxology {{
    text-align: center;
    text-indent: 0;
    margin: 2em 0 1.2em;
}}
.footnote {{
    font-size: 0.9em;
    text-indent: 0;
    margin: 0.3em 0;
}}
a.fn-link {{
    color: #0000EE;
    text-decoration: none;
    font-size: 0.85em;
    margin-right: 0.3em;
}}
aside[epub\:type~="footnote"] {{
    display: block;
}}
aside[epub\:type~="endnote"] {{
    margin-bottom: 0.8em;
    padding-left: 1.8em;
    text-indent: -1.8em;
}}
"""


def generate_font_styles(primary_font_name, primary_font_files):
    """Generate per-XHTML inline <style> block with @font-face declarations.
    
    Font files are stored flat in Fonts/ (no subdirectories), so we use
    os.path.basename() to flatten paths like 'Cardo/Cardo-Regular.ttf' → 'Cardo-Regular.ttf'.
    
    Returns the complete <style> element content as a string.
    """
    import os as _os
    
    # Find primary font file (basename only — files stored flat in Fonts/)
    primary_file = _os.path.basename(list(primary_font_files.values())[0])
    bold_file = None
    italic_file = None
    bold_italic_file = None
    
    for rel_path, font_file in primary_font_files.items():
        if 'Bold' in font_file and 'Italic' in font_file and 'Semi' not in font_file:
            bold_italic_file = _os.path.basename(font_file)
        elif 'Bold' in font_file and 'Semi' not in font_file:
            bold_file = _os.path.basename(font_file)
        elif 'Italic' in font_file and 'Semi' not in font_file:
            italic_file = _os.path.basename(font_file)
    
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
