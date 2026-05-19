"""
Shared constants for John Owen Works PDF → EPUB conversion.
All conversion scripts import from here — single source of truth for
volume metadata, Greek Beta Code maps, Hebrew Gideon maps, font pools,
and EPUB3 stylesheets.
"""

import unicodedata
import re
import os
import sys
import json
from copy import deepcopy
from pathlib import Path

GREEK_FONT_MARKERS = ('Koine',)
HEBREW_FONT_MARKERS = ('Gideon',)
GREEK_UNICODE_RE = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')
HEBREW_UNICODE_RE = re.compile(r'[\u0590-\u05FF]')


def is_greek_font(font_name):
    """Return True for AGES Koine font names, including subset prefixes."""
    font = font_name or ''
    return any(marker.lower() in font.lower() for marker in GREEK_FONT_MARKERS)


def is_hebrew_font(font_name):
    """Return True for AGES Gideon font names, including subset prefixes."""
    font = font_name or ''
    return any(marker.lower() in font.lower() for marker in HEBREW_FONT_MARKERS)


def contains_greek(text):
    return bool(GREEK_UNICODE_RE.search(text or ''))


def contains_hebrew(text):
    return bool(HEBREW_UNICODE_RE.search(text or ''))

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

# Global Volume Configuration
# NOTE: Volume-specific OCR fixes or layout hooks MUST be kept in
# volumes/vN/convert.py via the OVERRIDES dictionary to keep this file clean.
#
# Supported OVERRIDES keys (in addition to any VOLUME_CONFIG key):
#   page_height (int)  — PDF page height in pts; default 626. Override when a
#                        volume's PDF has non-standard dimensions so that
#                        coordinate_redactor clips the correct margin zones.
#   top_margin (int)   — top margin strip in pts; default 35.
#   bottom_margin (int)— bottom margin strip in pts; default 20.
#   post_extract_hook  — callable(intermediate_dict) → intermediate_dict for
#                        structural re-tagging after Stage 1 extraction.
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
        'treatises': [
            'Xristologia: Or, A Declaration of the Glorious Person of Christ, God and Man',
            'Meditations and Discourses on the Glory of Christ',
            'Meditations and Discourses on the Glory of Christ Applied to Sinners and Saints',
            'Two Short Catechisms'
        ],
        'text_replacements': {
            # Moved to volumes/v1/convert.py (Issue 26 cleanup)
        },
        'regex_replacements': {
            r'(\w+)]y\b': r'\1ly',
            r'\]earne': r'learne',
            r'\]earnt': r'learnt',
        }
    },
    2: {
        'title': 'The Works of John Owen, Volume 2: Communion with God',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Of Communion with God the Father, Son, and Holy Ghost, Each Person Distinctly, in Love, Grace, and Consolation',
            'A Vindication of Some Passages in a Discourse Concerning Communion with God',
            'A Brief Declaration and Vindication of the Doctrine of the Trinity'
        ]
    },
    3: {
        'title': 'The Works of John Owen, Volume 3: The Holy Spirit',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Pneumatologia: Or, A Discourse Concerning the Holy Spirit (Books I–V)'
        ]
    },
    4: {
        'title': 'The Works of John Owen, Volume 4: The Work of the Spirit',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The Reason of Faith',
            'Causes, Ways, and Means, of Understanding the Mind of God',
            'A Discourse Concerning the Work of the Holy Spirit in Prayer',
            'A Discourse Concerning the Holy Spirit and His Spiritual Gifts'
        ]
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
        'treatises': [
            'The Doctrine of Justification by Faith',
            'Evidences of the Faith of God’s Elect'
        ]
    },
    6: {
        'title': 'The Works of John Owen, Volume 6: Temptation and Sin',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Of the Mortification of Sin in Believers',
            'Of Temptation: The Nature and Power of It',
            'The Nature, Power, Deceit, and Prevalency of the Remainders of Indwelling Sin in Believers',
            'A Practical Exposition upon Psalm 130'
        ]
    },
    7: {
        'title': 'The Works of John Owen, Volume 7: Sin and Grace',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The Nature and Causes of Apostasy from the Profession of the Gospel',
            'The Grace and Duty of Being Spiritually-Minded',
            'A Treatise of the Dominion of Sin and Grace'
        ]
    },
    8: {
        'title': 'The Works of John Owen, Volume 8: Sermons to the Nation',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Sermons to the Nation (Sermons before the Long Parliament, Oliver Cromwell, and the Commonwealth)'
        ]
    },
    9: {
        'title': 'The Works of John Owen, Volume 9: Sermons to the Church',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Posthumous Sermons (83 Pastoral Sermons)',
            'Discourses Resolving Practical Cases of Conscience',
            'Discourses Intended as Preparation for the Lord’s Table'
        ]
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
        'treatises': [
            'A Display of Arminianism',
            'Salus Electorum, Sanguis Jesu: Or, The Death of Death in the Death of Christ',
            'Of the Death of Christ (A Reply to Richard Baxter)',
            'A Dissertation on Divine Justice'
        ]
    },
    11: {
        'title': 'The Works of John Owen, Volume 11: Continuing in the Faith',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The Doctrine of the Saints’ Perseverance Explained and Confirmed'
        ]
    },
    12: {
        'title': 'The Works of John Owen, Volume 12: The Gospel Defended',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Vindiciae Evangelicae: Or, The Mystery of the Gospel Vindicated and Socinianism Examined',
            'Of the Death of Christ, and of Justification',
            'A Review of the Annotations of Hugo Grotius'
        ]
    },
    13: {
        'title': 'The Works of John Owen, Volume 13: Ministry and Fellowship',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The Duty of Pastors and People Distinguished',
            'Eshcol: A Cluster of the Fruit of Canaan (Rules for Church Fellowship)',
            'Of Schism: The True Nature of It Stated',
            'A Review of the True Nature of Schism',
            'An Answer to a Late Treatise About Schism'
        ]
    },
    14: {
        'title': 'The Works of John Owen, Volume 14: True and False Religion',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Brill_font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'Animadversions on a Treatise Entitled "Fiat Lux"',
            'Fiat Lux Examined'
        ]
    },
    15: {
        'title': 'The Works of John Owen, Volume 15: Church Purity and Unity',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'A Discourse Concerning Liturgies, and Their Imposition',
            'A Brief Instruction in the Worship of God (The Independents\' Catechism)',
            'An Inquiry into the Original, Nature, Institution, Power, Order, and Communion of Evangelical Churches'
        ]
    },
    16: {
        'title': 'The Works of John Owen, Volume 16: The Church and the Bible',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The True Nature of a Gospel Church and Its Government',
            'Tracts on Excommunication and Church Censures',
            'Of Infant Baptism and Of Dipping',
            'Of the Divine Original, Authority, Self-Evidencing Light, and Power of the Scriptures',
            'Integrity and Purity of the Hebrew and Greek Text of the Scripture'
        ]
    },
}


