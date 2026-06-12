#!/usr/bin/env python3
"""
Audit and trace whitelist usage and greediness for Owen volumes.

This script:
1. Loads a volume's whitelist JSON.
2. Temporarily backs up existing anomaly and text integrity reports.
3. Runs the audit scripts with '--no-whitelist' to get raw, unfiltered issues.
4. Restores the original reports.
5. Matches the whitelist entries against the raw issues to trace exactly:
   - What each whitelist entry is silencing.
   - If an entry is 'greedy' (matching multiple distinct issues).
   - If an entry is unused (matching zero issues).
6. Outputs a detailed Markdown report under volumes/vN/bugs_fixes/volume_N_whitelist_audit.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cli_utils import bold, cyan, dim, green, red, status_icon, yellow

PYTHON = sys.executable


def resolve_volumes(args: list[str]) -> list[str]:
    OWEN_VOLUMES = [str(i) for i in range(1, 17)]
    HEBREWS_VOLUMES = [f"h{i}" for i in range(1, 8)]
    ALL_VOLUMES = OWEN_VOLUMES + HEBREWS_VOLUMES
    if not args:
        return []
    if len(args) == 1 and args[0].lower() in ("all", "--all"):
        return ALL_VOLUMES
    seen = set()
    result = []
    for arg in args:
        v_str = arg.lower()
        if v_str.startswith('h'):
            if v_str in HEBREWS_VOLUMES and v_str not in seen:
                seen.add(v_str)
                result.append(v_str)
        else:
            v_num = v_str[1:] if v_str.startswith('v') else v_str
            if v_num in [str(i) for i in range(1, 17)] and v_num not in seen:
                seen.add(v_num)
                result.append(v_num)
    return result


def match_quote_anomaly(item: str, target: str) -> bool:
    """Matches unmatched quotes using the same fuzzy cleaning logic as audit_anomalies.py."""
    # Strip unclosed HTML tags at the end of the string
    t_clean = re.sub(r'<[^>]*$', '', target)
    i_clean = re.sub(r'<[^>]*$', '', item)
    # Strip all closed HTML tags
    t_clean = re.sub(r'<[^+>]+>', '', t_clean)
    t_clean = re.sub(r'<[^>]+>', '', t_clean)
    i_clean = re.sub(r'<[^+>]+>', '', i_clean)
    i_clean = re.sub(r'<[^>]+>', '', i_clean)
    # Strip footnote brackets like [f23] or [12]
    t_clean = re.sub(r'\[[^\]]+\]', '', t_clean)
    i_clean = re.sub(r'\[[^\]]+\]', '', i_clean)
    # Strip markdown formatting
    t_clean = re.sub(r'\*\*|_', '', t_clean)
    i_clean = re.sub(r'\*\*|_', '', i_clean)
    # Remove ellipsis
    t_clean = t_clean[:-3] if t_clean.endswith("...") else t_clean
    i_clean = i_clean[:-3] if i_clean.endswith("...") else i_clean
    # Normalize whitespace and lowercase
    t_clean = re.sub(r'\s+', ' ', t_clean).lower().strip()
    i_clean = re.sub(r'\s+', ' ', i_clean).lower().strip()
    
    if t_clean and i_clean:
        return t_clean.startswith(i_clean) or i_clean.startswith(t_clean)
    return False


def run_whitelist_audit(vol: str) -> int:
    from shared import get_volume_dir
    vol_dir = get_volume_dir(vol)
    bugs_dir = vol_dir / "bugs_fixes"
    whitelist_path = bugs_dir / f"volume_{vol}_whitelist.json"
    
    if not whitelist_path.exists():
        print(f"[{vol}] Whitelist file not found: {whitelist_path}")
        return 0

    print(f"[{vol}] Loading whitelist...")
    try:
        whitelist = json.loads(whitelist_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[{vol}] {red('Error loading whitelist')}: {e}")
        return 1

    # Paths of reports to backup
    anomalies_json = bugs_dir / f"volume_{vol}_anomalies.json"
    anomalies_md = bugs_dir / f"volume_{vol}_anomalies.md"
    integrity_json = bugs_dir / f"volume_{vol}_text_integrity.json"
    integrity_md = bugs_dir / f"volume_{vol}_text_integrity.md"

    # Temporary backups
    backups: dict[Path, Path] = {}
    for p in (anomalies_json, anomalies_md, integrity_json, integrity_md):
        if p.exists():
            bak = Path(str(p) + ".bak_wl_audit")
            p.rename(bak)
            backups[p] = bak

    raw_anomalies: dict[str, Any] = {}
    raw_integrity: dict[str, Any] = {}

    try:
        print(f"[{vol}] Running audits without whitelists to collect raw issues...")
        # 1. Run anomalies audit
        cmd_anom = [PYTHON, str(ROOT / "scripts" / "audit_anomalies.py"), vol, "--no-whitelist"]
        subprocess.run(cmd_anom, capture_output=True, text=True, check=True)
        if anomalies_json.exists():
            raw_anomalies = json.loads(anomalies_json.read_text(encoding="utf-8"))

        # 2. Run text integrity audit
        cmd_integ = [PYTHON, str(ROOT / "scripts" / "audit_text_integrity.py"), vol, "--no-whitelist", "--no-bug-log"]
        subprocess.run(cmd_integ, capture_output=True, text=True, check=True)
        if integrity_json.exists():
            raw_integrity = json.loads(integrity_json.read_text(encoding="utf-8"))

    except Exception as e:
        print(f"[{vol}] {red('Error running raw audits')}: {e}")
        return 1
    finally:
        # Restore backups
        for original, bak in backups.items():
            if original.exists():
                original.unlink()
            if bak.exists():
                bak.rename(original)

    print(f"[{vol}] Tracing whitelist matches...")

    # Data structures for results
    anomaly_matches: dict[str, dict[str, list[dict]]] = {}
    split_matches: dict[Any, list[dict]] = {}
    warning_matches: dict[str, list[str]] = {}

    # 1. Audit Anomalies Whitelist
    whitelist_anom = whitelist.get("anomalies", {})
    raw_anom_cats = raw_anomalies.get("anomalies", {})

    for category, items in whitelist_anom.items():
        anomaly_matches[category] = {}
        raw_items = raw_anom_cats.get(category, [])
        for wl_item in items:
            anomaly_matches[category][wl_item] = []
            for raw_hit in raw_items:
                target = raw_hit.get("target", "")
                matched = False
                
                # Check match logic
                if target == wl_item:
                    matched = True
                elif target.strip().lower() == wl_item.strip().lower():
                    matched = True
                elif category == "Unmatched Quotation Marks":
                    matched = match_quote_anomaly(wl_item, target)
                else:
                    # Substring matching (greedy check)
                    if wl_item in target or target in wl_item:
                        matched = True

                if matched:
                    anomaly_matches[category][wl_item].append(raw_hit)

    # 2. Audit Text Integrity Whitelist
    # 2a. Paragraph Splits
    whitelist_splits = whitelist.get("text_integrity", {}).get("paragraph_splits", [])
    raw_splits = raw_integrity.get("paragraph_integrity", {}).get("split_candidates", [])
    
    # Check if there were splits loaded or if we need to search through raw_integrity keys
    if not raw_splits and "split_candidates" in raw_integrity:
        raw_splits = raw_integrity["split_candidates"]

    for wl_sp in whitelist_splits:
        sp_key = json.dumps(wl_sp, sort_keys=True) if isinstance(wl_sp, dict) else wl_sp
        split_matches[sp_key] = []
        for raw_sp in raw_splits:
            matched = False
            prev_txt = raw_sp.get("previous", "")
            next_txt = raw_sp.get("next", "")
            
            if isinstance(wl_sp, dict):
                p_wl = wl_sp.get("previous", "")
                n_wl = wl_sp.get("next", "")
                if (p_wl in prev_txt or prev_txt in p_wl) and (n_wl in next_txt or next_txt in n_wl):
                    matched = True
            elif isinstance(wl_sp, str):
                if wl_sp in prev_txt or wl_sp in next_txt:
                    matched = True

            if matched:
                split_matches[sp_key].append(raw_sp)

    # 2b. Ignored Warnings
    whitelist_warnings = whitelist.get("text_integrity", {}).get("ignored_warnings", [])
    raw_warnings = raw_integrity.get("warnings", [])
    for wl_w in whitelist_warnings:
        warning_matches[wl_w] = []
        for raw_w in raw_warnings:
            if raw_w.get("code") == wl_w:
                warning_matches[wl_w].append(raw_w.get("message", ""))

    # Compile report statistics
    total_entries = 0
    exact_matches = 0
    greedy_entries = []
    unused_entries = []

    # Count statistics
    for category, items in anomaly_matches.items():
        for wl_item, hits in items.items():
            total_entries += 1
            if len(hits) == 0:
                unused_entries.append(f"anomalies -> {category} -> '{wl_item}'")
            elif len(hits) == 1:
                exact_matches += 1
            else:
                greedy_entries.append((f"anomalies -> {category} -> '{wl_item}'", len(hits)))

    for sp_key, hits in split_matches.items():
        total_entries += 1
        if len(hits) == 0:
            unused_entries.append(f"text_integrity -> paragraph_splits -> {sp_key}")
        elif len(hits) == 1:
            exact_matches += 1
        else:
            greedy_entries.append((f"text_integrity -> paragraph_splits -> {sp_key}", len(hits)))

    for wl_w, hits in warning_matches.items():
        total_entries += 1
        if len(hits) == 0:
            unused_entries.append(f"text_integrity -> ignored_warnings -> '{wl_w}'")
        elif len(hits) == 1:
            exact_matches += 1
        else:
            greedy_entries.append((f"text_integrity -> ignored_warnings -> '{wl_w}'", len(hits)))

    # Write Markdown Report
    output_md = bugs_dir / f"volume_{vol}_whitelist_audit.md"
    print(f"[{vol}] Writing report to {output_md}...")
    
    md_lines = [
        f"# Whitelist Trace & Audit Report: Volume {vol}",
        "",
        "This report tracks and validates every whitelist entry to prevent greedy silencing of real anomalies.",
        "",
        "## Summary",
        "",
        f"* **Total Whitelisted Entries:** {total_entries}",
        f"* **Clean/Exact Matches (1 issue silenced):** {exact_matches}",
        f"* **Greedy Entries (silences multiple issues):** {len(greedy_entries)}",
        f"* **Unused Entries (silences 0 issues - safe to remove):** {len(unused_entries)}",
        "",
    ]

    if greedy_entries:
        md_lines.extend([
            "### ⚠️ Greedy Whitelist Entries",
            "These entries are too broad and matched multiple distinct anomalies. Consider making them more specific.",
            "",
            "| Whitelist Path / Entry | Match Count |",
            "|-------------------------|-------------|",
        ])
        for entry, count in greedy_entries:
            md_lines.append(f"| `{entry}` | {count} |")
        md_lines.append("")

    if unused_entries:
        md_lines.extend([
            "### ❌ Unused Whitelist Entries",
            "These entries matched zero raw issues. They should be deleted to keep the whitelist clean.",
            "",
        ])
        for entry in unused_entries:
            md_lines.append(f"* `{entry}`")
        md_lines.append("")

    md_lines.extend([
        "---",
        "",
        "## Detailed Trace by Category",
        "",
    ])

    # 1. Detail Anomalies Trace
    md_lines.append("### 1. Anomalies Whitelist")
    for category, items in anomaly_matches.items():
        md_lines.append(f"\n#### Category: `{category}`\n")
        if not items:
            md_lines.append("No whitelist entries for this category.\n")
            continue

        for wl_item, hits in items.items():
            status = "❌ Unused" if not hits else ("⚠️ Greedy" if len(hits) > 1 else "✅ Clean")
            md_lines.append(f"##### Entry: `{wl_item}` ({status})")
            if not hits:
                md_lines.append("  * Silenced 0 raw issues.")
            else:
                md_lines.append(f"  * Silenced {len(hits)} raw issue(s):")
                for hit in hits:
                    ch = hit.get("chapter", "Unknown Chapter")
                    desc = hit.get("description", "")
                    contexts = hit.get("contexts", [])
                    md_lines.append(f"    * **Chapter:** *{ch}* — `{desc}`")
                    for ctx in contexts:
                        highlighted = re.sub(rf"({re.escape(hit.get('target', ''))})", r"**\1**", ctx, flags=re.I)
                        md_lines.append(f"      * Context: `{highlighted.strip()}`")
            md_lines.append("")

    # 2. Detail Text Integrity Trace
    md_lines.append("\n### 2. Text Integrity Whitelist")
    md_lines.append("\n#### Paragraph Splits\n")
    if not split_matches:
        md_lines.append("No whitelist entries for paragraph splits.\n")
    else:
        for sp_key, hits in split_matches.items():
            status = "❌ Unused" if not hits else ("⚠️ Greedy" if len(hits) > 1 else "✅ Clean")
            md_lines.append(f"##### Split Entry: `{sp_key}` ({status})")
            if not hits:
                md_lines.append("  * Silenced 0 paragraph splits.")
            else:
                md_lines.append(f"  * Silenced {len(hits)} paragraph split(s):")
                for hit in hits:
                    file = hit.get("file", "Unknown File")
                    prev = hit.get("previous", "").replace("\n", " ").strip()
                    nxt = hit.get("next", "").replace("\n", " ").strip()
                    md_lines.extend([
                        f"    * **File:** `{file}`",
                        f"      * Previous: `... {prev}`",
                        f"      * Next: `{nxt} ...`"
                    ])
            md_lines.append("")

    md_lines.append("\n#### Ignored Warnings\n")
    if not warning_matches:
        md_lines.append("No whitelist entries for ignored warnings.\n")
    else:
        for wl_w, hits in warning_matches.items():
            status = "❌ Unused" if not hits else "✅ Clean"
            md_lines.append(f"##### Warning Entry: `{wl_w}` ({status})")
            if not hits:
                md_lines.append("  * Silenced 0 warnings.")
            else:
                md_lines.append(f"  * Silenced warning message(s):")
                for hit in hits:
                    md_lines.append(f"    * `{hit}`")
            md_lines.append("")

    output_md.write_text("\n".join(md_lines), encoding="utf-8")

    # Write JSON Report
    output_json = bugs_dir / f"volume_{vol}_whitelist_audit.json"
    print(f"[{vol}] Writing JSON report to {output_json}...")
    
    # Convert sets/paths for JSON serialization
    serialized_anom = {}
    for cat, items in anomaly_matches.items():
        serialized_anom[cat] = {}
        for wl_item, hits in items.items():
            serialized_anom[cat][wl_item] = hits

    serialized_splits = {}
    for sp_key, hits in split_matches.items():
        serialized_splits[sp_key] = hits

    try:
        output_json.write_text(json.dumps({
            "volume": vol,
            "summary": {
                "total_entries": total_entries,
                "exact_matches": exact_matches,
                "greedy_count": len(greedy_entries),
                "unused_count": len(unused_entries)
            },
            "greedy_entries": greedy_entries,
            "unused_entries": unused_entries,
            "anomaly_matches": serialized_anom,
            "split_matches": serialized_splits,
            "warning_matches": warning_matches
        }, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[{vol}] Failed to save JSON report: {e}")

    # Output Console Summaries
    print(f"\n======================================================================")
    print(f" WHITELIST AUDIT COMPLETE: VOLUME {vol}")
    print(f" Total whitelisted entries: {total_entries}")
    print(f" Exact matches: {exact_matches}")
    if greedy_entries:
        print(f" {yellow(f'Greedy entries: {len(greedy_entries)}')}")
        for entry, count in greedy_entries:
            print(f"   - '{entry}' matched {count} times")
    if unused_entries:
        print(f" {red(f'Unused entries: {len(unused_entries)}')}")
    print(f" Report written to: {output_md}")
    print(f"======================================================================\n")

    return 1 if (greedy_entries or unused_entries) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a volume's whitelist entries against raw issues to trace usage and greediness.")
    parser.add_argument("volumes", nargs="*", help="Volume numbers/identifiers (default: all volumes with whitelists)")
    parser.add_argument("--all", action="store_true", help="Process all volumes")
    args = parser.parse_args()

    volumes = resolve_volumes(args.volumes)
    if args.all or (not args.volumes and not volumes):
        # Auto-detect all volumes that have a whitelist
        detected = []
        for d in (ROOT / "volumes").iterdir():
            if d.is_dir() and d.name.startswith("v"):
                vol_num = d.name[1:]
                wl = d / "bugs_fixes" / f"volume_{vol_num}_whitelist.json"
                if wl.exists():
                    detected.append(vol_num)
            elif d.is_dir() and d.name.startswith("h") and d.name[1:].isdigit():
                vol_num = d.name
                wl = d / "bugs_fixes" / f"volume_{vol_num}_whitelist.json"
                if wl.exists():
                    detected.append(vol_num)
        
        # Sort using standard sorting
        from scripts.run_all_checks import vol_sort_key
        volumes = sorted(detected, key=vol_sort_key)

    if not volumes:
        print("No volumes with whitelists detected or specified.", file=sys.stderr)
        return 0

    print(f"Auditing whitelists for volume(s): {bold(', '.join(volumes))}")
    any_issues = False
    for vol in volumes:
        ret = run_whitelist_audit(vol)
        if ret > 0:
            any_issues = True

    return 1 if any_issues else 0


if __name__ == "__main__":
    sys.exit(main())
