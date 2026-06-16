# Volume 9 — Comprehensive Need Score Reduction Plan

> Current Need: **24.4** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.64% | **14.4** | YES |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | whitelisted | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/0 | **0.0** | — |
| Splits | 38 | **10.0** | YES |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **24.4** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 14.4 | **24.4** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 14.4 | **14.4** |
| **Whitelist quotes only** | 0.0 | 0.0 | 14.4 | **14.4** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 14.4 | **14.4** |

The coverage gap alone contributes **14.4** points. 
Reducing this requires finding and fixing missing content in the EPUB.
The dominant penalty is **Coverage** at **14.4** points.

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

**9 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 177 | beauty and glory when isaiah saw him isaiah he cries out am ... | scripture_refs | Whitelist |
| 319 | distresses that do befall us the psalmist doth so psalm he h... | scripture_refs | Whitelist |
| 322 | sermon f21 gospel charity and above all these things put on ... | patristic_latin | Whitelist |
| 338 | new creature therefore we are so expressly commanded by the ... | structural | Whitelist |
| 357 | sermon f24 christian god's temple for ye are the temple of t... | structural | Whitelist |
| 359 | us with his ordinances god took the first fruits as an ackno... | structural | Whitelist |
| 361 | that were to be poured out upon christ and believers under h... | patristic_latin | Whitelist |
| 362 | called the king of glory psalm lift up your heads ye everlas... | scripture_refs | Whitelist |
| 366 | visible presence in the temple and tabernacle was the ark an... | patristic_latin | Whitelist |

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

**Stale entries to remove**: [3, 4, 5, 6, 7, 8, 10, 26, 29, 42, 60, 73, 101, 106, 120, 132, 149, 150, 186, 187, 188, 192, 193, 200, 213, 218, 234, 243, 249, 252, 270, 273, 276, 283, 288, 292, 298, 300, 312, 316]

**New pages to add**: [177, 319, 322, 338, 357, 359, 361, 362, 366]

Updated whitelist:
```json
"dense_source_window_loss": [3, 4, 5, 6, 7, 8, 10, 26, 29, 42, 60, 73, 101, 106, 120, 132, 149, 150, 177, 186, 187, 188, 192, 193, 200, 213, 218, 234, 243, 249, 252, 270, 273, 276, 283, 288, 292, 298, 300, 312, 316, 319, 322, 338, 357, 359, 361, 362, 366]
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
7. Verify Need drops from 24.4 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.26% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.