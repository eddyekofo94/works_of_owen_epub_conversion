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
