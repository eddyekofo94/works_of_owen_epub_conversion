# Volume 1 Latin Marker Placement Verification

Date: 2026-07-01
Branch: `fix/latin-translation-footnotes`

## Issue

The Leo quotation in `EPUB/ch004.xhtml` had a source popup marker inserted inside the Latin text as `qui◇ nunquam`. The cause was a malformed `BODY_TRANSLATIONS` key truncated at:

`... et ideo materia nunquam deficit laudis; qui`

The same failure class also appeared in citation-list continuations, where markers could split a source title or range, for example `De◇ Fide`, `13◇-20`, or `distinct. 10◇, a 4`.

## Changes Verified

- Removed the malformed Leo quote citation key from `scripts/translation_db.py`.
- Removed partial citation-list keys that ended before the source item was complete.
- Added renderer guards so citation markers are skipped when the next visible text clearly continues the same Latin/source phrase.
- Added patristic fallback guards for `De`, `in`, `ad`, `cap`, `Fide`, `Johan`, and related source-title continuations.
- Updated citation parsing so numeric ranges such as `13-20` stay together.
- Added regression coverage in `tests/test_typography_standard.py`.

## EPUB Spot Checks

Checked `volumes/v1/output/volume_1.epub`, `EPUB/ch004.xhtml`.

- `qui◇`: absent.
- `De◇ Fide`: absent.
- `13◇-20`: absent.
- `10◇, a 4`: absent.
- Leo source marker is attached to `(Serm. 9, De Nativit.)◇` before the quote.
- The Leo Latin quote remains uninterrupted through `laudis; qui nunquam sufficit`.

## Commands

```bash
.venv/bin/python3 -m pytest tests/test_typography_standard.py tests/test_bug_regressions.py::test_latin_dedication_translation_matching tests/test_bug_regressions.py::test_latin_word_tagging tests/test_bug_regressions.py::test_latin_inline_translations
.venv/bin/python3 volumes/v1/convert.py --render-only
unzip -p volumes/v1/output/volume_1.epub EPUB/ch004.xhtml | rg -n "qui◇|De<a class=\"noteref noteref-citation\"|13<a class=\"noteref noteref-citation\"[^>]*><sup>◇</sup></a>-20|10,<a class=\"noteref noteref-citation\"[^>]*><sup>◇</sup></a> a 4|Serm\\. 9, De Nativit|De Fide ad Regin|13-20|distinct\\. 10" -C 1
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub
.venv/bin/python3 scripts/audit_text_integrity.py 1
.venv/bin/python3 scripts/audit_bug_regressions.py 1
.venv/bin/python3 scripts/audit_latin_research.py 1
```

## Results

- Focused pytest: 15 passed.
- EPUB audit: PASS, 0 errors, 0 warnings.
- Text integrity audit: WARN, 2 warnings.
  - Existing warning categories: `dense_source_window_loss`, `paragraph_split_candidates`.
  - Coverage ratio: 0.9998.
  - Latin word coverage ratio: 0.999.
  - Latin tagging ratio: 0.7263.
  - Latin translation ratio: 0.5388.
- Bug regression report: PASS.

## Archived Reports

- `volume_1_audit.md`
- `volume_1_audit.json`
- `volume_1_text_integrity.md`
- `volume_1_text_integrity.json`
- `volume_1_bug_regressions.md`
- `volume_1_bug_regressions.json`
- `volume_1_latin_research.md`
- `volume_1_latin_research.json`
