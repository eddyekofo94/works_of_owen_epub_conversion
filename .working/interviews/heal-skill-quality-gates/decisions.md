# Heal Skill Quality Gates Interview

## Goal

Improve the project-local `#heal` / `$heal` workflow so future heal runs account for the v10 under-1 verification caveats: Need can be arithmetically below target while text integrity, bug regression, whitelist debt, low Latin quality, source-text changes, and by-eye review risks remain.

## Exit Criteria

Implementation-ready: decisions are specific enough to update `skills/heal/SKILL.md`, related task docs, and any supporting validation/reporting scripts without further product-level discussion.

## Scope / Non-goals

Scope:
- Define final gate semantics for `#heal` when Need `<1.0` conflicts with WARN reports or regression budgets.
- Define how whitelist usage, ignored warnings, stale whitelist entries, and low Latin tagging/translation must be audited and reported.
- Define how heal reports should distinguish OCR/source-text repairs from report-only or scoring-only changes.
- Define required by-eye review packet contents and wording.

Non-goals:
- Do not implement changes during the interview unless the user explicitly switches from planning to implementation.
- Do not re-heal v10 in this interview.
- Do not redesign the entire Need scoring model unless needed to make `#heal` behavior coherent.

## Decisions

- Final readiness should use a **hybrid gate**, not Need alone and not a blanket block on every warning.
- Need `<1.0` is necessary but not sufficient for `strict ready for by-eye review`.
- Some WARN classes must block readiness and force continued repair or `blocked with evidence`; other WARN classes may be carried into the by-eye packet as disclosed review debt.
- The reported Need/readiness must reflect quality caveats accurately. A low Need score must not be presented as clean when blocker-class warnings, regression overruns, or hidden whitelist suppressions remain.
- Implement both mechanisms:
  - Global Need scoring should include conservative penalties for blocker-class issues so those issues keep Need from looking clean.
  - `#heal` should also run a dedicated readiness gate that fails closed and explains blockers separately from review debt.
- Add a dedicated readiness audit command, preferably `scripts/audit_heal_readiness.py N --strict`.
  - It should read the current target-volume reports.
  - It should write JSON and Markdown reports under `volumes/vN/bugs_fixes/volume_N_heal_readiness.{json,md}`.
  - It should exit nonzero in `--strict` mode when blocker-class issues remain.
  - Final `#heal` verification should run both the numeric Need gate and the heal readiness gate.
  - `report_volume_state.py` should share or mirror the same blocker classification so Need scoring and readiness do not drift.
- Update `README.md` as part of implementation so the new readiness gate is documented outside the skill file.
- Hybrid gate split:
  - Blockers: EPUB audit errors/warnings; bug-regression rows above budget; unwhitelisted dense source-window loss; paragraph split candidates; missing clauses; repeated windows caused by duplicated text; missing enumerators; untagged Greek/Hebrew; coverage below threshold; anomalies/unmatched quotes unless specifically verified and whitelisted; unresolved modern references; untranslated substantial foreign passages; unenriched legacy footnotes; whitelist entries that suppress real defects or lack concrete rationale; unreported source-text/conversion changes.
  - Review debt allowed if disclosed: verified false-positive syllabus/list candidates; low Latin tagging/translation when no Latin text is missing; stale unused whitelist entries, with preference to clean them; by-eye-only layout/polish items after automated checks pass.
- Latin quality policy:
  - Latin word coverage below threshold, missing Latin clauses, or untranslated substantial foreign passages are readiness blockers.
  - Latin tagging/translation ratio gaps are review debt only when no Latin text is missing and no substantial passage is untranslated.
  - Whitelisting `low_latin_tagging` or `low_latin_translation_coverage` must not erase the debt silently; readiness reports must show these as accepted review debt with ratios and samples.
  - Need scoring should include a modest, capped penalty for low Latin tagging/translation even when ignored, so the score reflects the debt without dominating true text loss or unresolved citations.
