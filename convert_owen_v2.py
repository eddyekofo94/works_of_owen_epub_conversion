#!/usr/bin/env python3
"""
Convert AGES Digital Library PDFs of John Owen's 16-volume Works to EPUBs via ThML XML.
Architecture: PDF → ThML XML → EPUB
"""

import os
import sys
import re
import unicodedata
from pathlib import Path
from collections import defaultdict
from xml.etree import ElementTree as ET
from xml.dom import minidom
import shutil
from datetime import datetime

# Third-party imports
try:
    from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTChar, LTAnno, LTFigure
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import PDFPageAggregator
except ImportError:
    print("Error: pdfminer.six not installed. Run: pip install pdfminer.six")
    sys.exit(1)

try:
    from ebooklib import epub
except ImportError:
    print("Error: ebooklib not installed. Run: pip install ebooklib")
    sys.exit(1)

# ============================================================================
# GREEK BETA CODE CONVERTER
# ============================================================================

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


def _convert_greek_word(word):
    """Convert Beta Code Greek to Unicode."""
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
        elif ch in DIACRITIC_CHARS and not result:
            # Leading diacritic with no base letter — drop it
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

# AGES Digital Library Gideon-Medium font encoding → Unicode Hebrew
# The Gideon font maps ASCII characters to Hebrew glyphs.
# Text is stored in visual L→R order (reversed from Hebrew reading direction).
# Each consonant may be followed by its vowel mark.

GIDEON_CHAR_MAP = {
    # Consonants (lowercase)
    'a': '\u05D0', 'b': '\u05D1', 'c': '\u05E1', 'd': '\u05D3',
    'f': '\u05D8', 'g': '\u05D2', 'h': '\u05D4', 'j': '\u05D7',
    'k': '\u05DB', 'l': '\u05DC', 'm': '\u05DE', 'n': '\u05E0',
    'q': '\u05E7', 'r': '\u05E8', 't': '\u05EA', 'v': '\u05E9\u05C1',
    'w': '\u05D5', 'x': '\u05E6', 'y': '\u05D9', '[': '\u05E2',
    # Uppercase = dagesh forms / final letters
    'A': '\u05D0',       'B': '\u05D1\u05BC', 'D': '\u05D3\u05BC',
    'G': '\u05D2\u05BC', 'K': '\u05DB\u05BC', 'M': '\u05DD',
    'N': '\u05DF',       'P': '\u05E3',       'Q': '\u05E7\u05BC',
    'T': '\u05EA\u05BC', 'W': '\u05D5\u05BC',
    # Vowel points
    ';': '\u05B8',   # ָ qamats
    '}': '\u05B2',   # ֲ chataf-patach
    ']': '\u05B0',   # ְ sheva
    '1': '\u05B7',   # ַ patach
    'e': '\u05B5',   # ֵ tsere
    'i': '\u05B4',   # ִ hiriq
    'o': '\u05B9',   # ֹ holem
    'O': '\u05B9',   # ֹ holem (uppercase variant)
    # Punctuation
    ',': ',', ' ': ' ',
}

# CID character codes (unresolved by pdfminer) → Unicode Hebrew
GIDEON_CID_MAP = {
    181: '\u05DD',   # ם final mem
    190: '\u05B7',   # ַ patach
    213: '\u05BE',   # ־ maqqef
    246: '\u05DF',   # ן final nun
    242: '\u05E3',   # ף final pe
    141: '\u05B8',   # ָ qamats
    139: '\u05B8',   # ָ qamats
    197: '\u05BC',   # ּ dagesh
    212: '\u05BF',   # ֿ rafe
    232: '\u05BC',   # ּ dagesh
    251: '\u05C2',   # שׂ sin-dot
}


def _is_hebrew_vowel(ch):
    """Check if a single character is a Hebrew combining mark."""
    if len(ch) != 1:
        return False
    cp = ord(ch)
    return (0x05B0 <= cp <= 0x05BD) or cp == 0x05BF or (0x05C1 <= cp <= 0x05C2)


def _convert_gideon_hebrew(encoded):
    """Convert Gideon font-encoded text to Unicode Hebrew.

    The Gideon encoding stores consonant+vowel pairs in visual L→R order.
    We map each character, tokenize into base+combining groups, then
    reverse the token/word order to get logical Hebrew reading order.
    """
    # Resolve (cid:NNN) references
    text = re.sub(
        r'\(cid:(\d+)\)',
        lambda m: GIDEON_CID_MAP.get(int(m.group(1)), ''),
        encoded
    )

    # Map each character to Hebrew
    mapped_chars = []
    for ch in text:
        if ch in GIDEON_CHAR_MAP:
            mapped_chars.append(GIDEON_CHAR_MAP[ch])
        elif ch == '\u00AF':       # macron → maqqef
            mapped_chars.append('\u05BE')
        else:
            mapped_chars.append(ch)
    flat = ''.join(mapped_chars)

    # Tokenize: group each base character with its following combining marks
    tokens = []
    current = ''
    for ch in flat:
        if _is_hebrew_vowel(ch):
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

    # Reverse tokens within each word, then reverse word order
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
# FONT ANALYSIS AND CLASSIFICATION
# ============================================================================

def classify_font(font_name, font_size):
    """
    Classify a font into semantic types.
    Returns (style_type, is_special_lang) where style_type is one of:
      h1, h2, h3, body, italic, bold, bold_italic, greek, hebrew, small_caps, skip
    """
    if not font_name:
        return 'body', False

    # Normalize font name (strip prefix)
    clean_font = font_name.split('+')[-1] if '+' in font_name else font_name

    is_greek = 'Koine' in clean_font
    is_hebrew = 'Gideon' in clean_font
    is_bold = 'Bold' in clean_font
    is_italic = 'Italic' in clean_font

    if is_greek:
        return 'greek', True
    if is_hebrew:
        return 'hebrew', True

    # Skip very small text (page numbers, scripture codes)
    if font_size < 9:
        return 'skip', False

    # Size-based classification for headings
    if font_size >= 20:
        return 'h1', False
    elif 14 <= font_size < 20:
        return 'h2', False

    # Small caps (size 9-10.5)
    if font_size < 10.5 and not is_bold:
        return 'small_caps', False

    # Body-size text (11-14): check bold/italic
    if is_bold and is_italic:
        return 'bold_italic', False
    elif is_bold:
        return 'bold', False
    elif is_italic:
        return 'italic', False
    else:
        return 'body', False


def is_page_number(text, font_size):
    """Check if text is a page number."""
    if font_size > 10:
        return False
    return text.strip().isdigit() and len(text.strip()) <= 3


def is_scripture_code(text):
    """Check if text is a scripture reference code like <401616>."""
    return bool(re.match(r'<[\dA-Z]{5,8}>', text.strip()))


# ============================================================================
# PDF TEXT EXTRACTION WITH FONT TRACKING
# ============================================================================

class FontRun:
    """Represents a run of text with consistent font properties."""

    def __init__(self, text, font_name, font_size, style_type):
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.style_type = style_type

    def __repr__(self):
        return f"FontRun({self.style_type}, {self.font_size}, {repr(self.text[:20])})"


