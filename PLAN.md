# John Owen Works — Active Plan

Last updated: 2026-05-11

## Current Focus

Stabilize and validate the 16-volume Owen Works EPUB3 pipeline. Hebrews is parked until the Owen volumes are done.

The active converter is `converter.py`, a PyMuPDF/PyMuPDF4LLM pipeline that extracts AGES PDFs, repairs text, converts Greek/Hebrew legacy encodings, merges footnotes, and packages EPUB3 files.

Operational rule: work on one volume at a time. Do not run batch conversion or batch audits unless the user explicitly asks for them.

## Current State

- All 16 Owen volumes have generated EPUB outputs in `volumes/vN/output/`.
- Volume 1 has received the deepest recent QA and repair work.
- Issues 38-42, 44, 48, and 49 are implemented but should remain validation-safe in per-volume logs unless the user explicitly approves them.
- Issue 43 blockquote detection was reverted because it damaged heading extraction.
- The `--hebrews` flag exists but is not implemented.
- `shared.py` lists CCEL XML sources for volumes 5 and 10, but the current `process_owen_volume()` still uses the AGES PDF path for every volume.

## Guiding Decision

Keep the PyMuPDF-based converter as the primary pipeline.

This project needs book-specific logic that generic PDF-to-EPUB tools will not handle well:

- AGES headers and footers
- old embedded Greek and Hebrew font encodings
- ghost text layers and phrase duplication
- page-boundary paragraph breaks
- footnote marker and endnote reconciliation
- multi-level theological treatise navigation
- EPUB3/Apple Books packaging details

Use alternate extractors as audit tools, not as replacement pipelines.

## Documentation Structure

Root files should stay small and active:

- `README.md`: project overview and quick start
- `AGENTS.md`: agent instructions and operating constraints
- `GEMINI.md`: mandatory project protocols
- `PLAN.md`: active roadmap
- `ENGINEERING_LOG.md`: detailed post-mortems and architectural notes

Historical planning notes belong in `docs/archive/`.

## Roadmap

### Phase 1 — Documentation Cleanup

- [x] Separate active docs from historical notes.
- [x] Archive stale PyMuPDF plan and previous session summary.
- [x] Rewrite `AGENTS.md` around the current Owen-only focus.
- [x] Rewrite this active plan around validation and QA.
- [ ] Keep future root docs concise and avoid duplicating roadmap content.

### Phase 2 — Golden Page Test Set

Goal: create a small, durable page set that represents the hard cases in each volume.

- [x] Add initial `qa/golden_pages.json` seed for volume 1.
- [ ] Expand golden page entries to all 16 volumes.
- [ ] Add automated checks that map golden source pages to generated XHTML.

For each volume, choose 5-10 PDF pages covering:

- cover/title/front matter
- table of contents
- chapter or treatise start
- normal prose
- page-boundary paragraph continuation
- Greek text
- Hebrew text, where present
- footnote marker in body text
- footnote/endnote source page
- any known blemish or volume-specific oddity

Suggested artifact:

```text
qa/golden_pages.json
```

Suggested schema:

```json
{
  "1": [
    {
      "page": 7,
      "kind": "page_boundary",
      "reason": "Known paragraph continuation across pages 7-8",
      "checks": ["no_header", "paragraph_join"]
    }
  ]
}
```

### Phase 3 — EPUB Audit Harness

Goal: inspect generated EPUBs automatically after conversion.

- [x] Add `scripts/audit_epub.py`.
- [x] Generate initial volume 1 reports in `qa/reports/`.
- [ ] Triage volume 1 warnings and decide which should become converter fixes.
- [ ] Run audits on other volumes only when the user names a specific volume or explicitly requests a batch run.

Suggested command:

```bash
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub
```

Checks to implement:

- EPUB package opens and contains `mimetype`, `META-INF/container.xml`, OPF, NAV, CSS.
- OPF is version 3.0 and includes cover, NCX, fonts, and `specified-fonts` support.
- XHTML files include `xmlns:epub`.
- Greek spans use `lang="el"` and `xml:lang="el"`.
- Hebrew spans use `lang="he"`, `xml:lang="he"`, and `dir="rtl"`.
- No obvious untranslated AGES Beta Code remnants in body text.
- No AGES boilerplate headers or footers remain.
- Repeated phrase detector finds no strong ghost-layer duplication.
- Footnote references and endnote anchors have matching counts.
- NAV links resolve to existing XHTML files.
- All spine items exist and are readable.

Default output for volume-specific audits:

