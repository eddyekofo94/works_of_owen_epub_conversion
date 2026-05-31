"""
test_v1_pipeline_regression.py
================================
Volume 1 regression guards.

Purpose: Catch pipeline regressions that affect Volume 1 when editing
shared rendering code (render.py, shared.py, converter.py).  Each test
covers a behaviour that has broken in the past.

Tests are intentionally self-contained — they call pipeline helpers
directly with hand-crafted input and assert precise output properties.
No PDF or full EPUB build is required.

Run with:
    python3 -m pytest tests/test_v1_pipeline_regression.py -v
"""

import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from shared import _repair_owen_ocr_errors
from render import (
    markdown_to_html,
    _detect_signature,
    _coalesce_adjacent_signatures,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _html(md, catechism=False, mode="FRONT_MATTER"):
    """Render markdown snippet and return the HTML string."""
    config = {'is_catechism_context': catechism} if catechism else {}
    html, _, _ = markdown_to_html(md, current_mode=mode, config=config)
    return html


def _plain(html):
    """Strip HTML tags."""
    return re.sub(r'<[^>]+>', '', html)


# ===========================================================================
# 1. OCR repair — "For, -" lone-hyphen normalisation  (Issue 44)
# ===========================================================================

class TestForCommaDashNormalisation:
    """'For, -' is an Owen construct that OCR renders as a lone hyphen.
    _repair_owen_ocr_errors must convert it to an em-dash."""

    def test_for_comma_hyphen_becomes_emdash(self):
        assert _repair_owen_ocr_errors("For, -") == "For, —"

    def test_thus_comma_hyphen_becomes_emdash(self):
        assert _repair_owen_ocr_errors("Thus, -") == "Thus, —"

    def test_wherefore_comma_hyphen_becomes_emdash(self):
        assert _repair_owen_ocr_errors("Wherefore, -") == "Wherefore, —"

    def test_trailing_space_after_hyphen_also_fixed(self):
        assert _repair_owen_ocr_errors("For, - ") == "For, —"

    def test_real_hyphen_in_word_not_touched(self):
        """Intra-word hyphens must not be converted."""
        result = _repair_owen_ocr_errors("self-evident truth")
        assert result == "self-evident truth"

    def test_em_dash_in_prose_not_doubled(self):
        """An existing em-dash must not be altered."""
        result = _repair_owen_ocr_errors("grace — that is to say")
        assert result == "grace — that is to say"


# ===========================================================================
# 2. Catechism A. label handling  (v1 Issues #30 / #11)
# ===========================================================================

class TestCatechismALabel:
    """In catechism context: bare 'A.' answer labels must be preserved.
    Outside catechism context: 'A.' before lowercase must be stripped of
    the spurious period (OCR artifact)."""

    def test_a_before_lowercase_in_body_prose_stripped(self):
        """Outside catechism: 'A. brief view' → 'A brief view' (no bold label)."""
        html = _html("A. brief view of the faith of the church.", mode="BODY_TEXT")
        plain = _plain(html)
        assert 'A brief view' in plain
        # No bold label wrapping the bare 'A.'
        assert '<b>A.</b>' not in html

    def test_a_before_uppercase_in_body_prose_preserved(self):
        """Structural 'A. THE FIRST HEAD' must not be stripped."""
        html = _html("**A.** THE FIRST HEAD of doctrine.", mode="BODY_TEXT")
        # The structural bold A. stays intact
        assert 'A.' in html

    def test_catechism_a_label_is_bolded_in_catechism_context(self):
        """In catechism context: 'A. N.' numbered answer is bold-wrapped."""
        md = "A. 3. God is a Spirit, infinite, eternal, and unchangeable."
        html = _html(md, catechism=True, mode="BODY_TEXT")
        # Label should be bold-wrapped
        assert '<b>' in html and 'A.' in html

    def test_catechism_context_does_not_bleed_across_chapters(self):
        """A chapter rendered WITHOUT catechism=True must not inherit the
        answer-label behaviour from a previously rendered catechism chapter."""
        # Render a catechism chapter first
        _html("A. 1. God is one.", catechism=True, mode="BODY_TEXT")
        # Now render a non-catechism chapter — 'A.' before lowercase must still be stripped
        html2 = _html("A. general account of the controversy.", mode="BODY_TEXT")
        plain2 = _plain(html2)
        assert 'A general account' in plain2
        assert '<b>A.</b>' not in html2


# ===========================================================================
# 3. Signature detection — individual lines  (Issues 31, 42, 46)
# ===========================================================================

class TestSignatureDetection:
    """Known v1 sign-off fragments must each be detected by _detect_signature."""

    def test_jo_bare_initials_detected(self):
        assert _detect_signature("J.O.", is_front_matter=False)

    def test_jo_spaced_initials_detected(self):
        assert _detect_signature("J. O.", is_front_matter=False)

    def test_from_my_study_standalone_detected(self):
        """Pattern 3b — 'From my Study,' must be a signature on its own."""
        assert _detect_signature("From my Study,", is_front_matter=False)

    def test_september_the_last_detected(self):
        """Pattern 5 — 'September the last, [1645].' must be a date signature."""
        assert _detect_signature("September the last, [1645].", is_front_matter=False)

    def test_whg_bare_initials_detected(self):
        assert _detect_signature("W. H. G.", is_front_matter=False)

    def test_edinburgh_month_year_detected(self):
        """Pattern 6b — 'Edinburgh, August 1850.' (place + month + year)."""
        assert _detect_signature("Edinburgh, August 1850.", is_front_matter=False)

    def test_plain_prose_not_a_signature(self):
        assert not _detect_signature(
            "From my study of the holy scriptures I have concluded that the love of God is infinite.",
            is_front_matter=False,
        )

    def test_john_owen_allcaps_in_front_matter(self):
        assert _detect_signature("JOHN OWEN", is_front_matter=True)

    def test_allcaps_name_NOT_detected_in_body(self):
        """ALL-CAPS names in body text are headings, not signatures."""
        assert not _detect_signature("THE HOLY SPIRIT", is_front_matter=False)


# ===========================================================================
# 4. Multi-paragraph signature coalescing  (Issue 31 / 46 — the core fix)
# ===========================================================================

class TestSignatureCoalescing:
    """Owen's letters split the sign-off across multiple paragraphs.
    After each line gets a signature class, _coalesce_adjacent_signatures
    must merge them into a single <p class="signature"> with <br/> joins."""

    def test_jo_three_line_coalesced(self):
        """J.O. / From my Study, / September the last, [1645]. → 1 signature."""
        html = "\n".join([
            '<p class="signature">J.O.</p>',
            '<p class="signature">From my Study,</p>',
            '<p class="signature">September the last, [1645].</p>',
        ])
        result = _coalesce_adjacent_signatures(html)
        assert result.count('<p class="signature">') == 1
        assert result.count('<br/>') == 2
        assert 'J.O.' in result
        assert 'From my Study,' in result
        assert 'September the last, [1645].' in result

    def test_whg_two_line_coalesced(self):
        """W. H. G. / Edinburgh, August 1850. → 1 signature."""
        html = "\n".join([
            '<p class="signature">W. H. G.</p>',
            '<p class="signature">Edinburgh, August 1850.</p>',
        ])
        result = _coalesce_adjacent_signatures(html)
        assert result.count('<p class="signature">') == 1
        assert result.count('<br/>') == 1

    def test_body_text_between_signatures_blocks_merge(self):
        """Two sign-offs in the same chapter (e.g., two letters) must not merge."""
        html = (
            '<p class="signature">J.O.</p>\n'
            '<p>Dearly beloved, I write again to you.</p>\n'
            '<p class="signature">W. H. G.</p>\n'
            '<p class="signature">Edinburgh, August 1850.</p>'
        )
        result = _coalesce_adjacent_signatures(html)
        # J.O. stays alone; W.H.G. and Edinburgh merge
        assert result.count('<p class="signature">') == 2

    def test_body_text_surrounding_signature_unchanged(self):
        """Body paragraphs adjacent to a lone signature must not be absorbed."""
        html = (
            '<p>Body text before.</p>\n'
            '<p class="signature">= John Owen</p>\n'
            '<p>Body text after.</p>'
        )
        result = _coalesce_adjacent_signatures(html)
        assert '<p>Body text before.</p>' in result
        assert '<p>Body text after.</p>' in result
        assert result.count('<p class="signature">') == 1


# ===========================================================================
# 5. Catechism context isolation — ensure per-chapter reset  (Issue 30 revisit)
# ===========================================================================

class TestCatechismContextIsolation:
    """The catechism flag must not bleed from one chapter call to another.
    Each call to markdown_to_html with config={'is_catechism_context': False}
    must behave as non-catechism regardless of prior calls."""

    def test_non_catechism_chapter_after_catechism_chapter_no_bleed(self):
        # Render a catechism chapter
        _html("Q. 1. Who made you?\n\nA. 1. God made me.", catechism=True, mode="BODY_TEXT")
        # A non-catechism chapter with prose 'A.' must NOT bold the label
        html = _html(
            "A. glorious representation of the love of God is here set before us.",
            catechism=False,
            mode="BODY_TEXT",
        )
        assert '<b>A.</b>' not in html
        assert 'A glorious representation' in _plain(html)

    def test_catechism_config_true_wraps_in_catechism_item(self):
        """In catechism context, A.-labeled paragraphs get class="catechism-item".
        The bold label is added by the v1 postprocess hook, but the class
        itself is applied by markdown_to_html when is_catechism_context=True."""
        html = _html("A. God made me.", catechism=True, mode="BODY_TEXT")
        # The paragraph must be classified as catechism-item (not plain body)
        assert 'catechism-item' in html


# ===========================================================================
# 6. List merging safety — period-terminated items must stay separate  (Issue 19)
# ===========================================================================

class TestListMergingSafety:
    """Short bold-labeled list items ending with periods must NOT be merged
    into a prose sentence (they are standalone theological statements)."""

    def test_period_terminated_items_not_merged(self):
        from render import _merge_short_inline_lists
        html = (
            '<p class="list-item"><b>1.</b> God is sovereign.</p>'
            '<p class="list-item"><b>2.</b> God is holy.</p>'
            '<p class="list-item"><b>3.</b> God is love.</p>'
        )
        result = _merge_short_inline_lists(html)
        # Must remain as three separate paragraphs
        assert result.count('<p class="list-item">') == 3

    def test_semicolon_terminated_items_are_merged(self):
        from render import _merge_short_inline_lists
        html = (
            '<p class="list-item"><b>1.</b> In the Father;</p>'
            '<p class="list-item"><b>2.</b> In the Son;</p>'
            '<p class="list-item"><b>3.</b> In the Holy Spirit.</p>'
        )
        result = _merge_short_inline_lists(html)
        assert result.count('<p class="list-item">') == 1


# ===========================================================================
# 7. Heading structure — key V1 heading classes present  (Issue 41)
# ===========================================================================

class TestHeadingStructure:
    """[[CHAPTER]] tokens must produce h1 elements; [[SUMMARY]] tokens must
    produce chapter-summary paragraphs and must NOT appear as raw text."""

    def test_chapter_token_produces_h1(self):
        md = "[[CHAPTER]] 1. Of the Glorious Mystery of the Incarnation"
        html = _html(md, mode="BODY_TEXT")
        assert '<h1' in html
        assert '[[CHAPTER]]' not in html

    def test_summary_token_produces_chapter_summary(self):
        md = "[[SUMMARY]] The divine nature of Christ is here declared."
        html = _html(md, mode="BODY_TEXT")
        assert 'chapter-summary' in html
        assert '[[SUMMARY]]' not in html

    def test_part_token_produces_h1_primary(self):
        md = "[[PART]] THE GLORY OF CHRIST"
        html = _html(md, mode="BODY_TEXT")
        assert 'class="primary"' in html
        assert '[[PART]]' not in html