def extract_text_with_fonts(pdf_path):
    """
    Extract text from PDF with per-character font metadata.
    Returns list of FontRun objects. A special FontRun with style_type='para_break'
    is inserted between textboxes to signal paragraph boundaries.
    """
    runs = []

    try:
        with open(pdf_path, 'rb') as fp:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page_num, page in enumerate(PDFPage.get_pages(fp)):
                interpreter.process_page(page)
                layout = device.get_result()

                for element in layout:
                    if isinstance(element, LTTextBox):
                        # Insert paragraph break between textboxes
                        if runs and runs[-1].style_type != 'para_break':
                            runs.append(FontRun('', '', 0, 'para_break'))

                        for line in element:
                            if isinstance(line, LTTextLine):
                                current_run_text = []
                                current_font = None
                                current_size = None

                                for char in line:
                                    if isinstance(char, LTChar):
                                        # Skip unmapped CID references (e.g., (cid:210))
                                        char_text = char.get_text()
                                        if char_text.startswith('(cid:'):
                                            continue

                                        font_name = char.fontname or 'Unknown'
                                        font_size = char.height

                                        # Check if we need to start a new run
                                        if (current_font is None or
                                            current_font != font_name or
                                            abs((current_size or 0) - font_size) > 0.5):

                                            # Save previous run
                                            if current_run_text:
                                                text = ''.join(current_run_text)
                                                style = classify_font(
                                                    current_font,
                                                    current_size
                                                )[0]
                                                if style == 'skip':
                                                    # Check for footnote ref: f followed by digits
                                                    clean = text.strip()
                                                    if re.match(r'^f\d{1,4}$', clean):
                                                        style = 'footnote_ref'
                                                    elif re.match(r'^FT\d{1,4}$', clean):
                                                        style = 'footnote_marker'
                                                if style != 'skip':
                                                    runs.append(FontRun(
                                                        text,
                                                        current_font,
                                                        current_size,
                                                        style
                                                    ))
                                            current_run_text = [char_text]
                                            current_font = font_name
                                            current_size = font_size
                                        else:
                                            current_run_text.append(char_text)
                                    elif isinstance(char, LTAnno):
                                        current_run_text.append(char.get_text())

                                # Save final run on line, adding trailing
                                # space so words don't merge across lines
                                if current_run_text:
                                    text = ''.join(current_run_text)
                                    if text and not text.endswith((' ', '\n', '-')):
                                        text += ' '
                                    style = classify_font(
                                        current_font,
                                        current_size
                                    )[0]
                                    if style == 'skip':
                                        clean = text.strip()
                                        if re.match(r'^f\d{1,4}$', clean):
                                            style = 'footnote_ref'
                                        elif re.match(r'^FT\d{1,4}$', clean):
                                            style = 'footnote_marker'
                                    if style != 'skip':
                                        runs.append(FontRun(
                                            text,
                                            current_font,
                                            current_size,
                                            style
                                        ))

    except Exception as e:
        print(f"  Error extracting text: {e}")
        return []

    return runs


# ============================================================================
# PDF CLEANUP AND PARAGRAPH DETECTION
# ============================================================================

def clean_text(text):
    """Remove artifacts and normalize text."""
    # Remove Private Use Area characters
    text = ''.join(ch for ch in text if not (0xE000 <= ord(ch) <= 0xF8FF))

    # Strip AGES font-change markers
    text = re.sub(r'\+(?=[a-zA-Z])', '', text)

    # Remove scripture reference codes
    text = re.sub(r'<[\dA-Z]{5,8}>', '', text)

    # Clean extra space after ( in scripture references
    text = re.sub(r'\(\s+', '(', text)

    # Collapse multiple spaces but preserve word boundaries
    text = re.sub(r' {2,}', ' ', text)
    # Replace newlines with spaces (PDF line breaks aren't real paragraphs)
    text = text.replace('\n', ' ')
    # Strip leading whitespace only
    text = text.lstrip()
    return text


def should_merge_chunks(prev_chunk, next_chunk):
    """Determine if two chunks should be merged (not new paragraph)."""
    if not prev_chunk or not next_chunk:
        return True

    prev = prev_chunk.strip()
    next_start = next_chunk.strip()

    if not prev or not next_start:
        return True

    # Never merge if next is a heading pattern
    heading_patterns = r'(?:CHAPTER|SERMON|DISCOURSE|PREFACE|INTRODUCTION|CONTENTS|INDEX)'
    if re.match(heading_patterns, next_start, re.IGNORECASE):
        return False

    # Always merge if prev ends mid-sentence
    if not prev[-1] in '.!?;:':
        return True

    # Always merge if next starts lowercase
    if next_start[0].islower():
        return True

    # Always merge if next is a Bible reference (book name + digit)
    bible_pattern = r'^(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1\s*Samuel|2\s*Samuel|1\s*Kings|2\s*Kings|1\s*Chronicles|2\s*Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs?|Ecclesiastes|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1\s*Corinthians|2\s*Corinthians|Galatians|Ephesians|Philippians|Colossians|1\s*Thessalonians|2\s*Thessalonians|1\s*Timothy|2\s*Timothy|Titus|Philemon|Hebrews|James|1\s*Peter|2\s*Peter|1\s*John|2\s*John|3\s*John|Jude|Revelation)\s+\d'
    if re.match(bible_pattern, next_start, re.IGNORECASE):
        return True

    # Always merge if prev ends with abbreviation
    if re.search(r'\b(?:chap|vol|pp?|ed|etc)\.$', prev, re.IGNORECASE):
        return True

    # Always merge if next is a verse reference
    if re.match(r'^\d+:\d+', next_start):
        return True

    # Default: don't merge (new paragraph)
    return False


# ============================================================================
# FOOTNOTE EXTRACTION
# ============================================================================

def extract_footnotes(pdf_path):
    """
    Extract footnotes from the end of PDF.
    Returns dict: {footnote_number: footnote_text}
    """
    footnotes = {}
    all_runs = extract_text_with_fonts(pdf_path)

    if not all_runs:
        return footnotes

    # Scan backwards to find footnote section
    ft_section_start = None
    non_ft_count = 0

    for i in range(len(all_runs) - 1, -1, -1):
        run_text = all_runs[i].text.strip()

        if run_text in ('FT', 'ft', 'NOTES', 'Notes'):
            ft_section_start = i + 1
            break

        # Allow up to 5 non-FT pages within footnote section
        if run_text and not run_text in ('FT', 'ft'):
            non_ft_count += 1
            if non_ft_count > 50:
                break

    if ft_section_start is None:
        return footnotes

    # Parse footnotes
    footnote_text = ' '.join(
        run.text for run in all_runs[ft_section_start:]
    )

    # Match footnote pattern: number followed by text
    pattern = r'(\d+)\s+(.+?)(?=\d+\s+|$)'
    for match in re.finditer(pattern, footnote_text, re.DOTALL):
        num = int(match.group(1))
        text = clean_text(match.group(2)).strip()
        if text:
            footnotes[num] = text

    return footnotes


# ============================================================================
# ThML XML GENERATION
# ============================================================================

