# Volume 16 — Comprehensive Need Score Reduction Plan

> Current Need: **2.0** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.95% | **2.0** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.96%>=99% | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/40 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **2.0** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 2.0 | **2.0** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 2.0 | **2.0** |
| **Whitelist quotes only** | 0.0 | 0.0 | 2.0 | **2.0** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 2.0 | **2.0** |

The coverage gap is only **2.0** points — very small. 
The dominant penalty is **Coverage** at **2.0** points.

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

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
'officepower': 'office-power',
'churchcommunion': 'church-communion',
'churchrule': 'church-rule',
'subjectmatter': 'subject-matter',
'churchofficer': 'church-officer',
'churchmember': 'church-member',
'churchprivileges': 'church-privileges',
'churchgovernment': 'church-government',
'churchaffairs': 'church-affairs',
'churchofficers': 'church-officers',
'churchpower': 'church-power',
'churchmembers': 'church-members',
'churchedification': 'church-edification',
'churchorder': 'church-order',
'churchassemblies': 'church-assemblies',
'churchcovenant': 'church-covenant',
'wellgoverned': 'well-governed',
'overreaching': 'over-reaching',
```

## Missing Word Samples

- `pre`: PDF=5, EPUB=0
- `eminence`: PDF=5, EPUB=0

## Excess Word Samples

- `translated`: PDF=14, EPUB=55
- `polyglot`: PDF=0, EPUB=18
- `montanus`: PDF=12, EPUB=23
- `digital`: PDF=0, EPUB=10
- `theological`: PDF=1, EPUB=10
- `historical`: PDF=3, EPUB=11
- `modern`: PDF=8, EPUB=15
- `editor`: PDF=6, EPUB=13
- `footnotes`: PDF=0, EPUB=7

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: [10, 16, 19, 25, 27, 28, 33, 34, 43, 48, 56, 59, 62, 65, 68, 71, 76, 77, 78, 82, 89, 93, 96, 97, 98, 100, 114, 134, 143, 145, 151, 152, 158, 159, 183, 184, 219, 227, 241, 244]

Updated whitelist:
```json
"dense_source_window_loss": [10, 16, 19, 25, 27, 28, 33, 34, 43, 48, 56, 59, 62, 65, 68, 71, 76, 77, 78, 82, 89, 93, 96, 97, 98, 100, 114, 134, 143, 145, 151, 152, 158, 159, 183, 184, 219, 227, 241, 244]
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
7. Verify Need drops from 2.0 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.96% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.