# Volume 1 Latin Translation Verification

- Branch: `fix/latin-translation-footnotes`
- EPUB: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/output/volume_1.epub`
- Intermediate JSON: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/intermediate/volume_1.json`

## Targeted Findings

- Body-text bracket pollution removed: `[Translated:]` count in V1 XHTML is `0`.
- Reported sample pollution removed: `[How therefore]` count in V1 XHTML is `0`.
- Old citation asterisk markers removed: `<sup>*</sup>` count in V1 XHTML is `0`.
- Lactantius source now renders as citation-only popup marker: `(lib. 4, De Vera Sapient.)◇`.
- The Latin quotation beginning `Quomodo igitur` remains in the main body without bracketed English additions; Owen's following English rendering remains in the body.

## Verification Commands

```bash
.venv/bin/python3 volumes/v1/convert.py
.venv/bin/python3 volumes/v1/convert.py --render-only
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub
.venv/bin/python3 scripts/audit_text_integrity.py 1
.venv/bin/python3 scripts/audit_bug_regressions.py 1
.venv/bin/python3 scripts/audit_latin_research.py 1
.venv/bin/python3 -m pytest tests/test_typography_standard.py tests/test_bug_regressions.py::test_latin_dedication_translation_matching tests/test_bug_regressions.py::test_latin_inline_translations tests/test_bug_regressions.py::test_latin_word_tagging
```

## Results

- EPUB audit: PASS, `0` errors, `0` warnings.
- Text-integrity audit: WARN, `2` warnings: `dense_source_window_loss`, `paragraph_split_candidates`.
- Bug regression report: PASS.
- Focused pytest: `12 passed`.
- Full cross-volume pytest was attempted and failed on pre-existing/stale cross-volume whitelist/anomaly checks plus two tests that still expected legacy bracket injection. The two obsolete inline-translation tests were updated and pass in the focused run.

## Included Reports

- `volume_1_audit.md` / `.json`
- `volume_1_text_integrity.md` / `.json`
- `volume_1_bug_regressions.md` / `.json`
- `volume_1_latin_research.md` / `.json`
