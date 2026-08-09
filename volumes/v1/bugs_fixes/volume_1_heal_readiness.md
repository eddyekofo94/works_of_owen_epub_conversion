# Volume 1 Heal Readiness

Generated: 2026-08-09T00:57:19Z

- Need: 0.8
- Need gate `<1.0`: PASS
- Strict ready for by-eye review: PASS
- Blockers: 0
- Review debt: 3

## Blockers

None.

## Review Debt

- `low_latin_tagging`: Latin tagging ratio 77.12% is below 99.00%; verify no Latin text is missing.
  - Value: `0.7712`
  - Samples: `[{"word": "nestorius", "epub": 8, "tagged": 0}, {"word": "serm", "epub": 5, "tagged": 0}, {"word": "folio", "epub": 3, "tagged": 0}]`
- `low_latin_translation`: Latin translation ratio 53.88% is below 99.00%; verify no Latin text is missing.
  - Value: `0.5388`
  - Samples: `[{"phrase": "quarto (Amsterdam"}, {"phrase": "nobis a praelo a capite"}, {"phrase": "operis absentibus"}]`
- `source_text_or_conversion_changes`: Conversion-affecting files have uncommitted changes on branch 'heal-v1-20260707'; disclose and commit them on the heal branch before merging.
  - Value: `2`
  - Samples: `[{"status": "M", "path": "shared.py"}, {"status": "M", "path": "volumes/v1/intermediate/volume_1.json"}]`
