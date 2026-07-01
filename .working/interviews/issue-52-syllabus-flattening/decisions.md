# Issue 52 Syllabus Flattening

## Goal

Agree on a robust Volume 1 fix for textual issue #52 so Owen's compact introduced syllabi flatten inline not only for "four heads," but also for equivalent introductions such as two/five/six heads, points, ways, parts, accounts, and other explicit point-introducer forms, while preserving real block exposition lists.

## Decisions

- Scope is broader than the literal phrase "four heads"; the fix should target Owenian introduced syllabus patterns generally.
- Use a two-pass architecture: keep automatic converter flattening conservative, then add or strengthen audits that flag broader likely scholastic-anchor/syllabus anomalies for agent review and whitelisting.
- The audit output should be useful as an agent work queue: a later agent should be able to read findings, inspect context, decide true issue versus false positive, and update whitelists accordingly.
- Syllabus audit findings should be decision-ready queue items, including enough context and a stable whitelist key, not merely raw warning snippets.
- Syllabus-anchor false positives should live in the existing per-volume whitelist files under a new `text_integrity.syllabus_anchor_candidates` section, with explanations mirrored in `volume_N_whitelist.md`.
- Converter auto-flattening should cover exact-count introduced runs plus strong formula runs, provided the items are short, sequential, and label-like. Weaker candidates should be audit-only.
- Syllabus audit findings should use action labels: `converter_missed_flatten`, `audit_only_weak_anchor`, `likely_false_positive`, `needs_pdf_check`, and `whitelisted`.

## Findings

- `scripts/owen_lists.py` already has `classify_flat_list_run()` and `_attach_em_dash_flat_list()` as the current decision surface for flat syllabi.
- Existing rules recognize count/category formulas including `two` through `ten`, `twofold` through `fourfold`, and category words such as `things`, `heads`, `parts`, `ways`, `points`, `accounts`, `regards`, `sorts`, `considerations`, `observations`, `particulars`, `respects`, and `instances`.
- `tests/test_bug_regressions.py` already contains a regression asserting the exact issue #52 Chapter 9 `four heads: I. ... IV.` case is flattened.
- Remaining risk is broader coverage: equivalent Owenian introducer formulas, Roman-marker handling, stale rendered output, and audit detection for unflattened introduced syllabi.

## Open Questions

- What exact distinction should govern "compact syllabus to flatten" versus "expository numbered block list to preserve"?
- Implementation should add regression coverage for strong formula/exact count flattening, Roman-marker introduced syllabi, audit candidate output, and whitelist suppression.
