# Owen Volumes — QA State Report

Generated: 2026-06-04T08:30:36Z

## Summary

**Need** (0–100): lower is better. Combines coverage, Greek/Hebrew/Latin health, unresolved citations, splits, warnings, and QA completeness into a single score. Volumes ranked worst first.

| Rank | Vol | Need | Font | Treatises | Coverage | Greek | Hebrew | Latin | Unres | QA Level |
|------|-----|------|------|-----------|----------|-------|--------|-------|-------|----------|
| 1 | 16 | 80.9 | gentium-plus-2 | 5 |  99.59 |   99.3 |  99.01 |      ? | 4 | FULL |
| 2 | 12 | 75.6 | arno-pro | 3 |   99.6 |  99.92 |  99.55 |  99.82 | 0 | PRISTINE |
| 3 | 5 | 62.2 | brill-font | 2 |  99.69 |  99.73 |  99.19 |      ? | 2 | FULL |
| 4 | 13 | 58.0 | baskerville | 5 |  89.75 |  96.19 |  100.0 |      ? | 0 | FULL |
| 5 | 10 | 51.5 | brill-font | 4 |  99.47 |  99.75 |  100.0 |      ? | 4 | FULL |
| 6 | 11 | 51.2 | minion-pro | 1 |  97.63 |   99.7 |  100.0 |      ? | 4 | FULL |
| 7 | 2 | 50.7 | libertinus | 3 |  99.68 |  99.77 |  100.0 |      ? | 2 | FULL |
| 8 | 4 | 50.4 | cardo | 4 |  99.67 |  99.71 |  100.0 |      ? | 8 | FULL |
| 9 | 7 | 41.3 | sabon-next-lt | 3 |  99.68 |  100.0 |  100.0 |      ? | 2 | FULL |
| 10 | 15 | 40.2 | sabon-next-lt | 3 |  99.67 |  100.0 |  100.0 |      ? | 4 | FULL |
| 11 | 6 | 39.4 | baskerville | 4 |  99.54 |  100.0 |  100.0 |      ? | 0 | FULL |
| 12 | 8 | 38.9 | gentium-plus-2 | 16 |  99.65 |  100.0 |  100.0 |      ? | 10 | FULL |
| 13 | 14 | 36.8 | brill-font | 2 |  99.69 |  100.0 |  100.0 |      ? | 6 | FULL |
| 14 | 9 | 36.6 | cardo | 3 |  99.61 |  100.0 |  100.0 |      ? | 0 | FULL |
| 15 | 1 | 33.9 | adobe-garamond-pro-2-2 | 4 |  99.92 |  99.87 |  100.0 |  99.71 | 0 | PRISTINE |
| 16 | 3 | 11.6 | minion-pro | 1 |  99.98 |  100.0 |  100.0 |  99.95 | 0 | PRISTINE |

## Per-Volume Details

### Volume 16 — Need: 80.9 (❌ Poor) — Rank 1

