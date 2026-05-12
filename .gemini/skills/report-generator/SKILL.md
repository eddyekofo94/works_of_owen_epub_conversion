---
name: report-generator
description: Generates or updates comprehensive reports for Owen volumes. Use when the user issues the #report command (e.g., #report 1, #report all, #report 1 2 3).
---

# Report Generator

This skill automates the generation and updating of reports for the Owen collection volumes.

## Command Syntax

The skill is triggered by the `#report` command followed by volume identifiers:

- `#report [n]`: Generate report for volume `n`.
- `#report [n1] [n2] [n3]`: Generate reports for multiple volumes.
- `#report all`: Generate reports for all 16 volumes.

## Workflow

1.  **Identify Volumes**: Parse the command to determine which volume numbers are requested.
2.  **Run Script**: For each volume `n`, execute the following command:
    ```bash
    .venv/bin/python3 generate_v1_report.py [n]
    ```
    *(Note: Although the script is named `generate_v1_report.py`, it accepts a volume number as an argument.)*
3.  **Validate Output**: Ensure the report is written to `volumes/v[n]/bugs_fixes/VOLUME_[n]_REPORT.md`.
4.  **Summary**: Provide a brief summary of the report status for each volume (e.g., "Volume 1: Updated", "Volume 5: Generated").

## Resource Locations

- **Script**: `generate_v1_report.py`
- **Output Directory**: `volumes/v[n]/bugs_fixes/`
- **Output Filename**: `VOLUME_[n]_REPORT.md` (and associated `.json` and audit files).
