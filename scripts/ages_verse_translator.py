import re

# ================================================================
# AGES VERSE MARKER TRANSLATION
# ================================================================

# AGES Software encodes Bible references as <BBCCVV> or <BBBCCVV> where
# BB/BBB = book code (1-based), CC = chapter (zero-padded), VV = verse.
_AGES_BOOK_NAMES = {
    1: 'Genesis', 2: 'Exodus', 3: 'Leviticus', 4: 'Numbers',
    5: 'Deuteronomy', 6: 'Joshua', 7: 'Judges', 8: 'Ruth',
    9: '1 Samuel', 10: '2 Samuel', 11: '1 Kings', 12: '2 Kings',
    13: '1 Chronicles', 14: '2 Chronicles', 15: 'Ezra', 16: 'Nehemiah',
    17: 'Esther', 18: 'Job', 19: 'Psalms', 20: 'Proverbs',
    21: 'Ecclesiastes', 22: 'Song of Solomon', 23: 'Isaiah', 24: 'Jeremiah',
    25: 'Lamentations', 26: 'Ezekiel', 27: 'Daniel', 28: 'Hosea',
    29: 'Joel', 30: 'Amos', 31: 'Obadiah', 32: 'Jonah', 33: 'Micah',
    34: 'Nahum', 35: 'Habakkuk', 36: 'Zephaniah', 37: 'Haggai',
    38: 'Zechariah', 39: 'Malachi',
    40: 'Matthew', 41: 'Mark', 42: 'Luke', 43: 'John', 44: 'Acts',
    45: 'Romans', 46: '1 Corinthians', 47: '2 Corinthians', 48: 'Galatians',
    49: 'Ephesians', 50: 'Philippians', 51: 'Colossians',
    52: '1 Thessalonians', 53: '2 Thessalonians',
    54: '1 Timothy', 55: '2 Timothy', 56: 'Titus', 57: 'Philemon',
    58: 'Hebrews', 59: 'James', 60: '1 Peter', 61: '2 Peter',
    62: '1 John', 63: '2 John', 64: '3 John', 65: 'Jude', 66: 'Revelation',
}

# Matches standard decimal AGES codes (6-9 digits) AND the Psalms hex-chapter
# variant where chapters 100-159 are encoded with a hex letter at position 2:
#   <19A225> = Psalms 102:25  (A=10 → ch = 10*10+2 = 102, v = 25)
#   <19B822> = Psalms 118:22  (B=11 → ch = 11*10+8 = 118, v = 22)
#   <19D504> = Psalms 135:4   (D=13 → ch = 13*10+5 = 135, v = 4)
# The hex letter appears only at position 2 of the code (after the 2-digit book).
_AGES_MARKER_RE = re.compile(r'<(\d{2}[0-9A-Fa-f]\d{3,6})>')

# Context-aware pattern: captures the code AND any immediately-following
# book+chapter:verse text so we can detect when the PDF already has the
# human-readable form right after the numeric code (both layers present).
# Group 1 = code (may include a hex letter), Group 2 = optional following ref text.
_AGES_MARKER_CONTEXT_RE = re.compile(
    r'<(\d{2}[0-9A-Fa-f]\d{3,6})>(\s*(?:[1-3]?\s*[A-Z][a-zA-Z ]{1,30}?\s+)?\d+:\d+(?:[-,]\s*\d+)*)?'
)

# Hex-letter → century value for the Psalms chapter encoding.
_HEX_CHAPTER_MAP = {
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15,
}


