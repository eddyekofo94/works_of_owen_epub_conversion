# Volume 12 Scholastic Anchor Redesign Verification

Status: **IMPLEMENTED (AWAITING VALIDATION)**  
Branch: `feature/scholastic-anchor-redesign`  
Scope: Volume 12 only

## Result

- Render completed from cached Volume 12 JSON: 53 chapters and 502 source
  footnotes; output package contains 1,089 noteref/endnote links after
  translation enrichment.
- EPUB audit: PASS, 0 errors, 0 warnings.
- Package: EPUB 3.0, 87 files, 78 manifest items, 61 spine items, 62 XHTML
  files, 11 embedded fonts, and 63 navigation links.
- `structural_guide.xhtml`: absent from package, manifest, spine, and NAV.
- `abbreviations_guide.xhtml`: present.
- Legacy `.owen-branch` wrappers: 0.
- Semantic occurrences: 1,034 `block-list-primary`, 388
  `block-list-subpoint`, 3 `scholastic-parent`, 15 `scholastic-child`, and 219
  blockquotes.
- Greek: 14,115 characters, 0 untagged; word coverage 99.92%.
- Hebrew: 1,456 characters, 0 untagged; word coverage 100%.

## Tests

- Focused structural/fidelity gate: 171 passed.
- New fixtures cover diagnostic flat/block decisions, developed-item
  exclusions, label OCR spacing, ordinary-word negatives, blockquote
  protection, bare numbered continuation purity, and wrapper absence.
- Additional updated bug fixtures: 10 passed; scoped Volume 12 package/integrity
  regression gates: 2 passed. Unrestricted `pytest -q` did not reach repository
  tests because it collected five unrelated pre-existing `scratch/test_*.py`
  files. A broader `tests/` run was interrupted after 158 results; remaining
  unrelated failures included stale Volume 1 EPUB expectations and existing
  Volume 11 OCR anomalies. All redesign-related failures observed before the
  interruption were updated and their focused reruns passed.

## Text-integrity findings

- PDF pages: 822; pages checked: 815; EPUB paragraphs/headings: 3,676.
- PDF content tokens: 270,735; EPUB content tokens: 271,853; approximate
  coverage ratio: 0.9993.
- Body paragraphs checked: 3,246; weak page matches: 0; possible faulty paragraph splits: 0; inline structural
  marker candidates: 0; adjacent duplicates: 0.
- Warnings: one dense source window on PDF page 181 and 25 repeated word
  windows. Existing page-window observations remain on pages 5, 11, 136, 175,
  438; these were not introduced or repaired by this structural-only change.
- Bug-regression budgets are within limits except the existing translated
  noteref-leading-space sample in `EPUB/ch027.xhtml` (observed 1, budget 0).
- Anomaly audit: 0 suspected anomalies.

## Presentation verification

Default CSS is mobile-first: all list roles and scholastic anchors are flush,
borderless paragraphs. A single `42em` media query gives all confirmed
subpoints (including semantic level 3) the same `0.65em` offset. Blockquotes
receive one independent `0.5em` desktop offset and no list-derived selector.
The in-app visual browser could not initialize in this environment, so no
screenshots were produced; direct package/XHTML/CSS inspection passed.

## Whitelists and limitations

No whitelist entries were added or changed. Existing Volume 12 whitelist
entries were applied by the audits and reported as unused where applicable.
User review in Apple Books remains required before changing the status from
**IMPLEMENTED (AWAITING VALIDATION)**.
