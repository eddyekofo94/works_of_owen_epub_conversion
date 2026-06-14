# Whitelist Legitimacy Audit — Volumes 7 & 8

**Date:** 2026-06-14
**Auditor:** opencode (automated EPUB + audit cross-reference)
**Scope:** `volumes/v7/bugs_fixes/volume_7_whitelist.{json,md}` and `volumes/v8/bugs_fixes/volume_8_whitelist.{json,md}`
**Method:** Each whitelisted item was verified against the actual EPUB XHTML content, the text integrity audit reports, and the bug regression reports.

---

## VOLUME 7 — Findings

### 1. OCR & Bracket Residues — REQUIRES CLEANUP

The JSON lists 6 entries: `sal vation`, `r own`, `S atan`, `l st`, `T he`, `u that`.

| Entry | Found in EPUB? | Verdict | Reason |
|-------|---------------|---------|--------|
| `sal vation` | **No** | **STALE — remove** | Not present in any XHTML file. Was likely fixed by a prior `text_replacements` pass but the whitelist entry was never removed. Leaving it causes the audit to suppress a warning for a pattern that no longer exists, and makes the whitelist harder to maintain. |
| `S atan` | **No** | **STALE — remove** | Not present in any XHTML file. Same situation as `sal vation`. |
| `T he` | **No** | **STALE — remove** | Not present in any XHTML file. Same situation. |
| `r own` | Yes (30+ hits) | **FALSE POSITIVE — relabel** | All occurrences are legitimate English: "their own", "our own". The anomaly detector flags the substring `r own` inside words like "thei**r own**", but these are not OCR errors — they are word-boundary false positives where the detector's word-splitting misses the apostrophe or punctuation boundary. Whitelisting them is fine, but the `.md` should describe them as "scanner substring false positives" rather than "OCR & Bracket Residues" to avoid confusion. |
| `l st` | Yes (20+ hits) | **FALSE POSITIVE — relabel** | All occurrences are legitimate English substrings: "spiri**tual st**rength", "rea**l st**ate", "fina**l st**ate". Same explanation as `r own`. Relabel as false positive. |
| `u that` | Yes (2 hits) | **FALSE POSITIVE — needs repair** | Found in ch042 ("so u that if they repeat not the same sin") and ch036 ("who shall give you that which is your own?"). The ch042 occurrence is a genuine OCR artifact: "so u that" should read "so, that" or similar. The ch036 hit is a legitimate substring in "yo**u that**". **Action:** Add `u that` → `so, that` (or what the PDF actually reads) to `text_replacements` in `volumes/v7/convert.py` for the ch042 case. The ch036 case is a false positive substring. If the OCR error was already partially fixed, remove from whitelist. |

### 2. Hyphenation Anomalies — ONE ITEM REQUIRES REPAIR

All 22 entries were verified as present in the EPUB. 21 of 22 are authentic 17th-century orthography and correctly whitelisted.

**Exception: `Adul-lam`**

- **Context:** "...when he escaped out of the cave at Adul-lam, and went thence unto Mizpeh of Moab..." (ch042.xhtml)
- **This is a PDF line-break carry-over, not authentic orthography.** The biblical place name is **Adullam** (1 Samuel 22:1). Owen's print edition writes "Adullam" as a single word. The hyphen appears because the PDF line-break split "Adul-" / "lam" across two lines and the paragraph-healing logic did not join it.
- **The correct spelling "Adullam" appears zero times in the EPUB.** The text only has the broken form.
- **Action:** Add `Adul-lam` → `Adullam` to `text_replacements` in `volumes/v7/convert.py`. Remove `Adul-lam` from the whitelist.

### 3. Mixed-Case Capitalization Errors — DISCREPANCY

The `.md` mentions `menlHow` as a Mixed-Case Capitalization Error. The JSON has an empty array: `"Mixed-Case Capitalization Errors": []`.

- **`menlHow` does not appear in the EPUB** — it was likely fixed earlier.
- **Action:** Remove `menlHow` from the `.md` file. Keep the JSON empty array as-is.

