# Scholastic Anchor Inline Rule

## Goal

Reach an agreed implementation design for a robust scholastic-anchor/list-structure rule that prevents false block lists when the previous point ends with a comma or semicolon, while preserving real block lists and defining enough search/regression coverage for the next implementation session.

## Decisions

- Scope: design only in this session. Implementation and verification will happen in a later session.
- Target failure: sibling point structures such as `(1.) As it was triumphant, as he was a King;` followed by `(2.) As it was gracious, as he was a Priest.` should be inline because the previous point ends with `;` and is syntactically continuing.
- Initial code finding: relevant gates are `_split_inline_structural_markers()` in `shared.py`, `_split_rendered_inline_structural_html()` in `render.py`, and the sibling/run logic in `scripts/owen_lists.py`, especially `_attach_em_dash_flat_list()`, `_allows_attach()`, `_merge_short_inline_lists()`, and `_add_owen_list_level_classes()`.
- Placement: use a two-layer rule. Add a conservative pre-render guard where applicable, but make the rendered HTML sibling pass in `scripts/owen_lists.py` authoritative because it can inspect the previous and next points together.
- Comma/semicolon policy: if a scholastic/enumerator point sees a comma or semicolon immediately before it in the visible reading stream, it should be inline, not block. Treat this as a strong default; block structure should survive only where the candidate is demonstrably not part of the same continuing scholastic run.
- Punctuation scope: only comma and semicolon are part of this new rule. Other punctuation classes should continue to be handled by existing list/anchor rules unless a separate concrete failure is found.
- "Immediately before it": use the reader-visible previous punctuation, after stripping HTML tags, whitespace, noterefs/footnote markers, and closing quotes/brackets. If the last meaningful visible character before the candidate point is `,` or `;`, force inline.
- Deep-search finding: existing `scripts/owen_lists.py` already has comma/semicolon continuation signals, but they are mostly run/classifier/word-cap driven. That leaves local pair failures when a broader run is rejected for `developed-item`, `long-final-item`, inconsistent marker family, or similar reasons.
- Deep-search finding: recent Volume 1 reports repeatedly surface the `ch023` ascension structure, including the run where `(1.) In his ascension...` leads to an inline `1st ... 2ndly ... 3rdly ...` sequence and then `[1.] As unto the manner...`; this should become a targeted regression fixture.
- Existing standards: `bugs_fixes/owenian-structure-rules.md` and `flat-list-rules.md` say ambiguity falls back to block, but compact/continuing syllabus runs should be inline. The new rule should be framed as a syntactic continuation invariant, not a broad flattening rule.
- Word-count caps: the pairwise comma/semicolon rule may bypass existing word-count caps for the immediate next point. Each subsequent point must be evaluated against the newly merged visible text rather than flattening an entire run blindly.
- Chain behavior: use pairwise repeat. Merge N+1 into N when N ends with comma/semicolon; then inspect the merged paragraph's new ending and repeat only if the new last meaningful visible character is again comma/semicolon.
- Verification gate: add focused unit/regression tests, render the target/default volume only, and run a diagnostic deep scan over existing generated XHTML/reports for adjacent list-item paragraphs where the previous point's last meaningful visible character is comma or semicolon. Do not batch-regenerate volumes.
- Deep scan form: create a persistent narrow helper script, e.g. `scripts/audit_inline_continuation_breaks.py`, rather than a one-off scratch diagnostic or immediate integration into the larger audits. If the script proves low-noise, it can later be folded into bug-regression reporting.

## Open Questions

- Define the minimal "not same continuing run" exceptions, if any.
- Implementation details remain for next session: exact helper names, function placement, tests, and report path.
