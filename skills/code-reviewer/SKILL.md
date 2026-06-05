---
name: code-reviewer
description: Performs automated code reviews on base converter modules and scripts, validating compliance with GEMINI.md mandates, identifying code smells, and suggesting actionable improvements. Triggered by #review or #code-review.
---

# Code Reviewer Skill

This skill automates code reviews and architectural validation for the John Owen Works conversion project. It helps developers ensure compliance with all `GEMINI.md` mandates, detect code smells, and keep the repository clean.

## Command Syntax

The skill is triggered by the following slash-like commands:

- `#review` or `#code-review`: Perform a full code review of the entire workspace codebase.
- `#review [file_or_dir]`: Run the code reviewer on a specific file or directory (e.g., `#review render.py` or `#review scripts/`).

## Automated Checks

The code reviewer script checks for:

1.  **Repository Cleanliness (GEMINI.md Rule 7)**: Flags any non-whitelisted files or folders in the root directory.
2.  **@font-face Integrity (GEMINI.md Rule 9)**: Scans python source files and inline CSS for `@font-face` definitions, ensuring that all contain both `font-weight` and `font-style` properties to prevent family override issues.
3.  **Greek/Hebrew Preservation (GEMINI.md Rule 6)**: Inspects overlap-removal / de-duplication functions (such as `_remove_adjacent_line_overlaps`) to confirm that they include Greek and Hebrew Unicode character ranges in their regex word patterns.
4.  **Architectural Separation (GEMINI.md Rule 5)**: Warns if base scripts (`shared.py`, `extract.py`, `render.py`, `converter.py`) contain volume-specific override keys or logic instead of delegating to per-volume configurations.
5.  **Footnote Placement (GEMINI.md Rule 11)**: Scans for regex or replacement operations that might put footnote links before punctuation, violating the after-punctuation rule.
6.  **Code Smells & Readability (AST-Based)**:
    -   **Long Functions**: Functions exceeding 150 lines (candidates for refactoring/modularization).
    -   **Excessive Parameters**: Functions taking more than 6 arguments.
    -   **Broad Excepts**: Use of `except:` or `except BaseException:` instead of catching `Exception` or concrete exceptions.
    -   **Leftover Prints**: Check for `print(...)` in core conversion libraries where logging or helper outputs should be used instead.
    -   **Type Hinting**: Recommends adding Python type hints to functions to improve type safety and documentation.

## Workflow

1.  **Parse Command**: Extract the optional file or directory path arguments.
2.  **Execute Review Tool**: Run the analysis script using the workspace Python interpreter:
    ```bash
    .venv/bin/python3 scripts/code_review.py [target]
    ```
3.  **Output Report**:
    -   Displays color-coded summaries in the CLI.
    -   Saves a comprehensive markdown report in `qa/reports/code_review.md`.
4.  **Action Plan**: Review the warnings and errors generated, prioritizing `GEMINI.md` violations and critical code smells, and make necessary code updates.

## Resource Locations

-   **Skill Definition**: `skills/code-reviewer/SKILL.md`
-   **Review Script**: `scripts/code_review.py`
-   **Generated Report**: `qa/reports/code_review.md`
-   **Key Reference Rules**: `GEMINI.md` and `AGENTS.md`
