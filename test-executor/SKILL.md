---
name: test-executor
description: Executes comprehensive audits, known-bug regression reports, or the full test suite for Owen volumes. Use when the user issues #test audit, #test bug, or #test all commands (e.g., #test audit 1, #test bug 2, #test all, #test audit all).
---

# Test Executor

This skill automates the auditing and testing of Owen collection volumes.

## Command Syntax

The skill is triggered by the `#test` command followed by a mode and volume identifiers:

- `#test audit [n]`: Run EPUB and text-integrity audits for volume `n`.
- `#test audit [n1] [n2] [n3]`: Run audits for multiple volumes.
- `#test audit all`: Run audits for all 16 volumes.
- `#test bug [n]`: Run the known-bug regression report for volume `n`.
- `#test bug [n1] [n2] [n3]`: Run bug-regression reports for multiple volumes.
- `#test bug all`: Run bug-regression reports for all 16 volumes.
- `#test all [n]`: Run the full check pipeline for volume `n` (converter, EPUB audit, text integrity, bug regressions, and pytest test suite).
- `#test all [n1] [n2] [n3]`: Run full checks for multiple volumes.
- `#test all`: Run full checks for all 16 volumes.
- `#test report [n]`: Generate ranked QA state report for volume `n` (empty = all 16).
- `#test report [n1] [n2] [n3]`: Generate QA state report for multiple volumes.
- `#test report`: Generate QA state report for all 16 volumes.

If the user says `test audit`, `test bug`, or `test all` without the leading `#`, treat it the same way when the intent is clear.

## Workflow

1.  **Identify Mode and Volumes**: Parse the command to determine whether the user requested `audit`, `bug`, or `all`, then parse the requested volume numbers.
2.  **Execute Audit Pipeline**: For each volume `n` requested by `#test audit`, perform the following:
    -   **Regenerate EPUB**: `.venv/bin/python3 converter.py [n]`
    -   **EPUB Audit**: `.venv/bin/python3 scripts/audit_epub.py volumes/v[n]/output/volume_[n].epub`
    -   **Text Integrity Audit**: `.venv/bin/python3 scripts/audit_text_integrity.py [n]`
3.  **Execute Bug Pipeline**: For each volume `n` requested by `#test bug`, perform the following:
    -   **Bug Regression Report**: `.venv/bin/python3 scripts/audit_bug_regressions.py [n]`
    -   This expects current `volume_[n]_audit.json` and `volume_[n]_text_integrity.json` reports to exist. If they are missing or stale, run `#test audit [n]` first.
4.  **Execute Full Pipeline**: For `#test all`, use the single-command orchestrator:
    -   **Run all checks**: `.venv/bin/python3 scripts/run_all_checks.py [n...]`
    -   This runs converter → EPUB audit → text integrity → bug regressions → pytest tests for each requested volume, then prints a unified summary table.
    -   Use `--no-rebuild` to skip converter and audit existing EPUBs: `.venv/bin/python3 scripts/run_all_checks.py [n...] --no-rebuild`
5. **Execute Report Pipeline**: For `#test report`, run:
    -   `.venv/bin/python3 scripts/report_volume_state.py` (all 16 volumes)
    -   With `--volumes` flag if specific volumes given: `.venv/bin/python3 scripts/report_volume_state.py --volumes 1 2 5`
    -   Writes report to `qa/reports/volume_state_report.md` and `.json`
    -   Updates Per-Volume Script Status table in README.md
6. **Provide Summary**: Extract key metrics from the relevant results:
    -   **EPUB Status**: Errors, Warnings, Footnote Count.
    -   **Integrity Status**: Word Coverage, Top/Bottom clipping, Structural splits.
    -   **Bug Regression Status**: Known recurring bug classes over budget, especially paragraph splits, inline structural markers, untagged Greek/Hebrew, and repeated word windows.
    -   **Pytest Status**: Pass/fail counts and duration (included for `#test all`).
    -   **Report Status**: Score, rank, and QA level for each volume (included for `#test report`).
7.  **Reference Reports**: Remind the user that detailed reports are available in `volumes/v[n]/bugs_fixes/` and `qa/reports/`.

## Resource Locations

- **Full Check Orchestrator**: `scripts/run_all_checks.py`
- **EPUB Audit**: `scripts/audit_epub.py`
- **Integrity Audit**: `scripts/audit_text_integrity.py`
- **Bug Regression Audit**: `scripts/audit_bug_regressions.py`
- **Volume State Report**: `scripts/report_volume_state.py`
- **Output Directory**: `volumes/v[n]/bugs_fixes/` (Look for `volume_[n]_audit.md`, `volume_[n]_text_integrity.md`, and `volume_[n]_bug_regressions.md`).
- **Report Output Directory**: `qa/reports/` (Look for `volume_state_report.md` and `volume_state_report.json`).