### 4. OCR Entry `them)is` — DOCUMENTATION-ONLY DISCREPANCY

The `.md` lists `them)is` as an OCR & Bracket Residue. The JSON does not include it.

- **`them)is` does not appear in the EPUB.** It was likely fixed but the `.md` was not updated.
- **Action:** Remove `them)is` from the `.md` file under the OCR section.

### 5. Punctuation Spacing Blemishes — LEGITIMATE (no action needed)

All 24 entries are verified as present in the EPUB. These are benign print spacing artifacts (`1 .`, `Lord ;`, `and ,`, `..`) that do not affect readability and are authentic to the AGES source layout.

### 6. Structural Nesting Sequence Jumps — LEGITIMATE (no action needed)

All 6 entries (`I. ... III.`, `III.`, `II.`, `1. ... 3.`, `II. ... XIX.`, `3. ... 5.`) are verified as genuine outline discontinuities in Owen's printed structure.

### 7. Unmatched Quotation Marks — PROBABLY LEGITIMATE

13 entries in JSON. Each is a scripture citation, Greek/Latin quote, or multi-paragraph blockquote. Spot-checking confirms:

- `Καὶ μέτοχοι γενηθέντες Πνεύματος ἁγίου` — Greek quote with partial closing quote
- `1. The gift of God, δωρεά, is either δόσις...` — inline Greek with nested quotes
- Multi-paragraph Owen exposition quotes open with `"` and close paragraphs later

These are structurally valid. **No action needed.**

### 8. Text Integrity — INCOMPLETELY DOCUMENTED

The JSON contains more entries than the `.md` documents:

| Category | JSON entries | MD documented | Missing from MD |
|---|---|---|---|
| `dense_source_window_loss` | [3, 4, 5, 6, 24, 31, 37, 39, 45] | "Pages 31, 37, 39, 45" | Pages 3, 4, 5, 6, 24 |
| `top_of_page_text_loss` | [3, 24, 183] | Not mentioned at all | All 3 pages |
| `bottom_of_page_text_loss` | [2] | Not mentioned at all | Page 2 |
| `front_matter_toc_loss` | [3, 7] | "Page 3" only | Page 7 |

**Action:** Update `volume_7_whitelist.md` section 2 to document all pages currently in the JSON, with explanations:

- **Pages 3–6, 24:** Dense source windows on TOC/prefatory pages and pages with Greek phrases or complex citations.
- **Page 183 (top_of_page):** Likely a chapter-boundary page where top-line text didn't align perfectly with the dense window scanner.
- **Page 2 (bottom_of_page):** Publisher imprint page, text loss is expected.
- **Page 7 (front_matter_toc_loss):** Continuation of the TOC override.

### 9. Paragraph Splits — LEGITIMATE but worth reviewing

21 entries in JSON. The `.md` only documents a subset. Key entries:

- `To The Reader`, `John Owen`, `BY THE LATE PIOUS AND LEARNED` — correct salutation/authorship breaks
- `Αδύνατον γὰρ τοὺς` — Greek epigraph starting a new section
- Em-dash entries (`—`, `— that is`) — Owen's characteristic inline exposition starts
- Enumerator entries (`III.`, `XIX.`, `(5thly.)`) — outline continuation points

**All are legitimate paragraph boundaries.** However, the `.md` should document all 21 entries (currently only shows a representative subset), or at minimum note the count and reference the JSON for the full list.

### 10. Latin Warning Suppression — JUSTIFIABLE but masks real gaps

The suppressed warnings are:
- `low_latin_tagging` — Tags ratio is 40.4% (159/394 words tagged)
- `low_latin_translation_coverage` — Translation ratio is 26.7% (12/45 runs translated)

The root cause is that the Latin detector flags common English words (`neighbor`, `advocate`, `palate`, `fervor`, `inveterate`) as untagged Latin because they share Latin etymology. These false positives inflate the "untagged" count and depress the tagging ratio.

