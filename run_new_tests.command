#!/bin/bash
# Double-click this file to run all Owen regression tests in Terminal.
cd "$(dirname "$0")"
echo "=== Owen regression test suite ==="
echo ""
echo "Running full text-fidelity suite (structure, syllabus, signal-F, blockquotes)..."
.venv/bin/python3 -m pytest tests/test_text_fidelity.py -v 2>&1
echo ""
echo "Running Volume 2 bug regressions..."
OWEN_REGRESSION_VOLUMES=2 .venv/bin/python3 -m pytest tests/test_bug_regressions.py -v 2>&1
echo ""
echo "Done."
