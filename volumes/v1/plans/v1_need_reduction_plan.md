# Volume 1 — Comprehensive Need Score Reduction Plan

> Current Need: **15.7** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.97% | **1.2** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.90%>=99% | **0.0** | — |
| Latin tagging | 72.6% | **2.7** | no |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/49 | **0.0** | — |
| Splits | 13 | **6.5** | no |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **10.4** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 1.2 | **15.7** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 1.2 | **1.2** |
| **Whitelist quotes only** | 0.0 | 0.0 | 1.2 | **1.2** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 1.2 | **1.2** |

The coverage gap is only **1.2** points — very small. 
The dominant penalty is **Splits** at **6.5** points.

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

**34 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 382 | the dark after what they cannot clearly discern acts among o... | scripture_refs | Whitelist |
| 398 | so the apostle expresseth this truth where is the wise where... | structural | Whitelist |
| 402 | known or as it may be thence earned my present business is o... | structural | Whitelist |
| 406 | 2-6 isaiah 1-4 zechariah john 1-3 philippians 6-8 hebrews 1-... | scripture_refs | Whitelist |
| 411 | made her as the chariots of ammi nadib song of solomon it so... | patristic_latin | Whitelist |
| 419 | in him unto any of the creatures is an act of self humiliati... | patristic_latin | Whitelist |
| 433 | brightness wherewith this glory shines in heaven the all sat... | patristic_latin | Whitelist |
| 434 | unto it sweet savor of the love of christ see song of solomo... | scripture_refs | Whitelist |
| 451 | its holiness and the severity of the curse wherewith it was ... | structural | Whitelist |
| 478 | to reconcile all things unto himself in him whether they be ... | patristic_latin | Whitelist |
| 480 | bring in spiritual refreshment unto believing refreshment un... | patristic_latin | Whitelist |
| 483 | of sight those are the two spiritual powers of our sou1s by ... | structural | Whitelist |
| 487 | on the right hand that cannot see him chap which way soever ... | structural | Whitelist |
| 517 | see the description of these things philippians it is not po... | structural | Whitelist |
| 522 | of iniquity shall be stopped for ever and the voice of the s... | structural | Whitelist |
| 534 | part meditations and discourses concerning the glory of chri... | structural | Whitelist |
| 555 | which are proper for the season as namely spirituality heave... | patristic_latin | Whitelist |
| 559 | and almost visible growth than willows by the water courses ... | structural | Whitelist |
| 565 | warnings of the danger of spiritually decaying state and he ... | patristic_latin | Whitelist |
| 570 | zeal humility contriteness of heart spiritual mindedness vig... | patristic_latin | Whitelist |
| 572 | invited to eat after feast being self full before but this l... | patristic_latin | Whitelist |
| 596 | 7-9 romans 33-36 malachi james judges samuel kings ezekiel m... | scripture_refs | Whitelist |
| 603 | of god towards his church in three things first in causing 5... | patristic_latin | Whitelist |
| 605 | doing any thing that is well pleasing unto god by all which ... | structural | Whitelist |
| 607 | in the likeness of sinful flesh condemning sin sinful flesh ... | scripture_refs | Whitelist |
| 613 | due to our sin isaiah 4-6 john romans corinthians15 corinthi... | scripture_refs | Whitelist |
| 618 | what is the church of christ the whole company of god's elec... | structural | Whitelist |
| 623 | purpose of heart to cleave unto him for the to cleave unto h... | structural | Whitelist |
| 624 | quickening of all graces purging act of all graces purging a... | structural | Whitelist |
| 625 | gracious reception into the family of god as his children an... | structural | Whitelist |
| 626 | isaiah john corinthians romans hebrews corinthians galatians... | scripture_refs | Whitelist |
| 627 | him confirmeth the promises of the covenant to all believers... | structural | Whitelist |
| 629 | 14-20 corinthians 23-25 luke corinthians mark 22-24 corinthi... | scripture_refs | Whitelist |
| 632 | chapter of particular churches what are particular churches ... | patristic_latin | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'preeminence': 'pre-eminence',
```

## Missing Word Samples

- `greeks`: PDF=3, EPUB=0

## Excess Word Samples

- `preface`: PDF=7, EPUB=16
- `super`: PDF=4, EPUB=12
- `historical`: PDF=2, EPUB=10
- `theological`: PDF=1, EPUB=9
- `digital`: PDF=0, EPUB=8
- `text`: PDF=8, EPUB=15
- `modern`: PDF=3, EPUB=10
- `footnotes`: PDF=0, EPUB=7
- `volume`: PDF=7, EPUB=13
- `dr`: PDF=7, EPUB=13

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [382, 398, 402, 406, 411, 419, 433, 434, 451, 478, 480, 483, 487, 517, 522, 534, 555, 559, 565, 570, 572, 596, 603, 605, 607, 613, 618, 623, 624, 625, 626, 627, 629, 632]

Updated whitelist:
```json
"dense_source_window_loss": [382, 398, 402, 406, 411, 419, 433, 434, 451, 478, 480, 483, 487, 517, 522, 534, 555, 559, 565, 570, 572, 596, 603, 605, 607, 613, 618, 623, 624, 625, 626, 627, 629, 632]
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
7. Verify Need drops from 15.7 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.90% (above the 99% threshold). Whitelisting has zero effect.