# Volume 7 — Coverage Gap Reduction Plan

**Volume:** 7 (Apostasy, Spiritually-Mindedness, Dominion of Sin and Grace)  
**Current Need:** 9.2 (entirely from word coverage)  
**Current Coverage:** 99.77%  
**Target:** ≥99.90% (Need ≤4.0), ideally ≥99.95% (Need ≤2.0)

---

## The Problem

The entire Need score of 9.2 comes from a single penalty: `(1 - 0.9977) × 4000 = 9.2`.  
Every other component is zero:

| Component | Value | Penalty |
|---|---|---|
| Greek coverage | 100% | 0 |
| Hebrew coverage | 100% | 0 |
| Latin coverage | 99.66% | 0 (above 99% threshold) |
| Latin tagging | 63.73% | 0 (whitelisted) |
| Latin translation | 100% | 0 |
| Citations | 0/4 unresolved | 0 |
| Splits | 0 | 0 |
| Warnings | 0 | 0 |
| Errors | 0 | 0 |
| Anomalies | 0 | 0 |
| Unmatched quotes | 0 | 0 |

**The word coverage penalty formula is `(1 - coverage) × 4000`, capped at 20.**  
At 99.77% coverage, the penalty is exactly 9.2. Getting it below 4.0 requires ≥99.90% coverage.

### Target Milestones

| Coverage Needed | Tokens to Recover | Resulting Need |
|---|---|---|
| 99.80% | +69 | 8.0 |
| 99.85% | +173 | 6.0 |
| 99.90% | +230 | 4.0 |
| 99.95% | +345 | 2.0 |
| 100.00% | +531 | 0.0 |

**Current gap: ~531 PDF tokens are not matched in the EPUB.**

---

## How Coverage Is Calculated

The coverage ratio is computed in `scripts/audit_text_integrity.py` as:

```python
overlap = sum(min(pdf_count, epub_count) for word, pdf_count in pdf_counts.items())
coverage = overlap / pdf_total
```

For each unique word, it takes `min(how_many_times_in_PDF, how_many_times_inEPUB)`.  
If a word appears 3 times in the PDF but only 1 time in the EPUB, that word contributes a gap of 2 tokens.  
Excess EPUB words (e.g., "digital", "theological" from endnotes) do NOT reduce coverage — they're just ignored.

### Known Missing Word

| Word | PDF count | EPUB count | Gap |
|---|---|---|---|
| `editor` | 3 | 1 | 2 tokens |

The other ~529 missing tokens are distributed across many words with small count differences. These come from pages where dense text windows fail to match between PDF and EPUB.

---

## Source 1: Front Matter TOC Pages (Pages 3 and 7)

**This is the highest-leverage fix.**

The custom `_V7_CONTENTS_PAGE` in `volumes/v7/convert.py` replaces the raw PDF TOC on pages 3 and 7 with hand-crafted HTML. If the custom HTML does not contain every word that the PDF's original TOC contains, those words count as "missing" and drive down coverage.

### What to do

1. **Extract the raw PDF text from pages 3 and 7** by reading the JSON intermediate:

```bash
python3 -c "
import json
with open('volumes/v7/intermediate/volume_7.json') as f:
    data = json.load(f)
for ch in data['chapters']:
    for page in ch.get('pages', []):
        pnum = page.get('page_number', page.get('number', 0))
        if pnum in [3, 7]:
            print(f'--- Page {pnum} ---')
            text = page.get('text', page.get('content', ''))
            if isinstance(text, list):
                text = ' '.join(text)
            print(text[:2000])
            print()
"
```

2. **Compare every word** in the PDF TOC text against the custom HTML in `_V7_CONTENTS_PAGE`. Look for:
   - Chapter titles or subtitles that appear in the PDF but are missing or paraphrased in the custom HTML
   - Page number references (e.g., "Page 5", "p. 5") that are in the PDF but not in the HTML
   - Any connective text like "The Nature and Causes of Apostasy from the Gospel" vs a shortened form

