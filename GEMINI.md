# Project Mandates — John Owen Works Conversion

## Workflow & Documentation
- **Validation Requirement:** NEVER update the status of an issue or task as "Finished", "Fixed", or "Done" in any changelog or status log (e.g., `BUGS_AND_FIXES.md`) unless the change has been explicitly validated and approved by the user. Use "IMPLEMENTED (AWAITING VALIDATION)".
- **Engineering Log:** Detailed technical post-mortems and architectural deep-dives must be recorded in `ENGINEERING_LOG.md` for all complex issues (Issue 40+).
- **Reporting:** Always provide a summary of the implemented fix and wait for a validation directive before marking the item as resolved in the project documentation.

## Technical Mandates
1.  **Paragraph Healing:** All volumes MUST use the holistic `reconstruct_paragraphs` logic (verified in Issue 42) to prevent sentence fragmentation across page boundaries.
2.  **Chapter Processing:** Chapters spanning multiple PDF pages must be merged in their raw state before cleaning or healing to ensure seamless sentence reconstruction.
3.  **Layout Preservation:** Healer logic must protect list items (using `list_item_re`) and avoid joining lines that follow terminal punctuation unless they start with a lowercase character.
4.  **Premium Aesthetics:** Adhere strictly to the Blue/Green/Italic hierarchy defined in `shared.py` for all front matter and headings.
5.  **Architectural Separation (Overrides):** Volume-specific data (OCR `text_replacements`, custom paragraph hooks, or local formatting logic) MUST reside within each volume's designated converter (e.g., `volumes/v1/convert.py`) using the `OVERRIDES` dictionary. Base scripts (`shared.py`, `extract.py`, `render.py`) must remain generic to avoid bloat and maintain a clean collection-wide pipeline.
6.  **Greek/Hebrew Preservation:** Deduplication and overlap-removal functions MUST include Greek (`\u0370-\u03FF\u1F00-\u1FFF`) and Hebrew (`\u0590-\u05FF`) Unicode ranges in word-matching regexes. Failure to do so causes false-positive ghost detection that drops entire Greek clauses.
7.  **AGES Koine Encoding:** The AGES Koine font uses non-standard Beta Code mappings:
    - `c` = chi (χ), `x` = xi (ξ) — opposite of standard Beta Code
    - `Y` = upsilon (Υ), `y` = psi (ψ) — uppercase Y is upsilon, not psi
    - `v` = final sigma (ς) — explicit final sigma marker
8.  **Per-Volume Script Requirement:** Always use `volumes/vN/convert.py` for testing and rebuilding. The legacy `converter.py` does not pass volume-specific `OVERRIDES` to the render pipeline, so EPUBs built with it will miss volume-specific OCR corrections.
