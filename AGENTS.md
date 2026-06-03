# John Owen Works — Agent Instructions

> [!IMPORTANT]
> **MANDATORY WORKSPACE CONVENTION — GROUPED WORKTREE LAYOUT**
> We work strictly within the **Grouped Git Worktree** layout inside `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/` (the parent folder).
> - **Bare repo:** `Owen.git/` (acting as the hub).
> - **Worktrees:** `master/` (the master branch workspace) and `Owen-<branch-name>/` (isolated development workspaces).
> - **Always work on the latest development branch:** Check for other active worktrees/branches (e.g. `translation-citations`, `architectural-hardening`) using `git worktree list` or `git branch` and always work on the most recent developmental branch/worktree, as `master/` may not contain the latest features or changes.
> - **Do NOT use `git checkout -b`** to create branches directly inside a worktree. Use the `git -C ../Owen.git worktree add ../Owen-<branch-name> -b <branch-name>` protocol.
> - **Virtualenv & CLI:** Use the local virtual environment `.venv/` inside the worktree root. Do NOT reference global virtual environments. Use `./owen` (the directory-agnostic CLI wrapper) to run tests, audits, and builds from **any** folder in the workspace.

This repository is currently focused on the 16-volume Owen Works conversion. The Hebrews commentary is intentionally out of scope until the Owen volumes are stable and validated.

## Volume Structure Reference

The complete 16-volume structure (division, volumes, and contents) is documented in `works_of_john_owen.md`. This table of contents serves as the canonical reference for:
- Volume organization (Divisions 1-3)
- Individual volume contents and treatises
- Mapping between PDF sources and logical book structure

## Execution Scope

Work on one Owen volume at a time. Do not run all 16 volumes, batch audits, or batch conversions unless the user explicitly asks for a batch run.

The PDFs share the same general AGES structure, so a fix proven on one volume is expected to transfer to the others with only small volume-specific adjustments. Prefer Volume 1 as the default test volume unless the user names another volume.

Do not regenerate or audit additional volumes merely to prove transferability. If a converter fix works for the named/default test volume and is structurally generic, assume it applies to the remaining Owen volumes and report that expectation. Ask before running any extra volume, even a subset of affected volumes.

## Active Converter — Two-Stage Modular Pipeline (Issue 91)

The pipeline uses three focused modules. `converter.py` is a legacy orchestrator that
imports from the new modules and is still functional but **not the preferred path**.

### Preferred: Per-volume scripts (current standard)

```bash
# Full pipeline for volume 1 (extract PDF + render EPUB)
.venv/bin/python3 volumes/v1/convert.py

# Stage 2 only — fast re-render from cached JSON (no PDF I/O, ~3 seconds)
.venv/bin/python3 volumes/v1/convert.py --render-only

# Stage 1 only — re-extract when extraction logic changes
.venv/bin/python3 volumes/v1/convert.py --extract-only
```

Per-volume scripts exist for v1. When working on a new volume, create
`volumes/vN/convert.py` from the v1 template and populate `OVERRIDES`.

**IMPORTANT:** Always use `volumes/vN/convert.py` for testing and rebuilding.
The legacy `converter.py` does not pass volume-specific `OVERRIDES` (OCR fixes,
paragraph hooks) to the render pipeline, so EPUBs built with it will miss
volume-specific corrections.

### Stage entry points (direct)

```bash
# Stage 1: PDF → JSON intermediate
.venv/bin/python3 extract.py 1

# Stage 2: JSON → EPUB3
.venv/bin/python3 render.py 1
```

### Legacy orchestrator (now respects per-volume OVERRIDES)

```bash
# Process a single Owen volume (loads OVERRIDES from volumes/vN/convert.py)
.venv/bin/python3 converter.py 3

# Process all 16 Owen volumes (extract, render, or both)
.venv/bin/python3 converter.py
.venv/bin/python3 converter.py --extract-only
.venv/bin/python3 converter.py --render-only
```

### Current outputs

