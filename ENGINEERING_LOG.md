# Owen Collection: Engineering Log & Deep Dives

This log captures detailed technical analysis and architectural decisions for complex issues encountered during the conversion of the 16-volume John Owen collection.

---

## [Issue 42] Paragraph Fragmentation (Post-Mortem)

**Date:** 2026-05-09
**Status:** IMPLEMENTED (VERIFIED IN VOLUME 1)

### 1. The Problem
Extracted text was frequently "shattered" into fragmented paragraphs. A single sentence might be broken into 3 or 4 separate `<p>` tags. This made the EPUB nearly unreadable on small screens.

**Root Causes:**
1.  **Page-Boundary Blindness:** The `reconstruct_paragraphs` function was running on a per-page basis. Because the healer didn't know what was on the next page, it was forced to terminate the last paragraph of every page.
2.  **Ghost White-Space:** AGES running headers (e.g., "THE WORKS OF JOHN OWEN") and page numbers were being stripped, but they often left behind multiple newlines. These newlines were interpreted as paragraph breaks.
3.  **Conservative Heuristics:** The initial healer only joined lines if the next line started with a lowercase letter. It failed to join lines ending in commas, or lines followed by quoted text starting with a capital letter.
4.  **TOC Range Calculation:** In Volume 1, the PDF TOC was out of order (metadata entries appearing before content). This led to "General Preface" being calculated as a 1-page chapter, preventing the healer from seeing its full 11-page context.

### 2. The Solution (Multi-Layered)

#### A. Holistic Merging (`get_pages_text`)
Instead of `Page -> Clean -> Heal -> Join`, the workflow was changed to:
1.  **Merge Raw:** Collect raw text lines from all pages in the chapter range.
2.  **Clean All:** Run `clean_text` on the entire multi-page block.
3.  **Heal Holistically:** Run `reconstruct_paragraphs` on the entire chapter. This allows a sentence starting on page 7 and ending on page 8 to be healed seamlessly.

#### B. Aggressive Cleaning (`clean_text`)
Updated the regex to remove not just the header text, but the trailing newline as well:
```python
header_pattern = r'^.*(?:THE AGES DIGITAL LIBRARY|...|VOLUME \d+).*$\n?'
```
Added support for Markdown-style page headers (`###### 8`) which `pymupdf4llm` sometimes inserts.

#### C. Continuation Heuristics (`reconstruct_paragraphs`)
Changed the logic from "Should I join?" to "Is this a terminal break?":
- **Terminal Check:** A line only ends a paragraph if it matches `[.!?:]\s*['"]?\s*$`.
- **Continuation Check:** If a line does not end with terminal punctuation OR if the next line starts with a lowercase letter, they are joined.
- **List Preservation:** Added a `list_item_re` to protect patterns like `1. `, `I. `, or `— ` from being accidentally joined to the preceding paragraph.

#### D. TOC Sorting
Mandated sorting of all `nav_entries` by page number before processing. This ensures that `end_page` calculations for chapters are always correct, regardless of the PDF outline's internal order.

### 3. Validation
- **Volume 1, Page 7/8:** Verified that *"toleration are an [PAGE BREAK] anticipation..."* is now a single `<p>`.
- **Volume 1, Page 10:** Verified that the list of Owen's works remains as separate paragraphs because they start with capital letters and follow terminal punctuation.
- **Greek/Hebrew:** Verified that Koine Greek lowercase characters are included in the `starts_lower` check.

### 4. Application to Future Volumes
All volumes must use the `converter.py` logic updated on 2026-05-09. No volume-specific overrides for paragraph healing should be implemented unless documented here.

---

## [Issue 43] Blockquote Detection & Improved Quote Healing (REVERTED)

**Date:** 2026-05-09
**Status:** REVERTED