**However**, genuinely untagged Latin phrases are also present and unaddressed:
- `Erasmus, ‡ "Fieri non` — untranslated Erasmus citation
- `etiam donum`, `nihilominus bonum`, `seculi futuri` — untranslated Latin phrases
- Greek-Latin bilingual phrases (`δωρεά, ἔστιν δόσις, "donatio"`) where the Latin portion is untagged

**Action:** The `low_latin_tagging` suppression is acceptable as a **temporary measure**, but the project should:
1. Improve the Latin detection heuristic to exclude common English words (`neighbor`, `advocate`, `palate`, `fervor`) and proper names (`Beza`, `Damasus`).
2. Add `<span lang="la">` tags to genuinely Latin phrases.
3. Add translation footnotes for the 33 untranslated Latin runs.

Until then, document in the `.md` that the suppression is a **known technical debt** masking a low tagging ratio.

### 11. Ignored Warnings — Review

| Warning | Verdict | Reason |
|---|---|---|
| `low_latin_tagging` | Acceptable temporarily | See §10 above |
| `low_latin_translation_coverage` | Acceptable temporarily | See §10 above |
| `repeated_windows` | **LEGITIMATE** | The repeated phrase "the grace and duty of being spiritually minded" is the treatise title, naturally occurring in transitional summaries |
| `roman_heading_candidates` | **LEGITIMATE** | Owen's outline numerals (I., II., III.) are legitimately non-heading |
| `enumerator_sequence_candidates` | **LEGITIMATE** | Authentic outline jumps |
| `dense_source_window_loss` | **LEGITIMATE** | Pages overridden by custom HTML or containing complex Greek |
| `front_matter_toc_loss` | **LEGITIMATE** | Custom TOC override |

---

## VOLUME 8 — Findings

### 1. OCR & Bracket Residues — REQUIRES CLEANUP

| Entry | Found in EPUB? | Verdict | Reason |
|-------|---------------|---------|--------|
| `y spirits` | Yes (`"try spirits"`, `"hasty spirits"`, `"y spirits"`) | **MIXED — one real OCR error, rest are false positives** | The `"y spirits"` occurrence in ch009 is a genuine OCR error: "indulge to y spirits" should likely be "indulge to your spirits" or similar. The other two hits ("try spirits", "hasty spirits") are legitimate substrings. **Action:** (a) Add a `text_replacements` fix for the ch009 OCR error. (b) Relabel the whitelist category from "OCR & Bracket Residues" to include a note about substring false positives. |
| `f or` | Yes (multiple) | **FALSE POSITIVE — relabel** | All occurrences are in legitimate English substrings: "of or", "for or", "difference of or opposition". The anomaly detector splits on these boundaries. Not an OCR error. |
| `p articular` | **No** | **STALE — remove** | Not present in any XHTML file. Was likely fixed earlier. |

### 2. Unmatched Quotation Marks — LEGITIMATE with count discrepancy

- JSON lists **22 entries**, `.md` says **28 instances**.
- The justification (multi-paragraph blockquotes, HTML span attributes, nested quotes) is sound.
- Spot-checked: `"Nothing so ill, but Christ† will compensate..."` with footnote superscript inside — the footnote `<a>` tag splits the quotation context, causing a false positive.
- **Action:** Reconcile the count. Verify all 22 JSON entries and update the `.md` to say 22, or verify 28 and update the JSON.

### 3. Ignored Warnings — MOSTLY LEGITIMATE, one concern

| Warning | Verdict | Reason |
|---|---|---|
| `front_matter_toc_loss` / `weak_page_coverage` | **LEGITIMATE** | Custom TOC HTML override |
| `orphan_endnotes` | **LEGITIMATE** | AGES source footnotes 5, 7, 30, 31 are naturally orphaned (content `--` or `-- x`) |
| `low_latin_tagging` / `low_latin_translation_coverage` / `low_latin_word_coverage` | **WEAK JUSTIFICATION** | See §4 below |
| `roman_heading_candidates` | **LEGITIMATE** | Outline numerals, not actual headings |
| `top_of_page_text_loss` / `bottom_of_page_text_loss` / `dense_source_window_loss` / `repeated_windows` / `suspicious_large_number_starts` | **LEGITIMATE** | Pages with overridden title pages, prefaces, and signatures |