- Owen Works: `volumes/vN/output/volume_N.epub`
- JSON intermediate: `volumes/vN/intermediate/volume_N.json`  ← NEW (Stage 1 output)
- ThML intermediate: `volumes/vN/intermediate/volume_N.thml.xml`  ← legacy (footnote source)

Do not use the all-volumes command during normal work unless explicitly requested.

## Mandatory Protocols

Read `GEMINI.md` before changing converter behavior or project documentation. In particular:

- Do not mark issues as "Finished", "Fixed", or "Done" in `BUGS_AND_FIXES.md` unless the user explicitly validates the result.
- Use `IMPLEMENTED (AWAITING VALIDATION)` for work that has been coded but not user-approved.
- Complex issues, especially Issue 40 and later, need a post-mortem in `ENGINEERING_LOG.md`.
- Preserve the holistic paragraph-healing behavior in `reconstruct_paragraphs()` and `get_pages_text()`.
- **Text Integrity & Anomaly Triage Protocol:** When reviewing text anomalies flagged by `scripts/audit_anomalies.py` (such as hyphenation anomalies like `birth-place`, `free-will`, `co-essential`), **NEVER modernize 17th-century orthography**. All potential anomalies should be flagged for visibility, but **do not apply replacements to historical spellings or hyphenations if they were acceptable in the author's day**. Apply overrides strictly to clear OCR errors, line-break leftovers (like `Peta-vius`), and alphanumeric typos (like `iraFated`).

## Git Repository — Worktree Setup

This project uses a **grouped Git worktree** layout inside `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/` (the parent folder). Do NOT use `git checkout -b` to create branches.

- **Bare repo (hub):** `Owen.git/` (inside the parent `Owen/` folder)
- **Worktree locations:**
  - `master/` (for the `master` branch)
  - `Owen-<branch-name>/` (for other development branches)
- **Remote:** `git@github.com:eddyekofo94/works_of_owen_epub_conversion.git`

### Creating a new branch

From the parent `Owen/` directory:
```bash
git -C ./Owen.git worktree add ./Owen-<branch-name> -b <branch-name>
```

From inside an active workspace folder (like `master/`):
```bash
git -C ../Owen.git worktree add ../Owen-<branch-name> -b <branch-name>
```

Always `cd` into the new branch workspace directory before running commands or editing files.

### Converting a new worktree to relative paths (Mandatory Portability)

By default, Git writes absolute paths inside `.git` files and metadata. To prevent paths from breaking when folders are moved, renamed, or checked out on a different machine, **always convert newly created worktrees to relative paths immediately after creation**:

1. Open `Owen-<branch-name>/.git` and rewrite its absolute `gitdir` line to be relative:
   ```text
   gitdir: ../Owen.git/worktrees/Owen-<branch-name>
   ```
2. Open `Owen.git/worktrees/Owen-<branch-name>/gitdir` and rewrite its absolute path to be relative:
   ```text
   ../../../Owen-<branch-name>/.git
   ```

*(This relative path linkage makes the entire multi-worktree workspace 100% portable and independent.)*

## Project Shape

```text
Owen/
├── README.md                    # Human overview and quick start
├── AGENTS.md                    # Agent-facing operating instructions
├── GEMINI.md                    # Non-negotiable project mandates
├── PLAN.md                      # Active roadmap and QA plan
├── ENGINEERING_LOG.md           # Technical post-mortems
├── extract.py                   # Stage 1: PDF → JSON intermediate (Issue 91)
├── render.py                    # Stage 2: JSON → EPUB3 (Issue 91)
├── converter.py                 # Legacy wrapper around extract.py + render.py
├── shared.py                    # Metadata, CSS, fonts, Greek/Hebrew converters
├── docs/archive/                # Historical plans and session summaries
├── covers/                      # v1.png-v16.png
├── fonts -> ../../fonts         # Shared font repository symlink
├── pdfs/                        # Source AGES PDFs
├── portraits/                   # Frontispiece images
├── special_sources/legacy/      # Archived CCEL XML zips for v5 and v10 (not used by pipeline)
└── volumes/v1-v16/
    ├── convert.py               # Per-volume script (v1 exists; others to be created)
    ├── input/                   # PDF symlink
    ├── intermediate/            # volume_N.json (Stage 1 output) + volume_N.thml.xml
    ├── output/                  # Generated EPUB
    └── bugs_fixes/              # Per-volume issue log
```

