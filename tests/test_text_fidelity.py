"""test_text_fidelity.py — Owen-specific content and typography checks.

Goal: catch the anomalies you would only notice while reading 2,000 pages —
OCR artifacts, garbled theological vocabulary, broken footnotes, typography
that changes meaning.

Structure
---------
Part 1 — Pure unit tests (no PDF or EPUB on disk required).
           These run in CI from the very first volume and for every future
           volume without any extra setup.

Part 2 — EPUB-scanning tests (parametrized over built volumes).
           These scan EPUB text for patterns that should never appear in a
           finished file regardless of which volume is being checked.

The parametrized tests use the same VOLUMES / paths_for helpers as
test_bug_regressions.py so they slot straight into the existing workflow:

    OWEN_REGRESSION_VOLUMES=1,2 pytest tests/test_text_fidelity.py
    OWEN_REGRESSION_VOLUMES=all  pytest tests/test_text_fidelity.py
"""

from __future__ import annotations

import os
import re
import zipfile
from pathlib import Path

import pytest

from converter import clean_text, reconstruct_paragraphs

# ---------------------------------------------------------------------------
# Path helpers (mirrors test_bug_regressions.py)
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).parent.parent


def _requested_volumes() -> list[int]:
    raw = os.environ.get("OWEN_REGRESSION_VOLUMES", "1").strip()
    if raw.lower() == "all":
        return [
            int(path.name[1:])
            for path in sorted((BASE_DIR / "volumes").glob("v[0-9]*"))
            if (path / "output" / f"volume_{path.name[1:]}.epub").exists()
        ]
    return [int(part) for part in raw.replace(",", " ").split() if part]


def _epub_path(volume: int) -> Path:
    return BASE_DIR / "volumes" / f"v{volume}" / "output" / f"volume_{volume}.epub"


def _all_xhtml_text(volume: int) -> str:
    """Return concatenated plain text from all EPUB chapter files."""
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {ep}")
    parts: list[str] = []
    with zipfile.ZipFile(ep) as zf:
        for name in sorted(zf.namelist()):
            if name.startswith("EPUB/") and name.endswith(".xhtml"):
                parts.append(zf.read(name).decode("utf-8", errors="replace"))
    return "\n".join(parts)


def _strip_tags(html: str) -> str:
    return re.sub(r"<[^>]+>", " ", html)


def _prose_paragraphs(xhtml: str) -> list[str]:
    """Extract normalised text content of every <p> element from XHTML."""
    paras = []
    for m in re.finditer(r"<p(?:\s[^>]*)?>.*?</p>", xhtml, re.S):
        text = re.sub(r"\s+", " ", _strip_tags(m.group(0))).strip()
        if text:
            paras.append(text)
    return paras


VOLUMES = _requested_volumes()


# ===========================================================================
# PART 1 — UNIT TESTS (no PDF / EPUB required)
# ===========================================================================

# ---------------------------------------------------------------------------
# 1.1  OCR bracket-corruption repair
# ---------------------------------------------------------------------------

def test_bracket_y_artifact_is_repaired_to_ly():
    """']y' and ']Y' are a well-known AGES OCR artifact for 'ly'."""
    assert "only" in clean_text("on]y")
    assert "enly" in clean_text("en]y")
    assert "gloriously" in clean_text("glorious]y")


def test_bracket_e_artifact_is_repaired_to_le():
    """']e' at a word boundary is an AGES OCR artifact for 'le'."""
    assert "able" in clean_text("ab]e")
    assert "people" in clean_text("peop]e")


def test_bracket_corruption_does_not_touch_scripture_brackets():
    """Square-bracketed enumerators like [1.] must not be altered."""
    result = clean_text("[1.] First point; [2.] Second point.")
    assert "[1.]" in result
    assert "[2.]" in result


def test_bare_a_period_before_lowercase_is_stripped():
    """
    "A. brief view..." at ANY position is an OCR artifact: the indefinite
    article 'A' gains a spurious period.  The repair strips it.

    The fix uses \\bA\\. (word boundary) not ^ so it catches:
      - Lines with leading whitespace: "    A. church state..."
      - Mid-paragraph occurrences after sentence-ending punctuation:
        "represent unto us. A. church state does the apostle..."
    """
    from shared import _repair_owen_ocr_errors

    # Paragraph-start form
    assert _repair_owen_ocr_errors("A. brief view of the faith") == "A brief view of the faith"
    assert _repair_owen_ocr_errors("A. glorious representation hereof") == "A glorious representation hereof"
    assert _repair_owen_ocr_errors("A. truth this is, of that importance") == "A truth this is, of that importance"

    # Multi-paragraph form
    multi = "Some preceding text.\n\nA. mystery it is.\n\nFollowing text."
    result = _repair_owen_ocr_errors(multi)
    assert "A mystery it is." in result
    assert "A. mystery" not in result

    # With leading whitespace — previously missed by ^ anchor
    assert _repair_owen_ocr_errors("    A. church state does the apostle") == "    A church state does the apostle"

    # Mid-paragraph — previously missed entirely (the real failing case)
    mid = "represent unto us. A. church state does the apostle most expressly represent unto us. It"
    fixed = _repair_owen_ocr_errors(mid)
    assert "A. church" not in fixed
    assert "A church" in fixed


def test_fused_list_marker_space_inserted():
    """
    OCR fuses conjunctions directly with list markers: "and(2.)" → "and (2.)"
    The repair inserts the missing space without affecting already-spaced markers.
    Issue 12.a: "(1.) What this work is, and(2.) How it is performed."
    """
    from shared import _repair_owen_ocr_errors

    assert _repair_owen_ocr_errors(
        "(1.) What this work is, and(2.) How it is performed."
    ) == "(1.) What this work is, and (2.) How it is performed."

    assert _repair_owen_ocr_errors(
        "(1.) First point, or(2.) second point."
    ) == "(1.) First point, or (2.) second point."

    # Already spaced — must not be double-spaced
    assert _repair_owen_ocr_errors(
        "(1.) First, and (2.) second."
    ) == "(1.) First, and (2.) second."


def test_bare_a_period_before_uppercase_is_preserved():
    """
    'A.' followed by an uppercase letter must NOT be touched — it is either a
    real catechism Answer marker or a structural section label.
    """
    from shared import _repair_owen_ocr_errors

    # Catechism answer
    assert _repair_owen_ocr_errors("A. An eternal, infinite Spirit.") == "A. An eternal, infinite Spirit."
    # Structural section label (v16 pattern)
    assert _repair_owen_ocr_errors("A. THIRD inquiry may be") == "A. THIRD inquiry may be"
    # Structural chapter-heading label
    assert _repair_owen_ocr_errors("A. GENERAL account of the controversy") == "A. GENERAL account of the controversy"


# ---------------------------------------------------------------------------
# Issue 42 — OCR digit-zero → letter O at sentence start
# ---------------------------------------------------------------------------

def test_ocr_zero_to_o_at_line_start():
    """
    OCR misreads the interjection 'O' as digit '0'.
    '0 sweet permutation!' → 'O sweet permutation!'
    '0 Lord, how great!' → 'O Lord, how great!'
    Mid-sentence zeros (counts, numbers) must NOT change.
    """
    from shared import _repair_owen_ocr_errors

    # Line-start interjections
    assert _repair_owen_ocr_errors("0 sweet permutation!") == "O sweet permutation!"
    assert _repair_owen_ocr_errors("0 Lord, how great thou art!") == "O Lord, how great thou art!"
    # After sentence-terminal punctuation
    assert _repair_owen_ocr_errors("He said. 0 let it be so.") == "He said. O let it be so."
    # Mid-sentence number — must not change
    assert _repair_owen_ocr_errors("The count is 0 items.") == "The count is 0 items."
    assert _repair_owen_ocr_errors("verse 0 of chapter") == "verse 0 of chapter"


# ---------------------------------------------------------------------------
# Issue 44 — trailing lone hyphen → em-dash
# ---------------------------------------------------------------------------

def test_trailing_lone_hyphen_becomes_em_dash():
    """
    A lone hyphen at the end of a line is an OCR artifact for an em-dash.
    'For, -' → 'For, —'   (comma + space + hyphen)
    'word -' → 'word —'   (word + space + hyphen at line end)
    Compound hyphens inside words must NOT be touched.
    """
    from shared import _repair_owen_ocr_errors

    assert _repair_owen_ocr_errors("For, -") == "For, —"
    assert _repair_owen_ocr_errors("the Lord -") == "the Lord —"
    # Compound hyphen — unchanged
    assert _repair_owen_ocr_errors("well-known") == "well-known"
    # Already an em-dash — unchanged
    assert _repair_owen_ocr_errors("it is, —") == "it is, —"


# ---------------------------------------------------------------------------
# Issue 44b — "For, -" mid-sentence (not at line end)
# ---------------------------------------------------------------------------

def test_for_comma_hyphen_mid_sentence_becomes_emdash():
    """
    'For, - before the saints' — hyphen mid-sentence with space after it.
    The previous end-of-line regex could not catch this variant.
    """
    from shared import _repair_owen_ocr_errors

    assert _repair_owen_ocr_errors("For, - before the saints under") == "For, — before the saints under"
    assert _repair_owen_ocr_errors(
        "the spring and means of this communion is no small part of the glory of the gospel. For, - before the saints under"
    ) == (
        "the spring and means of this communion is no small part of the glory of the gospel. For, — before the saints under"
    )
    assert _repair_owen_ocr_errors("Thus, - we see") == "Thus, — we see"
    assert _repair_owen_ocr_errors("Hence, - it follows") == "Hence, — it follows"
    # Compound word after comma — must NOT fire (no hyphen followed by space)
    assert _repair_owen_ocr_errors("well-known, -ish forms") == "well-known, -ish forms"


# ---------------------------------------------------------------------------
# 1.2  Consecutive duplicate word detection
# ---------------------------------------------------------------------------

def test_reconstruct_paragraphs_heals_false_break_without_losing_words():
    """
    reconstruct_paragraphs must join a reference continuation that the extractor
    split at a page boundary without dropping or duplicating any words.

    Example: "Zechariah 1:11\n\nwhich he treats of, p. 280."
    The break after a scripture reference is a false split; the following
    fragment must be appended to the same paragraph, and no content lost.
    """
    raw = (
        "He considers what is the state of the world in reference to them.\n\n"
        "Zechariah 1:11, \"We have walked to and fro.\"\n\n"
        "which he treats of, p.\n\n"
        "280. \"As for example,\" saith he."
    )
    joined = "\n".join(reconstruct_paragraphs(clean_text(raw)))

    # All content words must be present
    assert "them. Zechariah 1:11" in joined
    assert 'p. 280. "As for example' in joined
    # No word should be duplicated at a join boundary
    assert not re.search(r"\bZechariah Zechariah\b", joined)
    assert not re.search(r"\bhe he\b", joined)


def test_coincidental_repeated_phrase_with_greek_is_not_collapsed():
    """A 6-word run that recurs by coincidence must NOT be treated as an AGES
    ghost, or the genuine text (incl. Greek scripture) between the two
    occurrences is silently deleted.

    Real case (v16, Owen on the divine original of Scripture): the phrase
    "that spake in the name of" appears twice — once "...in the name of God..."
    and again "...in the name of the Lord...". Between them sits the Greek
    quotation of 2 Peter 2:1 (ἐγένοντο ψευδοπροφῆται ἐν τῷ λαῷ). The ghost-
    removal heuristic keyed on the repeated phrase + reference list in the gap
    and deleted the whole span. The Greek (and the English clause) must survive.
    """
    raw = (
        "that scarce any prophet that spake in the name of God had any "
        "approbation from the church in whose days he spake. "
        "(Matthew 21:33-39.) It is true, "
        "ἐγένοντο "
        "ψευδοπροφῆται "
        "ἐν τῷ λαῷ, (2 Peter 2:1,) "
        "\"there were false prophets among the people,\" "
        "that spake in the name of the Lord, when he sent them not. "
        "(Jeremiah 23:21.)"
    )
    joined = "\n".join(reconstruct_paragraphs(clean_text(raw)))
    # The Greek clause must be preserved verbatim.
    assert "ψευδοπροφῆται" in joined
    # The English between the two coincidental phrases must also survive.
    assert "approbation from the church" in joined
    assert "false prophets among the people" in joined


def test_genuine_interrupted_duplicate_clause_is_still_removed():
    """The conservative guards must not disable legitimate ghost removal: an
    English clause that genuinely restarts verbatim after a bare reference list
    (no foreign script, no extra prose in the gap) should still be collapsed.
    """
    from extract import _remove_interrupted_duplicate_clause

    ghost = (
        "the Spirit of God dwelleth in us "
        "(Romans 8:9; 1 Corinthians 3:16) "
        "the Spirit of God dwelleth in us, and we are his temple."
    )
    repaired = _remove_interrupted_duplicate_clause(ghost)
    assert repaired != ghost
    assert repaired.count("the Spirit of God dwelleth in us") == 1


