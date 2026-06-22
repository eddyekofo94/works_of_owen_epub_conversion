# Code Review and Compliance Audit Report

This report summarizes compliance audits against the architectural mandates and styling principles specified in `GEMINI.md` and `AGENTS.md`.

## Metrics Summary

| Metric | Value | Status |
|---|---|---|
| **GEMINI.md Compliance Errors** | 0 | ✅ Compliant |
| **Design / Code Quality Warnings** | 32 | ⚠️ Attention Suggested |
| **Refactoring Recommendations (Infos)** | 606 | Information |

## Detailed Findings

### `converter.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L102 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L103 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L104 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L105 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L106 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L108 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L110 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L111 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L114 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L122 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L131 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L137 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L212 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L232 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L242 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L246 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L302 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L306 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L320 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L331 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |
| L353 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'converter.py'. Use logging or structured UI messages. |

### `extract.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L128 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_volume' does not have full type annotations for arguments or return type. |
| L154 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'extract.py'. Use logging or structured UI messages. |
| L267 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'extract.py'. Use logging or structured UI messages. |
| L271 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_html_to_markdown' does not have full type annotations for arguments or return type. |
| L328 | 🟡 Warning | Code Smell (Long Function) | Function 'extract_epub2_volume' is 271 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L328 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_epub2_volume' does not have full type annotations for arguments or return type. |
| L344 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'extract.py'. Use logging or structured UI messages. |
| L387 | ⚪ Info | Style (Missing Type Hints) | Function 'parse_nav_point' does not have full type annotations for arguments or return type. |
| L595 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'extract.py'. Use logging or structured UI messages. |

### `render.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L158 | ⚪ Info | Style (Missing Type Hints) | Function 'normalize_footnote_markers' does not have full type annotations for arguments or return type. |
| L160 | ⚪ Info | Style (Missing Type Hints) | Function 'repl' does not have full type annotations for arguments or return type. |
| L187 | ⚪ Info | Style (Missing Type Hints) | Function 'force_polyglot_mapping' does not have full type annotations for arguments or return type. |
| L224 | ⚪ Info | Style (Missing Type Hints) | Function 'tag_unicode_ranges' does not have full type annotations for arguments or return type. |
| L244 | ⚪ Info | Style (Missing Type Hints) | Function 'tag_greek' does not have full type annotations for arguments or return type. |
| L255 | ⚪ Info | Style (Missing Type Hints) | Function 'tag_hebrew' does not have full type annotations for arguments or return type. |
| L298 | ⚪ Info | Style (Missing Type Hints) | Function 'emphasize_structural_prefix' does not have full type annotations for arguments or return type. |
| L378 | ⚪ Info | Style (Missing Type Hints) | Function '_split_rendered_inline_structural_html' does not have full type annotations for arguments or return type. |
| L706 | ⚪ Info | Style (Missing Type Hints) | Function 'find_cover' does not have full type annotations for arguments or return type. |
| L723 | ⚪ Info | Style (Missing Type Hints) | Function 'find_portrait' does not have full type annotations for arguments or return type. |
| L746 | ⚪ Info | Style (Missing Type Hints) | Function 'detect_page_type' does not have full type annotations for arguments or return type. |
| L813 | ⚪ Info | Style (Missing Type Hints) | Function 'is_toc_continuation_page' does not have full type annotations for arguments or return type. |
| L957 | ⚪ Info | Style (Missing Type Hints) | Function 'replace_first_outside_tags_and_comments' does not have full type annotations for arguments or return type. |
| L963 | ⚪ Info | Style (Missing Type Hints) | Function 'is_excluded' does not have full type annotations for arguments or return type. |
| L1001 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'render.py'. Use logging or structured UI messages. |
| L1312 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'render.py'. Use logging or structured UI messages. |
| L1315 | 🟡 Warning | Code Smell (Long Function) | Function 'render_volume' is 471 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L1315 | ⚪ Info | Style (Missing Type Hints) | Function 'render_volume' does not have full type annotations for arguments or return type. |
| L1501 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_and_map' does not have full type annotations for arguments or return type. |
| L1538 | ⚪ Info | Style (Missing Type Hints) | Function 'make_quote_agnostic' does not have full type annotations for arguments or return type. |
| L1664 | ⚪ Info | Style (Missing Type Hints) | Function 'replace_biographical' does not have full type annotations for arguments or return type. |

### `scripts/ages_verse_translator.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L223 | ⚪ Info | Style (Missing Type Hints) | Function '_has_repeated_ages_marker_cluster' does not have full type annotations for arguments or return type. |

### `scripts/audit_anomalies.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L678 | 🟡 Warning | Code Smell (Long Function) | Function 'main' is 279 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L678 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `scripts/audit_css.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L107 | 🟡 Warning | Code Smell (Long Function) | Function 'run_audit' is 177 lines long (exceeds recommended max of 150 lines). Consider modularizing. |

### `scripts/audit_epub.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L231 | 🟡 Warning | Code Smell (Long Function) | Function 'check_xhtml' is 381 lines long (exceeds recommended max of 150 lines). Consider modularizing. |

### `scripts/audit_spelling.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L235 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `scripts/audit_text_integrity.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L755 | 🟡 Warning | Code Smell (Long Function) | Function 'paragraph_integrity' is 332 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L1780 | 🟡 Warning | Code Smell (Long Function) | Function 'run_audit' is 482 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L2274 | 🟡 Warning | Code Smell (Long Function) | Function 'render_markdown' is 173 lines long (exceeds recommended max of 150 lines). Consider modularizing. |

### `scripts/audit_unmatched_quotes.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L17 | ⚪ Info | Style (Missing Type Hints) | Function 'repl' does not have full type annotations for arguments or return type. |
| L28 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `scripts/audit_whitelists.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L89 | 🟡 Warning | Code Smell (Long Function) | Function 'run_whitelist_audit' is 327 lines long (exceeds recommended max of 150 lines). Consider modularizing. |

### `scripts/catechism_parser.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L76 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_catechism_lookahead_ghosts' does not have full type annotations for arguments or return type. |

### `scripts/ccel_enrich.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L77 | ⚪ Info | Style (Missing Type Hints) | Function 'walk' does not have full type annotations for arguments or return type. |
| L95 | ⚪ Info | Style (Missing Type Hints) | Function '_ascii_fold' does not have full type annotations for arguments or return type. |
| L124 | ⚪ Info | Style (Missing Type Hints) | Function 'parse_ccel_xml' does not have full type annotations for arguments or return type. |

### `scripts/chapter_builder.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L68 | 🟡 Warning | Code Smell (Long Function) | Function 'build_chapters_from_toc' is 195 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L68 | 🟡 Warning | Code Smell (Too Many Parameters) | Function 'build_chapters_from_toc' has 7 arguments (recommended max of 6). |
| L68 | ⚪ Info | Style (Missing Type Hints) | Function 'build_chapters_from_toc' does not have full type annotations for arguments or return type. |

### `scripts/code_review.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L90 | ⚪ Info | Style (Missing Type Hints) | Function 'visit_FunctionDef' does not have full type annotations for arguments or return type. |
| L132 | ⚪ Info | Style (Missing Type Hints) | Function 'visit_Try' does not have full type annotations for arguments or return type. |
| L515 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_markdown_report' does not have full type annotations for arguments or return type. |
| L571 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `scripts/epub_builder.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L18 | ⚪ Info | Style (Missing Type Hints) | Function '_make_xhtml' does not have full type annotations for arguments or return type. |
| L22 | ⚪ Info | Style (Missing Type Hints) | Function 'wrap_footnote' does not have full type annotations for arguments or return type. |
| L70 | ⚪ Info | Style (Missing Type Hints) | Function '_polish_treatise_title_page_html' does not have full type annotations for arguments or return type. |
| L76 | ⚪ Info | Style (Missing Type Hints) | Function 'footnote_marker_repl' does not have full type annotations for arguments or return type. |
| L199 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_frontispiece_xhtml' does not have full type annotations for arguments or return type. |
| L203 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_nav_xhtml' does not have full type annotations for arguments or return type. |
| L269 | ⚪ Info | Style (Missing Type Hints) | Function 'build_hierarchical_toc' does not have full type annotations for arguments or return type. |
| L276 | ⚪ Info | Style (Missing Type Hints) | Function '_nest' does not have full type annotations for arguments or return type. |
| L310 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_ncx' does not have full type annotations for arguments or return type. |
| L330 | ⚪ Info | Style (Missing Type Hints) | Function 'repackage_canonical' does not have full type annotations for arguments or return type. |
| L380 | ⚪ Info | Style (Missing Type Hints) | Function '_inject_apple_books_options' does not have full type annotations for arguments or return type. |
| L407 | 🟡 Warning | Code Smell (Too Many Parameters) | Function 'build_endnotes_chapter' has 8 arguments (recommended max of 6). |
| L407 | ⚪ Info | Style (Missing Type Hints) | Function 'build_endnotes_chapter' does not have full type annotations for arguments or return type. |

### `scripts/epub_pages.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L15 | 🟡 Warning | Code Smell (Long Function) | Function '_polish_contents_page_html' is 153 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L171 | ⚪ Info | Style (Missing Type Hints) | Function 'format_treatise_title_page' does not have full type annotations for arguments or return type. |
| L213 | ⚪ Info | Style (Missing Type Hints) | Function 'starts_body_or_chapter' does not have full type annotations for arguments or return type. |
| L221 | ⚪ Info | Style (Missing Type Hints) | Function 'looks_like_body_run' does not have full type annotations for arguments or return type. |
| L323 | ⚪ Info | Style (Missing Type Hints) | Function 'format_title_page' does not have full type annotations for arguments or return type. |
| L407 | ⚪ Info | Style (Missing Type Hints) | Function 'restore_dropped_title_noteref' does not have full type annotations for arguments or return type. |
| L424 | ⚪ Info | Style (Missing Type Hints) | Function 'build_toc_page_xhtml' does not have full type annotations for arguments or return type. |
| L507 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_copyright_xhtml' does not have full type annotations for arguments or return type. |
| L638 | ⚪ Info | Style (Missing Type Hints) | Function '_init_render_paths_and_json' does not have full type annotations for arguments or return type. |
| L683 | ⚪ Info | Style (Missing Type Hints) | Function '_inject_fonts_and_css' does not have full type annotations for arguments or return type. |
| L755 | ⚪ Info | Style (Missing Type Hints) | Function '_add_cover_and_portrait' does not have full type annotations for arguments or return type. |
| L814 | ⚪ Info | Style (Missing Type Hints) | Function '_add_front_matter' does not have full type annotations for arguments or return type. |
| L925 | 🟡 Warning | Code Smell (Long Function) | Function '_render_single_chapter' is 317 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L925 | 🟡 Warning | Code Smell (Too Many Parameters) | Function '_render_single_chapter' has 13 arguments (recommended max of 6). |
| L925 | ⚪ Info | Style (Missing Type Hints) | Function '_render_single_chapter' does not have full type annotations for arguments or return type. |
| L1060 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_and_map' does not have full type annotations for arguments or return type. |
| L1093 | ⚪ Info | Style (Missing Type Hints) | Function 'make_quote_agnostic' does not have full type annotations for arguments or return type. |
| L1205 | ⚪ Info | Style (Missing Type Hints) | Function 'replace_biographical' does not have full type annotations for arguments or return type. |
| L1245 | 🟡 Warning | Code Smell (Too Many Parameters) | Function '_finalize_epub_and_write' has 12 arguments (recommended max of 6). |
| L1245 | ⚪ Info | Style (Missing Type Hints) | Function '_finalize_epub_and_write' does not have full type annotations for arguments or return type. |

