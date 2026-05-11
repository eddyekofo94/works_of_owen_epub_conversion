# Owen Collection: Engineering Log & Deep Dives

This log captures detailed technical analysis and architectural decisions for complex issues encountered during the conversion of the 16-volume John Owen collection.

---

## [Issue 70] Source-Aware Structural Boundary Promotion and Citation Continuation

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The remaining recorded open bugs were no longer simple OCR blemishes; they were boundary-classification failures. The converter had to decide whether a number or roman numeral belonged to the sentence before it, to a scripture/citation reference, or to a new Owen outline paragraph. Several cases were still wrong:

- `See August.` was split from `Lib. con. Serm. Arian. cap. 35...`, although the ThML/source keeps it as one citation sentence.
- `[1st,]` after `Two things...; —` needed to start its own paragraph.
- `II. This darkness...`, `4. Hitherto darkness...`, `2. Our second direction...`, and `6. Promises...` were embedded inside prose instead of being promoted to section/list starts.

### 2. Root Cause
Earlier safeguards deliberately became conservative after scripture-like tails because false splits such as `verse, 7` and `1 Corinthians 1:13, 15` were damaging. That prevented some genuine source structure from being promoted. The audit had a parallel blind spot: it inspected normalized paragraph text but not the rendered XHTML where markers had already become `<b>2.</b>` or `<b>II.</b>`.

The citation issue was the inverse: the healer knew how to join a paragraph ending in `chap.` to a following numeric reference, but not a paragraph ending with an author cue such as `See August.` followed by a scholarly abbreviation chain.

### 3. Fix
- Added citation-start recognition for `Lib.`, `Serm.`, `Epist.`, `Cap.`, `Orat.`, `Tract.`, `Homil.`, `Haer.`, `Dial.`, and related starts.
- Added author/citation-tail recognition for patristic cues such as `See August.` and related author abbreviations.
- Joined citation chains during paragraph post-processing before they can become false body paragraphs.
- Extended inline structural marker recognition to cover bare roman markers and markdown-bold decimal/roman forms such as `**6.**`.
- Added a guarded source-like marker promotion rule: if substantial prose is followed by a decimal/roman marker and uppercase continuation, promote the marker unless the preceding context is a scripture/reference/citation tail.
- Extended `scripts/audit_text_integrity.py` to inspect rendered XHTML for inline bold markers while suppressing citation-number false positives such as `Serm. 13` and `lib. 3`.
- Added an explicit `citation_continuation_splits` audit counter.

### 4. Why This Improves Extraction
This moves the converter from punctuation-only healing toward source-aware boundary classification. It no longer treats every terminal period as a paragraph boundary, nor every number as a possible verse continuation. Instead, it distinguishes three cases:

1. reference continuation: keep `verse, 7`, `chap. 7:26`, and scripture tails together;
2. citation continuation: keep `See August. Lib. con. Serm...` together;
3. structural outline marker: promote `II.`, `4.`, `2.`, `6.`, `[1st,]`, and similar Owen outline markers into their own styled paragraphs/headings.

That schema should transfer to other Owen volumes because AGES uses the same extraction patterns: patristic citation chains, bold outline numerals, roman section heads, and scripture-reference continuations recur across the set.

### 5. Validation
Regenerated Volume 1 only. Verified the recorded examples in `ch004.xhtml`, `ch013.xhtml`, `ch029.xhtml`, `ch030.xhtml`, and `ch035.xhtml`. Text-integrity audit now reports 0 inline structural marker candidates, 0 reference continuation splits, 0 citation continuation splits, and 0 roman heading candidates. EPUB audit reports 0 errors and 4 existing warnings.

---

## [Issue 68] Generated Title-Page Credit Alignment and Visible Publisher Credit

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The generated title page showed the lower credit block left-aligned even though the page as a whole should be centered. The ornament needed a gold treatment, and the visible `Banner of Truth Trust` line needed to be replaced with the user credit `Eduadus Ekofius`.

### 2. Root Cause
The stylesheet defined title-page layout near the top, but the later global `p` rule applied `text-align: justify` and indentation to ordinary paragraph elements. The generated `author`, `editor`, and `publisher` paragraphs did not yet have explicit title-page-specific overrides. The generated title-page template also hard-coded `Banner of Truth Trust`.

### 3. Fix
- Added explicit centered paragraph styles for title-page author, editor, and publisher credits.
- Styled the title-page ornament in gold.
- Changed the generated visible publisher credit to `Eduadus Ekofius`.
- Added a small margin after the italic `by` label.

### 4. Validation
Regenerated Volume 1 only. Confirmed unpacked `title.xhtml` has `<p class="publisher">Eduadus Ekofius</p>` and generated CSS centers the credit paragraphs while coloring the ornament `#b08d2d`. EPUB audit reports 0 errors and 4 existing warnings.

---