### 4. Latin Warning Suppression — WEAK JUSTIFICATION

Volume 8 has:
- **Latin word coverage:** 99.84% (excellent)
- **Latin tagging ratio:** 43.1% (568/1,318 words tagged — poor)
- **Latin translation ratio:** 37.1% (63/170 runs translated — moderate)
- **107 untranslated Latin runs** remaining

The justification in the `.md` is: *"Volume 8 consists of sermons preached on public occasions and does not contain dense Latin theological disputations requiring full-scale academic translations."*

**This is partially incorrect.** While V8 is sermons rather than treatises, it contains:
- Lengthy Latin dedicatory epistles (e.g., `INCLYTISSIMO POPULI ANGLICANI CONVENTUI`, `PRISCA ANGLO-BRITANNORUM JURA`) spanning multiple pages
- Patristic citations (e.g., Justin Martyr, Chrysostom references)
- Theological Latin phrases throughout

The untagged Latin samples include words that **are** genuinely Latin but flagged as common English: `protector` (11 occurrences, 0 tagged), `macedonia` (11, 0), `palestina` (8, 0), `pilate` (8, 0). Some of these are borderline (proper nouns from Latin texts), but `hist` (15 occurrences, 1 tagged) is a genuine Latin abbreviation for "Historia" in citations.

**Action:**
1. **Remove `low_latin_word_coverage` from `ignored_warnings`.** This metric is at 99.84% and should not need suppression.
2. **Keep `low_latin_tagging` and `low_latin_translation_coverage` suppressed** but document this as technical debt.
3. **Add translation footnotes** for the untranslated Latin dedicatory epistles and patristic citations, which are scholarly content that readers would benefit from.

### 5. Paragraph Splits — LEGITIMATE (no action needed)

All 5 entries are correct paragraph boundaries:
- `Reader,` — salutation starting a preface
- `Sir` — salutation starting a dedicatory epistle
- `John Owen` — author signature line
- `Your devoted Servant` — signature block closer
- `—` — em-dash starting an inline syllabus list

---

## CROSS-CUTTING ISSUES

### A. JSON ↔ MD Synchronization Mandate Violated

Both volumes have discrepancies between their `.json` and `.md` whitelist files. Per AGENTS.md: *"you MUST maintain two copies of the whitelist under `volumes/vN/bugs_fixes/`: an agent-readable JSON format and a human-readable Markdown format describing and explaining each item."*

| Volume | Discrepancy | Details |
|---|---|---|
| V7 | `.md` mentions `them)is` and `menlHow` | Not in JSON; not in EPUB. Stale documentation. |
| V7 | `.md` only documents 4 dense pages | JSON has 9 (pages 3,4,5,6,24,31,37,39,45) |
| V7 | `.md` does not document `top_of_page_text_loss` or `bottom_of_page_text_loss` | JSON has both |
| V7 | `.md` only documents page 3 for `front_matter_toc_loss` | JSON has pages 3 and 7 |
| V8 | `.md` says "28 instances" of unmatched quotes | JSON has 22 entries |

**Action:** Regenerate both `.md` files from their respective `.json` files to ensure full synchronization. The `.md` should comprehensively document every entry in the `.json`.

### B. False Positive OCR Patterns Should Be Relabeled

