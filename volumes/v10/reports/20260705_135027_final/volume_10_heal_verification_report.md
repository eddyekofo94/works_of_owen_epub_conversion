# Volume 10 Heal Verification Report

Generated: 2026-07-05
Branch: `heal-v10-20260705`
Archive: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_135027_final`

## Scope

Only Owen Works Volume 10 was repaired, rebuilt, and audited. Hebrews volumes and the other Owen volumes were not converted or audited as part of this heal pass.

## Repair Summary

- Fixed malformed title-page HTML in the Arminianism title page quote block.
- Added Volume 10 OCR/reference repairs for corrupted Jude, 2 Peter, John 10, and Romans 8 references.
- Repaired the raw John 3:3 / John 3:6 split that had moved text across a blockquote boundary.
- Repaired a raw table-continuation fragment in the providence/free-will antithesis so the text is represented as coherent paragraphs and blockquotes.
- Rebuilt `volumes/v10/intermediate/volume_10.json` and `volumes/v10/output/volume_10.epub`.
- Pruned stale Volume 10 whitelist entries that are no longer emitted by the final audits.

No new whitelist entries were added.

## Commands Run

```bash
PATH="$PWD/.venv/bin:$PATH" ./owen v10 --render-only
.venv/bin/python3 scripts/audit_epub.py volumes/v10/output/volume_10.epub --no-bug-log
.venv/bin/python3 scripts/audit_text_integrity.py 10 --no-bug-log
.venv/bin/python3 scripts/audit_anomalies.py 10
.venv/bin/python3 scripts/audit_unmatched_quotes.py 10
.venv/bin/python3 scripts/audit_bug_regressions.py 10
PATH="$PWD/.venv/bin:$PATH" ./owen v10 --extract-only
PATH="$PWD/.venv/bin:$PATH" ./owen v10 --render-only
.venv/bin/python3 -m pytest tests/test_bug_regressions.py
```

The pytest command was run with `OWEN_REGRESSION_VOLUMES="10"` for the report-driven checks. It failed because Volume 10 still emits new modern-notes warning codes and because several tests in the file still check unrelated generated volumes.

## Final Metrics

- Need score: 15.9
- QA level: FULL
- EPUB audit: PASS, 0 errors, 0 warnings
- Text integrity: WARN, 6 warning classes
- Word coverage: 99.94% (`262672` PDF tokens, `263334` EPUB tokens)
- Greek coverage: 100.00%
- Hebrew coverage: 100.00%
- Latin word coverage: 99.58%
- Latin tagging ratio: 58.82%
- Latin translation ratio: 38.82%
- Anomalies: 0
- Unmatched quotation paragraphs: 0
- Bug regressions: WARN, 1 regression budget issue

## Remaining Warning Queues

- Dense source window loss: 3 pages (`107`, `319`, `320`).
- Paragraph split candidates: 1, in `EPUB/ch021.xhtml`.
- Syllabus-anchor candidates: 25 observed; budget is 16.
- Modern notes: 2 unresolved reference candidates.
- Modern notes: 2 substantial foreign passages without high-confidence translation popup.
- Modern notes: 69 existing source footnotes needing editorial enrichment.

## Regression Status

`volume_10_bug_regressions.json` remains WARN because syllabus-anchor candidates exceed the baseline budget and because these text-integrity warning codes are not yet accepted by the v10 baseline:

- `unenriched_legacy_footnotes`
- `unresolved_modern_references`
- `untranslated_substantial_foreign_passages`

These were not suppressed or whitelisted in this pass.

## Archived Reports

This directory contains the final Markdown and JSON reports for:

- EPUB audit
- Text integrity
- Anomalies
- Unmatched quotes
- Bug regressions
- Modern notes manifest

The fresh baseline archive is at:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_022419_baseline`
