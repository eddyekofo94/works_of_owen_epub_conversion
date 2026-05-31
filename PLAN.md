# John Owen Works — Active Plan

Last updated: 2026-05-27 (structure refinement pass)

## Current Focus

Stabilize and validate the 16-volume Owen Works EPUB3 pipeline. Hebrews is parked until the Owen volumes are done.

Active branch for the current major rendering refactor:

```text
codex/owenian-structure-refactor
```

Current refactor checkpoint:

- [x] Branch created from `PyMuPDF` with the existing dirty workspace preserved.
- [x] Write the unified Owenian structure standard for flat syllabus lists,
  block exposition lists, nested subpoints, and blockquotes.
- [x] Refactor renderer list handling around an explicit Owenian classifier.
- [x] Add reader-facing list levels while preserving paragraph-based prose.
- [x] Add focused regression tests for flat/block/nested marker behavior.
- [x] Validate on Volume 2 only, unless the user names another volume.
- [x] Tighten Signal F word cap from +18 (30w) to +8 (20w) to prevent genuine
  binary exposition openings from being absorbed inline.
- [x] Expand `_preceding_allows_attachment` anchor detection: word limit raised
  from 45→80; added formula-tail patterns ("these following", "I shall observe",
  "may be considered", "as follows", etc.) and threefold/fourfold count words.
- [x] Emit `syllabus-anchor` class on paragraphs that absorb a flat list inline.
- [x] Add hairline left rule to `list-level-2` and `list-level-3` CSS for
  clearer nesting cues without imposing a modern outline aesthetic.
- [x] Update `bugs_fixes/owenian-structure-rules.md` with Signal F cap rationale,
  anchor word-limit documentation, and revised CSS spec.

Validation checkpoint for this refactor:

- Volume 2 render-only rebuild completed.
- Manual XHTML inspection confirmed:
  - `four things in sin ... : — (1.) ... (4.) ...` renders as an inline
    syllabus attached to the anchor paragraph.
  - The following `(1.) The desert of sin...` exposition remains a block
    paragraph with `list-level-1`.
  - The explanatory restart `[1.] Of the person suffering for it...` renders as
    `list-level-2`.
  - `six things are required: — 1. ... 6. ...` remains inline before the block
    exposition restarts.
- `tests/test_text_fidelity.py`: 83 passed.
- `OWEN_REGRESSION_VOLUMES=2 .venv/bin/python3 -m pytest tests/test_bug_regressions.py`:
  105 passed, 7 skipped.
- Volume 2 bug-regression report: PASS.
- Volume 2 text-integrity audit: WARN, with inline structural marker candidates
  0 and missing enumerator marker forms 0.

The active converter is the two-stage modular pipeline:

- `extract.py`: PDF to JSON intermediate
- `render.py`: JSON intermediate to EPUB3
- `volumes/vN/convert.py`: preferred per-volume entry point for passing `OVERRIDES`

`converter.py` is retained only as a legacy-compatible wrapper around the two
stage modules.

Operational rule: work on one volume at a time. Do not run batch conversion or batch audits unless the user explicitly asks for them.

## Current State

- All 16 Owen volumes have generated EPUB outputs in `volumes/vN/output/`.
- Volume 1 has received the deepest recent QA and repair work.
- Issues 38-42, 44, 48, and 49 are implemented but should remain validation-safe in per-volume logs unless the user explicitly approves them.
- Issue 43 blockquote detection was reverted because it damaged heading extraction.
- Structure refinement pass (2026-05-27): Signal F cap tightened, anchor
  detection expanded, `syllabus-anchor` class added, list-level-2/3 CSS updated
  with hairline left rule. Validated with targeted unit tests; full volume
  regression suite requires Python 3.14 on the user's machine.
- Visual Nesting DOM-Tree Refactor (2026-05-29): Implemented visual nesting DOM-tree architecture using a stack-based parser (`_nest_owen_list_hierarchies`) and relative container-based CSS in `shared.py` to prevent "patchy" paragraph-breaking layouts. Successfully validated on Volume 1 EPUB compilation and all 120 regression unit tests.
- Robust Inline Syllabus Flattening (2026-05-29): Refactored the list-flattening pipeline in `render.py` (`_attach_em_dash_flat_list`) to support colons (`:`) as introductory punctuation, removed the strict Roman single-word list-item veto, and implemented "Signal I: Exact Count Match" with a generous 50-word cap. Successfully validated on Volume 1, with Roman and Arabic outline syllabus blocks flattened inline while maintaining block-based detailed expositions.
- The `--hebrews` flag exists but is not implemented.
- `shared.py` lists CCEL XML sources for volumes 5 and 10, but the current `process_owen_volume()` still uses the AGES PDF path for every volume.

## Owenian Visual Nesting Architecture

To resolve "patchy" rendering (margins jumping back, disconnected left borders, and misaligned blockquotes) when deeply nested subdivisions span multiple paragraphs, we implement **DOM-Tree Nesting**:

1. **Stack-Based Tree Parser (`_nest_owen_list_hierarchies` in `render.py`):**
   * Scans flat top-level block elements (paragraphs, blockquotes, headings, horizontal rules, tables).
   * Maintains a stack of open nesting levels (`active_levels`).
   * **State Operations:**
     * *Ascend (`L > current_active`):* Opens intermediate `<div class="owen-branch owen-level-L">` tags and pushes `L` to stack.
     * *Descend/Sibling (`L <= current_active`):* Closes active containers down to and including level `L`, and opens a new sibling container at level `L`.
   * **Continuation Paragraphs & Blockquotes:** Elements with no explicit list class (`explicit_level = None`) automatically inherit the active nesting level and are appended inside the open container, maintaining visual continuity.
   * **Bulletproof Delimiter Indexing:** Uses a tag-span scanner to preserve unmatched text or custom tags, guaranteeing zero content loss.

2. **Mobile-First Container CSS (in `shared.py`'s `EPUB_STYLESHEET`):**
   * Margins, padding, and left borders are shifted from the `<p>` tags to the `div.owen-branch` containers, which explicitly allow natural page-breaking flow (`break-inside: auto`).
   * Spacing is kept compact to protect text from crushing on narrow iPhone screens:
     * `div.owen-level-1`: `margin-left: 0;` (major boundary).
     * `div.owen-level-2`: `margin-left: 0.75em !important; border-left: 1.5px solid rgba(42, 85, 160, 0.12) !important; padding-left: 0.6em !important;` (uses soft Owen Blue).
     * `div.owen-level-3`: `margin-left: 0.75em !important; border-left: none !important; padding-left: 0 !important;` (clean indentation, no double border).
   * Direct overrides (`margin-left: 0 !important; border-left: none !important; padding-left: 0 !important;`) are applied to the child paragraphs so they sit flush inside their respective container branches.

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
