import re
import sys
from html import escape as _raw_html_escape, unescape as _html_unescape
from shared import *

def _html_escape(text: str) -> str:
    escaped = _raw_html_escape(text)
    # Restore escaped span and a tags to preserve manual language tagging or inline links from intermediate JSON
    escaped = re.sub(
        r'&lt;(\/?(?:span|a)\b.*?)&gt;',
        lambda m: '<' + m.group(1).replace('&quot;', '"').replace('&#x27;', "'") + '>',
        escaped,
        flags=re.I
    )
    return escaped
from shared import (
    _normalize_spaced_caps, _normalize_i_will, _normalize_scholarly_citation_artifacts,
    _repair_owen_ocr_errors, _norm_for_dedupe, _is_scripture_ref_fragment,
    _scripture_ref_tokens, _split_inline_structural_markers,
    _trim_duplicate_reference_prefix
)
from scripts.owen_lists import *
from scripts.owen_lists import (
    _attach_em_dash_flat_list, _add_owen_list_level_classes,
    _merge_short_inline_lists, _nest_owen_list_hierarchies
)


_TRANSITIONAL_WORD_RE = re.compile(
    r'^(Therefore|Wherefore|Hence|Again|Moreover|Accordingly|Furthermore|'
    r'Nevertheless|Notwithstanding|Howbeit|Howsoever|Whence|Hereupon|'
    r'Herein|Hereby|Hereof|Hereto|Hereunto|Herewith|Therein|Thereby|'
    r'Thereof|Thereto|Thereunto|Therewith|But|So|Now|As|For)[,;.—\s]*$',
    re.I,
)

def _repair_markdown_tables(text: str) -> str:
    """Convert Markdown pipe-table paragraphs into [[BLOCKQUOTE]] / plain paragraph pairs."""
    if not text or ('|---|' not in text and '|--' not in text):
        return text

    paras = text.split('\n\n')
    out: list[str] = []

    for para in paras:
        stripped = para.strip()

        # Quick bail — paragraph has no table separator row
        if not re.search(r'\|[\-]+\|', stripped):
            out.append(para)
            continue

        # Normalise <br> tags → space so cell text reads as a single line
        normalised = re.sub(r'<br\s*/?>', ' ', stripped)

        # Split inline-concatenated rows. Each row ends with '|' and the next
        # starts with '|' with only whitespace between them.
        row_texts = re.split(r'(?<=\|)\s+(?=\|)', normalised)

        first_row = True
        for rt in row_texts:
            rt = rt.strip()
            if not rt:
                continue

            # Split cells by '|' and strip them.
            cells = [c.strip() for c in rt.split('|')]
            if cells and not cells[0]:
                cells.pop(0)
            if cells and not cells[-1]:
                cells.pop()

            if not cells:
                continue

            # Check if this is the separator row
            if all(re.match(r'^[\-]+$', c) for c in cells):
                continue

            if len(cells) >= 2:
                left = cells[0]
                right = cells[1]

                # Special case: unclosed preceding blockquote
                if first_row and out and out[-1].strip().startswith('[[BLOCKQUOTE]]') and out[-1].strip().endswith(','):
                    out[-1] = out[-1] + ' ' + right
                    out.append(left)
                else:
                    out.append('[[BLOCKQUOTE]] ' + right)
                    out.append(left)
                first_row = False

    return '\n\n'.join(out)


from dataclasses import dataclass, field
from typing import Optional, Set, List

@dataclass
class ParserState:
    current_mode: str = "BODY_TEXT"
    pending_drop_cap: bool = False
    recent_plain: List[str] = field(default_factory=list)
    roman_list_expected: Optional[int] = None
    roman_sequence_choice: Optional[str] = None
    pending_chapter_subtitle: bool = False
    summary_continuation_active: bool = False
    seen_footnote_refs: Set[str] = field(default_factory=set)
    fm_prose_started: bool = False
    next_blockquote_is_opening: bool = False
    is_sermon_volume: bool = False
    is_catechism_context: bool = False

    def add_recent_plain(self, text: str):
        from render import _strip_footnote_placeholders
        self.recent_plain.append(_strip_footnote_placeholders(text))
        if len(self.recent_plain) > 5:
            self.recent_plain = self.recent_plain[-5:]


def _preprocess_markdown_text(md_text: str, config: Optional[dict]) -> tuple[list[str], bool]:
    from scripts.analysis_parser import _merge_reference_continuation_paragraphs
    from scripts.catechism_parser import _split_inline_catechism_questions
    from scripts.roman_parser import _coalesce_roman_list_paragraphs
    from scripts.paragraph_healer import (
        _repair_dangling_initial_splits,
        _repair_flat_list_continuation_splits,
        _repair_fused_word_ordinals,
        _repair_lowercase_continuation_splits,
        _repair_mid_sentence_blockquote_splits,
        _repair_scholastic_anchor_splits,
        _repair_scholastic_blockquote_boundaries,
        _repair_sermon_prefatory_note_splits,
        _repair_transitional_word_isolation,
        _repair_unbalanced_bracket_splits,
        _split_tail_signature,
    )
    from render import normalize_footnote_markers

    md_text = normalize_characters(md_text)
    md_text = _split_tail_signature(md_text)
    md_text = _repair_sermon_prefatory_note_splits(md_text)
    md_text = _repair_owen_ocr_errors(md_text, config=config)
    md_text = _repair_markdown_tables(md_text)
    md_text = _repair_fused_word_ordinals(md_text)
    md_text = _repair_mid_sentence_blockquote_splits(md_text)
    md_text = _repair_scholastic_blockquote_boundaries(md_text)
    md_text = re.sub(r'(?<=[,;.!?\s])\+(?=[a-z])', '', md_text)

    md_text = _repair_unbalanced_bracket_splits(md_text)
    md_text = _repair_lowercase_continuation_splits(md_text)
    md_text = _repair_transitional_word_isolation(md_text)
    md_text = _repair_scholastic_anchor_splits(md_text)
    md_text = _repair_dangling_initial_splits(md_text)
    md_text = _repair_flat_list_continuation_splits(md_text)

    normalized_paragraphs = [
        normalize_footnote_markers(para)
        for para in _merge_reference_continuation_paragraphs(md_text.split('\n\n'))
    ]

    coalesce_hook = config.get('paragraph_coalesce_hook') if config else None
    is_catechism_context = bool(config.get('is_catechism_context')) if config else False
    if coalesce_hook:
        paragraphs = coalesce_hook(
            _split_inline_catechism_questions(
                _coalesce_roman_list_paragraphs(normalized_paragraphs),
                allow_bare_a=is_catechism_context,
            )
        )
    else:
        paragraphs = _split_inline_catechism_questions(
            _coalesce_roman_list_paragraphs(normalized_paragraphs),
            allow_bare_a=is_catechism_context,
        )

    expanded_paragraphs = []
    for para in paragraphs:
        expanded_paragraphs.extend(
            _split_inline_structural_markers(
                para,
                allow_bare_a=is_catechism_context,
            )
        )
    return expanded_paragraphs, is_catechism_context