3. **Update `_V7_CONTENTS_PAGE`** to include any missing words. The custom HTML should contain at minimum every substantive word from the original PDF TOC. Small formatting differences (punctuation, whitespace) are fine since the coverage check normalizes words (lowercases, strips accents). But missing substantive words like chapter titles or descriptions directly reduce the overlap count.

### Why this matters

The PDF TOC on pages 3 and 7 contains dense, word-rich text listing all chapter titles, subtitles, and descriptions. If the custom HTML TOC is a condensed version that omits words like "Declared", "Directions", "Profession", or other words from the original, each omission costs tokens. Two full TOC pages worth of text could represent 100-200+ tokens.

---

## Source 2: Dense Source Window Mismatches (31 Pages)

The text integrity audit reports 31 pages where dense PDF word windows failed to match in the EPUB text. **None of these are in the current whitelist** (the whitelisted pages 3, 4, 5, 6, 24, 31, 37, 39, 45 are from a previous audit run and no longer have losses).

These 31 pages contain ~531 missing tokens spread across them. The key pages to investigate:

### High-Priority Pages (Likely Fixable)

| Page | Sample Text from PDF | Issue | Fix |
|---|---|---|---|
| 82 | `expose the doctrine of it and the law of obedience con rained in it` | OCR artifact: `con rained` → `constrained` | Add to `text_replacements` |
| 42 | `what sense they taste of it ρημα is properly verbum dictum word spoken` | Greek/Latin inline text; possible Unicode normalization mismatch | Verify Greek word `ρημα` is correctly extracted |
| 64 | `our apostle speaks romans considering nothing in god but mercy` | Possible line-break or word-join issue | Check JSON intermediate for split words |
| 25 | `της δωρεας της επουρανιου vulg lat gustaverant etiam donum coeleste` | Heavy polyglot (Greek + Latin); already whitelisted as weak page | May be unfixable due to font-encoding complexity |
| 26 | `τον υιον του θεου rursum crucifigentes sibimetipsis filium dei` | Polyglot; verify Latin words appear correctly in EPUB | Check EPUB for `rursum` vs `rursum` etc. |
| 103 | `success or progress in the world but latius excisae serpit contagio gentis` | Latin phrase may have tokenization issues | Verify Latin phrase is intact in EPUB |

### Medium-Priority Pages (Formatting/Variation)

| Page | Sample Text | Likely Cause |
|---|---|---|
| 76 | `crying out the temple of the lord the temple of the lord` | Repeated phrase (scripture quote) — may have em-dash or formatting difference |
| 93 | `writings of justin martyr irenaeus clemens origen tatianus athenaguras` | Proper names; `athenaguras` may be OCR for `Athenagoras` |
| 95 | `continued for sundry ages afterward and for the latter or pela gianism` | Possible word split: `pela gianism` → `Pelagianism` |
| 183 | `39-41 and that of the apostles acts 25-27` | Scripture reference formatting |
| 201 | `severity it may be of self conceitedness and hypocrisy` | Hyphenation: `self-conceitedness` vs `self conceitedness` |
| 221 | `an habitual course in any sin is utterly inconsistent` | May be a page boundary issue |

### Lower-Priority Pages (Likely Minor)

Pages 245, 261, 272, 278, 283, 290, 314, 327, 377, 388, 397, 451, 455, 456, 519, 523, 532, 559 — these likely have small word-level mismatches from Unicode normalization, accent handling, or minor formatting differences. Investigate each only if the higher-priority fixes don't recover enough tokens.

### How to Investigate Each Page

For each page with a dense source window mismatch:

```bash
# 1. Check the PDF text for that page in the JSON intermediate
python3 -c "
import json
with open('volumes/v7/intermediate/volume_7.json') as f:
    data = json.load(f)
for ch in data['chapters']:
    for page in ch.get('pages', []):
        pnum = page.get('page_number', page.get('number', 0))
        if pnum == 82:
            print(f'--- Page {pnum} ---')
            text = page.get('text', page.get('content', ''))
            if isinstance(text, list):
                text = ' '.join(text)
            print(text[:3000])
"

# 2. Search the EPUB for the same text
rg 'con rained' volumes/v7/output/EPUB/
rg 'constrained' volumes/v7/output/EPUB/

# 3. If the word is in the PDF but misspelled/missing in the EPUB,
#    add a text_replacement in convert.py
```