def _deep_merge_config(base, override):
    """Return a recursive copy of base updated with override values."""
    result = deepcopy(base or {})
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge_config(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def merge_volume_config(vol_num, overrides=None):
    """Merge shared volume metadata with per-volume overrides.

    Per-volume scripts should pass their OVERRIDES through this helper rather
    than using a shallow dict spread. Nested maps such as text/regex
    replacements and title overrides then compose predictably.
    """
    return _deep_merge_config(VOLUME_CONFIG.get(vol_num, {}), overrides or {})


def run_volume_cli(vol_num, overrides=None, description=None):
    """Shared CLI for volumes/vN/convert.py entrypoints."""
    import argparse
    from extract import extract_volume
    from render import render_volume

    parser = argparse.ArgumentParser(
        description=description or f'Convert Owen Works Volume {vol_num}',
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
        print(f'=== Volume {vol_num}: Stage 1 — Extract ===')
        intermediate = extract_volume(vol_num, overrides=overrides)
        
        # Issue: Blemish fixes often require post-processing the whole intermediate JSON
        # (e.g. merging chapters, structural re-tagging) before rendering.
        post_extract_hook = (overrides or {}).get('post_extract_hook')
        if post_extract_hook:
            print(f'[shared] Running post_extract_hook for Volume {vol_num}')
            intermediate = post_extract_hook(intermediate)
            # Write back the modified intermediate
            vol_dir = Path(__file__).parent / 'volumes' / f'v{vol_num}'
            out_json = vol_dir / 'intermediate' / f'volume_{vol_num}.json'
            with open(out_json, 'w', encoding='utf-8') as f:
                json.dump(intermediate, f, indent=2, ensure_ascii=False)

    if not args.extract_only:
        print(f'=== Volume {vol_num}: Stage 2 — Render ===')
        render_volume(vol_num, overrides=overrides)

    print(f'=== Volume {vol_num}: Done ===')

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
        'treatises': [
            'Concerning the Epistle to the Hebrews (Exercitations Part 1)',
            'Concerning the Messiah',
            'Concerning the Jewish Church'
        ]
    },
    2: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 2',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Gentium-plus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': [
            'The Sacerdotal Office of Christ (Exercitations Part 2)',
            'A Day of Sacred Rest (Treatise on the Sabbath)',
            'Summary of Observations on Hebrews'
        ]
    },
    3: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 3',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Adobe-garamond-pro-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 1:1 - 3:6']
    },
    4: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 4',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 3:7 - 5:14']
    },
    5: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 5',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Minion_pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 6:1 - 7:28']
    },
    6: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 6',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'Baskervville/static',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 8:1 - 10:39']
    },
    7: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 7',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'sabon-next-lt',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 11:1 - 13:25']
    },
}

# ============================================================================
# CHARACTER NORMALIZATION — Gideon/AGES Legacy Artifacts
# ============================================================================

GIDEON_CHAR_MAP = {
    # === Punctuation & Smart Quotes (The U+2018 Group) ===
    '\u2018': "'",      # Left single quotation mark
    '\u2019': "'",      # Right single quotation mark / Typographic Apostrophe
    '\u201C': '"',      # Left double quotation mark
    '\u201D': '"',      # Right double quotation mark
    '\u2014': '—',      # Em-dash (Crucial for Owen's long, nested parenthetical clauses)
    '\u2013': '-',      # En-dash
    '\u2026': '...',    # Ellipsis points
    '\u00A0': ' ',      # Non-breaking space (often inserted around punctuation marks)

    # === Latin Extended-A / Diacritics (The U+00CB & U+00E3 Group) ===
    '\u00CB': 'Ë',      # Capital E with diaeresis
    '\u00EB': 'ë',      # Lowercase e with diaeresis (Commonly used in early English spellings)
    '\u00E3': 'ã',      # Lowercase a with tilde
    '\u00C3': 'Ã',      # Capital a with tilde
    '\u00E9': 'é',      # Lowercase e with acute accent (Used in French-derived loan words)
    '\u00E8': 'è',      # Lowercase e with grave accent
    '\u00E2': 'â',      # Lowercase a with circumflex
    '\u00F4': 'ô',      # Lowercase o with circumflex
    '\u00EF': 'ï',      # Lowercase i with diaeresis

    # === Historical Orthography & Ligatures (Legacy Text Layers) ===
    '\u00E6': 'ae',     # Lowercase ae ligature (æ) - e.g., "praedestination"
    '\u00C6': 'AE',     # Capital AE ligature (Æ)
    '\u0153': 'oe',     # Lowercase oe ligature (œ) - e.g., "foederis"
    '\u0152': 'OE',     # Capital OE ligature (Œ)
    '\u017F': 's',      # Historical Long 's' (ſ) - standardizes to modern lowercase 's'
    
    # === Mathematical & Logical Symbols (Used in Owen's Dialectical Schemes) ===
    '\u2234': '∴',      # Therefore symbol (Commonly used to flag a logical "Ratio" or "Usus")
    '\u2235': '∵',      # Because symbol
    '\u2020': '†',      # Dagger (Primary footnote anchor marker)
    '\u2021': '‡',      # Double dagger (Secondary footnote anchor marker)
    '\u00A7': '§'       # Section marker (Used heavily in multi-layered legal/theological outlines)
}


def normalize_characters(text: str) -> str:
    """
    Apply GIDEON_CHAR_MAP to normalize legacy AGES artifacts, smart punctuation,
    and historical ligatures to modern Unicode equivalents.
    """
    if not text:
        return ""
    
    # Use a translation table for efficiency
    trans_table = str.maketrans(GIDEON_CHAR_MAP)
    return text.translate(trans_table)


# ============================================================================
# GREEK BETA CODE CONVERTER
# ============================================================================

