import re
from scripts.markdown_parser import _TRANSITIONAL_WORD_RE

_SCHOLASTIC_QUOTED_OBJECTION_RE = re.compile(
    r'(?P<intro>\b(?:Obj(?:ection)?\.?\s*\d+\.?)\s+But\s+some\s+may\s+say,)\s*'
    r'(?P<quote>["“][^\n]+?)\n\n'
    r'\[\[BLOCKQUOTE\]\]\s*(?P<rest>.*?["”])',
    re.I | re.S,
)


def _repair_scholastic_blockquote_boundaries(text):
    """Move blockquote markers back over quoted Objection/Obj. openings."""
    if not text:
        return text

    def repl(match):
        quote = match.group("quote").strip()
        rest = re.sub(r'\s+', ' ', match.group("rest").strip())
        return f'{match.group("intro")}\n\n[[BLOCKQUOTE]] {quote} {rest}'

    return _SCHOLASTIC_QUOTED_OBJECTION_RE.sub(repl, text)


def _repair_fused_word_ordinals(text: str) -> str:
    """Split paragraphs at fused capitalised word ordinals (e.g. Secondly, Thirdly) that follow terminal punctuation."""
    if not text:
        return text

    paras = text.split('\n\n')
    out = []
    for para in paras:
        stripped = para.strip()
        # If it starts with a blockquote marker, do not split it.
        if stripped.startswith('[[BLOCKQUOTE]]'):
            out.append(para)
            continue

        # Otherwise, split at space before Thirdly/Secondly/etc. following terminal punctuation.
        pattern = r'(?<=[.!?])\s+(?=(?:Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Seventhly|Eighthly|Ninthly|Lastly|Finally),\s)'
        para_fixed = re.sub(pattern, '\n\n', para)
        out.append(para_fixed)

    return '\n\n'.join(out)


def _repair_mid_sentence_blockquote_splits(text: str) -> str:
    """Join paragraphs split mid-sentence before a [[BLOCKQUOTE]] marker."""
    if not text or '[[BLOCKQUOTE]]' not in text:
        return text

    paras = text.split('\n\n')
    out: list[str] = []
    i = 0
    n = len(paras)

    while i < n:
        para = paras[i]
        stripped = para.strip()

        if i == n - 1:
            out.append(para)
            i += 1
            continue

        next_para = paras[i+1].strip()
        if next_para.startswith('[[BLOCKQUOTE]]'):
            clean_end = stripped.rstrip('\"\' \t\r\n')
            if clean_end and not clean_end.endswith(('.', ',', ';', ':', '?', '!', '—', '-')):
                blockquote_content = next_para[len('[[BLOCKQUOTE]]'):].strip()
                merged_para = stripped + ' ' + blockquote_content
                paras[i+1] = merged_para
                i += 1
                continue

        out.append(para)
        i += 1

    return '\n\n'.join(out)


_TOKEN_STRIP_RE = re.compile(r'\[\[[A-Z_]+\]\]\s*')


def _repair_unbalanced_bracket_splits(text):
    """Rejoin paragraph fragments split across a \n\n where the previous
    paragraph has an unclosed '[' that isn't part of a [[TOKEN]] marker.

    This commonly occurs when a citation like '[Juv., 6. 546.]' gets broken
    across paragraphs during extraction: the structural token ends with '[Juv.,'
    and the continuation '6. 546.]' lands in its own paragraph.
    """
    if not text or '[' not in text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    i = 0
    while i < len(paragraphs):
        para = paragraphs[i]
        # Strip [[TOKEN]] markers to count only content brackets
        content = _TOKEN_STRIP_RE.sub('', para)
        if content.count('[') > content.count(']') and i + 1 < len(paragraphs):
            # Absorb the next paragraph (the continuation of the unclosed bracket)
            paragraphs[i + 1] = para + ' ' + paragraphs[i + 1]
            i += 1
            continue
        result.append(para)
        i += 1
    return '\n\n'.join(result)


_DOC_STRUCTURE_TOKENS_RE = re.compile(
    r'^\[\[(?:CHAPTER|PART|SUBTITLE|DIGRESSION|BLOCKQUOTE)\]\]'
)