### `scripts/footnote_extractor.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L65 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_footnotes_from_pdf' does not have full type annotations for arguments or return type. |
| L123 | ⚪ Info | Style (Missing Type Hints) | Function 'parse_thml_footnotes' does not have full type annotations for arguments or return type. |
| L150 | ⚪ Info | Style (Missing Type Hints) | Function 'get_all_text_between' does not have full type annotations for arguments or return type. |
| L243 | ⚪ Info | Style (Missing Type Hints) | Function 'merge_footnotes' does not have full type annotations for arguments or return type. |
| L266 | ⚪ Info | Style (Missing Type Hints) | Function 'find_footnote_refs_in_text' does not have full type annotations for arguments or return type. |
| L275 | ⚪ Info | Style (Missing Type Hints) | Function '_normalize_extracted_footnote_markers' does not have full type annotations for arguments or return type. |
| L277 | ⚪ Info | Style (Missing Type Hints) | Function 'repl' does not have full type annotations for arguments or return type. |

### `scripts/generate_need_reduction_plan.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L74 | ⚪ Info | Style (Missing Type Hints) | Function 'gather_volume_data' does not have full type annotations for arguments or return type. |
| L251 | ⚪ Info | Style (Missing Type Hints) | Function 'detect_compound_merges' does not have full type annotations for arguments or return type. |
| L328 | 🟡 Warning | Code Smell (Long Function) | Function 'generate_plan' is 247 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L328 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_plan' does not have full type annotations for arguments or return type. |
| L593 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `scripts/generate_untranslated_manifest.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L84 | ⚪ Info | Style (Missing Type Hints) | Function 'scan_collection' does not have full type annotations for arguments or return type. |

### `scripts/greek_hebrew_dedupe.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L24 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_adjacent_line_overlaps' does not have full type annotations for arguments or return type. |
| L29 | ⚪ Info | Style (Missing Type Hints) | Function 'words_with_spans' does not have full type annotations for arguments or return type. |

### `scripts/markdown_parser.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L114 | ⚪ Info | Style (Missing Type Hints) | Function 'add_recent_plain' does not have full type annotations for arguments or return type. |
| L188 | 🟡 Warning | Code Smell (Long Function) | Function '_process_structural_token' is 263 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L454 | 🟡 Warning | Code Smell (Long Function) | Function '_clean_and_format_paragraph' is 323 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L512 | ⚪ Info | Style (Missing Type Hints) | Function 'footnote_marker_repl' does not have full type annotations for arguments or return type. |
| L780 | 🟡 Warning | Code Smell (Long Function) | Function '_render_block_container' is 158 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L780 | 🟡 Warning | Code Smell (Too Many Parameters) | Function '_render_block_container' has 8 arguments (recommended max of 6). |
| L780 | ⚪ Info | Style (Missing Type Hints) | Function '_render_block_container' does not have full type annotations for arguments or return type. |
| L941 | 🟡 Warning | Code Smell (Long Function) | Function 'markdown_to_html' is 207 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L941 | ⚪ Info | Style (Missing Type Hints) | Function 'markdown_to_html' does not have full type annotations for arguments or return type. |

### `scripts/markdown_skeleton.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L28 | ⚪ Info | Style (Missing Type Hints) | Function 'page_has_special_fonts' does not have full type annotations for arguments or return type. |
| L45 | ⚪ Info | Style (Missing Type Hints) | Function 'page_is_structural' does not have full type annotations for arguments or return type. |
| L72 | 🟡 Warning | Code Smell (Long Function) | Function 'extract_structural_page' is 222 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L72 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_structural_page' does not have full type annotations for arguments or return type. |
| L88 | ⚪ Info | Style (Missing Type Hints) | Function 'flush' does not have full type annotations for arguments or return type. |
| L107 | ⚪ Info | Style (Missing Type Hints) | Function 'flush_blockquote' does not have full type annotations for arguments or return type. |
| L298 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_page_text_with_fonts' does not have full type annotations for arguments or return type. |
| L355 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_page_markdown' does not have full type annotations for arguments or return type. |
| L378 | ⚪ Info | Style (Missing Type Hints) | Function 'get_merged_page_text' does not have full type annotations for arguments or return type. |

### `scripts/owen_lists.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L6 | 🟡 Warning | Code Smell (Long Function) | Function '_attach_em_dash_flat_list' is 464 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L533 | 🟡 Warning | Code Smell (Long Function) | Function '_add_owen_list_level_classes' is 178 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L752 | ⚪ Info | Style (Missing Type Hints) | Function 'close_levels_down_to' does not have full type annotations for arguments or return type. |
| L852 | 🟡 Warning | Code Smell (Long Function) | Function '_merge_short_inline_lists' is 156 lines long (exceeds recommended max of 150 lines). Consider modularizing. |

### `scripts/paragraph_healer.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L17 | ⚪ Info | Style (Missing Type Hints) | Function 'repl' does not have full type annotations for arguments or return type. |
| L85 | ⚪ Info | Style (Missing Type Hints) | Function '_repair_unbalanced_bracket_splits' does not have full type annotations for arguments or return type. |

### `scripts/pdf_coordinates.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L8 | ⚪ Info | Style (Missing Type Hints) | Function 'coordinate_redactor' does not have full type annotations for arguments or return type. |
| L86 | ⚪ Info | Style (Missing Type Hints) | Function 'convert_span_text' does not have full type annotations for arguments or return type. |
| L94 | ⚪ Info | Style (Missing Type Hints) | Function '_merge_adjacent_blockquote_paragraphs' does not have full type annotations for arguments or return type. |
| L230 | ⚪ Info | Style (Missing Type Hints) | Function '_join_blockquote_lines' does not have full type annotations for arguments or return type. |
| L255 | ⚪ Info | Style (Missing Type Hints) | Function 'page_has_blockquote_geometry' does not have full type annotations for arguments or return type. |
| L269 | ⚪ Info | Style (Missing Type Hints) | Function '_compute_page_text_bounds' does not have full type annotations for arguments or return type. |
| L328 | ⚪ Info | Style (Missing Type Hints) | Function '_text_block_is_blockquote' does not have full type annotations for arguments or return type. |
| L492 | ⚪ Info | Style (Missing Type Hints) | Function 'extract_ages_nav' does not have full type annotations for arguments or return type. |

### `scripts/polish.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L3 | 🟡 Warning | Code Smell (Long Function) | Function '_apply_premium_signatures' is 154 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L8 | ⚪ Info | Style (Missing Type Hints) | Function 'replacer' does not have full type annotations for arguments or return type. |
| L21 | ⚪ Info | Style (Missing Type Hints) | Function 'parse_signature_paragraph' does not have full type annotations for arguments or return type. |
| L61 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_block' does not have full type annotations for arguments or return type. |
| L118 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_html_block' does not have full type annotations for arguments or return type. |
| L144 | ⚪ Info | Style (Missing Type Hints) | Function 'format_signature_html' does not have full type annotations for arguments or return type. |
| L188 | ⚪ Info | Style (Missing Type Hints) | Function 'replacer' does not have full type annotations for arguments or return type. |
| L234 | ⚪ Info | Style (Missing Type Hints) | Function 'replacer' does not have full type annotations for arguments or return type. |

### `scripts/progress.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L118 | ⚪ Info | Style (Missing Type Hints) | Function 'spinner_wrap_callback' does not have full type annotations for arguments or return type. |
| L127 | ⚪ Info | Style (Missing Type Hints) | Function 'wrapped' does not have full type annotations for arguments or return type. |

### `scripts/report_volume_state.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L68 | 🟡 Warning | Code Smell (Long Function) | Function 'gather_volume_data' is 184 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L365 | ⚪ Info | Style (Missing Type Hints) | Function 'vol_sort_key' does not have full type annotations for arguments or return type. |

### `scripts/roman_parser.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L112 | ⚪ Info | Style (Missing Type Hints) | Function '_coalesce_roman_list_paragraphs' does not have full type annotations for arguments or return type. |

### `scripts/run_all_checks.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L35 | ⚪ Info | Style (Missing Type Hints) | Function 'vol_sort_key' does not have full type annotations for arguments or return type. |

### `scripts/scan_citations.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L46 | ⚪ Info | Style (Missing Type Hints) | Function 'load_volume' does not have full type annotations for arguments or return type. |

### `scripts/technical_glossary.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L132 | ⚪ Info | Style (Missing Type Hints) | Function 'apply_glossary_footnotes' does not have full type annotations for arguments or return type. |
| L167 | ⚪ Info | Style (Missing Type Hints) | Function 'replace_glossary' does not have full type annotations for arguments or return type. |