def _translate_ages_marker(code_str: str) -> str:
    """Translate an AGES verse code to a readable Bible reference.

    Standard format: BBCCVV (6 digits) or BBBCCVV (7 digits) where
      BB/BBB = book number (decimal), CC = chapter, VV = verse.

    Psalms hex-chapter variant: 19XDVV where X is a hex letter A-F
      encoding the hundreds-of-chapter digit:
        19A225 → Psalms 102:25  (A=10, ch = 10*10+2 = 102)
        19B822 → Psalms 118:22  (B=11, ch = 11*10+8 = 118)
        19D504 → Psalms 135:4   (D=13, ch = 13*10+5 = 135)

    Example: 430316 → John 3:16  (43 = John, 03 = ch 3, 16 = v 16)
    Example: 1842077 → Job 42:7  (18 = Job, 42 = ch 42, 07 = v 7)
    """
    if not code_str:
        return f'[{code_str}]'

    # Detect Psalms hex-chapter encoding: 2 decimal digits + 1 hex letter + 3 digits
    # e.g. "19B822" — positions: [0:2]=book, [2]=hex_letter, [3]=ch_units, [4:6]=verse
    if len(code_str) == 6 and code_str[2].upper() in _HEX_CHAPTER_MAP:
        try:
            book_n = int(code_str[:2])
            hex_val = _HEX_CHAPTER_MAP[code_str[2]]
            ch_n = hex_val * 10 + int(code_str[3])
            v_n = int(code_str[4:6])
            book_name = _AGES_BOOK_NAMES.get(book_n)
            if book_name:
                if ch_n == 0 and v_n == 0:
                    return book_name
                if v_n == 0:
                    return f'{book_name} {ch_n}'
                return f'{book_name} {ch_n}:{v_n}'
        except (ValueError, IndexError):
            pass
        return f'[{code_str}]'

    # Standard all-decimal path
    s = code_str.lstrip('0')
    if not s:
        return f'[{code_str}]'

    try:
        # All-decimal format: BBCCVV (6 digits) or BBBCCVV (7+ digits).
        # Both forms share the same slice arithmetic: last 2 digits = verse,
        # next 2 = chapter, remainder = book.
        book_n = int(code_str[:-4])
        ch_n = int(code_str[-4:-2])
        v_n = int(code_str[-2:])
        # Correct AGES database corruption for Philippians chapter 2:
        # Chapter is incorrectly stored as 3 * Verse - 1.
        if book_n == 50 and ch_n > 4 and ch_n == 3 * v_n - 1:
            ch_n = 2
    except ValueError:
        return f'[{code_str}]'

    book_name = _AGES_BOOK_NAMES.get(book_n)
    if not book_name:
        # Unknown book code — preserve escaped form so audit catches it
        return f'[{code_str}]'
    if ch_n == 0 and v_n == 0:
        return book_name
    if v_n == 0:
        return f'{book_name} {ch_n}'
    return f'{book_name} {ch_n}:{v_n}'