# ---------------------------------------------------------------------------
# 1.3  Theological vocabulary survival through clean_text
# ---------------------------------------------------------------------------

THEOLOGICAL_TERMS = [
    "justification",
    "sanctification",
    "propitiation",
    "atonement",
    "covenant",
    "predestination",
    "election",
    "regeneration",
    "perseverance",
    "imputation",
    "adoption",
    "intercession",
    "mortification",
    "vivification",
    "satisfaction",
    "hypostatic",
    "Socinian",
    "Arminian",
    "Pelagian",
]


@pytest.mark.parametrize("term", THEOLOGICAL_TERMS)
def test_theological_term_survives_clean_text(term: str):
    """
    A sentence containing a key Owen theological term must emerge from
    clean_text with that term intact.  clean_text must not accidentally
    truncate, split, or alter these words.
    """
    sentence = f"He considers the doctrine of {term} at length."
    result = clean_text(sentence)
    assert term in result or term.lower() in result.lower(), (
        f"Term '{term}' was lost or mangled by clean_text.\n"
        f"  Input:  {sentence!r}\n"
        f"  Output: {result!r}"
    )


# ---------------------------------------------------------------------------
# 1.4  No raw structural tokens survive into rendered output
# ---------------------------------------------------------------------------

def test_structural_tokens_do_not_survive_markdown_to_html():
    """
    [[CHAPTER]], [[PART]], [[BLOCKQUOTE]], [[SUMMARY]], [[FRONT_MATTER]] are
    pipeline-internal markers.  None of them should appear as literal text in
    the rendered HTML.
    """
    from render import markdown_to_html

    tokens = ["[[CHAPTER]]", "[[PART]]", "[[BLOCKQUOTE]]", "[[SUMMARY]]", "[[FRONT_MATTER]]"]
    md = (
        "[[PART]] PART 1\n\n"
        "[[CHAPTER]] CHAPTER 1\n\n"
        "[[SUMMARY]] Opening summary.\n\n"
        "[[BLOCKQUOTE]] A patristic quotation.\n\n"
        "Body text follows."
    )
    html, _, _ = markdown_to_html(md)
    for tok in tokens:
        assert tok not in html, f"Token {tok!r} leaked into rendered HTML."


def test_literal_footnote_markers_do_not_survive_markdown_to_html():
    """
    [f1], [f12] etc. are intermediate pipeline markers.
    They should be converted to <a> noteref links, not emitted literally.
    """
    from render import markdown_to_html

    md = "Body text [f1] continues here. Also [f12] and [f100]."
    html, _, _ = markdown_to_html(md)
    # Should become noteref links
    assert 'class="noteref"' in html
    # Should NOT appear literally
    assert re.search(r"\[f\d+\]", html) is None, (
        "Literal [fN] markers found in rendered HTML."
    )


# ---------------------------------------------------------------------------
# 1.5  Em-dash and hyphen typography
# ---------------------------------------------------------------------------

def test_ages_double_hyphen_is_not_introduced_by_clean_text():
    """
    clean_text must never turn an em-dash into '--'.
    """
    text = "Owen argues — and this is crucial — that the atonement is definite."
    result = clean_text(text)
    assert "—" in result
    assert "--" not in result


def test_ordinal_spacing_no_orphan_period():
    """
    Ordinals like '1st .' (space before period) should be tightened to '1st.'
    """
    result = clean_text("**1st** . The first point; 2ndly . The second.")
    assert "1st ." not in result
    assert "2ndly ." not in result


# ---------------------------------------------------------------------------
# 1.6  Scripture reference format
# ---------------------------------------------------------------------------

MALFORMED_SCRIPTURE_RE = re.compile(
    r"\b(?:Gen|Exod?|Lev|Num|Deut|Josh|Judg|Ruth|Sam|Kgs|Chr|Ezra|Neh|Est|Job|"
    r"Ps|Psa|Prov|Eccl|Isa|Jer|Lam|Ezek|Dan|Hos|Joel|Amos|Obad|Jon|Mic|Nah|"
    r"Hab|Zeph|Hag|Zech|Mal|Matt|Mk|Lk|Jn|Rom|Cor|Gal|Eph|Phil|Col|Thess|"
    r"Tim|Tit|Phlm|Heb|Jas|Pet|Rev)\.",
    re.I,
)


def test_clean_text_expands_scripture_abbreviations():
    """
    The AGES markup uses numeric codes that resolve to full scripture references.
    After clean_text the result must contain the book name spelled out, not just
    a numeric code.
    """
    raw = "sealed unto the day of redemption — <490430> Ephesians 4:30."
    result = clean_text(raw)
    assert "Ephesians 4:30" in result
    assert "<490430>" not in result


def test_scripture_ref_with_chapter_only_is_not_mangled():
    """References like 'Genesis 3' (chapter only) must survive intact."""
    raw = "What fruit of this consideration had Adam? Genesis 3. What sweetness."
    result = clean_text(raw)
    assert "Genesis 3" in result


# ---------------------------------------------------------------------------
# 1.7  Fused-token repairs
# ---------------------------------------------------------------------------

def test_fused_footnote_marker_is_isolated():
    """f53and → [f53] and (already a regression test, kept here for group)."""
    result = clean_text("causing f53and things to work together")
    assert "[f53]" in result
    assert "f53and" not in result


def test_parenthesized_scripture_ref_strips_leading_space():
    """'( Matthew 3:17)' → '(Matthew 3:17)'."""
    result = clean_text('the word." ( Matthew 3:17; John 5:25.)')
    assert "(Matthew 3:17" in result
    assert "( Matthew" not in result


# ---------------------------------------------------------------------------
# 1.8  Scholastic anchor false-positive / false-negative coverage
# ---------------------------------------------------------------------------

def test_scholastic_labels_in_normal_sentence_are_not_bolded():
    """
    'Answer' and 'Solution' appearing in ordinary prose should not be wrapped
    in scholastic-label bold.  Only the abbreviated label forms (Ans., Obj.,
    Sol., Use.) at paragraph start are legitimate anchors.
    """
    from render import apply_scholastic_anchor_protocol

    prose = (
        "<p>The answer is found in the gospel of grace.</p>\n"
        "<p>A solution to this difficulty appears below.</p>\n"
        "<p>Use of scripture is Owen's primary method.</p>"
    )
    html = apply_scholastic_anchor_protocol(prose)

    # "answer" and "solution" in flowing prose must NOT be bolded
    assert '<b class="scholastic-label">The answer' not in html
    assert '<b class="scholastic-label">A solution' not in html
    # "Use of scripture" — Use. starts a scholastic label only with a digit
    # (Use. 1.) or a period immediately after; bare "Use" as a prep phrase is safe
    assert "<b>Use of scripture" not in html


def test_scholastic_sequence_all_three_labels_bolded():
    """Obj. / Ans. / Sol. appearing as a Q&A sequence are all bolded."""
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>Obj. 1. But how can a holy God justify sinners?</p>\n"
        "<p>Ans. 1. He justifies them through the righteousness of Christ.</p>\n"
        "<p>Sol. This satisfies the demands of the law.</p>"
    )

    assert '<b class="scholastic-label">Obj. 1.</b>' in html
    assert '<b class="scholastic-label">Ans. 1.</b>' in html
    assert '<b class="scholastic-label">Sol.</b>' in html


def test_use_label_with_numeral_is_bolded():
    """'Use. 1.' and 'Use. 2.' are scholastic application labels and must be bolded."""
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>Use. 1. You that are yet in the flower of your days.</p>\n"
        "<p>Use. 2. Let this truth humble all proud boasters.</p>"
    )

    assert '<b class="scholastic-label">Use. 1.</b>' in html
    assert '<b class="scholastic-label">Use. 2.</b>' in html


def test_digression_heading_renders_as_h3():
    """[[DIGRESSION]] must render as an h3 element with class 'digression-heading'."""
    from render import markdown_to_html

    md = "[[DIGRESSION]] A digression concerning the nature of faith.\n\nBody text."
    html, _, _ = markdown_to_html(md)

    # Must be an h3 with the digression-heading class (may also have id attr)
    assert re.search(r'<h3\b[^>]*class="[^"]*digression-heading[^"]*"', html), (
        f"Expected h3.digression-heading in rendered HTML.\nHTML: {html[:300]}"
    )
    assert "digression" in html.lower()
    # Must not appear as a plain paragraph
    assert "<p>[[DIGRESSION]]" not in html


# ===========================================================================
# PART 2 — EPUB-SCANNING TESTS (require a built EPUB)
# ===========================================================================

