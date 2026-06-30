# Volume 5 Quality Review — 2026-06-30

## Outcome

Volume 5 is structurally healthy and already below the project target: the regenerated Need plan reports **0.4**, with **99.99% overall coverage**, **100% Greek coverage**, **100% Hebrew coverage**, **99.71% Latin word coverage**, **0 unresolved citations out of 44**, **0 audit errors**, and **0 audit warnings**. The focused Volume 5 bug-regression pytest gate passed.

The remaining opportunities are editorial quality improvements, not package-integrity repairs. The largest real quality gap hidden by the score is Latin enrichment: **84.02% Latin tagging** and **75.63% Latin translation coverage**. Those checks are currently whitelisted, so they contribute no Need penalty.

## Reports Reviewed

- `volumes/v5/bugs_fixes/volume_5_audit.json`
- `volumes/v5/bugs_fixes/volume_5_text_integrity.json`
- `volumes/v5/bugs_fixes/volume_5_bug_regressions.json`
- `volumes/v5/bugs_fixes/volume_5_anomalies.json`
- `volumes/v5/bugs_fixes/volume_5_unmatched_quotes.json`
- `volumes/v5/bugs_fixes/volume_5_whitelist.json`
- `volumes/v5/bugs_fixes/volume_5_whitelist.md`
- `volumes/v5/plans/v5_need_reduction_plan.md`
- `volumes/v5/reports/volume_5_whitelist_audit.md`

## Verification Summary

- EPUB audit: PASS; 0 errors, 0 warnings; 69 files; 41 XHTML files; 14 fonts.
- Language integrity: 6,350 Greek characters and 980 Hebrew characters; none untagged; no Hebrew integrity failures.
- Footnotes: 207 references and 207 targets; no missing targets or orphan notes.
- Text integrity: PASS; 193,209 PDF tokens versus 194,290 EPUB tokens; 562 pages checked; no weak page matches, missing dense windows, top/bottom page losses, faulty paragraph splits, adjacent duplicates, missing enumerators, Greek clauses, or Hebrew clauses.
- Latin: 3,094 PDF words versus 3,097 EPUB words; 2,602 of 3,097 EPUB Latin words tagged; 447 of 591 tagged Latin runs translated; one missing-clause warning on PDF page 359 is documented as a ghost-layer duplicate.
- Regression gate: PASS. Two inline-marker candidates and 25 repeated windows remain within their established budgets.
- Treatise architecture: both Volume 5 treatises have hardcoded `treatise_title_overrides` in `volumes/v5/convert.py`.

## Whitelist Audit

The whitelist contains 50 entries: 34 exact/current matches, 5 broad entries matching multiple findings, and 11 unused entries. The whitelist auditor generated a complete trace in `volumes/v5/reports/volume_5_whitelist_audit.md` and `.json`.

### Text-integrity whitelist

- Ignored warnings: `repeated_phrases` (authentic repeated formulae; now unused), `missing_latin_clauses` (page 359 PDF ghost duplication), `low_latin_tagging` (mixed false positives but also masks a real enrichment backlog; now unused as a raw warning), `repeated_windows` (authentic repetition), `inline_structural_markers` (two reviewed candidates), `overlong_heading_candidates` (one legitimate long heading), and `low_latin_translation_coverage` (editorial enrichment backlog).
- Skipped pages 3–11: front matter/prefatory matter omitted from parsed chapter bodies.
- Paragraph split signatures: `To The Reader`; `was this, —`; `Whence I argue, —`; `the inquiry is, —`; `Justification by the law is this, —`; `various inquiries are made, —`; `hence we argue, —`; `observed, —`; `There was עֲצֶרֶת הַדְּבָרִים , —`; `I shall consider, first, —`; `Hence we argue, —`; `Wherefore, —`; `Again, —`; `the question proposed, —`. These are headings, list introductions, or authentic rhetorical continuations. `To The Reader` and lowercase `hence we argue, —` each match two locations and should be made context-specific if the whitelist format gains structured matching.
- Top-of-page exceptions 31 and 126: unstable/non-body page-top windows.
- Dense-window exceptions 15, 16, 29, 31, 35, 36, 37, 62, 77, 88, 89, 98, 122, 126, 151, 173, 182, 297, 358, 359, 377, 393, 431, 442, 469, 473, 499, and 538: historically recorded dense Latin, polyglot, Scripture-reference, or structural windows. The current raw audit has no missing dense windows, so all 28 are stale and removable after one clean re-audit confirms the current EPUB/report pairing.

