import re
import sys
from html import escape as _html_escape, unescape as _html_unescape
from shared import *
from shared import (
    _normalize_spaced_caps, _normalize_i_will, _normalize_scholarly_citation_artifacts,
    _repair_owen_ocr_errors, _norm_for_dedupe, _is_scripture_ref_fragment,
    _scripture_ref_tokens, _split_inline_structural_markers, _repair_known_catechism_ghosts,
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


def markdown_to_html(md_text, current_mode="BODY_TEXT", pending_drop_cap=False,
                     front_matter_style="blurb", config=None):
    from render import (

        _attach_colon_introduced_list,
        _clean_heading_text,
        _coalesce_adjacent_signatures,
        _coalesce_roman_list_paragraphs,
        _detect_signature,
        _is_roman_list_item,
        _is_roman_outline_entry,
        _looks_like_summary_continuation,
        _merge_reference_continuation_paragraphs,
        _polish_treatise_title_page_html,
        _remove_duplicate_catechism_answer_opening,
        _render_simple_roman_heading_content,
        _repair_dangling_initial_splits,
        _repair_flat_list_continuation_splits,
        _repair_fused_word_ordinals,
        _repair_known_front_matter_text,
        _repair_lowercase_continuation_splits,
        _repair_mid_sentence_blockquote_splits,
        _repair_scholastic_anchor_splits,
        _repair_scholastic_blockquote_boundaries,
        _repair_sermon_prefatory_note_splits,
        _repair_transitional_word_isolation,
        _repair_unbalanced_bracket_splits,
        _restore_footnote_placeholders,
        _roman_decimal_marker_match,
        _roman_head_match,
        _roman_to_int,
        _split_inline_catechism_questions,
        _split_leading_chapter_subtitle,
        _split_rendered_inline_structural_html,
        _split_roman_section_opening,
        _split_tail_signature,
        _starts_roman_outline,
        _strip_footnote_placeholders,
        _strip_inline_structural_tokens,
        emphasize_structural_prefix,
        normalize_footnote_markers,
        tag_unicode_ranges,
    )
    """
    Convert paragraph-healed text to clean XHTML.
    Input is paragraphs separated by double newlines.
    Handles headings, bold, italic, and footnote refs.
    Issue 107: Tracks three structural states (FRONT_MATTER, BODY_START, BODY_TEXT).
    Issue 89: front_matter_style controls rendering inside FRONT_MATTER mode:
      "prose" — running editorial text (prefaces, prefatory notes, analyses):
               justified body paragraphs with a proper h2 heading.
      "blurb" — decorative title-page-adjacent content: centered italic paragraphs.
    """
    if not md_text:
        return '', current_mode, pending_drop_cap
    
    html_parts = []
    
    # 0. Character normalization (Issue: Gideon/AGES legacy encoding)
    md_text = normalize_characters(md_text)

    # Apply replacements (Issue 108)
    md_text = _split_tail_signature(md_text)
    md_text = _repair_sermon_prefatory_note_splits(md_text)
    md_text = _repair_owen_ocr_errors(md_text, config=config)
    md_text = _repair_markdown_tables(md_text)
    md_text = _repair_fused_word_ordinals(md_text)
    md_text = _repair_mid_sentence_blockquote_splits(md_text)
    md_text = _repair_scholastic_blockquote_boundaries(md_text)
    # Strip stray '+' line-continuation OCR artifacts (e.g. ",+using" → ",using")
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
    
    # Apply volume-specific coalesce hook if provided (Issue 26)
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
    paragraphs = expanded_paragraphs
    paragraphs = [_repair_known_catechism_ghosts(para) for para in paragraphs]
    recent_plain = []
    roman_list_expected = None
    roman_sequence_choice = None
    pending_chapter_subtitle = False
    summary_continuation_active = False
    seen_footnote_refs = set()
    _fm_prose_started = False  # tracks first paragraph in a prose FM section
    _is_sermon_volume = bool(config.get('suppress_prefatory_note_heading')) if config else False
    _next_blockquote_is_opening = False  # reset per chapter in sermon volumes

    # Mode and drop cap state are passed in to preserve continuity across files
    
    for para_idx, para in enumerate(paragraphs):
        stripped = para.strip()
        if not stripped:
            continue
            
        # Detect pre-rendered HTML sections (Issue 106)
        if re.match(r'<section\b[^>]*class="[^"]*\btreatise-title-page\b', stripped):
            section_match = re.match(r'(?P<section><section\b[^>]*class="[^"]*\btreatise-title-page\b.*?</section>)(?P<trailing>.*)$', stripped, re.I | re.S)
            if section_match:
                html_parts.append(_polish_treatise_title_page_html(section_match.group('section'), seen_footnote_refs=seen_footnote_refs))
                trailing = section_match.group('trailing').strip()
                if trailing:
                    paragraphs.insert(para_idx + 1, trailing)
            else:
                html_parts.append(_polish_treatise_title_page_html(stripped, seen_footnote_refs=seen_footnote_refs))
            continue

        if stripped.startswith('>'):
            quote_content = re.sub(r'(?:^|\n)\s*>\s?', ' ', stripped).strip()
            stripped = f'[[BLOCKQUOTE]] {quote_content}'

        h_tag = None
        subtitle_md = None
        roman_heading = None
        is_centered_roman_list = False

        # State Transitions (Issue 107 Refinement)
        # We strip structural tokens for trigger detection
        clean_upper = re.sub(r'^\[\[(?:PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*', '', stripped.upper()).strip()
        
        # Rule 1: Reset to FRONT_MATTER upon editorial keywords (Issue 107)
        # Match standalone keywords or those with optional trailing dot
        if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in
               ["PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
                "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"]):
            current_mode = "FRONT_MATTER"
            pending_drop_cap = False
            _fm_prose_started = False  # new section → first paragraph gets .first
        
        # Rule 2: Leave FRONT_MATTER ONLY upon Major Heading (Issue 107)
        # Supports PART 1, BOOK I, specific Owen titles, and any short all-caps
        # standalone line that signals a section beginning (for sermon volumes etc.).
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
            # Generic: short all-caps line that is not a known front-matter keyword
            # and not a TOC entry (those contain dots or page numbers)
            len(clean_upper) >= 4 and len(clean_upper) < 55
            and clean_upper == clean_upper.upper()
            and not any(kw in clean_upper for kw in ["PREFACE", "CONTENTS", "ANALYSIS", "PREFATORY", "ADVERTISEMENT"])
            and not re.search(r'\d', clean_upper)
            and not re.search(r'\.{3}|,\s*\d+$', clean_upper)
            and current_mode == "FRONT_MATTER"
            and len(recent_plain) >= 3  # Must be past the first 3 paragraphs
        ):
            is_major_trigger = True
        
        if is_major_trigger:
            current_mode = "BODY_START"
            pending_drop_cap = True
        
        # While in FRONT_MATTER, detect special titles for styling
        if current_mode == "FRONT_MATTER":
            # If it's a standalone title line, style it and continue
            _fm_title_kws = ["PREFATORY NOTE", "ANALYSIS", "PREFACE", "CONTENTS",
                             "GENERAL PREFACE", "TO THE READER", "ADVERTISEMENT"]
            if any(re.match(rf'^(?:THE\s+)?{kw}\.?$', clean_upper) for kw in _fm_title_kws):
                if front_matter_style == "prose":
                    # h2 heading, AGES green, uppercase — proper section heading
                    html_parts.append(
                        f'<h2 class="front-matter-heading">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.rstrip(".").title()))}'
                        f'</h2>'
                    )
                    _fm_prose_started = False  # next paragraph gets .first
                else:
                    html_parts.append(
                        f'<h3 class="front-matter-title">'
                        f'{tag_unicode_ranges(_html_escape(clean_upper.title()))}'
                        f'</h3>'
                    )
                pending_drop_cap = False
                continue

        # Detect explicit structural tokens from robust extractor
        token_match = re.match(r'^\[\[(PART|CHAPTER|ROMAN_HEAD|SUBTITLE|SUMMARY|DIGRESSION|BLOCKQUOTE)\]\]\s*(.*)$', stripped, re.S)
        if token_match:
            kind = token_match.group(1)
            content = token_match.group(2).strip()

            def _render_heading_content(raw_content: str) -> str:
                """Escape content for use in a heading, converting [fN] markers to noteref links."""
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'
                
                content_clean = _strip_inline_structural_tokens(raw_content)
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            def _render_blockquote_content(raw_content: str) -> str:
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'

                content_clean = _strip_inline_structural_tokens(raw_content)
                # Issue 26: strip a trailing open/left quotation mark that has no
                # matching close — the blockquote itself is the container, so an
                # unclosed opening quote at the end is always an OCR artifact.
                # Strip trailing unclosed opening quotes (Issue 26)
                content_clean = content_clean.rstrip()
                if content_clean.endswith(('“', '‘')):
                    content_clean = content_clean[:-1].rstrip()
                elif content_clean.endswith('"'):
                    if len(content_clean) <= 1 or content_clean[-2].isspace():
                        content_clean = content_clean[:-1].rstrip()
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            if kind == 'BLOCKQUOTE':
                if not content.strip():
                    continue
                
                # Blemish 9: Extract leading scripture from blockquote content
                # e.g., "[[BLOCKQUOTE]] 1 Corinthians 10:9, \"Neither...\""
                scripture_match = re.match(
                    rf'^((?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\s+\d+:\d+(?:[-,]\s*\d+)*),\s+(.*)$',
                    content, re.I | re.S
                )
                if scripture_match:
                    ref = scripture_match.group(1)
                    content = scripture_match.group(2)
                    html_parts.append(f'<p class="scripture-ref-introduction">{tag_unicode_ranges(_html_escape(ref))},</p>')

                if _next_blockquote_is_opening:
                    bq_class = ' class="sermon-opening-scripture"'
                    _next_blockquote_is_opening = False
                else:
                    bq_class = ''
                html_parts.append(f'<blockquote{bq_class} epub:type="z3998:quotation"><p class="blockquote-content">{_render_blockquote_content(content)}</p></blockquote>')
                pending_drop_cap = False
                roman_list_expected = None
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            
            # Zone A (Front Matter) Immunity: Treat all structural components as
            # simple items until we hit the Body transition.
            if current_mode == "FRONT_MATTER" and not is_major_trigger:
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
                        _fm_prose_started = False
                        pending_drop_cap = False
                        continue
                    if kind == 'ROMAN_HEAD':
                        roman_match = re.match(r'^([IVXLCDM]+\.)\s*(.*)$', content, re.I | re.S)
                        if roman_match:
                            numeral = _html_escape(roman_match.group(1))
                            rest = _render_heading_content(roman_match.group(2).strip())
                            html_parts.append(f'<p class="roman-list-item"><b>{numeral}</b> {rest}</p>')
                        else:
                            html_parts.append(f'<p class="roman-list-item">{_escaped}</p>')
                        _fm_prose_started = False
                        pending_drop_cap = False
                        continue
                    # In prose mode, structural tokens that carry a section title
                    # (PREFACE, PREFATORY NOTE, ORIGINAL PREFACE, TO THE READER,
                    # etc.) become the h2 section heading; other tokens (e.g.
                    # "Christian Reader," salutations) become h3 subheadings.
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
                    _fm_prose_started = False
                else:
                    # In blurb mode render as a bold centered paragraph
                    html_parts.append(f'<p class="front-matter-body"><b>{_escaped}</b></p>')
                pending_drop_cap = False
                continue



            def _render_summary_content(raw_content: str) -> str:
                """Render chapter-summary text without body list/scholastic styling."""
                def _fn_repl(m):
                    fn_num = m.group(1)
                    if fn_num in seen_footnote_refs:
                        return ''
                    seen_footnote_refs.add(fn_num)
                    return f'FNREFTOKEN{fn_num}TOKEN'

                content_clean = _strip_inline_structural_tokens(raw_content)
                content_clean = re.sub(r'\*\*(.+?)\*\*', r'\1', content_clean)
                with_placeholders = FOOTNOTE_MARKER_RE.sub(_fn_repl, content_clean)
                escaped = _html_escape(with_placeholders)
                with_links = _restore_footnote_placeholders(escaped)
                return tag_unicode_ranges(with_links)

            def _render_roman_heading_content(raw_content: str) -> str:
                """Render a Roman heading with only the numeral bolded."""
                content_clean = _strip_inline_structural_tokens(raw_content)
                match = _roman_head_match(content_clean)
                if not match:
                    return _render_heading_content(content_clean)
                roman_html = f'<b>{_html_escape(match.group("roman"))}</b>'
                rest = (match.group('rest') or '').strip()
                if not rest:
                    return roman_html
                return f'{roman_html} {_render_heading_content(rest)}'

            if kind == 'PART':
                summary_continuation_active = False
                html_parts.append(f'<h1 class="primary" style="text-align:center;margin:2em 0 1.5em;">{_render_heading_content(content)}</h1>')
                # Only trigger BODY_START/drop cap if it matches the pattern (Issue 107 Refinement)
                if is_major_trigger:
                    pending_drop_cap = True
                    current_mode = "BODY_START"
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'CHAPTER':
                summary_continuation_active = False
                html_parts.append(f'<h1 class="secondary">{_render_heading_content(content)}</h1>')
                # In sermon volumes, the first blockquote after each chapter heading is the opening scripture
                if _is_sermon_volume:
                    _next_blockquote_is_opening = True
                # CHAPTER does not trigger or reset pending_drop_cap (Issue 107)
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'ROMAN_HEAD':
                summary_continuation_active = False
                previous_text = recent_plain[-1] if recent_plain else ''
                
                roman_match = _roman_head_match(content)
                roman_number = _roman_to_int(roman_match.group('roman')) if roman_match else None
                
                is_roman_list = False
                if roman_number == 1:
                    is_roman_list, next_roman = _is_roman_outline_entry(
                        content,
                        previous_text,
                        roman_list_expected,
                    )
                    roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                elif roman_number is not None and roman_number > 1:
                    if roman_sequence_choice == 'list-item':
                        is_roman_list = True
                    elif roman_sequence_choice == 'roman-subheading':
                        is_roman_list = False
                    else:
                        is_roman_list, next_roman = _is_roman_outline_entry(
                            content,
                            previous_text,
                            roman_list_expected,
                        )
                else:
                    is_roman_list, next_roman = _is_roman_outline_entry(
                        content,
                        previous_text,
                        roman_list_expected,
                    )

                if current_mode == "FRONT_MATTER":
                    html_parts.append(f'<p class="roman-list-item">{_render_roman_heading_content(content)}</p>')
                    roman_list_expected = roman_number + 1 if (is_roman_list and roman_number is not None) else None
                elif is_roman_list:
                    html_parts.append(f'<p class="roman-list-item">{_render_roman_heading_content(content)}</p>')
                    roman_list_expected = roman_number + 1 if roman_number is not None else None
                else:
                    html_parts.append(f'<h4 class="roman-subheading">{_render_roman_heading_content(content)}</h4>')
                    roman_list_expected = None
                pending_drop_cap = False
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'SUBTITLE':
                summary_continuation_active = False
                # Catechism protection: don't render Q./A. as subtitles (Issue 102)
                if re.match(r'^(?:\*\*)?(?:Q\.|Ques\.|A\.|Ans\.)\s*(?:\d+\.)?\s*(?:\*\*)?', content, re.I):
                    stripped = content
                    # Fall through to normal paragraph rendering
                else:
                    html_parts.append(f'<h4 class="chapter-subtitle">{_render_heading_content(content)}</h4>')
                    recent_plain.append(_strip_footnote_placeholders(content))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            elif kind == 'SUMMARY':
                # Blemish 7: Some chapter summaries begin with an all-caps titled
                # heading (the sub-topic title of the treatise) followed by a mixed-
                # case synopsis sentence.  Detect this and render the heading as
                # <h3 class="chapter-heading"> (slightly smaller than the chapter
                # title, larger than the synopsis) and the synopsis separately.
                #
                # Heuristic: content starts with ≥10-char all-caps run ending in
                # sentence punctuation, immediately followed by a mixed-case sentence.
                # Pure Roman-numeral tokens are excluded (handled by ROMAN_HEAD).
                _summary_heading_re = re.compile(
                    r"^(?P<heading>[A-Z][A-Z\s,;:'\u2018\u2019\u2014\-]{9,}[.!?])\s+"
                    r"(?P<synopsis>[\dA-Z\"\u201c\u2018(].{10,})$",
                    re.S,
                )
                # Issue 28: a footnote number immediately after sentence punctuation
                # (e.g. "AUGUSTINE.133") prevents the heading/synopsis split because
                # digits are not in the heading character class.  Strip inline
                # footnote refs (digits following [.!?] before a space) so the
                # heuristic sees clean all-caps heading text.
                _content_for_split = re.sub(
                    r'([.!?])(\d{1,4})(?=\s+[A-Z\"\u201c\u2018(])', r'\1', content.strip()
                )
                _smatch = _summary_heading_re.match(_content_for_split)
                # Synopsis must contain lowercase letters to confirm it's genuinely
                # mixed-case (avoids splitting a second all-caps run as heading+synopsis).
                _synopsis_has_lower = (
                    _smatch and bool(re.search(r'[a-z]', _smatch.group('synopsis')[:80]))
                )
                if _smatch and _synopsis_has_lower and not ROMAN_ONLY_RE.match(
                    _smatch.group('heading').rstrip('.!? ').strip()
                ):
                    # Case 2: All-caps heading + mixed-case synopsis in same paragraph.
                    # The synopsis may continue into the next paragraph (e.g. long
                    # outlines split across PDF pages), so keep continuation active.
                    h_text = _smatch.group('heading').strip()
                    s_text = _smatch.group('synopsis').strip()
                    html_parts.append(
                        f'<h3 class="chapter-heading">{_render_heading_content(h_text)}</h3>'
                    )
                    html_parts.append(
                        f'<p class="chapter-summary">{_render_summary_content(s_text)}</p>'
                    )
                    summary_continuation_active = True
                else:
                    # Distinguish Case 1 (entirely all-caps) from Case 3 (mixed-case synopsis).
                    # Owen chapter sub-headings are all-caps outline entries; synopses are prose.
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
                        # Case 1: Entirely all-caps → chapter sub-heading, body text follows.
                        html_parts.append(
                            f'<h3 class="chapter-heading">{_render_heading_content(content)}</h3>'
                        )
                        summary_continuation_active = False
                    else:
                        # Case 3: Mixed-case synopsis paragraph; continuation may follow.
                        html_parts.append(
                            f'<p class="chapter-summary">{_render_summary_content(content)}</p>'
                        )
                        summary_continuation_active = True
                # SUMMARY does not trigger or reset pending_drop_cap (Issue 107)
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue
            elif kind == 'DIGRESSION':
                summary_continuation_active = False
                # Generate unique ID for Digressions
                num_match = re.search(r'\d+', content)
                d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
                html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{_render_heading_content(content.upper().rstrip("."))}</h3>')
                pending_drop_cap = False
                recent_plain.append(_strip_footnote_placeholders(content))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

            # Fall through for non-structural content or protected Q/A
            # (continue not called above)
            pass
        
        # Detect heading level from leading #
        h_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
        
        if h_match:
            level = len(h_match.group(1))
            content = h_match.group(2)
            # Standard markdown Digression handling
            if 'DIGRESSION' in content.upper():
                num_match = re.search(r'\d+', content)
                d_id = f"digression-{num_match.group(0)}" if num_match else "digression-sub"
                html_parts.append(f'<h3 id="{d_id}" class="digression-heading">{tag_unicode_ranges(_html_escape(content.upper().rstrip(".")))}</h3>')
                pending_drop_cap = False
                continue
            h_tag = 'h1' if level <= 2 else ('h2' if level <= 4 else 'h3')
        else:
            content = stripped
            h_tag = None

        # Fix floating letter issue by stripping leading whitespace
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
        
        # Process footnote markers [fN]
        roman_list_match = re.match(rf'^{re.escape(ROMAN_LIST_TOKEN)}\s+([IVXLCDM]+\.?)\s+(.+)$', content)
        is_centered_roman_list = False
        if roman_list_match:
            is_centered_roman_list = True
            content = f'**{roman_list_match.group(1)}** {roman_list_match.group(2).strip()}'
            h_tag = None

        def footnote_marker_repl(match):
            fn_num = match.group(1)
            if fn_num in seen_footnote_refs:
                return ''
            seen_footnote_refs.add(fn_num)
            return f'FNREFTOKEN{fn_num}TOKEN'

        content_no_refs = FOOTNOTE_MARKER_RE.sub(footnote_marker_repl, content).strip()
        content_no_refs = _strip_inline_structural_tokens(content_no_refs)
        content_no_refs = re.sub(r'\s{2,}', ' ', content_no_refs)
        content_no_refs = _remove_duplicate_catechism_answer_opening(content_no_refs)
        content_no_refs = _repair_known_front_matter_text(content_no_refs)
        if recent_plain:
            content_no_refs = _trim_duplicate_reference_prefix(' '.join(recent_plain[-3:]), content_no_refs)
            if not content_no_refs:
                continue

        if h_tag:
            if current_mode == "FRONT_MATTER":
                if front_matter_style == "prose":
                    # In prose mode, let the heading fall through to normal
                    # heading rendering below (h2/h3 as appropriate).
                    pass
                else:
                    # Blurb mode: suppress markdown headings into bold centered
                    # paragraphs to avoid oversized numerals on title-adjacent pages.
                    html_parts.append(
                        f'<p class="front-matter-body">'
                        f'<b>{tag_unicode_ranges(_html_escape(content_no_refs))}</b>'
                        f'</p>'
                    )
                    pending_drop_cap = False
                    continue

            chapter_match = PLAIN_CHAPTER_RE.match(content_no_refs)
            if chapter_match:
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_rest = (chapter_match.group(2) or '').strip()
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if not chapter_rest:
                    pending_chapter_subtitle = True
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

                subtitle_md, body_after_subtitle = _split_leading_chapter_subtitle(chapter_rest)
                if subtitle_md:
                    subtitle = _clean_heading_text(subtitle_md)
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    content_no_refs = body_after_subtitle.strip()
                    h_tag = None
                    pending_chapter_subtitle = False
                else:
                    letters = [c for c in chapter_rest if c.isalpha()]
                    upper_ratio = (
                        sum(1 for c in letters if c.isupper()) / len(letters)
                        if letters else 0
                    )
                    if upper_ratio >= 0.72 and len(re.findall(r'\w+', chapter_rest)) <= 24:
                        subtitle = _clean_heading_text(chapter_rest)
                        html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                        pending_chapter_subtitle = False
                        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                        if len(recent_plain) > 5:
                            recent_plain = recent_plain[-5:]
                        continue
                    content_no_refs = chapter_rest
                    h_tag = None
                    pending_chapter_subtitle = False

        if h_tag:
            # Generic all-caps heading absorption split:
            # e.g. "THE DOCTRINE...VINDICATED The doctrine of..."
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
                summary_continuation_active = False
                chapter_label = chapter_match.group(1).rstrip('.')
                chapter_subtitle = _clean_heading_text(chapter_match.group(2) or '')
                html_parts.append(f'<h3 class="secondary">{chapter_label}</h3>')
                if chapter_subtitle:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(chapter_subtitle))}</h4>')
                    pending_chapter_subtitle = False
                else:
                    pending_chapter_subtitle = True
                recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                if len(recent_plain) > 5:
                    recent_plain = recent_plain[-5:]
                continue

            # PART/BOOK/SECTION headings → premium title-page style
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
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

        if pending_chapter_subtitle and not h_tag:
            # Detect italic chapter subtitles (Volume 2 pattern)
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
                    pending_chapter_subtitle = False
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            plain_letters = [c for c in content_no_refs if c.isalpha()]
            upper_ratio = (
                sum(1 for c in plain_letters if c.isupper()) / len(plain_letters)
                if plain_letters else 0
            )
            if len(content_no_refs) >= 18 and upper_ratio >= 0.72:
                subtitle = _clean_heading_text(content_no_refs)
                if subtitle:
                    html_parts.append(f'<h4 class="chapter-subtitle">{tag_unicode_ranges(_html_escape(subtitle))}</h4>')
                    pending_chapter_subtitle = False
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
            pending_chapter_subtitle = False

        if not h_tag:
            if summary_continuation_active:
                plain_summary_candidate = re.sub(r'\*\*(.+?)\*\*', r'\1', content_no_refs).strip()
                if _looks_like_summary_continuation(plain_summary_candidate):
                    summary_piece = _render_summary_content(content_no_refs)
                    if html_parts and html_parts[-1].startswith('<p class="chapter-summary">'):
                        html_parts[-1] = html_parts[-1][:-4] + f' {summary_piece}</p>'
                    else:
                        html_parts.append(f'<p class="chapter-summary">{summary_piece}</p>')
                    recent_plain.append(_strip_footnote_placeholders(plain_summary_candidate))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue
                summary_continuation_active = False

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
                    recent_plain.append(_strip_footnote_placeholders(content_no_refs))
                    if len(recent_plain) > 5:
                        recent_plain = recent_plain[-5:]
                    continue

        if not h_tag:
            subtitle_md, content_no_refs = _split_leading_chapter_subtitle(content_no_refs)

        if not h_tag and not subtitle_md:
            roman_decimal = _roman_decimal_marker_match(content_no_refs)
            if roman_decimal and roman_decimal.group('rest'):
                content_no_refs = f'**{_clean_heading_text(roman_decimal.group("marker"))}** {roman_decimal.group("rest").strip()}'
                roman_list_expected = None
            else:
                roman_match = ROMAN_HEADING_RE.match(content_no_refs)
                if roman_match:
                    roman_number = _roman_to_int(roman_match.group('roman'))
                    rest_after_roman = roman_match.group('rest').strip()
                    previous_text = recent_plain[-1] if recent_plain else ''
                    
                    is_roman_list = False
                    if roman_number == 1:
                        starts_roman_list = (
                            re.search(r'\b(?:heads|ways|parts|sorts|things)\s*:\s*(?:[—-]\s*)?$', previous_text, re.I)
                            or re.search(r'(?:[—-]|,)\s*$', previous_text)
                        )
                        if starts_roman_list and _is_roman_list_item(rest_after_roman):
                            is_roman_list = True
                        roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                    elif roman_number > 1:
                        if roman_sequence_choice == 'list-item':
                            is_roman_list = True
                        elif roman_sequence_choice == 'roman-subheading':
                            is_roman_list = False
                        else:
                            is_roman_list = roman_list_expected == roman_number
                    
                    if is_roman_list or current_mode == "FRONT_MATTER":
                        content_no_refs = f'**{roman_match.group("roman")}** {rest_after_roman}'
                        is_centered_roman_list = True
                        roman_list_expected = roman_number + 1 if (is_roman_list or current_mode == "FRONT_MATTER") else None
                    else:
                        roman_heading = _render_simple_roman_heading_content(roman_match.group('roman'))
                        content_no_refs = rest_after_roman
                        roman_list_expected = None
                else:
                    roman_section = None
                    roman_head_start = _roman_head_match(content_no_refs)
                    if roman_head_start:
                        roman_number = _roman_to_int(roman_head_start.group('roman'))
                        rest_after_roman = (roman_head_start.group('rest') or '').strip()
                        previous_text = recent_plain[-1] if recent_plain else ''
                        
                        is_roman_list = False
                        if roman_number == 1:
                            if _starts_roman_outline(previous_text, roman_number):
                                is_roman_list = True
                            roman_sequence_choice = 'list-item' if is_roman_list else 'roman-subheading'
                        elif roman_number > 1:
                            if roman_sequence_choice == 'list-item':
                                is_roman_list = True
                            elif roman_sequence_choice == 'roman-subheading':
                                is_roman_list = False
                            else:
                                is_roman_list = roman_list_expected == roman_number
                        
                        if is_roman_list:
                            content_no_refs = f'**{roman_head_start.group("roman")}** {rest_after_roman}'
                            is_centered_roman_list = True
                            roman_list_expected = roman_number + 1
                        else:
                            roman_section = _split_roman_section_opening(content_no_refs)
                    if roman_section:
                        roman_heading = _render_simple_roman_heading_content(roman_section[0])
                        content_no_refs = roman_section[1]
                        roman_list_expected = None
                    elif not roman_head_start:
                        roman_list_expected = None
        
        # Clean up Catechism artifacts (Issue 26)
        text_html = content_no_refs
        
        # 1. Standardize Q/A labels: "Q. , , 8 ." -> "Q. 8."
        # CASE-SENSITIVE and strictly anchored to start of paragraph (Issue 26)
        text_html = re.sub(r'^([QA])\.\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        text_html = re.sub(r'^(Q)\s*[, ]+\s*(\d+)\s*\.', r'\1. \2.', text_html)
        # Handle "Q., 8." (Issue 26)
        text_html = re.sub(r'^(Q)\.,\s*(\d+)\.', r'\1. \2.', text_html)
        
        # 2. Cleanup leading/trailing bold artifacts
        if not MARKDOWN_STRUCTURAL_START_RE.match(text_html):
            text_html = re.sub(r'^\*\*(?:\*\*)?', '', text_html)
            text_html = re.sub(r'\*\*(?:\*\*)?$', '', text_html)
        # Specifically remove surviving .** artifact (Issue 91/107)
        text_html = re.sub(r'(?<!\*)\b(\d+)\.\*\*(?=\s+)', r'\1.', text_html)
        
        # Standardize Q/A labels for bolding (CASE-SENSITIVE, anchored)
        # Only allow A if followed by period or Ans/Ques (Issue 26)
        text_html = re.sub(r'^(Q\.|Ans\.|Ques\.|A\.\s*\d+\.)\s+', r'**\1** ', text_html)
        # For Q. N. form
        text_html = re.sub(r'^(Q\.\s*\d+\.|A\.\s*\d+\.|Ques\.\s*\d+\.|Ans\.\s*\d+\.)\s+', r'**\1** ', text_html)

        # Apply replacements again on the standard markers (Issue 108)
        text_html = _repair_owen_ocr_errors(text_html, config=config)

        # Cleanup unbalanced bold markers (Issue 26)
        if text_html.count('**') % 2 != 0:
            text_html = text_html.replace('**', '')
            
        def _repair_bold_marker(m):
            # Check if there is an unclosed ** before this match (Issue 91/107)
            if text_html[:m.start()].count('**') % 2 != 0:
                return m.group(0)
            return f"**{m.group(1)}**"
            
        text_html = re.sub(r'(?<!\*)\b(\d+\.)\*\*(?=\s+)', _repair_bold_marker, text_html)
        text_html = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)
        text_html = re.sub(r'(?<!\*)_(.+?)_(?!\*)', r'<i>\1</i>', text_html)
        text_html = re.sub(rf'\s*\*\*\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', ' ', text_html, flags=re.I)
        
        # Clean up bolding on Q/A numbers
        text_html = re.sub(r'<b>(Q\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(A\.\s*)</b>(\d+\.)\*\*', r'<b>\1\2</b>', text_html)
        text_html = re.sub(r'<b>(Q\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(A\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.\s*\d+\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ans\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'<b>(Ques\.)</b>\s+', r'<b>\1</b> ', text_html)
        text_html = re.sub(r'^<b>([IVXLCDM]+\.)</b>\s+(\d+\.)\s+', r'<b>\1 \2</b> ', text_html)
        
        # Specific comma artifact cleanup (Issue 26)
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
        # Issue 27: if the paragraph STARTS with a bare bold number (e.g. <b>9.</b>) and
        # the previous paragraph ended with a scripture reference trailing comma or
        # a bare comma (suggesting a verse-range continuation split across lines),
        # the bold is spurious — undo it.
        _prev_plain = recent_plain[-1] if recent_plain else ''
        if (
            re.match(r'^<b>\d+[.;]?</b>\s', text_html)
            and re.search(r'(?:\b\d+:\d+(?:[-,]\s*\d+)*|\b\d+)\s*,\s*$', _prev_plain)
            and not _TRANSITIONAL_WORD_RE.match(_prev_plain.strip())
        ):
            text_html = re.sub(r'^<b>(\d+[.;]?)</b>\s', r'\1 ', text_html)
        
        # Tag Unicode Greek/Hebrew ranges
        text_html = tag_unicode_ranges(text_html)
        text_html = _restore_footnote_placeholders(text_html)
        
        # Final punctuation normalization (Issue 26)
        text_html = re.sub(r',[\s,]+,', ',', text_html)
        text_html = re.sub(r',+', ',', text_html)
        text_html = re.sub(r'\.+', '.', text_html)
        text_html = re.sub(r', \.', r'.', text_html)
        
        # Ensure Q/A bolding includes the number
        text_html = re.sub(r'<b>([QA])\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)
        text_html = re.sub(r'<b>(Ques|Ans)\.</b>\s+(\d+)\.', r'<b>\1. \2.</b>', text_html)

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
                subtitle_html = _clean_heading_text(subtitle_md)
                subtitle_html = tag_unicode_ranges(subtitle_html)
                if not subtitle_html:
                    pass
                else:
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
                    # Strip leading whitespace/hidden chars to fix the "floating letter" issue
                    paragraph_html = paragraph_html.lstrip()
                    if not paragraph_html:
                        continue
                    
                    # Signature detection — consolidated helper (replaces fragmented patterns)
                    _sig_plain = re.sub(r'<[^>]+>', '', paragraph_html).strip()
                    _is_signature = _detect_signature(
                        _sig_plain,
                        is_front_matter=(current_mode == "FRONT_MATTER"),
                    )
                    if _is_signature:
                        # Strip trailing Greek residue if it was pulled in (Issue 26)
                        paragraph_html = re.sub(r'\s*[\u0370-\u03FF\u1F00-\u1FFF].*$', '', paragraph_html)
                        
                        # Split Goold signature into two lines (Issue 99)
                        m_sig = re.match(r'^((?:<i>|<b>)*W\.\s*H\.\s*G\.(?:</i>|</b>)*)\s+((?:<i>|<b>)*[A-Z][a-z]+,.*18\d{2}\.?(?:</i>|</b>)*)\s*$', paragraph_html)
                        if m_sig:
                            paragraph_html = f'{m_sig.group(1)}<br/>{m_sig.group(2)}'
                        
                        # Split J.O. study signature: "J.O. From my study, September..."
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
                        pending_drop_cap = False
                        continue

                    # Rule 1: FRONT_MATTER rules
                    if current_mode == "FRONT_MATTER":
                        if front_matter_style == "prose":
                            # Check for embedded signature at end of paragraph (e.g., "...DANIEL BURGESS</b></i>")
                            _emb_sig = re.search(
                                r'(,\s*|\.\s*)(<i><b>|<b><i>|<i>|<b>)([A-Z][A-Z\s]+)(</b></i>|</i></b>|</i>|</b>)\s*\.?\s*(<a[^>]*noteref[^>]*>.*?</a>)?\s*$',
                                paragraph_html,
                            )
                            if _emb_sig:
                                sig_name = _emb_sig.group(3).strip()
                                sig_words = sig_name.split()
                                # Only treat as signature if 2-4 all-caps words (name)
                                if 2 <= len(sig_words) <= 4:
                                    prefix = paragraph_html[:_emb_sig.start()]
                                    # Remove trailing comma/space from prefix
                                    prefix = re.sub(r'[,.\s]+$', '', prefix)
                                    if prefix:
                                        html_parts.append(f'<p class="front-matter-prose">{prefix}</p>')
                                    html_parts.append(f'<p class="signature">{sig_name}</p>')
                                    pending_drop_cap = False
                                    continue
                            
                            # Running editorial prose: justify like normal body text.
                            if not _fm_prose_started:
                                p_cls = "front-matter-prose first"
                                _fm_prose_started = True
                            else:
                                p_cls = "front-matter-prose"
                            # Run prefix bolding on front-matter prose lists
                            paragraph_html = emphasize_structural_prefix(paragraph_html)
                            html_parts.append(f'<p class="{p_cls}">{paragraph_html}</p>')
                        else:
                            # Blurb: centered italic for decorative title-page content.
                            html_parts.append(f'<p class="front-matter-body">{paragraph_html}</p>')
                        pending_drop_cap = False
                    else:
                        # User-mandated Drop Cap Constraint (States 2 and 3)
                        p_class = ""
                        if pending_drop_cap and current_mode == "BODY_START":
                            # Exclude sub-points from drop caps (e.g. '(2.)', '1.', 'I.', 'Ans.')
                            # User: Never turn a character into a drop cap if it is a parenthesis ( or a number 1.
                            is_subpoint = re.match(
                                r'^(?:<b>)?(?:\([0-9IVXLCDM]+\.?\)|[0-9]+\.|[IVXLCDM]+\.|Ans\.|Sol\.|Obj\.|Objection|Answer|Solution|Use\s+\d+)', 
                                paragraph_html, re.I
                            )
                            # Also ensure the paragraph starts with a letter if we are to drop-cap it
                            starts_with_letter = re.match(r'^(?:<b>)?[A-Z]', paragraph_html, re.I)
                            
                            if not is_subpoint and starts_with_letter:
                                p_class = ' class="first"'
                                pending_drop_cap = False
                                current_mode = "BODY_TEXT" # Transition to State 3
                            # If is_subpoint or doesn't start with letter, we stay in BODY_START/pending_drop_cap=True
                        
                        # Catechism or List styling
                        if not p_class:
                            is_qa = (
                                re.match(r'^(?:<b>)?(?:Q\.|Ques\.|Ans\.)', paragraph_html, re.I)
                                or (
                                    is_catechism_context
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
                                    roman_list_expected == roman_number
                                    and _is_roman_list_item(rest_after_roman)
                                )
                                is_long_roman_section = (
                                    current_mode != "FRONT_MATTER"
                                    and
                                    not is_continued_roman_outline
                                    and len(re.findall(r'\w+', rest_after_roman)) >= 12
                                )
                                if is_long_roman_section:
                                    html_parts.append(f'<h4 class="roman-subheading">{paragraph_html}</h4>')
                                    pending_drop_cap = False
                                    continue
                            if is_qa or is_proof:
                                p_class = ' class="catechism-item"'
                            elif is_combined_roman_decimal:
                                p_class = ' class="list-item"'
                            elif is_continued_roman_outline:
                                p_class = ' class="roman-list-item"'
                                roman_list_expected = roman_number + 1
                            elif STRUCTURAL_START_RE.match(plain_for_class):
                                 # Numbered/lettered lists (Issue 23/26)
                                 p_class = ' class="list-item"'
                            elif re.match(r'^(?:<b>)?Part\s+[IVXLCDM]+\.', paragraph_html, re.I):
                                 p_class = ' class="list-item"'
                                
                            html_parts.append(f'<p{p_class}>{paragraph_html}</p>')
                        else:
                            html_parts.append(f'<p{p_class}>{paragraph_html}</p>')


        recent_plain.append(_strip_footnote_placeholders(content_no_refs))
        if len(recent_plain) > 5:
            recent_plain = recent_plain[-5:]
    
    result_html = '\n'.join(html_parts)
    result_html = _attach_colon_introduced_list(result_html)
    result_html = _attach_em_dash_flat_list(result_html, config=config)
    result_html = _coalesce_adjacent_signatures(result_html)
    result_html = _merge_short_inline_lists(result_html)
    result_html = _add_owen_list_level_classes(result_html)
    result_html = _nest_owen_list_hierarchies(result_html)
    return result_html, current_mode, pending_drop_cap