## [Issue 67] Navigation Page in Spine and Hidden Title Ornament

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Apple Books displayed the generated `nav.xhtml` page as ordinary reading content near the beginning of the book. In a two-page view this made the reader see the end of the table of contents and a redundant `Guide` section beside the generated title page. The title-page ornament also disappeared because a prior visual cleanup hid `.ornament` globally on title pages.

### 2. Root Cause
The EPUB3 navigation document needs to remain in the manifest with `properties="nav"`, but the converter also inserted that item into the spine. Some readers therefore treated the navigation page as a chapter. Separately, the earlier title-page cleanup solved a debris problem by setting `.title-page .ornament` to `display: none`, which removed the intentional generated ornament too.

### 3. Fix
- Removed the nav item from the spine while preserving it in the manifest as the EPUB3 navigation document.
- Reordered the opening spine as cover, generated title page, frontispiece, extracted front matter, then chapters.
- Restored `.ornament` as a small centered title-page element.
- Added an EPUB audit failure when any manifest item with `properties="nav"` appears in the spine.

### 4. Validation
Regenerated Volume 1 only. Confirmed `nav.xhtml` has `properties="nav"` in the manifest and no `idref="nav"` in the spine. Confirmed the first spine idrefs are `chapter_0`, `chapter_5`, `chapter_1`, `chapter_2`, `chapter_3`, `chapter_4`, corresponding to cover, generated title page, frontispiece, and front matter. Confirmed `title.xhtml` contains `<p class="ornament">❧</p>` and the generated CSS displays it. EPUB audit reports 0 errors and 4 existing warnings.

---

## [Issue 66] Uppercase/Spaced Footnote Marker Residue

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
`ORIGINAL PREFACE` part 2 still rendered the source marker `[ F18]` literally instead of turning it into an EPUB noteref. This was especially concerning because footnotes must be reliable across the whole book, not merely visually improved in isolated places.

### 2. Root Cause
The footnote normalizer recognized loose lowercase forms and bracketed lowercase forms, but its compiled marker regex was case-sensitive. As a result, uppercase/spaced residues such as `[ F18]` bypassed normalization and reached rendered XHTML. The EPUB audit had the same blind spot because its literal-marker scan was also case-sensitive.

### 3. Fix
- Made `LOOSE_FOOTNOTE_MARKER_RE` case-insensitive in `converter.py`.
- Made `scripts/audit_epub.py` scan literal footnote markers case-insensitively.

### 4. Validation
Regenerated Volume 1 only. Confirmed `ch042.xhtml` now links the former `[ F18]` residue to `endnotes.xhtml#fn18`. A whole-EPUB scan found 0 literal footnote marker residues, 125 noteref links, 124 unique noteref targets, 124 endnote anchors, and 0 missing targets. The one duplicate target is `fn18`, now legitimately referenced from two locations. EPUB audit reports 0 errors and 4 existing warnings.

---

## [Issue 65] Contents Page Continuation Lines and Mobile Sizing

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The generated `CONTENTS OF VOLUME 1` page split one contents entry after `Peter’s Confession;`, leaving `Matthew 16:16 — Conceits of the Papists...` as a separate contents paragraph. The contents text also rendered small/tight for phone use.

### 2. Root Cause
`build_toc_page_xhtml()` converted every PDF text block without a fresh label into a separate `.ContentsItem`, even when it was a visual continuation of the preceding item after a semicolon. `.ContentsItem` also had no explicit mobile-friendly font size or line height.

### 3. Fix
- Join non-label contents lines into the previous `.ContentsItem` when the previous item ends with `;`, `—`, or `-`.
- Set `.ContentsItem` to `font-size: 0.95em` and `line-height: 1.45`.

### 4. Validation
Regenerated Volume 1 only. Verified `contents_2.xhtml` now keeps the Chapter 1 entry in one paragraph and generated `style/main.css` includes the new `.ContentsItem` size/line-height. EPUB audit reports 0 errors and 4 warnings. Text-integrity audit reports 0 inline structural marker candidates and 0 reference continuation splits.

---

## [Issue 64] Title-Page Styling and `here is ... 1.` Marker Promotion

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The `TWO SHORT CATECHISMS` title page rendered as an ordinary page with a visible ornament/debris mark and an unpolished descriptive block. In the body, `And here is, — Isaiah 44:3, 4, 1. A supposition...` remained inline instead of starting `1.` as a bold structural paragraph.

### 2. Root Cause
Generated title pages use `class="title-page"`, but the stylesheet only targeted `.titlepage`, so the intended title-page rules were mostly not applied. The list-marker splitter also suppressed plain numeric markers after scripture-reference tails to protect references, and the first post-processing pass was not enough for all chapter paths.

### 3. Fix
- Added `.title-page` coverage alongside `.titlepage` in the EPUB stylesheet, centered and italicized descriptive title-page prose, and constrained the title-page layout. The ornament was temporarily hidden in this pass and later restored under Issue 67.
- Added a final guarded inline-structural split pass before HTML rendering.
- Allowed a list-introduction cue such as `here is ... Isaiah 44:3, 4, 1.` to promote the `1.` marker despite the preceding scripture-reference tail.
- Updated the audit to allow a structural paragraph after a reference tail without counting it as a broken reference continuation.