- **Body font:** gentium-plus-2
- **Source type:** ages_pdf
- **Treatises:** 5
- **QA level:** FULL
- **convert.py:** Yes (207 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 99.59
- **Greek coverage:** 99.30
- **Hebrew coverage:** 99.01
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=40, unresolved=4
- **Splits:** 28
- **Regressions:** 0
- **Suspected anomalies:** 299
- **Recommended:** translate_unresolved_citations; 🔍 Review OCR anomalies

### Volume 12 — Need: 75.6 (❌ Poor) — Rank 2

- **Body font:** arno-pro
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** PRISTINE
- **convert.py:** Yes (225 lines, 1 text_replacements)
- **Audit:** errors=1, warnings=3, footnotes=None
- **Word coverage:** 99.60
- **Greek coverage:** 99.92
- **Hebrew coverage:** 99.55
- **Latin coverage:** 99.82
- **Latin tagging:** 59.14
- **Latin translation:** 30.77
- **Citations:** total=70, unresolved=0
- **Splits:** 276
- **Regressions:** 2
- **Suspected anomalies:** 663
- **Recommended:** 🔍 Review OCR anomalies

### Volume 5 — Need: 62.2 (❌ Poor) — Rank 3

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 2
- **QA level:** FULL
- **convert.py:** Yes (118 lines, 1 text_replacements)
- **Audit:** errors=1, warnings=1, footnotes=None
- **Word coverage:** 99.69
- **Greek coverage:** 99.73
- **Hebrew coverage:** 99.19
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=45, unresolved=2
- **Splits:** 78
- **Regressions:** 5
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 13 — Need: 58.0 (🩷 Needs work) — Rank 4

- **Body font:** baskerville
- **Source type:** ages_pdf
- **Treatises:** 5
- **QA level:** FULL
- **convert.py:** Yes (281 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 89.75
- **Greek coverage:** 96.19
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=18, unresolved=0
- **Splits:** 76
- **Regressions:** 1
- **Suspected anomalies:** None
- **Recommended:** ⚠️ Investigate low word coverage

### Volume 10 — Need: 51.5 (🩷 Needs work) — Rank 5

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (239 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.47
- **Greek coverage:** 99.75
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=20, unresolved=4
- **Splits:** 158
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 11 — Need: 51.2 (🩷 Needs work) — Rank 6

- **Body font:** minion-pro
- **Source type:** ages_pdf
- **Treatises:** 1
- **QA level:** FULL
- **convert.py:** Yes (97 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 97.63
- **Greek coverage:** 99.70
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=52, unresolved=4
- **Splits:** 143
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 2 — Need: 50.7 (🩷 Needs work) — Rank 7

- **Body font:** libertinus
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (141 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.68
- **Greek coverage:** 99.77
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=3, unresolved=2
- **Splits:** 179
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 4 — Need: 50.4 (🩷 Needs work) — Rank 8

- **Body font:** cardo
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (192 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.67
- **Greek coverage:** 99.71
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=16, unresolved=8
- **Splits:** 75
- **Regressions:** 7
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 7 — Need: 41.3 (🩷 Needs work) — Rank 9

- **Body font:** sabon-next-lt
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (147 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.68
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=4, unresolved=2
- **Splits:** 126
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 15 — Need: 40.2 (🩷 Needs work) — Rank 10

- **Body font:** sabon-next-lt
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (194 lines, 2 text_replacements)
- **Audit:** errors=1, warnings=1, footnotes=None
- **Word coverage:** 99.67
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=59, unresolved=4
- **Splits:** 105
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 6 — Need: 39.4 (👌 Fair) — Rank 11

- **Body font:** baskerville
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (247 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.54
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=0, unresolved=0
- **Splits:** 193
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 8 — Need: 38.9 (👌 Fair) — Rank 12

- **Body font:** gentium-plus-2
- **Source type:** ages_pdf
- **Treatises:** 16
- **QA level:** FULL
- **convert.py:** Yes (134 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.65
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=38, unresolved=10
- **Splits:** 125
- **Regressions:** 1
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 14 — Need: 36.8 (👌 Fair) — Rank 13

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 2
- **QA level:** FULL
- **convert.py:** Yes (195 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 99.69
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=63, unresolved=6
- **Splits:** 75
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 9 — Need: 36.6 (👌 Fair) — Rank 14

- **Body font:** cardo
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (140 lines, 0 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.61
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** ?
- **Latin tagging:** ?
- **Latin translation:** ?
- **Citations:** total=0, unresolved=0
- **Splits:** 186
- **Regressions:** 5
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 1 — Need: 33.9 (👌 Fair) — Rank 15

- **Body font:** adobe-garamond-pro-2-2
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** PRISTINE
- **convert.py:** Yes (542 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.92
- **Greek coverage:** 99.87
- **Hebrew coverage:** 100.00
- **Latin coverage:** 99.71
- **Latin tagging:** 0.00
- **Latin translation:** 100.00
- **Citations:** total=49, unresolved=0
- **Splits:** 19
- **Regressions:** 0
- **Suspected anomalies:** 45
- **Recommended:** 🔍 Review OCR anomalies

### Volume 3 — Need: 11.6 (✅ Good) — Rank 16

- **Body font:** minion-pro
- **Source type:** ages_pdf
- **Treatises:** 1
- **QA level:** PRISTINE
- **convert.py:** Yes (163 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=0, footnotes=None
- **Word coverage:** 99.98
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Latin coverage:** 99.95
- **Latin tagging:** 50.82
- **Latin translation:** 81.40
- **Citations:** total=25, unresolved=0
- **Splits:** 0
- **Regressions:** 0
- **Suspected anomalies:** 30
- **Recommended:** 🔍 Review OCR anomalies
