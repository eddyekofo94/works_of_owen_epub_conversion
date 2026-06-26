# Plan: Add Safe Words to ENGLISH_WORDS for Latin Tagging Improvement

> **Volume:** 5 (primary), with positive cross-volume impact on v1, v3, v6, v8, v9, v11, v15
> **File to modify:** `shared.py` (line ~2339-2356)
> **Risk:** Zero — all 4 words have 0 tagged occurrences across all 16 volumes
> **Expected v5 impact:** Latin tagging ratio improves from 83.21% to ~84.02%

---

## Background

The Latin tagger in `shared.py` (`tag_latin_words()`, line 2415) uses a **run-based policy**: it only wraps text in `<span lang="la">` when it finds **≥2 consecutive Latin words**. A single Latin-looking word surrounded by English prose is deliberately never wrapped.

The audit in `audit_text_integrity.py` computes the tagging ratio differently: it counts **every word** that `is_latin_word()` classifies as Latin in the denominator, but only words actually inside `<span>` tags in the numerator. This creates a permanent gap — every isolated Latin-looking word inflates the denominator but can never make it into the numerator.

The `ENGLISH_WORDS` set in `shared.py` (line 2268) is the explicit exclusion list. Words in this set return `False` from `is_latin_word()`, removing them from the audit denominator entirely. This is the documented project practice for known false positives (see the comments at lines 2339-2346: "English words of Latin origin that end in Latin suffixes and are frequently mis-flagged").

## What to Change

Add 4 words to the `ENGLISH_WORDS` set in `shared.py`:

| Word | Category | v5 occurrences | Cross-volume total | Tagged anywhere? |
|------|----------|----------------|---------------------|-------------------|
| `obviate` | English word of Latin origin | 8 | 42 across 7 volumes | 0 — never tagged |
| `adequate` | English word of Latin origin | 7 | 28 across 5 volumes | 0 — never tagged |
| `genius` | English word of Latin origin | 5 | 11 across 2 volumes | 0 — never tagged |
| `onesimus` | Proper name (biblical/historical) | 10 | 10 in v5 only | 0 — never tagged |

### Why these are safe

Verified across **all 16 Owen volumes** — these 4 words have **zero tagged occurrences** anywhere in any volume. They are always singletons in English prose, never part of a multi-word Latin run. Removing them from the Latin classifier only shrinks the audit denominator; no `<span lang="la">` tags are lost.

### Why other words are NOT safe

These words were considered but rejected because they have tagged occurrences in Latin runs in other volumes:

| Word | Rejected because | Tagged occurrences |
|------|------------------|--------------------|
| `socinus` | v12 has 36 tagged in Latin citation runs | 41 total across volumes |
| `grotius` | v12 has 16 tagged | 20 total |
| `thomas` | 7 tagged across volumes | 7 total |
| `pelagius` | v11 has 2 tagged | 2 total |
| `schlichtingius` | v12 has 5 tagged | 5 total |
| `reus` | v5 has 5 tagged, genuine Latin legal usage | 5 total |

Adding these would break legitimate Latin spans in other volumes.

---

## Exact Code Change

### File: `shared.py`

#### Change 1: Add `obviate`, `adequate`, `genius` to the "English words of Latin origin" section

**Location:** Line 2339-2346

**Current code:**
```python
    # English words of Latin origin that end in Latin suffixes and are frequently mis-flagged
    'adhere', 'inordinate', 'profligate', 'forego', 'meditate', 'alas', 'stream', 'undergo',
    'pleas', 'communicate', 'hate', 'door', 'analysis', 'apostate', 'dream', 'succor',
    'contemplate', 'inferior', 'obstinate', 'innate', 'animate', 'nowhere', 'tract', 'insinuate',
    'magistrate', 'dissent', 'ere', 'accommodate', 'abhor', 'horror', 'armor', 'temperate',
    'premium', 'emphasis', 'create', 'laodicea', 'ephesus', 'proportionate', 'abate',
    'importunate', 'whereto', 'whoso', 'alienate', 'elisha', 'habituate', 'william',
    'captivate', 'beam', 'humor', 'ingenerate', 'malefactor',
```

