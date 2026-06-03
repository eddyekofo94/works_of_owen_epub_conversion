import json
import os
import re
import zipfile
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.audit_epub import Audit
from scripts.audit_text_integrity import Paragraph, paragraph_integrity, run_audit
from converter import clean_text, force_polyglot_mapping, get_pages_text, reconstruct_paragraphs
from render import (
    apply_scholastic_anchor_protocol,
    markdown_to_html,
    tag_unicode_ranges,
    _polish_contents_page_html,
    _merge_reference_continuation_paragraphs,
    _repair_analysis_spillover_chapters,
    _merge_short_inline_lists,
    _attach_colon_introduced_list,
    _detect_signature,
    _coalesce_adjacent_signatures,
    _repair_transitional_word_isolation,
    _foreign_fragments_in_section,
    _merge_titlepage_override,
)
from shared import (
    EPUB_STYLESHEET,
    EPUB3_FONT_STYLES,
    FONT_FAMILY_MAP,
    PROXIMA_NOVA_FILES,
    TITLE_PAGE_FONTS,
    GFS_PORSON_FILES,
    _get_font_name_records,
    generate_font_styles,
    select_primary_font,
    _repair_owen_ocr_errors,
)
from volumes.v1.convert import OVERRIDES as V1_OVERRIDES


BASE_DIR = Path(__file__).parent.parent
BASELINE_PATH = BASE_DIR / "qa" / "bug_regression_baselines.json"

# True only when the fonts symlink resolves to a real directory with files.
# In the sandbox the symlink target lives outside the mounted volume, so this
# will be False and any test that requires embedded font assets will be skipped.
_fonts_dir = BASE_DIR / "fonts"
try:
    FONTS_AVAILABLE = _fonts_dir.is_dir() and any(_fonts_dir.iterdir())
except (OSError, PermissionError):
    FONTS_AVAILABLE = False


def deep_merge(base, override):
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_baselines():
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def requested_volumes():
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "1").strip()
    if raw.lower() == "all":
        return [
            int(path.name[1:])
            for path in sorted((BASE_DIR / "volumes").glob("v[0-9]*"))
            if (path / "output" / f"volume_{path.name[1:]}.epub").exists()
        ]
    return [int(part) for part in raw.replace(",", " ").split() if part]


def budget_for(volume):
    data = load_baselines()
    default = data["default"]
    override = data.get("volumes", {}).get(str(volume), {})
    return deep_merge(default, override)


def paths_for(volume):
    volume_dir = BASE_DIR / "volumes" / f"v{volume}"
    return (
        volume_dir / "input" / f"owen-v{volume}.pdf",
        volume_dir / "output" / f"volume_{volume}.epub",
    )


def test_primary_font_selection_uses_real_internal_family_names():
    cases = {
        "adobe-garamond-pro-2-2": "Adobe Garamond Pro",
        "libertinus": "Libertinus Serif",
        "minion-pro": "Minion Pro",
        "brill-font": "Brill",
        "gentium-plus-2": "Gentium Plus",
        "sabon-next-lt": "Sabon Next LT",
        "baskerville": "Baskervville",
    }
    for directory, expected_family in cases.items():
        selected = select_primary_font(directory)
        assert selected["name"] == expected_family
        if directory == "sabon-next-lt" and not selected["files"]:
            # Sabon is a commercial font and may be absent from the environment
            continue
        assert selected["files"], f"{directory} should select at least one font file"
        css = generate_font_styles(selected["name"], selected["files"])
        assert f'font-family: "{expected_family}"' in css
        assert 'font-family: "Proxima Nova"' in css
        assert "Proxima Nova Rg" not in css


def test_mixed_font_directories_filter_to_body_family_faces():
    libertinus = select_primary_font("libertinus")
    # Support both .otf (original format) and .ttf (Google Fonts format)
    assert {os.path.splitext(f)[0] for f in libertinus["files"]} == {
        "LibertinusSerif-Regular",
        "LibertinusSerif-Bold",
        "LibertinusSerif-Italic",
        "LibertinusSerif-BoldItalic",
    }

    minion = select_primary_font("minion-pro")
    assert set(minion["files"]) == {
        "MinionPro-Regular.otf",
        "MinionPro-Bold.otf",
        "MinionPro-It.otf",
        "MinionPro-BoldIt.otf",
    }


def test_font_assets_exist_and_otf_metadata_is_readable():
    font_root = BASE_DIR / "fonts"
    for _name, rel_path in {**PROXIMA_NOVA_FILES, **TITLE_PAGE_FONTS, **GFS_PORSON_FILES}.items():
        if "proxima-nova" in rel_path and not (font_root / rel_path).exists():
            # Skip commercial Proxima Nova if not in environment
            continue
        assert (font_root / rel_path).exists(), rel_path

    adobe = font_root / "adobe-garamond-pro-2-2" / "AGaramondPro-Bold.otf"
    if adobe.exists():
        records = _get_font_name_records(adobe)
        assert records["family"] == "Adobe Garamond Pro Bold"
        assert records["preferred_family"] == FONT_FAMILY_MAP["adobe-garamond-pro-2-2"]


