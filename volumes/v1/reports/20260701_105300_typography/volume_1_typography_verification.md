# Volume 1 Typography and Popup-Footnote Verification

Date: 2026-07-01  
Status: **IMPLEMENTED (AWAITING VALIDATION)**

## Scope

- Shared body, paragraph, blockquote, list, footnote, noteref, and font CSS.
- Volume 1 catechism question/answer alignment.
- Shared symbolic translation, glossary, biographical, and patristic noteref markup.
- Apple Books popup rendering for original footnotes and enriched modern translations.
- Font packaging used by the shared stylesheet.

Styling affects all 85 reflowable XHTML files in the Volume 1 package. The
package contains 345 noteref links and 345 matching endnote anchors. Four
original footnotes contain enriched `.footnote-modern-translation` blocks.
No source or intermediate text was changed; the PDF comparison range remains
pages 1–633.

## Typography verification

- Root `body` and bare `p` have no explicit `font-size`.
- Body and paragraph prose use `line-height: 1.4`, justified alignment, and
  automatic hyphenation.
- List exposition, blockquote prose, analysis prose, and catechism answers are
  justified. Short catechism questions remain left-aligned intentionally.
- `a.noteref` and `a.noteref sup` are strictly inline; no `inline-block` marker
  rule remains.
- Noteref superscripts use `0.75rem`, `top: -0.32em`, and zero line-height so
  they sit slightly higher without expanding the body line box.
- Both `.footnote` and `.footnote-modern-translation` use `1.0em`, justified
  alignment, automatic hyphenation, zero indentation, and `1.30` popup leading.
- Both popup paragraph classes are explicitly included in the injected Adobe
  Garamond Pro primary-font selector.
- Greek runs use one authoritative `1.03em` size, relative to the reader's
  computed body size; the conflicting later `1.15em` override was removed.
- Modern translation paragraphs include the Apple Books inline override:
  `style="line-height: 1.30 !important;"`.
- All CSS font URLs now resolve to packaged font files. Embedded font count is
  17: three unused or incorrectly styled declarations were removed rather than
  packaging every font available to the repository.

## Automated verification

### Focused regression suite

`154 passed, 9 skipped, 46 deselected`.

The executed selection covered the typography-standard tests, footnote
round-trip integrity, EPUB structure, and all applicable known-bug regression
tests. The deselected global tests are existing all-volume whitelist/OCR-state
checks unrelated to this styling change.

### EPUB audit

- Status: PASS
- Errors: 0
- Warnings: 0
- Files: 119
- XHTML files: 85
- Embedded fonts: 17
- Noterefs / endnote anchors: 345 / 345
- Untagged Greek chars: 0
- Untagged Hebrew chars: 0

Detailed report: `volume_1_audit.md`.

### CSS audit

- Status: WARN
- Errors: 0
- Warnings: 46
- CSS files: 1
- `@font-face` rules: 20
- Embedded fonts: 17

The previous nine missing-font-file errors are eliminated. Remaining warnings
are shared classes unused specifically by Volume 1, intentional internal-family
aliases for SBL/Baskerville faces, and the auditor treating the CSS keyword
`inherit` as a font family. They do not identify a missing font asset.

Detailed report: `volume_1_css_audit.md`.

### Text-integrity audit

- Status: WARN
- Warnings: 2
- PDF content tokens: 191,907
- EPUB content tokens: 206,023
- Approximate coverage: 99.98%
- Pages checked: 581
- Weak page matches: 0
- Missing dense-source-window pages: 31
- Possible paragraph splits: 15
- Greek word coverage: 100%
- Hebrew word coverage: 100%
- Latin word coverage: 99.9%

The two warnings are the pre-existing dense-source-window and paragraph-split
review queues. The detailed report lists their page numbers and XHTML samples;
the typography change did not alter textual content.

Detailed report: `volume_1_text_integrity.md`.

## Whitelisting

No whitelist entries were added, removed, or modified in this session.
