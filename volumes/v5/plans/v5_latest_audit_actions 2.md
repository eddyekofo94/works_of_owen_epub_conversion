# Volume 5 — Latest Audit Analysis & Remaining Action Items

> **Generated:** 2026-06-26
> **Reports analyzed:** volume_5_audit.md, volume_5_text_integrity.md, volume_5_anomalies.md (latest run)
> **Current Need Score estimate:** ~2.0 (PRISTINE, rank 10/16)
> **Target:** Reduce to ~0.3 (matching Volume 2)

---

## Progress Since Earlier Analysis

Several issues from the earlier review have been resolved:

| Issue | Before | Now | How it was fixed |
|-------|--------|-----|------------------|
| Anomalies (4 count) | 3 punctuation spacing + 1 unmatched quote | **0** | Moved `Answer .`/`Ans .`/`A. full comprehension` to `regex_replacements` in convert.py:158-162 |
| Overlong headings | 2 (ch012 + ch022) | **1** (ch012 only) | ch022 fixed via regex replacement at convert.py:162 |
| Duplicate text_replacements | `Answer .`/`Ans .` duplicated in dict | **Cleaned** | Duplicates removed; moved to `regex_replacements` section |

---

## Current Need Score Breakdown (~2.0 total)

| Component | Penalty | Status |
|-----------|---------|--------|
| **Latin tagging** (83.21%) | **1.7** | NOT whitelisted — biggest remaining penalty |
| Coverage (99.99%) | **0.3** | Essentially at ceiling |
| Everything else | **0** | Clean (anomalies=0, splits=0, quotes=0, citations=0) |

---

## Action Items for Agent

### Action 1 — Whitelist `low_latin_tagging` (Impact: -1.7 Need)

**This is the single highest-impact action.** It alone drops the Need score from ~2.0 to ~0.3.

**Problem:** The text integrity JSON confirms `low_latin_tagging` is an active warning not covered by the whitelist:
```
"unused_whitelist_text_integrity": {
    "ignored_warnings": ["low_latin_tagging"]
}
```
(volume_5_text_integrity.json, line 796)

**The untagged "Latin" words are not actually Latin text:**
- **English words of Latin origin:** `obviate` (8 occurrences), `adequate` (7), `genius` (5) — these are standard English prose words, not Latin
- **Personal names used in English context:** `socinus` (29), `schlichtingius` (5), `grotius` (5), `pelagius` (4), `thomas` (6), `onesimus` (10) — proper names of historical figures, not Latin text
- `reus` (13, 5 tagged) — mixed usage, some genuinely Latin, some English legal terminology

Tagging these as "Latin" with `<span lang="la">` would be semantically incorrect — they are English usage of Latin-derived terms and personal names, not Latin language text.

**Fix:** Add `"low_latin_tagging"` to the `ignored_warnings` array in `volumes/v5/bugs_fixes/volume_5_whitelist.json`.

**Update:** Also update `volumes/v5/bugs_fixes/volume_5_whitelist.md` to document this whitelist entry with the justification above.

**After fix:** Re-run `.venv/bin/python3 scripts/report_volume_state.py 5` to confirm Need drops to ~0.3.

---

### Action 2 — Remove no-op text replacement (Impact: 0, code hygiene)

**Problem:** `volumes/v5/convert.py:98` contains:
```python
'justification; so the apostle James': 'justification; so the apostle James',
```
The key and value are identical — this replacement does nothing.

**Fix:** Remove this line from `text_replacements` in `convert.py`.

---

### Action 3 — Clean up stale whitelist anomaly entries (Impact: 0, housekeeping)

**Problem:** The anomalies report now shows **0 findings across all categories**, but the whitelist JSON (`volume_5_whitelist.json`) still lists entries under:
- `"OCR & Bracket Residues": ["qui et"]`
- `"Hyphenation Anomalies": ["wire-draw", "dikaio-oo", "non-imputation", "non-solvent", "blood-guiltiness", "co-interest"]`
- `"Structural Nesting Sequence Jumps": ["2.", "5. ... 7.", "2. ... 4."]`
- `"Unmatched Quotation Marks": [13 entries]`
- `"Invalid Bible References": ["John 22"]`

