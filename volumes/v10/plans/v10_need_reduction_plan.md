# Volume 10 — Comprehensive Need Score Reduction Plan

> Current Need: **4.4** | Grade: PRISTINE | QA Level: PRISTINE
> Target Need: **≤ 2.0** (PRISTINE)

## Need Score Breakdown

| Component | Value | Penalty | Capped? |
|---|---|---|---|
| Coverage | 99.89% | **4.4** | no |
| Greek coverage | 100.0% | **0.0** | — |
| Hebrew coverage | 100.0% | **0.0** | — |
| Latin word coverage | 99.43%>=99% | **0.0** | — |
| Latin tagging | whitelisted | **0.0** | — |
| Latin translation | whitelisted | **0.0** | — |
| Unresolved citations | 0/20 | **0.0** | — |
| Splits | 0 | **0.0** | — |
| Audit warnings | 0 | **0.0** | — |
| Audit errors | 0 | **0.0** | — |
| Anomalies | 0 | **0.0** | — |
| Unmatched quotes | 0 | **0.0** | — |
| **TOTAL** | | **4.4** | |

### Scenario Projections

| Scenario | Anomalies | Quotes | Coverage | Total |
|---|---|---|---|---|
| **Current state** | 0.0 | 0.0 | 4.4 | **4.4** |
| **Whitelist anomalies only** | 0.0 | 0.0 | 4.4 | **4.4** |
| **Whitelist quotes only** | 0.0 | 0.0 | 4.4 | **4.4** |
| **Whitelist both anomalies + quotes** | 0.0 | 0.0 | 4.4 | **4.4** |