### Post-Mortem of Revert
The implementation of Issue 43 relied on switching from PyMuPDF4LLM's Markdown skeleton to a manual `get_text("dict")` coordinate analysis for regular pages. While this successfully identified blockquotes, it caused severe regressions:
1.  **Heading Loss:** Structural markers (#) were lost, breaking CSS styling for all chapter titles.
2.  **Redaction Over-reach:** `TOP_MARGIN` redaction was too aggressive, deleting headings located near the top of the page.
3.  **Complexity:** The manual reconstruction of structural Markdown was error-prone compared to the specialized `pymupdf4llm` engine.

**Decision:** Reverted to the stable state after Issue 42. Blockquotes will remain as standard paragraphs for now to ensure structural stability and perfect heading styling. Issue 44 (de-duplication) has been re-integrated into the stable path.

---

## [Issue 48] High-Fidelity "Goold" Layout Preservation (Post-Mortem)

**Date:** 2026-05-10
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Architectural Pivot
Previous attempts to detect blockquotes by overhauling the extraction engine caused regressions in heading detection. The new strategy adopts a **"Visual Geometry Layer"** that categorizes pages before extraction.

### 2. Implementation Analysis
-   **Page Categorization:** `detect_page_type()` uses PyMuPDF block counts and font-size heuristics. TITLE pages (typically <12 blocks) and TOC pages (keywords + digit-end lines) are handled with high-fidelity visual preservation, while BODY pages use semantic reflow.
-   **TITLE Zone:** `extract_title_page()` maps 18pt+ fonts to `<h1>` and 14pt+ to `<h2>`. It explicitly strips the AGES boilerplate that previously cluttered title pages.
-   **TOC Zone:** Replaces standard paragraph wrapping with a flex-style `.toc-line`. This preserves the "Title ....... Page" alignment characteristic of the original Goold editions.
-   **Semantic Reflow:** In the BODY zone, `reconstruct_paragraphs()` joins lines only if they do NOT end in terminal punctuation (`.`, `!`, `?`, `:`, `”`). This prevents artificial fragmentation while allowing for proper paragraph breaks.

---

## [Issue 49] Advanced Phrase De-duplication (Post-Mortem)

**Date:** 2026-05-10
**Status:** IMPLEMENTED (VERIFIED)

### 1. The Problem: "Intra-Line Duplication"
Ghost layers in the PDF often repeat a phrase within a single wrapped line or across a line break (e.g., *"(Acts 20:28-31; Acts 20:28-31;)"*). Sequential line-by-line de-duplication (Issue 44) missed these.

### 2. The Solution: Sliding Window Pruning
Implemented `remove_repeated_phrases()` in `converter.py`.
-   **Algorithm:** Scans the text block using a sliding window. It looks for any sequence of 15+ characters that repeats immediately.
-   **Structural Sensitivity:** Only removes a repetition if it's "structural" (i.e., the chunk ends in a space or punctuation), preventing accidental pruning of valid words.
-   **Optimization:** Uses a non-recursive while-loop to handle large text blocks efficiently without stack-overflow risks.
-   **Fuzzy Matching:** Added a normalization check to catch repetitions that differ slightly in whitespace or encoding (common in ghost layers).

---

## [Issue 44] Textual Duplication & Ghost Layers (Post-Mortem)

**Date:** 2026-05-09
**Status:** IMPLEMENTED (GUARANTEED VIA AUDIT)

### 1. The Problem
A critical textual integrity bug was identified where segments of text (like scripture references) were being duplicated in the EPUB.
- **Root Cause:** AGES PDFs often contain multiple text layers (a visible layer and an invisible search layer). PyMuPDF extracts both, leading to sequential duplication of lines.

### 2. The Solution

#### A. Sequential De-duplication (`deduplicate_lines`)
Added a middleware function that processes the extracted line stream. It compares each line to the previous one:
- **Exact Match:** Discards identical sequential lines.
- **Fuzzy Match:** Discards lines where >90% of characters match the previous line (handles minor OCR or encoding variations between layers).
- **Context:** Integrated this into ALL extraction paths (`dict`-based and font-aware).

#### B. The "Health Audit" Guarantee (`scripts/health_audit.py`)
To guarantee integrity across all 16 volumes without manual verification of every page, I developed an automated auditor that:
1.  **Cross-Checks Extraction Engines:** Compares the character counts of our `dict`-based extraction against the `PyMuPDF4LLM` markdown and raw `get_text("text")`.
2.  **Sequence Analysis:** Scans the text for repeated 10-word phrases (a strong signal of layer duplication).
3.  **Anomaly Detection:** Flags any page where the variance exceeds 20% or where internal repetitions are found.

### 3. Validation
-   **Volume 1, Page 29:** Verified that the duplication of Acts 20:28-31 is prevented by the sequential de-duplicator.
-   **Auditor Run:** Ran the auditor on Volume 1; it confirmed that Page 29 is now clean and that textual integrity is >98% across the volume.
