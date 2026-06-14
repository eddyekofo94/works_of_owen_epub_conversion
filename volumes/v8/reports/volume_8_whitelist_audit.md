# Whitelist Legitimacy Audit — Volume 8

**Date:** 2026-06-15
**Auditor:** opencode (automated EPUB + audit cross-reference)
**Scope:** `volumes/v8/bugs_fixes/volume_8_whitelist.{json,md}`
**EPUB:** `volumes/v8/output/volume_8.epub`
**State report score:** Need 12.0 (PRISTINE, rank 11)

---

## 1. Audit Checklist Status (from 2026-06-14 audit)

| Item | Description | Status | Notes |
|------|-------------|--------|-------|
| V8-1 | Remove `p articular` from whitelist | ✅ Done | Not in EPUB, `OCR & Bracket Residues` is `[]` |
| V8-2 | Fix `y spirits` OCR error | ✅ Done | `'will so indulge to y spirits': 'will so indulge to your spirits'` in text_replacements. Remaining hits (`try spirits`, `haughty spirits`, `hasty spirits`) are legitimate English. |
| V8-3 | Create `Scanner Substring False Positives` category | ✅ Done | `f or` moved there |
| V8-4 | Reconcile unmatched quote count | ✅ Done | JSON=27, MD=27 — synchronized |
| V8-5 | Remove `low_latin_word_coverage` from ignored_warnings | ✅ Done | Not in ignored_warnings |
| V8-6 | Latin warning documentation | ⚠️ Gap | `low_latin_tagging`/`low_latin_translation_coverage` removed from `ignored_warnings` but `.md` Section 3 does not document them as tech debt |
| V8-7 | Regenerate `.md` from `.json` | ✅ Done | Both files synchronized |

---

## 2. Current Quality Metrics

| Metric | Value |
|--------|-------|
| EPUB Audit | PASS — 0 errors, 0 warnings |
| Text Integrity | WARN — 2 warnings (`low_latin_tagging`, `low_latin_translation_coverage`) |
| Bug Regressions | PASS — all 48 checks OK |
| Coverage | 99.95% |
| Greek word coverage | 100% (0 untagged chars) |
| Hebrew word coverage | 100% (0 untagged chars) |
| Latin coverage | 99.8% |
| Latin tagging ratio | 56.1% (562/1002 words tagged) |
| Latin translation ratio | 64.7% (108/167 runs translated) |
| Faulty paragraph splits | 0 |
| Short fragments | 53 |
| Repeated word windows | 25 (at budget ceiling) |
| Footnotes | 362 noterefs, 366 anchors, 4 orphan endnotes |
| Anomalies (whitelisted) | 145 items across 6 categories |

---

## 3. Whitelist Verification — Anomalies

### Scanner Substring False Positives (1 item)
- `f or` — matches "of or", "for or", "difference of or opposition"

### Hyphenation Anomalies (42 items)
All verified as authentic 17th-century orthography except:

**⚠️ `Giles-inthe` — probable line-break carry-over (MUST FIX)**
- EPUB context: *"...St. Giles-inthe [Field]..."*
- The original text reads "St. Giles-in-the-Fields" (a London parish). The PDF line-break split `Giles-` / `inthe` across lines and the paragraph healer joined it as `Giles-inthe`.
- **Action:** Add `'Giles-inthe': 'Giles-in-the'` to `text_replacements` in `volumes/v8/convert.py`, then remove from whitelist. This is NOT authentic orthography.

