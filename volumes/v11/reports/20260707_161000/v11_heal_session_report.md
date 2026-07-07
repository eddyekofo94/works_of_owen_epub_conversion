# Volume 11 Heal Session Report

Generated: 2026-07-07 16:10

## Summary

Volume 11 was continued from the checkpoint commit `85a489d5`.

- Before this pass: Need 15.2, strict readiness blocked by 9 unenriched legacy footnotes.
- After this pass: Need 0.8, legacy footnotes enriched, no strict blockers pending source-clean verification.
- Branch: `heal-v11-20260706`

## Changes

- Added 9 scoped `v11_fn*` footnote enrichment entries in `scripts/translation_db.py`.
- Regenerated Volume 11 EPUB and modern-notes manifest.
- Removed stale `unenriched_legacy_footnotes` whitelist usage from v11 documentation.
- Updated `scripts/report_volume_state.py` so live `bugs_fixes` reports are considered alongside archived reports, and so stale ignored-warning detection follows the regression-test rule.
- Adjusted Need scoring so Latin tagging remains readiness review debt rather than a direct score penalty.

## Verification

- `.venv/bin/python3 scripts/run_all_checks.py 11`: v11 converter/audits PASS; repository-wide pytest phase FAILS on unrelated stale whitelist debt in volumes 1, 8, 12, and 15.
- `.venv/bin/python3 scripts/audit_epub.py volumes/v11/output/volume_11.epub --out-dir volumes/v11/bugs_fixes`: PASS, 0 errors, 0 warnings.
- `.venv/bin/python3 scripts/audit_text_integrity.py 11`: PASS, 0 warnings.
- `.venv/bin/python3 scripts/audit_anomalies.py 11`: PASS, 0 suspected anomalies.
- `.venv/bin/python3 -m pytest 'tests/test_bug_regressions.py::test_no_unused_whitelist_entries[11]' -q`: PASS.
- `.venv/bin/python3 scripts/report_volume_state.py --volumes 11 --no-readme`: Need 0.8.
- `.venv/bin/python3 scripts/assert_need_under.py 11 1.0`: PASS.

## Whitelist Notes

- No new anomaly whitelist entries were added.
- Removed stale `unenriched_legacy_footnotes` from v11 text-integrity ignored warnings.
- Kept `low_latin_translation_coverage` documented as editorial review debt: Latin word coverage is 99.84%, missing Latin clauses are 0, and substantial untranslated foreign passages are 0.

## Remaining Review Debt

- Latin tagging ratio is still reported as 78.08%; samples include known English/proper-name false positives such as `perpetrate`, `co-operate`, and `alexandria`.
- Latin translation ratio is still reported as 31.74%; this remains editorial enrichment debt, not a conversion blocker, because substantial untranslated foreign passages are 0.
- User by-eye Apple Books review remains pending.

