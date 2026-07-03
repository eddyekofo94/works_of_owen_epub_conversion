# Modern Note Dedup Interview

## Goal

Fix duplicate modern-reference markers so overlapping citation candidates produce one reader-facing marker, not stacked or adjacent `◇◇` references.

## Decisions

- For overlapping modern-note candidates, keep only the longest/highest-confidence matched phrase and suppress every shorter overlapping legacy item.
- The sample failure should keep one `◇` for the complete curated reference unit instead of additional markers for `Epist. 78`, `Epist. 71`, `lib. 5`, `cap. 8, 9`, or other substrings.

## Open Questions

- None for the current bug. Implement and verify on v1 only.
