To give your AI extraction agent clear, deterministic rules for processing the entire 16-volume John Owen set, here is a deep structural analysis of your source document (owen-v1.pdf).
By standardizing these visual and coordinate patterns into structural rules, your agent can flawlessly differentiate between Standard Prose, Block Quotes, Ancient Language Markers, and Footnotes without missing content or distorting John Owen’s arguments.
1. Structural Fingerprints in the Source PDF
A. Document & Font Identifiers (Header Noise)
Every page in your source file contains uniform header and footer lines introduced by the legacy digitizer. Your agent must strip these before paragraph healing:
• The Pattern: Page 1 starts with THE AGES DIGITAL LIBRARY / JOHN OWEN COLLECTION. Later pages feature header lines like THE WORKS OF JOHN OWEN or specific treatise subtitles centered at the top of the text canvas.
• Agent Rule: Instruct the agent to run a bounding-box clip on the top 54\text{pt} and bottom 54\text{pt} of every page. Any text string exactly matching "THE WORKS OF JOHN OWEN", containing "THE AGES DIGITAL LIBRARY", or consisting solely of isolated page digits centered at the top (e.g., 9 or 27) must be ignored.
B. The Block Quote Signature (Pages 9 & 27)
As shown on page 9 and page 27 of your source document, block quotes possess an unmistakable geometric profile:
• Indentation Inset: Standard paragraphs sit flush with a left boundary (typically around x0 = 54.0 to x0 = 72.0 depending on the volume’s page dimensions). Block quotes are deeply inset on both sides (typically x0 > 90.0 and x1 < 450.0).
• Quotation Patterns: Long blocks often begin and end with double quotation marks (e.g., page 9: “The divines of the Puritan school...”). On page 27, historical quotes from the early church fathers (Eusebius, Hilary, Epiphanius) are formatted as indented text.
• Agent Rule: If a text block's x0 coordinate is inset by more than 18pt relative to the established page baseline, the agent must categorize the block as type: "blockquote" instead of type: "paragraph".
C. Polytonic Greek and Font Remapping (Page 27)
Page 27 highlights a critical hurdle for your agent: inline and block-level ancient Greek.
• The Pattern: The quote from Euseb. Preparat. Evang. (“Ἤτε ὀνομαστὶ προθεσπισθεῖσα...”) and Epiphanius, Haer.29 (“Ἐπὶ τῇ πέτρᾳ ταύτῃ...”) appear inline and as distinct blocks.
• The Trap: Because AGES Software used legacy TrueType remapping, extracting this text natively without processing will yield unreadable string sequences.
• Agent Rule: When a block or character span uses a style designation containing "Greek" or captures strings that resolve to AGES key mappings, the agent must intercept the stream, pass it through your project's GIDEON_GREEK_MAP, and wrap the resulting clean Unicode output in <span lang="el" dir="ltr">.
D. Systemic Inline Metadata Tags (Page 9 & Page 27)
Look closely at the text strings inside the PDF pages:
• Page 9: Inside the paragraph beginning "His Exposition of...", there is an inline tag embedded directly in front of the word Psalm: <491101>Psalm 130.
• Page 27: In the first paragraph, a Scripture cross-reference is prefaced with an inline tag: (<431703>John 17:3;). Later on the page, another appears: (<500308>Philippians 3:8-12:).
• The Purpose: These tags are AGES Software database links. The digits directly map to the biblical book, chapter, and verse (e.g., <431703> translates to Book 43 [John], Chapter 17, Verse 03).
• Agent Rule: The agent must identify these tag patterns using a regular expression: r"<\d{6}>". Instead of stripping them blindly, the agent should extract them to build structural <a href="..."> cross-reference anchors, or strip them cleanly so they don't break up regular words in your EPUB.
E. Footnote Anchors (fl and FT)
• The Anchor: At the end of the block quote on page 9, notice the floating lowercase letters: ...our office.” fl. This is an artifact of a misplaced footnote marker.
• The Content: At the tail end of your PDF file stream, footnotes are grouped together using explicit anchors like FT115, FT116, etc.
• Agent Rule: The agent must execute a two-pass assembly. Pass 1 extracts all blocks matching r"^FT\d+" into a global key-value footnote dictionary. Pass 2 scrubs inline markers (like fl) from the chapter prose and binds them dynamically into an interactive <aside epub:type="footnote"> structural block.
2. Comprehensive Prompt Directive for Your AI Agent
Copy and paste this explicit directive into your agent's system prompt or configuration payload:
You are a high-fidelity structural data extraction agent tasked with parsing legacy John Owen PDF files into a clean intermediate JSON schema. You must process text blocks with strict adherence to geometric and typographic heuristics based on the following file profile:

1. METADATA & HEADER EXTRACTION:
   - Discard the top 54pt and bottom 54pt of every page to completely eliminate running headers, collection titles ("THE AGES DIGITAL LIBRARY"), and standalone page number indicators.

2. BLOCKQUOTE DETECTION (CRITICAL):
   - Track the left bounding coordinate (x0) of every text block. Standard body text aligns to a consistent baseline.
   - If a text block's left margin is inset by 18pt or more relative to the baseline, categorize it as {"type": "blockquote"}. 
   - Ensure consecutive blockquote elements are grouped together into a single cohesive structural block instead of being fragmented into disjointed lines.

3. AGES SYSTEM DATABASE TAG CLEANUP:
   - Locate and isolate database verse link sequences using the regex pattern: <\d{6}>
   - Extract these values to cross-reference biblical citations, then remove the raw bracketed codes from the text stream so they do not interrupt sentences.