**Change:** Add `'obviate', 'adequate', 'genius',` to the end of this block (after `'malefactor',`):

```python
    # English words of Latin origin that end in Latin suffixes and are frequently mis-flagged
    'adhere', 'inordinate', 'profligate', 'forego', 'meditate', 'alas', 'stream', 'undergo',
    'pleas', 'communicate', 'hate', 'door', 'analysis', 'apostate', 'dream', 'succor',
    'contemplate', 'inferior', 'obstinate', 'innate', 'animate', 'nowhere', 'tract', 'insinuate',
    'magistrate', 'dissent', 'ere', 'accommodate', 'abhor', 'horror', 'armor', 'temperate',
    'premium', 'emphasis', 'create', 'laodicea', 'ephesus', 'proportionate', 'abate',
    'importunate', 'whereto', 'whoso', 'alienate', 'elisha', 'habituate', 'william',
    'captivate', 'beam', 'humor', 'ingenerate', 'malefactor',
    'obviate', 'adequate', 'genius',
```

#### Change 2: Add `onesimus` to the "More English words / proper nouns" section

**Location:** Line 2347-2356

**Current code:**
```python
    # More English words / proper nouns that end in Latin suffixes to avoid false-positive Latin classification
    'hist', 'seas', 'determinate', 'palestina', 'relate', 'manna', 'dictate', 'ago', 'governor', 
    'asia', 'cyrus', 'emperor', 'tibni', 'omri', 'propagate', 'lazarus', 'superior', 'cautionate', 
    'gate', 'sedate', 'basis', 'conqueror', 'jeroboam', 'senate', 'prejudicate',
    'precipitate', 'illustrate', 'interfere', 'delicate', 'potentate', 'tolerate', 'athanasius', 'valor', 
    'extricate', 'desolate', 'josephus', 'facto', 'date', 'splendor', 'translate', 'successor', 'officiate', 
    'bithynia', 'irenaeus', 'subordinate', 'vita', 'associate', 'christianos', 'augustus',
    'appropriate', 'inviolate', 'participate', 'delineate', 'inmate', 'operate', 'cognate', 'aggravate', 
    'dedicate', 'enervate', 'elevate', 'antithesis', 'anathema', 'decorum', 'novatianus', 'hegesippus', 
    'episcopius', 'anchor', 'moderate', 'demas', 'dam', 'dram', 'levi', 'sardis', 'jericho', 'erasmus',
```

**Change:** Add `'onesimus',` to the end of this block (after `'erasmus',`):

```python
    # More English words / proper nouns that end in Latin suffixes to avoid false-positive Latin classification
    'hist', 'seas', 'determinate', 'palestina', 'relate', 'manna', 'dictate', 'ago', 'governor', 
    'asia', 'cyrus', 'emperor', 'tibni', 'omri', 'propagate', 'lazarus', 'superior', 'cautionate', 
    'gate', 'sedate', 'basis', 'conqueror', 'jeroboam', 'senate', 'prejudicate',
    'precipitate', 'illustrate', 'interfere', 'delicate', 'potentate', 'tolerate', 'athanasius', 'valor', 
    'extricate', 'desolate', 'josephus', 'facto', 'date', 'splendor', 'translate', 'successor', 'officiate', 
    'bithynia', 'irenaeus', 'subordinate', 'vita', 'associate', 'christianos', 'augustus',
    'appropriate', 'inviolate', 'participate', 'delineate', 'inmate', 'operate', 'cognate', 'aggravate', 
    'dedicate', 'enervate', 'elevate', 'antithesis', 'anathema', 'decorum', 'novatianus', 'hegesippus', 
    'episcopius', 'anchor', 'moderate', 'demas', 'dam', 'dram', 'levi', 'sardis', 'jericho', 'erasmus',
    'onesimus',
```

---

## Verification Protocol

### Step 1: Make the code changes
Apply the two changes above to `shared.py`.

### Step 2: Verify classification changed
Run this quick check:
```bash
cd /Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen
.venv/bin/python3 -c "
import sys; sys.path.insert(0, '.')
from shared import is_latin_word
for w in ['obviate', 'adequate', 'genius', 'onesimus']:
    print(f'{w}: is_latin_word = {is_latin_word(w)}')
"
```
**Expected output:** All 4 words should return `False` (was `True` before).

