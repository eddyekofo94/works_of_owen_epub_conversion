# Heal Workflow Improvement Report — Escaping the Endless Loop

Generated: 2026-08-09. Scope: John Owen Works repo (16 Owen volumes + 7 Hebrews volumes), the
project-local `skills/heal/SKILL.md`, QA scoring in `scripts/report_volume_state.py`, and current
git/QA state.

## 1. Where the project actually stands

All 23 targets are QA level FULL with 0 audit errors. Per `qa/reports/volume_state_report.md`
(2026-07-07, mid-v1-heal):

- **Owen v1–v16:** 7 volumes already pass the strict Need `<1.0` gate (v1, v3, v4, v5, v6, v7, v11).
  Remaining 9 range from Need 0.4–22.0. The worst (v9 = 22.0) is dominated by one component:
  51 paragraph splits (capped at 10 pts) plus low Latin translation.
- **Hebrews h1–h7:** Need 32.9–43.2. Every one has the *same* profile: unresolved citations
  (103 total across the seven), hundreds of "suspected anomalies" (~1,500 total), and a constant
  `Splits: 40` on all seven volumes.
- **Corpus-wide untranslated debt is small:** `qa/untranslated_prose_report.md` counts only
  **376 items total** (15 footnotes + 361 body paragraphs) across all 16 Owen volumes.

The finish line is much closer than the loop makes it feel. The problem is workflow shape, not
volume quality.

## 2. Why the heal loop is endless — root causes

### 2.1 Per-volume healing of corpus-wide problems (the big one)
The heal skill forbids batching ("Never batch-heal volumes"), but the three components that
dominate remaining Need — Latin tagging, Latin translation, citation resolution — are **shared-data
problems**. Translations live in `translation_db.py`; citations in `patristic_refs.py`. Owen reuses
the same Latin phrases across volumes. Healing v13 adds entries that change v9's and v15's numbers,
so every heal run stales every other volume's reports, and you re-discover the same class of work
23 times. Each run also pays a fixed ceremony cost: clean master → fresh branch → full
`run_all_checks` → by-eye packet. That's ~23× overhead for work that is one deduped sweep.

### 2.2 The strict readiness gate fails by construction mid-run
`volume_1_heal_readiness.md` shows the pattern: v1 Need = 0.8 (gate PASS) but strict readiness
FAILS because of blocker class `source_text_or_conversion_changes` — i.e. *the heal branch's own
uncommitted work in progress*. A gate that flags the workflow's own dirty state guarantees most
sessions end "checkpointed", which is exactly the endless-loop feeling. The blocker is only
satisfiable by committing, but the skill also says "do not commit without asking" — a built-in
stall.

### 2.3 Review-debt thresholds set at 99% for inherently manual metrics
Readiness review debt flags Latin tagging/translation below **99%**. But the tagging samples in
`volume_1_heal_readiness.md` are things like `nestorius`, `serm`, `folio` — proper nouns and
abbreviations that arguably *shouldn't* be tagged as Latin. A 99% bar on a fuzzy heuristic means
every volume carries permanent "debt" and every heal run re-litigates it. Note the Need score
itself weights Latin translation at only max 5 pts (`(1 - ratio) * 10`, capped) — the readiness
gate is far stricter than the score, so volumes pass Need and still refuse to finish.

### 2.4 Suspicious metrics inflating Hebrews Need
- `Splits: 40` on all seven Hebrews volumes is almost certainly a capped or defaulted counter,
  not seven identical measurements. Worth 10 pts each (the cap) — a quarter of their Need.
- "Suspected anomalies" of 154–440 per Hebrews volume (also hitting the 10-pt cap) come from
  epub2 sources, not OCR; the anomaly detector was tuned for AGES PDF OCR debris and likely
  misfires on old-EPUB typography. Verify before "fixing" 1,500 anomalies by hand.
- Latin tagging/translation is *excluded* from Hebrews Need scoring
  (`report_volume_state.py:346-348`) but readiness review debt still reports it — inconsistent
  signals across the two tools.

### 2.5 Current git state blocks the next run
On branch `heal-v1-20260707` with: tracked deletions of `AGENTS.md`, `GEMINI.md`,
`ENGINEERING_LOG.md`; modified `shared.py`, v1 intermediates/outputs, QA reports; strays
(`bugs_fixes/untitled folder/False citation.png`, four untracked `volumes/v1/reports/2026*` dirs,
one v12 report dir). The skill's preflight ("stop if worktree dirty") means **no heal run can even
start** until this branch is resolved. This alone may be why recent sessions spun.