class ThMLBuilder:
    """Build a ThML XML document from extracted text runs."""

    # AGES front matter patterns to skip (handles drop-cap spacing like "AGES IGITAL")
    FRONT_MATTER_RE = re.compile(
        r'(?:AGES\s*[DI]\s*[GI]\s*[TI]|B\s*o\s*o\s*k\s*s\s*F\s*o\s*r|'
        r'T\s*HE\s*AGES|AGES\s*Software|AGES\s*Library|'
        r'Albany,?\s*OR|www\.ageslibrary|'
        r'OHN\s*WEN\s*OLLECTION|IGITAL\s*IBRARY)',
        re.IGNORECASE
    )

    def __init__(self, title, author, volume_num):
        self.title = title
        self.author = author
        self.volume_num = volume_num
        self.chapters = []
        self.current_chapter = None
        self.current_paragraph = []
        self.in_heading = False
        self._past_front_matter = False
        self._heading_count = 0

    def _is_front_matter(self, text):
        """Check if text is AGES front matter that should be skipped."""
        if self._past_front_matter:
            return False
        if self.FRONT_MATTER_RE.search(text):
            return True
        # Very short text with lots of spaces (drop-cap fragmented titles)
        stripped = re.sub(r'\s+', '', text)
        if len(stripped) < 3:
            return True
        # Check for spaced-out drop-cap text pattern (single letters separated by spaces)
        words = text.strip().split()
        if words and all(len(w) <= 2 for w in words) and len(words) > 3:
            return True
        return False

    def add_run(self, run):
        """Add a FontRun to the document."""
        # Handle paragraph break signals from PDF textbox boundaries
        if run.style_type == 'para_break':
            if self.current_paragraph:
                self._flush_paragraph()
            return

        if run.style_type in ('h1', 'h2', 'h3'):
            # Finalize current paragraph
            if self.current_paragraph:
                self._flush_paragraph()

            text = clean_text(run.text)
            if not text:
                return

            # Skip AGES front matter
            if self._is_front_matter(text):
                return

            # If we're already accumulating a heading, append to it
            if self.in_heading and self.current_chapter and not self.current_chapter['paragraphs']:
                self.current_chapter['title'] += ' ' + text
                # Use the highest heading level seen
                level_order = {'h1': 0, 'h2': 1, 'h3': 2}
                if level_order.get(run.style_type, 9) < level_order.get(self.current_chapter['level'], 9):
                    self.current_chapter['level'] = run.style_type
            else:
                # Save previous chapter — keep even if it has no body
                # paragraphs, as it may be a title page fragment that the
                # merge step needs (e.g. "THE DIFFERENCES BETWEEN FAITH...")
                if self.current_chapter and (
                        self.current_chapter['paragraphs']
                        or self.current_chapter['title'].strip()):
                    self.chapters.append(self.current_chapter)

                # Start new chapter/section
                self.current_chapter = {
                    'title': text,
                    'level': run.style_type,
                    'paragraphs': []
                }
            self.in_heading = True
        else:
            self.in_heading = False
            # Body text (including italic, bold, greek, hebrew)
            text = clean_text(run.text)
            if not text:
                return

            # Skip AGES front matter body text
            if self._is_front_matter(text):
                return

            # Once we see substantial body text, we're past front matter
            if not self._past_front_matter and len(text.strip()) > 50:
                self._past_front_matter = True

            # Check if bold text is actually a chapter/section heading
            if run.style_type == 'bold' and re.match(
                r'^(?:CHAPTER|SERMON|DISCOURSE|EXERCITATION|PREFACE|'
                r'PREFATORY NOTE|DEDICATION|APPENDIX)\b',
                text.strip()
            ):
                # Treat as heading
                if self.current_paragraph:
                    self._flush_paragraph()
                if self.current_chapter and self.current_chapter['paragraphs']:
                    self.chapters.append(self.current_chapter)
                self.current_chapter = {
                    'title': text.strip(),
                    'level': 'h3',
                    'paragraphs': []
                }
                return

            # Merge drop caps: single uppercase letter followed by small_caps
            # e.g., "P" (body, large) + "REFATORY " (small_caps) → "PREFATORY "
            if (run.style_type == 'small_caps' and
                    self.current_paragraph and
                    len(self.current_paragraph) >= 1):
                prev_type, prev_text = self.current_paragraph[-1]
                if (prev_type in ('body', 'bold') and
                        len(prev_text.strip()) == 1 and
                        prev_text.strip().isupper()):
                    # Merge: drop the previous single letter, prepend to small_caps
                    self.current_paragraph.pop()
                    text = prev_text.strip() + text
                    self.current_paragraph.append(('small_caps', text))
                    return

            # Handle special text types
            if run.style_type == 'greek':
                # Pre-process: merge orphaned diacritics at word boundaries.
                # AGES PDFs split Greek text across lines, causing diacritic
                # chars (|=iota subscript, ~=circumflex, etc.) to become
                # standalone words.  In Beta Code diacritics follow their
                # base letter, but AGES sometimes puts them before the word
                # or after a line break.
                tokens = re.split(r'(\s+)', text)
                merged_tokens = []
                pending_diacritics = ''
                for tok in tokens:
                    if not tok.strip():
                        merged_tokens.append(tok)
                        continue
                    # Strip leading diacritics from tokens like "|,"
                    # where | is a diacritic but , is not.
                    leading = ''
                    rest = tok
                    while rest and rest[0] in DIACRITIC_CHARS:
                        leading += rest[0]
                        rest = rest[1:]
                    if leading and rest:
                        # Attach leading diacritics to previous word
                        attached = False
                        for j in range(len(merged_tokens) - 1, -1, -1):
                            if merged_tokens[j].strip():
                                merged_tokens[j] += leading
                                attached = True
                                break
                        if not attached:
                            pending_diacritics += leading
                        tok = rest  # continue processing the remainder
                    # Check if token is entirely diacritics
                    if all(c in DIACRITIC_CHARS for c in tok):
                        # Try to append to previous non-space word
                        attached = False
                        for j in range(len(merged_tokens) - 1, -1, -1):
                            if merged_tokens[j].strip():
                                merged_tokens[j] += tok
                                attached = True
                                break
                        if not attached:
                            # No previous word — save to append to next word
                            pending_diacritics += tok
                        continue
                    # If we have pending diacritics from start of text,
                    # only apply them if they make sense on this word.
                    # AGES puts iota subscript before the word it belongs to.
                    if pending_diacritics:
                        # Find last base letter in this word
                        last_base = ''
                        for c in reversed(tok):
                            if c not in DIACRITIC_CHARS:
                                last_base = c.lower()
                                break
                        remaining = ''
                        for dc in pending_diacritics:
                            if dc == '|':
                                # Iota subscript: only on α, η, ω
                                if last_base in ('a', 'h', 'w'):
                                    tok = tok + dc
                                # else drop — line-break artifact
                            elif dc in ('~', '='):
                                # Circumflex: only if word doesn't
                                # already have one
                                if '~' not in tok and '=' not in tok:
                                    tok = tok + dc
                                # else drop — duplicate
                            else:
                                remaining += dc
                        pending_diacritics = ''
                    merged_tokens.append(tok)

                # Convert each word
                converted = []
                for w in merged_tokens:
                    if w.strip():
                        converted.append(_convert_greek_word(w))
                    else:
                        converted.append(w)
                text = ''.join(converted)
                self.current_paragraph.append(('greek', text))
            elif run.style_type == 'hebrew':
                text = _convert_gideon_hebrew(text)
                self.current_paragraph.append(('hebrew', text))
            elif run.style_type == 'italic':
                self.current_paragraph.append(('italic', text))
            elif run.style_type == 'bold':
                self.current_paragraph.append(('bold', text))
            elif run.style_type == 'bold_italic':
                self.current_paragraph.append(('bold_italic', text))
            elif run.style_type == 'footnote_ref':
                # Footnote reference marker (e.g., f5)
                fn_match = re.match(r'^f(\d+)', text.strip())
                if fn_match:
                    fn_num = fn_match.group(1)
                    self.current_paragraph.append(('footnote_ref', fn_num))
                return
            elif run.style_type == 'footnote_marker':
                # Endnote section marker (e.g., FT5)
                ft_match = re.match(r'^FT(\d+)', text.strip())
                if ft_match:
                    ft_num = ft_match.group(1)
                    self.current_paragraph.append(('footnote_marker', ft_num))
                return
            elif run.style_type == 'small_caps':
                # Filter out page numbers (just digits)
                if text.strip().isdigit():
                    return
                self.current_paragraph.append(('small_caps', text))
            else:
                self.current_paragraph.append(('body', text))

    def _flush_paragraph(self):
        """Finalize current paragraph and add to chapter."""
        if not self.current_paragraph:
            return

        if not self.current_chapter:
            self.current_chapter = {
                'title': 'Untitled',
                'level': 'h1',
                'paragraphs': []
            }

        self.current_chapter['paragraphs'].append(self.current_paragraph)
        self.current_paragraph = []

    def finalize(self):
        """Finalize the document and clean up."""
        self._flush_paragraph()
        if self.current_chapter and self.current_chapter['paragraphs']:
            self.chapters.append(self.current_chapter)

        # Post-process: merge broken paragraphs (PDF page boundary artifacts)
        self._merge_broken_paragraphs()

        # Post-process: drop orphaned Greek fragments left by CID removal
        self._strip_cid_orphan_paragraphs()

        # Post-process: merge tiny consecutive chapters that are really
        # multi-line title blocks (e.g., "CHRISTOLOGIA" / "OR" / "A DECLARATION...")
        # Must run BEFORE _remove_empty_chapters so fragments aren't deleted
        self._merge_title_fragments()

        # Post-process: remove AGES front matter and empty chapters
        self._remove_empty_chapters()

        # Post-process: clean up merged titles
        self._clean_titles()

        # Second pass removal after cleaning
        self._remove_empty_chapters()

    def _merge_broken_paragraphs(self):
        """Merge paragraphs broken by PDF page boundaries.

        When a paragraph is split across pages, pdfminer creates separate
        text boxes, producing false paragraph breaks. We detect these by:
        - Previous paragraph ends without sentence-ending punctuation
        - Next paragraph starts with a lowercase letter
        """
        SENTENCE_ENDERS = set('.?!:;\u201d\u201c')

        for ch in self.chapters:
            if len(ch['paragraphs']) < 2:
                continue

            merged = [ch['paragraphs'][0]]
            for para in ch['paragraphs'][1:]:
                prev = merged[-1]
                # Get the text of the last run in the previous paragraph
                prev_text = ''
                for _, t in reversed(prev):
                    prev_text = t.rstrip()
                    if prev_text:
                        break

                # Get the text of the first run in the current paragraph
                curr_text = ''
                for _, t in para:
                    curr_text = t.lstrip()
                    if curr_text:
                        break

                # Check for broken paragraph: prev ends without punctuation,
                # current starts with lowercase
                should_merge = False
                if (prev_text and curr_text
                        and prev_text[-1] not in SENTENCE_ENDERS
                        and len(prev_text) > 10
                        and curr_text[0].islower()):
                    should_merge = True

                # Also merge if prev ends with a hyphen (word broken across pages)
                if prev_text and prev_text.endswith('-') and curr_text:
                    should_merge = True

                if should_merge:
                    # Append current para's runs to previous paragraph
                    # Add a space between if needed
                    if prev_text and not prev_text.endswith((' ', '-')):
                        merged[-1] = list(merged[-1])
                        merged[-1].append(('body', ' '))
                    merged[-1] = list(merged[-1]) + list(para)
                else:
                    merged.append(para)

            ch['paragraphs'] = merged

    def _strip_cid_orphan_paragraphs(self):
        """Remove tiny Greek-only paragraphs that are CID removal artifacts.

        When pdfminer encounters unmapped CID glyphs (e.g., Greek quotation
        marks), we skip them during extraction. This can leave behind orphaned
        fragments — a word or two of Greek text that was adjacent to the CID
        character and got its own paragraph. These are not real content.

        Criteria for removal:
        - Paragraph is very short (under 20 chars of actual text)
        - Consists entirely of Greek-tagged runs (possibly with diacritics)
        - Contains no English/body text
        """
        for ch in self.chapters:
            if not ch['paragraphs']:
                continue
            filtered = []
            for para in ch['paragraphs']:
                text = ''.join(t for _, t in para).strip()
                # Strip diacritics and punctuation for length check
                clean = text.replace('|', '').replace('~', '').strip()
                if len(clean) < 20:
                    # Check if all runs are Greek (no body text)
                    run_types = set(rtype for rtype, rtext in para if rtext.strip())
                    if run_types and run_types <= {'greek'}:
                        # This is a CID orphan — drop it
                        continue
                filtered.append(para)
            ch['paragraphs'] = filtered

    @staticmethod
    def _is_title_page_body(chapter):
        """Check if a chapter's body looks like title page decoration
        (connectors, italic descriptions, epigraphs) rather than prose."""
        connector_re = re.compile(
            r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|'
            r'WHEREIN,?|BEING,?|INTO,?)\s*$',
            re.IGNORECASE
        )
        prose_chars = 0
        for para in chapter['paragraphs']:
            # Build plain text of the paragraph
            text = ''.join(t for _, t in para).strip()
            if not text:
                continue
            # Connector word?
            if connector_re.match(text) and len(text) < 20:
                continue
            # Mostly italic? (title page descriptions)
            italic_chars = sum(len(t) for st, t in para if st == 'italic')
            total_chars = sum(len(t) for _, t in para)
            if total_chars > 0 and italic_chars / total_chars > 0.7:
                continue
            # Short uppercase line (subtitle fragment)
            if text.isupper() and len(text) < 80:
                continue
            # Looks like prose
            prose_chars += len(text)
        return prose_chars < 500

    def _merge_title_fragments(self):
        """Merge consecutive tiny chapters that form multi-line title blocks.

        Title pages in the AGES PDFs produce a sequence of heading-only
        chapters (e.g. "CHRISTOLOGIA" / "OR" / "A DECLARATION OF…").
        This merges those fragments into a single chapter, but STOPS
        when the next chapter has substantial prose body text (like a
        PREFATORY NOTE), keeping the title page separate.
        """
        if len(self.chapters) < 2:
            return

        # Pattern for section headings that should NOT be merged
        # (roman numerals, arabic numbers, CHAPTER N, SERMON N, etc.)
        section_heading_re = re.compile(
            r'^(?:[IVXLCivxlc]+\.?|'
            r'\d+\.?|'
            r'(?:CHAPTER|SERMON|SECTION|DISCOURSE|EXERCITATION)\s+[\dIVXLCivxlc]+\.?)\s*$'
        )

        merged = [self.chapters[0]]
        for ch in self.chapters[1:]:
            prev = merged[-1]
            prev_content_size = sum(
                len(t) for para in prev['paragraphs'] for _, t in para
            )

            # If previous chapter has very little body text, consider merging
            if prev_content_size < 100 and len(prev['paragraphs']) <= 3:
                # Never merge numbered section headings — these are real
                # divisions within the text (I., II., III., CHAPTER 1, etc.)
                prev_title_stripped = prev['title'].strip()
                if section_heading_re.match(prev_title_stripped):
                    merged.append(ch)
                # Check if current chapter is also title page decoration
                # (connectors, italic descriptions, short uppercase lines)
                # rather than prose content
                elif self._is_title_page_body(ch):
                    # Both are title page fragments — merge
                    ch['title'] = prev['title'] + ' \u2014 ' + ch['title']
                    ch['paragraphs'] = prev['paragraphs'] + ch['paragraphs']
                    level_order = {'h1': 0, 'h2': 1, 'h3': 2}
                    if level_order.get(prev['level'], 9) < level_order.get(ch['level'], 9):
                        ch['level'] = prev['level']
                    merged[-1] = ch
                else:
                    # Current chapter has real prose — stop merging
                    merged.append(ch)
            else:
                merged.append(ch)

        self.chapters = merged

    def _remove_empty_chapters(self):
        """Remove chapters with no meaningful content."""
        if not self.chapters:
            return

        # Find where the real content begins: first chapter with > 2000 chars
        real_start = 0
        for i, ch in enumerate(self.chapters):
            total = sum(len(t) for para in ch['paragraphs'] for _, t in para)
            if total > 2000:
                real_start = i
                break

        # Everything before the first substantial chapter is front matter/TOC
        # unless it's itself substantial
        cleaned = []
        for i, ch in enumerate(self.chapters):
            total_text = sum(
                len(t) for para in ch['paragraphs'] for _, t in para
            )

            # Skip AGES-related leftovers anywhere
            if self.FRONT_MATTER_RE.search(ch['title']):
                continue

            # Skip chapters whose title is just fragmented drop-cap junk
            title_stripped = re.sub(r'\s+', '', ch['title'])
            if len(title_stripped) < 5 and total_text < 100:
                continue

            # Before real content starts: only keep chapters with decent content
            # But protect merged title pages (contain em-dash from merge)
            if i < real_start and total_text < 500:
                if ' \u2014 ' not in ch['title']:
                    continue

            cleaned.append(ch)
        self.chapters = cleaned

    def _clean_titles(self):
        """Clean up chapter titles — remove redundant spaces, normalize."""
        for ch in self.chapters:
            # Collapse multiple spaces
            ch['title'] = re.sub(r'\s{2,}', ' ', ch['title']).strip()
            # Remove trailing/leading punctuation artifacts
            ch['title'] = ch['title'].strip(' —-:')
            # Remove duplicate section indicators from merges
            ch['title'] = re.sub(r'\s*—\s*—\s*', ' — ', ch['title'])

    def to_xml(self):
        """Generate ThML XML."""
        root = ET.Element('ThML')

        # Head
        head = ET.SubElement(root, 'ThML.head')
        einfo = ET.SubElement(head, 'electronicEdInfo')
        dc = ET.SubElement(einfo, 'DC')

        title_elem = ET.SubElement(dc, 'DC.Title')
        title_elem.text = self.title

        creator = ET.SubElement(dc, 'DC.Creator')
        creator.set('sub', 'Author')
        creator.text = self.author

        date_elem = ET.SubElement(dc, 'DC.Date')
        date_elem.text = datetime.now().isoformat()

        # Body
        body = ET.SubElement(root, 'ThML.body')

        for ch_idx, chapter in enumerate(self.chapters):
            div = ET.SubElement(body, 'div1')
            div.set('title', chapter['title'])
            div.set('id', f"ch{ch_idx + 1:03d}")

            # Heading
            h_tag = chapter['level']
            h_elem = ET.SubElement(div, h_tag)
            h_elem.text = chapter['title']

            # Paragraphs
            for para_runs in chapter['paragraphs']:
                p_elem = ET.SubElement(div, 'p')
                p_elem.set('class', 'Body')

                for run_type, run_text in para_runs:
                    if run_type == 'body':
                        if len(p_elem):
                            p_elem[-1].tail = (p_elem[-1].tail or '') + run_text
                        else:
                            p_elem.text = (p_elem.text or '') + run_text
                    elif run_type == 'greek':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('lang', 'EL')
                        span.set('class', 'Greek')
                        span.text = run_text
                    elif run_type == 'hebrew':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('lang', 'HE')
                        span.set('class', 'Hebrew')
                        span.text = run_text
                    elif run_type == 'italic':
                        i_elem = ET.SubElement(p_elem, 'i')
                        i_elem.text = run_text
                    elif run_type == 'bold':
                        b_elem = ET.SubElement(p_elem, 'b')
                        b_elem.text = run_text
                    elif run_type == 'bold_italic':
                        b_elem = ET.SubElement(p_elem, 'b')
                        i_elem = ET.SubElement(b_elem, 'i')
                        i_elem.text = run_text
                    elif run_type == 'footnote_ref':
                        a_elem = ET.SubElement(p_elem, 'a')
                        a_elem.set('class', 'fnref')
                        a_elem.set('href', f'#fn{run_text}')
                        a_elem.text = run_text
                    elif run_type == 'footnote_marker':
                        a_elem = ET.SubElement(p_elem, 'a')
                        a_elem.set('class', 'fnmarker')
                        a_elem.set('data-fn', run_text)
                        a_elem.text = ''
                    elif run_type == 'small_caps':
                        span = ET.SubElement(p_elem, 'span')
                        span.set('style', 'font-variant:small-caps')
                        span.text = run_text
                    else:
                        # Fallback
                        if len(p_elem):
                            p_elem[-1].tail = (p_elem[-1].tail or '') + run_text
                        else:
                            p_elem.text = (p_elem.text or '') + run_text

        return root