The coverage gap is only **4.4** points — very small. 
The dominant penalty is **Coverage** at **4.4** points.

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
'subjectmatter': 'subject-matter',
'churchcommunion': 'church-communion',
```

## Excess Word Samples

- `digital`: PDF=0, EPUB=10
- `theological`: PDF=11, EPUB=20
- `historical`: PDF=2, EPUB=10
- `modern`: PDF=5, EPUB=12
- `chapters`: PDF=5, EPUB=12
- `footnotes`: PDF=0, EPUB=7
- `hebrew`: PDF=3, EPUB=9
- `edition`: PDF=2, EPUB=8

## Whitelist Updates Required

### `ignored_warnings` additions

```json
// No additions needed — all penalty-generating warnings are already whitelisted.
```

### `dense_source_window_loss` updates

**Stale entries to remove**: ['acts ephesians as distinguished from the world romans john his elect romans his children', 'all justified and made blessed through non imputation of their sin they who have', 'and room with an intention that he should live samuel romans so that christ', 'and the performance of good works is in their apprehension condition pre required to', 'and upon their consciences by reason of not understanding of this love which came', "consolation by his death chapter objections are answered being consideration of thomas more's reply", 'dagon cannot keep on his head nor the idol of uncontrollable free will enjoy', 'declared throughout all the earth chap 28-30 who are the called according to his', 'discovery of new geometrical proportion exclaim we have found it we have found it', 'foolishly that he is altogether like unto us psalm one of which inconveniences all', 'foreskin of your heart and be no more stiff necked deuteronomy and the lord', 'him for foundation stone tried stone precious corner stone sure foundation isaiah that whosoever', 'him is opposite to his eternal blessedness and all sufficiency thirdly god therefore to', 'in excellent order as is at large declared in that golden psalm and this', 'inasmuch as it conducteth to that end otherwise as weariness of the flesh ecclesiasties', 'judge of the rest of their fruit mors in olla mors in olla their', 'many in the conception and publication of some easily invented false opinions is it', 'many sons unto glory for god sent his only begotten son into the world', 'multiply genesis nor yet leave them to self subsistence he in the meantime only', 'nature for his glory was the glory of the only begotten of the father', 'needful of any more value for first those that were saved were saved upon', 'now this whole dispensation with especial regard to the death and blood shedding of', 'of bellarmine man otherwise not over well affected to truth predestination saith he from', 'one may see that can but read english in ore hence that multiplicity of', "opinion of his idol's deity and self sufficiency in the hearts of divers that", 'or gave himself ransom but for many or only for many or only for', 'psalmist from whence the apostle citeth these words psalm and did he die for', 'respect of conformity to the rule and so there is χασμα μεγαbetween them iii', 'salus electorum sanguis jesu or the death of death in the death of christ', 'some false principles which he hath framed unto himself as desire of self sufficiency', 'that of αντιλυτρον timothy do always denote by the not-to-be wrested genuine signification of', 'that ye have need of all these things mt god hopeth and expecteth divers', 'the conclusion by all the strength and skill of mr more neither is that', 'the sum of all is the death and blood shedding of jesus christ hath', 'things but because he doth not destroy them now that their proud god opposing', 'to the right honorable robert earl of warwick f232 etc my lord it is', 'to the right honorable the lords and gentlemen of the committee for religion f1', 'unite my heart to fear thy name psalm the god in whose hand try', 'we may nay we must grant twofold praying in our savior one by virtue', 'what hast thou that thou didst not receive corinthians are we better than they']

Updated whitelist:
```json
"dense_source_window_loss": ["acts ephesians as distinguished from the world romans john his elect romans his children", "all justified and made blessed through non imputation of their sin they who have", "and room with an intention that he should live samuel romans so that christ", "and the performance of good works is in their apprehension condition pre required to", "and upon their consciences by reason of not understanding of this love which came", "consolation by his death chapter objections are answered being consideration of thomas more's reply", "dagon cannot keep on his head nor the idol of uncontrollable free will enjoy", "declared throughout all the earth chap 28-30 who are the called according to his", "discovery of new geometrical proportion exclaim we have found it we have found it", "foolishly that he is altogether like unto us psalm one of which inconveniences all", "foreskin of your heart and be no more stiff necked deuteronomy and the lord", "him for foundation stone tried stone precious corner stone sure foundation isaiah that whosoever", "him is opposite to his eternal blessedness and all sufficiency thirdly god therefore to", "in excellent order as is at large declared in that golden psalm and this", "inasmuch as it conducteth to that end otherwise as weariness of the flesh ecclesiasties", "judge of the rest of their fruit mors in olla mors in olla their", "many in the conception and publication of some easily invented false opinions is it", "many sons unto glory for god sent his only begotten son into the world", "multiply genesis nor yet leave them to self subsistence he in the meantime only", "nature for his glory was the glory of the only begotten of the father", "needful of any more value for first those that were saved were saved upon", "now this whole dispensation with especial regard to the death and blood shedding of", "of bellarmine man otherwise not over well affected to truth predestination saith he from", "one may see that can but read english in ore hence that multiplicity of", "opinion of his idol's deity and self sufficiency in the hearts of divers that", "or gave himself ransom but for many or only for many or only for", "psalmist from whence the apostle citeth these words psalm and did he die for", "respect of conformity to the rule and so there is \u03c7\u03b1\u03c3\u03bc\u03b1 \u03bc\u03b5\u03b3\u03b1between them iii", "salus electorum sanguis jesu or the death of death in the death of christ", "some false principles which he hath framed unto himself as desire of self sufficiency", "that of \u03b1\u03bd\u03c4\u03b9\u03bb\u03c5\u03c4\u03c1\u03bf\u03bd timothy do always denote by the not-to-be wrested genuine signification of", "that ye have need of all these things mt god hopeth and expecteth divers", "the conclusion by all the strength and skill of mr more neither is that", "the sum of all is the death and blood shedding of jesus christ hath", "things but because he doth not destroy them now that their proud god opposing", "to the right honorable robert earl of warwick f232 etc my lord it is", "to the right honorable the lords and gentlemen of the committee for religion f1", "unite my heart to fear thy name psalm the god in whose hand try", "we may nay we must grant twofold praying in our savior one by virtue", "what hast thou that thou didst not receive corinthians are we better than they"]
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
7. Verify Need drops from 4.4 to target

## What NOT To Do

1. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage
   is already 99.43% (above the 99% threshold). Whitelisting has zero effect.
2. **Do NOT remove `low_latin_tagging` from `ignored_warnings`** — It would ADD penalty points.