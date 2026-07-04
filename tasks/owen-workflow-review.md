---
name: owen-workflow-review
description: Project-local reusable task for reviewing Owen workflow health, branch hygiene, root cleanliness, report placement, local skills, and task definitions.
scope: project-local
---

# Owen Workflow Review

Use this task to audit repository workflow health without changing converter output.

## Steps

1. Read `AGENTS.md`, `GEMINI.md`, and the README skill/task section.
2. Inspect `git status --short --branch` and note the active branch, dirty files, and whether unrelated user changes are present.
3. Check root cleanliness: no one-off scripts, reports, logs, or diagnostics should live in the repository root.
4. Verify local skill packaging under `skills/`: each active skill directory should have a matching `.skill` package; deprecated packages should be absent.
5. Verify task definitions under `tasks/` remain project-local and do not depend on global Codex state.
6. Check report placement rules: audit/session reports belong under `volumes/vN/reports/` or `qa/reports/`, not the root.
7. Write findings to `scratch/workflow-review/YYYYMMDD_HHMMSS/owen_workflow_review.md`.

## Output

Report findings first, ordered by severity, then list recommended fixes. Do not modify files unless the user explicitly asks for remediation.