### `scripts/text_cleaner.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L33 | ⚪ Info | Style (Missing Type Hints) | Function 'strip_false_ocr_bolds' does not have full type annotations for arguments or return type. |
| L38 | ⚪ Info | Style (Missing Type Hints) | Function 'replace_bold' does not have full type annotations for arguments or return type. |
| L63 | ⚪ Info | Style (Missing Type Hints) | Function '_is_terminal' does not have full type annotations for arguments or return type. |
| L93 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_text' does not have full type annotations for arguments or return type. |
| L170 | ⚪ Info | Style (Missing Type Hints) | Function '_normalize_scholarly_citation_artifacts' does not have full type annotations for arguments or return type. |
| L211 | 🟡 Warning | Code Smell (Long Function) | Function 'reconstruct_paragraphs' is 247 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L211 | ⚪ Info | Style (Missing Type Hints) | Function 'reconstruct_paragraphs' does not have full type annotations for arguments or return type. |
| L465 | ⚪ Info | Style (Missing Type Hints) | Function '_paragraph_needs_numeric_continuation' does not have full type annotations for arguments or return type. |
| L607 | ⚪ Info | Style (Missing Type Hints) | Function '_paragraph_needs_text_continuation' does not have full type annotations for arguments or return type. |
| L648 | ⚪ Info | Style (Missing Type Hints) | Function '_is_probable_duplicate_fragment' does not have full type annotations for arguments or return type. |
| L692 | ⚪ Info | Style (Missing Type Hints) | Function '_collapse_adjacent_duplicate_refs' does not have full type annotations for arguments or return type. |
| L719 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_duplicate_scripture_tail' does not have full type annotations for arguments or return type. |
| L786 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_interrupted_duplicate_clause' does not have full type annotations for arguments or return type. |
| L827 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_adjacent_repeated_word_runs' does not have full type annotations for arguments or return type. |
| L832 | ⚪ Info | Style (Missing Type Hints) | Function 'tokens' does not have full type annotations for arguments or return type. |
| L888 | ⚪ Info | Style (Missing Type Hints) | Function 'post_process_paragraphs' does not have full type annotations for arguments or return type. |
| L1002 | ⚪ Info | Style (Missing Type Hints) | Function '_remove_global_ngram_duplicates' does not have full type annotations for arguments or return type. |
| L1031 | ⚪ Info | Style (Missing Type Hints) | Function 'deduplicate_junction' does not have full type annotations for arguments or return type. |
| L1057 | 🟡 Warning | Code Smell (Too Many Parameters) | Function 'get_pages_text' has 9 arguments (recommended max of 6). |
| L1057 | ⚪ Info | Style (Missing Type Hints) | Function 'get_pages_text' does not have full type annotations for arguments or return type. |

### `shared.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L31 | ⚪ Info | Style (Missing Type Hints) | Function 'is_greek_font' does not have full type annotations for arguments or return type. |
| L37 | ⚪ Info | Style (Missing Type Hints) | Function 'is_hebrew_font' does not have full type annotations for arguments or return type. |
| L43 | ⚪ Info | Style (Missing Type Hints) | Function 'contains_greek' does not have full type annotations for arguments or return type. |
| L47 | ⚪ Info | Style (Missing Type Hints) | Function 'contains_hebrew' does not have full type annotations for arguments or return type. |
| L376 | ⚪ Info | Style (Missing Type Hints) | Function 'merge_volume_config' does not have full type annotations for arguments or return type. |
| L386 | ⚪ Info | Style (Missing Type Hints) | Function 'run_volume_cli' does not have full type annotations for arguments or return type. |
| L415 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L416 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L417 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L418 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L419 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L421 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L423 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L424 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L434 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L445 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L454 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L460 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L567 | ⚪ Info | Style (Missing Type Hints) | Function 'get_volume_dir' does not have full type annotations for arguments or return type. |
| L582 | ⚪ Info | Style (Missing Type Hints) | Function 'get_volume_label' does not have full type annotations for arguments or return type. |
| L746 | ⚪ Info | Style (Missing Type Hints) | Function 'clean_greek_text' does not have full type annotations for arguments or return type. |
| L777 | ⚪ Info | Style (Missing Type Hints) | Function 'convert_greek_word' does not have full type annotations for arguments or return type. |
| L971 | ⚪ Info | Style (Missing Type Hints) | Function 'is_hebrew_vowel' does not have full type annotations for arguments or return type. |
| L978 | ⚪ Info | Style (Missing Type Hints) | Function 'convert_gideon_hebrew' does not have full type annotations for arguments or return type. |
| L1004 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L1398 | 🟡 Warning | Code Smell (Long Function) | Function '_repair_owen_ocr_errors' is 214 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L1615 | ⚪ Info | Style (Missing Type Hints) | Function 'title_case' does not have full type annotations for arguments or return type. |
| L1637 | ⚪ Info | Style (Missing Type Hints) | Function 'nav_display_title' does not have full type annotations for arguments or return type. |
| L1694 | ⚪ Info | Style (Missing Type Hints) | Function '_split_inline_structural_markers' does not have full type annotations for arguments or return type. |
| L1843 | ⚪ Info | Style (Missing Type Hints) | Function '_trim_duplicate_reference_prefix' does not have full type annotations for arguments or return type. |
| L1940 | ⚪ Info | Style (Missing Type Hints) | Function '_read_sfnt_name_records' does not have full type annotations for arguments or return type. |
| L2004 | ⚪ Info | Style (Missing Type Hints) | Function '_get_font_name_records' does not have full type annotations for arguments or return type. |
| L2096 | ⚪ Info | Style (Missing Type Hints) | Function '_filter_font_files' does not have full type annotations for arguments or return type. |
| L2123 | ⚪ Info | Style (Missing Type Hints) | Function 'select_primary_font' does not have full type annotations for arguments or return type. |
| L2137 | ⚪ Info | Code Smell (Leftover Print) | print() statement found in core file 'shared.py'. Use logging or structured UI messages. |
| L2384 | ⚪ Info | Style (Missing Type Hints) | Function 'is_latin_word' does not have full type annotations for arguments or return type. |
| L2415 | ⚪ Info | Style (Missing Type Hints) | Function 'tag_latin_words' does not have full type annotations for arguments or return type. |
| L3922 | ⚪ Info | Style (Missing Type Hints) | Function 'generate_font_styles' does not have full type annotations for arguments or return type. |
| L3923 | ⚪ Info | Style (Missing Type Hints) | Function '_build_faces' does not have full type annotations for arguments or return type. |

### `tests/conftest.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L3 | ⚪ Info | Style (Missing Type Hints) | Function 'pytest_addoption' does not have full type annotations for arguments or return type. |
| L11 | ⚪ Info | Style (Missing Type Hints) | Function 'pytest_configure' does not have full type annotations for arguments or return type. |

### `tests/test_anomaly_audits.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L20 | ⚪ Info | Style (Missing Type Hints) | Function 'test_dictionary_loading' does not have full type annotations for arguments or return type. |
| L30 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_hyphenations' does not have full type annotations for arguments or return type. |
| L50 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_punctuation' does not have full type annotations for arguments or return type. |
| L65 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_ocr_residues' does not have full type annotations for arguments or return type. |
| L78 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_capitalization' does not have full type annotations for arguments or return type. |
| L88 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_unresolved_citations' does not have full type annotations for arguments or return type. |
| L96 | ⚪ Info | Style (Missing Type Hints) | Function 'test_check_structural_nesting' does not have full type annotations for arguments or return type. |