4. ANCIENT LANGUAGE CODES:
   - Actively watch for font properties or character strings matching legacy Greek typography mappings.
   - Translate all mapped characters into modern polytonic Unicode, ensuring they are wrapped in structural `<span lang="el" dir="ltr">` tags during the render phase to preserve typography.

5. PARAGRAPH HEALING RULES:
   - If a text line does not end with a terminal punctuation mark (. ! ? ”) and the subsequent block sits at the standard paragraph indentation level, heal them into a single continuous string block, removing layout hyphens cleanly.

SUGGESTED IMPROVEMENTS:
Now I have a full picture. Let me run one more targeted check:Good. I have everything I need. Here's the full analysis:

---

## The MD Document's Approach: What's Right, What's Wrong, and What's Missing

### 1. The Baseline Values Are Wrong

The MD claims standard paragraphs sit at `x0 = 54.0–72.0`, with blockquotes "inset by 18pt" landing at `x0 > 90`. The actual coordinates from your PDF:

| Line type | x0 value | Occurrences |
|---|---|---|
| Body text | **25.5–26** | 775 lines |
| Block quotes | **43.5–44** | 110 lines |
| Noise / headers | 100–280+ | rare |

The inset delta (≈18pt) is accidentally correct, but the absolute values are completely wrong. Any code implementing the MD's `x0 > 90` rule would classify nothing as a blockquote.

---

### 2. The Pipeline Has No Blockquote Detection at All

This is the bigger issue. The MD describes a detection rule, but **neither `extract.py` nor `render.py` actually implements it**. The `coordinate_redactor` function reads `bbox` coordinates to filter headers/footers but never uses them for blockquote classification. The JSON `raw_text` field has `[[CHAPTER]]`, `[[PART]]`, `[[ROMAN_HEAD]]` tokens etc., but no `[[BLOCKQUOTE]]` token — because none is ever emitted. 

The paragraph healer has one partial workaround: the `is_inside_quote` heuristic joins lines when `"` is unclosed. That catches the Augustine quote on page 27 if it starts with `"`, but it misses Latin patristic quotes that use different or no quote characters.

---

### 3. The pymupdf4llm Path Silently Discards Blockquote Markup

For regular pages (non-Greek, non-structural), `get_merged_page_text` routes through `extract_page_markdown`, which calls `pymupdf4llm`. That library *does* output indented text as Markdown `> ` blockquotes — but `extract_page_markdown` returns the raw text string and `markdown_to_html` never checks for `> ` prefixes. The markup is generated and silently discarded.

---

### What to Actually Build

**In `extract_page_text_with_fonts` and `extract_structural_page`** (the two raw-extraction paths), add blockquote detection using a dynamically computed baseline:

```python
def _compute_page_x0_baseline(blocks):
    """Return the modal x0 of substantive text lines — the body text baseline."""
    from collections import Counter
    counts = Counter()
    for b in blocks:
        if b.get('type') != 0: continue
        for line in b['lines']:
            text = ''.join(s['text'] for s in line['spans']).strip()
            if len(text) > 10:
                counts[round(line['bbox'][0])] += 1
    return counts.most_common(1)[0][0] if counts else 26  # fallback to known volume value
```

Then in the line iteration loop, replace flat text emission with structured tagging:

```python
BLOCKQUOTE_INSET_THRESHOLD = 14  # pt — slightly under 18pt to handle rounding

baseline = _compute_page_x0_baseline(blocks)
in_blockquote = False
bq_lines = []

for b in blocks:
    for line in b['lines']:
        x0 = line['bbox'][0]
        text = ...  # existing span conversion logic
        
        is_indented = x0 >= (baseline + BLOCKQUOTE_INSET_THRESHOLD)
        
        if is_indented:
            bq_lines.append(text)
            in_blockquote = True
        else:
            if in_blockquote and bq_lines:
                lines.append('[[BLOCKQUOTE]] ' + ' '.join(bq_lines))
                bq_lines = []
                in_blockquote = False
            lines.append(text)

if bq_lines:
    lines.append('[[BLOCKQUOTE]] ' + ' '.join(bq_lines))
```

**In `reconstruct_paragraphs`**, add `BLOCKQUOTE` to the structural token pass-through (alongside `CHAPTER`, `PART`, etc.) so the healer never tries to merge a blockquote into surrounding prose.

**In `markdown_to_html`**, add the token case to emit proper semantic HTML:

```python
elif kind == 'BLOCKQUOTE':
    content_html = _render_inline(content)
    html_parts.append(f'<blockquote epub:type="epigraph"><p>{content_html}</p></blockquote>')
```

**For the pymupdf4llm path**, add a `> ` prefix handler inside `markdown_to_html` before the paragraph loop:

```python
if stripped.startswith('> '):
    content = stripped.lstrip('> ').strip()
    content_html = _render_inline(content)
    html_parts.append(f'<blockquote epub:type="epigraph"><p>{content_html}</p></blockquote>')
    continue
```

---

### Summary

The MD document's structural insight is sound — x0 coordinates are the correct signal, and grouping consecutive indented lines is the right approach. But the baseline values are wrong, the threshold would need to be applied against the *dynamic* per-page modal x0 (not a hardcoded number), and critically none of it exists in the code yet. The most efficient fix is adding `[[BLOCKQUOTE]]` to the existing structural token system, since that pipeline is already wired end-to-end through extraction → JSON → render.