These are harmless (they just don't match anything in the current audit), but they are stale and could confuse a future agent into thinking these issues still exist.

**Fix:** Either:
- **Option A (recommended):** Keep the entries but add a note in `volume_5_whitelist.md` that these were resolved in the latest render and are retained for historical reference.
- **Option B:** Remove the entries from the JSON since the anomalies are now 0. Only do this if you're confident these won't regress.

**Note:** The `qui et` entry was already resolved (it no longer appears in anomalies). The hyphenation anomalies (`wire-draw`, `dikaio-oo`, etc.) are legitimate 17th-century spellings that should NOT be modernized per AGENTS.md. The `John 22` invalid Bible reference was fixed by the text replacement at convert.py:133 (`'John 22:30, 31': 'John 20:30, 31'`).

---

### Action 4 — Latin translation enrichment (Impact: 0, whitelisted, quality improvement)

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

**Fix:** Research the Latin context and add translations to `BODY_TRANSLATIONS` in `scripts/translation_db.py`. These are likely from Augustine, Bellarmine, or other patristic/scholastic sources Owen cites.

This is already whitelisted (`low_latin_translation_coverage` in `ignored_warnings`) so it has no Need score impact, but adding translations improves the reader experience.

---

### Action 5 — ch012 overlong heading (Impact: 0, already whitelisted, no action needed)

The remaining overlong heading at ch012:
```
IMPUTATION OF THE SINS OF THE CHURCH UNTO CHRIST — GROUNDS OF IT — THE NATURE OF HIS SURETISHIP — CAUSES OF THE NEW COVENANT — CHRIST AND THE CHURCH ONE MYSTICAL PERSON — CONSEQUENTS THEREOF
```

This is Owen's actual analytical heading from the Goold edition. It is long but authentic. Already whitelisted as `overlong_heading_candidates`. **No action needed.**

---

## Execution Order

1. **Action 1** — Whitelist `low_latin_tagging` (highest impact, -1.7 Need)
2. **Action 2** — Remove no-op text replacement (trivial cleanup)
3. **Action 3** — Clean up stale whitelist entries (housekeeping)
4. **Action 4** — Add Latin translations (optional, quality only)

Actions 1+2 should take under 5 minutes and drop Need from ~2.0 to ~0.3.

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
8. Verify Need drops from ~2.0 to ~0.3

All audit reports are saved under `volumes/v5/bugs_fixes/` and should be archived under `volumes/v5/reports/` with timestamps per the AGENTS.md report archiving mandate.

---

## What NOT To Do

1. **Do NOT modernize 17th-century orthography** — Hyphenation anomalies like `wire-draw`, `dikaio-oo`, `non-imputation`, `non-solvent`, `blood-guiltiness`, `co-interest` are historical spellings acceptable in Owen's day.
2. **Do NOT try to "fix" Owen's quotation conventions** — All unmatched quotes are legitimate 17th-century prose conventions.
3. **Do NOT add `low_latin_word_coverage` to `ignored_warnings`** — Latin word coverage is already 99.71% (above the 99% threshold). Whitelisting has zero effect.
4. **Do NOT add English Bible verse text as BODY_TRANSLATIONS keys** — This generates pointless notes on every scripture quotation.
5. **Do NOT add `<span lang="la">` manually** to raw_text in JSON intermediates — the renderer handles all language tagging automatically.
6. **Do NOT modify `render.py` or `shared.py` for volume-specific content** — All volume-specific fixes go in `volumes/v5/convert.py` OVERRIDES.
7. **Do NOT try to tag English words of Latin origin as Latin** — Words like `obviate`, `adequate`, `genius` are English prose. Personal names like `Socinus`, `Grotius`, `Pelagius` are names, not Latin text. This is why whitelisting `low_latin_tagging` is the correct approach, not improving tagging.
