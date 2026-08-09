# Volume 1 Heal Session Report

Generated: 2026-07-07 19:24 Europe/Paris

## Outcome

- Branch: `heal-v1-20260707`
- Target: Volume 1, *The Glory of Christ*
- Baseline Need in this run: `23.0` from the initial all-volume state report; `18.5` after fresh Volume 1 checks
- Final Need: `0.8`
- Numeric Need gate: PASS (`0.8 < 1.0`)
- Strict readiness gate: BLOCKED

Strict readiness is blocked only by uncommitted conversion-affecting changes:

- `shared.py`
- `volumes/v1/intermediate/volume_1.json`

The remaining non-blocking review debt is:

- Low Latin tagging ratio: `77.12%`
- Low Latin translation ratio: `53.88%`

Latin word coverage is healthy at `99.89%`, and the text-integrity audit reports no missing Latin clauses.

## Work Performed

1. Refreshed Volume 1 baseline checks and state reports.
2. Removed stale Volume 1 whitelist debt that no longer suppressed current findings.
3. Fixed `tests/test_structural_symmetry.py` so inline markers inside `syllabus-anchor` paragraphs advance sequence tracking.
4. Added obvious English false-positive words to the shared Latin classifier:
   `incarnate`, `consummate`, `invocate`, `inanimate`, `indicate`, `affectionate`, `fluctuate`, `possessor`, `irradiate`, `obdurate`.
5. Confirmed current dense/top/page/split findings as audit false positives where text is present in the EPUB but split by noteref, scripture-reference, title, catechism, language-span, or quotation markup.
6. Added exact current whitelist entries for confirmed Volume 1 false positives.
7. Rebuilt Volume 1 with `--render-only`.

## Whitelist Changes

Added current, evidence-backed entries in `volumes/v1/bugs_fixes/volume_1_whitelist.json` and documented them in `volume_1_whitelist.md`:

- `ignored_words`: `greeks`, visible in the EPUB but falsely reported by word coverage.
- `weak_pages`: page `398`.
- `dense_source_window_loss`: pages `382, 398, 402, 406, 411, 419, 433, 434, 451, 478, 480, 483, 487, 517, 522, 534, 555, 559, 565, 570, 572, 596, 603, 605, 607, 613, 618, 623, 624, 625, 626, 627, 629, 632`.
- `top_of_page_text_loss`: pages `398, 478`.
- `paragraph_splits`: current citation, foreign-quote, translation, and exposition-boundary false positives.
- `syllabus_anchor_candidates`: current exact audit keys in chapters 6, 10, 14, 22, 23, 28, 40, 45, and 48.

Removed stale entries that no longer matched current reports:

- old weak/dense page suppressions
- stale punctuation-spacing anomalies
- stale unmatched-quote entry
- unused ignored warnings: `low_latin_tagging`, `front_matter_toc_loss`, `repeated_phrases`

## Verification

Passed:

- `.venv/bin/python3 volumes/v1/convert.py --render-only`
- `.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub`
- `.venv/bin/python3 scripts/audit_text_integrity.py 1`
- `.venv/bin/python3 scripts/audit_anomalies.py 1`
- `.venv/bin/python3 scripts/audit_bug_regressions.py 1`
- `OWEN_REGRESSION_VOLUMES=1 .venv/bin/python3 -m pytest 'tests/test_bug_regressions.py::test_no_unused_whitelist_entries[1]' tests/test_structural_symmetry.py -q --tb=short`
- `.venv/bin/python3 scripts/report_volume_state.py --volumes 1 --no-readme`
- `.venv/bin/python3 scripts/assert_need_under.py 1 1.0`

Blocked:

- `.venv/bin/python3 scripts/audit_heal_readiness.py 1 --strict`

Reason: uncommitted conversion-affecting changes remain, as designed by the strict readiness gate.

Out-of-scope broad pytest note: `tests/test_bug_regressions.py` still surfaces unrelated stale whitelist failures for Volumes 8, 12, and 15. Those were not changed during this Volume 1 heal.

## Report Paths

- EPUB: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/output/volume_1.epub`
- EPUB audit: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/bugs_fixes/volume_1_audit.md`
- Text integrity: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/bugs_fixes/volume_1_text_integrity.md`
- Bug regressions: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/bugs_fixes/volume_1_bug_regressions.md`
- Heal readiness: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/bugs_fixes/volume_1_heal_readiness.md`
- This report: `/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/volumes/v1/reports/20260707_192400/volume_1_heal_session_report.md`
