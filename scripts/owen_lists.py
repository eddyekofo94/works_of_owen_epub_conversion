import re

# ---------------------------------------------------------------------------
# Issue #16 — em-dash / open-punctuation flat syllabus flattening
# ---------------------------------------------------------------------------
def _attach_em_dash_flat_list(html: str, config: dict = None) -> str:
    """Absorb short Owenian flat-list prefixes into a preceding em-dash anchor.

    Signals
    -------
    F  — announced count exactly matches run length, ≤20 w per item
    H  — ≥3 items, all end '.', all ≤25 w
    G  — single-item ordinal that continues an existing inline ordinal sequence
    all_non_final_semi — every non-final item ends ';', non-final ≤20 w
    cont-comma — non-final item ends ',' → final item joins regardless of length
    cont-connector — non-final item ends 'and'/'or' → same
    A  — non-final item ends ';' or ',', ≤12 w (hard cap, Bug #6 raised from 8)
    B  — any item ends 'and'/'or', ≤12 w
    C  — all items ≤3 w
    D  — ≥3 items, all ≤7 w
    """
    if not html:
        return html

    if config and config.get('chapter_title') in config.get('flat_list_exclude_chapters', []):
        return html

    import re as _re

    def _parse_roman(s: str) -> int:
        s = s.upper().strip('.,:;()[]')
        if not s or not _re.match(r'^[IVXLCDM]+$', s):
            return 0
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        val = 0
        prev_val = 0
        for char in reversed(s):
            curr_val = roman_map.get(char, 0)
            if curr_val >= prev_val:
                val += curr_val
            else:
                val -= curr_val
            prev_val = curr_val
        return val

    def _get_marker_val_and_type(marker_text: str) -> tuple[str, int]:
        clean = _re.sub(r'<[^>]+>', '', marker_text).strip()
        clean = clean.strip('.,:; \t\n\r*')
        if not clean:
            return ('empty', 0)
        
        clean_upper = clean.upper()
        
        if clean.startswith('(') and clean.endswith(')'):
            inner = clean[1:-1].strip('.,:; ')
            if inner.isdigit():
                return ('arabic_paren', int(inner))
            if len(inner) == 1 and inner.isalpha():
                return ('alpha_paren', ord(inner.lower()) - ord('a') + 1)
            roman_val = _parse_roman(inner)
            if roman_val > 0:
                return ('roman_paren', roman_val)
                
        if clean.startswith('[') and clean.endswith(']'):
            inner = clean[1:-1].strip('.,:; ')
            if inner.isdigit():
                return ('arabic_bracket', int(inner))
            if len(inner) == 1 and inner.isalpha():
                return ('alpha_bracket', ord(inner.lower()) - ord('a') + 1)
            roman_val = _parse_roman(inner)
            if roman_val > 0:
                return ('roman_bracket', roman_val)

        w = clean_upper
        if 'FIRST' in w or '1ST' in w: return ('ordinal', 1)
        if 'SECOND' in w or '2ND' in w or '2DLY' in w: return ('ordinal', 2)
        if 'THIRD' in w or '3RD' in w or '3DLY' in w: return ('ordinal', 3)
        if 'FOURTH' in w or '4TH' in w or '4THLY' in w: return ('ordinal', 4)
        if 'FIFTH' in w or '5TH' in w or '5THLY' in w: return ('ordinal', 5)
        if 'SIXTH' in w or '6TH' in w: return ('ordinal', 6)
        if 'SEVENTH' in w or '7TH' in w: return ('ordinal', 7)
        if 'EIGHTH' in w or '8TH' in w: return ('ordinal', 8)
        if 'NINTH' in w or '9TH' in w: return ('ordinal', 9)
        if 'TENTH' in w or '10TH' in w: return ('ordinal', 10)

        if clean.isdigit():
            return ('arabic_bare', int(clean))
            
        roman_val = _parse_roman(clean)
        if roman_val > 0:
            return ('roman_bare', roman_val)
            
        if len(clean) == 1 and clean.isalpha():
            return ('alpha_bare', ord(clean.lower()) - ord('a') + 1)
            
        return ('unknown', 0)

    def _is_sequential_sequence(pairs) -> bool:
        parsed = [_get_marker_val_and_type(mk) for mk, _ in pairs]
        known_parsed = [(t, v) for t, v in parsed if t != 'unknown' and t != 'empty' and v > 0]
        if len(known_parsed) < 2:
            return True
            
        first_type = known_parsed[0][0]
        if not all(t == first_type for t, _ in known_parsed):
            return False
            
        for idx in range(1, len(known_parsed)):
            if known_parsed[idx][1] <= known_parsed[idx-1][1]:
                return False
        return True


    # ── caps ─────────────────────────────────────────────────────────────────
    _HARD_CAP     = 12   # base cap raised from 8 (Bug #6)
    _SIGNAL_F_CAP = config.get('list_item_merge_cap', 20) if config else 20   # exact announced-count match (tightened 2026-05-27)
    _SIGNAL_H_CAP = 25   # preview-syllabus: ≥3 items, all end '.', all ≤25 w
    _ALL_SEMI_CAP = 20   # all_non_final_semi: non-final items must be ≤20 w
    _ANCHOR_LIMIT = 80   # max plain words in a list-item anchor for auto-attach

    # ── patterns ─────────────────────────────────────────────────────────────
    _EXPLICIT_COUNT_RE = _re.compile(
        r'\b(?:I\s+understand\s+)?(?:two|three|four|five|six|seven|'
        r'eight|nine|ten|twofold|threefold|fourfold|\d+)\b.{0,120}'
        r'\b(?:things?|ways?|heads?|accounts?|regards?|parts?|'
        r'sorts?|considerations?|observations?|particulars?|'
        r'respects?|instances?)\b.{0,100}[—\-:,;.]\s*$',
        _re.I,
    )
    _FORMULA_TAIL_RE = _re.compile(
        r'\b(?:these?\s+following|as\s+follows?|following\s+particulars?|'
        r'(?:may|to)\s+be\s+(?:observed|noted|considered|mentioned)|'
        r'I\s+shall\s+(?:observe|note|propose|mention|consider)|'
        r'in\s+particular|are\s+these|namely\s+these|namely,\s+these)\b.{0,60}[—\-:,;.]\s*$',
        _re.I,
    )
    _LIST_ITEM_RE = _re.compile(
        r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
        _re.S,
    )
    # Ordinal markers: (1st.), (2ndly.), 3rdly., etc.
    _ORDINAL_MK_RE = _re.compile(
        r'^\(?(?:\d+(?:(?:st|nd|rd|th)ly?|dly|ly)|1st|2nd(?:ly)?|'
        r'3rd(?:ly)?|4th(?:ly)?)\.?\)?\.?$',
        _re.I,
    )
    # Detect inline ordinals already embedded in a preceding paragraph
    _HAS_INLINE_ORDINAL_RE = _re.compile(
        r'\((?:1st|2nd(?:ly|dly)?|3rd(?:ly|dly)?|4th(?:ly)?|5th(?:ly)?)\.\)',
        _re.I,
    )

    # ── helpers ───────────────────────────────────────────────────────────────
    def _plain(frag: str) -> str:
        import html as _html
        text = _re.sub(r'<[^>]+>', '', frag)
        text = _html.unescape(text)
        return _re.sub(r'\s+', ' ', text).strip()

    def _wc(frag: str) -> int:
        return len(_plain(frag).split())

    def _strip_marker(text: str) -> str:
        text = _re.sub(r'^\s*(?:[IVXLCDM]+|\d+)\s*[\).:]\s*', '', text, flags=_re.I)
        text = _re.sub(r'^\s*\(\s*(?:[IVXLCDM]+|\d+)\.?\s*\)\s*', '', text, flags=_re.I)
        text = _re.sub(r'^\s*\[\s*(?:[IVXLCDM]+|\d+)\.?\s*\]\s*', '', text, flags=_re.I)
        return text.strip()

    def _extract_count(text: str) -> int:
        """Return announced count only when text matches _EXPLICIT_COUNT_RE."""
        if not _EXPLICIT_COUNT_RE.search(text):
            return 0
        cleaned = _strip_marker(text)
        m = _re.search(
            r'\b(two|three|four|five|six|seven|eight|nine|ten|'
            r'twofold|threefold|fourfold|\d+)\b',
            cleaned, _re.I,
        )
        if not m:
            return 0
        w = m.group(1).lower()
        if w.isdigit():
            return int(w)
        return {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
                'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                'twofold': 2, 'threefold': 3, 'fourfold': 4}.get(w, 0)

    def _allows_attach(plain: str, is_list_item: bool = False) -> bool:
        plain = plain.strip()
        if not plain:
            return False
        if _re.search(r'\bwhereby\b', plain, _re.I):
            return False
        if is_list_item:
            stripped = _strip_marker(plain)
            body_wc = len(stripped.split())
            if body_wc > _ANCHOR_LIMIT:
                if not (_EXPLICIT_COUNT_RE.search(stripped) or _FORMULA_TAIL_RE.search(stripped)):
                    return False
            last = stripped.rstrip('\"\'').strip()
            if not last:
                return False
            if last[-1] in ('—', ':'):
                return True
            return bool(_EXPLICIT_COUNT_RE.search(stripped) or _FORMULA_TAIL_RE.search(stripped))

        last = plain.rstrip('\"\'').strip()
        if not last:
            return False
        if last[-1] in ('—', ',', ';', ':'):
            return True
        if last[-1] == '.':
            return bool(_EXPLICIT_COUNT_RE.search(plain) or _FORMULA_TAIL_RE.search(plain))
        return False

    def _add_anchor_class(para_html: str) -> str:
        if 'syllabus-anchor' in para_html:
            return para_html
        if _re.match(r'<p\s+class="([^"]*)"', para_html):
            return _re.sub(
                r'<p\s+class="([^"]*)"',
                lambda mm: f'<p class="{mm.group(1)} syllabus-anchor"',
                para_html, count=1,
            )
        if para_html.startswith('<p>'):
            return '<p class="syllabus-anchor">' + para_html[3:]
        return para_html

    def _absorb(preceding: str, pairs: list, count: int) -> str:
        parts = [((mk or '') + ' ' + ct).strip() for mk, ct in pairs[:count]]
        inline = _re.sub(r'\s+', ' ', ' '.join(parts))
        merged = _re.sub(r'</p>\s*$', ' ' + inline + '</p>', preceding, count=1)
        return _add_anchor_class(merged)

    # ── main loop ─────────────────────────────────────────────────────────────
    paras = html.split('\n')
    out: list[str] = []
    i = 0
    n = len(paras)

    while i < n:
        para = paras[i]
        stripped = para.strip()

        m_item = _LIST_ITEM_RE.match(stripped)
        if not m_item:
            out.append(para)
            i += 1
            continue

        # Collect consecutive list-item run
        run_indices: list[int] = []
        j = i
        while j < n:
            curr = paras[j].strip()
            if not curr:
                j += 1
                continue
            if _LIST_ITEM_RE.match(curr):
                run_indices.append(j)
                j += 1
            else:
                break

        # ── Signal G: single-item ordinal continuation ───────────────────────
        if len(run_indices) == 1:
            pm = _LIST_ITEM_RE.match(stripped)
            mk_plain = _plain(pm.group(2) or '').strip() if pm else ''
            if pm and _ORDINAL_MK_RE.match(mk_plain):
                prev_idx = next(
                    (k for k in range(len(out) - 1, -1, -1) if out[k].strip()), -1
                )
                if prev_idx >= 0 and _HAS_INLINE_ORDINAL_RE.search(_plain(out[prev_idx])):
                    # Ensure the next ordinal is a numerical continuation (Issue 91/107)
                    def _parse_val(marker_text: str) -> int:
                        m = _re.search(r'\d+', marker_text)
                        if m: return int(m.group(0))
                        w = marker_text.lower()
                        if 'first' in w or '1st' in w: return 1
                        if 'second' in w or '2nd' in w or '2dly' in w: return 2
                        if 'third' in w or '3rd' in w or '3dly' in w: return 3
                        if 'fourth' in w or '4th' in w: return 4
                        if 'fifth' in w or '5th' in w: return 5
                        return 0
                    
                    preceding_plain = _plain(out[prev_idx])
                    matches = list(_re.finditer(r'\((?:\d+(?:st|nd|rd|th|ly|dly)?|1st|2nd(?:ly)?|3rd(?:ly)?|4th(?:ly)?)\.?\)', preceding_plain, _re.I))
                    is_continuation = True
                    if matches:
                        last_val = _parse_val(matches[-1].group(0))
                        next_val = _parse_val(mk_plain)
                        if next_val != last_val + 1:
                            is_continuation = False
                    
                    if is_continuation:
                        ct = pm.group(3) or ''
                        out[prev_idx] = _absorb(out[prev_idx], [(pm.group(2) or '', ct)], 1)
                        i = j
                        continue
            out.append(para)
            i += 1
            continue

        if len(run_indices) < 2:
            out.append(para)
            i += 1
            continue

        # ── is_case_2: first list-item ends '—' (nested sub-list anchor) ─────
        is_case_2 = False
        first_plain = _plain(para)
        if first_plain.rstrip('\"\'').strip().endswith('—'):
            is_li = bool(_re.match(r'<p class="(?:list-item|roman-list-item)">', stripped))
            if is_li and _allows_attach(first_plain, is_list_item=True):
                is_case_2 = True

        if is_case_2:
            preceding      = para
            preceding_plain = first_plain
            candidate_idx  = run_indices[1:]
        else:
            prev_idx = next(
                (k for k in range(len(out) - 1, -1, -1) if out[k].strip()), -1
            )
            if prev_idx == -1:
                out.append(para)
                i += 1
                continue
            preceding      = out[prev_idx]
            preceding_plain = _plain(preceding)
            is_prec_li = bool(_re.match(
                r'<p class="(?:list-item|roman-list-item)">', preceding.strip()
            ))
            if not _allows_attach(preceding_plain, is_list_item=is_prec_li):
                out.append(para)
                i += 1
                continue
            candidate_idx = run_indices

        # Build item pairs
        item_pairs: list[tuple[str, str]] = []
        for idx in candidate_idx:
            pm = _LIST_ITEM_RE.match(paras[idx].strip())
            item_pairs.append((pm.group(2) or '', pm.group(3) or ''))

        announced = _extract_count(preceding_plain)

        # ── determine flat prefix length ──────────────────────────────────────
        flat_prefix_len = 0

        for L in range(len(item_pairs), 1, -1):
            sub   = item_pairs[:L]
            if not _is_sequential_sequence(sub):
                continue
            wcs   = [_wc(ct) for _, ct in sub]
            nf    = sub[:-1]      # non-final items

            # Signal F: exact announced count, ≤20 w each
            if announced == L and all(wc <= _SIGNAL_F_CAP for wc in wcs):
                flat_prefix_len = L
                break

            # Signal H: ≥3 items, all end '.', all ≤25 w
            if (L >= 3
                    and all(ct.rstrip('\"\'').strip().endswith('.') for _, ct in sub)
                    and all(wc <= _SIGNAL_H_CAP for wc in wcs)):
                flat_prefix_len = L
                break

            # all_non_final_semi: every non-final item ends ';', non-final ≤20 w
            if (nf
                    and all(ct.rstrip('\"\'').strip().endswith(';') for _, ct in nf)
                    and all(wcs[k] <= _ALL_SEMI_CAP for k in range(len(nf)))):
                flat_prefix_len = L
                break

            # Continuation comma: non-final item ends ',' → final joins
            if nf and any(ct.rstrip('\"\'').strip().endswith(',') for _, ct in nf):
                flat_prefix_len = L
                break

            # Continuation connector: non-final ends 'and'/'or' → final joins
            if nf and any(
                _re.search(r'\b(?:and|or)\s*$', ct.rstrip('\"\'').strip(), _re.I)
                for _, ct in nf
            ):
                flat_prefix_len = L
                break

            # Standard hard cap
            if any(wc > _HARD_CAP for wc in wcs):
                continue

            # Standard signals A/B/C/D
            sig_a = any(ct.rstrip('\"\'').strip().endswith((';', ',')) for _, ct in nf)
            sig_b = any(
                _re.search(r'\b(?:and|or)\s*$', ct.rstrip('\"\'').strip(), _re.I)
                for _, ct in sub
            )
            sig_c = all(wc <= 3 for wc in wcs)
            sig_d = L >= 3 and all(wc <= 7 for wc in wcs)

            if sig_a or sig_b or sig_c or sig_d:
                flat_prefix_len = L
                break

        if flat_prefix_len == 0:
            out.append(para)
            remaining = run_indices[1:]
            if remaining:
                sub_html = '\n'.join([paras[idx] for idx in remaining])
                recurse_res = _attach_em_dash_flat_list(sub_html, config=config)
                out.extend(recurse_res.split('\n'))
            i = j
            continue

        # Re-emit remaining expansion items (recurse)
        remaining = [paras[idx] for idx in candidate_idx[flat_prefix_len:]]
        remaining_to_absorb = []
        remaining_to_recurse = []

        # Find the type and value of the last item in the flattened prefix to act as a sequence anchor
        last_type = 'unknown'
        last_val = 0
        if flat_prefix_len > 0:
            last_mk_plain = _plain(item_pairs[flat_prefix_len - 1][0]).strip()
            last_type, last_val = _get_marker_val_and_type(last_mk_plain)

        if flat_prefix_len > 0 and remaining and last_type != 'unknown' and last_val > 0:
            absorb_all = True
            current_type = last_type
            current_val = last_val
            for idx in candidate_idx[flat_prefix_len:]:
                curr_para = paras[idx].strip()
                pm = _LIST_ITEM_RE.match(curr_para)
                if pm:
                    mk_plain = _plain(pm.group(2) or '').strip()
                    m_type, m_val = _get_marker_val_and_type(mk_plain)
                    # Must be the same marker family (type) and strictly sequential (+1)
                    if m_type == current_type and m_val == current_val + 1:
                        current_val = m_val
                    else:
                        absorb_all = False
                        split_idx = candidate_idx.index(idx)
                        remaining_to_absorb = [paras[k] for k in candidate_idx[flat_prefix_len:split_idx]]
                        remaining_to_recurse = [paras[k] for k in candidate_idx[split_idx:]]
                        break
            if absorb_all:
                remaining_to_absorb = remaining
                remaining_to_recurse = []
        else:
            remaining_to_recurse = remaining

        total_to_absorb = flat_prefix_len + len(remaining_to_absorb)

        # ── absorb ───────────────────────────────────────────────────────────
        new_preceding = _absorb(preceding, item_pairs, total_to_absorb)

        if is_case_2:
            out.append(new_preceding)
        else:
            out[prev_idx] = new_preceding

        if remaining_to_recurse:
            out.extend(_attach_em_dash_flat_list('\n'.join(remaining_to_recurse)).split('\n'))

        i = j
        continue

    return '\n'.join(out)


def _owen_marker_level(marker_text: str, previous_marker_family: str = None) -> tuple[str, str]:
    """Classify an Owenian structural list marker into a reader level.
    
    Returns (level_class, marker_family).
    """
    marker_text = re.sub(r'<[^>]+>', '', marker_text).strip()
    if not marker_text:
        return 'list-level-1', previous_marker_family or 'other'

    # Strip bold tags and normalize casing
    clean = marker_text.strip('.,:; \t\n\r*')
    clean_upper = clean.upper()

    # 1. Level 3: Ordinals (1st., 2dly., 3dly., [SECONDLY], [3dly.])
    is_digit_ordinal = bool(re.search(r'\d(?:ST|ND|RD|TH|DLY|LY)', clean_upper))
    is_bracketed_word_ordinal = clean_upper.startswith('[') and clean_upper.endswith(']') and any(
        w in clean_upper for w in [
            'FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'SIXTH', 'SEVENTH',
            'EIGHTH', 'NINTH', 'LAST', 'LY'
        ]
    )
    is_local_ordinal = any(clean_upper.startswith(w) for w in ['1ST', '2DLY', '3DLY', '4THLY'])
    
    if is_digit_ordinal or is_bracketed_word_ordinal or is_local_ordinal:
        return 'list-level-3', 'ordinal'

    # 2. Level 2: Bracketed markers (e.g., [1.], [1], [a]) that are NOT word ordinals
    if clean.startswith('[') and clean.endswith(']'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return 'list-level-2', 'arabic_bracket'
        elif len(inner) == 1 and inner.isalpha():
            return 'list-level-2', 'alpha_bracket'
        else:
            return 'list-level-2', 'other_bracket'
    if clean.startswith('[') or re.match(r'^\[\d+\]\.?$', clean):
        return 'list-level-2', 'arabic_bracket'

    # 3. Level 2: Parenthesized markers (1.), (a.) (subordinate to main points)
    if clean.startswith('(') and clean.endswith(')'):
        inner = clean[1:-1].strip('.,:; ')
        if inner.isdigit():
            return 'list-level-2', 'arabic_paren'
        elif len(inner) == 1 and inner.isalpha():
            return 'list-level-2', 'alpha_paren'
        else:
            return 'list-level-2', 'other_paren'

    if clean.isdigit() or re.match(r'^\d+$', clean):
        return 'list-level-1', 'arabic'
        
    if any(w in clean_upper for w in ['FIRST', 'SECOND', 'THIRD', 'FOURTH', 'FIFTH', 'OBJECTION', 'ANSWER', 'USE', 'SOL']):
        return 'list-level-1', 'word'

    if re.search(r'[IVXLCDM]+\.?\s+\d+', clean):
        return 'list-level-1', 'roman_decimal'

    return 'list-level-1', previous_marker_family or 'other'


def _add_owen_list_level_classes(html: str) -> str:
    """Add modest reader-facing hierarchy classes to remaining block lists,
    dynamically adjusting nesting levels based on count-phrase triggers in parent paragraphs.
    """
    if not html:
        return html

    import re

    # Trigger patterns
    COUNT_TRIGGER_RE = re.compile(
        r'\b(?:two|three|four|five|six|seven|eight|nine|ten|sundry|several|twofold|threefold|fourfold|ensuing|following)\s+'
        r'(?:ways|reasons|things|respects|accounts|causes|parts|points|arguments|properties|instances|ends|acts|observations|propositions|heads)\b',
        re.I
    )
    ENDS_WITH_INTRO_RE = re.compile(r'[:—\-]\s*$', re.I)

    # Helper to check if a block contains a list trigger
    def has_list_trigger(text: str) -> bool:
        clean = re.sub(r'<[^>]+>', '', text).strip()
        m = COUNT_TRIGGER_RE.search(clean)
        if not m:
            return False
        dist_from_end = len(clean) - m.end()
        return dist_from_end <= 120 and bool(ENDS_WITH_INTRO_RE.search(clean))

    # Helper to convert Roman to Int
    def roman_to_int(s: str) -> int:
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        val = 0
        prev_val = 0
        for char in reversed(s.upper()):
            curr_val = roman_map.get(char, 0)
            if curr_val == 0:
                return None
            if curr_val >= prev_val:
                val += curr_val
            else:
                val -= curr_val
            prev_val = curr_val
        return val

    # Block regex to split the XHTML safely
    block_re = re.compile(
        r'(<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )

    blocks = []
    last_idx = 0
    for m in block_re.finditer(html):
        inter = html[last_idx:m.start()]
        if inter.strip():
            blocks.append(inter)
        blocks.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:]
    if tail.strip():
        blocks.append(tail)

    output_blocks = []
    active_override_level = None
    previous_family = None

    last_digit_at_level = {1: None, 2: None, 3: None}
    last_family_at_level = {1: None, 2: None, 3: None}

    for block in blocks:
        # Check if it's a list item
        p_match = re.match(r'^<p class="(?P<classes>[^"]*)">(?P<inner>.*?)</p>$', block, re.S)
        if p_match:
            classes_list = p_match.group('classes').split()
            if 'list-item' in classes_list or 'roman-list-item' in classes_list:
                cls = 'roman-list-item' if 'roman-list-item' in classes_list else 'list-item'
                inner = p_match.group('inner')
                marker_match = re.match(r'\s*(<b>[^<]{1,40}</b>)', inner, re.S)
                marker_raw = marker_match.group(1) if marker_match else ''
                
                # Determine base level and family
                if cls == 'roman-list-item':
                    base_level_class = 'list-level-1'
                    family = 'roman'
                else:
                    base_level_class, family = _owen_marker_level(marker_raw, previous_family)
                
                previous_family = family
                
                try:
                    base_level = int(base_level_class.split('-')[-1])
                except ValueError:
                    base_level = 1
                
                # Extract decimal / Roman integer value if available
                clean_marker = re.sub(r'<[^>]+>', '', marker_raw).strip('.,:; \t\n\r*()[]')
                val = None
                if clean_marker.isdigit():
                    val = int(clean_marker)
                elif re.match(r'^[IVXLCDM]+$', clean_marker, re.I):
                    val = roman_to_int(clean_marker)

                # Determine dynamic context-aware level
                assigned_level = base_level

                if val is not None:
                    # Check in descending order of levels to prefer the deepest active sequence (Issue #91 / list refinement)
                    if last_digit_at_level[3] is not None and val == last_digit_at_level[3] + 1 and (family == last_family_at_level[3] or active_override_level == 3):
                        assigned_level = 3
                        active_override_level = None
                    elif last_digit_at_level[2] is not None and val == last_digit_at_level[2] + 1 and family == last_family_at_level[2]:
                        assigned_level = 2
                        active_override_level = None
                    elif last_digit_at_level[1] is not None and val == last_digit_at_level[1] + 1 and family == last_family_at_level[1]:
                        active_override_level = None
                        assigned_level = 1
                    elif val == 1:
                        if active_override_level is not None:
                            assigned_level = max(base_level, active_override_level)
                            active_override_level = None
                        else:
                            # If Level 2 is occupied by a different family, nest to Level 3
                            if base_level == 2 and last_digit_at_level[2] is not None and family != last_family_at_level[2]:
                                assigned_level = 3
                            else:
                                assigned_level = base_level
                    # 5. Fallback for non-sequential but numeric items
                    else:
                        if active_override_level is not None:
                            assigned_level = max(base_level, active_override_level)
                            active_override_level = None
                        else:
                            assigned_level = base_level
                else:
                    # Non-numeric items (e.g. scholastic anchors, ordinals)
                    if active_override_level is not None:
                        assigned_level = max(base_level, active_override_level)
                        active_override_level = None
                    else:
                        assigned_level = base_level

                # Update sequence trackers
                if val is not None:
                    last_digit_at_level[assigned_level] = val
                    last_family_at_level[assigned_level] = family
                    # Reset sequence trackers for all deeper levels to prevent scoping carryover bugs
                    for lvl in range(assigned_level + 1, 4):
                        last_digit_at_level[lvl] = None
                        last_family_at_level[lvl] = None

                # Reconstruct the list item paragraph preserving other classes (like syllabus-anchor)
                other_classes = [c for c in classes_list if c not in ('list-item', 'roman-list-item') and not c.startswith('list-level-')]
                new_classes = [cls, f'list-level-{assigned_level}'] + other_classes
                block = f'<p class="{" ".join(new_classes)}">{inner}</p>'
                
                # Check if this list item itself acts as an introducing trigger for a sub-list
                if has_list_trigger(inner):
                    active_override_level = min(3, assigned_level + 1)
                
                output_blocks.append(block)
            else:
                output_blocks.append(block)
        elif re.match(r'^<h[1-6]\b', block):
            output_blocks.append(block)
            active_override_level = None
        else:
            output_blocks.append(block)
            
            # Check if it acts as a list trigger
            if has_list_trigger(block):
                active_override_level = 1
            else:
                # Non-list paragraph with no trigger resets overrides
                active_override_level = None

    return "".join(output_blocks)


def _nest_owen_list_hierarchies(html: str) -> str:
    """Reconstruct flat list-item paragraphs into a nested <div> tree.
    
    This function processes top-level block elements (paragraphs, blockquotes, headings)
    and wraps them in <div class="owen-branch owen-level-X"> containers based on their
    list-level markings. Continuation prose and quotes automatically nest inside the
    active leaf container.
    """
    import re
    block_re = re.compile(
        r'(<p\b[^>]*>.*?</p>|'
        r'<blockquote\b[^>]*>.*?</blockquote>|'
        r'<h[1-6]\b[^>]*>.*?</h[1-6]>|'
        r'<aside\b[^>]*>.*?</aside>|'
        r'<div\b[^>]*>.*?</div>|'
        r'<table\b[^>]*>.*?</table>|'
        r'<hr\s*/?>)',
        re.S
    )
    
    blocks = []
    last_idx = 0
    for m in block_re.finditer(html):
        inter = html[last_idx:m.start()].strip()
        if inter:
            blocks.append(inter)
        blocks.append(m.group(0))
        last_idx = m.end()
    tail = html[last_idx:].strip()
    if tail:
        blocks.append(tail)
        
    if not blocks:
        return html
        
    output_parts = []
    active_levels = []  # Stack of currently open levels (e.g. [1, 2])
    
    def close_levels_down_to(target_level: int):
        """Close all open divs deeper than or equal to target_level."""
        while active_levels and active_levels[-1] >= target_level:
            output_parts.append("</div>")
            active_levels.pop()

    for i, block in enumerate(blocks):
        explicit_level = None
        
        p_match = re.match(r'^<p\b([^>]*)>', block)
        if p_match:
            attrs = p_match.group(1)
            if 'list-level-3' in attrs:
                explicit_level = 3
            elif 'list-level-2' in attrs:
                explicit_level = 2
            elif 'list-level-1' in attrs:
                explicit_level = 1
            elif 'signature' in attrs or 'front-matter' in attrs:
                explicit_level = 0
        elif re.match(r'^<h[1-6]\b', block):
            explicit_level = 0
        elif re.match(r'^<aside\b', block):
            explicit_level = 0
            
        if explicit_level is not None:
            if explicit_level == 0:
                close_levels_down_to(1)
                output_parts.append(block)
            else:
                current_active = active_levels[-1] if active_levels else 0
                
                if explicit_level > current_active:
                    for level in range(current_active + 1, explicit_level + 1):
                        output_parts.append(f'<div class="owen-branch owen-level-{level}">')
                        active_levels.append(level)
                    output_parts.append(block)
                    
                elif explicit_level == current_active:
                    output_parts.append("</div>")
                    active_levels.pop()
                    output_parts.append(f'<div class="owen-branch owen-level-{explicit_level}">')
                    active_levels.append(explicit_level)
                    output_parts.append(block)
                    
                else:  # explicit_level < current_active
                    close_levels_down_to(explicit_level)
                    output_parts.append(f'<div class="owen-branch owen-level-{explicit_level}">')
                    active_levels.append(explicit_level)
                    output_parts.append(block)
        else:
            # Lookahead to find the next explicit list level or heading/reset
            next_level = 0
            for j in range(i + 1, len(blocks)):
                next_block = blocks[j]
                next_explicit_level = None
                p_match_next = re.match(r'^<p\b([^>]*)>', next_block)
                if p_match_next:
                    attrs_next = p_match_next.group(1)
                    if 'list-level-3' in attrs_next:
                        next_explicit_level = 3
                    elif 'list-level-2' in attrs_next:
                        next_explicit_level = 2
                    elif 'list-level-1' in attrs_next:
                        next_explicit_level = 1
                    elif 'signature' in attrs_next or 'front-matter' in attrs_next:
                        next_explicit_level = 0
                elif re.match(r'^<h[1-6]\b', next_block):
                    next_explicit_level = 0
                elif re.match(r'^<aside\b', next_block):
                    next_explicit_level = 0
                elif re.match(r'^<div\b', next_block):
                    next_explicit_level = 0
                
                if next_explicit_level is not None:
                    next_level = next_explicit_level
                    break
            
            # If the current active nesting level is deeper than the next list item's level,
            # the deeper list/subpoint is finished. Close it.
            current_active = active_levels[-1] if active_levels else 0
            if current_active > next_level:
                close_levels_down_to(next_level + 1)
                
            output_parts.append(block)
            
    close_levels_down_to(1)
    
    return "\n".join(output_parts)


# ---------------------------------------------------------------------------
# Issue 19: Inline list merging
# ---------------------------------------------------------------------------
_LIST_ITEM_CONTENT_RE = re.compile(
    r'<p class="(list-item|roman-list-item)">(<b>[^<]{1,30}</b>\s*)?(.*?)</p>',
    re.S,
)


def _merge_short_inline_lists(html: str) -> str:
    """Merge consecutive list items into continuous prose when appropriate.

    Two complementary rules:

    Rule A — short-item run (Issue 13 / Issue 19.b):
      If every item in the entire run has very short plain-text content
      (≤ _SHORT_ITEM_WORD_LIMIT words after stripping the bold marker),
      the whole run is a "pseudo-list" — really an inline enumeration —
      and is merged unconditionally into a single prose paragraph,
      regardless of terminal punctuation.
      Examples: "1. Complacency; 2. Permanency."
                "1. Illumination; 2. Conviction; 3. Reformation."

    Rule B — semicolon sub-run:
      An item whose content ends with ';' or ',' is accumulated into the
      current sub-run.  When a terminating item (ends with anything else) is
      reached, the accumulated sub-run (≥ 2 items) is merged.  Items that
      stand alone remain on their own line.

      Handles heterogeneous runs naturally: a long 'Secondly,…' paragraph
      ending with '.' stays separate while short ';' items are merged.
    """
    import re as _re

    _SHORT_ITEM_WORD_LIMIT = 4   # items with ≤ this many words are "not really list items"
    _RULE_B_WORD_LIMIT = 40      # cap to prevent merging long exposition paragraphs

    def _plain_text(html_frag: str) -> str:
        return _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', html_frag)).strip()

    def _content_word_count(plain: str) -> int:
        return len(plain.split())

    def _is_non_terminating_item(html_frag: str) -> bool:
        plain = _plain_text(html_frag).rstrip()
        if _content_word_count(plain) > _RULE_B_WORD_LIMIT:
            return False
        if plain.endswith((';', ',')):
            return True
        if _re.search(r'\b(and|or)\b\s*$', plain, _re.I):
            return True
        return False

    # Split on both list-item and roman-list-item paragraphs
    parts = _re.split(r'(<p class="(?:list-item|roman-list-item)">.*?</p>)', html, flags=_re.S)

    def _item_class(frag: str) -> str:
        """Return the CSS class of a list-item paragraph fragment."""
        m2 = _re.match(r'<p class="(list-item|roman-list-item)">', frag)
        return m2.group(1) if m2 else 'list-item'

    out = []
    i = 0
    while i < len(parts):
        token = parts[i]
        if not _re.match(r'<p class="(?:list-item|roman-list-item)">', token):
            out.append(token)
            i += 1
            continue

        # Collect a run of consecutive list-item paragraphs of the SAME class
        run_cls = _item_class(token)
        run = [token]
        j = i + 1
        while j < len(parts):
            if parts[j].strip() == '':
                j += 1
                continue
            if _re.match(rf'<p class="{run_cls}">', parts[j]):
                run.append(parts[j])
                j += 1
            else:
                break

        # Extract (marker, content) pairs — bold group is optional
        item_contents = []
        for item in run:
            m = _LIST_ITEM_CONTENT_RE.match(item)
            if m:
                # group(1)=class, group(2)=optional bold marker, group(3)=content
                item_contents.append((m.group(2) or '', m.group(3)))
            else:
                # Fallback: strip outer <p> tags to get inner HTML
                inner = _re.sub(
                    r'^<p class="(?:list-item|roman-list-item)">(.*?)</p>$',
                    r'\1', item, flags=_re.S,
                )
                item_contents.append(('', inner))

        # ── Sibling Symmetry Guard: if any item in the run is a long paragraph
        #    exceeding _RULE_B_WORD_LIMIT, do not merge the run at all.
        #    Keep all items as block paragraphs to ensure sibling symmetry.
        if len(item_contents) >= 2:
            any_long = any(
                _content_word_count(_plain_text(ct)) > _RULE_B_WORD_LIMIT
                for _mk, ct in item_contents
            )
            if any_long:
                run_out = []
                for mk2, ct2 in item_contents:
                    run_out.append(f'<p class="{run_cls}">{mk2}{ct2}</p>')
                out.append('\n'.join(run_out))
                i = j
                continue

        # ── Rule A: all items are very short AND at least one non-final item
        #    ends with ';' or ',' or a connector → merge the entire run.
        #
        #    The semicolon/comma guard prevents period-terminated standalone
        #    statements ("God is sovereign. God is holy.") from merging, while
        #    still catching short pseudo-lists ("1. Complacency; 2. Permanency.")
        #    that Rule B would also handle.
        if len(item_contents) >= 2:
            all_short = all(
                _content_word_count(_plain_text(ct)) <= _SHORT_ITEM_WORD_LIMIT
                for _mk, ct in item_contents
            )
            any_non_final_has_semi = any(
                _is_non_terminating_item(ct)
                for _mk, ct in item_contents[:-1]
            )
            if all_short and any_non_final_has_semi:
                merged = ' '.join(mk2 + ct2 for mk2, ct2 in item_contents)
                out.append(f'<p class="{run_cls}">{merged}</p>')
                i = j
                continue

        # ── Rule B: semicolon/comma sub-run accumulation ──────────────────────
        run_out = []
        current_subrun = []

        for mk, ct in item_contents:
            current_subrun.append((mk, ct))
            if not _is_non_terminating_item(ct):
                # Terminating item — flush the accumulated sub-run
                if len(current_subrun) >= 2:
                    merged = ' '.join(mk2 + ct2 for mk2, ct2 in current_subrun)
                    run_out.append(f'<p class="{run_cls}">{merged}</p>')
                else:
                    mk2, ct2 = current_subrun[0]
                    run_out.append(f'<p class="{run_cls}">{mk2}{ct2}</p>')
                current_subrun = []

        # Flush any remaining items (run where every item ends with ; or ,)
        if current_subrun:
            if len(current_subrun) >= 2:
                merged = ' '.join(mk2 + ct2 for mk2, ct2 in current_subrun)
                run_out.append(f'<p class="{run_cls}">{merged}</p>')
            else:
                mk2, ct2 = current_subrun[0]
                run_out.append(f'<p class="{run_cls}">{mk2}{ct2}</p>')

        out.append('\n'.join(run_out))
        i = j

    return ''.join(out)

