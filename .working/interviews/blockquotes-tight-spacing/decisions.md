# Blockquote Tight Spacing

## Goal

Agree on a blockquote spacing standard that makes quotes feel integrated with the surrounding paragraph/body text instead of fragmented, while preserving enough visual separation for readability in Apple Books/mobile EPUB.

## Decisions

- `margin: 1.2em 0;` means top/bottom outside spacing of `1.2em` and left/right outside spacing of `0`.
- The current vertical gap is perceived as too fragmented; spacing should become slightly tighter.
- Use asymmetric spacing rather than symmetric spacing: the top gap should be tighter because a quotation usually belongs to the preceding sentence, while the bottom gap may remain slightly larger to return to body prose.
- Ordinary blockquotes should use `margin: 0.7em 0 0.85em;`.
- `blockquote.sermon-opening-scripture` already has a distinct centered/italic rule and should not be changed with ordinary displayed quotations.

## Open Questions

No open design questions remain for this pass.
