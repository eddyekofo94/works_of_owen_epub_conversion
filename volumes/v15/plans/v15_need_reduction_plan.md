# Volume 15 — Comprehensive Need Score Reduction Plan

> Current Need: **12.4** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.94% | **2.4** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.68%>=99% | **0.0** | — |
| Latin tagging | 29.6% | **5.0** | no |
| Latin translation | 44.1% | **5.0** | no |
| Unresolved citations | 0/57 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **12.4** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 2.4 | **12.4** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 2.4 | **2.4** |
| **Whitelist quotes only** | 0.0 | 0.0 | 2.4 | **2.4** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 2.4 | **2.4** |

The coverage gap is only **2.4** points — very small. 
The dominant penalty is **Latin tagging** at **5.0** points.

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
| 3 | righteousness and legal ceremonies contended for together th... | structural | Whitelist |
| 4 | worship prohibitions of additions produced considered applie... | structural | Whitelist |
| 5 | ignorance readiness to take offense remedies hereof pride fa... | patristic_latin | Whitelist |
| 7 | discourse concerning liturgies and their imposition prefator... | structural | Whitelist |
| 10 | from the authority of the law maker the latter he utterly re... | structural | Whitelist |
| 17 | de rom pontif lib cap but whereas they double the mumber of ... | patristic_latin | Whitelist |
| 19 | executed by persons variously called thereunto acording to h... | structural | Whitelist |
| 29 | their religion as were then fallen out lib concione advocata... | patristic_latin | Whitelist |
| 34 | about such things as were not in rerum natura in the days wh... | patristic_latin | Whitelist |
| 52 | may keep the commandments of the lord your god which command... | structural | Whitelist |
| 75 | with the occasions and reasons of the present differences an... | patristic_latin | Whitelist |
| 90 | and power do make compliance with themselves in all their im... | patristic_latin | Whitelist |
| 102 | in our hearts and made natural unto us by that one and self ... | patristic_latin | Whitelist |
| 103 | profess and yet notwithstanding all this such cross entangle... | patristic_latin | Whitelist |
| 106 | 9-11 he would not continue from generation to generation to ... | structural | Whitelist |
| 108 | judge by the fundamental principles and laws of their church... | patristic_latin | Whitelist |
| 115 | them who first possessed the rule of such churches about the... | patristic_latin | Whitelist |
| 119 | where the calves were set up kings chronicles accordingly ma... | scripture_refs | Whitelist |
| 126 | should all or any of them immediately forfeit their church s... | structural | Whitelist |
| 137 | far easier thing to satisfy conscience with pretense of pres... | structural | Whitelist |
| 138 | fell out among them on account of pre eminences jurisdiction... | patristic_latin | Whitelist |
| 141 | about revealed truths nor different practice in sacred admin... | patristic_latin | Whitelist |
| 145 | ordained or for which pastors and teachers are granted unto ... | structural | Whitelist |
| 180 | to observe when imposed as necessary conditions of all churc... | patristic_latin | Whitelist |
| 188 | who were recommended unto the church by the apostle john pro... | scripture_refs | Whitelist |
| 189 | and unskilful as to degrees in the word of truth romans phil... | scripture_refs | Whitelist |
| 200 | advantages prompts them to pour out upon us for our non comp... | patristic_latin | Whitelist |
| 218 | are cast out and excluded from church communion with them by... | patristic_latin | Whitelist |
| 219 | to act obedientially towards him and ministerially towards o... | structural | Whitelist |
| 239 | to be supposed that diotrephes was alone in his desire of pr... | patristic_latin | Whitelist |
| 245 | christian nations but to give farther evidence hereunto shal... | patristic_latin | Whitelist |
| 248 | did the example of the apostolical churches acts 23-31 insta... | scripture_refs | Whitelist |
| 250 | no intimation is given of any pre eminence or superiority am... | structural | Whitelist |
| 269 | quidem est nomen pacis et pulchra opinio unitatis sed quis a... | patristic_latin | Whitelist |
| 271 | of force in the arguments pleaded for non compliance with ar... | patristic_latin | Whitelist |
| 289 | to think of or to assert any other church state it was impos... | structural | Whitelist |
| 293 | good in there is no benefit to be obtained by any church sta... | patristic_latin | Whitelist |
| 297 | especial nature and condition of the evangelical church stat... | structural | Whitelist |
| 300 | the majesty of the name of the lord his god micah so did the... | structural | Whitelist |
| 307 | have dominion over your faith but are helpers of your joy ch... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'churchcommunion': 'church-communion',
'preeminence': 'pre-eminence',
'churchrule': 'church-rule',
'churchpower': 'church-power',
'churchaffairs': 'church-affairs',
'churchofficers': 'church-officers',
'churchofficer': 'church-officer',
'churchorder': 'church-order',
```

## Missing Word Samples

- `pre`: PDF=6, EPUB=0
- `self`: PDF=5, EPUB=1
- `eminence`: PDF=4, EPUB=0
- `defence`: PDF=3, EPUB=1

## Excess Word Samples

- `churchstate`: PDF=0, EPUB=19
- `digital`: PDF=0, EPUB=10
- `theological`: PDF=0, EPUB=9
- `churchcommunion`: PDF=0, EPUB=9
- `historical`: PDF=1, EPUB=9
- `greek`: PDF=6, EPUB=13
- `footnotes`: PDF=0, EPUB=7
- `modern`: PDF=0, EPUB=7
- `edition`: PDF=5, EPUB=11
- `hebrew`: PDF=0, EPUB=6

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [3, 4, 5, 7, 10, 17, 19, 29, 34, 52, 75, 90, 102, 103, 106, 108, 115, 119, 126, 137, 138, 141, 145, 180, 188, 189, 200, 218, 219, 239, 245, 248, 250, 269, 271, 289, 293, 297, 300, 307]

Updated whitelist:
```json
"dense_source_window_loss": [3, 4, 5, 7, 10, 17, 19, 29, 34, 52, 75, 90, 102, 103, 106, 108, 115, 119, 126, 137, 138, 141, 145, 180, 188, 189, 200, 218, 219, 239, 245, 248, 250, 269, 271, 289, 293, 297, 300, 307]
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
7. Verify Need drops from 12.4 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.68% (above the 99% threshold). Whitelisting has zero effect.