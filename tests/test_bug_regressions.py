import json
import os
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import pytest

from scripts.audit_epub import Audit
from scripts.audit_text_integrity import run_audit
from converter import clean_text, force_polyglot_mapping


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
        "grace; Christ; us; vol. 1, and [1.] markers."
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

    failures = [
        f"{name}: observed {observed}, budget {limit}, samples {samples}"
        for name, (observed, limit, samples) in checks.items()
        if observed > limit
    ]
    assert not failures, "\n".join(failures)


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
