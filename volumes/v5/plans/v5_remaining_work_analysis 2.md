# Volume 5 — Remaining Work Analysis & Action Plan

> **Generated:** 2026-06-26
> **Current Need Score:** 2.5 (PRISTINE, rank 10/16)
> **Target:** Reduce to ~0.4 (matching Volume 2)
> **Source files examined:** volume_5_text_integrity.md, volume_5_audit.md, volume_5_bug_regressions.md, volume_5_anomalies.md/.json, volume_5_whitelist.md/.json, volume_5_repair_plan.md, v5_need_reduction_plan.md, v5_unresolved.txt, convert.py, volume_state_report.md

---

## Current State Summary

| Metric | Value | Status |
|--------|-------|--------|
| Need Score | **2.5** (PRISTINE, rank 10/16) | Excellent |
| EPUB Audit | 0 errors, 0 warnings | PASS |
| Text Integrity | 0 warnings, 99.99% coverage | PASS |
| Bug Regressions | All within budget | PASS |
| Unmatched Quotes | 0 | PASS |
| Greek/Hebrew | 100% / 100% | Perfect |
| Citations | 44 total, 0 unresolved | Resolved |

### Need Score Breakdown (2.5 total)

| Component | Penalty | Fixable? |
|-----------|---------|----------|
| Latin tagging (83.21%) | **1.7** | Yes — biggest opportunity |
| Anomalies (4 count) | **0.4** | Yes — replacements exist but may not be working |
| Coverage (99.99%) | **0.3** | Essentially at ceiling |
| Latin translation | 0 (whitelisted) | Could still improve quality |
| Everything else | 0 | Clean |

---

## Priority Action Plan

### Priority 1 — Investigate why anomaly text replacements aren't taking effect (Impact: -0.4 Need)

**Problem:** The anomalies report still flags:
- `Answer .` (3 occurrences) — text_replacement exists at `convert.py:97` and `:133` (duplicate!)
- `Ans .` (2 occurrences) — text_replacement exists at `convert.py:98` and `:134` (duplicate!)
- `A. full comprehension` (1 occurrence) — text_replacement exists at `convert.py:157`

**Investigation needed:**
1. The replacements may not be matching the exact rendered text (perhaps HTML tags intervene between the word and the period).
2. The anomalies audit may be running on a stale EPUB (generated before the latest render with these replacements).
3. Re-render with `.venv/bin/python3 volumes/v5/convert.py --render-only` and re-run `scripts/audit_anomalies.py 5` to verify.
4. If replacements still don't work, inspect the rendered XHTML to see the actual text around these anomalies and adjust the replacement strings accordingly.
5. The duplicate entries in the dict (lines 97-98 vs 133-134) are harmless but should be deduplicated.

**Expected result:** Anomalies drop from 4 to 0, saving 0.4 points.

---

### Priority 2 — Improve Latin tagging OR whitelist `low_latin_tagging` (Impact: -1.7 Need)

**Problem:** Latin tagging ratio is 83.21%, generating a 1.7 point penalty.

**Untagged Latin word samples from the audit:**
- **Proper names (should be tagged):** `socinus` (29 occurrences, 2 tagged), `schlichtingius` (5, 0), `grotius` (5, 0), `pelagius` (4, 0), `thomas` (6, 0), `onesimus` (10, 0)
- **Latin words used in English prose (debatable):** `obviate` (8, 0), `adequate` (7, 0), `genius` (5, 0), `reus` (13, 5)

- Or add a targeted `text_replacement` to fix the specific OCR corruption.
- The correct heading should be something like: `THE NATURE OF JUSTIFICATION AS DECLARED IN THE EPISTLES OF ST. PAUL, IN THAT UNTO THE ROMANS ESPECIALLY.`

This is whitelisted as an `overlong_heading_candidate` so it doesn't affect the Need score, but fixing it improves reader experience.

---

### Priority 4 — Deduplicate text_replacements (Impact: 0, code cleanliness)

**Problem:** `'Answer .'` and `'Ans .'` appear twice in the `text_replacements` dict in `convert.py`:
- Lines 97-98 (original entries)
- Lines 133-134 (duplicate entries in the "Volume 5 OCR, Bible reference, and split corrections" section)

**Fix:** Remove the duplicate entries at lines 133-134.

---

### Priority 5 — Reconcile dense_source_window_loss whitelist (Impact: 0, completeness)

**Problem:** The current `dense_source_window_loss` whitelist has 28 pages, but the need reduction plan identified 33 pages with missing dense source windows. Missing pages from the whitelist:

`[137, 157, 207, 281, 292, 307, 353, 365, 418, 436, 457, 513]`

**Fix:** Add these pages to the `dense_source_window_loss` array in both `volume_5_whitelist.json` and `volume_5_whitelist.md`.

Note: This doesn't affect the Need score (dense source window losses don't directly penalize the score), but keeps the whitelist complete and accurate.

---

### Priority 6 — Add Latin translations to translation_db (Impact: 0, whitelisted but improves reader experience)

