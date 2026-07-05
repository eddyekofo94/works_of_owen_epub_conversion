# Volume 10 Heal Checkpoint Report

Generated: 2026-07-05 17:18
Branch: `heal-v10-20260705`
Archive: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_171118`

## Scope

Only Owen Works Volume 10 was rebuilt, audited, and modified in this continuation pass.

## Change Applied

- Added citation metadata to two existing `BODY_TRANSLATIONS` entries in `scripts/translation_db.py`.
- The affected passages are already translated by Owen in nearby text, so the modern-notes system now emits citation popups only, suppressing duplicate translation popups:
  - Arnold of Bonneval, `De Cardinalibus Operibus Christi`, Sermon 7, formerly attributed to Cyprian.
  - Prosper of Aquitaine, `De Vocatione Omnium Gentium`, Book 1, Chapter 3.

No source text was changed. No new whitelist entries were added.

## Before / After

- Need score: `15.9` -> `12.9`
- Text-integrity warning classes: `6` -> `4`
- Unresolved modern references: `2` -> `0`
- Untranslated substantial foreign passages: `2` -> `0`
- Body citation popups in modern-notes manifest: `15` -> `17`
- Unenriched legacy footnotes: remains `69`
- EPUB audit: remains `0` errors, `0` warnings
- Anomalies: remains `0`
- Unmatched quotation paragraphs: remains `0`

## Verification Commands

```bash
PATH="$PWD/.venv/bin:$PATH" ./owen v10 --render-only
.venv/bin/python3 -m pytest tests/test_modern_notes.py
.venv/bin/python3 scripts/run_all_checks.py 10
.venv/bin/python3 scripts/report_volume_state.py --volumes 10 --no-readme
```

## Verification Status

- Render-only build: PASS.
- `tests/test_modern_notes.py`: PASS, `4 passed`.
- Volume 10 rebuild and target audits inside `scripts/run_all_checks.py 10`: PASS for converter, EPUB audit, text-integrity execution, bug-regression execution, anomalies, and report archiving.
- Full pytest step inside `scripts/run_all_checks.py 10`: FAIL, `9 failed, 455 passed, 11 skipped`. This is repository-wide pytest, not limited to the two modern-note records changed in this pass.
- Current Volume 10 status remains WARN because Need is `12.9`, above the project-local strict target `<1.0`.

## Current Metrics

- Need score: `12.9`
- QA level: `FULL`
- Word coverage: `99.94%`
- Greek coverage: `100.00%`
- Hebrew coverage: `100.00%`
- Latin word coverage: `99.58%`
- Latin tagging ratio: `58.82%`
- Latin translation ratio: `38.82%`
- Text-integrity warnings: `4`
- Bug-regression over-budget checks: `1`

## Remaining Blockers

- `unenriched_legacy_footnotes`: 69 existing source footnotes still need editorial enrichment. This is the largest remaining Need-score penalty and requires source-by-source citation or translation judgment.
- `syllabus_anchor_candidates`: 25 candidates remain against the current v10 budget of 16. The refreshed text-integrity report labels the displayed candidates as `likely_false_positive`, but they have not been formally retired or budget-adjusted.
- `dense_source_window_loss`: 3 pages remain flagged: 107, 319, 320.
- `paragraph_split_candidates`: 1 candidate remains in `EPUB/ch021.xhtml`; inspection shows a chapter-summary line followed by a standalone Roman numeral outline item, so an automatic merge would be unsafe.
- Latin tagging and translation coverage remain below the strict PRISTINE target.

## Key Report Paths

- EPUB: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/output/volume_10.epub`
- Text integrity: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/bugs_fixes/volume_10_text_integrity.md`
- Bug regressions: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/bugs_fixes/volume_10_bug_regressions.md`
- Modern notes manifest: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_170941_modern_notes/volume_10_modern_notes_manifest.md`
- Archived reports: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v10/reports/20260705_171118`