Both volumes whitelist "OCR & Bracket Residues" that are actually scanner substring false positives (where the anomaly detector's word-boundary regex matches a substring across legitimate English word boundaries). These include:

- V7: `r own`, `l st`, `u that` (partial)
- V8: `f or` (partial), `y spirits` (partial)

**Action:** Create a new whitelist category `"Scanner Substring False Positives"` in both JSON files, and move the legitimate false-positive entries there. This distinguishes them from genuine OCR errors and makes the audit clearer.

### C. Stale Whitelist Entries (Not in EPUB)

These entries no longer appear in the rendered EPUB and should be removed from both `.json` and `.md`:

| Volume | Entry | Category |
|---|---|---|
| V7 | `sal vation` | OCR & Bracket Residues |
| V7 | `S atan` | OCR & Bracket Residues |
| V7 | `T he` | OCR & Bracket Residues |
| V8 | `p articular` | OCR & Bracket Residues |

### D. Items That Should Be Repaired Rather Than Whitelisted

The following are genuine text errors that should be fixed via `text_replacements` in the respective volume's `convert.py`, then removed from the whitelist:

| Volume | Current Form | Correct Form | Location | Reason |
|---|---|---|---|---|
| V7 | `Adul-lam` | `Adullam` | ch042 | PDF line-break carry-over, not authentic spelling |
| V7 | `u that` (ch042) | `so, that` (or per PDF) | ch042 | Genuine OCR error |

---

## IMPLEMENTATION CHECKLIST

### Volume 7

- [ ] **V7-1:** Add `Adul-lam` → `Adullam` to `text_replacements` in `volumes/v7/convert.py`
- [ ] **V7-2:** Remove `Adul-lam` from `Hyphenation Anomalies` in both `.json` and `.md`
- [ ] **V7-3:** Remove `sal vation`, `S atan`, `T he` from `OCR & Bracket Residues` in both `.json` and `.md` (stale entries, not in EPUB)
- [ ] **V7-4:** Move `r own`, `l st` to a new category `"Scanner Substring False Positives"` in both `.json` and `.md`
- [ ] **V7-5:** Investigate and repair `u that` in ch042 (add to `text_replacements` if confirmed OCR error), then remove from whitelist or move to false positives
- [ ] **V7-6:** Remove `them)is` from `.md` OCR section (not in EPUB, not in JSON)
- [ ] **V7-7:** Remove `menlHow` from `.md` Mixed-Case section (not in EPUB, not in JSON)
- [ ] **V7-8:** Add missing dense source window pages (3, 4, 5, 6, 24) to `.md` with explanations
- [ ] **V7-9:** Add `top_of_page_text_loss` (pages 3, 24, 183) and `bottom_of_page_text_loss` (page 2) to `.md` with explanations
- [ ] **V7-10:** Add page 7 to `front_matter_toc_loss` in `.md`
- [ ] **V7-11:** Add a note to `.md` about `low_latin_tagging` suppression being technical debt
- [ ] **V7-12:** Rebuild V7 EPUB with `--render-only` and re-run audits to verify `Adul-lam` fix

### Volume 8

- [ ] **V8-1:** Remove `p articular` from `OCR & Bracket Residues` in both `.json` and `.md` (stale, not in EPUB)
- [ ] **V8-2:** Investigate `"y spirits"` in ch009 — if genuine OCR error, add to `text_replacements`; relabel remaining `y spirits` and `f or` as `"Scanner Substring False Positives"`
- [ ] **V8-3:** Create `"Scanner Substring False Positives"` category; move `f or` there
- [ ] **V8-4:** Reconcile unmatched quotation mark count (JSON=22, MD=28)
- [ ] **V8-5:** Remove `low_latin_word_coverage` from `ignored_warnings` (coverage is 99.84%, no need to suppress)
- [ ] **V8-6:** Add a note in `.md` that `low_latin_tagging` and `low_latin_translation_coverage` are technical debt, with a recommendation to add translation footnotes for the 107 untranslated Latin runs
- [ ] **V8-7:** Regenerate `.md` from `.json` to ensure full synchronization

### Cross-Volume

- [ ] **X-1:** Consider improving the Latin detection heuristic in `audit_text_integrity.py` (or whichever script generates these warnings) to exclude common English words (`neighbor`, `advocate`, `palate`, `fervor`, `inveterate`, `protector`, `macedonia`, `pilate`) from the untagged Latin count. This would eliminate the need for `low_latin_tagging` suppression in both volumes.