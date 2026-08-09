---
name: heal
description: Heal exactly one John Owen Works EPUB volume, scoped to volumes 1-16, toward a strict Need score below 1.0 and PRISTINE Apple Books-compliant EPUB3 output ready for human by-eye cleanup. Use for $heal, #heal, heal worst, heal volume N, or requests to clean up a volume, reduce Need score, prepare a volume for Apple Books review, or make an Owen EPUB ready through extraction, rendering, anomaly, whitelist, citation, EPUB, visual-review, and regression fixes without auto-merging to master.
---

# Heal

## Overview

Use this project-local skill only inside the John Owen Works repository. Do not install, edit, or depend on `~/.codex/skills/heal`; this repo owns its own `skills/heal` definition.

Heal one Owen volume at a time. The only valid targets are Owen volumes `1` through `16`; the Hebrews commentary and unrelated EPUB projects are out of scope unless the user explicitly changes the scope in a new request.

## Success Target

Drive the selected volume to one of these outcomes:

- **Strict ready for by-eye review:** Need score is strictly below `1.0`, `.venv/bin/python3 scripts/audit_heal_readiness.py N --strict` passes, EPUB audit has `0` errors and `0` warnings, text-integrity warnings are eliminated or fully explained without suppressing real defects, anomaly and unmatched-quote reports are clean, current bug-regression budgets are respected, generated-file state is clean, Apple Books EPUB3 output is polished, and a by-eye review packet is ready for the user.
- **Blocked with evidence:** Need `<1.0` is not safely achievable in the current run because further reduction needs source-image judgment, user validation, a larger structural decision, or would require unsafe textual correction. Document exact blockers with page/chapter/report evidence and the remaining score components.

Treat Need `<20.0` as only an intermediate green milestone, never as completion. Do not stop merely because critical errors are gone, the volume is `FULL`, or the score is below `20.0`. Continue reducing warnings, anomalies, citation gaps, Latin tagging/translation gaps, modern-note debt, whitelist debt, duplicate generated files, and polish issues until Need is `<1.0`, the target is blocked with evidence, or the session is near the context floor. For long autonomous healing runs, continue until roughly 20% context remains, then leave a precise checkpoint report.

## Guardrails

- Never batch-heal volumes. `heal worst` may scan all volumes to choose the target, but repair and verification stay on one selected volume.
- Exception: corpus-wide shared-data passes — `scripts/translation_db.py` entries, Latin lexicon/tagging classification, `scripts/patristic_refs.py` citation data, and whitelist categories — may be prepared across all volumes when the user explicitly requests a batch sweep. Structural/rendering repairs and final verification remain one volume at a time.
- Use standard Git branches only. Do not use worktrees and do not merge to `master`.
- Start every new heal run from the latest clean `master`: inspect `git status`, stop if the worktree is dirty, switch to `master`, fast-forward from `origin/master`, confirm `master` is clean, then create a fresh local heal branch. Never stash, reset, discard, or overwrite user changes unless the user explicitly asks.
- Use the local environment: `./owen vN`, `.venv/bin/python3`, and repository scripts only.
- Keep the repository root pristine. Put temporary diagnostics under `scratch/`, persistent helpers under `scripts/`, and generated verification reports under `volumes/vN/reports/`.
- Do not modernize 17th-century spelling, punctuation, or historical hyphenation. Apply text replacements only for clear OCR/extraction defects.
- If whitelisting anything, maintain both `volumes/vN/bugs_fixes/volume_N_whitelist.json` and `volume_N_whitelist.md`, and explain all whitelisted items in the final report.
- Whitelist cleanup is part of healing. Remove obviously unused stale entries for categories with zero current findings. Keep broad policy suppressions, such as low Latin tagging or translation coverage, only with concrete rationale and surface them as review debt in readiness reports.
- Keep volume-specific content in `volumes/vN/convert.py` `OVERRIDES`. Do not place volume-specific title pages, OCR lists, or hooks in shared modules.
- Latin/foreign-language translations and expanded citations must render as popup/endnote notes, never as inline replacement text in body prose. Treat inline `Modern Translation:` or `Modern Citation:` body content as a blocker.
- Use external Owen witnesses only as exception-driven evidence for audit-flagged windows, suspicious OCR patterns, paragraph splits, language/citation hotspots, or dense source-window loss. Do not require manual page-by-page collation across a whole volume, and do not inject external text unless source family, edition, and local PDF agreement are verified.
- Use available tools to reduce manual burden: browser/computer-use for visual and Apple Books checks, GitHub for optional issue/branch hygiene, code-review for a final review pass when requested, and bounded read-only subagent/plugin work for external collation or citation research when useful.
- Branch, commit, and push are recommended durability steps, but do not commit or push without asking first. Before asking, show the exact changed-file scope and generated artifacts. PR creation is optional and only when explicitly requested.
- Preserve Apple Books EPUB3 polish: mobile-safe CSS, `@font-face` weight/style integrity, CDATA-wrapped CSS, Greek/Hebrew language spans, Hebrew RTL isolation, tappable footnotes, valid NAV/NCX/landmarks, and embedded fonts.
- Do not claim a volume is visually approved unless the user has reviewed it by eye. The skill may make the EPUB ready for that review and identify exact places to inspect.

