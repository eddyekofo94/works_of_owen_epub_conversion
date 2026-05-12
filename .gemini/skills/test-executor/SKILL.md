---
name: test-executor
description: Executes comprehensive audits (EPUB and Text Integrity) for Owen volumes. Use when the user issues the #test command (e.g., #test 1, #test all, #test 1 2 3).
---

# Test Executor

This skill automates the auditing of Owen collection volumes.

## Command Syntax

The skill is triggered by the `#test` command followed by volume identifiers:

- `#test [n]`: Run audits for volume `n`.
- `#test [n1] [n2] [n3]`: Run audits for multiple volumes.
- `#test all`: Run audits for all 16 volumes.

## Workflow

1.  **Identify Volumes**: Parse the command to determine which volume numbers are requested.
2.  **Execute Pipeline**: For each volume `n`, perform the following:
    -   **Regenerate EPUB**: `.venv/bin/python3 converter.py [n]`
    -   **EPUB Audit**: `.venv/bin/python3 scripts/audit_epub.py volumes/v[n]/output/volume_[n].epub`
    -   **Text Integrity Audit**: `.venv/bin/python3 scripts/audit_text_integrity.py [n]`
3.  **Provide Summary**: Extract key metrics from the audit results:
    -   **EPUB Status**: Errors, Warnings, Footnote Count.
    -   **Integrity Status**: Word Coverage, Top/Bottom clipping, Structural splits.
4.  **Reference Reports**: Remind the user that detailed reports are available in `volumes/v[n]/bugs_fixes/`.

## Resource Locations

- **EPUB Audit**: `scripts/audit_epub.py`
- **Integrity Audit**: `scripts/audit_text_integrity.py`
- **Output Directory**: `volumes/v[n]/bugs_fixes/` (Look for `volume_[n]_audit.md` and `volume_[n]_text_integrity.md`).
