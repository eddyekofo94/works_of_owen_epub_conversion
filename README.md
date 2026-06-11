# John Owen Works EPUB Conversion

This project converts the 16-volume Works of John Owen from AGES PDFs into polished EPUB3 files.

The active goal is to stabilize the Owen Works pipeline. The Hebrews commentary is not part of the current work.

Default workflow is one volume at a time. Do not run batch conversion or batch audits unless explicitly requested.

## Quick Start

```bash
# Preferred full pipeline for volume 1
.venv/bin/python3 volumes/v1/convert.py

# Fast re-render from cached JSON (Stage 2 only, ~3 seconds)
.venv/bin/python3 volumes/v1/convert.py --render-only

# Stage 1 only (re-extract PDF)
.venv/bin/python3 volumes/v1/convert.py --extract-only
```

Generated EPUBs are written to:

```text
volumes/vN/output/volume_N.epub
```

## Build Commands

### Per-volume scripts (preferred)

These load volume-specific `OVERRIDES` (OCR fixes, paragraph hooks, CSS). Currently exists for volumes 1-3.

```bash
# Full pipeline: extract + render
.venv/bin/python3 volumes/v1/convert.py

# Stage 2 only — re-render from cached JSON (fast)
.venv/bin/python3 volumes/v1/convert.py --render-only

# Stage 1 only — re-extract PDF
.venv/bin/python3 volumes/v1/convert.py --extract-only
```

Replace `v1` with `v2` or `v3` for those volumes. Volumes 4-16 do not yet have per-volume scripts.

### Legacy orchestrator (now respects per-volume OVERRIDES)

```bash
# Single volume
.venv/bin/python3 converter.py 3

# Multiple volumes
.venv/bin/python3 converter.py 1 2 5

# All 16 volumes (explicit flag)
.venv/bin/python3 converter.py --all

# Extract all 16 volumes (Stage 1 only)
.venv/bin/python3 converter.py --extract-only

# Render all 16 volumes (Stage 2 only, requires existing JSON intermediates)
.venv/bin/python3 converter.py --render-only

# Full pipeline (both stages) for all 16 volumes
.venv/bin/python3 converter.py

# Volume 1 only
.venv/bin/python3 converter.py --test
```

The legacy orchestrator now dynamically loads per-volume OVERRIDES from
`volumes/vN/convert.py` when they exist, so it behaves identically to the
per-volume scripts for volumes 1-3.

### Stage entry points (direct)

```bash
# Stage 1: PDF → JSON intermediate (single, multiple, or all)
.venv/bin/python3 extract.py 1
.venv/bin/python3 extract.py 1 2 5
.venv/bin/python3 extract.py --all

# Stage 2: JSON → EPUB3 (single, multiple, or all)
.venv/bin/python3 render.py 1
.venv/bin/python3 render.py 1 2 5
.venv/bin/python3 render.py --all
```

These do not load per-volume OVERRIDES. Prefer the per-volume scripts or
legacy orchestrator when volume-specific corrections are needed.

## Test Commands

Tests use the `OWEN_REGRESSION_VOLUMES` environment variable to select which
volumes to test. Default is volume 1.

```bash
# Run all tests (default: volume 1 only)
.venv/bin/python3 -m pytest tests/

# Run all tests for specific volumes
OWEN_REGRESSION_VOLUMES="1 3 5" .venv/bin/python3 -m pytest tests/

# Run all tests for all volumes (requires all EPUBs to exist)
OWEN_REGRESSION_VOLUMES="all" .venv/bin/python3 -m pytest tests/

# Run a single test file
.venv/bin/python3 -m pytest tests/test_bug_regressions.py

# Run a single test function
.venv/bin/python3 -m pytest tests/test_bug_regressions.py::test_i_will_and_i_am_are_not_forced_to_all_caps
```

### Test files