def _process_structural_token(kind: str, content: str, state: ParserState, front_matter_style: str, html_parts: list[str]) -> bool:
    from render import (
        _restore_footnote_placeholders,
        _strip_footnote_placeholders,
        _strip_inline_structural_tokens,
        tag_unicode_ranges,
    )
    from scripts.roman_parser import (
        _clean_heading_text,
        _is_roman_outline_entry,
        _render_simple_roman_heading_content,
        _roman_head_match,
        _roman_to_int,
    )

    def _render_heading_content(raw_content: str) -> str:
        content_clean = _strip_inline_structural_tokens(raw_content)
        def _fn_repl(m):
            fn_num = m.group(1)
            if fn_num in state.seen_footnote_refs:
                return ''
            state.seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'
        with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
        escaped = _html_escape(with_placeholders)
        with_links = _restore_footnote_placeholders(escaped)
        return tag_unicode_ranges(with_links)

    def _render_blockquote_content(raw_content: str) -> str:
        content_clean = _strip_inline_structural_tokens(raw_content)
        content_clean = content_clean.rstrip()
        if content_clean.endswith(('“', '‘')):
            content_clean = content_clean[:-1].rstrip()
        elif content_clean.endswith('"'):
            if len(content_clean) <= 1 or content_clean[-2].isspace():
                content_clean = content_clean[:-1].rstrip()
        def _fn_repl(m):
            fn_num = m.group(1)
            if fn_num in state.seen_footnote_refs:
                return ''
            state.seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'
        with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
        escaped = _html_escape(with_placeholders)
        with_links = _restore_footnote_placeholders(escaped)
        return tag_unicode_ranges(with_links)

    def _render_summary_content(raw_content: str) -> str:
        content_clean = _strip_inline_structural_tokens(raw_content)
        content_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', content_clean)
        def _fn_repl(m):
            fn_num = m.group(1)
            if fn_num in state.seen_footnote_refs:
                return ''
            state.seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'
        with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
        escaped = _html_escape(with_placeholders)
        with_links = _restore_footnote_placeholders(escaped)
        return tag_unicode_ranges(with_links)

    def _render_roman_heading_content(raw_content: str) -> str:
        content_clean = _strip_inline_structural_tokens(raw_content)
        match = _roman_head_match(content_clean)
        if not match:
            return _render_heading_content(content_clean)
        roman_html = f'<b>{_html_escape(match.group("roman"))}</b>'
        rest = (match.group('rest') or '').strip()
        if not rest:
            return roman_html
        return f'{roman_html} {_render_heading_content(rest)}'

    if kind == 'BLOCKQUOTE':
        if not content.strip():
            return True
        scripture_match = re.match(
            rf'^((?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\s+\d+:\d+(?:[-,]\s*\d+)*),\s+(.*)$',
            content, re.I | re.S
        )
        if scripture_match:
            ref = scripture_match.group(1)
            content = scripture_match.group(2)
            html_parts.append(f'<p class="scripture-ref-introduction">{tag_unicode_ranges(_html_escape(ref))},</p>')

        if state.next_blockquote_is_opening:
            bq_class = ' class="sermon-opening-scripture"'
            state.next_blockquote_is_opening = False
        else:
            bq_class = ''
        html_parts.append(f'<blockquote{bq_class} epub:type="z3998:quotation"><p class="blockquote-content">{_render_blockquote_content(content)}</p></blockquote>')
        state.pending_drop_cap = False
        state.roman_list_expected = None
        state.add_recent_plain(content)
        return True

    if state.current_mode == "FRONT_MATTER":
        _escaped = _render_heading_content(content)
        if front_matter_style == "prose":
            if kind == 'PART':
                part_match = re.match(r'^(Part\s+[IVXLCDM]+\.?)(.*)$', content, re.I | re.S)
                if part_match:
                    lead = _html_escape(part_match.group(1).rstrip('.'))
                    rest = _render_heading_content(part_match.group(2).strip())
                    html_parts.append(f'<p class="analysis-part"><b>{lead}.</b> {rest}</p>')
                else:
                    html_parts.append(f'<p class="analysis-part"><b>{_escaped}</b></p>')
                state.fm_prose_started = False
                state.pending_drop_cap = False
                return True
            if kind == 'ROMAN_HEAD':
                roman_match = re.match(r'^([IVXLCDM]+\.)\s*(.*)$', content, re.I | re.S)
                if roman_match:
                    numeral = _html_escape(roman_match.group(1))
                    rest = _render_heading_content(roman_match.group(2).strip())
                    html_parts.append(f'<p class="roman-list-item"><b>{numeral}</b> {rest}</p>')
                else:
                    html_parts.append(f'<p class="roman-list-item">{_escaped}</p>')
                state.fm_prose_started = False
                state.pending_drop_cap = False
                return True
            _content_upper = content.upper().strip().rstrip('.')
            _is_fm_section_title = any(
                re.match(rf'^(?:THE\s+)?{kw}\.?$', _content_upper)
                for kw in [
                    "PREFATORY NOTE", "ANALYSIS", "PREFACE",
                    "ORIGINAL PREFACE", "PREFACE TO THE READER",
                    "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT",
                ]
            )
            if _is_fm_section_title:
                title_text = content.rstrip('.').title()
                html_parts.append(
                    f'<h2 class="front-matter-heading">'
                    f'{_render_heading_content(title_text)}'
                    f'</h2>'
                )
            else:
                html_parts.append(f'<h3 class="secondary">{_escaped}</h3>')
            state.fm_prose_started = False
        else:
            html_parts.append(f'<p class="front-matter-body"><b>{_escaped}</b></p>')
        state.pending_drop_cap = False
        return True

    if kind == 'PART':
        state.summary_continuation_active = False
        html_parts.append(f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">{_render_heading_content(content)}</h1>')
        if state.current_mode == "BODY_START":
            state.pending_drop_cap = True
        state.add_recent_plain(content)
        return True
    elif kind == 'CHAPTER':
        state.summary_continuation_active = False
        html_parts.append(f'<h1 class="secondary">{_render_heading_content(content)}</h1>')
        if state.is_sermon_volume:
            state.next_blockquote_is_opening = True
        state.add_recent_plain(content)
        return True
    elif kind == 'ROMAN_HEAD':
        state.summary_continuation_active = False
        previous_text = state.recent_plain[-1] if state.recent_plain else ''
        roman_match = _roman_head_match(content)
        roman_number = _roman_to_int(roman_match.group('roman')) if roman_match else None
        
        is_roman_list = False
        if roman_number == 1:
            is_roman_list, next_roman = _is_roman_outline_entry(
                content,
                previous_text,
                state.roman_list_expected,
            )
            state.roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
        elif roman_number is not None and roman_number > 1:
            if state.roman_sequence_choice == 'list-item':
                is_roman_list = True
            elif state.roman_sequence_choice == 'roman-subheading':
                is_roman_list = False
            else:
                is_roman_list, next_roman = _is_roman_outline_entry(
                    content,
                    previous_text,
                    state.roman_list_expected,
                )
        else:
            is_roman_list, next_roman = _is_roman_outline_entry(
                content,
                previous_text,
                state.roman_list_expected,
            )

        if is_roman_list:
            html_parts.append(f'<p class="roman-list-item">{_render_roman_heading_content(content)}</p>')
            state.roman_list_expected = roman_number + 1 if roman_number is not None else None
        else:
            html_parts.append(f'<h4 class="roman-subheading">{_render_roman_heading_content(content)}</h4>')
            state.roman_list_expected = None
        state.pending_drop_cap = False
        state.add_recent_plain(content)
        return True
    elif kind == 'SUBTITLE':
        state.summary_continuation_active = False
        if re.match(r'^(?:\*\*)?(?:Q\.|Ques\.|A\.|Ans\.)\s*(?:\d+\.)?\s*(?:\*\*)?', content, re.I):
            return False
        else:
            html_parts.append(f'<h4 class="chapter-subtitle">{_render_heading_content(content)}</h4>')
            state.add_recent_plain(content)
            return True
    elif kind == 'SUMMARY':
        _summary_heading_re = re.compile(
            r"^(?P<heading>[A-Z][A-Z\s,;:'\u2018\u2019\u2014\-]{9,}[.!?])\s+"
            r"(?P<synopsis>[\dA-Z\"\u201c\u2018(].{10,})$",
            re.S,
        )
        _content_for_split = re.sub(
            r'([.!?])(\d{1,4})(?=\s+[A-Z\"\u201c\u2018(])', r'\1', content.strip()
        )
        _smatch = _summary_heading_re.match(_content_for_split)
        _synopsis_has_lower = (
            _smatch and bool(re.search(r'[a-z]', _smatch.group('synopsis')[:80]))
        )
        if _smatch and _synopsis_has_lower and not ROMAN_ONLY_RE.match(
            _smatch.group('heading').rstrip('.!? ').strip()
        ):
            h_text = _smatch.group('heading').strip()
            s_text = _smatch.group('synopsis').strip()
            html_parts.append(
                f'<h3 class="chapter-heading">{_render_heading_content(h_text)}</h3>'
            )
            html_parts.append(
                f'<p class="chapter-summary">{_render_summary_content(s_text)}</p>'
            )
            state.summary_continuation_active = True
        else:
            _content_letters = [c for c in content if c.isalpha()]
            _upper_ratio = (
                sum(1 for c in _content_letters if c.isupper()) / len(_content_letters)
                if _content_letters else 0
            )
            _is_all_caps_heading = (
                _upper_ratio >= 0.92
                and not ROMAN_ONLY_RE.match(content.strip().rstrip('.!? ').strip())
            )
            if _is_all_caps_heading:
                html_parts.append(
                    f'<h3 class="chapter-heading">{_render_heading_content(content)}</h3>'
                )
                state.summary_continuation_active = False
            else:
                html_parts.append(
                    f'<p class="chapter-summary">{_render_summary_content(content)}</p>'
                )
                state.summary_continuation_active = True
        state.add_recent_plain(content)
        return True
    elif kind == 'DIGRESSION':
        state.summary_continuation_active = False
        num_match = re.search(r'\d+', content)
        d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
        html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{_render_heading_content(content.upper().rstrip("."))}</h3>')
        state.pending_drop_cap = False
        state.add_recent_plain(content)
        return True

    return False


def _clean_and_format_paragraph(para: str, state: ParserState, config: Optional[dict], html_parts: list[str]) -> tuple[str, Optional[str], Optional[str], bool, Optional[str]]:
    from render import (
        _restore_footnote_placeholders,
        _split_leading_chapter_subtitle,
        _strip_inline_structural_tokens,
        _trim_duplicate_reference_prefix,
        tag_unicode_ranges,
    )
    from scripts.roman_parser import (
        _clean_heading_text,
        _is_roman_list_item,
        _render_simple_roman_heading_content,
        _roman_decimal_marker_match,
        _roman_head_match,
        _roman_to_int,
        _split_roman_section_opening,
        _starts_roman_outline,
    )

    stripped = para.strip()
    h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
    
    if h_match:
        level = len(h_match.group(1))
        content = h_match.group(2)
        if 'DIGRESSION' in content.upper():
            num_match = re.search(r'\d+', content)
            d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
            html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{tag_unicode_ranges(_html_escape(content.upper().rstrip(".")))}</h3>')
            state.pending_drop_cap = False
            return '', None, None, False, None
        h_tag = 'h1' if level <= 2 else ('h2' if level <= 4 else 'h3')
    else:
        content = stripped
        h_tag = None

    content = content.lstrip()

    frontmatter_inline = None
    if h_tag:
        frontmatter_inline = re.match(
            r'^(?:THE\s+)?(PREFACE|PREFATORY NOTE|ORIGINAL PREFACE)(\.?)\s+(.{40,})$',
            content,
            re.S,
        )
    if frontmatter_inline:
        heading = f'{frontmatter_inline.group(1)}{frontmatter_inline.group(2)}'
        html_parts.append(f'<h3 class="secondary">{heading}</h3>')
        content = frontmatter_inline.group(3).strip()
        h_tag = None

    roman_list_match = re.match(rf'^{re.escape(ROMAN_LIST_TOKEN)}\s+([IVXLCDM]+\.?)\s+(.+)$', content)
    is_centered_roman_list = False
    if roman_list_match:
        is_centered_roman_list = True
        content = f'**{roman_list_match.group(1)}** {roman_list_match.group(2).strip()}'
        h_tag = None

    def footnote_marker_repl(match):
        fn_num = match.group(1)
        if fn_num in state.seen_footnote_refs:
            return ''
        state.seen_footnote_refs.add(fn_num)
        return f'FNREFTOKEN{fn_num}TOKEN'

    content_no_refs = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, content).strip()
    content_no_refs = _strip_inline_structural_tokens(content_no_refs)
    content_no_refs = re.sub(r'\s{2,}', ' ', content_no_refs)
    from scripts.catechism_parser import _remove_duplicate_catechism_answer_opening
    content_no_refs = _remove_duplicate_catechism_answer_opening(content_no_refs)

    if state.recent_plain:
        content_no_refs = _trim_duplicate_reference_prefix(' '.join(state.recent_plain[-3:]), content_no_refs)
        if not content_no_refs:
            return '', None, None, False, None

    if h_tag:
        if state.current_mode == "FRONT_MATTER":
            front_matter_style = config.get('front_matter_style', 'blurb')
            if front_matter_style != "prose":
                html_parts.append(
                    f'<p class="front-matter-body">'
                    f'<b>{tag_unicode_ranges(_html_escape(content_no_refs))}</b>'
                    f'</p>'
                )
                state.pending_drop_cap = False
                return '', None, None, False, None

        chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
        if chapter_match:
            chapter_label = chapter_match.group(1).rstrip('.')
            chapter_rest = (chapter_match.group(2) or '').strip()
            html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
            if not chapter_rest:
                state.pending_chapter_subtitle = True
                state.add_recent_plain(content_no_refs)
                return '', None, None, False, None

            subtitle_md, body_after_subtitle = _split_leading_chapter_subtitle(chapter_rest)
            if subtitle_md:
                subtitle = _clean_heading_text(subtitle_md)
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                content_no_refs = body_after_subtitle.strip()
                h_tag = None
                state.pending_chapter_subtitle = False
            else:
                letters = [c for c in chapter_rest if c.isalpha()]
                upper_ratio = (
                    sum(1 for c in letters if c.isupper()) / len(letters)
                    if letters else 0
                )
                if upper_ratio >= 0.72 and len(re.findall(r'\w+', chapter_rest)) <= 24:
                    subtitle = _clean_heading_text(chapter_rest)
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    state.pending_chapter_subtitle = False
                    state.add_recent_plain(content_no_refs)
                    return '', None, None, False, None
                content_no_refs = chapter_rest
                h_tag = None
                state.pending_chapter_subtitle = False

    if h_tag:
        ac_match = re.match(
            r'^([A-Z][A-Z\s,;:\u2013\u2014\-\(\)\']{18,}?)'
            r'\s+([A-Z][a-z].{40,})$',
            content_no_refs.strip(),
            re.S,
        )
        if ac_match:
            h_text = ac_match.group(1).strip().rstrip('.')
            b_text = ac_match.group(2).strip()
            letters = [c for c in h_text if c.isalpha()]
            upper_ratio = (
                sum(1 for c in letters if c.isupper()) / len(letters)
                if letters else 0
            )
            if upper_ratio >= 0.72 and len(re.findall(r'\w+', h_text)) >= 4:
                cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
                html_parts.append(f'<{h_tag}{cls}>{h_text}</{h_tag}>')
                content_no_refs = b_text
                h_tag = None

    if not h_tag:
        chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
        if chapter_match:
            state.summary_continuation_active = False
            chapter_label = chapter_match.group(1).rstrip('.')
            chapter_subtitle = _clean_heading_text(chapter_match.group(2) or '')
            html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
            if chapter_subtitle:
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(chapter_subtitle))}</h4>')
                state.pending_chapter_subtitle = False
            else:
                state.pending_chapter_subtitle = True
            state.add_recent_plain(content_no_refs)
            return '', None, None, False, None

        part_book_match = re.match(
            r'^(PART|BOOK|SECTION)\s+([IVXLCDM\d]+)(?:\s*[.—–-]\s*(.*))?$',
            content_no_refs.strip(),
            re.I,
        )
        if part_book_match:
            marker = f'{part_book_match.group(1).title()} {part_book_match.group(2).upper()}.'
            rest = (part_book_match.group(3) or '').strip()
            if rest and len(rest) > 18:
                content_no_refs = f'**{marker}** {rest}'
            else:
                part_label = part_book_match.group(0).strip()
                html_parts.append(
                    f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">'
                    f'{part_label}</h1>'
                )
                state.add_recent_plain(content_no_refs)
                return '', None, None, False, None

    if state.pending_chapter_subtitle and not h_tag:
        italic_subtitle = re.match(
            r'^_(.+)_\s*$', content_no_refs.strip(), re.S
        )
        if italic_subtitle:
            sub_text = italic_subtitle.group(1).strip()
            sub_text = re.sub(r'\s+', ' ', sub_text)
            if len(sub_text) >= 18 and len(re.findall(r'\w+', sub_text)) <= 40:
                html_parts.append(
                    f'<h4 class="chapter-subtitle">'
                    f'{tag_unicode_ranges(_html_escape(sub_text))}'
                    f'</h4>'
                )
                state.pending_chapter_subtitle = False
                state.add_recent_plain(content_no_refs)
                return '', None, None, False, None
        plain_letters = [c for c in content_no_refs if c.isalpha()]
        upper_ratio = (
            sum(1 for c in plain_letters if c.isupper()) / len(plain_letters)
            if plain_letters else 0
        )
        if len(content_no_refs) >= 18 and upper_ratio >= 0.72:
            subtitle = _clean_heading_text(content_no_refs)
            if subtitle:
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                state.pending_chapter_subtitle = False
                state.add_recent_plain(content_no_refs)
                return '', None, None, False, None
        state.pending_chapter_subtitle = False

    if not h_tag:
        if state.summary_continuation_active:
            from scripts.analysis_parser import _looks_like_summary_continuation
            plain_summary_candidate = re.sub(r'\*\*(.+?)\*\*', r'\1', content_no_refs).strip()
            if _looks_like_summary_continuation(plain_summary_candidate):
                def _render_summary_content(raw_content: str) -> str:
                    content_clean = _strip_inline_structural_tokens(raw_content)
                    content_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', content_clean)
                    def _fn_repl(m):
                        fn_num = m.group(1)
                        if fn_num in state.seen_footnote_refs:
                            return ''
                        state.seen_footnote_refs.add(fn_num)
                        return f'FNREFTOKEN{fn_num}TOKEN'
                    with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                    escaped = _html_escape(with_placeholders)
                    with_links = _restore_footnote_placeholders(escaped)
                    return tag_unicode_ranges(with_links)

                summary_piece = _render_summary_content(content_no_refs)
                if html_parts and html_parts[-1].startswith('<p class="chapter-summary">'):
                    html_parts[-1] = html_parts[-1][:-4] + f' {summary_piece}</p>'
                else:
                    html_parts.append(f'<p class="chapter-summary">{summary_piece}</p>')
                state.add_recent_plain(plain_summary_candidate)
                return '', None, None, False, None
            state.summary_continuation_active = False

        standalone_bold = re.fullmatch(r'\*\*(.+?)\*\*', content_no_refs.strip(), re.S)
        if standalone_bold:
            bold_plain = standalone_bold.group(1).strip()
            letters = [c for c in bold_plain if c.isalpha()]
            upper_ratio = (
                sum(1 for c in letters if c.isupper()) / len(letters)
                if letters else 0
            )
            if len(bold_plain) >= 12 and upper_ratio >= 0.72:
                html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(_clean_heading_text(bold_plain)))}</h4>')
                state.add_recent_plain(content_no_refs)
                return '', None, None, False, None

    subtitle_md = None
    if not h_tag:
        subtitle_md, content_no_refs = _split_leading_chapter_subtitle(content_no_refs)

    roman_heading = None
    if not h_tag and not subtitle_md:
        roman_decimal = _roman_decimal_marker_match(content_no_refs)
        if roman_decimal and roman_decimal.group('rest'):
            content_no_refs = f'**{_clean_heading_text(roman_decimal.group("marker"))}** {roman_decimal.group("rest").strip()}'
            state.roman_list_expected = None
        else:
            roman_match = ROMAN_HEADING_RE.match(content_no_refs)
            if roman_match:
                roman_number = _roman_to_int(roman_match.group('roman'))
                rest_after_roman = roman_match.group('rest').strip()
                previous_text = state.recent_plain[-1] if state.recent_plain else ''
                
                is_roman_list = False
                if roman_number == 1:
                    starts_roman_list = (
                        re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                        or re.search(r'(?:[—-]|,)\s*$', previous_text)
                    )
                    if starts_roman_list and _is_roman_list_item(rest_after_roman):
                        is_roman_list = True
                    state.roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                elif roman_number > 1:
                    if state.roman_sequence_choice == 'list-item':
                        is_roman_list = True
                    elif state.roman_sequence_choice == 'roman-subheading':
                        is_roman_list = False
                    else:
                        is_roman_list = state.roman_list_expected == roman_number
                
                if is_roman_list or state.current_mode == "FRONT_MATTER":
                    content_no_refs = f'**{roman_match.group("roman")}** {rest_after_roman}'
                    is_centered_roman_list = True
                    state.roman_list_expected = roman_number + 1 if (is_roman_list or state.current_mode == "FRONT_MATTER") else None
                else:
                    roman_heading = _render_simple_roman_heading_content(roman_match.group('roman'))
                    content_no_refs = rest_after_roman
                    state.roman_list_expected = None
            else:
                roman_section = None
                roman_head_start = _roman_head_match(content_no_refs)
                if roman_head_start:
                    roman_number = _roman_to_int(roman_head_start.group('roman'))
                    rest_after_roman = (roman_head_start.group('rest') or '').strip()
                    previous_text = state.recent_plain[-1] if state.recent_plain else ''
                    
                    is_roman_list = False
                    if roman_number == 1:
                        if _starts_roman_outline(previous_text, roman_number):
                            is_roman_list = True
                        state.roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                    elif roman_number > 1:
                        if state.roman_sequence_choice == 'list-item':
                            is_roman_list = True
                        elif state.roman_sequence_choice == 'roman-subheading':
                            is_roman_list = False
                        else:
                            is_roman_list = state.roman_list_expected == roman_number
                    
                    if is_roman_list:
                        content_no_refs = f'**{roman_head_start.group("roman")}** {rest_after_roman}'
                        is_centered_roman_list = True
                        state.roman_list_expected = roman_number + 1
                    else:
                        roman_section = _split_roman_section_opening(content_no_refs)
                if roman_section:
                    roman_heading = _render_simple_roman_heading_content(roman_section[0])
                    content_no_refs = roman_section[1]
                    state.roman_list_expected = None
                elif not roman_head_start:
                    state.roman_list_expected = None

    return content_no_refs, h_tag, subtitle_md, is_centered_roman_list, roman_heading