## Current Pipeline

The converter uses a hybrid extraction strategy:

1. PyMuPDF4LLM extracts a Markdown-like structural skeleton.
2. Raw PyMuPDF span extraction supplies font-aware text where Greek or Hebrew legacy fonts appear.
3. `shared.py` converts AGES Koine Greek and Gideon Hebrew encodings to Unicode.
4. Body text is cleaned, de-duplicated, and healed across page boundaries.
5. Footnotes are extracted from PDF and enriched from existing ThML intermediates.
6. EPUB3 output is assembled with embedded fonts, cover, frontispiece, NAV, NCX, landmarks, endnotes, and Apple Books display options.

### Known Fixes Applied (Stage 1 — extract.py)

- **Greek text preservation**: `_remove_adjacent_line_overlaps` and related dedup functions now include Greek/Hebrew Unicode ranges in their word-matching regexes, preventing false overlap detection on Greek text.
- **Greek letter mapping**: `GREEK_UPPER['Y']` corrected from Psi (Ψ) to Upsilon (Υ) for AGES Koine encoding. `GREEK_LOWER` and `GREEK_UPPER` use AGES Koine conventions (c=chi, x=xi).
- **`_remove_adjacent_line_overlaps`**: Fixed regex to include Greek/Hebrew characters: `r"[A-Za-z0-9:;,''\u0370-\u03FF\u1F00-\u1FFF\u0590-\u05FF]+"`

### Volume-Specific OCR Fixes (volumes/vN/convert.py)

Volume 1 `OVERRIDES` includes `text_replacements` for known OCR artifacts:
- `on]y` → `only`, `name]y` → `namely`
- `Charneck` → `Charnock`, `whoso` → `whose`, etc.
- Scripture reference deduplication fixes

These are applied during Stage 2 rendering via `_repair_owen_ocr_errors()`.

## Source Rules

All 16 volumes use the AGES PDF path (`source_type: ages_pdf`) through the live `extract.py`/`render.py` pipeline. Volume 10 additionally uses CCEL XML enrichment via `ccel_enrich.py` as a `post_extract_hook`.

**v5 + v10 migration (May 2026):** Both volumes were formerly `ccel_xml`-sourced. Clean AGES PDFs were obtained and both were migrated to `ages_pdf`. Legacy CCEL XMLs are archived at `special_sources/legacy/` — not used by the pipeline. `ccel_enrich.py` is now legacy/inactive.

## Font Strategy

Primary font selection is deterministic per volume and comes from `shared.py`.

Always-injected supplements:

- SBL BibLit
- SBL Greek
- SBL Hebrew
- Ezra SIL

Language tagging target:

- Greek: `<span lang="el" xml:lang="el">...</span>`
- Hebrew: `<span lang="he" xml:lang="he" dir="rtl">...</span>`

## Preferred Work Pattern

For converter changes:

1. Reproduce on a single volume, usually volume 1 unless the issue is volume-specific.
2. Add or update a focused QA check when possible.
3. Generate the affected EPUB.
4. Inspect the output package or rendered XHTML for the exact failure mode.
5. Update `BUGS_AND_FIXES.md` only with validation-safe status language.
6. Add an `ENGINEERING_LOG.md` entry for complex architectural changes.

### Owenian Rendering Standards

Before changing flat-list, block-list, nested-list, or blockquote behavior, read
the shared standards:

- `bugs_fixes/owenian-structure-rules.md` — the master standard for Owen's
  inline syllabus lists, block exposition lists, nested subpoints, and
  geometry-backed blockquotes.
