# John Owen Works EPUB Conversion

This project converts the 16-volume Works of John Owen from AGES PDFs into polished EPUB3 files.

The active goal is to stabilize the Owen Works pipeline. The Hebrews commentary is not part of the current work.

Default workflow is one volume at a time. Do not run batch conversion or batch audits unless explicitly requested.

## Quick Start

```bash
# Process one volume
.venv/bin/python3 converter.py 1

# Process all 16 volumes
.venv/bin/python3 converter.py

# Smoke test volume 1
.venv/bin/python3 converter.py --test
```

Use the all-volumes command only when a batch run has been explicitly requested.

Generated EPUBs are written to:

```text
volumes/vN/output/volume_N.epub
```

## What the Converter Does

`converter.py` uses PyMuPDF and PyMuPDF4LLM to extract source PDFs, then builds EPUB3 output with:

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
├── converter.py
├── shared.py
├── pdfs/
├── covers/
├── portraits/
├── special_sources/
├── volumes/v1-v16/
│   ├── input/
│   ├── intermediate/
│   ├── output/
│   └── bugs_fixes/
└── docs/archive/
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

Older notes may mention `pdfminer.six` or Poppler-based pipelines. Those are historical or comparison paths, not the current primary converter.

## Validation Rule

Do not mark issues as fully fixed in per-volume bug logs until the user has validated the output. Use `IMPLEMENTED (AWAITING VALIDATION)` for completed but unapproved work.
