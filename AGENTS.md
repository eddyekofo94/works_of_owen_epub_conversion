# John Owen Works — Agent Instructions

This repository is currently focused on the 16-volume Owen Works conversion. The Hebrews commentary is intentionally out of scope until the Owen volumes are stable and validated.

## Active Converter

`converter.py` is the active EPUB3 pipeline.

```bash
# Process a single Owen volume
.venv/bin/python3 converter.py 3

# Process all 16 Owen volumes
.venv/bin/python3 converter.py

# Quick smoke run on volume 1
.venv/bin/python3 converter.py --test
```

Current outputs:

- Owen Works: `volumes/vN/output/volume_N.epub`
- Intermediates: `volumes/vN/intermediate/volume_N.thml.xml`

The `--hebrews` CLI flag exists, but the Hebrews pipeline is not implemented in the current checkout.

## Mandatory Protocols

Read `GEMINI.md` before changing converter behavior or project documentation. In particular:

- Do not mark issues as "Finished", "Fixed", or "Done" in `BUGS_AND_FIXES.md` unless the user explicitly validates the result.
- Use `IMPLEMENTED (AWAITING VALIDATION)` for work that has been coded but not user-approved.
- Complex issues, especially Issue 40 and later, need a post-mortem in `ENGINEERING_LOG.md`.
- Preserve the holistic paragraph-healing behavior in `reconstruct_paragraphs()` and `get_pages_text()`.

## Project Shape

```text
Owen/
├── README.md                    # Human overview and quick start
├── AGENTS.md                    # Agent-facing operating instructions
├── GEMINI.md                    # Non-negotiable project mandates
├── PLAN.md                      # Active roadmap and QA plan
├── ENGINEERING_LOG.md           # Technical post-mortems
├── converter.py                 # Active PyMuPDF/PyMuPDF4LLM EPUB3 converter
├── shared.py                    # Metadata, CSS, fonts, Greek/Hebrew converters
├── docs/archive/                # Historical plans and session summaries
├── covers/                      # v1.png-v16.png
├── fonts -> ../../fonts         # Shared font repository symlink
├── pdfs/                        # Source AGES PDFs
├── portraits/                   # Frontispiece images
├── special_sources/             # CCEL XML references for volumes 5 and 10
└── volumes/v1-v16/
    ├── input/                   # PDF symlink
    ├── intermediate/            # ThML XML
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

## Source Rules

Volumes 1-16 currently use the AGES PDF path in `converter.py`. `shared.py` records CCEL XML sources for volumes 5 and 10, but the current live `process_owen_volume()` still opens `volumes/vN/input/owen-vN.pdf` for every volume.

Do not remove the CCEL XML files; they remain useful comparison sources and may become preferred source text later.

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

For documentation changes:

1. Keep root docs short and current.
2. Move historical notes to `docs/archive/` instead of deleting them.
3. Avoid duplicating the same roadmap in multiple files.
