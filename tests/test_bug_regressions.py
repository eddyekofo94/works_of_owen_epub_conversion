import json
import os
import re
import zipfile
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.audit_epub import Audit
from scripts.audit_text_integrity import run_audit
from converter import clean_text, force_polyglot_mapping, get_pages_text, reconstruct_paragraphs
from render import apply_scholastic_anchor_protocol, markdown_to_html
from volumes.v1.convert import OVERRIDES as V1_OVERRIDES


BASE_DIR = Path(__file__).parent.parent
BASELINE_PATH = BASE_DIR / "qa" / "bug_regression_baselines.json"


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
    assert '<p class="list-item"><b>(1.)</b> His incarnation' not in html
    assert '<h4 class="roman-subheading"><b>II.</b> Christ values his saints' in html


def test_bracketed_and_parenthesized_markers_split_and_bold_cleanly():
    html, _, _ = markdown_to_html(
        "**(1.)** For their sanctification;\n\n"
        "**(2.)** For their consolation: to which two all the particular acts of "
        "purging, teaching, anointing, and the rest that are ascribed to him, may "
        "be referred. So there be two ways whereby we may grieve him: — "
        "**[1].** In respect of sanctification;\n\n"
        "**[2.]** In respect of consolation: —"
    )

    assert '<p class="list-item"><b>(2.)</b> For their consolation:' in html
    assert '<p class="list-item"><b>[1].</b> In respect of sanctification;</p>' in html
    assert '<p class="list-item"><b>[2.]</b> In respect of consolation: —</p>' in html
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
    assert '<p class="list-item"><b>2dly.</b> Our holiness' in html
    assert '<b>[1st.]</b> It is the glory of the Father' in html
    assert '<b>[2dly.]</b> The Son is gloried thereby' in html


