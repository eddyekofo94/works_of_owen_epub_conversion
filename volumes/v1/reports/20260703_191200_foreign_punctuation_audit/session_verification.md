# Volume 1 Foreign Punctuation Verification

Date: 2026-07-03

Status: IMPLEMENTED (AWAITING VALIDATION)

## Scope

This pass targeted Greek/Hebrew span punctuation defects around `volumes/v1/bugs_fixes/textual.txt` items #24 and #59. It specifically checked for:

- Foreign-script title/gloss quote bleed, such as `</span>", Songs of Degrees,"`.
- Foreign-script closing quote glued to a following English word, such as `</span>"like`.
- Quote-adjacent Greek/Hebrew spans that are not high-confidence failures but should remain visible for review.

## Repairs Applied

- `EPUB/ch023.xhtml`: `Songs of Degrees,"` no longer appears. The rendered phrase is now:
  `whose titles are <span lang="he" xml:lang="he" dir="rtl">"צִֹירֵי המעְלוֹת"</span>, Songs of Degrees, or rather ascents`.
- `EPUB/ch027.xhtml`: `ἰσάγγελοι</span>"like` no longer appears. The rendered phrase is now:
  `for we shall be "<span lang="el" xml:lang="el">ἰσάγγελοι</span>" like unto angels`.

## Verification Commands

- `.venv/bin/python3 -m pytest tests/test_bug_regressions.py::test_issue_59_v1_songs_of_degrees_gloss_drops_stray_closing_quote tests/test_bug_regressions.py::test_foreign_span_quote_bleed_audit_catches_unquoted_english_gloss -q`
- `.venv/bin/python3 volumes/v1/convert.py --render-only`
- `.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub --out-dir volumes/v1/reports/20260703_191200_foreign_punctuation_audit --no-bug-log`
- `.venv/bin/python3 scripts/audit_foreign_punctuation.py 1 --out-dir volumes/v1/reports/20260703_191200_foreign_punctuation_audit`
- `.venv/bin/python3 scripts/audit_text_integrity.py 1 --out-dir volumes/v1/reports/20260703_191200_foreign_punctuation_audit --no-bug-log`
- `.venv/bin/python3 scripts/audit_bug_regressions.py 1`

## Results

- Focused regression tests: PASS, 2 tests.
- Direct EPUB string checks: `Songs of Degrees,"` absent; `</span>"like` absent.
- EPUB audit: PASS, 0 errors, 0 warnings.
- EPUB foreign punctuation high-confidence detectors:
  - `foreign_span_quote_bleed_files`: 0
  - `foreign_span_quote_word_glue_files`: 0
- Foreign punctuation inventory: PASS, 156 Greek/Hebrew span contexts scanned, 0 warnings, 95 review-only contexts recorded.
- Text integrity audit: WARN, 7 existing broader warning categories.
- Bug regression audit: PASS.

## Notes

The 95 review-only foreign punctuation contexts are intentionally not treated as failures. Most are normal Owen patterns where a Greek or Hebrew term sits inside a quoted sentence or beside an English translation. They remain fully enumerated in `volume_1_foreign_punctuation.json` and partially listed in `volume_1_foreign_punctuation.md` so future checks can audit them without rereading the EPUB manually.
