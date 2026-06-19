# Volume 15 Heal Report — Independent Review

- **Reviewer:** opencode agent
- **Date:** June 16, 2026 (updated after full audit)
- **Source report:** `.gemini/brain/.../volume_15_heal_report.md`
- **Verification report:** `volumes/v15/reports/volume_15_verification_report_20260616.md`
- **Branch:** `heal-v15`
- **Current Need score:** 2.5 (PRISTINE)

---

## 1. Verified Correct (Prior Review Items — Now All Resolved)

All issues from the first review have been addressed in the verification report:

| Prior Issue | Resolution | Status |
|---|---|---|
| No-op `'Stillingfleet ': 'Stillingfleet '` | Removed from `convert.py` | RESOLVED |
| Blanket `'..'` → `'.'` replacement | Removed from `convert.py` | RESOLVED |
| `churchofficers`/`churchofficer` overlap | Documented with comment at lines 213-214 | RESOLVED |
| Dense page count (was 39, report said 40) | Page 307 added; now 40 pages | RESOLVED |
| `Axplanation` in TOC | Confirmed: EPUB TOC shows "An Explanation Upon the Same — Questions" | RESOLVED |
| `saith Hilary` blockquote merge bug | Capitalised to `Saith Hilary` in `post_extract_hook` (line 183) | RESOLVED |

### Current Quality Metrics

| Metric | Value |
|---|---|
| Word coverage | 99.94% |
| Greek coverage | 100.0% |
| Hebrew coverage | 100.0% |
| Latin word coverage | 99.46% |
| Latin tagging ratio | 55.06% (whitelisted) |
| Latin translation ratio | 51.46% (whitelisted) |
| Faulty paragraph splits | 0 |
| Dense source window misses | 0 (after whitelist) |
| Bug regressions | ALL PASS |

---

## 2. New Issues Found — Unfixed OCR Errors in the Rendered EPUB

The following OCR errors are **still present in the rendered EPUB output** and are not covered by any replacement rule or global OCR correction in `shared.py`.

### 2.1 Compound Merge: `churchstate` (HIGH — 7 chapters affected)

The most significant gap. Same class as the 8 `church-*` compound fixes already in `text_replacements`, but this one was missed.

| Merged form | Correct form | Merged chapters | Hyphenated chapters |
|---|---|---|---|
| `churchstate` | `church-state` | 7 | 22 |

The hyphenated form `church-state` appears in 22 chapters alongside the 7 merged occurrences, confirming this is a line-break hyphen drop. It is also the **#3 excess word** in the text integrity report (`churchstate`: pdf 0, epub 9), directly inflating the coverage gap.

**Fix:** Add `'churchstate': 'church-state'` to `text_replacements` in `convert.py`.

### 2.2 Compound Merge: `churchsocieties` (MEDIUM — 1 chapter)

Same class. Hyphenated form `church-societies` appears in 5 chapters; merged form in 1 chapter.

**Fix:** Add `'churchsocieties': 'church-societies'` to `text_replacements`.

### 2.3 OCR Misread: `theft` → `that` (HIGH — 5 chapters)

The word `theft` appears 5 times in the EPUB where the PDF clearly reads `that`. This is an OCR long-s / f confusion (`thft` misread as `theft`).

Occurrences and their correct readings:

| EPUB text | Correct text | Chapter |
|---|---|---|
| `theft the church be the pillar` | `that the church be the pillar` | ch029 (Chapter 6) |
| `theft numbers of them` | `that numbers of them` | ch029 (Chapter 6) |
| `theft sentence, "Every plant` | `that sentence, "Every plant` | ch036 (Answer to Stillingfleet) |
| `theft the whole church may perish` | `that the whole church may perish` | ch037 (Section 2) |
| `theft it is somewhat oddly` | `that it is somewhat oddly` | ch038 (Section 3) |

**Fix:** Add `text = text.replace('theft the ', 'that the ')` and `text = text.replace('theft it ', 'that it ')` and `text = text.replace('theft sentence', 'that sentence')` and `text = text.replace('theft numbers', 'that numbers')` to `post_extract_hook` in `convert.py`. Alternatively, a single regex: `text = re.sub(r'\btheft\b', 'that', text)` — but this risks replacing legitimate uses of "theft" if any exist. Targeted string replacements are safer.

### 2.4 OCR Misread: `parochisl` → `parochial` (MEDIUM — 1 chapter)

Found in Section 3: `"refraining communion from parochisl assemblies"`.

**Fix:** Add `text = text.replace('parochisl', 'parochial')` to `post_extract_hook`.

### 2.5 OCR Misread: `cougregational` → `congregational` (MEDIUM — 1 chapter)

Found in Section 3: `"a new cougregational church was set up"`.

**Fix:** Add `text = text.replace('cougregational', 'congregational')` to `post_extract_hook`.

### 2.6 OCR Misread: `ms infinite` → `his infinite` (MEDIUM — 1 chapter)

Found in Chapter 10: `"according to ms infinite wisdom"`. The OCR misread `his` as `ms`. Only 1 occurrence of standalone `ms` in the entire JSON.

**Fix:** Add `text = text.replace('ms infinite', 'his infinite')` to `post_extract_hook`.

### 2.7 OCR Misread: `Hobart alarms` → `Hobart affirms` (MEDIUM — 1 chapter)

Found in Section 3: `"as Justice Hobart alarms"`. The OCR misread `affirms` as `alarms`.

