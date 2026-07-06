# Volume 13 — Comprehensive Need Score Reduction Plan

> Current Need: **46.0** | Grade: FULL | QA Level: FULL
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.89% | **4.4** | no |
| Greek coverage | 97.4% | **15.0** | YES |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 95.53% | **10.0** | YES |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/18 | **0.0** | — |
| Splits | 1 | **0.5** | no |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 1 | **0.1** | no |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **30.0** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.1 | 0.0 | 4.4 | **46.0** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 4.4 | **4.4** |
| **Whitelist quotes only** | 0.1 | 0.0 | 4.4 | **4.5** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 4.4 | **4.4** |

The coverage gap is only **4.4** points — very small. 
The dominant penalty is **Greek coverage** at **15.0** points.

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

**40 pages** with missing dense source windows.

| Page | Sample | Category | Action |
|---|---|---|---|
| 31 | the law of nature being pre supposed we find them farther sp... | patristic_latin | Whitelist |
| 46 | or no may better serve to illustrate plutarch's discourse of... | structural | Whitelist |
| 50 | and jesuits pretending falsely by their impostures to the po... | structural | Whitelist |
| 58 | they may interest themselves in holy soul concerning affairs... | patristic_latin | Whitelist |
| 68 | is an ignorant congregation of which thanks to our prelates ... | patristic_latin | Whitelist |
| 76 | eshcol cluster of the fruit of canaan rules of walking in fe... | patristic_latin | Whitelist |
| 77 | election appointment acceptation submission galatians acts t... | scripture_refs | Whitelist |
| 87 | commandment and is peculiarly the law of christ john thessal... | scripture_refs | Whitelist |
| 95 | daily while it is called to day lest any of you be hardened ... | patristic_latin | Whitelist |
| 99 | the command with the threatenings attending its non performa... | patristic_latin | Whitelist |
| 102 | alone with submission to the all disposing sovereignty of go... | structural | Whitelist |
| 105 | of god because many false prophets are gone out into the wor... | scripture_refs | Whitelist |
| 112 | it especially seeing that upon consideration and supposition... | structural | Whitelist |
| 136 | the administration of discipline in particular chapter after... | patristic_latin | Whitelist |
| 140 | the adjacent region to metropolis and such like things as th... | structural | Whitelist |
| 143 | to the civil wherever there was metropolis in civil politica... | patristic_latin | Whitelist |
| 145 | was pleading against the donatists basil in epist ad amphilo... | polyglot | Whitelist |
| 151 | to mention their old altare contra altare anti popes anti-co... | structural | Whitelist |
| 152 | quiet the contest of the franciscans and dominicans about th... | patristic_latin | Whitelist |
| 158 | chapter objections against the former discourse proposed to ... | patristic_latin | Whitelist |
| 177 | of the catholic church all profane ignorant self justiciarie... | structural | Whitelist |
| 182 | numerical ordinances the union of this church is not really ... | structural | Whitelist |
| 216 | the generality of their priests and people that of self righ... | structural | Whitelist |
| 223 | and at ephesus chapter as was that of corinth corinthians co... | scripture_refs | Whitelist |
| 251 | sacraments which excludes them from being fideles or church ... | structural | Whitelist |
| 253 | so doing for besides what they have to plead as to the non i... | patristic_latin | Whitelist |
| 270 | disadvantage manifested in behalf of their brethren nor much... | patristic_latin | Whitelist |
| 271 | return unto it out of vulgar discourses about ministers call... | patristic_latin | Whitelist |
| 314 | contrary let him cease from cavilling at words and by expres... | patristic_latin | Whitelist |
| 323 | is no schism is that afore mentioned that schism in the scri... | patristic_latin | Whitelist |
| 330 | forms of the practice of new and old england of admission of... | structural | Whitelist |
| 349 | will speak for itself with all impartial men much less shall... | structural | Whitelist |
| 351 | how they came into such possession of all church state in en... | patristic_latin | Whitelist |
| 353 | the consideration of the severals of them to re assume this ... | structural | Whitelist |
| 364 | albae nos viles pulli nati infelicibus ovis juv l4l shall fa... | structural | Whitelist |
| 368 | of it are relieved by scheme of my self contradictions in th... | patristic_latin | Whitelist |
| 369 | sober man freed from pride passion self fullness and prejudi... | patristic_latin | Whitelist |
| 377 | are schism and errors in the faith are schism and schism and... | patristic_latin | Whitelist |
| 382 | limited nature of schism in its evangelically-ecclesiastical... | patristic_latin | Whitelist |
| 389 | brief vindication of the nonconformists from the charge of s... | structural | Whitelist |

## Compound Word Merging Fixes

The following merged compounds were found in the JSON intermediate.
Add these to `OVERRIDES['text_replacements']` in `convert.py`:

```python
# Compound word merging fixes (extract.py drops hyphen at line breaks)
'churchcommunion': 'church-communion',
'churchgovernment': 'church-government',
'churchmember': 'church-member',
'churchmembers': 'church-members',
'preeminence': 'pre-eminence',
```

## Missing Word Samples

- `self`: PDF=13, EPUB=6
- `fellow`: PDF=3, EPUB=0
- `re`: PDF=3, EPUB=1

## Excess Word Samples

- `prefatory`: PDF=14, EPUB=30
- `editor`: PDF=0, EPUB=12
- `volume`: PDF=5, EPUB=13
- `digital`: PDF=0, EPUB=8
- `historical`: PDF=0, EPUB=8
- `theological`: PDF=0, EPUB=7
- `footnotes`: PDF=0, EPUB=7
- `modern`: PDF=5, EPUB=11

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**New pages to add**: [31, 46, 50, 58, 68, 76, 77, 87, 95, 99, 102, 105, 112, 136, 140, 143, 145, 151, 152, 158, 177, 182, 216, 223, 251, 253, 270, 271, 314, 323, 330, 349, 351, 353, 364, 368, 369, 377, 382, 389]

Updated whitelist:
```json
"dense_source_window_loss": [31, 46, 50, 58, 68, 76, 77, 87, 95, 99, 102, 105, 112, 136, 140, 143, 145, 151, 152, 158, 177, 182, 216, 223, 251, 253, 270, 271, 314, 323, 330, 349, 351, 353, 364, 368, 369, 377, 382, 389]
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
7. Verify Need drops from 46.0 to target

## What NOT To Do

2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.
3. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are
   legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.