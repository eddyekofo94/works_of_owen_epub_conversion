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

from cli_utils import cyan, green

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
        'body_font': 'adobe-garamond-pro-2-2',
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
            # Issue 43: PDF page-break splits "Hebrews 9:24" → "Hebrews 9" / "24"
            # which after reconstruction appears as "Hebrews 9 24".
            'Hebrews 9 24': 'Hebrews 9:24',
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
        'body_font': 'libertinus',
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
        'body_font': 'minion-pro',
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
        'body_font': 'cardo',
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
        'body_font': 'brill-font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'treatises': [
            'The Doctrine of Justification by Faith',
            "Evidences of the Faith of God's Elect"
        ]
    },
    6: {
        'title': 'The Works of John Owen, Volume 6: Temptation and Sin',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'baskerville',
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
        'body_font': 'gentium-plus-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'suppress_prefatory_note_heading': True,  # Bug #2: Apple Books shows nav title; body h2 is redundant
        'treatises': [
            'Sermon 1 — A Vision of Unchangeable, Free Mercy',
            'Sermon 2 — A Memorial of the Deliverance of Essex County, and Committee',
            'Sermon 3 — Righteous Zeal Encouraged by Divine Protection',
            'Sermon 4 — The Steadfastness of the Promises',
            'Sermon 5 — The Shaking and Translating of Heaven and Earth',
            'Sermon 6 — The Branch of the Lord the Beauty of Zion',
            'Sermon 7 — Advantage of the Kingdom of Christ',
            'Sermon 8 — The Laboring Saint\'s Dismission to Rest',
            'Sermon 9 — Christ\'s Kingdom and the Magistrate\'s Power',
            'Sermon 10 — God\'s Work in Founding Zion',
            'Sermon 11 — God\'s Presence With a People the Spring of Their Prosperity',
            'Sermon 12 — The Glory and Interest of Nations Professing the Gospel',
            'Sermon 13 — How We May Bring Our Hearts to Bear Reproofs',
            'Sermon 14 — The Testimony of the Church Is Not the Only Nor Chief Reason of Our Faith',
            'Sermon 15 — The Chamber of Imagery in the Church of Rome Laid Open',
            'Sermon 16 — An Humble Testimony Unto the Goodness and Severity of God',
        ]
    },
    9: {
        'title': 'The Works of John Owen, Volume 9: Sermons to the Church',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'cardo',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
        'suppress_prefatory_note_heading': True,  # Bug #2
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
        'body_font': 'brill-font',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'ages_pdf',
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
        'body_font': 'minion-pro',
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
        'body_font': 'arno-pro',
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
        'body_font': 'baskerville',
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
        'body_font': 'brill-font',
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
        'body_font': 'gentium-plus-2',
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
    from progress import SequentialMode, spinner_wrap_callback
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

    config = merge_volume_config(vol_num, overrides)
    body_font = config.get('body_font', 'unknown')
    internal_name = FONT_FAMILY_MAP.get(body_font, body_font)
    treatises = config.get('treatises', [])
    langs = config.get('secondary_languages')

    print(cyan(f'═══ Volume {vol_num} — config ═══'))
    print(f'  Title:      {config.get("title", "unknown")}')
    print(f'  Font:       {body_font} → "{internal_name}"')
    print(f'  Source:     {config.get("source_type", "unknown")}')
    print(f'  Treatises  ({len(treatises)}):')
    for i, t in enumerate(treatises, 1):
        print(f'    {i}. {t}')
    if langs:
        print(f'  Languages:  {", ".join(langs)}')
    print()

    # Per-volume scripts get \r progress bar when stdout is a tty
    _seq = SequentialMode()
    def _progress(current, total, label):
        _seq.update(current, total)
        if current >= total:
            _seq.done(final_message=f"\r\033[K{label} {current}/{total} ✓\n")

    if not args.render_only:
        print(cyan(f'=== Volume {vol_num}: Stage 1 — Extract ==='))
        _extract_cb, _extract_spin = spinner_wrap_callback(_progress)
        _extract_spin.message = f'Extracting Volume {vol_num}'
        _extract_spin.start()
        intermediate = extract_volume(vol_num, overrides=overrides,
                                      progress_callback=_extract_cb)
        
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
        print(cyan(f'=== Volume {vol_num}: Stage 2 — Render ==='))
        _render_cb, _render_spin = spinner_wrap_callback(_progress)
        _render_spin.message = f'Rendering Volume {vol_num}'
        _render_spin.start()
        render_volume(vol_num, overrides=overrides, progress_callback=_render_cb)

    print(green(f'=== Volume {vol_num}: Done ==='))

# ============================================================================
# NAV / TOC DISPLAY HELPERS
# ============================================================================

# Apple Books silently truncates TOC sidebar entries longer than ~100 characters.
_NAV_TITLE_MAX_CHARS = 100

def nav_display_title(title: str) -> str:
    """Truncate a nav/TOC entry to _NAV_TITLE_MAX_CHARS, appending an ellipsis if needed."""
    if not title or len(title) <= _NAV_TITLE_MAX_CHARS:
        return title
    return title[:_NAV_TITLE_MAX_CHARS - 1].rstrip() + '…'

# ============================================================================
# VOLUME METADATA — Hebrews Commentary (7 volumes)
# ============================================================================

HEBREWS_VOLUME_CONFIG = {
    1: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 1',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'adobe-garamond-pro-2-2',
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
        'body_font': 'gentium-plus-2',
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
        'body_font': 'adobe-garamond-pro-2-2',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 1:1 - 3:6']
    },
    4: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 4',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'libertinus',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 3:7 - 5:14']
    },
    5: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 5',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'minion-pro',
        'publisher': 'Eduardus Ekofius',
        'source_type': 'epub2',
        'treatises': ['Exposition of Hebrews, 6:1 - 7:28']
    },
    6: {
        'title': 'An Exposition of the Epistle to the Hebrews, Volume 6',
        'authors': ['John Owen'],
        'editors': ['William H. Goold'],
        'secondary_languages': ['el', 'he'],
        'body_font': 'baskerville',
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
    2. Strip "[" artifact immediately preceding Greek Unicode characters (legacy
       AGES rough-breathing prefix -- the PDF encodes rough breathing as "[" before
       the vowel; extraction captures the Unicode Greek glyph correctly but leaves
       "[" as a stray literal character outside the Greek span).
    3. Strip "+" and "{" immediately preceding Greek Unicode characters.
       In AGES Koine encoding "+" and "{" are rough-breathing / diacritic prefixes
       that appear as stray literals outside the Unicode span (e.g. "+\u03a9 \u0392\u03ac\u03b8\u03bf\u03c2").
       polytonic_sweep() strips them INSIDE spans; this guard catches them OUTSIDE,
       before tag_unicode_ranges() wraps them.
    4. Normalize to NFC.
    """
    if not text:
        return ""
    # 1. Strip the "j" artifact prepended to Greek characters.
    # Handle both "j\u0395" and "j \u0395" patterns found in PDF extraction.
    text = re.sub(r'\b[jJ]\s*([\u0370-\u03FF\u1F00-\u1FFF])', r'\1', text)
    # 2. Strip "[" immediately before a Greek Unicode character (Issue #17).
    # The lookahead ensures we only strip "[" directly adjacent to Greek text,
    # leaving list markers "[1.]", abbreviations "[LXX]", and space-padded
    # semantic brackets "[ eleos ]" untouched.
    text = re.sub(r'\[(?=[\u0370-\u03FF\u1F00-\u1FFF])', '', text)
    # 3. Strip "+" and "{" immediately before Greek Unicode (Issue #4).
    text = re.sub(r'[+{](?=[\u0370-\u03FF\u1F00-\u1FFF])', '', text)
    # 4. Normalize to NFC
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
    r'(?<=[a-z])f(\d{1,3})(?=[a-z])|'
    r'(?<![A-Za-z])f\s*(\d{1,3})(?=[a-z])|'
    r'(?<=[a-z])f(\d{1,3})\b|'
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
    r'\[(?:FIRST|SECONDLY|SECOND|THIRDLY|THIRD|FOURTHLY|FOURTH|FIFTHLY|FIFTH|'
    r'SIXTHLY|SIXTH|SEVENTHLY|SEVENTH|EIGHTHLY|EIGHTH|NINTHLY|NINTH|LASTLY|LAST)\][,.;]?\s+|'
    r'(?!\*{0,2}(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\*{0,2}[.\s])[IVXLCDM]+\.\s+|'  # I. / II. (not LXX/MT/OT/NT etc.)
    r'(?:Q\.|Ques\.|Ans\.|A\.\s*\d+\.)\s+|'                       # Q. / Ques. / Ans. / A. 1.
    r'(?:Obj(?:ection)?\.?\s*\d*\.?|Ans(?:wer)?\.?\s*\d*\.?|Sol(?:ution)?\.?\s*\d*\.?|Use\.?\s*\d+\.?)\s+|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]\s+|'  # 1st, 2nd, 3rd, 4th,
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?\s+|'  # 2ndly, 3rdly
    r'(?:First|Firstly|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Seventhly|Eighthly|Ninthly|Lastly|Again|But)\b[,.]?\s+'
    r')'
)
INLINE_STRUCTURAL_MARKER_RE = re.compile(
    r'(?<!^)(?P<lead>\s+)'
    r'(?P<marker>'
    r'\((?!\d{4}\))\d+\.?\)|'
    r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
    r'\[\d+\.?\]|'
    r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
    r'\[(?:FIRST|SECONDLY|SECOND|THIRDLY|THIRD|FOURTHLY|FOURTH|FIFTHLY|FIFTH|'
    r'SIXTHLY|SIXTH|SEVENTHLY|SEVENTH|EIGHTHLY|EIGHTH|NINTHLY|NINTH|LASTLY|LAST)\][,.;]?|'
    r'\*\*\d+\.\*\*|'
    r'\*\*\((?!\d{4}\))\d+\.?\)\*\*|'
    r'\*\*\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\*\*|'
    r'\*\*\[\d+\.?\]\.?\*\*|'
    r'\*\*\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\.?\*\*|'
    r'\*\*\[(?:FIRST|SECONDLY|SECOND|THIRDLY|THIRD|FOURTHLY|FOURTH|FIFTHLY|FIFTH|'
    r'SIXTHLY|SIXTH|SEVENTHLY|SEVENTH|EIGHTHLY|EIGHTH|NINTHLY|NINTH|LASTLY|LAST)\][,.;]?\*\*|'
    r'\*\*\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)\*\*\s*[,.;]?|'
    r'\*\*(?!(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\.)[IVXLCDM]+\.\*\*|'
    r'(?!(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\.)[IVXLCDM]+\.|'
    r'(?<![:\d-])(?!\d{4}\.)\d+\.|'
    r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
    r'(?:Obj(?:ection)?\.?|Ans(?:wer)?\.?|Sol(?:ution)?\.?|Use\.?)\s*(?:\d+\.)?|'
    r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
    r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
    r')(?P<trail>\s+)'
)
# ROMAN_HEADING_RE / ROMAN_ONLY_RE: Only match if the following text is short or
# All-Caps (Issue 21).  Negative lookahead excludes well-known scholarly/biblical
# abbreviations that happen to be composed entirely of Roman-numeral letters:
#   LXX  — Septuagint (L=50, X=10, X=10 → looks like Roman 70)
#   MT   — Masoretic Text
#   OT / NT — Old/New Testament
#   DV   — Douay-Vulgate
#   KJV / AV / NIV / ESV / NRSV — Bible translations
# The lookahead is case-insensitive and matches with or without surrounding ** bold markers.
_ROMAN_EXCLUSION_LOOKAHEAD = (
    r'(?!\*{0,2}(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\*{0,2}[.\s])'
)
ROMAN_HEADING_RE = re.compile(
    _ROMAN_EXCLUSION_LOOKAHEAD
    + r'(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?\s+'
    r'(?P<rest>[^a-z]{1,150}|[A-Z][a-z ]{1,45}|[A-Z][a-z ]{1,45}\.)$',
    re.I,
)
ROMAN_ONLY_RE = re.compile(
    _ROMAN_EXCLUSION_LOOKAHEAD
    + r'(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$',
    re.I,
)
PLAIN_CHAPTER_RE = re.compile(r'^(CHAPTER\s+\d+\.?)(?:\s+(.+))?$')
CITATION_ABBREV_TRAIL_RE = re.compile(
    r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
    r'enchirid|distinct|q|a|p|pp|page|pages|sec|ad|m|aen|liv|hist)\.?\s*$'
    r'|'
    r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kings|Chron|Ezra|Neh|Esth|Job|Ps|Prov|Eccl|Cant|'
    r'Sol|Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|'
    r'Matt|Mk|Lk|Jn|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Pet|Jude|Rev)\.\s*$'
    r'|'
    # Patristic author abbreviations
    r'\b(?:Aug|August|Austin|Chrys|Chrysost|Hierom|Jerome|Clem|Clement|Tertull|Orig|Origen|Cyp|Cyprian|'
    r'Euseb|Athan|Athanas|Basil|Naz|Nazianz|Nyss|Ambr|Ambrose|Theod|Theodoret|Cyril|Hilar|Hilary|Leo|Bern|'
    r'Bernard|Bell|Bellar|Soc|Socin|Faust|Faustus|Calv|Calvin|Epiph|Epiphan|Greg|Gregory|Plut|Cic|Sen|Tac|'
    r'Plin|Arist|Plat|Justin|Iren|Alex|Alexand|Mart)\.\s*$'
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
    r'\b(?:Aen|Liv|Hist)\.?,?(?:\s+Hist\.?)?(?:\s+[ivxlcdm]+|\s+\d+)?\.\s*$',
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
    # Failed AGES verse-code translation can leave opaque source ids such as
    # [4611605]16:5-15 or [19B9105]Psalm 119:105.  These are not editorial
    # brackets, dates, footnotes, or section labels; remove only long alphanumeric
    # codes with at least one digit when they directly prefix a scripture locator.
    ages_code = r'\[(?=[0-9A-Z]{6,8}\])(?=[0-9A-Z]*\d)[0-9A-Z]{6,8}\]'
    text = re.sub(
        rf'{ages_code}(?=\s*(?:(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b|\d{{1,3}}(?::|-|,)))',
        '',
        text,
        flags=re.I,
    )
    # v11 has double-bracket variants: [[4313101]] — strip those too
    text = re.sub(
        rf'\[{ages_code}\](?=\s*(?:(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b|\d{{1,3}}(?::|-|,)))',
        '',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\*\*\[(\d{1,3})\*\*\s+_?\*\*(st|nd|rd|th|dly|ly)\.?\*\*_?\s+\*\*\.?\]\*\*',
        lambda m: f'**[{m.group(1)}{m.group(2).lower()}.]**',
        text,
        flags=re.I,
    )
    # OCR sometimes separates ordinal/list suffixes into "1 st ." or "2 dly .".
    # When the PDF uses italic for the suffix the extraction produces markdown like
    # "**1** _**st**_ ." or "**2** _**dly**_ ." — normalise to "**1st.**" etc.
    text = re.sub(
        r'\*\*(\d{1,3})\*\*\s+_\*\*(st|nd|rd|th|dly|ndly|rdly|thly|ly)\*\*_\s*([.,;]?)',
        lambda m: f'**{m.group(1)}{m.group(2).lower()}{m.group(3) or "."}**',
        text,
        flags=re.I,
    )
    # Also handle variant without inner bold: "**1** _st_ ."
    text = re.sub(
        r'\*\*(\d{1,3})\*\*\s+_(st|nd|rd|th|dly|ndly|rdly|thly|ly)_\s*([.,;]?)',
        lambda m: f'**{m.group(1)}{m.group(2).lower()}{m.group(3) or "."}**',
        text,
        flags=re.I,
    )
    # OCR sometimes separates ordinal/list suffixes into "1 st ." or "2 dly .".
    # Normalize before marker splitting so the usual structural formatters see it.
    text = re.sub(
        r'\b(\d{1,3})\s+(st|nd|rd|th|dly|ly)\s*([.,;])',
        lambda m: f'{m.group(1)}{m.group(2).lower()}{m.group(3)}',
        text,
        flags=re.I,
    )
    # Issue 30: OCR sometimes produces a double period after an ordinal — "1st.."
    # or "2dly.." — because the ordinal already carries a period and a sentence
    # boundary adds another.  Collapse to a single period.
    text = re.sub(
        r'\b(\d{1,3}(?:st|nd|rd|th|dly|ndly|rdly|thly|ly))\.\.',
        r'\1.',
        text,
        flags=re.I,
    )
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


LATIN_OCR_CORRECTIONS = {
    'sod': 'sed',
    'Cicerco': 'Cicero',
    'sub ape': 'sub spe',
    'credere ilium': 'credere illum',
    'putaut': 'putant',
    'efiiciens': 'efficiens',
    'queastum facere solitua': 'quaestum facere solitus',
    'prerumque': 'plerumque',
    'graneis': 'ganeis',
    'nulla pietatis commendatione, nulla': 'nulla pietatis commendatione, nullo',
    'delictorum nostrorum remain': 'delictorum nostrorum veniam',
    'Virgln': 'Virgin',
    'Virglnique': 'Virginique',
    'Francisei': 'Francisci',
    'Fragm, de Jus. tificat.': 'Fragm. de Justificat.',
    'Pater quam inepte': 'Patet quam inepte',
    'pater denique quam': 'patet denique quam',
    'adversari. orum': 'adversariorum',
    'Clarke': 'Clarae',
    'Voss. Rasp': 'Voss. Resp',
}


def _repair_owen_ocr_errors(text: str, config: dict = None) -> str:
    """Repair known OCR character misreads using volume-specific configuration."""
    # Apply centralized Latin OCR corrections
    for wrong, right in LATIN_OCR_CORRECTIONS.items():
        pattern = re.escape(wrong)
        if wrong and wrong[0].isalnum():
            pattern = r'\b' + pattern
        if wrong and wrong[-1].isalnum():
            pattern = pattern + r'\b'
        text = re.sub(pattern, right, text)

    text = _normalize_scholarly_citation_artifacts(text)
    text = _unwrap_quote_wrapped_structural_markers(text)
    text = _repair_scripture_reference_artifacts(text)
    text = re.sub(r'\b([A-Za-z]{2,})]y\b', r'\1ly', text)
    text = re.sub(r'\b([A-Za-z]{2,})]e\b', r'\1le', text)
    text = re.sub(r'(?<!\w)](?=earn|earning|earned|earnt|edge)', 'l', text, flags=re.I)
    text = re.sub(r'\bI\s+a\s+will\b', 'I will', text)
    text = re.sub(r'\b(Objection|Ans|Q)\s+\.', r'\1.', text)
    # Issue 29a: Remove stray underscore characters that are not part of
    # markdown emphasis (i.e. not _word_ or __word__).  Isolated underscores
    # or underscores adjacent to spaces are OCR artifacts in the Owen corpus.
    # Stray isolated underscore: surrounded by whitespace or start/end of string.
    # Only these are OCR artifacts; underscores adjacent to word characters may
    # be markdown emphasis (_word_) or intra-word separators — leave those alone.
    text = re.sub(r'(?:^|(?<=\s))_(?=\s|$)', '', text)
    text = re.sub(r'(?<=\S)\s+(?:-|--|–)\s+(?=\S)', ' — ', text)
    # Strip spurious period from the indefinite article 'A' when followed by
    # a lowercase word.  The original fix anchored to line-start (^) but the
    # artifact also appears mid-paragraph after sentence-ending punctuation
    # ("...gave them. A. church state does...") and after leading whitespace.
    # Using \b (word boundary) catches all positions safely.
    #
    # Example: "A. brief view of the faith" → "A brief view of the faith"
    #          "the Lord gave them. A. church state..." → "...A church state..."
    #
    # Safe because every real structural label (A. FIRST, A. GATHERED, catechism
    # A. The...) is always followed by a capital letter or digit — never lowercase.
    text = re.sub(r'\bA\. (?=[a-z])', 'A ', text)

    # Insert missing space before fused list markers: "and(2.)" → "and (2.)"
    # OCR often fuses a conjunction or word directly with the opening parenthesis
    # of a numbered sub-point.  Only fires when a word character immediately
    # precedes '(' — already-spaced markers are unaffected.
    text = re.sub(r'(\w)\((\d+\.)\)', r'\1 (\2)', text)

    # Issue 42: OCR misreads the interjection letter 'O' as digit '0'.
    # "0 sweet permutation!" → "O sweet permutation!"
    # "0 Lord, how great thou art!" → "O Lord, how great thou art!"
    # Two positions are safe to fix:
    #   (a) at the very start of a line (paragraph-opening interjection)
    #   (b) immediately after sentence-terminal punctuation + space
    # Both require a letter to follow — preserving numeric "0 units" etc.
    text = re.sub(r'(?m)^0 (?=[A-Za-z])', 'O ', text)
    text = re.sub(r'(?<=[.!?] )0 (?=[A-Za-z])', 'O ', text)

    # Repair Volume 1 Chapter 15 scripture reference split OCR error ("verse, 7. He has," -> "verse 7. He has,")
    text = re.sub(
        r'\bverse\s*,\s*7\.\s+He\s+has\s*,',
        r'verse 7. He has,',
        text,
        flags=re.I
    )

    # Simon Magus case-insensitive OCR repair and casing normalization
    def _fix_simon_magus(m):
        orig = m.group(0)
        if orig.islower():
            return "simon magus"
        else:
            return "Simon Magus"
    # Matches "Simon M Agus", "Simon M. Agus", "Simon M'Agus", "Simon M’Agus" etc.
    text = re.sub(r"\bSimon\s+M(?:['’]|\.?\s+)?Agus\b", _fix_simon_magus, text, flags=re.I)
    # Also normalize any all-caps "SIMON MAGUS" (which is usually an OCR/small-caps artifact)
    text = re.sub(r"\bSIMON\s+MAGUS\b", "Simon Magus", text)

    # Clean stray double quotes preceding a scripture reference (e.g. '," " John' -> '," John')
    text = re.sub(
        rf'([”"“]\s*,?\s*)[”"“]\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)',
        r'\1',
        text,
        flags=re.I
    )

    # Repair Volume 1 Meditations Chapter 1 missing list marker '4.' OCR error
    text = text.replace(
        "\n\nConsider therefore, his infinite condescension",
        "\n\n4. Consider therefore, his infinite condescension"
    )

    # Issue 44: A trailing lone hyphen at end of a line or sentence fragment
    # is an OCR artifact for an em-dash that was at line's end in the source.
    # "For, -" → "For, —"  (comma + space + hyphen → comma + em-dash)
    # Also handles: word-space-hyphen at end of line (no comma).
    text = re.sub(r'(?m),\s*-\s*$', ', —', text)
    text = re.sub(r'(?m)(?<=\w) -\s*$', ' —', text)
    # Issue 44b: "For, - before the saints" — hyphen mid-sentence with a space
    # after it.  ", -\s+letter" is always an OCR em-dash in Owen's usage.
    # The end-of-line rules above cannot catch this variant.
    text = re.sub(r',\s*-\s+(?=[A-Za-z])', ', — ', text)

    # Issue 47a: Colon/punctuation (not word-char) + space + lone hyphen at EOL.
    # “directions: -” → “directions: —“
    # The existing Issue 44 rule uses (?<=\w) which misses ‘:’ (not \w).
    text = re.sub(r'(?m)(?<=[!?:;]) -\s*$', ' —', text)
    # Issue 47b: Paragraph opening with a lone hyphen before a quotation mark.
    # ‘- “We could not...’ → ‘— “We could not...’
    # OCR often renders an opening em-dash as a bare hyphen when it starts a line.
    # Matches straight double-quote, curly open/close double-quotes (U+201C/201D).
    text = re.sub(r'(?m)^-\s+(?=["“”])', '— ', text)

    # Issue 48.a: Fused Roman-numeral list items — OCR omits paragraph breaks.
    # “I. Honor.II. Obedience.III. Conformity.” →
    # “I. Honor.\n\nII. Obedience.\n\nIII. Conformity.”
    # Safe trigger: period preceded by lowercase letter AND followed DIRECTLY
    # (no space) by a Roman-numeral token + period + space/tab.  The no-space
    # requirement means lib. IV. (space before IV) never fires.
    text = re.sub(r'(?<=[a-z])\.(?=[IVX]+\.[  \t])', '.\n\n', text)

    # Sermon volumes sometimes split bracketed ordinal markers across markdown
    # emphasis runs: "**[** _**3dly**_ **.]**". Normalize before rendering so
    # the marker is counted and styled like ordinary "[3dly.]".
    text = re.sub(
        r'\*\*\[\*\*\s*_?\*\*(\d+(?:st|nd|rd|th|dly|ly))\*\*_?\s*\*\*\.\]\*\*',
        r'**[\1.]**',
        text,
        flags=re.I,
    )

    # Issue 21: Spurious backslash OCR artifact before word-start.
    # OCR occasionally renders a character defect as a backslash at the boundary
    # between paragraphs or inline: "\which" → "which", "\the" → "the".
    # Only strip when the backslash is NOT preceded by a word character (i.e. it
    # is a lone artifact, not part of a recognised escape) AND is followed by a
    # lowercase letter (uppercase would indicate a new sentence after a genuine
    # punctuation mark, which we leave alone).
    text = re.sub(r'(?<!\w)\\(?=[a-z])', '', text)

    # Bare ALL-CAPS ordinal adverbs at paragraph/line start are OCR artefacts
    # for bold or italic rendering of structural section markers in the original
    # print.  Normalize to title-case so STRUCTURAL_PREFIX_HTML_RE bolds them
    # and STRUCTURAL_START_RE assigns class="list-item" in render.py.
    #
    # Covers comma- and period-terminated forms across all volumes:
    #   "SECONDLY, There is in this death…"  →  "Secondly, There is…"
    #   "SEVENTHLY. He is the head…"         →  "Seventhly. He is…"
    #
    # Anchored to line/paragraph start (^, MULTILINE) — never fires mid-sentence.
    # FIRST(?:LY)? handles the "FIRST," form (Owen's preferred bare ordinal for
    # the first item); FIRSTLY is included for completeness.
    text = re.sub(
        r'^(FIRST(?:LY)?|SECONDLY|THIRDLY|FOURTHLY|FIFTHLY|SIXTHLY|'
        r'SEVENTHLY|EIGHTHLY|NINTHLY|LASTLY)([,.])',
        lambda m: m.group(1).capitalize() + m.group(2),
        text,
        flags=re.MULTILINE,
    )

    # OCR misreads "thy" as "try" in archaic/biblical phrases.
    # "thy" and "try" differ only in glyph form for 'h'/'r'; both are real words,
    # so we only fix in high-confidence biblical phrases attested across Owen's corpus.
    text = re.sub(r'\bin whose hand try (breath|soul|life|spirit)\b',
                  lambda m: f'in whose hand thy {m.group(1)}', text, flags=re.I)
    text = re.sub(r'\bwhose are all try (ways|works|deeds|paths)\b',
                  lambda m: f'whose are all thy {m.group(1)}', text, flags=re.I)

    # Stray bold-opener OCR artifact: ", ** Word" — the PDF extractor occasionally
    # emits a dangling "**" (Markdown bold-open with no closing marker) before a
    # capitalised word following a comma or semicolon.  The "**" + surrounding space
    # is invisible to the reader but leaves a stray token in the Markdown source
    # that the renderer strips as a malformed bold marker, producing a double space.
    # Strip the "** " to leave a clean single space after the punctuation.
    # Example: "enemies, ** Luke 1:74;" → "enemies, Luke 1:74;"
    text = re.sub(r'([,;])\s+\*\*\s+(?=[A-Z])', r'\1 ', text)

    # OCR month abbreviation: "APRI" → "APRIL" (missing final letter in dates).
    # Example: "COGGESHALL, APRI 25, 1648." — the trailing 'L' was not captured.
    # Anchored to a day-number to avoid false positives.
    text = re.sub(r'\bAPRI\b(?=\s+\d{1,2}[,.])', 'APRIL', text)

    # Clean up spacing inside brackets for single word/digit tokens (e.g. [ a] or [ a ] -> [a])
    text = re.sub(r'\[\s*([^\s\]]+)\s*\]', r'[\1]', text)

    if not config:
        return text

    corrections = config.get('text_replacements', {})
    regex_corrections = config.get('regex_replacements', {})

    result = text
    for wrong, right in corrections.items():
        if wrong.startswith('(') or wrong.endswith('\\b'):
            result = re.sub(wrong, right, result)
        else:
            # Only apply \b if the boundary characters are word characters
            pattern = re.escape(wrong)
            if wrong and wrong[0].isalnum():
                pattern = r'\b' + pattern
            if wrong and wrong[-1].isalnum():
                pattern = pattern + r'\b'
            result = re.sub(pattern, right, result)

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
    # 3-Level Indentation Cap: If the paragraph itself starts with a Level 3 marker (an ordinal),
    # any deeper sub-points represent Level 4+ and should remain flat/inline inside this paragraph.
    clean_start = re.sub(r'<[^>]+>', '', para).strip().upper()
    is_level_3_start = (
        re.match(r'^\(?(?:\d+(?:ST|ND|RD|TH|DLY|LY))\b', clean_start)
        or re.match(r'^\[(?:FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH|SEVENTH|EIGHTH|NINTH|LAST|LY)\]', clean_start)
        or re.match(r'^\d+(?:ST|ND|RD|TH|DLY|LY)\b', clean_start)
    )
    if is_level_3_start:
        return [para]

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
        # Unbalanced square brackets before this marker mean we're inside a
        # citation like “[Juv., 6. 546.]” — don't split there.
        _before_content = re.sub(r'\[\[[A-Z_]+\]\]\s*', '', para[:match.start()])
        _inside_bracket = _before_content.count('[') > _before_content.count(']')

        if (
            (
                SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
                or CITATION_ABBREV_TRAIL_RE.search(before[-80:])
                or re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
                or re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
                or (para[:match.start()].count('”') % 2 != 0)
                or (para[:match.start()].count('”') > para[:match.start()].count('”'))
                or _inside_bracket
            )
            and not marker_is_wrapped
            and not has_list_intro_before_reference
        ):
            continue

        # Mid-sentence dangling connectors, commas, or hyphens must NEVER cause a split
        before_tail_clean = re.sub(r'[*_”"\'’\s]+$', '', before)
        is_preceded_by_dangling = (
            bool(re.search(
                r'(?i)\b(?:and|the|of|for|with|in|to|a|is|was|were|be|been|being|has|have|had|by|from|as|at|or|which|who|whom|this|that|these|those)\b\s*$',
                before_tail_clean
            ))
            or bool(re.search(r',(?!\s*”)\s*$', before_tail_clean))
            or bool(re.search(r'-\s*$', before_tail_clean))
        )
        if is_preceded_by_dangling:
            continue

        before_tail = re.sub(r'[*_]+$', '', before).rstrip()
        # Flat lists (ordinals) preceded by a comma, semicolon, or connector word must remain inline.
        is_ordinal_marker = bool(re.search(
            r'(?i)\b(?:1st|2nd(?:ly)?|2dly|3rd(?:ly)?|3dly|4th(?:ly)?|first|secondly|thirdly|fourthly|lastly|firstly)\b',
            marker
        ))
        if is_ordinal_marker:
            is_preceded_by_connector = bool(re.search(
                r'(?i)(?:'
                r'[,;]\s*|'
                r'\b(?:and|or|but|as|to|into|unto|of|in|by|with|that|which|is|are|were|was|be|been)\b\s*'
                r')[”"\'’]*\s*$',
                before_tail
            ))
            if is_preceded_by_connector:
                continue

        before_ends_structural = bool(re.search(r'[,;:—-]\s*$', before_tail))
        before_ends_terminal = bool(re.search(r"""[.!?][""')\]]?\s*$""", before_tail))
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
        # Scholastic citation tail: "22. q. 174, a. 1" — the "22." is not a list
        # item; "q. 174" is a Thomistic question reference.  Skip split when the
        # text after the marker begins with a known citation abbreviation.
        _after_is_citation_tail = bool(re.match(
            r'^(?:q|a|p|pp|vol|sec|lib|cap|chap|serm|art|dist|part|num)\.\s*\d',
            after_preview,
            re.I,
        ))
        if _after_is_citation_tail:
            continue
        # Author-initial context: if the text immediately before this marker
        # ends with a bare single-letter initial (e.g. "R."), the current
        # single-letter marker is also an author initial, NOT a list marker.
        # Prevents "R. D. Kimchi" from splitting at "D.", "V. C." at "V.", etc.
        _before_ends_bare_initial = bool(re.search(r'(?<!\S)[A-Z]\.\s*$', before_tail))
        if _before_ends_bare_initial and re.match(r'^[IVXLCDM]\.$', marker, re.I):
            continue
        strong_source_like_marker = (
            (marker_is_bare_decimal or marker_is_bare_roman or marker_is_bare_ordinal)
            and len(before) >= 35
            and after_starts_like_heading
            and not SCRIPTURE_CONTINUATION_TRAIL_RE.search(before[-120:])
            and not CITATION_ABBREV_TRAIL_RE.search(before[-80:])
            and not re.search(r'\b(?:verse|verses|chap|chapter|page|pages)[.,]?\s*$', before, re.I)
            and not re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', before, re.I)
            and not re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', before, re.I)
            and marker_clean not in {'i', 'v', 'x', 'l', 'c', 'd', 'm'}
        )
        if not (re.search(r'[.,;:—-]\s*$', before_tail) or before_ends_terminal or before_ends_lead_word or before_ends_objection):
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

# ============================================================================
# FONT FAMILY NAME MAPPING
# Maps directory names to the actual internal font-family names embedded in
# the .ttf/.otf files. Apple Books/WebKit requires these to match for proper
# font rendering.
# ============================================================================

FONT_FAMILY_MAP = {
    # Body fonts (available for per-volume selection)
    'adobe-garamond-pro-2-2': 'Adobe Garamond Pro',
    'arno-pro':               'Arno Pro',
    'baskerville':            'Baskervville',
    'brill-font':             'Brill',
    'cardo':                  'Cardo',
    'gentium-plus-2':         'Gentium Plus',
    'libertinus':             'Libertinus Serif',
    'minion-pro':             'Minion Pro',
    'sabon-next-lt':          'Sabon Next LT',
    'cormorant-garamond':     'Cormorant Garamond',
    'im-fell-english':        'IM Fell English',
    'libre-caslon-text':      'Libre Caslon Text',
    'playfair-display':       'Playfair Display',
    # Heading-only fonts
    'proxima-nova':           'Proxima Nova',
    # Supplemental (not for body selection)
    'sbl-blit':               'SBL BibLit',
    'stix-two-text':          'STIX Two Text',
    'ezra-sil-2-51':          'Ezra SIL',
    'gfs-porson':             'GFS Porson',
}

# Fonts excluded from body-font selection (used only for specific purposes)
BODY_FONT_EXCLUDES = {'stix-two-text', 'ezra-sil-2-51', 'proxima-nova', 'gfs-porson'}


def _decode_font_name(raw, platform_id):
    """Decode an OpenType name table string without requiring fontTools."""
    encodings = ('utf-16-be', 'mac_roman') if platform_id == 3 else ('mac_roman', 'utf-16-be')
    for encoding in encodings:
        try:
            text = raw.decode(encoding).strip('\x00').strip()
            if text:
                return text
        except Exception:
            continue
    return ''


def _read_sfnt_name_records(font_path):
    """Read useful OpenType/TrueType name records with only the stdlib.

    Apple Books/WebKit is much happier when CSS uses the font's preferred
    family name (nameID 16) or, when absent, the legacy family name (nameID 1).
    This parser keeps OTF/TTF metadata checks working even when fontTools is
    not installed in the active virtualenv.
    """
    import struct

    records = {}
    try:
        with open(font_path, 'rb') as fh:
            data = fh.read()
        if len(data) < 12:
            return records
        num_tables = struct.unpack('>H', data[4:6])[0]
        name_offset = None
        name_length = None
        for idx in range(num_tables):
            off = 12 + idx * 16
            if off + 16 > len(data):
                break
            tag = data[off:off + 4]
            table_offset, table_length = struct.unpack('>II', data[off + 8:off + 16])
            if tag == b'name':
                name_offset = table_offset
                name_length = table_length
                break
        if name_offset is None or name_offset + 6 > len(data):
            return records

        table = data[name_offset:name_offset + name_length]
        _fmt, count, string_offset = struct.unpack('>HHH', table[:6])
        wanted = {
            1: 'family',
            2: 'subfamily',
            4: 'full_name',
            6: 'postscript',
            16: 'preferred_family',
            17: 'preferred_subfamily',
        }
        for idx in range(count):
            off = 6 + idx * 12
            if off + 12 > len(table):
                break
            platform_id, _encoding_id, language_id, name_id, length, offset = struct.unpack(
                '>HHHHHH', table[off:off + 12]
            )
            if name_id not in wanted:
                continue
            start = string_offset + offset
            end = start + length
            if end > len(table):
                continue
            key = wanted[name_id]
            decoded = _decode_font_name(table[start:end], platform_id)
            if decoded and (key not in records or (platform_id == 3 and language_id in (0x0409, 0))):
                records[key] = decoded
        return records
    except Exception:
        return records


def _get_font_name_records(font_path):
    """Return key OpenType name records for a .ttf/.otf file."""
    try:
        from fontTools.ttLib import TTFont
        font = TTFont(font_path)
        wanted = {
            1: 'family',
            2: 'subfamily',
            4: 'full_name',
            6: 'postscript',
            16: 'preferred_family',
            17: 'preferred_subfamily',
        }
        records = {}
        for record in font['name'].names:
            key = wanted.get(record.nameID)
            if key and key not in records:
                value = record.toUnicode().strip()
                if value:
                    records[key] = value
        if records:
            return records
    except Exception:
        pass
    return _read_sfnt_name_records(font_path)


def _get_internal_family_name(font_path):
    """Read the preferred internal font-family name from a .ttf/.otf file."""
    records = _get_font_name_records(font_path)
    return records.get('preferred_family') or records.get('family')


def _font_style_key(filename, records=None):
    """Return the canonical CSS slot for a standard family member."""
    records = records or {}
    text = ' '.join([
        filename,
        records.get('subfamily', ''),
        records.get('preferred_subfamily', ''),
        records.get('full_name', ''),
    ]).lower()
    is_bold = any(token in text for token in ('bold', '-bd', '_bd'))
    is_italic = any(token in text for token in ('italic', 'ital', '-it', '_it'))
    if is_bold and is_italic:
        return 'bold_italic'
    if is_bold:
        return 'bold'
    if is_italic:
        return 'italic'
    return 'regular'


def _is_standard_body_face(filename, records, primary_family):
    """Reject auxiliary display/width/weight faces in mixed font folders."""
    style_text = ' '.join([
        filename,
        records.get('family', ''),
        records.get('preferred_family', ''),
        records.get('subfamily', ''),
        records.get('preferred_subfamily', ''),
        records.get('full_name', ''),
    ]).lower()
    banned = (
        'cond', 'condensed', 'narrow', 'display', 'initial', 'keyboard', 'math',
        'mono', 'semibold', 'semi bold', 'smbd', 'medium', 'light', 'extra',
        'black', 'thin',
    )
    if 'sans' in style_text and 'sans' not in primary_family.lower():
        return False
    return not any(token in style_text for token in banned)


def _font_sort_key(path):
    n = os.path.basename(path).lower()
    stem = os.path.splitext(n)[0]
    is_regular = (
        'regular' in n or 'roman' in n or stem.endswith('-r') or stem.endswith('_r')
        or stem.endswith('regular')
    )
    return (0 if is_regular else 1, len(n), n)


def _font_belongs_to_family(records, primary_family):
    family_values = {
        records.get('preferred_family', ''),
        records.get('family', ''),
    }
    full_name = records.get('full_name', '')
    return primary_family in family_values or bool(full_name and full_name.startswith(primary_family))


def _filter_font_files(files, primary_family):
    """Filter font files to only include those belonging to the primary family.

    Some font directories (Libertinus, Minion_pro) contain multiple font
    families. This ensures only the relevant variants are included.
    """
    by_style = {}
    fallback = {}
    for fname, rel_path in files.items():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, 'fonts', rel_path)
        if os.path.exists(full_path):
            records = _get_font_name_records(full_path)
            if _font_belongs_to_family(records, primary_family):
                fallback[fname] = rel_path
                if _is_standard_body_face(fname, records, primary_family):
                    by_style.setdefault(_font_style_key(fname, records), (fname, rel_path))
    if by_style:
        ordered = {}
        for key in ('regular', 'bold', 'italic', 'bold_italic'):
            if key in by_style:
                fname, rel_path = by_style[key]
                ordered[fname] = rel_path
        return ordered
    return fallback if fallback else files  # fallback: keep all if no metadata match


def select_primary_font(body_font_name):
    """Select a primary font by name and scan its directory for associated files.

    Looks in fonts/<body_font_name>/ for .ttf and .otf files.
    Returns a dict: {'name': internal_font_family, 'files': {basename: relative_path}}.
    Falls back to SBL_BLit with a printed warning if the directory is missing —
    a missing font dir is almost always a typo in body_font or a missing font folder.
    """
    # Base directory for fonts (shared.py is in project root)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_dir = os.path.join(base_dir, 'fonts', body_font_name)

    if not os.path.isdir(font_dir):
        print(
            f"[WARN] Font directory not found for '{body_font_name}' "
            f"(looked in fonts/{body_font_name}/). Falling back to sbl-blit.",
            file=sys.stderr,
        )
        body_font_name = 'sbl-blit'
        font_dir = os.path.join(base_dir, 'fonts', body_font_name)

    files = {}
    internal_name = FONT_FAMILY_MAP.get(body_font_name, body_font_name)
    if os.path.isdir(font_dir):
        for f in sorted(os.listdir(font_dir), key=_font_sort_key):
            if f.lower().endswith(('.ttf', '.otf')):
                files[f] = f"{body_font_name}/{f}"

        # Determine internal font family name from the first readable face.
        if files:
            detected = None
            for rel_path in files.values():
                full_path = os.path.join(base_dir, 'fonts', rel_path)
                detected = _get_internal_family_name(full_path)
                if detected:
                    break
            internal_name = FONT_FAMILY_MAP.get(body_font_name, detected or internal_name)
            files = _filter_font_files(files, internal_name)

    return {
        'name': internal_name,
        'files': files,
    }


SBL_SUPPLEMENTS = {
    'SBL_BLit.ttf': 'sbl-blit/SBL_BLit.ttf',
    'SBL_grk.ttf': 'sbl-blit/SBL_grk.ttf',
    'SBL_Hbrw.ttf': 'sbl-blit/SBL_Hbrw.ttf',
}

EZRA_SIL_FILES = {
    'SILEOT.ttf': 'ezra-sil-2-51/SILEOT.ttf',
}

TITLE_PAGE_FONTS = {
    'BaskervilleBT.ttf': 'baskerville/BaskervilleBT.ttf',
    'BaskervilleItalicBT.ttf': 'baskerville/BaskervilleItalicBT.ttf',
}

PROXIMA_NOVA_FILES = {
    'Proxima Nova Regular.ttf': 'proxima-nova/Proxima Nova Regular.ttf',
    'Proxima Nova Extrabold.ttf': 'proxima-nova/Proxima Nova Extrabold.ttf',
    'Proxima Nova Light.ttf': 'proxima-nova/Proxima Nova Light.ttf',
    'Proxima Nova Semibold.ttf': 'proxima-nova/Proxima Nova Semibold.ttf',
}

GFS_PORSON_FILES = {
    'GFSPorson.ttf': 'gfs-porson/GFSPorson.ttf',
}

CARDO_FILES = {
    'Cardo-Regular.ttf': 'cardo/Cardo-Regular.ttf',
    'Cardo-Italic.ttf': 'cardo/Cardo-Italic.ttf',
    'Cardo-Bold.ttf': 'cardo/Cardo-Bold.ttf',
}

GENTIUM_PLUS_FILES = {
    'GentiumPlus-R.ttf': 'gentium-plus-2/GentiumPlus-R.ttf',
    'GentiumPlus-I.ttf': 'gentium-plus-2/GentiumPlus-I.ttf',
}

# Distinctly Latin words for tagging
LATIN_DICTIONARY = {
    'et', 'est', 'non', 'ut', 'ad', 'cum', 'qui', 'quae', 'quod', 'quibus', 'sub', 'pro', 'per', 
    'ab', 'ex', 'sine', 'de', 'sunt', 'esse', 'fuit', 'deus', 'dominus', 'christus', 'jesu', 
    'patris', 'filii', 'spiritus', 'sancti', 'gratia', 'fide', 'scriptura', 'ecclesia', 'vero', 
    'enim', 'autem', 'etiam', 'nam', 'quia', 'sicut', 'ita', 'tamen', 'sed', 'nisi', 'hic', 
    'haec', 'hoc', 'illud', 'ipsum', 'eum', 'ejus', 'tibi', 'mihi', 'nobis', 'vobis', 'se', 
    'suo', 'sua', 'suum', 'aliquid', 'omnia', 'nihil', 'unus', 'duo', 'tres', 'primo', 'secundo', 
    'tertio', 'liber', 'caput', 'versus', 'sermo', 'epistola', 'tractatus', 'distinctio', 
    'quaestio', 'articulus', 'apud', 'vel', 'atque', 'ac', 'si', 'nunc', 'tunc', 'post', 'ante', 
    'inter', 'contra', 'super', 'ob', 'propter', 'modo', 'ratione', 'causa', 're', 'rem', 'res', 
    'eorum', 'earum', 'suorum', 'suarum', 'illius', 'hujus', 'eo', 'ea', 'id', 'quos', 
    'quas', 'quo', 'qua', 'unde', 'ubi', 'ibi', 'inde', 'dum', 'donec', 'antequam', 
    'priusquam', 'quasi', 'tamquam', 'velut', 'utrum', 'an', 'num', 'ne', 'nonne', 'imo', 'potius', 
    'solum', 'tantum', 'ergo', 'ideo', 'igitur', 'itaque', 'propterea', 'quocirca', 'simul', 
    'hinc', 'illinc', 'illuc', 'huc', 'ii', 'eae', 'eius', 'ei', 'eam', 'eis', 'eos', 'eas', 
    'alius', 'alia', 'aliud', 'alter', 'altera', 'alterum', 'neuter', 'neutra', 'neutrum', 
    'solus', 'sola', 'solum', 'totus', 'tota', 'totum', 'ullus', 'ulla', 'ullum', 'nullus', 
    'nulla', 'nullum', 'uter', 'utra', 'utrum', 'quivis', 'quaevis', 'quodvis', 'quilibet', 
    'quaelibet', 'quodlibet', 'quisque', 'quaeque', 'quodque', 'unusquisque', 'unaquaeque', 
    'unumquodque', 'quidam', 'quaedam', 'quoddam', 'quis', 'quid', 'quisnam', 'quaenam', 
    'quidnam', 'ecquis', 'ecquae', 'ecquid', 'quispiam', 'quaepiam', 'quidpiam', 'pene', 
    'prope', 'fere', 'vix', 'statim', 'mox', 'deinde', 'tum', 'nuper', 'olim', 'aliquando', 
    'saepe', 'semper', 'nunquam', 'usque', 'quousque', 'adhuc', 'jam', 'equidem', 'saltem', 
    'nihilominus', 'attamen', 'verumtamen', 'nemo', 'nihilum', 'alias', 'aliter', 'secus', 
    'frustra', 'gratis', 'invito', 'sponte', 'vulgo', 'passim', 'idcirco', 'quapropter', 
    'quare', 'quomodo', 'quemadmodum', 'utpote', 'nempe', 'scilicet', 'videlicet', 'quippe', 
    'sane', 'profecto', 'certe', 'forsitan', 'fortasse', 'forte', 'casu', 'temere', 'nequicquam', 
    'magis', 'minus', 'plus', 'aeque', 'pariter', 'similiter', 'valde', 'admodum', 'nimis', 
    'satis', 'bene', 'male', 'facile', 'difficile', 'cito', 'tarde', 'diu', 'pridem', 'antea', 
    'postea', 'deinceps', 'protinus', 'subito', 'repente', 'derepente', 'sensim', 'paulatim', 
    'pedetentim', 'ubique', 'nusquam', 'alibi', 'undique', 'utrobique', 'intus', 'foris', 
    'procul', 'longe', 'alio', 'eodem', 'utroque', 'quorsum', 'dextrorsum', 'sinistrorsum', 
    'sursum', 'deorsum', 'retrorsum', 'ultro', 'citro', 'obviam', 'unice', 'praecipue', 
    'praesertim', 'maximiter', 'plurimum', 'multum', 'paulum', 'aliquantum', 'partim', 
    'singulatim', 'generatim', 'speciatim', 'nominatim', 'sigillatim', 'vicissim', 'rursus', 
    'iterum', 'denuo', 'novo', 'semel', 'bis', 'ter', 'quater', 'pluries', 'saepius', 
    'frequentius', 'rarius', 'primum', 'secundum', 'tertium', 'postremum', 'ultima', 
    'postremo', 'denique', 'tandem', 'demum', 'extremum', 'finem', 'viro', 'domino', 
    'patrono', 'regis', 'observantia', 'subscribitur', 'cliens', 'tuus', 'invictissimi', 
    'clarissimoque', 'Poloniae', 'archiatro', 'conciliario', 'intimo', 'perpetua', 'colendo', 
    'deditissimus', 'Stephani', 'lib', 'cap', 'serm', 'sermo', 'epist', 'orat', 'tract', 
    'homil', 'haer', 'dial', 'enchirid', 'distinct', 'ad', 'aen', 'liv', 'hist', 'operam', 
    'omnem', 'suam', 'fucandis', 'barbarissimi', 'scriptoris', 'commentis', 'navante',
    'controversiam', 'moverunt', 'quidam', 'advenae', 'praecipui', 'theologus', 'medicus',
    'quorum', 'initio', 'opera', 'reformationis', 'valde', 'procliva', 'unius', 'solius',
    'vera', 'religione', 'deinceps', 'propter', 'nobis', 'vobis', 'tibi', 'te', 'me', 'se',
    'dei', 'patri', 'patre', 'filio', 'spiritui', 'sancto', 'eiusque', 'suisque', 'suae',
    'suis', 'suos', 'suas', 'sua', 'suum', 'suorum', 'suarum', 'nobiscum', 'vobiscum',
    'deum', 'christum', 'jesum', 'salvatorem', 'salvatore', 'redemptorem', 'redemptore',
    'mediatorem', 'mediatore', 'pontificem', 'pontifice', 'sacrificium', 'sacrificio',
    'satisfactionem', 'satisfactione', 'justificationem', 'justificatione', 'fidei',
    'operum', 'legis', 'gratiae', 'foederis', 'foedere', 'testamenti', 'testamento',
    'morte', 'cruce', 'sanguine', 'passione', 'resurrectione', 'ascensione', 'regno',
    'regni', 'regis', 'rege', 'altare', 'altari', 'templo', 'sacerdote', 'sacerdotibus',
    'pontifice', 'pontificibus', 'apostolo', 'apostolis', 'propheta', 'prophetis',
    'scriptura', 'scripturis', 'libris', 'libro', 'capite', 'versu', 'versibus',
    'dictis', 'dicto', 'verbis', 'verbo', 'sententia', 'sententiis', 'auctoritate', 'etc'
}

# English vocabulary to filter out false positives
ENGLISH_WORDS = {
    # Most common English words
    'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', 'you', 'that', 'he', 'was', 'for', 'on', 
    'are', 'as', 'with', 'his', 'they', 'i', 'at', 'be', 'this', 'have', 'from', 'or', 'one', 
    'had', 'by', 'word', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 
    'said', 'there', 'use', 'an', 'each', 'which', 'she', 'do', 'how', 'their', 'if', 'will', 
    'up', 'other', 'about', 'out', 'many', 'then', 'them', 'these', 'so', 'some', 'her', 
    'would', 'make', 'like', 'him', 'into', 'has', 'look', 'two', 'more', 'write', 'go', 
    'see', 'no', 'way', 'could', 'people', 'my', 'than', 'first', 'water', 'been', 'call', 
    'who', 'oil', 'its', 'now', 'find', 'long', 'down', 'day', 'did', 'get', 'come', 'made', 
    'may', 'part', 'over', 'new', 'sound', 'take', 'only', 'little', 'work', 'know', 'place', 
    'year', 'live', 'me', 'back', 'give', 'most', 'very', 'after', 'thing', 'our', 'just', 
    'name', 'good', 'sentence', 'man', 'think', 'say', 'great', 'where', 'help', 'through', 
    'much', 'before', 'line', 'right', 'too', 'mean', 'old', 'any', 'same', 'tell', 'boy', 
    'follow', 'came', 'want', 'show', 'also', 'around', 'form', 'three', 'small', 'set', 
    'end', 'does', 'another', 'well', 'large', 'must', 'big', 'even', 'such', 'because', 
    'turn', 'here', 'why', 'ask', 'went', 'men', 'read', 'need', 'land', 'different', 'home', 
    'us', 'move', 'try', 'kind', 'hand', 'picture', 'again', 'change', 'off', 'play', 'spell', 
    'air', 'away', 'animal', 'house', 'point', 'page', 'letter', 'mother', 'answer', 'found', 
    'study', 'still', 'learn', 'should', 'america', 'world', 'high', 'every', 'near', 'add', 
    'food', 'between', 'own', 'below', 'country', 'plant', 'last', 'school', 'father', 'keep', 
    'tree', 'never', 'start', 'city', 'earth', 'eye', 'light', 'thought', 'head', 'under', 
    'story', 'saw', 'left', 'don', 'few', 'while', 'along', 'might', 'close', 'something', 
    'seem', 'next', 'hard', 'open', 'example', 'begin', 'life', 'always', 'those', 'both', 
    'paper', 'together', 'got', 'group', 'often', 'run', 'important', 'until', 'children', 
    'side', 'feet', 'car', 'mile', 'night', 'walk', 'white', 'sea', 'began', 'grow', 'took', 
    'river', 'four', 'carry', 'state', 'once', 'book', 'hear', 'stop', 'without', 'second', 
    'late', 'later', 'miss', 'idea', 'enough', 'eat', 'face', 'watch', 'far', 'indian', 
    'really', 'almost', 'let', 'above', 'girl', 'sometimes', 'mountain', 'cut', 'young', 
    'talk', 'soon', 'list', 'song', 'being', 'leave', 'family', 'it', 'its', 'unto', 'thus', 
    # Theological / Context-specific English words
    'editor', 'note', 'treatise', 'death', 'justification', 'review', 'annotation', 
    'doctrine', 'deity', 'satisfaction', 'christ', 'gospel', 'mystery', 'vindicated', 
    'examined', 'catechism', 'published', 'common', 'called', 'testimony', 'perverse', 
    'exposition', 'interpretation', 'believe', 'proof', 'declare', 'divine', 'scripture', 
    'lectures', 'sec', 'sect', 'section', 'reference', 'objection', 'answer', 'firstly', 
    'secondly', 'thirdly', 'fourthly', 'lastly', 'indeed', 'rather', 'curious', 'intricate', 
    'accurate', 'private', 'public', 'particular', 'different', 'same', 'another', 
    'between', 'among', 'throughout', 'against', 'without', 'within', 'whose', 'whom', 
    'labor', 'favor', 'honor', 'error', 'pastor', 'doctor', 'counselor', 'impostor', 
    'author', 'savior', 'saviour', 'preface', 'reader', 'blessed', 'holy', 'spirit', 
    'grace', 'faith', 'works', 'law', 'covenant', 'blood', 'cross', 'resurrection', 
    'ascension', 'kingdom', 'church', 'apostle', 'prophet', 'psalm', 'chapter', 'verse', 
    'objections', 'answers', 'questions', 'question', 'translation', 'translated', 
    'ridiculous', 'gentile', 'gentiles', 'jews', 'jewish', 'greek', 'hebrew', 'syriac', 
    'latin', 'english', 'french', 'german', 'italian', 'spanish', 'romans', 'corinthians', 
    'ephesians', 'philippians', 'colossians', 'thessalonians', 'timothy', 'titus', 
    'philemon', 'hebrews', 'james', 'peter', 'john', 'jude', 'revelation', 'genesis', 
    'exodus', 'levitique', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 
    'ruth', 'samuel', 'kings', 'chronicles', 'ezra', 'nehemiah', 'esther', 'job', 
    'psalms', 'proverbs', 'ecclesiastes', 'canticles', 'isaiah', 'jeremiah', 'lamentations', 
    'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah', 'jonah', 'micah', 'nahum', 
    'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi', 'matthew', 'mark', 'luke', 
    'acts', 'opinion', 'opinions', 'heresy', 'heresies', 'orthodox', 'socinian', 
    'socinians', 'arian', 'arians', 'sabellian', 'sabellians', 'trinitarian', 
    'trinitarians', 'antitrinitarian', 'antitrinitarians'
}

SHARED_WORDS = {
    'in', 'is', 'an', 'a', 'ad', 'me', 'etc', 'post', 'cap', 'lib', 'sub', 'rem', 're', 
    'res', 'am', 'as', 'os', 'or', 'do', 'no', 'si', 'vel', 'ac', 'inter', 'pro', 'per', 'ab', 
    'ex', 'id', 'ii', 'eo', 'ea', 'sine', 'art', 'sect', 'sec'
}

# Common Latin endings (suffixes)
LATIN_SUFFIX_RE = re.compile(
    r'.*(?:orum|arum|ibus|issimus|issimi|issimusque|issimique|ae|am|um|as|os|is|'
    r'untur|itur|amur|emur|imur|antur|entur|isset|issent|issentque|ate|atis|'
    r'ere|ari|iri|or|ris|tur|mur|mini|ntur|o|i|(?<!o)us|a)$',
    re.I
)

def is_latin_word(word):
    word_clean = re.sub(r'[^a-zA-ZæœæŒ]', '', word).lower()
    if not word_clean:
        return False
    if word_clean in SHARED_WORDS:
        return 'shared'
    if word_clean in ENGLISH_WORDS:
        return False
    if word_clean in LATIN_DICTIONARY:
        return True
    if len(word_clean) >= 3 and LATIN_SUFFIX_RE.match(word_clean):
        return True
    return False

def tag_latin_words(text):
    """Scan the text (ignoring HTML tags) and wrap runs of 2+ Latin words in <span lang="la" xml:lang="la">."""
    if not text:
        return ""
    parts = re.split(r'(<[^>]+>)', text)
    out_parts = []
    
    for part in parts:
        if part.startswith('<'):
            out_parts.append(part)
        else:
            tokens = re.split(r'(\b[a-zA-ZæœæŒ\’-]+\b)', part)
            n = len(tokens)
            
            # Label word tokens as Latin, shared, or not
            labeled_tokens = []
            for idx, token in enumerate(tokens):
                if re.match(r'^[a-zA-ZæœæŒ\’-]+$', token):
                    labeled_tokens.append((token, is_latin_word(token)))
                else:
                    labeled_tokens.append((token, None))
            
            reconstructed = []
            i = 0
            while i < n:
                token, is_lat = labeled_tokens[i]
                if is_lat in (True, 'shared'):
                    # Collect Latin run
                    run_tokens = [labeled_tokens[i]]
                    j = i + 1
                    while j < n:
                        next_token, next_is_lat = labeled_tokens[j]
                        if next_is_lat in (True, 'shared'):
                            run_tokens.append(labeled_tokens[j])
                            j += 1
                        elif next_is_lat is False:
                            break
                        else:
                            # It is a separator. Only accumulate if there is a subsequent Latin word in the remaining tokens.
                            has_more_latin = False
                            k = j + 1
                            while k < n:
                                k_tok, k_is_lat = labeled_tokens[k]
                                if k_is_lat in (True, 'shared'):
                                    has_more_latin = True
                                    break
                                elif k_is_lat is False:
                                    break
                                k += 1
                            if has_more_latin and re.match(r'^[^\w<>&]+$', next_token):
                                run_tokens.append(labeled_tokens[j])
                                j += 1
                            else:
                                break
                    
                    # Trim trailing separators and shared words from the end of the run
                    while run_tokens:
                        last_tok, last_is_lat = run_tokens[-1]
                        if last_is_lat is True:
                            break
                        # It is a separator (None) or 'shared'. Pop it and adjust j.
                        run_tokens.pop()
                        j -= 1

                    # Count uniquely Latin words in the run
                    latin_word_count = sum(1 for tok, is_l in run_tokens if is_l is True)
                    if latin_word_count >= 2:
                        run_str = "".join(tok for tok, is_l in run_tokens)
                        # Split out leading/trailing spaces so they stay outside the tag
                        m = re.match(r'^(\s*)(.*?)(\s*)$', run_str, re.S)
                        lead_space, inner, trail_space = m.group(1), m.group(2), m.group(3)
                        reconstructed.append(f'{lead_space}<span lang="la" xml:lang="la">{inner}</span>{trail_space}')
                        i = j
                    else:
                        reconstructed.append(tokens[i])
                        i += 1
                else:
                    reconstructed.append(token)
                    i += 1
            
            out_parts.append("".join(reconstructed))
            
    return "".join(out_parts)

# ============================================================================
# EPUB STYLESHEET (GEMINI.md compliant)
# ============================================================================

EPUB_STYLESHEET = r"""
/*<![CDATA[*/
/* Eduardus Ekofius style — mobile-first, vintage serif */
body {
    -webkit-text-size-adjust: 100%;
    -webkit-font-smoothing: antialiased;
    overflow-wrap: break-word;   /* CSS3 standard */
    word-break: break-word;      /* Legacy WebKit fallback */
    line-height: 1.65;
    margin: 0.4em 0.5em !important;
    color: #111;
}

body, div, p, span, h1, h2, h3, h4, h5, h6 {
    font-family: Georgia, "Times New Roman", serif;
    /* No !important — lets Apple Books honour the reader's chosen font */
}

p {
    -webkit-hyphens: auto;
    hyphens: auto;
}

[lang="el"], [lang="el"] * {
    font-family: "GFS Porson", "SBL Greek", "Cardo", "SBL BibLit", serif !important;
    font-size: 1.15em;
}

[lang="he"], [lang="he"] * {
    direction: rtl;
    unicode-bidi: isolate;
    font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif !important;
    font-size: 1.5em;
    line-height: 1.24;
}

[lang="he"], [lang="he"] p, [lang="he"], [lang="he"] div {
    text-align: left;
}

/* Interactive Owen Blue Palette (#2a55a0) */
a, .noteref, a.footnote-ref, a.fn-link {
    color: #2a55a0 !important;
    text-decoration: none;
}

.noteref {
    vertical-align: super;
    font-size: 0.85rem;   /* root-relative to remain consistent inside headings */
    padding: 0.1em 0.2em; /* Easy-tap */
}

.noteref-glossary, .noteref-biographical {
    vertical-align: super;
    font-size: 0.85rem;
    padding: 0.1em 0.2em;
}

/* Modern Editorial Translation Link (Elegant Amber/Gold) */
a.noteref-trans, .noteref-trans {
    color: #b8860b !important;
    text-decoration: none;
    vertical-align: super;
    font-size: 0.85rem;
    padding: 0.1em 0.2em;
    font-weight: bold;
}
.noteref-trans sup {
    font-size: 0.95em;
    line-height: 1;
}

/* Modern Translation Footnote Sub-Block */
.footnote-modern-translation {
    margin-top: 0.4em !important;
    margin-bottom: 0.2em !important;
    font-size: 0.95em !important;
    color: #555 !important;
    border-left: 3px solid #d4af37 !important;
    padding-left: 8px !important;
    font-style: normal !important;
}

/* Modern Editorial Translations Page Header */
.translation-notes-header {
    margin-top: 3em !important;
    border-top: 2px double #ccc !important;
    padding-top: 1.5em !important;
    margin-bottom: 1.5em !important;
}

.endnotes-section-title {
    font-family: 'Proxima Nova', sans-serif !important;
    font-size: 1.4em !important;
    color: #111 !important;
    text-align: center !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* Original Phrase Label in Modern Translations */
.original-phrase {
    font-weight: bold !important;
}

/* Continuous Blockquotes */
blockquote p {
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    display: inline; /* Keep multiple <p> flowing as one prose block */
}

blockquote {
    display: block;
    border-left: 2.5px solid rgba(0, 0, 0, 0.08) !important;
    padding-left: 1.2em !important;
    margin: 1.2em 0 !important;
    font-size: 0.95em;
    text-align: left;
    line-height: 1.47;
}

/* Paragraph inside a <blockquote epub:type="z3998:quotation"> */
.blockquote-content {
    margin: 0;
    padding: 0;
    display: inline;
}

.cover {
    text-align: center;
    margin: 0;
    padding: 0;
}

.cover img {
    display: block;
    max-width: 100%;
    max-height: 100vh;
    height: auto;
    width: auto;
    margin: 0 auto;
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
    font-size: 0.72em;       /* Was 0.15em — literally 2px on a phone. Made readable. */
    font-weight: normal;
    text-transform: uppercase;
    letter-spacing: 0.35em;
    margin: 1.2em auto;
    opacity: 0.55;
    text-align: center;
    text-indent: 0;
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
.volume-title-page .title-divider-double {
    border-top: 1.5px solid rgba(176, 141, 45, 0.45);
    border-bottom: 0.5px solid rgba(176, 141, 45, 0.25);
    height: 3px;
    width: 60%;
    margin: 1.6em auto 1.4em;
}
.volume-title-page .title-meta-divider {
    border-top: 0.5px solid rgba(176, 141, 45, 0.25);
    width: 40%;
    margin: 2em auto 1.5em;
}
.volume-title-page .title-work-top {
    text-align: center;
    text-indent: 0;
    margin: 0 0 0.4em;
    font-size: 0.85em;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: #666;
    opacity: 0.75;
}
.volume-title-page .title-author-main {
    text-align: center;
    text-indent: 0;
    margin: 0 auto 0.6em;
    font-size: 2.3em;
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: bold;
    border: 0;
    padding: 0;
    color: #2a55a0; /* Monumental deep Owen Blue */
}
.volume-title-page .title-volume-number {
    text-align: center;
    text-indent: 0;
    margin: 1.2em 0 0.35em;
    font-size: 0.95em;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #2a55a0; /* Owen Blue */
    font-weight: bold;
}
.volume-title-page .title-volume-subtitle {
    text-align: center;
    text-indent: 0;
    margin: 0.3em 0;
    font-size: 1.2em;
    font-style: italic;
    color: #333;
    line-height: 1.35;
}
.volume-title-page .editor {
    font-size: 0.88em;
    font-style: italic;
    color: #555;
    margin-bottom: 0.8em;
    text-align: center !important;
    text-indent: 0 !important;
}
.volume-title-page .publisher-brand {
    font-variant: small-caps;
    letter-spacing: 0.16em;
    font-size: 1.05em;
    font-weight: 600;
    color: #111;
    margin: 0.4em auto 0.1em;
    text-align: center !important;
    text-indent: 0 !important;
}
.volume-title-page .publisher-loc {
    font-size: 0.76em;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: #666;
    margin: 0.1em auto;
    text-align: center !important;
    text-indent: 0 !important;
}
.volume-title-page .edition-year {
    font-size: 0.88em;
    letter-spacing: 0.18em;
    color: #b08d2d; /* Elegant Gold */
    font-weight: bold;
    margin-top: 0.4em;
    text-align: center !important;
    text-indent: 0 !important;
}


h1 {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 1.55em;
    font-weight: 700;
    letter-spacing: 0.04em;
    line-height: 1.25;
    margin: 2.2em 0 1.2em;
    page-break-before: always;
    -webkit-column-break-before: always;
    color: #111;
}

h1.primary {
    font-size: 1.5em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    text-align: center;
    border-bottom: 2px double rgba(42, 85, 160, 0.22); /* Owen Blue double brand border */
    padding-bottom: 0.45em;
    margin-bottom: 1.5em;
}

h2 {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 1.3em;
    font-weight: bold;
    margin: 1.6em 0 0.6em;
    line-height: 1.3;
    color: #111;
}

/* Elegant chapter number label (e.g. "CHAPTER I") */
h2.secondary, h3.secondary, h1.secondary {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    font-size: 0.9em;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.18em; /* Generous letter spacing */
    text-align: center;
    margin: 2.4em 0 0.4em !important;
    line-height: 1.3;
    border: none;
    padding: 0;
    color: #b08d2d; /* Elegant Muted Gold */
}

h3 {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 1.12em;
    font-weight: bold;
    margin: 1.4em 0 0.5em;
    line-height: 1.3;
    color: #222;
}

/* Chapter sub-topic heading within summaries */
h3.chapter-heading {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 0.95em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    line-height: 1.35;
    margin: 1.4em 6% 0.6em !important;
    text-indent: 0;
    color: #222;
}

/* Chapter title subtitle */
h4.chapter-subtitle {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 1.3em;
    font-weight: bold;
    letter-spacing: 0.02em;
    line-height: 1.3;
    margin: 0.4em 6% 1.2em !important;
    text-indent: 0;
    color: #111;
}

/* Editorial synopsis/summary block */
p.chapter-summary {
    font-family: Georgia, "Times New Roman", serif;
    font-style: italic;
    font-size: 0.92em;
    text-align: center;
    margin: 1.4em 10% 2.2em !important;
    text-indent: 0;
    line-height: 1.6;
    color: #444;
    border-top: 1.5px solid rgba(42, 85, 160, 0.12); /* Owen Blue top hairline */
    border-bottom: 1.5px solid rgba(42, 85, 160, 0.12); /* Owen Blue bottom hairline */
    padding: 0.85em 0.5em !important;
}

.digression-heading {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-size: 1.25em;
    color: #111;
    margin: 1.8em 0 0.6em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    page-break-before: always;
}

.roman-subheading {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    text-align: center;
    font-weight: normal; /* Preserves Goold look (bold numerals with normal-weight text) */
    text-indent: 0;
    margin: 1.4em 0 0.55em;
    color: #111;
    break-after: avoid;
    page-break-after: avoid;
    break-inside: avoid;
    page-break-inside: avoid;
}

.roman-list-item {
    text-align: left;
    text-indent: 0;
    margin: 0.5em 0;         /* Was 0.65em — reduces whitespace between list entries */
}

.list-item {
    text-align: left;
    text-indent: 0;
    margin: 0.45em 0;        /* Was 0.55em */
}

.list-item.list-level-1,
.roman-list-item.list-level-1,
.list-item.list-level-2,
.list-item.list-level-3,
.roman-list-item.list-level-2,
.roman-list-item.list-level-3 {
    margin-left: 0 !important;
    border-left: none !important;
    padding-left: 0 !important;
}

/* --- Visual Nesting Containers --- */
div.owen-branch {
    margin-top: 0.6em;
    margin-bottom: 0.6em;
    break-inside: auto !important;
    page-break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
}
div.owen-level-1 {
    margin-left: 0;
}
div.owen-level-2 {
    margin-left: 0.75em !important;
    border-left: 1.5px solid rgba(42, 85, 160, 0.12) !important;
    padding-left: 0.6em !important;
}
div.owen-level-3 {
    margin-left: 0.75em !important;
    border-left: none !important;
    padding-left: 0 !important;
}

/* Nested blockquotes alignment */
div.owen-branch blockquote {
    margin-left: 0.8em !important;
    border-left: 1.5px solid rgba(0, 0, 0, 0.06) !important;
    padding-left: 0.8em !important;
}

.roman-list-item b {
    display: inline;
    margin-bottom: 0;
}

/* Flat-syllabus anchor: a paragraph that has absorbed an inline enumeration.
   The absorbed markers are bold inline text; no extra indent is needed.
   This class exists primarily for future CSS targeting and reader tools. */
.syllabus-anchor {
    /* No override needed — inherits body paragraph spacing */
}

.analysis-part {
    text-align: left;
    text-indent: 0;
    margin: 1.2em 0 0.45em; /* Was 1.4em top — unnecessary height on mobile */
}

/* Front Matter Styling (Issue 107 / Issue 89) */

/* Decorative blurb title — used for 1-3 line ornamental headings on
   title-adjacent pages (e.g. "PREFACE" as a standalone centered line
   in blurb style). */
.front-matter-title {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    font-size: 1.3em;
    text-align: center;
    margin: 2.2em 0 1.2em;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #111;
}

/* Section heading for prose-heavy front matter (General Preface,
   Prefatory Notes, Prefaces, Analyses). h2-level, uppercase, centered — same visual weight as front-matter-title
   but semantically a heading element. */
.front-matter-heading {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif !important;
    font-size: 1.4em;
    text-align: center;
    margin: 2.4em auto 1.4em;
    font-weight: bold;
    text-transform: uppercase;
    text-indent: 0;
    max-width: 22em;
    letter-spacing: 0.08em;
    padding-bottom: 0.5em;
    border-bottom: 1.5px solid rgba(42, 85, 160, 0.22); /* Beautiful Owen Blue bottom divider */
    color: #111;
}

/* Decorative blurb body — for 2-5 line centered ornamental paragraphs
   on title-adjacent pages (author name, dedications, publisher info). */
.front-matter-body {
    font-family: Georgia, "Times New Roman", serif;
    text-align: center;
    font-style: italic;
    margin: 1.4em 8% !important;
    line-height: 1.6;
    text-indent: 0;
    color: #444;
}

/* Structural guide page — the full-page TOC-overview container */
.front-matter-section {
    margin: 1.5em 0;
}

.structural-guide-page {
    page-break-after: always;
}

.structural-guide-levels {
    margin: 1.8em 5%;
    padding: 0.5em 0.8em;
    border-left: 2.5px solid #2a55a0;
    background-color: rgba(42, 85, 160, 0.03);
}

/* Table of Abbreviations & Citations Guide */
.abbreviations-guide-page {
    page-break-after: always;
}
.abbreviations-table {
    width: 90% !important;
    margin: 1.5em auto !important;
    border-collapse: collapse !important;
    font-size: 0.95em !important;
}
.abbr-row {
    border-bottom: 1px solid #eee !important;
}
.abbr-row:last-child {
    border-bottom: none !important;
}
.abbr-code {
    font-weight: bold !important;
    color: #d4af37 !important;
    padding: 0.6em 1em 0.6em 0.5em !important;
    white-space: nowrap !important;
    vertical-align: top !important;
    width: 25% !important;
}
.abbr-desc {
    padding: 0.6em 0.5em 0.6em 1em !important;
    color: #444 !important;
    line-height: 1.5 !important;
    text-align: left !important;
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
    text-indent: 1.1em;
    margin: 0;
    text-align: justify;
    orphans: 2;
    widows: 2;
}

p.first, p.noindent {
    text-indent: 0;
}

/* Scripture reference used as a standalone introduction to a displayed
   quotation, e.g. "1 Corinthians 10:9," on its own line before the blockquote.
   No indent — it reads as the lead-in citation for the following block. */
p.scripture-ref-introduction {
    margin-bottom: 0.1em;
    font-size: 0.92em;
    color: inherit;
    text-indent: 0;
}

/* Proof-text hierarchy: a blockquote immediately following a list-item should
   appear visually subordinate to it, not jut left at body margin.

   Without this rule, a list-item's text starts at ~2.1em (margin 1.25em +
   border 2px + padding 0.7em) while the default blockquote sits at only 1.2em —
   so the proof-text quote sticks out to the LEFT of the item it proves.

   The selectors mirror the three list levels. list-level-1 items have no
   left margin so 1.5em is enough; level-2 and level-3 need proportionally
   more to clear the item's own indent. */
p.list-item.list-level-1 + blockquote {
    margin-left: 1.5em;
    border-left-color: rgba(0, 0, 0, 0.12);
}
p.list-item.list-level-2 + blockquote {
    margin-left: 2.7em;
    border-left-color: rgba(0, 0, 0, 0.10);
}
p.list-item.list-level-3 + blockquote {
    margin-left: 3.5em;
    border-left-color: rgba(0, 0, 0, 0.08);
}

/* Sermon opening scripture verse — the text the sermon expounds.
   Centred, italic, no side border; distinct from inline doctrinal quotations. */
blockquote.sermon-opening-scripture {
    border-left: none;
    text-align: center;
    font-style: italic;
    font-size: 1em;
    margin: 1.4em 1.5em 1.8em;
    padding: 0;
    line-height: 1.55;
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

.small-caps {
    font-variant: small-caps;
}

sup {
    font-size: 0.72em;
    line-height: 0;
    vertical-align: super;
}

.footnote {
    font-size: 0.88em;
    text-indent: 0;
    margin: 0.4em 0;        /* Slightly more space between footnotes on mobile */
    line-height: 1.55;
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

/* Consecutive noterefs: keep them visually separated */
.noteref + .noteref {
    margin-left: 0;
}

.noteref sup {
    font-size: 0.95em;
    line-height: 1;
}

.doxology {
    text-align: center;
    text-indent: 0;
    margin: 2em 0 1.2em;
}

/* Scholastic anchor: Obj. / Ans. / Use N. — each on its own paragraph */
p.scholastic-anchor {
    text-align: left;
    text-indent: 0;
    margin-top: 1.5em;
}
p.scholastic-anchor-parent,
p.scholastic-anchor-child {
    /* Semantic subclasses for mobile-first visual Cap */
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
.contents-general-preface {
    margin-top: 1em;
    margin-bottom: 1em;
    font-weight: bold;
    text-align: center;
}
.contents-page {
    max-width: 38em;
    margin: 0 auto;
    padding: 1.5em 1em 2.5em;
    box-sizing: border-box;
}
.contents-volume-title {
    text-align: center;
    text-indent: 0;
    font-family: "Owen Title", "Baskervville", "Baskerville", serif !important;
    font-size: 1.55em;
    margin: 1.5em 0 1.8em;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #111;
    font-weight: bold;
    border: 0;
    padding: 0 0 0.6em;
    border-bottom: 1.5px double rgba(42, 85, 160, 0.25); /* Double border in Owen Blue */
}
.contents-treatise-title {
    text-align: center;
    text-indent: 0;
    font-family: "Owen Title", "Baskervville", "Baskerville", serif !important;
    font-size: 1.15em;
    line-height: 1.45;
    margin: 2.5em 0 1.2em;
    padding: 0.75em 5%;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #2a55a0; /* Owen Blue */
    font-weight: bold;
    border-top: 1.5px solid rgba(42, 85, 160, 0.15);
    border-bottom: 1.5px solid rgba(42, 85, 160, 0.15);
}
.contents-section-title {
    text-align: center;
    text-indent: 0;
    font-size: 0.9em;
    line-height: 1.4;
    margin: 1em auto 0.5em;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #555;
    font-weight: bold;
}
.contents-frontmatter-line {
    text-align: center;
    text-indent: 0;
    margin: 0.8em auto 1.4em;
    font-size: 0.82em;
    line-height: 1.5;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #555;
}
.contents-part-title {
    text-align: left;
    text-indent: 0;
    font-size: 1.1em;
    line-height: 1.3;
    font-weight: bold;
    margin: 1.8em 0 0.8em;
    padding-bottom: 0.2em;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
    letter-spacing: 0.02em;
    color: #111;
}
.contents-item,
.ContentsItem {
    margin: 1.2em 0;
    padding: 0;
    text-indent: 0 !important;
    text-align: left;
    color: #111;
    font-size: 0.95em;
    line-height: 1.5;
}
.contents-desc {
    margin: 0.5em 0 1em 1.5em;
    font-size: 0.9em;
    line-height: 1.4;
    color: #555;
    font-style: italic;
}
.contents-label {
    display: block;
    font-family: "Proxima Nova", "Owen Title", "Baskervville", sans-serif !important;
    font-size: 0.72rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #2a55a0; /* Accent color */
    margin-bottom: 0.2em;
}

/* Colophon/Copyright Page Styling */
.colophon-page {
    font-family: Georgia, "Times New Roman", serif;
    padding: 10% 8% 8%;
    max-width: 32em;
    margin: 0 auto;
    page-break-before: always;
    -webkit-column-break-before: always;
    box-sizing: border-box;
    font-size: 0.9em;
    line-height: 1.6;
    color: #333;
}
.colophon-title {
    font-family: "Baskervville", "Baskerville", "Hoefler Text", "Garamond", serif;
    font-variant: small-caps;
    font-size: 1.5em;
    font-weight: bold;
    text-align: center;
    margin-bottom: 2em;
    color: #111;
    letter-spacing: 0.05em;
}
.colophon-section {
    margin-bottom: 1.8em;
}
.colophon-section-title {
    font-family: "Baskervville", "Baskerville", serif;
    font-weight: bold;
    text-transform: uppercase;
    font-size: 0.85em;
    letter-spacing: 0.1em;
    color: #2a55a0;
    margin-bottom: 0.4em;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    padding-bottom: 0.2em;
}
.colophon-section p {
    text-indent: 0 !important;
    text-align: left !important;
    margin: 0 0 0.5em 0 !important;
    font-size: 0.95em;
}
.colophon-text {
    text-indent: 0 !important;
    text-align: left !important;
    margin: 0 0 0.5em 0 !important;
    font-size: 0.95em;
}
.colophon-metadata-list {
    margin: 0;
    padding: 0;
    list-style: none;
}
.colophon-metadata-item {
    margin-bottom: 0.4em;
    text-align: left;
}
.colophon-metadata-label {
    font-weight: bold;
    color: #555;
    display: inline-block;
    width: 8.5em;
}
.colophon-metadata-value {
    color: #111;
}
.colophon-ornament {
    text-align: center;
    font-size: 1.2em;
    margin: 2em auto;
    color: #b08d2d;
}

/* Premium Curation Styles */
.emblem-container {
    text-align: center;
    margin: 0 auto 1.5em;
    width: 90px;
    height: 90px;
    display: block;
    border-radius: 50%;
    overflow: hidden;
    border: 1.5px solid rgba(176, 141, 45, 0.45);
    box-shadow: 0 4px 12px rgba(176, 141, 45, 0.2);
    background: transparent;
}
.title-emblem-seal {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
}
.epub-signature {
    margin-top: 2.2em;
    margin-bottom: 2em;
    text-align: right;
    font-style: italic;
    break-inside: avoid;
    padding-right: 1.2em;
    border-right: 2px solid rgba(176, 141, 45, 0.22);
}
.signature-intro {
    margin: 0 0 0.3em;
    font-size: 0.95em;
    color: #444;
}
.signature-name {
    margin: 0 0 0.3em;
    font-weight: bold;
    font-size: 1.05em;
    font-variant: small-caps;
    letter-spacing: 0.08em;
    color: #2a55a0;
}
.signature-date {
    margin: 0;
    font-size: 0.90em;
    color: #666;
}
.contents-part-divider {
    text-align: center;
    margin: 2.2em 0 1.6em;
    break-after: avoid;
}
.contents-part-divider .divider-ornament {
    display: block;
    font-size: 1.1em;
    color: #b08d2d;
    margin-bottom: 0.3em;
}
.contents-part-divider .contents-part-title {
    font-family: inherit;
    font-size: 1.12em;
    font-weight: bold;
    font-variant: small-caps;
    letter-spacing: 0.12em;
    color: #2a55a0;
    margin: 0 auto;
    display: inline-block;
    padding: 0.25em 1.2em;
    border-top: 1px solid rgba(176, 141, 45, 0.22);
    border-bottom: 1px solid rgba(176, 141, 45, 0.22);
}
.chapter-end-marker {
    text-align: center;
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif;
    font-size: 1.05em;
    font-weight: bold;
    font-variant: small-caps;
    letter-spacing: 0.18em;
    color: #b08d2d; /* Classic Gold */
    margin: 2.5em auto 1.8em;
    display: block;
    break-inside: avoid;
}
.prefatory-salutation {
    font-family: "Owen Title", "Baskervville", "Baskerville", "Hoefler Text", "Garamond", "Times New Roman", serif;
    font-size: 1.05em;
    font-weight: bold;
    font-style: italic;
    color: #444;
    text-align: left !important;
    text-indent: 0 !important;
    margin: 1.6em 0 1.2em !important;
    display: block;
    border: none !important;
    padding: 0 !important;
}
/*]]>*/
"""


# ============================================================================
# EPUB3 INLINE FONT INJECTION STYLES
# ============================================================================

EPUB3_FONT_STYLES = r"""
/* Injected font-face declarations and language-specific overrides */
/* Primary body font: {primary_font} */
@font-face {{
    font-family: "{primary_font}";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/{primary_file}");
}}
{bold_face}
{italic_face}
{bold_italic_face}
/* Proxima Nova — heading display font */
@font-face {{
    font-family: "Proxima Nova";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/Proxima Nova Regular.ttf");
}}
@font-face {{
    font-family: "Proxima Nova";
    font-weight: bold;
    font-style: normal;
    src: url("../Fonts/Proxima Nova Extrabold.ttf");
}}
@font-face {{
    font-family: "Proxima Nova";
    font-weight: normal;
    font-style: italic;
    src: url("../Fonts/Proxima Nova Light.ttf");
}}
@font-face {{
    font-family: "Proxima Nova";
    font-weight: bold;
    font-style: italic;
    src: url("../Fonts/Proxima Nova Semibold.ttf");
}}
/* SBL BibLit — universal biblical fallback */
@font-face {{
    font-family: "SBL BibLit";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/SBL_BLit.ttf");
}}
/* SBL Greek — polytonic Greek */
@font-face {{
    font-family: "SBL Greek";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/SBL_grk.ttf");
}}
/* SBL Hebrew — fully pointed Hebrew */
@font-face {{
    font-family: "SBL Hebrew";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/SBL_Hbrw.ttf");
}}
/* Ezra SIL — BHS-style Hebrew fallback */
@font-face {{
    font-family: "Ezra SIL";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/SILEOT.ttf");
}}
/* GFS Porson — classical Greek font */
@font-face {{
    font-family: "GFS Porson";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/GFSPorson.ttf");
}}
/* Cardo — Latin font designed for classical scholarship */
@font-face {{
    font-family: "Cardo";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/Cardo-Regular.ttf");
}}
@font-face {{
    font-family: "Cardo";
    font-weight: bold;
    font-style: normal;
    src: url("../Fonts/Cardo-Bold.ttf");
}}
@font-face {{
    font-family: "Cardo";
    font-weight: normal;
    font-style: italic;
    src: url("../Fonts/Cardo-Italic.ttf");
}}
/* Gentium Plus — Latin backup font */
@font-face {{
    font-family: "Gentium Plus";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/GentiumPlus-R.ttf");
}}
@font-face {{
    font-family: "Gentium Plus";
    font-weight: normal;
    font-style: italic;
    src: url("../Fonts/GentiumPlus-I.ttf");
}}
/* Owen Title - embedded Baskervville title display face */
@font-face {{
    font-family: "Baskervville";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/BaskervilleBT.ttf");
}}
@font-face {{
    font-family: "Baskervville";
    font-weight: normal;
    font-style: italic;
    src: url("../Fonts/BaskervilleItalicBT.ttf");
}}
@font-face {{
    font-family: "Owen Title";
    font-weight: normal;
    font-style: normal;
    src: url("../Fonts/BaskervilleBT.ttf");
}}
@font-face {{
    font-family: "Owen Title";
    font-weight: bold;
    font-style: normal;
    src: url("../Fonts/BaskervilleBT.ttf");
}}
@font-face {{
    font-family: "Owen Title";
    font-weight: normal;
    font-style: italic;
    src: url("../Fonts/BaskervilleItalicBT.ttf");
}}
/* Body text — primary embedded font (Apple Books must respect this) */
body, div, p, span {{
    font-family: "{primary_font}", "SBL BibLit", serif !important;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
}}
/* Headings — Baskervville vintage serif display font (Issue 25) */
h1, h2, h3, h4, h5, h6 {{
    font-family: "Baskervville", "Owen Title", "Baskerville", "Hoefler Text", "Garamond", "{primary_font}", serif !important;
    line-height: 1.3;
    -webkit-font-smoothing: antialiased;
}}
/* Roman list items and subheadings use body font, not heading font (Issue 24) */
h4.roman-subheading, .roman-list-item, .roman-list-item b {{
    font-family: "{primary_font}", "SBL BibLit", serif !important;
}}
[lang="el"], [lang="el"] *, .greek, .greek * {{
    font-family: "GFS Porson", "SBL Greek", "SBL BibLit", serif !important;
    font-size: 1.05em;
}}
[lang="he"], [lang="he"] *, .hebrew, .hebrew * {{
    direction: rtl;
    unicode-bidi: isolate;
    font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", serif !important;
    font-size: 1.10em;
    line-height: 1.24;
}}
[lang="he"], [lang="he"] p,
[lang="he"], [lang="he"] div {{
    text-align: left;
}}
{latin_styles}
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
    
    # Sort files so that explicitly-named Regular/Roman faces come first,
    # ensuring they claim the primary slot ahead of Medium/Condensed/etc.
    # Within each group sort by (length, name) for deterministic results.
    def _font_sort_key(path):
        n = os.path.basename(path).lower()
        stem = os.path.splitext(n)[0]
        is_explicitly_regular = ('regular' in n or 'roman' in n
                                  or n.endswith('-r.') or n.endswith('_r.'))
        return (0 if is_explicitly_regular else 1, len(n), n)

    sorted_files = sorted(primary_font_files.values(), key=_font_sort_key)

    for font_file in sorted_files:
        fname = os.path.basename(font_file).lower()

        is_bold = 'bold' in fname or '-b.' in fname or '_b.' in fname or '-bd.' in fname or '_bd.' in fname
        _ext = os.path.splitext(fname)[1]
        _stem = os.path.splitext(fname)[0]
        is_italic = (
            'italic' in fname or 'ital' in fname
            or '-i.' in fname or '-it.' in fname
            or '_i.' in fname or '_it.' in fname
            or _stem.endswith('-it') or _stem.endswith('_it')
            or _stem.endswith('it')  # e.g. boldit, semiboldit
        )
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
        bold_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    font-style: normal;\n    src: url("../Fonts/{bold_file}");\n}}'
    
    italic_face = ''
    if italic_file:
        italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: normal;\n    font-style: italic;\n    src: url("../Fonts/{italic_file}");\n}}'
    
    bold_italic_face = ''
    if bold_italic_file:
        bold_italic_face = f'@font-face {{\n    font-family: "{primary_font_name}";\n    font-weight: bold;\n    font-style: italic;\n    src: url("../Fonts/{bold_italic_file}");\n}}'
    
    if 'cardo' in primary_font_name.lower():
        latin_font_stack = '"Gentium Plus", serif'
    else:
        latin_font_stack = '"Cardo", "Gentium Plus", serif'
    
    latin_styles = f'[lang="la"], [lang="la"] *, .latin, .latin * {{\n    font-family: {latin_font_stack} !important;\n}}'
    
    return EPUB3_FONT_STYLES.format(
        primary_font=primary_font_name,
        primary_file=primary_file,
        bold_face=bold_face,
        italic_face=italic_face,
        bold_italic_face=bold_italic_face,
        latin_styles=latin_styles,
    )
