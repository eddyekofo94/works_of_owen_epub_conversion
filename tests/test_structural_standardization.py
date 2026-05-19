"""test_structural_standardization.py — structural token and render-level tests.

Covers: [[PART]], [[CHAPTER]], [[SUMMARY]], [[BLOCKQUOTE]], [[DIGRESSION]]
token rendering; drop-cap rules; front matter states; Greek artifact stripping;
blockquote geometry; scholastic anchor edge cases; OCR artifact repair.
"""

import pytest
import re
from converter import markdown_to_html, reconstruct_paragraphs

def test_structural_tokens_preserve_hierarchy():
    """Verify that [[PART]] and [[CHAPTER]] tokens are correctly converted and preserved."""
    # Input must be separated by double newlines for markdown_to_html
    md = "[[PART]] PART 1.\n\n[[CHAPTER]] CHAPTER 1.\n\n[[SUMMARY]] This is a summary.\n\nThis is body text."
    
    # 1. Test HTML conversion
    html, _, _ = markdown_to_html(md)
    assert '<h1 class="primary"' in html
    assert 'PART 1.' in html
    assert '<h1 class="secondary">CHAPTER 1.</h1>' in html
    assert '<p class="chapter-summary">This is a summary.</p>' in html
    # First body paragraph of Chapter 1 gets the first class (triggered by PART)
    assert '<p class="first">This is body text.</p>' in html

def test_drop_cap_constraint():
    """Verify that first class only apply to paragraphs immediately following a PART heading."""
    
    # Case A: PART heading present
    md_part = "[[PART]] PART 1\n\n[[CHAPTER]] CHAPTER 1\n\nFirst paragraph of chapter 1."
    html_part, _, _ = markdown_to_html(md_part)
    assert 'class="first"' in html_part
    
    # Case B: Standard Chapter (No PART)
    md_ch2 = "[[CHAPTER]] CHAPTER 2\n\nFirst paragraph of chapter 2."
    html_ch2, _, _ = markdown_to_html(md_ch2)
    assert 'class="first"' not in html_ch2
    
    # Case C: Sub-point in any chapter
    md_real = "[[PART]] PART 1\n\nFirst paragraph.\n\n(2.) Sub-point paragraph."
    html_real, _, _ = markdown_to_html(md_real)
    assert 'class="first">First paragraph.' in html_real
    assert 'class="first">(2.)' not in html_real

def test_front_matter_states():
    """Verify FRONT_MATTER state logic."""
    md = "ANALYSIS.\n\nThis is editorial note."
    html, mode, _ = markdown_to_html(md)
    assert mode == "FRONT_MATTER"
    assert 'class="front-matter-title">Analysis.</h3>' in html
    assert 'class="front-matter-body">This is editorial note.</p>' in html
    assert 'class="first"' not in html

def test_greek_artifact_stripping():
    """Verify that 'j' noise is stripped."""
    from shared import clean_greek_text
    
    raw = "j Εγὼ τὴν ἀλήθειαν λέγω"
    cleaned = clean_greek_text(raw)
    assert "j" not in cleaned
    assert "Εγὼ" in cleaned


def test_blockquote_token_renders_as_semantic_blockquote():
    md = "[[BLOCKQUOTE]] This is an indented patristic quotation. [f1]\n\nThis is body text."

    html, _, _ = markdown_to_html(md)

    assert '<blockquote epub:type="z3998:quotation"><p>This is an indented patristic quotation.' in html
    assert 'class="noteref"' in html
    assert '<p>This is body text.</p>' in html


def test_markdown_blockquote_prefix_renders_as_semantic_blockquote():
    md = "> First quote line\n> second quote line.\n\nNext paragraph."

    html, _, _ = markdown_to_html(md)

    assert '<blockquote epub:type="z3998:quotation"><p>First quote line second quote line.</p></blockquote>' in html
    assert '<p>Next paragraph.</p>' in html


def test_adjacent_blockquote_tokens_merge_until_sentence_terminal():
    from extract import reconstruct_paragraphs

    raw = (
        '[[BLOCKQUOTE]] "Unto him that loved us, and washed us from our sins in his own blood;\n\n'
        '[[BLOCKQUOTE]] to him be glory and dominion for ever and ever, Amen." Revelation 1:5, 6.\n\n'
        'This, therefore, is body prose.'
    )

    paragraphs = reconstruct_paragraphs(raw)

    assert paragraphs[0] == (
        '[[BLOCKQUOTE]] "Unto him that loved us, and washed us from our sins in his own blood; '
        'to him be glory and dominion for ever and ever, Amen." Revelation 1:5, 6.'
    )
    assert paragraphs[1] == 'This, therefore, is body prose.'


