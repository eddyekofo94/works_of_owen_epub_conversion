import re

from scripts.owen_lists import classify_flat_list_run
from scripts.scholastic_parser import apply_scholastic_anchor_protocol, normalized_visible_text


def test_explicit_compact_syllabus_is_flat_with_diagnostics():
    decision = classify_flat_list_run(
        "There are two heads: —",
        [("<strong>1.</strong>", "Temptations;"), ("<strong>2.</strong>", "Afflictions.")],
        chapter_title="fixture-v2",
    )
    assert decision["role"] == "flat_syllabus"
    assert decision["announced_count"] == 2
    assert "announced-count-matches-run" in decision["positive_reasons"]


def test_developed_or_ambiguous_run_falls_back_to_block():
    decision = classify_flat_list_run(
        "The matter may be considered: —",
        [("<strong>1.</strong>", "This is a developed argument. It contains its own proof."),
         ("<strong>2.</strong>", "A shorter conclusion.")],
    )
    assert decision["role"] == "block_list"
    assert "multiple-sentences" in decision["hard_exclusions"]


def test_scholastic_annotation_preserves_visible_words_and_bare_continuation():
    source = '<p>Ans. 1. First answer.</p>\n<p class="list-item"><strong>2.</strong> Second answer.</p>'
    result = apply_scholastic_anchor_protocol(source)
    assert normalized_visible_text(result) == normalized_visible_text(source)
    assert "Ans. 2." not in result
    assert '<strong>2.</strong>' in result
    assert "owen-branch" not in result


def test_safe_label_ocr_spacing_is_the_only_text_change():
    result = apply_scholastic_anchor_protocol("<p>Ans .1. The reply.</p>")
    assert normalized_visible_text(result) == "Ans. 1. The reply."
    assert '<strong class="scholastic-label">Ans. 1.</strong>' in result


def test_approved_labels_and_ordinary_words():
    source = (
        "<p>Question 1. What follows?</p>\n<p>Response 1. This follows.</p>\n"
        "<p>The use of Scripture is plain, and the answer remains.</p>"
    )
    result = apply_scholastic_anchor_protocol(source)
    assert result.count("scholastic-anchor") >= 2
    assert "scholastic-parent" in result and "scholastic-child" in result
    assert "The use of Scripture" in result
    assert not re.search(r'<strong class="scholastic-label">The use', result)


def test_labels_inside_blockquotes_are_protected():
    source = '<blockquote><p>Obj. 1. Quoted, not an anchor.</p></blockquote>'
    assert apply_scholastic_anchor_protocol(source) == source