**Fix:** Add `text = text.replace('Hobart alarms', 'Hobart affirms')` to `post_extract_hook`.

### 2.8 OCR Misread: `aider Christ` → `after Christ` (MEDIUM — 1 chapter)

Found in Chapter 5: `"two hundred years aider Christ"`. The OCR misread `after` as `aider`.

**Fix:** Add `text = text.replace('aider Christ', 'after Christ')` to `post_extract_hook`.

### 2.9 OCR Misread: `afar the apostles` → `after the apostles` (MEDIUM — 1 chapter)

Found in Section 3: `"in the age afar the apostles"`. Same OCR pattern as 2.8 (`after` → `afar`).

**Fix:** Add `text = text.replace('afar the apostles', 'after the apostles')` to `post_extract_hook`.

### 2.10 OCR Misread: `hose which` → `those which` (LOW — 1 chapter)

Found in Section 3: `"And hose which relate hereunto"`. Missing initial `t`.

**Fix:** Add `text = text.replace('hose which relate', 'those which relate')` to `post_extract_hook`.

---

## 3. Items Investigated — No Action Needed

### 3.1 Missing words `pre` and `eminence` (FALSE POSITIVE)

The text integrity report flags `pre` (pdf: 6, epub: 0) and `eminence` (pdf: 4, epub: 0) as missing. These are **tokenizer artifacts**: the PDF tokenizer splits `pre-eminence` into `pre` + `eminence`, but the EPUB renders it as the single hyphenated token `pre-eminence`. No actual text is missing.

### 3.2 Missing word `self` (FALSE POSITIVE)

Same tokenizer artifact: `self-denial`, `self-love` etc. tokenize as `self` + `denial` in the PDF counter but as `self-denial` in the EPUB. No actual text is missing.

### 3.3 Missing word `defence` (INVESTIGATE)

`defence` appears 3x in PDF, only 1x in EPUB. The 2 "missing" occurrences appear to be in the treatise title page HTML (`IN DEFENCE OF THE VINDICATION`) which the word counter may not pick up from non-body HTML elements. The word itself is present in the EPUB. Likely a counter scope issue, not a text gap.

### 3.4 Excess words `digital`, `theological`, `historical`, `greek`, `footnotes`, `modern`, `edition`, `hebrew` (AGES METADATA)

These are AGES Digital Library boilerplate words that appear in the EPUB front/back matter but not in the PDF content stream. Expected and harmless.

### 3.5 Repeated word windows (Ephesians 4:16 — 25 windows)

All 25 repeated windows are the same scripture verse (Eph 4:16) cited multiple times by Owen. Legitimate repetition, not ghost-layer duplication. At budget (25/25).

### 3.6 Overlong heading candidates (7 items)

These are Owen's catechism question headings, which are genuinely long ALL-CAPS sentences. They are correctly rendered as `h3` elements. Not swallowed body text.

### 3.7 Suspicious large-number starts (4 items)

These are legitimate footnote/reference continuation numbers (e.g., `30. again, cap. 39:`). Not broken references.

### 3.8 Untagged Latin proper nouns (alexandria, victor, polycarpus, etc.)

These are English-context proper nouns (place names, person names) that happen to have Latin etymology. The 55% tagging ratio is appropriate — genuine Latin phrases are tagged; proper nouns used in English sentences need not be.

### 3.9 Untranslated Latin citations

Phrases like `Musculus, Grotius`, `Baronius, ad an. Christi`, `Mendacium mendacio tegendum ne` could benefit from `WORK_MAP` entries per the citation system documented in `AGENTS.md`. This is a **separate enhancement** (citation resolution), not a bug in the heal report.

---

## 4. Recommended Action Plan (Prioritized)

### Priority 1 — Compound merges (directly affect coverage metric)

Add to `text_replacements` in `convert.py`:

```python
'churchstate': 'church-state',
'churchsocieties': 'church-societies',
```

### Priority 2 — OCR misreads in `post_extract_hook`

Add to `post_extract_hook` in `convert.py`, after the existing fixes:

```python
text = text.replace('theft the ', 'that the ')
text = text.replace('theft it ', 'that it ')
text = text.replace('theft sentence', 'that sentence')
text = text.replace('theft numbers', 'that numbers')
text = text.replace('parochisl', 'parochial')
text = text.replace('cougregational', 'congregational')
text = text.replace('ms infinite', 'his infinite')
text = text.replace('Hobart alarms', 'Hobart affirms')
text = text.replace('aider Christ', 'after Christ')
text = text.replace('afar the apostles', 'after the apostles')
text = text.replace('hose which relate', 'those which relate')
```

### Priority 3 — Re-render and verify

```bash
.venv/bin/python3 volumes/v15/convert.py --render-only
.venv/bin/python3 scripts/audit_text_integrity.py 15
.venv/bin/python3 scripts/audit_bug_regressions.py 15
```

### Priority 4 — Expected outcome

After these fixes:
- `churchstate` disappears from the excess word list → word coverage should improve toward 99.95%+
- All 10 OCR misreads corrected → text fidelity improves
- Need score should drop below 2.0 (potentially to ~1.5 or lower)
- No whitelist changes needed (these are genuine errors, not anomalies to suppress)

### Priority 5 — Future work (separate task)

- Latin citation resolution via `WORK_MAP` additions
- Investigate `defence` counter scope issue
