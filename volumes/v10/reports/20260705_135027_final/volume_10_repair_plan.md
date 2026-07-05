# Volume 10 Heal Repair Plan

Generated: 2026-07-05
Branch: `heal-v10-20260705`

## Target

Heal one Owen Works volume only: Volume 10.

Fresh baseline reports placed Volume 10 below the mandatory green threshold already, but with visible residual defects. This pass focused on high-confidence converter repairs that reduced malformed rendered text without modernizing historical spelling or widening scope to other volumes.

## Checklist

- [x] Create a standard git branch for the heal pass.
- [x] Rebuild Volume 10 from the local `.venv/` and `./owen` wrapper.
- [x] Capture baseline EPUB, text-integrity, anomalies, unmatched-quotes, and bug-regression reports.
- [x] Repair malformed Volume 10 title-page HTML.
- [x] Repair clear OCR/reference corruptions in scripture references.
- [x] Repair the John 3:3 / John 3:6 raw-text split around the Remonstrant quotation.
- [x] Repair the raw table-continuation fragment in the providence/free-will antithesis.
- [x] Prune stale whitelist entries that final audits no longer emit.
- [x] Re-extract, re-render, and re-run the focused Volume 10 audit suite.
- [x] Archive final reports under `volumes/v10/reports/`.

## Remaining Review Items

- [ ] Modern-notes editorial enrichment: 2 unresolved main-body references, 2 untranslated substantial foreign passages, and 69 unenriched legacy footnotes.
- [ ] Latin quality: Latin word coverage is high, but tagging and translation coverage remain below PRISTINE thresholds.
- [ ] Syllabus-anchor triage: 25 observed candidates remain against a regression budget of 16.
- [ ] One paragraph-split candidate remains in `EPUB/ch021.xhtml`.
- [ ] Focused pytest still fails for v10 because the baseline does not allow the new modern-notes warning codes; the same run also reports unrelated failures in other volumes.

## Whitelist Handling

No new whitelist entries were added in this heal pass. Stale Volume 10 whitelist entries were removed where the latest audits no longer emit the corresponding issue.