| File | Description | Volume dependency |
|---|---|---|
| `tests/test_bug_regressions.py` | Known bug regression guards (fonts, scripture refs, catechism, structural markers) | `OWEN_REGRESSION_VOLUMES` |
| `tests/test_epub_structure.py` | EPUB structural checks (nav, spine, HTML classes, language tags) | `OWEN_REGRESSION_VOLUMES` |
| `tests/test_text_fidelity.py` | Text extraction fidelity (bracket repair, scripture refs, terminology) | `OWEN_REGRESSION_VOLUMES` |
| `tests/test_footnote_integrity.py` | Footnote endnote linkage, counts, artifact checks | `OWEN_REGRESSION_VOLUMES` |
| `tests/test_golden_pages.py` | Page-level extraction baselines against known-good text | `OWEN_REGRESSION_VOLUMES` |
| `tests/test_structural_standardization.py` | Structural tokens, drop caps, blockquote geometry, scholastic anchors | None (unit tests) |
| `tests/test_config_hardening.py` | Volume config deep-merge logic | None (unit tests) |
| `tests/test_greek_extraction_hardening.py` | Greek font conversion and page detection | None (unit tests) |
| `tests/test_gideon_mapping.py` | Gideon (Hebrew) font character mapping | None (unit tests) |

### Golden page baselines

Golden page tests compare extracted text against hand-verified baselines in
`tests/baselines/`. To generate or update baselines:

```bash
GOLDEN_GENERATE=1 .venv/bin/python3 -m pytest tests/test_golden_pages.py
```

This writes/overwrites baseline `.txt` files in `tests/baselines/`. Commit
them after verifying correctness.

### Running tests via slash commands