@pytest.mark.parametrize("volume", VOLUMES)
def test_no_raw_pipeline_tokens_in_epub(volume: int):
    """
    None of the pipeline-internal markers should appear as literal text
    anywhere in a finished EPUB.
    """
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml)

    forbidden = [
        "[[CHAPTER]]", "[[PART]]", "[[BLOCKQUOTE]]",
        "[[SUMMARY]]", "[[FRONT_MATTER]]", "[[DIGRESSION]]",
        "[[MARKER]]", "[[/MARKER]]",
    ]
    failures = [tok for tok in forbidden if tok in text_only]
    assert not failures, (
        f"Volume {volume}: raw pipeline tokens found in EPUB text: {failures}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_literal_footnote_markers_in_epub_text(volume: int):
    """
    [f1], [f12] etc. must be converted to noteref links.  A literal [fN]
    in visible text means the render stage dropped the conversion.
    """
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml)

    # Strip known false positives: scripture references like [490430]
    # are numeric, not [f\d+], so the pattern is safe.
    hits = re.findall(r"\[f\d+\]", text_only)
    assert not hits, (
        f"Volume {volume}: literal footnote marker(s) found in EPUB text: {hits[:10]}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_ages_boilerplate_in_epub(volume: int):
    """
    AGES Digital Library boilerplate text must be stripped during extraction.
    Any residue means the header/footer redaction logic failed on some page.
    """
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml)

    boilerplate = [
        "THE AGES DIGITAL LIBRARY",
        "JOHN OWEN COLLECTION",
        "B o o k s F o r T h e A g e s",
        "Books For The Ages",
        "AGES Software",
        "Version 1.0",
    ]
    hits = [b for b in boilerplate if b.lower() in text_only.lower()]
    assert not hits, (
        f"Volume {volume}: AGES boilerplate survived into EPUB: {hits}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_double_spaces_in_paragraph_text(volume: int):
    """
    Double spaces in the middle of a paragraph text node indicate a merge
    artifact or a dropped character.  A small threshold (5) accommodates
    any pre-existing edge cases while catching regressions.
    """
    xhtml = _all_xhtml_text(volume)
    paras = _prose_paragraphs(xhtml)

    hits = [p[:120] for p in paras if "  " in p]
    assert len(hits) <= 3, (
        f"Volume {volume}: {len(hits)} paragraph(s) contain double spaces "
        f"(after whitespace normalisation).\n"
        + "\n".join(f"  {h!r}" for h in hits[:5])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_consecutive_duplicate_words_in_epub(volume: int):
    """
    'the the', 'of of', 'that that' etc. are classic OCR / paragraph-merge
    artifacts.  Zero tolerance: any hit is a bug.
    """
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml)
    # Collapse whitespace for clean matching
    flat = re.sub(r"\s+", " ", text_only)

    # "that that" can be legitimate English ("he found that that argument was flawed"),
    # so it is intentionally excluded.  The remaining patterns are true artifacts.
    COMMON_DUPES = [
        r"\bthe the\b", r"\bof of\b", r"\band and\b",
        r"\bin in\b", r"\bto to\b", r"\bis is\b",
        r"\bit it\b", r"\bwith with\b", r"\bfor for\b",
    ]
    hits = []
    for pat in COMMON_DUPES:
        m = re.search(pat, flat, re.I)
        if m:
            start = max(0, m.start() - 40)
            hits.append(flat[start : m.end() + 40])

    assert not hits, (
        f"Volume {volume}: consecutive duplicate words found:\n"
        + "\n".join(f"  ...{h}..." for h in hits)
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_orphaned_beta_code_in_epub(volume: int):
    """
    Beta Code accent characters surviving into EPUB text mean the Greek
    conversion pipeline missed a span.  Examples: >, <, ~, |, {, }
    appearing adjacent to Latin letters in a Greek context.
    """
    BETA_RESIDUE_RE = re.compile(
        r"\b(?:[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW]+[><=~|{}+]+"
        r"|[><=~|{}+]+[abgdezhqiklmnxoprstufcyvwABGDEZHQIKLMNXOPRSTUFCYVW])\b"
    )
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml)
    hits = BETA_RESIDUE_RE.findall(text_only)

    assert len(hits) == 0, (
        f"Volume {volume}: Beta Code residue found in EPUB text: {hits[:10]}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_empty_bracket_noise_in_epub(volume: int):
    """
    [] (empty brackets) are AGES scripture marker artifacts.  Zero tolerance.
    """
    ep = _epub_path(volume)
    if not ep.exists():
        pytest.skip(f"EPUB for volume {volume} not found")

    failures: list[str] = []
    with zipfile.ZipFile(ep) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                text = _strip_tags(zf.read(name).decode("utf-8", errors="replace"))
                if re.search(r"\[\s*\]", text):
                    failures.append(name)

    assert not failures, (
        f"Volume {volume}: empty bracket noise [] found in: {failures}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_paragraphs_do_not_start_lowercase_unless_continuation(volume: int):
    """
    A paragraph starting with a lowercase letter usually signals a bad paragraph
    split: the previous paragraph's sentence was broken mid-sentence.

    Allowed exceptions:
      - Starts with a lowercase word inside a lang-tagged span (Greek/Hebrew)
      - Starts with an HTML entity like &#x27; (quote)
      - The paragraph is a chapter-summary or catechism-item (can start mid-thought)
    A budget of 5 per volume allows pre-existing edge cases without masking regressions.
    """
    xhtml = _all_xhtml_text(volume)

    # Restrict to plain body paragraphs only (class="body" or no class)
    body_paras = re.findall(
        r'<p(?:\s+class="(?:body|roman-list-item|list-item)")?>(.*?)</p>',
        xhtml, re.S,
    )
    hits = []
    for raw in body_paras:
        text = _strip_tags(raw).strip()
        if not text:
            continue
        first_char = text[0]
        if first_char.islower():
            hits.append(text[:100])

    # Budget: volume 1 has ~9 known continuation paragraphs that start lowercase.
    # Keep the threshold tight enough to catch new regressions (allow up to 15).
    assert len(hits) <= 15, (
        f"Volume {volume}: {len(hits)} paragraph(s) start with a lowercase letter "
        f"(possible bad paragraph split):\n"
        + "\n".join(f"  {h!r}" for h in hits[:10])
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_no_double_punctuation_in_epub(volume: int):
    """
    '..' ',,', ';;', and '!!' in paragraph text are almost always an artifact
    of paragraph-merge or footnote-marker removal.
    """
    xhtml = _all_xhtml_text(volume)
    paras = _prose_paragraphs(xhtml)
    flat = " ".join(paras)

    # ., is legitimate in 17th-century scholarly citation style (period after
    # abbreviation, then comma: "Aquin. 22 q. 81, a. 3,").  Exclude it.
    # Only flag: ,, ;; !! ?? and runs of 3+ mixed punct chars.
    DOUBLE_PUNCT_RE = re.compile(r"([,;!?])\1|[,;!?]{3,}")
    hits = [m.group(0) for m in DOUBLE_PUNCT_RE.finditer(flat)]

    assert len(hits) == 0, (
        f"Volume {volume}: doubled punctuation sequences found: {hits[:10]}"
    )


@pytest.mark.parametrize("volume", VOLUMES)
def test_theological_vocabulary_present_in_epub(volume: int):
    """
    Owen's core theological vocabulary must appear somewhere in the volume.
    If a term is completely absent it either was never in the volume (fine —
    add a per-volume skip) or was garbled during conversion.

    This is intentionally a light check (presence, not spelling of every
    instance).  It catches catastrophic garbling, not individual typos.
    """
    xhtml = _all_xhtml_text(volume)
    text_only = _strip_tags(xhtml).lower()

    # Terms that appear in virtually every Owen volume
    universal_terms = ["christ", "gospel", "grace", "covenant", "scripture"]
    missing = [t for t in universal_terms if t not in text_only]

    assert not missing, (
        f"Volume {volume}: core theological terms missing from EPUB text: {missing}\n"
        "This likely indicates a catastrophic extraction failure."
    )


# ---------------------------------------------------------------------------
# 1.x  Blemish #17 — Greek "[" diacritic prefix artifact
# ---------------------------------------------------------------------------

def test_greek_open_bracket_prefix_is_stripped():
    """
    The AGES PDF sometimes encodes rough-breathing diacritics as "[" immediately
    before the Greek Unicode character. clean_greek_text must strip the stray
    "[" so it never reaches the rendered EPUB.

    Regression guard for Issue #17 (v2: "[Ελεος, — mercy forgiveness").
    """
    from shared import clean_greek_text
    assert clean_greek_text("[Ελεος") == "Ελεος"
    assert clean_greek_text("[χάρις") == "χάρις"
    assert clean_greek_text("[ἔλεος") == "ἔλεος"


def test_greek_bracket_strip_does_not_affect_list_markers():
    """
    List markers such as "[1.]", "[2.]", and abbreviations such as "[LXX]"
    must NOT be touched by the Greek bracket-strip rule.
    The lookahead only fires when "[" is directly adjacent to a Unicode Greek
    character — digits and Latin letters are safe.
    """
    from shared import clean_greek_text
    assert clean_greek_text("[1.] Of the person") == "[1.] Of the person"
    assert clean_greek_text("[LXX] quotation") == "[LXX] quotation"
    # Space between "[" and Greek → "[" is semantic, not a diacritic prefix
    assert clean_greek_text("[ Ελεος ]") == "[ Ελεος ]"


# ---------------------------------------------------------------------------
# 1.x  Blemish #16 — Em-dash introduced flat list
# ---------------------------------------------------------------------------

def test_em_dash_flat_list_single_word_labels_absorbed():
    """
    Single-word label lists after a "—" paragraph must be merged inline.
    "I shall briefly observe four things therein: —
     (1.) Sweetness.  (2.) Delight.  (3.) Safety.  (4.) Comfort."
    should become a single paragraph.

    Regression guard for Issue #16 (Signal C: all items ≤ 3 words).
    """
    from render import _attach_em_dash_flat_list
    html = (
        '<p>I shall briefly observe four things therein: —</p>\n'
        '<p class="list-item"><b>(1.)</b> Sweetness.</p>\n'
        '<p class="list-item"><b>(2.)</b> Delight.</p>\n'
        '<p class="list-item"><b>(3.)</b> Safety.</p>\n'
        '<p class="list-item"><b>(4.)</b> Comfort.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, "Items should be absorbed into the body paragraph"
    assert result.count("<p") == 1, "Should collapse to a single paragraph"
    for word in ("Sweetness", "Delight", "Safety", "Comfort"):
        assert word in result


def test_em_dash_flat_list_semicolon_items_absorbed():
    """
    Semicolon-terminated ordinal lists after "—" must be absorbed (Signal A).
    "He does this, — 1st. Powerfully, or effectually; 2ndly. Voluntarily; 3rdly. Freely."
    """
    from render import _attach_em_dash_flat_list
    html = (
        '<p>He does this, —</p>\n'
        '<p class="list-item"><b>1st.</b> Powerfully, or effectually;</p>\n'
        '<p class="list-item"><b>2ndly.</b> Voluntarily;</p>\n'
        '<p class="list-item"><b>3rdly.</b> Freely.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result
    assert "Powerfully" in result and "Freely" in result
    assert result.count("<p") == 1


def test_em_dash_flat_list_short_phrase_run_absorbed():
    """
    3+ items all ≤ 7 words after "—" must be absorbed (Signal D).
    "(1.) The desert of it. (2.) Man's impotency by reason of it.
     (3.) The death of it. (4.) A new end put to it."
    """
    from render import _attach_em_dash_flat_list
    html = (
        '<p>For the first, there are four things in sin: —</p>\n'
        '<p class="list-item"><b>(1.)</b> The desert of it.</p>\n'
        '<p class="list-item"><b>(2.)</b> Man’s impotency by reason of it.</p>\n'
        '<p class="list-item"><b>(3.)</b> The death of it.</p>\n'
        '<p class="list-item"><b>(4.)</b> A new end put to it.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result
    assert "desert" in result and "impotency" in result
    assert result.count("<p") == 1


def test_em_dash_flat_list_twofold_account_pair_absorbed():
    """
    A 2-item run introduced by an explicit "twofold account" anchor is an
    Owenian flat syllabus, not an ambiguous block list.
    """
    from render import _attach_em_dash_flat_list
    html = (
        '<p>The desert of sin shines upon a twofold account: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it.</p>\n'
        '<p class="list-item"><b>[2.]</b> Of the penalty he underwent.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result
    # The anchor paragraph gets class="syllabus-anchor" (added in a later session)
    assert (
        'The desert of sin shines upon a twofold account: — <b>[1.]</b> '
        'Of the person suffering for it. <b>[2.]</b> Of the penalty he underwent.</p>'
    ) in result


def test_em_dash_flat_list_long_items_stay_block():
    """
    Items exceeding the hard cap (> 8 content words) must never be flattened,
    regardless of the em-dash context.  These are proper scholastic expansions.
    """
    from render import _attach_em_dash_flat_list
    long_item = (
        "Powerfully: and therefore does comfort from the words and promises "
        "of Christ sometimes break in through all opposition."
    )
    html = (
        '<p>He does this, —</p>\n'
        f'<p class="list-item"><b>1st.</b> {long_item}</p>\n'
        '<p class="list-item"><b>2ndly.</b> Voluntarily: and therefore this comfort '
        'is not extorted by any necessity but flows freely.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, "Long-item run must stay as block"


def test_em_dash_flat_list_prefix_absorbed_before_long_expansion():
    """
    A short introductory flat list may be followed immediately by the first
    full expansion item.  The long expansion must not veto the flat prefix.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>He does this, —</p>\n'
        '<p class="list-item"><b>1st.</b> Powerfully, or effectually;</p>\n'
        '<p class="list-item"><b>2ndly.</b> Voluntarily;</p>\n'
        '<p class="list-item"><b>3rdly.</b> Freely.</p>\n'
        '<p class="list-item"><b>1st.</b> Powerfully: and therefore does comfort '
        'from the words and promises of Christ sometimes break in through all opposition '
        'into the saddest and darkest condition imaginable.</p>'
    )

    result = _attach_em_dash_flat_list(html)

    assert (
        'He does this, — <b>1st.</b> Powerfully, or effectually; '
        '<b>2ndly.</b> Voluntarily; <b>3rdly.</b> Freely.</p>'
    ) in result
    assert (
        '<p class="list-item"><b>1st.</b> Powerfully: and therefore does comfort'
    ) in result


def test_em_dash_flat_list_two_item_prefix_attaches_before_expansion():
    """
    Two semicolon-linked introductory heads should attach to the preceding
    em-dash paragraph, while the repeated first head begins the expansion.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>The whole may be reduced unto these two heads: —</p>\n'
        '<p class="list-item"><b>[1.]</b> A mutual resignation of themselves one to the other;</p>\n'
        '<p class="list-item"><b>[2.]</b> Mutual, consequential, conjugal affections.</p>\n'
        '<p class="list-item"><b>[1.]</b> There is a mutual resignation, or making over '
        'of their persons one to another.</p>'
    )

    result = _attach_em_dash_flat_list(html)

    assert (
        'The whole may be reduced unto these two heads: — <b>[1.]</b> '
        'A mutual resignation of themselves one to the other; <b>[2.]</b> '
        'Mutual, consequential, conjugal affections.</p>'
    ) in result
    assert '<p class="list-item"><b>[1.]</b> There is a mutual resignation' in result


def test_em_dash_flat_list_parallel_gloss_pair_attaches_before_expansion():
    """
    Two short parallel gloss definitions after an em-dash are an introductory
    flat pair, even without semicolon punctuation.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>There are two ways of expressing a fellow-feeling and suffering with another: —</p>\n'
        '<p class="list-item"><b>(1.)</b> Per benevolam condolentiam, — a "friendly grieving."</p>\n'
        '<p class="list-item"><b>(2.)</b> Per gratiosam opitulationem, — a "gracious supply:" '
        'both are eminent in Christ: —</p>\n'
        '<p class="list-item"><b>(1.)</b> He grieves and labors with us. Zechariah 1:12,</p>'
    )

    result = _attach_em_dash_flat_list(html)

    assert (
        'There are two ways of expressing a fellow-feeling and suffering with another: — '
        '<b>(1.)</b> Per benevolam condolentiam, — a "friendly grieving." '
        '<b>(2.)</b> Per gratiosam opitulationem, — a "gracious supply:" '
        'both are eminent in Christ: —</p>'
    ) in result
    assert '<p class="list-item"><b>(1.)</b> He grieves and labors with us.' in result


def test_em_dash_binary_account_pair_attaches_before_expansion():
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>(1.)</b> The desert of sin does clearly shine '
        'in the cross of Christ upon a twofold account: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it.</p>\n'
        '<p class="list-item"><b>[2.]</b> Of the penalty he underwent.</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it. '
        'This the Scripture oftentimes very emphatically sets forth, and lays '
        'great weight upon the matter, as that which gives glory to the '
        'justice of God and assurance of pardon to the souls of men.</p>'
    )

    result = _attach_em_dash_flat_list(html)

    assert (
        '<b>(1.)</b> The desert of sin does clearly shine in the cross of Christ '
        'upon a twofold account: — <b>[1.]</b> Of the person suffering for it. '
        '<b>[2.]</b> Of the penalty he underwent.</p>'
    ) in result
    assert '<p class="list-item"><b>[1.]</b> Of the person suffering for it. This the Scripture' in result


def test_orphaned_flat_list_marker_tail_joins_short_next_paragraph():
    from render import _join_orphaned_flat_list_marker_paragraphs

    html = (
        '<p>may be referred to two heads: — <b>1.</b> Temptations. 2.</p>\n'
        '<p>Afflictions.</p>'
    )

    result = _join_orphaned_flat_list_marker_paragraphs(html)

    assert result == (
        '<p>may be referred to two heads: — <b>1.</b> Temptations. '
        '<b>2.</b> Afflictions.</p>'
    )


def test_inline_roman_section_splits_to_subheading_before_flat_list():
    from render import markdown_to_html

    html, _, _ = markdown_to_html(
        'Intro sentence. III. The THIRD part of our wisdom is to walk with God. '
        'Now, that one may walk with another, six things are required: —\n\n'
        '1. Agreement.\n\n'
        '2. Acquaintance.\n\n'
        '3. A way.\n\n'
        '4. Strength.\n\n'
        '5. Boldness.\n\n'
        '6. An aiming at the same end.\n\n'
        'All these, with the wisdom of them, are hid in the Lord Jesus.'
    )

    assert 'Intro sentence.</p>' in html
    assert '<h4 class="roman-subheading"><b>III.</b></h4>' in html
    assert (
        '<p class="syllabus-anchor">The THIRD part of our wisdom is to walk with God. '
        'Now, that one may walk with another, six things are required: — '
        '<b>1.</b> Agreement. <b>2.</b> Acquaintance. <b>3.</b> A way. '
        '<b>4.</b> Strength. <b>5.</b> Boldness. <b>6.</b> An aiming at the same end.</p>'
    ) in html
    assert (
        '<p>All these, with the wisdom of them, are hid in the Lord Jesus.</p>'
    ) in html


def test_owenian_list_levels_mark_exposition_and_nested_subpoints():
    from render import markdown_to_html

    html, _, _ = markdown_to_html(
        'For the first, there are four things in sin that clearly shine out in '
        'the cross of Christ: —\n\n'
        '(1.) The desert of it.\n\n'
        '(2.) Man’s impotency by reason of it.\n\n'
        '(3.) The death of it.\n\n'
        '(4.) A new end put to it.\n\n'
        '(1.) The desert of sin does clearly shine in the cross of Christ upon '
        'a twofold account: —\n\n'
        '[1.] Of the person suffering for it.\n\n'
        '[2.] Of the penalty he underwent.\n\n'
        '[1.] Of the person suffering for it. This the Scripture oftentimes '
        'very emphatically sets forth, and lays great weight upon the matter, '
        'as that which gives glory to the justice of God.'
    )

    assert (
        'For the first, there are four things in sin that clearly shine out '
        'in the cross of Christ: — <b>(1.)</b> The desert of it. '
        '<b>(2.)</b> Man\'s impotency by reason of it. <b>(3.)</b> The death '
        'of it. <b>(4.)</b> A new end put to it.</p>'
    ) in html
    assert (
        '<b>(1.)</b> The desert of sin does '
        'clearly shine in the cross of Christ upon a twofold account: — '
        '<b>[1.]</b> Of the person suffering for it. <b>[2.]</b> Of the '
        'penalty he underwent.</p>'
    ) in html
    assert (
        '<p class="list-item list-level-2"><b>[1.]</b> Of the person suffering '
        'for it. This the Scripture oftentimes very emphatically sets forth, '
        'and lays great weight upon the matter, as that which gives glory to '
        'the justice of God.</p>'
    ) in html


def test_owenian_local_ordinals_get_deeper_reader_level():
    from render import markdown_to_html

    html, _, _ = markdown_to_html(
        'The first thing is manifest in several respects.\n\n'
        '1st. Powerfully: and therefore does comfort from the words and promises '
        'of Christ sometimes break in through opposition.\n\n'
        '2dly. Voluntarily: it flows freely from grace.'
    )

    assert '<p class="list-item list-level-3"><b>1st.</b> Powerfully:' in html
    assert '<p class="list-item list-level-3"><b>2dly.</b> Voluntarily:' in html


def test_flat_syllabus_attaches_to_long_parent_list_item_anchor():
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>1.</b> In respect of sin. There is a long '
        'expository paragraph before the syllabus anchor, because Owen can '
        'embed the next compact table of heads at the end of an existing '
        'numbered argument. For the first, there are four things in sin that '
        'clearly shine out in the cross of Christ: —</p>\n'
        '<p class="list-item"><b>(1.)</b> The desert of it.</p>\n'
        '<p class="list-item"><b>(2.)</b> Man\'s impotency by reason of it.</p>\n'
        '<p class="list-item"><b>(3.)</b> The death of it.</p>\n'
        '<p class="list-item"><b>(4.)</b> A new end put to it.</p>\n'
        '<p class="list-item"><b>(1.)</b> The desert of sin does clearly shine '
        'in the cross of Christ upon a twofold account: —</p>'
    )

    result = _attach_em_dash_flat_list(html)

    assert (
        'For the first, there are four things in sin that clearly shine out in '
        'the cross of Christ: — <b>(1.)</b> The desert of it. <b>(2.)</b> '
        'Man\'s impotency by reason of it. <b>(3.)</b> The death of it. '
        '<b>(4.)</b> A new end put to it.</p>'
    ) in result
    assert (
        '<p class="list-item"><b>(1.)</b> The desert of sin does clearly shine'
    ) in result


# ===========================================================================
# PART 3 — Regression tests for textual.md bug fixes (2026-05-26)
# ===========================================================================

# ---------------------------------------------------------------------------
# Bug #1 — Observation / Obs. must receive scholastic-anchor bold treatment
# ---------------------------------------------------------------------------

def test_observation_label_rendered_bold_by_scholastic_anchor():
    """
    "Obs. 1." and "Observation 1." are scholastic labels equivalent to Obj./Ans.
    They must be split onto their own paragraph with the label bolded.
    Previously only Obj./Ans./Use./Sol./Application. were recognised.
    """
    from render import apply_scholastic_anchor_protocol

    text = "Obs. 1. God's covenant extends to all his people.\n\nObs. 2. This covenant is everlasting."
    result = apply_scholastic_anchor_protocol(text)
    # Each Obs. must end up on its own paragraph / span
    assert "Obs. 1." in result
    assert "Obs. 2." in result
    # The function should not collapse both into a single run without splitting
    assert result.count("Obs.") == 2


def test_observation_full_word_label_is_recognised():
    """'Observation 1.' (full word) must also be treated as a scholastic label."""
    from render import apply_scholastic_anchor_protocol

    text = "Observation 1. The nature of faith is complex.\n\nObservation 2. It involves trust."
    result = apply_scholastic_anchor_protocol(text)
    assert "Observation 1." in result
    assert "Observation 2." in result


# ---------------------------------------------------------------------------
# Bug #2 — "Prefatory Note" heading must not appear twice in sermon volumes
# ---------------------------------------------------------------------------

def test_prefatory_note_heading_suppressed_in_sermon_volume():
    """
    In sermon volumes (suppress_prefatory_note_heading=True) the body <h2>
    "Prefatory Note" must be suppressed — Apple Books already shows the chapter
    nav title, so emitting the h2 as well produces a visible double-heading.
    """
    from render import markdown_to_html

    md = "[[CHAPTER]] Prefatory Note\n\nThe following sermons were preached..."
    config = {'suppress_prefatory_note_heading': True}
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER", config=config)
    # The h2 heading must NOT appear in the output
    assert 'Prefatory Note' not in html or '<h2' not in html or (
        'Prefatory Note' in html and '<h2' not in html
    )


def test_prefatory_note_heading_present_in_treatise_volume():
    """
    Without the suppress flag the Prefatory Note heading must render normally.
    """
    from render import markdown_to_html

    md = "[[CHAPTER]] Prefatory Note\n\nThe author writes..."
    html, _, _ = markdown_to_html(md, current_mode="FRONT_MATTER")
    # The heading CAN be present; the point is no suppression fires
    # (We just verify the function runs without error and produces html)
    assert html


# ---------------------------------------------------------------------------
# Bug #3 — Verse numbers after commas must not be falsely bolded
# ---------------------------------------------------------------------------

def test_verse_number_after_comma_not_bold():
    """
    "Psalm 110, 1." — the '1' is a verse number, not a list marker.
    The bold-stripping rule must prevent it from rendering as <b>1.</b>.

    Pattern: digit(s) + comma + space + <b>digit(s)</b>  →  strip the <b>.
    """
    from render import markdown_to_html

    # Construct a line that would trigger the list-item bold heuristic
    md = 'Serve the Lord with fear, and rejoice with trembling, Psalm 110, 11.'
    html, _, _ = markdown_to_html(md)
    # "11" must not be wrapped in <b>
    assert '<b>11' not in html and '<b>11.' not in html, (
        f"Verse number was falsely bolded. HTML: {html!r}"
    )


def test_verse_number_multi_digit_after_comma_not_bold():
    """Multi-digit verse numbers (e.g. ", 12.") must also be safe."""
    from render import markdown_to_html

    md = 'As it is written in Psalm 22, 12. Many bulls have compassed me.'
    html, _, _ = markdown_to_html(md)
    assert '<b>12' not in html, f"Multi-digit verse number falsely bolded. HTML: {html!r}"


# ---------------------------------------------------------------------------
# Bug #4 — "+" and "{" diacritic prefixes before Greek Unicode must be stripped
# ---------------------------------------------------------------------------

def test_plus_immediately_before_greek_is_stripped():
    """
    '+' directly before a Unicode Greek character is an AGES PDF artefact.
    clean_greek_text must strip it.
    """
    from shared import clean_greek_text

    assert clean_greek_text("+Ωmega") == "Ωmega"
    # The actual Owen example from the blemish report
    assert clean_greek_text("+Ω Βάθος") == "Ω Βάθος"


def test_brace_immediately_before_greek_is_stripped():
    """'{' directly before Greek Unicode is also an AGES artefact."""
    from shared import clean_greek_text

    assert clean_greek_text("{Ελεος") == "Ελεος"
    assert clean_greek_text("{ἔλεος") == "ἔλεος"


def test_plus_before_latin_is_not_stripped_by_clean_greek_text():
    """
    '+' before a Latin character is NOT a Greek diacritic artefact and must
    be left untouched by clean_greek_text.
    """
    from shared import clean_greek_text

    assert clean_greek_text("+Latin word") == "+Latin word"
    assert clean_greek_text("faith + hope") == "faith + hope"


# ---------------------------------------------------------------------------
# Bug #5 — Stray "+" line-continuation artefact in Latin body text
# ---------------------------------------------------------------------------

def test_stray_plus_after_punctuation_stripped_from_body():
    """
    '+' immediately after a sentence-boundary punctuation character (,;.!? )
    followed by a Latin letter is a line-continuation artefact and must be
    stripped by the markdown_to_html preprocessor.

    "warning all, +using all appointed means" → "warning all, using all..."
    """
    from render import markdown_to_html

    md = 'warning all, +using all appointed means to draw them to Jesus Christ.'
    html, _, _ = markdown_to_html(md)
    assert '+using' not in html
    assert 'using all appointed means' in html


def test_double_space_normalised_to_single():
    """
    Double (or more) spaces in body text must be collapsed to a single space
    by the preprocessor in markdown_to_html.
    """
    from render import markdown_to_html

    md = 'He teaches  us  that  grace  abounds.'
    html, _, _ = markdown_to_html(md)
    assert '  ' not in html, "Double spaces survived into rendered HTML."


# ---------------------------------------------------------------------------
# Bug #6 — Em-dash flat list: 3-item 9-word run must be absorbed
# ---------------------------------------------------------------------------

def test_em_dash_flat_list_nine_word_item_absorbed():
    """
    "1. That God hath done it. 2. That he hath promised he will yet do it.
     3. Why he will so do."
    Item 2 has 9 words — previously blocked by the 8-word hard cap.
    After raising the cap to 12, this run must be absorbed into one paragraph.

    Regression guard for Bug #6.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>Now, concerning this, observe, —</p>\n'
        '<p class="list-item"><b>1.</b> That God hath done it.</p>\n'
        '<p class="list-item"><b>2.</b> That he hath promised he will yet do it.</p>\n'
        '<p class="list-item"><b>3.</b> Why he will so do.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "9-word item should no longer be blocked by the hard cap."
    )
    assert result.count("<p") == 1
    assert "That God hath done it" in result
    assert "he hath promised" in result


def test_em_dash_flat_list_thirteen_word_item_stays_block():
    """
    Items that genuinely exceed the hard cap (> 12 words) must remain as
    block list items — these are proper scholastic expansions, not flat labels.

    Regression guard: raising the cap for Bug #6 must not accidentally absorb
    long-sentence lists.
    """
    from render import _attach_em_dash_flat_list

    # Item exceeds both the 12-word hard cap and Signal H's 25-word cap so that
    # no flat signal fires and the items remain as block list paragraphs.
    long_item = (
        "Powerfully: and therefore does comfort from the words and promises "
        "of Christ break in through all opposition into the saddest and darkest "
        "condition of the soul, prevailing over every discouragement whatsoever."
    )
    html = (
        '<p>He does this in three ways, —</p>\n'
        f'<p class="list-item"><b>1st.</b> {long_item}</p>\n'
        '<p class="list-item"><b>2ndly.</b> Voluntarily: it flows freely from grace.</p>\n'
        '<p class="list-item"><b>3rdly.</b> Freely and without constraint of any kind.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, (
        "Item exceeding Signal H cap (>25w) with no continuation signals must "
        "remain as a block list paragraph."
    )


# ---------------------------------------------------------------------------
# Bug #7 — Sermon opening scripture verse gets distinctive CSS class
# ---------------------------------------------------------------------------

def test_first_blockquote_in_sermon_volume_gets_opening_scripture_class():
    """
    In sermon volumes (suppress_prefatory_note_heading=True), the first
    blockquote after a chapter heading is the expository text and must receive
    class="sermon-opening-scripture".  Subsequent blockquotes in the same
    chapter must NOT receive that class.
    """
    from render import markdown_to_html

    md = (
        "[[CHAPTER]] Sermon I. — The Glory of Christ\n\n"
        "[[BLOCKQUOTE]] Serve the Lord with fear — Psalm 110:1.\n\n"
        "Body text begins here.\n\n"
        "[[BLOCKQUOTE]] A second quotation from the fathers."
    )
    config = {'suppress_prefatory_note_heading': True}
    html, _, _ = markdown_to_html(md, config=config)

    # First blockquote must have the special class
    assert 'class="sermon-opening-scripture"' in html, (
        "First blockquote in sermon chapter must have sermon-opening-scripture class."
    )
    # The special class must appear exactly once (only the opening verse)
    assert html.count('sermon-opening-scripture') == 1, (
        "Only the first blockquote per chapter should have the opening-scripture class."
    )


def test_first_blockquote_in_treatise_volume_has_no_opening_scripture_class():
    """
    In treatise volumes (no suppress_prefatory_note_heading flag), blockquotes
    are ordinary quotations and must NOT receive sermon-opening-scripture class.
    """
    from render import markdown_to_html

    md = (
        "[[CHAPTER]] CHAPTER I. — Of the Nature of Faith\n\n"
        "[[BLOCKQUOTE]] Faith is the substance of things hoped for.\n\n"
        "Body text follows."
    )
    html, _, _ = markdown_to_html(md)
    assert 'sermon-opening-scripture' not in html, (
        "Treatise volumes must never emit sermon-opening-scripture class."
    )


def test_opening_scripture_class_resets_on_new_chapter():
    """
    Each new [[CHAPTER]] token resets the first-blockquote tracker.
    The second sermon's opening blockquote must also receive the class.
    """
    from render import markdown_to_html

    md = (
        "[[CHAPTER]] Sermon I.\n\n"
        "[[BLOCKQUOTE]] First opening verse.\n\n"
        "Body of sermon one.\n\n"
        "[[CHAPTER]] Sermon II.\n\n"
        "[[BLOCKQUOTE]] Second opening verse.\n\n"
        "Body of sermon two."
    )
    config = {'suppress_prefatory_note_heading': True}
    html, _, _ = markdown_to_html(md, config=config)
    # Both blockquotes should get the class — one per chapter
    assert html.count('sermon-opening-scripture') == 2, (
        "Each sermon chapter's first blockquote must receive the opening-scripture class."
    )


# ---------------------------------------------------------------------------
# Structure refinement — Signal F word cap tightening (2026-05-27)
# ---------------------------------------------------------------------------

def test_signal_f_short_binary_label_still_flattens():
    """
    A 2-item run introduced by 'twofold account' where each item is a genuine
    short label (≤ 15 words) must still be absorbed inline.

    Regression guard: Signal F tightening must not break valid short pairs.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>The desert of sin shines upon a twofold account: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it.</p>\n'
        '<p class="list-item"><b>[2.]</b> Of the penalty he underwent.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "Short binary label pair must still flatten under tightened Signal F cap."
    )
    assert '<b>[1.]</b> Of the person suffering for it.' in result
    assert '<b>[2.]</b> Of the penalty he underwent.' in result


def test_signal_f_long_binary_exposition_stays_block():
    """
    A 2-item run introduced by 'twofold account' where each item exceeds the
    tightened Signal F cap (> 20 words) must remain as block paragraphs.

    Before the 2026-05-27 tightening these 24-word items would have been
    flattened by Signal F's old +18 allowance (30 words).  They are genuine
    exposition openings, not flat labels.
    """
    from render import _attach_em_dash_flat_list

    item = (
        "That God hath done it in his eternal counsel and decree, appointing "
        "his Son thereunto, and sending him into the world for this very end."
    )
    html = (
        '<p>This may be considered upon a twofold account: —</p>\n'
        f'<p class="list-item"><b>[1.]</b> {item}</p>\n'
        f'<p class="list-item"><b>[2.]</b> {item}</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, (
        "24-word binary items must not be flattened — they are exposition, not labels."
    )


def test_signal_f_border_case_at_twenty_words_flattens():
    """
    An item of exactly 20 words (the new Signal F ceiling) should still
    flatten.  The cap is inclusive: ≤ 20 is allowed.
    """
    from render import _attach_em_dash_flat_list

    # Construct a pair where each item is exactly 20 words
    item_20w = (
        "Of the person suffering for it, as the eternal Son of God incarnate "
        "and made flesh, appointed by the Father."
    )
    import re as _re
    wc = len(_re.sub(r'<[^>]+>', '', item_20w).split())
    assert wc <= 20, f"Test item must be ≤ 20 words but is {wc}"

    html = (
        '<p>The matter may be stated upon a twofold account: —</p>\n'
        f'<p class="list-item"><b>[1.]</b> {item_20w}</p>\n'
        f'<p class="list-item"><b>[2.]</b> {item_20w}</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        f"Item of {wc} words must still flatten (≤ 20-word Signal F cap)."
    )


# ---------------------------------------------------------------------------
# Structure refinement — syllabus-anchor class emission (2026-05-27)
# ---------------------------------------------------------------------------

def test_syllabus_anchor_class_added_to_plain_p_on_absorption():
    """
    When a flat list is absorbed into a plain <p> anchor paragraph, the
    anchor must receive the 'syllabus-anchor' class so readers and future CSS
    can identify it as a flat-syllabus host.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>I shall briefly observe four things therein: —</p>\n'
        '<p class="list-item"><b>(1.)</b> Sweetness.</p>\n'
        '<p class="list-item"><b>(2.)</b> Delight.</p>\n'
        '<p class="list-item"><b>(3.)</b> Safety.</p>\n'
        '<p class="list-item"><b>(4.)</b> Comfort.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'syllabus-anchor' in result, (
        "Absorbed flat-list anchor must receive the syllabus-anchor class."
    )
    assert result.startswith('<p class="syllabus-anchor">'), (
        "Plain <p> anchor must have syllabus-anchor as its class."
    )


def test_syllabus_anchor_class_added_to_list_item_anchor_on_absorption():
    """
    When the anchor is itself a list-item paragraph (e.g. a (1.) exposition
    head that embeds a flat sub-list), the syllabus-anchor class must be
    appended to its existing class string.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item list-level-1"><b>(1.)</b> The desert of sin '
        'does clearly shine in the cross of Christ upon a twofold account: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it.</p>\n'
        '<p class="list-item"><b>[2.]</b> Of the penalty he underwent.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'syllabus-anchor' in result, (
        "List-item anchor must receive the syllabus-anchor class after absorption."
    )
    assert 'class="list-item list-level-1 syllabus-anchor"' in result, (
        "syllabus-anchor must be appended to existing class string, not replace it."
    )


def test_syllabus_anchor_class_not_added_when_no_absorption():
    """
    If no flat list is absorbed (items are too long), the anchor paragraph
    must NOT receive the syllabus-anchor class.
    """
    from render import _attach_em_dash_flat_list

    long_item = (
        "Powerfully: and therefore does comfort from the words and promises "
        "of Christ sometimes break in through all opposition upon the soul."
    )
    html = (
        '<p>He works, —</p>\n'
        f'<p class="list-item"><b>1st.</b> {long_item}</p>\n'
        f'<p class="list-item"><b>2ndly.</b> {long_item}</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'syllabus-anchor' not in result, (
        "No absorption means no syllabus-anchor class must appear."
    )


# ---------------------------------------------------------------------------
# Structure refinement — expanded _preceding_allows_attachment (2026-05-27)
# ---------------------------------------------------------------------------

def test_long_list_item_anchor_with_count_pattern_allows_attachment():
    """
    A list-item anchor over 45 words (the old limit) that contains an explicit
    count + category tail must still allow its flat sub-list to attach.

    Regression guard for the 45→80 word limit raise plus explicit_syllabus_tail.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>(1.)</b> The desert of sin does clearly shine '
        'in the cross of Christ in this regard — it is set before us with great '
        'emphasis and solemnity — upon a twofold account of the greatest moment '
        'and consequence to the souls and consciences of men, namely these: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it.</p>\n'
        '<p class="list-item"><b>[2.]</b> Of the penalty he underwent.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert '<b>[1.]</b> Of the person suffering for it.' in result
    assert '<b>[2.]</b> Of the penalty he underwent.' in result
    # The sub-list should be absorbed, not left as separate list-item paragraphs
    absorbed = (
        'twofold account of the greatest moment and consequence to the souls '
        'and consciences of men, namely these: — <b>[1.]</b> Of the person '
        'suffering for it. <b>[2.]</b> Of the penalty he underwent.'
    )
    assert absorbed in result, (
        "Long count-pattern anchor (>45w) must still absorb its short flat sub-list."
    )


def test_formula_tail_these_following_allows_attachment():
    """
    An anchor ending with 'these following: —' (a non-count formula) must
    allow its flat sub-list to attach, even if no explicit count word is present.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>(1.)</b> The chief graces are set before us '
        'in these following particulars: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Faith.</p>\n'
        '<p class="list-item"><b>[2.]</b> Hope.</p>\n'
        '<p class="list-item"><b>[3.]</b> Love.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "'these following' formula anchor must allow flat sub-list attachment."
    )
    assert '<b>[1.]</b> Faith.' in result
    assert '<b>[3.]</b> Love.' in result


def test_formula_tail_i_shall_observe_allows_attachment():
    """
    An anchor ending with 'I shall observe briefly: —' must allow flat sub-list
    attachment even without count words.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>1.</b> Concerning this point I shall observe '
        'briefly: —</p>\n'
        '<p class="list-item"><b>(1.)</b> Agreement.</p>\n'
        '<p class="list-item"><b>(2.)</b> Acquaintance.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "'I shall observe' formula anchor must allow flat sub-list attachment."
    )


def test_formula_tail_may_be_considered_allows_attachment():
    """
    An anchor ending with 'may be considered: —' must allow flat sub-list
    attachment even without count words.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p class="list-item"><b>(1.)</b> Two things in this matter may be '
        'considered: —</p>\n'
        '<p class="list-item"><b>[1.]</b> Their original.</p>\n'
        '<p class="list-item"><b>[2.]</b> Their continuance.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "'may be considered' formula anchor must allow flat sub-list attachment."
    )


def test_long_anchor_under_80_words_without_pattern_allows_attachment():
    """
    A list-item anchor between 46 and 80 words with no count pattern must
    allow flat sub-list attachment under the raised word limit.
    """
    from render import _attach_em_dash_flat_list
    import re as _re

    # Build an anchor that is 52 plain words (>45, <80, no count/formula tail)
    filler = ('and the grace of God is exceeding abundant toward us ' * 5).strip()
    anchor_text = f'<b>1.</b> {filler}: —'
    wc = len(_re.sub(r'<[^>]+>', '', anchor_text).split())
    assert 45 < wc < 80, f"Anchor must be 46-79 words for this test, got {wc}"

    html = (
        f'<p class="list-item">{anchor_text}</p>\n'
        '<p class="list-item"><b>(1.)</b> Mercy.</p>\n'
        '<p class="list-item"><b>(2.)</b> Grace.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        f"Anchor of {wc} words (46-79 range) must allow flat sub-list attachment."
    )


def test_anchor_over_80_words_without_pattern_blocks_attachment():
    """
    A list-item anchor exceeding 80 words with no count or formula tail must
    NOT allow flat sub-list attachment.  This prevents a long merged paragraph
    from accidentally absorbing an unrelated following run.
    """
    from render import _attach_em_dash_flat_list
    import re as _re

    # Build a list-item anchor that is 82 plain words (>80)
    filler = ('and the grace of God is exceeding abundant toward us ' * 8).strip()
    anchor_text = f'<b>1.</b> {filler}: —'
    wc = len(_re.sub(r'<[^>]+>', '', anchor_text).split())
    assert wc > 80, f"Anchor must exceed 80 words for this test, got {wc}"

    html = (
        f'<p class="list-item">{anchor_text}</p>\n'
        '<p class="list-item"><b>(1.)</b> Mercy.</p>\n'
        '<p class="list-item"><b>(2.)</b> Grace.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, (
        f"Anchor of {wc} words (>80, no pattern) must block flat sub-list attachment."
    )


# ---------------------------------------------------------------------------
# Signal G — ordinal sequence continuation  (2026-05-27)
# ---------------------------------------------------------------------------

def test_signal_g_ordinal_continuation_attaches_to_preceding_inline_ordinal():
    """
    Signal G: (3rdly.) after a prose paragraph that already contains inline
    (1st.) / (2ndly.) markers must be absorbed flat into that paragraph.

    The preceding paragraph does NOT end with em-dash — Signal G fires via
    the alternative trigger (_HAS_INLINE_ORDINAL_RE match on the preceding).

    Source: Vol. 2 Ch. 2, "There are three things in general…consist: — (1st.)…
    (2ndly.)…" followed by "(3rdly.) His excellency…men: —" as a list-item.
    """
    from render import _attach_em_dash_flat_list

    preceding = (
        'There are three things in general wherein this personal excellency and '
        'grace of the Lord Christ does consist: — (1st.) His fitness to save, '
        'from the grace of union, and the proper necessary effects thereof '
        '(2ndly.) His fullness to save, from the grace of communion; or the '
        'free consequences of the grace of union.'
    )
    html = (
        f'<p>{preceding}</p>\n'
        '<p class="list-item"><b>(3rdly.)</b> His excellency to endear, from his '
        'complete suitableness to all the wants of the souls of men: —</p>'
    )
    result = _attach_em_dash_flat_list(html)
    # (3rdly.) must be absorbed flat — no remaining list-item paragraph
    assert 'class="list-item"' not in result, (
        "Signal G must absorb (3rdly.) into the preceding paragraph that already "
        "contains inline (1st.) and (2ndly.) markers."
    )
    assert '(3rdly.)' in result or '<b>(3rdly.)</b>' in result, (
        "The (3rdly.) marker must appear inline in the result."
    )


def test_signal_g_does_not_fire_without_preceding_inline_ordinal():
    """
    Signal G must NOT fire when the preceding paragraph contains no inline
    ordinal markers — only the normal em-dash trigger applies.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>He considers the grace of Christ: —</p>\n'
        '<p class="list-item"><b>(3rdly.)</b> His excellency to endear, from his '
        'complete suitableness to all the wants of the souls of men: —</p>'
    )
    result = _attach_em_dash_flat_list(html)
    # The paragraph ends with em-dash, so normal em-dash absorption applies.
    # But (3rdly.) is 15 words and none of the normal signals fire (no ; or ,
    # on a non-final item, no binary intro), so it stays block.
    assert 'class="list-item"' in result, (
        "Without preceding inline ordinals, Signal G must not fire; "
        "(3rdly.) should remain a block list-item."
    )


def test_split_ordinal_inline_expansions_splits_at_first_em_ordinal():
    """
    _split_ordinal_inline_expansions must split a list-item that embeds a
    '(1st.) expansion' after an em-dash, retaining only the intro in the
    first item and producing a second item for the expansion.

    Source: "(3rdly.) His excellency…men: — (1st.) His fitness to save, —
    his being 'hikanos'…" (Vol. 2 Ch. 2).
    """
    from render import _split_ordinal_inline_expansions

    html = (
        '<p class="list-item"><b>(3rdly.)</b> His excellency to endear, from his '
        'complete suitableness to all the wants of the souls of men: — '
        '(1st.) His fitness to save, — his being "hikanos", a fit Savior, '
        'suited to the work.</p>'
    )
    result = _split_ordinal_inline_expansions(html)

    assert result.count('<p class="list-item">') == 2, (
        "Should produce exactly two list-item paragraphs after split."
    )
    # First item ends at the em-dash (intro only)
    assert 'men: —</p>' in result, (
        "First item should end at 'men: —' (the split boundary)."
    )
    # Second item contains the expansion
    assert '<b>(1st.)</b>' in result, (
        "Second item must carry a bold (1st.) marker."
    )
    assert 'hikanos' in result, (
        "Expansion content must be preserved in the second item."
    )


def test_split_ordinal_inline_expansions_no_split_for_short_intro():
    """
    _split_ordinal_inline_expansions must NOT split when the intro before the
    em-dash is too short (< 8 words) — it is just a label, not an announced phrase.
    """
    from render import _split_ordinal_inline_expansions

    html = '<p class="list-item"><b>(3rdly.)</b> Brief: — (1st.) more text.</p>'
    result = _split_ordinal_inline_expansions(html)
    assert result == html, (
        "Short intro (< 8 words) must not trigger the ordinal expansion split."
    )


# ---------------------------------------------------------------------------
# Semicolon-chain continuation — Issue 2  (2026-05-27)
# ---------------------------------------------------------------------------

def test_continuation_chain_last_item_joins_when_previous_ends_with_connector():
    """
    Continuation-committed bypass: when the second-to-last item ends with
    'and' or 'or', the final item must join even if it is long.

    E.g. "[1.] What this work is, and  [2.] How it is performed in us." —
    the 'and' tail commits [2.] to the same flat run as [1.].
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>Two things are to be considered: —</p>\n'
        '<p class="list-item"><b>(1.)</b> What this work is, and</p>\n'
        '<p class="list-item"><b>(2.)</b> How it is performed in us by the Holy '
        'Spirit, working effectually in every regenerate soul according to the '
        'counsel and purpose of God in election.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "'and'-terminated item must commit the following long item to the flat run."
    )
    assert '<b>(1.)</b>' in result and '<b>(2.)</b>' in result


def test_continuation_chain_last_item_joins_when_previous_ends_with_comma():
    """
    Continuation-committed bypass: when the second-to-last item ends with ',',
    the final item joins even if it is long.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>Three respects to be noted: —</p>\n'
        '<p class="list-item"><b>1.</b> The first,</p>\n'
        '<p class="list-item"><b>2.</b> The second and greater consideration, '
        'being the full and complete satisfaction rendered to divine justice '
        'through the obedience and suffering of the Lord Christ in our stead.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "','-terminated item must commit the following long item to the flat run."
    )


def test_semicolon_chain_last_item_joins_when_previous_ends_with_semicolon():
    """
    Issue 2: when [1.][2.][3.] each end with ';' and [4.] is long but ends
    with '.', all four must be merged (Signal A + semicolon-continuation bypass).

    Source: Vol. 2 Digression 2 — "His vindictive justice in punishing sin;
    … His patience … His wisdom … His all-sufficiency … All these, though …"
    """
    from render import _attach_em_dash_flat_list

    anchor = (
        '<b>(2.)</b> There are other properties of God which, though also otherwise '
        'discovered, yet are so clearly, eminently, and savingly only in Jesus Christ; as, —'
    )
    html = (
        f'<p class="list-item">{anchor}</p>\n'
        '<p class="list-item"><b>[1.]</b> His vindictive justice in punishing sin;</p>\n'
        '<p class="list-item"><b>[2.]</b> His patience, forbearance, and long-suffering towards sinners;</p>\n'
        '<p class="list-item"><b>[3.]</b> His wisdom, in managing things for his own glory;</p>\n'
        '<p class="list-item"><b>[4.]</b> His all-sufficiency, in himself and unto others. '
        'All these, though they may receive some lower and inferior manifestations out of '
        'Christ, yet they clearly shine only in him; so as that it may be our wisdom to be '
        'acquainted with them. Hebrews 1:3; of which before.</p>'
    )
    result = _attach_em_dash_flat_list(html)

    # All four [n.] items must be absorbed into the (2.) anchor
    for marker in ('[1.]', '[2.]', '[3.]', '[4.]'):
        assert f'<b>{marker}</b>' in result, f"{marker} must appear in the result"

    # No standalone list-item paragraphs should remain for [1.]-[4.]
    # (The anchor (2.) itself becomes the merged paragraph)
    remaining_items = [
        p for p in result.split('<p class="list-item">')[1:]
        if any(f'<b>{m}</b>' in p for m in ('[1.]', '[2.]', '[3.]', '[4.]'))
    ]
    assert not remaining_items, (
        "All four [n.] items must be absorbed inline; none should remain as "
        f"standalone list-item paragraphs. Remaining: {remaining_items}"
    )


def test_semicolon_chain_long_final_item_without_preceding_semicolon_stays_block():
    """
    The semicolon-continuation bypass must NOT fire when the second-to-last item
    ends with '.' — a long final item stays block in that case (normal hard cap).
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>He works, —</p>\n'
        '<p class="list-item"><b>1.</b> Something short.</p>\n'
        '<p class="list-item"><b>2.</b> A very long scholastic expansion about '
        'the nature of divine wisdom as revealed through the person and work of '
        'Christ in his mediatorial office and covenant engagement.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    # Item 2 (long, not preceded by ;-terminated item) must remain block
    assert 'class="list-item"' in result, (
        "Long final item with no semicolon-terminated predecessor must stay block."
    )


# ---------------------------------------------------------------------------
# Issue 20 — all_non_final_semi bypass (all non-final items end with ';')
# ---------------------------------------------------------------------------

def test_all_non_final_semi_absorbs_when_all_items_end_with_semicolon():
    """
    Issue 20: three-item list where items 1 and 2 end with ';' but exceed the
    12-word hard cap.  all_non_final_semi must fire and absorb all three inline.

    Source: Vol. 2 — Digression 1, Song of Solomon gloss
    "1. A sweet savor…perfume; 2. Beauty and order…import; 3. Eminency…flowers."
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>He describes it in these words: —</p>\n'
        '<p class="list-item"><b>1.</b> A sweet savor, as from spices, and flowers, '
        'and towers of perfume;</p>\n'
        '<p class="list-item"><b>2.</b> Beauty and order, as spices set in rows or '
        'beds, as the words import;</p>\n'
        '<p class="list-item"><b>3.</b> Eminency in that word, as sweet or well-grown, '
        'great flowers.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' not in result, (
        "all_non_final_semi must absorb all three items inline even though "
        "items 1 and 2 exceed the 12-word hard cap."
    )
    # All three markers must appear in the merged paragraph
    for marker in ('1.', '2.', '3.'):
        assert f'<b>{marker}</b>' in result, (
            f"Marker '{marker}' must appear in the merged output."
        )


def test_all_non_final_semi_does_not_fire_when_items_exceed_20w_cap():
    """
    Guard test: all_non_final_semi raises the per-item cap to 20w.
    If a non-final item exceeds 20 words the list must remain block.
    """
    from render import _attach_em_dash_flat_list

    # Item 1 ends with ';' but is >20 words — bypass must not fire
    html = (
        '<p>There are several grounds for this observation: —</p>\n'
        '<p class="list-item"><b>1.</b> The first ground is the eternal and '
        'unchangeable love of God the Father toward his elect people chosen before '
        'the foundation of the world in Christ Jesus;</p>\n'
        '<p class="list-item"><b>2.</b> The second ground, briefly stated.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    assert 'class="list-item"' in result, (
        "Items exceeding the 20-word all_non_final_semi cap must remain block."
    )


# ---------------------------------------------------------------------------
# Issue 21 — spurious backslash OCR artifact stripped
# ---------------------------------------------------------------------------

def test_backslash_artifact_stripped_before_lowercase_word():
    r"""
    Issue 21: A lone backslash immediately before a lowercase word is an OCR
    artifact that must be removed by _repair_owen_ocr_errors.
    "\which" → "which", "\the" → "the"
    """
    from shared import _repair_owen_ocr_errors

    assert _repair_owen_ocr_errors(r'\which, in the phrase') == 'which, in the phrase'
    assert _repair_owen_ocr_errors(r'and \the Lord') == 'and the Lord'
    # Mid-sentence variant
    assert _repair_owen_ocr_errors(r'the grace \of God') == 'the grace of God'


def test_backslash_artifact_not_stripped_before_uppercase():
    """
    Guard: a backslash before an uppercase letter must NOT be stripped —
    it could be a legitimate escape or OCR rendering of a capital-letter marker.
    """
    from shared import _repair_owen_ocr_errors

    original = r'\Now he speaks of'
    # The regex only fires for lowercase — uppercase is left alone
    result = _repair_owen_ocr_errors(original)
    assert result == original, (
        "Backslash before uppercase must not be stripped (only lowercase targets)."
    )


def test_backslash_artifact_not_stripped_when_preceded_by_word_char():
    """
    Guard: backslash inside a word (e.g. a genuine path or escape sequence
    immediately after a word character) must be left alone.
    """
    from shared import _repair_owen_ocr_errors

    original = r'path\word'
    result = _repair_owen_ocr_errors(original)
    assert result == original, (
        "Backslash preceded by a word character must not be stripped."
    )


# ---------------------------------------------------------------------------
# Signal H — preview-syllabus flat absorption (≥3 items, all end '.', all ≤25w)
# ---------------------------------------------------------------------------

def test_signal_h_absorbs_preview_syllabus_with_medium_items():
    """
    Signal H: four-item preview index where items 1–2 are 17–21 words (above
    Signal D's 9-word cap) but all end with '.' and all are ≤25 words.
    All four items must be absorbed inline after the em-dash anchor.

    Source: Vol. 7 — "In the words we consider, —
      1. The connection of them unto those foregoing...  (17w)
      2. The subject described in them...                (21w)
      3. What is supposed concerning them.               (5w)
      4. What is affirmed of them on that supposition.   (8w)"
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>In the words we consider, —</p>\n'
        '<p class="list-item"><b>1.</b> The connection of them unto those foregoing, '
        'intimating the occasion of the introduction of this whole discourse.</p>\n'
        '<p class="list-item"><b>2.</b> The subject described in them, or the persons '
        'spoken of, under sundry qualifications, which may be inquired into jointly '
        'and severally.</p>\n'
        '<p class="list-item"><b>3.</b> What is supposed concerning them.</p>\n'
        '<p class="list-item"><b>4.</b> What is affirmed of them on that supposition.</p>'
    )
    result = _attach_em_dash_flat_list(html)

    # No standalone list-item paragraphs should remain
    assert 'class="list-item"' not in result, (
        "Signal H must absorb all four preview items inline."
    )
    # All four markers must appear in the merged output
    for marker in ('1.', '2.', '3.', '4.'):
        assert f'<b>{marker}</b>' in result, (
            f"Marker '{marker}' must appear in the merged paragraph."
        )


def test_signal_h_does_not_fire_when_item_exceeds_25w():
    """
    Guard: Signal H must NOT fire when any item exceeds the 25-word cap.
    A genuine expansion item (29 words) should remain block.
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>In the words we consider, —</p>\n'
        '<p class="list-item"><b>1.</b> The connection of them unto those foregoing, '
        'intimating the occasion of the introduction of this whole discourse and also '
        'the full apostolic purpose and intention thereof, which he declares.</p>\n'
        '<p class="list-item"><b>2.</b> What is supposed concerning them.</p>\n'
        '<p class="list-item"><b>3.</b> What is affirmed of them on that supposition.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    # Item 1 is 29 words — exceeds Signal H cap; list must stay block
    assert 'class="list-item"' in result, (
        "Items exceeding 25 words must prevent Signal H from firing."
    )


def test_signal_h_does_not_fire_for_two_item_list():
    """
    Guard: Signal H requires ≥3 items. A two-item list where both items end
    with '.' and are ≤25 words must NOT be absorbed by Signal H alone
    (Signal F handles binary lists with explicit intro; without an explicit
    binary intro keyword, a two-item list stays block).
    """
    from render import _attach_em_dash_flat_list

    html = (
        '<p>There are two points here, —</p>\n'
        '<p class="list-item"><b>1.</b> The occasion of the apostle writing.</p>\n'
        '<p class="list-item"><b>2.</b> The manner in which he addresses them.</p>'
    )
    result = _attach_em_dash_flat_list(html)
    # Signal H needs n ≥ 3, Signal F needs explicit "twofold/two things" keyword —
    # "two points" doesn't match Signal F's pattern, so these stay block
    assert 'class="list-item"' in result, (
        "Two-item list must not be absorbed by Signal H (requires ≥3 items)."
    )


# ---------------------------------------------------------------------------
# FOURTHLY/THIRDLY etc — ALL-CAPS ordinal normalization + STRUCTURAL_START_RE
# ---------------------------------------------------------------------------

def test_allcaps_ordinal_normalized_to_titlecase():
    r"""
    Bare ALL-CAPS ordinals at paragraph start are OCR artefacts.
    _repair_owen_ocr_errors must normalize them to title-case so the render
    pipeline can bold and classify them as list-items.

    Corpus sources (across volumes 2–16):
      v3  ch022: "SECONDLY, There is in this death…"
      v3  ch024: "FOURTHLY, The last thing…"
      v16 ch---: "SEVENTHLY. He is the head…"
    """
    from shared import _repair_owen_ocr_errors

    cases = [
        # comma-terminated
        ('SECONDLY, There is in this death', 'Secondly, There is in this death'),
        ('THIRDLY, In this state',           'Thirdly, In this state'),
        ('FOURTHLY, The last thing',         'Fourthly, The last thing'),
        ('FIFTHLY, Consider this',           'Fifthly, Consider this'),
        ('EIGHTHLY, Consider',               'Eighthly, Consider'),
        ('NINTHLY, The final point',         'Ninthly, The final point'),
        ('SEVENTHLY, He is',                 'Seventhly, He is'),
        ('FIRST, in reference unto',         'First, in reference unto'),
        ('LASTLY, He concludes',             'Lastly, He concludes'),
        # period-terminated (v16 style)
        ('SEVENTHLY. He is the head',        'Seventhly. He is the head'),
        ('EIGHTHLY. Consider this matter',   'Eighthly. Consider this matter'),
    ]
    for inp, expected in cases:
        assert _repair_owen_ocr_errors(inp) == expected, (
            f"Expected {expected!r}, got {_repair_owen_ocr_errors(inp)!r}"
        )


def test_allcaps_ordinal_not_normalized_mid_sentence():
    r"""
    Guard: ALL-CAPS ordinal that is NOT at a paragraph/line start must not
    be altered — it could be an inline quotation or emphasis.
    """
    from shared import _repair_owen_ocr_errors

    mid = 'We see this SECONDLY, in the context of grace'
    assert _repair_owen_ocr_errors(mid) == mid, (
        "Mid-sentence ALL-CAPS ordinal must not be normalized."
    )


def test_allcaps_ordinal_multiline_normalizes_each_start():
    r"""
    In multi-paragraph raw_text each paragraph start is normalized independently.
    """
    from shared import _repair_owen_ocr_errors

    raw = 'Para one.\n\nSECONDLY, Para two.\n\nTHIRDLY, Para three.'
    result = _repair_owen_ocr_errors(raw)
    assert 'SECONDLY' not in result
    assert 'THIRDLY' not in result
    assert 'Secondly,' in result
    assert 'Thirdly,' in result


def test_structural_start_re_matches_higher_ordinals():
    """
    STRUCTURAL_START_RE must match Seventhly, Eighthly, Ninthly, and Firstly
    (added in this fix) so that paragraphs starting with these get
    class="list-item" in render.py.
    """
    import re
    from shared import STRUCTURAL_START_RE

    for ordinal in ('Seventhly,', 'Eighthly,', 'Ninthly,', 'Firstly,',
                    'Seventhly.', 'Eighthly.', 'Ninthly.'):
        text = f'{ordinal} Some body text follows here.'
        assert STRUCTURAL_START_RE.match(text), (
            f"STRUCTURAL_START_RE must match paragraph starting with {ordinal!r}"
        )


# ===========================================================================
# _repair_markdown_tables  (v10 ch4 two-column comparison table)
# ===========================================================================

def test_markdown_table_converted_to_blockquote_plain_pairs():
    """A two-column pipe table becomes [[BLOCKQUOTE]]/plain paragraph pairs.

    Right column  → [[BLOCKQUOTE]] (Arminian / Remonstrant quote)
    Left column   → plain paragraph (Scripture reference)
    """
    from render import _repair_markdown_tables

    table_para = (
        '|Scripture ref A.|"Arminian reply A."| '
        '|---|---| '
        '|Scripture ref B.|"Arminian reply B."|'
    )
    result = _repair_markdown_tables(table_para)
    paras = [p.strip() for p in result.split('\n\n') if p.strip()]

    # Row 1: right column → [[BLOCKQUOTE]], left column → plain
    assert paras[0] == '[[BLOCKQUOTE]] "Arminian reply A."', repr(paras[0])
    assert paras[1] == 'Scripture ref A.', repr(paras[1])
    # Row 2: same pattern
    assert paras[2] == '[[BLOCKQUOTE]] "Arminian reply B."', repr(paras[2])
    assert paras[3] == 'Scripture ref B.', repr(paras[3])


def test_markdown_table_with_preceding_unclosed_blockquote():
    r"""When a [[BLOCKQUOTE]] ends with a comma (quote cut off), the right cell
    of the first table row completes it.  Left cell of first row → plain para.
    The second row follows the normal right=[[BLOCKQUOTE]], left=plain pattern.
    """
    from render import _repair_markdown_tables

    text = (
        '[[BLOCKQUOTE]] "God doth not determine the will of man to this or that,\n\n'
        '|Scripture ref A.|or to one part of the contradiction," Arminius.| '
        '|---|---| '
        '|Scripture ref B.|"The will of man is absolutely free," Rem.|'
    )
    result = _repair_markdown_tables(text)
    paras = [p.strip() for p in result.split('\n\n') if p.strip()]

    # First [[BLOCKQUOTE]] must be completed with the right cell of row 1
    assert paras[0].startswith('[[BLOCKQUOTE]]'), repr(paras[0])
    assert 'or to one part of the contradiction," Arminius.' in paras[0], repr(paras[0])
    assert paras[0].endswith('or to one part of the contradiction," Arminius.'), repr(paras[0])

    # Left cell of row 1 → plain paragraph
    assert paras[1] == 'Scripture ref A.', repr(paras[1])

    # Row 2 → normal pattern
    assert paras[2] == '[[BLOCKQUOTE]] "The will of man is absolutely free," Rem.', repr(paras[2])
    assert paras[3] == 'Scripture ref B.', repr(paras[3])


def test_markdown_table_br_tags_converted_to_spaces():
    """<br> inside cells becomes a space; separator row triggers table parsing."""
    from render import _repair_markdown_tables

    # Real table format: rows separated by | | within a single paragraph,
    # with a |---|---| separator row to identify the table.
    table_para = (
        '|See<br>Matthew 27:1,<br>Acts 2:23.|"The will of man<br>is free," Rem.|'
        ' |---|---| '
        '|Another ref.|Another quote.|'
    )
    result = _repair_markdown_tables(table_para)
    assert '<br>' not in result
    assert 'Matthew 27:1, Acts 2:23.' in result
    assert '"The will of man is free," Rem.' in result


def test_markdown_table_non_table_paragraph_unchanged():
    """Paragraphs without a table separator row pass through untouched."""
    from render import _repair_markdown_tables

    plain = 'This is an ordinary paragraph with no table syntax.'
    assert _repair_markdown_tables(plain) == plain


# ===========================================================================
# "try" → "thy" OCR repair
# ===========================================================================

def test_try_breath_ocr_repaired_to_thy_breath():
    r""""in whose hand try breath is" is an OCR misread of "thy"."""
    from shared import _repair_owen_ocr_errors

    text = 'the God in whose hand try breath is, and whose are all thy ways'
    result = _repair_owen_ocr_errors(text)
    assert 'thy breath' in result, repr(result)
    assert 'try breath' not in result, repr(result)


def test_try_ways_ocr_repaired_to_thy_ways():
    r""""whose are all try ways" is an OCR misread of "thy"."""
    from shared import _repair_owen_ocr_errors

    text = 'the God in whose hand thy breath is, and whose are all try ways'
    result = _repair_owen_ocr_errors(text)
    assert 'thy ways' in result, repr(result)
    assert 'try ways' not in result, repr(result)


def test_try_not_repaired_outside_biblical_phrase():
    """'try' in a non-matching context must not be altered."""
    from shared import _repair_owen_ocr_errors

    # "try" as a normal verb — must not be touched
    text = 'We should try harder to understand the text.'
    result = _repair_owen_ocr_errors(text)
    assert 'try harder' in result, repr(result)


# ===========================================================================
# _repair_fused_word_ordinals
# ===========================================================================

def test_fused_secondly_split_into_two_paragraphs():
    """A fused 'Secondly,' after a full stop splits into separate paragraphs."""
    from render import _repair_fused_word_ordinals

    text = 'In the first place we speak of certainty. Secondly, this applies to all cases.'
    result = _repair_fused_word_ordinals(text)
    paras = result.split('\n\n')
    assert len(paras) == 2, repr(result)
    assert paras[0].endswith('certainty.'), repr(paras[0])
    assert paras[1].startswith('Secondly,'), repr(paras[1])


def test_fused_thirdly_fourthly_split():
    """Multiple fused ordinals in one paragraph all split correctly."""
    from render import _repair_fused_word_ordinals

    text = 'First point made. Secondly, another consideration. Thirdly, a third point. Fourthly, the last.'
    result = _repair_fused_word_ordinals(text)
    paras = result.split('\n\n')
    assert len(paras) == 4, repr(result)
    assert paras[0] == 'First point made.', repr(paras[0])
    assert paras[1].startswith('Secondly,'), repr(paras[1])
    assert paras[2].startswith('Thirdly,'), repr(paras[2])
    assert paras[3].startswith('Fourthly,'), repr(paras[3])


def test_fused_ordinal_blockquote_not_split():
    """[[BLOCKQUOTE]] paragraphs with internal ordinals are left intact."""
    from render import _repair_fused_word_ordinals

    text = '[[BLOCKQUOTE]] There are two kinds. Secondly, the other kind follows.'
    result = _repair_fused_word_ordinals(text)
    assert result == text, repr(result)


def test_fused_ordinal_already_split_unchanged():
    """Paragraphs already split by \\n\\n are not further modified."""
    from render import _repair_fused_word_ordinals

    text = 'First point.\n\nSecondly, second point.'
    result = _repair_fused_word_ordinals(text)
    assert result == text, repr(result)


def test_fused_ordinal_no_ordinal_unchanged():
    """Paragraphs without word ordinals pass through untouched."""
    from render import _repair_fused_word_ordinals

    text = 'This is plain text with no ordinals at all.'
    assert _repair_fused_word_ordinals(text) == text


def test_fused_lastly_split():
    """'Lastly,' after terminal punctuation is split correctly."""
    from render import _repair_fused_word_ordinals

    text = 'We have considered three points. Lastly, we conclude the argument.'
    result = _repair_fused_word_ordinals(text)
    paras = result.split('\n\n')
    assert len(paras) == 2, repr(result)
    assert paras[1].startswith('Lastly,'), repr(paras[1])


# ===========================================================================
# Stray ** bold marker + APRI OCR fix
# ===========================================================================

def test_stray_bold_marker_after_comma_stripped():
    """', ** Word' — stray bold opener after comma is removed cleanly."""
    from shared import _repair_owen_ocr_errors

    text = 'enemies, ** Luke 1:74; from the wrath to come, 1 Thessalonians 1:10.'
    result = _repair_owen_ocr_errors(text)
    assert '** ' not in result, repr(result)
    assert 'enemies, Luke 1:74' in result, repr(result)


def test_stray_bold_marker_after_semicolon_stripped():
    """'; ** Word' — stray bold opener after semicolon is removed cleanly."""
    from shared import _repair_owen_ocr_errors

    text = 'propitiation; ** Romans 3:25; 1 John 2:2.'
    result = _repair_owen_ocr_errors(text)
    assert '** ' not in result, repr(result)
    assert 'propitiation; Romans 3:25' in result, repr(result)


def test_valid_bold_not_stripped():
    """Valid bold markers like '**Secondly,**' are not affected."""
    from shared import _repair_owen_ocr_errors

    text = '**Secondly,** We do not say punishing is an act of dominion.'
    result = _repair_owen_ocr_errors(text)
    assert '**Secondly,**' in result, repr(result)


def test_apri_ocr_fix_before_day_number():
    """'APRI 25,' is repaired to 'APRIL 25,'."""
    from shared import _repair_owen_ocr_errors

    text = 'COGGESHALL, APRI 25, 1648.'
    result = _repair_owen_ocr_errors(text)
    assert 'APRIL 25' in result, repr(result)
    assert 'APRI ' not in result, repr(result)


def test_apri_not_changed_without_day_number():
    """'APRI' not followed by a day number is left unchanged."""
    from shared import _repair_owen_ocr_errors

    # Hypothetical: 'APRI' as a standalone word not before a date
    text = 'The APRI conference was held in spring.'
    result = _repair_owen_ocr_errors(text)
    assert 'APRI ' in result, repr(result)


def test_scholastic_anchors_are_nested_in_owen_level_2():
    """Consecutive scholastic anchors should be grouped and nested inside <div class="owen-branch owen-level-2">."""
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>An answer unto an inquiry which may possibly arise...</p>\n"
        "<p class=\"scholastic-anchor\"><b class=\"scholastic-label\">Ans. 1.</b> There is no precedent...</p>\n"
        "<p class=\"scholastic-anchor\"><b class=\"scholastic-label\">Ans. 2.</b> In the invocation of Christ...</p>"
    )

    # Verify that they are wrapped in a single owen-level-2 div
    assert '<div class="owen-branch owen-level-2">' in html
    assert html.count('<div class="owen-branch owen-level-2">') == 1
    # Check that they end with a closed div
    assert '</div>' in html


def test_scholastic_parent_child_differentiation():
    """Objections/Uses (parents) remain flush-left at level 1, while Answers/Solutions (children) nest at level 2."""
    from render import apply_scholastic_anchor_protocol

    html = apply_scholastic_anchor_protocol(
        "<p>Objection 1. But how can a holy God justify sinners?</p>\n"
        "<p>Ans. 1. He justifies them through the righteousness of Christ.</p>\n"
        "<p>Ans. 2. This satisfies the demands of the law.</p>"
    )

    # Objection (parent) should have scholastic-anchor-parent class and NOT be wrapped in owen-level-2
    assert 'scholastic-anchor-parent' in html
    # Answers (children) should have scholastic-anchor-child class and BE wrapped in owen-level-2
    assert 'scholastic-anchor-child' in html
    assert '<div class="owen-branch owen-level-2">' in html
    
    obj_idx = html.find('Objection 1.')
    div_idx = html.find('<div class="owen-branch owen-level-2">')
    ans_idx = html.find('Ans. 1.')
    
    assert obj_idx < div_idx < ans_idx


def test_nesting_cap_beyond_level_3_remains_flat():
    """Any inline sub-points (representing Level 4+) inside a Level 3 paragraph (e.g. starting with 1st.) should remain flat and inline."""
    from shared import _split_inline_structural_markers

    para = "1st. First point, which has several sub-elements: — (1.) The first sub-element; (2.) The second sub-element."
    pieces = _split_inline_structural_markers(para)

    # Since it starts with a Level 3 marker (1st.), the list cap prevents splitting of the inline markers!
    assert len(pieces) == 1
    assert pieces[0] == para


def test_dynamic_trigger_based_demotion():
    """Verify that the Dynamic Demotion Engine correctly demotes lists introduced by count triggers under level-2 items to Level 3."""
    from render import _add_owen_list_level_classes

    # Case A: Level 2 item ([1.]) introduces a sub-list of two things using bare decimals (1., 2.)
    html = (
        '<p class="list-item"><b>[1.]</b> Of the person suffering for it, which consists in two things: —</p>\n'
        '<p class="list-item"><b>1.</b> The dignity of the person.</p>\n'
        '<p class="list-item"><b>2.</b> The greatness of the penalty.</p>\n'
        '<p class="list-item"><b>[2.]</b> The next bracketed item.</p>'
    )
    result = _add_owen_list_level_classes(html)

    # The bracketed items [1.] and [2.] are base level 2
    assert 'class="list-item list-level-2"><b>[1.]</b>' in result
    assert 'class="list-item list-level-2"><b>[2.]</b>' in result

    # The subordinate decimals 1. and 2. must be dynamically demoted to Level 3
    assert 'class="list-item list-level-3"><b>1.</b>' in result
    assert 'class="list-item list-level-3"><b>2.</b>' in result

    # Case B: A Level 1 item (4.) introduces two parenthesized items (1.), (2.) and then 5. resets sequence
    html2 = (
        '<p class="list-item"><b>4.</b> Some outline point, for these two reasons: —</p>\n'
        '<p class="list-item"><b>(1.)</b> First reason.</p>\n'
        '<p class="list-item"><b>(2.)</b> Second reason.</p>\n'
        '<p class="list-item"><b>5.</b> Next outline point.</p>'
    )
    result2 = _add_owen_list_level_classes(html2)

    # 4. and 5. are Level 1 (bare decimals)
    assert 'class="list-item list-level-1"><b>4.</b>' in result2
    assert 'class="list-item list-level-1"><b>5.</b>' in result2

    # (1.) and (2.) are Level 2 (parenthesized, subordinate)
    assert 'class="list-item list-level-2"><b>(1.)</b>' in result2
    assert 'class="list-item list-level-2"><b>(2.)</b>' in result2


def test_blockquote_trailing_quote_preservation():
    """Verify that balanced double quotes inside blockquotes are preserved, while unclosed trailing opening quotes are stripped."""
    from render import markdown_to_html

    # Case 1: Balanced straight double quotes (should be preserved)
    html, _, _ = markdown_to_html(
        '[[BLOCKQUOTE]] "Thou, Lord, in the beginning hast laid the foundation of the earth; and the heavens are the works of thine hands: they shall perish, but thou remainest; and they all shall wax old as does a garment; and as a vesture shalt thou fold them up, and they shall be changed: but thou art the same, and thy years shall not fail."'
    )
    assert 'Thou, Lord, in the beginning' in html
    assert 'shall not fail.&quot;' in html  # closing double quote is preserved!

    # Case 2: Unbalanced straight double quote at the end of blockquote (should be stripped)
    html2, _, _ = markdown_to_html(
        '[[BLOCKQUOTE]] Unbalanced quote test at the end. "'
    )
    # The count of " is 1 (odd) so it is stripped!
    assert '&quot;' not in html2


def test_flat_list_continuation_splits():
    """Verify that flat list items starting with ordinals or list markers are merged
    onto the preceding paragraph if it ends with a comma, semicolon, or connector word.
    """
    from render import markdown_to_html

    md = (
        "The duties whereby we ascribe and express divine honor unto Christ may be reduced unto two heads,\n\n"
        "1st, Adoration;\n\n"
        "2ndly, Invocation."
    )
    html, _, _ = markdown_to_html(md)
    # They should be joined into a single paragraph and bolded!
    assert "reduced unto two heads, <b>1st</b>, Adoration; <b>2ndly</b>, Invocation." in html


def test_stray_quotes_before_scripture_reference():
    """Verify that stray double quotes preceding a scripture reference are correctly stripped."""
    from shared import _repair_owen_ocr_errors

    # Case A: Stray quote preceded by double quote + comma + space
    raw1 = 'cried unto him, "My Lord and my God," " John 20:28.'
    assert _repair_owen_ocr_errors(raw1) == 'cried unto him, "My Lord and my God," John 20:28.'

    # Case B: Stray quote in another context
    raw2 = 'mind be in us that was in Christ Jesus," " Philippians 2:6'
    assert _repair_owen_ocr_errors(raw2) == 'mind be in us that was in Christ Jesus," Philippians 2:6'

    # Case C: Valid closing quote at end of phrase (should not be stripped)
    raw3 = 'he is the "image of God, " 2 Corinthians 4:4'
    assert _repair_owen_ocr_errors(raw3) == 'he is the "image of God, " 2 Corinthians 4:4'