def translate_ages_verse_markers(text: str) -> str:
    """Replace all AGES verse marker codes with readable Bible references.

    <430316> → John 3:16
    Unknown codes are preserved as [NNNNNN] so the audit can flag them.

    Context-aware: AGES PDFs sometimes encode a reference as both a numeric
    code AND the already-decoded human-readable text immediately following it
    (two layers in the same PDF text stream). When the following text starts
    with the same reference as the translated code — possibly with a richer
    verse range like "1 Peter 2:6-8" vs bare "1 Peter 2:6" — the code is
    suppressed and only the already-present text is kept, preventing doubling
    such as "Isaiah 9:6Isaiah 9:6".
    """
    def _norm_for_cmp(s: str) -> str:
        """Normalise a reference string for dedup comparison.

        Collapses whitespace, lowercases, and strips a trailing 's' from the
        book name so that 'Psalm'/'Psalms' and 'Samuel'/'Samuels' etc. compare
        equal regardless of which form the PDF uses.
        """
        s = re.sub(r'\s+', ' ', s).lower().strip()
        # Strip trailing 's' from the book-name portion (before the chapter number)
        s = re.sub(r's\b(?=\s+\d)', '', s, count=1)
        return s

    def _repl(m: re.Match) -> str:
        code = m.group(1)
        following = m.group(2) or ''
        translated = _translate_ages_marker(code)
        
        # Check if 'chap.' or 'chapter' precedes the match in the full text
        # by looking at the characters before m.start()
        start_idx = m.start()
        # Look back for book name to avoid doubling (Issue 108/Audit)
        preceding_full = text[max(0, start_idx-60):start_idx].lower()
        has_chap_prefix = bool(re.search(r'\b(?:chap|chapter)\.?\s*$', preceding_full))
        
        # Extract book name from translation for comparison
        book_match = re.match(r'([1-3]?\s*[A-Z][a-zA-Z ]{1,30}?)[\s,;.]+\d', translated)
        book_name = book_match.group(1).strip() if book_match else ''
        book_norm = _norm_for_cmp(book_name) if book_name else ''
        
        # If the book name already appears right before the marker, don't prepend it
        # Handle cases like "Romans 8:29 <450829>" (Issue 108/Audit)
        already_has_book = book_norm and (book_norm in preceding_full)

        if following:
            norm_following = _norm_for_cmp(following)

            # If following already starts with the book name, it's a duplicate (Issue 108/Audit)
            if book_norm and book_norm in norm_following:
                return following

            norm_translated = _norm_for_cmp(translated)            
            # Match the first reference coordinate in the following text
            # Allow optional punctuation after book name (Issue 108/Audit)
            match = re.match(r'((?:[1-3]?\s*[a-z][a-z ]{1,30}?)[,;.]?\s+)?(\d+:\d+|\d+)', norm_following)
            if match:
                base_following = match.group(0).strip()
                
                # Check for internal repetition in the following layer (Issue 26)
                # e.g. "16:1516:15" or "John 16:15John 16:15"
                if len(norm_following) >= 10:
                    half = len(norm_following) // 2
                    if norm_following[:half] == norm_following[half:]:
                        following = following[:half]
                        norm_following = norm_following[:half]
                        match = re.match(r'((?:[1-3]?\s*[a-z][a-z ]{1,30}?)[,;.]?\s+)?(\d+:\d+|\d+)', norm_following)
                        if match:
                             base_following = match.group(0).strip()

                if norm_translated.startswith(base_following) or norm_translated.endswith(base_following):
                    # It's a duplicate. We keep the `following` text.
                    # If the following text didn't have a book name, prepend the book name from the translation
                    # ONLY IF 'chap.' wasn't already there.
                    if not match.group(1) and not has_chap_prefix and not already_has_book:
                        if book_name:
                            return book_name + ' ' + following
                    return following
        # If the book name already appears right before the marker, don't prepend it
        if already_has_book:
            # Extract just the chapter:verse from translated
            coord_match = re.search(r'\d+:\d+', translated)
            if coord_match:
                coord = coord_match.group(0)
                # If following already starts with the coordinate, it's a duplicate (Issue 108/Audit)
                # e.g. "Romans 8:29 <450829>8:29, 30" -> "Romans 8:29, 30"
                follow_strip = following.lstrip()
                if follow_strip.startswith(coord):
                    return follow_strip[len(coord):]
                if follow_strip.startswith(',' + coord):
                    return follow_strip[len(coord)+1:]
                if follow_strip.startswith(';' + coord):
                    return follow_strip[len(coord)+1:]
                
                # Return only the coordinate if book name is already present
                return coord_match.group(0) + following
            # If no coordinate match, but book is already there, return following as is
            return following

        return translated + following

    return _AGES_MARKER_CONTEXT_RE.sub(_repl, text)
def _has_repeated_ages_marker_cluster(text):
    """Return True when PyMuPDF4LLM duplicated nearby AGES verse-marker runs."""
    if not text:
        return False
    markers = [(m.group(1), m.start()) for m in _AGES_MARKER_RE.finditer(text)]
    if len(markers) < 4:
        return False

    positions_by_code = {}
    for code, pos in markers:
        positions_by_code.setdefault(code, []).append(pos)

    repeated_pairs = []
    for code, positions in positions_by_code.items():
        if len(positions) < 2:
            continue
        for i, first in enumerate(positions[:-1]):
            for second in positions[i + 1:]:
                if 0 < second - first <= 900:
                    repeated_pairs.append((first, second, code))
                    break

    if len(repeated_pairs) < 2:
        return False

    repeated_pairs.sort()
    for idx, (first_a, second_a, _) in enumerate(repeated_pairs[:-1]):
        for first_b, second_b, _ in repeated_pairs[idx + 1:]:
            if abs(first_b - first_a) <= 300 or abs(second_b - second_a) <= 300:
                return True
    return False
