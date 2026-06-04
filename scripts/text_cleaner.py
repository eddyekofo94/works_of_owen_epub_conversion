import re
from shared import (
    convert_greek_word, clean_greek_text, convert_gideon_hebrew,
    normalize_characters,
    is_greek_font, is_hebrew_font, contains_greek, contains_hebrew,
    SCRIPTURE_BOOK_RE, SCRIPTURE_REF_RE, SCRIPTURE_CONTINUATION_TRAIL_RE,
    FOOTNOTE_MARKER_RE, LOOSE_FOOTNOTE_MARKER_RE, FOOTNOTE_PLACEHOLDER_RE,
    FT_MARKER_RE, EMPTY_BRACKET_RE,
    STRUCTURAL_START_RE, CITATION_ABBREV_TRAIL_RE,
    CITATION_ABBREV_START_RE, CITATION_AUTHOR_TRAIL_RE,
    MARKDOWN_STRUCTURAL_START_RE, ROMAN_LIST_TOKEN, PLAIN_CHAPTER_RE,
    INLINE_STRUCTURAL_MARKER_RE, ROMAN_HEADING_RE, ROMAN_ONLY_RE,
    _is_scripture_ref_fragment, _scripture_ref_tokens,
    _split_inline_structural_markers,
    _trim_duplicate_reference_prefix, _norm_for_dedupe,
    _normalize_spaced_caps, _normalize_i_will, _repair_owen_ocr_errors,
)
from scripts.pdf_coordinates import (
    _merge_adjacent_blockquote_paragraphs,
    _split_leading_scripture_reference_tail,
    _paragraph_expects_scripture_reference_tail,
    CONNECTOR_STARTERS_RE,
    SCRIPTURE_TAIL_RE,
    DANGLING_CONNECTOR_RE,
    _repair_glued_scripture_book_references,
)
from scripts.ages_verse_translator import translate_ages_verse_markers
from scripts.footnote_extractor import _normalize_extracted_footnote_markers
from scripts.greek_hebrew_dedupe import _remove_adjacent_duplicates, _remove_adjacent_line_overlaps
from scripts.markdown_skeleton import get_merged_page_text

OWEN_HARD_HYPHENS = {
    'Spiritual-mindedness', 'spiritually-minded', 'heavenly-mindedness',
    'self-denial', 'faith-fulness', 'church-state', 'fellow-creature',
    'well-pleased', 'good-will', 'soul-satisfying'
}

def strip_false_ocr_bolds(text):
    """Strip false OCR bold markers (**word**) that are not structural list or heading elements."""
    if not text:
        return text

    def replace_bold(match):
        full_match = match.group(0)
        content = match.group(1)
        clean_content = content.strip()

        # Preserve structural list markers: e.g. "1.", "(1)", "[1]", "I.", "Q.", "Ans.", "First.", "1stly", "[1st.]"
        # Handles optional brackets or parentheses around digit/ordinal/Roman/Letter
        if re.match(
            r'^[\(\[]?(?:(?!\d{4}\.)\d{1,4}(?:st|nd|rd|th)?(?:ly|dly)?|[IVXLCDM]+|[A-Z])\.?[\)\]]?$',
            clean_content,
            re.I
        ):
            return full_match
        if re.match(r'^(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?$', clean_content, re.I):
            return full_match
        if re.match(r'^(?:First|Secondly|Thirdly|Fourthly|Fifthly|Lastly)\.?$', clean_content, re.I):
            return full_match

        # Otherwise, if it is a random word or phrase in the text, it is likely false OCR bold.
        return content

    # Use re.sub with a non-greedy match for **content**
    return re.sub(r'\*\*(?!\*)([^\n*]+?)\*\*', replace_bold, text)


def _is_terminal(text):
    """Check if the text ends in a terminal punctuation, excluding abbreviations."""
    if not text:
        return False
    text_clean = text.strip()
    if not re.search(r'[.!?]"?\s*$', text_clean):
        return False
    # If it ends with a citation abbreviation, it's not a true terminal period
    if CITATION_ABBREV_TRAIL_RE.search(text_clean):
        return False
    # Also check other common theological/patristic/Bible abbreviations
    abbrevs = (
        r'\b(?:Dr|Mr|Mrs|St|viz|i\.e|e\.g|[A-Z])\.\s*$'
        r'|'
        # Bible books
        r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kings|Chron|Ezra|Neh|Esth|Job|Ps|Prov|Eccl|Cant|'
        r'Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|'
        r'Matt|Mk|Lk|Jn|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Pet|Jude|Rev)\.\s*$'
        r'|'
        # Patristic / Scholastic authors
        r'\b(?:Aug|August|Austin|Chrys|Chrysost|Hierom|Jerome|Clem|Clement|Tertull|Orig|Origen|Cyp|Cyprian|'
        r'Euseb|Athan|Athanas|Basil|Naz|Nazianz|Nyss|Ambr|Ambrose|Theod|Theodoret|Cyril|Hilar|Hilary|Leo|Bern|'
        r'Bernard|Bell|Bellar|Soc|Socin|Faust|Faustus|Calv|Calvin|Epiph|Epiphan|Greg|Gregory|Plut|Cic|Sen|Tac|'
        r'Plin|Arist|Plat|Justin|Iren|Alex|Alexand|Mart)\.\s*$'
    )
    if re.search(abbrevs, text_clean, re.I):
        return False
    return True


