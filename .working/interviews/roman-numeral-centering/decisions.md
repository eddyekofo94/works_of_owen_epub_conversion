# Roman Numeral Flat-List And Centering

## Goal

Reach shared understanding on a global Roman-numeral rendering rule: Roman numerals should participate in the same flat-list/inline classification rules as other enumerators, while genuine Roman section heads should be centered where appropriate. The design must explain the current Volume 1 miss and define a rule precise enough to fix it without damaging compact Roman outline lists.

## Decisions

- Current observed output: the cited Volume 1 examples render in `EPUB/ch027.xhtml` as `<p class="roman-list-item list-level-1 block-list-primary"><strong>I.</strong> ...</p>`, not as centered `.roman-subheading`.
- Current cause: `scripts/markdown_parser.py` treats Roman heads in `FRONT_MATTER` as Roman list items, and `.roman-list-item` is styled as justified prose while `.roman-subheading` is centered.
- Long Roman section openers should render with only the Roman numeral centered as its own `.roman-subheading`; the following prose should be a normal paragraph. Example target shape: centered `I.`, then `He it is in whom...` as prose.
- User clarified desired scope: this should be a global fix, not a v1-only override and not merely a front-matter-only rule.
- Roman numerals should remain eligible for the same flat-list/inline rules as other enumerators.
- Where Roman numerals are genuine section heads rather than flat-list items, they should be centered appropriately.
- Implement the rule in the shared parser/classification path, not as a Volume 1 postprocess override.
- Ordering: apply flat-list/inline eligibility first for Roman numerals. Centered Roman section rendering is the fallback only after the classifier determines the Roman numeral is not part of a flat/inline list.
- Roman flat/inline eligibility should use the same classifier path as other markers but with Roman-specific safety guards, because Roman numerals are often genuine section heads.
- False-positive guard requirement: abbreviation or ordinary-word fragments such as `ill.` must not be promoted as Roman numerals. Current code already rejects `ill.`/`Ill.`/`ILL.` in the checked path and has an existing regression around `ill. For what he so does`; the global Roman change must preserve this behavior.
- Roman matching should use a hybrid guard: canonical Roman-numeral grammar plus a small scholarly-abbreviation denylist for Roman-looking strings that are not structural markers in context.

## Open Questions

- None for this design pass.