### Step 3: Re-render Volume 5
```bash
.venv/bin/python3 volumes/v5/convert.py --render-only
```

### Step 4: Re-run Volume 5 audits
```bash
.venv/bin/python3 scripts/audit_epub.py 5
.venv/bin/python3 scripts/audit_text_integrity.py 5
.venv/bin/python3 scripts/audit_anomalies.py 5
.venv/bin/python3 scripts/audit_bug_regressions.py 5
```

### Step 5: Verify v5 Latin tagging ratio improved
Check `volumes/v5/bugs_fixes/volume_5_text_integrity.md`:
- Latin word tagging ratio should increase from 0.8321 to ~0.84
- Untagged Latin word samples should no longer list `obviate`, `adequate`, `genius`, `onesimus`
- All other metrics should remain unchanged (Greek 100%, Hebrew 100%, coverage 99.99%, splits 0, anomalies 0)

### Step 6: Run regression tests
```bash
.venv/bin/python3 -m pytest tests/test_bug_regressions.py
```
All tests must pass.

### Step 7: Spot-check another affected volume
Re-render and audit v3 (or v11) to confirm no regression:
```bash
.venv/bin/python3 volumes/v3/convert.py --render-only
.venv/bin/python3 scripts/audit_text_integrity.py 3
```
Check that v3's Latin tagging ratio improved or stayed the same (should improve since `obviate` and `adequate` are in v3 too).

### Step 8: Regenerate state report
```bash
.venv/bin/python3 scripts/report_volume_state.py
```
Verify v5 Need score stayed at 0.4 (or improved if Latin tagging crosses a threshold that allows removing the whitelist entry).

### Step 9: Archive reports
Copy the latest audit reports to the timestamped archive:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p volumes/v5/reports/$TIMESTAMP
cp volumes/v5/bugs_fixes/volume_5_*.{md,json} volumes/v5/reports/$TIMESTAMP/
```

---

## Cross-Volume Impact Summary

All changes are positive (denominator shrinks, ratio improves or stays same):

| Volume | Words removed from denominator | Expected ratio change |
|--------|-------------------------------|----------------------|
| v1 | 8 (adequate) | Slight improvement |
| v3 | 15 (obviate + adequate) | Noticeable improvement |
| v5 | 30 (obviate + adequate + genius + onesimus) | 83.21% → ~84.02% |
| v6 | 8 (obviate) | Slight improvement |
| v8 | 3 (obviate) | Slight improvement |
| v9 | 7 (obviate + adequate) | Slight improvement |
| v11 | 13 (obviate + genius) | Noticeable improvement |
| v15 | 7 (obviate + adequate) | Slight improvement |

Volumes not listed (v2, v4, v7, v10, v12, v13, v14, v16) are unaffected — none of these 4 words appear in their untagged samples.

---

## What NOT to Change

1. **Do NOT add `socinus`, `grotius`, `thomas`, `pelagius`, `schlichtingius`, `reus` to `ENGLISH_WORDS`** — these have tagged occurrences in Latin runs in other volumes (especially v12). Adding them would break legitimate Latin spans.
2. **Do NOT change the tagger's ≥2-word run policy** — this is the correct semantic behavior. Single Latin-looking words in English prose should not be wrapped in `<span lang="la">`.
3. **Do NOT change the audit metric** — that is a separate concern not in scope for this change.
4. **Do NOT modify `render.py`** — the Latin tagging logic lives in `shared.py` and is invoked via `tag_unicode_ranges()` in `render.py`. No changes needed in `render.py`.
5. **Do NOT remove the `low_latin_tagging` whitelist entry** from `volume_5_whitelist.json` — the ratio will still be below 99% even after this change. The whitelist is still needed.

---

## Expected Final State

After this change:
- v5 Latin tagging ratio: ~84.02% (up from 83.21%)
- v5 Need score: 0.4 (unchanged — `low_latin_tagging` still whitelisted)
- All regression tests pass
- No volume regresses
- 4 fewer false-positive Latin words in the classifier across all 16 volumes
