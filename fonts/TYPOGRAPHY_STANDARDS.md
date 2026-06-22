# Universal EPUB Typography & Mobile-First Styling Standard

This document serves as the master blueprint for EPUB3 styling across all book conversion projects. It synthesizes mobile-first typographic principles, font selection guidelines, accessibility rules, and platform-specific fixes (like bypassing Apple Books' layout quirks).

Any agent working on styling EPUBs for any volume or project **must** adhere to these universal standards.

---

## 1. Digital & Mobile-First Typography Reference

For a digital and mobile-first launch, traditional print rules like point sizes (`pt`) and tight leading do not translate well to responsive screens. Mobile readers need breathing room to prevent eye strain on backlit displays, and sizes must adapt to various device widths.

### Core Layout Metrics (Responsive)
Instead of fixed print points, digital layouts use relative units (`em`, `rem`, or percentages) to ensure the text scales perfectly across all devices.
* **Body Font Size:** Must be left `unset` on the root `body` or bare `<p>` elements. (See Accessibility section below).
* **Heading Font Size:** 
  * **Chapter Numbers/Titles (H1):** `1.75rem` to `2rem` (approx. 28px–32px).
  * **Subheadings (H2):** `1.25rem` to `1.5rem` (approx. 20px–24px).
* **Line Spacing (Leading):** `1.5em` to `1.65em` (150%–165% of the font size). Screens require more vertical white space than paper.
* **Line Length (Measure):** **45 to 60 characters per line**.
* **Alignment:** Body and paragraph prose are typically justified with hyphenation enabled. Headings should be allowed to use their explicit centering or left-alignment without being forcefully overridden.
* **Paragraph Separation:** Use a subtle bottom margin (`margin-bottom: 0.5em`) or a very light indent (max `1.5em`) without extra paragraph spacing.
* **Margins:** Maintain a minimum **8% to 10% padding** on the left and right edges.

---

## 2. Paragraph and Body Justification

### The Rule
Both the `body` and `p` elements are justified by default to create a clean, uniform block of text for the main prose. 

### Why this decision was made
While some digital layouts prefer left-aligned text, this project standardizes on full justification for `body` and `p` tags to mirror classic print layout. However, it is critical that this inheritance does not forcefully overwrite explicit heading alignments. Do not apply `!important` alignment rules globally to headings (`h1`-`h6`), as that breaks specific centered title pages.

### Required CSS Pattern
```css
body {
    text-align: justify;
    text-justify: inter-word;
    overflow-wrap: break-word;
    word-break: break-word;
}

p {
    text-align: justify;
    -epub-text-align-last: left;
    text-align-last: left;
    -webkit-hyphens: auto;
    hyphens: auto;
}
```
*Note: The `-epub-text-align-last: left;` property is critical when justifying text to prevent e-readers from awkwardly stretching the final, short line of a paragraph across the entire screen width.*

---

## 3. Global Font Size Best Practices (Accessibility)

### The Rule
**Never** explicitly set a `font-size` on the root `body` or bare `<p>` elements. They must be left `unset` to inherit the e-reader's default base size.

### Why this decision was made
1. **User Control (The "Aa" Menu):** Forcing a font-size on the body (e.g., `font-size: 12pt;`) risks locking the text size and breaking the user's ability to resize the text using their device's built-in controls.
2. **Device Optimization:** Leaving the body font size unset allows the device's native reading engine to provide the mathematically ideal base size for its specific hardware.

### When to use `font-size`
You should *only* use explicit `font-size` declarations (and only in relative units like `em` or `%`) for elements that need to scale proportionally to the base size:
- `h1 { font-size: 2em; }` (Always twice as big as the body text)
- `.footnote { font-size: 0.85em; }` (Always slightly smaller than the body text)

---

## 4. Font Selection & Pairings

Theology and complex non-fiction projects require rigorous hierarchy. The fonts must handle extensive footnotes, scripture references, blockquotes, small caps for the divine name (LORD), and original languages.

### Top Font Picks for Mobile-First Literature
- **Georgia** and **Minion Pro**: Engineered with larger "x-heights" and sturdier serifs, they won't degrade on smartphone screens.
- **Modern Non-Fiction (Sans-Serif):** Use clean sans-serifs like **Inter**, **Roboto**, or **Helvetica Neue**.

### Theology & Academic Typography
- **The Heritage Classics (Historical/Confessional):** Bembo, Galliard, Adobe Jenson/Centaur.
- **Modern Academic Workhorses (Commentaries/Multi-Language):** SBL BibLit (Golden standard for Greek/Hebrew), Minion Pro.
- **High-Legibility Digital Options (Devotionals/Bibles):** Lexicon, Merriweather.

### Classic Font Pairings
| Body Font | Ideal Heading Font | Visual Aesthetic & Best Use |
|---|---|---|
| **Garamond** | Garamond Bold or Baskerville | *Classic & Warm.* General fiction, historical fiction, memoirs. |
| **Caslon** | Caslon Bold/Semibold or Garamond Italic | *Historic Authority.* High literary fiction, historical narratives. |
| **Sabon** | Sabon Bold, Futura, or Gill Sans | *Quiet Prestige.* Poetry, premium literary, geometric contrast. |
| **Baskerville** | Baskerville Bold or Italic | *Intellectual & Crisp.* Contemporary literary, authoritative non-fiction. |
| **Minion Pro** | Minion Bold or Myriad Pro | *Invisible Workhorse.* Clean, highly functional digital-first design. |
| **Palatino** | Palatino Bold or Optima | *Open Proportions.* Generous spacing for older/younger readers. |
| **Georgia** | Georgia Bold or Arial/Helvetica | *Screen-Optimized.* Digital literature, low-resolution constraints. |
| **Bembo** | Trajan or Cinzel | *The Cathedral Aesthetic.* Uses Roman monumental capitals for a timeless, sacred appearance. |
| **SBL BibLit** | SBL BibLit Bold | *The Academic Standard.* Kept uniform, clean, and strictly focused on the text's data. |
| **Galliard** | Optima (or Classico) | *The Modern Liturgical.* Optima is a sans-serif with a humanist swell that pairs beautifully with historic serifs. |
| **Merriweather** | Montserrat | *The Modern Digital First.* Clean, highly readable, and perfectly optimized for app-based reading environments. |

### A Crucial Tip for EPUBs
Ensure that your CSS includes styles for **`font-variant: small-caps;`** and that your embedded font files fully support true small caps (e.g., for "LORD" or "BC/AD").

---

## 5. Handling System Fonts & Empty Directories

Certain system-level fonts (such as **Palatino**, **Georgia**, **Times New Roman**, **Baskerville**, and **Hoefler Text**) do not require physical `.otf` or `.ttf` files to be embedded into the EPUB package.

If a system font is selected:
1. **Bypass Fallbacks:** The pipeline should bypass any default fallbacks and preserve the intended system font selection.
2. **Audit Exemption:** EPUB audit scripts must suppress missing-font errors for these known system fonts.
3. **Local Injection:** The CSS compiler should automatically inject `@font-face` rules using `src: local("Font Name")` (along with its bold/italic variants) instead of a physical `url()`. This ensures that Apple Books and other advanced reading systems natively render the OS-level typography smoothly without bloating the EPUB file size.

---

## 6. The "Apple Books Quirks" for Footnote Pop-ups

Apple Books aggressively overrides CSS inside footnote pop-up windows.

### A. The Paragraph Wrapper & Inline Line-Height
**The Rule:** You **must** wrap the inner text of the `<aside>` tag inside a `<p class="footnote">` tag, and you **must** inject the `line-height` as an **inline style** directly onto that `<p>` tag.
- Wrapping the text in a `<p>` ensures Apple Books respects the spacing applied to the child element.
- Apple Books ignores class-based `line-height` rules inside popups. The *only* way to bypass this WebKit override is by using an inline style (`style="line-height: 1.30 !important;"`).

### B. Stripping Backlink Whitespace
**The Rule:** You must strip any regular spaces or hidden non-breaking spaces (`&nbsp;` or `\xa0`) that immediately follow the footnote backlink (`</a>` or `<span class="fn-link">`) tag.
Because we apply a large `padding-top` to push the footnote text down, any space character sitting directly after the backlink tag will be pushed to the very beginning of the first visual line, creating an ugly indent.

**Code Example (Python Regex for Post-Processing):**
```python
def wrap_footnote(match):
    opening = match.group(1)
    inner = match.group(2)
    closing = match.group(3)
    
    # STRIP logic: Find the backlink tag and remove any following whitespace
    inner = re.sub(r'(</a>|</span>)[\s\xa0]+', r'\1', inner.strip())
    
    # Prevent double-wrapping
    if '<p class="footnote"' in inner or '<div' in inner:
        return match.group(0)
        
    return f'{opening}\n<p class="footnote" style="line-height: 1.30 !important;">{inner}</p>\n{closing}'

content = re.sub(r'(<aside[^>]*epub:type="[^"]*footnote[^"]*"[^>]*>)(.*?)(</aside>)', wrap_footnote, content, flags=re.DOTALL)
```

### C. The CSS: Padding vs. Margin
**The Rule:** Use `padding` instead of `margin` to create vertical clearance from the top of the popup window. Zero out the margins on the parent `<aside>`.
Apple Books automatically strips `margin-top` from the first child element inside a popup. `padding-top` is respected by WebKit.

```css
aside[epub\:type~="footnote"] {
    display: block;
    margin: 0 !important;
    padding: 0 !important;
}

.footnote {
    font-size: 1.0em !important;
    text-align: left !important;
    margin: 0 !important;
    padding: 1.5em 0 0.8em 0 !important; /* 1.5em top padding forces clearance */
    text-indent: 0 !important;
    display: block;
}
```

---

## 7. Inline Footnote Reference Numbers (Superscript)

**The Rule:** When styling the superscript footnote numbers within the main body text, you **must** use `display: inline !important;`.
By default, hyperlink tags (`<a>`) are `display: inline`. While Apple Books supports horizontal margins, WebKit's text justification engine treats `display: inline-block` as a separate layout unit, which can cause massive justification gaps around footnotes. To prevent this while still expanding the touch target, keep it `inline` and use asymmetric horizontal padding instead of margins.

```css
a[epub\:type="noteref"], .noteref {
    display: inline !important;
    vertical-align: super; 
    font-size: 0.70rem;
    line-height: 0;
    padding: 0.1em 0.15em 0.1em 0.4em !important; /* Touch target + 0.25em left separation */
    white-space: nowrap;
}
```

### Potential Anomalies
- **The "Massive Gap" Justification Bug:** Do not use `display: inline-block` on inline footnotes. While `inline-block` allows applying explicit margins, Apple Books' proprietary text justification engine treats `inline-block` elements as separate block-formatting layout items rather than continuous inline text nodes. On fully justified lines that need to stretch to fit the screen width, Apple Books will distribute massive amounts of flex-like "justification space" on both sides of the footnote symbol (often looking like 5-6 spaces wide). 
- **Word Joiner Ignored:** When this anomaly occurs, injecting zero-width word joiners (`&#8288;`) to glue the word to the footnote will **not work**, because the `inline-block` node boundary completely breaks the text node sequence in WebKit's layout engine.
- **The Fix:** Maintain `display: inline !important;` and use an asymmetrical horizontal `padding` rule (e.g., `padding-left: 0.4em;`) to visually separate the footnote from the preceding word while maintaining one continuous inline text node.

---

## 8. Project-Specific Font Documentation Requirement

**The Rule:** You **must** always generate and maintain a project-specific font tracker (e.g., `font_checklist.md`) for every new EPUB conversion project.

### Why this decision was made
While this `TYPOGRAPHY_STANDARDS.md` document provides the universal rules, each project will have its own unique set of volumes, assigned font pairings, and physical asset dependencies. Separating the universal rules from the project-specific tracking makes it significantly easier to debug font issues across different books.

### Required Contents for the Project Tracker
Your project-specific documentation must include at minimum:
1. **Core Asset Checklist:** A verified list of the physical `.ttf` / `.otf` files available in the project's font directories.
2. **Restoration / Licensing Notes:** A record of where the fonts were acquired (e.g., Google Fonts, system copies, commercial licenses).
3. **Volume-to-Font Mappings:** A master table explicitly defining which volume/book is assigned which Body Font and Heading Font pairing. This provides a quick-look reference for debugging why a specific volume might be failing an audit or rendering incorrectly.

