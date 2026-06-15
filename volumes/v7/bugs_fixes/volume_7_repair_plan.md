# Volume 7 Repair Plan & Improvement Roadmap

**Volume:** 7 (Apostasy, Spiritually-Mindedness, Dominion of Sin and Grace)  
**Current State:** PRISTINE (Need: 9.2, Coverage: 99.77%)  
**Last Audit:** 2026-06-15  
**Bug Regressions:** PASS (all 63 checks OK)  
**EPUB Audit:** PASS (0 errors, 0 warnings)  
**Text Integrity:** PASS (0 warnings)

---

## Priority 1 — Latin Tagging & Translation Footnotes (Expected Need Reduction: up to 7.0 points)

**Current metrics:**
- Latin word tagging ratio: 51.19% (target: ≥99%)
- Latin translation coverage: 71.43% (target: ≥99%)
- This gap contributes a combined ~7.0 penalty to the Need score (5.0 missing coverage + 2.0 missing tagging)

**What to fix:** Add `<span lang="la">` tags and translation footnotes for all untagged/untranslated Latin phrases. The text integrity audit identifies 12 untranslated Latin phrases:

| Latin Phrase | Expected Context | Action |
|---|---|---|
| `sui juris` | Legal Latin ("of one's own right") | Add `<span lang="la">` tag + translation footnote |
| `amor patriae` | Love of country/fatriotism | Add `<span lang="la">` tag + translation footnote |
| `immensam cupido` | "Vast desire" (Ovid/Claudian quote fragment) | Add `<span lang="la">` tag + translation footnote |
| `Ammianus Marcellinus` | Proper name (Roman historian) | Add `<span lang="la">` tag (proper name, no translation needed) |
| `animae vehicula` | "Vehicles of the soul" | Add `<span lang="la">` tag + translation footnote |
| `Nemo moritur` | Fragment of legal maxim ("No one dies...") | Add `<span lang="la">` tag + translation footnote |
| `Apostata est osor sui ordinis` | "An apostate is a hater of his own order" | Add `<span lang="la">` tag + translation footnote |
| `Deos et coeli Numina vobis` | "The gods and the powers of heaven to you" | Add `<span lang="la">` tag + translation footnote |
| `Prudentia, sapientia, intelligentia` | "Prudence, wisdom, understanding" | Add `<span lang="la">` tag + translation footnote |
| `cogitatio, discretio, id quod Spiritus` | "Thought, discernment, that which the Spirit..." | Add `<span lang="la">` tag + translation footnote |
| `naturae clamantis ad Dominum naturae` | "Nature crying out to the Lord of nature" | Add `<span lang="la">` tag + translation footnote |
| `ignis fatuus` | "Will-o'-the-wisp" | Add `<span lang="la">` tag + translation footnote |

**How to fix:** In `volumes/v7/convert.py`, the `text_replacements` dict in `OVERRIDES` supports both:
1. **Tagging:** Add entries like `'sui juris': '<span lang="la">sui juris</span>'` to wrap untagged Latin phrases.
2. **Translation footnotes:** For phrases that need translation, the renderer (`render.py`) automatically generates endnote footnotes for `<span lang="la">` phrases if a translation mapping exists. Check if a `latin_translations` override key is supported, or if these need to go into `shared.py`'s `BODY_TRANSLATIONS` or the citation system.

**IMPORTANT:** Search the EPUB XHTML files first to find the exact surrounding context of each Latin phrase before writing replacements. Some phrases may already be partially tagged or have inline English translations following them that make a translation footnote redundant. Use:
```bash
rg "sui juris" volumes/v7/intermediate/volume_7.json
rg "amor patriae" volumes/v7/intermediate/volume_7.json
# etc.
```

**Verification:** After fix, rebuild with `--render-only` and re-run:
```bash
.venv/bin/python3 scripts/audit_text_integrity.py 7
```
Latin tagging ratio should approach ≥99%, and translation coverage should approach ≥99%.

---

## Priority 2 — Fix Double Period (`..`) via Regex (Minor Cleanup)

**Problem:** The `text_replacements` entry `'..': '.'` does not catch all `..` occurrences. The whitelist audit shows 3 remaining instances inside bold markup: `**..**. advantage`, `**..**. basement`, `**..**. ng so long`. These appear as `2dly..` and `1st..` patterns where the double period is between bold markers.