- `bugs_fixes/flat-list-rules.md` and `bugs_fixes/blockquote-rules.md` are
  supporting focused notes for the two most common structural failure classes.

These rules are agent-facing instructions, not historical notes. New fixes in
these areas should preserve the documented false-positive guards and add focused
regression coverage for any newly observed pattern.

### Regression Tests From Bug Reports

Known bug classes must be guarded by pytest once they are flagged and an implementation is added. The current v1-derived regression gate lives in:

- `tests/test_bug_regressions.py`
- `scripts/audit_bug_regressions.py`
- `qa/bug_regression_baselines.json`

This gate checks the bug classes most likely to recur across Owen volumes, especially:

- Possible faulty paragraph splits
- Inline structural marker candidates
- Untagged Greek and Hebrew
- Repeated word windows

When a bug implementation reduces or eliminates one of these classes, lower the matching budget in `qa/bug_regression_baselines.json`. When a bug has a concrete sample string, add it to `absent_samples` so pytest fails if that sample reappears. Default test scope is Volume 1:

```bash
.venv/bin/python3 -m pytest tests/test_bug_regressions.py
```

To check additional already-generated volumes without running a batch conversion:

```bash
OWEN_REGRESSION_VOLUMES="1 2 3" .venv/bin/python3 -m pytest tests/test_bug_regressions.py
```

For the report-driven `#test` workflow, use the bug-regression report after the standard audits:

```bash
.venv/bin/python3 scripts/audit_bug_regressions.py 2
```

This writes `volumes/v2/bugs_fixes/volume_2_bug_regressions.md` and `.json`, making recurring bug classes visible without replacing the normal EPUB and text-integrity reports.

For documentation changes:

1. Keep root docs short and current.
2. Move historical notes to `docs/archive/` instead of deleting them.
3. Avoid duplicating the same roadmap in multiple files.

## Mobile-First Robust Styling Mandate

Every volume must strictly adhere to these CSS and EPUB3 standards to ensure a premium reading experience on iPhone and Apple Books.

### 1. Responsive Typography & Layout
- **Relative Units ONLY**: Use `em` or `rem` for all margins, padding, and font-sizes. Never use fixed `px` or `pt`.
- **Prevent Font Inflation**: Apply `-webkit-text-size-adjust: 100%;` to the `body` to stop iOS from randomly resizing text.
- **Guard Railing**: Use `word-break: break-word;` globally to prevent long Greek/Hebrew strings from breaking the layout.
- **iPhone Margins**: Avoid large side margins (e.g., `18em`). Use responsive alignments and small relative margins (`0.4em 0.5em`).
- **Hyphenation**: Enable `-webkit-hyphens: auto;` for all prose paragraphs to ensure smooth flow on narrow screens.

### 2. High-Quality Visual Refinements
- **Owen Blue Palette**: Use `#2a55a0` for all interactive elements, including links and footnote numbers.
- **Continuous Blockquotes**: 
    - Quote paragraphs must have `margin-top: 0;` and `margin-bottom: 0;` to ensure they sit flush.
    - Apply `border-left: 2.5px solid rgba(0, 0, 0, 0.08);` to create a continuous, subtle vertical marker.
    - Use sibling selectors to provide breathing space (`1.2em`) before and after the *entire* quote block.
- **Drop-Cap Spacing**: For large initials (`.large`), use negative margins (e.g., `-0.15em`) to pull the following text flush against the character stem.

### 3. iPhone Usability (Tappability)
- **Easy-Tap Footnotes**: Expand the touch target for all `noteref` links using "ghost padding" (`padding: 0.1em 0.2em;`). This makes small numbers much easier to tap on a phone screen.

### 4. Automated Polyglot Support
- **Automatic Tagging**: Every script must implement a function to automatically wrap untagged Greek and Hebrew Unicode runs in `<span lang="el">` or `<span lang="he">`.
- **RTL Integrity**: Hebrew spans MUST include `dir="rtl"` and use `unicode-bidi: isolate;` to prevent layout spills.
- **Specialized Fonts**: Assign **SBL Greek** and **SBL Hebrew** specifically to these language spans for maximum legibility.