GREEK_LOWER = {
    'a': '\u03b1',  # alpha (α)
    'b': '\u03b2',  # beta (β)
    'g': '\u03b3',  # gamma (γ)
    'd': '\u03b4',  # delta (δ)
    'e': '\u03b5',  # epsilon (ε)
    'z': '\u03b6',  # zeta (ζ)
    'h': '\u03b7',  # eta (η)
    'q': '\u03b8',  # theta (θ)
    'i': '\u03b9',  # iota (ι)
    'k': '\u03ba',  # kappa (κ)
    'l': '\u03bb',  # lambda (λ)
    'm': '\u03bc',  # mu (μ)
    'n': '\u03bd',  # nu (ν)
    'c': '\u03c7',  # chi (χ) — AGES Koine uses 'c' for chi
    'o': '\u03bf',  # omicron (ο)
    'p': '\u03c0',  # pi (π)
    'r': '\u03c1',  # rho (ρ)
    's': '\u03c3',  # sigma (σ - medial, context → ς final)
    't': '\u03c4',  # tau (τ)
    'u': '\u03c5',  # upsilon (υ)
    'f': '\u03c6',  # phi (φ)
    'x': '\u03be',  # xi (ξ) — AGES Koine uses 'x' for xi
    'y': '\u03c8',  # psi (ψ)
    'w': '\u03c9',  # omega (ω)
    'v': '\u03c2',  # final sigma (ς) — explicit AGES marker
}

GREEK_UPPER = {
    'A': '\u0391',  # Alpha (Α)
    'B': '\u0392',  # Beta (Β)
    'G': '\u0393',  # Gamma (Γ)
    'D': '\u0394',  # Delta (Δ)
    'E': '\u0395',  # Epsilon (Ε)
    'Z': '\u0396',  # Zeta (Ζ)
    'H': '\u0397',  # Eta (Η)
    'Q': '\u0398',  # Theta (Θ)
    'I': '\u0399',  # Iota (Ι)
    'K': '\u039a',  # Kappa (Κ)
    'L': '\u039b',  # Lambda (Λ)
    'M': '\u039c',  # Mu (Μ)
    'N': '\u039d',  # Nu (Ν)
    'C': '\u03a7',  # Chi (Χ) — AGES Koine uses 'C' for chi
    'O': '\u039f',  # Omicron (Ο)
    'P': '\u03a0',  # Pi (Π)
    'R': '\u03a1',  # Rho (Ρ)
    'S': '\u03a3',  # Sigma (Σ)
    'T': '\u03a4',  # Tau (Τ)
    'U': '\u03a5',  # Upsilon (Υ)
    'F': '\u03a6',  # Phi (Φ)
    'X': '\u039e',  # Xi (Ξ) — AGES Koine uses 'X' for xi
    'Y': '\u03a5',  # Upsilon (Υ) — AGES Koine uses 'Y' for uppercase upsilon
    'W': '\u03a9',  # Omega (Ω)
    'V': '\u03a3',  # Final sigma (uppercase, rare)
}
ALL_GREEK = {**GREEK_LOWER, **GREEK_UPPER}

SMOOTH = '\u0313'
ROUGH = '\u0314'
ACUTE = '\u0301'
GRAVE = '\u0300'
CIRCUMFLEX = '\u0342'
IOTASUB = '\u0345'