### 4. Validation
Regenerated Volume 1 only. Verified `ch046_title.xhtml` is styled through `.title-page` rules in `style/main.css`, and `ch045.xhtml` now emits `<p><b>1.</b> A supposition...`. Text-integrity audit reports 0 inline structural marker candidates and 0 reference continuation splits. EPUB audit reports 0 errors and 4 warnings.

---

## [Issue 63] Inline Section Markers

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION) via Issue 70

### 1. The Problem
Several outline markers still remain embedded inside prose in the regenerated Volume 1 EPUB. Confirmed examples include `ch029.xhtml` with inline `4. Hitherto darkness...`, `ch030.xhtml` with inline `2. Our second direction...`, and `ch035.xhtml` with inline `6. Promises, prophecies...`. The user also reports a roman numeral case, `II. This darkness in the minds of men...`, and related ordinal forms such as `1st,` and `[5thly]` not starting on their own line. The former `[ F18]` footnote portion of this handoff is now tracked separately under Issue 66.

### 2. Why Existing Guards Missed It
The structural splitter still errs conservative around completed prose followed by numeric/roman markers, because earlier fixes had to avoid breaking scripture references such as `verse 7` or `1 Corinthians 1:13, 15`. Some markers become rendered bold HTML before the text audit checks them, so the current text-only inline marker scan reports 0 candidates even while `<b>4.</b>` remains embedded.

### 3. Follow-up Implementation
Issue 70 implements the handoff: source-like decimal/roman marker promotion, markdown-bold marker support, rendered XHTML audit detection, and regression checks for `ch029.xhtml`, `ch030.xhtml`, and `ch035.xhtml`.

---

## [Issue 62] `verse, N` Numeric Reference Continuation

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Volume 1 still had a reference continuation split in `ch019.xhtml`: `...gift of Christ,” verse,` ended one paragraph and `7. He has...` began a false numbered paragraph. The source text has this as `verse, 7. He has...`.

### 2. Root Cause
The numeric-continuation guard recognized paragraph endings such as `verse` and `verse.`, but not `verse,`. Once joined, the audit also treated `verse, 7.` as an inline structural marker because the inline-marker exemption only considered complete verse trails, not a reference stem ending in a comma.

### 3. Fix
- Broadened converter reference-stem matching from `verse.?` to `verse[.,]?` for `verse`, `verses`, `chap`, and `chapter`.
- Broadened the text-integrity audit reference-stem exemption so joined `verse, 7.` references do not become false inline-structural warnings.

### 4. Validation
Regenerated Volume 1 only. Verified `ch019.xhtml` now keeps `verse, 7. He has...` in one paragraph. Text-integrity audit reports 0 inline structural marker candidates and 0 reference continuation splits. EPUB audit reports 0 errors and 4 warnings.

---

## [Issue 61] Citation Continuation and Inline Bracketed Ordinal

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION) via Issue 70

### 1. The Problem
Two structural defects remain in Volume 1 after the latest rebuild. First, a patristic citation is split after `See August.`, leaving `Lib. con. Serm. Arian. cap. 35, and Epist. 66 ad Maximum.` as a false new paragraph in `ch004.xhtml`. Second, the marker `[1st,]` remains inline after `in such a season; —` in `ch013.xhtml` instead of beginning its own paragraph/list item.

### 2. Why Existing Guards Missed It
The reference-continuation logic handles several scripture and abbreviation tails, but this example starts the next paragraph with a citation chain (`Lib. con. Serm. Arian. cap...`) rather than ending the previous paragraph with `cap.` or `chap.`. The inline marker schema includes `[1st,]`, but the current promotion logic still misses at least the semicolon/dash lead-in form `; — [1st,]`. The audit also misses both cases, because it reports 0 reference-continuation splits and 0 inline structural marker candidates on the current EPUB.

### 3. Follow-up Implementation
Issue 70 implements the handoff: citation-start continuation joining after author cues, rendered marker auditing, and validation for the `See August. Lib. con. Serm...` and `[1st,]` examples.

---

## [Issue 60] Chapter Heading/Body Absorption Regression

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
After the front-matter heading work, ordinary chapter openings regressed: several chapters rendered `CHAPTER N`, the all-caps subtitle, and the first paragraph inside one huge `<h3>` element. This made chapter headings and opening paragraphs visibly broken.

### 2. Root Cause
PyMuPDF4LLM can emit a whole chapter opening as one Markdown heading, for example `###### CHAPTER 8 **SUBTITLE** A brief view...`. The existing splitter for plain `CHAPTER N ...` only ran when the paragraph was not already detected as a heading. The front-matter fix handled `PREFACE` and `PREFATORY NOTE` inline headings, but did not add the equivalent path for real chapter headings.