**How to fix:** In `volumes/v7/convert.py`, add a regex replacement to `OVERRIDES['regex_replacements']`:
```python
r'\.{2,}': '.',  # Collapse double/triple periods to single period
```

This regex catches `..` regardless of surrounding bold markers (`**..**`) or ordinal suffixes (`1st..`, `2dly..`).

**WARNING:** Apply this regex carefully. Owen sometimes uses `..` intentionally as abbreviation ellipsis (e.g., in volume numbers or editorial sigla). Run the replacement and then inspect the EPUB output for any false positives before committing. If this proves too greedy, use a more specific pattern like `r'(?<=\w)\.{2}(?=[\s\W])': '.'` to only match double periods after word characters.

**Verification:** After fix, rebuild and check that the 3 `..` instances in the whitelist audit no longer appear:
```bash
.venv/bin/python3 volumes/v7/convert.py --render-only
.venv/bin/python3 scripts/audit_anomalies.py 7
```
The Punctuation Spacing Blemishes entry for `'..'` should have 0 matches, and it can be removed from the whitelist.

---

## Priority 3 — Collapse Spaced List-Marker Punctuation via Regex (Cleanup + 6 Whitelist Entry Removals)

**Problem:** The current `regex_replacements` in `OVERRIDES` includes `r'\b\s+([.,;:?!])'` which catches word-adjacent spaces before punctuation (e.g., `and ,`, `Lord ;`), but does NOT catch the pattern `digit + space + period` used in Owen's numbered lists (e.g., `1 .`, `2 .`, `3 .`).

The whitelist has 6 punctuation spacing entries (covering 27+ individual anomalies) that could be eliminated entirely:
- `1 .` (3 matches), `1st .` (3 matches), `2 .` (6 matches), `2dly .` (2 matches), `3 .` (5 matches), `4 .` (5 matches), `5 .` (3 matches)
- Plus: `6 .` (1 match), `7 .` (1 match)

**How to fix:** In `volumes/v7/convert.py`, add these regex patterns to `OVERRIDES['regex_replacements']`:
```python
r'(\b\d+)(\s+)(\.)': r'\1\3',      # "1 ." → "1.", "2 ." → "2."
r'(\d+)(st|dly|th|nd|rd)(\s+)(\.)': r'\1\2\4',  # "1st ." → "1st.", "2dly ." → "2dly."
```

**IMPORTANT:** Test carefully. The existing `r'\b\s+([.,;:?!])'` rule should already handle cases like `2dly ,` → `2dly,` and `1st ,` → `1st,`. The new rules specifically target the period cases with digits.

**After implementing:**
1. Remove these whitelist entries from `volume_7_whitelist.json` under `anomalies.Punctuation Spacing Blemishes`: `"1 ."`, `"1st ."`, `"2 ."`, `"2dly ."`, `"3 ."`, `"4 ."`, `"5 ."`, `"6 ."`, `"7 ."`.
2. Remove the corresponding entries from `volume_7_whitelist.md`.
3. Re-run the anomaly audit to verify these blemishes are gone.

**Verification:**
```bash
.venv/bin/python3 volumes/v7/convert.py --render-only
.venv/bin/python3 scripts/audit_anomalies.py 7
```

---

## Priority 4 — Promote 3 Roman Heading Candidates (Structural Improvement)

**Problem:** The text integrity audit flags 3 paragraphs where Roman numerals start body text but are likely structural headings that should be promoted:

| File | Text | Issue |
|---|---|---|
| `EPUB/ch046.xhtml` | `I. 1. That spiritual life whereof we are made partakers in this world is threefold, or there are three gospel privileges or graces so expressed: —` | Major outline heading (Part II ch.20 opening) rendered as paragraph |
| `EPUB/ch049.xhtml` | `I. As to the nature of this dominion, —` | Section heading rendered as paragraph |
| `EPUB/ch049.xhtml` | `II. As to the evidence of this dominion, —` | Section heading rendered as paragraph |

**How to fix:** In `volumes/v7/convert.py`, add a `heading_overrides` entry to `OVERRIDES` that promotes these to proper headings. The `render.py` pipeline supports heading overrides that match against paragraph text. Check the render.py code for the exact format (likely a dict mapping paragraph substrings to heading-level specifications). For example:
```python
'heading_overrides': {
    'I. 1. That spiritual life whereof we are made partakers': ('h2', None),
    'I. As to the nature of this dominion': ('h3', None),
    'II. As to the evidence of this dominion': ('h3', None),
},
```