### `tests/test_bug_regressions.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L62 | ⚪ Info | Style (Missing Type Hints) | Function 'deep_merge' does not have full type annotations for arguments or return type. |
| L72 | ⚪ Info | Style (Missing Type Hints) | Function 'load_baselines' does not have full type annotations for arguments or return type. |
| L76 | ⚪ Info | Style (Missing Type Hints) | Function 'requested_volumes' does not have full type annotations for arguments or return type. |
| L92 | ⚪ Info | Style (Missing Type Hints) | Function 'budget_for' does not have full type annotations for arguments or return type. |
| L99 | ⚪ Info | Style (Missing Type Hints) | Function 'paths_for' does not have full type annotations for arguments or return type. |
| L115 | ⚪ Info | Style (Missing Type Hints) | Function 'test_primary_font_selection_uses_real_internal_family_names' does not have full type annotations for arguments or return type. |
| L138 | ⚪ Info | Style (Missing Type Hints) | Function 'test_mixed_font_directories_filter_to_body_family_faces' does not have full type annotations for arguments or return type. |
| L157 | ⚪ Info | Style (Missing Type Hints) | Function 'test_font_assets_exist_and_otf_metadata_is_readable' does not have full type annotations for arguments or return type. |
| L173 | ⚪ Info | Style (Missing Type Hints) | Function 'volume_intermediate' does not have full type annotations for arguments or return type. |
| L181 | ⚪ Info | Style (Missing Type Hints) | Function 'chapter_matching' does not have full type annotations for arguments or return type. |
| L190 | ⚪ Info | Style (Missing Type Hints) | Function 'epub_audit_result' does not have full type annotations for arguments or return type. |
| L198 | ⚪ Info | Style (Missing Type Hints) | Function 'text_integrity_result' does not have full type annotations for arguments or return type. |
| L208 | ⚪ Info | Style (Missing Type Hints) | Function 'epub_xhtml_text' does not have full type annotations for arguments or return type. |
| L223 | ⚪ Info | Style (Missing Type Hints) | Function 'test_polyglot_fallback_does_not_convert_english_prose' does not have full type annotations for arguments or return type. |
| L234 | ⚪ Info | Style (Missing Type Hints) | Function 'test_polyglot_fallback_converts_unambiguous_residue_only' does not have full type annotations for arguments or return type. |
| L247 | ⚪ Info | Style (Missing Type Hints) | Function 'test_empty_scripture_code_brackets_are_removed' does not have full type annotations for arguments or return type. |
| L254 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_footnote_marker_before_word_is_isolated' does not have full type annotations for arguments or return type. |
| L261 | ⚪ Info | Style (Missing Type Hints) | Function 'test_false_himself_footnote_overlap_becomes_second_list_item' does not have full type annotations for arguments or return type. |
| L278 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ages_song_of_solomon_marker_does_not_keep_stale_proverbs_book' does not have full type annotations for arguments or return type. |
| L292 | ⚪ Info | Style (Missing Type Hints) | Function 'test_residual_square_ages_codes_are_removed_before_scripture_refs' does not have full type annotations for arguments or return type. |
| L306 | ⚪ Info | Style (Missing Type Hints) | Function 'test_spaced_ordinal_markers_are_normalized_before_formatting' does not have full type annotations for arguments or return type. |
| L315 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_fragmented_ordinal_markers_are_normalized' does not have full type annotations for arguments or return type. |
| L327 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracketed_word_ordinal_marker_splits_to_new_paragraph' does not have full type annotations for arguments or return type. |
| L338 | ⚪ Info | Style (Missing Type Hints) | Function 'test_inline_bold_decimal_markers_split_after_emphasized_semicolon' does not have full type annotations for arguments or return type. |
| L354 | ⚪ Info | Style (Missing Type Hints) | Function 'test_chapter_summary_continuations_stop_at_body_opener' does not have full type annotations for arguments or return type. |
| L367 | ⚪ Info | Style (Missing Type Hints) | Function 'test_secondly_the_opener_is_not_swallowed_by_summary' does not have full type annotations for arguments or return type. |
| L380 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_synopsis_line_continues_chapter_summary' does not have full type annotations for arguments or return type. |
| L393 | ⚪ Info | Style (Missing Type Hints) | Function 'test_analysis_spillover_is_moved_back_to_previous_chapter' does not have full type annotations for arguments or return type. |
| L412 | ⚪ Info | Style (Missing Type Hints) | Function 'test_chap_reference_continuation_paragraphs_are_merged' does not have full type annotations for arguments or return type. |
| L426 | ⚪ Info | Style (Missing Type Hints) | Function 'test_hebrew_inside_greek_span_is_retagged_separately' does not have full type annotations for arguments or return type. |
| L435 | ⚪ Info | Style (Missing Type Hints) | Function 'test_footnote_merge_translates_ages_verse_markers' does not have full type annotations for arguments or return type. |
| L448 | ⚪ Info | Style (Missing Type Hints) | Function 'test_i_will_and_i_am_are_not_forced_to_all_caps' does not have full type annotations for arguments or return type. |
| L459 | ⚪ Info | Style (Missing Type Hints) | Function 'test_parenthesized_scripture_refs_do_not_keep_opening_space' does not have full type annotations for arguments or return type. |
| L467 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ordinal_spacing_handles_bold_and_adverbial_forms' does not have full type annotations for arguments or return type. |
| L475 | ⚪ Info | Style (Missing Type Hints) | Function 'test_reference_and_scripture_false_breaks_are_healed' does not have full type annotations for arguments or return type. |
| L497 | ⚪ Info | Style (Missing Type Hints) | Function 'test_same_page_treatise_title_keeps_only_title_section' does not have full type annotations for arguments or return type. |
| L515 | ⚪ Info | Style (Missing Type Hints) | Function 'test_summary_continuation_is_rendered_as_one_summary_paragraph' does not have full type annotations for arguments or return type. |
| L539 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracketed_and_parenthesized_markers_split_and_bold_cleanly' does not have full type annotations for arguments or return type. |
| L564 | ⚪ Info | Style (Missing Type Hints) | Function 'test_quote_wrapped_structural_markers_are_unwrapped_and_bolded' does not have full type annotations for arguments or return type. |
| L579 | ⚪ Info | Style (Missing Type Hints) | Function 'test_sermon_fragmented_ordinal_marker_is_normalized' does not have full type annotations for arguments or return type. |
| L591 | ⚪ Info | Style (Missing Type Hints) | Function 'test_sermon_prefatory_dates_are_not_inline_structural_markers' does not have full type annotations for arguments or return type. |
| L617 | ⚪ Info | Style (Missing Type Hints) | Function 'test_sermon_prefatory_note_scripture_split_is_healed' does not have full type annotations for arguments or return type. |
| L631 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_quoted_objection_opener_moves_inside_blockquote' does not have full type annotations for arguments or return type. |
| L649 | ⚪ Info | Style (Missing Type Hints) | Function 'test_open_parenthesis_scripture_reference_is_closed_before_following_prose' does not have full type annotations for arguments or return type. |
| L659 | ⚪ Info | Style (Missing Type Hints) | Function 'test_duplicated_chapter_reference_noise_is_collapsed' does not have full type annotations for arguments or return type. |
| L670 | ⚪ Info | Style (Missing Type Hints) | Function 'test_contents_pages_split_parts_and_chapters_with_clean_labels' does not have full type annotations for arguments or return type. |
| L694 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_29_scholarly_citation_breaks_are_healed' does not have full type annotations for arguments or return type. |
| L723 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issues_37_to_40_textual_todo_regressions_are_guarded' does not have full type annotations for arguments or return type. |
| L741 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_39_combined_roman_decimal_marker_stays_inline' does not have full type annotations for arguments or return type. |
| L749 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_32_pdf_page_384_reference_run_is_not_jumbled' does not have full type annotations for arguments or return type. |
| L782 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_34_numbered_answer_anchor_is_normalized_and_bolded' does not have full type annotations for arguments or return type. |
| L790 | ⚪ Info | Style (Missing Type Hints) | Function 'test_spaced_scholastic_labels_are_repaired_globally' does not have full type annotations for arguments or return type. |
| L803 | ⚪ Info | Style (Missing Type Hints) | Function 'test_objection_and_use_labels_are_bolded_as_scholastic_anchors' does not have full type annotations for arguments or return type. |
| L813 | ⚪ Info | Style (Missing Type Hints) | Function 'test_question_followed_by_scripture_tail_stays_in_same_paragraph' does not have full type annotations for arguments or return type. |
| L826 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_33_shared_treatise_starter_pages_are_split_in_intermediate' does not have full type annotations for arguments or return type. |
| L866 | ⚪ Info | Style (Missing Type Hints) | Function 'test_v2_same_page_part_entries_do_not_duplicate_chapter_one' does not have full type annotations for arguments or return type. |
| L898 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_33_shared_treatise_starter_pages_are_not_title_styled_in_epub' does not have full type annotations for arguments or return type. |
| L1017 | ⚪ Info | Style (Missing Type Hints) | Function 'test_v1_catechism_questions_and_answers_are_grouped_and_bolded' does not have full type annotations for arguments or return type. |
| L1072 | ⚪ Info | Style (Missing Type Hints) | Function 'test_blockquote_geometry_renders_quotes_without_promoting_body_wraps' does not have full type annotations for arguments or return type. |
| L1127 | ⚪ Info | Style (Missing Type Hints) | Function 'test_roman_markers_render_left_aligned_without_marker_escaping' does not have full type annotations for arguments or return type. |
| L1174 | ⚪ Info | Style (Missing Type Hints) | Function 'test_list_item_announcer_syllabus_is_flattened' does not have full type annotations for arguments or return type. |
| L1188 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_29_scholarly_citation_splits_do_not_recur_in_epub' does not have full type annotations for arguments or return type. |
| L1216 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_32_page_384_reference_run_does_not_recur_in_epub' does not have full type annotations for arguments or return type. |
| L1253 | ⚪ Info | Style (Missing Type Hints) | Function 'test_known_text_integrity_bug_classes_do_not_regress' does not have full type annotations for arguments or return type. |
| L1348 | ⚪ Info | Style (Missing Type Hints) | Function 'test_known_epub_bug_classes_do_not_regress' does not have full type annotations for arguments or return type. |
| L1421 | ⚪ Info | Style (Missing Type Hints) | Function 'test_implemented_bug_samples_stay_absent' does not have full type annotations for arguments or return type. |
| L1448 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_21_dangling_initial_pair_is_joined' does not have full type annotations for arguments or return type. |
| L1478 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_21_chap_roman_numeral_not_merged' does not have full type annotations for arguments or return type. |
| L1491 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_21_structural_dash_roman_not_merged' does not have full type annotations for arguments or return type. |
| L1504 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_21_multi_volume_known_cases' does not have full type annotations for arguments or return type. |
| L1537 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_22_hebrew_css_uses_bidi_isolate' does not have full type annotations for arguments or return type. |
| L1549 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_22_hebrew_keri_bracket_outside_span' does not have full type annotations for arguments or return type. |
| L1568 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_23_blockquote_css_is_compact' does not have full type annotations for arguments or return type. |
| L1582 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_23_blockquote_p_margin_is_compact' does not have full type annotations for arguments or return type. |
| L1609 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_semicolon_list_merged_into_single_paragraph' does not have full type annotations for arguments or return type. |
| L1636 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_long_items_with_semicolons_still_merge' does not have full type annotations for arguments or return type. |
| L1649 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_period_terminated_items_stay_separate' does not have full type annotations for arguments or return type. |
| L1662 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_heterogeneous_run_splits_correctly' does not have full type annotations for arguments or return type. |
| L1694 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19d_last_item_without_bold_marker_no_nested_p' does not have full type annotations for arguments or return type. |
| L1711 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_roman_list_single_word_items_merge' does not have full type annotations for arguments or return type. |
| L1724 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_roman_list_semicolon_run_merges' does not have full type annotations for arguments or return type. |
| L1740 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_19_roman_list_does_not_merge_with_arabic_run' does not have full type annotations for arguments or return type. |
| L1758 | ⚪ Info | Style (Missing Type Hints) | Function 'test_detect_signature_pattern_3b_from_my_study' does not have full type annotations for arguments or return type. |
| L1769 | ⚪ Info | Style (Missing Type Hints) | Function 'test_detect_signature_pattern_6b_city_month_year' does not have full type annotations for arguments or return type. |
| L1778 | ⚪ Info | Style (Missing Type Hints) | Function 'test_coalesce_jo_three_line_signature' does not have full type annotations for arguments or return type. |
| L1795 | ⚪ Info | Style (Missing Type Hints) | Function 'test_coalesce_whg_two_line_signature' does not have full type annotations for arguments or return type. |
| L1810 | ⚪ Info | Style (Missing Type Hints) | Function 'test_coalesce_does_not_merge_unrelated_signatures' does not have full type annotations for arguments or return type. |
| L1823 | ⚪ Info | Style (Missing Type Hints) | Function 'test_coalesce_single_signature_unchanged' does not have full type annotations for arguments or return type. |
| L1834 | ⚪ Info | Style (Missing Type Hints) | Function 'test_owenian_link_as_emdash_merged_with_preceding' does not have full type annotations for arguments or return type. |
| L1843 | ⚪ Info | Style (Missing Type Hints) | Function 'test_owenian_link_for_emdash_merged_with_preceding' does not have full type annotations for arguments or return type. |
| L1851 | ⚪ Info | Style (Missing Type Hints) | Function 'test_owenian_link_does_not_merge_at_document_start' does not have full type annotations for arguments or return type. |
| L1863 | ⚪ Info | Style (Missing Type Hints) | Function 'test_list_items_joined_by_and_merge' does not have full type annotations for arguments or return type. |
| L1875 | ⚪ Info | Style (Missing Type Hints) | Function 'test_list_items_joined_by_or_merge' does not have full type annotations for arguments or return type. |
| L1885 | ⚪ Info | Style (Missing Type Hints) | Function 'test_connector_merge_does_not_swallow_following_item' does not have full type annotations for arguments or return type. |
| L1907 | ⚪ Info | Style (Missing Type Hints) | Function 'test_list_items_period_terminated_still_stay_separate' does not have full type annotations for arguments or return type. |
| L1923 | ⚪ Info | Style (Missing Type Hints) | Function 'test_tail_signature_split_from_body_paragraph' does not have full type annotations for arguments or return type. |
| L1936 | ⚪ Info | Style (Missing Type Hints) | Function 'test_jo_full_single_paragraph_gets_three_line_split' does not have full type annotations for arguments or return type. |
| L1953 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bold_list_anchor_preserved_after_for_comma' does not have full type annotations for arguments or return type. |
| L1964 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bold_list_anchor_preserved_after_i_say_comma' does not have full type annotations for arguments or return type. |
| L1971 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bold_verse_continuation_number_still_unbolded' does not have full type annotations for arguments or return type. |
| L1984 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_for_comma_merges_onto_preceding_paragraph' does not have full type annotations for arguments or return type. |
| L2002 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_as_comma_merges_onto_preceding_paragraph' does not have full type annotations for arguments or return type. |
| L2015 | ⚪ Info | Style (Missing Type Hints) | Function 'test_for_emdash_in_roman_heading_stays_on_heading' does not have full type annotations for arguments or return type. |
| L2038 | ⚪ Info | Style (Missing Type Hints) | Function 'test_contents_last_chapter_before_next_treatise_heading' does not have full type annotations for arguments or return type. |
| L2072 | ⚪ Info | Style (Missing Type Hints) | Function 'test_front_matter_prose_hyphen_to_emdash_is_repaired' does not have full type annotations for arguments or return type. |
| L2082 | ⚪ Info | Style (Missing Type Hints) | Function 'test_front_matter_prose_comma_hyphen_emdash_repaired' does not have full type annotations for arguments or return type. |
| L2089 | ⚪ Info | Style (Missing Type Hints) | Function 'test_front_matter_prose_list_anchors_are_bold' does not have full type annotations for arguments or return type. |
| L2098 | ⚪ Info | Style (Missing Type Hints) | Function 'test_general_preface_v1_renders_without_standalone_for_comma' does not have full type annotations for arguments or return type. |
| L2127 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_47a_colon_hyphen_at_eol_repaired' does not have full type annotations for arguments or return type. |
| L2135 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_47a_semicolon_hyphen_at_eol_repaired' does not have full type annotations for arguments or return type. |
| L2143 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_47b_paragraph_opening_hyphen_before_quote_repaired' does not have full type annotations for arguments or return type. |
| L2150 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_47_existing_word_hyphen_not_disturbed' does not have full type annotations for arguments or return type. |
| L2157 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_47_existing_comma_hyphen_eol_still_repaired' does not have full type annotations for arguments or return type. |
| L2168 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48_colon_para_merges_onto_first_list_item' does not have full type annotations for arguments or return type. |
| L2183 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48_list_item_class_preserved_for_downstream_merge' does not have full type annotations for arguments or return type. |
| L2205 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48_no_match_when_para_ends_with_non_colon' does not have full type annotations for arguments or return type. |
| L2216 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48_existing_list_item_not_treated_as_intro' does not have full type annotations for arguments or return type. |
| L2231 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48a_fused_roman_items_split_in_raw_text' does not have full type annotations for arguments or return type. |
| L2244 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48a_split_does_not_fire_on_spaced_roman_items' does not have full type annotations for arguments or return type. |
| L2255 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48a_lib_cap_reference_not_split' does not have full type annotations for arguments or return type. |
| L2264 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_48a_single_word_roman_rule_a_guard' does not have full type annotations for arguments or return type. |
| L2291 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_49_missing_period_repaired_by_v1_overrides' does not have full type annotations for arguments or return type. |
| L2303 | ⚪ Info | Style (Missing Type Hints) | Function 'test_issue_49_period_not_doubled_when_already_present' does not have full type annotations for arguments or return type. |
| L2317 | ⚪ Info | Style (Missing Type Hints) | Function 'test_titlepage_override_preserves_greek_epigraph' does not have full type annotations for arguments or return type. |
| L2340 | ⚪ Info | Style (Missing Type Hints) | Function 'test_titlepage_override_does_not_duplicate_existing_foreign_text' does not have full type annotations for arguments or return type. |
| L2353 | ⚪ Info | Style (Missing Type Hints) | Function 'test_titlepage_override_unchanged_when_no_foreign_text' does not have full type annotations for arguments or return type. |
| L2370 | ⚪ Info | Style (Missing Type Hints) | Function 'test_mid_sentence_before_blockquote_is_merged' does not have full type annotations for arguments or return type. |
| L2387 | ⚪ Info | Style (Missing Type Hints) | Function 'test_content_word_before_blockquote_is_merged' does not have full type annotations for arguments or return type. |
| L2400 | ⚪ Info | Style (Missing Type Hints) | Function 'test_prepositional_tail_before_blockquote_is_merged' does not have full type annotations for arguments or return type. |
| L2413 | ⚪ Info | Style (Missing Type Hints) | Function 'test_comma_ending_intro_does_not_merge_with_blockquote' does not have full type annotations for arguments or return type. |
| L2428 | ⚪ Info | Style (Missing Type Hints) | Function 'test_closed_quote_ending_before_blockquote_not_merged' does not have full type annotations for arguments or return type. |
| L2447 | ⚪ Info | Style (Missing Type Hints) | Function 'test_render_repair_mid_sentence_blockquote_strips_marker' does not have full type annotations for arguments or return type. |
| L2464 | ⚪ Info | Style (Missing Type Hints) | Function 'test_render_repair_leaves_comma_intro_untouched' does not have full type annotations for arguments or return type. |
| L2479 | ⚪ Info | Style (Missing Type Hints) | Function 'test_render_repair_mid_sentence_used_in_full_pipeline' does not have full type annotations for arguments or return type. |
| L2498 | ⚪ Info | Style (Missing Type Hints) | Function 'test_comma_introduced_flat_syllabus_absorbed' does not have full type annotations for arguments or return type. |
| L2518 | ⚪ Info | Style (Missing Type Hints) | Function 'test_closed_sentence_gate_prevents_false_positives' does not have full type annotations for arguments or return type. |
| L2548 | ⚪ Info | Style (Missing Type Hints) | Function 'test_apply_premium_salutations' does not have full type annotations for arguments or return type. |
| L2578 | ⚪ Info | Style (Missing Type Hints) | Function 'test_apply_premium_chapter_endings' does not have full type annotations for arguments or return type. |
| L2594 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ocr_bold_and_paragraph_healing' does not have full type annotations for arguments or return type. |
| L2634 | ⚪ Info | Style (Missing Type Hints) | Function 'test_simon_magus_casing_normalization' does not have full type annotations for arguments or return type. |
| L2653 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_spacing_cleanup' does not have full type annotations for arguments or return type. |
| L2670 | ⚪ Info | Style (Missing Type Hints) | Function 'test_latin_dedication_translation_matching' does not have full type annotations for arguments or return type. |
| L2686 | ⚪ Info | Style (Missing Type Hints) | Function 'test_latin_word_tagging' does not have full type annotations for arguments or return type. |
| L2712 | ⚪ Info | Style (Missing Type Hints) | Function 'test_cardo_gentium_style_overrides' does not have full type annotations for arguments or return type. |
| L2726 | ⚪ Info | Style (Missing Type Hints) | Function 'test_citation_abbrev_split_false_positive' does not have full type annotations for arguments or return type. |
| L2739 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nav_xhtml_double_wrap_prevention' does not have full type annotations for arguments or return type. |
| L2751 | ⚪ Info | Style (Missing Type Hints) | Function 'test_latin_ocr_repairs' does not have full type annotations for arguments or return type. |
| L2776 | ⚪ Info | Style (Missing Type Hints) | Function 'test_latin_inline_translations' does not have full type annotations for arguments or return type. |
| L2800 | ⚪ Info | Style (Missing Type Hints) | Function 'get_volume_overrides' does not have full type annotations for arguments or return type. |
| L2814 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_unwhitelisted_split_word_anomalies_in_json' does not have full type annotations for arguments or return type. |
| L2867 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_unused_whitelist_entries' does not have full type annotations for arguments or return type. |