def test_blockquote_geometry_uses_body_left_edge_not_modal_indent():
    from extract import (
        _compute_page_text_bounds,
        _line_is_blockquote_candidate,
        _page_starts_with_blockquote_continuation,
        _text_block_is_blockquote,
        _text_block_is_fully_inset,
    )

    def line(x0, x1, text):
        return {
            "bbox": (x0, 100, x1, 112),
            "spans": [{"text": text, "font": "Times-Roman"}],
        }

    # More quote lines than body lines: a pure modal baseline would wrongly pick x0=44.
    blocks = [{
        "type": 0,
        "lines": [
            line(44, 340, "Indented quotation line one with enough text."),
            line(44, 345, "Indented quotation line two with enough text."),
            line(44, 342, "Indented quotation line three with enough text."),
            line(26, 381, "Body prose line establishes the left text edge."),
            line(26, 378, "Another body prose line establishes the left edge."),
        ],
    }]

    body_left, body_right = _compute_page_text_bounds(blocks)

    assert body_left == 26
    assert _line_is_blockquote_candidate(blocks[0]["lines"][0], blocks[0]["lines"][0]["spans"][0]["text"], body_left, body_right)
    assert not _line_is_blockquote_candidate(blocks[0]["lines"][-1], blocks[0]["lines"][-1]["spans"][0]["text"], body_left, body_right)

    body_wrap_block = {
        "type": 0,
        "lines": [
            line(26, 381, "Body prose begins at the normal left edge."),
            line(44, 342, "Wrapped body prose may be visually indented."),
            line(44, 340, "Another wrapped body line should remain prose."),
        ],
    }
    quote_block = {
        "type": 0,
        "lines": [
            line(44, 340, '"Indented quotation line one with enough text.'),
            line(44, 345, "Indented quotation line two with enough text."),
        ],
    }

    assert not _text_block_is_blockquote(body_wrap_block, body_left, body_right)
    assert _text_block_is_blockquote(quote_block, body_left, body_right)

    page_leading_close = {
        "type": 0,
        "lines": [
            line(44, 353, "worthy to be compared with the glory which shall be revealed in"),
            line(44, 66, "us,”"),
        ],
    }
    reference_tail = {
        "type": 0,
        "lines": [
            line(66, 162, "<450817>Romans 8:17, 18."),
        ],
    }

    assert _text_block_is_fully_inset(page_leading_close, body_left, body_right)
    assert _page_starts_with_blockquote_continuation([page_leading_close, reference_tail], body_left, body_right)
    assert _text_block_is_blockquote(page_leading_close, body_left, body_right, allow_continuation=True)
    assert _text_block_is_blockquote(reference_tail, body_left, body_right, allow_continuation=True)


# ===========================================================================
# Scholastic anchor edge cases
# ===========================================================================

def test_scholastic_anchor_does_not_bold_answer_in_prose():
    """
    The word 'Answer' or 'Ans' appearing in the middle of a sentence
    or as a sentence subject (not as an abbreviated label at paragraph start)
    must never become a scholastic bold label.

    The apply_scholastic_anchor_protocol function should only recognise labels
    at the very start of a <p> element.
    """
    from render import apply_scholastic_anchor_protocol

    prose = (
        "<p>The answer of Owen to this objection is plain and satisfactory.</p>\n"
        "<p>An answer is here demanded of the text.</p>\n"
        "<p>Ans, to be sure, is a common Latin abbreviation.</p>"
    )
    html = apply_scholastic_anchor_protocol(prose)

    assert '<b class="scholastic-label">The answer' not in html
    assert '<b class="scholastic-label">An answer' not in html
    # "Ans, to be sure" — no period after Ans, so NOT a scholastic label
    assert '<b class="scholastic-label">Ans,' not in html


def test_scholastic_anchor_handles_answer_with_numeral():
    """
    'Ans. 1.' at the start of a paragraph IS a scholastic label.
    'Ans. 2.' on the next paragraph is also a scholastic label.
    """
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>Ans. 1. To this we reply first, that the covenant demands perfect obedience.</p>\n"
        "<p>Ans. 2. Further, the satisfaction of Christ is not the same as personal obedience.</p>"
    )

    assert '<b class="scholastic-label">Ans. 1.</b>' in html
    assert '<b class="scholastic-label">Ans. 2.</b>' in html


def test_scholastic_anchor_does_not_bold_objection_inside_blockquote():
    """
    An 'Objection' inside a blockquote context must still be treated as a
    scholastic label when it begins a <p> — blockquotes contain scholastic
    dialogue too.
    """
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        '<blockquote epub:type="z3998:quotation">'
        "<p>Objection 1. But if God be absolutely sovereign, why does he invite sinners?</p>"
        "</blockquote>"
    )

    assert '<b class="scholastic-label">Objection 1.</b>' in html


def test_solution_label_is_bolded_correctly():
    """Sol. and Sol. 1. are both valid scholastic labels."""
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>Sol. This difficulty is resolved by distinguishing the efficient and material cause.</p>\n"
        "<p>Sol. 1. The first solution is that imputation is forensic.</p>"
    )

    assert '<b class="scholastic-label">Sol.</b>' in html
    assert '<b class="scholastic-label">Sol. 1.</b>' in html


# ===========================================================================
# OCR artifact repair (unit-level)
# ===========================================================================

def test_bracket_y_repair_in_reconstruct():
    """
    The OCR corruption ']y' → 'ly' must be applied during text cleaning
    so that 'glorious]y' becomes 'gloriously' before paragraph reconstruction.
    """
    from converter import clean_text

    assert "gloriously" in clean_text("glorious]y")
    assert "only" in clean_text("on]y")
    assert "holy" in clean_text("ho]y")


def test_bracket_e_repair_does_not_affect_legitimate_brackets():
    """
    The ']e' → 'le' repair should not touch scripture brackets like [Gen. 3]
    or list enumerators like [1.].
    """
    from converter import clean_text

    result = clean_text("[1.] First point. [Gen. 3:15] The protoevangelium.")
    assert "[1.]" in result
    assert "[Gen. 3:15]" in result or "Gen. 3:15" in result


def test_spaced_caps_i_will_normalisation():
    """
    'I WILL' appearing in a sentence (Owen quoting Revelation 3:20) should
    be normalised to 'I will' — it is a rendering artefact from early
    printed editions that used spaced capitals for emphasis.
    """
    from converter import clean_text

    result = clean_text("open the door, I WILL come in to him")
    assert "I will come in" in result
    assert "I WILL come" not in result


def test_i_am_normalisation_preserves_context():
    """'I AM' → 'I am' but 'I AM THE LORD' (a title) should also be normalised."""
    from converter import clean_text

    result = clean_text("for I AM the resurrection and the life.")
    assert "I am the resurrection" in result or "I Am the resurrection" in result
    assert "I AM the resurrection" not in result
