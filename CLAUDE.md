# Owen EPUB Conversion — Development & Conversion Guidelines

This repository provides tools and scripts to convert scanned and OCR'ed PDF volumes of John Owen's works into high-quality, modern EPUB formats.

## Development Workflow

### Python Environment
Always use the virtual environment for running conversion scripts, tests, or utility scripts:
* Activator: `.venv/bin/activate`
* Run python: `./.venv/bin/python3 <script_name>.py`

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