### `tests/test_config_hardening.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L4 | ⚪ Info | Style (Missing Type Hints) | Function 'test_volume_config_deep_merges_nested_override_maps' does not have full type annotations for arguments or return type. |
| L21 | ⚪ Info | Style (Missing Type Hints) | Function 'test_volume_config_merge_does_not_mutate_shared_defaults' does not have full type annotations for arguments or return type. |

### `tests/test_epub_structure.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L78 | ⚪ Info | Style (Missing Type Hints) | Function 'test_chapter_files_have_at_most_two_h1_elements' does not have full type annotations for arguments or return type. |
| L106 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_empty_paragraph_elements' does not have full type annotations for arguments or return type. |
| L125 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_raw_markdown_bold_in_xhtml' does not have full type annotations for arguments or return type. |
| L153 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_spans_have_correct_lang_attributes' does not have full type annotations for arguments or return type. |
| L180 | ⚪ Info | Style (Missing Type Hints) | Function 'test_hebrew_spans_have_correct_lang_and_dir_attributes' does not have full type annotations for arguments or return type. |
| L218 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nav_has_no_duplicate_chapter_entries' does not have full type annotations for arguments or return type. |
| L257 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nav_entry_lengths_are_within_apple_books_limit' does not have full type annotations for arguments or return type. |
| L293 | ⚪ Info | Style (Missing Type Hints) | Function 'test_all_nav_hrefs_resolve_to_files_in_epub' does not have full type annotations for arguments or return type. |
| L339 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nav_chapter_count_is_plausible' does not have full type annotations for arguments or return type. |
| L366 | ⚪ Info | Style (Missing Type Hints) | Function 'test_html_classes_are_defined_in_main_css' does not have full type annotations for arguments or return type. |
| L420 | ⚪ Info | Style (Missing Type Hints) | Function 'test_all_spine_items_appear_in_nav' does not have full type annotations for arguments or return type. |
| L479 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_duplicate_raw_toc_in_chapters' does not have full type annotations for arguments or return type. |

### `tests/test_footnote_integrity.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L131 | ⚪ Info | Style (Missing Type Hints) | Function 'test_endnotes_file_exists_in_epub' does not have full type annotations for arguments or return type. |
| L156 | ⚪ Info | Style (Missing Type Hints) | Function 'test_every_noteref_href_resolves_to_an_endnote_anchor' does not have full type annotations for arguments or return type. |
| L204 | ⚪ Info | Style (Missing Type Hints) | Function 'test_every_endnote_has_a_back_link_noteref' does not have full type annotations for arguments or return type. |
| L239 | ⚪ Info | Style (Missing Type Hints) | Function 'test_endnote_ids_are_sequential_and_start_at_one' does not have full type annotations for arguments or return type. |
| L270 | ⚪ Info | Style (Missing Type Hints) | Function 'test_endnote_text_is_free_of_extraction_artifacts' does not have full type annotations for arguments or return type. |
| L311 | ⚪ Info | Style (Missing Type Hints) | Function 'test_noteref_count_matches_endnote_count' does not have full type annotations for arguments or return type. |
| L342 | ⚪ Info | Style (Missing Type Hints) | Function 'test_intermediate_footnote_count_matches_epub_endnote_count' does not have full type annotations for arguments or return type. |

