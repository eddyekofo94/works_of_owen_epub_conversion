# Blemish: General Preface Extraction and Nesting Errors — FIXED

## Status: FIXED [2026-05-09]
**Verification:** Verified via Volume 1 conversion. "General Preface" is now correctly identified as a Level-1 front-matter section, matched to high-quality `pdftohtml` content, and Greek titles like `ΘΕΟΛΟΓΟΥΜΕΝΑ` now use the correct `Upsilon` (Υ).

## Issue
... (rest of content) ...

## Implementation
- **Centering Fix:** Updated `classify_paragraph` to use estimated text center `(left + width/2)` instead of just `left`.
- **Match Improvement:** Allowed `build_chapters` to keep title-only chapters and improved `_normalize_title` to handle merged words.
- **Greek Map:** Fixed `shared.py` to map `Y`/`y` to `Upsilon` (Υ/υ).
- **Nesting Logic:** Refined major front-matter detection to reset state for 'GENERAL PREFACE' but keep 'PREFACE' nested under treatises.
