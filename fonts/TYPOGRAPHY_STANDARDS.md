# Universal EPUB Typography & Mobile-First Styling Standard

This document serves as the master blueprint for EPUB3 styling across all book conversion projects. It synthesizes mobile-first typographic principles, font selection guidelines, accessibility rules, and platform-specific fixes (like bypassing Apple Books' layout quirks).

Any agent working on styling EPUBs for any volume or project **must** adhere to these universal standards.

---

## 🚨 MANDATORY AGENT IMPLEMENTATION CHECKLIST 🚨
Before declaring any styling or conversion task "Done", you **must** explicitly confirm that EVERY SINGLE point below has been successfully implemented in the target project's CSS or python injection logic:

### 1. Global Typography & Layout
- [ ] **Body Font Size:** Is the `font-size` on the root `body` or bare `<p>` elements left completely `unset` (or absent) so the e-reader handles it naturally?
- [ ] **Justification & Hyphenation:** Are you explicitly applying `text-align: justify;`, `hyphens: auto;`, and `-webkit-hyphens: auto;` globally to the body/paragraph text?
- [ ] **Small Caps:** Have you confirmed that `font-variant: small-caps;` is properly styled and supported by the embedded fonts?

### 2. Inline Footnote Markers
- [ ] **Inline Flow:** Did you explicitly include `display: inline !important;` on `a.noteref` and `display: inline !important;` on `a.noteref sup` to prevent them from snapping to a new line?

### 3. Apple Books Footnote Popups (The Quirks)
- [ ] **Popup Formatting:** Are you wrapping the text inside the `<aside>` with a `<p class="footnote">` tag?
- [ ] **Popup Line-Height (Bypass):** Did you aggressively inject `style="line-height: 1.30 !important;"` directly into the generated `<p class="footnote">` HTML tag?
- [ ] **Popup Justification:** Does the `.footnote` class explicitly contain `text-align: justify !important; hyphens: auto !important; -webkit-hyphens: auto !important;`?
- [ ] **Popup Margins:** Did you explicitly zero out margins and padding on the `aside[epub\:type~="footnote"]` container (`margin: 0 !important; padding: 0 !important;`)?
- [ ] **Backlink Stripping:** Did you strip whitespace immediately following the footnote backlink tag to prevent ugly indentations?
- [ ] **Header Spacing:** Did you inject a physical space character between the footnote marker tag and the subsequent text inside the popup?

### 4. Project Font Management
- [ ] **Project Tracker:** Have you created or updated the project-specific `font_checklist.md` mapping the volumes to their specific font files?

---

## 1. Digital & Mobile-First Typography Reference

For a digital and mobile-first launch, traditional print rules like point sizes (`pt`) and tight leading do not translate well to responsive screens. Mobile readers need breathing room to prevent eye strain on backlit displays, and sizes must adapt to various device widths.

### Core Layout Metrics (Responsive)
Instead of fixed print points, digital layouts use relative units (`em`, `rem`, or percentages) to ensure the text scales perfectly across all devices.
* **Body Font Size:** Must be left `unset` on the root `body` or bare `<p>` elements. (See Accessibility section below).
* **Heading Font Size:** 
  * **Chapter Numbers/Titles (H1):** `1.75rem` to `2rem` (approx. 28px–32px).
  * **Subheadings (H2):** `1.25rem` to `1.5rem` (approx. 20px–24px).
* **Line Spacing (Leading):** `1.35` (unitless) to create a cohesive, dense, print-like layout on mobile. Avoid values higher than `1.45` to prevent text from feeling overly spaced out.
* **Line Length (Measure):** **45 to 60 characters per line**.
* **Alignment:** **Justified** alignment should be used for body text, but it **must** be paired with `hyphens: auto` and `-webkit-hyphens: auto` to prevent large rivers of white space on mobile screens.
* **Paragraph Separation:** Use a subtle bottom margin (`margin-bottom: 0.5em`) or a very light indent (max `1.5em`) without extra paragraph spacing.
* **Margins:** Maintain a minimum **8% to 10% padding** on the left and right edges.

---

## 2. Global Font Size Best Practices (Accessibility)

### The Rule
**Never** explicitly set a `font-size` on the root `body` or bare `<p>` elements. They must be left `unset` to inherit the e-reader's default base size.

### Why this decision was made
1. **User Control (The "Aa" Menu):** Forcing a font-size on the body (e.g., `font-size: 12pt;`) risks locking the text size and breaking the user's ability to resize the text using their device's built-in controls.
2. **Device Optimization:** Leaving the body font size unset allows the device's native reading engine to provide the mathematically ideal base size for its specific hardware.

### When to use `font-size`
You should *only* use explicit `font-size` declarations (and only in relative units like `em` or `%`) for elements that need to scale proportionally to the base size:
- `h1 { font-size: 2em; }` (Always twice as big as the body text)
- `.footnote { font-size: 1.0em; }` (Same size as the body text for enhanced readability)
- Footnote popups must be **justified** and explicitly enable hyphenation (`hyphens: auto; -webkit-hyphens: auto;`) to prevent ragged edges on mobile.

---

## 3. Font Selection & Pairings

Theology and complex non-fiction projects require rigorous hierarchy. The fonts must handle extensive footnotes, scripture references, blockquotes, small caps for the divine name (LORD), and original languages.

### The Optical Size Rule for EPUBs
> [!IMPORTANT]
> **CRITICAL EPUB RULE: Always use "Caption" or "Text/Regular" optical sizes.**
> If a font family includes optical sizes (e.g., Caption, Text, Subhead, Display), **always** select the **Caption** or **Text** variants for the EPUB body text. Display and Subhead sizes are designed for large print headlines; when scaled down on lower-resolution e-reader screens, their high contrast and thin strokes will wash out, become brittle, and ruin legibility. The Caption and Text cuts are engineered with sturdier strokes, thicker serifs, and open counters specifically to survive harsh digital rendering at small sizes.

### Top Font Picks for Mobile-First Literature
- **Garamond Premier Pro** (Adobe / Robert Slimbach)
  - *Why it's premium:* The definitive modern digital cut of Garamond. It includes four distinct optical sizes (Caption, Text, Subhead, Display). For ePubs, using the Caption or Text weight ensures the thin strokes don't wash out or become brittle on lower-resolution screens.
- **Minion Pro** (Adobe / Robert Slimbach)
  - *Why it's premium:* An exceptionally versatile workhorse. Like Garamond Premier, it features dedicated optical sizes (Caption, Regular, Subhead, Display). Use the "Regular" or "Caption" cuts to maintain a sturdy presence on smartphone screens.
- **Georgia**
  - *Why it's premium:* A legendary digital-first system font engineered specifically for screen legibility. It features a large "x-height" and sturdy serifs that thrive on both old and high-res screens.
- **Modern Non-Fiction (Sans-Serif):** Use clean sans-serifs like **Inter**, **Roboto**, or **Helvetica Neue** for high legibility in structured layouts.

### Theology & Academic Typography
- **Adobe Jenson Pro**
  - *Why it's premium:* A beautiful Venetian old-style serif. It includes optical sizes (Caption, Regular, Subhead, Display). Use the "Caption" or "Regular" cuts for robust reading.
- **Bembo & ITC Galliard**
  - *Why it's premium:* The heritage classics for historical and confessional works. They provide an authentic traditional print feel, though care must be taken on digital screens.
- **SBL BibLit**
  - *Why it's premium:* The absolute golden standard for academic multi-language works. It effortlessly handles complex Greek and Hebrew polytonal diacritics with perfect vertical alignment.
- **High-Legibility Digital Options:**
  - **Lexicon:** Originally designed for dictionaries, it offers extreme legibility at small sizes and short text blocks.
  - **Merriweather:** A custom-tailored screen font with wide proportions and thick serifs that is very easy to read on mobile.

### Required Font Standards
- **Body Text:** Use `Garamond Premier Pro`, `adobe-garamond-pro`, or an equivalent high-legibility serif.
- **Headings:** Use a Baskerville-style face or an equivalent sturdy serif.
- **Greek/Hebrew:** Use `SBL BibLit` (or `GFS Porson` / `SBL Hebrew`). *Note: Original language fonts like SBL BibLit often have a larger x-height than standard body serifs. You must dynamically tune the Greek/Hebrew `font-size` to match the specific body font being used (e.g., limit it to `1.05em` when paired with Garamond, but it may require `1.15em` or `1em` when paired with other faces like Bembo or Minion) so it blends seamlessly without popping out.*

### A Crucial Tip for EPUBs
Ensure that your CSS includes styles for **`font-variant: small-caps;`** and that your embedded font files fully support true small caps (e.g., for "LORD" or "BC/AD").

---

## 4. Handling System Fonts & Empty Directories

Certain system-level fonts (such as **Palatino**, **Georgia**, **Times New Roman**, **Baskerville**, and **Hoefler Text**) do not require physical `.otf` or `.ttf` files to be embedded into the EPUB package.

### How to configure a System Font for the Pipeline
Even though these fonts do not need physical files, the pipeline logic often scans the `fonts/` directory to discover available font families. To register a system font:
1. **Create an Empty Directory:** You **must** create an empty folder in the `fonts/` directory named after the font (e.g., `fonts/hoefler-text/`, `fonts/palatino/`). This empty directory acts as a marker so the orchestrator knows the font is available for selection.
2. **Bypass Fallbacks:** The pipeline should bypass any default fallbacks and preserve the intended system font selection when it detects this empty directory.
3. **Audit Exemption:** EPUB audit scripts must suppress missing-font errors for these known system fonts.
4. **Local Injection:** The CSS compiler should automatically inject `@font-face` rules using `src: local("Font Name")` (along with its bold/italic variants) instead of a physical `url()`. This ensures that Apple Books and other advanced reading systems natively render the OS-level typography smoothly without bloating the EPUB file size.

---

## 5. The "Apple Books Quirks" for Footnote Pop-ups

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
    text-align: justify !important;
    hyphens: auto !important;
    -webkit-hyphens: auto !important;
    margin: 0 !important;
    padding: 1.5em 0 0.8em 0 !important; /* 1.5em top padding forces clearance */
    text-indent: 0 !important;
    display: block;
}
```

### D. Forcing Space in Popup Headers
**The Rule:** Apple Books often ignores CSS `margin` and `padding` rules applied to inline elements deep within a popup (like the `<a href>` tag representing the footnote marker). To ensure a guaranteed visual separation between the footnote marker (e.g., `VI.1`) and the adjacent text (e.g., `John 17:3`), you **must** inject a physical space character directly into the HTML between the tags.
- This should be enforced via a global string replacement during the EPUB repackaging phase.

**Code Example:**
```python
# Ensure physical space between pf-ref footnote marker and scripture text
content = re.sub(r'(</a>)(<strong>)', r'\1 \2', content)
```

### E. Global Line-Height Override
**The Rule:** Apple Books on iOS uses an internal system stylesheet that forcefully overrides `line-height` by injecting its own defaults directly into `<p>` tags. 
To bypass this and reclaim our tight `1.35` text blocks, you **must** apply `line-height` with `!important` to both the `<body>` and directly to the `<p>` tags. You must also anchor the `<p>` tag's `font-size` so iOS doesn't hijack the spacing.

```css
body {
    line-height: 1.35 !important;
}
p {
    font-size: 1em !important;
    line-height: 1.35 !important;
}
```

---

## 6. Inline Footnote Reference Numbers (Superscript)

> [!CAUTION]
> **CRITICAL AGENT INSTRUCTION: NEVER USE `display: inline-block` FOR FOOTNOTES!**
> You must **STRICTLY** use `display: inline !important;` for all `.noteref` elements. 
> Using `inline-block` forces horizontal padding and margins to physically push adjacent text away, resulting in ugly, broken gaps around the footnote marker. You are forbidden from using `inline-block` here.

**The Rule:** Keep superscript footnote numbers as standard inline elements to allow "ghost padding" for touch targets without breaking text flow.

```css
a[epub\:type="noteref"], .noteref {
    display: inline !important;
    vertical-align: super;
    font-size: 0.80rem;   /* slightly larger, root-relative to remain legible */
    line-height: 0;
    padding: 0.1em 0.15em 0.1em 0.05em !important; /* 0.05em left padding snaps it tight against previous word */
    white-space: nowrap;
}

