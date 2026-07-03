# V1 Textual Issue 53

## Goal

Agree on a bounded, auditable fix plan for `volumes/v1/bugs_fixes/textual.txt` issue `#53`, then implement it on a normal Git branch, rebuild Volume 1, and produce targeted verification reports.

## Decisions

- Interview goal: plan then implement a bounded repair for Volume 1 textual issue `#53`.
- Scope narrowed by user: fix only item `## 53` in `volumes/v1/bugs_fixes/textual.txt`.
- Target behavior: only the Hebrews 2:14/16 quotation and Philippians 2:6-7 quotation should render as blockquotes; the explanatory prose beginning `and in sundry other places...` must render as a normal paragraph.
- Initial finding: Stage 1 JSON already has two `[[BLOCKQUOTE]]` markers at the right starts, but the final EPUB merges both quotations and the following prose into one blockquote during render-side adjacent blockquote handling.
- Implemented decision: fix render-side healing, not extraction. Preserve plain-prose mid-sentence blockquote repair, but prevent closed/marked blockquotes from swallowing the next blockquote or following lowercase exposition.
- Verification decision: use focused pytest coverage plus Volume 1 render-only, EPUB audit, text-integrity audit, and direct XHTML inspection for `EPUB/ch022.xhtml`.

## Open Questions

- User validation is still required before marking issue `#53` as fixed in project status docs.