### `tests/test_gideon_mapping.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L17 | ⚪ Info | Style (Missing Type Hints) | Function 'test_observed_gideon_span_characters_are_mapped' does not have full type annotations for arguments or return type. |
| L22 | ⚪ Info | Style (Missing Type Hints) | Function 'test_gideon_mapping_outputs_only_hebrew_marks_and_allowed_spacing' does not have full type annotations for arguments or return type. |
| L33 | ⚪ Info | Style (Missing Type Hints) | Function 'test_known_ages_gideon_samples_convert_without_legacy_residue' does not have full type annotations for arguments or return type. |
| L52 | ⚪ Info | Style (Missing Type Hints) | Function 'test_corpus_gideon_character_inventory_has_no_unmapped_warning_residue' does not have full type annotations for arguments or return type. |

### `tests/test_golden_pages.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L27 | ⚪ Info | Style (Missing Type Hints) | Function 'load_golden_pages' does not have full type annotations for arguments or return type. |
| L36 | ⚪ Info | Style (Missing Type Hints) | Function 'test_golden_pages' does not have full type annotations for arguments or return type. |
| L92 | ⚪ Info | Style (Missing Type Hints) | Function 'test_page_continuation_healing' does not have full type annotations for arguments or return type. |

### `tests/test_greek_extraction_hardening.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L5 | ⚪ Info | Style (Missing Type Hints) | Function 'test_koine_subset_font_names_are_converted' does not have full type annotations for arguments or return type. |
| L11 | ⚪ Info | Style (Missing Type Hints) | Function 'test_unicode_greek_page_uses_font_aware_path' does not have full type annotations for arguments or return type. |
| L39 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_clause_audit_does_not_join_across_english_prose' does not have full type annotations for arguments or return type. |

### `tests/test_structural_standardization.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L12 | ⚪ Info | Style (Missing Type Hints) | Function 'test_structural_tokens_preserve_hierarchy' does not have full type annotations for arguments or return type. |
| L26 | ⚪ Info | Style (Missing Type Hints) | Function 'test_drop_cap_constraint' does not have full type annotations for arguments or return type. |
| L45 | ⚪ Info | Style (Missing Type Hints) | Function 'test_front_matter_states' does not have full type annotations for arguments or return type. |
| L54 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_artifact_stripping' does not have full type annotations for arguments or return type. |
| L64 | ⚪ Info | Style (Missing Type Hints) | Function 'test_blockquote_token_renders_as_semantic_blockquote' does not have full type annotations for arguments or return type. |
| L74 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_blockquote_prefix_renders_as_semantic_blockquote' does not have full type annotations for arguments or return type. |
| L83 | ⚪ Info | Style (Missing Type Hints) | Function 'test_adjacent_blockquote_tokens_merge_until_sentence_terminal' does not have full type annotations for arguments or return type. |
| L101 | ⚪ Info | Style (Missing Type Hints) | Function 'test_blockquote_geometry_uses_body_left_edge_not_modal_indent' does not have full type annotations for arguments or return type. |
| L110 | ⚪ Info | Style (Missing Type Hints) | Function 'line' does not have full type annotations for arguments or return type. |
| L177 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_anchor_does_not_bold_answer_in_prose' does not have full type annotations for arguments or return type. |
| L201 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_anchor_handles_answer_with_numeral' does not have full type annotations for arguments or return type. |
| L217 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_anchor_does_not_bold_objection_inside_blockquote' does not have full type annotations for arguments or return type. |
| L234 | ⚪ Info | Style (Missing Type Hints) | Function 'test_solution_label_is_bolded_correctly' does not have full type annotations for arguments or return type. |
| L251 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_y_repair_in_reconstruct' does not have full type annotations for arguments or return type. |
| L263 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_e_repair_does_not_affect_legitimate_brackets' does not have full type annotations for arguments or return type. |
| L275 | ⚪ Info | Style (Missing Type Hints) | Function 'test_spaced_caps_i_will_normalisation' does not have full type annotations for arguments or return type. |
| L288 | ⚪ Info | Style (Missing Type Hints) | Function 'test_i_am_normalisation_preserves_context' does not have full type annotations for arguments or return type. |
| L301 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_a_dot_not_treated_as_qa_in_prose_context' does not have full type annotations for arguments or return type. |
| L314 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_a_dot_is_treated_as_qa_in_catechism_context' does not have full type annotations for arguments or return type. |
| L326 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_context_resets_per_chapter_no_bleed' does not have full type annotations for arguments or return type. |
| L352 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_context_detected_from_title' does not have full type annotations for arguments or return type. |
| L368 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_context_detected_from_raw_text' does not have full type annotations for arguments or return type. |

### `tests/test_structural_symmetry.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L59 | 🟡 Warning | Code Smell (Long Function) | Function 'test_structural_symmetry_and_sequential_completeness' is 234 lines long (exceeds recommended max of 150 lines). Consider modularizing. |
| L59 | ⚪ Info | Style (Missing Type Hints) | Function 'test_structural_symmetry_and_sequential_completeness' does not have full type annotations for arguments or return type. |

