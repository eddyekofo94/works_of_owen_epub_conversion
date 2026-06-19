# Volume 5 — Comprehensive Need Score Reduction Plan

> Current Need: **8.7** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.98% | **0.8** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.73%>=99% | **0.0** | — |
| Latin tagging | 67.4% | **3.3** | no |
| Latin translation | 63.4% | **3.7** | no |
| Unresolved citations | 0/44 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 10 | **1.0** | no |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **8.7** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 1.0 | 0.0 | 0.8 | **8.7** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 0.8 | **0.8** |
| **Whitelist quotes only** | 1.0 | 0.0 | 0.8 | **1.8** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 0.8 | **0.8** |

The coverage gap is only **0.8** points — very small. 
The dominant penalty is **Latin translation** at **3.7** points.

## Anomaly Breakdown

| Category | Count | Legitimate? | Fixable? |
|---|---|---|---|
| Hyphenation Anomalies | 0 | See analysis | See analysis |
| Punctuation Spacing Blemishes | 0 | See analysis | See analysis |
| OCR & Bracket Residues | 8 | See analysis | See analysis |
| Mixed-Case Capitalization Errors | 0 | See analysis | See analysis |
| Unresolved Citation References | 0 | See analysis | See analysis |
| Structural Nesting Sequence Jumps | 0 | See analysis | See analysis |
| Invalid Bible References | 1 | See analysis | See analysis |
| List Formatting Inconsistencies | 0 | See analysis | See analysis |
| Unmatched Quotation Marks | 1 | See analysis | See analysis |

### Unmatched Quotation Marks

**1 entries** — Owen's 17th-century convention of opening quotation marks
without closing them in debate/citation/Scripture contexts. These are authentic
and should not be modernized per AGENTS.md.

Anomalies penalty: **1.0** (10 anomalies × 0.1).
White-list all legitimate anomaly categories to eliminate this penalty.

## Dense Source Window Losses

**33 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 15 | charles wolsley baronet of some reputation who had been memb... | patristic_latin | Whitelist |
| 16 | joseph williams of kidderminster at last the time of his mr ... | structural | Whitelist |
| 35 | totum committe hac sola te totum contege totum immisce te in... | patristic_latin | Whitelist |
| 77 | how unsearchable are his judgments and his ways past finding... | scripture_refs | Whitelist |
| 88 | the old testament as is plainly declared luke 25-27 for it w... | scripture_refs | Whitelist |
| 89 | them which will be pleaded in their proper place chapter 14-... | patristic_latin | Whitelist |
| 122 | the clear revelation of christ and his mediation so did the ... | scripture_refs | Whitelist |
| 126 | of his belly shall flow rivers of living water so chapter 35... | scripture_refs | Whitelist |
| 137 | mentioned in the scripture what shall we do what shall we do... | patristic_latin | Whitelist |
| 151 | acts the word of god acts thessalonians the atonement made b... | scripture_refs | Whitelist |
| 157 | proposed wherefore it so respects and receives christ as pro... | patristic_latin | Whitelist |
| 173 | word is used and in the same signification corinthians timot... | scripture_refs | Whitelist |
| 182 | isaiah hebrews 13-15 1-13 peter john other plea for sinner b... | scripture_refs | Whitelist |
| 207 | this charge be by the law by the law we must be justified bu... | structural | Whitelist |
| 281 | by us he returned it unto him and what he underwent and suff... | structural | Whitelist |
| 292 | case be the righteousness of god the righteousness of god on... | structural | Whitelist |
| 297 | was their father and they his people chapter and the righteo... | structural | Whitelist |
| 307 | do say so but not all not the most not the most learned with... | patristic_latin | Whitelist |
| 353 | are justified before god be our own our own personal righteo... | structural | Whitelist |
| 358 | world obnoxious unto the judgment of god chapter which none ... | patristic_latin | Whitelist |
| 359 | revelato testamento novo non observantur christianis sicut e... | patristic_latin | Whitelist |
| 365 | he treats for as unto our justification whatever they are th... | structural | Whitelist |
| 377 | old testament are leaning on god micah or christ cant rollin... | structural | Whitelist |
| 393 | the epistles of st paul in that unto the romans especially c... | scripture_refs | Whitelist |
| 418 | judgment of death is to this man this man is guilty of death... | structural | Whitelist |
| 431 | which he uses on the like occasions chap what shall we say t... | structural | Whitelist |
| 436 | looks for no righteousness from us but what is prescribed in... | patristic_latin | Whitelist |
| 442 | graecorum chrysostomi et caeterorum quia peccatum emphaticως... | polyglot | Whitelist |
| 457 | least principally himself declares works say some of the law... | structural | Whitelist |
| 469 | such distinction bellarmine considers this testimony in thre... | patristic_latin | Whitelist |
| 499 | live in whatever sins their lusts inclined them unto chap 1-... | patristic_latin | Whitelist |
| 513 | do themselves to be saved what shall we do what shall we do ... | structural | Whitelist |
| 538 | declaration and confirmation of the assertion namely treat t... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
```

## Excess Word Samples

- `digital`: PDF=0, EPUB=10
- `theological`: PDF=3, EPUB=12
- `historical`: PDF=4, EPUB=12
- `greek`: PDF=5, EPUB=12
- `modern`: PDF=3, EPUB=10
- `footnotes`: PDF=0, EPUB=7
- `hebrew`: PDF=4, EPUB=10
- `edition`: PDF=2, EPUB=8
- `section`: PDF=0, EPUB=6

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [15, 16, 35, 77, 88, 89, 122, 126, 137, 151, 157, 173, 182, 207, 281, 292, 297, 307, 353, 358, 359, 365, 377, 393, 418, 431, 436, 442, 457, 469, 499, 513, 538]

Updated whitelist:
```json
"dense_source_window_loss": [15, 16, 35, 77, 88, 89, 122, 126, 137, 151, 157, 173, 182, 207, 281, 292, 297, 307, 353, 358, 359, 365, 377, 393, 418, 431, 436, 442, 457, 469, 499, 513, 538]
```

## Action Checklist

### Step 1: White-list anomaly categories (Impact: −1.0 Need)

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
7. Verify Need drops from 8.7 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.73% (above the 99% threshold). Whitelisting has zero effect.
3. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are
   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.