### Anomaly whitelist

- OCR/bracket signature `qui et`: authentic Latin words falsely read by the detector as split English `quiet`.
- Historical/technical hyphenation: `wire-draw`, `dikaio-oo`, `non-imputation`, `sub-distinguished`, `non-solvent`, `blood-guiltiness`, and `co-interest`. Preserve the historical forms. `sub-distinguished` is currently unused; `non-imputation` correctly matches four chapters.
- Structural sequences: `2.`, `5. ... 7.`, `3. ... 5.`, and `2. ... 4.`. These cover Owen's numbering/digressions. `3. ... 5.` is unused; the `2.` and `2. ... 4.` rules overlap and are overly broad.
- Unmatched-quote signatures: `The first inquiry in this matter, in a way of duty, is after the proper relief`; `Credisne te non posse salvari`; `Whence the prophet says in the psalm`; `The excellent words of Justin Martyr`; `A full comprehension of it no creature`; `But the true and genuine signification of these words`; `3. "Ex injuria; or,`; `(1.) "Injuriarum," of wrongs:`; `In this state the apostle interposes himself`; `(1.) The Lord Christ, our mediator and surety`; `We shall take our fourth argument from the express exclusion`; `originally included no merit`; `Si obedientia vitae Christi nobis`; `injustus", 1 Peter 3:18`; `This treatise, entitled Gospel Grounds and Evidences`; and `Isaiah 13:6, 7; — "When the day`. These represent authentic quotation conventions or previously corrected text. Seven are now unused: the first, second, third, fifth, seventh, twelfth, and thirteenth entries in this list.
- Invalid reference `John 22`: stale. `volumes/v5/convert.py` already corrects `John 22:30, 31` to `John 20:30, 31`.

## Recommended Improvements, in Priority Order

1. **Increase Latin translation coverage (highest reader value).** Translate the remaining 144 of 591 tagged Latin runs, prioritizing full clauses rather than fragments such as `propitiatio est`, `nemo unquam`, and `incertior sum multo, quam dudum`. Add exact, source-faithful entries to `scripts/translation_db.py`; do not manufacture vague citation notes.
2. **Improve Latin tagging with precision.** Review the 495 untagged Latin-word occurrences. Names such as Socinus, Thomas, Schlichtingius, Grotius, and Pelagius should generally remain untagged; genuine terms/phrases such as `reus`, `subjectum`, `totum`, and `congruo` should be tagged through the generic language pipeline. Do not optimize the percentage by tagging English words or personal names.
3. **Prune stale whitelist entries.** Remove the 11 entries proven unused by the raw audit and, after a fresh full audit, remove the 28 obsolete dense-window page exceptions. Update both JSON and Markdown copies together. This does not lower the current Need score, but makes future regressions visible.
4. **Tighten broad whitelist matching.** Replace bare structural key `2.` and overlapping `2. ... 4.` with chapter/context-specific entries. Keep `non-imputation`; its four matches are the same legitimate historical compound, not accidental greediness.
5. **Review the two inline structural candidates.** The ch002 editorial summary ending `20. — Ed.` is prose, not a list. The ch004 sentence beginning `All men in those days...` also appears to be prose. If confirmed in the PDF, add exact contextual exclusions rather than retaining the category-wide ignored warning.
6. **Verify page 359 once manually.** The missing Latin clause is documented as duplicate PDF ghost text. Retain the whitelist only if side-by-side PDF/EPUB inspection confirms one complete visible occurrence in the EPUB.
7. **Avoid coverage-score chasing.** The remaining 0.4 Need is rounding-level coverage variance. Editorial translation text explains most EPUB excess words; deleting enrichment to improve raw token parity would reduce actual quality.

## Tooling Finding

`scripts/audit_whitelists.py 5` temporarily moved current audit files and initially left backup artifacts instead of restoring cleanly. The original Volume 5 reports were restored, and the generated whitelist audit was moved from `bugs_fixes/` to the mandated `volumes/v5/reports/` location. The auditor should be fixed separately to use a temporary directory and a `try/finally` restoration path.
