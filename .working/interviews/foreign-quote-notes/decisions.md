# Foreign Quote Notes Interview

## Goal

Decide whether and how to keep the Latin/Greek/Hebrew popup feature by replacing word-level and mid-quote notes with a strict whole-quote/passages-only system: translate quoted foreign-language passages only when Owen does not already provide a translation; attach one clean footnote/popup at the appropriate quote boundary; include a modern source reference when the passage is a citation and the source can be responsibly identified; avoid clutter and false positives.

## Decisions

- The feature must not translate individual words inside a foreign-language quote.
- The main body text must remain unpolluted: no bracketed translations and no dense scattered markers.
- Owen's own translations suppress modern translation notes for the corresponding quote/passages.
- Source/citation information belongs in the same clean popup as the translation when available, or as a citation-only popup only where the user-facing value is high and the anchor can be placed correctly.
- Eligible translation popups include explicit foreign-language quotations and substantial standalone foreign-language clauses/passages.
- Tiny word-level foreign-language runs are not eligible for translation popups.
- Translation popup markers must be anchored after the full foreign-language quote/passage and after its trailing source citation when a trailing citation belongs to that quote.
- Citation-only popup markers may attach to a source citation only when no translation note is needed for the nearby foreign-language quote/passage.
- When Owen provides a nearby English translation or meaningful paraphrase, the system should not duplicate it with a full modern translation note.
- For Owen-translated or Owen-paraphrased foreign-language passages, citation/source-only notes may remain when they add real value and can be anchored after the complete quote/citation unit.
- Modern source references must be high-confidence only: author, work, and location must be identified from Owen's citation or a curated exact mapping.
- If the source is uncertain, the popup should provide the translation only and omit speculative source claims.
- The current phrase/key-driven body translation and citation insertion must be disabled for user-facing output.
- Existing translation/citation databases may be retained as research material, but they should not create fragment-level markers in the rendered body.
- Replacement work should be a quote-level engine that creates at most one note per eligible foreign-language quote/passage.

## Open Questions

- Design and implement the replacement whole-quote note engine.
