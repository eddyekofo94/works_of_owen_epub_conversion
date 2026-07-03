import re

from scripts.owen_lists import (
    _attach_em_dash_flat_list,
    _merge_short_inline_lists,
    classify_flat_list_run,
    last_meaningful_visible_char,
)
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


def test_strong_formula_syllabus_is_flat_without_exact_count():
    decision = classify_flat_list_run(
        "The particulars to be observed are these: —",
        [
            ("<strong>1.</strong>", "The person considered."),
            ("<strong>2.</strong>", "The office declared."),
            ("<strong>3.</strong>", "The use applied."),
        ],
        chapter_title="fixture-v1",
    )
    assert decision["role"] == "flat_syllabus"
    assert "introductory-formula" in decision["positive_reasons"]


def test_roman_exact_count_syllabus_is_flat_with_diagnostics():
    result = _attach_em_dash_flat_list(
        '<p>After three inquiries already handled, the respect may be reduced unto these four heads:</p>\n'
        '<p class="roman-list-item"><strong>I.</strong> Honor.</p>\n'
        '<p class="roman-list-item"><strong>II.</strong> Obedience.</p>\n'
        '<p class="roman-list-item"><strong>III.</strong> Conformity.</p>\n'
        '<p class="roman-list-item"><strong>IV.</strong> The use of him in all Gospel privileges.</p>'
    )
    assert result.count("<p") == 1
    assert 'class="syllabus-anchor"' in result
    assert "<strong>IV.</strong> The use of him" in result


def test_long_multiclass_list_item_anchor_absorbs_roman_syllabus():
    result = _attach_em_dash_flat_list(
        '<p class="list-item list-level-1 block-list-primary"><strong>Secondly,</strong> '
        'After three inquiries already handled, the Scripture may be reduced unto these four heads: —</p>\n'
        '<p class="roman-list-item list-level-2 block-list-subpoint"><strong>I.</strong> The assumption of our nature.</p>\n'
        '<p class="roman-list-item list-level-2 block-list-subpoint"><strong>II.</strong> The union of the two natures.</p>\n'
        '<p class="roman-list-item list-level-2 block-list-subpoint"><strong>III.</strong> The mutual communication.</p>\n'
        '<p class="roman-list-item list-level-2 block-list-subpoint"><strong>IV.</strong> The enunciations concerning Christ.</p>'
    )
    assert result.count("<p") == 1
    assert 'class="list-item list-level-1 block-list-primary syllabus-anchor"' in result
    assert "<strong>IV.</strong> The enunciations concerning Christ." in result


def test_partial_inline_roman_syllabus_absorbs_final_roman_item():
    result = _attach_em_dash_flat_list(
        '<p class="syllabus-anchor">The respect may be reduced unto these four heads: '
        '<strong>I.</strong> Honor. <strong>II.</strong> Obedience. '
        '<strong>III.</strong> Conformity.</p>\n'
        '<p class="roman-list-item list-level-1 block-list-primary"><strong>IV.</strong> '
        'The use we make of him, for the attaining and receiving of all Gospel privileges.</p>'
    )
    assert result.count("<p") == 1
    assert "<strong>III.</strong> Conformity. <strong>IV.</strong> The use we make of him" in result


def test_developed_or_ambiguous_run_falls_back_to_block():
    decision = classify_flat_list_run(
        "The matter may be considered: —",
        [("<strong>1.</strong>", "This is a developed argument. It contains its own proof."),
         ("<strong>2.</strong>", "A shorter conclusion.")],
    )
    assert decision["role"] == "block_list"
    assert "multiple-sentences" in decision["hard_exclusions"]


def test_announced_scholastic_gloss_run_is_flat_despite_long_glosses():
    decision = classify_flat_list_run(
        "The gospel is declared: Romans 1:1-4; 1 Corinthians 1:23, 24; "
        "Galatians 3:1. Wherefore three things are herein to be considered.",
        [
            (
                "<strong>1.</strong>",
                '"Objectum reale et formale fidei" — "the real, formal object of our '
                "faith in this matter. This is the person of Christ, the Son of God "
                "incarnate, the representative image of the glory of God unto us.",
            ),
            (
                "<strong>2.</strong>",
                '"Medium revelans", or "lumen deferens" — the means of its revelation, '
                "or the objective light whereby the perception and knowledge of it is "
                "conveyed unto our minds. This is the gospel: 2 Corinthians 3:18.",
            ),
            (
                "<strong>3.</strong>",
                '"Lumen praeparans, elevans, disponens subjectum" — "the internal '
                "light of the mind in the saving illumination of the Holy Spirit, "
                "enabling us spiritually to behold and discern the glory of God in "
                "the face of Christ: 2 Corinthians 4:6.",
            ),
        ],
        chapter_title="Chapter 5 - The Person of Christ the Great Representative of God and His Will",
    )
    assert decision["role"] == "flat_syllabus"
    assert decision["announced_count"] == 3
    assert "scholastic-gloss-run" in decision["positive_reasons"]
    assert "developed-item" not in decision["hard_exclusions"]
    assert "scripture-density" not in decision["hard_exclusions"]


