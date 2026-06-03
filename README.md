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

## Per-Volume Script Status

| Volume | convert.py | OVERRIDES | QA Level | Notes |
|---|---|---|---|---|
| 1 | v1 | Populated | FULL | Cov 99.68 Greek 99.87 Heb 100.00 |
| 2 | v2 | Populated | FULL | Cov 99.68 Greek 99.77 Heb 100.00 |
| 3 | v3 | Populated | FULL | Cov 98.51 Greek 99.36 Heb 94.54 |
| 4 | v4 | Populated | FULL | Cov 99.67 Greek 99.71 Heb 100.00 |
| 5 | v5 | Populated | FULL | Cov 99.69 Greek 99.73 Heb 99.19 |
| 6 | v6 | Populated | FULL | Cov 99.54 Greek 100.00 Heb 100.00 |
| 7 | v7 | Populated | FULL | Cov 99.68 Greek 100.00 Heb 100.00 |
| 8 | v8 | Populated | FULL | Cov 99.65 Greek 100.00 Heb 100.00 |
| 9 | v9 | Empty | FULL | Cov 99.61 Greek 100.00 Heb 100.00 |
| 10 | v10 | Populated | FULL | Cov 99.47 Greek 99.75 Heb 100.00 |
| 11 | v11 | Populated | FULL | Cov 97.63 Greek 99.70 Heb 100.00 |
| 12 | v12 | Populated | FULL | Cov 99.58 Greek 100.00 Heb 99.55 |
| 13 | v13 | Populated | FULL | Cov 99.62 Greek 99.22 Heb 100.00 |
| 14 | v14 | Populated | FULL | Cov 99.69 Greek 100.00 Heb 100.00 |
| 15 | v15 | Populated | FULL | Cov 99.67 Greek 100.00 Heb 100.00 |
| 16 | v16 | Populated | FULL | Cov 99.59 Greek 99.30 Heb 99.01 |

## Slash Commands (test-executor Skill)

For agent-driven workflows, the `test-executor` skill in `test-executor/SKILL.md`
provides `#test` slash commands:

### `#test audit [n...]`

Regenerates EPUB and runs EPUB audit + text integrity audit.

```text
#test audit 1        → audit volume 1
#test audit 1 2 5    → audit volumes 1, 2, 5
#test audit all      → audit all 16 volumes
```

### `#test bug [n...]`

Runs the known-bug regression report against existing audit data.

```text
#test bug 1          → bug regression for volume 1
#test bug 1 2 5      → bug regressions for volumes 1, 2, 5
#test bug all        → bug regressions for all 16 volumes
```

### `#test all [n...]`

Runs the full check pipeline (converter → audits → bug regressions → pytest).

```text
#test all            → full pipeline for all 16 volumes
#test all 3          → full pipeline for volume 3
#test all 1 2 5      → full pipeline for volumes 1, 2, 5
```

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