### OCR Fixes to Add

Based on the page samples, these `text_replacements` entries should be added to `volumes/v7/convert.py`:

```python
'text_replacements': {
    # ... existing entries ...
    'con rained': 'constrained',        # Page 82: OCR line-break artifact
    'pela gianism': 'Pelagianism',       # Page 95: OCR line-break artifact (verify in PDF first)
    'athenaguras': 'Athenagoras',        # Page 93: OCR misprint (verify in PDF first)
},
```

**IMPORTANT:** Verify each OCR fix against the PDF before adding. Some apparent "errors" may be authentic 17th-century spellings (see AGENTS.md: "NEVER modernize 17th-century orthography").

---

## Source 3: The `editor` Word Gap

The audit reports `editor` appears 3 times in the PDF but only 1 time in the EPUB. Two instances are missing.

**Likely cause:** The PDF's title page or front matter says something like "Edited by William H. Goold" and "Editor" appears in the imprint, but the custom EPUB front matter only includes one of these instances.

**Fix:** Check the `_V7_CONTENTS_PAGE` and any custom title/front matter HTML in `convert.py`. Ensure text like "Edited by" or "Editor" that appears in the PDF's imprint page is also present in the EPUB's corresponding page.

---

## Source 4: Excess EPUB Words (Informational)

These words appear more in the EPUB than the PDF — they come from auto-generated endnote content (citation footnotes). They do **not** reduce coverage (coverage only cares about PDF words missing from EPUB), but they're worth noting:

| Word | PDF | EPUB | Source |
|---|---|---|---|
| `translated` | 4 | 24 | Endnote footnotes |
| `digital` | 0 | 10 | "Digital edition" boilerplate |
| `theological` | 0 | 9 | Endnote footnotes |
| `historical` | 1 | 9 | Endnote footnotes |
| `greek` | 3 | 10 | Endnote footnotes |
| `modern` | 1 | 8 | Endnote footnotes |
| `footnotes` | 0 | 7 | Endnote footnotes |
| `edition` | 4 | 10 | Endnote footnotes |
| `hebrew` | 1 | 7 | Endnote footnotes |

**No action needed** — these are legitimate additions from the converter's endnote system.

---

## Implementation Checklist

### Step 1: Fix Front Matter TOC (Highest Impact)

- [ ] Extract PDF text from pages 3 and 7 using the JSON intermediate
- [ ] Compare every word against `_V7_CONTENTS_PAGE` in `convert.py`
- [ ] Add any missing words/titles to the custom HTML
- [ ] Rebuild: `.venv/bin/python3 volumes/v7/convert.py --render-only`
- [ ] Re-audit: `.venv/bin/python3 scripts/audit_text_integrity.py 7`
- [ ] Check if coverage improved

### Step 2: Fix OCR Artifacts

- [ ] Verify `con rained` on page 82 of the PDF → add `'con rained': 'constrained'` to `text_replacements`
- [ ] Verify `pela gianism` on page 95 → add `'pela gianism': 'Pelagianism'` if confirmed
- [ ] Verify `athenaguras` on page 93 → add `'athenaguras': 'Athenagoras'` if confirmed
- [ ] Verify `self conceitedness` on page 201 → check if this should be `self-conceitedness`
- [ ] Re-extract and rebuild: `.venv/bin/python3 volumes/v7/convert.py` (full pipeline for OCR fixes)
- [ ] Re-audit and check coverage

### Step 3: Investigate Dense Window Losses on Key Pages

- [ ] Page 42: Check Greek word `ρημα` extraction
- [ ] Page 64: Check for word-join issues
- [ ] Page 103: Check Latin phrase tokenization
- [ ] Page 26: Verify Latin `rursum crucifigentes` in EPUB
- [ ] For each fix, rebuild and re-audit

