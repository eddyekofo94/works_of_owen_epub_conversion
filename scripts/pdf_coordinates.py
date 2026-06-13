import re
from shared import SCRIPTURE_BOOK_RE, STRUCTURAL_START_RE, OWEN_HARD_HYPHENS

PAGE_H = 792
TOP_MARGIN = 50
BOTTOM_MARGIN = 50

def coordinate_redactor(blocks, page_height=PAGE_H, top_margin=TOP_MARGIN, bottom_margin=BOTTOM_MARGIN):
    """
    Filter out text blocks that overlap the top `top_margin` pts
    or bottom `bottom_margin` pts of the page.

    Uses LINE-level filtering within blocks: only keeps lines whose
    vertical midpoint is inside the safe reading zone [top_margin, page_h - bottom_margin].
    This preserves content like 'CONTENTS OF VOLUME 1' (y≈62) while removing
    page numbers (y≈30) and AGES header blocks (y≈26-75).
    """
    keep = []
    for b in blocks:
        if b.get('type') != 0:
            continue
        keep_lines = []
        for line in b['lines']:
            y_center = (line['bbox'][1] + line['bbox'][3]) / 2
            line_text = ''.join(span.get('text', '') for span in line.get('spans', [])).strip()
            
            # PROTECTIVE MARGINS: If a line is in the margin zone but looks like 
            # substantial body text (not a header/footer), keep it.
            is_header_footer = (
                re.fullmatch(r'\d{1,4}', line_text)
                or re.search(
                    r'THE AGES DIGITAL LIBRARY|THE WORKS OF JOHN OWEN|'
                    r'JOHN OWEN COLLECTION|BOOKS FOR THE AGES|AGES SOFTWARE|'
                    r'VERSION \d\.\d|VOLUME \d+',
                    line_text,
                    re.I,
                )
            )
            
            # Bottom safety: Owen's footnotes or low body lines often sit at y=580-605
            # We use a 70pt window from the bottom. If the text looks substantial, keep it.
            if y_center > page_height - 70 and not is_header_footer and len(line_text) >= 4:
                keep_lines.append(line)
                continue

            if y_center < top_margin and not is_header_footer:
                # Top safety: don't clip lines that might be part of a chapter head or list start
                if y_center > 25 and (
                    len(line_text) > 20
                    or STRUCTURAL_START_RE.match(line_text + ' ')
                    or any(c.islower() for c in line_text)
                ):
                    keep_lines.append(line)
                    continue
                continue
            
            if is_header_footer and (y_center < 75 or y_center > page_height - 75):
                continue

            if top_margin <= y_center <= page_height - bottom_margin:
                keep_lines.append(line)
        if keep_lines:
            # Rebuild block with only kept lines
            new_block = dict(b)
            new_block['lines'] = keep_lines
            # Recalculate bbox from kept lines
            if keep_lines:
                x0 = min(l['bbox'][0] for l in keep_lines)
                y0 = min(l['bbox'][1] for l in keep_lines)
                x1 = max(l['bbox'][2] for l in keep_lines)
                y1 = max(l['bbox'][3] for l in keep_lines)
            new_block['bbox'] = (x0, y0, x1, y1)
            keep.append(new_block)
    return keep


BLOCKQUOTE_INSET_THRESHOLD = 14
BLOCKQUOTE_RIGHT_INSET_THRESHOLD = 8


def _line_text_from_spans(line):
    return ''.join(convert_span_text(span['text'], span.get('font', '')) for span in line.get('spans', [])).strip()



def convert_span_text(text, font):
    """Convert text based on font encoding."""
    from shared import is_greek_font, convert_greek_word, is_hebrew_font, convert_gideon_hebrew
    if is_greek_font(font):
        return convert_greek_word(text)
    if is_hebrew_font(font):
        return convert_gideon_hebrew(text)
    return text
