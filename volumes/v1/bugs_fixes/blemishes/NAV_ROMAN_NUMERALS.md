# Blemish: Redundant Roman Numeral NAV Entries (REVISED)

## Issue
The EPUB navigation menu (NAV) contains numerous entries that are simply Roman numerals (e.g., "I.", "II.", "III.", "IV."). These are internal sub-sections of chapters. Initially, these were filtered out, but the user prefers them to be included and properly nested within their respective sections for better organization.

## Evidence
- `ch033` ("IV.") appears after Chapter 18.
- `ch034` through `ch037` ("I.", "II.", "III.", "IV.") appear before Chapter 19.
- These should be children of their parent chapters in the Table of Contents.

## Solution Plan
1.  **Restore Roman Numeral Entries:** Stop filtering out titles that match the Roman numeral pattern.
2.  **Implement Hierarchical Nesting:**
    *   Identify titles that are solely Roman numerals (e.g., "I.", "IV.").
    *   Assign these entries to a deeper level in the TOC (e.g., `toc_level + 1`).
    *   Chapters (Level 2) will then act as parents to these sub-sections (Level 3).
3.  **Append Subtitles:** Continue using the subtitle extraction logic to provide descriptive labels for these sections where possible.
4.  **XML Validity:** The existing `generate_nav_xhtml` logic already handles multi-level nesting and tag closure.

## Implementation
- Modify the chapter loop in `converter.py` to assign Level 3 to Roman numeral sections while maintaining their natural order.
