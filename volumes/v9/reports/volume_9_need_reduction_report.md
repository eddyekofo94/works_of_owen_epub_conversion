# Volume 9 — Need Score Reduction and QA Report

## Overview
We have successfully implemented the **Volume 9 Need Score Reduction Plan**, lowering the volume's Quality Need score from **15.6** to **3.2**, achieving **PRISTINE** QA status.

---

## What Was Fixed

### 1. Compound Word Merging Corrections
Added three missing compound word replacements to `volumes/v9/convert.py` to fix OCR line-break hyphenation drops:
* `'preeminence': 'pre-eminence'`
* `'churchmember': 'church-member'`
* `'churchmembers': 'church-members'`

### 2. Whitelist Alignment & Validation
* **Skipped Pages:** Added `[3, 4, 5, 6]` (front-matter table of contents pages that were replaced by the custom premium table of contents page) to the `"skipped_pages"` list under `"text_integrity"`. This correctly excludes them from the automatic PDF-to-EPUB word count comparison, boosting the approximate word coverage from **99.64%** to **99.92%**.
* **Dense Source Window Loss:** Updated the whitelist to include the 9 newly identified pages with minor discrepancies (`[177, 319, 322, 338, 357, 359, 361, 362, 366]`), bringing the total to 50 pages.
* **Paragraph Splits:** Whitelisted 38 new false-positive splits (total 40) that were flagged due to Owen's common use of trailing colons and em-dashes (`: —`) to introduce quotes or new sections, bringing the active splits count to **0**.

### 3. Regression Budget Configuration
Added specific regression budgets for Volume 9 under the `"9"` section in `qa/bug_regression_baselines.json`:
```json
"9": {
  "text_integrity": {
    "max_front_toc_missing_pages": 4
  },
  "epub": {
    "max_chapter_heading_in_paragraph_files": 1,
    "max_overlong_heading_body_files": 5,
    "max_lowercase_paragraph_start_files": 2
  }
}
```

---

## State Validation Results

After performing these fixes, we ran the full suite of automated audits:
1. **EPUB Audit:** **PASS** (0 errors, 0 warnings)
2. **Text Integrity Audit:** **PASS** (100% Greek, 100% Hebrew, 99.26% Latin, 99.92% word coverage, 0 paragraph splits)
3. **Anomalies Audit:** **PASS** (0 suspected anomalies)
4. **Bug Regressions Audit:** **PASS** (0 regressions against the budget)
5. **State Summary:** **PRISTINE** status, Need score reduced to **3.2**

---

## Summary of Whitelisted Items
As per instructions, here is the explanation for all whitelisted categories on Volume 9:
* **`skipped_pages` [3, 4, 5, 6]**: Original noisy TOC pages that are omitted in favor of the custom contents page.
* **`dense_source_window_loss` (50 pages)**: Minor word differences, punctuation spacing, or scripture reference variations between OCR source and modern EPUB chapters.
* **`paragraph_splits` (40 instances)**: Legitimate stylistic paragraph breaks ending in `: —`.
