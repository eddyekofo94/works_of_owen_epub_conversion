# Volume h2 — Comprehensive Need Score Reduction Plan

> Current Need: **28.7** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.81% | **7.6** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 97.40% | **10.0** | YES |
| Latin tagging | 70.6% | **2.9** | no |
| Latin translation | 11.8% | **5.0** | no |
| Unresolved citations | 39/87 | **6.7** | no |
| Splits | 40 | **10.0** | YES |
| Audit warnings | 1 | **2.0** | no |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 154 | **10.0** | YES |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **54.3** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 10.0 | 0.0 | 7.6 | **28.7** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 7.6 | **7.6** |
| **Whitelist quotes only** | 10.0 | 0.0 | 7.6 | **17.6** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 7.6 | **7.6** |

The coverage gap alone contributes **7.6** points. 
Reducing this requires finding and fixing missing content in the EPUB.
The dominant penalty is **Latin word coverage** at **10.0** points.

## Anomaly Breakdown

| Category | Count | Legitimate? | Fixable? |
|---|---|---|---|
| Hyphenation Anomalies | 33 | See analysis | See analysis |
| Punctuation Spacing Blemishes | 0 | See analysis | See analysis |
| OCR & Bracket Residues | 0 | See analysis | See analysis |
| Mixed-Case Capitalization Errors | 2 | See analysis | See analysis |
| Unresolved Citation References | 29 | See analysis | See analysis |
| Structural Nesting Sequence Jumps | 64 | See analysis | See analysis |
| Invalid Bible References | 1 | See analysis | See analysis |
| List Formatting Inconsistencies | 0 | See analysis | See analysis |
| Unmatched Quotation Marks | 25 | See analysis | See analysis |

### Structural Nesting Sequence Jumps

