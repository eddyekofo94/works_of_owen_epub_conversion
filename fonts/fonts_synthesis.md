# Font Guide Synthesis & Download Checklist

Based on the `font_mobile_first_guide.md` provided, I have synthesized the key typography recommendations for mobile-first and theological EPUB design, and downloaded the available fonts. I have also audited the CSS standards per your request.

## Typography Recommendations & Synthesis

1. **Digital & Mobile-First Approach**:
   - **Relative Sizes**: Use `em` or `rem` instead of `pt` for fluid scaling.
   - **Spacing**: Keep line spacing (leading) around `1.5em` to `1.65em` for breathability.
   - **Alignment**: **Do not justify** headings or mobile text to avoid rivers of white space. I have updated `GEMINI.md` and `shared.py` to enforce `text-align: left !important` and `-webkit-hyphens: none !important` for all heading tags (`h1`–`h6`). You were happy with paragraph hyphenation, so it remains untouched.
   
2. **Theological Needs**:
   - The typography must support original languages (Greek, Hebrew) and small caps (e.g., for "LORD").
   - **Heritage Classics** (Bembo, Galliard, Jenson) are ideal for historical authority.
   - **Modern Academic** (SBL BibLit, Minion Pro) handle mixed languages and transliterations perfectly.

## Font Checklist

Here is the complete list of fonts mentioned in your guide. I have ticked off the ones that are either successfully downloaded just now or were already present in your `fonts/` directory.

### Body & Heading Classics
- [x] **Garamond** *(available via adobe-garamond-pro & EB Garamond)*
- [x] **Caslon** *(available via ACaslonPro-Regular.otf & libre-caslon-text)*
- [x] **Sabon** *(available via sabon-next-lt)*
- [x] **Baskerville** *(available via baskerville)*
- [x] **Minion Pro** *(available via minion-pro)*
- [ ] **Palatino** *(Commercial/System font)*
- [ ] **Georgia** *(System font)*

### Mobile-First Sans-Serifs & Modern Serifs
- [x] **Inter** *(Downloaded from Google Fonts)*
- [x] **Roboto** *(Downloaded from Google Fonts)*
- [ ] **Helvetica Neue** *(Commercial/System font)*
- [x] **Merriweather** *(Downloaded from Google Fonts)*

### Heritage Classics & Academic (Theology Specific)
- [ ] **Bembo (Bembo Book)** *(Commercial font)*
- [ ] **Galliard (ITC Galliard)** *(Commercial font)*
- [ ] **Adobe Jenson / Centaur** *(Commercial font)*
- [x] **SBL BibLit** *(available via sbl-blit)*
- [x] **SBL Greek & Hebrew** *(available via sbl-blit, ezra-sil-2-51, gfs-porson)*
- [ ] **Lexicon** *(Commercial font)*

### Ideal Heading Font Pairings
- [ ] **Futura** *(Commercial/System font)*
- [ ] **Gill Sans** *(Commercial/System font)*
- [ ] **Myriad Pro** *(Commercial font)*
- [ ] **Optima / Classico** *(Commercial/System font)*
- [ ] **Arial / Helvetica** *(System fonts)*
- [ ] **Trajan** *(Commercial font)*
- [x] **Cinzel** *(Downloaded from Google Fonts)*
- [x] **Montserrat** *(Downloaded from Google Fonts)*

> [!NOTE]
> Open-source fonts (EB Garamond, Inter, Roboto, Merriweather, Cinzel, Montserrat) have been successfully fetched from Google Fonts. Commercial and default macOS system fonts (like Palatino, Georgia, Helvetica, Bembo, etc.) were skipped as they require proprietary licenses, but many macOS/iOS devices will render system fonts perfectly if specified as fallbacks in your CSS.