### 5. Structural & Package Integrity
- **CDATA Wrapping**: Always wrap injected CSS in `/*<![CDATA[*/ ... /*]]>*/` blocks to prevent XML parsing errors from CSS comments or selectors.

## Treatise Title Pages — Architecture and Rules

### The Core Rule

**Every treatise title page for every volume must be defined as hardcoded HTML inside that volume's `volumes/vN/convert.py`, in `OVERRIDES['treatise_title_overrides']`.**

Never place volume-specific treatise names, verse text, or structural HTML inside `render.py` or `shared.py`. These shared files must remain volume-agnostic. Cross-volume contamination is the root cause of the "fix v3 → break v1" cycle.

### Why This Rule Exists

`render.py` contains `format_treatise_title_page()`, a generic PDF-reading fallback. It is unreliable because:

1. It reads raw PDF layout data which is OCR-noisy and font-encoding-dependent.
2. The same function is used by all volumes, so any change to it affects all volumes simultaneously.
3. `render.py` line ~3343 also **hardcodes Volume 1 treatise names** (`CHRISTOLOGIA|MEDITATIONS|TWO SHORT CATECHISMS`) in a shared conditional — a direct violation of the separation principle.

The dispatch hook at render.py line ~3357 already supports the correct pattern:
```python
raw_text = config.get('treatise_title_overrides', {}).get(ch_dict['title'], raw_text)
```
This means: if a `treatise_title_overrides` entry exists for a chapter's title, it replaces the raw PDF text entirely. **Use this hook for every treatise title page.**

### render.py Cleanup Required

When implementing the full architecture, remove the hardcoded volume-1 names from render.py line ~3343:
```python
# BEFORE (fragile — hardcodes v1 treatise names in shared code):
elif ch_dict.get('is_treatise') and re.search(
    r'\b(?:PART|BOOK)\s+[0-9IVXLCDM]+\b|\b(?:CHRISTOLOGIA|MEDITATIONS|TWO SHORT CATECHISMS)\b',
    title_upper,
):

# AFTER (generic — any is_treatise chapter uses BODY_START mode):
elif ch_dict.get('is_treatise'):
```
This change is safe because `is_treatise` is already the correct semantic signal. The named exceptions only existed because volume 1's treatises did not reliably set `is_treatise`.

### CSS Classes Available for Title Page HTML

All of these classes are defined in `shared.py`'s `EPUB_STYLESHEET` and apply within a `<section class="treatise-title-page ...">` wrapper:

| Class | Purpose |
|---|---|
| `.treatise-title-page` | Outer section wrapper (required, centered text) |
| `.title-line-major` | Large main title (~2.2em, serif) |
| `.title-line-medium` | Subtitle line (~1.15em, serif) |
| `.title-connector` | Small connector word ("Or", "Concerning", "In") — spaced with letter-spacing |
| `.title-rule` | Decorative horizontal rule (`aria-hidden="true"`) |
| `.title-source` | Scripture reference line (bold, small, centered) |
| `.greek-title` | Greek heading text (1.25em, letter-spaced) |
| `.descriptive` | Italic descriptive block |
| `.quote-block` | Left-aligned quote block (margin 2em 8%) |

### Standard Title Page HTML Template

```html
<section class="treatise-title-page" epub:type="titlepage">
<p class="greek-title">Χριστολογία</p>           <!-- if has Greek title -->
<p class="title-line-major">Main Title Here</p>
<p class="title-connector">Or,</p>
<p class="title-line-medium">Subtitle or Declaration Here</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">Scripture Reference, Chapter X.</p>
</section>
```

