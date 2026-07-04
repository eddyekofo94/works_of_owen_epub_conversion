---
name: heal
description: Heal exactly one John Owen Works EPUB volume, scoped to volumes 1-16, toward PRISTINE Apple Books-compliant EPUB3 output. Use for $heal, #heal, heal worst, heal volume N, or requests to reduce an Owen volume's Need score through extraction, rendering, anomaly, whitelist, citation, EPUB, and regression fixes without auto-merging to master.
---

# Heal

## Overview

Use this project-local skill only inside the John Owen Works repository. Do not install, edit, or depend on `~/.codex/skills/heal`; this repo owns its own `skills/heal` definition.

Heal one Owen volume at a time. The only valid targets are Owen volumes `1` through `16`; the Hebrews commentary and unrelated EPUB projects are out of scope unless the user explicitly changes the scope in a new request.

## Success Target

Drive the selected volume to one of these outcomes:

- **PRISTINE-ready:** Need score below `20.0`, no EPUB audit errors, acceptable text-integrity coverage, no unhandled anomaly class that can be safely fixed, current bug-regression budget respected, and polished Apple Books-compliant EPUB3 output.
- **Blocked with evidence:** further reduction needs source-image judgment, user validation, a larger structural decision, or would require unsafe textual correction. Document exact blockers with page/chapter/report evidence.

Do not stop merely because critical errors are gone. Continue reducing warnings, anomalies, citation gaps, whitelist debt, and polish issues until the target is PRISTINE-ready, blocked with evidence, or the session is near the context floor. For long autonomous healing runs, continue until roughly 20% context remains, then leave a precise checkpoint report.

## Guardrails

- Never batch-heal volumes. `heal worst` may scan all volumes to choose the target, but repair and verification stay on one selected volume.
- Use standard Git branches only. Do not use worktrees and do not merge to `master`.
- Start from a clean, current branch when safe: inspect `git status`, preserve unrelated user changes, then create or reuse a local branch named `heal-vN` or a conflict-free variant.
- Use the local environment: `./owen vN`, `.venv/bin/python3`, and repository scripts only.
- Keep the repository root pristine. Put temporary diagnostics under `scratch/`, persistent helpers under `scripts/`, and generated verification reports under `volumes/vN/reports/`.
- Do not modernize 17th-century spelling, punctuation, or historical hyphenation. Apply text replacements only for clear OCR/extraction defects.
- If whitelisting anything, maintain both `volumes/vN/bugs_fixes/volume_N_whitelist.json` and `volume_N_whitelist.md`, and explain all whitelisted items in the final report.
- Keep volume-specific content in `volumes/vN/convert.py` `OVERRIDES`. Do not place volume-specific title pages, OCR lists, or hooks in shared modules.
- Preserve Apple Books EPUB3 polish: mobile-safe CSS, `@font-face` weight/style integrity, CDATA-wrapped CSS, Greek/Hebrew language spans, Hebrew RTL isolation, tappable footnotes, valid NAV/NCX/landmarks, and embedded fonts.

## Commands

- `$heal worst`, `#heal worst`, `$heal`, or `#heal`: choose the Owen volume with the highest current Need score.
- `$heal N`, `#heal N`, or `heal volume N`: heal volume `N`, where `N` is `1` through `16`.

## Workflow

1. Read `GEMINI.md` before changing converter behavior or project documentation. For list or blockquote fixes, also read `bugs_fixes/owenian-structure-rules.md` and its focused companion notes.
2. Identify the target:
   - For `worst`, run `.venv/bin/python3 scripts/report_volume_state.py --all --no-readme`, then read `qa/reports/volume_state_report.json` and choose the highest Need score.
   - For an explicit number, validate it is `1` through `16`.
3. Establish the branch safely:
   - Inspect `git status --short --branch`.
   - If unrelated dirty changes exist, do not overwrite them. Continue only if edits can be isolated safely.
   - Use a standard local branch such as `heal-vN`; never auto-merge to `master`.
4. Capture the baseline for only the target volume:
   - Prefer `./owen vN` for rebuilding when `volumes/vN/convert.py` exists.
   - If a per-volume script is missing and healing requires one, create it from the v1 template and populate `OVERRIDES`.
   - Run `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Run or inspect `.venv/bin/python3 scripts/generate_need_reduction_plan.py N`.
5. Plan from current reports:
   - `volumes/vN/bugs_fixes/volume_N_audit.json`
   - `volumes/vN/bugs_fixes/volume_N_text_integrity.json`
   - `volumes/vN/bugs_fixes/volume_N_bug_regressions.json`
   - `volumes/vN/bugs_fixes/volume_N_anomalies.json`
   - `volumes/vN/plans/vN_need_reduction_plan.md`
6. Repair in priority order:
   - EPUB validity, package/navigation, and Apple Books display defects.
   - Text-integrity losses, paragraph splits, repeated windows, inline structural markers, and list/blockquote structure.
   - Clear OCR defects via volume-local `text_replacements` or narrowly justified shared corrections.
   - Unresolved patristic/classical citations through `translation_db.py` or `scripts/patristic_refs.py` only when work identity is known.
   - Whitelist only confirmed false positives or acceptable historical/source forms.
7. Verify after each meaningful repair:
   - Fast render: `./owen vN --render-only` when extraction is unchanged.
   - Full target checks: `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Focused pytest for changed behavior, usually `.venv/bin/python3 -m pytest tests/test_bug_regressions.py` or the smallest relevant test file.
8. Finish with a target-scoped verification bundle:
   - Re-run `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Re-run `.venv/bin/python3 scripts/report_volume_state.py --volumes N --no-readme`.
   - Locate the latest detailed report under `volumes/vN/reports/` or generate a session report there.

## Final Report

Summarize:

- target volume and branch
- before/after Need score and main changed metrics
- files changed
- validation commands and pass/fail status
- absolute path to the detailed verification/audit report
- every whitelist addition or removal, with rationale
- remaining blockers or review-needed items

Do not call the volume healed if it remains above the PRISTINE target without clearly stating the blocker.
