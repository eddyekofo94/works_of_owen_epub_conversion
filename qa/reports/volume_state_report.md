# Owen Volumes — QA State Report

Generated: 2026-06-05T16:11:10Z

## Summary

**Need** (0–100): lower is better. Combines coverage, Greek/Hebrew/Latin health, unresolved citations, splits, warnings, and QA completeness into a single score. Volumes ranked worst first.

| Rank | Vol | Need | Font | Treatises | Coverage | Greek | Hebrew | Latin | Unres | QA Level |
|------|-----|------|------|-----------|----------|-------|--------|-------|-------|----------|
| 1 | 2 | 66.4 | libertinus | 3 |  99.48 |  99.77 |  100.0 |   99.5 | 2 | FULL |
| 2 | 5 | 66.2 | brill-font | 2 |  98.07 |  99.73 |  99.19 |  98.91 | 2 | FULL |
| 3 | 12 | 60.8 | arno-pro | 3 |   99.9 |  99.92 |  99.55 |   99.7 | 0 | PRISTINE |
| 4 | 13 | 58.0 | baskerville | 5 |  89.75 |  96.19 |  100.0 |      ? | 0 | FULL |
| 5 | 10 | 51.5 | brill-font | 4 |  99.47 |  99.75 |  100.0 |      ? | 4 | FULL |
| 6 | 11 | 51.2 | minion-pro | 1 |  97.63 |   99.7 |  100.0 |      ? | 4 | FULL |
| 7 | 4 | 50.4 | cardo | 4 |  99.67 |  99.71 |  100.0 |      ? | 8 | FULL |
| 8 | 7 | 41.3 | sabon-next-lt | 3 |  99.68 |  100.0 |  100.0 |      ? | 2 | FULL |
| 9 | 15 | 40.2 | sabon-next-lt | 3 |  99.67 |  100.0 |  100.0 |      ? | 4 | FULL |
| 10 | 6 | 39.4 | baskerville | 4 |  99.54 |  100.0 |  100.0 |      ? | 0 | FULL |
| 11 | 16 | 39.3 | gentium-plus-2 | 5 |  99.92 |   99.5 |  100.0 |  99.88 | 0 | PRISTINE |
| 12 | 8 | 38.9 | gentium-plus-2 | 16 |  99.65 |  100.0 |  100.0 |      ? | 10 | FULL |
| 13 | 14 | 36.8 | brill-font | 2 |  99.69 |  100.0 |  100.0 |      ? | 6 | FULL |
| 14 | 9 | 36.6 | cardo | 3 |  99.61 |  100.0 |  100.0 |      ? | 0 | FULL |
| 15 | 1 | 35.9 | adobe-garamond-pro-2-2 | 4 |  99.92 |  99.87 |  100.0 |  99.74 | 0 | PRISTINE |
| 16 | 3 | 11.6 | minion-pro | 1 |  99.98 |  100.0 |  100.0 |  99.95 | 0 | PRISTINE |

## Per-Volume Details

### Volume 2 — Need: 66.4 (❌ Poor) — Rank 1

- **Body font:** libertinus
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (164 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.48
- **Greek coverage:** 99.77
- **Hebrew coverage:** 100.00
- **Latin coverage:** 99.50
- **Latin tagging:** 22.26
- **Latin translation:** 24.26
- **Citations:** total=3, unresolved=2
- **Splits:** 15
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 5 — Need: 66.2 (❌ Poor) — Rank 2

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 2
- **QA level:** FULL
- **convert.py:** Yes (136 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 98.07
- **Greek coverage:** 99.73
- **Hebrew coverage:** 99.19
- **Latin coverage:** 98.91
- **Latin tagging:** 70.91
- **Latin translation:** 59.89
- **Citations:** total=45, unresolved=2
- **Splits:** 7
- **Regressions:** 5
- **Suspected anomalies:** None
- **Recommended:** translate_unresolved_citations

### Volume 12 — Need: 60.8 (❌ Poor) — Rank 3

- **Body font:** arno-pro
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** PRISTINE
- **convert.py:** Yes (232 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=3, footnotes=None
- **Word coverage:** 99.90
- **Greek coverage:** 99.92
- **Hebrew coverage:** 99.55
- **Latin coverage:** 99.70
- **Latin tagging:** 60.86
- **Latin translation:** 40.71
- **Citations:** total=70, unresolved=0
- **Splits:** 40
- **Regressions:** 1
- **Suspected anomalies:** 663
- **Recommended:** 🔍 Review OCR anomalies

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

### Volume 4 — Need: 50.4 (🩷 Needs work) — Rank 7

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

### Volume 7 — Need: 41.3 (🩷 Needs work) — Rank 8

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

### Volume 15 — Need: 40.2 (🩷 Needs work) — Rank 9

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

### Volume 6 — Need: 39.4 (👌 Fair) — Rank 10

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

### Volume 16 — Need: 39.3 (👌 Fair) — Rank 11

- **Body font:** gentium-plus-2
- **Source type:** ages_pdf
- **Treatises:** 5
- **QA level:** PRISTINE
- **convert.py:** Yes (261 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.92
- **Greek coverage:** 99.50
- **Hebrew coverage:** 100.00
- **Latin coverage:** 99.88
- **Latin tagging:** 40.49
- **Latin translation:** 42.20
- **Citations:** total=40, unresolved=0
- **Splits:** 2
- **Regressions:** 0
- **Suspected anomalies:** 57
- **Recommended:** 🔍 Review OCR anomalies

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

### Volume 1 — Need: 35.9 (👌 Fair) — Rank 15

- **Body font:** adobe-garamond-pro-2-2
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** PRISTINE
- **convert.py:** Yes (561 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.92
- **Greek coverage:** 99.87
- **Hebrew coverage:** 100.00
- **Latin coverage:** 99.74
- **Latin tagging:** 33.36
- **Latin translation:** 55.17
- **Citations:** total=49, unresolved=0
- **Splits:** 19
- **Regressions:** 0
- **Suspected anomalies:** 26
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