@lru_cache(maxsize=None)
def volume_intermediate(volume):
    path = BASE_DIR / "volumes" / f"v{volume}" / "intermediate" / f"volume_{volume}.json"
    if not path.exists():
        pytest.skip(f"Intermediate JSON for volume {volume} not found at {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def chapter_matching(volume, pattern):
    regex = re.compile(pattern, re.I)
    for chapter in volume_intermediate(volume)["chapters"]:
        if regex.search(chapter["title"]):
            return chapter
    pytest.fail(f"No chapter title matched {pattern!r} in volume {volume}")


@lru_cache(maxsize=None)
def epub_audit_result(volume):
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")
    return Audit(epub_path).run()


@lru_cache(maxsize=None)
def text_integrity_result(volume):
    pdf_path, epub_path = paths_for(volume)
    if not pdf_path.exists():
        pytest.skip(f"PDF for volume {volume} not found at {pdf_path}")
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")
    return run_audit(volume, pdf_path, epub_path)


@lru_cache(maxsize=None)
def epub_xhtml_text(volume):
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")
    with zipfile.ZipFile(epub_path) as zf:
        return "\n".join(
            zf.read(name).decode("utf-8")
            for name in sorted(zf.namelist())
            if name.startswith("EPUB/ch") and name.endswith(".xhtml")
        )


VOLUMES = requested_volumes()


def test_polyglot_fallback_does_not_convert_english_prose():
    text = (
        "The author's design concerns justification, Jesus Christ, John 3:36, "
        "grace; Christ; us; vol. 1, and [1.] markers, including [characters] and [from]."
    )

    mapped = force_polyglot_mapping(text)

    assert mapped == text


def test_polyglot_fallback_converts_unambiguous_residue_only():
    # pneu=ma uses a genuine Beta Code accent character (=) so BETA_CODE_RE matches it.
    # pneu'ma (plain apostrophe, no accent) is intentionally NOT converted — it is
    # ambiguous with English transliterations and the "does not convert prose" test
    # covers that boundary.  ytb;h}aæB] is a real Gideon-encoded Hebrew string.
    mapped = force_polyglot_mapping("pneu=ma ytb;h}aæB]")

    assert 'lang="el"' in mapped
    assert 'lang="he"' in mapped
    assert "pneu=ma" not in mapped
    assert "ytb;h}aæB]" not in mapped


def test_empty_scripture_code_brackets_are_removed():
    cleaned = clean_text("sealed unto the day of redemption. — [<490430>] Ephesians 4:30.")

    assert "[]" not in cleaned
    assert "Ephesians 4:30" in cleaned


def test_fused_footnote_marker_before_word_is_isolated():
    cleaned = clean_text("In three things; — first, in causing f53and things to work together.")

    assert "causing [f53] and things" in cleaned
    assert "f53and" not in cleaned


def test_false_himself_footnote_overlap_becomes_second_list_item():
    paragraphs = reconstruct_paragraphs(
        clean_text(
            "Now, the things may be referred to these two heads: —\n\n"
            "1. Himsel[f2]. His kingdom.\n\n"
            "1. Himself.\n\n"
            "2. His kingdom."
        )
    )

    joined = "\n".join(paragraphs)
    assert "1. Himself" in joined
    assert "2. His kingdom" in joined
    assert "[f2]" not in joined
    assert "Himsel[" not in joined


def test_ages_song_of_solomon_marker_does_not_keep_stale_proverbs_book():
    cleaned = clean_text(
        "opened, Proverbs 4:16<220416>; also Proverbs 2:1<220201>-7. "
        "His description, Proverbs 5:1Song of Solomon 5, opened."
    )

    assert "Song of Solomon 4:16" in cleaned
    assert "Song of Solomon 2:1-7" in cleaned
    assert "Song of Solomon 5, opened" in cleaned
    assert "Proverbs 4:16Song of Solomon" not in cleaned
    assert "Proverbs 2:1Song of Solomon" not in cleaned
    assert "Proverbs 5:1Song of Solomon" not in cleaned


def test_residual_square_ages_codes_are_removed_before_scripture_refs():
    cleaned = clean_text(
        'And chap. [4611605]16:5-15, chap. [810119]1:19-21, '
        'and [19B9105]Psalm 119:105, and is said.'
    )

    assert "[4611605]" not in cleaned
    assert "[810119]" not in cleaned
    assert "[19B9105]" not in cleaned
    assert "chap. 16:5-15" in cleaned
    assert "chap. 1:19-21" in cleaned
    assert "Psalm 119:105" in cleaned


def test_spaced_ordinal_markers_are_normalized_before_formatting():
    cleaned = clean_text("1 st . Such as consist in grace. 2 dly . Such as flow from revelation.")

    assert "1st." in cleaned
    assert "2dly." in cleaned
    assert "1 st ." not in cleaned
    assert "2 dly ." not in cleaned


def test_markdown_fragmented_ordinal_markers_are_normalized():
    cleaned = clean_text(
        "**[1** _**st**_ **.]** That we endeavor diligently. "
        "**[2** _**dly.**_ **]** That we live and abound."
    )

    assert "**[1st.]** That we endeavor" in cleaned
    assert "**[2dly.]** That we live" in cleaned
    assert "_**st**_" not in cleaned
    assert "_**dly.**_" not in cleaned


def test_bracketed_word_ordinal_marker_splits_to_new_paragraph():
    html, _, _ = markdown_to_html(
        'This impotency is to be cured in our return. [SECONDLY], '
        'The minds of men unregenerate being thus depraved and corrupted.'
    )

    assert '[SECONDLY]' in html
    assert '<b>[SECONDLY],</b>' in html
    assert re.search(r'</p>\s*(?:<div[^>]*>\s*)*<p class="list-item list-level-3"><b>\[SECONDLY\],</b>', html)


def test_inline_bold_decimal_markers_split_after_emphasized_semicolon():
    # Items 1 and 2 end with ';' inside <i> tags — plain text ends with ';'
    # so the new semicolon-based rule merges all 3 into one continuous paragraph.
    html, _, _ = markdown_to_html(
        '**1.** Of _sanctifying grace;_ **2.** Of _especial gifts;_ '
        '**3.** Of peculiar _evangelical privileges._'
    )

    assert html.count('class="list-item ') == 1, (
        "Items ending with ';' must be merged into one continuous paragraph"
    )
    assert '<b>1.</b> Of <i>sanctifying grace;</i>' in html
    assert '<b>2.</b> Of <i>especial gifts;</i>' in html
    assert '<b>3.</b> Of peculiar <i>evangelical privileges.</i>' in html


def test_chapter_summary_continuations_stop_at_body_opener():
    html, _, _ = markdown_to_html(
        '[[CHAPTER]] CHAPTER 1.\n\n'
        '[[SUMMARY]] GENERAL PRINCIPLES CONCERNING THE HOLY SPIRIT AND HIS WORK. '
        '1 Corinthians 12:1 opened — Dispensation of the Spirit not confined to the first ages of the church\n\n'
        '— The great necessity of a diligent inquiry into the things taught concerning the Spirit of God and his work.\n\n'
        'THE apostle Paul, in the 12th chapter, proceeds with his argument.'
    )

    assert 'The great necessity' in re.search(r'<p class="chapter-summary">(.*?)</p>', html, re.S).group(1)
    assert re.search(r'<p>THE apostle Paul', html)


def test_secondly_the_opener_is_not_swallowed_by_summary():
    html, _, _ = markdown_to_html(
        '[[CHAPTER]] CHAPTER 4.\n\n'
        '[[SUMMARY]] WORK OF THE HOLY SPIRIT IN AND ON THE HUMAN NATURE OF CHRIST. '
        'What it is to love Christ as we ought.\n\n'
        'Secondly, THE human nature of Christ being thus formed in the womb by a creating act of the Holy Spirit.'
    )

    summary = re.search(r'<p class="chapter-summary">(.*?)</p>', html, re.S).group(1)
    assert "Secondly" not in summary
    assert re.search(r'<p class="list-item list-level-1"><b>Secondly,</b> THE human nature', html)


def test_greek_synopsis_line_continues_chapter_summary():
    html, _, _ = markdown_to_html(
        '[[CHAPTER]] CHAPTER 9.\n\n'
        '[[SUMMARY]] CORRUPTION OR DEPRAVATION OF THE MIND BY SIN. 1 Corinthians 2:14 opened —\n\n'
        'Υυχικὸς ἄνθρωπος, or the "natural man," who — Spiritual things, what they are — Power of darkness declared.\n\n'
        'WE have considered the state of the mind.'
    )

    summary = re.search(r'<p class="chapter-summary">(.*?)</p>', html, re.S).group(1)
    assert 'Υυχικὸς' in summary
    assert re.search(r'<p>WE have considered', html)


def test_analysis_spillover_is_moved_back_to_previous_chapter():
    intermediate = {
        "chapters": [
            {"title": "Prefatory Note", "raw_text": 'of the Holy Spirit," etc., attempted "a'},
            {
                "title": "Analysis",
                "raw_text": (
                    'confutation of some part of Dr. Owen\'s work on that subject." '
                    'Mr. John Humfrey added more context.\n\nANALYSIS.\n\nPart I. The first thing.'
                ),
            },
        ]
    }

    repaired = _repair_analysis_spillover_chapters(intermediate)
    assert 'attempted "a confutation of some part' in repaired["chapters"][0]["raw_text"]
    assert repaired["chapters"][1]["raw_text"].startswith("[[SUBTITLE]] ANALYSIS.")


def test_chap_reference_continuation_paragraphs_are_merged():
    merged = _merge_reference_continuation_paragraphs([
        'And chap.',
        '16:5-15, "Now I go my way."',
        'This is another paragraph.',
        'that grace abound, chapter',
        '9:8; that "without Christ we can do nothing."',
    ])

    assert merged[0] == 'And chap. 16:5-15, "Now I go my way."'
    assert merged[1] == 'This is another paragraph.'
    assert merged[2].startswith('that grace abound, chapter 9:8;')


def test_hebrew_inside_greek_span_is_retagged_separately():
    tagged = tag_unicode_ranges("Φανέρωσις τοῦ Πνεύματος נלינא דרוחה Syr.")

    assert '<span lang="he" xml:lang="he" dir="rtl">נלינא דרוחה</span>' in tagged
    greek_spans = re.findall(r'<span lang="el" xml:lang="el">(.*?)</span>', tagged)
    assert greek_spans
    assert all(not re.search(r'[\u0590-\u05FF]', span) for span in greek_spans)


def test_footnote_merge_translates_ages_verse_markers():
    from extract import merge_footnotes

    footnotes = merge_footnotes(
        {},
        {5: "<460408>1 Corinthians 4:8-13; <450835>Romans 8:35,36."},
    )

    assert "1 Corinthians 4:8" in footnotes[5].text
    assert "Romans 8:35" in footnotes[5].text
    assert "<460408>" not in footnotes[5].text


def test_i_will_and_i_am_are_not_forced_to_all_caps():
    cleaned = clean_text("If he open the door, I WILL come in; for I AM ready. 'I a will arise;'")

    assert "I will come in" in cleaned
    assert "I am ready" in cleaned
    assert "I will arise" in cleaned
    assert "I WILL come in" not in cleaned
    assert "I AM ready" not in cleaned
    assert "I a will" not in cleaned


def test_parenthesized_scripture_refs_do_not_keep_opening_space():
    cleaned = clean_text('the dead hear his voice and live." ( Matthew 3:17; John 5:25.) ** Strong text')

    assert "(Matthew 3:17; John 5:25.)" in cleaned
    assert "( Matthew" not in cleaned
    assert "** Strong text" in cleaned


def test_ordinal_spacing_handles_bold_and_adverbial_forms():
    cleaned = clean_text("**1st** . Resolution.\n\n2ndly . Diligence.\n\n**3rdly** , Another.")

    assert "**1st**. Resolution" in cleaned
    assert "2ndly. Diligence" in cleaned
    assert "**3rdly**," in cleaned


def test_reference_and_scripture_false_breaks_are_healed():
    raw = (
        "He considers what is the state of the world in reference to them.\n\n"
        "Zechariah 1:11, \"We have walked to and fro.\"\n\n"
        "which he treats of, p.\n\n"
        "280. \"As for example,\" saith he.\n\n"
        "obedience, p. 181,' sec.\n\n"
        "14. And it is strange.\n\n"
        '"Morte tua vivens?" — Aen.\n\n'
        "10. 846.\n\n"
        "Liv., Hist. viii.\n\n"
        "9. His son,"
    )

    joined = "\n".join(reconstruct_paragraphs(clean_text(raw)))
    assert "them. Zechariah 1:11" in joined
    assert 'p. 280. "As for example' in joined
    assert "sec. 14. And it is strange" in joined
    assert "Aen. 10. 846." in joined
    assert "Liv., Hist. viii. 9. His son" in joined


def test_same_page_treatise_title_keeps_only_title_section():
    from extract import _keep_only_prerendered_treatise_title_page

    raw = (
        '<section class="treatise-title-page" epub:type="titlepage">'
        '<p class="title-line -major">PART 2</p></section> '
        'CHAPTER 1\n\nThis belongs to the next chapter.'
    )

    trimmed = _keep_only_prerendered_treatise_title_page(raw)
    assert trimmed == (
        '<section class="treatise-title-page" epub:type="titlepage">'
        '<p class="title-line -major">PART 2</p></section>'
    )
    assert "CHAPTER 1" not in trimmed
    assert "This belongs to the next chapter" not in trimmed


def test_summary_continuation_is_rendered_as_one_summary_paragraph():
    html, _, _ = markdown_to_html(
        "[[CHAPTER]] CHAPTER 5\n\n"
        "[[SUMMARY]] Other consequential affections: — 1 On the part of Christ — "
        "He values his saints — Evidences of that valuation: —\n\n"
        "**(1.)** His incarnation; **(2.)** Exinanition, 2 Corinthians 8:9;\n\n"
        "**(3.)** Obedience as a servant;\n\n"
        "2. Believers' estimation of Christ: —\n\n"
        "**(1.)** They value him above all other things and persons;\n\n"
        "II. Christ values his saints, values believers "
        "(which is the second branch of that conjugal affection he bears towards them)."
    )

    summary_paragraphs = re.findall(r'<p class="chapter-summary">.*?</p>', html, re.S)
    assert len(summary_paragraphs) == 1
    summary = summary_paragraphs[0]
    assert "(1.) His incarnation;" in summary
    assert "(2.) Exinanition, 2 Corinthians 8:9;" in summary
    assert "2. Believers&#x27; estimation of Christ: —" in summary
    assert "</p> <p" not in summary
    assert '<h4 class="roman-subheading"><b>II.</b></h4>' in html
    assert 'Christ values his saints' in html


def test_bracketed_and_parenthesized_markers_split_and_bold_cleanly():
    # (1.) ends with ';' → merges with (2.) which ends with '—' (terminator)
    # → (1.)+(2.) become one paragraph.
    # [1]. ends with ';' → merges with [2.] which ends with '—' (terminator)
    # → [1].+[2.] become one paragraph.
    html, _, _ = markdown_to_html(
        "**(1.)** For their sanctification;\n\n"
        "**(2.)** For their consolation: to which two all the particular acts of "
        "purging, teaching, anointing, and the rest that are ascribed to him, may "
        "be referred. So there be two ways whereby we may grieve him: — "
        "**[1].** In respect of sanctification;\n\n"
        "**[2.]** In respect of consolation: —"
    )

    # (1.) and (2.) merge — (1.) ends with ';'
    assert '<b>(1.)</b> For their sanctification;' in html
    assert '<b>(2.)</b> For their consolation:' in html
    assert html.count('class="list-item ') == 2, (
        "Expected (1.)+(2.) to merge and [1].+[2.] to merge → 2 paragraphs total"
    )
    assert '<p class="list-item list-level-2"><b>(1.)</b>' in html
    assert '<p class="list-item list-level-3"><b>[1].</b>' in html
    assert '(2.)<b> For their consolation' not in html


def test_quote_wrapped_structural_markers_are_unwrapped_and_bolded():
    html, _, _ = markdown_to_html(
        '"2dly. Our holiness, our obedience, work of righteousness, is one end.\n\n'
        'Particularly, — " [1st.] It is the glory of the Father. And, — " [2dly.] '
        'The Son is gloried thereby.'
    )

    assert '"2dly' not in html
    assert '" [1st' not in html
    assert '" [2dly' not in html
    assert '<p class="list-item list-level-3"><b>2dly.</b> Our holiness' in html
    assert '<b>[1st.]</b> It is the glory of the Father' in html
    assert '<b>[2dly.]</b> The Son is gloried thereby' in html


def test_sermon_fragmented_ordinal_marker_is_normalized():
    cleaned = _repair_owen_ocr_errors(
        '**[** _**3dly**_ **.]** Whereas in these dispensations it is most eminently said.'
    )
    html, _, _ = markdown_to_html(cleaned)

    assert '**[**' not in cleaned
    assert '**[3dly.]**' in cleaned
    assert '<p class="list-item list-level-3"><b>[3dly.]</b> Whereas in these dispensations' in html
    assert '[ <i>3dly</i> .]' not in html


def test_sermon_prefatory_dates_are_not_inline_structural_markers():
    result = paragraph_integrity([
        Paragraph(
            file='EPUB/ch025.xhtml',
            tag='p',
            index=1,
            classes='front-matter-prose',
            html=(
                '<p class="front-matter-prose">ALL the information which can be given respecting '
                'these sermons on Isaiah 56:7, will be found in the "Life," vol. i. p. 45, '
                'and the dedication to Cromwell which is prefixed to them. The first sermon '
                'was preached at Berwick, July 21, 1650. The date of the dedication is '
                'November 26, 1650.</p>'
            ),
            text=(
                'ALL the information which can be given respecting these sermons on Isaiah 56:7, '
                'will be found in the "Life," vol. i. p. 45, and the dedication to Cromwell '
                'which is prefixed to them. The first sermon was preached at Berwick, '
                'July 21, 1650. The date of the dedication is November 26, 1650.'
            ),
        )
    ])

    assert result['inline_structural_candidate_count'] == 0


def test_sermon_prefatory_note_scripture_split_is_healed():
    html, _, _ = markdown_to_html(
        'THIS sermon, from\n\n'
        '[[SUMMARY]] Hebrews 12:27, was preached before Parliament on a\n\n'
        'day set apart for extraordinary humiliation.'
    )

    assert '<h3 class="secondary">Hebrews 12:27' not in html
    assert (
        '<p>THIS sermon, from Hebrews 12:27, was preached before '
        'Parliament on a day set apart for extraordinary humiliation.</p>'
    ) in html


def test_scholastic_quoted_objection_opener_moves_inside_blockquote():
    html, _, _ = markdown_to_html(
        'Objection 1. But some may say, "Alas! how shall I hold communion with '
        'the Father in love? I know not at all whether he loves me or no;\n\n'
        '[[BLOCKQUOTE]] and shall I venture to cast myself upon it? How if I '
        'should not be accepted?"'
    )

    assert '<p class="list-item list-level-1"><b>Objection 1.</b> But some may say,</p>' in html
    assert (
        '<blockquote epub:type="z3998:quotation"><p class="blockquote-content">&quot;Alas! how shall I hold '
        'communion with the Father in love? I know not at all whether he loves '
        'me or no; and shall I venture to cast myself upon it? How if I should '
        'not be accepted?&quot;</p></blockquote>'
    ) in html
    assert 'But some may say, &quot;Alas!' not in html


def test_open_parenthesis_scripture_reference_is_closed_before_following_prose():
    cleaned = clean_text(
        '(2.) He sends them his Holy Spirit, to quicken them, '
        '(John 6:63, to cause them that are dead to hear his voice.'
    )

    assert '(John 6:63), to cause them' in cleaned
    assert '(John 6:63, to cause' not in cleaned


def test_duplicated_chapter_reference_noise_is_collapsed():
    cleaned = clean_text(
        'pronounces those censures, Romans 1:1 1; '
        '1 Corinthians 1:11 Corinthians 1.'
    )

    assert 'pronounces those censures, Romans 1; 1 Corinthians 1.' in cleaned
    assert 'Romans 1:1 1' not in cleaned
    assert '1 Corinthians 1:11 Corinthians 1' not in cleaned


def test_contents_pages_split_parts_and_chapters_with_clean_labels():
    html = _polish_contents_page_html(
        '<section epub:type="toc">'
        '<h2>CONTENTS OF VOL. 2.</h2>'
        '<h2>NOTE TO THE READER BY D. BURGESS</h2>'
        '<p class="contents-item">Part 2.</p>'
        '<p class="contents-item"><b>Chapter 1</b> . First chapter. Chapter 2 . Second chapter, from</p>'
        '<p class="contents-item">the grace of union — continuation. Digression 1. A useful aside.</p>'
        '<p class="contents-item">A VINDICATION OF SOME PASSAGES IN A DISCOURSE</p>'
        '</section>'
    )

    assert '<h1 class="contents-volume-title">CONTENTS OF VOL. 2.</h1>' in html
    assert '<p class="contents-frontmatter-line">NOTE TO THE READER BY D. BURGESS</p>' in html
    assert '<h2 class="contents-part-title">Part 2.</h2>' in html
    assert '<span class="contents-label">Chapter 1.</span> First chapter.' in html
    assert '<span class="contents-label">Chapter 2.</span> Second chapter, from the grace of union' in html
    assert '<span class="contents-label">Digression 1.</span> A useful aside.' in html
    assert '<h2 class="contents-treatise-title">A VINDICATION OF SOME PASSAGES IN A DISCOURSE</h2>' in html
    assert 'Chapter 1</b> .' not in html
    assert 'Chapter 2 .' not in html
    assert 'class="ContentsItem"' not in html


def test_issue_29_scholarly_citation_breaks_are_healed():
    raw = """Augustine gives an account of the same difference: De Trinitate, lib. 5 cap. , 8,
9. Athanasius endeavored the composing of this difference.

See Aquin. 22 q. , 81,
a. 3, ad prim. , and
q. , 84,
a. 1, ad tertium; Alexand. Alens. p. 3,
q. 30,
m. 1,
a. 3.
But yet, although we may call on God in and by the name of any divine person.

Chapter,
8. Then follows the next matter."""

    paragraphs = reconstruct_paragraphs(clean_text(raw))
    joined = "\n".join(paragraphs)

    assert "De Trinitate, lib. 5 cap. 8, 9. Athanasius" in joined
    assert "See Aquin. 22 q. 81, a. 3, ad prim. , and q. 84, a. 1, ad tertium; Alexand. Alens. p. 3, q. 30, m. 1, a. 3. But yet" in joined
    assert "Chapter 8. Then follows" in joined
    assert "cap. ," not in joined
    assert "q. ," not in joined
    assert "q.," not in joined
    assert "cap.," not in joined
    assert not re.search(r'De Trinitate, lib\. 5 cap\. 8,\s*\n\s*9\.', joined)


def test_issues_37_to_40_textual_todo_regressions_are_guarded():
    if 1 not in VOLUMES:
        pytest.skip("Issues 37-40 samples are volume 1-specific")
    html = epub_xhtml_text(1)

    assert "anything he has done ill. For what he so does" in html
    assert '<b>ill.</b> For what he so does' not in html
    assert (
        '<blockquote epub:type="z3998:quotation"><p class="blockquote-content">"Behold my servant, whom I uphold; '
        'mine elect, in whom my soul delighteth;" (Isaiah 42:1;)</p></blockquote>'
    ) in html
    assert "</blockquote>\n<p>as he also proclaims the same delight" in html
    assert "open the door, I WILL come in to him, and will sup with him" not in html
    assert "open the door, I will come in to him, and will sup with him" in html
    assert "I. 1. What he did, what obedience he yielded" in re.sub(r"</?b>", "", html)
    assert 'enter into his glory?" Luke 24:26. The one is frequently expressed elsewhere' in html


def test_issue_39_combined_roman_decimal_marker_stays_inline():
    html, _, _ = markdown_to_html(
        "I. 1. What he did preparatory unto his death, which was the first thing proposed unto consideration."
    )

    assert '<p class="list-item list-level-1"><b>I. 1.</b> What he did preparatory' in html


def test_issue_32_pdf_page_384_reference_run_is_not_jumbled():
    fitz = pytest.importorskip("fitz")
    pymupdf4llm = pytest.importorskip("pymupdf4llm")
    pdf_path, _ = paths_for(1)
    if not pdf_path.exists():
        pytest.skip(f"PDF for volume 1 not found at {pdf_path}")

    with fitz.open(pdf_path) as doc:
        page_md = pymupdf4llm.to_markdown(
            str(pdf_path),
            pages=[383],
            page_chunks=True,
            show_progress=False,
        )[0]
        pages_md = [None] * 384
        pages_md[383] = page_md
        text = get_pages_text(doc, pages_md, 383, 383, config=V1_OVERRIDES)
    expected = (
        'The church then knew him; yet so as that they had an apprehension that '
        'he dwelt in "thick darkness," where they could not have any clear views '
        'of him, Exodus 21; Deuteronomy 5:22; 1 Kings 8:12; 2 Chronicles 6:1. '
        'And the reason why God so represented himself in darkness unto them'
    )

    assert expected in text
    assert '4. Hitherto darkness in general covered the earth' in text
    assert '1 Kings 8:121Kings' not in text
    assert '1 Kings, 8:12' not in text
    assert '2 Chronicles 6:12 Chronicles' not in text
    assert '2 Chronicles him, Exodus' not in text
    assert 'Kings, 8:12; 4. Hitherto' not in text


def test_issue_34_numbered_answer_anchor_is_normalized_and_bolded():
    cleaned = clean_text("Ans . 1. There is no precedent nor example")
    html = apply_scholastic_anchor_protocol(f"<p>{cleaned}</p>")

    assert cleaned == "Ans. 1. There is no precedent nor example"
    assert '<b class="scholastic-label">Ans. 1.</b> There is no precedent nor example' in html


def test_spaced_scholastic_labels_are_repaired_globally():
    repaired = _repair_owen_ocr_errors(
        "Objection . But some may say.\n\nAns . 1. There is no precedent.\n\nQ . What is required?"
    )

    assert "Objection. But some may say." in repaired
    assert "Ans. 1. There is no precedent." in repaired
    assert "Q. What is required?" in repaired
    assert "Objection ." not in repaired
    assert "Ans ." not in repaired
    assert "Q ." not in repaired


def test_objection_and_use_labels_are_bolded_as_scholastic_anchors():
    html = apply_scholastic_anchor_protocol(
        "<p>Objection 1. But some may say, Alas!</p>\n"
        "<p>Use. 1. You that are yet in the flower of your days.</p>"
    )

    assert '<b class="scholastic-label">Objection 1.</b> But some may say' in html
    assert '<b class="scholastic-label">Use. 1.</b> You that are yet' in html


def test_question_followed_by_scripture_tail_stays_in_same_paragraph():
    paragraphs = reconstruct_paragraphs(
        clean_text(
            "What fruit of this consideration had Adam in the garden?\n\n"
            "Genesis 3. What sweetness, what encouragement, is there in knowing"
        )
    )

    joined = "\n".join(paragraphs)
    assert "garden? Genesis 3. What sweetness" in joined


@pytest.mark.parametrize("volume", VOLUMES)
def test_issue_33_shared_treatise_starter_pages_are_split_in_intermediate(volume):
    if volume != 1:
        pytest.skip("Issue 33 samples are volume 1-specific")

    part_2 = chapter_matching(volume, r"^Part 2 - Meditations and Discourses Concerning")
    part_2_raw = part_2["raw_text"]
    assert '<section class="treatise-title-page"' in part_2_raw
    assert "PART 2" in part_2_raw
    assert "MEDITATIONS AND DISCOURSES CONCERNING" in part_2_raw
    assert "CHAPTER 1" not in part_2_raw
    assert "That which remains" not in part_2_raw

    part_2_chapter = chapter_matching(
        volume,
        r"^Chapter 1 - Meditations and Discourses Concerning the Glory of Christ$",
    )
    chapter_raw = part_2_chapter["raw_text"]
    assert chapter_raw.startswith("[[CHAPTER]] CHAPTER 1")
    assert "[[PART]] PART 2" not in chapter_raw
    assert '<section class="treatise-title-page"' not in chapter_raw
    assert "That which remains is, to make some application" in chapter_raw

    greater = chapter_matching(volume, r"^The Greater Catechism$")
    greater_raw = greater["raw_text"]
    assert '<section class="treatise-title-page"' in greater_raw
    assert "THE GREATER CATECHISM" in greater_raw
    assert "CHAPTER 1" not in greater_raw
    assert "Ques. 1. What is Christian religion?" not in greater_raw
    assert "Ans. The only way" not in greater_raw

    greater_chapter = chapter_matching(volume, r"^Chapter 1 - of the Scripture\.$")
    greater_chapter_raw = greater_chapter["raw_text"]
    assert greater_chapter_raw.startswith("[[CHAPTER]] CHAPTER 1")
    assert "[[PART]] THE GREATER CATECHISM" not in greater_chapter_raw
    assert '<section class="treatise-title-page"' not in greater_chapter_raw
    assert "Ques. 1. What is Christian religion?" in greater_chapter_raw
    assert "Ans. The only way" in greater_chapter_raw


@pytest.mark.parametrize("volume", VOLUMES)
def test_v2_same_page_part_entries_do_not_duplicate_chapter_one(volume):
    if volume != 2:
        pytest.skip("V2 same-page Part/Chapter samples are volume 2-specific")

    part_1 = chapter_matching(volume, r"^Part 1\.$")
    assert '<section class="treatise-title-page"' in part_1["raw_text"]
    assert "PART 1" in part_1["raw_text"]
    assert "CHAPTER 1" not in part_1["raw_text"]
    assert "That the saints have communion with God" not in part_1["raw_text"]

    part_1_chapter = chapter_matching(volume, r"^Chapter 1\.$")
    assert part_1_chapter["raw_text"].startswith("[[CHAPTER]] CHAPTER 1")
    assert "That the saints have communion with God" in part_1_chapter["raw_text"]
    assert '<section class="treatise-title-page"' not in part_1_chapter["raw_text"]

    part_2 = chapter_matching(volume, r"^Part 2 - Of Communion With the Son Jesus Christ$")
    assert '<section class="treatise-title-page"' in part_2["raw_text"]
    assert "PART 2" in part_2["raw_text"]
    assert "CHAPTER 1" not in part_2["raw_text"]
    assert "Of the fellowship which the saints have with Jesus Christ" not in part_2["raw_text"]

    matching_chapters = [
        chapter for chapter in volume_intermediate(volume)["chapters"]
        if chapter["title"] == "Chapter 1"
        and "Of the fellowship which the saints have with Jesus Christ" in chapter["raw_text"]
    ]
    assert len(matching_chapters) == 1
    assert matching_chapters[0]["raw_text"].startswith("[[CHAPTER]] CHAPTER 1")
    assert '<section class="treatise-title-page"' not in matching_chapters[0]["raw_text"]


@pytest.mark.parametrize("volume", VOLUMES)
def test_issue_33_shared_treatise_starter_pages_are_not_title_styled_in_epub(volume):
    if volume != 1:
        pytest.skip("Issue 33 samples are volume 1-specific")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    files = {}
    css = ""
    nav = ""
    opf = ""
    with zipfile.ZipFile(epub_path) as zf:
        names = set(zf.namelist())
        for name in zf.namelist():
            if name.endswith("nav.xhtml"):
                nav = zf.read(name).decode("utf-8", "replace")
                continue
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", "replace")
            elif name.endswith("style/main.css"):
                css = zf.read(name).decode("utf-8", "replace")
            elif name.endswith("content.opf"):
                opf = zf.read(name).decode("utf-8", "replace")

    title_pages = [
        html for name, html in files.items()
        if name.rsplit("/", 1)[-1].startswith("title_")
    ]
    assert any("Edited by William H. Goold" in html for html in title_pages)
    assert any("Eduardus Ekofius" in html for html in title_pages)
    assert any("2026" in html or "MMXXVI" in html for html in title_pages)

    part_2_title = next(
        html for html in files.values()
        if "<title>Part 2 — Meditations and Discourses Concerning The Glory of Christ</title>" in html
    )
    assert 'class="treatise-title-page' in part_2_title
    assert '<section class="treatise-title-page v1-applied-glory-title"' in part_2_title
    assert "Unconverted Sinners" in part_2_title
    assert "Saints Under Spiritual Decays" in part_2_title
    assert "In Two Chapters, from John XVII. 24." in part_2_title
    assert "<p>\n        <section" not in part_2_title
    assert "CHAPTER 1" not in part_2_title
    assert "That which remains" not in part_2_title

    part_2_chapter = next(
        html for html in files.values()
        if "<title>Chapter 1 — Meditations and Discourses Concerning the Glory of Christ</title>" in html
    )
    assert '<section class="treatise-title-page"' not in part_2_chapter
    assert "Application of the Foregoing Meditations" in part_2_chapter
    assert "That which remains is, to make some application" in part_2_chapter

    greater_chapter = next(
        html for html in files.values()
        if "<title>Chapter 1 — of the Scripture.</title>" in html
    )
    assert '<section class="treatise-title-page"' not in greater_chapter
    assert 'class="catechism-item catechism-question"' in greater_chapter
    assert "<b>Ques. 1.</b> What is Christian religion?" in greater_chapter
    assert "<b>Ans.</b> The only way" in greater_chapter

    christologia_title = next(
        html for html in files.values()
        if "<title>Christologia — a Declaration of the Glorious Mystery</title>" in html
    )
    # Christologia title page is now hardcoded in v1/convert.py — correct classes and mixed case
    assert 'class="greek-title"' in christologia_title
    assert 'ΧΡΙΣΤΟΛΟΓΙΑ:' in christologia_title
    assert '<p class="title-line-major">Christologia</p>' in christologia_title
    assert '<p class="title-connector">Or,</p>' in christologia_title
    assert 'Declaration of the Glorious Mystery' in christologia_title
    assert 'The Person of Christ' in christologia_title
    assert 'Philippians 3:8' in christologia_title
    # No raw heading fallback artifacts
    assert "<h2>OR</h2>" not in christologia_title
    assert "<h2>OF</h2>" not in christologia_title
    assert "<h2>WITH</h2>" not in christologia_title

    first_title_page = next(html for name, html in files.items() if name.endswith("title_0.xhtml"))
    assert '<section class="title-page volume-title-page"' in first_title_page
    assert '<p class="title-work-top">The Works of</p>' in first_title_page
    assert '<h1 class="title-author-main">John Owen</h1>' in first_title_page
    assert '<p class="title-volume-number">Volume 1</p>' in first_title_page

    contents = next(html for name, html in files.items() if name.endswith("contents_2.xhtml"))
    assert '<section class="contents-page" epub:type="toc">' in contents
    assert '<h1 class="contents-volume-title">CONTENTS OF VOLUME 1.</h1>' in contents
    assert '<a href="ch042.xhtml">Original Preface</a>' in contents
    assert 'class="ContentsItem"' not in contents

    chapter_1 = next(html for html in files.values() if "<title>Chapter 1 — Peter's Confession</title>" in html)
    assert "Peter's Confession; Matthew 16:16" in chapter_1
    assert "PETER'S CONFESSION; MATTHEW 16:16" not in chapter_1

    greater_chapter_15 = next(
        html for html in files.values()
        if "<title>Chapter 15 — of the Persons to Whom the Benefits of Christ's Offices Do Belong.</title>" in html
    )
    assert "Of the Persons to Whom the Benefits of Christ's Offices Do Belong." in greater_chapter_15
    assert "OF THE PERSONS TO WHOM THE BENEFITS OF CHRIST'S OFFICES DO BELONG." not in greater_chapter_15

    assert "EPUB/ch078.xhtml" not in names
    assert ">Footnotes<" not in nav
    assert "href=\"ch078.xhtml\"" not in nav
    assert "href=\"ch078.xhtml\"" not in opf
    assert re.search(r"\.treatise-title-page\s*\{[^}]*min-height:\s*92vh;", css, re.S)
    assert re.search(r"\.treatise-title-page\s*\{[^}]*display:\s*flex;", css, re.S)
    assert 'font-family: "Owen Title"' in css
    assert re.search(r"\.front-matter-heading\s*\{[^}]*border-bottom:\s*1\.5px solid rgba\(42,\s*85,\s*160,\s*0\.22\);", css, re.S)
    assert ".contents-page" in css
    assert ".volume-title-page .title-author-main" in css
    if FONTS_AVAILABLE:
        assert "EPUB/Fonts/BaskervilleBT.ttf" in names
        assert "EPUB/Fonts/BaskervilleItalicBT.ttf" in names
    assert re.search(r"\.treatise-title-page \.title-connector\s*\{[^}]*font-size:\s*0\.68em;", css, re.S)


@pytest.mark.parametrize("volume", VOLUMES)
def test_v1_catechism_questions_and_answers_are_grouped_and_bolded(volume):
    if volume != 1:
        pytest.skip("Catechism visual polish is a Volume 1-specific override")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    files = {}
    css = ""
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", "replace")
            elif name.endswith("style/main.css"):
                css = zf.read(name).decode("utf-8", "replace")

    lesser = next(
        html for html in files.values()
        if "<title>The Lesser Catechism</title>" in html
    )
    greater_chapter_1 = next(
        html for html in files.values()
        if "<title>Chapter 1 — of the Scripture.</title>" in html
    )

    assert ".v1-catechism-pair" in css
    assert "front-matter-prose" not in lesser
    assert '<div class="v1-catechism-pair">\n<p class="catechism-item catechism-question"><b>Ques.</b> Whence is all truth' in lesser
    assert '<p class="catechism-item catechism-answer"><b>Ans.</b> From the holy Scripture' in lesser
    assert '<p class="catechism-item catechism-answer"><b>A.</b> An eternal, infinite' in lesser
    assert '<p class="catechism-item catechism-question"><b>Q. 2.</b> What is repentance?</p>' in lesser
    assert '<p class="catechism-item catechism-answer"><b>A.</b> A forsaking of all sin, with godly sorrow for what we have committed. — Chapter 20.</p>' in lesser
    assert '<p>- Chapter 20.</p>' not in lesser
    assert '<p>- Chapter 21.</p>' not in lesser
    assert "know.?" not in lesser

    assert '<div class="v1-catechism-pair">\n<p class="catechism-item catechism-question"><b>Ques. 1.</b> What is Christian religion?</p>' in greater_chapter_1
    assert '<p class="catechism-item catechism-answer"><b>A.</b> From the holy' in greater_chapter_1

    combined = "\n".join(files.values())
    # These sentences start with "A" in the prose.
    # They must be present as normal prose and NOT incorrectly parsed as catechism answers.
    false_answer_samples = [
        "A prefatory note has commonly been given to the different treatises.",
        "A complete index will be given in the last volume",
        "A glorious representation hereof",
    ]
    for sample in false_answer_samples:
        rest = sample[2:]  # strip "A " prefix to get the body text
        assert sample in combined
        assert f'<p class="catechism-item"><b>A.</b> {rest}' not in combined
        assert f'<p class="catechism-item">A. {rest}' not in combined


@pytest.mark.parametrize("volume", VOLUMES)
def test_blockquote_geometry_renders_quotes_without_promoting_body_wraps(volume):
    if volume != 1:
        pytest.skip("Blockquote geometry samples are volume 1-specific")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    files = {}
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", "replace")

    general_preface = next(
        html for html in files.values()
        if re.search(r"<title>General Preface\.?</title>", html)
    )
    peters_confession = next(
        html for html in files.values()
        if "<title>Chapter 1 — Peter's Confession</title>" in html
    )
    latin_quote_chapter = next(
        html for html in files.values()
        if "Universam significabat ecclesiam" in html
    )
    power_chapter = next(
        html for html in files.values()
        if "<title>Chapter 7 — Power and Efficacy Communicated Unto the Office of Christ</title>" in html
    )
    honor_chapter = next(
        html for html in files.values()
        if "<title>Chapter 9 — Honor Due to the Person of Christ</title>" in html
    )
    conformity_chapter = next(
        html for html in files.values()
        if "<title>Chapter 15 — Conformity Unto Christ</title>" in html
    )
    combined = "\n".join(files.values())

    assert '<blockquote epub:type="z3998:quotation"><p class="blockquote-content">"The divines of the Puritan school' in general_preface
    assert "Universam significabat ecclesiam" in latin_quote_chapter
    assert '<blockquote epub:type="z3998:quotation"><p class="blockquote-content">"And Simon Peter answered' in peters_confession
    quote_blocks = re.findall(r"<blockquote[^>]*>.*?</blockquote>", peters_confession, re.S)
    assert not any("Baronius" in block for block in quote_blocks)
    assert 'The faith of Peter in this confession' in peters_confession
    assert not any("1. The faith of Peter" in block for block in quote_blocks)
    assert re.search(r'<blockquote[^>]*><p[^>]*>"Thou, Lord,.*?a vesture shalt thou fold them up.*?not fail\."</p></blockquote>', power_chapter, re.S)
    assert re.search(r'<blockquote[^>]*><p[^>]*>"Unto him that loved us,.*?Amen\." Revelation 1:5, 6\.</p></blockquote>', honor_chapter, re.S)
    assert '<p>This, therefore, is another season that calls for this duty.</p>' in honor_chapter
    assert re.search(r'<blockquote[^>]*><p[^>]*>"If so be that we suffer with him,.*?Romans 8:17, 18\.</p></blockquote>', conformity_chapter, re.S)
    assert re.search(r"<blockquote[^>]*><p[^>]*/\s*>", combined) is None
    assert re.search(r"<blockquote[^>]*><p[^>]*>\s*</p>", combined) is None


@pytest.mark.parametrize("volume", VOLUMES)
def test_roman_markers_render_left_aligned_without_marker_escaping(volume):
    if volume != 1:
        pytest.skip("Roman heading samples are volume 1-specific")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    files = {}
    css = ""
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", "replace")
            elif name.endswith("style/main.css"):
                css = zf.read(name).decode("utf-8", "replace")

    roman_html = "\n".join(
        html for html in files.values()
        if "roman-subheading" in html or "roman-list-item" in html
    )
    assert "[[MARKER]]" not in roman_html
    assert "[[/MARKER]]" not in roman_html
    assert "&lt;b&gt;" not in roman_html
    assert "&lt;/b&gt;" not in roman_html
    assert re.search(r"\.roman-subheading\s*\{[^}]*text-align:\s*center;", css, re.S)
    assert re.search(r"\.roman-subheading\s*\{[^}]*font-weight:\s*normal;", css, re.S)
    assert re.search(r"\.roman-list-item\s*\{[^}]*text-align:\s*left;", css, re.S)
    assert re.search(r"\.roman-list-item b\s*\{[^}]*display:\s*inline;", css, re.S)

    chapter_9 = next(
        html for html in files.values()
        if "<title>Chapter 9 — Honor Due to the Person of Christ</title>" in html
    )
    assert '<p class="syllabus-anchor">' in chapter_9
    assert 'The respect which we have in all acts of religion unto the person of Christ may be reduced unto these four heads: <b>I.</b> Honor. <b>II.</b> Obedience. <b>III.</b> Conformity. <b>IV.</b> The use we make of him, for the attaining and receiving of all Gospel privileges — all grace and glory. And hereunto the whole of our religion, as it is Christian or evangelical, may be reduced.</p>' in chapter_9
    assert '<h4 class="roman-subheading"><b>I.</b> Honor.</h4>' not in chapter_9
    assert '<h4 class="roman-subheading"><b>I.</b></h4>' in chapter_9
    assert 'The person of Christ is the object of divine honor and worship.' in chapter_9

    chapter_7 = next(
        html for html in files.values()
        if "<title>Chapter 7 — Power and Efficacy Communicated Unto the Office of Christ</title>" in html
    )
    assert '<h4 class="roman-subheading"><b>I.</b></h4>' in chapter_7
    assert 'The first of these is, that he should have a nature provided for him,' in chapter_7


def test_list_item_announcer_syllabus_is_flattened():
    from render import markdown_to_html
    md = (
        "1. There are two things wherein the glory of truth does consist.\n\n"
        "(1.) Its light.\n\n"
        "(2.) Its efficacy or power. And both these do all supernatural truths derive from this relation unto Christ.\n\n"
        "(1.) No truth whatever brings any spiritual light unto the mind, but by virtue thereof."
    )
    html, _, _ = markdown_to_html(md)
    assert '<p class="list-item list-level-1 syllabus-anchor"><b>1.</b> There are two things wherein the glory of truth does consist. <b>(1.)</b> Its light. <b>(2.)</b> Its efficacy or power. And both these do all supernatural truths derive from this relation unto Christ.</p>' in html
    assert '<b>(1.)</b> No truth whatever' in html


@pytest.mark.parametrize("volume", VOLUMES)
def test_issue_29_scholarly_citation_splits_do_not_recur_in_epub(volume):
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    bad_patterns = [
        re.compile(r'\b(?:cap|chap|lib|q|a|m|p)\.,\s*\d'),
        re.compile(r'\b(?:cap|chap|lib|q|a|m|p)\.\s*,\s*\d'),
        re.compile(r'De Trinitate,\s*lib\.\s*5\s*cap\.\s*</p>\s*<p[^>]*>\s*(?:<b>)?9\.', re.I | re.S),
        re.compile(r'See Aquin\.\s*22\s*q\.\s*81,\s*</p>\s*<p[^>]*>\s*a\.\s*3', re.I | re.S),
        re.compile(r'\bChapter,?\s*</p>\s*<p[^>]*>\s*(?:<b>)?8\.', re.I | re.S),
    ]

    failures = []
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if not name.endswith(".xhtml"):
                continue
            html = zf.read(name).decode("utf-8", "replace")
            for pattern in bad_patterns:
                match = pattern.search(html)
                if match:
                    failures.append(f"{name}: {match.group(0)[:160]}")

    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("volume", VOLUMES)
def test_issue_32_page_384_reference_run_does_not_recur_in_epub(volume):
    if volume != 1:
        pytest.skip("Issue 32 page 384 sample is volume 1-specific")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    html_parts = []
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                html_parts.append(zf.read(name).decode("utf-8", "replace"))
    html = "\n".join(html_parts)
    plain = re.sub(r"<[^>]+>", " ", html)
    plain = re.sub(r"\s+", " ", plain)

    expected = (
        'The church then knew him; yet so as that they had an apprehension that '
        'he dwelt in "thick darkness," where they could not have any clear views '
        'of him, Exodus 21; Deuteronomy 5:22; 1 Kings 8:12; 2 Chronicles 6:1. '
        'And the reason why God so represented himself in darkness unto them'
    )
    bad_samples = [
        "1 Kings 8:121Kings",
        "1 Kings, 8:12",
        "2 Chronicles 6:12 Chronicles",
        "2 Chronicles him, Exodus",
        "Kings, 8:12; 4. Hitherto",
    ]

    assert expected in plain
    assert "4. Hitherto darkness in general covered the earth" in plain
    failures = [sample for sample in bad_samples if sample in plain]
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("volume", VOLUMES)
def test_known_text_integrity_bug_classes_do_not_regress(volume):
    result = text_integrity_result(volume)
    budget = budget_for(volume)["text_integrity"]
    paragraph = result["paragraph_integrity"]
    enumerators = result["enumerator_integrity"]
    front_toc = result["front_matter_toc_integrity"]

    warning_codes = {item["code"] for item in result["warnings"]}
    allowed_codes = set(budget["allowed_warning_codes"])
    assert warning_codes <= allowed_codes

    checks = {
        "possible faulty paragraph splits": (
            paragraph["split_candidate_count"],
            budget["max_split_candidate_count"],
            paragraph["split_candidates"][:5],
        ),
        "inline structural marker candidates": (
            paragraph["inline_structural_candidate_count"],
            budget["max_inline_structural_candidate_count"],
            paragraph["inline_structural_candidates"][:5],
        ),
        "repeated word windows": (
            len(result["repeated_windows"]),
            budget["max_repeated_window_count"],
            result["repeated_windows"][:5],
        ),
        "missing front contents pages": (
            front_toc["missing_front_toc_pages"],
            budget["max_front_toc_missing_pages"],
            front_toc["missing_front_toc_samples"][:5],
        ),
        "reference continuation splits": (
            paragraph["reference_continuation_split_count"],
            budget["max_reference_continuation_split_count"],
            paragraph["reference_continuation_splits"][:5],
        ),
        "citation continuation splits": (
            paragraph["citation_continuation_split_count"],
            budget["max_citation_continuation_split_count"],
            paragraph["citation_continuation_splits"][:5],
        ),
        "adjacent duplicate paragraphs": (
            paragraph["adjacent_duplicate_count"],
            budget["max_adjacent_duplicate_count"],
            paragraph["adjacent_duplicates"][:5],
        ),
        "missing enumerator markers": (
            enumerators["missing_marker_count"],
            budget["max_missing_marker_count"],
            enumerators["missing_markers"][:5],
        ),
    }

    gh = result["greek_hebrew_word_coverage"]
    ghf = result["greek_hebrew_clause_fidelity"]
    if gh["pdf_greek_word_count"] >= 20:
        checks["greek word coverage"] = (
            gh["greek_word_coverage_ratio"],
            budget["min_greek_word_coverage_ratio"],
            gh["missing_greek_word_samples"][:5],
        )
    if gh["pdf_hebrew_word_count"] >= 10:
        checks["hebrew word coverage"] = (
            gh["hebrew_word_coverage_ratio"],
            budget["min_hebrew_word_coverage_ratio"],
            gh["missing_hebrew_word_samples"][:5],
        )
    checks["missing greek clauses"] = (
        ghf["missing_greek_clause_count"],
        budget["max_missing_greek_clauses"],
        ghf["missing_greek_clauses"][:5],
    )
    checks["missing hebrew clauses"] = (
        ghf["missing_hebrew_clause_count"],
        budget["max_missing_hebrew_clauses"],
        ghf["missing_hebrew_clauses"][:5],
    )

    failures = [
        f"{name}: observed {observed}, budget {limit}, samples {samples}"
        for name, (observed, limit, samples) in checks.items()
        if "coverage" not in name and observed > limit
    ]
    # Coverage ratios: lower is worse
    ratio_failures = [
        f"{name}: observed {observed}, budget {limit}, samples {samples}"
        for name, (observed, limit, samples) in checks.items()
        if "coverage" in name and observed < limit
    ]
    assert not failures, "\n".join(failures)
    assert not ratio_failures, "\n".join(ratio_failures)


@pytest.mark.parametrize("volume", VOLUMES)
def test_known_epub_bug_classes_do_not_regress(volume):
    result = epub_audit_result(volume)
    budget = budget_for(volume)["epub"]
    info = result["info"]
    language = info["language"]
    scan = info["content_scan"]

    warning_codes = {item["code"] for item in result["warnings"]}
    allowed_codes = set(budget["allowed_warning_codes"])
    assert warning_codes <= allowed_codes

    # In the sandbox the fonts symlink points outside the mount, so the rendered
    # EPUB will lack embedded fonts.  Filter that known-environment error so it
    # doesn't mask real regressions.
    errors = result["errors"]
    if not FONTS_AVAILABLE:
        errors = [e for e in errors if e.get("code") != "missing_fonts"]
    errors = [e for e in errors if e.get("code") != "nav_in_spine"]
    error_count = len(errors)

    checks = {
        "EPUB packaging errors": (error_count, budget["max_error_count"], errors[:5]),
        "untagged Greek characters": (
            language["greek_untagged_chars"],
            budget["max_greek_untagged_chars"],
            scan["samples"]["untagged_greek"][:5],
        ),
        "untagged Hebrew characters": (
            language["hebrew_untagged_chars"],
            budget["max_hebrew_untagged_chars"],
            scan["samples"]["untagged_hebrew"][:5],
        ),
        "repeated phrase hits": (
            scan["repeated_phrase_count"],
            budget["max_repeated_phrase_count"],
            scan["samples"]["repeated_phrase"][:5],
        ),
        "possible Beta Code residue files": (
            scan["beta_code_files"],
            budget["max_beta_code_files"],
            scan["samples"]["beta_code"][:5],
        ),
        "escaped language-tag files": (
            scan["escaped_lang_tag_files"],
            budget["max_escaped_lang_tag_files"],
            scan["samples"]["escaped_lang_tag"][:5],
        ),
        "literal footnote marker files": (
            scan["literal_footnote_marker_files"],
            budget["max_literal_footnote_marker_files"],
            scan["samples"]["literal_footnote_marker"][:5],
        ),
        "empty bracket noise files": (
            scan["empty_bracket_noise_files"],
            budget["max_empty_bracket_noise_files"],
            scan["samples"]["empty_bracket_noise"][:5],
        ),
        "noteref links without spacing class": (
            scan["noteref_without_class"],
            budget["max_noteref_without_class"],
            scan["samples"]["noteref_without_class"][:5],
        ),
    }

    failures = [
        f"{name}: observed {observed}, budget {limit}, samples {samples}"
        for name, (observed, limit, samples) in checks.items()
        if observed > limit
    ]
    assert not failures, "\n".join(failures)


@pytest.mark.parametrize("volume", VOLUMES)
def test_implemented_bug_samples_stay_absent(volume):
    budget = budget_for(volume)
    samples = budget.get("absent_samples", [])
    if not samples:
        pytest.skip("No implemented bug samples have been ratcheted into the baseline yet")

    text_result = text_integrity_result(volume)
    epub_result = epub_audit_result(volume)
    haystacks = {
        "text_integrity": json.dumps(text_result, ensure_ascii=False).lower(),
        "epub": json.dumps(epub_result, ensure_ascii=False).lower(),
    }

    failures = []
    for sample in samples:
        audit_name = sample["audit"]
        needle = sample["text"].lower()
        if needle in haystacks[audit_name]:
            failures.append(f"{audit_name} still contains sample: {sample['text']}")

    assert not failures, "\n".join(failures)


# ---------------------------------------------------------------------------
# Issue 21: dangling single-letter initial splits
# ---------------------------------------------------------------------------

def test_issue_21_dangling_initial_pair_is_joined():
    """A paragraph ending with a bare capital-letter initial (e.g. "S.") must be
    merged with the following paragraph.  Real v3 case:

        "…clamorous writings of S.\\n\\nP. [f80] do sufficiently manifest."

    Both initials belong to the same author citation ("S. P.") and must land in
    the same HTML paragraph — not split into <p>…S.</p> / <p>P…</p>.
    """
    md = (
        "These things are sufficiently manifest, as the scurrilous, clamorous writings of S.\n\n"
        "P. [f80] do sufficiently manifest.\n\n"
        "Secondly, Regeneration by the Holy Spirit is the same work."
    )
    html, _, _ = markdown_to_html(md)
    paras = re.findall(r'<p[^>]*>(.*?)</p>', html, re.S)
    plain_paras = [re.sub(r'<[^>]+>', '', p) for p in paras]
    # After the fix there should be exactly 2 body paragraphs (merged + Secondly)
    # and the first must contain BOTH "S." and "P."
    first_para = plain_paras[0] if plain_paras else ""
    assert "S." in first_para and "P." in first_para, (
        f"S. and P. must be in the same paragraph after the fix.\n"
        f"Paragraphs: {plain_paras}"
    )
    # No paragraph should start with bare "P." (the orphan)
    for para in plain_paras:
        assert not re.match(r'^\s*P\.\s', para), \
            f"Orphan paragraph starting with 'P.' found: {para[:80]!r}"


def test_issue_21_chap_roman_numeral_not_merged():
    """'chap. I.' at end of a paragraph is a chapter reference; the following
    paragraph must NOT be swallowed into it.
    """
    md = (
        "The complacency of the mind in them, chap. I.\n\n"
        "The treatise is divided into two parts: —"
    )
    html, _, _ = markdown_to_html(md)
    assert re.search(r'<p[^>]*>The treatise is divided', html), \
        "chap. I. paragraph boundary must be preserved"


def test_issue_21_structural_dash_roman_not_merged():
    """'— I.' (em-dash + Roman numeral) marks a numbered observation.
    The following observation text must stay in its own paragraph.
    """
    md = (
        "This title of the psalm will yield us these two observations: — I.\n\n"
        "That the espousals of Christ and his church are real and true."
    )
    html, _, _ = markdown_to_html(md)
    assert re.search(r'<p[^>]*>That the espousals', html), \
        "observation text must remain its own paragraph after '— I.'"


def test_issue_21_multi_volume_known_cases():
    """Real dangling-initial pairs from multiple volumes must be joined into one
    paragraph — no orphan paragraph that opens with just the second initial.

    Without the fix, D./V. at the start of a paragraph are promoted to bold
    list-item markers: <p class="list-item"><b>D.</b> Kimchi …>.  After the fix
    they are absorbed into the preceding paragraph as plain inline text.
    """
    cases = [
        # v12: Rabbi David Kimchi — "R.\n\nD. Kimchi" → single paragraph
        (
            "men who are of the greatest note amongst them in these latter days, as R.\n\n"
            "D. Kimchi, Aben Ezra, Abrabanel, Lipman.",
            # The orphan pattern matches either a list-item bold marker or a bare <p>
            r'<p[^>]*>(?:\s*<b>)?D\.',
        ),
        # v14: "Mr J.\n\nV. C." → single paragraph
        (
            "happily ensue after so various tumults in the kingdom. By Mr J.\n\n"
            "V. C., a friend to men of all religions, 1661.",
            r'<p[^>]*>(?:\s*<b>)?V\.',
        ),
    ]
    for md, orphan_pattern in cases:
        html, _, _ = markdown_to_html(md)
        assert not re.search(orphan_pattern, html), \
            f"Orphan paragraph detected in: {md[:60]!r}"


# ---------------------------------------------------------------------------
# Issue 22: Hebrew bidi isolation
# ---------------------------------------------------------------------------

def test_issue_22_hebrew_css_uses_bidi_isolate():
    """Hebrew spans must declare unicode-bidi: isolate so brackets surrounding
    inline Hebrew (e.g. '[Hebrew Keri]') stay on the correct visual side.
    """
    # Hebrew CSS lives in EPUB3_FONT_STYLES (the per-XHTML inline style block),
    # not in the base EPUB_STYLESHEET.
    assert 'unicode-bidi: isolate' in EPUB3_FONT_STYLES, \
        "Hebrew CSS must use unicode-bidi: isolate, not embed"
    assert 'unicode-bidi: embed' not in EPUB3_FONT_STYLES, \
        "unicode-bidi: embed must be replaced with unicode-bidi: isolate"


def test_issue_22_hebrew_keri_bracket_outside_span():
    """tag_unicode_ranges must NOT pull the ASCII word 'Keri' inside a Hebrew
    span — 'Keri' is an English label and must stay in LTR context.
    """
    from render import tag_unicode_ranges
    from html import escape as _esc
    raw = 'תוֹרָתִי [רֻבֵּי Keri] תֻבֵּוֹּ'
    result = tag_unicode_ranges(_esc(raw))
    # 'Keri' must appear outside any <span lang="he"…> element
    assert 'Keri</span>' not in result, \
        f"'Keri' is swallowed inside a Hebrew span: {result}"
    assert re.search(r'</span>[^<]*Keri', result), \
        f"'Keri' must follow the closing </span> of its Hebrew word: {result}"


# ---------------------------------------------------------------------------
# Issue 23: compact blockquote CSS
# ---------------------------------------------------------------------------

def test_issue_23_blockquote_css_is_compact():
    """Blockquote margins must conform to GEMINI.md mandate: 1.2em top/bottom and 0 left/right."""
    bq_match = re.search(r'blockquote\s*\{([^}]+)\}', EPUB_STYLESHEET, re.S)
    assert bq_match, "No blockquote rule found in EPUB_STYLESHEET"
    bq_rule = bq_match.group(1)

    m = re.search(r'margin\s*:\s*([\d.]+)em\s+([\d.]+)(?:em)?', bq_rule)
    assert m, f"Expected 'margin: Xem Yem' in blockquote rule; got:\n{bq_rule}"
    top_bottom = float(m.group(1))
    left_right = float(m.group(2))
    assert top_bottom == 1.2
    assert left_right == 0.0


def test_issue_23_blockquote_p_margin_is_compact():
    """blockquote p must have a small vertical margin — enough for breathing
    room between quoted paragraphs but not so large that blockquotes feel airy.
    """
    bq_p_match = re.search(r'blockquote\s+p\s*\{([^}]+)\}', EPUB_STYLESHEET, re.S)
    assert bq_p_match, "No 'blockquote p' rule found in EPUB_STYLESHEET"
    bq_p_rule = bq_p_match.group(1)
    p_m = re.search(r'margin\s*:\s*([\d.]+)', bq_p_rule)
    if p_m:
        assert float(p_m.group(1)) <= 0.3, \
            f"blockquote p margin {p_m.group(1)}em is too large"


# ---------------------------------------------------------------------------
# Issue 19 – semicolon/comma-based list merging
# Rule: items ending with ';' or ',' accumulate; items ending with anything
# else flush the accumulated run into a single continuous paragraph.
# ---------------------------------------------------------------------------

def _build_list_html(*items):
    """Build consecutive <p class="list-item"> elements from (marker, content) pairs."""
    return ''.join(
        f'<p class="list-item"><b>{mk}</b> {ct}</p>'
        for mk, ct in items
    )


def test_issue_19_semicolon_list_merged_into_single_paragraph():
    """All non-final items ending with ';' — entire run merges to one paragraph.

    Canonical example: 1. Wisdom; 2. Knowledge, 1 Cor. 12:8; 3. Faith; ...
    9. Interpretation of tongues, verse 10.
    Non-finals end with ';' → all 9 items merge to one <p class="list-item">.
    """
    html = _build_list_html(
        ('1.', 'Wisdom;'),
        ('2.', 'Knowledge, 1 Corinthians 12: 8, or the word of wisdom and the word of knowledge;'),
        ('3.', 'Faith;'),
        ('4.', 'Healing, verse 9;'),
        ('5.', 'Working of miracles;'),
        ('6.', 'Prophecy;'),
        ('7.', 'Discerning of spirits;'),
        ('8.', 'Kinds of tongues;'),
        ('9.', 'Interpretation of tongues, verse 10.'),
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 1, (
        "Expected 9-item semicolon list to merge into a single paragraph"
    )
    assert 'Wisdom;' in result
    assert 'Prophecy;' in result
    assert 'Interpretation of tongues, verse 10.' in result


def test_issue_19_long_items_with_semicolons_still_merge():
    """Word count is irrelevant — long items ending with ';' must still merge."""
    html = _build_list_html(
        ('1.', 'God is absolutely sovereign over all creation, and his will cannot be frustrated;'),
        ('2.', 'God is perfectly holy in all his ways and works;'),
        ('3.', 'God is love, and all his acts flow from that love.'),
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 1, (
        "Long-item semicolon list must merge regardless of word count"
    )


def test_issue_19_period_terminated_items_stay_separate():
    """Items ending with '.' are standalone statements — must not be merged."""
    html = _build_list_html(
        ('1.', 'God is sovereign.'),
        ('2.', 'God is holy.'),
        ('3.', 'God is love.'),
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 3, (
        "Period-terminated list items must remain as separate paragraphs"
    )


def test_issue_19_heterogeneous_run_splits_correctly():
    """In a mixed run, long period-terminated items stay separate while the
    following semicolon sub-run merges independently.
    """
    html = _build_list_html(
        ('Secondly,', 'the Holy Spirit illuminates the mind with a full and clear apprehension of truth.'),
        ('1.', 'Illumination;'),
        ('2.', 'Conviction;'),
        ('3.', 'Reformation.'),
    )
    result = _merge_short_inline_lists(html)
    # 'Secondly' ends with '.' → stays alone; items 1-3 merge (non-finals end with ';')
    assert result.count('<p class="list-item">') == 2, (
        "Expected 'Secondly' paragraph to stay separate while 1/2/3 sub-run merges"
    )


# ---------------------------------------------------------------------------
# Issue 19.d – last item of inline run lacks a bold marker
# When "5. To depart." is split from a merged paragraph, it may arrive as a
# plain <p class="list-item"> with no <b> wrapper.  The regex must not create
# nested <p> tags by falling through to the old 'item_contents' fallback.
# ---------------------------------------------------------------------------

def _build_roman_list_html(*items):
    """Build consecutive <p class="roman-list-item"> elements from (marker, content) pairs."""
    return ''.join(
        f'<p class="roman-list-item"><b>{mk}</b> {ct}</p>'
        for mk, ct in items
    )


def test_issue_19d_last_item_without_bold_marker_no_nested_p():
    """A list-item paragraph that has no bold marker must not produce nested <p> tags."""
    html = (
        '<p class="list-item"><b>1.</b> To proceed;</p>'
        '<p class="list-item"><b>2.</b> To come, or come upon;</p>'
        '<p class="list-item"><b>3.</b> To fall on men;</p>'
        '<p class="list-item"><b>4.</b> To rest; and,</p>'
        '<p class="list-item">5. To depart.</p>'
    )
    result = _merge_short_inline_lists(html)
    assert '<p class="list-item">' not in result.replace(
        '<p class="list-item">', '', 1
    ), "Should merge into a single list-item paragraph"
    assert '<p <p' not in result, "Must not produce nested <p> tags"
    assert 'To depart.' in result, "Last item content must survive the merge"


def test_issue_19_roman_list_single_word_items_merge():
    """Roman numeral list with single-word items should merge into continuous prose (Rule A)."""
    html = _build_roman_list_html(
        ('I.', 'Complacency;'),
        ('II.', 'Permanency.'),
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="roman-list-item">') == 1, (
        "Single-word Roman list items must merge into one paragraph (Rule A)"
    )
    assert 'Complacency' in result and 'Permanency' in result


def test_issue_19_roman_list_semicolon_run_merges():
    """Roman numeral items ending in ';' accumulate under Rule B."""
    html = _build_roman_list_html(
        ('I.', 'To proceed;'),
        ('II.', 'To come, or come upon;'),
        ('III.', 'To fall on men;'),
        ('IV.', 'To rest; and,'),
        ('V.', 'To depart.'),
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="roman-list-item">') == 1, (
        "Semicolon-terminated Roman items must merge into one paragraph (Rule B)"
    )
    assert 'To depart.' in result


def test_issue_19_roman_list_does_not_merge_with_arabic_run():
    """A roman-list-item run and a list-item run must not be merged together."""
    html = (
        '<p class="roman-list-item"><b>I.</b> First;</p>'
        '<p class="roman-list-item"><b>II.</b> Second.</p>'
        '<p class="list-item"><b>1.</b> One;</p>'
        '<p class="list-item"><b>2.</b> Two.</p>'
    )
    result = _merge_short_inline_lists(html)
    # Each class merges independently; classes must not bleed into each other
    assert result.count('<p class="roman-list-item">') == 1
    assert result.count('<p class="list-item">') == 1


# ---------------------------------------------------------------------------
# Signature detection and coalescing (multi-paragraph sign-offs)
# ---------------------------------------------------------------------------

def test_detect_signature_pattern_3b_from_my_study():
    """Standalone 'From my Study,' is detected as a signature (Pattern 3b)."""
    assert _detect_signature("From my Study,", is_front_matter=False)
    assert _detect_signature("From my study at —", is_front_matter=False)
    # Long prose sentence starting with 'From' must NOT trigger
    assert not _detect_signature(
        "From my study of the scriptures I have concluded that the love of God is infinite.",
        is_front_matter=False,
    )


def test_detect_signature_pattern_6b_city_month_year():
    """'Edinburgh, August 1850.' is detected as a signature (Pattern 6b)."""
    assert _detect_signature("Edinburgh, August 1850.", is_front_matter=False)
    assert _detect_signature("London, September 1677", is_front_matter=False)
    assert _detect_signature("Oxford, January 1670.", is_front_matter=False)
    # Body text that happens to start with a city should not match without a date
    assert not _detect_signature("Edinburgh, the seat of the ancient church", is_front_matter=False)


def test_coalesce_jo_three_line_signature():
    """J.O. sign-off split across three paragraphs is merged into one signature block."""
    html = (
        '\n'.join([
            '<p class="signature">J.O.</p>',
            '<p class="signature">From my Study,</p>',
            '<p class="signature">September the last, [1645].</p>',
        ])
    )
    result = _coalesce_adjacent_signatures(html)
    assert result.count('<p class="signature">') == 1
    assert 'J.O.' in result
    assert 'From my Study,' in result
    assert 'September the last, [1645].' in result
    assert result.count('<br/>') == 2


def test_coalesce_whg_two_line_signature():
    """W.H.G. sign-off split across two paragraphs is merged into one signature block."""
    html = (
        '\n'.join([
            '<p class="signature">W. H. G.</p>',
            '<p class="signature">Edinburgh, August 1850.</p>',
        ])
    )
    result = _coalesce_adjacent_signatures(html)
    assert result.count('<p class="signature">') == 1
    assert 'W. H. G.' in result
    assert 'Edinburgh, August 1850.' in result
    assert result.count('<br/>') == 1


def test_coalesce_does_not_merge_unrelated_signatures():
    """Two signature blocks separated by body text must not be merged."""
    html = (
        '<p class="signature">J.O.</p>\n'
        '<p>This is body text between two letters.</p>\n'
        '<p class="signature">W. H. G.</p>\n'
        '<p class="signature">Edinburgh, August 1850.</p>'
    )
    result = _coalesce_adjacent_signatures(html)
    # J.O. stays separate; W.H.G. and Edinburgh merge
    assert result.count('<p class="signature">') == 2


def test_coalesce_single_signature_unchanged():
    """A lone signature paragraph is not modified."""
    html = '<p>Body text.</p>\n<p class="signature">= John Owen</p>\n<p>More body text.</p>'
    result = _coalesce_adjacent_signatures(html)
    assert result == html


# ---------------------------------------------------------------------------
# Owenian connector links ("As, —" / "For, —") — merge with preceding paragraph
# ---------------------------------------------------------------------------

def test_owenian_link_as_emdash_merged_with_preceding():
    """'As, —' as a standalone paragraph is appended to the preceding sentence."""
    md = "Some things have an evidence in them.\n\nAs, —\n\n1st, That there is nothing carnal in it."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    # The 'As, —' must NOT be a separate paragraph
    assert html.count('<p') <= 2  # body + list item, not three separate paragraphs
    # "As, —" must appear at the end of the first body paragraph
    assert 'As, —' in html or 'As, —' in html

def test_owenian_link_for_emdash_merged_with_preceding():
    """'For, —' as a standalone paragraph is appended to the preceding sentence."""
    md = "Consider these things carefully.\n\nFor, —\n\n1. First, the grace of God."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    import re
    # 'For, —' should not be its own paragraph; it should follow the sentence
    assert not re.search(r'<p[^>]*>\s*For,\s*[—–]\s*</p>', html)

def test_owenian_link_does_not_merge_at_document_start():
    """A connector phrase with no preceding paragraph must not error."""
    md = "For, —\n\n1. The first thing."
    # Should render without crashing; the connector stays as its own paragraph
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert html  # no exception


# ---------------------------------------------------------------------------
# "(1.) ... and (2.) ..." — connector-terminated list items merge  (Issue 27)
# ---------------------------------------------------------------------------

def test_list_items_joined_by_and_merge():
    """'(1.) ... and' followed by '(2.) ...' must merge into one paragraph
    because the trailing 'and' is a grammatical connector, not a sentence end."""
    html = (
        '<p class="list-item"><b>(1.)</b> What this work is, and</p>'
        '<p class="list-item"><b>(2.)</b> How it is performed.</p>'
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 1
    assert 'What this work is, and' in result
    assert 'How it is performed.' in result

def test_list_items_joined_by_or_merge():
    """Items joined by 'or' behave the same as 'and'."""
    html = (
        '<p class="list-item"><b>1.</b> Whether it be true or</p>'
        '<p class="list-item"><b>2.</b> Whether it be false.</p>'
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 1


def test_connector_merge_does_not_swallow_following_item():
    """Regression for the Rule-C over-merge bug (Issue 27 follow-up).

    Run:  (1.) ...and  |  (2.) ...period  |  (1.) In general; ...
    Expected: items 1+2 merge into one paragraph; the third (1.) stays separate.
    The old Rule C merged all three because it scanned the WHOLE run for any
    non-final connector.  Rule B with connector-as-non-terminating only merges
    the contiguous 'and'-connected pair and then starts a fresh sub-run.
    """
    html = (
        '<p class="list-item"><b>(1.)</b> What this work is, and</p>'
        '<p class="list-item"><b>(2.)</b> How it is performed.</p>'
        '<p class="list-item"><b>(1.)</b> In general; herein we must consider the agent.</p>'
    )
    result = _merge_short_inline_lists(html)
    # Pair (1.)+(2.) → 1 merged paragraph; third (1.) → 1 separate paragraph
    assert result.count('<p class="list-item">') == 2
    assert 'What this work is, and' in result
    assert 'How it is performed.' in result
    assert 'In general; herein' in result


def test_list_items_period_terminated_still_stay_separate():
    """Items that end with a period (standalone statements) must NOT merge even
    when surrounded by items with 'and'/'or' — guard only fires when a
    NON-FINAL item ends with a connector."""
    html = (
        '<p class="list-item"><b>1.</b> God is sovereign.</p>'
        '<p class="list-item"><b>2.</b> God is holy.</p>'
    )
    result = _merge_short_inline_lists(html)
    assert result.count('<p class="list-item">') == 2


# ---------------------------------------------------------------------------
# J.O. tail-signature split (body paragraph ending with signature)  (Issue 29)
# ---------------------------------------------------------------------------

def test_tail_signature_split_from_body_paragraph():
    """When 'J.O. From my Study, ...' is fused at the END of a body paragraph,
    the pre-pass should split it off so it gets the signature class."""
    md = (
        "the spring and means of this communion is no small part of the glory of the gospel. "
        "J.O. From my Study, September the last, [1645]."
    )
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER", front_matter_style="prose")
    # Should produce a signature paragraph
    assert '<p class="signature">' in html
    # The body text should be separate from the signature
    assert 'glory of the gospel' in html

def test_jo_full_single_paragraph_gets_three_line_split():
    """'J.O. From my Study, September the last, [1645].' as one paragraph
    should produce three visual lines joined by <br/>."""
    md = "J.O. From my Study, September the last, [1645]."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert '<p class="signature">' in html
    # Two <br/> separators for three lines
    assert html.count('<br/>') >= 2
    assert 'J.O.' in html
    assert 'From my Study' in html
    assert 'September the last' in html


# ---------------------------------------------------------------------------
# Issue #32 — Bold scholastic anchors preserved after connector comma
# ---------------------------------------------------------------------------

def test_bold_list_anchor_preserved_after_for_comma():
    """'1.' should remain bold when the preceding paragraph is 'For,' (a short
    connector phrase ending with a comma).  Previously the over-broad unbold
    guard stripped bold from any paragraph starting with a number when the
    previous paragraph ended with a comma.
    """
    md = "For,\n\n1. It will herein appear, that the grace of God is sufficient."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert '<b>1.' in html, "The list anchor '1.' must be bold after 'For,'"


def test_bold_list_anchor_preserved_after_i_say_comma():
    """'1.' should remain bold when the preceding paragraph ends with 'I say,'."""
    md = "And unto the objection I say,\n\n1. Nothing is more fully evident in Scripture."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert '<b>1.' in html, "The list anchor '1.' must be bold after 'I say,'"


def test_bold_verse_continuation_number_still_unbolded():
    """Regression guard: a bare number after a scripture-reference comma should
    still be unbolded (it is a verse range continuation, not a list anchor).
    """
    md = "Rom. 5:12, 14,\n\n9. This is a verse number continuation."
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert '<b>9.' not in html, "Verse-range continuation '9.' must not be bold"


# ---------------------------------------------------------------------------
# Issue #33 — "For, —" / "For," merge onto preceding paragraph
# ---------------------------------------------------------------------------

def test_bare_for_comma_merges_onto_preceding_paragraph():
    """A standalone 'For,' paragraph (no em-dash) must be appended to the
    preceding prose paragraph, not left as an isolated element.
    """
    md = (
        "But we may proceed to what is of our immediate concernment.\n\n"
        "For,\n\n"
        "1. It is known with what subtlety and urgency his divine nature was assailed."
    )
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    # 'For,' must NOT be its own paragraph
    assert not re.search(r'<p[^>]*>\s*For,\s*</p>', html), (
        "'For,' must be merged onto the preceding paragraph, not standalone"
    )
    # It should appear at the end of the preceding prose paragraph
    assert 'For,' in html


def test_bare_as_comma_merges_onto_preceding_paragraph():
    """Same as above for 'As,' — a standalone 'As,' must attach to the preceding."""
    md = (
        "The instances which I shall give concerning the use are these.\n\n"
        "As,\n\n"
        "1. The first instance is this."
    )
    html, _, _ = markdown_to_html(md, current_mode="BODY_TEXT")
    assert not re.search(r'<p[^>]*>\s*As,\s*</p>', html), (
        "'As,' must be merged onto the preceding paragraph, not standalone"
    )


def test_for_emdash_in_roman_heading_stays_on_heading():
    """When 'For, —' appears at the END of a roman-section paragraph (e.g.
    'II. This darkness ... so to be. For, —'), the roman-section splitter
    must NOT peel it off into a separate paragraph.  It belongs on the heading.
    """
    text = (
        "II. This darkness in the minds of men, this ignorance of God, his nature "
        "and his will, was the original of all evil unto the world, and yet continues "
        "so to be. For, —"
    )
    html, _, _ = markdown_to_html(text, current_mode="BODY_TEXT")
    # Must not produce a lone <p>For, —</p>
    assert not re.search(r'<p[^>]*>\s*For,\s*[—–]\s*</p>', html), (
        "'For, —' must not appear as a standalone paragraph"
    )
    # The connector must be part of the heading element
    assert 'For, —' in html


# ---------------------------------------------------------------------------
# Issue #34 — Contents page: CHAPTER 20 must appear before MEDITATIONS heading
# ---------------------------------------------------------------------------

def test_contents_last_chapter_before_next_treatise_heading():
    """The last chapter of one treatise must appear BEFORE the next treatise's
    heading in the rendered contents page, not after it.

    Root cause: _polish_contents_page_html used a pending_item buffer that
    deferred the CHAPTER 20 entry until the first item of the next section
    was encountered.  The MEDITATIONS heading appeared in the gap between
    CHAPTER 20 and '1. —', so CHAPTER 20 was flushed AFTER the heading.
    """
    # Minimal reproduction: a contents page with two treatises
    html = (
        '<section class="contents-page" epub:type="toc">'
        '<h1 class="contents-volume-title">CONTENTS OF VOLUME 1.</h1>'
        '<h2>CRISTOLOGIA</h2>'
        '<p class="contents-item"><b>Chapter 19</b>. The Exaltation of Christ.</p>'
        '<p class="contents-item"><b>Chapter 20</b>. The Exercise of the Mediatory Office.</p>'
        '<h2>MEDITATIONS AND DISCOURSES ON THE GLORY OF CHRIST.</h2>'
        '<p class="contents-item"><b>1. — </b> The Explication of the Text.</p>'
        '<p class="contents-item"><b>2. — </b> The Glory of the Person of Christ.</p>'
        '</section>'
    )
    result = _polish_contents_page_html(html)
    idx_ch20 = result.find('Chapter 20')
    idx_med = result.find('MEDITATIONS AND DISCOURSES')
    assert idx_ch20 < idx_med, (
        f"CHAPTER 20 (pos {idx_ch20}) must appear before MEDITATIONS heading "
        f"(pos {idx_med}) in the contents page"
    )


# ---------------------------------------------------------------------------
# Issue #35 — Front-matter prose chapters receive OCR text repairs
# ---------------------------------------------------------------------------

def test_front_matter_prose_hyphen_to_emdash_is_repaired():
    """A hyphen-as-em-dash (' - ') in a FRONT_MATTER prose chapter (General
    Preface, Prefatory Note) must be normalised to ' — '.
    """
    md = "The editor worked diligently - indeed without ceasing - on this edition."
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER", front_matter_style="prose")
    assert ' - ' not in html, "Hyphen-as-em-dash should be normalised in front-matter prose"
    assert '—' in html


def test_front_matter_prose_comma_hyphen_emdash_repaired():
    """'For, -' (comma + hyphen) in front-matter prose must become 'For, —'."""
    md = "For, -\n\n1. It begins with a clear principle."
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER", front_matter_style="prose")
    assert 'For, -' not in html, "'For, -' must be normalised to 'For, —' in front matter"


def test_front_matter_prose_list_anchors_are_bold():
    """Numbered list anchors in FRONT_MATTER prose must still receive bold
    treatment, just as they do in body chapters.
    """
    md = "There are three reasons,\n\n1. The first is this.\n\n2. The second is that."
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER", front_matter_style="prose")
    assert '<b>1.' in html or '<b>1.</b>' in html, "List anchor '1.' must be bold in front-matter prose"


def test_general_preface_v1_renders_without_standalone_for_comma():
    """The v1 General Preface raw text must not produce any lone 'For,' paragraphs
    after the full markdown_to_html pipeline.
    """
    import json
    v1_path = Path(__file__).parent.parent / 'volumes' / 'v1' / 'intermediate' / 'volume_1.json'
    if not v1_path.exists():
        pytest.skip('v1 intermediate JSON not available')
    with open(v1_path) as f:
        data = json.load(f)
    # Chapter 0 is the General Preface
    raw = data['chapters'][0].get('raw_text', '')
    html, _, _ = markdown_to_html(raw, current_mode="FRONT_MATTER", front_matter_style="prose")
    # No bare 'For,' paragraph should remain
    assert not re.search(r'<p[^>]*>\s*For,\s*</p>', html), (
        "General Preface must not contain a standalone 'For,' paragraph"
    )
    # No ' - ' (hyphen as dash) should survive repair
    plain = re.sub(r'<[^>]+>', '', html)
    # Allow compound words (letter-letter) and dates (digit-digit)
    leftover = [m.group() for m in re.finditer(r'[^a-zA-Z\d]-[^a-zA-Z\d]', plain)
                if m.group().strip() == '-']
    assert not leftover, f"Unrepaired hyphen-as-dash found in General Preface: {leftover[:3]}"


# ---------------------------------------------------------------------------
# Issue #47 — em-dash repair for colon + hyphen and paragraph-opening hyphen
# ---------------------------------------------------------------------------

def test_issue_47a_colon_hyphen_at_eol_repaired():
    """'directions: -\\n' must become 'directions: —\\n' (Issue 47a)."""
    raw = 'I shall tender the ensuing directions: -\n\nAnd here note'
    result = _repair_owen_ocr_errors(raw)
    assert 'directions: —' in result, f"Expected colon+hyphen repaired: {result!r}"
    assert 'directions: -' not in result


def test_issue_47a_semicolon_hyphen_at_eol_repaired():
    """Semicolon + space + hyphen at EOL is also an em-dash OCR artifact."""
    raw = 'He proceeds thus; -\n\nNaming the point'
    result = _repair_owen_ocr_errors(raw)
    assert '; —' in result, f"Expected semicolon+hyphen repaired: {result!r}"
    assert '; -' not in result


def test_issue_47b_paragraph_opening_hyphen_before_quote_repaired():
    """A paragraph starting '- \"quote...' must open with '— \"quote...' (Issue 47b)."""
    raw = '- "We could not otherwise have learned the things of God, unless our Master,'
    result = _repair_owen_ocr_errors(raw)
    assert result.startswith('— "'), f"Expected opening hyphen→em-dash: {result!r}"


def test_issue_47_existing_word_hyphen_not_disturbed():
    """A hyphen between words ('well-known') must not be touched by the new rules."""
    raw = 'a well-known matter\n\nsome other text'
    result = _repair_owen_ocr_errors(raw)
    assert 'well-known' in result, "Intra-word hyphen must be preserved"


def test_issue_47_existing_comma_hyphen_eol_still_repaired():
    """Existing Issue 44 rule ('For, -\\n') must still work alongside new rules."""
    raw = 'For, -\n\ncontinued text'
    result = _repair_owen_ocr_errors(raw)
    assert 'For, —' in result, f"Existing comma+hyphen rule must still fire: {result!r}"


# ---------------------------------------------------------------------------
# Issue #48 — colon-introduced (1.) list must not split to new paragraph
# ---------------------------------------------------------------------------

def test_issue_48_colon_para_merges_onto_first_list_item():
    """A <p> ending ':' immediately before <p class="list-item"> must be merged."""
    html = (
        '<p>And of them two things may be considered:</p>\n'
        '<p class="list-item"><b>(1.)</b> Their original; '
        '<b>(2.)</b> The design of their accomplishment.</p>'
    )
    result = _attach_colon_introduced_list(html)
    assert result.startswith('<p class="list-item">And of them two things'), (
        f"Colon paragraph must be merged onto list-item: {result[:120]!r}"
    )
    assert '<p>And of them' not in result, "Original standalone <p> must be gone"
    assert '(1.)' in result, "List item marker must be preserved"


def test_issue_48_list_item_class_preserved_for_downstream_merge():
    """After attachment the merged paragraph must still carry class='list-item'
    so that _merge_short_inline_lists can handle the full run."""
    html = (
        '<p>As follows:</p>\n'
        '<p class="list-item"><b>(1.)</b> First; </p>\n'
        '<p class="list-item"><b>(2.)</b> Second.</p>'
    )
    attached = _attach_colon_introduced_list(html)
    # The intro "As follows:" must now open a list-item paragraph
    assert attached.startswith('<p class="list-item">As follows:'), (
        f"Intro text must be merged into list-item: {attached[:80]!r}"
    )
    # The (2.) item must remain as a separate list-item for downstream Rule B
    assert attached.count('<p class="list-item">') == 2, (
        f"Expected 2 list-item paragraphs after attachment: {attached!r}"
    )
    merged = _merge_short_inline_lists(attached)
    # Rule B should merge both items since (1.) ends with ';'
    assert '<b>(2.)</b>' in merged, "Second item must still be present after full pipeline"


def test_issue_48_no_match_when_para_ends_with_non_colon():
    """A paragraph that does NOT end with ':' must not trigger the merge."""
    html = (
        '<p>This is a regular paragraph.</p>\n'
        '<p class="list-item"><b>(1.)</b> An item.</p>'
    )
    result = _attach_colon_introduced_list(html)
    # Original structure must be unchanged
    assert '<p>This is a regular paragraph.</p>' in result


def test_issue_48_existing_list_item_not_treated_as_intro():
    """A <p class="list-item"> ending in ':' must NOT swallow the next list-item."""
    html = (
        '<p class="list-item"><b>(1.)</b> First heading:</p>\n'
        '<p class="list-item"><b>(2.)</b> Second item.</p>'
    )
    result = _attach_colon_introduced_list(html)
    # The list-item should be left intact (it matches the exclusion clause)
    assert result == html, f"List-item ending ':' must not consume the next item: {result!r}"


# ---------------------------------------------------------------------------
# Issue #48.a — fused single-word Roman items must be split in raw text
# ---------------------------------------------------------------------------

def test_issue_48a_fused_roman_items_split_in_raw_text():
    """'I. Honor.II. Obedience.' must be split into two paragraphs by OCR repair."""
    raw = 'I. Honor.II. Obedience.III. Conformity.'
    result = _repair_owen_ocr_errors(raw)
    paragraphs = [p.strip() for p in result.split('\n\n') if p.strip()]
    assert len(paragraphs) == 3, (
        f"Expected 3 paragraphs after splitting fused Roman items, got {len(paragraphs)}: {paragraphs}"
    )
    assert paragraphs[0] == 'I. Honor.'
    assert paragraphs[1] == 'II. Obedience.'
    assert paragraphs[2] == 'III. Conformity.'


def test_issue_48a_split_does_not_fire_on_spaced_roman_items():
    """'I. Honor. II. Obedience.' (with space) must NOT be split again."""
    raw = 'I. Honor. II. Obedience. III. Conformity.'
    result = _repair_owen_ocr_errors(raw)
    # No extra paragraph breaks should be introduced (there's a space before II., III.)
    paragraphs = [p.strip() for p in result.split('\n\n') if p.strip()]
    assert len(paragraphs) == 1, (
        f"Spaced Roman items must stay in one paragraph, got {len(paragraphs)}: {paragraphs}"
    )


def test_issue_48a_lib_cap_reference_not_split():
    """'lib. IV. cap. 5' must not be split — space before IV. is the guard."""
    raw = 'See Aquin. lib. IV. cap. 5, and lib. VIII. cap. 2.'
    result = _repair_owen_ocr_errors(raw)
    assert '\n\n' not in result, (
        f"Scholarly reference with spaced Roman numerals must not be split: {result!r}"
    )


def test_issue_48a_single_word_roman_rule_a_guard():
    """_merge_short_inline_lists must not merge single-word roman-list-items AND must
    preserve the newline separators between them (Issue 48.a root cause)."""
    html = (
        '<p>four heads:</p>\n'
        '<p class="roman-list-item"><b>I.</b> Honor.</p>\n'
        '<p class="roman-list-item"><b>II.</b> Obedience.</p>\n'
        '<p class="roman-list-item"><b>III.</b> Conformity.</p>\n'
        '<p>After.</p>'
    )
    result = _merge_short_inline_lists(html)
    # Items must remain as 3 separate paragraphs, not merged into one
    count = result.count('<p class="roman-list-item">')
    assert count == 3, (
        f"Single-word roman-list-items must not be merged by Rule A, got {count} paragraphs:\n{result}"
    )
    # Items must NOT be directly adjacent (the \n separators must be preserved)
    assert '</p><p class="roman-list-item">' not in result, (
        "Roman-list-item paragraphs must be separated by whitespace, not run together:\n"
        + result
    )


# ---------------------------------------------------------------------------
# Issue #49 — missing terminal period in Ch 20 para 45
# ---------------------------------------------------------------------------

def test_issue_49_missing_period_repaired_by_v1_overrides():
    """V1 regex_replacements must add the terminal period to the bare phrase."""
    from shared import _repair_owen_ocr_errors
    raw = 'communication of the effects and likeness of the same image unto us which was essentially in himself\n\n(2.) We were by nature'
    config = {'regex_replacements': V1_OVERRIDES.get('regex_replacements', {})}
    result = _repair_owen_ocr_errors(raw, config=config)
    assert 'essentially in himself.' in result, (
        f"Missing terminal period must be added by v1 regex_replacements: {result!r}"
    )
    assert 'essentially in himself\n' not in result


def test_issue_49_period_not_doubled_when_already_present():
    """If the source ever gains the period, the replacement must not double it."""
    raw = 'which was essentially in himself.\n\n(2.) We were by nature'
    config = {'regex_replacements': V1_OVERRIDES.get('regex_replacements', {})}
    result = _repair_owen_ocr_errors(raw, config=config)
    assert 'himself..' not in result, (
        f"Period must not be doubled: {result!r}"
    )


# ---------------------------------------------------------------------------
# Title-page override must preserve foreign-script (Greek/Hebrew) epigraphs
# ---------------------------------------------------------------------------

def test_titlepage_override_preserves_greek_epigraph():
    """When a curated English title page replaces an extracted treatise title
    page, any Greek/Hebrew epigraph or scripture motto on the extracted page
    must be carried into the override — never silently dropped."""
    extracted = (
        '<section class="treatise-title-page" epub:type="titlepage">'
        '<h1 class="title-line-major">A Treatise</h1>'
        '<blockquote class="greek-title">ἐγένοντο ψευδοπροφῆται ἐν τῷ λαῷ</blockquote>'
        '</section>'
    )
    fragments = _foreign_fragments_in_section(extracted)
    assert any('ψευδοπροφῆται' in f for f in fragments), fragments

    override = (
        '<section class="treatise-title-page v1-applied-glory-title" epub:type="titlepage">'
        '<h1 class="title-line-major">A Treatise</h1>'
        '</section>'
    )
    merged = _merge_titlepage_override(override, fragments)
    assert 'ψευδοπροφῆται' in merged, merged
    assert merged.rstrip().endswith('</section>'), merged


def test_titlepage_override_does_not_duplicate_existing_foreign_text():
    """If the override already carries the same Greek text, it must not be
    appended a second time."""
    fragments = ['<blockquote class="greek-title">ἐν τῷ λαῷ</blockquote>']
    override = (
        '<section class="treatise-title-page" epub:type="titlepage">'
        '<blockquote class="greek-title">ἐν τῷ λαῷ</blockquote>'
        '</section>'
    )
    merged = _merge_titlepage_override(override, fragments)
    assert merged.count('ἐν τῷ λαῷ') == 1, merged


def test_titlepage_override_unchanged_when_no_foreign_text():
    """A title page with no Greek/Hebrew leaves the override byte-for-byte."""
    extracted = (
        '<section class="treatise-title-page" epub:type="titlepage">'
        '<h1 class="title-line-major">A Treatise</h1>'
        '</section>'
    )
    fragments = _foreign_fragments_in_section(extracted)
    assert fragments == []
    override = '<section class="treatise-title-page"><h1>A Treatise</h1></section>'
    assert _merge_titlepage_override(override, fragments) == override


# ---------------------------------------------------------------------------
# Mid-sentence → [[BLOCKQUOTE]] merging (faulty paragraph splits at page breaks)
# ---------------------------------------------------------------------------

def test_mid_sentence_before_blockquote_is_merged():
    """When prose ends mid-sentence before a [[BLOCKQUOTE]], the two should
    be joined — catching PDF page-break splits like 'They saw ⏎ [[BLOCKQUOTE]]
    "his glory..."' (v1 ch9 real case)."""
    from extract import _merge_adjacent_blockquote_paragraphs
    paras = [
        'when he dwelt among them in the days of his flesh. They saw',
        '[[BLOCKQUOTE]] "his glory, the glory as of the only-begotten of the Father, full of grace and truth:" John 1:14.',
        'So the apostle continues.',
    ]
    result = _merge_adjacent_blockquote_paragraphs(paras)
    assert len(result) == 2, f"Expected 2 paragraphs (merged+rest), got {len(result)}: {result}"
    assert 'They saw' in result[0] and 'his glory' in result[0], (
        f"Mid-sentence break before blockquote was not merged: {result[0]!r}"
    )


def test_content_word_before_blockquote_is_merged():
    """'tender' is a content word not in DANGLING_CONNECTOR_RE; it must still
    merge when it appears mid-sentence before [[BLOCKQUOTE]] (v1 ch11 real case)."""
    from extract import _merge_adjacent_blockquote_paragraphs
    paras = [
        'he was so to prophet of the church always as to tender',
        '[[BLOCKQUOTE]] manifold instructions unto the perishing, unbelieving world.',
    ]
    result = _merge_adjacent_blockquote_paragraphs(paras)
    assert len(result) == 1, f"Expected single merged paragraph, got {len(result)}: {result}"
    assert 'tender' in result[0] and 'manifold instructions' in result[0]


def test_prepositional_tail_before_blockquote_is_merged():
    """'in his' (v1 ch17) — a prepositional phrase that is incomplete — must
    merge with the following blockquote."""
    from extract import _merge_adjacent_blockquote_paragraphs
    paras = [
        'Psalm 36:8, 9 — that in his',
        '[[BLOCKQUOTE]] "presence is fullness of joy, and at his right hand are pleasures for evermore," Psalm 16:11.',
    ]
    result = _merge_adjacent_blockquote_paragraphs(paras)
    assert len(result) == 1
    assert 'in his' in result[0] and 'presence is fullness' in result[0]


def test_comma_ending_intro_does_not_merge_with_blockquote():
    """A sentence that ends with a comma (quote-intro style, e.g. 'saith God,')
    should NOT be merged into the following blockquote — Owen intentionally
    separates these as distinct paragraphs."""
    from extract import _merge_adjacent_blockquote_paragraphs
    paras = [
        'But this I will do, saith God,',
        '[[BLOCKQUOTE]] "I will make my glory pass before thee, and thou shalt see my back parts."',
    ]
    result = _merge_adjacent_blockquote_paragraphs(paras)
    assert len(result) == 2, (
        f"Comma-ending intro should NOT be merged with blockquote, got: {result}"
    )


def test_closed_quote_ending_before_blockquote_not_merged():
    """A paragraph ending with a closing quotation mark (a completed Latin
    citation) should NOT be merged with the following English translation
    blockquote — they are intentionally separate."""
    from extract import _merge_adjacent_blockquote_paragraphs
    paras = [
        'Patrise profitetur aequalem"',
        '[[BLOCKQUOTE]] “Human nature is assumed into the society of the Creator.”',
    ]
    result = _merge_adjacent_blockquote_paragraphs(paras)
    assert len(result) == 2, (
        f"Closed-quote ending should NOT merge with next blockquote: {result}"
    )


# ---------------------------------------------------------------------------
# render.py: _repair_mid_sentence_blockquote_splits (render-time counterpart)
# ---------------------------------------------------------------------------

def test_render_repair_mid_sentence_blockquote_strips_marker():
    """The render-time repair strips [[BLOCKQUOTE]] and merges content as plain
    prose when the previous paragraph ends mid-sentence (v1 ch9 pattern)."""
    from render import _repair_mid_sentence_blockquote_splits
    raw = (
        "when he dwelt among them in the days of his flesh. They saw\n\n"
        '[[BLOCKQUOTE]] "his glory, the glory as of the only-begotten of the Father," John 1:14.\n\n'
        "So the apostle proceeds."
    )
    result = _repair_mid_sentence_blockquote_splits(raw)
    paras = [p.strip() for p in result.split('\n\n') if p.strip()]
    assert len(paras) == 2, f"Expected 2 paragraphs after merge, got {len(paras)}"
    assert 'They saw' in paras[0] and 'his glory' in paras[0], paras[0]
    assert '[[BLOCKQUOTE]]' not in paras[0], "Marker must be stripped from merged paragraph"
    assert paras[1] == "So the apostle proceeds."


def test_render_repair_leaves_comma_intro_untouched():
    """Comma-ending intro ('saith God,') before [[BLOCKQUOTE]] must NOT merge."""
    from render import _repair_mid_sentence_blockquote_splits
    raw = (
        'But this I will do, saith God,\n\n'
        '[[BLOCKQUOTE]] "I will make my glory pass before thee."\n\n'
        'And so he continued.'
    )
    result = _repair_mid_sentence_blockquote_splits(raw)
    paras = [p.strip() for p in result.split('\n\n') if p.strip()]
    assert len(paras) == 3, f"Comma-ending intro must keep blockquote separate: {paras}"
    assert paras[0].endswith('saith God,')
    assert paras[1].startswith('[[BLOCKQUOTE]]')


def test_render_repair_mid_sentence_used_in_full_pipeline():
    """End-to-end: markdown_to_html must produce merged prose (no orphaned
    blockquote) when prose ends mid-sentence before [[BLOCKQUOTE]]."""
    html, _, _ = markdown_to_html(
        "in the days of his flesh. They saw\n\n"
        '[[BLOCKQUOTE]] "his glory, the glory as of the only-begotten of the Father."'
    )
    # Should be a single <p> containing both parts — no blockquote element
    assert 'They saw' in html
    assert 'his glory' in html
    assert '<blockquote' not in html, (
        "Mid-sentence break before blockquote must render as plain prose, not blockquote"
    )


# ---------------------------------------------------------------------------
# render.py: Grammar-aware introductory punctuation support & Closed-Sentence Gate
# ---------------------------------------------------------------------------

def test_comma_introduced_flat_syllabus_absorbed():
    """
    Grammatically open introductory paragraphs (ending in comma, semicolon, etc.)
    should be allowed to absorb flat lists.
    "two heads,
     1st, Adoration; 2ndly, Invocation."
    should become a single paragraph: "two heads, 1st, Adoration; 2ndly, Invocation."
    """
    from render import _attach_em_dash_flat_list
    html = (
        '<p>reduced unto two heads,</p>\n'
        '<p class="list-item"><b>1st,</b> Adoration;</p>\n'
        '<p class="list-item"><b>2ndly,</b> Invocation.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, "Items should be absorbed flat"
    assert result.count("<p") == 1, "Should collapse to a single paragraph"
    assert "reduced unto two heads, <b>1st,</b> Adoration; <b>2ndly,</b> Invocation.</p>" in result


def test_closed_sentence_gate_prevents_false_positives():
    """
    Introductory paragraphs ending in a period (closed punctuation) must NOT
    absorb list items unless they match an explicit syllabus signal (exact count,
    binary count, or formula tail).
    """
    from render import _attach_em_dash_flat_list
    
    # 1. Plain prose ending in period with no explicit counts/formula: stays separate block
    html = (
        '<p>This was a great doctrine of the church.</p>\n'
        '<p class="list-item"><b>1.</b> First item here.</p>\n'
        '<p class="list-item"><b>2.</b> Second item here.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, "Plain period-ending prose must not flatten"
    assert result.count("<p") == 3
    
    # 2. Period-ending prose with exact count match (announced two, got two items): allowed to flatten
    html_exact = (
        '<p>The apostle here proposes two things.</p>\n'
        '<p class="list-item"><b>(1.)</b> The person of Christ.</p>\n'
        '<p class="list-item"><b>(2.)</b> The work of Christ.</p>'
    )
    result_exact = _attach_em_dash_flat_list(html_exact)
    assert 'class="list-item"' not in result_exact, "Exact count match list after period should flatten"
    assert result_exact.count("<p") == 1
    assert "proposes two things. <b>(1.)</b> The person of Christ. <b>(2.)</b> The work of Christ.</p>" in result_exact


def test_apply_premium_salutations():
    """Verify that prefatory salutations like 'Christian Reader,' are properly converted and styled, while standard prose references are ignored."""
    from render import _apply_premium_salutations

    # 1. Volume 1 Preface summary-tagged greeting
    html1 = '<p class="chapter-summary">Christian Reader,</p>'
    res1 = _apply_premium_salutations(html1)
    assert res1 == '<p class="prefatory-salutation">Christian Reader,</p>'

    # 2. Wrapped in bold/italic tags
    html2 = '<p class="front-matter-prose"><i><b>To the Christian Reader,</b></i></p>'
    res2 = _apply_premium_salutations(html2)
    assert res2 == '<p class="prefatory-salutation">To the Christian Reader,</p>'

    # 3. Plain tag version
    html3 = '<p>To the Reader.</p>'
    res3 = _apply_premium_salutations(html3)
    assert res3 == '<p class="prefatory-salutation">To the Reader.</p>'

    # 4. Standard sentence containing the words (Should be skipped!)
    html4 = '<p class="front-matter-prose">The Christian Reader will immediately notice the depth of Owen\'s thought.</p>'
    res4 = _apply_premium_salutations(html4)
    assert res4 == html4

    # 5. H3 heading tag (like those produced in front-matter prose mode)
    html5 = '<h3 class="secondary">Christian Reader,</h3>'
    res5 = _apply_premium_salutations(html5)
    assert res5 == '<p class="prefatory-salutation">Christian Reader,</p>'


def test_apply_premium_chapter_endings():
    """Verify that chapter ending statements (like 'END OF PART 2') are isolated and styled, while not touching other text."""
    from render import _apply_premium_chapter_endings

    # 1. Standalone ending in bold
    html1 = '<p><b>END OF PART 2.</b></p>'
    res1 = _apply_premium_chapter_endings(html1)
    assert res1 == '<p class="chapter-end-marker"><b>END OF PART 2.</b></p>'

    # 2. Trailing ending in paragraph
    html2 = '<p>This concludes the meditations. **THE END.**</p>'
    res2 = _apply_premium_chapter_endings(html2)
    assert '<p class="chapter-end-marker"><b>THE END.</b></p>' in res2
    assert '<p>This concludes the meditations.</p>' in res2


def test_ocr_bold_and_paragraph_healing():
    """Verify that false OCR bolds are stripped, structural ones are kept, and false paragraph splits at abbreviations are healed."""
    from extract import clean_text, reconstruct_paragraphs

    # Test 1: Strip false OCR bolds in middle of sentences but preserve structural ones
    raw_text = (
        "We have **seen** that **Dr.** Owen writes about the **holy** spirit.\n\n"
        "**1.** He is active. **Ans.** Indeed he is.\n\n"
        "**[2.]** In the church.\n\n"
        "**Secondly.** For the elect."
    )
    cleaned = clean_text(raw_text)
    # False bolds must be stripped
    assert "We have seen" in cleaned
    assert "Dr. Owen writes" in cleaned
    assert "the holy spirit" in cleaned
    # Structural ones must be kept
    assert "**1.**" in cleaned
    assert "**Ans.**" in cleaned
    assert "**[2.]**" in cleaned
    assert "**Secondly.**" in cleaned

    # Test 2: Heals false paragraph breaks at abbreviations and initials
    raw_lines = (
        "This is discussed by Aug.\n\n"
        "In his book on trinity.\n\n"
        "We also read in Rom.\n\n"
        "VIII. 1. that there is no condemnation.\n\n"
        "This was confirmed by St.\n\n"
        "Augustine in his letters.\n\n"
        "According to J.\n\n"
        "Owen, this is true."
    )
    joined = "\n".join(reconstruct_paragraphs(clean_text(raw_lines)))
    assert "Aug. In his book" in joined
    assert "Rom. VIII. 1." in joined
    assert "St. Augustine" in joined
    assert "J. Owen," in joined


def test_simon_magus_casing_normalization():
    """Verify that Simon Magus, Simon M. Agus, Simon M'Agus, and SIMON MAGUS are correctly normalized."""
    from shared import _repair_owen_ocr_errors
    
    # Test case 1: Simon M Agus (case variations)
    assert _repair_owen_ocr_errors("Simon M Agus") == "Simon Magus"
    assert _repair_owen_ocr_errors("Simon M. Agus") == "Simon Magus"
    assert _repair_owen_ocr_errors("Simon M'Agus") == "Simon Magus"
    assert _repair_owen_ocr_errors("Simon M’Agus") == "Simon Magus"
    assert _repair_owen_ocr_errors("SIMON M AGUS") == "Simon Magus"
    assert _repair_owen_ocr_errors("simon m agus") == "simon magus"
    
    # Test case 2: SIMON MAGUS all-caps
    assert _repair_owen_ocr_errors("SIMON MAGUS") == "Simon Magus"
    
    # Test case 3: Simon Magus normal Title Case unchanged
    assert _repair_owen_ocr_errors("Simon Magus") == "Simon Magus"


def test_bracket_spacing_cleanup():
    """Verify that spaces inside brackets for single word/digit tokens are cleaned up corpus-wide."""
    from shared import _repair_owen_ocr_errors
    
    assert _repair_owen_ocr_errors("Some text [ a] reference.") == "Some text [a] reference."
    assert _repair_owen_ocr_errors("Some text [ a ] reference.") == "Some text [a] reference."
    assert _repair_owen_ocr_errors("Some text [a ] reference.") == "Some text [a] reference."
    assert _repair_owen_ocr_errors("Some text [ft10 ] reference.") == "Some text [ft10] reference."
    assert _repair_owen_ocr_errors("Some text [ f12] reference.") == "Some text [f12] reference."
    assert _repair_owen_ocr_errors("Some text [β ] reference.") == "Some text [β] reference."
    assert _repair_owen_ocr_errors("Some text [ 1 ] reference.") == "Some text [1] reference."
    
    # Multi-word/longer contents within brackets should remain untouched
    assert _repair_owen_ocr_errors("Some text [See page 638.] reference.") == "Some text [See page 638.] reference."
    assert _repair_owen_ocr_errors("Some text [Translated: to cherish] reference.") == "Some text [Translated: to cherish] reference."


def test_latin_dedication_translation_matching():
    """Verify that the Latin dedicatory inscription is matched and translated under the Volume 12 config, and is not double-replaced."""
    from render import apply_inline_translations
    
    text = 'whose inscription is, "Amplissimo clarissimoque viro Georgio Blandratae Stephani invictissimi regis Poloniae, etc., archiatro et conciliario intimo, domino, ae patrono suo perpetua observantia colendo; et subscribitur, Tibi in Domino Jesu deditissimus cliens tuus F. S."'
    repaired = apply_inline_translations(text)
    
    assert "[Translated:" in repaired
    assert "George Blandrata, physician-in-chief and intimate counselor of Stephen" in repaired
    
    # Run a second time to ensure no double translation
    repaired_twice = apply_inline_translations(repaired)
    assert repaired_twice == repaired
    assert repaired_twice.count("[Translated:") == 1


def test_latin_word_tagging():
    """Verify that runs of Latin text are tagged with lang="la" spans, while English words are not."""
    from shared import tag_latin_words
    
    # Simple runs of 2+ Latin words
    assert tag_latin_words("This is a simple sentence.") == "This is a simple sentence."
    assert tag_latin_words("He said, sola fide.") == 'He said, <span lang="la" xml:lang="la">sola fide</span>.'
    assert tag_latin_words("Wait, simul iustus et peccator is latin.") == 'Wait, <span lang="la" xml:lang="la">simul iustus et peccator</span> is latin.'
    
    # A single distinctly Latin word that is not in English dictionary and matches Latin suffix
    # (Since our rule requires latin_word_count >= 2, single Latin words are NOT tagged to avoid false positives,
    # which is the safest approach.)
    assert tag_latin_words("An alumnus of the school.") == "An alumnus of the school."
    
    # Verify that false positives are avoided
    assert tag_latin_words("The book is a classic, in a ridiculous style.") == "The book is a classic, in a ridiculous style."
    assert tag_latin_words("He was an intimate counselor to the king.") == "He was an intimate counselor to the king."
    assert tag_latin_words("Here also we find some curious, intricate opinions.") == "Here also we find some curious, intricate opinions."
    assert tag_latin_words("Servetus at Geneva was a ridiculous impostor, Beza said.") == "Servetus at Geneva was a ridiculous impostor, Beza said."
    assert tag_latin_words("who, as Smalcius and others had done, argued for this.") == "who, as Smalcius and others had done, argued for this."
    assert tag_latin_words("They took much labor. Thus, the work was finished.") == "They took much labor. Thus, the work was finished."
    
    # HTML tag protection
    assert tag_latin_words("Look at <a href=\"#\">sola fide</a> in context.") == 'Look at <a href=\"#\"><span lang="la" xml:lang="la">sola fide</span></a> in context.'


def test_cardo_gentium_style_overrides():
    """Verify that Latin font stack dynamically switches to Gentium Plus when Cardo is the body font."""
    from shared import generate_font_styles
    
    # Case 1: Primary font is NOT Cardo
    styles_standard = generate_font_styles("Arno Pro", {})
    assert '"Cardo", "Gentium Plus", serif' in styles_standard
    
    # Case 2: Primary font IS Cardo (either case-insensitive or exact)
    styles_cardo = generate_font_styles("Cardo", {})
    assert '"Gentium Plus", serif' in styles_cardo
    assert '"Cardo", "Gentium Plus", serif' not in styles_cardo


def test_citation_abbrev_split_false_positive():
    """Verify that citation abbreviations followed by spaces and numbers (e.g. Haer. 51.)
    do not trigger false-positive paragraph splits in _split_rendered_inline_structural_html."""
    from render import _split_rendered_inline_structural_html
    text_html = (
        'even in the entrance of the Gospel being confounded by John, as is affirmed by '
        '<span lang="la" xml:lang="la">Epiphanius, Haer</span>. 51. '
        '"Hieronymus de Seriptoribus Ecclesiasticis de Johanne." The same abomination'
    )
    result = _split_rendered_inline_structural_html(text_html)
    assert len(result) == 1, f"Should not split paragraph on Haer. 51.: {result}"


def test_nav_xhtml_double_wrap_prevention():
    """Verify that generate_nav_xhtml generates a clean navigation document without duplicate
    head or body double-wrap markers."""
    from render import generate_nav_xhtml
    toc_entries = [(1, "Contents", "contents.xhtml"), (2, "Chapter 1", "ch001.xhtml")]
    nav_html = generate_nav_xhtml(toc_entries, "Volume 12")
    # Verify it has exactly one head, body, and html set, and no nested duplicate headers
    assert nav_html.count("<head>") == 1
    assert nav_html.count("<body>") == 1
    assert nav_html.count("Table of Contents") == 3  # One in title, one in h2, one in landmarks guide


def test_latin_ocr_repairs():
    """Verify that centralized Latin OCR corrections are correctly applied."""
    from shared import _repair_owen_ocr_errors
    
    # Check 'sod' -> 'sed'
    text_sod = "sod credere illum oportet"
    repaired_sod = _repair_owen_ocr_errors(text_sod)
    assert repaired_sod.startswith("sed ")
    
    # Check 'Cicerco' -> 'Cicero'
    text_cic = "ut ait Cicerco in"
    repaired_cic = _repair_owen_ocr_errors(text_cic)
    assert "Cicero" in repaired_cic
    
    # Check 'remain' -> 'veniam' restricted to Latin phrase
    text_remain_latin = "delictorum nostrorum remain"
    repaired_remain = _repair_owen_ocr_errors(text_remain_latin)
    assert repaired_remain == "delictorum nostrorum veniam"
    
    # Make sure English 'remain' is not corrupted
    text_remain_eng = "we remain in the faith"
    repaired_remain_eng = _repair_owen_ocr_errors(text_remain_eng)
    assert repaired_remain_eng == "we remain in the faith"


def test_latin_inline_translations():
    """Verify that inline translations are correctly injected without corrupting language span tags."""
    from render import apply_inline_translations
    
    body_html = '<p>whose inscription is, <span lang="la" xml:lang="la">Amplissimo clarissimoque viro Georgio Blandratae Stephani invictissimi regis Poloniae, etc., archiatro et conciliario intimo, domino, ae patrono suo perpetua observantia colendo; et subscribitur, Tibi in Domino Jesu deditissimus cliens tuus F. S.</span>.</p>'
    
    repaired = apply_inline_translations(body_html)
    assert '[Translated: ' in repaired
    assert '“To the most distinguished and renowned George Blandrata' in repaired
    assert '</span>.' in repaired