def _render_block_container(text_html: str, h_tag: Optional[str], subtitle_md: Optional[str], is_centered_roman_list: bool, roman_heading: Optional[str], state: ParserState, front_matter_style: str, html_parts: list[str]):
    from render import (
        _detect_signature,
        _split_rendered_inline_structural_html,
        emphasize_structural_prefix,
        tag_unicode_ranges,
    )
    from scripts.roman_parser import _roman_head_match, _roman_to_int, _is_roman_list_item, _roman_decimal_marker_match
    from shared import STRUCTURAL_START_RE, SCRIPTURE_BOOK_RE

    plain_for_class = re.sub(r'<[^>]+>', '', text_html)
    plain_for_class = re.sub(r'\s+', ' ', plain_for_class).strip()
    
    if h_tag:
        cls = ' class="secondary"' if h_tag in ('h2', 'h3') else ''
        html_parts.append(f'<{h_tag}{cls}>{text_html}</{h_tag}>')
    elif text_html.startswith('---') or text_html.startswith('***'):
        html_parts.append('<hr/>')
    elif is_centered_roman_list:
        html_parts.append(f'<p class="roman-list-item">{text_html}</p>')
    else:
        if subtitle_md:
            from scripts.roman_parser import _clean_heading_text
            subtitle_html = _clean_heading_text(subtitle_md)
            subtitle_html = tag_unicode_ranges(subtitle_html)
            if subtitle_html:
                roman_match = re.match(r'^(?P<title>.+?)\s+(?P<roman>[IVXLCDM]+\.?)$', subtitle_html)
                if roman_match and len(roman_match.group('title')) >= 18:
                    html_parts.append(f'<h4 class="chapter-subtitle">{roman_match.group("title")}</h4>')
                    html_parts.append(f'<h4 class="chapter-subtitle roman-subheading">{roman_match.group("roman")}</h4>')
                else:
                    html_parts.append(f'<h4 class="chapter-subtitle">{subtitle_html}</h4>')
        if roman_heading:
            html_parts.append(f'<h4 class="roman-subheading">{roman_heading}</h4>')
        if plain_for_class in {
            'Glory be to God on high!',
            'To Him be all glory and honor for evermore! Amen.',
        }:
            html_parts.append(f'<p class="doxology">{text_html}</p>')
        else:
            for paragraph_html in _split_rendered_inline_structural_html(text_html):
                paragraph_html = paragraph_html.lstrip()
                if not paragraph_html:
                    continue
                
                _sig_plain = re.sub(r'<[^>]+>', '', paragraph_html).strip()
                _is_signature = _detect_signature(
                    _sig_plain,
                    is_front_matter=(state.current_mode == "FRONT_MATTER"),
                )
                if _is_signature:
                    paragraph_html = re.sub(r'\s*[\u0370-\u03FF\u1F00-\u1FFF].*$', '', paragraph_html)
                    m_sig = re.match(r'^((?:<i>|<b>)*W\.\s*H\.\s*G\.(?:</i>|</b>)*)\s+((?:<i>|<b>)*[A-Z][a-z]+,.*18\d{2}\.?(?:</i>|</b>)*)\s*$', paragraph_html)
                    if m_sig:
                        paragraph_html = f'{m_sig.group(1)}<br/>{m_sig.group(2)}'
                    
                    m_study = re.match(
                        r'^((?:<i>|<b>)*[A-Z]\.[A-Z]\.(?:</i>|</b>)*)\s+'
                        r'(From\s+my\s+study\b.*?),\s*'
                        r'([A-Z][a-z]+(?:\s+the\s+last)?,\s*\[?\d{4}\]?\.?)$',
                        paragraph_html,
                        re.I
                    )
                    if m_study:
                        paragraph_html = f'{m_study.group(1)}<br/>{m_study.group(2)}<br/>{m_study.group(3)}'
                    else:
                        m_study2 = re.match(r'^((?:<i>|<b>)*[A-Z]\.[A-Z]\.(?:</i>|</b>)*)\s+(From\s+my\s+study.*)$', paragraph_html, re.I)
                        if m_study2:
                            paragraph_html = f'{m_study2.group(1)}<br/>{m_study2.group(2)}'
                    
                    html_parts.append(f'<p class="signature">{paragraph_html}</p>')
                    state.pending_drop_cap = False
                    continue

                if state.current_mode == "FRONT_MATTER":
                    if front_matter_style == "prose":
                        _emb_sig = re.search(
                            r'(,\s*|\.\s*)(<i><b>|<b><i>|<i>|<b>)([A-Z][A-Z\s]+)(</b></i>|</i></b>|</i>|</b>)\s*\.?\s*(<a[^>]*noteref[^>]*>.*?</a>)?\s*$',
                            paragraph_html,
                        )
                        if _emb_sig:
                            sig_name = _emb_sig.group(3).strip()
                            sig_words = sig_name.split()
                            if 2 <= len(sig_words) <= 4:
                                prefix = paragraph_html[:_emb_sig.start()]
                                prefix = re.sub(r'[,.\s]+$', '', prefix)
                                if prefix:
                                    html_parts.append(f'<p class="front-matter-prose">{prefix}</p>')
                                html_parts.append(f'<p class="signature">{sig_name}</p>')
                                state.pending_drop_cap = False
                                continue
                        
                        if not state.fm_prose_started:
                            p_cls = "front-matter-prose first"
                            state.fm_prose_started = True
                        else:
                            p_cls = "front-matter-prose"
                        html_parts.append(f'<p class="{p_cls}">{emphasize_structural_prefix(paragraph_html)}</p>')
                    else:
                        html_parts.append(f'<p class="front-matter-body">{paragraph_html}</p>')
                    state.pending_drop_cap = False
                else:
                    p_class = ""
                    if state.pending_drop_cap and state.current_mode == "BODY_START":
                        is_subpoint = re.match(
                            r'^(?:<b>)?(?:\([0-9IVXLCDM]+\.?\)|[0-9]+\.|[IVXLCDM]+\.|Ans\.|Sol\.|Obj\.|Objection|Answer|Solution|Use\s+\d+)', 
                            paragraph_html, re.I
                        )
                        starts_with_letter = re.match(r'^(?:<b>)?[A-Z]', paragraph_html, re.I)
                        
                        if not is_subpoint and starts_with_letter:
                            p_class = ' class="first"'
                            state.pending_drop_cap = False
                            state.current_mode = "BODY_TEXT"
                    
                    if not p_class:
                        is_qa = (
                            re.match(r'^(?:<b>)?(?:Q\.|Ques\.|Ans\.)', paragraph_html, re.I)
                            or (
                                state.is_catechism_context
                                and re.match(r'^(?:<b>)?A\.', paragraph_html, re.I)
                            )
                        )
                        is_proof = re.match(rf'^(?:<b>)?(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b', paragraph_html, re.I)
                        roman_plain_match = _roman_head_match(plain_for_class)
                        is_combined_roman_decimal = bool(_roman_decimal_marker_match(plain_for_class))
                        is_continued_roman_outline = False
                        if roman_plain_match and not is_combined_roman_decimal:
                            roman_number = _roman_to_int(roman_plain_match.group('roman'))
                            rest_after_roman = (roman_plain_match.group('rest') or '').strip()
                            is_continued_roman_outline = (
                                state.roman_list_expected == roman_number
                                and _is_roman_list_item(rest_after_roman)
                            )
                            is_long_roman_section = (
                                state.current_mode != "FRONT_MATTER"
                                and
                                not is_continued_roman_outline
                                and len(re.findall(r'\w+', rest_after_roman)) >= 12
                            )
                            if is_long_roman_section:
                                html_parts.append(f'<h4 class="roman-subheading">{paragraph_html}</h4>')
                                state.pending_drop_cap = False
                                continue
                        if is_qa or is_proof:
                            p_class = ' class="catechism-item"'
                        elif is_combined_roman_decimal:
                            p_class = ' class="list-item"'
                        elif is_continued_roman_outline:
                            p_class = ' class="roman-list-item"'
                            state.roman_list_expected = roman_number + 1
                        elif STRUCTURAL_START_RE.match(plain_for_class):
                             p_class = ' class="list-item"'
                        elif re.match(r'^(?:<b>)?Part\s+[IVXLCDM]+\.', paragraph_html, re.I):
                             p_class = ' class="list-item"'
                            
                        html_parts.append(f'<p{p_class}>{paragraph_html}</p>')
                    else:
                        html_parts.append(f'<p{p_class}>{paragraph_html}</p>')


