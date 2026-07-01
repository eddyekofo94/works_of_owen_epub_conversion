# Ephraim Reference Fix Verification

Date: 2026-07-01
Branch: `fix/latin-translation-footnotes`
Volume: 1

## Goal

Ensure Ephraim/Ephrem references mark the full patristic name when present, and avoid false positives for biblical uses of Ephraim.

## Changes Verified

- `scripts/biography_db.py` no longer contains a global bare `Ephraim` biography key.
- Biography keys now include `Ephraim Syrus`, `Ephrem the Syrian`, and `Ephraem Syrus`.
- `scripts/patristic_refs.py` no longer treats bare `ephraim` as an author abbreviation for patristic citation resolution.
- Patristic citation resolution still works when context contains `Ephraim Syrus`, because the unambiguous `Syrus` cue canonicalizes to the Ephraim/Ephrem work map.

## EPUB Spot Checks

Generated EPUB:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/output/volume_1.epub`

Observed in `EPUB/ch004.xhtml`:

- `Ephraim Syrus` is followed by a biographical noteref anchor.
- The old broken placement `Ephraim‡ Syrus` is absent.

Observed in `EPUB/ch045.xhtml`:

- Biblical uses of `Ephraim` in Hosea contexts remain unmarked.

Endnote check:

- `EPUB/endnotes.xhtml` contains the biographical note headed `Ephraim Syrus`.

## Commands Run

```bash
.venv/bin/python3 -m pytest tests/test_typography_standard.py -k "ephraim or patristic_citation_regex_keeps_numeric_ranges_together"
.venv/bin/python3 volumes/v1/convert.py --render-only
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub --out-dir volumes/v1/bugs_fixes
.venv/bin/python3 scripts/audit_text_integrity.py 1
```

## Test Results

- Focused pytest: 4 passed.
- Volume 1 render-only: successful.

## EPUB Audit Summary

Source report:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/reports/20260701_150319_ephraim_reference_fix/volume_1_audit.md`

- Status: PASS
- Errors: 0
- Warnings: 0
- OPF: `EPUB/content.opf`
- OPF version: 3.0
- Files: 116
- Manifest items: 107
- Spine items: 84
- XHTML files: 85
- Embedded fonts: 17
- NAV links: 86
- Greek chars: 4091
- Untagged Greek chars: 0
- Hebrew chars: 157
- Untagged Hebrew chars: 0
- Noteref links: 223
- Endnote anchors: 223
- Boilerplate hits: 0
- Possible Beta Code files: 0

## Text Integrity Summary

Source report:

`/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/reports/20260701_150319_ephraim_reference_fix/volume_1_text_integrity.md`

- Status: WARN
- Warnings: 1
- Warning code: `dense_source_window_loss`
- PDF pages: 633
- EPUB text files: 83
- EPUB paragraphs/headings: 2714
- PDF content tokens: 191893
- EPUB content tokens: 205657
- Approximate PDF-to-EPUB coverage ratio: 0.9998
- Pages checked: 581
- Weak page matches: 0
- Dense source windows checked: 26712
- Missing dense source-window pages: 32
- Body paragraphs checked: 2276
- Possible faulty paragraph splits: 0
- Citation continuation splits: 0
- Greek word coverage ratio: 1.0
- Hebrew word coverage ratio: 1.0
- Latin word coverage ratio: 0.999
- Latin word tagging ratio: 0.7263
- Latin translation ratio: 0.5388

Sample pages affected by the existing dense source-window warning:

- 382
- 402
- 406
- 411
- 419
- 433
- 434
- 451
- 480
- 483

## Notes

- No whitelist entries were added or changed.
- The audit scripts reported pre-existing unused whitelist entries; this session did not modify the whitelist.
- A mistaken initial EPUB audit command treated `1` as a path and wrote `qa/reports/1_audit.*`; those files were removed before this report was finalized.