def clean_text(text, config=None):
    """Sanitize extracted text before paragraph reconstruction."""
    if not text:
        return ''

    # 0. Character normalization (Issue: Gideon/AGES legacy encoding)
    text = normalize_characters(text)

    # 0a. Owen-specific OCR repairs (Issue 75/108)
    text = _repair_owen_ocr_errors(text, config=config)
    text = _normalize_extracted_footnote_markers(text)
    # Normalize loose bracketed footnote letters: [ a] or [ a[ -> [a]
    text = re.sub(r'\[\s*([a-z])\s*[\]\[]', r'[\1]', text, flags=re.I)

    # 0b. Normalize spaced-caps OCR and I WILL / I AM mangles
    text = _normalize_spaced_caps(text)
    text = _normalize_i_will(text)
    
    # 0c. Scripture range OCR repairs (Issue 108)
    # Handles "7 ( 8)" -> "7, 8" misreads
    text = re.sub(r'(\d)\s+\(\s*(\d+)\s*\)', r'\1, \2', text)
    text = _normalize_scholarly_citation_artifacts(text)

    # 1. Translate AGES scripture reference codes to readable citations.
    #    <430316> → John 3:16. Must run BEFORE EMPTY_BRACKET_RE so we don't
    #    clobber the translated output.
    text = translate_ages_verse_markers(text)
    text = _repair_glued_scripture_book_references(text)
    text = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', text, flags=re.I)
    # General enough for "( John" while avoiding global "** Text" corruption.
    text = re.sub(r'\(\s+([A-Z])', r'(\1', text)
    text = EMPTY_BRACKET_RE.sub('', text)
    # 2. Remove AGES running headers (whole-line removal)
    text = re.sub(
        r'^.*(?:THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|'
        r'BOOKS FOR THE AGES|AGES SOFTWARE|VERSION \d\.\d|'
        r'VOLUME \d+|JOHN OWEN COLLECTION|Books For The Ages).*$',
        '', text, flags=re.MULTILINE | re.IGNORECASE
    )
    # 3. Collapse multiple spaces → single space
    text = re.sub(r' {2,}', ' ', text)
    # Normalize Q/A labels that are clearly structural (Issue 26)
    # Strictly case-sensitive and anchored to start of line to avoid corrupting prose
    text = re.sub(r'\bAns\s+\.\s+(\d+)\b\.?', r'Ans. \1.', text)
    text = re.sub(r'(?m)^([QA])\s*[\., ]+\s*(\d+)\s*\.?', r'\1. \2.', text)
    text = re.sub(r'(?m)^([QA])\s*[\., ]+\s*', r'\1. ', text)
    text = re.sub(r'(?m)^(A)\s*\.\s*,\s*', r'\1. ', text) # A. , -> A.
    
    # Fix ordinal spacing: "1st ." -> "1st.", "**1st** ." -> "**1st**.", "2ndly ," -> "2ndly,"
    # Handles both plain and bold-wrapped ordinals, including adverbial forms
    text = re.sub(
        r'(\*\*)?(\d+(?:(?:st|nd|rd|th)ly|dly|ly|st|nd|rd|th))(\*\*)?\s+([,.;])',
        r'\1\2\3\4',
        text
    )
    
    # 4. Strip leading/trailing whitespace per line
    text = '\n'.join(line.strip() for line in text.split('\n'))
    
    # 4a. Ensure space between Greek/Hebrew and English (Issue 108/Audit)
    # Handles cases like “ἰσάγγελοι”like -> “ἰσάγγελοι” like
    # Includes common trailing punctuation/quotes in the junction check
    text = re.sub(r'([\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF][”"’)]?)([A-Za-z])', r'\1 \2', text)
    text = re.sub(r'([A-Za-z])([“"‘(]?[\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF])', r'\1 \2', text)

    # 4b. Aggressive remove leading Latin artifact noise before Greek (Issue: j jEgw)
    # Standalone 'j' or 'J' followed by space or before Greek is noise.
    text = re.sub(r'(?i)\b[jJ]\s+', '', text)
    text = re.sub(r'(?i)\b[jJ](?=[\u0370-\u03FF\u1F00-\u1FFF])', '', text)
    
    # 5. Remove adjacent ghost-layer duplicates and repeated line tails
    text = _remove_adjacent_duplicates(text)
    text = _remove_adjacent_line_overlaps(text)
    text = strip_false_ocr_bolds(text)
    return clean_greek_text(text.strip())


def _normalize_scholarly_citation_artifacts(text):
    """Repair OCR punctuation that breaks patristic/scholastic citations.

    AGES extraction sometimes turns citation abbreviations into forms like
    "cap., 8" or splits "Chapter, 8." across lines. Those commas make the
    paragraph healer treat the following number as a list item instead of a
    citation continuation.
    """
    if not text:
        return text

    # "cap., 8" / "q. , 81" -> "cap. 8" / "q. 81"
    text = re.sub(
        r'\b(?P<label>cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|'
        r'dial|enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\s*\.\s*,\s*(?=\d)',
        lambda m: f'{m.group("label")}. ',
        text,
        flags=re.I,
    )

    # "Chapter,\n8." / "Chap., 8." -> "Chapter 8." / "Chap. 8."
    text = re.sub(
        r'\b(?P<label>chapter|chap)\s*(?:\.\s*)?,\s*(?=\d)',
        lambda m: f'{m.group("label")} ' if m.group("label").lower() == 'chapter' else f'{m.group("label")}. ',
        text,
        flags=re.I,
    )

    return text


# Short introductory connectors that should be merged with previous text (Issue 1)
SEMANTIC_CONNECTOR_RE = re.compile(
    r'^(?:For|As|Wherefore|And|Or|Yea|Yet|So|Thus|Hence|Moreover)\s*[,;—\-]\s*$',
    re.I
)

