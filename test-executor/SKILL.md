---
name: test-executor
description: Executes comprehensive audits or known-bug regression reports for Owen volumes. Use when the user issues #test audit or #test bug commands (e.g., #test audit 1, #test bug 2, #test audit all).
---

# Test Executor

This skill automates the auditing of Owen collection volumes.

## Command Syntax

The skill is triggered by the `#test` command followed by a mode and volume identifiers:

- `#test audit [n]`: Run EPUB and text-integrity audits for volume `n`.
- `#test audit [n1] [n2] [n3]`: Run audits for multiple volumes.
- `#test audit all`: Run audits for all 16 volumes.
- `#test bug [n]`: Run the known-bug regression report for volume `n`.
- `#test bug [n1] [n2] [n3]`: Run bug-regression reports for multiple volumes.
- `#test bug all`: Run bug-regression reports for all 16 volumes.

If the user says `test audit` or `test bug` without the leading `#`, treat it the same way when the intent is clear.

## Workflow

1.  **Identify Mode and Volumes**: Parse the command to determine whether the user requested `audit` or `bug`, then parse the requested volume numbers.
2.  **Execute Audit Pipeline**: For each volume `n` requested by `#test audit`, perform the following:
    -   **Regenerate EPUB**: `.venv/bin/python3 converter.py [n]`
    -   **EPUB Audit**: `.venv/bin/python3 scripts/audit_epub.py volumes/v[n]/output/volume_[n].epub`
    -   **Text Integrity Audit**: `.venv/bin/python3 scripts/audit_text_integrity.py [n]`
3.  **Execute Bug Pipeline**: For each volume `n` requested by `#test bug`, perform the following:
    -   **Bug Regression Report**: `.venv/bin/python3 scripts/audit_bug_regressions.py [n]`
    -   This expects current `volume_[n]_audit.json` and `volume_[n]_text_integrity.json` reports to exist. If they are missing or stale, run `#test audit [n]` first.
4.  **Provide Summary**: Extract key metrics from the relevant results:
    -   **EPUB Status**: Errors, Warnings, Footnote Count.
    -   **Integrity Status**: Word Coverage, Top/Bottom clipping, Structural splits.
    -   **Bug Regression Status**: Known recurring bug classes over budget, especially paragraph splits, inline structural markers, untagged Greek/Hebrew, and repeated word windows.
5.  **Reference Reports**: Remind the user that detailed reports are available in `volumes/v[n]/bugs_fixes/`.

## Resource Locations

- **EPUB Audit**: `scripts/audit_epub.py`
- **Integrity Audit**: `scripts/audit_text_integrity.py`
- **Bug Regression Audit**: `scripts/audit_bug_regressions.py`
- **Output Directory**: `volumes/v[n]/bugs_fixes/` (Look for `volume_[n]_audit.md`, `volume_[n]_text_integrity.md`, and `volume_[n]_bug_regressions.md`).