- Latin/foreign-language translations and citations must render as footnote/popover notes, never as inline replacement text in the body. `#heal` must treat inline inserted translations as a blocker/regression.
- Enforce the no-inline-translation rule in both places:
  - Focused pytest tests when translation/citation/rendering logic changes.
  - Built-EPUB readiness audit that scans body XHTML and fails if modern translation/citation note content appears outside note anchors/endnotes.

## Evidence / Findings

- v10 report claim: Need `0.5` was arithmetically true under current `scripts/report_volume_state.py`.
- Current score formula penalizes paragraph splits, audit warnings/errors, anomalies, unmatched quotes, unresolved citations/modern notes, and coverage below `99.5%`, but does not penalize existing text-integrity WARN status or bug-regression overruns once reports exist.
- v10 text integrity remained WARN with 3 warnings: dense source-window loss, one paragraph split, and syllabus-anchor candidates.
- v10 bug regression remained WARN: syllabus-anchor candidates were 25 observed vs 16 budget.
- v10 Latin tagging was 58.82% and Latin translation 38.82%; both were ignored through whitelist entries.
- Current unresolved dense-window samples and the one paragraph-split candidate were not whitelisted; the under-1 score came from formula behavior, not direct suppression of those exact items.
- v10 whitelist contained stale historical allowances after anomalies and unmatched quotes were 0.
- v10 final report phrase "No source text was changed" was too strong because `volumes/v10/convert.py` added raw intermediate text repairs and `volumes/v10/intermediate/volume_10.json` changed.
- Existing `skills/heal/SKILL.md` already says strict ready requires Need `<1.0`, EPUB audit clean, text-integrity warnings eliminated or fully explained, anomaly/unmatched clean, bug-regression budgets respected, generated-file clean, Apple Books polish, and by-eye packet.
- Existing `scripts/assert_need_under.py` only asserts numeric Need below a threshold using `gather_volume_data()` and `score_volume()`.
- No existing `assert_heal_ready.py` or equivalent readiness gate was found.
- `render.py` contains `apply_inline_translations()` with a docstring stating legacy inline translations are disabled and Latin translation data must render only as popup/endnote content.
- `tests/test_typography_standard.py` includes `test_inline_translation_injection_is_disabled()` and body-translation-note default behavior tests.
- `tests/test_modern_notes.py` checks popup note insertion, punctuation placement, and citation symbols for modern body notes.
- User wants to finish the overall Owen project soon, and is open to using external Owen texts or plugins/tools if they speed completion without compromising textual integrity.
- External text sources found:
  - Digital Puritan Press indexes Owen Works volumes and links PDF/EPUB/MOBI/TXT/web copies via Internet Archive, including all 16 project-relevant Works volumes.
  - Internet Archive item pages expose generated EPUB/FULL TEXT/HOCR or OCR search text downloads, useful for automated collation but still OCR-derived.
  - The Online Books Page lists Owen works with EEBO TCP HTML and HathiTrust page-image links for many individual treatises; useful as a secondary witness, especially for original/near-original editions.
  - CCEL has Owen works/treatise pages and PDFs for some texts; useful as a structured secondary witness, but this repository currently treats archived CCEL XML for v5/v10 as legacy/inactive.
- External sources should speed triage and collation, but automatic text injection is risky unless source family/edition and local PDF agreement are verified.
- External collation must be exception-driven. The workflow must not require manual page-by-page review across all 16 Owen Works volumes or the broader 23-volume Owen corpus including Hebrews commentary.
- External witness comparison should target audit-flagged pages/windows, known OCR patterns, dense source-window loss, suspicious paragraph splits, and high-risk language/citation areas.
- Plugins/tools should be incorporated to reduce manual burden: browser/computer-use for visual and Apple Books checks, GitHub for issue/PR tracking, code-review for final review, and multi-agent tooling if available for bounded read-only collation/research tasks.
- GitHub workflow policy:
  - Use a hybrid/lightweight GitHub workflow.
  - The user is the solo developer and does not want a heavy PR-centric process.
  - `#heal` should still treat GitHub/remote push as part of durable workflow hygiene so code and reports are backed up remotely.
  - Branch, commit, and push are part of the recommended completion path, but `#heal` must ask before committing or pushing.
  - Before asking, `#heal` should show the exact changed-file scope and any generated artifacts so accidental clutter is visible.
  - PR creation/review is overkill for normal solo project work and must remain optional unless explicitly requested.
  - GitHub issues/checklists may be used as a completion ledger if useful, but must not slow down local healing.