## Commands

- `$heal worst`, `#heal worst`, `$heal`, or `#heal`: choose the Owen volume with the highest current Need score.
- `$heal N`, `#heal N`, or `heal volume N`: heal volume `N`, where `N` is `1` through `16`.

## Context Preflight

Before a long heal run, check whether the conversation already contains substantial prior work, large pasted content, long command logs, or a recent near-context-limit checkpoint. If the session is fresh or the user has just run `/clear`, skip this preflight and start normally.

If context is already substantial, stop before running audits or edits and ask the user to choose:

```text
This heal run may be long, and the current conversation already has substantial context.

1. Clear first (recommended): type `/clear`, then send `#heal N` again.
2. Continue now: heal volume N using the current session context.
```

For `#heal worst`, use `#heal worst` in option 1 and "select and heal the worst volume" in option 2. If a choice UI is available, present these as two options; otherwise ask in plain text. Do not run `/clear` yourself. If the user chooses clear-first, stop and wait for the next command. If the user chooses continue-now, proceed without asking again in the same invocation.

## Workflow

1. Run the Context Preflight above before any audits, branch changes, or file edits.
2. Read `CLAUDE.md` before changing converter behavior or project documentation. For list or blockquote fixes, also read `bugs_fixes/owenian-structure-rules.md` and its focused companion notes.
3. Establish the clean `master` base:
   - Run `git status --short --branch`.
   - If any tracked or untracked files are dirty, stop before switching branches. Report the dirty files and ask the user to commit, stash, or otherwise resolve them. Do not run `git stash`, `git reset`, `git checkout --`, or cleanup commands for user changes unless the user explicitly asks.
   - Run `git checkout master`.
   - Run `git fetch origin master` and `git pull --ff-only origin master`.
   - If the pull cannot fast-forward, stop and report the exact git blocker instead of merging.
   - Confirm `git status --short --branch` is clean on `master`.
4. Identify the target:
   - For `worst`, run `.venv/bin/python3 scripts/report_volume_state.py --all --no-readme`, then read `qa/reports/volume_state_report.json` and choose the highest Need score.
   - For an explicit number, validate it is `1` through `16`.
5. Create the heal branch:
   - Create a fresh branch from updated `master`, such as `heal-vN-YYYYMMDD` or a conflict-free variant.
   - Do not reuse an old heal branch unless the user explicitly asks to resume that branch.
   - Never auto-merge to `master`.
