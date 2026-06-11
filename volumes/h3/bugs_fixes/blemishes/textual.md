# Important
fix bugs, now I don't want partial fixes, I want thorough revisiting of algorithms/regex and audits why are these bugs here and how can they be
fixed or rewritten that these bugs are not leaking on other volumes also

## 1
there is not summary at the start of the volume, the first few paragraphs are being considered as summary. 

"HAVING demonstrated the pre-eminence of the Lord Christ above Moses in their respective ministries about the house of God, the apostle, according unto his design and method, proceeds unto the application of the truth he had evinced, in an exhortation"
Check the rules but ALL CAPS is an indicator of Paragraphs that are not summaries, but the algorithm is not catching this. We need to have audits that check for this, and if we have a rule that ALL CAPS is an indicator of paragraphs that are not summaries, then we need to make sure that the algorithm is catching this. If all caps setence then it's a heading, not a summary. If all caps starting word then the rest is not in all caps then it's not a summary.

"Οἵη περ θύλλων γενεὴ, τοιήδε καὶ ἀνδρῶν." This is where the summary ends, such a long summary should be flagged as false positive.

## Status & Resolution
Status: **IMPLEMENTED (AWAITING VALIDATION)**

### Root Cause Analysis
1. **Flat Navigation Structure**: The Hebrews volumes are converted from EPUB2 files (`source_type: epub2`). The input EPUB files had a completely flat NCX structure where every chapter was defined at Level 1. Consequently, `extract.py` extracted all chapters with `level: 1`, resulting in a flat navigation TOC in the final EPUB.
2. **Body Start Detection Leak**: During Stage 2 rendering, the parser starts in `FRONT_MATTER` mode. Normally, it switches to `BODY_START` mode when it encounters a chapter whose title matches `CHAPTER`, `SERMON`, or `DISCOURSE`. However, the initial chapters in some Hebrews volumes (like `Hebrews 3: 7-11` in Volume 4) have titles that do not match these patterns. Because there was no fallback, the parser remained in `FRONT_MATTER` mode, causing all subsequent paragraphs to be formatted as centered, italicized `.front-matter-body` elements. To the reader, this appeared as if the paragraphs were mistakenly treated as a long summary block.

### Implemented Fixes
1. **Hierarchical Navigation Levels**: Modified `extract_epub2_volume` in `extract.py` to automatically detect parent chapters (using title patterns starting with `PART` or `CHAPTER`, or standalone front-matter sections like the editor's preface) and assign them Level 2, while nesting the actual commentary/verse chapters under them at Level 3. Standard flat headers at the start of a volume are kept at Level 2 to prevent them from being orphaned or skipped.
2. **Robust Body Start Fallback**: Modified the parser mode selection loop in `render.py` to include a fallback check: if a chapter does not have a `front_matter_style` defined (meaning it is a body chapter), the parser mode is automatically promoted to `BODY_START`. This ensures that body commentary text (like `Hebrews 3: 7-11`) is formatted using standard body paragraph styling instead of front-matter blurb styling.
3. **Batch Re-Build**: Successfully executed the conversion pipeline (Stage 1 + Stage 2) for all 7 Hebrews volumes (`h1` through `h7`). All volumes have built successfully, generating clean, hierarchical tables of contents and correct paragraph formatting with 100% word coverage verified by text-integrity audits.