### 3. Fix
- Added a heading-path chapter splitter in `markdown_to_html()`.
- When a heading begins with `CHAPTER N`, the converter now emits the chapter number as `<h3>`, extracts bold all-caps text into `<h4 class="chapter-subtitle">`, and sends the remaining text through the normal paragraph path.
- Added an overlong-heading audit check to catch any future heading that likely swallowed body text.

### 4. Validation
Regenerated Volume 1 only. Verified `ch009.xhtml`, `ch010.xhtml`, and `ch012.xhtml` now separate chapter heading, subtitle, and first paragraph. A direct XHTML scan found 0 headings over 180 characters. EPUB audit reports 0 errors and 4 warnings. Text-integrity audit reports 0 overlong heading candidates, 0 front-matter heading/body candidates, 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

---

## [Issue 59] Prefatory Note OCR Blemishes and Heading/Body Regression Guard

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The `PREFATORY NOTE` heading on Volume 1 was no longer swallowing the body paragraph, but the opening paragraph still showed a severe OCR/source blemish: `To object of Dr. Owen...` instead of `The object of Dr. Owen...`. Nearby front-matter paragraphs had similar source-level defects, including `Own`, `Owens`, and `firsts as`. The catechism prefatory note also needed the same structural protection because it has a heading, an all-caps subtitle, and a body paragraph on the same PDF page.

### 2. Root Cause
The extracted PDF text itself contains several front-matter OCR defects, so paragraph reconstruction alone cannot infer the intended words. The front-matter heading split introduced for Issue 58 handled bare `PREFACE`/`PREFATORY NOTE` prefixes, but the audit did not yet have a direct check for future headings that accidentally contain prose.

### 3. Fix
- Added scoped front-matter phrase repairs for the Prefatory Note OCR blemishes.
- Broadened inline front-matter heading splitting to accept optional heading periods, preserving labels such as `PREFATORY NOTE.`.
- Added a text-integrity audit counter for chapter front-matter headings that look like they contain body text.

### 4. Validation
Regenerated Volume 1 only. Verified `ch003.xhtml` now has a separate `PREFATORY NOTE` heading followed by `The object of Dr. Owen...`. Verified `ch047.xhtml` now separates `PREFATORY NOTE`, the catechism subtitle, and the body paragraph, with `They were among the first, as...`. EPUB audit reports 0 errors and 4 warnings. Text-integrity audit reports 0 front-matter heading/body candidates, 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

---

## [Issue 58] Sliced Source Sentence, Verse-Range Continuation, and Prefatory Heading Styling

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Three serious extraction/styling failures remained in Volume 1. A scripture range was split as `Hebrews 10:19` followed by a new paragraph beginning `22.`. A Greek-bearing page lost the middle of a sentence around `Nestorius,f9`, producing the broken text `This being the 9 declare wherein he placed...`. The `PREFACE` heading was merged with the opening body paragraph and promoted as one large heading.

### 2. Root Cause
The paragraph-healing continuation rule handled references after `chap.` and comma-ended references, but did not recognize a bare verse range continuation after `Hebrews 10:19`. The Nestorius failure came from the font-aware extraction path used on pages with Greek spans; that path preserved the footnote marker but dropped the Latin words surrounding the overlay. The preface failure came from PyMuPDF4LLM extracting the line as `###### PREFACE` followed by body text, which became a single heading during paragraph reconstruction.

### 3. Fix
- Added verse-range continuation joining for `Book N:N` followed by a numeric continuation.
- Restored the known Nestorius sentence from the source wording when the font-aware extraction output collapses around the footnote overlay.
- Split inline front-matter heading prefixes into a heading element plus a normal paragraph.
- Added suspicious large-number paragraph-start auditing with suppression for legitimate numeric sequences.
- Added dense PDF source-window auditing to identify pages where source word windows are absent from the EPUB.

### 4. Validation
Regenerated Volume 1 only. Verified `ch024.xhtml` has `Hebrews 10:19-22`, `ch022.xhtml` has the full Nestorius sentence with footnote 9 in the correct place, and `ch004.xhtml` has a separate `PREFACE` heading followed by body text. EPUB audit reports 0 errors and 4 warnings. Text-integrity audit reports 0 inline structural marker candidates, 0 reference continuation splits, 0 suspicious large-number starts, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms. The new dense source-window scan reports 93 pages for triage; these are broad candidates rather than confirmed defects.

---

## [Issue 57] Scripture-Tail Structural Breaks and Reference Continuation Splits

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Two numeric-boundary failures remained after the footnote cleanup. A real structural marker, `(3.) Power`, stayed embedded after a scripture-reference tail, while a reference continuation around footnote 10 split `chap.` and `7:26` across paragraphs.

### 2. Root Cause
The inline structural splitter was intentionally conservative after scripture tails to protect references like `1 Corinthians 1:13, 15`, but that guard also blocked wrapped structural markers such as `(3.)`. Separately, the paragraph healer knew how to join non-terminal prose, but did not force a join when a paragraph ended with `chap.` and the next paragraph began with a chapter/verse number. A later text-continuation safeguard also rejoined markdown-bold ordinal markers such as `**1st**,` to their lead-in because the bold ordinal start pattern was too narrow.

