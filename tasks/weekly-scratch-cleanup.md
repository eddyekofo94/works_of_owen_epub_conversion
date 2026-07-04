---
name: weekly-scratch-cleanup
description: Project-local reusable task for weekly cleanup of disposable diagnostics under scratch while preserving active notes and useful artifacts.
scope: project-local
---

# Weekly Scratch Cleanup

Use this task to keep `scratch/` usable without touching source, volume outputs, or reports outside `scratch/`.

## Steps

1. Inspect `scratch/` and group items as active notes, reusable diagnostics, stale generated files, or unclear.
2. Preserve active notes, current investigation artifacts, and anything referenced by recent engineering logs or open plans.
3. Delete only clearly disposable stale files under `scratch/`, such as temporary extraction dumps, throwaway logs, and generated experiments that are no longer referenced.
4. Move any persistent helper discovered in `scratch/` to `scripts/` only when it is clearly reusable and the user requested remediation.
5. Do not delete anything outside `scratch/`.
6. Write a cleanup report to `scratch/cleanup/YYYYMMDD_HHMMSS/weekly_scratch_cleanup.md` listing deleted paths, preserved paths, and uncertain paths left untouched.

## Safety

If a file's purpose is unclear, leave it in place and list it under review-needed items.