```text
volumes/v1/bugs_fixes/volume_1_audit.json
volumes/v1/bugs_fixes/volume_1_audit.md
volumes/v1/bugs_fixes/BUGS_AND_FIXES.md
```

### Phase 4 — Alternate Extractor Comparison

Goal: use other extraction engines to flag suspicious pages.

Comparison extractors:

- PyMuPDF raw text: `page.get_text("text")`
- PyMuPDF4LLM Markdown: current structural source
- PyMuPDF dict spans: current font-aware source
- Poppler `pdftotext`, if installed
- existing ThML intermediate, where useful
- CCEL XML for volumes 5 and 10, as a textual comparison source

Checks:

- large character-count divergence
- pages with many repeated 8-12 word sequences
- missing headings compared with PDF outline
- missing footnote markers
- pages with Greek/Hebrew in one extractor but not the output EPUB

Suggested artifact:

```text
qa/reports/extractor_compare_v1.json
```

### Phase 4A — Textual Integrity Audit

Goal: make text fidelity measurable before manual proofreading.

- [x] Add `scripts/audit_text_integrity.py`.
- [x] Write volume-specific reports to `volumes/vN/bugs_fixes/`.
- [x] Update `BUGS_AND_FIXES.md` with an automated textual-integrity section.
- [x] Regenerate and audit Volume 1.
- [x] Enforce holistic paragraph healing in `get_pages_text()`.
- [x] Ensure normal chapter body text always uses the paragraph healer.
- [ ] Triage the remaining Volume 1 split candidates around footnote/page-number residue.
- [ ] Run textual-integrity audits on other volumes only when the user names a specific volume or explicitly requests a batch run.

Volume 1 baseline after this pass:

| Metric | Result |
|--------|--------|
| Approximate PDF-to-EPUB content-word coverage | 0.9854 |
| Possible faulty paragraph splits | 3 |
| Adjacent duplicate paragraphs | 0 |
| Repeated word windows | 2 |
| Detected chapter subtitles | 59 |

### Phase 5 — Per-Volume Validation Pass

Goal: turn "works well" into repeatable confidence across all 16 volumes.

For each volume:

1. Run the converter.
2. Run the EPUB audit harness.
3. Run golden page checks.
4. Review flagged pages manually.
5. Update `volumes/vN/bugs_fixes/BUGS_AND_FIXES.md` with validation-safe status.
6. Only mark an issue fully resolved after user validation, per `GEMINI.md`.

Suggested tracking table:

| Vol | EPUB Generated | Audit Clean | Golden Pages Reviewed | User Validated | Notes |
|-----|----------------|-------------|-----------------------|----------------|-------|
| 1 | yes | pending | partial | pending | deepest current QA |
| 2 | yes | pending | pending | pending |  |
| 3 | yes | pending | pending | pending |  |
| 4 | yes | pending | pending | pending |  |
| 5 | yes | pending | pending | pending | compare CCEL XML |
| 6 | yes | pending | pending | pending |  |
| 7 | yes | pending | pending | pending |  |
| 8 | yes | pending | pending | pending |  |
| 9 | yes | pending | pending | pending |  |
| 10 | yes | pending | pending | pending | compare CCEL XML |
| 11 | yes | pending | pending | pending |  |
| 12 | yes | pending | pending | pending |  |
| 13 | yes | pending | pending | pending |  |
| 14 | yes | pending | pending | pending |  |
| 15 | yes | pending | pending | pending |  |
| 16 | yes | pending | pending | pending |  |

### Phase 6 — Optional Source Improvements

Consider after the audit harness exists:

- Add a CCEL branch for volumes 5 and 10 if CCEL text is demonstrably cleaner.
- Add a targeted rendered-XHTML visual check for title pages and TOCs.
- Add a small regression fixture for the most fragile known pages.
- Revisit blockquote detection only if it can be added without replacing the stable structural extraction path.

## Recommended Next Implementation Slice

Build `scripts/audit_epub.py` first. It gives immediate value against the EPUBs that already exist and does not require changing the converter.

Minimum useful version:

1. Open EPUB as ZIP.
2. Locate OPF, NAV, CSS, and XHTML files.
3. Check NAV links and spine item existence.
4. Count Greek/Hebrew spans and missing language attributes.
5. Count noteref links and endnote anchors.
6. Scan text for AGES boilerplate and repeated phrases.
7. Print a short Markdown report plus JSON details.

After that, add `qa/golden_pages.json` and make the audit script optionally inspect only those pages/files when a volume-specific page map exists.