## 3. Recommendations

### A. Replace per-volume healing with four corpus-wide passes (highest leverage)
1. **Latin translation sweep (one pass, all volumes).** Regenerate
   `qa/untranslated_prose_manifest.json`, dedupe the 376 phrases, translate once into
   `translation_db.py` (batchable: Claude can draft, you review the ledger diff), re-render all
   volumes. Kills the largest Need + review-debt component everywhere simultaneously.
2. **Latin tagging sweep.** Tagging is deterministic. Build the union of untagged-word samples
   across volumes, classify once (Latin vs. proper noun vs. abbreviation → whitelist), apply
   shared lexicon, re-render.
3. **Hebrews citation resolution.** 103 unresolved citations across h1–h7, concentrated in h1/h2
   (69). One `scan_citations.py`/`patristic_refs.py` session with the existing pipeline.
4. **Hebrews anomaly triage.** First validate the detector against epub2 sources (2.4); tune or
   whitelist per *category*, not per volume.

After these four passes, re-run `report_volume_state.py --all` once. Expect most volumes near or
under 1.0; then per-volume heal only for genuine residuals (v9's 51 splits, v2 word coverage,
volume-specific OCR).

### B. Fix the gates so runs can actually finish
- Exclude in-branch heal work from `source_text_or_conversion_changes` (or make readiness run on
  committed state / allow checkpoint commits on the heal branch without asking each time).
- Split readiness "review debt" from "blockers" in the completion definition: strict-ready should
  mean *blockers = 0*; Latin tagging/translation ratios are reported debt, not gate failures —
  or lower the 99% bar to a value the corpus can meet after pass A (e.g. 95%).
- Investigate the constant `Splits: 40` and the Hebrews anomaly counts before treating them as work.

### C. Repo hygiene (do first, ~30 min)
- Decide the v1 branch: Need gate already passes; commit it (including the intentional
  AGENTS/GEMINI/ENGINEERING_LOG deletions if intended — otherwise restore them), or abandon it.
- Delete `bugs_fixes/untitled folder/`; move `False citation.png` to `scratch/` if still needed.
- Sweep untracked timestamped report dirs into commits or the ignore list.

### D. Adopting the heal skill for Claude
The skill is already project-local (`skills/heal/SKILL.md`) and already loads in Claude Code (it's
in the invocable skill list). Only three Gemini-era edits are needed:
1. Workflow step 2 says "Read `GEMINI.md`" — point it at `CLAUDE.md` (GEMINI.md is being deleted
   on the current branch anyway).
2. Context Preflight says "Codex cannot run `/clear` itself" — generalize the wording; the
   mechanic is the same in Claude Code.
3. Add a sanctioned **batch exception**: "Corpus-wide data passes (translation_db, Latin lexicon,
   citation DB, whitelist categories) may run across all volumes; per-volume scope applies to
   structural/rendering repairs and final verification." This legalizes pass A without losing the
   one-volume discipline where it matters.

## 4. Sequenced finish plan

| # | Step | Scope | Exit condition |
|---|------|-------|----------------|
| 1 | Close out `heal-v1-20260707` + hygiene (C) | git | clean master, strays gone |
| 2 | Gate fixes + skill edits (B, D) | `heal_readiness.py`, `skills/heal` | readiness no longer flags its own branch; batch exception documented |
| 3 | Latin translation + tagging sweep (A1, A2) | all volumes, one branch | untranslated manifest ≈ 0; tagging debt reclassified |
| 4 | Hebrews citations + anomaly triage (A3, A4) | h1–h7, one branch | unresolved ≤ handful with evidence; anomaly detector validated |
| 5 | Residual per-volume heals | v9, v2, v8, v10, v12–v16 as needed | strict gate per volume |
| 6 | By-eye packets, one per volume | all | your manual review — the only truly serial human step |

Estimated: steps 1–4 are ~3–5 focused sessions total, versus 16+ more per-volume heal loops on
the current trajectory. The human by-eye pass (step 6) is the real long pole and is untouched by
any of this — everything else exists to stop re-running the robot work.
