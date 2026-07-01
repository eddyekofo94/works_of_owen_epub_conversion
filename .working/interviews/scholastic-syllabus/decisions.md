# Scholastic Syllabus Classifier

## Goal

Agree on a global, low-false-positive classifier for Owen scholastic anchors that fixes #50 inline-flat false breaks and #51 bare `1.` anchor styling, with explicit guards for cases that must remain block.

## Decisions

- The fix should be global, not a v1-only patch.
- Owen's syllabus statements normally announce points first, then proceed to expound them. The announced point-list should render inline as a flat syllabus; the later exposition should remain block.
- The first entry in an immediately following marker run is often diagnostic: if the first entry is classified as inline syllabus, the rest of that adjacent point run should generally follow inline, subject to hard false-positive guards.
- Use the hybrid classifier bias: explicit syllabus evidence always wins; first-item-led flattening is allowed only when the run itself is strongly syllabus-like.
- First-item evidence should be weighted: if item 1 ends with a comma or semicolon, or is only a few words, that increases confidence that the adjacent sequential run is a flat syllabus. It should not be an unconditional trigger without supporting evidence.
- Hard exclusions override first-item-led flattening:
  - developed prose, including multi-sentence items, long explanatory clauses, scripture chains, or proof language;
  - marker-family restarts after a just-flattened syllabus, unless a new anchor sentence intervenes;
  - protected contexts such as blockquotes, footnotes/asides, citation-heavy text, or obvious scripture reference runs.
- Two-item runs use a hybrid rule: explicit two-count anchors flatten freely; otherwise the run needs at least two non-anchor signals, such as item 1 punctuation, both items compact, parallel opening syntax, sequential same marker family, and open anchor punctuation.
- Issue #51 inline bare-marker styling should be handled after flat-syllabus classification: only confirmed `syllabus-anchor` paragraphs should receive inline marker normalization/bolding for bare `1.`, `(1.)`, etc. Do not run a broad inline-marker bolding pass over ordinary prose.
- Implementation should be gates-first, scoring-second. Hard exclusions run first; explicit syllabus anchors pass; ambiguous cases can pass by score when they have enough real evidence. Scoring evidence should include compact item word counts, especially sub-20-word items, item-1 comma/semicolon/colon endings, sequential markers, and parallel phrasing.
- Compactness thresholds should be moderate: item 1 under 12 words is strong evidence; all items under 20 words is strong run evidence; any item over 25 words usually blocks unless explicit count/formula evidence makes it a longer preview syllabus.
- Exposition-restart protection should use a local window: remember the last flattened marker family until a new normal anchor sentence, heading, or explicit syllabus anchor resets the context. This should be validated against real Owen/PDF-derived structure, not only isolated synthetic strings.
- Verification scope should include global tests plus v1 render/audit, and a broader non-conversion scan across existing generated artifacts or JSON for available volumes. The scan should produce a diagnostic report explaining classifier decisions and likely false-positive/false-negative risks.
- New audit/diagnostic reports can be created and must be saved under the relevant volume reports directory, preferably a deterministic timestamped subdirectory under `volumes/v1/reports/` for this global-classifier session.

## Open Questions

- Implementation details remain: exact score weights, local-window reset rules, and diagnostic scan format.
