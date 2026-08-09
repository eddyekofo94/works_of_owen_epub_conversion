# Volume 1 By-Eye Review Packet

Generated: 2026-07-07 19:24 Europe/Paris

Status: pending user eye review. Automated checks passed the Need gate, but strict readiness remains blocked until conversion-affecting changes are committed or otherwise accepted.

EPUB:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/output/volume_1.epub`

## Automated Check Status

- Need gate: PASS (`0.8 < 1.0`)
- EPUB audit: PASS, 0 errors, 0 warnings
- Text anomalies: PASS, 0 suspected anomalies
- Bug regressions: PASS for Volume 1
- Strict readiness: BLOCKED by uncommitted conversion-affecting changes

## Inspect By Eye

1. Cover, title page, NAV/TOC, and colophon.
2. Treatise title pages:
   - `Christologia`
   - `Meditations and Discourses on the Glory of Christ`
   - `Meditations and Discourses on the Glory of Christ Applied to Sinners and Saints`
   - `Two Short Catechisms`
3. Chapter 4: Greek/Latin quotation runs and following English exposition.
4. Chapters 6, 10, 14, 22, 23, 28, 40, 45, and 48: syllabus/list transitions that were whitelisted as audit false positives.
5. Pages represented by dense/top-window whitelist entries, especially source pages 398, 406, 478, and 632.
6. Catechism Q/A sections near the end of the EPUB, including chapter 26 on particular churches.
7. Footnote tap targets and backlinks in chapters with modern citation/translation notes.
8. Greek, Hebrew, and Latin-heavy paragraphs for font choice, spacing, and line height.
9. Long blockquotes and nested list sections on a narrow mobile viewport.

## What To Check

- No visible OCR debris or duplicated text around whitelisted windows.
- Paragraph flow around foreign quotations reads naturally and is not accidentally joined or split.
- Inline syllabus lists remain readable and do not create confusing outline jumps.
- Footnote markers are tappable and appear after punctuation.
- Greek/Hebrew spans render in the correct fonts; Hebrew remains isolated RTL.
- Mobile margins remain comfortable in Apple Books.
- Catechism proof references do not crowd the answer text.
