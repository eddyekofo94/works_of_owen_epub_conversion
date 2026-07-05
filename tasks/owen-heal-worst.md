---
name: owen-heal-worst
description: Project-local reusable task that invokes the Owen-only heal workflow for the current worst Need-score volume and prepares it for by-eye Apple Books review.
scope: project-local
skill: heal
---

# Owen Heal Worst

Use this task when the user asks to heal the currently worst Owen volume.

## Steps

1. Use the project-local `$heal` skill at `skills/heal/SKILL.md`.
2. Run `.venv/bin/python3 scripts/report_volume_state.py --all --no-readme` to identify the volume with the highest Need score.
3. Heal exactly that one Owen volume, scoped to volumes `1` through `16`.
4. Target polished Apple Books-compliant EPUB3 output and readiness for human by-eye cleanup, not merely removal of critical errors.
5. Continue iterating until Need is below `1.0` and `.venv/bin/python3 scripts/audit_heal_readiness.py N --strict` passes, remaining issues are documented blockers, or the session approaches the 20% context floor.
6. Do not batch-heal additional volumes and do not auto-merge to `master`.
7. End with a final report that includes absolute paths to the target volume's verification/audit report and by-eye review packet under `volumes/vN/reports/`.
