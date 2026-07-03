# Owen Workflow Reminder

## Next Time You Start Work

- Start from a narrow goal: one volume, one issue class, or one workflow decision.
- Check `git status --short --branch` before editing.
- If the task is ambiguous, use `grill-me` only until the decision record has exit criteria, scope/non-goals, evidence, validation plan, and ready-to-act steps.
- If the task is deterministic, skip extra planning and run the focused command or test directly.
- Keep branches reviewable: avoid mixing parser architecture, report regeneration, modern notes, and unrelated textual fixes in one commit.
- Before committing, run focused tests for touched behavior and record the report path if converter/rendering work occurred.

## Cleanup Reminder

- Do not casually delete `scratch/`: many files are tracked and may contain historical diagnostics.
- Use a dedicated cleanup branch when ready.
- Classify scratch files into: keep as historical evidence, promote to `scripts/`, archive under a dated folder, or delete.
- Keep new one-off diagnostics in `scratch/`; promote repeated diagnostics to `scripts/`.

## Suggested Next Review

- Review the current broad commit by topic before opening or merging anything.
- Split future work by story: modern notes, Roman/list classification, foreign punctuation audits, and Volume 1 textual fixes should normally be separate branches.
