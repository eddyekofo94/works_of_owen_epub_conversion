# Volume 12 Whitelist

This document tracks all known and deliberately bypassed anomalies and structural deviations in Volume 12. These are not OCR errors, but rather original structural decisions or known constraints of the text.

## Textual Anomalies

### `blind eyes...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `qui et...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `e manibus...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `E verbo...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `Pater noster...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `e lacu...`
- **Type:** split_word
- **Reason:** English/Latin false positive

### `w him`
- **Type:** split_word (isolated letter 'w')
- **Reason:** OCR residual / text artifact

### `s subsisting`
- **Type:** split_word (isolated letter 's')
- **Reason:** OCR residual / text artifact

## Dense Source Window Loss
- **Pages:** 4, 5, 6, 7, 11, 17, 29, 30, 32, 41, 48, 55, 59, 63, 94, 100, 104, 105, 110, 113, 116, 118, 120, 128, 136, 137, 144, 145, 146, 154, 162, 169, 174, 175, 184, 194, 197, 199, 220, 223
- **Reason:** Mostly due to structural elements, patristic Latin passages, polyglot strings, or scripture references dominating the OCR output on these pages.

## Text Integrity Audit Warnings

- `possible_beta_code_residue`
- `repeated_phrases`
- `missing_enumerator_markers`
- `front_matter_toc_loss`
- `top_of_page_text_loss`
- `bottom_of_page_text_loss`
- `suspicious_large_number_starts`
- `enumerator_sequence_candidates`
- `missing_latin_clauses`
- `low_latin_translation_coverage`
- `low_latin_tagging`
- `low_latin_word_coverage`
