# Whitelist Legitimacy Audit — Volume 7

**Date:** 2026-06-15
**Auditor:** opencode (automated EPUB + audit cross-reference)
**Scope:** `volumes/v7/bugs_fixes/volume_7_whitelist.{json,md}`
**EPUB:** `volumes/v7/output/volume_7.epub`
**State report score:** Need 9.6 (PRISTINE, rank 12)

---

## 1. Audit Checklist Status (from 2026-06-14 audit)

All 12 original audit items have been completed:

| Item | Description | Status | Notes |
|------|-------------|--------|-------|
| V7-1 | Add `Adul-lam` → `Adullam` to text_replacements | ✅ Done | Confirmed in EPUB |
| V7-2 | Remove `Adul-lam` from whitelist | ✅ Done | Not in JSON Hyphenation Anomalies |
| V7-3 | Remove stale OCR entries (`sal vation`, `S atan`, `T he`) | ✅ Done | `OCR & Bracket Residues` is `[]` |
| V7-4 | Relabel false positives to `Scanner Substring False Positives` | ✅ Done | `r own`, `l st` correctly categorized |
| V7-5 | Repair `u that` in ch042 | ✅ Done | `'so u that': 'so that'` in text_replacements |
| V7-6 | Remove `them)is` from `.md` | ✅ Done | Not present |
| V7-7 | Remove `menlHow` from `.md` | ✅ Done | Not present |
| V7-8 | Document all dense source window pages in `.md` | ✅ Done | All 9 pages documented |
| V7-9 | Document top/bottom of page text loss in `.md` | ✅ Done | Pages 3, 24, 183 (top) and 2, 103 (bottom) |
| V7-10 | Add page 7 to front_matter_toc_loss in `.md` | ✅ Done | Pages 3 and 7 both documented |
| V7-11 | Note `low_latin_tagging` as technical debt in `.md` | ⚠️ Partial | `low_latin_tagging`/`low_latin_translation_coverage` removed from `ignored_warnings` but `.md` does not document this gap |
| V7-12 | Rebuild V7 EPUB and verify | ✅ Done | EPUB confirms fixes |

---

## 2. Current Quality Metrics

| Metric | Value |
|--------|-------|
| EPUB Audit | PASS — 0 errors, 0 warnings |
| Text Integrity | WARN — 2 warnings (`low_latin_tagging`, `low_latin_translation_coverage`) |
| Bug Regressions | PASS — all 48 checks OK |
| Coverage | 99.77% |
| Greek word coverage | 100% (0 untagged chars) |
| Hebrew word coverage | 100% (0 untagged chars) |
| Latin coverage | 99.66% |
| Latin tagging ratio | 51.2% (151/295 words tagged) |
| Latin translation ratio | 71.4% (30/42 runs translated) |
| Faulty paragraph splits | 0 |
| Short fragments | 22 |
| Repeated word windows | 25 (at budget ceiling) |
| Footnotes | 91 noterefs, 91 anchors, 0 orphan endnotes |

---

## 3. Whitelist Verification — Anomalies

### Scanner Substring False Positives (2 items)
All verified as legitimate substrings, not OCR errors:
- `r own` — matches "their own", "our own"
- `l st` — matches "spiritual strength", "real state"

### Hyphenation Anomalies (19 items)
All 19 entries are authentic 17th-century orthography. Verified in EPUB:
`Spiritual-mindedness`, `ale-house`, `cross-ways`, `evil-doer`, `fire-ball`, `hand-breadth`, `here-withal`, `new-fangledness`, `non-proficiency`, `over-earnest`, `over-fullness`, `over-valuation`, `pre-admonition`, `pre-admonitions`, `stout-hearted`, `stout-heartedness`, `three-fold`, `top-stone`, `un-commanded`, `un-humbled`, `where-into`

### Punctuation Spacing Blemishes (17 items)
All verified as benign print spacing artifacts (`..`, `1 .`, `and ,`, `Lord ;`, etc.).

### Structural Nesting Sequence Jumps (6 items)
All verified as authentic outline discontinuities in Owen's printed structure.

### Unmatched Quotation Marks (13 items)
All verified as structurally valid — scripture citations, Greek/Latin quotes, and multi-paragraph blockquotes.

### OCR & Bracket Residues (0 items) ✅
Properly empty after cleanup.

### Mixed-Case Capitalization Errors (0 items) ✅
Properly empty after cleanup.

---

## 4. Whitelist Verification — Text Integrity

### Front Matter & Dense Pages
- **Pages 3, 7** (front_matter_toc_loss): Overridden by custom HTML TOC (`_V7_CONTENTS_PAGE`).
- **Pages 3, 4, 5, 6, 24, 31, 37, 39, 45** (dense_source_window_loss): Dense source windows on introductory/Greek pages.

### Top/Bottom of Page Text Loss
- **Pages 3, 24, 183** (top_of_page): Chapter boundary and header pages.
- **Pages 2, 103** (bottom_of_page): Publisher imprint and bottom Latin quote.

### Weak Pages
- **Page 25**: Heavily polyglot Greek/Hebrew page.

### Paragraph Splits (26 items)
All verified as correct paragraph boundaries — salutations, Greek epigraphs, em-dash transitions, outline markers.

### Inline Structural Markers (4 items)
All verified as authentic inline enumerators within prose.

### Ignored Warnings (5 items)
- `repeated_windows`: Treatise title naturally repeated.
- `roman_heading_candidates` / `enumerator_sequence_candidates`: Authentic outline jumps.
- `dense_source_window_loss` / `front_matter_toc_loss`: Custom HTML overrides.

---

## 5. Remaining Technical Debt

### Latin Tagging & Translation (MEDIUM priority)
**Issue:** `low_latin_tagging` and `low_latin_translation_coverage` warnings are **no longer suppressed** in the whitelist's `ignored_warnings`, but the `.md` does not document this gap.
- Latin tagging: 51.2% (threshold ~80%)
- Latin translation: 71.4% (threshold ~80%)
- Root cause: Latin detector flags common English words (`sincere`, `poor`, `advocate`, `palate`, `fervor`) as untagged Latin.

**Action needed:** Add to `volume_7_whitelist.md` Section 3:
> `low_latin_tagging` / `low_latin_translation_coverage`: Technical Debt. Latin tagging is at 51.2%, translation at 71.4%. Common English words inflate the untagged count. Adding targeted `<span lang="la">` tags and translation footnotes for genuinely Latin phrases would improve these metrics over time.

---

## 6. Files Reference

| File | Location |
|------|----------|
| Whitelist JSON | `volumes/v7/bugs_fixes/volume_7_whitelist.json` |
| Whitelist MD | `volumes/v7/bugs_fixes/volume_7_whitelist.md` |
| EPUB Audit | `volumes/v7/bugs_fixes/volume_7_audit.json` / `.md` |
| Text Integrity | `volumes/v7/bugs_fixes/volume_7_text_integrity.json` / `.md` |
| Bug Regressions | `volumes/v7/bugs_fixes/volume_7_bug_regressions.json` / `.md` |
| Anomalies | `volumes/v7/bugs_fixes/volume_7_anomalies.json` / `.md` |
| Convert Script | `volumes/v7/convert.py` (text_replacements) |