6. Capture the baseline for only the target volume:
   - Prefer `./owen vN` for rebuilding when `volumes/vN/convert.py` exists.
   - If a per-volume script is missing and healing requires one, create it from the v1 template and populate `OVERRIDES`.
   - Run `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Run or inspect `.venv/bin/python3 scripts/generate_need_reduction_plan.py N`.
7. Plan from current reports:
   - `volumes/vN/bugs_fixes/volume_N_audit.json`
   - `volumes/vN/bugs_fixes/volume_N_text_integrity.json`
   - `volumes/vN/bugs_fixes/volume_N_bug_regressions.json`
   - `volumes/vN/bugs_fixes/volume_N_anomalies.json`
   - `volumes/vN/plans/vN_need_reduction_plan.md`
   - current score components from `.venv/bin/python3 scripts/report_volume_state.py --volumes N --no-readme`
8. Repair in priority order:
   - EPUB validity, package/navigation, and Apple Books display defects.
   - Text-integrity losses, paragraph splits, repeated windows, inline structural markers, and list/blockquote structure.
   - Need-score components with the largest safe reduction: word coverage, Greek/Hebrew/Latin coverage, Latin tagging, Latin translation, unresolved modern references, untranslated foreign passages, unenriched legacy footnotes, split candidates, audit warnings/errors, anomalies, unmatched quotes, and bug-regression overruns.
   - Clear OCR defects via volume-local `text_replacements` or narrowly justified shared corrections.
   - Unresolved patristic/classical citations through `translation_db.py` or `scripts/patristic_refs.py` only when work identity is known.
   - Whitelist only confirmed false positives or acceptable historical/source forms.
9. Clean generated-file state:
   - Remove untracked space-versioned duplicates such as `volume_1_audit 2.md`, `volume_1 3.epub`, or `decisions 2.md`.
   - Keep reports in deterministic timestamped subdirectories under `volumes/vN/reports/`.
   - Leave unrelated user changes untouched and explicitly report any dirty state that remains.
10. Verify after each meaningful repair:
   - Fast render: `./owen vN --render-only` when extraction is unchanged.
   - Full target checks: `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Score gate check: `.venv/bin/python3 scripts/assert_need_under.py N 1.0`.
   - Readiness gate check: `.venv/bin/python3 scripts/audit_heal_readiness.py N --strict`.
   - If Need remains `>= 1.0`, read the refreshed reports and continue with the next score component instead of finalizing.
   - If readiness fails while Need is `<1.0`, continue blocker repairs if safe; otherwise finish as `blocked with evidence` and disclose review debt separately. Uncommitted heal work on the active heal branch is reported as review debt, not a blocker; it blocks readiness only when the worktree is dirty on `master`.
   - Focused pytest for changed behavior, usually `.venv/bin/python3 -m pytest tests/test_bug_regressions.py` or the smallest relevant test file.
11. Prepare the by-eye review packet:
   - Create `volumes/vN/reports/YYYYMMDD_HHMMSS/volume_N_by_eye_review.md`.
   - Include the absolute EPUB path and the final audit/report paths.
   - List exact EPUB locations to inspect: cover, title page, NAV/TOC, first body chapter, last body chapter, every treatise title page, chapter transitions touched by fixes, pages flagged by audits, Greek/Hebrew-heavy sections, long footnote sections, blockquotes, nested lists, tables, and any repaired citation/translation areas.
   - For each location, state what the user should check by eye: spacing, title hierarchy, paragraph flow, footnote tap targets and backlinks, language rendering, mobile margins, quote/list continuity, and absence of OCR debris.
   - Mark items as `pending user eye review`; mark `pass` only for automated checks the agent actually ran.
12. Finish with a target-scoped verification bundle:
   - Re-run `.venv/bin/python3 scripts/run_all_checks.py N`.
   - Run the hard final Need gate: `.venv/bin/python3 scripts/assert_need_under.py N 1.0`.
   - Run the strict final readiness gate: `.venv/bin/python3 scripts/audit_heal_readiness.py N --strict`.
   - If the Need gate exits nonzero, do not finalize as ready or complete. Continue repairs if safe; otherwise finish only as `blocked with evidence`, with the exact remaining score components.
   - If the readiness gate exits nonzero, do not finalize as ready even if Need is `<1.0`; report blocker-class warnings, regression overruns, inline note leaks, whitelist debt, and Latin review debt from `volumes/vN/bugs_fixes/volume_N_heal_readiness.md`.
   - Locate the latest detailed report under `volumes/vN/reports/` or generate a session report there.
   - Confirm `git status --short` has no accidental root files, duplicate report copies, or unintended generated clutter.

## Final Report

Summarize:

- target volume and branch
- before/after Need score and main changed metrics
- files changed
- validation commands and pass/fail status
- absolute path to the detailed verification/audit report
- absolute path to the by-eye review packet
- every whitelist addition or removal, with rationale
- remaining blockers or review-needed items
- final Need gate status, exactly as `PASS (<1.0)` or `BLOCKED (>=1.0)`
- final readiness gate status, exactly as `PASS (strict ready for by-eye review)` or `BLOCKED`, with the absolute path to `volume_N_heal_readiness.md`

Do not call the volume healed or ready if Need remains `>=1.0` or strict readiness fails; report it as blocked or checkpointed with exact remaining score components and blockers. Do not call the volume visually complete until the user has done the by-eye cleanup pass. The correct agent-owned result is "strict ready for by-eye review" unless the user has explicitly validated the output.