**Before implementing**, verify the exact mechanism by checking how `heading_overrides` or similar keys are processed in `render.py`. Search for `heading_override` or `heading_promotion` in the renderer.

**Verification:** After fix, these paragraphs should appear as `<h2>` or `<h3>` elements in the EPUB, and the "Roman heading candidates" count in the text integrity audit should drop from 3 to 0.

---

## Priority 5 — Verify 2 Enumerator Sequence Candidates (Validation Only)

**Problem:** The text integrity audit flags 2 enumerator sequence candidates that may indicate structural issues:

| File | Marker | Context |
|---|---|---|
| `EPUB/ch030.xhtml` | `(2.)` | `(2.) WE have treated in general before of the proper objects of our spiritual thoughts...` |
| `EPUB/ch030.xhtml` | `[3.]` | `[3.] Again; meditate and think of the glory of heaven so as to compare it with the opposite state...` |

These are already whitelisted as `inline_structural_markers` because they are authentic inline enumerators inside prose paragraphs (not standalone list items). They are verified as correct structure in Owen's text.

**Action:** No code change needed. These are legitimate Owenian inline enumerators. The whitelist correctly silences them. Confirm with PDF page inspection if desired.

---

## Priority 6 — Dense Source Window Loss: Investigate 10 Non-Front-Matter Pages

**Problem:** The text integrity audit reports 31 missing dense source windows, of which 9 are explicitly whitelisted (front matter/TOC pages). The remaining 22 pages include some non-front-matter pages that may represent genuine text coverage gaps:

Key non-front-matter pages with missing dense windows (sampled from the text integrity report):
| Page | Sample | Risk |
|---|---|---|
| 25 | Heavy polyglot Greek/Hebrew — already whitelisted | Low |
| 42 | `what sense they taste of it ρημα is properly verbum dictum word spoken` | Medium — Greek/Latin phrase may have extraction issues |
| 64 | `our apostle speaks romans considering nothing in god but mercy` | Low — likely formatting variation |
| 76 | `crying out the temple of the lord the temple of the lord` | Low — repeated phrase, likely scripture quote |
| 82 | `expose the doctrine of it and the law of obedience con rained in it` | Medium — possible OCR issue (`con rained` → `constrained`) |
| 100 | `whether greek or latin before st austin's time` | Low |
| 103 | `success or progress in the world but latius excisae serpit contagio` | Medium — Latin phrase may be partially lost |

**Actions:**
1. Check page 82 in the PDF for the OCR artifact `con rained` → should be `constrained`. If confirmed, add `'con rained': 'constrained'` to `OVERRIDES['text_replacements']`.
2. The dense source window gaps for pages 25 and 103 are expected (polyglot content). No action needed.
3. Other pages have minor mismatches from formatting variations. No action needed unless coverage drops below 99.5%.

---

## Priority 7 — Reduce Whitelist Greediness (Optional Cleanup)

The whitelist audit identifies 20 "greedy" entries that match multiple distinct anomalies. While none of these are silencing real problems (all matches are legitimate), the greediness could mask future issues. The primary categories:

1. **Structural Nesting Sequence Jumps** (6 entries, 22 total matches): Entries like `II.` match both `II.` and `VII.`/`VIII.` because they are substring matches. This is inherent to the whitelist matching mechanism and not easily fixable without reworking the matching to be exact-position or exact-word-boundary.

2. **Punctuation Spacing Blemishes** (8 entries, 28 total matches): These are pattern-based (e.g., `2 .` matches any occurrence of `2 .`). This is correct behavior — each instance IS the same blemish type.

3. **Hyphenation** (2 entries: `stout-hearted`/`stout-heartedness` matching 5 each): The word `stout-hearted` appears in the text in multiple chapters. Each occurrence is correctly whitelisted.

**Action:** No immediate action required. The greediness is benign. If Priority 3 is implemented (regex collapsing of `digit + space + period`), 8 of the 20 greedy entries will be eliminated entirely.

---

## Priority 8 — Short Fragments Review (Informational)

The text integrity audit reports 22 short fragments. Most are authentic structural elements (Roman numerals like `I.`, `II.`, `VIII.`, `III.` in the analysis section `ch003.xhtml`, heading fragments like `To The Reader`, and connective fragments like `And, —` and `Ans.`). One may warrant attention:

