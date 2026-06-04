import re
from shared import _repair_owen_ocr_errors, STRUCTURAL_START_RE
from scripts.roman_parser import _roman_head_match

def _polish_analysis_html(html: str) -> str:
    """Keep front-matter analysis outlines compact instead of heading-heavy."""
    if not html:
        return html
    return re.sub(
        r'<h4 class="roman-subheading">(.*?)</h4>',
        r'<p class="roman-list-item">\1</p>',
        html,
        flags=re.I | re.S,
    )










def _looks_like_summary_body_start(text: str) -> bool:
    """Detect the first real body paragraph after a chapter summary."""
    if not text:
        return False
    plain = re.sub(r'\*\*(.+?)\*\*', r'\1', text).strip()
    plain = re.sub(r'\s+', ' ', plain)
    # Owen chapters commonly begin with a drop-cap all-caps word followed by
    # ordinary prose.  Keep this strict so all-caps summary fragments survive.
    if re.match(r'^(?:THE|WE|I|THIS|THAT|THERE|BEING|HAVING)\b\s+[a-zA-Z]', plain):
        return True
    # Some body sections begin with an outline word followed by the all-caps
    # drop word from the source page: "Secondly, THE human nature..."
    if re.match(
        r'^(?:First|Firstly|Secondly|Thirdly|Fourthly|Fifthly|Sixthly|Lastly),?\s+THE\b',
        plain,
        re.I,
    ):
        return True
    return False


def _looks_like_summary_continuation(text: str) -> bool:
    """Return True for summary fragments that continue after a [[SUMMARY]] tag."""
    if not text:
        return False
    plain = re.sub(r'\*\*(.+?)\*\*', r'\1', text).strip()
    if not plain or _looks_like_summary_body_start(plain):
        return False
    if plain.startswith(('—', '–', '-')):
        # Explicit continuation marker — synopsis fragments that overflow onto
        # the next PDF page always begin with an em/en-dash in Owen.
        return True
    if re.match(r'^[\u0370-\u03FF\u1F00-\u1FFF]', plain):
        return True
    if STRUCTURAL_START_RE.match(plain):
        return not bool(
            _roman_head_match(plain)
            and len(re.findall(r'\w+', (_roman_head_match(plain).group('rest') or ''))) >= 8
        )
    # Long synopsis continuations often contain em-dash-separated clauses but
    # are not outline/body paragraphs yet.  Require mostly uppercase — Owen
    # synopses are all-caps; mixed-case body prose with em-dashes must not be
    # absorbed (e.g. "Our blessed Savior — as he was usually...").
    if '—' in plain:
        _letters = [c for c in plain if c.isalpha()]
        _upper_ratio = (
            sum(1 for c in _letters if c.isupper()) / len(_letters)
            if _letters else 0
        )
        return len(re.findall(r'\w+', plain)) >= 8 and _upper_ratio >= 0.65
    return False


def _prepare_analysis_raw_text(raw_text: str) -> str:
    """Normalize Analysis chapters into a stable outline before rendering.

    The AGES PDFs often flatten front-matter analysis pages into prose. This
    keeps the fix shared across volumes instead of relying on v2-only JSON
    rewrites.
    """
    if not raw_text:
        return raw_text

    text = raw_text
    text = re.sub(r'\*\*(Part\s+[IVXLCDM]+)\*\*\s*\.', r'[[PART]] \1.', text, flags=re.I)
    text = re.sub(r'\*\*(Part\s+[IVXLCDM]+\.)\*\*', r'[[PART]] \1', text, flags=re.I)
    text = re.sub(r'(?m)^(?!\[\[PART\]\]\s*)(Part\s+[IVXLCDM]+\.?\s*[—\-])', r'[[PART]] \1', text, flags=re.I)
    text = re.sub(r'(?<!\n)(\s+)(\[\[PART\]\]\s*Part\s+[IVXLCDM]+\.?)', r'\n\n\2', text, flags=re.I)
    text = re.sub(
        r'(?m)^(?!\[\[)([IVXLCDM]{1,8}\.\s+(?:Communion|It\s+is\s+shown|and\s+practical|'
        r'The\s+foundation|His\s+gracious|The\s+elements|The\s+effects|General\s+inferences)\b)',
        r'[[ROMAN_HEAD]] \1',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'([,;])\s+([IVXLCDM]{1,8}\.\s+(?:Communion|It\s+is\s+shown|and\s+practical)\b)',
        r'\1\n\n[[ROMAN_HEAD]] \2',
        text,
        flags=re.I,
    )
    return text


def _repair_analysis_spillover_chapters(intermediate: dict) -> dict:
    """Move prose accidentally captured before ANALYSIS back to the prior chapter.

    AGES occasionally cuts a front-matter paragraph at the page where the
    ANALYSIS title begins, producing one chapter that starts with the previous
    sentence tail and only later says "ANALYSIS".  Rendering can repair this
    without rewriting the cached JSON.
    """
    chapters = intermediate.get('chapters') or []
    for index, chapter in enumerate(chapters):
        if index == 0 or 'ANALYSIS' not in (chapter.get('title') or '').upper():
            continue
        raw_text = chapter.get('raw_text') or ''
        if not raw_text or raw_text.lstrip().startswith('[['):
            continue
        match = re.search(r'\bANALYSIS\.?\s*', raw_text, re.I)
        if not match or match.start() < 80:
            continue
        spill = raw_text[:match.start()].strip()
        analysis_body = raw_text[match.end():].strip()
        if not spill or not analysis_body:
            continue

        previous = chapters[index - 1]
        previous_raw = (previous.get('raw_text') or '').rstrip()
        separator = ' ' if previous_raw and not re.search(r'[.!?]["”\')\]]?\s*$', previous_raw) else '\n\n'
        previous['raw_text'] = f'{previous_raw}{separator}{spill}'.strip()
        chapter['raw_text'] = f'[[SUBTITLE]] ANALYSIS.\n\n{analysis_body}'
    return intermediate


def _merge_reference_continuation_paragraphs(paragraphs: list[str]) -> list[str]:
    """Heal paragraph breaks inserted between "chap." and a following locator."""
    merged: list[str] = []
    for para in paragraphs:
        current = para.strip()
        if not current:
            continue
        if (
            merged
            and re.search(r'\b(?:chap|chapter)\.?\s*$', merged[-1], re.I)
            and re.match(r'^\d{1,3}:\d+(?:[-,]\s*\d+)*[,:;]?\b', current)
        ):
            merged[-1] = f'{merged[-1].rstrip()} {current}'
        else:
            merged.append(current)
    return merged


