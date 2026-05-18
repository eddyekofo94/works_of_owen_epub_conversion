# Roman Heading (`ROMAN_HEAD`) Technical Issue Report

## Overview
There are two interconnected problems currently preventing the correct extraction and rendering of Roman numeral subheadings in Volume 1 (and likely other volumes). 

1. **The Heuristic Problem:** Distinguishing between a Roman numeral that acts as a major section subheading (which should be centered) and a Roman numeral that is just a short list item (which should be left-aligned).
2. **The Escaping Problem:** Attempting to bold the Roman numerals during the HTML rendering phase results in double-escaping (e.g., `<h4 class="roman-subheading">&lt;b&gt;I.&lt;/b&gt; ... </h4>`).

---

## 1. The Heuristic Problem (Identification in `extract.py` and `render.py`)

### The Symptom
The text frequently uses Roman numerals (I., II., III.) for two completely different structural purposes:
*   **Major Subheadings:** "I. The first of these is, that he should have a nature provided for him..." -> This introduces a large section of text and should be styled as `<h4 class="roman-subheading">`.
*   **List Items:** 
    "I. Honor."
    "II. Obedience."
    "III. Conformity." -> These are short enumerations and should be styled as `<p class="roman-list-item">`.

### The Extraction Challenge (`extract.py`)
Currently, `extract.py` tries to identify Roman headings by looking for lines that start with Roman numerals. If it finds one, it tags it as `[[ROMAN_HEAD]]`. 
*   If we make the regex too strict (e.g., requiring it to be a standalone numeral `I.`), we miss headings that include text on the same line.
*   If we make the regex too loose, we accidentally tag short list items as `[[ROMAN_HEAD]]`.

### The Rendering Challenge (`render.py`)
When `render.py` processes the `[[ROMAN_HEAD]]` tag, it doesn't inherently know if it should be an `h4` or a `p`. 
*   We attempted to build a "density heuristic" (e.g., if the text is short and follows a sequence like I, II, III, make it a list item). 
*   This heuristic proved brittle because Front Matter lists behave differently than Body lists, and tracking the sequence state (`roman_list_expected`) across different paragraph processing loops led to inconsistent results.

---

## 2. The Escaping Problem (HTML Rendering in `render.py`)

### The Symptom
When the renderer decides a line is a Roman Heading, we want the numeral itself to be bolded, but the rest of the heading to be normal weight. 
Expected: `<h4 class="roman-subheading"><b>I.</b> The first of these...</h4>`
Actual output: `<h4 class="roman-subheading">&lt;b&gt;I.&lt;/b&gt; The first of these...</h4>`

### The Cause
The `render.py` script has a complex, multi-pass pipeline for sanitizing text and generating HTML.
1. `_html_escape()` is called to sanitize the raw markdown text.
2. `tag_unicode_ranges()` wraps Greek/Hebrew text in spans.
3. `emphasize_structural_prefix()` is called to wrap the Roman numeral in `<b>` tags or `<span class="marker">`.
4. However, because of the order of operations and subsequent string replacements or escapes in `markdown_to_html`, any literal HTML tags we inject (like `<b>`) end up being treated as plain text and get HTML-escaped into `&lt;b&gt;`.

### Failed Attempts to Fix
*   **Injecting early:** Fails because later passes escape it.
*   **Injecting late:** Fails because we lose the regex context of where the Roman numeral is.
*   **Post-processing string replace:** I attempted to add a final `body_html = body_html.replace('&lt;b&gt;', '<b>')` at the very end of `render_volume`. This also failed, suggesting the escaping is happening either at the `epublib` packaging level, or there is another hidden escape pass in the pipeline that I missed.

---

## Proposed Direction for Other Agents

To solve this, the next agent should investigate:

1. **For the Heuristic:** Instead of relying on sequence tracking, implement a simple word-count threshold during extraction. If a Roman numeral line has > 15 words, it's a heading. If < 15, it's a list item.
2. **For the Escaping:** Stop trying to inject literal `<b>` tags in the python string manipulation. Instead, output a unique, non-HTML markdown token (e.g., `**I.** The first...`) and rely on the existing markdown-to-HTML regex (`re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text_html)`) which runs later in the pipeline and is known to work safely without double-escaping.