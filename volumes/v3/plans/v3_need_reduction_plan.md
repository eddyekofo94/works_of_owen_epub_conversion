# Volume 3 — Comprehensive Need Score Reduction Plan

> Current Need: **5.5** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.97% | **1.2** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.94%>=99% | **0.0** | — |
| Latin tagging | 78.0% | **2.2** | no |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/25 | **0.0** | — |
| Splits | 4 | **2.0** | no |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 1 | **0.1** | no |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **5.5** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.1 | 0.0 | 1.2 | **5.5** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 1.2 | **1.2** |
| **Whitelist quotes only** | 0.1 | 0.0 | 1.2 | **1.3** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 1.2 | **1.2** |

The coverage gap is only **1.2** points — very small. 
The dominant penalty is **Latin tagging** at **2.2** points.

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
| Unmatched Quotation Marks | 1 | See analysis | See analysis |

### Unmatched Quotation Marks

**1 entries** — Owen's 17th-century convention of opening quotation marks
without closing them in debate/citation/Scripture contexts. These are authentic
and should not be modernized per AGENTS.md.

Anomalies penalty: **0.1** (1 anomalies × 0.1).
White-list all legitimate anomaly categories to eliminate this penalty.

## Dense Source Window Losses

**21 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 191 | to come as to put an end unto that whole church state wherei... | patristic_latin | Whitelist |
| 193 | in that holy obedience which he requires at our hands luke o... | scripture_refs | Whitelist |
| 202 | immediate actings of the holy ghost are not spoken of him ab... | structural | Whitelist |
| 226 | death and חֶבְלֵי־מָוֶת are the cords of death see psalm and... | polyglot | Whitelist |
| 233 | of holiness because in him there was an all fullness of the ... | patristic_latin | Whitelist |
| 240 | for by our lord jesus christ there is no church state amongs... | structural | Whitelist |
| 243 | whose name he doth accomplish it john howbeit when the spiri... | scripture_refs | Whitelist |
| 271 | wrought in us consists doth always certainly and infallibly ... | patristic_latin | Whitelist |
| 284 | disposition is where one degree of the same kind disposeth t... | structural | Whitelist |
| 303 | and heresies are again revived among us by crew of sociniani... | patristic_latin | Whitelist |
| 326 | unto them that believe the effectual working of his grace in... | patristic_latin | Whitelist |
| 339 | own kind whereby men inflame themselves isaiah waxing worse ... | scripture_refs | Whitelist |
| 364 | 2d in an especial manner from the great sin of despising god... | patristic_latin | Whitelist |
| 373 | are rejected inexcusable so isaiah 3-5 proverbs chronicles 1... | scripture_refs | Whitelist |
| 407 | with the effects of it deuteronomy the lord thy god will cir... | structural | Whitelist |
| 410 | chapter the manner of conversion explained in the instance o... | patristic_latin | Whitelist |
| 463 | so it is extreme pride and cursed self confidence for them t... | patristic_latin | Whitelist |
| 472 | is that which our apostle so commendeth in the thessalonians... | patristic_latin | Whitelist |
| 490 | say that as great winds and storms do sometimes contribute t... | structural | Whitelist |
| 498 | worketh faith in us and then preserveth it when it is wrough... | patristic_latin | Whitelist |
| 506 | grow up in some into penances vows uncommanded abstinences a... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
'selfabasement': 'self-abasement',
'selfdenial': 'self-denial',
```

## Missing Word Samples

- `self`: PDF=14, EPUB=6

## Excess Word Samples

- `book`: PDF=15, EPUB=31
- `digital`: PDF=0, EPUB=10
- `theological`: PDF=3, EPUB=12
- `volume`: PDF=0, EPUB=9
- `modern`: PDF=8, EPUB=16
- `historical`: PDF=3, EPUB=11
- `edition`: PDF=1, EPUB=9
- `greek`: PDF=1, EPUB=9
- `ii`: PDF=6, EPUB=13
- `has`: PDF=5, EPUB=12

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: [41, 59, 60, 66, 69, 81, 82, 83, 89, 92, 111, 147, 152, 155, 158, 162, 163, 165, 185]

**New pages to add**: [191, 193, 202, 226, 233, 240, 243, 271, 284, 303, 326, 339, 364, 373, 407, 410, 463, 472, 490, 498, 506]

Updated whitelist:
```json
"dense_source_window_loss": [41, 59, 60, 66, 69, 81, 82, 83, 89, 92, 111, 147, 152, 155, 158, 162, 163, 165, 185, 191, 193, 202, 226, 233, 240, 243, 271, 284, 303, 326, 339, 364, 373, 407, 410, 463, 472, 490, 498, 506]
```

## Action Checklist

### Step 1: White-list anomaly categories (Impact: −0.1 Need)

Update the anomalies section in `volume_{vol}_whitelist.json` to cover all flagged categories.
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
7. Verify Need drops from 5.5 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.94% (above the 99% threshold). Whitelisting has zero effect.
3. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are
   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.