DIACRITIC_CHARS = set('><=~]J[j}|{=+\'')
# DIACRITIC_MAP: Maps AGES/Beta Code marks to Unicode combining diacritics.
DIACRITIC_MAP = {
    'j': ('\u0313',),        # SMOOTH breathing
    'J': ('\u0314',),        # ROUGH breathing
    '>': ('\u0301',),        # ACUTE accent
    '<': ('\u0300',),        # GRAVE accent
    '\'': ('\u0301',),       # ACUTE accent
    '~': ('\u0342',),        # CIRCUMFLEX
    '=': ('\u0342',),        # CIRCUMFLEX
    '+': ('\u0342',),        # CIRCUMFLEX
    ']': ('\u0313', '\u0301'), # SMOOTH + ACUTE
    '}': ('\u0313', '\u0342'), # SMOOTH + CIRCUMFLEX
    '[': ('\u0314', '\u0301'), # ROUGH + ACUTE
    '{': ('\u0314', '\u0342'), # ROUGH + CIRCUMFLEX
    '|': ('\u0345',),        # IOTA subscript
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
      - 'y' → final sigma ς (Issue 26/7: frequent in AGES)
    """
    if not word:
        return ""

    # AGES-specific: handle 'h' as rough breathing marker.
    # In some AGES fonts, 'h' is a prefix for rough breathing.
    # Note: 'h' in standard Beta Code is Eta (handled in GREEK_LOWER).
    # We only treat 'h' as breathing if it is followed by a vowel AND not
    # preceded by another letter (i.e. start of word).
    VOWELS_PLAIN = set('aeiouwAEIOUW')
    temp_word = []
    w_chars = list(word)
    idx = 0
    while idx < len(w_chars):
        c = w_chars[idx]
        if c == 'h' and idx == 0 and idx + 1 < len(w_chars) and w_chars[idx+1] in VOWELS_PLAIN:
            # Prefix 'h' at start of word -> move breathing marker AFTER the vowel
            vowel = w_chars[idx+1]
            temp_word.append(vowel)
            temp_word.append('J') # J is ROUGH breathing in our map
            idx += 2
            continue
        temp_word.append(c)
        idx += 1
    word = "".join(temp_word)

    result = []
    i = 0
    while i < len(word):
        ch = word[i]
        # Determine the next non-diacritic character for sigma-end detection
        if ch in GREEK_LOWER:
            # Check for final sigma: 's' or 'y' is final only when it is the last
            # alphabetic character in the current WORD (stops at space).
            if ch == 's' or ch == 'y':
                # Look ahead for any more Greek letters before the next space or word end
                rest_alpha = []
                for j in range(i + 1, len(word)):
                    if word[j] == ' ': break
                    if word[j].lower() in GREEK_LOWER:
                        rest_alpha.append(word[j])
                
                if not rest_alpha:
                    result.append('ς')
                else:
                    # 'y' is 'psi' if not final; 's' is 'sigma'
                    result.append('σ' if ch == 's' else 'ψ')
            else:
                result.append(GREEK_LOWER[ch])
            i += 1
            # Process following diacritics for this character
            while i < len(word) and (word[i] in DIACRITIC_CHARS or word[i] == 'J'):
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
            while i < len(word) and (word[i] in DIACRITIC_CHARS or word[i] == 'J'):
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

HEBREW_GIDEON_MAP = {
    # ── Consonants (Gideon / AGES legacy encoding) ────────────────────────
    # Backed by the public Gideon-Medium character map and by a 16-volume
    # scan of actual Gideon-Medium PDF spans. Keep this table explicit:
    # unknown characters in Gideon spans are extraction bugs, not prose.
    'a': '\u05d0',  # Aleph (א)
    'b': '\u05d1',  # Beth (ב)
    'g': '\u05d2',  # Gimel (ג)
    'd': '\u05d3',  # Dalet (ד)
    'h': '\u05d4',  # He (ה)
    'H': '\u05d4',  # He (ה) uppercase variant
    'w': '\u05d5',  # Waw (ו)
    'z': '\u05d6',  # Zayin (ז)
    'Z': '\u05d6',  # Zayin (ז) uppercase variant
    'j': '\u05d7',  # Het (ח)
    'J': '\u05d7',  # Het (ח) uppercase/scan variant
    'f': '\u05d8',  # Tet (ט)
    'F': '\u05d8',  # Tet (ט) uppercase variant
    'y': '\u05d9',  # Yodh (י)
    'Y': '\u05d9',  # Yodh (י) uppercase variant
    'k': '\u05db',  # Kaph (כ)
    'K': '\u05db\u05bc',  # Kaph + Dagesh (כּ)
    'l': '\u05dc',  # Lamedh (ל)
    'L': '\u05dc',  # Lamedh (ל) uppercase variant
    'm': '\u05de',  # Mem (מ)
    'M': '\u05de',  # Mem (מ) uppercase variant
    'n': '\u05e0',  # Nun (נ)
    'N': '\u05e0',  # Nun (נ) uppercase variant
    's': '\u05e1',  # Samekh (ס)
    'S': '\u05e1\u05bc',  # Samekh + Dagesh (סּ)
    '[': '\u05e2',  # Ayin (ע)
    'p': '\u05e4',  # Pe (פ)
    'P': '\u05e4',  # Pe (פ) uppercase variant
    'c': '\u05e6',  # Tsadi (צ)
    'C': '\u05e6',  # Tsadi (צ) uppercase variant
    'x': '\u05e6',  # Tsadi (צ) AGES variant
    'X': '\u05e5',  # Tsadi final (ץ)
    '\u2248': '\u05e5',  # ≈ → Tsadi final (ץ)
    'q': '\u05e7',  # Qoph (ק)
    'Q': '\u05e7\u05bc',  # Qoph + Dagesh (קּ)
    'r': '\u05e8',  # Resh (ר)
    'R': '\u05e8',  # Resh (ר) uppercase variant
    'v': '\u05e9\u05c1',  # Shin (שׁ)
    'V': '\u05e9\u05c1',  # Shin (שׁ) uppercase variant
    '\u00E7': '\u05e9\u05c1',  # ç → Shin (שׁ), e.g. ajyçm = משיחא
    't': '\u05ea',  # Taw (ת)
    'T': '\u05ea',  # Taw (ת)
    # ── Final forms / AGES high-byte variants ─────────────────────────────
    '\u00B5': '\u05dd',   # µ → Mem Final (ם)
    '\u02C6': '\u05df',   # ˆ → Nun Final (ן)
    '\u00E3': '\u05df',   # ã → Nun Final (ן)
    '\u00CB': '\u05da',   # Ë → Kaph Final (ך)
    '\u00DA': '\u05da',   # Ú → Kaph Final (ך)
    '\u02DA': '\u05da',   # ˚ → Kaph Final (ך)
    # ── Final forms (uppercase with dagesh) ───────────────────────────────
    'A': '\u05be',        # Maqef (־), often in compounds such as כָּל־
    'B': '\u05d1\u05bc',  # Bet + Dagesh
    'D': '\u05d3\u05bc',  # Dalet + Dagesh
    'G': '\u05d2\u05bc',  # Gimel + Dagesh
    'W': '\u05d5\u05bc',  # Vav + Dagesh (Shureq)
    # ── Vowel points / diacritics ─────────────────────────────────────────
    ';': '\u05b8',   # Qamats
    '}': '\u05b2',   # Hataf Patah
    ']': '\u05b0',   # Sheva
    '1': '\u05b7',   # Patah
    '\u00E6': '\u05b7',   # æ → Patah (Latin ae ligature artifact)
    ',': '\u05b6',   # Segol
    'e': '\u05b5',   # Tsere
    'E': '\u05b5',   # Tsere
    'i': '\u05b4',   # Hiriq
    'I': '\u05b4',   # Hiriq
    'o': '\u05b9',   # Holam
    'O': '\u05b9',   # Holam (alternate)
    'u': '\u05bb',   # Qubuts
    'U': '\u05bb',   # Qubuts
    '`': '\u05b0',   # Sheva (alternate)
    '=': '\u05bc',   # Dagesh / Mappiq
    '/': '\u05d5\u05b9',  # Vav + Holam, observed in מות-like forms
    # ── Punctuation / spacing ─────────────────────────────────────────────
    "'": '\u05be',        # Maqef / hyphen artifact
    '\u2018': '\u05be',   # ‘ → Maqef
    '\u2019': '\u05be',   # ’ → Maqef
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
    session) so gaps in HEBREW_GIDEON_MAP can be identified and filled.
    """
    _warned_chars: set = getattr(convert_gideon_hebrew, '_warned_chars', set())
    convert_gideon_hebrew._warned_chars = _warned_chars

    text = re.sub(
        r'\(cid:(\d+)\)',
        lambda m: GIDEON_CID_MAP.get(int(m.group(1)), ''),
        encoded
    )
    mapped_chars = []
    for ch in text:
        if ch in HEBREW_GIDEON_MAP:
            mapped_chars.append(HEBREW_GIDEON_MAP[ch])
        elif ch == '\u00AF':
            mapped_chars.append('\u05BE')  # Maqef
        elif ord(ch) > 127 and ch not in _warned_chars:
            # Non-ASCII character not in map — log once
            _warned_chars.add(ch)
            print(f"[GIDEON WARNING] Unmapped character U+{ord(ch):04X} ({repr(ch)}) — add to HEBREW_GIDEON_MAP", file=sys.stderr)
            mapped_chars.append(ch)
        else:
            mapped_chars.append(ch)
    flat = ''.join(mapped_chars)
    # Multiple extraction paths can emit adjacent maqef artifacts for the same
    # visual hyphen; collapse them before reversing logical Hebrew order.
    flat = re.sub('\u05be+', '\u05be', flat)

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
# PIPELINE CONSTANTS — shared between extract.py and render.py
# Moving these here eliminates the extract → render import dependency.
# ============================================================================

FOOTNOTE_MARKER_RE = re.compile(r'\[f(\d+)\]')
LOOSE_FOOTNOTE_MARKER_RE = re.compile(
    r'\[\s*f\s*(\d{1,3})\s*\]|'
    r'(?<=[a-z])f\s*(\d{1,3})(?=[a-z])|'
    r'(?<![A-Za-z])f\s*(\d{1,3})(?=[a-z])|'
    r'(?<=[a-z])f\s*(\d{1,3})\b|'
    r'(?<![A-Za-z])f\s*(\d{1,3})\b',
    re.I,
)
FOOTNOTE_PLACEHOLDER_RE = re.compile(r'FNREFTOKEN(\d+)TOKEN')
FT_MARKER_RE = re.compile(r'^ft(\d+)\s*', re.I)
EMPTY_BRACKET_RE = re.compile(r'\[\s*\]')

STRUCTURAL_START_RE = re.compile(
    r'^(?:(?:\*\*|__)?)'
    r'(?:'
    r'(?!\d{4}\.)\d{1,3}\.\s+|'                         # 5. Mankind...
    r'\((?!\d{4}\))\d+\.?\)\s+|'                    # (1.) There... / (1) There...
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\s+|'  # (1st,) Such...
    r'\[\d+\.?\]\.?\s+|'                    # [1.] There... / [1]. There...
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\.?\s+|'  # [1st,] There...
    r'[IVXLCDM]+\.\s+|'                  # I. / II.
    r'(?:Q\.|Ques\.|Ans\.|A\.\s*\d+\.)\s+|'                       # Q. / Ques. / Ans. / A. 1.
    r'(?:Obj(?:ection)?\.?\s*\d*\.?|Ans(?:wer)?\.?\s*\d*\.?|Sol(?:ution)?\.?\s*\d*\.?|Use\.?\s*\d+\.?)\s+|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]\s+|'  # 1st, 2nd, 3rd, 4th,
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?\s+|'  # 2ndly, 3rdly
    r'(?:First|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly|Again|But)\b[,.]?\s+'
    r')'
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
    r'\*\*\[\d+\.?\]\.?\*\*|'
    r'\*\*\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\.?\*\*|'
    r'\*\*\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)\*\*\s*[,.;]?|'
    r'\*\*[IVXLCDM]+\.\*\*|'
    r'[IVXLCDM]+\.|'
    r'(?<![:\d-])(?!\d{4}\.)\d+\.|'
    r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
    r'(?:Obj(?:ection)?\.?|Ans(?:wer)?\.?|Sol(?:ution)?\.?|Use\.?)\s*(?:\d+\.)?|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<trail>\s+)'
)
# ROMAN_HEADING_RE: Only match if the following text is short or All-Caps (Issue 21)
ROMAN_HEADING_RE = re.compile(
    r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?\s+'
    r'(?P<rest>[^a-z]{1,150}|[A-Z][a-z ]{1,45}|[A-Z][a-z ]{1,45}\.)$'
)
ROMAN_ONLY_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$')
PLAIN_CHAPTER_RE = re.compile(r'^(CHAPTER\s+\d+\.?)(?:\s+(.+))?$')
CITATION_ABBREV_TRAIL_RE = re.compile(
    r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|q|a|p|pp|sec|ad|m|aen|liv|hist)\.?\s*$'
    r'|'
    # Scholarly citation tails: "cap. 8," / "q. 81,"
    r'\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|pp|sec|ad|aen|liv|hist)'
    r'\.?\s+\d+(?:[-,;]\s*\d+)*,?\s*$'
    r'|'
    # Page references: "p. 43" or "pp. 43" — should not be sentence ends
    r'\bp+\.\s+\d{1,4}\s*$'
    r'|'
    # Classical references: "Aen. 10." / "Liv., Hist. viii."
    r'\b(?:Aen|Liv|Hist)\.?,?(?:\s+Hist\.?)?(?:\s+[ivxlcdm]+|\s+\d+)?\.\s*$'
    r'|'
    # Scripture book abbreviations before chapter:verse — e.g. "Cant. 5:10"
    r'\b(?:Cant|Prov|Eccl|Sol|Isa|Jer|Lam|Ezek|Dan|Hos|Zeph|Zech|Mal|'
    r'Matt|Mk|Lk|Jn|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Rev)\.\s*$',
    re.I,
)
CITATION_ABBREV_START_RE = re.compile(
    r'^(?:Lib|Serm|Sermo|Epist|Ep|Cap|Chap|Orat|Tract|Homil|Haer|Dial|Quest|Art|Dist|Part|Vol)\.?\s+',
    re.I,
)
CITATION_AUTHOR_TRAIL_RE = re.compile(
    r'\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|'
    r'Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan|Aquin|Alexand|Alens)\.?\s*$',
    re.I,
)
ROMAN_LIST_TOKEN = '@@ROMAN_LIST@@'
MARKDOWN_STRUCTURAL_START_RE = re.compile(
    r'^\*\*(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
    r'\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\*\*\s*[,.;]?\s+'
)

