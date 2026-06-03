# Project Mandates — John Owen Works Conversion

## Workflow & Documentation
- **Validation Requirement:** NEVER update the status of an issue or task as "Finished", "Fixed", or "Done" in any changelog or status log (e.g., `BUGS_AND_FIXES.md`) unless the change has been explicitly validated and approved by the user. Use "IMPLEMENTED (AWAITING VALIDATION)".
- **Engineering Log:** Detailed technical post-mortems and architectural deep-dives must be recorded in `ENGINEERING_LOG.md` for all complex issues (Issue 40+).
- **Reporting:** Always provide a summary of the implemented fix and wait for a validation directive before marking the item as resolved in the project documentation.

### Typography & CSS (Mobile-First v5.1)
Inject this CSS into every XHTML `<head>` using `!important` to override legacy styles. Wrap the content in CDATA blocks for XML compliance.

```css
/*<![CDATA[*/
body {
  -webkit-text-size-adjust: 100%;
  -webkit-font-smoothing: antialiased;
  word-break: break-word;
  line-height: 1.65;
  margin: 0.4em 0.5em !important;
}
body, div, p, span, h1, h2, h3, h4, h5, h6 {
  font-family: "[PRIMARY]", "SBL BibLit", "Gentium Plus", serif !important;
}
p {
  -webkit-hyphens: auto;
  hyphens: auto;
}
[lang="el"], [lang="el"] * {
  font-family: "SBL Greek", "Cardo", "SBL BibLit", serif !important;
  font-size: 1.15em;
}
[lang="he"], [lang="he"] * {
  direction: rtl;
  unicode-bidi: isolate;
  font-family: "SBL Hebrew", "Ezra SIL", "SBL BibLit", "Cardo", serif !important;
  font-size: 1.5em;
  line-height: 1.24;
}
[lang="he"], [lang="he"] p, [lang="he"], [lang="he"] div {
  text-align: left;
}
/* Interactive Owen Blue Palette (#2a55a0) */
a, .noteref {
  color: #2a55a0 !important;
  text-decoration: none;
}
.noteref {
  vertical-align: super;
  font-size: 0.85rem;
  padding: 0.1em 0.2em; /* Easy-tap */
}
.footnote {
  font-size: 0.9em;
  text-indent: 0;
  margin: 0.3em 0;
}
a.fn-link {
  color: #2a55a0 !important;
  text-decoration: none;
  font-size: 0.85em;
  margin-right: 0.3em;
}
/* Continuous Blockquotes */
blockquote p {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}
blockquote {
  border-left: 2.5px solid rgba(0, 0, 0, 0.08) !important;
  padding-left: 1.2em !important;
  margin: 1.2em 0 !important;
}
aside[epub\:type~="footnote"] { display: block; }
aside[epub\:type~="endnote"] {
  margin-bottom: 0.8em;
  padding-left: 1.8em;
  text-indent: -1.8em;
}
/*]]>*/
```

## Technical Mandates
1.  **Paragraph Healing:** All volumes MUST use the holistic `reconstruct_paragraphs` logic (verified in Issue 42) to prevent sentence fragmentation across page boundaries.
2.  **Chapter Processing:** Chapters spanning multiple PDF pages must be merged in their raw state before cleaning or healing to ensure seamless sentence reconstruction.
3.  **Layout Preservation:** Healer logic must protect list items (using `list_item_re`) and avoid joining lines that follow terminal punctuation unless they start with a lowercase character.
5.  **Architectural Separation (Overrides):** Volume-specific data (OCR `text_replacements`, custom paragraph hooks, or local formatting logic) MUST reside within each volume's designated converter (e.g., `volumes/v1/convert.py`) using the `OVERRIDES` dictionary. Base scripts (`shared.py`, `extract.py`, `render.py`) must remain generic to avoid bloat and maintain a clean collection-wide pipeline.
6.  **Greek/Hebrew Preservation:** Deduplication and overlap-removal functions MUST include Greek (`\u0370-\u03FF\u1F00-\u1FFF`) and Hebrew (`\u0590-\u05FF`) Unicode ranges in word-matching regexes. Failure to do so causes false-positive ghost detection that drops entire Greek clauses.
7.  **AGES Koine Encoding:** The AGES Koine font uses non-standard Beta Code mappings:
    - `c` = chi (χ), `x` = xi (ξ) — opposite of standard Beta Code
    - `Y` = upsilon (Υ), `y` = psi (ψ) — uppercase Y is upsilon, not psi
    - `v` = final sigma (ς) — explicit final sigma marker
8.  **Per-Volume Script Requirement:** Always use `volumes/vN/convert.py` for testing and rebuilding. The legacy `converter.py` does not pass volume-specific `OVERRIDES` to the render pipeline, so EPUBs built with it will miss volume-specific OCR corrections.
9.  **@font-face Integrity (MANDATORY):** Every `@font-face` declaration MUST include both `font-weight` and `font-style` properties. The primary font template and all dynamically generated variants in `shared.py` (`generate_font_styles`) must emit complete declarations. Without these properties, the browser registers only the last-loaded variant for the entire family, causing ALL text to render as the wrong weight/style. When modifying `EPUB3_FONT_STYLES` or `generate_font_styles`, verify every `@font-face` block has `font-weight: normal|bold` and `font-style: normal|italic`.
10. **Historical Orthography Whitelisting:** When triaging text anomalies flagged by `scripts/audit_anomalies.py`, preserve authentic 17th-century spelling variants and compound hyphens (e.g. `birth-place`, `free-will`, `co-essential`). While flagging them for awareness is expected and correct, **never modernize these historical forms** in `text_replacements`. Restrict replacements solely to clear OCR anomalies (like `Peta-vius` containing a page-split hyphen residue) or alphanumeric typos (like `iraFated`).
11. **Footnote Placement Rule:** Footnote references (both standard and translation-enriched) MUST always be placed AFTER punctuation marks (such as periods, commas, question marks, quotation marks, etc.). For example, `"Quae regio in terris nostri non plena cruoris?"[2]` or `lib. 5 cap. ult.,[14]`. Never place footnote references before punctuation.