All other hyphenations are verified authentic (e.g., `Beerlahai-roi` = biblical place name Gen 16:14, `mitred-confirmations` = Owen's compound term, `Sabbath-breaker`, `evil-doer`, etc.).

### Punctuation Spacing Blemishes (41 items)
All verified as benign print spacing artifacts. No action needed.

### Structural Nesting Sequence Jumps (34 items)
All verified as authentic outline discontinuities from Owen's complex sermon structures.

### Unmatched Quotation Marks (27 items)
All verified as structurally valid — multi-paragraph sermon blockquotes, nested citations, inline Hebrew/Latin quotes, and HTML span artifacts in title pages.

### OCR & Bracket Residues (0 items) ✅
Properly empty after cleanup.

---

## 4. Whitelist Verification — Text Integrity

### Front Matter & Dense Pages
- **Pages 3, 4** (front_matter_toc_loss): Overridden by custom HTML TOC (`_V8_CONTENTS_PAGE`).

### Orphan Endnotes (4 items)
- Footnotes 5, 7, 30, 31 — all contain `--` or `-- x` in the AGES source, never cited in the body. Legitimate orphan endnotes.

### Paragraph Splits (14 items)
All verified as correct paragraph boundaries:
- Salutations: `Reader,`, `Sir`, `John Owen`, `Your devoted Servant`
- Latin dedication lines: `AMPLISSIMO`, `SENATUI,`, `INCLYTISSIMO`, `OB`, `ADMINISTRATAM;`, `POTISSIMUM`, `D.D.C. JOANNES OWEN.`
- Em-dash: `—`
- Transitions: `All these things being considered, I cannot so well close with them`, `PATRIAM (NEFARUS QUORUNDAM`

### Ignored Warnings (10 items)
- `front_matter_toc_loss`: Custom TOC override.
- `suspicious_large_number_starts`: Legitimate sermon paragraph starts.
- `repeated_windows`: Sermon titles naturally repeated.
- `weak_page_coverage` / `dense_source_window_loss` / `top_of_page_text_loss` / `bottom_of_page_text_loss`: Title pages, prefaces, and signatures.
- `orphan_endnotes`: AGES source placeholders.
- `roman_heading_candidates`: Outline numerals, not headings.
- `missing_latin_clauses`: English translation blocks break Latin sentence contiguity on the dedication page.

---

## 5. Remaining Technical Debt

### HIGH: `Giles-inthe` — Must Fix

**Current:** Whitelisted as "authentic" hyphenation. **This is incorrect.**
- `Giles-inthe` is a PDF line-break carry-over from "St. Giles-in-the-Fields"
- Should be repaired to `Giles-in-the` via `text_replacements`
- Remove from `Hyphenation Anomalies` in both JSON and MD

**Steps:**
1. Add `'Giles-inthe': 'Giles-in-the'` to `volumes/v8/convert.py` OVERRIDES `text_replacements`
2. Remove `"Giles-inthe"` from `volume_8_whitelist.json` `Hyphenation Anomalies`
3. Remove from `volume_8_whitelist.md` hyphenation list
4. Re-render: `.venv/bin/python3 volumes/v8/convert.py --render-only`
5. Verify in EPUB

### MEDIUM: Latin Warning Documentation Gap

**Issue:** `low_latin_tagging` and `low_latin_translation_coverage` were removed from `ignored_warnings` but the `.md` doesn't document this.
- Latin tagging: 56.1% (threshold ~80%)
- Latin translation: 64.7% (threshold ~80%)
- Common English false positives inflating untagged count: `protector` (11, 0 tagged), `macedonia` (11, 0), `palestina` (8, 0), `pilate` (8, 0), `vice-chancellor` (4, 0), `apud` (3, 0)

**Action:** Add to `volume_8_whitelist.md` Section 3:
> `low_latin_tagging` / `low_latin_translation_coverage`: Technical Debt. Latin tagging at 56.1%, translation at 64.7%. The Latin detector flags common English words and proper nouns (protector, macedonia, pilate, vice-chancellor). Lengthy Latin dedicatory epistles (e.g., INCLYTISSIMO POPULI ANGLICANI CONVENTUI) and patristic citations remain partially untagged and untranslated. Targeted `<span lang="la">` tagging and translation footnotes would improve these metrics.

### LOW: Anomaly Count Reduction (Optional)

V8 has 145 whitelisted anomaly items (42 hyphenation + 41 punctuation + 34 nesting + 27 quotes + 1 substring false positive). The punctuation spacing blemishes could be reduced via `text_replacements` entries (e.g., `'e )'`, `'s )'`, `'Colchester ,'`, `'Zion ,'`), but this is cosmetic and non-blocking.

---

## 6. Files Reference

| File | Location |
|------|----------|
| Whitelist JSON | `volumes/v8/bugs_fixes/volume_8_whitelist.json` |
| Whitelist MD | `volumes/v8/bugs_fixes/volume_8_whitelist.md` |
| EPUB Audit | `volumes/v8/bugs_fixes/volume_8_audit.json` / `.md` |
| Text Integrity | `volumes/v8/bugs_fixes/volume_8_text_integrity.json` / `.md` |
| Bug Regressions | `volumes/v8/bugs_fixes/volume_8_bug_regressions.json` / `.md` |
| Anomalies | `volumes/v8/bugs_fixes/volume_8_anomalies.json` / `.md` |
| Convert Script | `volumes/v8/convert.py` (text_replacements) |
