# Volume 3 — Comprehensive Need Score Reduction Plan

> Current Need: **4.5** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.97% | **1.2** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.94%>=99% | **0.0** | — |
| Latin tagging | 79.2% | **2.1** | no |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/25 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 12 | **1.2** | no |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **4.5** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 1.2 | 0.0 | 1.2 | **4.5** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 1.2 | **1.2** |
| **Whitelist quotes only** | 1.2 | 0.0 | 1.2 | **2.4** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 1.2 | **1.2** |

The coverage gap is only **1.2** points — very small. 
The dominant penalty is **Latin tagging** at **2.1** points.

## Anomaly Breakdown

| Category | Count | Legitimate? | Fixable? |
|---|---|---|---|
| Hyphenation Anomalies | 0 | See analysis | See analysis |
| Punctuation Spacing Blemishes | 12 | See analysis | See analysis |
| OCR & Bracket Residues | 0 | See analysis | See analysis |
| Mixed-Case Capitalization Errors | 0 | See analysis | See analysis |
| Unresolved Citation References | 0 | See analysis | See analysis |
| Structural Nesting Sequence Jumps | 0 | See analysis | See analysis |
| Invalid Bible References | 0 | See analysis | See analysis |
| List Formatting Inconsistencies | 0 | See analysis | See analysis |
| Unmatched Quotation Marks | 0 | See analysis | See analysis |

Anomalies penalty: **1.2** (12 anomalies × 0.1).
White-list all legitimate anomaly categories to eliminate this penalty.

## Dense Source Window Losses

**1 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 506 | grow up in some into penances vows uncommanded abstinences a... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
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

**Stale entries to remove**: [37, 41, 59, 60, 66, 69, 81, 82, 83, 89, 92, 111, 147, 152, 155, 158, 162, 163, 165, 185, 191, 193, 202, 226, 233, 240, 243, 271, 284, 303, 326, 339, 364, 373, 407, 410, 463, 472, 490, 498]

**New pages to add**: [506]

Updated whitelist:
```json
"dense_source_window_loss": [37, 41, 59, 60, 66, 69, 81, 82, 83, 89, 92, 111, 147, 152, 155, 158, 162, 163, 165, 185, 191, 193, 202, 226, 233, 240, 243, 271, 284, 303, 326, 339, 364, 373, 407, 410, 463, 472, 490, 498, 506]
```

## Action Checklist

### Step 1: White-list anomaly categories (Impact: −1.2 Need)

Update the anomalies section in `volume_{vol}_whitelist.json` to cover all flagged categories.

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
7. Verify Need drops from 4.5 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.94% (above the 99% threshold). Whitelisting has zero effect.