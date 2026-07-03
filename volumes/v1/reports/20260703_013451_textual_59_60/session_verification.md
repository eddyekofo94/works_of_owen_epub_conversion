# Volume 1 Textual #59-60 Verification

Date: 2026-07-03

## Scope

- Targeted `volumes/v1/bugs_fixes/textual.txt` items #59 and #60 only.
- Rebuilt Volume 1 from cached JSON with `volumes/v1/convert.py --render-only`.

## Changes Verified

1. `EPUB/ch023.xhtml`
   - Before: `"צִֹירֵי המעְלוֹת", Songs of Degrees,"`
   - Corrected in the follow-up report `../20260703_185846_textual_59_quote_fix/session_verification.md`.
   - Final after: `<span lang="he" xml:lang="he" dir="rtl">"צִֹירֵי המעְלוֹת"</span>, Songs of Degrees, or rather ascents...`
   - The Hebrew title remains language-tagged with `lang="he"` and `dir="rtl"`.

2. `EPUB/ch005.xhtml`
   - Before: `(2.) Doctrinal...` rendered as a separate block paragraph after `(1.) Real;`.
   - After: `The foundation of the church is twofold: (1.) Real; (2.) Doctrinal. And in both ways...` renders in one syllabus-anchor paragraph.

## Reports

- EPUB audit: `volume_1_audit.md` / `volume_1_audit.json`
  - Status: PASS
  - Errors: 0
  - Warnings: 0
  - Greek chars: 4091; untagged Greek chars: 0
  - Hebrew chars: 157; untagged Hebrew chars: 0

- Text-integrity audit: `volume_1_text_integrity.md` / `volume_1_text_integrity.json`
  - Status: WARN
  - Warnings: 7
  - PDF pages: 633
  - PDF-to-EPUB coverage ratio: 0.9996
  - Possible faulty paragraph splits: 13
  - Syllabus-anchor candidates: 16
  - Greek word coverage ratio: 1.0
  - Hebrew word coverage ratio: 1.0
  - Latin word coverage ratio: 0.999
  - Remaining warnings are the existing broader v1 queues, including dense source-window loss, paragraph split candidates, syllabus-anchor candidates, and modern-note queues.

- Bug-regression report: `volume_1_bug_regressions.md` / `volume_1_bug_regressions.json`
  - Status: PASS

## Test Notes

- Focused pytest coverage for the two new regressions and existing issue #50 binary syllabus coverage passed.
- Full `tests/test_bug_regressions.py` was also attempted. It failed on pre-existing/global hygiene issues: v1 modern-note warning codes not present in the current baseline, stale unused whitelist entries across volumes 1, 8, 10, 11, 12, 13, and 15, and existing v11 split-word anomalies. These failures are outside the #59-60 patch path.
