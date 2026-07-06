# Volume 13 Heal Readiness

Generated: 2026-07-06T02:09:47Z

- Need: 23.1
- Need gate `<1.0`: FAIL
- Strict ready for by-eye review: FAIL
- Blockers: 17
- Review debt: 19

## Blockers

- `epub_audit_warnings`: EPUB audit warnings remain.
  - Value: `1`
- `unresolved_modern_references`: Unresolved modern references remain.
  - Value: `2`
- `untranslated_substantial_foreign_passages`: Substantial foreign passages remain untranslated.
  - Value: `2`
- `unenriched_legacy_footnotes`: Legacy footnotes remain unenriched.
  - Value: `4`
- `unresolved_anomalies`: Text anomalies remain unless specifically verified and whitelisted.
  - Value: `1`
- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `unresolved_modern_references`: Modern notes manifest contains unresolved main-body reference candidates.
- `untranslated_substantial_foreign_passages`: Modern notes manifest contains substantial foreign passages without a high-confidence translation popup.
- `unenriched_legacy_footnotes`: Modern notes manifest contains existing source footnotes needing editorial enrichment.
- `bug_regression_over_budget`: Untagged Greek characters exceeds its budget.
  - Value: `{'observed': 134, 'budget': 55}`
  - Samples: `[{"file": "EPUB/ch027.xhtml", "text": "Δοῦλον Κυρίου οὐ δεῖ μάχεσθαι."}, {"file": "EPUB/ch027.xhtml", "text": "Δεῖ τὸν ἐπίσκοπον ἀνέγκλητον εῖναι, ὡς Θεοῦ οἰκονόμον, μὴ αὐθάδη, μὴ ὀργίλον, μὴ πάροινον, μὴ πλήκτην, μὴ αἰσχροκερδῆ."}, {"file": "EPUB/ch046.xhtml", "text": "Οὐδὲν ἄτερ γραφῆς."}]`
- `source_text_or_conversion_changes`: Source-text or conversion-affecting files have uncommitted changes and must be explicitly reported before readiness.
  - Value: `2`
  - Samples: `[{"status": "M", "path": "volumes/v13/convert.py"}, {"status": "M", "path": "volumes/v13/intermediate/volume_13.json"}]`

## Review Debt

- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `low_latin_tagging`: Latin tagging ratio 65.25% is below 99.00%; verify no Latin text is missing.
  - Value: `0.6525`
  - Samples: `[{"word": "populi", "epub": 8, "tagged": 0}, {"word": "apollos", "epub": 7, "tagged": 0}, {"word": "regulate", "epub": 7, "tagged": 0}]`
- `low_latin_translation`: Latin translation ratio 41.44% is below 99.00%; verify no Latin text is missing.
  - Value: `0.4144`
  - Samples: `[{"phrase": "Medio tutissimus"}, {"phrase": "Sixtus Senensis"}, {"phrase": "in causa facili"}]`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.paragraph_splits: kύριαι δόξαι in Christian religion`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.paragraph_splits: Dum pluit in terras, ut possint sole`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Now, three ways may a man receive`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Motives to the observance of this rule are`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Explication III. The greatness of the work`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Let motives hereunto be`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Now, to a right performance of this duty`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Motives to this duty are`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Now, to a close adhering to the church`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Motives hereunto are`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Now, admonition is twofold`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: These and the like things being duly weighed`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: Thus, in general, to take a view of some particular passages`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `text_integrity.inline_structural_markers: The reasonableness of this gospel institution is manifested by the Holy Ghost`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_tagging`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_translation_coverage`
