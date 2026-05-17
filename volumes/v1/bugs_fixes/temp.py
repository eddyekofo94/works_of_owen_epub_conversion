
   1 - #!/usr/bin/env python3
         2 - """
         3 - render.py — Stage 2: Rendering and EPUB3 assembly.
         4 -
         5 - Responsible for:
         6 -   - markdown_to_html() and all paragraph/inline rendering helpers
         7 -   - Catechism Q&A rendering
         8 -   - Greek/Hebrew Unicode tagging (tag_unicode_ranges, force_polyglot_mapping)
         9 -   - EPUB3 assembly: nav, ncx, title page, endnotes, cover, frontispiece
        10 -   - find_cover(), find_portrait(), generate_nav_xhtml(), etc.
        11 -   - Scholastic anchor post-processor
        12 -
        13 - Imported by converter.py (legacy orchestrator) and volumes/vN/convert.py.
        14 - Issue 91: Extracted from converter.py as part of the two-stage modular refactor.
        15 - """
        16 -
        17 - import sys, os, re, uuid, shutil, zipfile, tempfile, hashlib, json, subprocess
        18 - from datetime import datetime
        19 - from html import escape as _html_escape
        20 - from pathlib import Path
        21 - from dataclasses import dataclass, field
        22 - from typing import Optional
        23 -
        24 - _RENDER_DIR = Path(__file__).parent.resolve()
        25 - if str(_RENDER_DIR) not in sys.path:
        26 -     sys.path.insert(0, str(_RENDER_DIR))
        27 -
        28 - from shared import (
        29 -     VOLUME_CONFIG, VOLUME_SUBTITLES,
        30 -     EPUB_STYLESHEET, generate_font_styles,
        31 -     select_primary_font, SBL_SUPPLEMENTS, EZRA_SIL_FILES,
        32 -     convert_greek_word, clean_greek_text, convert_gideon_hebrew,
        33 -     normalize_characters, polytonic_sweep,
        34 - )
        35 -
        36 - try:
        37 -     from ebooklib import epub
        38 - except ImportError:
        39 -     sys.exit("Error: ebooklib not installed.")
        40 -
        41 - FONT_BASE = os.path.join(_RENDER_DIR, 'fonts')
        42 -
        43 -
        44 - # ================================================================
        45 - # SHARED CONSTANTS (also used by extract.py)
        46 - # ================================================================
        47 -
        48 - # ─── Font Detection ────────────────────────────────────────────
        49 - GREEK_FONTS = {'Koine-Medium', 'ENLFEN+Koine-Medium'}
        50 - HEBREW_FONTS = {'Gideon-Medium', 'MOLFEN+Gideon-Medium'}
        51 -
        52 - # Regex for detecting Beta Code words that missed font tagging.
        53 - # Keep this conservative: the fallback runs after ordinary prose has been
        54 - # escaped, so broad markers like apostrophe or leading j/J corrupt English
        55 - # words such as "author's", "Jesus", "John", and "justification".
        56 - BETA_CODE_RE = re.compile(
        57 -     r"(?<!\S)(?![^æ;]*[æ;])(?:"
        58 -     r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+[><=~|{}+]+"
        59 -     r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
        60 -     r"[><=~|{}+]+[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+"
        61 -     r"[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW><=~|{}\[\]jJ+']*|"
        62 -     r"pneu'ma"
        63 -     r")\.?(?!\S)"
        64 - )
        65 -
        66 - # Regex for detecting Gideon Hebrew words that missed font tagging.
        67 - # Matches words containing unambiguous Gideon-only marks. Plain semicolon,
        68 - # bracket, and digit 1 are ordinary English/list punctuation and caused major
        69 - # false positives ("grace;" and "vol. 1" became Hebrew).
        70 - GIDEON_HEBREW_RE = re.compile(r'(?<!\S)[a-zA-Z\[\];1]*(?:[æ}])[a-zA-Zæ}\];1\[]*\.?(?!\S)')
        71 -
        72 - FOOTNOTE_MARKER_RE = re.compile(r'\[f(\d+)\]')
        73 - LOOSE_FOOTNOTE_MARKER_RE = re.compile(
        74 -     r'\[\s*f\s*(\d{1,3})\s*\]|(?<=[a-z])f\s*(\d{1,3})\b|(?<![A-Za-z])f\s*(\d{1,3})\b',
        75 -     re.I,
        76 - )
        77 - FOOTNOTE_PLACEHOLDER_RE = re.compile(r'FNREFTOKEN(\d+)TOKEN')
        78 - FT_MARKER_RE = re.compile(r'^ft(\d+)\s*', re.I)
        79 - EMPTY_BRACKET_RE = re.compile(r'\[\s*\]')
        80 - # Core structural regexes (Issue 26: CASE-SENSITIVE to avoid prose regressions)
        81 - STRUCTURAL_START_RE = re.compile(
        82 -     r'^(?:(?:\*\*|__)?)'
        83 -     r'(?:'
        84 -     r'(?!\d{4}\.)\d{1,3}\.\s+|'                         # 5. Mankind...
        85 -     r'\((?!\d{4}\))\d+\.?\)\s+|'                    # (1.) There... / (1) There...
        86 -     r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\s+|'  # (1st,) Such...
        87 -     r'\[\d+\.?\]\s+|'                    # [1.] There...
        88 -     r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\s+|'  # [1st,] There...
        89 -     r'[IVXLCDM]+\.\s+|'                  # I. / II.
        90 -     r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?\s+|'                       # Q. / A. catechism lines
        91 -     r'\d+(?:st|nd|rd|th)\b\s*[,.;]\s+|'  # 1st, 2nd, 3rd, 4th,
        92 -     r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?\s+|'  # 2ndly, 3rdly
        93 -     r'(?:First|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly|Again|But)\b[,.]?\s+'
        94 -     r')'
        95 - )
        96 -
        97 - STRUCTURAL_PREFIX_HTML_RE = re.compile(
        98 -     r'^(?P<marker>'
        99 -     r'(?!\d{4}\.)\d{1,3}\.|'
       100 -     r'\((?!\d{4}\))\d+\.?\)|'
       101 -     r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
       102 -     r'\[\d+\.?\]|'
       103 -     r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
       104 -     r'[IVXLCDM]+\.|'
       105 -     r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
       106 -     r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
       107 -     r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
       108 -     r')(?P<space>\s+)'
       109 - )
       110 -
       111 - INLINE_STRUCTURAL_MARKER_RE = re.compile(
       112 -     r'(?<!^)(?P<lead>\s+)'
       113 -     r'(?P<marker>'
       114 -     r'\((?!\d{4}\))\d+\.?\)|'
       115 -     r'\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)|'
       116 -     r'\[\d+\.?\]|'
       117 -     r'\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]|'
       118 -     r'\*\*\d+\.\*\*|'
       119 -     r'\*\*\((?!\d{4}\))\d+\.?\)\*\*|'
       120 -     r'\*\*\((?!\d{4}\))\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\)\*\*|'
       121 -     r'\*\*\[\d+\.?\]\*\*|'
       122 -     r'\*\*\[\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?\]\*\*|'
       123 -     r'\*\*\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)\*\*\s*[,.;]?|'
       124 -     r'\*\*[IVXLCDM]+\.\*\*|'
       125 -     r'[IVXLCDM]+\.|'
       126 -     r'(?<![:\d-])(?!\d{4}\.)\d+\.|'
       127 -     r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
       128 -     r'\d+(?:st|nd|rd|th)\b\s*[,.;]|'
       129 -     r'\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b[,.]?'
       130 -     r')(?P<trail>\s+)'
       131 - )
       132 - # ROMAN_HEADING_RE: Only match if the following text is short or All-Caps (Issue 21)
       133 - ROMAN_HEADING_RE = re.compile(
       134 -     r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?\s+'
       135 -     r'(?P<rest>[^a-z]{1,150}|[A-Z][a-z ]{1,45}|[A-Z][a-z ]{1,45}\.)$'
       136 - )
       137 - ROMAN_ONLY_RE = re.compile(r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?$')
       138 - PLAIN_CHAPTER_RE = re.compile(r'^(CHAPTER\s+\d+\.?)(?:\s+(.+))?$')
       139 - CITATION_ABBREV_TRAIL_RE = re.compile(
       140 -     r'\b(?:cap|chap|lib|serm|sermo|epist|orat|tract|homil|haer|dial|'
       141 -     r'enchirid|distinct|q|a|p|ad|m)\.?\s*$'
       142 -     r'|'
       143 -     # Page references: "p. 43" or "pp. 43" — should not be sentence ends
       144 -     r'\bp+\.\s+\d{1,4}\s*$'
       145 -     r'|'
       146 -     # Scripture book abbreviations before chapter:verse — e.g. "Cant. 5:10"
       147 -     r'\b(?:Cant|Prov|Eccl|Sol|Isa|Jer|Lam|Ezek|Dan|Hos|Zeph|Zech|Mal|'
       148 -     r'Matt|Mk|Lk|Jn|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Rev)\.\s*$',
       149 -     re.I,
       150 - )
       151 - CITATION_ABBREV_START_RE = re.compile(
       152 -     r'^(?:Lib|Serm|Sermo|Epist|Ep|Cap|Chap|Orat|Tract|Homil|Haer|Dial|Quest|Art|Dist|Part|Vol)\.?\s+',
       153 -     re.I,
       154 - )
       155 - CITATION_AUTHOR_TRAIL_RE = re.compile(
       156 -     r'\b(?:See\s+)?(?:August|Austin|Athan|Chrysost|Clem|Iren|Tertull|Jerome|'
       157 -     r'Basil|Nazianz|Cyprian|Ambros|Hilary|Epiphan|Aquin|Alexand|Alens)\.?\s*$',
       158 -     re.I,
       159 - )
       160 - ROMAN_LIST_TOKEN = '@@ROMAN_LIST@@'
       161 - MARKDOWN_STRUCTURAL_START_RE = re.compile(
       162 -     r'^\*\*(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
       163 -     r'\d+(?:(?:st|nd|rd|th)ly|st|nd|rd|th|dly|ly)[,.;]?)\*\*\s*[,.;]?\s+'
       164 - )
       165 - # ================================================================
       166 - # SCHOLASTIC ANCHOR POST-PROCESSOR
       167 - # ================================================================
       168 -
       169 - _SCHOLASTIC_LABEL_RE = re.compile(
       170 -     r'(?<![A-Z])'           # Not mid-word all-caps
       171 -     r'(?P<label>'
       172 -     r'(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.'
       173 -     r')'
       174 -     r'(?P<rest>\s)',
       175 -     re.I,
       176 - )
       177 -
       178 - _SCHOLASTIC_ANCHOR_SPLIT_RE = re.compile(
       179 -     r'([.!?"\u201d])\s+'           # closing punctuation / quote
       180 -     r'(?P<label>'
       181 -     r'(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.'
       182 -     r')\s',
       183 -     re.I,
       184 - )
       185 -
       186 - # Pattern to detect "Objection ." (space before period) — OCR artifact
       187 - _SCHOLASTIC_SPACE_DOT_RE = re.compile(
       188 -     r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application)\s+\.',
       189 -     re.I,
       190 - )
       191 -
       192 -
       193 - def apply_scholastic_anchor_protocol(html: str) -> str:
       194 -     """Post-processor: ensure Obj./Ans./Use. labels start their own paragraphs.
       195 -
       196 -     Runs on the assembled chapter XHTML string after markdown_to_html().
       197 -     Three transformations:
       198 -       1. Normalize "Objection ." → "Objection." (stray space OCR artifact).
       199 -       2. Force </p><p> break before any Obj./Ans./Use. label that appears
       200 -          mid-paragraph after closing punctuation.
       201 -       3. Wrap the label itself in <b> and assign class="scholastic-anchor".
       202 -     """
       203 -     # 1. Remove stray space before period in scholastic labels
       204 -     html = _SCHOLASTIC_SPACE_DOT_RE.sub(lambda m: m.group(1) + '.', html)
       205 -
       206 -     # 2. Force paragraph break before scholastic labels that appear mid-paragraph
       207 -     def _split_before_label(m: re.Match) -> str:
       208 -         return f'{m.group(1)}</p>\n<p class="scholastic-anchor"><b>{m.group("label")}</b> '
       209 -
       210 -     html = _SCHOLASTIC_ANCHOR_SPLIT_RE.sub(_split_before_label, html)
       211 -
       212 -     # 3. Ensure labels at paragraph start are bold
       213 -     html = re.sub(
       214 -         r'(<p(?:\s[^>]*)?>)\s*'
       215 -         r'(?P<label>(?:Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use\s+\d+\.?|Usus\s+\d+\.?|Application\s+\d+\.?)\.)\s',
       216 -         lambda m: f'{m.group(1)}<b class="scholastic-label">{m.group("label")}</b> ',
       217 -         html,
       218 -         flags=re.I,
       219 -     )