| File | Text | Notes |
|---|---|---|
| `EPUB/ch013.xhtml` | `Verse 20,` | Possibly a fragment that should be joined to the next paragraph, or a legitimate sub-heading |

**Action:** Verify in PDF. If `Verse 20,` is a standalone sub-heading label (which is common in Owen's commentary), no action needed. If it's an orphaned fragment, it should be joined.

---

## Summary of Changes Required

All changes go into **`volumes/v7/convert.py`** in the `OVERRIDES` dict:

### In `text_replacements`:
Add entries for Latin phrase tagging and any OCR fixes found in Priority 6:
```python
'text_replacements': {
    # ... existing entries ...
    # Latin tagging (Priority 1) — add each phrase with <span lang="la"> wrapper
    'sui juris': '<span lang="la">sui juris</span>',
    'amor patriae': '<span lang="la">amor patriae</span>',
    'immensam cupido': '<span lang="la">immensam cupido</span>',
    'animae vehicula': '<span lang="la">animae vehicula</span>',
    'Nemo moritur': '<span lang="la">Nemo moritur</span>',
    'Apostata est osor sui ordinis': '<span lang="la">Apostata est osor sui ordinis</span>',
    'Deos et coeli Numina vobis': '<span lang="la">Deos et coeli Numina vobis</span>',
    'Prudentia, sapientia, intelligentia': '<span lang="la">Prudentia, sapientia, intelligentia</span>',
    'cogitatio, discretio, id quod Spiritus': '<span lang="la">cogitatio, discretio, id quod Spiritus</span>',
    'naturae clamantis ad Dominum naturae': '<span lang="la">naturae clamantis ad Dominum naturae</span>',
    'ignis fatuus': '<span lang="la">ignis fatuus</span>',
    # OCR fix from Priority 6
    'con rained': 'constrained',
},
```

**IMPORTANT:** Before adding these, search the JSON intermediate to verify each Latin phrase appears exactly as written (with correct casing and spelling). Some may already be inside `<span lang="la">` tags, in which case wrapping them again would create nested tags. Also verify there's no partial overlap (e.g., if `Nemo moritur` is actually `Nemo moritur in declinatione morbi`, wrap the full phrase).

### In `regex_replacements`:
Add entries for Priorities 2 and 3:
```python
'regex_replacements': {
    # ... existing entries ...
    r'\.{2,}': '.',                          # Priority 2: collapse double/triple periods
    r'(\b\d+)(\s+)(\.)': r'\1\3',            # Priority 3: "1 ." → "1."
    r'(\d+(?:st|dly|th|nd|rd))(\s+)(\.)': r'\1\3',  # Priority 3: "1st ." → "1st."
},
```

### In `treatise_title_overrides` (if needed):
No changes needed — all 3 treatises already have hardcoded title pages.

### Whitelist Updates (after fixes):
After implementing and verifying each priority, update the whitelist files:
1. Remove `..` from `Punctuation Spacing Blemishes` in both `.json` and `.md`
2. Remove `1 .`, `1st .`, `2 .`, `2dly .`, `3 .`, `4 .`, `5 .`, `6 .`, `7 .` from `Punctuation Spacing Blemishes`
3. Remove `1st ,`, `2dly ,`, `and ,`, `flatteries :`, `ignorant ,`, `Lord ;`, `First ,` IF they are also fixed by the broader regex (verify first — the existing `r'\b\s+([.,;:?!])'` rule should already handle most of these)
4. Re-run audits and update the whitelist audit report

---

## Verification Commands

After making changes:
```bash
# Rebuild EPUB from cached JSON (fast, ~3 seconds)
.venv/bin/python3 volumes/v7/convert.py --render-only

# Run anomaly audit
.venv/bin/python3 scripts/audit_anomalies.py 7

# Run text integrity audit (includes Latin metrics)
.venv/bin/python3 scripts/audit_text_integrity.py 7

# Run EPUB structural audit
.venv/bin/python3 scripts/audit_epub.py 7

# Run bug regressions
.venv/bin/python3 -m pytest tests/test_bug_regressions.py

# Run the state report to see updated Need score
.venv/bin/python3 scripts/audit_bug_regressions.py 7
```

Target outcome: Need score drops from 9.2 → approximately 2.0 (mainly from Latin tagging fix eliminating ~7.0 points of penalty), plus cleaner text with fewer whitespace blemishes.