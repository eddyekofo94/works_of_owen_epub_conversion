# Owen Volumes — QA State Report

Generated: 2026-06-03T11:43:09Z

## Summary

**Need** (0–100): lower is better. Combines coverage, Greek/Hebrew health, splits, warnings, and QA completeness into a single score. Volumes ranked worst first.

| Rank | Vol | Need | Font | Treatises | Coverage | Greek | Hebrew | Anomalies | QA Level |
|------|-----|------|------|-----------|----------|-------|--------|-----------|----------|
| 1 | 12 | 74.5 | arno-pro | 3 |    93.81 |    89.79 |    99.55 | 663 | FULL |
| 2 | 3 | 72.0 | minion-pro | 1 |    98.53 |    99.36 |     95.8 | 598 | FULL |
| 3 | 16 | 70.4 | gentium-plus-2 | 5 |    99.59 |     99.3 |    99.01 | 299 | FULL |
| 4 | 5 | 52.5 | brill-font | 2 |    99.69 |    99.73 |    99.19 | None | FULL |
| 5 | 13 | 49.0 | baskerville | 5 |    89.75 |    96.19 |    100.0 | None | FULL |
| 6 | 11 | 41.0 | minion-pro | 1 |    97.63 |     99.7 |    100.0 | None | FULL |
| 7 | 10 | 39.5 | brill-font | 4 |    99.47 |    99.75 |    100.0 | None | FULL |
| 8 | 4 | 33.9 | cardo | 4 |    99.67 |    99.71 |    100.0 | None | FULL |
| 9 | 2 | 31.7 | libertinus | 3 |    99.68 |    99.77 |    100.0 | None | FULL |
| 10 | 6 | 30.4 | baskerville | 4 |    99.54 |    100.0 |    100.0 | None | FULL |
| 11 | 15 | 30.2 | sabon-next-lt | 3 |    99.67 |    100.0 |    100.0 | None | FULL |
| 12 | 1 | 28.7 | adobe-garamond-pro-2-2 | 4 |    99.68 |    99.87 |    100.0 | None | FULL |
| 13 | 9 | 27.6 | cardo | 3 |    99.61 |    100.0 |    100.0 | None | FULL |
| 14 | 14 | 26.4 | brill-font | 2 |    99.69 |    100.0 |    100.0 | None | FULL |
| 15 | 8 | 26.0 | gentium-plus-2 | 16 |    99.65 |    100.0 |    100.0 | None | FULL |
| 16 | 7 | 24.8 | sabon-next-lt | 3 |    99.68 |    100.0 |    100.0 | None | FULL |

## Per-Volume Details

### Volume 12 — Need: 74.5 (❌ Poor) — Rank 1

