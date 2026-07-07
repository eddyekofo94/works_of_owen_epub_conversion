# Volume 11 Heal Readiness

Generated: 2026-07-07T13:53:51Z

- Need: 15.2
- Need gate `<1.0`: FAIL
- Strict ready for by-eye review: FAIL
- Blockers: 1
- Review debt: 7

## Blockers

- `unenriched_legacy_footnotes`: Legacy footnotes remain unenriched.
  - Value: `9`

## Review Debt

- `low_latin_tagging`: Latin tagging ratio 78.08% is below 99.00%; verify no Latin text is missing.
  - Value: `0.7808`
  - Samples: `[{"word": "perpetrate", "epub": 10, "tagged": 0}, {"word": "salmasius", "epub": 9, "tagged": 0}, {"word": "vedelius", "epub": 8, "tagged": 0}]`
- `low_latin_translation`: Latin translation ratio 31.74% is below 99.00%; verify no Latin text is missing.
  - Value: `0.3174`
  - Samples: `[{"phrase": "catena patrum"}, {"phrase": "Sancti Sanciti"}, {"phrase": "Sancta sanctis"}]`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_translation_coverage`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: unenriched_legacy_footnotes`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: suspicious_large_number_starts`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: roman_heading_candidates`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: enumerator_sequence_candidates`
