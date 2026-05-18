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