### 3. Fix
- Allow wrapped structural markers after scripture-reference tails while continuing to protect bare numeric continuations.
- Add explicit reference-continuation healing for `chap.` / `7:26` and similar patterns.
- Append orphan scripture-reference fragments back to the previous paragraph when they are produced by a structural split.
- Broaden markdown-bold ordinal detection for `**1st**,`, `**2ndly**,`, and related forms.
- Extend the text-integrity audit with a `Reference continuation splits` counter.

### 4. Validation
Regenerated Volume 1 only. Verified `ch020.xhtml` starts `(3.) Power` in its own paragraph, `ch023.xhtml` keeps `chap. 7:26` together after footnote 10, and the following `1st`/`2ndly` markers start paragraphs. Text-integrity audit reports 0 inline structural marker candidates, 0 reference continuation splits, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms. EPUB audit reports 0 errors and 4 warnings.

---

## [Issue 56] Inline Footnote Placement and Catechism Doxology Layout

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The catechism footnote references were technically linked but visually collapsed into unreadable/tiny tap targets, especially where several notes were adjacent. The General Preface also showed a deeper placement bug: literal `fN` residue remained at the correct PDF positions while normalized `[fN]` markers from the extraction overlay were collected and appended later, creating false clusters such as notes 2 and 3 appearing together in the wrong paragraph. Closing doxologies in the catechisms were not separated from the main body.

### 2. Root Cause
`markdown_to_html()` treated footnotes as paragraph metadata. It collected every `[fN]` marker from the paragraph, stripped the markers from the text, and appended the resulting links at the paragraph end. That design could never preserve exact footnote positions. It also did not normalize loose AGES markers such as `f2` or `[ f1]`, so the right marker could remain as text while a duplicate overlay marker became a misplaced noteref.

### 3. Fix
- Normalize loose AGES footnote markers before paragraph conversion.
- Replace footnote markers inline through a parser-safe placeholder, restoring them only after emphasis and language tagging.
- Add a first-reference-wins guard so duplicate overlay markers for an already-linked footnote are dropped.
- Add `.noteref` spacing and padding for adjacent note references.
- Restore the Volume 1 title-page noteref for note 18, which PyMuPDF drops from the sparse title page, giving all 124 endnotes matching noteref anchors.
- Add `.doxology` rendering for the catechism closing lines.
- Extend `scripts/audit_epub.py` to fail on literal rendered `fN` residue or noteref links missing the spacing class.

### 4. Validation
Regenerated Volume 1 only. Verified General Preface notes 1-3 at their PDF/source positions, confirmed the false later 2/3 cluster is gone, confirmed catechism note clusters 83-85 and 86-90 render as separate spaced noteref anchors, confirmed both catechism doxologies use `class="doxology"`, and confirmed the package has 124 noteref links for 124 endnote anchors. EPUB audit reports 0 errors and 4 warnings. Text-integrity audit reports 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, 0 roman heading candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

---

## [Issue 55] Front-Matter Prose and Roman Outline Lists

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The front-matter pass still had false structure around prose references and scholarly citations. `Chapter 1 of the work...` in the Prefatory Note was promoted to a chapter heading, citation numbers after abbreviations such as `Epist.` and `lib. ... cap.` were treated as paragraph/list starts, and short roman outline entries were rendered as section headings rather than centered list items.

### 2. Root Cause
The plain chapter detector was case-insensitive, so prose `Chapter N` references looked identical to real `CHAPTER N` headings. The numeric marker splitter also treated any number after punctuation as potentially structural, without enough awareness of patristic/scholarly citation abbreviations. Finally, roman numeral handling had only two categories: summary list after words such as `heads:` and true section headings. It lacked a third category for short centered roman outline lists introduced by a dash or comma.

### 3. Fix
- Restricted plain chapter-heading promotion to uppercase `CHAPTER`.
- Added a citation-abbreviation guard for `cap.`, `chap.`, `lib.`, `serm.`, `sermo.`, `Epist.`, `Orat.`, `Tract.`, `Homil.`, `Haer.`, and related forms.
- Excluded four-digit parenthesized years from structural-marker matching.
- Added `.roman-list-item` rendering for short roman list entries after list-introducing prose while preserving long-form roman sections as `.roman-subheading`.
- Preserved all-caps front-matter labels in NAV/NCX.
- Updated the text-integrity audit to treat `.roman-list-item` as intentional.

### 4. Validation
Regenerated Volume 1 only. Verified the NAV/NCX all-caps preface labels, the Prefatory Note page 20 prose, citation continuations in `ch004.xhtml`, and the reported roman outline list examples in `ch031.xhtml` and `ch032.xhtml`. EPUB audit reports 0 errors and 5 warnings. Text-integrity audit reports 0 roman heading candidates, 0 inline structural marker candidates, 0 repeated word windows, and 0 missing enumerator marker forms.

---

