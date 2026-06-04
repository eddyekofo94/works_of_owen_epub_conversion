import re

# ================================================================
# RENDER-ONLY CONSTANTS (not used by extract.py)

# Raw string used in _SCHOLASTIC_ANCHOR_SPLIT_RE and apply_scholastic_anchor_protocol
_SCHOLASTIC_LABEL_RE = (
    r'(?:Obj(?:ection)?\.?\s*\d*\.?|Ans(?:wer)?\.?\s*\d*\.?|'
    r'Sol(?:ution)?\.?\s*\d*\.?|Use\.?\s*\d+\.?|Usus\.?\s*\d+\.?|'
    r'Application\.?\s*\d+\.?)'
)

_SCHOLASTIC_ANCHOR_SPLIT_RE = re.compile(
    r'([.!?"\u201d])\s+'           # closing punctuation / quote
    r'(?P<label>'
    + _SCHOLASTIC_LABEL_RE +
    r')\s',
    re.I,
)

# Pattern to detect "Objection ." (space before period) — OCR artifact
_SCHOLASTIC_SPACE_DOT_RE = re.compile(
    r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application)\s+\.',
    re.I,
)






def _get_scholastic_subclass(label_text: str) -> str:
    label_upper = label_text.upper()
    if any(w in label_upper for w in ['OBJ', 'USE', 'USUS', 'APPLICATION', 'INQUIRY']):
        return 'scholastic-anchor-parent'
    if any(w in label_upper for w in ['ANS', 'SOL', 'RESPONSE']):
        return 'scholastic-anchor-child'
    return 'scholastic-anchor-child'  # default fallback is child


def _nest_scholastic_in_divs(html: str) -> str:
    """Group consecutive scholastic-anchor-child paragraphs and nest them in a <div class="owen-branch owen-level-2">
    container under their preceding introducing paragraph/objection, ensuring proper vertical border and indentation.
    """
    import re
    # 1. Promote level-1 divs that start with a scholastic child anchor to level-2
    html = re.sub(
        r'<div class="owen-branch owen-level-1">\s*(<p\b[^>]*class="[^"]*scholastic-anchor-child[^"]*")',
        r'<div class="owen-branch owen-level-2">\n\1',
        html,
        flags=re.I
    )

    # 2. Token-based wrapping for any remaining top-level scholastic child anchors
    token_re = re.compile(
        r'(<div\b[^>]*>|</div>|<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )
    
    tokens = []
    last_idx = 0
    for m in token_re.finditer(html):
        inter = html[last_idx:m.start()]
        if inter:
            tokens.append(inter)
        tokens.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:]
    if tail:
        tokens.append(tail)

    def is_scholastic_child(t: str) -> bool:
        if not t.startswith('<p') or not t.endswith('</p>'):
            return False
        m = re.match(r'^<p\b[^>]*class="([^"]*)"', t)
        if m:
            classes = m.group(1).split()
            return 'scholastic-anchor-child' in classes
        return False

    def is_whitespace(t: str) -> bool:
        return not t.strip()

    output_tokens = []
    active_divs = []
    i = 0
    n = len(tokens)
    while i < n:
        token = tokens[i]
        if token.startswith('<div'):
            m_div = re.match(r'^<div\b[^>]*class="([^"]*)"', token)
            div_classes = m_div.group(1).split() if m_div else []
            level = 0
            for c in div_classes:
                if c.startswith('owen-level-'):
                    try:
                        level = int(c.split('-')[-1])
                    except ValueError:
                        pass
            active_divs.append(level)
            output_tokens.append(token)
            i += 1
        elif token == '</div>':
            if active_divs:
                active_divs.pop()
            output_tokens.append(token)
            i += 1
        elif is_scholastic_child(token):
            current_level = active_divs[-1] if active_divs else 0
            if current_level >= 2:
                output_tokens.append(token)
                i += 1
            else:
                seq_indices = [i]
                j = i + 1
                while j < n:
                    if is_scholastic_child(tokens[j]):
                        seq_indices.append(j)
                        j += 1
                    elif is_whitespace(tokens[j]):
                        j += 1
                    else:
                        break
                
                end_idx = seq_indices[-1]
                output_tokens.append('<div class="owen-branch owen-level-2">')
                for idx in range(i, end_idx + 1):
                    output_tokens.append(tokens[idx])
                output_tokens.append('</div>')
                i = end_idx + 1
        else:
            output_tokens.append(token)
            i += 1
            
    return "".join(output_tokens)


