# Volume 1 Legacy Body Notes Disabled Verification

Date: 2026-07-01
Branch: `fix/latin-translation-footnotes`

## Goal

Disable the current phrase/key-driven body translation and citation popup inserter because it creates fragment-level markers inside or around Latin/Greek/Hebrew passages. Preserve the underlying research databases for a future whole-quote note system.

## Design Decision

The replacement feature must translate substantial foreign-language quotes/passages only when Owen does not already translate or meaningfully paraphrase them. It must use one popup after the complete quote/passage and its trailing source citation when present. Modern source references must be high-confidence only.

Decision source:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/.working/interviews/foreign-quote-notes/decisions.md`

## Changes Verified

- `render.py` now uses `body_translation_notes_enabled(config)`, defaulting to `False`.
- The `BODY_TRANSLATIONS` phrase matcher and patristic inline citation fallback are gated behind that switch.
- `scripts/epub_pages.py` uses the same switch for the single-chapter render path.
- Translation/citation databases remain available as research material, but they no longer insert fragment-level body markers by default.

## EPUB Spot Checks

Checked `volumes/v1/output/volume_1.epub`, `EPUB/ch004.xhtml`.

- `noteref-trans` body anchors: 0.
- `noteref-citation` body anchors: 0.
- Cyprian example: no `†` inside `Quod homo est esse Christus voluit; ut et homo possit esse quod Christus est`.
- Cyprian source line: no `cap. 3.◇` marker.
- Clement Greek example: no `†` after `Οῦτος γοῦν ὁ λόγος`.

## Commands

```bash
.venv/bin/python3 -m pytest tests/test_typography_standard.py tests/test_bug_regressions.py::test_latin_dedication_translation_matching tests/test_bug_regressions.py::test_latin_word_tagging tests/test_bug_regressions.py::test_latin_inline_translations
.venv/bin/python3 volumes/v1/convert.py --render-only
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub
.venv/bin/python3 scripts/audit_text_integrity.py 1
.venv/bin/python3 scripts/audit_bug_regressions.py 1
```

## Results

- Focused pytest: 16 passed.
- EPUB audit: PASS, 0 errors, 0 warnings.
- Bug regression report: PASS.
- Text integrity audit: WARN, 1 warning.
  - Existing warning category: `dense_source_window_loss`.
  - Coverage ratio: 0.9998.
  - Latin word coverage ratio: 0.999.
  - Latin tagging ratio: 0.7263.
  - Latin translation ratio remains report-data only and no longer implies rendered body markers.

## Archived Reports

- `volume_1_audit.md`
- `volume_1_audit.json`
- `volume_1_text_integrity.md`
- `volume_1_text_integrity.json`
- `volume_1_bug_regressions.md`
- `volume_1_bug_regressions.json`