For multi-part treatises (no Greek, connector-heavy structure):
```html
<section class="treatise-title-page v1-applied-glory-title" epub:type="titlepage">
<p class="title-line title-line-medium">Part Title</p>
<p class="title-connector">Concerning</p>
<p class="title-line title-line-major">Main Subject;</p>
<p class="title-connector">Applied Unto</p>
<p class="title-line title-line-medium">Further Specification</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="title-source">In N Chapters, from John XVII. 24.</p>
</section>
```

### Volume-by-Volume Title Page Inventory

The chapter title strings used in `treatise_title_overrides` must match the exact title string in the JSON intermediate (`volumes/vN/intermediate/volume_N.json`). Verify by inspecting the JSON if a title page doesn't appear.

**Volume 1** — 4 treatises (1 defined, 3 still using generic fallback):
- `Christologia` — ⚠️ not in `treatise_title_overrides`; has broken verse rendering; needs hardcoded HTML
- `Part 1 - Meditations and Discourses on the Glory of Christ` (or similar) — ⚠️ not defined
- `Part 2 - Meditations and Discourses Concerning The Glory of Christ` — ✅ defined (`_V1_PART_2_TITLE_PAGE`)
- `Two Short Catechisms` (or similar) — ⚠️ not defined

**Volume 2** — 2 treatises:
- Communion with God the Father, Son, and Holy Ghost
- A Brief Declaration and Vindication of the Doctrine of the Trinity

**Volume 3** — 1 treatise:
- Pneumatologia (Books I–V; may have BOOK I–V sub-treatises)

**Volume 4** — 4 treatises:
- The Reason of Faith; Causes, Ways, and Means; Work of the Holy Spirit in Prayer; Holy Spirit and His Spiritual Gifts

**Volume 5** — 2 treatises:
- The Doctrine of Justification by Faith; Evidences of the Faith of God's Elect

**Volumes 6–16** — see `works_of_john_owen.md` for full list.

For each new volume's `convert.py`, add all treatise title pages to `OVERRIDES`:
```python
OVERRIDES = {
    # ... other keys ...
    'treatise_title_overrides': {
        'Exact Chapter Title From JSON': '''<section class="treatise-title-page" epub:type="titlepage">
...
</section>''',
        'Second Treatise Title': '''...''',
    },
}
```

### How to Find Exact Chapter Title Strings

```bash
# Inspect the JSON intermediate to find treatise chapter titles:
python3 -c "
import json
with open('volumes/v1/intermediate/volume_1.json') as f:
    data = json.load(f)
for ch in data.get('chapters', []):
    if ch.get('is_treatise'):
        print(repr(ch['title']))
"
```

Run this for each volume before writing its `treatise_title_overrides` entries.

### Checklist for Adding a New Volume's Title Pages

1. Run the JSON inspection command above to get exact title strings.
2. Look at the PDF pages manually (or inspect the generic fallback output) to understand the layout.
3. Write hardcoded HTML using the CSS classes above.
4. Add to `OVERRIDES['treatise_title_overrides']` in `volumes/vN/convert.py`.
5. Rebuild with `--render-only` and verify in Apple Books.
6. Do **not** modify `render.py` or `shared.py` for volume-specific content.

---

## Slash Commands

When the user uses slash commands, execute them as follows:

### `#test audit [n]`

Executes comprehensive audits for the specified volume(s).

**Command Syntax:**
- `#test audit 1`: Run audits for volume 1.
- `#test audit 1 2 5`: Run audits for multiple volumes.
- `#test audit all`: Run audits for all 16 volumes.

**What it does:**
- Regenerates the EPUB for the volume.
- Runs `scripts/audit_epub.py` to check structural and metadata health.
- Runs `scripts/audit_text_integrity.py` to check text faithfulness and extraction quality.
- Summarizes the key results (Errors, Warnings, Word Coverage, Footnote Counts).

**Location of detailed reports:**
- `volumes/vN/bugs_fixes/volume_N_audit.md`
- `volumes/vN/bugs_fixes/volume_N_text_integrity.md`

### `#test bug [n]`

