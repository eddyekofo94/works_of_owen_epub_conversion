# Volume 5 — Comprehensive Need Score Reduction Plan

> Current Need: **0.4** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.99% | **0.4** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.71%>=99% | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/44 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **0.4** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 0.4 | **0.4** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 0.4 | **0.4** |
| **Whitelist quotes only** | 0.0 | 0.0 | 0.4 | **0.4** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 0.4 | **0.4** |

The coverage gap is only **0.4** points — very small. 
The dominant penalty is **Coverage** at **0.4** points.

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

## Excess Word Samples

- `translated`: PDF=3, EPUB=19
- `translation`: PDF=10, EPUB=25
- `digital`: PDF=0, EPUB=10
- `theological`: PDF=3, EPUB=12
- `historical`: PDF=4, EPUB=12
- `greek`: PDF=5, EPUB=12
- `modern`: PDF=3, EPUB=10
- `footnotes`: PDF=0, EPUB=7
- `hebrew`: PDF=4, EPUB=10
- `edition`: PDF=2, EPUB=8

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: [15, 16, 29, 31, 35, 36, 37, 62, 77, 88, 89, 98, 122, 126, 151, 173, 182, 297, 358, 359, 377, 393, 431, 442, 469, 473, 499, 538]

Updated whitelist:
```json
"dense_source_window_loss": [15, 16, 29, 31, 35, 36, 37, 62, 77, 88, 89, 98, 122, 126, 151, 173, 182, 297, 358, 359, 377, 393, 431, 442, 469, 473, 499, 538]
```

## Action Checklist

### Step 1: Update dense source window whitelist

Replace the `dense_source_window_loss` array in `volume_{vol}_whitelist.json`
with the updated list shown above.

### Step 2: Re-audit and verify

After all changes:
1. Re-render: `.venv/bin/python3 volumes/v{vol}/convert.py --render-only`
2. Audit EPUB: `.venv/bin/python3 scripts/audit_epub.py {vol}`
3. Audit text integrity: `.venv/bin/python3 scripts/audit_text_integrity.py {vol}`
4. Audit anomalies: `.venv/bin/python3 scripts/audit_anomalies.py {vol}`
5. Audit bug regressions: `.venv/bin/python3 scripts/audit_bug_regressions.py {vol}`
6. Report state: `.venv/bin/python3 scripts/report_volume_state.py`
7. Verify Need drops from 0.4 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.71% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.