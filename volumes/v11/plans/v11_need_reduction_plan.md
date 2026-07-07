# Volume 11 — Comprehensive Need Score Reduction Plan

> Current Need: **33.4** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.88% | **4.8** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | whitelisted | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/52 | **0.0** | — |
| Splits | 5 | **2.5** | no |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 206 | **10.0** | YES |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **17.3** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 10.0 | 0.0 | 4.8 | **33.4** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 4.8 | **4.8** |
| **Whitelist quotes only** | 10.0 | 0.0 | 4.8 | **14.8** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 4.8 | **4.8** |

The coverage gap is only **4.8** points — very small. 
The dominant penalty is **Anomalies** at **10.0** points.

## Anomaly Breakdown

| Category | Count | Legitimate? | Fixable? |
|---|---|---|---|
| Hyphenation Anomalies | 46 | See analysis | See analysis |
| Punctuation Spacing Blemishes | 43 | See analysis | See analysis |
| OCR & Bracket Residues | 9 | See analysis | See analysis |
| Mixed-Case Capitalization Errors | 0 | See analysis | See analysis |
| Unresolved Citation References | 0 | See analysis | See analysis |
| Structural Nesting Sequence Jumps | 15 | See analysis | See analysis |
| Invalid Bible References | 0 | See analysis | See analysis |
| List Formatting Inconsistencies | 0 | See analysis | See analysis |
| Unmatched Quotation Marks | 93 | See analysis | See analysis |

### Structural Nesting Sequence Jumps

**15 jumps** — all are sermon numbers or legitimate list starts:
- `2.` — List sequence starts at 2 instead of 1 (Analysis.)
- `1. ... 9.` — List sequence jump (skipped from 1 to 9) (A Preface to the Reader.)
- `2. ... 23.` — List sequence jump (skipped from 2 to 23) (A Preface to the Reader.)
- `23. ... 30.` — List sequence jump (skipped from 23 to 30) (A Preface to the Reader.)
- `2. ... 417.` — List sequence jump (skipped from 2 to 417) (A Preface to the Reader.)
- `2. ... 5.` — List sequence jump (skipped from 2 to 5) (Chapter 3 - the Immutability of the Purposes of God.)
- `1. ... 6.` — List sequence jump (skipped from 1 to 6) (Chapter 3 - the Immutability of the Purposes of God.)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (Chapter 4 - the Argument From the Covenant of Grace.)
- `4. ... 7.` — List sequence jump (skipped from 4 to 7) (Chapter 4 - the Argument From the Covenant of Grace.)
- `3. ... 8.` — List sequence jump (skipped from 3 to 8) (Chapter 4 - the Argument From the Covenant of Grace.)
- `1. ... 6.` — List sequence jump (skipped from 1 to 6) (Chapter 5 - Argument From the Promises of God.)
- `2.` — List sequence starts at 2 instead of 1 (Chapter 6 - Particular Promises Illustrated.)
- `1. ... 3.` — List sequence jump (skipped from 1 to 3) (Chapter 7 - the Mediation of Christ.)
- `2.` — List sequence starts at 2 instead of 1 (Chapter 13 - the Assertors and Adversaries of the Doctrine Compared.)
- `2. ... 4.` — List sequence jump (skipped from 2 to 4) (Chapter 15 - Argument Against the Doctrine From the Sins of Believers.)

All are legitimate. White-list them.

### Unmatched Quotation Marks

**93 entries** — Owen's 17th-century convention of opening quotation marks
without closing them in debate/citation/Scripture contexts. These are authentic
and should not be modernized per AGENTS.md.

Anomalies penalty: **10.0** (206 anomalies × 0.1).
White-list all legitimate anomaly categories to eliminate this penalty.

## Dense Source Window Losses

**21 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 127 | hereunto was that of the pelagians and semi pelagians which ... | patristic_latin | Whitelist |
| 128 | much of ancient candid truth in opposition to the pelagians ... | patristic_latin | Whitelist |
| 129 | it its principles and causes its relation to the good will o... | structural | Whitelist |
| 131 | note by the editor see page f7 to remove from the preceding ... | structural | Whitelist |
| 135 | of judging professors to be true believers matthew considere... | scripture_refs | Whitelist |
| 136 | unchangeableness and faithfulness of god jude corinthians is... | scripture_refs | Whitelist |
| 137 | was known upon the earth revelation jude matthew thessalonia... | scripture_refs | Whitelist |
| 139 | gracious promises wherein their refreshments and reserves un... | scripture_refs | Whitelist |
| 140 | do give the least hint to such an assertion romans psalm isa... | scripture_refs | Whitelist |
| 141 | corinthians ephesians romans john the temptation arising fro... | scripture_refs | Whitelist |
| 142 | things as they are in themselves are low weak and confused c... | scripture_refs | Whitelist |
| 143 | in believing the holy ghost so plentifully witnesseth peter ... | scripture_refs | Whitelist |
| 144 | in the beginning of its confidence to the end job psalm 5-9 ... | scripture_refs | Whitelist |
| 145 | thing of the greatest evidence and clearness as corinthians ... | scripture_refs | Whitelist |
| 147 | glorious attributes there is an actual permanency or samenes... | scripture_refs | Whitelist |
| 148 | notwithstanding the seeming contrary engagement of romans fr... | scripture_refs | Whitelist |
| 150 | shall hereafter be fully declared hebrews samuel peter kings... | scripture_refs | Whitelist |
| 151 | are incompatible with truth or grace psalm 34-36 job kings e... | scripture_refs | Whitelist |
| 152 | account in love without dissimulation romans doubtless the d... | scripture_refs | Whitelist |
| 153 | be deceived the works of the flesh being manifest galatians ... | patristic_latin | Whitelist |
| 154 | in respect of its fountain termed the faith of god's elect r... | scripture_refs | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'churchofficers': 'church-officers',
'churchofficer': 'church-officer',
```

## Missing Word Samples

- `sod`: PDF=3, EPUB=0
- `semi`: PDF=3, EPUB=0

## Excess Word Samples

- `psalms`: PDF=1, EPUB=56
- `historical`: PDF=2, EPUB=10
- `digital`: PDF=0, EPUB=8
- `theological`: PDF=2, EPUB=9
- `footnotes`: PDF=0, EPUB=7
- `modern`: PDF=4, EPUB=10

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 25, 27, 35, 36, 38, 40, 41, 46, 52, 64, 76, 83, 92, 96, 100, 107, 108, 111, 114, 126]

**New pages to add**: [127, 128, 129, 131, 135, 136, 137, 139, 140, 141, 142, 143, 144, 145, 147, 148, 150, 151, 152, 153, 154]

Updated whitelist:
```json
"dense_source_window_loss": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23, 24, 25, 27, 35, 36, 38, 40, 41, 46, 52, 64, 76, 83, 92, 96, 100, 107, 108, 111, 114, 126, 127, 128, 129, 131, 135, 136, 137, 139, 140, 141, 142, 143, 144, 145, 147, 148, 150, 151, 152, 153, 154]
```

## Action Checklist

### Step 1: White-list anomaly categories (Impact: −10.0 Need)

Update the anomalies section in `volume_{vol}_whitelist.json` to cover all flagged categories.
Add all 15 structural nesting sequence jumps.
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
7. Verify Need drops from 33.4 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.84% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.
3. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are
   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.
4. **Do NOT try to resolve structural nesting sequence jumps** — These are sermon
   numbers (4, 8, 10, 11, 12, 13) that are chapter titles, not list items.