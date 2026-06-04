import re

def _remove_adjacent_duplicates(text):
    """Remove ghost-layer duplicates — identical lines only (fast)."""
    if not text or len(text) < 40:
        return text
    lines = text.split('\n')
    # Single pass: remove any line that's identical to one of the
    # next 5 lines (ghost layers in pymupdf4llm are usually within
    # a few lines of each other, separated by blanks).
    out = []
    skip = set()
    for i, line in enumerate(lines):
        if i in skip:
            continue
        if len(line) >= 20:
            for j in range(i + 1, min(i + 6, len(lines))):
                if lines[j] == line:
                    skip.add(j)
        out.append(line)
    return '\n'.join(out)


def _remove_adjacent_line_overlaps(text):
    """Trim ghost-layer overlaps where the next line repeats the prior line tail."""
    if not text or len(text) < 40:
        return text

    def words_with_spans(value):
        return [
            (m.group(0).lower(), m.start(), m.end())
            for m in re.finditer(r"[A-Za-z0-9:;,''\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+", value)
        ]

    lines = text.split('\n')
    out = []
    for line in lines:
        if not out or not line.strip():
            out.append(line)
            continue

        # Find the last non-empty line in out
        last_non_empty = None
        for prev_line in reversed(out):
            if prev_line.strip():
                last_non_empty = prev_line
                break

        if last_non_empty is None:
            out.append(line)
            continue

        prev_words = words_with_spans(last_non_empty)
        curr_words = words_with_spans(line)
        max_overlap = min(8, len(prev_words), len(curr_words))
        trim_at = None
        for size in range(max_overlap, 1, -1):
            if [w for w, _, _ in prev_words[-size:]] != [w for w, _, _ in curr_words[:size]]:
                continue
            overlap_text = line[curr_words[0][1]:curr_words[size - 1][2]]
            if len(overlap_text) >= 12:
                trim_at = curr_words[size - 1][2]
                break

        if trim_at is not None:
            line = line[trim_at:].lstrip(' ,;:.')
        out.append(line)

    return '\n'.join(out)