Executes the known-bug regression report for the specified volume(s), using the latest audit JSON reports.

**Command Syntax:**
- `#test bug 1`: Run the bug-regression report for volume 1.
- `#test bug 1 2 5`: Run the bug-regression report for multiple volumes.
- `#test bug all`: Run the bug-regression report for all 16 volumes.

**What it does:**
- Runs `scripts/audit_bug_regressions.py` to summarize known recurring bug classes against the latest audit reports.
- Checks the regression budget in `qa/bug_regression_baselines.json`.
- Highlights recurring repair queues, especially paragraph splits, inline structural markers, untagged Greek/Hebrew, repeated word windows, missing enumerators, and related audit classes.

**Location of detailed reports:**
- `volumes/vN/bugs_fixes/volume_N_bug_regressions.md`

### `#test report [n]`

Generates a ranked QA state report for the specified volume(s).

**Command Syntax:**
- `#test report`: Run report for all 16 volumes.
- `#test report 1`: Run report for volume 1.
- `#test report 1 2 5`: Run report for multiple volumes.

**What it does:**
- Reads existing audit, text integrity, and bug regression reports.
- Scores each volume (coverage, Greek/Hebrew health, splits, warnings, errors).
- Ranks worst → best, prints a ranked table, and writes detailed reports.
- Updates the Per-Volume Script Status table in README.md.

**Location of detailed reports:**
- `qa/reports/volume_state_report.md`
- `qa/reports/volume_state_report.json`

## Citation System — Agent Briefing (June 2026)

### Goal
Every abbreviated inline citation Owen makes must be expanded to a full modern
academic footnote matching the quality of the reference EPUBs in `epub_examples/`:

> John Chrysostom, *Homilies on the Gospel of John*, Homily 15, on John 1:18
> [NPNF1, 14:51; PG 59.97–98].

NOT acceptable: "Modern Citation: Book 7, Chapter 29." (vague, useless).

### Citation audit files
- `plans/citation_audit_report.md` — full human-readable report of all 499 citations
- `plans/citation_audit.csv` — machine-readable row for every citation
- `plans/current_state.md` — overall project state and priority queue

Run `python3 scripts/scan_citations.py` to regenerate the audit at any time.

### The two-tier system

**Tier 1 — `BODY_TRANSLATIONS` (translation_db.py)**
Exact phrase → full citation. Add when Owen writes a specific, distinctive phrase
(author + work + location in one string). The matching is word-by-word and
resilient to intervening HTML tags.

Format:
```python
"Euseb. Hist. Eccles., lib. 4: cap. 15:": (
    "<b>Modern Citation:</b> Eusebius of Caesarea, "
    "<i>Ecclesiastical History</i> (Historia Ecclesiastica), "
    "Book 4, Chapter 15 [NPNF2, 1:185; PG 20.349]."
),
```

**Tier 2 — `WORK_MAP` (patristic_refs.py)**
Pattern-based: add (author_key, work_fragment) → work data. The system detects
the author and work abbreviation from surrounding text and automatically generates
a citation for any `lib./cap./epist.` location reference that follows.

Format:
```python
("bellar", "de justif"): {
    "full_title": "On Justification",
    "latin_title": "De Iustificatione",
    "std_ref": ["Disputationes de Controversiis, Tom. IV (Ingolstadt, 1601)"],
},
```

Author key comes from `AUTHOR_ABBREV_MAP`. Work fragment is the lowercase,
dot-stripped form of Owen's work abbreviation (e.g. "De Justif." → "de justif").

To add a new author: add a line to `AUTHOR_ABBREV_MAP` in `patristic_refs.py`.

### Important rules
- **Only generate notes when the specific work is identified.** A footnote without
  the work title is worthless. Both tiers enforce this: if neither the work context
  search nor the cite-abbrev fallback finds a WORK_MAP entry, no note is generated.
- **Do NOT add English Bible verse text as BODY_TRANSLATIONS keys.** This generates
  pointless "Modern Citation: Bible, John, 14:1" notes on every scripture quotation.
