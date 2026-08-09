import subprocess
import zipfile

from scripts import heal_readiness
from scripts.heal_readiness import (
    build_readiness_report,
    classify_state_data,
    detect_source_text_changes,
    scan_inline_modern_note_leaks,
)
from scripts.report_volume_state import score_volume


def _base_state(**overrides):
    data = {
        "vol": 10,
        "qa_level": "FULL",
        "audit_status": "pass",
        "audit_errors": 0,
        "audit_warnings": 0,
        "coverage": 0.9998,
        "greek_coverage": 1.0,
        "hebrew_coverage": 1.0,
        "latin_coverage": 0.995,
        "latin_tagging": 0.62,
        "latin_translation": 0.51,
        "unresolved_citations": 0,
        "total_citations": 10,
        "unresolved_modern_references": 0,
        "untranslated_substantial_foreign_passages": 0,
        "unenriched_legacy_footnotes": 0,
        "anomalies_count": 0,
        "unmatched_quotes": 0,
        "splits": 0,
        "audit_warnings": 0,
        "text_warning_details": [],
        "regressions": 0,
        "regression_details": [],
        "ignored_warnings": ["low_latin_tagging", "low_latin_translation_coverage"],
        "stale_whitelist_entries": [],
    }
    data.update(overrides)
    return data


def test_need_score_penalizes_blocker_warnings_and_regression_overruns():
    clean = _base_state(latin_tagging=1.0, latin_translation=1.0, ignored_warnings=[])
    blocked = _base_state(
        latin_tagging=1.0,
        latin_translation=1.0,
        ignored_warnings=[],
        text_warning_details=[{"code": "dense_source_window_loss", "message": "Dense source loss remains."}],
        regression_details=[{"label": "Syllabus-anchor candidates", "observed": 25, "budget": 16}],
        regressions=1,
    )

    assert score_volume(clean) < 1.0
    assert score_volume(blocked) >= 1.0


def test_readiness_passes_with_only_disclosed_latin_review_debt():
    result = classify_state_data(_base_state())

    assert result["ready"]
    assert result["blocker_count"] == 0
    assert {item["code"] for item in result["review_debt"]} == {
        "low_latin_tagging",
        "low_latin_translation",
    }


def test_readiness_blocks_text_integrity_blocker_warning():
    result = classify_state_data(_base_state(
        text_warning_details=[{"code": "paragraph_split_candidates", "message": "Possible paragraph split."}],
    ))

    assert not result["ready"]
    assert result["blocker_count"] == 1
    assert result["blockers"][0]["code"] == "paragraph_split_candidates"


def test_readiness_blocks_bug_regression_budget_overrun():
    result = classify_state_data(_base_state(
        regressions=1,
        regression_details=[{"label": "Repeated phrase hits", "observed": 3, "budget": 0}],
    ))

    assert not result["ready"]
    assert result["blockers"][0]["code"] == "bug_regression_over_budget"
    assert result["blockers"][0]["value"] == {"observed": 3, "budget": 0}


def test_readiness_blocks_inline_modern_note_content_in_body_xhtml(tmp_path):
    epub_path = tmp_path / "sample.epub"
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("EPUB/ch001.xhtml", "<p><strong>Modern Translation:</strong> inline body text.</p>")
        zf.writestr("EPUB/endnotes.xhtml", "<p><strong>Modern Citation:</strong> allowed note text.</p>")

    leaks = scan_inline_modern_note_leaks(epub_path)

    assert len(leaks) == 1
    assert leaks[0]["file"] == "EPUB/ch001.xhtml"
    assert leaks[0]["pattern"] == "Modern Translation:"


def _clean_epub(tmp_path):
    epub_path = tmp_path / "sample.epub"
    with zipfile.ZipFile(epub_path, "w") as zf:
        zf.writestr("EPUB/ch001.xhtml", "<p>Body text.</p>")
    return epub_path


def test_uncommitted_changes_are_review_debt_on_heal_branch(monkeypatch, tmp_path):
    monkeypatch.setattr(heal_readiness, "_current_branch", lambda: "heal-v10-20260809")
    monkeypatch.setattr(
        heal_readiness,
        "detect_source_text_changes",
        lambda volume: [{"status": "M", "path": "shared.py"}],
    )

    report = build_readiness_report("10", _base_state(), 0.5, _clean_epub(tmp_path))

    assert report["strict_ready"]
    assert report["blocker_count"] == 0
    debt_codes = {item["code"] for item in report["review_debt"]}
    assert "source_text_or_conversion_changes" in debt_codes


def test_uncommitted_changes_still_block_on_master(monkeypatch, tmp_path):
    monkeypatch.setattr(heal_readiness, "_current_branch", lambda: "master")
    monkeypatch.setattr(
        heal_readiness,
        "detect_source_text_changes",
        lambda volume: [{"status": "M", "path": "shared.py"}],
    )

    report = build_readiness_report("10", _base_state(), 0.5, _clean_epub(tmp_path))

    assert not report["strict_ready"]
    assert report["blockers"][0]["code"] == "source_text_or_conversion_changes"


def test_detect_source_text_changes_reports_target_conversion_files(monkeypatch):
    def fake_run(*args, **kwargs):
        return subprocess.CompletedProcess(
            args=args[0],
            returncode=0,
            stdout=" M volumes/v10/convert.py\n?? volumes/v10/intermediate/volume_10.json\n",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert detect_source_text_changes("10") == [
        {"status": "M", "path": "volumes/v10/convert.py"},
        {"status": "??", "path": "volumes/v10/intermediate/volume_10.json"},
    ]