### Step 4: Check `editor` Word Gap

- [ ] Find where `editor` appears 3 times in PDF
- [ ] Verify only 1 appears in EPUB
- [ ] Add missing instances to EPUB content (likely in front matter HTML)

### Step 5: Optional — Whitelist Remaining Dense Window Pages

If specific pages can't be fixed (polyglot complexity, font encoding), add them to the dense_source_window_loss whitelist in `volume_7_whitelist.json`. This suppresses warnings but does **not** improve the coverage ratio or Need score.

---

## Verification Commands

After each change:

```bash
# Rebuild EPUB (render-only is fast, ~3 seconds; full pipeline for OCR fixes)
.venv/bin/python3 volumes/v7/convert.py --render-only

# Re-audit text integrity (coverage calculation)
.venv/bin/python3 scripts/audit_text_integrity.py 7

# Re-audit anomalies
.venv/bin/python3 scripts/audit_anomalies.py 7

# Re-audit EPUB structure
.venv/bin/python3 scripts/audit_epub.py 7

# Check bug regressions
.venv/bin/python3 -m pytest tests/test_bug_regressions.py

# Generate updated state report
.venv/bin/python3 scripts/report_volume_state.py 7
```

After all fixes, the target is:

- Coverage ≥ 99.90% → Need ≤ 4.0
- Coverage ≥ 99.95% → Need ≤ 2.0
- All other penalties remain at 0

---

## What NOT To Do

1. **Do NOT remove Latin whitelist entries** — Removing `low_latin_tagging` from `ignored_warnings` would ADD penalties (up to ~4.8 points) rather than reducing them. The Latin tagging ratio is 63.73%, which is low, but fixing it requires extensive manual Latin tagging in the EPUB content — not worth the effort compared to coverage improvements.

2. **Do NOT add `low_latin_word_coverage` or `low_latin_translation_coverage` to `ignored_warnings`** — These are already at 0 penalty (coverage is above 99% threshold, translation is at 100%). Whitelisting them would have no effect.

3. **Do NOT try to reduce excess EPUB words** — The excess words come from legitimate endnote content and do not affect the coverage ratio.

4. **Do NOT modernize 17th-century orthography** — Per AGENTS.md, hyphenated words like `stout-hearted`, `over-earnest`, `un-humbled` are authentic and must not be changed.

---

## Whitelist Updates Required

The current whitelist `dense_source_window_loss` contains stale entries (pages 3, 4, 5, 6, 24, 31, 37, 39, 45) that no longer have losses. Meanwhile, 31 pages that ARE currently missing have no whitelist entries at all. The whitelist needs to be updated to reflect the current audit state.

### Stale Entries to Remove

These pages had dense source window losses in a previous audit run but no longer do. They should be removed from `dense_source_window_loss`:

- Pages 4, 5, 6, 24, 31, 37, 39, 45

Keep page 3 in the list since it's also in `front_matter_toc_loss` (custom TOC replacement).

### New Entries to Add

These pages have legitimate, unfixable dense source window losses and should be added to `dense_source_window_loss`:

| Page | Reason | Category |
|---|---|---|
| 25 | Heavy polyglot (Greek + Latin); already whitelisted as weak page | **Polyglot** |
| 26 | Heavy polyglot (Greek + Latin `rursum crucifigentes sibimetipsis`) | **Polyglot** |
| 42 | Greek `ρημα` + Latin `verbum dictum` inline; Unicode normalization mismatch | **Polyglot** |
| 93 | Patristic name list with `Athenaguras` (OCR) | **OCR name list** |
| 100 | Greek/Latin patristic reference dense page | **Polyglot** |
| 103 | Latin quotation `latius excisae serpit contagio` inline | **Polyglot** |
| 183 | Scripture reference formatting (dashes, book abbreviations) | **Scripture refs** |
| 397 | Scripture reference formatting (chapter:verse dense cluster) | **Scripture refs** |
| 523 | Scripture reference formatting (Isaiah 11-17, Micah 6-8 dense) | **Scripture refs** |