def _merge_adjacent_blockquote_paragraphs(paragraphs):
    merged = []
    for paragraph in paragraphs:
        # Merge: paragraph ending with connector word + next starting with [[BLOCKQUOTE]]
        if (
            merged
            and paragraph.startswith('[[BLOCKQUOTE]]')
            and DANGLING_CONNECTOR_RE.search(merged[-1])
        ):
            merged[-1] = merged[-1].rstrip() + ' ' + paragraph
            continue
        # Merge: paragraph ends mid-sentence (plain word, no terminal punctuation) before
        # [[BLOCKQUOTE]] — catches page-break splits like "They saw\n\n[[BLOCKQUOTE]] his glory"
        # where the sentence was split at a PDF page boundary.
        if (
            merged
            and paragraph.startswith('[[BLOCKQUOTE]]')
            and re.search(r'[a-zA-Z]\s*$', merged[-1])
            and not re.search(r'[.!?:;,\"“”‘’\']\s*$', merged[-1])
        ):
            merged[-1] = merged[-1].rstrip() + ' ' + paragraph
            continue
        # Merge: paragraph ends with dangling connector + next starts with connector word
        if (
            merged
            and DANGLING_CONNECTOR_RE.search(merged[-1])
            and CONNECTOR_STARTERS_RE.match(paragraph)
        ):
            merged[-1] = merged[-1].rstrip() + ' ' + paragraph
            continue
        # Merge: paragraph ends with scripture reference + next starts with uppercase
        if (
            merged
            and SCRIPTURE_TAIL_RE.search(merged[-1])
            and paragraph[0].isupper()
            and not paragraph.startswith('[[')
        ):
            merged[-1] = merged[-1].rstrip() + ' ' + paragraph
            continue
        if (
            merged
            and merged[-1].startswith('[[BLOCKQUOTE]]')
            and paragraph.startswith('[[BLOCKQUOTE]]')
            and not _blockquote_has_sentence_terminal(merged[-1])
        ):
            merged[-1] = merged[-1].rstrip() + ' ' + _blockquote_content(paragraph)
        elif merged and merged[-1].startswith('[[BLOCKQUOTE]]'):
            tail, rest = _split_leading_scripture_reference_tail(paragraph)
            if tail and re.search(r'\(\s*$', _blockquote_content(merged[-1])):
                merged[-1] = merged[-1].rstrip() + ' ' + tail
                if rest:
                    merged.append(rest)
            else:
                merged.append(paragraph)
        elif merged and _paragraph_expects_scripture_reference_tail(merged[-1]):
            tail, rest = _split_leading_scripture_reference_tail(paragraph)
            if tail and rest:
                merged[-1] = merged[-1].rstrip() + ' ' + tail + ' ' + rest
            else:
                merged.append(paragraph)
        else:
            merged.append(paragraph)
    return merged


_GLUED_SCRIPTURE_REF_RE = re.compile(
    rf'\b(?P<wrong>(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE})\s+'
    r'(?P<coord>\d+:\d+)'
    rf'(?P<right>(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE})\s+'
    r'(?P=coord)(?P<tail>(?:[-,]\s*\d+)*)',
    re.I,
)


def _repair_glued_scripture_book_references(text: str) -> str:
    """Remove stale adjacent book names left by overlapping AGES marker layers."""
    if not text:
        return text

    def repl(match: re.Match) -> str:
        wrong = re.sub(r'\s+', ' ', match.group('wrong')).strip().lower()
        right = re.sub(r'\s+', ' ', match.group('right')).strip().lower()
        if wrong == right:
            return match.group(0)
        return f'{match.group("right")} {match.group("coord")}{match.group("tail")}'

    text = _GLUED_SCRIPTURE_REF_RE.sub(repl, text)
    text = re.sub(
        r'\bProverbs\s+(\d+):(\d+)Song\s+of\s+Solomon\s+\1\b(?!:)',
        r'Song of Solomon \1',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bProverbs\s+(\d+):(\d+)Song\s+of\s+Solomon\b',
        r'Song of Solomon \1:\2',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bProverbs\s+(\d+):(\d+)Song\s+of\b.{0,180}?\bSong\s+of\s+Solomon\s+\1:\2\b',
        r'Song of Solomon \1:\2',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\bSong\s+of\s+Solomon\s+3:1\s+it,\s*"Go forth',
        'Song of Solomon 3:11, "Go forth',
        text,
        flags=re.I,
    )
    return text