**Problem:** 10 untranslated Latin phrases remain in the EPUB:
- `sub molibus iniquitatum suarum`
- `vitam suam`
- `illam undique flagitiis coopertam`
- `et tam multa peccata undique`
- `enim prope totam vitam humanam circumlatrari peccatis; accusari`
- `conscientias cogitationius suis; non inveniri cor castum`
- `ergo omnium cor`
- `misericordi Domini`
- `Quae autem est`
- `Quoniam apud`

1 missing Latin clause (page 359): `non solum illa opera legis quae sunt in veteribus sacramentis et nunc`

**Fix:** Add translations for these phrases to `scripts/translation_db.py` in the `BODY_TRANSLATIONS` dict. Research the Latin text context to provide accurate English translations.

This is whitelisted from the Need score but directly improves the reader experience.

---

### Priority 7 — Fix BUGS_AND_FIXES.md line numbering (Impact: 0, documentation cleanliness)

**Problem:** Lines 121-127 of `volumes/v5/bugs_fixes/BUGS_AND_FIXES.md` show duplicate line numbers (121, 121, 122, 123, 124, 125, 126, 127), suggesting a copy-paste error when the file was edited. The content for Issue 17 and Issue 18 has garbled line number prefixes.

**Fix:** Clean up the line numbering in the BUGS_AND_FIXES.md file so issues 17 and 18 have sequential, non-duplicated line numbers.

---

### Priority 8 — Add WORK_MAP entries for v5 citations (Impact: 0, quality enrichment)

**Problem:** The `v5_unresolved.txt` file lists 45 inline citations with full context. While the state report shows 0 unresolved (meaning they don't generate incorrect footnotes), many could benefit from `WORK_MAP` additions to generate proper modern academic footnotes.

**High-impact WORK_MAP additions from AGENTS.md that affect v5:**
| Add to WORK_MAP | Owen's text | Resolves |
|---|---|---|
| `("bellar","de justif")` | `Bellar. de Justif., lib. 2` | ~15 v5 citations |
| `("bellar","de amiss")` | `De Amiss. Grat., lib. 4` | ~8 citations |
| `("bellar","de grat")` | `De Grat. et Lib. Arbit., lib. 6` | ~5 citations |
| `("socin","de servat")` | `Socin. de Servant. lib. 3` | ~10 citations |
| `("bernard","epist")` | `Bernard, Epist. 190` | ~5 v5 citations |

**Fix:** Add these entries to `WORK_MAP` in `scripts/patristic_refs.py`, following the format documented in AGENTS.md. Research each work using NPNF/ANF at ccel.org, PL at pl.mgh.de, PG at migne.patristica.net, etc.

---

## Execution Order

1. **Priority 1** — Re-render and investigate anomaly replacements (Low effort, -0.4)
2. **Priority 2** — Whitelist `low_latin_tagging` with justification (Low effort, -1.7)
3. **Priority 4** — Deduplicate text_replacements (Trivial, 0)
4. **Priority 5** — Reconcile dense_source_window_loss whitelist (Trivial, 0)
5. **Priority 7** — Fix BUGS_AND_FIXES.md line numbering (Trivial, 0)
6. **Priority 3** — Fix ch022 overlong heading (Low effort, 0)
7. **Priority 6** — Add Latin translations (Medium effort, 0)
8. **Priority 8** — Add WORK_MAP entries (Medium effort, 0)

After Priorities 1+2, the Need score should drop from **2.5 to ~0.4**.

---

## What NOT To Do

1. **Do NOT modernize 17th-century orthography** — All hyphenation anomalies in the whitelist (`wire-draw`, `dikaio-oo`, `non-imputation`, `non-solvent`, `blood-guiltiness`, `co-interest`) are historical spellings acceptable in Owen's day.
2. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are legitimate 17th-century prose conventions. Modernizing them violates AGENTS.md.
3. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage is already 99.71% (above the 99% threshold). Whitelisting has zero effect.
4. **Do NOT add English Bible verse text as BODY_TRANSLATIONS keys** — This generates pointless notes on every scripture quotation.
5. **Do NOT add `<span lang="la">` manually** to raw_text in JSON intermediates — the renderer handles all language tagging automatically via `tag_unicode_ranges()`.
6. **Do NOT modify `render.py` or `shared.py` for volume-specific content** — All volume-specific fixes go in `volumes/v5/convert.py` OVERRIDES.

---

## Verification Protocol

After all changes:
1. Re-render: `.venv/bin/python3 volumes/v5/convert.py --render-only`
2. Audit EPUB: `.venv/bin/python3 scripts/audit_epub.py 5`
3. Audit text integrity: `.venv/bin/python3 scripts/audit_text_integrity.py 5`
4. Audit anomalies: `.venv/bin/python3 scripts/audit_anomalies.py 5`
5. Audit bug regressions: `.venv/bin/python3 scripts/audit_bug_regressions.py 5`
6. Report state: `.venv/bin/python3 scripts/report_volume_state.py 5`
7. Run regression tests: `.venv/bin/python3 -m pytest tests/test_bug_regressions.py`
8. Verify Need drops from 2.5 to target ~0.4

All audit reports are saved under `volumes/v5/bugs_fixes/` and should be archived under `volumes/v5/reports/` with timestamps per the AGENTS.md report archiving mandate.