def test_long_announced_non_scholastic_run_still_remains_block():
    decision = classify_flat_list_run(
        "Wherefore three things are herein to be considered.",
        [
            ("<strong>1.</strong>", "The first head is argued at length. This is the proof of it from Scripture."),
            ("<strong>2.</strong>", "The second head is also argued at length. This is another proof."),
            ("<strong>3.</strong>", "The third head concludes the matter. This is the final proof."),
        ],
    )
    assert decision["role"] == "block_list"
    assert "scholastic-gloss-run" not in decision["positive_reasons"]
    assert "multiple-sentences" in decision["hard_exclusions"]


def test_scholastic_gloss_flattening_handles_adjacent_paragraph_tags_without_newlines():
    source = (
        '<p>Wherefore three things are herein to be considered.</p>'
        '<p class="list-item"><strong>1.</strong> "Objectum reale et formale fidei" — '
        '"the real, formal object of our faith in this matter. This is the person of Christ.</p>'
        '<p class="list-item"><strong>2.</strong> "Medium revelans", or "lumen deferens" — '
        "the means of its revelation. This is the gospel: 2 Corinthians 3:18.</p>"
        '<p class="list-item"><strong>3.</strong> "Lumen praeparans, elevans, disponens subjectum" — '
        '"the internal light of the mind. This is by the Holy Spirit: 2 Corinthians 4:6.</p>'
        '<p class="list-item"><strong>1.</strong> The glory of God is then expounded.</p>'
    )
    result = _attach_em_dash_flat_list(source)
    assert result.count('class="syllabus-anchor"') == 1
    assert result.count('<p class="list-item">') == 1
    assert '<strong>1.</strong> The glory of God is then expounded.' in result


def test_scholastic_continuation_pair_merges_after_semicolon_despite_length_caps():
    source = (
        '<p class="list-item"><strong>(1.)</strong> As it was triumphant, as he was a King;</p>\n'
        '<p class="list-item"><strong>(2.)</strong> As it was gracious, as he was a Priest.</p>'
    )
    result = _merge_short_inline_lists(source)
    assert result.count('<p class="list-item">') == 1
    assert '<strong>(1.)</strong> As it was triumphant, as he was a King; <strong>(2.)</strong> As it was gracious, as he was a Priest.' in result


def test_scholastic_continuation_pair_repeats_only_when_new_ending_is_open():
    source = (
        '<p class="list-item"><strong>(1.)</strong> The first branch continues;</p>\n'
        '<p class="list-item"><strong>(2.)</strong> the second branch also continues,</p>\n'
        '<p class="list-item"><strong>(3.)</strong> the third branch closes.</p>\n'
        '<p class="list-item"><strong>(4.)</strong> A fresh exposition remains block.</p>'
    )
    result = _merge_short_inline_lists(source)
    assert result.count('<p class="list-item">') == 2
    assert '<strong>(3.)</strong> the third branch closes.</p>' in result
    assert '<p class="list-item"><strong>(4.)</strong> A fresh exposition remains block.</p>' in result


def test_last_meaningful_visible_char_ignores_noteref_and_closing_marks():
    html = 'as he was a King;<a class="noteref" href="endnotes.xhtml#n1">1</a>”]'
    assert last_meaningful_visible_char(html) == ';'


def test_v1_ch023_ascension_continuation_merges_open_points_pairwise():
    source = (
        '<p class="list-item"><strong>(1.)</strong> In his ascension, as it was triumphant, three things may be considered:</p>\n'
        '<p class="list-item"><strong>1st</strong>, The manner of it, With its representation of old;</p>\n'
        '<p class="list-item"><strong>2ndly</strong>, The place whereinto he ascended;</p>\n'
        '<p class="list-item"><strong>3rdly</strong>, The end of it, or what was the work which he had to do thereon.</p>\n'
        '<p class="list-item"><strong>[1.]</strong> As unto the manner of it, it was openly triumphant and glorious.</p>'
    )
    result = _merge_short_inline_lists(source)
    assert result.count('<p class="list-item">') == 3
    assert '<strong>1st</strong>, The manner of it, With its representation of old; <strong>2ndly</strong>, The place whereinto he ascended; <strong>3rdly</strong>, The end of it' in result
    assert '<p class="list-item"><strong>[1.]</strong> As unto the manner of it' in result


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
