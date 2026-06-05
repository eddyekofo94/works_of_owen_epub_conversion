#!/usr/bin/env python3
"""
John Owen Works Conversion — Code Review & Architectural Audit Tool.

This script performs automated static analysis of the Python source files and CSS
templates to ensure compliance with GEMINI.md mandates, detect common code smells,
and verify repository cleanliness.
"""

import os
import re
import sys
import ast
from typing import List, Dict, Any, Set

# Allowed files and directories in the repository root (GEMINI.md Rule 7)
ALLOWED_ROOT_ITEMS = {
    # Directories
    ".git",
    ".venv",
    ".pytest_cache",
    ".antigravitycli",
    ".gemini",
    "__pycache__",
    "bugs_fixes",
    "covers",
    "covers_backup",
    "docs",
    "epub_examples",
    "fonts",
    "pdfs",
    "plans",
    "portraits",
    "qa",
    "scratch",
    "scripts",
    "skills",
    "special_sources",
    "tests",
    "volumes",
    # Files
    "README.md",
    "AGENTS.md",
    "GEMINI.md",
    "PLAN.md",
    "ENGINEERING_LOG.md",
    "extract.py",
    "render.py",
    "converter.py",
    "shared.py",
    "owen",
    "requirements.txt",
    "works_of_john_owen.md",
    ".gitignore",
    "CLAUDE.md",
    ".DS_Store",
    "pytest.ini",
}

# Colorized helpers
def _supports_color() -> bool:
    return sys.stdout.isatty()

def green(text: str) -> str:
    return f"\033[92m{text}\033[0m" if _supports_color() else text

def red(text: str) -> str:
    return f"\033[91m{text}\033[0m" if _supports_color() else text

def yellow(text: str) -> str:
    return f"\033[93m{text}\033[0m" if _supports_color() else text

def cyan(text: str) -> str:
    return f"\033[96m{text}\033[0m" if _supports_color() else text

def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m" if _supports_color() else text

def dim(text: str) -> str:
    return f"\033[2m{text}\033[0m" if _supports_color() else text


