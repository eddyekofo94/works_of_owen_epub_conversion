# Volume 13 Heal Readiness

Generated: 2026-07-06T02:39:17Z

- Need: 15.5
- Need gate `<1.0`: FAIL
- Strict ready for by-eye review: FAIL
- Blockers: 8
- Review debt: 5

## Blockers

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `source_text_or_conversion_changes`: Source-text or conversion-affecting files have uncommitted changes and must be explicitly reported before readiness.
  - Value: `3`
  - Samples: `[{"status": "M", "path": "scripts/translation_db.py"}, {"status": "M", "path": "volumes/v13/convert.py"}, {"status": "M", "path": "volumes/v13/intermediate/volume_13.json"}]`

## Review Debt

- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `low_latin_tagging`: Latin tagging ratio 65.25% is below 99.00%; verify no Latin text is missing.
  - Value: `0.6525`
  - Samples: `[{"word": "populi", "epub": 8, "tagged": 0}, {"word": "apollos", "epub": 7, "tagged": 0}, {"word": "regulate", "epub": 7, "tagged": 0}]`
- `low_latin_translation`: Latin translation ratio 41.44% is below 99.00%; verify no Latin text is missing.
  - Value: `0.4144`
  - Samples: `[{"phrase": "Medio tutissimus"}, {"phrase": "Sixtus Senensis"}, {"phrase": "in causa facili"}]`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_tagging`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_translation_coverage`