def apply_scholastic_anchor_protocol(html: str) -> str:
    """Post-processor: ensure Obj./Ans./Use. labels start their own paragraphs
    and sequentially chain bare ordinals following a starting scholastic label.

    Runs on the assembled chapter XHTML string after markdown_to_html().
    """
    # 1. Remove stray space before period in scholastic labels
    html = _SCHOLASTIC_SPACE_DOT_RE.sub(lambda m: m.group(1) + '.', html)

    # 2. Force paragraph break before scholastic labels that appear mid-paragraph
    def _split_before_label(m: re.Match) -> str:
        return f'{m.group(1)}</p>\n<p class="scholastic-anchor"><b>{m.group("label")}</b> '

    html = _SCHOLASTIC_ANCHOR_SPLIT_RE.sub(_split_before_label, html)

    # 3. Clean up leading <b> tags around Obj./Ans. abbreviations to expose them as plain text
    # e.g., <b>Ans.</b> 1. -> Ans. 1.
    def _strip_b_tags(m: re.Match) -> str:
        label_word = m.group(2)
        digit_part = m.group(3)
        return f'{m.group(1)}{label_word} {digit_part} '

    _STRIP_B_RE = re.compile(
        r'(<p(?:\s[^>]*)?>)\s*<b>\s*(Obj(?:ection)?\.?|Ans(?:wer)?\.?|Sol(?:ution)?\.?|Use\.?|Usus\.?|Application\.?)\s*</b>\s*(\d+\.?)\s*',
        re.I
    )
    html = _STRIP_B_RE.sub(_strip_b_tags, html)

    # 4. Bold all scholastic labels at paragraph start (improved original step)
    def _clean_scholastic_label(label: str) -> str:
        label = re.sub(r'\s+', ' ', label).strip()
        label = re.sub(r'\s+\.', '.', label)
        label = re.sub(r'\.(?=\d)', '. ', label)
        return label

    html = re.sub(
        r'(<p(?:\s[^>]*)?>)\s*'
        r'(?P<label>' + _SCHOLASTIC_LABEL_RE + r')\s',
        lambda m: f'{m.group(1)}<b class="scholastic-label">{_clean_scholastic_label(m.group("label"))}</b> ',
        html,
        flags=re.I,
    )

    # 5. Standardize paragraph class to "scholastic-anchor" for all scholastic labels
    _SCHOLASTIC_ANCHOR_PARA_RE = re.compile(
        r'<p\s+class="([^"]*)"([^>]*)>\s*(<b class="scholastic-label">.*?</b>)',
        re.I
    )
    def _add_anchor_class(m: re.Match) -> str:
        classes = m.group(1).split()
        filtered = [c for c in classes if not (c.startswith('list-') or c == 'roman-list-item')]
        if 'scholastic-anchor' not in filtered:
            filtered.append('scholastic-anchor')
            
        label_content = re.sub(r'<[^>]+>', '', m.group(3))
        subclass = _get_scholastic_subclass(label_content)
        if subclass not in filtered:
            filtered.append(subclass)
            
        return f'<p class="{" ".join(filtered)}"{m.group(2)}>{m.group(3)}'

    html = _SCHOLASTIC_ANCHOR_PARA_RE.sub(_add_anchor_class, html)

    # Add class to bare paragraphs starting with a scholastic label
    def _add_bare_anchor_class(m: re.Match) -> str:
        label_content = re.sub(r'<[^>]+>', '', m.group(1))
        subclass = _get_scholastic_subclass(label_content)
        return f'<p class="scholastic-anchor {subclass}">{m.group(1)}'

    html = re.sub(
        r'<p>\s*(<b class="scholastic-label">.*?</b>)',
        _add_bare_anchor_class,
        html,
        flags=re.I
    )

    # 6. Smart Scholastic Chain State Machine
    lines = html.split('\n')
    out = []
    active_prefix = None
    expected_idx = None

    for line in lines:
        stripped = line.strip()
        
        m_label = re.search(
            r'<p[^>]*class="[^"]*scholastic-anchor[^"]*"[^>]*>\s*<b class="scholastic-label">(Obj|Ans|Sol|Use|Usus|Application)\.\s*(\d+)\.</b>',
            stripped,
            re.I
        )
        if m_label:
            active_prefix = m_label.group(1)
            expected_idx = int(m_label.group(2)) + 1
            out.append(line)
            continue

        if active_prefix and expected_idx is not None:
            m_digit = re.search(
                r'(<p\s+class=")([^"]*)("[^>]*>\s*)<b>(\d+)\.</b>\s*(.*)',
                line,
                re.I
            )
            if m_digit:
                digit_val = int(m_digit.group(4))
                if digit_val == expected_idx:
                    classes = m_digit.group(2).split()
                    filtered = [c for c in classes if not (c.startswith('list-') or c == 'roman-list-item')]
                    subclass = _get_scholastic_subclass(active_prefix)
                    if 'scholastic-anchor' not in filtered:
                        filtered.append('scholastic-anchor')
                    if subclass not in filtered:
                        filtered.append(subclass)

                    rewritten_line = (
                        f'{m_digit.group(1)}{" ".join(filtered)}{m_digit.group(3)}'
                        f'<b class="scholastic-label">{active_prefix.capitalize()}. {digit_val}.</b> {m_digit.group(5)}'
                    )
                    out.append(rewritten_line)
                    expected_idx += 1
                    continue

        if '<h' in stripped or '<hr' in stripped:
            active_prefix = None
            expected_idx = None

        out.append(line)

    combined_html = '\n'.join(out)
    return _nest_scholastic_in_divs(combined_html)