def prettify_xml(elem):
    """Return prettified XML string."""
    rough = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent='  ')


# ============================================================================
# PDF TO ThML CONVERSION
# ============================================================================

def pdf_to_thml(pdf_path, output_xml_path, volume_num):
    """
    Convert PDF to ThML XML.
    Returns True if successful, False otherwise.
    """
    print(f"  Extracting text from PDF...")
    runs = extract_text_with_fonts(pdf_path)

    if not runs:
        print(f"  Warning: No text extracted from PDF")
        return False

    print(f"  Building ThML document ({len(runs)} runs)...")
    subtitle = VOLUME_SUBTITLES.get(volume_num, "")
    title = f"The Works of John Owen, Vol. {volume_num}"
    if subtitle:
        title += f" — {subtitle}"

    builder = ThMLBuilder(title, "John Owen", volume_num)

    for run in runs:
        builder.add_run(run)

    builder.finalize()

    print(f"  Writing ThML XML...")
    root = builder.to_xml()
    xml_str = prettify_xml(root)

    try:
        with open(output_xml_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        print(f"  Saved ThML: {output_xml_path}")
        return True
    except Exception as e:
        print(f"  Error writing ThML: {e}")
        return False


# ============================================================================
# ThML TO EPUB CONVERSION
# ============================================================================

EPUB_STYLESHEET = """\
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
    margin: 0.5em 0 0.5em 0;
    font-size: 0.95em;
    text-indent: 0;
}

a.fn-link {
    color: #0066cc;
    text-decoration: none;
    font-size: 0.85em;
    margin-right: 0.3em;
}

aside[epub|type="endnote"] {
    margin-bottom: 0.8em;
    padding-left: 1.8em;
    text-indent: -1.8em;
}

a.footnote-ref {
    text-decoration: none;
    color: #0066cc;
    vertical-align: super;
    font-size: 0.75em;
}

/* Title page */
.title-page {
    text-align: center;
    margin: 0;
    padding: 8% 8% 5%;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 90vh;
}
.title-page .ornament {
    font-size: 1.6em;
    letter-spacing: 0.4em;
    margin-bottom: 2em;
    color: #8b6914;
}
.title-page h1 {
    font-size: 1.6em;
    margin: 0 0 0.2em;
    text-align: center;
    letter-spacing: 0.03em;
    line-height: 1.3;
}
.title-page .rule {
    display: block;
    width: 40%;
    max-width: 8em;
    height: 1px;
    background: #8b6914;
    border: none;
    margin: 1.2em auto;
}
.title-page .subtitle {
    font-size: 1.15em;
    font-style: italic;
    margin: 0.4em 0 0;
    text-align: center;
    letter-spacing: 0.02em;
}
/* Frontispiece portrait page */
.frontispiece {
    text-align: center;
    margin: 0;
    padding: 10% 10% 5%;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 85vh;
}
.frontispiece img {
    max-width: 80%;
    max-height: 70vh;
    height: auto;
    border: 1px solid #999;
}
.frontispiece .caption {
    font-size: 0.8em;
    font-style: italic;
    margin-top: 1em;
    letter-spacing: 0.03em;
}
.title-page .author {
    font-size: 1.05em;
    margin-top: 1.2em;
    text-align: center;
    letter-spacing: 0.05em;
}
.title-page .author .by {
    font-size: 0.85em;
    font-style: italic;
    display: block;
    margin-bottom: 0.3em;
    letter-spacing: 0;
}
.title-page .editor {
    font-size: 0.85em;
    font-style: italic;
    margin-top: 1em;
    text-align: center;
}
.title-page .publisher {
    margin-top: auto;
    padding-top: 2em;
    font-size: 0.8em;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    text-align: center;
}

/* Treatise title pages — decorative centered layouts */
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


def _escape_xml(text):
    """Escape text for safe embedding in XHTML."""
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def _make_xhtml(title, body_html, css_href='style/main.css'):
    """Create a well-formed XHTML5 document for Apple Books compatibility."""
    safe_title = _escape_xml(title)
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">'
        '<head>'
        '<meta charset="utf-8"/>'
        f'<title>{safe_title}</title>'
        f'<link rel="stylesheet" type="text/css" href="{css_href}"/>'
        '</head>'
        f'<body>{body_html}</body>'
        '</html>'
    )


def _is_treatise_title_page(div1):
    """
    Detect if a div1 is a decorative treatise title page.
    Pattern: short bold connector words (OR, OF, WITH, AS ALSO, AND, ON, IN)
    interspersed with italic description paragraphs.
    Three detection strategies:
      A) Classic: >=2 connectors among body paras, total body <2000 chars
      B) Leading connectors: the first few body paragraphs are ALL single
         connector words (common when title is in the heading)
      C) Heading connectors: the heading itself (from merged fragments)
         contains connector words separated by em-dashes
    """
    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )

    # Strategy C: Check heading for merged title fragments with connectors
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            heading_text = (h_elem.text or '') + ''.join(
                (c.text or '') + (c.tail or '') for c in h_elem
            )
            heading_text = heading_text.strip()
            # Split on em-dash or " — "
            parts = re.split(r'\s*[\u2014]\s*', heading_text)
            if len(parts) <= 1:
                parts = [p.strip() for p in heading_text.split(' — ') if p.strip()]
            heading_connectors = sum(
                1 for p in parts if connector_re.match(p.strip())
            )
            if heading_connectors >= 2:
                return True
            break

    paras = div1.findall('p')
    if not paras:
        # Even with no body paras, strategy C may have matched
        return False

    connectors = 0
    italics = 0
    total_body_text = 0
    leading_connectors = 0
    leading_done = False

    for p in paras:
        text = _elem_to_html(p).strip()
        plain = re.sub(r'<[^>]+>', '', text).strip()
        total_body_text += len(plain)

        is_connector = False
        # Check for bold connector
        if re.match(r'^<b>[^<]{1,20}</b>$', text):
            bold_text = re.sub(r'</?b>', '', text).strip()
            if connector_re.match(bold_text):
                connectors += 1
                is_connector = True
        # Also check for plain connector (not bold)
        elif connector_re.match(plain) and len(plain) < 15:
            connectors += 1
            is_connector = True
        # Check if all italic
        elif text.startswith('<i>') and '</i>' in text:
            italics += 1

        # Track leading connectors (first N paras all connectors)
        if not leading_done:
            if is_connector:
                leading_connectors += 1
            else:
                leading_done = True

    # Strategy A: Classic detection (short title page)
    if connectors >= 2 and total_body_text < 2000:
        return True

    # Strategy B: Leading connectors in first paragraphs
    if leading_connectors >= 2:
        return True

    return False


def _build_treatise_title(div1):
    """Build centered decorative HTML for a treatise title page."""
    connector_re = re.compile(
        r'^(?:OR,?|OF,?|ON,?|IN,?|WITH,?|AS\s+ALSO,?|AND,?|ALSO,?|WHEREIN,?|BEING,?)\s*$',
        re.IGNORECASE
    )

    parts = ['<div class="treatise-title">']

    # Get the heading text
    heading_text = ''
    heading_tag = 'h1'
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            heading_text = _elem_to_html(h_elem).strip()
            heading_tag = h_tag
            break

    # Split merged heading on em-dash to recover individual title lines
    heading_lines = [h.strip() for h in re.split(r'\s*\u2014\s*', heading_text) if h.strip()]
    # Also try legacy " — " (space-endash-space) separator
    if len(heading_lines) <= 1 and ' — ' in heading_text:
        heading_lines = [h.strip() for h in heading_text.split(' — ') if h.strip()]

    # Collect body paragraphs and separate connectors from descriptions
    body_paras = []
    body_connectors = []
    for p_elem in div1.findall('p'):
        html = _elem_to_html(p_elem)
        trimmed = html.strip()
        if not trimmed:
            continue
        plain = re.sub(r'<[^>]+>', '', trimmed).strip()

        # Check if it's a connector (bold or plain)
        is_conn = False
        if re.match(r'^<b>[^<]{1,20}</b>$', trimmed):
            bold_text = re.sub(r'</?b>', '', trimmed).strip()
            if connector_re.match(bold_text):
                body_connectors.append(bold_text)
                body_paras.append(('connector', bold_text))
                is_conn = True
        elif connector_re.match(plain) and len(plain) < 15:
            body_connectors.append(plain)
            body_paras.append(('connector', plain))
            is_conn = True

        if not is_conn:
            body_paras.append(('other', trimmed, plain))

    # Categorise each heading line as a connector or a title
    heading_titles = []      # (type, text) — 'title' or 'connector'
    for line in heading_lines:
        plain_line = re.sub(r'<[^>]+>', '', line).strip()
        if connector_re.match(plain_line) and len(plain_line) < 15:
            heading_titles.append(('connector', plain_line))
        else:
            heading_titles.append(('title', line))

    # Separate body connectors and non-connector body paragraphs
    body_conn_queue = [item[1] for item in body_paras if item[0] == 'connector']
    body_other = [item for item in body_paras if item[0] != 'connector']

    # Build the full interleaved sequence of titles and connectors.
    # Sources of connectors: heading lines that are connectors, or body
    # paragraph connectors.  We merge both into one ordered sequence,
    # interleaving body connectors BETWEEN heading titles when the heading
    # itself contains no connectors.
    heading_has_connectors = any(k == 'connector' for k, _ in heading_titles)

    if len(heading_lines) > 1:
        if heading_has_connectors:
            # Heading already contains connectors — render as-is
            first_title = True
            for kind, text in heading_titles:
                if kind == 'connector':
                    parts.append(
                        f'<p class="connector">{_escape_xml(text)}</p>'
                    )
                elif first_title:
                    parts.append(f'<h1>{_escape_xml(text)}</h1>')
                    first_title = False
                else:
                    parts.append(f'<h2>{_escape_xml(text)}</h2>')
            # Body connectors that duplicate heading connectors are skipped
            heading_conn_set = set(
                t.upper() for k, t in heading_titles if k == 'connector'
            )
        else:
            # No connectors in heading — interleave body connectors
            # Pattern: title1, conn1, title2, conn2, title3, ...
            conn_idx = 0
            first_title = True
            for kind, text in heading_titles:
                if first_title:
                    parts.append(f'<h1>{_escape_xml(text)}</h1>')
                    first_title = False
                else:
                    # Insert a body connector before this title if available
                    if conn_idx < len(body_conn_queue):
                        parts.append(
                            f'<p class="connector">'
                            f'{_escape_xml(body_conn_queue[conn_idx])}</p>'
                        )
                        conn_idx += 1
                    parts.append(f'<h2>{_escape_xml(text)}</h2>')
            # Any remaining body connectors go after the last heading
            while conn_idx < len(body_conn_queue):
                parts.append(
                    f'<p class="connector">'
                    f'{_escape_xml(body_conn_queue[conn_idx])}</p>'
                )
                conn_idx += 1
            heading_conn_set = set(c.upper() for c in body_conn_queue)
    else:
        parts.append(f'<{heading_tag}>{heading_text}</{heading_tag}>')
        heading_conn_set = set()

    # Remaining non-connector body paragraphs
    for item in body_other:
        # 'other' tuple: (type, trimmed_html, plain_text)
        trimmed = item[1]
        plain = item[2]

        # All-italic paragraph = subtitle/description
        if trimmed.startswith('<i>'):
            parts.append(f'<p class="desc">{trimmed}</p>')
            continue

        # Quote paragraph (starts with opening quote mark)
        if plain.startswith(('"', '\u201c', "'", '\u2018')):
            parts.append(f'<p class="epigraph">{trimmed}</p>')
            continue

        # Default: centered paragraph
        parts.append(f'<p>{trimmed}</p>')

    parts.append('</div>')
    return ''.join(parts)


def _build_footnotes_chapter(div1):
    """Build a properly numbered endnotes chapter with EPUB 3 semantics.

    Uses FT markers (FT1, FT2, ...) embedded in the ThML as <a class="fnmarker">
    elements to assign correct endnote IDs that align with inline f1, f2, ... refs.
    A single paragraph may contain multiple FT markers for short footnotes.
    Falls back to sequential numbering if no FT markers are found.
    """
    import xml.etree.ElementTree as ET

    # Build a linear stream of (marker_or_text) tokens from all paragraphs.
    # Each token is either ('marker', ft_num_str) or ('text', html_fragment).
    # We walk each paragraph's children to split on fnmarker boundaries.
    stream = []  # list of ('marker', num) or ('text', html)

    for p_elem in div1.findall('p'):
        # Walk the element tree and build segments split by fnmarker
        # elem.text, then for each child: child + child.tail
        if p_elem.text and p_elem.text.strip():
            stream.append(('text', _escape_xml(p_elem.text)))
        elif p_elem.text:
            stream.append(('text', p_elem.text))  # whitespace

        for child in p_elem:
            if child.tag == 'a' and child.get('class') == 'fnmarker':
                ft_num = child.get('data-fn', '')
                if ft_num:
                    stream.append(('marker', ft_num))
                # Include tail text after the marker
                if child.tail:
                    stream.append(('text', _escape_xml(child.tail)))
            else:
                # Regular child element — render to HTML
                if child.tag == 'a' and child.get('class') == 'fnref':
                    fn_num = child.text or ''
                    fn_href = child.get('href', '')
                    html = (f'<a epub:type="noteref" role="doc-noteref" '
                            f'href="{fn_href}" '
                            f'class="footnote-ref"><sup>{_escape_xml(fn_num)}</sup></a>')
                elif child.tag == 'span':
                    lang = child.get('lang', '')
                    cls = child.get('class', '')
                    style = child.get('style', '')
                    attrs = ''
                    if lang:
                        attrs += f' lang="{lang}"'
                    if cls:
                        attrs += f' class="{cls}"'
                    if style:
                        attrs += f' style="{style}"'
                    inner = _elem_to_html(child)
                    html = f'<span{attrs}>{inner}</span>'
                elif child.tag in ('i', 'b', 'em', 'strong'):
                    inner = _elem_to_html(child)
                    html = f'<{child.tag}>{inner}</{child.tag}>'
                else:
                    html = _elem_to_html(child)
                stream.append(('text', html))
                if child.tail:
                    stream.append(('text', _escape_xml(child.tail)))

    # Now group the stream into footnotes: each 'marker' starts a new footnote,
    # all 'text' tokens until the next marker belong to that footnote.
    footnotes = []  # list of (ft_number_int, combined_html)
    current_ft = None
    current_parts = []

    for token_type, token_val in stream:
        if token_type == 'marker':
            # Save previous footnote
            if current_ft is not None:
                combined = ''.join(current_parts).strip()
                if combined:
                    footnotes.append((int(current_ft), combined))
            current_ft = token_val
            current_parts = []
        else:
            if current_ft is not None:
                current_parts.append(token_val)

    # Don't forget the last footnote
    if current_ft is not None:
        combined = ''.join(current_parts).strip()
        if combined:
            footnotes.append((int(current_ft), combined))

    # If no FT markers were found, fall back to sequential numbering
    if not footnotes:
        raw_paras = []
        for p_elem in div1.findall('p'):
            p_html = _elem_to_html(p_elem)
            if not p_html.strip():
                continue
            raw_paras.append(p_html)
        footnotes = [(i, html) for i, html in enumerate(raw_paras, 1)]

    # Build the endnotes section
    body_parts = ['<section epub:type="endnotes" role="doc-endnotes">']
    body_parts.append('<h1>FOOTNOTES</h1>')

    for fn_num, fn_html in footnotes:
        body_parts.append(
            f'<aside epub:type="endnote" role="doc-endnote" id="fn{fn_num}">'
            f'<p class="footnote">'
            f'<a epub:type="noteref" href="#fn{fn_num}" class="fn-link">'
            f'<sup>{fn_num}</sup></a> {fn_html}</p>'
            f'</aside>'
        )

    body_parts.append('</section>')
    return ''.join(body_parts)


def _build_normal_chapter(div1):
    """Build standard chapter HTML."""
    body_parts = ['<section>']

    # Add heading (use first found heading tag)
    for h_tag in ('h1', 'h2', 'h3'):
        h_elem = div1.find(h_tag)
        if h_elem is not None:
            body_parts.append(
                f'<{h_tag}>{_elem_to_html(h_elem)}</{h_tag}>'
            )
            break

    # Add paragraphs
    para_count = 0
    for p_elem in div1.findall('p'):
        p_html = _elem_to_html(p_elem)
        if not p_html.strip():
            continue
        css_class = ' class="first"' if para_count == 0 else ''
        body_parts.append(f'<p{css_class}>{p_html}</p>')
        para_count += 1

    body_parts.append('</section>')
    return ''.join(body_parts)


def thml_to_epub(thml_path, epub_path, volume_num, cover_image=None, fonts_dir=None, portrait_image=None):
    """
    Convert ThML XML to EPUB 3.0 (Apple Books compatible).
    Returns True if successful, False otherwise.
    """
    print(f"  Parsing ThML XML...")

    try:
        tree = ET.parse(thml_path)
        root = tree.getroot()
    except Exception as e:
        print(f"  Error parsing ThML: {e}")
        return False

    # Extract metadata
    dc_title = root.find('.//DC.Title')
    dc_creator = root.find('.//DC.Creator')

    title = dc_title.text if dc_title is not None else f"The Works of John Owen, Vol. {volume_num}"
    author = dc_creator.text if dc_creator is not None else "John Owen"
    subtitle = VOLUME_SUBTITLES.get(volume_num, "")

    print(f"  Creating EPUB 3 structure...")

    # Create EPUB book
    book = epub.EpubBook()
    # Generate a stable UUID from the volume number
    import uuid
    vol_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, f'john-owen-works-bot-vol-{volume_num}')
    book.set_identifier(f'urn:uuid:{vol_uuid}')
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Apple Books metadata
    book.add_metadata('DC', 'publisher', 'Banner of Truth Trust')
    book.add_metadata('DC', 'subject', 'Theology')
    book.add_metadata('DC', 'subject', 'Puritanism')
    book.add_metadata('DC', 'description',
                       f'Volume {volume_num} of The Works of John Owen, '
                       f'edited by William H. Goold.')

    # Stylesheet
    style = epub.EpubItem(
        uid='main-css',
        file_name='style/main.css',
        media_type='text/css',
        content=EPUB_STYLESHEET.encode('utf-8')
    )
    book.add_item(style)

    # Cover image
    cover_item = None
    if cover_image and os.path.exists(cover_image):
        try:
            with open(cover_image, 'rb') as f:
                cover_data = f.read()
            ext = os.path.splitext(cover_image)[1].lower()
            book.set_cover(f'images/cover{ext}', cover_data)
            print(f"  Added cover image")
        except Exception as e:
            print(f"  Warning: Could not add cover: {e}")

    # ---- Portrait image ----
    portrait_item = None
    if portrait_image and os.path.exists(portrait_image):
        try:
            with open(portrait_image, 'rb') as f:
                portrait_data = f.read()
            ext = os.path.splitext(portrait_image)[1].lower()
            media_type = 'image/jpeg' if ext in ('.jpg', '.jpeg') else 'image/png'
            portrait_item = epub.EpubItem(
                uid='portrait-img',
                file_name=f'images/portrait{ext}',
                media_type=media_type,
                content=portrait_data
            )
            book.add_item(portrait_item)
            print(f"  Added portrait: {os.path.basename(portrait_image)}")
        except Exception as e:
            print(f"  Warning: Could not add portrait: {e}")

    # ---- Frontispiece (portrait on its own page) ----
    frontispiece_page = None
    if portrait_item:
        frontispiece_body = (
            '<div class="frontispiece">'
            f'<img src="{portrait_item.file_name}" alt="Portrait of John Owen"/>'
            '<p class="caption">John Owen (1616&#x2013;1683)</p>'
            '</div>'
        )
        frontispiece_page = epub.EpubHtml(
            title='Frontispiece', file_name='frontispiece.xhtml', lang='en'
        )
        frontispiece_page.set_content(
            _make_xhtml('Frontispiece', frontispiece_body).encode('utf-8')
        )
        frontispiece_page.add_item(style)
        book.add_item(frontispiece_page)

    # ---- Title page ----
    title_body = (
        '<div class="title-page">'
        '<p class="ornament">&#x2767;</p>'
        f'<h1>The Works of<br/>John Owen</h1>'
        '<hr class="rule"/>'
        f'<p class="subtitle">Volume {_escape_xml(str(volume_num))}</p>'
        f'<p class="subtitle">{_escape_xml(subtitle)}</p>'
        f'<p class="author"><span class="by">by</span>{_escape_xml(author)}</p>'
        '<p class="editor">Edited by William H. Goold</p>'
        '<p class="publisher">Banner of Truth Trust</p>'
        '</div>'
    )
    title_page = epub.EpubHtml(
        title='Title Page', file_name='title.xhtml', lang='en'
    )
    title_page.set_content(
        _make_xhtml('Title Page', title_body).encode('utf-8')
    )
    title_page.add_item(style)
    book.add_item(title_page)

    # ---- Content chapters from ThML ----
    print(f"  Converting chapters...")
    epub_chapters = []
    div1_elements = root.findall('.//div1')

    # First pass: find the footnotes chapter filename
    fn_chapter_file = None
    for div_idx, div1 in enumerate(div1_elements):
        ch_title = div1.get('title', '').strip().upper()
        ch_id = div1.get('id', f'ch{div_idx + 1:03d}')
        if ch_title == 'FOOTNOTES':
            fn_chapter_file = f'{ch_id}.xhtml'
            break

    for div_idx, div1 in enumerate(div1_elements):
        chapter_title = div1.get('title', f'Chapter {div_idx + 1}')
        chapter_id = div1.get('id', f'ch{div_idx + 1:03d}')

        # Check chapter type and build appropriate HTML
        is_footnotes = chapter_title.strip().upper() == 'FOOTNOTES'
        is_treatise_title = (not is_footnotes) and _is_treatise_title_page(div1)

        if is_footnotes:
            body_html = _build_footnotes_chapter(div1)
        elif is_treatise_title:
            body_html = _build_treatise_title(div1)
        else:
            body_html = _build_normal_chapter(div1)

        # Fix footnote ref hrefs to point to the footnotes chapter file
        if fn_chapter_file and not is_footnotes:
            body_html = body_html.replace(
                'href="#fn', f'href="{fn_chapter_file}#fn'
            )

        ch_item = epub.EpubHtml(
            title=chapter_title[:200],
            file_name=f'{chapter_id}.xhtml',
            lang='en'
        )
        ch_item.set_content(
            _make_xhtml(chapter_title, body_html).encode('utf-8')
        )
        ch_item.add_item(style)
        book.add_item(ch_item)
        epub_chapters.append((ch_item, chapter_title))

    print(f"  {len(epub_chapters)} chapters created")

    # ---- Table of contents ----
    # Build hierarchical TOC: major sections (h1/h2) as top-level,
    # sub-chapters nested underneath
    toc_entries = []
    for ch_item, ch_title in epub_chapters:
        toc_entries.append(ch_item)

    book.toc = [title_page] + toc_entries

    # Navigation documents (both NCX for backwards compat and Nav for EPUB 3)
    book.add_item(epub.EpubNcx())
    nav = epub.EpubNav()
    nav.add_item(style)
    book.add_item(nav)

    # Spine: reading order (frontispiece before title page if present)
    front_pages = []
    if frontispiece_page:
        front_pages.append(frontispiece_page)
    front_pages.append(title_page)
    spine_items = ['nav'] + front_pages + [ch[0] for ch in epub_chapters]
    book.spine = spine_items

    # ---- Write EPUB ----
    print(f"  Writing EPUB file...")
    try:
        epub.write_epub(epub_path, book, {})
        file_size = os.path.getsize(epub_path)
        print(f"  Saved EPUB: {epub_path} ({file_size / 1024:.0f} KB)")
        return True
    except Exception as e:
        print(f"  Error writing EPUB: {e}")
        import traceback
        traceback.print_exc()
        return False


def _elem_to_html(elem):
    """Convert XML element to HTML string, handling nested tags recursively."""
    html_parts = []

    # Opening tag text — must escape to prevent stray HTML tags
    if elem.text:
        html_parts.append(_escape_xml(elem.text))

    # Process child elements
    for child in elem:
        if child.tag == 'span':
            lang = child.get('lang', '')
            cls = child.get('class', '')
            style = child.get('style', '')
            attrs = ''
            if lang:
                attrs += f' lang="{lang}"'
            if cls:
                attrs += f' class="{cls}"'
            if style:
                attrs += f' style="{style}"'
            inner = _elem_to_html(child)
            html_parts.append(f'<span{attrs}>{inner}</span>')
        elif child.tag == 'a' and child.get('class') == 'fnref':
            fn_num = child.text or ''
            fn_href = child.get('href', '')
            html_parts.append(
                f'<a epub:type="noteref" role="doc-noteref" '
                f'href="{fn_href}" '
                f'class="footnote-ref"><sup>{_escape_xml(fn_num)}</sup></a>'
            )
        elif child.tag == 'a' and child.get('class') == 'fnmarker':
            # FT marker — skip in HTML output (used only for ID assignment)
            pass
        elif child.tag in ('i', 'b', 'em', 'strong'):
            inner = _elem_to_html(child)
            html_parts.append(f'<{child.tag}>{inner}</{child.tag}>')
        else:
            inner = _elem_to_html(child)
            html_parts.append(inner)

        if child.tail:
            html_parts.append(_escape_xml(child.tail))

    return ''.join(html_parts)


# ============================================================================
# FILE DISCOVERY AND UTILITY FUNCTIONS
# ============================================================================

def extract_volume_number(filename):
    """Extract volume number from PDF filename."""
    # Try pattern: vol_1, vol 1, vol1
    match = re.search(r'vol[_\s]*(\d{1,2})', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try pattern: -v1-, _v1_, v1_
    match = re.search(r'[-_]v(\d{1,2})[-_.]', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try pattern: just a number
    match = re.search(r'(\d{1,2})', filename)
    if match:
        num = int(match.group(1))
        if 1 <= num <= 16:
            return num

    return None


def find_portrait(work_dir, volume_num):
    """Find a portrait image for a volume, selected pseudo-randomly by volume number."""
    import random
    # Check common portrait directory names
    for dirname in ['portraits', 'portrait']:
        portraits_dir = os.path.join(work_dir, dirname)
        if os.path.isdir(portraits_dir):
            portraits = [
                os.path.join(portraits_dir, f)
                for f in os.listdir(portraits_dir)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))
            ]
            if portraits:
                portraits.sort()  # Stable ordering
                # Use volume number as seed for reproducible "random" selection
                rng = random.Random(volume_num)
                return rng.choice(portraits)
    return None


def find_cover(work_dir, volume_num):
    """Find cover image for a volume."""
    covers_dir = os.path.join(work_dir, 'covers')
    if not os.path.isdir(covers_dir):
        return None

    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        cover_path = os.path.join(covers_dir, f'v{volume_num}{ext}')
        if os.path.exists(cover_path):
            return cover_path

    return None


def find_fonts_dir(work_dir):
    """Find fonts directory."""
    fonts_candidates = [
        os.path.join(work_dir, 'fonts'),
        os.path.expanduser('~/Library/Fonts'),
        '/Library/Fonts',
        '/usr/share/fonts',
    ]

    for fonts_dir in fonts_candidates:
        if os.path.isdir(fonts_dir):
            return fonts_dir

    return None


def discover_pdfs(work_dir):
    """Discover PDF files in work directory."""
    pdfs = []

    for file in os.listdir(work_dir):
        if not file.lower().endswith('.pdf'):
            continue

        # Skip if it's the collected works
        if 'works_of_john_owen' in file.lower():
            continue

        pdf_path = os.path.join(work_dir, file)
        volume_num = extract_volume_number(file)

        if volume_num and 1 <= volume_num <= 16:
            pdfs.append((volume_num, pdf_path, file))

    return sorted(pdfs, key=lambda x: x[0])


# ============================================================================
# MAIN CONVERSION PIPELINE
# ============================================================================

def process_volume(pdf_path, work_dir, volume_num, force=False, assets_dir=None):
    """
    Process a single PDF volume.
    work_dir: where to write ThML/EPUB outputs
    assets_dir: where to find covers/fonts (defaults to work_dir)
    Returns (success, thml_path, epub_path)
    """
    if assets_dir is None:
        assets_dir = work_dir

    basename = os.path.basename(pdf_path)
    print(f"\nProcessing Volume {volume_num}: {basename}")

    # Output paths
    thml_path = os.path.join(work_dir, f'volume_{volume_num}.thml.xml')
    epub_path = os.path.join(work_dir, f'volume_{volume_num}.epub')

    # Check if already processed
    if not force and os.path.exists(thml_path) and os.path.exists(epub_path):
        print(f"  Skipping (already processed, use --force to rebuild)")
        return True, thml_path, epub_path

    # Stage 1: PDF → ThML XML
    print(f"STAGE 1: PDF \u2192 ThML XML")
    if not pdf_to_thml(pdf_path, thml_path, volume_num):
        return False, None, None

    # Stage 2: ThML XML → EPUB
    print(f"STAGE 2: ThML XML \u2192 EPUB")
    cover_image = find_cover(assets_dir, volume_num)
    fonts_dir = find_fonts_dir(assets_dir)
    portrait_image = find_portrait(assets_dir, volume_num)

    if not thml_to_epub(thml_path, epub_path, volume_num, cover_image, fonts_dir, portrait_image):
        return False, thml_path, None

    return True, thml_path, epub_path


def main():
    """Main entry point."""
    import argparse as _ap
    parser = _ap.ArgumentParser(description="John Owen PDF → EPUB Converter")
    parser.add_argument('work_dir', nargs='?', default=os.getcwd(),
                        help='Directory containing PDFs (default: cwd)')
    parser.add_argument('--output-dir', '-o', default=None,
                        help='Separate output directory for ThML/EPUB files')
    parser.add_argument('--volumes', type=str, default=None,
                        help='Comma-separated volume numbers to process')
    parser.add_argument('--force', action='store_true',
                        help='Force regeneration even if outputs exist')
    args = parser.parse_args()

    work_dir = os.path.abspath(args.work_dir)
    out_dir = os.path.abspath(args.output_dir) if args.output_dir else work_dir

    print(f"John Owen's Works PDF → EPUB Converter")
    print(f"Working directory: {work_dir}")
    if out_dir != work_dir:
        print(f"Output directory: {out_dir}")
        os.makedirs(out_dir, exist_ok=True)
    print()

    if not os.path.isdir(work_dir):
        print(f"Error: Directory not found: {work_dir}")
        sys.exit(1)

    # Parse --volumes filter
    vol_filter = None
    if args.volumes:
        vol_filter = set(int(v.strip()) for v in args.volumes.split(','))

    # Discover PDFs
    print(f"Discovering PDFs...")
    pdfs = discover_pdfs(work_dir)

    if not pdfs:
        print(f"No suitable PDF files found in {work_dir}")
        sys.exit(1)

    if vol_filter:
        pdfs = [(v, p, f) for v, p, f in pdfs if v in vol_filter]

    print(f"Found {len(pdfs)} PDF(s):\n")
    for vol_num, pdf_path, filename in pdfs:
        print(f"  Vol {vol_num}: {filename}")

    # Process each volume
    print(f"\n{'=' * 70}")
    results = []

    for vol_num, pdf_path, filename in pdfs:
        success, thml_path, epub_path = process_volume(
            pdf_path,
            out_dir,
            vol_num,
            force=args.force,
            assets_dir=work_dir
        )
        results.append((vol_num, success, thml_path, epub_path))

    # Summary
    print(f"\n{'=' * 70}")
    print(f"SUMMARY\n")

    succeeded = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]

    print(f"Succeeded: {len(succeeded)}/{len(results)}")
    for vol_num, _, thml_path, epub_path in succeeded:
        print(f"  Vol {vol_num}:")
        print(f"    ThML: {thml_path}")
        print(f"    EPUB: {epub_path}")

    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for vol_num, _, _, _ in failed:
            print(f"  Vol {vol_num}")

    print(f"\n{'=' * 70}")


if __name__ == '__main__':
    main()