def _repair_lowercase_continuation_splits(text: str) -> str:
    """Rejoin paragraphs that open with a lowercase letter.

    Owen never begins a fresh paragraph with a lowercase letter.  When a
    paragraph starts with one it is a PDF page-boundary split: the sentence was
    cut mid-stream at a page turn and the continuation was left as a separate
    paragraph in the intermediate JSON.

    Structural document tokens ([[CHAPTER]], [[SUMMARY]], [[PART]], etc.) are
    never lowercased, so they are never affected.  [[BLOCKQUOTE]] text CAN be
    extended (the quote itself may have split across a page).

    Skipped when the previous paragraph is a bare document-structure header
    (those have no trailing prose that could be incomplete).
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and stripped
            and stripped[0].islower()
            and not _DOC_STRUCTURE_TOKENS_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            result[-1] = result[-1].rstrip() + ' ' + stripped
        else:
            result.append(para)
    return '\n\n'.join(result)


_CONNECTOR_END_RE = re.compile(
    r'(?:'
    r'[,;:—–-]\s*|'
    r'\b(?:and|or|but|as|to|into|unto|of|in|by|with|that|which|is|are|were|was|be|been)\b\s*'
    r')[”"\'’]*\s*$',
    re.I
)

_LIST_MARKER_START_RE = re.compile(
    r'^\s*(?:'
    r'[\(\[]?(?:1st|2nd(?:ly)?|2dly|3rd(?:ly)?|3dly|4th(?:ly)?|5th(?:ly)?|first|secondly|thirdly|fourthly|fifthly|lastly)\b'
    r')\s*',
    re.I
)


def _repair_flat_list_continuation_splits(text: str) -> str:
    """Rejoin paragraphs that open with a list marker when the previous paragraph
    ends with a connector or punctuation (e.g. comma, semicolon, colon, or connector word).
    This ensures that short inline lists that flow with the sentence are elegantly joined
    into a single paragraph, wrapping the inline markers in bold formatting (**marker**)
    to preserve their visual distinction.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        match = _LIST_MARKER_START_RE.match(stripped)
        if (
            result
            and stripped
            and match
            and _CONNECTOR_END_RE.search(result[-1].strip())
            and not _DOC_STRUCTURE_TOKENS_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            marker = match.group(0)
            marker_stripped = marker.strip()
            # Wrap marker in markdown bold asterisks if not already bolded
            if not (marker_stripped.startswith('**') and marker_stripped.endswith('**')):
                trailing_space = marker[len(marker_stripped):]
                bold_marker = f"**{marker_stripped}**{trailing_space}"
                stripped_bolded = bold_marker + stripped[match.end():]
            else:
                stripped_bolded = stripped
            
            result[-1] = result[-1].rstrip() + ' ' + stripped_bolded
        else:
            result.append(para)
    return '\n\n'.join(result)


_SCHOLASTIC_CONTINUATION_RE = re.compile(
    r'^\d{1,3}\.\s+(?:q|a|p|pp|vol|sec|lib|cap|chap|serm|art|dist|part|num)\.',
    re.I,
)


def _repair_transitional_word_isolation(text: str) -> str:
    """Merge lone transitional words back onto their preceding paragraph.

    Owen sometimes had sentences like "...these things are inseparable.
    Therefore, 3. The difference..." which PDF extraction splits into three
    separate paragraphs. The middle "Therefore," fragment has no prose on its
    own and must be appended to the preceding paragraph.

    Only words known to function as sentence connectors are merged; proper
    nouns, names, and structural tokens are never touched.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and _TRANSITIONAL_WORD_RE.match(stripped)
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            # Append transitional fragment with a space
            trail = stripped.rstrip()
            result[-1] = result[-1].rstrip() + ' ' + trail
        else:
            result.append(para)
    return '\n\n'.join(result)


def _repair_scholastic_anchor_splits(text: str) -> str:
    """Rejoin scholastic citation tails split from their introducing clause.

    Pattern: paragraph ending with a comma after an author name, followed by a
    paragraph that begins with a two-or-more-digit number and a lowercase
    abbreviation (e.g. "22. q. 174, a. 1" — a Thomistic q./a. reference).
    These are never list items; they are inlined citation locators.
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result = []
    for para in paragraphs:
        stripped = para.strip()
        if (
            result
            and _SCHOLASTIC_CONTINUATION_RE.match(stripped)
            and result[-1].rstrip().endswith(',')
            and not _DOC_STRUCTURE_TOKENS_RE.match(result[-1].strip())
        ):
            result[-1] = result[-1].rstrip() + ' ' + stripped
        else:
            result.append(para)
    return '\n\n'.join(result)


# ---------------------------------------------------------------------------
# Dangling single-letter initial repair (Issue 21)
# ---------------------------------------------------------------------------
_DANGLING_INITIAL_END_RE = re.compile(
    r'(?<!\S)([A-Z])\.\s*$'   # bare single capital + period at end of paragraph
)
_CITATION_ABBREV_BEFORE_INITIAL_RE = re.compile(
    r'\b(?:chap|cap|lib|part|sect|num|vol|art|op|cit|ibid|serm)\.\s+[A-Z]\.\s*$',
    re.I,
)
_STRUCTURAL_DASH_BEFORE_INITIAL_RE = re.compile(
    r'[—–]\s*[A-Z]\.\s*$'
)
_COMMA_BEFORE_INITIAL_RE = re.compile(
    r',\s*[A-Z]\.\s*$'
)


def _repair_dangling_initial_splits(text: str) -> str:
    """Join a paragraph ending with a bare single-letter initial to the next.

    When a PDF line break falls in the middle of an author-initials citation
    (e.g. "S. P."), extract.py emits one paragraph ending with "S." and the
    next paragraph starting with "P. do sufficiently…".  This function merges
    them back into one paragraph.

    Guards — these endings are NOT merged (false positives):
    - Citation abbreviation before initial: "chap. I.", "cap. V.", etc.
    - Structural dash before initial:       "— I.", "– V." (numbered observations)
    - Doc-structure token at para start:    "[[ROMAN_HEAD]]", "[[CHAPTER]]", etc.
    - Comma immediately before initial:     ", V." (Roman numeral list entries)
    - Standalone initial paragraph:         "I." alone (Roman numeral heading)
    """
    if not text:
        return text
    paragraphs = text.split('\n\n')
    result: list = []
    for para in paragraphs:
        stripped = para.strip()
        if result:
            prev_stripped = result[-1].rstrip()
            m = _DANGLING_INITIAL_END_RE.search(prev_stripped)
            if m:
                text_before = prev_stripped[:m.start()].strip()
                if text_before:  # skip standalone initials (would be Roman headings)
                    is_citation = bool(_CITATION_ABBREV_BEFORE_INITIAL_RE.search(prev_stripped))
                    is_dash = bool(_STRUCTURAL_DASH_BEFORE_INITIAL_RE.search(prev_stripped))
                    is_doc_token = bool(re.match(r'^\[\[', prev_stripped))
                    is_comma = bool(_COMMA_BEFORE_INITIAL_RE.search(prev_stripped))
                    if not any([is_citation, is_dash, is_doc_token, is_comma]):
                        result[-1] = result[-1].rstrip() + ' ' + stripped
                        continue
        result.append(para)
    return '\n\n'.join(result)


def _repair_sermon_prefatory_note_splits(text: str) -> str:
    """Heal sermon prefatory note split by summary tag and page boundary.
    
    Pattern:
      Paragraph 1: 'THIS sermon, from'
      Paragraph 2: '[[SUMMARY]] Hebrews 12:27, was preached before Parliament on a'
      Paragraph 3: 'day set apart for extraordinary humiliation.'
    """
    if not text:
        return text
    pattern = re.compile(
        r'(THIS\s+sermon,\s+from)\s*\n\n\s*\[\[SUMMARY\]\]\s*([^A-Z\n]*[A-Z][^\n]*?)\s*\n\n\s*([a-z][^\n]*?)(?=\n\n|$)',
        re.S | re.I
    )
    return pattern.sub(r'\1 \2 \3', text)


def _split_tail_signature(text: str) -> str:
    """Split J.O. signature fused at the end of a body paragraph into its own paragraph."""
    if not text:
        return text
    pattern = re.compile(
        r'([.!?”"])\s+'
        r'(?P<sig>'
        r'J\.?\s*O\.?\s+From\s+my\s+Study.*|'
        r'J\.?\s*O\.?\s+September\s+the\s+last.*'
        r')$',
        re.I
    )
    return pattern.sub(r'\1\n\n\g<sig>', text)
