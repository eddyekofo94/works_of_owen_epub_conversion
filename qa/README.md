# QA

This folder contains validation scaffolding for the Owen Works EPUBs.

- `golden_pages.json`: hand-picked source pages that represent fragile extraction cases.
- Generated audit reports are stored in each volume's `bugs_fixes/` directory.

Run the current EPUB audit with:

```bash
.venv/bin/python3 scripts/audit_epub.py volumes/v1/output/volume_1.epub
```

The audit does not mutate the EPUB. By default it writes `volume_N_audit.json`, `volume_N_audit.md`, and an automated audit section into `volumes/vN/bugs_fixes/BUGS_AND_FIXES.md`.

It inspects EPUB package structure, metadata, NAV links, language tagging, footnotes, AGES boilerplate residue, possible Beta Code residue, and repeated phrase risks.

## Bug Regression Tests

`tests/test_bug_regressions.py` turns known Volume 1 bug classes into pytest gates. It runs the existing audit code against generated EPUBs and compares the results with `qa/bug_regression_baselines.json`.

The report-friendly version is intended for `#test bug` after the standard EPUB and text-integrity audits:

```bash
.venv/bin/python3 scripts/audit_bug_regressions.py 2
```

It writes `volumes/v2/bugs_fixes/volume_2_bug_regressions.md` and `.json`.

Use `#test audit 2` to regenerate Volume 2 and write the standard EPUB/text-integrity reports. Use `#test bug 2` to turn those reports into the known-bug repair queue.

Default scope is Volume 1:

```bash
.venv/bin/python3 -m pytest tests/test_bug_regressions.py
```

To check more already-generated volumes:

```bash
OWEN_REGRESSION_VOLUMES="1 2 3" .venv/bin/python3 -m pytest tests/test_bug_regressions.py
```

When an implementation fixes a bug, ratchet the relevant max count downward or add a concrete `absent_samples` entry. This keeps future converter work from reintroducing fixed paragraph splits, inline structural markers, untagged Greek/Hebrew, or repeated word-window duplication.