class ASTVisitor(ast.NodeVisitor):
    """AST Visitor to analyze Python files for structural code smells."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # 1. Function length check (max 150 lines)
        length = (node.end_lineno - node.lineno) if node.end_lineno else 0
        if length > 150:
            self.issues.append({
                "type": "Code Smell (Long Function)",
                "severity": "Warning",
                "message": f"Function '{node.name}' is {length} lines long (exceeds recommended max of 150 lines). Consider modularizing.",
                "line": node.lineno
            })

        # 2. Too many arguments (max 6)
        args_count = len(node.args.args)
        if args_count > 6:
            self.issues.append({
                "type": "Code Smell (Too Many Parameters)",
                "severity": "Warning",
                "message": f"Function '{node.name}' has {args_count} arguments (recommended max of 6).",
                "line": node.lineno
            })

        # 3. Missing type hints recommendation
        has_hints = True
        for arg in node.args.args:
            if arg.arg != "self" and arg.arg != "cls" and arg.annotation is None:
                has_hints = False
                break
        if node.returns is None:
            has_hints = False

        if not has_hints:
            # We suggest hints for non-private or substantial functions (>20 lines)
            if not node.name.startswith("_") or length > 20:
                self.issues.append({
                    "type": "Style (Missing Type Hints)",
                    "severity": "Info",
                    "message": f"Function '{node.name}' does not have full type annotations for arguments or return type.",
                    "line": node.lineno
                })

        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        # 4. Broad exception handling check
        for handler in node.handlers:
            if handler.type is None:
                self.issues.append({
                    "type": "Code Smell (Broad except)",
                    "severity": "Warning",
                    "message": "Broad 'except:' clause is discouraged. Catch 'Exception' or a specific subclass instead.",
                    "line": handler.lineno
                })
            elif isinstance(handler.type, ast.Name) and handler.type.id == "BaseException":
                self.issues.append({
                    "type": "Code Smell (Catch BaseException)",
                    "severity": "Warning",
                    "message": "Catching 'BaseException' directly can intercept system-exit exceptions like KeyboardInterrupt. Catch 'Exception' instead.",
                    "line": handler.lineno
                })
        self.generic_visit(node)


def audit_clean_root(root_path: str) -> List[Dict[str, Any]]:
    """Verify Rule 7: Root folder remains clean."""
    issues = []
    try:
        for entry in os.scandir(root_path):
            if entry.name not in ALLOWED_ROOT_ITEMS:
                issues.append({
                    "type": "GEMINI.md Rule 7 (Root Cleanliness)",
                    "severity": "Error",
                    "message": f"Non-whitelisted item '{entry.name}' found in repository root. Move all diagnostic/temporary files to 'scratch/' and persistent helpers to 'scripts/'.",
                    "line": 0
                })
    except Exception as e:
        issues.append({
            "type": "System Error",
            "severity": "Error",
            "message": f"Failed to audit root directory cleanliness: {e}",
            "line": 0
        })
    return issues


def audit_font_face_integrity(content: str, filename: str) -> List[Dict[str, Any]]:
    """Verify Rule 9: Every @font-face declaration contains weight and style."""
    issues = []
    
    # Use robust brace counting to extract @font-face blocks (handles double and nested braces)
    # Find all occurrences of "@font-face"
    for m in re.finditer(r'@font-face', content):
        start_idx = m.end()
        # Scan forward to find the opening brace
        open_brace_idx = -1
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                open_brace_idx = i
                break
        if open_brace_idx == -1:
            continue
            
        # Check if the opening brace is close to @font-face (only whitespace or comments allowed in between)
        between = content[start_idx:open_brace_idx]
        between_clean = re.sub(r'/\*.*?\*/', '', between, flags=re.S)
        if not re.match(r'^\s*$', between_clean):
            continue
            
        # Scan forward matching braces to find the closing brace (handles placeholders inside f-strings)
        depth = 0
        close_brace_idx = -1
        for i in range(open_brace_idx, len(content)):
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
                if depth == 0:
                    close_brace_idx = i
                    break
                    
        if close_brace_idx != -1:
            block = content[open_brace_idx + 1:close_brace_idx]
            line_num = content.count('\n', 0, m.start()) + 1
            
            # Skip check if the block appears to be a dynamic formatting template variable reference
            # (e.g. "@font-face { {bold_face} }") and check if it is defined in the variables.
            # Usually, those variables will be checked individually.
            is_template_ref = "{" in block and "}" in block and not any(kw in block for kw in ["font-weight", "font-style"])
            if is_template_ref and ("bold_face" in content or "italic_face" in content):
                continue
                
            has_weight = "font-weight" in block
            has_style = "font-style" in block
            
            if not has_weight or not has_style:
                missing = []
                if not has_weight: missing.append("font-weight")
                if not has_style: missing.append("font-style")
                issues.append({
                    "type": "GEMINI.md Rule 9 (@font-face Integrity)",
                    "severity": "Error",
                    "message": f"@font-face declaration block is missing: {', '.join(missing)}.",
                    "line": line_num
                })
                
    # Also verify in shared.py generate_font_styles code explicitly
    if "shared.py" in filename:
        # Check dynamic templates inside shared.py using the same brace counting
        dynamic_vars = ["bold_face", "italic_face", "bold_italic_face"]
        dynamic_checks = {
            "bold_face": ("font-weight: bold", "font-style: normal"),
            "italic_face": ("font-weight: normal", "font-style: italic"),
            "bold_italic_face": ("font-weight: bold", "font-style: italic")
        }
        for var_name in dynamic_vars:
            # Locate where the variable is assigned to a font-face string
            var_match = re.search(rf'{var_name}\s*=\s*(?:f)?\'@font-face', content)
            if var_match:
                start_idx = var_match.end()
                # Find opening brace
                open_brace_idx = -1
                for i in range(start_idx, len(content)):
                    if content[i] == '{':
                        open_brace_idx = i
                        break
                if open_brace_idx == -1:
                    continue
                # Count braces to extract block
                depth = 0
                close_brace_idx = -1
                for i in range(open_brace_idx, len(content)):
                    if content[i] == '{':
                        depth += 1
                    elif content[i] == '}':
                        depth -= 1
                        if depth == 0:
                            close_brace_idx = i
                            break
                if close_brace_idx != -1:
                    block_content = content[open_brace_idx + 1:close_brace_idx]
                    line_num = content.count('\n', 0, var_match.start()) + 1
                    req_weight, req_style = dynamic_checks[var_name]
                    if req_weight not in block_content or req_style not in block_content:
                        issues.append({
                            "type": "GEMINI.md Rule 9 (@font-face Integrity)",
                            "severity": "Error",
                            "message": f"Dynamic font template variable '{var_name}' is missing weight/style ('{req_weight}' or '{req_style}').",
                            "line": line_num
                        })
    return issues


def audit_greek_hebrew_ranges(content: str, filename: str) -> List[Dict[str, Any]]:
    """Verify Rule 6: Overlap-removal and deduplication functions include Greek and Hebrew Unicode ranges."""
    issues = []
    
    # Check for functions like _remove_adjacent_line_overlaps or regex patterns checking overlap words
    if "dedupe" in filename or "clean" in filename or "extract" in filename:
        # Check if we find standard word regexes used in overlaps
        # e.g., words_with_spans or adjacent line overlap regexes
        overlap_func = re.search(r'def\s+(_remove_adjacent_line_overlaps|_remove_overlaps|words_with_spans)\b', content)
        if overlap_func:
            line_num = content.count('\n', 0, overlap_func.start()) + 1
            # Check for the greek and hebrew unicode block patterns:
            # Greek: \u0370-\u03FF and \u1F00-\u1FFF
            # Hebrew: \u0590-\u05FF
            has_greek = r"\u0370-\u03FF" in content and r"\u1F00-\u1FFF" in content
            has_hebrew = r"\u0590-\u05FF" in content
            
            if not has_greek or not has_hebrew:
                missing = []
                if not has_greek: missing.append("Greek (\\u0370-\\u03FF and \\u1F00-\\u1FFF)")
                if not has_hebrew: missing.append("Hebrew (\\u0590-\\u05FF)")
                
                issues.append({
                    "type": "GEMINI.md Rule 6 (Greek/Hebrew Preservation)",
                    "severity": "Error",
                    "message": f"Word overlap / deduplication function might be missing Greek/Hebrew Unicode ranges: {', '.join(missing)}.",
                    "line": line_num
                })
    return issues


def audit_architectural_separation(content: str, filename: str) -> List[Dict[str, Any]]:
    """Verify Rule 5: Base scripts should not contain volume-specific hardcoded overrides."""
    issues = []
    basename = os.path.basename(filename)
    
    # Only base scripts should be checked for this
    if basename in ["shared.py", "extract.py", "render.py", "converter.py"]:
        # Look for hardcoded references to specific volume override dicts or conditions.
        # e.g., checking if volume number == X and applying specific text replacements inside the base file
        # We permit normal operations that load overrides dynamically via CONFIG or config.get() or volumes/v{n} dynamic paths,
        # but we flag hardcoded overrides.
        
        # Search for hardcoded text replacements like `"on]y": "only"` or volume-specific titles.
        hardcoded_ocr_pat = r'("on\]y"\s*:\s*"only"|"Charneck"\s*:\s*"Charnock"|"whoso"\s*:\s*"whose")'
        match = re.search(hardcoded_ocr_pat, content)
        if match:
            line_num = content.count('\n', 0, match.start()) + 1
            issues.append({
                "type": "GEMINI.md Rule 5 (Architectural Separation)",
                "severity": "Error",
                "message": f"Found volume-specific OCR replacements hardcoded in base script '{basename}'. These must reside in volume-specific OVERRIDES.",
                "line": line_num
            })
            
        # Search for hardcoded treatise title matches in conditionals (re.search)
        # e.g. CHRISTOLOGIA, MEDITATIONS, etc.
        hardcoded_titles = r'\b(CHRISTOLOGIA|TWO SHORT CATECHISMS|PNEUMATOLOGIA|Evidences of the Faith)\b'
        for match in re.finditer(hardcoded_titles, content):
            # Check context to see if it's in a comment (which is fine) or code
            start = match.start()
            line_num = content.count('\n', 0, start) + 1
            line = content.split('\n')[line_num - 1]
            if "#" not in line.split(match.group(0))[0]:  # Not a comment
                # Allow it if it is an archive index or documentation list, but warn if it is code logic
                if "def " in line or "elif " in line or "if " in line or "==" in line or "re.search" in line:
                    issues.append({
                        "type": "GEMINI.md Rule 5 (Architectural Separation)",
                        "severity": "Warning",
                        "message": f"Hardcoded treatise title '{match.group(0)}' found in conditional logic in '{basename}'. Treatises should be handled via treatise_title_overrides.",
                        "line": line_num
                    })
    return issues


def audit_footnote_placement(content: str, filename: str) -> List[Dict[str, Any]]:
    """Verify Rule 11: Footnote links must always be placed AFTER punctuation marks."""
    issues = []
    
    # Scan for logic that replaces or swaps footnotes with punctuation.
    # If the code swaps a punctuation character and a footnote number to place the footnote FIRST, that violates Rule 11.
    # e.g. re.sub(r'(\.noteref.*?)([\.,;])', r'\2\1', ...) -> correct (moves punctuation before footnote)
    # re.sub(r'([\.,;])(\.noteref)', r'\2\1', ...) -> incorrect (moves footnote before punctuation)
    
    incorrect_swap = re.search(r're\.sub\([^)]*?[\'"]\\2\\1[\'"]\s*,\s*text\)', content)
    if incorrect_swap:
        line_num = content.count('\n', 0, incorrect_swap.start()) + 1
        issues.append({
            "type": "GEMINI.md Rule 11 (Footnote Placement)",
            "severity": "Warning",
            "message": "Potential footnote swap operation detected that may put footnote reference before punctuation.",
            "line": line_num
        })
    return issues


def audit_code_smells_file(content: str, filename: str) -> List[Dict[str, Any]]:
    """Audit python files for broad except, leftover print debugs, etc."""
    issues = []
    
    # Find leftover prints in core files (exclude utility scripts)
    basename = os.path.basename(filename)
    if basename in ["shared.py", "extract.py", "render.py", "converter.py"]:
        matches = re.finditer(r'\bprint\s*\([^)]*\)', content)
        for m in matches:
            line_num = content.count('\n', 0, m.start()) + 1
            line = content.split('\n')[line_num - 1]
            if "#" not in line.split("print")[0]: # Not in comment
                # Allow print if it's part of a logging print or CLI runner output, but warn
                issues.append({
                    "type": "Code Smell (Leftover Print)",
                    "severity": "Info",
                    "message": f"print() statement found in core file '{basename}'. Use logging or structured UI messages.",
                    "line": line_num
                })
                
    # Run AST-based structural analysis
    try:
        tree = ast.parse(content, filename=filename)
        visitor = ASTVisitor(filename)
        visitor.visit(tree)
        issues.extend(visitor.issues)
    except SyntaxError as se:
        issues.append({
            "type": "Syntax Error",
            "severity": "Error",
            "message": f"Syntax error preventing AST parse: {se}",
            "line": se.lineno or 0
        })
    except Exception as e:
        issues.append({
            "type": "System Error",
            "severity": "Error",
            "message": f"AST parser failed: {e}",
            "line": 0
        })
        
    return issues


def run_code_review(target_path: str = ".") -> Dict[str, List[Dict[str, Any]]]:
    """Execute all review rules across target path files."""
    results: Dict[str, List[Dict[str, Any]]] = {}
    
    # 1. Root directory cleanliness audit (always run on root)
    root_issues = audit_clean_root(".")
    if root_issues:
        results["Repository Root"] = root_issues
        
    # Determine target files
    files_to_check = []
    if os.path.isfile(target_path):
        if target_path.endswith(".py"):
            files_to_check.append(target_path)
    else:
        # Walk directories (skip .venv, .git, scratch, __pycache__, volumes outputs)
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in [".venv", ".git", "scratch", "__pycache__", "output", "intermediate"]]
            for f in files:
                if f.endswith(".py"):
                    files_to_check.append(os.path.join(root, f))
                    
    # Scan target files
    for filepath in sorted(files_to_check):
        rel_path = os.path.relpath(filepath, ".")
        file_issues = []
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            results[rel_path] = [{
                "type": "System Error",
                "severity": "Error",
                "message": f"Failed to read file: {e}",
                "line": 0
            }]
            continue
            
        # Run Rule audits
        file_issues.extend(audit_font_face_integrity(content, filepath))
        file_issues.extend(audit_greek_hebrew_ranges(content, filepath))
        file_issues.extend(audit_architectural_separation(content, filepath))
        file_issues.extend(audit_footnote_placement(content, filepath))
        file_issues.extend(audit_code_smells_file(content, filepath))
        
        if file_issues:
            results[rel_path] = file_issues
            
    return results


def print_cli_report(results: Dict[str, List[Dict[str, Any]]]) -> int:
    """Print results to standard output and count issues by severity."""
    total_errors = 0
    total_warnings = 0
    total_infos = 0
    
    print("\n" + bold(cyan("=== John Owen Works Conversion — Code Review Report ===")))
    
    if not results:
        print(green("\nNo code issues or compliance violations found. Codebase is in excellent shape! ✓\n"))
        return 0
        
    for source, issues in results.items():
        print(f"\n{bold(source)}:")
        # Sort issues by severity (Error -> Warning -> Info) and line number
        severity_order = {"Error": 0, "Warning": 1, "Info": 2}
        sorted_issues = sorted(issues, key=lambda x: (severity_order.get(x["severity"], 3), x["line"]))
        
        for issue in sorted_issues:
            sev = issue["severity"]
            line_str = f"L{issue['line']}: " if issue["line"] > 0 else ""
            msg = f"{line_str}{bold(issue['type'])} — {issue['message']}"
            
            if sev == "Error":
                print(f"  {red('[ERROR]')} {msg}")
                total_errors += 1
            elif sev == "Warning":
                print(f"  {yellow('[WARN] ')} {msg}")
                total_warnings += 1
            else:
                print(f"  {dim('[INFO] ')} {msg}")
                total_infos += 1
                
    print("\n" + bold(cyan("=== Summary ===")))
    print(f"Errors:   {red(str(total_errors)) if total_errors else green('0')}")
    print(f"Warnings: {yellow(str(total_warnings)) if total_warnings else green('0')}")
    print(f"Infos:    {dim(str(total_infos))}")
    
    # Return exit code based on Errors
    return 1 if total_errors > 0 else 0


def generate_markdown_report(results: Dict[str, List[Dict[str, Any]]], report_path: str):
    """Write detailed code review findings to a Markdown report file."""
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    total_errors = 0
    total_warnings = 0
    total_infos = 0
    
    for issues in results.values():
        for iss in issues:
            if iss["severity"] == "Error": total_errors += 1
            elif iss["severity"] == "Warning": total_warnings += 1
            else: total_infos += 1
            
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Code Review and Compliance Audit Report\n\n")
        f.write("This report summarizes compliance audits against the architectural mandates and styling principles specified in `GEMINI.md` and `AGENTS.md`.\n\n")
        
        f.write("## Metrics Summary\n\n")
        f.write("| Metric | Value | Status |\n")
        f.write("|---|---|---|\n")
        f.write(f"| **GEMINI.md Compliance Errors** | {total_errors} | {'❌ Action Required' if total_errors > 0 else '✅ Compliant'} |\n")
        f.write(f"| **Design / Code Quality Warnings** | {total_warnings} | {'⚠️ Attention Suggested' if total_warnings > 0 else '✅ Good'} |\n")
        f.write(f"| **Refactoring Recommendations (Infos)** | {total_infos} | Information |\n\n")
        
        if total_errors == 0 and total_warnings == 0:
            f.write("> [!NOTE]\n")
            f.write("> **Code Quality Check Passed:** The codebase complies perfectly with all repository and style guidelines. No violations were found.\n\n")
            
        f.write("## Detailed Findings\n\n")
        
        if not results:
            f.write("No issues detected.\n")
            return
            
        for source, issues in sorted(results.items()):
            f.write(f"### `{source}`\n\n")
            f.write("| Line | Severity | Check Type | Description |\n")
            f.write("|---|---|---|---|\n")
            
            # Sort issues by line number
            sorted_issues = sorted(issues, key=lambda x: x["line"])
            for iss in sorted_issues:
                line_text = f"L{iss['line']}" if iss["line"] > 0 else "Root"
                sev_icon = "🔴 Error" if iss["severity"] == "Error" else ("🟡 Warning" if iss["severity"] == "Warning" else "⚪ Info")
                f.write(f"| {line_text} | {sev_icon} | {iss['type']} | {iss['message']} |\n")
            f.write("\n")
            
        f.write("## Next Steps\n\n")
        if total_errors > 0:
            f.write("1. **Resolve GEMINI.md Errors (Critical)**: Fix font weight/style definitions, clear root-level temporary files, and check Greek/Hebrew regex formats.\n")
        if total_warnings > 0:
            f.write("2. **Refactor Code Smells (Recommended)**: Decompose functions exceeding 150 lines, avoid catching base exceptions, and reduce arguments on large functions.\n")
        f.write("3. **Validate Rebuilds**: Once fixes are applied, rebuild the volume using `volumes/vN/convert.py` and run tests `pytest tests/` to confirm correctness.\n")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    results = run_code_review(target)
    
    # Save markdown report to qa/reports/code_review.md
    report_file = os.path.join("qa", "reports", "code_review.md")
    generate_markdown_report(results, report_file)
    
    print(f"\nDetailed report written to: {bold(report_file)}")
    
    exit_code = print_cli_report(results)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
