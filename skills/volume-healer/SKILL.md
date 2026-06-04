---
name: volume-healer
description: Automates the process of identifying the worst quality volume, branching, pre-auditing, creating a detailed repair plan, executing repairs, verifying results, and reporting quality progression. Use when the user issues #heal worst or #heal [n] commands.
---

# Volume Healer

This skill automates the end-to-end quality healing workflow for a John Owen volume.

## Command Syntax

The skill is triggered by the `#heal` command:

- `#heal worst` (or `#heal` without arguments): Identify the worst volume by Need score, then run the full healing pipeline.
- `#heal [n]`: Run the full healing pipeline for a specific volume `n`.

## Workflow

### 1. Identify Target Volume
- If `#heal worst` is requested:
  - Run the volume state report: `.venv/bin/python3 scripts/report_volume_state.py --all`
  - Read the generated JSON report `qa/reports/volume_state_report.json` to find the volume with the highest `Need` score (the worst quality).
- If `#heal [n]` is requested:
  - Target volume `n` directly.

### 2. Setup Development Branch
- Ensure you are on `master` and pull the latest changes:
  ```bash
  git checkout master
  git pull
  ```
- Create a dedicated development branch for the volume:
  ```bash
  git checkout -b heal-v[n]
  ```

### 3. Run Pre-Audit (Before State)
- Run the full check pipeline for the volume to gather initial baseline metrics:
  ```bash
  .venv/bin/python3 scripts/run_all_checks.py [n]
  ```
- Gather baseline metrics from `volumes/v[n]/bugs_fixes/`:
  - Word coverage and language coverages in `volume_[n]_text_integrity.json`
  - Total and unresolved citations in `volume_[n]_bug_regressions.json` (or scan using `scripts/scan_citations.py --vol [n]`)
  - Suspected OCR anomalies in `volume_[n]_anomalies.json`
  - EPUB packaging errors/warnings in `volume_[n]_audit.json`

### 4. Create Detailed Repair Plan
- Analyze the anomalies, regressions, and unresolved citations.
- Create a detailed repair checklist at `volumes/v[n]/bugs_fixes/volume_[n]_repair_plan.md` listing:
  - Unresolved patristic/classical citations that need mapping.
  - OCR typos or character-splitting anomalies that need correction.
  - False-positive paragraph splits or list layout issues.
  - Any styling or mobile usability adjustments needed.

### 5. Execute Healing & Repairs
- Apply automated fixes and curation:
  - **OCR Spelling corrections**: Add clear typos to the volume-specific overrides in `volumes/v[n]/convert.py` (or add them to the centralized `LATIN_OCR_CORRECTIONS` in `shared.py` if they are general).
  - **Unresolved patristic/classical citations**: Resolve citations by matching they find to `translation_db.py` (`BODY_TRANSLATIONS`) or `patristic_refs.py` (`WORK_MAP`).
  - **Inline lists & split errors**: Adjust list-item caps or add paragraph hooks in `convert.py` overrides to heal split paragraphs.
- Mark completed items in `volume_[n]_repair_plan.md` with `[x]`, and keep track of false positives or items requiring user decision with notes.

### 6. Verify and Post-Audit (After State)
- Rebuild the volume's EPUB:
  ```bash
  .venv/bin/python3 volumes/v[n]/convert.py
  ```
- Run the full checks suite to ensure no regressions and verify bug regression budget:
  ```bash
  .venv/bin/python3 scripts/run_all_checks.py [n]
  ```
- Re-run pytest to verify all test cases pass:
  ```bash
  .venv/bin/python3 -m pytest tests/
  ```

### 7. Generate Progression Report
- Run the overall volume state report to update rankings:
  ```bash
  .venv/bin/python3 scripts/report_volume_state.py --all
  ```
- Compare "Before" vs "After" metrics and present them in a clean comparative markdown table:
  - Need Score
  - Word Coverage %
  - Greek / Hebrew / Latin Coverage %
  - Unresolved Citations Count
  - Total anomalies / splits count
- Present the volume's new position in the ranked collection list.