# Terms where a hyphen at EOL should be preserved (Issue 1)


def reconstruct_paragraphs(text):
    """Heal broken lines into proper, reflowable paragraphs."""
    if not text:
        return []

    lines = text.split('\n')
    paragraphs = []
    current = []
    _bracket_continuation = False  # Issue 8: flag when last structural token has unbalanced [

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Issue 8: if previous structural token had unclosed bracket, join this line to it
        if _bracket_continuation and stripped:
            _bracket_continuation = False
            if paragraphs:
                paragraphs[-1] = paragraphs[-1] + ' ' + stripped
            continue

        if not stripped:
            if current:
                prev = current[-1]
                ends_terminal = _is_terminal(prev)
                # Look ahead: if next non-empty line starts with connector, don't break
                next_nonempty = None
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        next_nonempty = lines[j].strip()
                        break
                
                starts_with_connector = (
                    next_nonempty is not None and
                    bool(CONNECTOR_STARTERS_RE.match(next_nonempty))
                )
                starts_with_scripture = (
                    next_nonempty is not None and
                    bool(re.match(rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b', next_nonempty, re.I))
                )
                starts_with_bare_ref = (
                    next_nonempty is not None and
                    bool(re.match(r'^\d+:\d+', next_nonempty))
                )
                
                # Issue 108/Blemish 8: Reference continuation awareness across blank lines
                ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
                prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
                next_starts_with_ref_number = next_nonempty and bool(re.match(r'^\d{1,4}\b', next_nonempty))
                
                if ends_terminal and not starts_with_connector:
                    if starts_with_scripture or starts_with_bare_ref:
                        continue
                    if prev_is_ref_abbrev and next_starts_with_ref_number:
                        # Reference continuation (p.\n\n280) -> join
                        continue
                    paragraphs.append(' '.join(current))
                    current = []
            continue

        # Preserve heading markers and structural tokens as standalone paragraphs
        is_structural_token = stripped.startswith('[[') and ']]' in stripped
        if stripped.startswith('#') or is_structural_token:
            if current:
                paragraphs.append(' '.join(current))
                current = []
            paragraphs.append(stripped)
            # Issue 8: check for unbalanced '[' after stripping [[TOKEN]] markers.
            # If content after the markers has more '[' than ']', the next line
            # (e.g. "6. 546.]") belongs to this paragraph (e.g. "[Juv.,\n6. 546.]").
            _token_stripped = re.sub(r'\[\[[A-Z_]+\]\]\s*', '', stripped)
            _bracket_continuation = _token_stripped.count('[') > _token_stripped.count(']')
            continue

        # Preserve numbered/list-like starts as real paragraph breaks.
        if STRUCTURAL_START_RE.match(stripped):
            if current:
                prev = current[-1]

                # Blemish fix: numeric range hyphen — "Romans 1:19-" + "21. This..."
                # The continuation digit matches STRUCTURAL_START_RE but it's a verse
                # range continuation, not a new list item.  Join and preserve hyphen.
                if re.search(r'\d+-$', prev):
                    current[-1] = prev + stripped
                    continue

                ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
                prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
                starts_with_ref_number = bool(re.match(r'^\d{1,4}\.\s+', stripped))
                if prev_is_ref_abbrev and starts_with_ref_number:
                    current.append(stripped)
                    continue

                # Hard structural: markers that are nearly always paragraph starts
                # Q./A./Ques./Ans. must be UPPERCASE to avoid scholastic citations (Issue 17/26)
                hard_structural = re.match(
                    r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
                    r'(?:Q\.|A\.|Ques\.|Ans\.)\s*(?:\d+\.)?|'
                    r'\d+(?:st|nd|rd|th)\b[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)',
                    stripped
                )
                if not hard_structural:
                     # Fallback for case-insensitive Roman numerals but NOT Q/A
                     hard_structural = re.match(
                        r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|'
                        r'\d+(?:st|nd|rd|th)\b[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)',
                        stripped,
                        re.I
                    )
                
                # Blemish 11: Classical/Scholarly reference tail detection: "Liv. viii." -> "9."
                prev_is_classical_ref = bool(re.search(
                    r'\b(?:liv|aen|hist|tac|plut|cic|sen|aug)\.?\s+(?:hist\.?\s+)?[ivxlcdm]+\.\s*$',
                    prev, re.I
                ))
                is_bare_decimal = bool(re.match(r'^\d{1,2}\.\s+[A-Z]', stripped))
                if prev_is_classical_ref and is_bare_decimal:
                    current.append(stripped)
                    continue

                # Bible book abbreviation followed by Roman or Arabic chapter/verse marker
                prev_is_book_abbrev = bool(re.search(
                    r'\b(?:Gen|Exod|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kings|Chron|Ezra|Neh|Esth|Job|Ps|Prov|Eccl|Cant|'
                    r'Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jonah|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|'
                    r'Matt|Mk|Lk|Jn|Acts|Rom|Cor|Gal|Eph|Phil|Col|Thess|Tim|Tit|Phlm|Heb|Jas|Pet|Jude|Rev)\.\s*$',
                    prev, re.I
                ))
                is_ref_start = bool(re.match(r'^(?:[ivxlcdm]+|\d+)\b', stripped, re.I))
                if prev_is_book_abbrev and is_ref_start:
                    current.append(stripped)
                    continue

                ends_terminal = _is_terminal(prev)
                is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))
                is_comma_continuation = bool(re.search(r',\s*$', prev))

                # Blemish fix: a line ending with a dangling connector word (e.g. "the",
                # "of", "from") or a comma must ALWAYS join the next line, even if that next line
                # superficially matches hard_structural (e.g. "the\n11th, which we…").
                # "11th," looks like an ordinal list marker but it's mid-sentence here.
                # However, if the next line starts with a clear structural list marker (like "(2.)" or "2."),
                # it should NOT be merged since lists can end items with commas.
                is_clear_list_marker = bool(re.match(
                    r'^(?:\(\d+\.?\)|\(\w+\.?\)|\[\d+\.?\]|\[\w+\.?\]|\b\d+\.\s+[A-Z]|\b[IVXLCDM]+\.\s+[A-Z])',
                    stripped
                ))
                if (is_dangling or is_comma_continuation) and not is_clear_list_marker:
                    current.append(stripped)
                    continue

                if (not ends_terminal) and not hard_structural:
                    current.append(stripped)
                    continue
            if current:
                paragraphs.append(' '.join(current))
            current = [stripped]
            continue

        # De-hyphenation: strip trailing hyphen, merge with no space
        if current and current[-1].endswith('-'):
            prev_tail = current[-1]
            candidate = prev_tail + stripped
            # Blemish fix: numeric range hyphens (e.g. "1:19-" / "19-") must be
            # preserved as-is — they are verse/chapter range delimiters, NOT
            # word-break hyphens.  "Romans 1:19-\n21" → "Romans 1:19-21".
            if re.search(r'\d+-$', prev_tail):
                current[-1] = prev_tail + stripped
                continue
            # If the resulting word is a known hard-hyphenated term, keep the hyphen (Issue 1)
            if any(term.lower() == candidate.lower() for term in OWEN_HARD_HYPHENS):
                current[-1] = prev_tail + " " + stripped
            else:
                current[-1] = prev_tail[:-1] + stripped
            continue

        if current:
            prev = current[-1]
            ends_terminal = _is_terminal(prev)
            starts_lower = bool(re.match(r'^[a-z0-9({\[\'"\u201c\u2018]', stripped))
            is_dangling = bool(DANGLING_CONNECTOR_RE.search(prev))
            is_semantic_connector = bool(SEMANTIC_CONNECTOR_RE.match(stripped))
            starts_with_connector = bool(CONNECTOR_STARTERS_RE.match(stripped))

            # Blemish 5, 8, 10: Reference and Scripture continuation awareness
            starts_with_scripture = bool(re.match(rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b', stripped, re.I))
            starts_with_bare_ref = bool(re.match(r'^\d+:\d+', stripped))
            
            ref_abbrevs = r'(?:p|pp|page|pages|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
            prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
            starts_with_ref_number = bool(re.match(r'^\d{1,4}\b', stripped))
            prev_ends_with_number_period = bool(re.search(r'\d+\.\s*$', prev))

            # Issue 76: Multiline block quote preservation
            all_current_text = ' '.join(current)
            is_inside_quote = (
                (all_current_text.count('\u201c') > all_current_text.count('\u201d')) or
                (all_current_text.count('"') % 2 != 0)
            )
            # Blemish fix: unclosed parenthetical \u2014 if the accumulated paragraph
            # has more open parens than closing parens we are inside a parenthetical
            # expression (e.g. a Latin citation like "(Crell. de Natur. Spir.\nSanc.)")
            # and must always join the continuation, regardless of terminal punctuation.
            is_inside_paren = all_current_text.count('(') > all_current_text.count(')')

            if not ends_terminal or is_dangling or is_semantic_connector:
                # Line does not end with terminal punctuation or ends with a connector
                # OR the current line is a semantic connector ("For,", "As,") → join
                current.append(stripped)
            elif starts_lower:
                # Starts lowercase after terminal (e.g. middle of quotation) → join
                current.append(stripped)
            elif is_inside_quote or is_inside_paren:
                # Inside an unclosed quote or parenthetical → join
                current.append(stripped)
            elif starts_with_connector:
                # Next starts with connector word ("Wherefore", "But", "And", etc.) → join
                current.append(stripped)
            elif starts_with_scripture or starts_with_bare_ref:
                # Blemish 5: Scripture continuation → join
                current.append(stripped)
            elif prev_is_ref_abbrev and (starts_with_ref_number or prev_ends_with_number_period):
                # Blemish 8/10: Reference number continuation (p. 280, Aen. 10.) → join
                current.append(stripped)
            else:
                # Terminal punctuation + uppercase start → new paragraph
                paragraphs.append(' '.join(current))
                current = [stripped]
        else:
            current = [stripped]

    if current:
        paragraphs.append(' '.join(current))

    paragraphs = _merge_adjacent_blockquote_paragraphs(paragraphs)
    return post_process_paragraphs(paragraphs)






def _paragraph_needs_numeric_continuation(prev, current):
    """Return True when a numeric-looking paragraph is really a reference tail."""
    if not prev or not current:
        return False

    current_clean = current.strip()
    current_clean = re.sub(r'^\*\*(\d{1,3}[,.;]?)\*\*', r'\1', current_clean)
    if not re.match(r'^\d{1,3}[,.;]?\s+', current_clean):
        return False

    prev_clean = prev.strip()
    
    # Mid-sentence dangling connectors, commas, or hyphens always indicate continuation
    if (
        bool(DANGLING_CONNECTOR_RE.search(prev_clean))
        or bool(re.search(r',\s*$', prev_clean))
        or bool(re.search(r'-\s*$', prev_clean))
    ):
        return True
    if re.search(
        r'\b(?:p|pp|sec|chap|vol|cf|see|ibid|id|op|cit|fol|col|liv|aen|hist)\.?\s*$',
        prev_clean,
        re.I,
    ):
        return True
    if re.search(r'\b(?:Aen|Liv|Hist)\.?\s+\d+\.\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b(?:Liv|Tac|Plut|Cic|Sen|Aug)\.?,?\s+Hist\.?\s+[ivxlcdm]+\.\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev_clean, re.I):
        return True
    if re.search(r'\b\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+\s*$', prev_clean, re.I):
        return True
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,]\s*\d+)*,\s*$', prev_clean, re.I):
        return True
    if _is_scholarly_citation_tail(prev_clean):
        return True
    return False


def _join_numeric_continuation(prev, current):
    """Join numeric continuations, preserving verse ranges where possible."""
    if re.search(r'\b\d+:\d+\s*$', prev.strip()) and re.match(r'^\d{1,3}\.?\s+', current.strip()):
        current = re.sub(r'^(\d{1,3})\.?\s+', r'\1. ', current.strip(), count=1)
        return f"{prev.rstrip()}-{current}"
    return f"{prev} {current}".strip()


def _is_reference_continuation(prev, current):
    """Return True for broken reference tails such as `chap.` / `7:26`."""
    if not prev or not current:
        return False
    prev_clean = prev.strip()
    current_clean = current.strip()
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev_clean, re.I):
        return bool(re.match(r'^\d{1,3}(?::\d+)?(?:[-,;]\s*\d+)*[,:;]?\b', current_clean))
    if SCRIPTURE_CONTINUATION_TRAIL_RE.search(prev_clean):
        return bool(re.match(r'^\d{1,3}(?:[-,;]\s*\d+)*[,:;]?\s+', current_clean))
    return False