**64 jumps** — all are sermon numbers or legitimate list starts:
- `5. ... 8.` — List sequence jump (skipped from 5 to 8) (XXV. —The office of priesthood)
- `2. ... 14.` — List sequence jump (skipped from 2 to 14) (XXV. —The office of priesthood)
- `11. ... 17.` — List sequence jump (skipped from 11 to 17) (XXV. —The office of priesthood)
- `9. ... 11.` — List sequence jump (skipped from 9 to 11) (XXVI. —Of the origin of the priesthood of Christ)
- `11. ... 13.` — List sequence jump (skipped from 11 to 13) (XXVI. —Of the origin of the priesthood of Christ)
- `2. ... 17.` — List sequence jump (skipped from 2 to 17) (XXVII. —The original of the priesthood of Christ in the counsel of God)
- `1. ... 14.` — List sequence jump (skipped from 1 to 14) (XXVII. —The original of the priesthood of Christ in the counsel of God)
- `9. ... 14.` — List sequence jump (skipped from 9 to 14) (XXVII. —The original of the priesthood of Christ in the counsel of God)
- `3. ... 8.` — List sequence jump (skipped from 3 to 8) (XXVIII. —Federal transactions between the Father and the Son)
- `9. ... 11.` — List sequence jump (skipped from 9 to 11) (XXVIII. —Federal transactions between the Father and the Son)
- `9. ... 18.` — List sequence jump (skipped from 9 to 18) (XXVIII. —Federal transactions between the Father and the Son)
- `9. ... 19.` — List sequence jump (skipped from 9 to 19) (XXVIII. —Federal transactions between the Father and the Son)
- `3. ... 15.` — List sequence jump (skipped from 3 to 15) (XXIX. —The necessity of the priesthood of Christ on the supposition of sin and grace)
- `15. ... 21.` — List sequence jump (skipped from 15 to 21) (XXIX. —The necessity of the priesthood of Christ on the supposition of sin and grace)
- `14. ... 22.` — List sequence jump (skipped from 14 to 22) (XXIX. —The necessity of the priesthood of Christ on the supposition of sin and grace)
- `8. ... 10.` — List sequence jump (skipped from 8 to 10) (XXXI. —The nature of the priesthood of Christ)
- `8. ... 13.` — List sequence jump (skipped from 8 to 13) (XXXI. —The nature of the priesthood of Christ)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (XXXII. —The nature of the priesthood of Christ)
- `2. ... 5.` — List sequence jump (skipped from 2 to 5) (XXXII. —The nature of the priesthood of Christ)
- `5. ... 10.` — List sequence jump (skipped from 5 to 10) (XXXII. —The nature of the priesthood of Christ)
- `13. ... 19.` — List sequence jump (skipped from 13 to 19) (XXXIII. —Of the acts of the priesthood of Christ, their object, with the time and place of its)
- `6. ... 10.` — List sequence jump (skipped from 6 to 10) (XXXIII. —Of the acts of the priesthood of Christ, their object, with the time and place of its)
- `8. ... 13.` — List sequence jump (skipped from 8 to 13) (XXXIII. —Of the acts of the priesthood of Christ, their object, with the time and place of its)
- `7. ... 17.` — List sequence jump (skipped from 7 to 17) (XXXIV. —Prefigurations of the priesthood and sacrifice of Christ)
- `3. ... 14.` — List sequence jump (skipped from 3 to 14) (I. —Differences concerning a day of sacred rest—Principles directing to the observance of it—Th)
- `4. ... 16.` — List sequence jump (skipped from 4 to 16) (II. —Of the original of the Sabbath)
- `11. ... 15.` — List sequence jump (skipped from 11 to 15) (II. —Of the original of the Sabbath)
- `8. ... 12.` — List sequence jump (skipped from 8 to 12) (II. —Of the original of the Sabbath)
- `13. ... 16.` — List sequence jump (skipped from 13 to 16) (II. —Of the original of the Sabbath)
- `17. ... 20.` — List sequence jump (skipped from 17 to 20) (II. —Of the original of the Sabbath)
- `16. ... 20.` — List sequence jump (skipped from 16 to 20) (III. —Of the causes of the Sabbath)
- `1. ... 34.` — List sequence jump (skipped from 1 to 34) (III. —Of the causes of the Sabbath)
- `14. ... 46.` — List sequence jump (skipped from 14 to 46) (III. —Of the causes of the Sabbath)
- `19. ... 49.` — List sequence jump (skipped from 19 to 49) (III. —Of the causes of the Sabbath)
- `16. ... 53.` — List sequence jump (skipped from 16 to 53) (III. —Of the causes of the Sabbath)
- `8. ... 16.` — List sequence jump (skipped from 8 to 16) (IV. —Of the Judaical Sabbath)
- `12. ... 17.` — List sequence jump (skipped from 12 to 17) (IV. —Of the Judaical Sabbath)
- `2. ... 19.` — List sequence jump (skipped from 2 to 19) (IV. —Of the Judaical Sabbath)
- `7. ... 15.` — List sequence jump (skipped from 7 to 15) (IV. —Of the Judaical Sabbath)
- `9. ... 20.` — List sequence jump (skipped from 9 to 20) (IV. —Of the Judaical Sabbath)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (V. —Of the Lord's Day)
- `4. ... 6.` — List sequence jump (skipped from 4 to 6) (V. —Of the Lord's Day)
- `7. ... 13.` — List sequence jump (skipped from 7 to 13) (V. —Of the Lord's Day)
- `10. ... 13.` — List sequence jump (skipped from 10 to 13) (V. —Of the Lord's Day)
- `1. ... 30.` — List sequence jump (skipped from 1 to 30) (V. —Of the Lord's Day)
- `3. ... 10.` — List sequence jump (skipped from 3 to 10) (VI. —The practical observance of the Lord's Day)
- `4. ... 6.` — List sequence jump (skipped from 4 to 6) (CHAPTERS 1, 2: Pre-eminent dignity of Christ, both absolutely and comparatively—His superiority to a)
- `2. ... 9.` — List sequence jump (skipped from 2 to 9) (CHAPTERS 1, 2: Pre-eminent dignity of Christ, both absolutely and comparatively—His superiority to a)
- `8. ... 10.` — List sequence jump (skipped from 8 to 10) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `7. ... 9.` — List sequence jump (skipped from 7 to 9) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `3. ... 5.` — List sequence jump (skipped from 3 to 5) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `10. ... 13.` — List sequence jump (skipped from 10 to 13) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `6. ... 8.` — List sequence jump (skipped from 6 to 8) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `12. ... 15.` — List sequence jump (skipped from 12 to 15) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `1. ... 3.` — List sequence jump (skipped from 1 to 3) (CHAPTERS 3, 4:1–13: Christ's superiority to Moses, the agent in founding the old dispensation)
- `8. ... 10.` — List sequence jump (skipped from 8 to 10) (CHAPTERS 4:14–16, 5–8" Superiority of Christ as priest to the Levitical priesthood, from the analogy)
- `7. ... 9.` — List sequence jump (skipped from 7 to 9) (CHAPTERS 4:14–16, 5–8" Superiority of Christ as priest to the Levitical priesthood, from the analogy)
- `3. ... 5.` — List sequence jump (skipped from 3 to 5) (CHAPTERS 9, 10:1–18: Superiority of Christ's priesthood from the superior value of his sacrifice)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (CHAPTERS 9, 10:1–18: Superiority of Christ's priesthood from the superior value of his sacrifice)
- `10. ... 13.` — List sequence jump (skipped from 10 to 13) (CHAPTERS 10:19–39, 11: The obligation, advantage, and necessity of steadfast adherence to the gospel)
- `6. ... 8.` — List sequence jump (skipped from 6 to 8) (CHAPTERS 10:19–39, 11: The obligation, advantage, and necessity of steadfast adherence to the gospel)
- `12. ... 15.` — List sequence jump (skipped from 12 to 15) (CHAPTERS 10:19–39, 11: The obligation, advantage, and necessity of steadfast adherence to the gospel)
- `1. ... 3.` — List sequence jump (skipped from 1 to 3) (CHAPTERS 10:19–39, 11: The obligation, advantage, and necessity of steadfast adherence to the gospel)

All are legitimate. White-list them.

### Unmatched Quotation Marks

**25 entries** — Owen's 17th-century convention of opening quotation marks
without closing them in debate/citation/Scripture contexts. These are authentic
and should not be modernized per AGENTS.md.

Anomalies penalty: **10.0** (154 anomalies × 0.1).
White-list all legitimate anomaly categories to eliminate this penalty.

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
```

## Missing Word Samples

- `quæ`: PDF=44, EPUB=0
- `hæc`: PDF=20, EPUB=0
- `naturæ`: PDF=8, EPUB=0
- `cœlo`: PDF=7, EPUB=0
- `judæis`: PDF=7, EPUB=0
- `nostræ`: PDF=7, EPUB=0
- `præterea`: PDF=6, EPUB=0
- `pœna`: PDF=6, EPUB=0
- `cœlum`: PDF=6, EPUB=0
- `hebræos`: PDF=6, EPUB=0

## Excess Word Samples

- `quae`: PDF=1, EPUB=45
- `trials`: PDF=30, EPUB=58
- `encouragement`: PDF=28, EPUB=51
- `haec`: PDF=0, EPUB=20
- `afflictions`: PDF=17, EPUB=33
- `mercies`: PDF=17, EPUB=32
- `preserve`: PDF=16, EPUB=30
- `persecution`: PDF=15, EPUB=29
- `dangerous`: PDF=14, EPUB=27
- `evils`: PDF=13, EPUB=25

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: ['100', '104', '105', '11', '110', '113', '116', '118', '120', '128', '136', '137', '144', '145', '146', '154', '162', '169', '17', '174', '175', '184', '194', '197', '199', '220', '223', '29', '30', '32', '4', '41', '48', '5', '55', '59', '6', '63', '7', '94']

Updated whitelist:
```json
"dense_source_window_loss": ["100", "104", "105", "11", "110", "113", "116", "118", "120", "128", "136", "137", "144", "145", "146", "154", "162", "169", "17", "174", "175", "184", "194", "197", "199", "220", "223", "29", "30", "32", "4", "41", "48", "5", "55", "59", "6", "63", "7", "94"]
```

## Action Checklist

### Step 1: White-list anomaly categories (Impact: −10.0 Need)

Update the anomalies section in `volume_{vol}_whitelist.json` to cover all flagged categories.
Add all 64 structural nesting sequence jumps.
Add unmatched quotation marks explanation (legitimate Owen convention).

### Step 2: Fix compound word merging (Impact: readability + coverage)

Add the `text_replacements` entries listed above to `convert.py`.

### Step 3: Update dense source window whitelist

Replace the `dense_source_window_loss` array in `volume_{vol}_whitelist.json`
with the updated list shown above.

### Step 4: Re-audit and verify

After all changes:
1. Re-render: `.venv/bin/python3 volumes/v{vol}/convert.py --render-only`
2. Audit EPUB: `.venv/bin/python3 scripts/audit_epub.py {vol}`
3. Audit text integrity: `.venv/bin/python3 scripts/audit_text_integrity.py {vol}`
4. Audit anomalies: `.venv/bin/python3 scripts/audit_anomalies.py {vol}`
5. Audit bug regressions: `.venv/bin/python3 scripts/audit_bug_regressions.py {vol}`
6. Report state: `.venv/bin/python3 scripts/report_volume_state.py`
7. Verify Need drops from 28.7 to target

## What NOT To Do

3. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are
   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.
4. **Do NOT try to resolve structural nesting sequence jumps** — These are sermon
   numbers (4, 8, 10, 11, 12, 13) that are chapter titles, not list items.