def test_scholastic_quoted_objection_opener_moves_inside_blockquote():
    html, _, _ = markdown_to_html(
        'Objection 1. But some may say, "Alas! how shall I hold communion with '
        'the Father in love? I know not at all whether he loves me or no;\n\n'
        '[[BLOCKQUOTE]] and shall I venture to cast myself upon it? How if I '
        'should not be accepted?"'
    )

    assert '<p class="list-item"><b>Objection 1.</b> But some may say,</p>' in html
    assert (
        '<blockquote epub:type="z3998:quotation"><p>&quot;Alas! how shall I hold '
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
        '<blockquote epub:type="z3998:quotation"><p>"Behold my servant, whom I uphold; '
        'mine elect, in whom my soul delighteth;" ( Isaiah 42:1;)</p></blockquote>'
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

    assert '<p class="list-item"><b>I. 1.</b> What he did preparatory' in html


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
    assert any("2026" in html for html in title_pages)

    part_2_title = next(
        html for html in files.values()
        if "<title>Part 2 - Meditations and Discourses Concerning The Glory of Christ</title>" in html
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
        if "<title>Chapter 1 - Meditations and Discourses Concerning the Glory of Christ</title>" in html
    )
    assert '<section class="treatise-title-page"' not in part_2_chapter
    assert "Application of the Foregoing Meditations" in part_2_chapter
    assert "That which remains is, to make some application" in part_2_chapter

    greater_chapter = next(
        html for html in files.values()
        if "<title>Chapter 1 - of the Scripture.</title>" in html
    )
    assert '<section class="treatise-title-page"' not in greater_chapter
    assert 'class="catechism-item"' in greater_chapter
    assert "<b>Ques. 1.</b> What is Christian religion?" in greater_chapter
    assert "<b>Ans.</b> The only way" in greater_chapter

    christologia_title = next(
        html for html in files.values()
        if "<title>Christologia - a Declaration of the Glorious Mystery</title>" in html
    )
    assert '<p class="greek-title"><span lang="el" xml:lang="el">ΧΡΙΣΤΟΛΟΓΙΑ:</span></p>' in christologia_title
    assert '<p class="title-line title-line-major">CHRISTOLOGIA</p>' in christologia_title
    assert '<p class="title-connector">OR</p>' in christologia_title
    assert '<p class="title-connector">OF</p>' in christologia_title
    assert '<p class="title-connector">WITH</p>' in christologia_title
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
    assert '<p class="contents-frontmatter-line">ORIGINAL PREFACE</p>' in contents
    assert 'class="ContentsItem"' not in contents

    chapter_1 = next(html for html in files.values() if "<title>Chapter 1 - Peter's Confession</title>" in html)
    assert "Peter's Confession; Matthew 16:16" in chapter_1
    assert "PETER'S CONFESSION; MATTHEW 16:16" not in chapter_1

    greater_chapter_15 = next(
        html for html in files.values()
        if "<title>Chapter 15 - of the Persons to Whom the Benefits of Christ's Offices Do Belong.</title>" in html
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
    assert re.search(r"\.front-matter-heading\s*\{[^}]*border-bottom:\s*1px solid #777;", css, re.S)
    assert ".contents-page" in css
    assert ".volume-title-page .title-author-main" in css
    assert "EPUB/Fonts/Baskervville-Regular.ttf" in names
    assert "EPUB/Fonts/Baskervville-Bold.ttf" in names
    assert "EPUB/Fonts/Baskervville-Italic.ttf" in names
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
        if "<title>Chapter 1 - of the Scripture.</title>" in html
    )

    assert ".v1-catechism-pair" in css
    assert "front-matter-prose" not in lesser
    assert '<div class="v1-catechism-pair">\n<p class="catechism-item"><b>Ques.</b> Whence is all truth' in lesser
    assert '<p class="catechism-item"><b>Ans.</b> From the holy Scripture' in lesser
    assert '<p class="catechism-item"><b>A.</b> An eternal, infinite' in lesser
    assert '<p class="catechism-item"><b>Q. 2.</b> What is repentance?</p>' in lesser
    assert '<p class="catechism-item"><b>A.</b> A forsaking of all sin, with godly sorrow for what we have committed. — Chapter 20.</p>' in lesser
    assert '<p>- Chapter 20.</p>' not in lesser
    assert '<p>- Chapter 21.</p>' not in lesser
    assert "know.?" not in lesser

    assert '<div class="v1-catechism-pair">\n<p class="catechism-item"><b>Ques. 1.</b> What is Christian religion?</p>' in greater_chapter_1
    assert '<p class="catechism-item"><b>A.</b> From the holy' in greater_chapter_1

    combined = "\n".join(files.values())
    false_answer_samples = [
        "A prefatory note has commonly been given to the different treatises.",
        "A complete index will be given in the last volume",
        "A glorious representation hereof",
    ]
    for sample in false_answer_samples:
        assert sample in combined
        assert f'<p class="catechism-item"><b>A.</b> {sample[2:]}' not in combined
        assert f'<p class="catechism-item">A. {sample[2:]}' not in combined


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
        if "<title>Chapter 1 - Peter's Confession</title>" in html
    )
    latin_quote_chapter = next(
        html for html in files.values()
        if "Universam significabat ecclesiam" in html
    )
    power_chapter = next(
        html for html in files.values()
        if "<title>Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ</title>" in html
    )
    honor_chapter = next(
        html for html in files.values()
        if "<title>Chapter 9 - Honor Due to the Person of Christ</title>" in html
    )
    conformity_chapter = next(
        html for html in files.values()
        if "<title>Chapter 15 - Conformity Unto Christ</title>" in html
    )
    combined = "\n".join(files.values())

    assert '<blockquote epub:type="z3998:quotation"><p>"The divines of the Puritan school' in general_preface
    assert "Universam significabat ecclesiam" in latin_quote_chapter
    assert '<blockquote epub:type="z3998:quotation"><p>"And Simon Peter answered' in peters_confession
    quote_blocks = re.findall(r"<blockquote[^>]*>.*?</blockquote>", peters_confession, re.S)
    assert not any("Baronius" in block for block in quote_blocks)
    assert '<p class="list-item"><b>1.</b> The faith of Peter in this confession' in peters_confession
    assert not any("1. The faith of Peter" in block for block in quote_blocks)
    assert re.search(r'<blockquote[^>]*><p>"Thou, Lord,.*?a vesture shalt thou fold them up.*?not fail\."</p></blockquote>', power_chapter, re.S)
    assert re.search(r'<blockquote[^>]*><p>"Unto him that loved us,.*?Amen\." Revelation 1:5, 6\.</p></blockquote>', honor_chapter, re.S)
    assert '<p>This, therefore, is another season that calls for this duty.</p>' in honor_chapter
    assert re.search(r'<blockquote[^>]*><p>"If so be that we suffer with him,.*?Romans 8:17, 18\.</p></blockquote>', conformity_chapter, re.S)
    assert re.search(r"<blockquote[^>]*><p\s*/>", combined) is None
    assert re.search(r"<blockquote[^>]*><p>\s*</p>", combined) is None


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
    assert re.search(r"\.roman-subheading\s*\{[^}]*text-align:\s*left;", css, re.S)
    assert re.search(r"\.roman-subheading\s*\{[^}]*font-weight:\s*normal;", css, re.S)
    assert re.search(r"\.roman-list-item\s*\{[^}]*text-align:\s*left;", css, re.S)
    assert re.search(r"\.roman-list-item b\s*\{[^}]*display:\s*inline;", css, re.S)

    chapter_9 = next(
        html for html in files.values()
        if "<title>Chapter 9 - Honor Due to the Person of Christ</title>" in html
    )
    assert '<p class="roman-list-item"><b>I.</b> Honor.</p>' in chapter_9
    assert '<p class="roman-list-item"><b>II.</b> Obedience.</p>' in chapter_9
    assert '<p class="roman-list-item"><b>III.</b> Conformity.</p>' in chapter_9
    assert (
        '<p class="roman-list-item"><b>IV.</b> The use we make of him, for the attaining '
        'and receiving of all Gospel privileges'
    ) in chapter_9
    assert '<h4 class="roman-subheading"><b>I.</b> Honor.</h4>' not in chapter_9
    assert '<b>I.</b> The person of Christ is the object of divine honor and worship.' in chapter_9

    chapter_7 = next(
        html for html in files.values()
        if "<title>Chapter 7 - Power and Efficacy Communicated Unto the Office of Christ</title>" in html
    )
    assert '<b>I.</b> The first of these is, that he should have a nature provided for him,' in chapter_7


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

    checks = {
        "EPUB packaging errors": (result["error_count"], budget["max_error_count"], result["errors"][:5]),
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
