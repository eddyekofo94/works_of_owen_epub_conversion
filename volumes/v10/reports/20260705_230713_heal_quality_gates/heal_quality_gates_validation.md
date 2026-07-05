# Heal Skill Quality Gates Validation

Generated: 2026-07-05 23:07 local time

## Scope

Implemented the quality-gate decisions from `.working/interviews/heal-skill-quality-gates/decisions.md`.

## Validation Commands

- PASS: `.venv/bin/python3 -m pytest tests/test_heal_readiness.py`
- PASS: `.venv/bin/python3 -m pytest tests/test_modern_notes.py tests/test_typography_standard.py`
- FAIL: `.venv/bin/python3 -m pytest tests/test_bug_regressions.py`
  - Existing fixture/report debt surfaced outside this feature: v1 warning-code budget, v11 split-word anomalies, and stale whitelist entries in v1, v8, v11, v12, v13, and v15.
- PASS: `.venv/bin/python3 scripts/report_volume_state.py --volumes 10 --no-readme`
  - Volume 10 Need: `13.2`
  - EPUB audit errors: `0`
  - EPUB audit warnings: `0`
  - Word coverage: `99.94%`
  - Greek coverage: `100.00%`
  - Hebrew coverage: `100.00%`
  - Latin coverage: `99.58%`
  - Latin tagging: `58.82%`
  - Latin translation: `38.82%`
  - Bug regressions: `1`
- EXPECTED FAIL: `.venv/bin/python3 scripts/audit_heal_readiness.py 10 --strict`
  - Need gate `<1.0`: `FAIL`
  - Strict ready for by-eye review: `FAIL`
  - Blockers: `4`
  - Review debt: `10`

## Readiness Blockers Confirmed

- `dense_source_window_loss`: text-integrity blocker warning remains.
- `paragraph_split_candidates`: text-integrity blocker warning remains.
- `bug_regression_over_budget`: syllabus-anchor candidates are `25` observed vs `16` budget.
- `source_text_or_conversion_changes`: target conversion/source-text files have uncommitted changes and must be explicitly reported before readiness.

## Review Debt Confirmed

- `syllabus_anchor_candidates`: disclosed review debt in the text-integrity report.
- `low_latin_tagging`: `58.82%`, with samples in the readiness report.
- `low_latin_translation`: `38.82%`, with samples in the readiness report.
- Stale whitelist entries reported from the current v10 audit data.

## Report Paths

- State report: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/qa/reports/volume_state_report.md`
- State JSON: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/qa/reports/volume_state_report.json`
- Heal readiness report: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/bugs_fixes/volume_10_heal_readiness.md`
- Heal readiness JSON: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/bugs_fixes/volume_10_heal_readiness.json`
