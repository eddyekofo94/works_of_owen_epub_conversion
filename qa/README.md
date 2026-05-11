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