## [Issue 54] Footnote and Catechism Cleanup

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The next visual pass found several extraction failures outside the earlier enumerator schema: plain chapter headings were not normalized, malformed markdown left `1.**` markers visible, the EPUB exposed a visible final Footnotes chapter, PDF-derived footnote text could be corrupted, and the catechism retained Q/A and scripture-reference ghost text from AGES footnote/column layers.

### 2. Root Cause
There were three separate causes:
- Some chapter headings arrived as plain body paragraphs rather than Markdown headings.
- The original ThML footnote parser did not reliably collect text between adjacent `<a class="fnmarker">` markers, so the converter fell back to noisier PDF footnotes.
- Catechism pages contain dense Q/A text, footnote markers, scripture references, and repeated column/footnote material, so ordinary paragraph de-duplication could not tell when text from the following answer had been pulled into the current one.

### 3. Fix
- Added plain `CHAPTER N TITLE` normalization and shared heading sanitation.
- Repaired malformed structural-marker markdown before bold conversion.
- Rebuilt ThML footnote parsing with `lxml` sibling traversal, yielding all 124 clean Volume 1 notes.
- Kept `endnotes.xhtml` as a hidden manifest resource with semantic footnote/endnote roles, but removed it from the reading spine and navigation.
- Escaped footnote text before language tagging to avoid raw/escaped span artifacts.
- Added catechism-specific Q splitting, scripture-spill filtering, duplicate answer-opening removal, adjacent repeated-run cleanup, following-answer ghost removal, and source-confirmed repairs for the Chapter 18 vocation answer text.

### 4. Validation
Regenerated Volume 1 only. Verified the reported Chapter 15 headings, the `1.**` marker, hidden clean footnotes, clean footnote 4, and the Chapter 18 vocation catechism section. EPUB audit reports 0 errors and 5 warnings. Text-integrity audit reports 0 repeated word windows, 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, and 0 roman heading candidates. Remaining warnings are treated as triage, not user validation.

---

## [Issue 53] Numeric Reference Continuations and Enumerator Schema

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Volume 1 still had extraction artifacts clustered around small numeric markers: inline `1st,`/`2ndly,` labels, continuation references such as `verse 60` and `1 Corinthians 1:13, 15`, a false split at `45th Psalm`, duplicated `chap.` overlap text, malformed `Ans . 1`, a trailing roman `II.` merged into an all-caps subtitle, and roman summary-list labels being mistaken for centered subsection headings.

### 2. Root Cause
The paragraph healer needed a more precise distinction between three visually similar cases:
- structural list markers that should start paragraphs,
- numeric scripture or verse continuations that should stay inside the same sentence,
- ordinary ordinal phrases that should not be treated as list markers.
- roman numerals used as true subheadings versus roman numerals used as summary-list labels after introductions such as `four heads:`.

AGES ghost layers also repeat tails around scripture references, so exact adjacent-line de-duplication was insufficient for cases where the repeated clause restarted after a reference-heavy gap.

### 3. Fix
- Refined the structural-marker regexes to exclude ordinary ordinals such as `45th Psalm` while preserving real starts like `(1.)`, `(1st,)`, `[1.]`, `1st,`, and `2ndly,`.
- Added inline marker promotion so enumerators embedded after introductory prose become paragraph starts.
- Added continuation healing for `verse`, `chap.`, and scripture-reference tails followed by numeric lines.
- Added adjacent overlap trimming and interrupted duplicate-clause pruning for scripture-reference-heavy ghost tails.
- Normalized `Ans . N` labels.
- Split trailing roman subtitle markers into `.roman-subheading`.
- Extended the schema to markdown-bold decimal/list markers, short lead-ins such as `For — (1.)`, and duplicated leading scripture-reference runs across a multi-paragraph lookback.
- Extended inline promotion to markdown-bold wrapped ordinal forms such as `**(1st,)**` and `**(3rdly,)**`.
- Added guarded plain-decimal promotion for cases such as `two ways: — 1. ... 2. ...`, while preserving scripture and citation continuations such as `1 Corinthians 1:13, 15`, `Revelation 2, 3`, `verse 60`, and `lib. 5 cap. 8, 9`.
- Updated `.roman-subheading` styling so roman sub-subheadings are centered and use `break-after/page-break-after: avoid` to keep them with the following paragraph instead of stranded at the foot of a page.
- Added roman-list coalescing for sequences introduced by `heads:`, `ways:`, `parts:`, `sorts:`, or `things:`. These now render as list paragraphs such as `<p><b>I.</b> Honor.</p>`, while later section-opening roman numerals remain centered `.roman-subheading` elements.
- Tightened `scripts/audit_text_integrity.py` so it reports non-terminal paragraph breaks, inline structural markers, and roman numeral headings left in body paragraphs.

