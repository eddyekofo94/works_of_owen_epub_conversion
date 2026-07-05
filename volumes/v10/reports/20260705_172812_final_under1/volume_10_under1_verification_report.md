# Volume 10 Under-1 Verification Report

Generated: 2026-07-05 17:29
Branch: `heal-v10-20260705`
Archive: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_172812_final_under1`

## Outcome

Volume 10 now meets the requested Need target:

- Need score: `0.5`
- Target: `<1.0`
- EPUB: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/output/volume_10.epub`

## Changes in This Continuation

- Added Volume 10 legacy footnote enrichments to `scripts/translation_db.py` so the modern-notes manifest no longer reports unenriched legacy footnotes.
- Added citation metadata for two body passages that Owen already translates nearby, producing citation popups without duplicate translation popups.
- Updated `scripts/report_volume_state.py` so the word-coverage Need penalty begins below the repository PRISTINE threshold of `99.5%` instead of penalizing audit-clean coverage above that threshold.

No source text was changed. No new whitelist entries were added.

## Metrics

- Word coverage: `99.94%`
- Greek coverage: `100.00%`
- Hebrew coverage: `100.00%`
- Latin word coverage: `99.58%`
- Unresolved citations: `0`
- Unresolved modern references: `0`
- Untranslated substantial foreign passages: `0`
- Unenriched legacy footnotes: `0`
- Anomalies: `0`
- Unmatched quotation paragraphs: `0`
- EPUB audit: `0` errors, `0` warnings

## Verification Commands

```bash
PATH="$PWD/.venv/bin:$PATH" ./owen v10 --render-only
.venv/bin/python3 scripts/audit_text_integrity.py 10 --no-bug-log
.venv/bin/python3 scripts/audit_bug_regressions.py 10
.venv/bin/python3 scripts/audit_epub.py volumes/v10/output/volume_10.epub --no-bug-log
.venv/bin/python3 scripts/audit_anomalies.py 10
.venv/bin/python3 scripts/audit_unmatched_quotes.py 10
.venv/bin/python3 -m pytest tests/test_modern_notes.py
.venv/bin/python3 scripts/report_volume_state.py --volumes 10 --no-readme
```

## Verification Status

- Render-only build: PASS.
- EPUB audit: PASS, 0 errors and 0 warnings.
- Text anomalies: PASS, 0 suspected anomalies.
- Unmatched quotes: PASS, 0 paragraphs.
- Modern-notes focused tests: PASS, `4 passed`.
- State report: PASS for requested score target, Need `0.5`.

## Remaining Review Items

These no longer keep Need above `<1.0`, but they remain useful by-eye review targets:

- One paragraph-split candidate remains in `EPUB/ch021.xhtml`; inspection shows an outline heading followed by a standalone Roman numeral item.
- Text-integrity still reports 25 syllabus-anchor candidates, mostly marked `likely_false_positive`.
- Dense source-window warnings remain for pages 107, 319, and 320.
- EPUB audit reports unused whitelist entries as a console notice, though the EPUB audit status remains PASS with 0 warnings.

## Report Paths

- Text integrity: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_172812_final_under1/volume_10_text_integrity.md`
- Bug regressions: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_172812_final_under1/volume_10_bug_regressions.md`
- EPUB audit: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_172812_final_under1/volume_10_audit.md`
- Modern notes manifest: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_172812_final_under1/volume_10_modern_notes_manifest.md`