def _is_citation_abbrev_continuation(prev, current):
    """Return True for scholarly citation chains split after an author cue."""
    if not prev or not current:
        return False
    prev_clean = prev.strip()
    current_clean = current.strip()
    if not CITATION_ABBREV_START_RE.match(current_clean):
        return False
    if CITATION_AUTHOR_TRAIL_RE.search(prev_clean):
        return True
    if re.search(r'\b(?:see|apud|contra|adv|ad)\s*$', prev_clean, re.I):
        return True
    return False


def _is_scholarly_citation_tail(text):
    """Return True when text ends inside a scholarly citation number chain."""
    if not text:
        return False
    return bool(re.search(
        r'\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*,?\s*$',
        text.strip(),
        re.I,
    ))


def _is_scholarly_citation_fragment(text):
    """Return True for short paragraphs that are only citation tail fragments."""
    if not text:
        return False
    clean = text.strip()
    if len(clean) > 140:
        return False
    return bool(re.fullmatch(
        r'(?:'
        r'(?:and\s+)?(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*|'
        r'ad\s+(?:prim|tert|secund)\.?'
        r')'
        r'(?:[,;]\s*(?:and\s+)?(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*|[,;]\s*ad\s+(?:prim|tert|secund)\.?)*'
        r'\.?',
        clean,
        re.I,
    ))