### 4. Validation
Regenerated Volume 1 only and inspected the generated XHTML for the reported examples. The EPUB audit reports 0 errors. The text-integrity audit reports 0 missing top-of-page body windows, 0 missing enumerator marker forms, 0 enumerator sequence candidates, 0 adjacent duplicate paragraphs, 0 inline structural marker candidates, and 0 roman heading candidates. Remaining mechanical warnings are weak page coverage from converted Greek/Hebrew, possible non-terminal paragraph split candidates, and two repeated word windows.

---

## [Issue 50] Textual Integrity Audit & Paragraph Healing Enforcement

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
The initial textual-integrity audit showed that Volume 1 still contained likely paragraph fractures even after earlier paragraph-healing work. The broad EPUB package audit could confirm structural validity, but it could not answer the more important question: whether the EPUB text was faithful, continuous, and free of extraction damage.

The first pass of `scripts/audit_text_integrity.py` found:
- 817 possible faulty paragraph split candidates.
- 5 adjacent duplicate paragraph candidates.
- 0.9854 approximate PDF-to-EPUB content-word coverage.

### 2. Root Cause
Two converter behaviors were working against the project mandate for holistic paragraph healing:

1. `get_pages_text()` was reconstructing paragraphs page-by-page, then joining page results. This allowed extraction boundaries to become EPUB paragraph boundaries.
2. Early chapter body text could bypass the healer because `healer_active` depended on a `healer_page` front-matter heuristic. This caused the General Preface and similar early material to retain PDF line fragmentation.

### 3. Fix
- Added `scripts/audit_text_integrity.py`, which compares source PDF extraction against generated EPUB text and flags:
  - weak page-level source matches,
  - possible faulty paragraph splits,
  - short fragments,
  - adjacent duplicate paragraphs,
  - repeated word windows,
  - approximate content-word coverage.
- Changed `get_pages_text()` to merge the entire chapter/range raw text first, then run cleaning and `reconstruct_paragraphs()` once.
- Changed `reconstruct_paragraphs()` so blank extraction separators only end a paragraph when the current text already ends with terminal punctuation.
- Changed normal chapter body extraction to always use the healer. Title/TOC/front-matter preservation still uses the separate layout path.
- Added a structural-start grammar to both the converter and audit so legitimate Owen paragraph starts are preserved and not reported as false split candidates. This covers numeric heads (`5.`), parenthesized numeric heads (`(1.)`), bracketed labels, roman numerals, catechism `Q.`/`A.`, ordinal heads (`2ndly`), and common discourse labels (`First,`, `Secondly,`, `Lastly,`).

### 4. Validation
After regenerating Volume 1:
- Possible faulty paragraph split candidates dropped from 817 to 3.
- Adjacent duplicate paragraph candidates dropped from 5 to 0.
- Body paragraph count dropped from 5122 to 2390, indicating that fragmented PDF lines were consolidated into healthier reflowable paragraphs.
- Approximate PDF-to-EPUB content-word coverage remained 0.9854.
- After the structural-start guard, the audit excluded 57 legitimate structural starts from false split warnings in Volume 1.

Remaining warnings are now narrower: three split candidates tied to footnote/page-number residue in catechism-style material, repeated word-window samples, and weak page matches where raw PDF extraction contains legacy Greek transliteration while the EPUB contains converted Unicode.

---

## [Issue 51] Chapter Subtitles & Scripture-Reference Ghost Duplicates

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Visual review of Volume 1, Chapter 6 showed that the chapter subtitle was being merged into the opening body paragraph. The same area exposed scripture-reference duplication: repeated opening prose and a repeated reference tail were present after the main paragraph.

### 2. Root Cause
The converter treated the first paragraph after a chapter heading as ordinary body text, even when it began with bold all-caps subtitle runs. Separately, AGES ghost/reference layers could surface as duplicate scripture lists that were not always exact adjacent-line duplicates.

### 3. Fix
- Added `_split_leading_chapter_subtitle()` to detect leading bold all-caps subtitles and emit them as `<h4 class="chapter-subtitle">`.
- Added `.chapter-subtitle` styling to `shared.py`.
- Added paragraph post-processing for:
  - duplicated opening clauses,
  - duplicate scripture-reference tails,
  - standalone scripture-reference fragments already represented in the previous paragraph.

### 4. Validation
Volume 1 was regenerated and Chapter 6 now emits:

```html
<h3 class="secondary">CHAPTER 6</h3>
<h4 class="chapter-subtitle">THE PERSON OF CHRIST THE GREAT REPOSITORY OF SACRED TRUTH — ITS RELATION THEREUNTO.</h4>
<p>Divine supernatural truth is called...</p>
```

The highlighted duplicate "So we are said..." opening and the standalone repeated reference tail after it are removed. The EPUB package audit's repeated phrase count dropped from 10 to 7, and the textual-integrity audit reports 59 detected chapter subtitles in Volume 1.

---

## [Issue 52] Enumerator Integrity and Top-Margin Clipping

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
Volume 1 Chapter 9 showed `[2.]` in the EPUB while the preceding `[1.] With the same honor...` text was missing. The source PDF did contain `[1.]` at the top of page 148.