### `tests/test_text_fidelity.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L102 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_y_artifact_is_repaired_to_ly' does not have full type annotations for arguments or return type. |
| L109 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_e_artifact_is_repaired_to_le' does not have full type annotations for arguments or return type. |
| L115 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bracket_corruption_does_not_touch_scripture_brackets' does not have full type annotations for arguments or return type. |
| L122 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_a_period_before_lowercase_is_stripped' does not have full type annotations for arguments or return type. |
| L155 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_list_marker_space_inserted' does not have full type annotations for arguments or return type. |
| L177 | ⚪ Info | Style (Missing Type Hints) | Function 'test_bare_a_period_before_uppercase_is_preserved' does not have full type annotations for arguments or return type. |
| L196 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ocr_zero_to_o_at_line_start' does not have full type annotations for arguments or return type. |
| L219 | ⚪ Info | Style (Missing Type Hints) | Function 'test_trailing_lone_hyphen_becomes_em_dash' does not have full type annotations for arguments or return type. |
| L240 | ⚪ Info | Style (Missing Type Hints) | Function 'test_for_comma_hyphen_mid_sentence_becomes_emdash' does not have full type annotations for arguments or return type. |
| L263 | ⚪ Info | Style (Missing Type Hints) | Function 'test_reconstruct_paragraphs_heals_false_break_without_losing_words' does not have full type annotations for arguments or return type. |
| L288 | ⚪ Info | Style (Missing Type Hints) | Function 'test_coincidental_repeated_phrase_with_greek_is_not_collapsed' does not have full type annotations for arguments or return type. |
| L319 | ⚪ Info | Style (Missing Type Hints) | Function 'test_genuine_interrupted_duplicate_clause_is_still_removed' does not have full type annotations for arguments or return type. |
| L364 | ⚪ Info | Style (Missing Type Hints) | Function 'test_theological_term_survives_clean_text' does not have full type annotations for arguments or return type. |
| L383 | ⚪ Info | Style (Missing Type Hints) | Function 'test_structural_tokens_do_not_survive_markdown_to_html' does not have full type annotations for arguments or return type. |
| L404 | ⚪ Info | Style (Missing Type Hints) | Function 'test_literal_footnote_markers_do_not_survive_markdown_to_html' does not have full type annotations for arguments or return type. |
| L425 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ages_double_hyphen_is_not_introduced_by_clean_text' does not have full type annotations for arguments or return type. |
| L435 | ⚪ Info | Style (Missing Type Hints) | Function 'test_ordinal_spacing_no_orphan_period' does not have full type annotations for arguments or return type. |
| L457 | ⚪ Info | Style (Missing Type Hints) | Function 'test_clean_text_expands_scripture_abbreviations' does not have full type annotations for arguments or return type. |
| L469 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scripture_ref_with_chapter_only_is_not_mangled' does not have full type annotations for arguments or return type. |
| L480 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_footnote_marker_is_isolated' does not have full type annotations for arguments or return type. |
| L487 | ⚪ Info | Style (Missing Type Hints) | Function 'test_parenthesized_scripture_ref_strips_leading_space' does not have full type annotations for arguments or return type. |
| L498 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_labels_in_normal_sentence_are_not_bolded' does not have full type annotations for arguments or return type. |
| L521 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_sequence_all_three_labels_bolded' does not have full type annotations for arguments or return type. |
| L536 | ⚪ Info | Style (Missing Type Hints) | Function 'test_use_label_with_numeral_is_bolded' does not have full type annotations for arguments or return type. |
| L549 | ⚪ Info | Style (Missing Type Hints) | Function 'test_digression_heading_renders_as_h3' does not have full type annotations for arguments or return type. |
| L570 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_raw_pipeline_tokens_in_epub' does not have full type annotations for arguments or return type. |
| L590 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_literal_footnote_markers_in_epub_text' does not have full type annotations for arguments or return type. |
| L607 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_ages_boilerplate_in_epub' does not have full type annotations for arguments or return type. |
| L630 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_double_spaces_in_paragraph_text' does not have full type annotations for arguments or return type. |
| L648 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_consecutive_duplicate_words_in_epub' does not have full type annotations for arguments or return type. |
| L679 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_orphaned_beta_code_in_epub' does not have full type annotations for arguments or return type. |
| L699 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_empty_bracket_noise_in_epub' does not have full type annotations for arguments or return type. |
| L721 | ⚪ Info | Style (Missing Type Hints) | Function 'test_paragraphs_do_not_start_lowercase_unless_continuation' does not have full type annotations for arguments or return type. |
| L760 | ⚪ Info | Style (Missing Type Hints) | Function 'test_no_double_punctuation_in_epub' does not have full type annotations for arguments or return type. |
| L781 | ⚪ Info | Style (Missing Type Hints) | Function 'test_theological_vocabulary_present_in_epub' does not have full type annotations for arguments or return type. |
| L807 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_open_bracket_prefix_is_stripped' does not have full type annotations for arguments or return type. |
| L821 | ⚪ Info | Style (Missing Type Hints) | Function 'test_greek_bracket_strip_does_not_affect_list_markers' does not have full type annotations for arguments or return type. |
| L839 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_single_word_labels_absorbed' does not have full type annotations for arguments or return type. |
| L863 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_semicolon_items_absorbed' does not have full type annotations for arguments or return type. |
| L881 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_short_phrase_run_absorbed' does not have full type annotations for arguments or return type. |
| L901 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_twofold_account_pair_absorbed' does not have full type annotations for arguments or return type. |
| L921 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_long_items_stay_block' does not have full type annotations for arguments or return type. |
| L941 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_prefix_absorbed_before_long_expansion' does not have full type annotations for arguments or return type. |
| L969 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_two_item_prefix_attaches_before_expansion' does not have full type annotations for arguments or return type. |
| L994 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_parallel_gloss_pair_attaches_before_expansion' does not have full type annotations for arguments or return type. |
| L1020 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_binary_account_pair_attaches_before_expansion' does not have full type annotations for arguments or return type. |
| L1044 | ⚪ Info | Style (Missing Type Hints) | Function 'test_orphaned_flat_list_marker_tail_joins_short_next_paragraph' does not have full type annotations for arguments or return type. |
| L1060 | ⚪ Info | Style (Missing Type Hints) | Function 'test_inline_roman_section_splits_to_subheading_before_flat_list' does not have full type annotations for arguments or return type. |
| L1088 | ⚪ Info | Style (Missing Type Hints) | Function 'test_owenian_list_levels_mark_exposition_and_nested_subpoints' does not have full type annotations for arguments or return type. |
| L1127 | ⚪ Info | Style (Missing Type Hints) | Function 'test_owenian_local_ordinals_get_deeper_reader_level' does not have full type annotations for arguments or return type. |
| L1141 | ⚪ Info | Style (Missing Type Hints) | Function 'test_flat_syllabus_attaches_to_long_parent_list_item_anchor' does not have full type annotations for arguments or return type. |
| L1179 | ⚪ Info | Style (Missing Type Hints) | Function 'test_observation_label_rendered_bold_by_scholastic_anchor' does not have full type annotations for arguments or return type. |
| L1196 | ⚪ Info | Style (Missing Type Hints) | Function 'test_observation_full_word_label_is_recognised' does not have full type annotations for arguments or return type. |
| L1210 | ⚪ Info | Style (Missing Type Hints) | Function 'test_prefatory_note_heading_suppressed_in_sermon_volume' does not have full type annotations for arguments or return type. |
| L1227 | ⚪ Info | Style (Missing Type Hints) | Function 'test_prefatory_note_heading_present_in_treatise_volume' does not have full type annotations for arguments or return type. |
| L1244 | ⚪ Info | Style (Missing Type Hints) | Function 'test_verse_number_after_comma_not_bold' does not have full type annotations for arguments or return type. |
| L1262 | ⚪ Info | Style (Missing Type Hints) | Function 'test_verse_number_multi_digit_after_comma_not_bold' does not have full type annotations for arguments or return type. |
| L1275 | ⚪ Info | Style (Missing Type Hints) | Function 'test_plus_immediately_before_greek_is_stripped' does not have full type annotations for arguments or return type. |
| L1287 | ⚪ Info | Style (Missing Type Hints) | Function 'test_brace_immediately_before_greek_is_stripped' does not have full type annotations for arguments or return type. |
| L1295 | ⚪ Info | Style (Missing Type Hints) | Function 'test_plus_before_latin_is_not_stripped_by_clean_greek_text' does not have full type annotations for arguments or return type. |
| L1310 | ⚪ Info | Style (Missing Type Hints) | Function 'test_stray_plus_after_punctuation_stripped_from_body' does not have full type annotations for arguments or return type. |
| L1326 | ⚪ Info | Style (Missing Type Hints) | Function 'test_double_space_normalised_to_single' does not have full type annotations for arguments or return type. |
| L1342 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_nine_word_item_absorbed' does not have full type annotations for arguments or return type. |
| L1368 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_flat_list_thirteen_word_item_stays_block' does not have full type annotations for arguments or return type. |
| L1402 | ⚪ Info | Style (Missing Type Hints) | Function 'test_first_blockquote_in_sermon_volume_gets_opening_scripture_class' does not have full type annotations for arguments or return type. |
| L1430 | ⚪ Info | Style (Missing Type Hints) | Function 'test_first_blockquote_in_treatise_volume_has_no_opening_scripture_class' does not have full type annotations for arguments or return type. |
| L1448 | ⚪ Info | Style (Missing Type Hints) | Function 'test_opening_scripture_class_resets_on_new_chapter' does not have full type annotations for arguments or return type. |
| L1475 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_f_short_binary_label_still_flattens' does not have full type annotations for arguments or return type. |
| L1497 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_f_long_binary_exposition_stays_block' does not have full type annotations for arguments or return type. |
| L1523 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_f_border_case_at_twenty_words_flattens' does not have full type annotations for arguments or return type. |
| L1554 | ⚪ Info | Style (Missing Type Hints) | Function 'test_syllabus_anchor_class_added_to_plain_p_on_absorption' does not have full type annotations for arguments or return type. |
| L1578 | ⚪ Info | Style (Missing Type Hints) | Function 'test_syllabus_anchor_class_added_to_list_item_anchor_on_absorption' does not have full type annotations for arguments or return type. |
| L1601 | ⚪ Info | Style (Missing Type Hints) | Function 'test_syllabus_anchor_class_not_added_when_no_absorption' does not have full type annotations for arguments or return type. |
| L1627 | ⚪ Info | Style (Missing Type Hints) | Function 'test_long_list_item_anchor_with_count_pattern_allows_attachment' does not have full type annotations for arguments or return type. |
| L1658 | ⚪ Info | Style (Missing Type Hints) | Function 'test_formula_tail_these_following_allows_attachment' does not have full type annotations for arguments or return type. |
| L1680 | ⚪ Info | Style (Missing Type Hints) | Function 'test_formula_tail_i_shall_observe_allows_attachment' does not have full type annotations for arguments or return type. |
| L1699 | ⚪ Info | Style (Missing Type Hints) | Function 'test_formula_tail_may_be_considered_allows_attachment' does not have full type annotations for arguments or return type. |
| L1718 | ⚪ Info | Style (Missing Type Hints) | Function 'test_long_anchor_under_80_words_without_pattern_allows_attachment' does not have full type annotations for arguments or return type. |
| L1743 | ⚪ Info | Style (Missing Type Hints) | Function 'test_anchor_over_80_words_without_pattern_blocks_attachment' does not have full type annotations for arguments or return type. |
| L1773 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_g_ordinal_continuation_attaches_to_preceding_inline_ordinal' does not have full type annotations for arguments or return type. |
| L1809 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_g_does_not_fire_without_preceding_inline_ordinal' does not have full type annotations for arguments or return type. |
| L1831 | ⚪ Info | Style (Missing Type Hints) | Function 'test_split_ordinal_inline_expansions_splits_at_first_em_ordinal' does not have full type annotations for arguments or return type. |
| L1866 | ⚪ Info | Style (Missing Type Hints) | Function 'test_split_ordinal_inline_expansions_no_split_for_short_intro' does not have full type annotations for arguments or return type. |
| L1884 | ⚪ Info | Style (Missing Type Hints) | Function 'test_continuation_chain_last_item_joins_when_previous_ends_with_connector' does not have full type annotations for arguments or return type. |
| L1908 | ⚪ Info | Style (Missing Type Hints) | Function 'test_continuation_chain_last_item_joins_when_previous_ends_with_comma' does not have full type annotations for arguments or return type. |
| L1928 | ⚪ Info | Style (Missing Type Hints) | Function 'test_semicolon_chain_last_item_joins_when_previous_ends_with_semicolon' does not have full type annotations for arguments or return type. |
| L1970 | ⚪ Info | Style (Missing Type Hints) | Function 'test_semicolon_chain_long_final_item_without_preceding_semicolon_stays_block' does not have full type annotations for arguments or return type. |
| L1995 | ⚪ Info | Style (Missing Type Hints) | Function 'test_all_non_final_semi_absorbs_when_all_items_end_with_semicolon' does not have full type annotations for arguments or return type. |
| L2026 | ⚪ Info | Style (Missing Type Hints) | Function 'test_all_non_final_semi_does_not_fire_when_items_exceed_20w_cap' does not have full type annotations for arguments or return type. |
| L2051 | ⚪ Info | Style (Missing Type Hints) | Function 'test_backslash_artifact_stripped_before_lowercase_word' does not have full type annotations for arguments or return type. |
| L2065 | ⚪ Info | Style (Missing Type Hints) | Function 'test_backslash_artifact_not_stripped_before_uppercase' does not have full type annotations for arguments or return type. |
| L2080 | ⚪ Info | Style (Missing Type Hints) | Function 'test_backslash_artifact_not_stripped_when_preceded_by_word_char' does not have full type annotations for arguments or return type. |
| L2098 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_h_absorbs_preview_syllabus_with_medium_items' does not have full type annotations for arguments or return type. |
| L2135 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_h_does_not_fire_when_item_exceeds_25w' does not have full type annotations for arguments or return type. |
| L2157 | ⚪ Info | Style (Missing Type Hints) | Function 'test_signal_h_does_not_fire_for_two_item_list' does not have full type annotations for arguments or return type. |
| L2183 | ⚪ Info | Style (Missing Type Hints) | Function 'test_allcaps_ordinal_normalized_to_titlecase' does not have full type annotations for arguments or return type. |
| L2217 | ⚪ Info | Style (Missing Type Hints) | Function 'test_allcaps_ordinal_not_normalized_mid_sentence' does not have full type annotations for arguments or return type. |
| L2230 | ⚪ Info | Style (Missing Type Hints) | Function 'test_allcaps_ordinal_multiline_normalizes_each_start' does not have full type annotations for arguments or return type. |
| L2244 | ⚪ Info | Style (Missing Type Hints) | Function 'test_structural_start_re_matches_higher_ordinals' does not have full type annotations for arguments or return type. |
| L2265 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_table_converted_to_blockquote_plain_pairs' does not have full type annotations for arguments or return type. |
| L2289 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_table_with_preceding_unclosed_blockquote' does not have full type annotations for arguments or return type. |
| L2318 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_table_br_tags_converted_to_spaces' does not have full type annotations for arguments or return type. |
| L2335 | ⚪ Info | Style (Missing Type Hints) | Function 'test_markdown_table_non_table_paragraph_unchanged' does not have full type annotations for arguments or return type. |
| L2347 | ⚪ Info | Style (Missing Type Hints) | Function 'test_try_breath_ocr_repaired_to_thy_breath' does not have full type annotations for arguments or return type. |
| L2357 | ⚪ Info | Style (Missing Type Hints) | Function 'test_try_ways_ocr_repaired_to_thy_ways' does not have full type annotations for arguments or return type. |
| L2367 | ⚪ Info | Style (Missing Type Hints) | Function 'test_try_not_repaired_outside_biblical_phrase' does not have full type annotations for arguments or return type. |
| L2381 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_secondly_split_into_two_paragraphs' does not have full type annotations for arguments or return type. |
| L2393 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_thirdly_fourthly_split' does not have full type annotations for arguments or return type. |
| L2407 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_ordinal_blockquote_not_split' does not have full type annotations for arguments or return type. |
| L2416 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_ordinal_already_split_unchanged' does not have full type annotations for arguments or return type. |
| L2425 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_ordinal_no_ordinal_unchanged' does not have full type annotations for arguments or return type. |
| L2433 | ⚪ Info | Style (Missing Type Hints) | Function 'test_fused_lastly_split' does not have full type annotations for arguments or return type. |
| L2448 | ⚪ Info | Style (Missing Type Hints) | Function 'test_stray_bold_marker_after_comma_stripped' does not have full type annotations for arguments or return type. |
| L2458 | ⚪ Info | Style (Missing Type Hints) | Function 'test_stray_bold_marker_after_semicolon_stripped' does not have full type annotations for arguments or return type. |
| L2468 | ⚪ Info | Style (Missing Type Hints) | Function 'test_valid_bold_not_stripped' does not have full type annotations for arguments or return type. |
| L2477 | ⚪ Info | Style (Missing Type Hints) | Function 'test_apri_ocr_fix_before_day_number' does not have full type annotations for arguments or return type. |
| L2487 | ⚪ Info | Style (Missing Type Hints) | Function 'test_apri_not_changed_without_day_number' does not have full type annotations for arguments or return type. |
| L2497 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_anchors_are_nested_in_owen_level_2' does not have full type annotations for arguments or return type. |
| L2514 | ⚪ Info | Style (Missing Type Hints) | Function 'test_scholastic_parent_child_differentiation' does not have full type annotations for arguments or return type. |
| L2537 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nesting_cap_beyond_level_3_remains_flat' does not have full type annotations for arguments or return type. |
| L2549 | ⚪ Info | Style (Missing Type Hints) | Function 'test_dynamic_trigger_based_demotion' does not have full type annotations for arguments or return type. |
| L2588 | ⚪ Info | Style (Missing Type Hints) | Function 'test_blockquote_trailing_quote_preservation' does not have full type annotations for arguments or return type. |
| L2607 | ⚪ Info | Style (Missing Type Hints) | Function 'test_flat_list_continuation_splits' does not have full type annotations for arguments or return type. |
| L2623 | ⚪ Info | Style (Missing Type Hints) | Function 'test_stray_quotes_before_scripture_reference' does not have full type annotations for arguments or return type. |
| L2640 | ⚪ Info | Style (Missing Type Hints) | Function 'test_list_nesting_lookahead_termination' does not have full type annotations for arguments or return type. |
| L2664 | ⚪ Info | Style (Missing Type Hints) | Function 'test_nesting_precedence_fix' does not have full type annotations for arguments or return type. |

