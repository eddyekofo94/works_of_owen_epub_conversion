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
from render import apply_scholastic_anchor_protocol
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


VOLUMES = requested_volumes()


def test_polyglot_fallback_does_not_convert_english_prose():
    text = (
        "The author's design concerns justification, Jesus Christ, John 3:36, "
        "grace; Christ; us; vol. 1, and [1.] markers, including [characters] and [from]."
    )

    mapped = force_polyglot_mapping(text)

    assert mapped == text


def test_polyglot_fallback_converts_unambiguous_residue_only():
    mapped = force_polyglot_mapping("pneu'ma ytb;h}aæB]")

    assert 'lang="el"' in mapped
    assert 'lang="he"' in mapped
    assert "pneu'ma" not in mapped
    assert "ytb;h}aæB]" not in mapped


def test_empty_scripture_code_brackets_are_removed():
    cleaned = clean_text("sealed unto the day of redemption. — [<490430>] Ephesians 4:30.")

    assert "[]" not in cleaned
    assert "Ephesians 4:30" in cleaned


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
def test_issue_33_shared_treatise_starter_pages_are_not_title_styled_in_epub(volume):
    if volume != 1:
        pytest.skip("Issue 33 samples are volume 1-specific")
    _, epub_path = paths_for(volume)
    if not epub_path.exists():
        pytest.skip(f"EPUB for volume {volume} not found at {epub_path}")

    files = {}
    with zipfile.ZipFile(epub_path) as zf:
        for name in zf.namelist():
            if name.endswith(".xhtml"):
                files[name] = zf.read(name).decode("utf-8", "replace")

    part_2_title = next(
        html for html in files.values()
        if "<title>Part 2 - Meditations and Discourses Concerning The Glory of Christ</title>" in html
    )
    assert '<section class="treatise-title-page"' in part_2_title
    assert "CHAPTER 1" not in part_2_title
    assert "That which remains" not in part_2_title

    part_2_chapter = next(
        html for html in files.values()
        if "<title>Chapter 1 - Meditations and Discourses Concerning the Glory of Christ</title>" in html
    )
    assert '<section class="treatise-title-page"' not in part_2_chapter
    assert "APPLICATION OF THE FOREGOING MEDITATIONS" in part_2_chapter
    assert "That which remains is, to make some application" in part_2_chapter

    greater_chapter = next(
        html for html in files.values()
        if "<title>Chapter 1 - of the Scripture.</title>" in html
    )
    assert '<section class="treatise-title-page"' not in greater_chapter
    assert 'class="catechism-item"' in greater_chapter
    assert "<b>Ques. 1.</b> What is Christian religion?" in greater_chapter
    assert "<b>Ans.</b> The only way" in greater_chapter


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
