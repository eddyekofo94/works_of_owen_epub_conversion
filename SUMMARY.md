# Converter Work — Summary

## What Went Wrong

My previous edit of `converter.py` was a destructive "simplification" that gutted a working 1662-line pipeline down to 859 lines. It removed:

| Feature | Effect |
|---------|--------|
| **Visual TOC fallback** | Chapters got CONTENTS page text instead of real content |
| **Front matter detection** | Page numbers leaked into title pages as `<p class="subtitle">2</p>` |
| **Font conversion from `shared.py`** | Proper Greek/Hebrew conversion replaced with broken Beta Code map |
| **Title/TOC/preserve page distinction** | Every page treated as body text |
| **OPF repackaging** | Missing cover meta, NCX, guide landmarks |
| **CLI argparse** | Couldn't run `--test` or process all volumes |
| **Font CSS in stylesheet** | `@font-face` was in inline `<style>` which ebooklib strips |

## What Was Fixed (in this session)

1. **Reverted to base commit** `f8997e02` — restored the complete pipeline

2. **Merged `@font-face` into `main.css`** — font CSS is now in the stylesheet file, not inline `<style>`, so ebooklib doesn't strip it. Removed `font_styles` parameter from `_make_xhtml()` and all callers.

3. **Manual cover page** — replaced `book.set_cover()` with manual `EpubHtml` creation so the cover can be placed first in the spine and have proper `<meta name="cover">` in the OPF.

4. **Fixed spine order** — cover → frontispiece → nav → title → front matter → chapters

5. **NAV landmarks** — `generate_nav_xhtml()` now includes `<nav epub:type="landmarks">` with entries for cover, toc, frontispiece, and bodymatter.

6. **Cover meta in OPF** — added during repackaging step if missing.

7. **Apple Books display-options** — `_inject_apple_books_options()` post-processes the EPUB to enable `specified-fonts=true`.

8. **Ghost layer de-duplication** — `_remove_adjacent_duplicates()` in `clean_text()` removes identical lines within a 5-line window that are produced by pymupdf4llm when it renders PDF ghost layers.

## Current State

- Volume 1 converts successfully in ~53 seconds
- Chapter content is real text (not CONTENTS listing)
- Ghost layer duplication removed
- NAV has proper hierarchy + landmarks
- OPF has cover meta + Apple Books options + NCX
- Fonts embedded with `@font-face` rules in `main.css`

## What's NOT Done (would need future work)

- **Hebrews pipeline** — not implemented (CLI `--hebrebs` exits with message)
- **Special source volumes (5, 10)** — these use CCEL XML sources, not PDF. Current pipeline only handles PDF.
- **Multi-volume testing** — only volume 1 verified. Volumes 2–16 may have edge cases.
- **Comprehensive content QA** — spot-check showed content is real text and ghost layers removed, but full proofreading across all volumes is needed.