- **Body font:** arno-pro
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (163 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=3, footnotes=None
- **Word coverage:** 93.81
- **Greek coverage:** 89.79
- **Hebrew coverage:** 99.55
- **Splits:** 257
- **Regressions:** 5
- **Suspected anomalies:** 663
- **Recommended:** 🔤 Investigate Greek extraction; 🔍 Review OCR anomalies

### Volume 3 — Need: 72.0 (❌ Poor) — Rank 2

- **Body font:** minion-pro
- **Source type:** ages_pdf
- **Treatises:** 1
- **QA level:** FULL
- **convert.py:** Yes (115 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 98.53
- **Greek coverage:** 99.36
- **Hebrew coverage:** 95.80
- **Splits:** 161
- **Regressions:** 0
- **Suspected anomalies:** 598
- **Recommended:** 🔍 Review OCR anomalies

### Volume 16 — Need: 70.4 (❌ Poor) — Rank 3

- **Body font:** gentium-plus-2
- **Source type:** ages_pdf
- **Treatises:** 5
- **QA level:** FULL
- **convert.py:** Yes (206 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 99.59
- **Greek coverage:** 99.30
- **Hebrew coverage:** 99.01
- **Splits:** 28
- **Regressions:** 0
- **Suspected anomalies:** 299
- **Recommended:** 🔍 Review OCR anomalies

### Volume 5 — Need: 52.5 (🩷 Needs work) — Rank 4

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 2
- **QA level:** FULL
- **convert.py:** Yes (118 lines, 1 text_replacements)
- **Audit:** errors=1, warnings=1, footnotes=None
- **Word coverage:** 99.69
- **Greek coverage:** 99.73
- **Hebrew coverage:** 99.19
- **Splits:** 78
- **Regressions:** 5
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 13 — Need: 49.0 (🩷 Needs work) — Rank 5

- **Body font:** baskerville
- **Source type:** ages_pdf
- **Treatises:** 5
- **QA level:** FULL
- **convert.py:** Yes (281 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 89.75
- **Greek coverage:** 96.19
- **Hebrew coverage:** 100.00
- **Splits:** 76
- **Regressions:** 1
- **Suspected anomalies:** None
- **Recommended:** ⚠️ Investigate low word coverage

### Volume 11 — Need: 41.0 (🩷 Needs work) — Rank 6

- **Body font:** minion-pro
- **Source type:** ages_pdf
- **Treatises:** 1
- **QA level:** FULL
- **convert.py:** Yes (97 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 97.63
- **Greek coverage:** 99.70
- **Hebrew coverage:** 100.00
- **Splits:** 143
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 10 — Need: 39.5 (👌 Fair) — Rank 7

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (203 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.47
- **Greek coverage:** 99.75
- **Hebrew coverage:** 100.00
- **Splits:** 158
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 4 — Need: 33.9 (👌 Fair) — Rank 8

- **Body font:** cardo
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (192 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.67
- **Greek coverage:** 99.71
- **Hebrew coverage:** 100.00
- **Splits:** 75
- **Regressions:** 7
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 2 — Need: 31.7 (👌 Fair) — Rank 9

- **Body font:** libertinus
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (140 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.68
- **Greek coverage:** 99.77
- **Hebrew coverage:** 100.00
- **Splits:** 179
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 6 — Need: 30.4 (👌 Fair) — Rank 10

- **Body font:** baskerville
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (162 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.54
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 193
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 15 — Need: 30.2 (👌 Fair) — Rank 11

- **Body font:** sabon-next-lt
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (166 lines, 2 text_replacements)
- **Audit:** errors=1, warnings=1, footnotes=None
- **Word coverage:** 99.67
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 105
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 1 — Need: 28.7 (👌 Fair) — Rank 12

- **Body font:** adobe-garamond-pro-2-2
- **Source type:** ages_pdf
- **Treatises:** 4
- **QA level:** FULL
- **convert.py:** Yes (540 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.68
- **Greek coverage:** 99.87
- **Hebrew coverage:** 100.00
- **Splits:** 101
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 9 — Need: 27.6 (👌 Fair) — Rank 13

- **Body font:** cardo
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (140 lines, 0 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.61
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 186
- **Regressions:** 5
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 14 — Need: 26.4 (👌 Fair) — Rank 14

- **Body font:** brill-font
- **Source type:** ages_pdf
- **Treatises:** 2
- **QA level:** FULL
- **convert.py:** Yes (195 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=2, footnotes=None
- **Word coverage:** 99.69
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 75
- **Regressions:** 0
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 8 — Need: 26.0 (👌 Fair) — Rank 15

- **Body font:** gentium-plus-2
- **Source type:** ages_pdf
- **Treatises:** 16
- **QA level:** FULL
- **convert.py:** Yes (134 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.65
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 125
- **Regressions:** 1
- **Suspected anomalies:** None
- **Recommended:** 

### Volume 7 — Need: 24.8 (👌 Fair) — Rank 16

- **Body font:** sabon-next-lt
- **Source type:** ages_pdf
- **Treatises:** 3
- **QA level:** FULL
- **convert.py:** Yes (147 lines, 1 text_replacements)
- **Audit:** errors=0, warnings=1, footnotes=None
- **Word coverage:** 99.68
- **Greek coverage:** 100.00
- **Hebrew coverage:** 100.00
- **Splits:** 126
- **Regressions:** 3
- **Suspected anomalies:** None
- **Recommended:** 