### `tests/test_unresolved_citations.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L89 | ⚪ Info | Style (Missing Type Hints) | Function 'get_available_volumes' does not have full type annotations for arguments or return type. |
| L112 | ⚪ Info | Style (Missing Type Hints) | Function 'test_unresolved_citation_budgets' does not have full type annotations for arguments or return type. |
| L141 | ⚪ Info | Style (Missing Type Hints) | Function 'test_untranslated_prose_footnotes' does not have full type annotations for arguments or return type. |
| L183 | ⚪ Info | Style (Missing Type Hints) | Function 'test_untranslated_prose_body' does not have full type annotations for arguments or return type. |

### `tests/test_v1_pipeline_regression.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L56 | ⚪ Info | Style (Missing Type Hints) | Function 'test_for_comma_hyphen_becomes_emdash' does not have full type annotations for arguments or return type. |
| L59 | ⚪ Info | Style (Missing Type Hints) | Function 'test_thus_comma_hyphen_becomes_emdash' does not have full type annotations for arguments or return type. |
| L62 | ⚪ Info | Style (Missing Type Hints) | Function 'test_wherefore_comma_hyphen_becomes_emdash' does not have full type annotations for arguments or return type. |
| L65 | ⚪ Info | Style (Missing Type Hints) | Function 'test_trailing_space_after_hyphen_also_fixed' does not have full type annotations for arguments or return type. |
| L68 | ⚪ Info | Style (Missing Type Hints) | Function 'test_real_hyphen_in_word_not_touched' does not have full type annotations for arguments or return type. |
| L73 | ⚪ Info | Style (Missing Type Hints) | Function 'test_em_dash_in_prose_not_doubled' does not have full type annotations for arguments or return type. |
| L88 | ⚪ Info | Style (Missing Type Hints) | Function 'test_a_before_lowercase_in_body_prose_stripped' does not have full type annotations for arguments or return type. |
| L96 | ⚪ Info | Style (Missing Type Hints) | Function 'test_a_before_uppercase_in_body_prose_preserved' does not have full type annotations for arguments or return type. |
| L102 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_a_label_is_bolded_in_catechism_context' does not have full type annotations for arguments or return type. |
| L109 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_context_does_not_bleed_across_chapters' does not have full type annotations for arguments or return type. |
| L128 | ⚪ Info | Style (Missing Type Hints) | Function 'test_jo_bare_initials_detected' does not have full type annotations for arguments or return type. |
| L131 | ⚪ Info | Style (Missing Type Hints) | Function 'test_jo_spaced_initials_detected' does not have full type annotations for arguments or return type. |
| L134 | ⚪ Info | Style (Missing Type Hints) | Function 'test_from_my_study_standalone_detected' does not have full type annotations for arguments or return type. |
| L138 | ⚪ Info | Style (Missing Type Hints) | Function 'test_september_the_last_detected' does not have full type annotations for arguments or return type. |
| L142 | ⚪ Info | Style (Missing Type Hints) | Function 'test_whg_bare_initials_detected' does not have full type annotations for arguments or return type. |
| L145 | ⚪ Info | Style (Missing Type Hints) | Function 'test_edinburgh_month_year_detected' does not have full type annotations for arguments or return type. |
| L149 | ⚪ Info | Style (Missing Type Hints) | Function 'test_plain_prose_not_a_signature' does not have full type annotations for arguments or return type. |
| L155 | ⚪ Info | Style (Missing Type Hints) | Function 'test_john_owen_allcaps_in_front_matter' does not have full type annotations for arguments or return type. |
| L158 | ⚪ Info | Style (Missing Type Hints) | Function 'test_allcaps_name_NOT_detected_in_body' does not have full type annotations for arguments or return type. |
| L172 | ⚪ Info | Style (Missing Type Hints) | Function 'test_jo_three_line_coalesced' does not have full type annotations for arguments or return type. |
| L186 | ⚪ Info | Style (Missing Type Hints) | Function 'test_whg_two_line_coalesced' does not have full type annotations for arguments or return type. |
| L196 | ⚪ Info | Style (Missing Type Hints) | Function 'test_body_text_between_signatures_blocks_merge' does not have full type annotations for arguments or return type. |
| L208 | ⚪ Info | Style (Missing Type Hints) | Function 'test_body_text_surrounding_signature_unchanged' does not have full type annotations for arguments or return type. |
| L230 | ⚪ Info | Style (Missing Type Hints) | Function 'test_non_catechism_chapter_after_catechism_chapter_no_bleed' does not have full type annotations for arguments or return type. |
| L242 | ⚪ Info | Style (Missing Type Hints) | Function 'test_catechism_config_true_wraps_in_catechism_item' does not have full type annotations for arguments or return type. |
| L259 | ⚪ Info | Style (Missing Type Hints) | Function 'test_period_terminated_items_not_merged' does not have full type annotations for arguments or return type. |
| L270 | ⚪ Info | Style (Missing Type Hints) | Function 'test_semicolon_terminated_items_are_merged' does not have full type annotations for arguments or return type. |
| L289 | ⚪ Info | Style (Missing Type Hints) | Function 'test_chapter_token_produces_h1' does not have full type annotations for arguments or return type. |
| L295 | ⚪ Info | Style (Missing Type Hints) | Function 'test_summary_token_produces_chapter_summary' does not have full type annotations for arguments or return type. |
| L301 | ⚪ Info | Style (Missing Type Hints) | Function 'test_part_token_produces_h1_primary' does not have full type annotations for arguments or return type. |

### `volumes/h1/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L67 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h2/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L59 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h3/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L58 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h4/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L65 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h5/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L54 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h6/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L81 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/h7/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L99 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v1/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L70 | ⚪ Info | Style (Missing Type Hints) | Function '_normalize_v1_catechism_paragraph' does not have full type annotations for arguments or return type. |
| L142 | ⚪ Info | Style (Missing Type Hints) | Function '_postprocess_v1_html' does not have full type annotations for arguments or return type. |
| L380 | ⚪ Info | Style (Missing Type Hints) | Function '_v1_heading_caps_text' does not have full type annotations for arguments or return type. |
| L408 | ⚪ Info | Style (Missing Type Hints) | Function '_postprocess_v1_chapter_summaries' does not have full type annotations for arguments or return type. |
| L572 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v10/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L240 | ⚪ Info | Style (Missing Type Hints) | Function 'post_extract_hook' does not have full type annotations for arguments or return type. |
| L275 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v11/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L190 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v12/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L117 | ⚪ Info | Style (Missing Type Hints) | Function 'post_extract_hook' does not have full type annotations for arguments or return type. |
| L309 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v13/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L325 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v14/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L215 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v15/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L280 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v16/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L379 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v2/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L173 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v3/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L103 | ⚪ Info | Style (Missing Type Hints) | Function 'html_postprocess_hook' does not have full type annotations for arguments or return type. |
| L176 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v4/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L219 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v5/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L161 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v6/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L172 | ⚪ Info | Style (Missing Type Hints) | Function 'post_extract_hook' does not have full type annotations for arguments or return type. |
| L176 | ⚪ Info | Style (Missing Type Hints) | Function 'move_tail' does not have full type annotations for arguments or return type. |
| L253 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v7/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L149 | ⚪ Info | Style (Missing Type Hints) | Function 'html_postprocess_hook' does not have full type annotations for arguments or return type. |
| L234 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v8/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L157 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

### `volumes/v9/convert.py`

| Line | Severity | Check Type | Description |
|---|---|---|---|
| L150 | ⚪ Info | Style (Missing Type Hints) | Function 'main' does not have full type annotations for arguments or return type. |

## Next Steps

2. **Refactor Code Smells (Recommended)**: Decompose functions exceeding 150 lines, avoid catching base exceptions, and reduce arguments on large functions.
3. **Validate Rebuilds**: Once fixes are applied, rebuild the volume using `volumes/vN/convert.py` and run tests `pytest tests/` to confirm correctness.
