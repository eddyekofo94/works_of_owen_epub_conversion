# Volume 10 Heal Readiness

Generated: 2026-07-05T21:08:27Z

- Need: 13.2
- Need gate `<1.0`: FAIL
- Strict ready for by-eye review: FAIL
- Blockers: 4
- Review debt: 10

## Blockers

- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `bug_regression_over_budget`: Syllabus-anchor candidates exceeds its budget.
  - Value: `{'observed': 25, 'budget': 16}`
  - Samples: `[{"key": "EPUB/ch008.xhtml#p172-syllabus-providence-is-a-word-which-in-its-proper-signification-may-seem-to", "action": "likely_false_positive", "file": "EPUB/ch008.xhtml", "anchor_index": 172, "item_range": "p173-p174", "anchor": "ee, or the counsel of his will,\" Ephesians 1:11, for whatsoever he doth now it pleased him from the beginning, Psalm 115:3; seeing, also, that known unto God are all his works from eternity; therefore, three things concerning his providence are considerable: —", "items": [{"marker": "1.", "text": "His decree or purpose, 57 whereby he hath disposed of all things in order, and appointed them for certain ends, which he hath fore-ordained."}, {"marker": "2.", "text": "His prescience, whereby he certainly fore-knoweth all things that shall come to pass."}], "marker_family": "arabic", "item_count": 2, "announced_count": 3, "positive_reasons": ["sequential-marker-family", "count-category-formula", "introductory-punctuation", "parallel-opening-word"], "hard_exclusions": ["developed-item"], "whitelist_key": "EPUB/ch008.xhtml#p172-syllabus-providence-is-a-word-which-in-its-proper-signification-may-seem-to"}, {"key": "EPUB/ch021.xhtml#p699-syllabus-chapter-3-an-unfolding-of-the-remaining-texts-of-scripture-produced-for", "action": "likely_false_positive", "file": "EPUB/ch021.xhtml", "anchor_index": 699, "item_range": "p700-p707", "anchor": "Chapter 3. An unfolding of the remaining texts of Scripture produced for the confirmation of the first general objection or argument for universal redemption.", "items": [{"marker": "2.", "text": "1 John 2:l, 2, largely opened and vindicated."}, {"marker": "3.", "text": "John 6:51 explained."}, {"marker": "4.", "text": "A vindication of other texts produced by Thomas More, viz.: —"}, {"marker": "(1.)", "text": "2 Corinthians 5:19."}, {"marker": "(2.)", "text": "John 1:9."}, {"marker": "(3.)", "text": "John 1:29."}, {"marker": "(4.)", "text": "John 3:17."}, {"marker": "(5.)", "text": "John 4:42; 1 John 4:14; John 6:51."}], "marker_family": "arabic", "item_count": 8, "announced_count": null, "positive_reasons": ["count-category-formula", "compact-first-item", "compact-run"], "hard_exclusions": ["scripture-density", "inconsistent-sequence"], "whitelist_key": "EPUB/ch021.xhtml#p699-syllabus-chapter-3-an-unfolding-of-the-remaining-texts-of-scripture-produced-for"}, {"key": "EPUB/ch021.xhtml#p708-syllabus-chapter-4-answer-to-the-second-general-objection-or-argument-for-the", "action": "likely_false_positive", "file": "EPUB/ch021.xhtml", "anchor_index": 708, "item_range": "p709-p713", "anchor": "Chapter 4. Answer to the second general objection or argument for the universality of redemption.", "items": [{"marker": "2.", "text": "From the word \"all\" in several scriptures, viz.: —"}, {"marker": "1.", "text": "1 Timothy 2:4, 6. 2. 2 Peter 3:9."}, {"marker": "3.", "text": "Hebrews 2:9."}, {"marker": "4.", "text": "2 Corinthians 5:14, 15. 5. 1 Corinthians 15:22."}, {"marker": "6.", "text": "Romans 5:18."}], "marker_family": "arabic", "item_count": 5, "announced_count": null, "positive_reasons": ["count-category-formula", "compact-first-item", "compact-run"], "hard_exclusions": ["scripture-density", "multiple-sentences", "inconsistent-sequence"], "whitelist_key": "EPUB/ch021.xhtml#p708-syllabus-chapter-4-answer-to-the-second-general-objection-or-argument-for-the"}]`
- `source_text_or_conversion_changes`: Source-text or conversion-affecting files have uncommitted changes and must be explicitly reported before readiness.
  - Value: `3`
  - Samples: `[{"status": "M", "path": "scripts/translation_db.py"}, {"status": "M", "path": "volumes/v10/convert.py"}, {"status": "M", "path": "volumes/v10/intermediate/volume_10.json"}]`

## Review Debt

- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage
- `low_latin_tagging`: Latin tagging ratio 58.82% is below 99.00%; verify no Latin text is missing.
  - Value: `0.5882`
  - Samples: `[{"word": "ejusdem", "epub": 17, "tagged": 2}, {"word": "tantidem", "epub": 12, "tagged": 0}, {"word": "scotus", "epub": 4, "tagged": 0}]`
- `low_latin_translation`: Latin translation ratio 38.82% is below 99.00%; verify no Latin text is missing.
  - Value: `0.3882`
  - Samples: `[{"phrase": "Elenchus Controversiarum"}, {"phrase": "Martii, anno Domini"}, {"phrase": "Tantum religio"}]`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: inline_structural_markers`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_tagging`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: low_latin_translation_coverage`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: repeated_windows`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: roman_heading_candidates`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: suspicious_large_number_starts`
- `stale_whitelist_entry`: Stale whitelist entry remains and should be cleaned when safe.
  - Value: `epub_warnings: weak_page_coverage`