SCRIPTURE_BOOK_RE = (
    r'(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|'
    r'Proverbs|Ecclesiastes|Song(?:\s+of\s+Solomon)?|Isaiah|Jeremiah|Lamentations|Ezekiel|'
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

# ── Text-processing helpers ──────────────────────────────────────────────────

_SPACED_CAPS_RE = re.compile(r'\b([A-Z](?:\s[A-Z]){2,})\b')
_I_WILL_RE = re.compile(r'\bI\s*WILL\b|\bIWILL\b', re.I)
_I_AM_RE = re.compile(r'\bI\s*AM\b|\bIAM\b', re.I)


def _normalize_spaced_caps(text: str) -> str:
    """Collapse M E → ME, T H E → THE for all-caps spaced sequences."""
    def _join(m: re.Match) -> str:
        return m.group(1).replace(' ', '')
    return _SPACED_CAPS_RE.sub(_join, text)


def _normalize_i_will(text: str) -> str:
    """Normalize OCR forms like IWILL/I WILL without preserving false capitals."""
    text = _I_WILL_RE.sub('I will', text)
    text = _I_AM_RE.sub('I am', text)
    return text


def _normalize_scholarly_citation_artifacts(text: str) -> str:
    """Repair OCR punctuation that would split scholarly citation chains."""
    if not text:
        return text
    text = re.sub(
        r'\b(?P<label>cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|'
        r'dial|enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\s*\.\s*,\s*(?=\d)',
        lambda m: f'{m.group("label")}. ',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\b(?P<label>chapter|chap)\s*(?:\.\s*)?,\s*(?=\d)',
        lambda m: f'{m.group("label")} ' if m.group("label").lower() == 'chapter' else f'{m.group("label")}. ',
        text,
        flags=re.I,
    )
    return text


_QUOTE_WRAPPED_STRUCTURAL_RE = re.compile(
    r'(?P<prefix>^|[\s([{—–-])["“]\s*'
    r'(?='
    r'(?:'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]\.?|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\.?|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')'
    r')'
)


