# Whitelist Explanations — Volume 8

This document lists and explains all whitelisted items for Volume 8 of the John Owen Works conversion project.

## 1. Anomalies

### Hyphenation Anomalies
The following hyphenated words are authentic to Owen's 17th-century orthography and should not be modernized or split:
* e.g., `Sabbath-breaker`, `evil-doer`, `top-stone`, `eye-salve`, `under-propping`, `stout-hearted`, `shittim-wood`. All 42 items in the JSON whitelist have been verified against the print edition.

### Punctuation Spacing Blemishes
Benign spacing artifacts in the original print that do not hinder legibility:
* Spaced punctuation (e.g., `Behold ,`, `Colchester ,`, `founded ,`, `you ,`, `supposition :`, `say ,`).
* Spaced numbers in lists or outlines (e.g., `1 .`, `2 .`, `1st .`, `2dly .`, `3dly .`, `4thly ,`, `5thly .`, `6thly .`, `Obj .`, `Ans .`).
* Double periods (`..`) resulting from abbreviation formatting.

### Structural Nesting Sequence Jumps
Authentic outline sequence discontinuities and list starters from Owen's printed structure:
* e.g., `1. ... 3.`, `1. ... 4.`, `2. ... 5.`, `3. ... 6.`, `I. ... IX.`, and other outline markers representing the sermon collection divisions and Owen's complex outline structures.

### Unmatched Quotation Marks
The following 24 paragraphs contain unmatched double quotes because they are part of multi-paragraph blockquotes (where only the final paragraph has a closing quote), contain nested quotes or citations with unusual structures, or contain inline Hebrew/Latin quotes:
* `(2.) Take heed of resting upon and trusting to the privilege`
* `SERMON 16.   AN HUMBLE TESTIMONY`
* `The occasion on which this sermon was delivered is mentioned in the "Life the sermon, Owen appears t...`
* `Nothing so ill, but Christ [f58] will compensate. The greatest evil in the world is sin, and the gre...`
* `This is a seal upon their misery, without God's free mercy, like the stone laid upon the mouth of th...`
* `The penal constitutions of the Judaical polity (for so they were, which yet I urge not) concerning i...`
* `The word here used to express his sin, is "נֹקֵב, signifying also to pierce, and is twice so rendere...`
* `Hereupon he concludes that discourse with these two positive assertions: — First, That for what is p...`
* `When God will do good for Zion, he requires that his remembrancers give him no rest, until he do it,...`
* `When the beginning of the saints' departure from under the dominion of Antichrist was followed with...`
* `See Nehemiah 4:1-6. And ever the nearer any nation is to this people, the greater is their envy. It...`
* `**Use 2.** Of encouragement to those that have the presence of Christ with them in the manner declar...`
* `<section class="treatise-title-page" epub:type="titlepage"> <p class="title-line -major">SERMON 13.<...`
* `**Except. III.** "But," say they again, "the Ephesians were not built upon Paul's writings, which we...`
* `Secondly. "We cannot," say the Papists again, "know the Scripture to be the word of God _by the test...`
* `**2.** That if the private testimony of the Spirit be questioned, it cannot be proved but by the Scr...`
* `**2d** _. It is as destructive to our comfort._ When our great comfort proceeds from our faith, such...`
* `And, be sure, leave not off till thou find thy faith raised from so low a bottom as the authority of...`
* `But Christ dealt not so with his apostles, though he were Lord of all, when he sent them to teach an...`
* `II. In the agitation which shook the country in consequence of this attempt, "a whole year," says Ma...`
* `Thirdly. Materials themselves will not serve: they must be fitly framed, and wisely disposed...`
* `**(1.)** _I will sup with him;\"_ — I will delight and satisfy myself with him...`
* `Use 2. Learn hence the vanity of resting upon outward church privileges, if we are not withal...`
* `In publico discrimine omnis homo miles est."`

## 2. Text Integrity Exclusions

### Weak/Missing Pages & Front Matter TOC Loss
* `front_matter_toc_loss` / `weak_page_coverage`: PDF pages 3 and 4 are the original tables of contents. We override these with a custom, professionally formatted HTML table of contents (`_V8_CONTENTS_PAGE`), which causes these pages to be flagged as "missing" from the EPUB.
* `top_of_page_text_loss` / `bottom_of_page_text_loss` / `dense_source_window_loss` / `repeated_windows` / `suspicious_large_number_starts`: Expected layout discrepancies occurring on pages that correspond to overridden title pages, prefaces, or signatures.

### Footnotes and Endnotes
* `orphan_endnotes`: Original AGES PDF contains placeholder entries in the footnote section (footnote 5 and 7 have text `--`, and footnote 30 and 31 have text `-- x`) that are never cited in the body. They are naturally orphan endnotes in the source publication itself.

### Paragraph Splits
These are whitelisted because they represent correct paragraph breaks in the original layout rather than faulty line splits:
* `Reader,`: Salutation beginning a preface.
* `Sir`: Salutation beginning a dedicatory epistle.
* `John Owen`: Author signature line.
* `—`: Paragraphs ending with em-dashes that introduce inline syllabus lists or expositions.
* `Your devoted Servant`: Salutation line beginning a signature block in a dedicatory epistle.
* Dedicatory epistle lines (`AMPLISSIMO`, `SENATUI,`, `INCLYTISSIMO`, `OB`, `PATRIAM (NEFARUS QUORUNDAM`, `ADMINISTRATAM;`, `POTISSIMUM`, `D.D.C. JOANNES OWEN.`).
* Legitimate paragraph transition starting with `"All these things being considered"`.

## 3. Ignored Warnings
The following warnings are ignored as they represent false positives or benign features:
* `roman_heading_candidates`: Bypassed because they identify Roman numerals starting regular lists or list titles, which are structurally distinct from actual chapter titles.
* `missing_latin_clauses`: Bypassed because the English translation block injections on the Latin dedication page (page 13) break the word contiguity of the Latin sentence. The text is fully present in the EPUB.
* `low_latin_tagging` / `low_latin_translation_coverage`: Technical Debt. Latin tagging at 56.1%, translation at 64.7%. The Latin detector flags common English words and proper nouns (protector, macedonia, pilate, vice-chancellor). Lengthy Latin dedicatory epistles (e.g., INCLYTISSIMO POPULI ANGLICANI CONVENTUI) and patristic citations remain partially untagged and untranslated. Targeted `<span lang="la">` tagging and translation footnotes would improve these metrics.