### 2. Root Cause
Pages with Greek/Hebrew spans use the font-aware PyMuPDF extraction path. Its top-margin cutoff was 65pt, which removed the first two body lines on page 148 while preserving the third line, causing the EPUB to begin mid-paragraph at "give glory...".

### 3. Fix
- Lowered the cutoff to 40pt and filtered page numbers/running headers explicitly in the top band.
- Added bracketed/parenthesized ordinal guards such as `[1st,]` and `(1st,)`.
- Bolded structural markers at paragraph starts so visible enumerators keep their PDF-like emphasis.
- Extended `scripts/audit_text_integrity.py` with an enumerator-integrity check that compares bracketed/parenthesized marker forms between PDF and EPUB and reports sequence jumps.
- Added a top-of-page body-window check that samples the first real body lines of each PDF page and verifies that stable Latin text survives in the EPUB. Font-encoded Greek/Hebrew windows are counted separately as unstable rather than treated as clipping failures.

### 4. Validation
Regenerated Volume 1 only. `EPUB/ch013.xhtml` now contains `[1.] With the same honor...`, `[2.] In the same manner...`, `[1st,] that their thoughts...`, and `[2ndly,] Such persons...`. The latest text audit reports 0 missing top-of-page body windows, 0 missing enumerator marker forms, and 0 enumerator sequence candidates.

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

---

## [Issue 69] Enhanced Extraction Testing & Bottom-Clipping Discovery

**Date:** 2026-05-11
**Status:** IMPLEMENTED (AWAITING VALIDATION)

### 1. The Problem
While the converter had high word-coverage (≈98%), visual inspection alone could not guarantee that no text was lost near difficult PDF boundaries (like footnote-heavy page bottoms) or that all ghost-layer duplicates were pruned. Heuristic audits were helpful but lacked deterministic regression safety for known fragile pages.

### 2. The Solution: Comprehensive Hybrid Testing
We implemented a two-tier testing strategy:

1.  **Deterministic Regression (Golden Masters):**
    - Created `tests/test_golden_pages.py` using `pytest`.
    - It extracts specific high-risk pages (TOCs, mixed-font pages, ghost-layer risk pages) and compares the text against a validated "Golden Master" baseline in `tests/baselines/`.
    - This prevents future code changes from silently re-introducing extraction regressions on the most complex pages of the collection.

2.  **Heuristic Enhancement (Integrity Audit):**
    - **Bottom-of-Page Integrity:** Added `bottom_of_page_integrity()` to `scripts/audit_text_integrity.py`. It samples the last 2 lines of the main body block on every PDF page and verifies their presence in the EPUB.
    - **Global N-Gram De-duplication:** Upgraded `repeated_windows()` to scan the entire text for non-consecutive n-gram repetitions (size 10+). This is much more effective than sequential line-by-line checks for catching complex ghost-layer "stuttering."

### 3. Discovery & Analysis of Findings
The first run of the enhanced audit on Volume 1 revealed significant previously hidden defects:

-   **Bottom-Clipping (42 Pages):** The audit flagged 42 pages where the final body lines were not found in the EPUB.
    - *Example Page 27:* Lost "...rock is not called Petra from Peter, but Peter is so called".
    - *Root Cause:* Pages with dense footnotes or complex overlays (like those using font-aware extraction) have tighter bottom margins. The 50pt global bottom margin was too aggressive for these layouts, causing the final lines of the body text to be clipped as if they were footers.
-   **Persistent Duplicates (25 Clusters):** The n-gram scan identified 25 recurring phrases, such as a 4-fold repetition of the "Worthy is the Lamb..." doxology.
    - *Root Cause:* These are "interrupted duplicates" where the ghost layer repeats a whole section after a scripture-reference break, bypassing the sequential de-duplicator.

### 4. Follow-up Implementation
The first recovery pass reduced `BOTTOM_MARGIN` from `50` to `25`. This keeps a footer safety band, but stops treating legitimate low body lines as page debris. The change is intentionally conservative: it recovers body text before adding a more complex page-by-page dynamic redaction rule.

Confirmed recovered examples in the unpacked Volume 1 EPUB include:

- `rock is not called Petra...`
- `Council of Nice...`
- `Lib. De Incarnat...`

### 5. Remaining Risk
The margin change materially improves extraction, but it does not eliminate the warning class. After regenerating Volume 1:

- approximate PDF-to-EPUB word coverage improved to `0.9915`;
- weak page matches dropped to `8`;
- missing bottom-of-page windows dropped from `42` to `20`;
- repeated word windows remain at `25`.

The remaining `20` bottom-window samples may include unstable extraction windows, footnote-region ambiguity, or real body text still being lost. They should be triaged before this issue is marked validated.

### 6. Validation
- `pytest tests/test_golden_pages.py` passed with 2 test cases during the enhanced-audit implementation.
- Regenerated Volume 1 only after reducing `BOTTOM_MARGIN`.
- `audit_text_integrity.py` correctly tracks the residual bottom-of-page warnings in `BUGS_AND_FIXES.md`.