def _unwrap_quote_wrapped_structural_markers(text: str) -> str:
    """Remove OCR quote marks that wrap list/outline anchors, not quotations."""
    if not text:
        return text
    return _QUOTE_WRAPPED_STRUCTURAL_RE.sub(lambda m: m.group("prefix"), text)


def _repair_scripture_reference_artifacts(text: str) -> str:
    """Repair recurring OCR/reference punctuation artifacts from AGES PDFs."""
    if not text:
        return text
    # A single in-parenthesis reference can lose its closing parenthesis when
    # the following prose continues after a comma: "(John 6:63, to cause".
    text = re.sub(
        rf'\(\s*((?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*)'
        r',\s+(?=(?:to|and|or|that|which|who|where|whereby|for|in)\b)',
        r'(\1), ',
        text,
        flags=re.I,
    )
    # Page/line OCR occasionally duplicates a chapter reference as if it were
    # chapter:verse plus the same chapter again.
    text = re.sub(r'\bRomans\s+(\d+):1\s+\1\b', r'Romans \1', text)
    text = re.sub(r'\b1\s+Corinthians\s+(\d+):1\s*1\s+Corinthians\s+\1\b', r'1 Corinthians \1', text)
    return text


def _repair_owen_ocr_errors(text: str, config: dict = None) -> str:
    """Repair known OCR character misreads using volume-specific configuration."""
    text = _normalize_scholarly_citation_artifacts(text)
    text = _unwrap_quote_wrapped_structural_markers(text)
    text = _repair_scripture_reference_artifacts(text)
    text = re.sub(r'\b([A-Za-z]{2,})]y\b', r'\1ly', text)
    text = re.sub(r'\b([A-Za-z]{2,})]e\b', r'\1le', text)
    text = re.sub(r'(?<!\w)](?=earn|earning|earned|earnt|edge)', 'l', text, flags=re.I)
    text = re.sub(r'\bI\s+a\s+will\b', 'I will', text)
    if not config:
        return text

    corrections = config.get('text_replacements', {})
    regex_corrections = config.get('regex_replacements', {})

    result = text
    for wrong, right in corrections.items():
        if wrong.startswith('(') or wrong.endswith('\\b'):
            result = re.sub(wrong, right, result)
        else:
            result = re.sub(r'\b' + re.escape(wrong) + r'\b', right, result)

    for pattern, repl in regex_corrections.items():
        result = re.sub(pattern, repl, result)

    return result


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


_NAV_TITLE_MAX_CHARS = 100  # Apple Books truncates sidebar entries beyond this


def nav_display_title(text):
    """Return a title-cased label suitable for the EPUB nav sidebar.

    Front-matter labels are normalised to their canonical upper-case form.
    All other titles are title-cased.  Any result longer than
    _NAV_TITLE_MAX_CHARS is truncated with an ellipsis so that Apple Books
    does not silently cut mid-word.
    """
    stripped = (text or '').strip()
    normalized = stripped.rstrip('.').upper()
    if normalized in {
        'GENERAL PREFACE',
        'PREFATORY NOTE',
        'PREFACE',
        'PREFACE TO THE READER',
        'ORIGINAL PREFACE',
    }:
        result = normalized + ('.' if stripped.endswith('.') else '')
    else:
        result = title_case(stripped)

    if len(result) > _NAV_TITLE_MAX_CHARS:
        result = result[: _NAV_TITLE_MAX_CHARS - 1].rstrip() + '…'  # …

    return result


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


