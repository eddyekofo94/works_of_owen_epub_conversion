import re
from shared import (
    FOOTNOTE_MARKER_RE,
    SCRIPTURE_REF_RE,
    SCRIPTURE_BOOK_RE,
    _norm_for_dedupe,
)


def _split_inline_catechism_questions(paragraphs, allow_bare_a=False):
    out = []
    # Split on space followed by Q./Ques. or A./Ans. markers
    # Supports optional bold ** markers.
    # NOTE: Case-sensitive to avoid catching scholarly citations like 'q. 81' (Issue 17)
    answer_marker = r'A\.|' if allow_bare_a else ''
    pattern = re.compile(
        rf'(?<!^)\s+(?=(?:\*\*)?(?:Q\.|Ques\.|{answer_marker}Ans\.)\s*(?:\d+\.)?\s*(?:\*\*)?)'
    )
    for para_idx, para in enumerate(paragraphs):
        parts = [part.strip() for part in pattern.split(para) if part.strip()]
        out.extend(parts or [para])
    return out


def _is_catechism_scripture_spill(text):
    clean = re.sub(r'\[f\d+\]', ' ', text)
    if re.match(r'^(?:\*\*)?[QA]\.', clean.strip()):
        return False
    has_ref_code = bool(re.search(r'<[0-9A-Fa-f]{6}>', clean))
    has_ref = bool(SCRIPTURE_REF_RE.search(clean))
    if not (has_ref_code or has_ref):
        return False
    clean = re.sub(r'<[0-9A-Fa-f]{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(
        rf'\b(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b|\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+\b',
        ' ',
        clean,
        flags=re.I,
    )
    leftovers = re.sub(r'[;:,.()\-\s]', '', clean)
    return len(leftovers) <= 20


def _answer_head(text):
    clean = FOOTNOTE_MARKER_RE.sub(' ', text)
    clean = re.sub(r'<[0-9A-Fa-f]{6}>', ' ', clean)
    clean = SCRIPTURE_REF_RE.sub(' ', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    match = re.match(r'^(?:\*\*)?A\.(?:\*\*)?\s+(.{5,120}?[.!?;])', clean, re.I)
    return _norm_for_dedupe(match.group(1)) if match else ''


def _clean_catechism_footnote_spill(paragraphs):
    out = []
    in_catechism = False
    last_answer_head = ''
    for para_idx, para in enumerate(paragraphs):
        stripped = para.strip()
        if re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            in_catechism = True
            last_answer_head = ''
        if in_catechism and _is_catechism_scripture_spill(stripped):
            continue
        current_answer_head = _answer_head(stripped)
        if in_catechism and current_answer_head and current_answer_head == last_answer_head:
            continue
        out.append(para)
        if current_answer_head:
            last_answer_head = current_answer_head
        elif re.search(r'(?:\*\*)?Q\.\s*\d+\.', stripped):
            last_answer_head = ''
    return out


def _remove_catechism_lookahead_ghosts(paragraphs):
    """Remove text that was pulled forward from following paragraphs (AGES ghosting)."""
    cleaned = list(paragraphs)
    for idx, para in enumerate(cleaned[:-1]):
        # Look ahead up to 6 paragraphs for ghosting
        for offset in range(1, min(7, len(cleaned) - idx)):
            next_para = cleaned[idx + offset].strip()
            if not next_para:
                continue

            curr_words = [
                (m.group(0).lower(), m.start(), m.end())
                for m in re.finditer(r"[A-Za-z0-9:]+", para)
            ]
            next_words = [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9:]+", next_para)]
            if len(curr_words) < 8 or len(next_words) < 6:
                continue

            best = None
            max_size = min(18, len(curr_words), len(next_words))
            for size in range(max_size, 5, -1):
                next_runs = {tuple(next_words[j:j + size]) for j in range(len(next_words) - size + 1)}
                for i in range(1, len(curr_words) - size + 1):
                    run = tuple(w for w, _, _ in curr_words[i:i + size])
                    if run in next_runs:
                        best = (curr_words[i][1], curr_words[i + size - 1][2])
                        break
                if best:
                    break

            if best:
                start, end = best
                while start > 0 and para[start - 1] in ' \t,;:':
                    start -= 1
                while end < len(para) and para[end] in ' \t,;:.':
                    end += 1
                para = re.sub(r'\s{2,}', ' ', (para[:start] + ' ' + para[end:]).strip())
                cleaned[idx] = para
    return cleaned


def _remove_duplicate_catechism_answer_opening(text):
    """Collapse ghosted catechism answer openings inside one paragraph."""
    # Pattern: A. Body text. A. Body text.
    pattern = re.compile(
        r'^(?P<label>(?:\*\*)?(?:A\.|Ans\.|Q\.|Ques\.)(?:\*\*)?\s*(?:\d+\.)?\s*)'
        r'(?P<body>.{6,180}?[.!?;])\s+'
        r'(?:\*\*)?(?:A\.|Ans\.|Q\.|Ques\.)(?:\*\*)?\s*(?:\d+\.)?\s*(?P=body)',
        re.I,
    )
    previous = None
    while previous != text:
        previous = text
        text = pattern.sub(r'\g<label>\g<body>', text)
    return text