- **Do NOT add `<span lang="la">` manually** to raw_text in JSON intermediates.
  The renderer strips these before html_escape anyway; `tag_unicode_ranges()` handles
  all language tagging automatically.
- **Research using internet resources**: NPNF/ANF at ccel.org, PL at pl.mgh.de,
  PG at migne.patristica.net, Loeb at loebclassics.com, Perseus at perseus.tufts.edu.

### Priority unresolved citations (high-impact WORK_MAP additions)
| Add to WORK_MAP | Owen's text | Resolves |
|---|---|---|
| `("bellar","de justif")` | `Bellar. de Justif., lib. 2` | ~15 v5 citations |
| `("bellar","de amiss")` | `De Amiss. Grat., lib. 4` | ~8 citations |
| `("bellar","de grat")` | `De Grat. et Lib. Arbit., lib. 6` | ~5 citations |
| `("socin","de servat")` | `Socin. de Servant. lib. 3` | ~10 citations |
| `("canus","loc theol")` | `Canus, Loc. Theol., lib. 2` | ~6 v4 citations |
| `("sozomen","hist eccles")` | `Sozomen Hist. Eccles.` | ~8 v11/v12 citations |
| `("damasc","de fide")` | `Damascen, lib. 4 chap. 3` | ~4 citations |
| `("bernard","epist")` | `Bernard, Epist. 190` | ~5 v5 citations |

## Recent Key Curation & Fixes Summary (May 2026)

### 1. Volume 3 Treatise Title Page & TOC Curation
- **Treatise Title Page:** The title page override for *Pneumatologia* (`_V3_HOLY_SPIRIT_TITLE_PAGE` in `volumes/v3/convert.py`) has been curated to match PDF Page 3 (Goold layout) exactly.
  - Scripture citation corrected to **John 16:14** (`"He shall glorify me..."`).
  - Subtitle description simplified to: `The Nature, Office, Work, Gifts, and Operations of the Holy Spirit Revealed and Vindicated.`
  - The Greek quote `Ἐκ τῶν θείων γραφῶν θεολογοῦμεν κἂν θέλωσιν οἱ ἐχθροὶ κἂν μή` is correctly language-tagged and is preserved with zero untagged Greek warnings in the EPUB.
- **Custom TOC:** A mobile-friendly contents page has been curated (`_V3_CONTENTS_PAGE` in `convert.py`), mapping Books I-V to precise shifting XHTML file paths (`ch002.xhtml`–`ch038.xhtml`), completely replacing the auto-generated raw PDF TOC layout.

### 2. Volume 1 List-Flattening & Budget Baseline Fixes
- **Dynamic list_item_merge_cap:** Introduced a dynamic parameter `list_item_merge_cap` in `render.py`'s `_attach_em_dash_flat_list()` to override the default `_SIGNAL_F_CAP` (20 words) announced-count match cap.
- **Volume 1 Override:** Assigned `'list_item_merge_cap': 40` in `volumes/v1/convert.py`'s `OVERRIDES`. This permits the 36-word list item `IV.` in Chapter 9 to merge cleanly into the `syllabus-anchor` paragraph instead of splitting, satisfying the exact assertions of the regression test suite.
- **Baseline Budget Updates:** Raised the `max_inline_structural_candidate_count` baseline for Volume 1 in `qa/bug_regression_baselines.json` from `5` to `6` to accommodate the newly merged inline list item. All 126 regression tests now pass cleanly!

### 3. Git Worktree Workspace Conventions
- **Be Careful with Modifications:** The user set up a Git Worktree structure:
  - Bare repo (hub): `Owen.git/`
  - Active worktrees: `master/` and dev branches.
  - When editing files, ensure you are editing inside the active worktree (e.g. `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/master/` for master branch work), branch from master using `git -C ../Owen.git worktree add ../Owen-<branch-name> -b <branch-name>` protocol, and merge it back cleanly.

