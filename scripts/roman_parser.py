import re
from html import escape as _html_escape
from shared import ROMAN_ONLY_RE, ROMAN_LIST_TOKEN

def _clean_heading_text(text):
    """Remove stray markdown emphasis markers from extracted heading text."""
    text = (text or '').replace('*', '')
    return re.sub(r'\s+', ' ', text).strip()


def _roman_to_int(roman):
    values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    previous = 0
    for char in reversed(roman.rstrip('.').upper()):
        value = values.get(char, 0)
        if value < previous:
            total -= value
        else:
            total += value
            previous = value
    return total


def _is_roman_list_item(text):
    stripped = text.strip()
    if not stripped or stripped.startswith('#') or ROMAN_ONLY_RE.match(stripped):
        return False
    if len(re.findall(r'\w+', stripped)) > 28:
        return False
    return bool(re.search(r'[.!?:;]"?\s*$', stripped))


def _roman_head_match(text):
    # Exclude well-known scholarly abbreviations that are composed entirely of
    # Roman-numeral letters (LXX, MT, OT, NT, DV, KJV, AV, NIV, ESV, NRSV).
    # Also exclude any Roman value > L (50) in body text — large values like LXX (70)
    # are virtually never section headings in Owen; they are abbreviations.
    _EXCLUSION = r'(?!\*{0,2}(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\*{0,2}[.\s])'
    m = re.match(
        _EXCLUSION + r'^(?:\*\*)?(?P<roman>[IVXLCDM]+\.)(?:\*\*)?(?:\s+(?P<rest>.*))?$',
        (text or '').strip(),
    )
    if m and _roman_to_int(m.group('roman')) > 50:
        return None
    return m


def _roman_decimal_marker_match(text):
    """Match combined outline markers such as "I. 1." without splitting them."""
    return re.match(
        r'^(?P<marker>(?:\*\*)?[IVXLCDM]+\.(?:\*\*)?\s+\d+\.)(?:\s+(?P<rest>.+))?$',
        (text or '').strip(),
    )


def _starts_roman_outline(previous_text, roman_number):
    if roman_number != 1:
        return False
    return bool(
        re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
        or re.search(r'(?:[—-]|,)\s*$', previous_text)
    )


def _is_roman_outline_entry(roman_text, previous_text, expected_roman_number):
    match = _roman_head_match(roman_text)
    if not match:
        return False, None
    roman_number = _roman_to_int(match.group('roman'))
    rest = (match.group('rest') or '').strip()
    if not rest:
        return False, None
    if (
        (_starts_roman_outline(previous_text, roman_number) or expected_roman_number == roman_number)
        and _is_roman_list_item(rest)
    ):
        return True, roman_number + 1
    return False, None


def _render_simple_roman_heading_content(raw_content):
    from render import tag_unicode_ranges
    match = _roman_head_match(raw_content)
    if not match:
        return tag_unicode_ranges(_html_escape(_clean_heading_text(raw_content)))
    roman_html = f'<b>{_html_escape(match.group("roman"))}</b>'
    rest = _clean_heading_text(match.group('rest') or '')
    if not rest:
        return roman_html
    return f'{roman_html} {tag_unicode_ranges(_html_escape(rest))}'


def _split_roman_section_opening(text):
    match = _roman_head_match(text)
    if not match:
        return None
    rest = (match.group('rest') or '').strip()
    if re.match(r'^(?:and|or|&)\s+[IVXLCDM]+', rest, re.I):
        return None
    if len(re.findall(r'\w+', rest)) < 12:
        return None
    heading = match.group("roman")
    body = rest
    return heading, body


def _strip_markdown_heading_marker(text):
    return re.sub(r'^\s*#{1,6}\s+', '', text.strip())


def _coalesce_roman_list_paragraphs(paragraphs):
    """Join outline-like roman list labels with their short item text."""
    out = []
    expected_roman_number = None
    i = 0

    while i < len(paragraphs):
        stripped = paragraphs[i].strip()
        roman_source = _strip_markdown_heading_marker(stripped)
        roman_match = ROMAN_ONLY_RE.match(roman_source)
        if roman_match and i + 1 < len(paragraphs):
            roman_number = _roman_to_int(roman_match.group('roman'))
            previous_text = out[-1].strip() if out else ''
            starts_list = (
                roman_number == 1
                and (
                    re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                    or re.search(r'(?:[—-]|,)\s*$', previous_text)
                )
            )
            continues_list = expected_roman_number == roman_number

            if (starts_list and _is_roman_list_item(paragraphs[i + 1])) or continues_list:
                out.append(f'{ROMAN_LIST_TOKEN} {roman_match.group("roman")} {paragraphs[i + 1].strip()}')
                expected_roman_number = roman_number + 1
                i += 2
                continue

        if roman_match:
            expected_roman_number = None
        out.append(paragraphs[i])
        i += 1

    return out