def _ends_with_scholarly_citation_sentence(text):
    """Return True when a paragraph ends with a scholarly citation sentence."""
    if not text:
        return False
    clean = text.strip()
    if len(clean) > 500:
        clean = clean[-500:]
    return bool(re.search(
        r'\b(?:cap|chap|lib|serm|sermo|epist|ep|orat|tract|homil|haer|dial|'
        r'enchirid|distinct|quest|art|dist|part|vol|q|a|m|p|ad)'
        r'\.?\s+\d+(?:[-,;]\s*\d+)*\.\s*$',
        clean,
        re.I,
    ))


def _trim_overlapping_prefix(prev, current):
    """Return current with a duplicated prefix removed when it repeats prev's tail."""
    prev_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", prev)]
    curr_words = [(m.group(0).lower(), m.start(), m.end()) for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", current)]
    max_overlap = min(10, len(prev_words), len(curr_words))
    for size in range(max_overlap, 1, -1):
        if [w for w, _, _ in prev_words[-size:]] == [w for w, _, _ in curr_words[:size]]:
            cut = curr_words[size - 1][2]
            return current[cut:].lstrip(' ,;:.')
    return current


def _paragraph_needs_text_continuation(prev, current):
    if not prev or not current:
        return False
    if current.startswith('#') or '[[' in current:
        return False
    if '[[' in prev:
        return False
    
    # Check for continuation contexts FIRST (Issues 71, 72)
    # Book + reference (e.g. "1 Corinthians" + "1. Wherefore...")
    if re.search(rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s*$', prev, re.I) and \
       re.match(r'^\d{1,3}[,.;]?\s+', current):
        return True
    
    # Chapter range continuation (e.g. "Chapter 9 to" + "15. It is followed...")
    if re.search(r'\b(?:chapter|chap)\.?\s+[IVXLCDM0-9]+\s+to\s*$', prev, re.I) and \
       re.match(r'^\d{1,3}[,.;]?\s+', current):
        return True


    hard_structural = re.match(r'^(?:(?!\d{4}\.)\d{1,3}\.|\((?!\d{4}\))\d+\.?\)|\[\d+\.?\]|[IVXLCDM]+\.|\d+(?:st|nd|rd|th)\b\s*[,.;]|\d+(?:(?:st|nd|rd|th)ly|dly|ly)\b)', current)
    if hard_structural or MARKDOWN_STRUCTURAL_START_RE.match(current):
        return False

    # Issue 76: Quote continuation
    if (prev.count('\u201c') > prev.count('\u201d')) or (prev.count('"') % 2 != 0):
        return True

    if not _is_terminal(prev):
        return True
    if re.search(r'\b(?:verse|verses|chap|chapter)[.,]?\s*$', prev, re.I):
        return True
    if re.search(r'\b(?:of|the|and|or|to|in|with|from|unto|for)\s*$', prev, re.I):
        return True
    return False


def _is_probable_duplicate_fragment(prev, current):
    """Drop ghost fragments whose words already occur in the previous paragraph."""
    if not prev or not current:
        return False
    
    # Increase threshold for Owen volumes (Issue 108/Audit)
    if len(current) > 1200: 
        return False
        
    prev_norm = _norm_for_dedupe(prev)
    current_norm = _norm_for_dedupe(current)
    
    # 1. Prefix match (Issue 108/Audit ch032): 
    # If the current paragraph is a prefix of the previous one, it is a ghost.
    if prev_norm.startswith(current_norm) and len(current_norm) > 30:
        return True

    # 2. Word overlap match
    prev_words = set(re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", prev_norm))
    current_words = re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", current_norm)
    
    useful = [w for w in current_words if len(w) > 2]
    if len(useful) < 8:
        return False
        
    overlap = sum(1 for w in useful if w in prev_words)
    ratio = overlap / len(useful)
    
    # High confidence for short runs, very high for longer ones
    if len(useful) < 25:
        return ratio >= 0.90
    return ratio >= 0.95


def _remove_repeated_opening_clause(text):
    """Remove duplicated opening clauses like 'So we are said ...: So we are said ...:'."""
    pattern = re.compile(r'^(.{25,220}?[.:;])\s+\1', re.I)
    prev = None
    while prev != text:
        prev = text
        text = pattern.sub(r'\1 ', text)
    return text


def _collapse_adjacent_duplicate_refs(text):
    """Collapse directly-concatenated duplicate scripture references."""
    def _dedup_repl(m):
        first = m.group(1)
        second = m.group(2)
        # Normalize for comparison (Issue 108/Audit)
        f_norm = re.sub(r'[^a-z0-9:]', '', first.lower())
        s_norm = re.sub(r'[^a-z0-9:]', '', second.lower())
        
        if f_norm == s_norm or f_norm.endswith(s_norm) or s_norm.endswith(f_norm):
             return first if len(first) >= len(second) else second
        return m.group(0)

    # Pattern: Book Ch:v followed by optional punctuation and potentially a repeat.
    # Allow zero or more punctuation/spaces between them (Issue 108/Audit)
    _ADJ_DUP_RE = re.compile(
        r'(\b(?:[1-3]\s+)?[A-Z][a-zA-Z ]{1,30}?\s+\d+:\d+(?:[-,]\s*\d+)*)'
        r'[\s,;.]*'
        r'((?:(?:[1-3]\s+)?[A-Z][a-zA-Z, ]{1,30}?\s+)?\d+:\d+(?:[-,]\s*\d+)*)',
    )
    previous = None
    while previous != text:
        previous = text
        text = _ADJ_DUP_RE.sub(_dedup_repl, text)
    return text


def _remove_duplicate_scripture_tail(text):
    """Trim repeated scripture-reference tails inside one paragraph."""
    previous = None
    while previous != text:
        previous = text
        refs = list(SCRIPTURE_REF_RE.finditer(text))
        if len(refs) < 4:
            return text

        # Compare normalized reference tokens and cut if the same tail starts over.
        norm_refs = []
        for m in refs:
            token = re.sub(r'\s+', ' ', m.group(0).lower())
            token = re.sub(r'^(?:[1-3]\s+)?', '', token)
            norm_refs.append((token, m.start(), m.end()))

        changed = False
        for i in range(len(norm_refs)):
            for j in range(i + 2, len(norm_refs)):
                if norm_refs[i][0] != norm_refs[j][0]:
                    continue
                run = 0
                while (
                    i + run < len(norm_refs)
                    and j + run < len(norm_refs)
                    and norm_refs[i + run][0] == norm_refs[j + run][0]
                ):
                    run += 1
                if run >= 2:
                    cut_start = norm_refs[j][1]
                    cut_end = norm_refs[j + run - 1][2]
                    while cut_start > 0 and text[cut_start - 1] in ' \t':
                        cut_start -= 1
                    while cut_end < len(text) and text[cut_end] in ' ;,.:':
                        cut_end += 1
                    # AGES sometimes leaves a bare verse number between duplicated
                    # reference runs, such as "Ezekiel 36:26; 26; John 1:13".
                    bare_verse = re.match(r'\s*\d{1,3}\s*[;,]\s*', text[cut_end:])
                    if bare_verse:
                        cut_end += bare_verse.end()
                    text = re.sub(r'\s{2,}', ' ', (text[:cut_start] + ' ' + text[cut_end:]).strip())
                    changed = True
                    break
            if changed:
                break
        if not changed:
            return text
    return text


def _remove_interrupted_duplicate_clause(text):
    """Remove reference-list ghosts that interrupt and restart the same clause."""
    words = [
        (re.sub(r'[^a-z0-9\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+', '', m.group(0).lower()), m.start(), m.end())
        for m in re.finditer(r"[A-Za-z0-9'\u2019\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF-]+", text)
    ]
    words = [item for item in words if item[0]]
    size = 6
    for i in range(0, max(0, len(words) - (size * 2))):
        first = [w for w, _, _ in words[i:i + size]]
        if sum(1 for w in first if re.search(r'[a-z]', w)) < 4:
            continue
        for j in range(i + size, min(len(words) - size + 1, i + 80)):
            if first != [w for w, _, _ in words[j:j + size]]:
                continue
            gap = text[words[i + size - 1][2]:words[j][1]]
            if len(SCRIPTURE_REF_RE.findall(gap)) < 2:
                continue
            # Guard 1 — never delete a span carrying source-language text. A true
            # AGES ghost is an English clause restarting after a bare reference
            # list; it never contains Greek/Hebrew. If the gap holds any Greek or
            # Hebrew, the repeated phrase is coincidental (two distinct sentences
            # that happen to share a 6-word run) and the Greek is genuine content
            # that must not be dropped. (v16: "that spake in the name of" recurs
            # around 2 Peter 2:1, ἐγένοντο ψευδοπροφῆται ἐν τῷ λαῷ.)
            if re.search(r'[Ͱ-Ͽἀ-῿֐-׿]', gap):
                continue
            # Guard 2 — a genuine ghost interruption is essentially just the
            # reference list. If, after removing the scripture references, the gap
            # still carries substantive prose (more than a few words), the two
            # occurrences are separate sentences, not a ghost restart — keep both.
            residual = SCRIPTURE_REF_RE.sub(' ', gap)
            residual_words = [w for w in re.findall(r"[A-Za-z]{2,}", residual)]
            if len(residual_words) > 3:
                continue
            cut_start = words[i + size - 1][2]
            cut_end = words[j + size - 1][2]
            return (text[:cut_start] + text[cut_end:]).strip()
    return text


def _remove_adjacent_repeated_word_runs(text):
    """Collapse adjacent ghost repeats inside a paragraph."""
    if not text or len(text) < 20:
        return text

    def tokens(value):
        return [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", value)
        ]

    previous = None
    while previous != text:
        previous = text
        words = tokens(text)
        changed = False
        max_size = min(14, len(words) // 2)
        for size in range(max_size, 1, -1):
            for i in range(0, len(words) - (size * 2) + 1):
                first = [w for w, _, _ in words[i:i + size]]
                second = [w for w, _, _ in words[i + size:i + (size * 2)]]
                if first != second:
                    continue
                useful = [w for w in first if len(w) > 2 or ':' in w]
                if len(useful) < 2:
                    continue
                cut_start = words[i + size][1]
                cut_end = words[i + (size * 2) - 1][2]
                while cut_start > 0 and text[cut_start - 1] in ' \t':
                    cut_start -= 1
                while cut_end < len(text) and text[cut_end] in ' \t,;:.':
                    cut_end += 1
                text = (text[:cut_start] + ' ' + text[cut_end:]).strip()
                changed = True
                break
            if changed:
                break
        if changed:
            continue
        text = re.sub(r'\b([A-Z][a-z]{3,})\s+\1\b', r'\1', text)
    return re.sub(r'\s{2,}', ' ', text)


def post_process_paragraphs(paragraphs):
    """Clean paragraph-level artifacts after line healing."""
    # 1. Primary cleanup of OCR artifacts and noise
    pre_cleaned = []
    for para in paragraphs:
        stripped = para.strip()
        # Sweep 'stray letter' paragraphs (Issue 1)
        # standalone lowercase letters (often from Christ -> i, or headers)
        if re.match(r'^[a-z]\s*$', stripped):
            continue
        pre_cleaned.append(para)
    paragraphs = pre_cleaned

    cleaned = []
    for para in paragraphs:
        para = _remove_repeated_opening_clause(para.strip())
        para = _collapse_adjacent_duplicate_refs(para)
        
        # Aggressive book doubling fix (Issue 108/Audit)
        # Handles "Romans 8:29Romans" or "Hebrews 9:14Hebrews"
        para = re.sub(r'(\b(?:[1-3]\s+)?[A-Z][a-z]{3,}\s+\d+:\d+(?:[-,]\s*\d+)*)\s*([A-Z][a-z]{3,})\b', 
                      lambda m: m.group(1) if m.group(1).startswith(m.group(2)) else m.group(0), para)
        
        # Aggressive coordinate doubling fix (Issue 108/Audit)
        # Handles "Romans 8:29, 8:29" or "Romans 8:29 8:29"
        para = re.sub(r'(\b(?:[1-3]\s+)?[A-Z][a-z]{3,}\s+\d+:\d+(?:[-,]\s*\d+)*)[\s,;.]+(\d+:\d+(?:[-,]\s*\d+)*)\b',
                      lambda m: m.group(1) if m.group(1).endswith(m.group(2)) else m.group(0), para)
        
        para = _remove_interrupted_duplicate_clause(para)
        para = _repair_glued_scripture_book_references(para)
        para = _remove_duplicate_scripture_tail(para)
        para = _remove_adjacent_repeated_word_runs(para)
        # Catechism ghosts repaired in v1 overrides during rendering
        if not para:
            continue

        for part in _split_inline_structural_markers(para):
            if not part:
                continue

            if (
                cleaned
                and re.fullmatch(r'(?:Objection|Obj\.?|Answer|Ans\.?|Solution|Sol\.?)', cleaned[-1].strip(), re.I)
                and re.match(r'^\d+\.?\s+', part)
            ):
                label = cleaned[-1].strip()
                cleaned[-1] = f"{label} {part}".strip()
                continue

            if cleaned and _paragraph_needs_numeric_continuation(cleaned[-1], part):
                cleaned[-1] = _join_numeric_continuation(cleaned[-1], part)
                continue

            if cleaned and _is_citation_abbrev_continuation(cleaned[-1], part):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            if cleaned:
                recent_context = ' '.join(cleaned[-3:])
                part = _trim_duplicate_reference_prefix(recent_context, part)
                if not part:
                    continue

            if cleaned and _paragraph_needs_text_continuation(cleaned[-1], part):
                trimmed = _trim_overlapping_prefix(cleaned[-1], part)
                if (
                    trimmed != part
                    or _is_reference_continuation(cleaned[-1], part)
                    or not _is_terminal(cleaned[-1])
                    or re.match(r'^(?:\*\*)?\d+(?:st|nd|rd|th)\b\s+', part)
                ):
                    cleaned[-1] = f"{cleaned[-1]} {trimmed}".strip()
                    continue

            if (
                cleaned
                and (
                    _is_scholarly_citation_fragment(cleaned[-1])
                    or _ends_with_scholarly_citation_sentence(cleaned[-1])
                )
                and re.match(r'^(?:But|And|For|Yea|Yet|So|Herein|Wherefore)\b', part)
            ):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            if cleaned and _is_probable_duplicate_fragment(cleaned[-1], part):
                continue

            if cleaned and _is_scripture_ref_fragment(part):
                para_norm = _norm_for_dedupe(part)
                prev_norm = _norm_for_dedupe(cleaned[-1])
                if para_norm and para_norm in prev_norm[-500:]:
                    continue
                para_refs = _scripture_ref_tokens(part)
                prev_refs = set(_scripture_ref_tokens(cleaned[-1]))
                if para_refs and prev_refs:
                    overlap = sum(1 for ref in para_refs if ref in prev_refs)
                    if overlap / len(para_refs) >= 0.6:
                        continue
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            # Owen-specific: Join short transitional paragraphs with the next one (Issue 1)
            # Match "But —", "For —", "And —", "Or —", etc.
            # Don't join if the next part is structural (Issue 1 Refinement)
            is_structural = part.startswith('[[')
            if cleaned and not is_structural and re.match(r'^(?:But|For|And|Or|Yea|Yet|So|Wherefore)\s*[—\-]\s*$', cleaned[-1].strip()):
                cleaned[-1] = f"{cleaned[-1]} {part}".strip()
                continue

            cleaned.append(part)
    return _remove_global_ngram_duplicates(cleaned)


def _remove_global_ngram_duplicates(paragraphs, size=14):
    """
    Remove non-consecutive paragraph-level duplicates using n-gram anchors.
    This catches 'interrupted' ghost layers that sequential de-duplication misses.
    """
    seen_anchor_pairs = set()
    cleaned = []
    for para in paragraphs:
        # Normalize for dedupe to avoid minor spacing/punctuation differences
        para_norm = _norm_for_dedupe(para)
        words = [w for w in re.findall(r"[a-z0-9:\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", para_norm)]
        if len(words) < size:
            cleaned.append(para)
            continue

        # Check first and last n-gram of the paragraph
        first_anchor = tuple(words[:size])
        last_anchor = tuple(words[-size:])
        anchor_pair = (first_anchor, last_anchor)

        # Require BOTH anchors as a pair to match to be considered a ghost-layer duplicate (Issue 108/Audit)
        if anchor_pair in seen_anchor_pairs:
            continue

        seen_anchor_pairs.add(anchor_pair)
        cleaned.append(para)
    return cleaned


def deduplicate_junction(prev_text, next_text, threshold=0.85):
    """Lookback buffer: remove duplicate text at page junctions."""
    if not prev_text or not next_text:
        return next_text
    
    overlap_len = min(60, len(prev_text), len(next_text))
    if overlap_len < 15:
        return next_text
    
    prev_tail = prev_text[-overlap_len:].lower().strip()
    next_head = next_text[:overlap_len].lower().strip()
    
    matches = sum(1 for a, b in zip(prev_tail, next_head) if a == b)
    ratio = matches / max(len(prev_tail), len(next_head))
    
    if ratio >= threshold:
        cut = overlap_len
        while cut < len(next_text) and cut < overlap_len + 40:
            if next_text[:cut].lower().strip() == prev_tail:
                return next_text[cut:]
            cut += 1
        return next_text[overlap_len:].lstrip()
    
    return next_text


def get_pages_text(
    doc,
    pages_md,
    start_page,
    end_page,
    healer_mode=True,
    title="",
    chapter_id="",
    config=None,
    allow_treatise_title_page=True,
):
    """Get merged text for a range of pages with optional paragraph healing.

    Paragraph healing must be holistic across the full page range. Running
    reconstruction page-by-page forces false breaks at page boundaries.

    When healer_mode=False, returns clean raw text without paragraph
    reconstruction (used for layout-preserved front matter pages).
    """
    _page_h = (config or {}).get('page_height', None)
    raw_parts = []

    for pg in range(start_page, min(end_page + 1, len(doc))):
        raw = get_merged_page_text(
            doc,
            pages_md,
            pg,
            allow_treatise_title_page=allow_treatise_title_page,
            page_height=_page_h,
        )
        if not raw.strip():
            continue
        raw_parts.append(raw)
    
    if not raw_parts:
        return ''

    # Clean and heal the whole chapter/range at once so sentences that cross
    # PDF page boundaries stay inside the same EPUB paragraph.
    cleaned = clean_text('\n'.join(raw_parts), config=config)
    if not cleaned:
        return ''

    return '\n\n'.join(reconstruct_paragraphs(cleaned))


def _build_flat_chapters(doc, pages_md, footnote_map):
    """Fallback: create one chapter per PDF page."""
    chapters = []
    for pg in range(len(doc)):
        text = get_merged_page_text(doc, pages_md, pg)
        if not text.strip():
            continue
        page_num = pg + 1
        chapters.append(Chapter(
            cid=f'page{page_num:04d}',
            title=f'Page {page_num}',
            level=2,
            raw_text=text,
            body_html=f'<p>{_html_escape(text.strip())}</p>',
            page_start=pg,
            page_end=pg,
        ))
    return chapters


