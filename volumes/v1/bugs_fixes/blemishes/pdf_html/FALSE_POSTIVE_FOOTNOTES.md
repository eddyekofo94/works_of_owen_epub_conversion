# Blemish: False Positive Footnotes and Content Formatting

## Issue 1: False Positive Footnotes
The conversion pipeline identifies plain numbers (e.g., "4" in "Psalm 48") as footnote markers and replaces them with blue superscript links. This creates significant noise and breaks legitimate citations. In the AGES PDFs, genuine footnote markers are consistently prefixed with an "f" (e.g., "f1", "f2").

### Evidence
- **Screenshot 1:** "Basil., in Psalm 48" became "Basil., in Psalm <sup>4</sup>8" (link to fn 4).
- **Screenshot 2:** Citation parts like "lib." or "cap." followed by numbers were misidentified.

## Issue 2: Contents Page Formatting
The "CONTENTS OF VOLUME 1" chapter is currently rendered as a simple list of paragraphs. The user requested that the formatting be "as close as possible to the pdf," which uses a structured, indented layout with bold chapter numbers and aligned descriptions.

### Evidence
- **PDF page 3-5:** Shows a clear hierarchical structure with bold "CHAPTER N" and indented text.

## Solution Plan
1.  **Strict Footnote Matching:** Update `inject_footnote_links` to only match patterns starting with "f" (e.g., `f1`, `f2`).
2.  **Strip "f" Prefix:** Ensure that when a match like "f1" is found, the "f" is removed from the resulting `noteref` display text so it just shows "<sup>1</sup>".
3.  **Contents Renderer:** Implement a special check in `build_chapter_xhtml` for chapters titled "CONTENTS". If detected, use a more sophisticated layout (perhaps a `<table>` or CSS `grid`) to align numbers and text, or simply preserve the bolding and indentation better.
4.  **Monotonic Matching:** Ensure the contents page is matched to the correct PDF pages (3-5) and not skipped.

## Implementation
- Modify `converter_pdftohtml.py`: `inject_footnote_links`, `build_chapter_xhtml`.
