# Volume 1 — Comprehensive Need Score Reduction Plan

> Current Need: **6.7** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.93% | **2.8** | no |
| Greek coverage | 99.9% | **3.9** | no |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.85%>=99% | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/49 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **6.7** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 2.8 | **6.7** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 2.8 | **2.8** |
| **Whitelist quotes only** | 0.0 | 0.0 | 2.8 | **2.8** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 2.8 | **2.8** |

The coverage gap is only **2.8** points — very small. 
The dominant penalty is **Greek coverage** at **3.9** points.

## Anomaly Breakdown

| Category | Count | Legitimate? | Fixable? |
|---|---|---|---|
| Hyphenation Anomalies | 0 | See analysis | See analysis |
| Punctuation Spacing Blemishes | 0 | See analysis | See analysis |
| OCR & Bracket Residues | 0 | See analysis | See analysis |
| Mixed-Case Capitalization Errors | 0 | See analysis | See analysis |
| Unresolved Citation References | 0 | See analysis | See analysis |
| Structural Nesting Sequence Jumps | 0 | See analysis | See analysis |
| Invalid Bible References | 0 | See analysis | See analysis |
| List Formatting Inconsistencies | 0 | See analysis | See analysis |
| Unmatched Quotation Marks | 0 | See analysis | See analysis |

## Dense Source Window Losses

**40 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 3 | contents of χριστολογια or declaration of the glorious myste... | polyglot | Whitelist |
| 4 | person of christ which is love its truth and reality vindica... | structural | Whitelist |
| 5 | the accomplishment of the work of mediation in this world re... | patristic_latin | Whitelist |
| 6 | of the holy trinity of the works of god and first of those t... | structural | Whitelist |
| 7 | and misapprehension on the principles asserted in the proleg... | patristic_latin | Whitelist |
| 9 | embraces the most comprehensive view of this vitally-importa... | scripture_refs | Whitelist |
| 10 | learned puritan we are informed by dr steven that his exposi... | structural | Whitelist |
| 21 | individuals since the reformation next to calvin's instituti... | structural | Whitelist |
| 26 | whole church aedificar quid dicturus what will you say es de... | patristic_latin | Whitelist |
| 27 | not prevail against it for unum hoc est this is one thing im... | patristic_latin | Whitelist |
| 34 | scrutator majestatis absorbetur gloria the searcher of majes... | structural | Whitelist |
| 35 | scrutari and most impudent is he who searches cupot opificem... | structural | Whitelist |
| 51 | imago id est verbum dei ad eum qui est ad imaginem hoc est h... | patristic_latin | Whitelist |
| 53 | declaration of the glorious mystery of the person of christ ... | scripture_refs | Whitelist |
| 56 | lively stones also as this apostle assures us epist they mus... | structural | Whitelist |
| 76 | of the same mystery is elsewhere testified unto hebrews god ... | scripture_refs | Whitelist |
| 78 | so the apostle expresseth it hebrews god who at sundry times... | scripture_refs | Whitelist |
| 83 | of his person by whom they are performed john if any man sin... | scripture_refs | Whitelist |
| 90 | place no small portion of divine blessedness self existence ... | patristic_latin | Whitelist |
| 101 | glory and the firmament always showed his handy work the inv... | structural | Whitelist |
| 105 | image of the other for he and the father are one and one and... | structural | Whitelist |
| 106 | unto his divine person as the son of the father the only beg... | structural | Whitelist |
| 117 | most frequently expressed by the knowledge of him john corin... | scripture_refs | Whitelist |
| 148 | the son of god has not life chap v5 if we are wanting herein... | structural | Whitelist |
| 150 | for when he brought the first begotten into the world he sai... | polyglot | Whitelist |
| 188 | all the people shall say amen deut and on the other hand he ... | patristic_latin | Whitelist |
| 194 | the spirit as he is the only begotten of the father he is th... | structural | Whitelist |
| 203 | divine goodness how great is his goodness how great is his b... | structural | Whitelist |
| 223 | one whose benignity is ready to exercise loving kindness on ... | structural | Whitelist |
| 239 | own glory in and by their own immediate proper ends proverbs... | patristic_latin | Whitelist |
| 269 | and obedience absolute and universal into condition of self ... | structural | Whitelist |
| 297 | of one into another such notions of these things some fancie... | structural | Whitelist |
| 319 | residence of god in glory and majesty chap there on the thro... | patristic_latin | Whitelist |
| 328 | and worship have we communion by faith whilst we are here be... | scripture_refs | Whitelist |
| 332 | figure of christ on his forehead exodus he has made atonemen... | patristic_latin | Whitelist |
| 341 | by god the father unto his only begotten son no other being ... | structural | Whitelist |
| 356 | so as to abide one foot breadth above the earth we tread upo... | patristic_latin | Whitelist |
| 374 | as one of old complained to the same purpose upon his perusa... | structural | Whitelist |
| 375 | they taste of its goodness by any of its first fruits in the... | patristic_latin | Whitelist |
| 379 | face of jesus christ corinthians otherwise we know it not we... | scripture_refs | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
```

## Excess Word Samples

- `digital`: PDF=0, EPUB=10
- `theological`: PDF=2, EPUB=11
- `historical`: PDF=2, EPUB=10
- `modern`: PDF=4, EPUB=11
- `footnotes`: PDF=0, EPUB=7
- `hebrew`: PDF=3, EPUB=9

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [3, 4, 5, 6, 7, 9, 10, 21, 26, 27, 34, 35, 51, 53, 56, 76, 78, 83, 90, 101, 105, 106, 117, 148, 150, 188, 194, 203, 223, 239, 269, 297, 319, 328, 332, 341, 356, 374, 375, 379]

Updated whitelist:
```json
"dense_source_window_loss": [3, 4, 5, 6, 7, 9, 10, 21, 26, 27, 34, 35, 51, 53, 56, 76, 78, 83, 90, 101, 105, 106, 117, 148, 150, 188, 194, 203, 223, 239, 269, 297, 319, 328, 332, 341, 356, 374, 375, 379]
```

## Action Checklist

### Step 1: Fix compound word merging (Impact: readability + coverage)

Add the `text_replacements` entries listed above to `convert.py`.

### Step 2: Update dense source window whitelist

Replace the `dense_source_window_loss` array in `volume_{vol}_whitelist.json`
with the updated list shown above.

### Step 3: Re-audit and verify

After all changes:
1. Re-render: `.venv/bin/python3 volumes/v{vol}/convert.py --render-only`
2. Audit EPUB: `.venv/bin/python3 scripts/audit_epub.py {vol}`
3. Audit text integrity: `.venv/bin/python3 scripts/audit_text_integrity.py {vol}`
4. Audit anomalies: `.venv/bin/python3 scripts/audit_anomalies.py {vol}`
5. Audit bug regressions: `.venv/bin/python3 scripts/audit_bug_regressions.py {vol}`
6. Report state: `.venv/bin/python3 scripts/report_volume_state.py`
7. Verify Need drops from 6.7 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.85% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.