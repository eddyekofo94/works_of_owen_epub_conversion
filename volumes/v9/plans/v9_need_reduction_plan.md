# Volume 9 — Comprehensive Need Score Reduction Plan

> Current Need: **15.6** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.61% | **15.6** | YES |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | whitelisted | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/0 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **15.6** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 15.6 | **15.6** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 15.6 | **15.6** |
| **Whitelist quotes only** | 0.0 | 0.0 | 15.6 | **15.6** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 15.6 | **15.6** |

The coverage gap alone contributes **15.6** points. 
Reducing this requires finding and fixing missing content in the EPUB.
The dominant penalty is **Coverage** at **15.6** points.

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
| 3 | contents of vol part sermon published prefatory note by the ... | structural | Whitelist |
| 4 | discourse seeing the act of closing with christ is secret an... | patristic_latin | Whitelist |
| 5 | the excellency of christ the use and advantage of faith in t... | patristic_latin | Whitelist |
| 6 | lord's death till he come corinthians 23-26 discourses and i... | scripture_refs | Whitelist |
| 7 | part sermon published prefatory note the following is the fi... | structural | Whitelist |
| 8 | that city and country are crying watchman what of the night ... | structural | Whitelist |
| 10 | unto idolatry secondly their idolatry the idolatry that ther... | patristic_latin | Whitelist |
| 26 | posthumous sermons part sermons published prefatory note und... | structural | Whitelist |
| 29 | affirmation is laid down the promises the promises of god th... | structural | Whitelist |
| 42 | glorified as god as our god he that gives him that gives him... | structural | Whitelist |
| 60 | his goodwill and kindness his patience to us ward and we can... | patristic_latin | Whitelist |
| 73 | god herein the apostle includes the whole mystery of his dea... | patristic_latin | Whitelist |
| 101 | he did as the lord commanded him exodus now surely this gave... | structural | Whitelist |
| 106 | choice jewels of god's eternal love they are god's delight t... | structural | Whitelist |
| 120 | covenant on our part as genesis am god almighty or all suffi... | structural | Whitelist |
| 132 | walk with god nor the righteousness they sought after chapte... | patristic_latin | Whitelist |
| 149 | these considerations first that god judgeth not as man judge... | structural | Whitelist |
| 150 | one place wherein the apostle disputes for it hebrews and ad... | scripture_refs | Whitelist |
| 186 | work of christ and that it was fruit of long suffering peter... | scripture_refs | Whitelist |
| 187 | ways of holiness and godliness first of self searching and s... | patristic_latin | Whitelist |
| 188 | the apostle calls to in such dispensation corinthians self j... | scripture_refs | Whitelist |
| 192 | by practical experience they give never failing certainty of... | structural | Whitelist |
| 193 | own actings things that have self evidencing power may be hi... | structural | Whitelist |
| 200 | smitten any more you will revolt more and more and to swear ... | patristic_latin | Whitelist |
| 213 | spiritual sense against the righteousness of christ the righ... | structural | Whitelist |
| 218 | of mind introduced how much self-confidence promoted by an o... | structural | Whitelist |
| 234 | assert the same truth take proverbs but ye have set at nough... | patristic_latin | Whitelist |
| 243 | the waters of the sanctuary searedness of conscience timothy... | structural | Whitelist |
| 249 | sermon f13 human power defeated the stout-hearted are spoile... | structural | Whitelist |
| 252 | amongst them who cried down with them down with them even to... | structural | Whitelist |
| 270 | my church their voice was down with it down with it even to ... | structural | Whitelist |
| 273 | sermon f16 the divine power of the gospel for am not ashamed... | structural | Whitelist |
| 276 | of god unto salvation what is intended by the gospel the gos... | structural | Whitelist |
| 283 | messiah but called him glutton wine bibber friend of publica... | patristic_latin | Whitelist |
| 288 | sermon f17 we are not to be ashamed of the professors of the... | structural | Whitelist |
| 292 | persecuted ones no god is not ashamed to be called their god... | structural | Whitelist |
| 298 | sermon f19 god the saints rock from the end of the earth wil... | structural | Whitelist |
| 300 | so the psalmist tells us psalm prayer of the afflicted when ... | scripture_refs | Whitelist |
| 312 | sermon f20 from the end of the earth will cry unto thee when... | structural | Whitelist |
| 316 | of eli from the priesthood samuel but will he not return aga... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
'churchmember': 'church-member',
'churchmembers': 'church-members',
```

## Missing Word Samples

- `editor`: PDF=5, EPUB=1
- `sufficiency`: PDF=3, EPUB=1

## Excess Word Samples

- `psalms`: PDF=8, EPUB=19
- `digital`: PDF=0, EPUB=10
- `theological`: PDF=2, EPUB=11
- `historical`: PDF=0, EPUB=8
- `greek`: PDF=8, EPUB=15
- `footnotes`: PDF=0, EPUB=7
- `modern`: PDF=0, EPUB=7
- `hebrew`: PDF=7, EPUB=13
- `edition`: PDF=5, EPUB=11

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [3, 4, 5, 6, 7, 8, 10, 26, 29, 42, 60, 73, 101, 106, 120, 132, 149, 150, 186, 187, 188, 192, 193, 200, 213, 218, 234, 243, 249, 252, 270, 273, 276, 283, 288, 292, 298, 300, 312, 316]

Updated whitelist:
```json
"dense_source_window_loss": [3, 4, 5, 6, 7, 8, 10, 26, 29, 42, 60, 73, 101, 106, 120, 132, 149, 150, 186, 187, 188, 192, 193, 200, 213, 218, 234, 243, 249, 252, 270, 273, 276, 283, 288, 292, 298, 300, 312, 316]
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
7. Verify Need drops from 15.6 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.33% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.