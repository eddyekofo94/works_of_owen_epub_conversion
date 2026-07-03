# Volume 1 Textual #59 Quote Placement Verification

Date: 2026-07-03

## Scope

- Corrected the Volume 1 textual #59 quote placement around the Hebrew title and English gloss.
- Rebuilt Volume 1 with `volumes/v1/convert.py --render-only`.

## Direct XHTML Verification

Target file: `EPUB/ch023.xhtml`

Verified rendered XHTML:

```html
whose titles are <span lang="he" xml:lang="he" dir="rtl">"צִֹירֵי המעְלוֹת"</span>, Songs of Degrees, or rather ascents
```

Negative checks passed:

- No `are "<span lang="he"...` opener remains outside the Hebrew span.
- No `Songs of Degrees,"` trailing quote remains.

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
  - EPUB text files: 83
  - EPUB paragraphs/headings: 2692
  - PDF content tokens: 191893
  - EPUB content tokens: 205236
  - PDF-to-EPUB coverage ratio: 0.9996
  - Possible faulty paragraph splits: 13
  - Syllabus-anchor candidates: 16
  - Greek word coverage ratio: 1.0
  - Hebrew word coverage ratio: 1.0
  - Latin word coverage ratio: 0.999

Remaining warnings are the existing broader v1 queues: weak page coverage, dense source-window loss, top-of-page text loss, paragraph split candidates, syllabus-anchor candidates, unresolved modern references, and untranslated substantial foreign passages.

## Tests

- `tests/test_bug_regressions.py::test_issue_59_v1_songs_of_degrees_gloss_drops_stray_closing_quote` passed.