def _flush_blockquote_lines(output_lines, pending_bq):
    if pending_bq:
        joined = _join_blockquote_lines(pending_bq)
        if joined and (len(pending_bq) >= 2 or re.match(r'^[“"\']', pending_bq[0])):
            output_lines.append('[[BLOCKQUOTE]] ' + joined)
        else:
            output_lines.extend(pending_bq)
    return []


def _append_blockquote_aware(output_lines, pending_bq, text, is_bq):
    """Group consecutive inset lines and emit them as a single BLOCKQUOTE token."""
    if is_bq:
        pending_bq.append(text)
        return pending_bq

    pending_bq = _flush_blockquote_lines(output_lines, pending_bq)
    if text:
        output_lines.append(text)
    return pending_bq


def _join_blockquote_lines(lines):
    joined = ''
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if joined.endswith('-'):
            # Word-level hard-hyphen check
            m_prev = re.search(r'([A-Za-z0-9\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+)-$', joined)
            m_next = re.match(r'^([A-Za-z0-9\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+)', stripped)
            
            is_hard = False
            if m_prev and m_next:
                word_candidate = m_prev.group(1) + '-' + m_next.group(1)
                is_hard = any(term.lower() == word_candidate.lower() for term in OWEN_HARD_HYPHENS)
                
            if is_hard:
                joined += stripped
            else:
                joined = joined[:-1] + stripped
        else:
            joined = (joined + ' ' + stripped).strip()
    return joined.strip()


def page_has_blockquote_geometry(page, page_height=PAGE_H):
    """Detect consecutive inset text lines before choosing the raw extraction path."""
    blocks = coordinate_redactor(page.get_text('dict')['blocks'], page_height)
    body_left, body_right = _compute_page_text_bounds(blocks)
    continuation_allowed = _page_starts_with_blockquote_continuation(blocks, body_left, body_right)
    for b in blocks:
        if _text_block_is_blockquote(b, body_left, body_right, continuation_allowed):
            return True
        lines = _text_block_lines(b)
        if lines:
            continuation_allowed = False
    return False


def _compute_page_text_bounds(blocks):
    """Return robust body left/right baselines for substantive lines on a page."""
    from collections import Counter

    left_counts = Counter()
    right_counts = Counter()
    for b in blocks:
        if b.get('type') != 0:
            continue
        for line in b.get('lines', []):
            text = _line_text_from_spans(line)
            if len(text) <= 10:
                continue
            if re.fullmatch(r'\d{1,4}', text):
                continue
            left_counts[round(line['bbox'][0])] += 1
            right_counts[round(line['bbox'][2])] += 1

    if not left_counts:
        return 26, None

    # The lowest repeated x0 is the safest body baseline. A pure modal baseline
    # fails on pages mostly occupied by a blockquote, where the quote indent wins.
    repeated_lefts = [x for x, count in left_counts.items() if count >= 2]
    body_left = min(repeated_lefts or left_counts.keys())
    body_right = max(right_counts.keys()) if right_counts else None
    return body_left, body_right


def _line_is_blockquote_candidate(line, text, body_left, body_right=None):
    if not text or len(text) < 8:
        return False
    if re.match(r'^\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]', text):
        return False
    if STRUCTURAL_START_RE.match(text):
        return False
    if re.match(r'^(?:CHAPTER|PART|BOOK|DIGRESSION)\b', text, re.I):
        return False

    x0 = line['bbox'][0]
    x1 = line['bbox'][2]
    if x0 < body_left + BLOCKQUOTE_INSET_THRESHOLD:
        return False
    if body_right is not None and x1 > body_right - BLOCKQUOTE_RIGHT_INSET_THRESHOLD:
        return False
    return True


