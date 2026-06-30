# Volume 1 Build and Audit Analysis

Generated: 2026-05-17

## Build Result

Volume 1 was rebuilt through the preferred per-volume pipeline:

```bash
.venv/bin/python3 volumes/v1/convert.py
```

Outputs:

- EPUB: `volumes/v1/output/volume_1.epub`
- JSON intermediate: `volumes/v1/intermediate/volume_1.json`

Build summary:

- Stage 1 extraction completed successfully.
- Stage 2 render completed successfully.
- Rendered structure: 78 chapters, 124 footnotes.

## Audit Result

Reports generated:

- `volumes/v1/bugs_fixes/volume_1_audit.md`
- `volumes/v1/bugs_fixes/volume_1_audit.json`
- `volumes/v1/bugs_fixes/volume_1_text_integrity.md`
- `volumes/v1/bugs_fixes/volume_1_text_integrity.json`
- `volumes/v1/bugs_fixes/volume_1_bug_regressions.md`
- `volumes/v1/bugs_fixes/volume_1_bug_regressions.json`

Overall status:

- EPUB audit: WARN
- Text integrity audit: WARN
- Bug regression budget: PASS

## High-Level Assessment

Volume 1 is structurally sound as an EPUB package. The EPUB audit found 0 errors, valid EPUB3 metadata, a valid spine/navigation structure, embedded fonts, no AGES boilerplate residue, no possible Beta Code residue files, no escaped language-tag files, no empty bracket noise files, and no missing chapter initialization files.

The text-integrity audit also shows strong broad coverage: the approximate PDF-to-EPUB coverage ratio is 0.9983, Greek word coverage is 0.9987, and Hebrew word coverage is 1.0. These are good collection-level signals.

The remaining warnings are not packaging blockers. They are quality-triage items around Greek clause matching, paragraph classification, repeated phrase detection, and a few source-window misses at page boundaries.

## Key Metrics

EPUB package:

- Errors: 0
- Warnings: 4
- Files: 105
- Manifest items: 96
- Spine items: 83
- XHTML files: 84
- Embedded fonts: 8
- NAV links: 82
- Noteref links: 130
- Endnote anchors: 124

Text integrity:

- PDF pages: 644
- EPUB text files: 83
- EPUB paragraphs/headings: 3203
- PDF content tokens: 210900
- EPUB content tokens: 214406
- Coverage ratio: 0.9983
- Weak page matches: 5
- Missing top-of-page body windows: 2
- Missing bottom-of-page body windows: 22
- Possible faulty paragraph splits: 76
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Repeated word windows: 25
- Missing Greek clauses: 16
- Missing Hebrew clauses: 0

Regression gate:

- PASS against current Volume 1 regression budgets.
- All tracked bug classes are within budget.

## Findings To Triage

### 1. Greek Clause Fidelity

The largest meaningful quality warning is `missing_greek_clauses`: 16 of 44 dense Greek clauses were not matched by the text-integrity audit.

This does not necessarily mean the EPUB has lost all Greek content. The EPUB has 835 Greek words against 824 PDF Greek words, and Greek word coverage is 0.9987. The warning is more likely about clause-level normalization, font conversion differences, dropped breathings/accents, or audit matching sensitivity around dense Greek spans.

Recommended next step:

- Inspect the listed pages first: 26, 31, 32, 37, 42, 57, 105, 109, and 293.
- Compare source PDF span extraction, JSON intermediate, and rendered XHTML for those pages.
- If the EPUB contains the Greek but with normalization differences, tune the audit rather than the converter.
- If clauses are genuinely absent, add targeted extraction/render regression samples.

### 2. Untagged Greek

The EPUB audit found 8 Greek characters outside `lang="el"` context. Samples are mostly short `κ.τ.λ.` fragments in chapters 4, 5, and 19.

Recommended next step:

- Add or adjust a small render-stage tagger rule for short Greek abbreviation fragments.
- This looks narrow and low risk because Hebrew tagging is clean and broader Greek tagging is already mostly working.

### 3. Paragraph Split Candidates

The audit reports 76 possible faulty paragraph splits. The first several samples are scholastic/citation fragments in `EPUB/ch004.xhtml`, such as `Aquin. 22 q., 81,` followed by `a. 3, ad prim., and q., 84,`.

Some later samples are chapter-title-to-opening transitions and may be false positives rather than actual broken prose.

Recommended next step:

- Separate true citation continuations from heading/opening false positives.
- Start with `EPUB/ch004.xhtml`, because the samples are concrete and likely repairable through citation-continuation handling.
- Avoid broad paragraph-healer changes unless a specific pattern is confirmed.

### 4. Repeated Phrase Windows

The text-integrity audit reports 25 repeated word windows, and the EPUB audit reports 5 repeated phrase hits. The samples are common theological/title phrases, especially "the glory of Christ" and chapter-title language.

Recommended next step:

- Treat these as likely false positives unless visual inspection finds duplicated paragraphs.
- Keep the current budget unchanged until a concrete repeated-text defect is confirmed.

### 5. Endnote / Noteref Count Mismatch

The EPUB audit reports 130 noteref links and 124 endnote anchors, with an `orphan_endnotes` warning.

Recommended next step:

- Inspect whether the six-link difference comes from repeated references to the same endnote or genuine missing endnote anchors.
- If repeated references intentionally point to a single endnote, the audit language may need refinement.

### 6. Page Boundary Source Windows

The text-integrity audit reports 2 missing top-of-page windows and 22 missing bottom-of-page windows. Many samples look like scripture-reference boundary fragments or unstable page-edge extraction.

Recommended next step:

- Review the top-of-page samples on pages 157 and 619 first.
- Review bottom-page samples where wording looks semantically broken, especially pages 99, 105, 156, and 302.
- Do not treat all page-window misses as defects without PDF/EPUB side-by-side confirmation.

## Recommended Priority Order

1. Greek clause fidelity samples, because this is the most content-sensitive warning.
2. Untagged short Greek abbreviation fragments, because the fix is likely narrow.
3. `EPUB/ch004.xhtml` citation paragraph splits.
4. Endnote/noteref mismatch classification.
5. Page-boundary source-window samples.
6. Repeated phrase windows, only if manual inspection confirms actual duplicate prose.

## Validation Note

This analysis records the current automated audit state after a fresh build. It does not mark any issue as fixed or validated. Any status changes in `BUGS_AND_FIXES.md` should wait for explicit user validation.
