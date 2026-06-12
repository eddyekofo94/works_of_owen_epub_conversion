---
name: pristine-healer
description: Automates the workflow to elevate a John Owen volume to green status (Need score < 20.0). Triggered by #pristine [n] or #pristine.
---

# Pristine Healer Skill

This skill automates the workflow to elevate a John Owen volume to green status (Need score < 20.0, 0 unresolved citations, 0 warnings, 0 regressions, all pytests passing).

## Command Syntax

The skill is triggered by the `#pristine` command:

-   `#pristine [n]`: Elevate volume `n` to `PRISTINE` quality.
-   `#pristine`: Scans the collection, identifies the volume with the worst (highest) quality `Need` score (i.e. the highest score in the report, typically Rank 1, such as Volume 11), and automatically runs the healing workflow on it. Do not pick the one with the lowest Need score among non-pristine volumes.

## Workflow

### Phase 1: Branch Setup & Environment Verification
1.  **Commit Master Changes**: Ensure all active changes on the current branch are committed/stashed. Switch to the `master` branch and run `git pull origin master` to fetch the latest changes.
2.  **Create Pristine Branch**: Check out a new branch named `volume-[n]-pristine` from clean `master` history.
3.  **Initial Audit**: Run `.venv/bin/python3 scripts/run_all_checks.py [n]` to generate initial reports.

### Phase 2: Analysis & Healing
1.  **Analyze Reports**: Inspect the generated files in `volumes/v[n]/bugs_fixes/` to identify errors, warnings, unresolved citations, missing translations, spelling errors, and faulty splits.
2.  **Apply Local & Generic Fixes**:
    -   Add volume-specific OCR corrections and local layout modifications to `text_replacements` or override parameters inside `volumes/v[n]/convert.py`.
    -   Add missing Latin/Greek translations to `scripts/translation_db.py`.
    -   Add unrecognized patristic/classical references to `scripts/patristic_refs.py`.
    -   Correct any Bible reference encoding issues in `scripts/ages_verse_translator.py`.
3.  **Verify Progression**: Rebuild the volume using `.venv/bin/python3 volumes/v[n]/convert.py` and run audits until warnings are resolved.

### Phase 3: Whitelisting (Dual-Format Mandate)
1.  **Generate Agent Whitelist**: Save any verified historical orthography variants (e.g. archaic hyphenations), list sequence jumps, or acceptable paragraph splits into `volumes/v[n]/bugs_fixes/volume_[n]_whitelist.json`.
2.  **Generate Human Whitelist**: Create a companion Markdown file `volumes/v[n]/bugs_fixes/volume_[n]_whitelist.md` explaining each whitelisted item and category.

### Phase 4: Final Validation & Submission
1.  **Full Quality Check**: Run the check suite `.venv/bin/python3 scripts/run_all_checks.py [n]`. Confirm:
    -   0 text anomalies, 0 splits, 0 regressions, 0 errors, and 0 warnings.
    -   Need score is under 20.0 (PRISTINE status).
2.  **Pytest Validation**: Execute the full pytest suite: `.venv/bin/python3 -m pytest`.
3.  **State Reporting**: Run `.venv/bin/python3 scripts/report_volume_state.py --volumes [n]` to update the QA tables and README.md.
4.  **Push Branch**: Stage and commit all changes, and run `git push origin volume-[n]-pristine`.
5.  **Final Report**: Present a concise before-and-after report to the user including the pull request link.

## Worst-Volume Detection (No Arguments)

If `#pristine` is called without a volume number:
1.  Execute `.venv/bin/python3 scripts/report_volume_state.py --no-readme` to obtain the latest collection rankings.
2.  Locate the worst non-PRISTINE volume (the one with the HIGHEST Need score, which is Rank 1 at the top of the report table, such as Volume 11).
    - **CRITICAL WARNING**: Do NOT select the volume closest to entering the PRISTINE tier (the one with the lowest Need score among non-pristine volumes, like Volume 16). You MUST target the worst quality volume (highest Need score) to lift it.
3.  Launch the `#pristine [worst_volume_number]` workflow on that worst volume (e.g. Volume 11).