def _split_inline_structural_markers(para, allow_bare_a=False):
    """Promote inline Owen list markers to paragraph starts."""
    pieces = []
    pos = 0
    for match in INLINE_STRUCTURAL_MARKER_RE.finditer(para):
        before = para[pos:match.start()].strip()
        marker = match.group('marker')
        after_start = match.start('marker')

        if not allow_bare_a and re.match(r'^(?:\*\*)?A\.', marker, re.I):
            continue
        marker_is_wrapped = marker.startswith(('(', '[', '**(', '**['))
        if marker in {'q.', 'a.', 'm.', 'p.'} and re.match(r'\s*\d', para[match.end():]):
            continue
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
                or (para[:match.start()].count('“') > para[:match.start()].count('”'))
            )
            and not marker_is_wrapped
            and not has_list_intro_before_reference
        ):
            continue

        before_ends_structural = bool(re.search(r'[,;:—-]\s*$', before))
        before_ends_terminal = bool(re.search(r"""[.!?][""')\]]?\s*$""", before))
        before_ends_lead_word = bool(re.search(
            r'\b(?:wherefore|therefore|for|but|and|or|as)\s*$',
            before,
            re.I,
        ))
        before_ends_objection = bool(re.search(r'\b(?:Objection|Obj)\b\.?\s*$', before, re.I))
        if before_ends_objection and re.match(r'^(?:\*\*)?\d+\.(?:\*\*)?$', marker.strip()):
            continue
        if len(before) < 12 and not (before_ends_structural or before_ends_lead_word or before_ends_objection):
            continue
        marker_clean = re.sub(r'[\*\[\]\(\),;.\s]', '', marker).lower()
        marker_is_bare_decimal = bool(re.match(r'^(?:\*\*)?\d+\.(?:\*\*)?$', marker.strip()))
        marker_is_bare_roman = bool(re.match(r'^(?:\*\*)?[IVXLCDM]+\.(?:\*\*)?$', marker.strip(), re.I))
        marker_is_bare_ordinal = bool(re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b,?\s*(?:\*\*)?$', marker.strip(), re.I))
        after_preview = para[match.end():match.end() + 80].lstrip()
        after_starts_like_heading = bool(re.match(r"""[A-Z""']""", after_preview))
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

    # Skip leading digits/item markers that might be OCR artifacts (Issue 26)
    prefix_match = re.match(r'^(\d{1,3}\.?\s+)', current)
    content_start = prefix_match.end() if prefix_match else 0

    pos = content_start
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
        # If we trimmed something, drop the leading artifact prefix too
        return current[pos:].lstrip()
    return current


# ============================================================================
# FONT POOLS
# ============================================================================

def select_primary_font(body_font_name):
    """Select a primary font by name and scan its directory for associated files.

    Looks in fonts/<body_font_name>/ for .ttf and .otf files.
    Returns a dict: {'name': body_font_name, 'files': {basename: relative_path}}.
    Falls back to SBL_BLit with a printed warning if the directory is missing —
    a missing font dir is almost always a typo in body_font or a missing font folder.
    """
    # Base directory for fonts (shared.py is in project root)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(base_dir, 'fonts', body_font_name)

    if not os.path.isdir(font_dir):
        print(
            f"[WARN] Font directory not found for '{body_font_name}' "
            f"(looked in fonts/{body_font_name}/). Falling back to SBL_BLit.",
            file=sys.stderr,
        )
        body_font_name = 'SBL_BLit'
        font_dir = os.path.join(base_dir, 'fonts', body_font_name)

    files = {}
    if os.path.isdir(font_dir):
        for f in os.listdir(font_dir):
            if f.lower().endswith(('.ttf', '.otf')):
                files[f] = f"{body_font_name}/{f}"

    return {
        'name': body_font_name,
        'files': files,
    }


SBL_SUPPLEMENTS = {
    'SBL_BLit.ttf': 'SBL_BLit/SBL_BLit.ttf',
    'SBL_grk.ttf': 'SBL_BLit/SBL_grk.ttf',
    'SBL_Hbrw.ttf': 'SBL_BLit/SBL_Hbrw.ttf',
}

EZRA_SIL_FILES = {
    'SILEOT.ttf': 'EzraSIL2.51/SILEOT.ttf',
}

TITLE_PAGE_FONTS = {
    'Baskervville-Regular.ttf': 'Baskervville/static/Baskervville-Regular.ttf',
    'Baskervville-Bold.ttf': 'Baskervville/static/Baskervville-Bold.ttf',
    'Baskervville-Italic.ttf': 'Baskervville/static/Baskervville-Italic.ttf',
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

/* Title Page Majesty (Puritan / Vintage Style) */
.titlepage,
.title-page,
.treatise-title-page {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    padding: 8% 6% 8%;
    max-width: 36em;
    margin: 0 auto;
    page-break-before: always;
    -webkit-column-break-before: always;
    box-sizing: border-box;
    min-height: 90vh;
}
.titlepage .ornament,
.title-page .ornament,
.treatise-title-page .ornament {
    display: block;
    text-align: center;
    font-size: 1.2em;
    line-height: 1;
    margin: 0 auto 1.5em;
    color: #b08d2d;
    text-indent: 0;
}
.titlepage h1,
.title-page h1,
.treatise-title-page h1 {
    font-variant: small-caps;
    font-size: 2.1em;
    line-height: 1.15;
    margin: 0 0 1.2em;
    letter-spacing: 0.02em;
    font-weight: bold;
    text-align: center;
}
.titlepage h2,
.title-page h2,
.treatise-title-page h2 {
    font-weight: bold;
    font-size: 1.3em;
    line-height: 1.35;
    margin: 1.1em 0;
    letter-spacing: 0.01em;
    text-align: center;
}
.titlepage h3,
.title-page h3,
.treatise-title-page h3 {
    text-align: center;
    font-size: 1.1em;
    line-height: 1.35;
    margin: 1em 0;
    font-weight: bold;
}
.titlepage h4,
.title-page h4,
.treatise-title-page h4 {
    font-size: 0.9em;
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin: 1.2em 0;
    text-align: center;
}
.titlepage h5,
.title-page h5,
.treatise-title-page h5 {
    font-size: 0.15em; /* Extremely small as requested */
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 0.6em;
    margin: 1.5em auto;
    opacity: 0.6;
    display: flex !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100%;
    clear: both;
}
.titlepage .subtitle,
.title-page .subtitle {
    font-size: 1.15em;
    margin-top: 1.1em;
    text-align: center;
}
.titlepage .descriptive,
.title-page .descriptive,
.treatise-title-page .descriptive {
    text-align: center;
    font-style: italic;
    line-height: 1.5;
    margin: 1.8em auto 0;
    max-width: 31em;
    text-indent: 0;
    font-size: 0.95em;
}
.titlepage .author,
.titlepage .editor,
.titlepage .publisher,
.titlepage .edition-year,
.title-page .author,
.title-page .editor,
.title-page .publisher,
.title-page .edition-year {
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
.titlepage .title-meta,
.title-page .title-meta {
    margin-top: 2em;
}
.volume-title-page {
    min-height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 34em;
}
.volume-title-page .title-work-top {
    text-align: center;
    text-indent: 0;
    margin: 0 0 0.15em;
    font-size: 1.12em;
    text-transform: uppercase;
    letter-spacing: 0.14em;
}
.volume-title-page .title-author-main {
    text-align: center;
    text-indent: 0;
    margin: 0 0 0.5em;
    font-size: 2.55em;
    line-height: 1.05;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border: 0;
    padding: 0;
}
.volume-title-page .title-volume-number {
    text-align: center;
    text-indent: 0;
    margin: 1.4em 0 0.35em;
    font-size: 0.95em;
    text-transform: uppercase;
    letter-spacing: 0.18em;
}
.volume-title-page .title-volume-subtitle {
    text-align: center;
    text-indent: 0;
    margin: 0;
    font-size: 1.18em;
    font-style: italic;
}

h1 {
    text-align: center;
    font-size: 1.4em;
    font-weight: bold;
    letter-spacing: 0.03em;
    margin: 1.8em 0 0.6em;
    page-break-before: always;
    -webkit-column-break-before: always;
}

h1.primary {
    font-size: 1.35em;
    text-align: center;
    border-bottom: 1px solid #000;
    padding-bottom: 0.2em;
}

h2 {
    text-align: center;
    font-size: 1.15em;
    font-weight: bold;
    margin: 1.5em 0 0.5em;
}

h2.secondary, h3.secondary, h1.secondary {
    font-size: 1.15em;
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
    text-align: left;
    font-weight: normal;
    text-indent: 0;
    margin: 1em 0 0.65em;
    break-after: avoid;
    page-break-after: avoid;
    break-inside: avoid;
    page-break-inside: avoid;
}

.roman-list-item {
    text-align: left;
    text-indent: 0;
    margin: 0.65em 0;
}

.roman-list-item b {
    display: inline;
    margin-bottom: 0;
}

.analysis-part {
    text-align: left;
    text-indent: 0;
    margin: 1.4em 0 0.55em;
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
    margin: 2em auto 1.35em;
    font-weight: bold;
    text-transform: uppercase;
    text-indent: 0;
    max-width: 18em;
    padding-bottom: 0.45em;
    border-bottom: 1px solid #777;
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

blockquote p {
    text-indent: 0;
    margin: 0.45em 0;
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
    padding: 4% 5% 5%;
    max-width: 42em;
    margin: 0 auto;
    page-break-before: always;
    min-height: 92vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    break-inside: avoid;
    page-break-inside: avoid;
}
.treatise-title-page .greek-title {
    text-align: center;
    font-size: 1.25em;
    margin: 0 0 1.25em;
    text-indent: 0;
    font-weight: bold;
    letter-spacing: 0.08em;
}
.treatise-title-page h1,
.treatise-title-page .title-line-major {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    font-size: 2.2em;
    margin: 0.45em 0 0.35em;
    text-transform: uppercase;
    line-height: 1.15;
    font-weight: bold;
    letter-spacing: 0.12em;
    font-style: normal;
    text-align: center;
    text-indent: 0;
}
.treatise-title-page h2,
.treatise-title-page .title-line-medium {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    font-size: 1.15em;
    margin: 0.38em 0;
    line-height: 1.3;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-style: normal;
    text-align: center;
    text-indent: 0;
}
.treatise-title-page p {
    text-align: center;
    text-indent: 0;
    margin: 0.42em 0;
    line-height: 1.4;
}
.treatise-title-page .separator,
.treatise-title-page .title-connector {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    margin: 0.55em 0 0.35em;
    text-transform: uppercase;
    font-size: 0.68em;
    font-style: normal;
    font-weight: bold;
    letter-spacing: 0.18em;
}
.treatise-title-page .descriptive {
    font-style: normal;
    font-size: 0.96em;
    margin: 0.85em auto;
    max-width: 34em;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    line-height: 1.35;
}
.treatise-title-page .quote-block {
    text-align: left;
    margin: 2em 8% 0;
    font-size: 0.92em;
    line-height: 1.55;
    text-indent: 0;
    font-style: italic;
    border-top: 1px solid #777;
    padding-top: 1em;
}
.treatise-title-page .title-rule {
    width: 4em;
    height: 1px;
    background: #777;
    margin: 1.35em auto 1em;
    padding: 0;
    line-height: 1;
}
.treatise-title-page .title-source {
    text-align: center;
    text-indent: 0;
    margin: 0;
    font-size: 0.92em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: bold;
}
.v1-applied-glory-title .title-line-major {
    font-size: 2em;
}

aside[epub\:type~="footnote"] {
    display: block;
}

aside[epub\:type~="endnote"] {
    margin-bottom: 0.8em;
    padding-left: 1.8em;
    text-indent: -1.8em;
}

/* Contents page */
.contents-page {
    max-width: 42em;
    margin: 0 auto;
    padding: 4% 2%;
}
.contents-volume-title {
    text-align: center;
    text-indent: 0;
    font-size: 1.45em;
    margin: 0 0 1.4em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border: 0;
    padding: 0 0 0.5em;
    border-bottom: 1px solid #777;
}
.contents-treatise-title {
    text-align: center;
    text-indent: 0;
    font-size: 1.02em;
    line-height: 1.35;
    margin: 1.8em auto 0.45em;
    max-width: 30em;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.contents-frontmatter-line {
    text-align: center;
    text-indent: 0;
    margin: 0.4em auto 0.85em;
    font-size: 0.86em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.contents-item,
.ContentsItem {
    margin: 0.8em 0 0.2em;
    padding-left: 6.5em;
    text-indent: -6.5em;
    text-align: left;
    color: #000;
    font-size: 0.95em;
    line-height: 1.45;
}

.contents-desc-wrap,
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
    src: url("../Fonts/{primary_file}");
}}
{bold_face}
{italic_face}
{bold_italic_face}
/* SBL BibLit — universal biblical fallback */
@font-face {{
    font-family: "SBL BibLit";
    src: url("../Fonts/SBL_BLit.ttf");
}}
/* SBL Greek — polytonic Greek */
@font-face {{
    font-family: "SBL Greek";
    src: url("../Fonts/SBL_grk.ttf");
}}
/* SBL Hebrew — fully pointed Hebrew */
@font-face {{
    font-family: "SBL Hebrew";
    src: url("../Fonts/SBL_Hbrw.ttf");
}}
/* Ezra SIL — BHS-style Hebrew fallback */
@font-face {{
    font-family: "Ezra SIL";
    src: url("../Fonts/SILEOT.ttf");
}}
/* Owen Title - embedded Baskervville title display face */
@font-face {{
    font-family: "Owen Title";
    src: url("../Fonts/Baskervville-Regular.ttf");
}}
@font-face {{
    font-family: "Owen Title";
    font-weight: bold;
    src: url("../Fonts/Baskervville-Bold.ttf");
}}
@font-face {{
    font-family: "Owen Title";
    font-style: italic;
    src: url("../Fonts/Baskervville-Italic.ttf");
}}
/* Language overrides (GEMINI.md Section 4.2) */
body, div, p, span, h1, h2, h3, h4, h5, h6 {{
    font-family: "{primary_font}", "SBL BibLit", serif !important;
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
    # 1. Identify primary, bold, italic, and bold-italic files using robust heuristics
    primary_file = None
    bold_file = None
    italic_file = None
    bold_italic_file = None
    
    # Sort files to ensure deterministic results (prefer shorter names or 'Regular')
    sorted_files = sorted(primary_font_files.values(), key=lambda x: (len(x), x))
    
    for font_file in sorted_files:
        fname = os.path.basename(font_file).lower()
        
        is_bold = 'bold' in fname or '-b.' in fname or '_b.' in fname
        is_italic = 'italic' in fname or 'ital' in fname or '-i.' in fname or '_i.' in fname
        is_regular = 'regular' in fname or 'roman' in fname or '-r.' in fname or '_r.' in fname or (not is_bold and not is_italic)
        
        if is_bold and is_italic:
            if not bold_italic_file: bold_italic_file = os.path.basename(font_file)
        elif is_bold:
            if not bold_file: bold_file = os.path.basename(font_file)
        elif is_italic:
            if not italic_file: italic_file = os.path.basename(font_file)
        elif is_regular:
            if not primary_file: primary_file = os.path.basename(font_file)

    # Fallback for primary_file if no "Regular" found
    if not primary_file and primary_font_files:
        primary_file = os.path.basename(list(primary_font_files.values())[0])
    
    bold_face = ''
    if bold_file:
        bold_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    src: url("../Fonts/{bold_file}");\n}}'
    
    italic_face = ''
    if italic_file:
        italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-style: italic;\n    src: url("../Fonts/{italic_file}");\n}}'
    
    bold_italic_face = ''
    if bold_italic_file:
        bold_italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    font-style: italic;\n    src: url("../Fonts/{bold_italic_file}");\n}}'
    
    return EPUB3_FONT_STYLES.format(
        primary_font=primary_font_name,
        primary_file=primary_file,
        bold_face=bold_face,
        italic_face=italic_face,
        bold_italic_face=bold_italic_face,
    )