/* Prevent <sup> tags inside .noteref from double-shrinking */
.noteref sup {
    font-size: 1em;
    line-height: inherit;
    vertical-align: baseline;
}
```

---

## 7. Project-Specific Font Documentation Requirement

**The Rule:** You **must** always generate and maintain a project-specific font tracker (e.g., `font_checklist.md`) for every new EPUB conversion project.

### Why this decision was made
While this `TYPOGRAPHY_STANDARDS.md` document provides the universal rules, each project will have its own unique set of volumes, assigned font pairings, and physical asset dependencies. Separating the universal rules from the project-specific tracking makes it significantly easier to debug font issues across different books.

### Required Contents for the Project Tracker
Your project-specific documentation must include at minimum:
1. **Core Asset Checklist:** A verified list of the physical `.ttf` / `.otf` files available in the project's font directories.
2. **Restoration / Licensing Notes:** A record of where the fonts were acquired (e.g., Google Fonts, system copies, commercial licenses).
3. **Volume-to-Font Mappings:** A master table explicitly defining which volume/book is assigned which Body Font and Heading Font pairing. This provides a quick-look reference for debugging why a specific volume might be failing an audit or rendering incorrectly.



---

## 8. Comprehensive Directory of Font Assets & Optical Sizing

This section serves as a reference for agents when selecting appropriate typography for a volume. It outlines every font available in the system (or highly recommended missing additions), their historical/aesthetic description, and critical details about their optical sizes.

> [!TIP]
> **Agent Selection Guide:** When picking a font for body text, always check the "Optical Sizes" entry. If a font has optical sizes (indicated with **Yes** below), you **must** select the `Caption` or `Text/Regular` cuts for the main epub body text, as `Display` or `Subhead` cuts will render too thin on digital screens.

### Current System Fonts & Assets

#### 1. Cormorant Garamond
* **Description:** Designed by Christian Thalmann, this is a beautiful, highly expressive family inspired by Claude Garamond’s legacy. It features crisp, elegant lines and uniquely sharp tracking curves.
* **Optical Sizes:** **Yes.** It is inherently structured around optical optimization, featuring distinct versions such as *Cormorant Garamond* (optimized for text readability), *Cormorant Infant*, *Cormorant Upright*, and *Cormorant Display* (exquisitely high-contrast for titles).

#### 2. IM Fell English
* **Description:** Part of Igino Marini’s "FELL Types" revival project. It digitizes the historic 17th-century types collected by Bishop John Fell for Oxford University Press. It features delightful, uneven "ink bleed" imperfections that add incredible historical texture to print layouts.
* **Optical Sizes:** **No** (traditionally delivered as an individual historical face optimized for text size).

#### 3. Ezra SIL (2/51)
* **Description:** A highly specialized, academic typeface developed by SIL International to correctly display Biblical Hebrew text according to the Tiberian pointing system. It mimics the calligraphy found in the traditional *Biblia Hebraica Stuttgartensia* (BHS).
* **Optical Sizes:** **No.** It is tailored for standard academic and biblical layout text blocks.

#### 4. Goudi (Goudy Old Style)
* **Description:** Designed by Frederic W. Goudy in 1915, this is a quintessential American Old Style font. It features elegant, upward-curved ear elements on characters like the 'g' and diamond-shaped periods. It is highly readable, warm, and distinctly editorial.
* **Optical Sizes:** **Varies.** Standard digital cuts are uniform, though premium foundry editions include dedicated *Text* and *Title/Display* cuts.

#### 5. ITC Galliard
* **Description:** A masterful 1978 design by Matthew Carter based on the 16th-century work of Robert Granjon. It possesses an intense, dramatic energy with highly expressive, sharp italics that add unmatched premium weight to dynamic prose.
* **Optical Sizes:** **Yes** (Premium releases from foundries like Linotype/ITC feature dedicated *Text* and *Display* weights).

#### 6. Inter
* **Description:** An exceptionally well-engineered, low-contrast, open-source geometric sans-serif designed by Rasmus Andersson. It is fine-tuned specifically for user interfaces and high-density technical layouts on modern computer screens.
* **Optical Sizes:** **Yes.** Modern iterations contain explicit OpenType layout adjustments (`opsz` variables) for seamless scaling from micro-captions to massive headings.

#### 7. Gentium Plus (2)
* **Description:** Another elite SIL International creation, designed by Victor Gaultney. It is an elegant, highly legible serif optimized for extensive multilingual publishing, featuring exhaustive support for the Latin, Greek, and Cyrillic character sets.
* **Optical Sizes:** **No.** However, its unique glyph proportions are inherently designed to maintain visibility at small sizes.

#### 8. EB Garamond
* **Description:** Georg Duffner’s masterful, open-source digitization of Claude Garamond’s original specimens from the Egenolff-Berner sheet. It offers the truest historical look and character among free Garamond fonts.
* **Optical Sizes:** **Yes.** It features full variable optical axes (`opsz`), scaling gracefully from detailed display sizes down to readable text sizes.

#### 9. GFS Porson
* **Description:** Developed by the Greek Font Society, this typeface reproduces the elegant Greek cursive handwriting of 18th-century English scholar Richard Porson. It is an industry-standard companion for setting classical Greek texts.
* **Optical Sizes:** **No.** It is traditionally issued as a single text weight for continuous reading.

#### 10. Centaur
* **Description:** Designed by Bruce Rogers in 1914, Centaur is a Venetian Old Style font based on Nicolas Jenson's 1470 prints. It is thin, light, elegant, and calligraphic, looking stunningly premium when spaced well.
* **Optical Sizes:** **No** (Most modern digital cuts are unified, meaning it behaves best at medium-to-large sizes due to its fine lines).

#### 11. Arno Pro
* **Description:** A masterful creation by Robert Slimbach for Adobe. Drawing inspiration from humanistic Italian handwriting, it is incredibly warm, readable, and features highly artistic, fluid italic shapes.
* **Optical Sizes:** **Yes.** It includes five robust optical sizes: *Caption, SmText, Regular, Subhead,* and *Display*.

#### 12. Cinzel
* **Description:** Designed by Natanael Gama, Cinzel is an all-caps display serif based on classical Roman proportions and stone inscriptions. It brings immediate architectural gravity to book covers and title layouts.
* **Optical Sizes:** **No** (but it functions natively as a display-tier typeface).

#### 13. Georgia
* **Description:** Matthew Carter’s iconic transitional web serif. Designed explicitly for early Microsoft screens, it features a large x-height and heavy strokes to ensure readability at tiny resolutions.
* **Optical Sizes:** **No** (though newer Pro variants expand weight selections).

#### 14. SBL-BLit (SBL Hebrew / Greek)
* **Description:** Commissioned by the Society of Biblical Literature, this typeface is a premier tool used globally by scholars to properly print and display biblical Hebrew and critical textual marks.
* **Optical Sizes:** **No.** Engineered purely for uniform academic text precision.

#### 15. New Caledonia LT Std
* **Description:** A crisp, authoritative transitional font based on William Addison Dwiggins' classic Caledonia. It draws inspiration from Scotch Roman cuts, delivering clear, punchy text layouts for historical or legal treatises.
* **Optical Sizes:** **No** (but it maintains excellent structural stability at standard print sizes).

#### 16. Adobe Garamond Pro
* **Description:** Robert Slimbach's elegant 1989 design. It is arguably the most famous, highly balanced digital representation of Garamond’s punches, prized for its organic, inviting reading texture.
* **Optical Sizes:** **No.** It is optimized globally for classic text block ranges (roughly 10pt–12pt).

#### 17. Adobe Caslon Pro (listed as "adobe-carlson-pro")
* **Description:** Slimbach’s treatment of William Caslon’s 18th-century typefaces. It embodies a sturdy, slightly rugged Anglo-American aesthetic that looks clean, classic, and extremely professional.
* **Optical Sizes:** **No** (Standardized text cut, though its bold and regular weights scale beautifully).

#### 18. Cardo
* **Description:** David Perry's massive, high-quality open-source serif designed specifically for classicists, biblical scholars, medievalists, and linguists who require specialized old-style glyphs.
* **Optical Sizes:** **No.** It is structurally weighted for reading-level text layouts.

#### 19. Playfair Display
* **Description:** A high-contrast modern serif by Claus Eggers Sørensen inspired by John Baskerville's writing style. It features dramatic differences between thick and thin lines, making it perfect for elegant title formatting.
* **Optical Sizes:** **Yes.** Newer updates include structural scaling optimized for headline rendering.

#### 20. Sabon Next LT
* **Description:** Jean François Porchez’s brilliant expansion of Jan Tschichold's Sabon. It restores the original French Renaissance spirit of Garamond with improved weight distributions for screen display.
* **Optical Sizes:** **Yes.** Elite versions include discrete *Text* and *Display* cuts.

#### 21. Libre Caslon Text
* **Description:** An open-source revival specifically tuned for body text layouts. It features thicker lines and wider proportions to ensure it stays crisp and legible on e-ink e-readers.
* **Optical Sizes:** **Yes** (Distinguished explicitly from its sibling, *Libre Caslon Display*).

#### 22. Merriweather
* **Description:** A low-contrast, highly robust serif typeface designed by Eben Sorkin specifically for effortless reading on digital screens. Its tall x-height makes it highly friendly to mobile formatting.
* **Optical Sizes:** **No** (Uniformly engineered for digital screen text).

#### 23. Baskerville
* **Description:** The legendary 18th-century transitional typeface. It represents structural balance, sharp serifs, and high-contrast vertical weight distribution, bridging old-style and modern letter design.
* **Optical Sizes:** **Varies.** Generic cuts lack optical adjustments, while premium editions include them.

#### 24. Minion Pro
* **Description:** Robert Slimbach's highly functional, compact Renaissance-style masterpiece. It is exceptionally space-efficient, looking orderly and beautiful in complex academic or multi-volume works.
* **Optical Sizes:** **Yes.** Features *Caption, Regular, Subhead,* and *Display* packages.

#### 25. STIX Two Text
* **Description:** Short for the *Scientific and Technical Information Exchange*, this is an outstanding, professional-grade typeface optimized for journals and books with heavy technical notation. It is clean, legible, and balanced.
* **Optical Sizes:** **No** (but it is specifically tailored to excel in standard 10pt–12pt text ranges).

#### 26. Libertinus
* **Description:** An excellent open-source fork of the *Linux Libertine* font project. It corrects sizing inconsistencies and expands support for advanced mathematical typography and classic text formatting.
* **Optical Sizes:** **No** (though it splits tasks across specific *Libertinus Serif*, *Sans*, and *Math* fonts).

#### 27. Proxima Nova
* **Description:** Mark Simonson’s mega-popular modern sans-serif. It perfectly blends geometric structures with humanistic proportions, offering clean text blocks that feel current and polished.
* **Optical Sizes:** **No** (but features a massive array of individual width expansions).

#### 28. Bembo
* **Description:** Monotype’s famous revival of a 1495 font cut by Francesco Griffo for Aldus Manutius. It is considered one of the most elegant, literary old-style typefaces ever made.
* **Optical Sizes:** **Yes** (Premium modern cuts like *Bembo Book* or *Bembo Book MT* restore dedicated text scaling).

#### 29. Coelacanth
* **Description:** A highly unique, open-source old-style font family inspired by the legendary Centaur. It was engineered from the ground up to support variable rendering scales.
* **Optical Sizes:** **Yes.** Remarkably, it features up to six distinct optical size levels ranging from tiny *4pt* rendering up to giant *60pt* display sizes.

#### 30. Brill Font
* **Description:** Commissioned by the Dutch publisher Koninklijke Brill. It is an exceptional academic typeface with perfect weight consistency and unmatched support for complex notations and accents.
* **Optical Sizes:** **No** (Built inherently with a sturdy "color" profile that reads seamlessly at normal sizes).

#### 31. Montserrat
* **Description:** A geometric, urban-style sans-serif inspired by historical signage in Buenos Aires. Excellent for bold chapter headings or modern editorial splash pages.
* **Optical Sizes:** **No.**

#### 32. Roboto
* **Description:** Google’s signature neo-grotesque sans-serif. It features mechanical efficiency paired with open curves, ensuring high accessibility across digital reading interfaces.
* **Optical Sizes:** **No** (Unified scaling system).

#### 33. Palatino
* **Description:** Hermann Zapf's iconic 1949 post-Renaissance design. It features broad, calligraphic brushstroke angles that make it incredibly strong, versatile, and highly beautiful in print layouts.
* **Optical Sizes:** **No** (though modern premium expansions like *Palatino Nova* offer specialized tuning).

#### 34. Literata
* **Description:** Originally designed by TypeTogether for Google Play Books, this font is meticulously engineered for optimal reading experiences on digital tablets and e-ink displays.
* **Optical Sizes:** **Yes.** It includes full variable optical size axes tailored to display small text beautifully.

#### 35. Garamond Premier Pro
* **Description:** Robert Slimbach's comprehensive, historical research-driven expansion of his earlier Garamond work. It is considered one of the highest-quality digital Garamonds ever produced.
* **Optical Sizes:** **Yes.** Fully equipped with *Caption, Text, Subhead,* and *Display* optical packages.

#### 36. Hoefler Text
* **Description:** Jonathan Hoefler’s highly sophisticated literary serif family. Built specifically to bring classical typographical rules into digital formats, it handles space, ornaments, and tracking exceptionally well.
* **Optical Sizes:** **No** (but incorporates elegant built-in features like engraving cuts and varying number variants).

---

### 🚀 Key Additions Missing From Library (Recommended)

Given the academic, literary, and historical focus of this collection, adding these premium typefaces would perfectly bridge any gaps:

#### 1. Miller Text *(Transitional / Scotch Roman)*
* **Status:** ❌ Missing from system.
* **Why it's missing:** While the collection features excellent old-style fonts (Garamond, Bembo, Minion) and excellent academic fonts (Brill, STIX Two), it lacks a heavy-duty, modern **Scotch Roman** typeface. Miller Text features a sharp, authoritative, news-editorial structure that is perfect for history volumes, biographies, and modern critiques.
* **Optical Sizes:** **Yes.** The Miller family famously splits into *Miller Text* and *Miller Display* for appropriate scaling.

#### 2. Quadraat / Quadraat Sans *(Modern Classic)*
* **Status:** ❌ Missing from system.
* **Why it's missing:** Designed by Fred Smeijers, FF Quadraat is a highly unique serif with crisp, slightly rugged, diamond-like angles. Even better is its sibling, **Quadraat Sans**, which shares the exact same letter spacing and structural skeleton. This allows for seamless pairings where titles and body text flow in perfect aesthetic unity.

#### 3. Scala Sans *(The Ultimate Complementary Sans-Serif)*
* **Status:** ❌ Missing from system.
* **Why it's missing:** While the collection has great sans-serifs like Inter and Proxima Nova, they are geometric or technical. **FF Scala Sans** is a *humanistic* sans-serif built using old-style proportions. Pairing Scala Sans for chapter headers with old-style serifs like Garamond Premier Pro or Sabon Next creates an incredibly premium, custom-designed publishing aesthetic.

#### 4. Warnock Pro *(Modern Classicist)*
* **Status:** ❌ Missing from system.
* **Why it's missing:** Robert Slimbach’s Warnock Pro offers a modern, slightly sharper, and highly energetic serif that doesn't rely entirely on historical models. It is brilliant for modern academic works that want a premium, contemporary feel.
* **Optical Sizes:** **Yes.** Includes *Caption, Regular, Subhead,* and *Display* weights.