- Whitelist cleanup policy:
  - Use a hybrid cleanup strategy.
  - `#heal` should remove obviously unused stale whitelist entries for categories with zero current findings, updating both JSON and Markdown.
  - Broad/policy-level suppressions, especially Latin tagging/translation review debt, should not be silently removed; they should remain only if justified and must be surfaced in readiness reports.
  - Stale whitelist entries that cannot be safely classified should be reported as cleanup debt rather than hidden.

## Tradeoffs / Risks

- If `#heal` treats any WARN as blocking, it may block on false positives and require more human judgment.
- If `#heal` treats Need `<1.0` as sufficient, it can report a volume as cleaner than the detailed QA reports justify.
- If whitelist entries can hide broad classes such as Latin tagging/translation, final reports must make that visible or the score is misleading.
- If Need scoring itself is changed globally, existing volume rankings may shift and old "under 1" claims may no longer compare directly with prior reports.
- If the stricter logic is only added to `#heal`, the global state report may still show a misleading Need value unless final heal reports clearly distinguish score from readiness.

## Validation Plan

- Add/adjust tests for Need scoring so blocker-class warnings and bug-regression overruns keep Need from looking clean.
- Add tests for `audit_heal_readiness.py` classification:
  - PASS when Need `<1.0`, no blockers, and only disclosed review debt remains.
  - FAIL when text-integrity blocker warnings remain.
  - FAIL when bug-regression rows exceed budget.
  - FAIL when modern translation/citation content appears inline in body XHTML.
  - Report low Latin tagging/translation as review debt when no Latin text is missing.
- Run focused existing tests:
  - `.venv/bin/python3 -m pytest tests/test_modern_notes.py tests/test_typography_standard.py`
  - `.venv/bin/python3 -m pytest tests/test_bug_regressions.py`
- Run v10 as a regression fixture after implementing readiness logic:
  - `.venv/bin/python3 scripts/report_volume_state.py --volumes 10 --no-readme`
  - `.venv/bin/python3 scripts/audit_heal_readiness.py 10 --strict`
  - Expected: v10 should not be silently "ready" while the known blocker/review-debt state remains; exact pass/fail depends on whether current syllabus regression is classified as blocker or verified review debt.
- Update README and `skills/heal/SKILL.md`, then verify docs mention the readiness gate, plugin roles, exception-driven external collation, and no-required-PR GitHub workflow.

## Ready To Act

Implementation can start. Suggested steps:
1. Add shared readiness classification helpers or a standalone `scripts/audit_heal_readiness.py`.
2. Update `scripts/report_volume_state.py` scoring to include blocker-class penalties and modest Latin-review-debt penalties.
3. Update `scripts/assert_need_under.py` wording if needed so it remains the numeric gate, not the full readiness gate.
4. Update `skills/heal/SKILL.md` to require the readiness audit, exception-driven external collation, no-inline-translation enforcement, whitelist cleanup/reporting, and ask-before-commit/push behavior.
5. Update `README.md` with the new command and plugin/tool workflow.
6. Add or update tests.
7. Run the validation plan.

## Open Questions

- Decide whether external online Owen texts should become an official text-integrity evidence source and how conservative replacement should be.
- Should stale whitelist entries be cleaned during every heal, or only reported?
- Should raw intermediate JSON changes be categorized as source-text/conversion changes in final reports?
- Identify useful plugins/tools that could speed completion.
No open planning questions remain for the current goal.