def markdown_to_html(md_text, current_mode="BODY_TEXT", pending_drop_cap=False,
                     front_matter_style="blurb", config=None):
    from render import (
        _attach_colon_introduced_list,
        _coalesce_adjacent_signatures,
        emphasize_structural_prefix,
        tag_unicode_ranges,
    )
    if not md_text:
        return '', current_mode, pending_drop_cap

    config = config or {}

    state = ParserState(
        current_mode=current_mode,
        pending_drop_cap=pending_drop_cap,
        is_sermon_volume=bool(config.get('suppress_prefatory_note_heading')),
        next_blockquote_is_opening=False
    )

    paragraphs, is_catechism_context = _preprocess_markdown_text(md_text, config)
    state.is_catechism_context = is_catechism_context

    html_parts = []

    for para_idx, para in enumerate(paragraphs):
        stripped = para.strip()
        if not stripped:
            continue

        if re.match(r'<section\b[^>]*class="[^"]*\btreatise-title-page\b', stripped):
            from scripts.epub_builder import _polish_treatise_title_page_html
            section_match = re.match(
                r'(?P<section><section\b[^>]*class="[^"]*\btreatise-title-page\b.*?</section>)(?P<trailing>.*)$',
                stripped, re.I | re.S
            )
            if section_match:
                html_parts.append(_polish_treatise_title_page_html(section_match.group('section'), seen_footnote_refs=state.seen_footnote_refs))
                trailing = section_match.group('trailing').strip()
                if trailing:
                    paragraphs.insert(para_idx + 1, trailing)
            else:
                html_parts.append(_polish_treatise_title_page_html(stripped, seen_footnote_refs=state.seen_footnote_refs))
            continue

        if stripped.startswith('>'):
            quote_content = re.sub(r'(?:^|\n)\s*>\s?', ' ', stripped).strip()
            stripped = f'[[BLOCKQUOTE]] {quote_content}'

        clean_upper = re.sub(r'^\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*', '', stripped.upper()).strip()

        if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in [
            "PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
            "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"
        ]):
            state.current_mode = "FRONT_MATTER"
            state.pending_drop_cap = False
            state.fm_prose_started = False

        is_major_trigger = False
        if re.match(r'^(?:PART|BOOK)\s+[0-9IVXLCDM]+\.?$', clean_upper):
            is_major_trigger = True
        elif len(clean_upper) < 60 and any(kw == clean_upper.rstrip('.') for kw in [
            "CHRISTOLOGIA", "MEDITATIONS", "TWO SHORT CATECHISMS",
            "A DISCOURSE", "A TREATISE", "OF COMMUNION", "OF TEMPTATION",
            "THE NATURE", "THE DOCTRINE", "THE MORTIFICATION",
            "SERMON", "SERMONS", "INTRODUCTION",
        ]):
            is_major_trigger = True
        elif (
            len(clean_upper) >= 4 and len(clean_upper) < 55
            and clean_upper == clean_upper.upper()
            and not any(kw in clean_upper for kw in ["PREFACE", "CONTENTS", "ANALYSIS", "PREFATORY", "ADVERTISEMENT"])
            and not re.search(r'\d', clean_upper)
            and not re.search(r'\.{3}|,\s*\d+$', clean_upper)
            and state.current_mode == "FRONT_MATTER"
            and len(state.recent_plain) >= 3
        ):
            is_major_trigger = True

        if is_major_trigger:
            state.current_mode = "BODY_START"
            state.pending_drop_cap = True

        if state.current_mode == "FRONT_MATTER":
            _fm_title_kws = ["PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
                             "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"]
            if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in _fm_title_kws):
                if front_matter_style == "prose":
                    html_parts.append(
                        f'<h2 class="front-matter-heading">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.rstrip(".").title()))}'
                        f'</h2>'
                    )
                    state.fm_prose_started = False
                else:
                    html_parts.append(
                        f'<h3 class="front-matter-title">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.title()))}'
                        f'</h3>'
                    )
                state.pending_drop_cap = False
                continue

        token_match = re.match(r'^\[\[(PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*(.*)$', stripped, re.S)
        if token_match:
            kind = token_match.group(1)
            content = token_match.group(2).strip()
            handled = _process_structural_token(kind, content, state, front_matter_style, html_parts)
            if handled:
                continue

        content_no_refs, h_tag, subtitle_md, is_centered_roman_list, roman_heading = _clean_and_format_paragraph(para, state, config, html_parts)
        if not content_no_refs:
            continue

        text_html = content_no_refs
        text_html = re.sub(r'^([QA])\.\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        text_html = re.sub(r'^(Q)\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        text_html = re.sub(r'^(Q)\.,\s*(\d+)\.', r'\1. \2.', text_html)

        if not MARKDOWN_STRUCTURAL_START_RE.match(text_html):
            text_html = re.sub(r'^\*\*(?:\*\*)?', '', text_html)
            text_html = re.sub(r'\*\*(?:\*\*)?$', '', text_html)
        text_html = re.sub(r'(?<!\*)\b(\d+)\.\*\*(?=\s+)', r'\1.', text_html)

        text_html = re.sub(r'^(Q\.|Ans\.|Ques\.|A\.\s*\d+\.)\s+', r'**\1** ', text_html)
        text_html = re.sub(r'^(Q\.\s*\d+\.|A\.\s*\d+\.|Ques\.\s*\d+\.|Ans\.\s*\d+\.)\s+', r'**\1** ', text_html)

        text_html = _repair_owen_ocr_errors(text_html, config=config)

        if text_html.count('**') % 2 != 0:
            text_html = text_html.replace('**', '')

        def _repair_bold_marker(m):
            if text_html[:m.start()].count('**') % 2 != 0:
                return m.group(0)
            return f"**{m.group(1)}**"

        text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', _repair_bold_marker, text_html)
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)

        text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(A\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(Q\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(A\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(\d+\.)\s+', r'<b>\1 \2</b> ', text_html)
        text_html = re.sub(r'<b>([QA])\.</b>\s*,\s*', r'<b>\1.</b> ', text_html)

        text_html = re.sub(
            r'^(<b>A\.</b>\s+)([^<]{6,180}?[.!?;])\s+<b>A\.</b>\s+\2',
            r'\1\2',
            text_html,
            flags=re.I,
        )
        text_html = emphasize_structural_prefix(text_html)
        text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(?:<b>)?(\d+\.)(?:</b>)?\s+', r'<b>\1 \2</b> ', text_html)
        text_html = re.sub(r'(\b(?:verse|verses|chap|chapter)\.?\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html, flags=re.I)
        text_html = re.sub(r'(\b\d+:\d+(?:[-,]\s*\d+)*,\s*)<b>(\d+[.;]?)</b>', r'\1\2', text_html)
        text_html = re.sub(r'<b>(\d+(?:st|nd|rd|th))</b>(\s+(?:Psalm|Psalms)\b)', r'\1\2', text_html)

        _prev_plain = state.recent_plain[-1] if state.recent_plain else ''
        if (
            re.match(r'^<b>\d+[.;]?</b>\s', text_html)
            and re.search(r'(?:\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+)\s*,\s*$', _prev_plain)
            and not _TRANSITIONAL_WORD_RE.match(_prev_plain.strip())
        ):
            text_html = re.sub(r'^<b>(\d+[.;]?)</b>\s', r'\1 ', text_html)

        text_html = tag_unicode_ranges(text_html)
        from render import _restore_footnote_placeholders
        text_html = _restore_footnote_placeholders(text_html)

        text_html = re.sub(r',[\s,]+,', ',', text_html)
        text_html = re.sub(r',+', ',', text_html)
        text_html = re.sub(r'\.+', '.', text_html)
        text_html = re.sub(r', \.', r'.', text_html)

        text_html = re.sub(r'<b>([QA])\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)
        text_html = re.sub(r'<b>(Ques|Ans)\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)

        _render_block_container(
            text_html=text_html,
            h_tag=h_tag,
            subtitle_md=subtitle_md,
            is_centered_roman_list=is_centered_roman_list,
            roman_heading=roman_heading,
            state=state,
            front_matter_style=front_matter_style,
            html_parts=html_parts
        )

        state.add_recent_plain(content_no_refs)

    result_html = '\n'.join(html_parts)
    result_html = _attach_colon_introduced_list(result_html)
    result_html = _attach_em_dash_flat_list(result_html, config=config)
    result_html = _coalesce_adjacent_signatures(result_html)
    result_html = _merge_short_inline_lists(result_html)
    result_html = _add_owen_list_level_classes(result_html)
    result_html = _nest_owen_list_hierarchies(result_html)
    return result_html, state.current_mode, state.pending_drop_cap