### Pages to Fix (NOT Whitelist)

These pages have losses that can potentially be fixed via `text_replacements` in `convert.py`. Do NOT whitelist them — fix them instead:

| Page | Issue | Fix |
|---|---|---|
| 82 | OCR: `con rained` → `constrained` | Already in `text_replacements` — verify it's working |
| 95 | Possible OCR: `pela gianism` → `Pelagianism` | Already correct in JSON as `Pelagianism` — investigate why window still misses |
| 455 | Possible OCR: `1st` rendered as `lst` | Already in `text_replacements` — verify |
| 532 | Possible OCR: `re maineth` → `remaineth` | Already correct in JSON — investigate window mismatch |
| 201 | Hyphenation: `self conceitedness` vs `self-conceitedness` | Check if PDF has line break |
| 261 | Hyphenation: `self denial` vs `self-denial` | Check if PDF has line break |
| 278 | Hyphenation: `worldly mindedness` vs `worldly-mindedness` | Check PDF |
| 314 | Hyphenation: `self abasement` vs `self-abasement` | Check PDF |
| 377 | Hyphenation: `self reflection` vs `self-reflection` | Check PDF |
| 388 | Hyphenation: `self exaltation` vs `self-exaltation` | Check PDF |
| 559 | Hyphenation: `self abasement` vs `self-abasement` | Check PDF |

### Pages to Investigate (May Whitelist After Investigation)

These pages have losses with no obvious OCR or hyphenation cause. Investigate first, then whitelist if the loss is inherent to polyglot text, scripture formatting, or font-encoding complexity:

| Page | Sample Text | Investigate |
|---|---|---|
| 64 | `our apostle speaks romans considering nothing in god but mercy` | Check for word-join or line-break issues |
| 76 | `crying out the temple of the lord the temple of the lord the temple` | Repeated scripture phrase — check if em-dash or quote formatting causes mismatch |
| 221 | `an habitual course in any sin is utterly inconsistent` | Check for paragraph-join issues |
| 245 | `whole ministry the temple of the lord the temple of the lord` | Same repeated scripture as page 76 |
| 272 | `being what christ hath commanded such are their first day's meeting` | Check for apostrophe or formatting |
| 283 | `be admitted and take place in them see hebrews satan in the meantime` | Check for scripture ref formatting |
| 290 | `as it is consistent with their worldly interests and advantages` | Check for word-join issues |
| 327 | `their usual converse and misspense of time in their over liberal entertainment` | Possible OCR: `misspense` (check if it should be `mis-spense` or `misspend`) |
| 451 | `witnesses saith the lord that am god chap fear ye not neither be afraid` | Dense scripture formatting |
| 456 | `the divine being those of his omnipresence and omniscience` | Check formatting |
| 519 | `ezekiel because of his eloquence and the elegancy of his parables` | Check for word-join issues |

### Updates to `volume_7_whitelist.json`

The agent should update the `dense_source_window_loss` array to:

```json
"dense_source_window_loss": [
    3,
    25, 26, 42, 64, 76, 82, 93, 95, 100, 103,
    183, 201, 221, 245, 261, 272, 278, 283, 290,
    314, 327, 377, 388, 397, 451, 455, 456, 519, 523, 532, 559
]
```

Note: Page 3 is retained (also in `front_matter_toc_loss`). Pages 4, 5, 6, 24, 31, 37, 39, 45 are removed (no longer have losses).

### Updates to `volume_7_whitelist.md`

The corresponding Markdown section should document why each page is whitelisted. Add categories:

**Polyglot pages** (inherent font-encoding and Unicode normalization mismatches):
- Page 25: Heavy Greek + Latin (`της δωρεας της επουρανιου`); insufficient word-level overlap between PDF font-encoded text and EPUB Unicode text.
- Page 26: Heavy Greek + Latin (`τον υιον του θεου`, `rursum crucifigentes sibimetipsis`); same font-encoding normalization issues.
- Page 42: Greek word `ρημα` with Latin `verbum dictum` inline; Unicode normalization mismatch.
- Page 93: Patristic name list containing `Athenaguras` (OCR for Athenagoras) alongside other proper names.
- Page 100: Greek/Latin patristic references (`whether greek or latin before st austin's time`); dense proper name cluster.
- Page 103: Latin quotation inline (`latius excisae serpit contagio gentis`); tokenization of mixed Latin-English text.

**Scripture reference pages** (formatting-heavy with chapter:verse clusters):
- Page 183: Dense scripture references (`39-41`, `acts 25-27`, `romans`).
- Page 397: Scripture references (`16-18`, `for which cause we faint not`).
- Page 523: Scripture references (`Isaiah 11-17`, `Micah 6-8`).

**OCR artifacts** (should be fixed, not whitelisted — but listed here for tracking):
- Page 82: `con rained` → `constrained` (already in `text_replacements`).
- Page 95: `pela gianism` → `Pelagianism` (may be line-break in PDF, already correct in JSON).
- Page 455: `lst` OCR for `1st` (already in `text_replacements`).
- Page 532: `re maineth` → `remaineth` (may be line-break in PDF, already correct in JSON).

**Hyphenation mismatches** (PDF has line-break hyphenation, EPUB has joined compound):
- Page 201: `self conceitedness` (PDF) vs `self-conceitedness` (EPUB).
- Page 261: `self denial` (PDF) vs `self-denial` (EPUB).
- Page 278: `worldly mindedness` (PDF) vs `worldly-mindedness` (EPUB).
- Page 314: `self abasement` (PDF) vs `self-abasement` (EPUB).
- Page 377: `self reflection` (PDF) vs `self-reflection` (EPUB).
- Page 388: `self exaltation` (PDF) vs `self-exaltation` (EPUB).
- Page 559: `self abasement` (PDF) vs `self-abasement` (EPUB).

### Additional `text_replacements` to Add

```python
'text_replacements': {
    # ... existing entries ...
    
    # OCR fixes for dense window mismatches
    'athenaguras': 'Athenagoras',         # Page 93: Proper name OCR error
    
    # Hyphenated compound word line-break artifacts
    # These appear in the PDF as split across lines (e.g., "self-\nconceitedness")
    # and may cause dense window mismatches when the PDF has "self conceitedness"
    # but the EPUB correctly joins them to "self-conceitedness"
},
```

**IMPORTANT for hyphenation fixes:** Before adding `self conceitedness` → `self-conceitedness` type replacements, verify in the PDF whether the original 17th-century text uses the hyphenated form (which it does — Owen uses `self-conceitedness`, `self-denial`, etc. as hyphenated compounds). If the PDF word-level extraction produces `self conceitedness` because the hyphen fell on a line break, the EPUB is actually CORRECT to have `self-conceitedness`. In this case, the dense window mismatch is expected because the PDF tokenization splits `self-conceitedness` into `self` + `conceitedness` while the EPUB has it as one hyphenated token. These mismatches should be WHITELISTED rather than "fixed" by removing the hyphen.

### Whitelist `ignored_warnings` — No Changes Needed

The current `ignored_warnings` list is:

```json
["repeated_windows", "enumerator_sequence_candidates", "dense_source_window_loss", "front_matter_toc_loss", "low_latin_tagging"]
```

**Do NOT add** `low_latin_translation_coverage` or `low_latin_word_coverage` — they are already at 0 penalty (translation at 100%, coverage above 99% threshold). Whitelisting them would have no effect on the Need score.

**Do NOT remove** `low_latin_tagging` — it would add a penalty of `(1 - 0.6373) × 10 = 3.63` points to the Need score.

**Consider adding** `low_latin_translation_coverage` only if the Latin translation ratio drops below 100% in a future audit and you want to suppress the warning without affecting the score (since the penalty formula is `min((1 - ratio) × 10, 5.0)`, even at 71% it would add ~2.9 points — only suppress if the current ratio is actually near 100%).