# Owen EPUB Conversion — Development & Conversion Guidelines

This repository provides tools and scripts to convert scanned and OCR'ed PDF volumes of John Owen's works into high-quality, modern EPUB formats.

## Development Workflow

### Python Environment
Always use the virtual environment for running conversion scripts, tests, or utility scripts:
* Activator: `.venv/bin/activate`
* Run python: `./.venv/bin/python3 <script_name>.py`

> [!NOTE]
> **arm64 (2026-07-14):** `.venv` was rebuilt on native arm64 Python 3.14.6 after this Mac's Rosetta→arm64 migration removed the old Intel `python@3.14` that had killed the venv. It's healthy (`tests/` 515 passed; the 3 `test_no_unused_whitelist_entries[8/12/15]` failures are pre-existing, unrelated to arch). If `.venv/bin/python` ever disappears again, rebuild: `mv .venv .venv.intel-dead && uv venv .venv --python 3.14 && uv pip install -r requirements.txt --python .venv/bin/python`, then verify `.venv/bin/python -c "import fitz; print(fitz.pymupdf_version)"`.

### Build / Conversion Commands
To convert a volume from PDF to EPUB:
```bash
# Convert a specific volume (e.g. Volume 12)
./.venv/bin/python3 volumes/v12/convert.py

# Extract only (Stage 1: PDF -> intermediate JSON)
./.venv/bin/python3 volumes/v12/convert.py --extract-only

# Render only (Stage 2: JSON -> EPUB)
./.venv/bin/python3 volumes/v12/convert.py --render-only
```

### Running Tests
To run tests to verify conversions and check for regressions:
```bash
# Run all regression tests
./.venv/bin/python3 -m pytest tests/

# Run a specific test
./.venv/bin/python3 -m pytest tests/test_bug_regressions.py -k "latin_word_tagging"
```

## Git Branching Workflow

This repository uses a standard Git branching model. Do not use worktrees unless explicitly required.

### Working with Branches
1. **Create and switch to a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Commit changes**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```
3. **Push to GitHub**:
   ```bash
   git push origin feature/your-feature-name
   ```
4. **Merge to master**:
   Once changes are verified, merge feature branches back to `master`:
   ```bash
   git checkout master
   git pull origin master
   git merge feature/your-feature-name
   git push origin master
   ```

## Scratch Scripts
Any temporary developer or agent scratch scripts should be placed inside a `scratch/` directory. This directory is global-ignored via `.gitignore` and will not be committed to the repository.

## Project Mandates

Full mandates (workflow rules, mobile-first CSS spec, and numbered Technical Mandates referenced by `scripts/code_review.py`) live in `docs/project_mandates.md`. Read it before changing converter behavior. Non-negotiables:

- **Never merge to `master`** unless the user explicitly instructs it. Keep work on local branches.
- **Never mark an issue "Fixed"/"Done"** in changelogs until the user validates it; use "IMPLEMENTED (AWAITING VALIDATION)".
- **Never modernize 17th-century spelling or historical hyphenation.** `text_replacements` are for clear OCR defects only.
- **Volume-specific logic stays in `volumes/vN/convert.py` `OVERRIDES`**; `shared.py`/`extract.py`/`render.py` stay generic.
- **Whitelists are dual-format** (`volume_N_whitelist.json` + `.md` under `volumes/vN/bugs_fixes/`) and every entry must be explained in the final report.
- **Keep the repo root pristine**: diagnostics in `scratch/`, helpers in `scripts/`, session reports in `volumes/vN/reports/`.
- **Always build via `volumes/vN/convert.py`**, never legacy `converter.py` (it drops `OVERRIDES`).