def _text_block_lines(block):
    lines = []
    if block.get('type') != 0:
        return lines
    for line in block.get('lines', []):
        text = _line_text_from_spans(line)
        if text:
            lines.append((line, text))
    return lines


def _text_block_is_blockquote(block, body_left, body_right=None, allow_continuation=False):
    """Classify blockquotes by the first substantive line, not wrapped continuations."""
    lines = _text_block_lines(block)
    if not lines:
        return False

    if allow_continuation and _text_block_is_reference_tail(block):
        return True

    first_line, first_text = lines[0]
    if not _line_is_blockquote_candidate(first_line, first_text, body_left, body_right):
        return False

    # Avoid promoting ordinary right-shifted fragments unless the whole block
    # has the inset profile or begins with an explicit quotation.
    if re.match(r'^[“"\']', first_text):
        return True
    if not allow_continuation:
        return False

    inset_lines = sum(
        1 for line, text in lines
        if _line_is_blockquote_continuation_candidate(line, text, body_left, body_right)
    )
    return inset_lines == len(lines)


def _line_is_blockquote_continuation_candidate(line, text, body_left, body_right=None):
    if _line_is_blockquote_candidate(line, text, body_left, body_right):
        return True
    if not text:
        return False
    x0 = line['bbox'][0]
    if x0 < body_left + BLOCKQUOTE_INSET_THRESHOLD:
        return False
    # Short closing lines such as "us,”" are real quote continuations, but
    # they are too short for the normal candidate heuristic.
    return bool(re.search(r',?\s*[”"]\s*$', text))


def _text_block_is_fully_inset(block, body_left, body_right=None):
    lines = _text_block_lines(block)
    if not lines:
        return False
    inset_lines = sum(
        1 for line, text in lines
        if _line_is_blockquote_continuation_candidate(line, text, body_left, body_right)
    )
    return inset_lines == len(lines)


def _clean_reference_tail_text(text):
    text = re.sub(r'<\d[A-Za-z0-9]{5}>', '', text)
    return text.strip()


def _is_blockquote_reference_tail_text(text):
    clean = _clean_reference_tail_text(text)
    return bool(re.fullmatch(
        rf'(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+(?:[-,;]\s*\d+)*\.?',
        clean,
        re.I,
    ))


def _text_block_is_reference_tail(block):
    lines = _text_block_lines(block)
    if not lines:
        return False
    text = _join_blockquote_lines([line_text for _, line_text in lines])
    return _is_blockquote_reference_tail_text(text)


def _page_starts_with_blockquote_continuation(blocks, body_left, body_right=None):
    text_blocks = [b for b in blocks if _text_block_lines(b)]
    if not text_blocks:
        return False
    first_text = _join_blockquote_lines([text for _, text in _text_block_lines(text_blocks[0])])
    if _text_block_is_fully_inset(text_blocks[0], body_left, body_right) and re.search(r'[”"]', first_text):
        return True
    if len(text_blocks) < 2:
        return False
    return (
        _text_block_is_fully_inset(text_blocks[0], body_left, body_right) and
        (
            _text_block_is_fully_inset(text_blocks[1], body_left, body_right) or
            _text_block_is_reference_tail(text_blocks[1])
        )
    )


def _quote_run_is_open(text):
    return (
        text.count('“') > text.count('”') or
        text.count('"') % 2 != 0
    )


def _quote_run_expects_reference_tail(text):
    return bool(re.search(r'[”"]\s*$', text)) and not _is_blockquote_reference_tail_text(text)


def _blockquote_content(text):
    return re.sub(r'^\[\[BLOCKQUOTE\]\]\s*', '', text).strip()


def _blockquote_has_sentence_terminal(text):
    content = _blockquote_content(text)
    return bool(re.search(r'[.!?][”"\')\]]?\s*$', content))


