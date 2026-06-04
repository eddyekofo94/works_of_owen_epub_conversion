# Render.py Refactoring Plan

This plan outlines the systematic breakdown of the monolithic `render.py` script into smaller, domain-specific modules inside the `scripts/` directory. Each phase will be executed on its own isolated Git worktree branch and ticked off upon completion and verification.

## Strategy: Outside-In
We will extract pure text-processing functions first (like markdown conversion and list processing) because they are stateless and easiest to decouple from the core EPUB assembly logic. As `render.py` shrinks, the remaining structural logic will be easier to organize.

## Refactoring Progress Tracking

| Phase | Branch Name | Target File | Functions Extracted | Built Fine? | Tests Passed? | Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Phase 1** | `render-refactor-lists` | `scripts/owen_lists.py` | `_attach_em_dash_flat_list`, `_add_owen_list_level_classes`, `_merge_short_inline_lists`, `_nest_owen_list_hierarchies`, `_owen_marker_level` | [x] | [x] | ✅ Complete |
| **Phase 2** | `render-refactor-markdown` | `scripts/markdown_parser.py` | `markdown_to_html`, `_repair_markdown_tables` | [x] | [x] | ✅ Complete |
| **Phase 3** | `render-refactor-glossary` | `scripts/technical_glossary.py` | Encapsulate glossary text-scanning loop into `apply_glossary_footnotes()`, add complex nested dictionaries with regex rules. | [x] | [x] | ✅ Complete |
| **Phase 4** | `render-refactor-epub-pages`| `scripts/epub_pages.py` | `format_treatise_title_page`, `_polish_contents_page_html`, `generate_copyright_xhtml`, `format_title_page`, `build_toc_page_xhtml` | [x] | [x] | ✅ Complete |
| **Phase 5** | `render-refactor-scholastic`| `scripts/scholastic_parser.py`, `scripts/polish.py` | `apply_scholastic_anchor_protocol`, `_nest_scholastic_in_divs`, `_apply_premium_signatures` | [x] | [x] | ✅ Complete |
| **Phase 6** | `render-refactor-volume` | `render.py` | `load_volume_intermediate`, `initialize_epub_book`, `embed_fonts_and_stylesheet`, `add_cover_and_frontispiece`, `build_and_add_front_matter`, `finalize_epub_archive` | [x] | [x] | ✅ Complete |

---

## Execution Protocol
For each phase, I will:
1. Create a new worktree branch (e.g., `Owen-render-refactor-lists`).
2. Implement the relative path linkage for worktree portability.
3. Extract the functions into the new script in `scripts/`.
4. Update `render.py` to import and use the extracted functions.
5. Generate the EPUB and run the `#test audit 1` validation command to ensure Volume 1 still builds perfectly and all tests pass.
6. Tick the boxes in the table above and mark the phase as ✅ Complete.
