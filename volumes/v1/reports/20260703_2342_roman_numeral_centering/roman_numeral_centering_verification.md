# Roman Numeral Centering Verification

## Scope

- Decision file implemented: `.working/interviews/roman-numeral-centering/decisions.md`
- Target volume rebuilt: Volume 1
- Affected source range verified: `Preface (Meditations and Discourses on the Glory of Christ)`, PDF pages 351-366
- Affected EPUB file verified: `EPUB/ch027.xhtml`

## Implementation Summary

- Roman numeral matching now uses canonical Roman numeral grammar plus the scholarly-abbreviation denylist.
- `ill.`, `Ill.`, and `ILL.` are no longer promoted as Roman headings, list markers, or bold structural prefixes.
- Tokenized `[[ROMAN_HEAD]]` paragraphs and ordinary Roman-leading paragraphs now share the same rule:
  - Roman flat-list eligibility is checked first.
  - Non-list Roman section openers render as a centered `.roman-subheading` containing only the numeral.
  - The following text renders as a normal prose paragraph.
- Bare comma/dash lead-ins such as `For,` only start Roman list runs when the Roman item is compact; long prose openers fall back to section rendering.

## XHTML Verification

Generated EPUB inspected: `volumes/v1/output/volume_1.epub`

`EPUB/ch027.xhtml`:

- `roman-list-item` count: 0
- `roman-subheading` count: 4
- Verified section shapes:
  - `<h4 class="roman-subheading"><strong>I.</strong></h4>` followed by `He it is in whom our nature...`
  - `<h4 class="roman-subheading"><strong>II.</strong></h4>` followed by `In him the relation...`
  - `<h4 class="roman-subheading"><strong>III.</strong></h4>` followed by `It is he in whom our nature...`
  - `<h4 class="roman-subheading"><strong>IV.</strong></h4>` followed by `He it is who in himself...`

Regression preservation:

- `EPUB/ch013.xhtml` still contains the flattened Chapter 9 Roman syllabus anchor.
- The bad form `<h4 class="roman-subheading"><strong>I.</strong> Honor.</h4>` is absent.
- The expected form `<h4 class="roman-subheading"><strong>I.</strong></h4>` remains present for the later section head.

## Test Commands

- `.venv/bin/python3 -m pytest tests/test_bug_regressions.py::test_for_comma_long_roman_opener_is_section_not_list tests/test_bug_regressions.py::test_tokenized_long_roman_opener_centers_numeral_only tests/test_bug_regressions.py::test_tokenized_front_matter_roman_opener_uses_centered_fallback tests/test_bug_regressions.py::test_tokenized_compact_roman_syllabus_still_flattens tests/test_bug_regressions.py::test_ill_abbreviation_is_not_promoted_to_roman_heading tests/test_owen_structure_classifier.py tests/test_text_fidelity.py::test_inline_roman_section_splits_to_subheading_before_flat_list`
  - Result: 23 passed.
- `.venv/bin/python3 volumes/v1/convert.py --render-only`
  - Result: EPUB rebuilt at `volumes/v1/output/volume_1.epub`.

## Audit Reports

EPUB audit:

- Report: `volume_1_audit.md`
- Status: PASS
- Errors: 0
- Warnings: 0
- Greek chars: 4091
- Untagged Greek chars: 0
- Hebrew chars: 157
- Untagged Hebrew chars: 0
- Noteref links: 313
- Endnote anchors: 313

Text integrity audit:

- Report: `volume_1_text_integrity.md`
- Status: WARN
- Warnings: 7
- PDF pages: 633
- EPUB text files: 83
- EPUB paragraphs/headings: 2695
- PDF content tokens: 191893
- EPUB content tokens: 205448
- Approximate PDF-to-EPUB coverage ratio: 0.9997
- Pages checked: 581
- Weak page matches: 1
- Missing dense source-window pages: 34
- Missing top-of-page body windows: 2
- Possible faulty paragraph splits: 13
- Inline structural marker candidates: 0
- Roman heading candidates: 1
- Greek word coverage ratio: 1.0
- Hebrew word coverage ratio: 1.0
- Latin word coverage ratio: 0.999

Text-integrity warning classes:

- `weak_page_coverage`
- `dense_source_window_loss`
- `top_of_page_text_loss`
- `paragraph_split_candidates`
- `syllabus_anchor_candidates`
- `unresolved_modern_references`
- `untranslated_substantial_foreign_passages`