def _split_leading_scripture_reference_tail(text):
    """Split a leading scripture reference tail from following prose."""
    match = re.match(
        rf'^(?P<tail>(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+:\d+'
        r'(?:[-,]\s*\d+)*(?:[;,.]\s*\)?)?)'
        r'(?:\s+(?P<rest>.+))?$',
        (text or '').strip(),
        re.I,
    )
    if not match:
        match = re.match(
            rf'^(?P<tail>(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\s+\d+\.?)'
            r'(?:\s+(?P<rest>.+))?$',
            (text or '').strip(),
            re.I,
        )
    if not match:
        return None, None
    return match.group('tail').strip(), (match.group('rest') or '').strip()


def _paragraph_expects_scripture_reference_tail(text):
    stripped = (text or '').strip()
    if not stripped or stripped.startswith('[[BLOCKQUOTE]]'):
        return False
    return bool(
        re.search(r'[?!.][”"\']?\s*$', stripped)
        and (
            re.search(r'[”"]\s*$', stripped)
            or re.search(r'\?\s*$', stripped)
        )
    )


CONNECTOR_STARTERS_RE = re.compile(
    r'^(But|And|Wherefore|Therefore|For|Nevertheless|However|Moreover|Yea|Yet|'
    r'Also|Further|Again|Now|So|Thus|Hence|Consequently)\s+[,;:\-—]?\s*',
    re.I
)

SCRIPTURE_TAIL_RE = re.compile(
    r'[1-3]?\s*(?:GenesisExodusLeviticusNumbersDeuteronomyJoshuaJudgesRuth'
    r'|SamuelKingsChroniclesEzraNehemiahEstherJobPsalms?ProverbsEcclesiastes'
    r'|Song(?: of Solomon)?|IsaiahJeremiahLamentationsEzekielDanielHosea'
    r'|JoelAmosObadiahJonahMicahNahumHabakkukZephaniahHaggaiZechariahMalachi'
    r'|MatthewMarkLukeJohnActsRomans?1?2?Corinthians?Galatians?Ephesians?'
    r'|PhilippiansColossians?1?2?Thessalonians?1?2?TimothyTitusPhilemon'
    r'|HebrewsJames?1?2?Peter?1?2?3?JohnJudeRevelation)'
    r'\s*\d+:\d+(?:-\d+)?(?:,\s*\d+(?::\d+(?:-\d+)?)?)*\.?\s*$',
    re.I
)


def extract_ages_nav(doc, config=None):
    """
    Extract navigation hierarchy from the PDF's internal outline/bookmarks.
    Returns list of (level, title, page_num_0indexed).
    
    Falls back to parsing the visual 'CONTENTS OF VOLUME' page if outline is empty.
    """
    toc = doc.get_toc()
    if toc:
        nav = []
        for item in toc:
            level, title, page = item
            if page < 1:
                continue  # skip entries with no page (-1)
            nav.append((level, title.strip(), page - 1))  # convert to 0-indexed
        if nav:
            return nav

    # Fallback: parse the visual TOC from the CONTENTS page
    for pg in range(len(doc)):
        page = doc[pg]
        text = page.get_text()
        if 'CONTENTS OF VOLUME' in text:
            return _parse_visual_toc(doc, pg, config=config)
    return []


def _parse_visual_toc(doc, toc_page_num, config=None):
    """
    Parse the visual 'CONTENTS OF VOLUME' page to extract chapter titles
    and map them to PDF page numbers.
    """
    from collections import OrderedDict
    nav = []
    page = doc[toc_page_num]
    blocks = page.get_text('dict')['blocks']
    
    lines = []
DANGLING_CONNECTOR_RE = re.compile(
    r'\b(?:and|the|of|for|with|in|to|a|is|was|were|be|been|being|has|have|had|'
    r'by|from|as|at|or|which|who|whom|this|that|these|those)\s*$',
    re.I
)