The `test-executor` skill provides `#test` slash commands for agent workflows.
See the [Slash Commands](#slash-commands-test-executor-skill) section below.

## Audit Commands

Audit scripts analyze generated EPUBs for structural issues, text faithfulness,
and known bug classes. They write both JSON and Markdown reports to
`volumes/vN/bugs_fixes/`.

```bash
# EPUB structural audit (errors, warnings, footnote counts, navigation)
.venv/bin/python3 scripts/audit_epub.py volumes/v3/output/volume_3.epub

# Text integrity audit (single, multiple, or all)
.venv/bin/python3 scripts/audit_text_integrity.py 3
.venv/bin/python3 scripts/audit_text_integrity.py 1 2 5
.venv/bin/python3 scripts/audit_text_integrity.py --all

# Bug regression report (single, multiple, or all)
.venv/bin/python3 scripts/audit_bug_regressions.py 3
.venv/bin/python3 scripts/audit_bug_regressions.py 1 2 5
.venv/bin/python3 scripts/audit_bug_regressions.py --all

# Bug regression with strict exit code
.venv/bin/python3 scripts/audit_bug_regressions.py 3 --strict
```

### Audit output files

```text
volumes/v3/bugs_fixes/
├── volume_3_audit.md                 # EPUB audit report
├── volume_3_audit.json               # Machine-readable audit data
├── volume_3_text_integrity.md        # Text integrity report
├── volume_3_text_integrity.json      # Machine-readable integrity data
├── volume_3_bug_regressions.md       # Bug regression report
└── volume_3_bug_regressions.json     # Machine-readable regression data
```

## Full Check Pipeline

Runs converter → EPUB audit → text integrity audit → bug regression report →
pytest tests in a single command with a unified summary.

```bash
# All 16 volumes (full pipeline — may take hours)
.venv/bin/python3 scripts/run_all_checks.py
.venv/bin/python3 scripts/run_all_checks.py --all

# Single volume
.venv/bin/python3 scripts/run_all_checks.py 3

# Multiple volumes
.venv/bin/python3 scripts/run_all_checks.py 1 2 5

# Skip converter, audit existing EPUBs only (fast re-check)
.venv/bin/python3 scripts/run_all_checks.py 3 --no-rebuild

# Help
.venv/bin/python3 scripts/run_all_checks.py --help
```

## Volume State Report

A single command to inventory all 16 volumes, read existing QA reports (audit,
text integrity, bug regressions), score each volume by severity, and produce a
ranked report from worst to best. Run this when you want to know which volume
needs attention most urgently.

Reports are written to:
- `qa/reports/volume_state_report.md` — human-readable per-volume detail
- `qa/reports/volume_state_report.json` — machine-readable for agent workflows

The `--audit-missing` flag runs audit scripts for any volume that has no reports
yet (handy for backfilling new volumes). The README Per-Volume Status table is
updated automatically on each run (use `--no-readme` to skip).

```bash
# Quick inventory (reads existing data, no re-generation)
.venv/bin/python3 scripts/report_volume_state.py
.venv/bin/python3 scripts/report_volume_state.py --all

# Run audits for volumes that have no QA reports yet
.venv/bin/python3 scripts/report_volume_state.py --audit-missing

# Skip README update
.venv/bin/python3 scripts/report_volume_state.py --no-readme
```
## Academic Translation & Citation Audit

This project implements a proactive, collection-wide **Academic Translation & Citation Audit** to locate and annotate classical Latin, Greek, and Hebrew prose or verse quotes. This process ensures that the EPUB outputs are of the highest academic standard, complete with interactive pop-up translation footnotes in standard rendering engines.

### Collection-Wide Sweep & Manifest

The `scripts/generate_untranslated_manifest.py` script performs a thorough sweep across all 16 volumes, scanning paragraphs and footnotes using optimized language-ratio density algorithms to flag unreferenced or untranslated foreign-language blocks:

```bash
# Execute the collection-wide translation audit
.venv/bin/python3 scripts/generate_untranslated_manifest.py
```

This script generates:
- `qa/untranslated_prose_manifest.json`: A unified machine-readable JSON log of all unannotated prose blocks.
- `qa/untranslated_prose_report.md`: A detailed, human-readable volume-by-volume markdown audit log containing exact context strings.
- `qa/dashboard.html`: A premium HSL-color-coded glassmorphism leaderboard dashboard showing coverage ranking from best to worst.

### Verification & Regression Budgets

To prevent regressions, the ratio-based prose translation checks are integrated directly into the pytest suite under `tests/test_unresolved_citations.py`. Every volume is constrained by a strict budget of allowed untranslated footnotes and unresolved citations:

```bash
# Run unresolved citation and untranslated prose tests
.venv/bin/python3 -m pytest tests/test_unresolved_citations.py
```

Under this model, **Volume 12 (The Gospel Defended)** serves as the pristine **100% complete and validated Golden Baseline** (0 untranslated footnotes or body paragraphs remaining).

### HTML-Aware Signature Splitter

To split prefaces, dedications, or chapters at exact author signatures or valedictions without breaking formatting, the rendering pipeline implements an **HTML-Aware Signature Splitter** (`map_plain_to_html_index` in `render.py`).

Prior naive splitters stripped XML/HTML tags and split on plain-text character offsets, which resulted in truncated tags, missing footnote anchors, or malformed inline Greek or Hebrew spans.

The new engine:
1. Translates the plaintext signature split offset to the exact corresponding byte index in the original markup-heavy HTML stream.
2. Resolves HTML entities, inline tag bounds, and nested elements transparently.
3. Automatically balances tags across split pages to guarantee 100% valid XHTML packaging while preserving all patristic citations, scripture references, and language spans completely intact.

## Per-Volume Script Status

| Volume | convert.py | OVERRIDES | QA Level | Notes |
|---|---|---|---|---|
| 1 | v1 | Populated | FULL | Cov 99.93 Greek 99.73 Heb 100.00 Lat 99.80 Quotes 19 |
| 2 | v2 | Populated | FULL | Cov 99.49 Greek 99.54 Heb 100.00 Lat 99.50 Unres 2 Quotes 43 |
| 3 | v3 | Populated | FULL | Cov 99.97 Greek 99.87 Heb 100.00 Lat 99.95 Quotes 30 |
| 4 | v4 | Populated | FULL | Cov 99.85 Greek 98.99 Heb 100.00 Lat 99.78 Unres 7 Quotes 27 |
| 5 | v5 | Populated | PRISTINE | Cov 99.98 Greek 100.00 Heb 100.00 Lat 99.73 |
| 6 | v6 | Populated | FULL | Cov 99.26 Greek 100.00 Heb 100.00 Lat 99.01 Quotes 31 |
| 7 | v7 | Populated | FULL | Cov 99.71 Greek 99.69 Heb 100.00 Lat 99.62 Unres 2 Quotes 13 |
| 8 | v8 | Populated | FULL | Cov 99.65 Greek 100.00 Heb 100.00 Lat ? Unres 10 Quotes 26 |
| 9 | v9 | Empty | FULL | Cov 99.61 Greek 100.00 Heb 100.00 Lat ? Quotes 65 |
| 10 | v10 | Populated | FULL | Cov 99.47 Greek 99.75 Heb 100.00 Lat ? Unres 4 Quotes 77 |
| 11 | v11 | Populated | FULL | Cov 97.62 Greek 99.31 Heb 100.00 Lat 98.64 Unres 4 Quotes 99 |
| 12 | v12 | Populated | FULL | Cov 99.91 Greek 99.80 Heb 99.55 Lat 99.80 Quotes 114 |
| 13 | v13 | Populated | FULL | Cov 90.14 Greek 95.21 Heb 100.00 Lat 90.40 Quotes 70 |
| 14 | v14 | Populated | FULL | Cov 98.45 Greek 99.17 Heb 100.00 Lat 98.83 Unres 5 Quotes 30 |
| 15 | v15 | Populated | PRISTINE | Cov 99.94 Greek 100.00 Heb 100.00 Lat 99.68 |
| 16 | v16 | Populated | FULL | Cov 99.94 Greek 100.00 Heb 100.00 Lat 99.94 Unres 1 Quotes 56 |

## Hebrews Commentary Script Status

| Volume | convert.py | OVERRIDES | QA Level | Notes |
|---|---|---|---|---|
| h1 | h1 | Populated | FULL | Cov 99.99 Greek 100.00 Heb 100.00 Unres 34 |
| h2 | h2 | Empty | NONE | No QA reports |
| h3 | h3 | Empty | NONE | No QA reports |
| h4 | h4 | Empty | NONE | No QA reports |
| h5 | h5 | Empty | NONE | No QA reports |
| h6 | h6 | Empty | NONE | No QA reports |
| h7 | h7 | Populated | NONE | No QA reports |

## Agent-Driven Skills & Slash Commands

For agent-driven workflows, three packaged skills are available to automate testing, report generation, and volume healing.

### 1. Test Executor Skill (`test-executor.skill`)
Provides `#test` commands to execute audits, bug-regression reports, and pytest suites.

*   `#test audit [n...]` — Rebuilds EPUB and runs EPUB and text-integrity audits.
    *   `#test audit 1` (volume 1)
    *   `#test audit 1 2 5` (multiple)
    *   `#test audit all` (all 16 volumes)
*   `#test bug [n...]` — Runs the known-bug regression report against existing audit data.
    *   `#test bug 3`
    *   `#test bug all`
*   `#test all [n...]` — Runs the full check pipeline (converter → audits → bug regressions → pytest).
    *   `#test all 12`
    *   `#test all`
*   `#test report [n...]` — Gathers QA state reports, updates README table and state files.
    *   `#test report 1 2`
    *   `#test report` (all 16 volumes)

### 2. Report Generator Skill (`report-generator.skill`)
Provides `#report` commands to generate or update volume-specific markdown and JSON reports.

*   `#report [n...]` — Generates reports at `volumes/v[n]/bugs_fixes/VOLUME_[n]_REPORT.md`.
    *   `#report 1`
    *   `#report 1 2 5`
    *   `#report all` (all 16 volumes)

### 3. Volume Healer Skill (`volume-healer.skill`)
Provides `#heal` commands to automatically heal bugs, resolve citations, correct spelling errors, and verify the progression.

*   `#heal worst` — Scans rankings, checks out a new branch (`heal-v[n]`), runs pre-audit, plans the repair, executes automated fixes, verifies via tests, and reports before-and-after progression.
*   `#heal [n]` — Runs the healing pipeline for a specific volume `n`.

## What the Converter Does

The active converter uses `extract.py` and `render.py` to extract source PDFs,
repair text, then build EPUB3 output with:

- AGES header/footer removal
- paragraph healing across page boundaries
- ghost text de-duplication
- Greek Koine font conversion to Unicode
- Hebrew Gideon font conversion to Unicode
- Greek/Hebrew language tagging
- footnote extraction and endnote generation
- cover, frontispiece, title page, NAV, NCX, landmarks
- embedded biblical-language fonts
- Apple Books specified-font support

Shared metadata, CSS, font configuration, and Greek/Hebrew maps live in `shared.py`.

## Repository Layout

```text
Owen/
├── converter.py                # Legacy orchestrator (now respects per-volume OVERRIDES)
├── extract.py                  # Stage 1: PDF → JSON intermediate
├── render.py                   # Stage 2: JSON → EPUB3
├── shared.py                   # Metadata, CSS, fonts, Greek/Hebrew converters
├── scripts/
│   ├── run_all_checks.py       # Full pipeline: converter → audits → tests
│   ├── audit_epub.py           # EPUB structural audit
│   ├── audit_text_integrity.py # Text faithfulness audit
│   ├── audit_bug_regressions.py # Known bug regression report
│   └── report_volume_state.py  # Ranked QA state report
├── tests/
│   ├── test_bug_regressions.py
│   ├── test_epub_structure.py
│   ├── test_text_fidelity.py
│   ├── test_footnote_integrity.py
│   ├── test_golden_pages.py
│   ├── test_structural_standardization.py
│   ├── test_config_hardening.py
│   ├── test_greek_extraction_hardening.py
│   └── test_gideon_mapping.py
├── test-executor/
│   └── SKILL.md                # #test slash command definitions
├── qa/
│   ├── bug_regression_baselines.json
│   └── golden_pages.json
├── pdfs/                       # Source AGES PDFs
├── covers/                     # Cover images (v1.png-v16.png)
├── portraits/                  # Frontispiece images
├── special_sources/legacy/     # Archived CCEL XML zips for v5 and v10 (not used)
├── fonts/ -> ../../fonts       # Shared font repository symlink
└── volumes/v1-v16/
    ├── convert.py              # Per-volume script (v1-v3 exist)
    ├── input/                  # PDF symlink (owen-vN.pdf)
    ├── intermediate/           # volume_N.json (Stage 1) + volume_N.thml.xml
    ├── output/                 # volume_N.epub (generated)
    └── bugs_fixes/             # Audit and regression reports
```

## Documentation

- `AGENTS.md`: agent-facing instructions
- `GEMINI.md`: mandatory project protocols
- `PLAN.md`: active roadmap and QA plan
- `ENGINEERING_LOG.md`: technical post-mortems
- `docs/archive/`: historical plans and old session summaries

## Dependencies

The current converter expects the project virtual environment.

```bash
.venv/bin/pip install ebooklib pymupdf pymupdf4llm
```

Older notes may mention `pdfminer.six` or Poppler-based pipelines. Those are
historical or comparison paths, not the current primary converter.

## Validation Rule

Do not mark issues as fully fixed in per-volume bug logs until the user has
validated the output. Use `IMPLEMENTED (AWAITING VALIDATION)` for completed
but unapproved work.
