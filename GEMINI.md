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
