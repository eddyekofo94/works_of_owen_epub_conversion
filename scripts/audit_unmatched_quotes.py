#!/usr/bin/env python3
"""
Audit unmatched quotation marks in a volume's intermediate JSON.
Generates a detailed report listing full paragraphs with highlighted quotes.
"""

import json
import re
import sys
import argparse
from pathlib import Path

def highlight_quotes(text: str) -> str:
    """Highlight all double quotes in the text by wrapping them in double asterisks."""
    # We want to match straight and curly double quotes: ", “, ”
    # Wrap them in **"**, **“**, **”** respectively.
    def repl(match):
        char = match.group(0)
        return f"**{char}**"
    return re.sub(r'["“”]', repl, text)

def count_quotes(text: str) -> int:
    """Count double quotes in the text."""
    # Strip HTML tags to avoid counting double quotes inside attribute values (e.g. lang="la")
    clean_text = re.sub(r'<[^>]+>', '', text)
    return len(re.findall(r'["“”]', clean_text))

def main():
    parser = argparse.ArgumentParser(description="Audit and output unclosed/unmatched quotation marks for a given volume.")
    parser.add_argument("volume", type=int, help="Volume number (e.g., 5)")
    args = parser.parse_args()

    vol_num = args.volume
    here = Path(__file__).resolve().parent
    root = here.parent
    vol_dir = root / "volumes" / f"v{vol_num}"
    vol_json_path = vol_dir / "intermediate" / f"volume_{vol_num}.json"
    output_md_path = vol_dir / "bugs_fixes" / f"volume_{vol_num}_unmatched_quotes.md"

    if not vol_json_path.exists():
        print(f"Error: Volume intermediate JSON not found: {vol_json_path}")
        sys.exit(1)

    print(f"Reading Volume {vol_num} intermediate JSON...")
    with open(vol_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Load whitelist if it exists to allow skipping known safe/acceptable unmatched quotes
    # (e.g. intentional multi-paragraph quotes, list items with quotes, etc.)
    whitelist = {}
    whitelist_path = vol_dir / "bugs_fixes" / f"volume_{vol_num}_whitelist.json"
    if whitelist_path.exists():
        try:
            whitelist = json.loads(whitelist_path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[Warning] Failed to load whitelist {whitelist_path}: {e}")

    whitelisted_quotes = whitelist.get("anomalies", {}).get("Unmatched Quotation Marks", [])

    # Load config overrides if available to apply repairs before auditing
    config = {}
    vol_convert_path = vol_dir / "convert.py"
    if vol_convert_path.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"v{vol_num}_convert", vol_convert_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                config = getattr(module, "OVERRIDES", {})
        except Exception as e:
            print(f"[Warning] Failed to load overrides from {vol_convert_path}: {e}")

    from shared import _repair_owen_ocr_errors

    unmatched_paras = []
    total_paragraphs = 0
    total_unmatched = 0

    for ch in data.get("chapters", []):
        title = ch.get("title", "Unknown Chapter")
        raw_text = ch.get("raw_text", "")
        if not raw_text:
            continue

        raw_text = _repair_owen_ocr_errors(raw_text, config=config)


        paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        for idx, para in enumerate(paragraphs):
            total_paragraphs += 1
            q_count = count_quotes(para)
            if q_count % 2 != 0:
                # Check if it is whitelisted
                # Match by checking if the whitelist item is contained in the paragraph
                is_whitelisted = False
                import re
                for w_item in whitelisted_quotes:
                    w_clean = re.sub(r'\*\*|_', '', w_item).rstrip(".\"\' ")
                    p_clean = re.sub(r'\*\*|_', '', para).rstrip(".\"\' ")
                    if w_clean in p_clean or p_clean in w_clean:
                        is_whitelisted = True
                        break
                
                if is_whitelisted:
                    continue

                total_unmatched += 1
                unmatched_paras.append({
                    "chapter": title,
                    "paragraph_index": idx + 1,
                    "quote_count": q_count,
                    "text": para,
                    "highlighted_text": highlight_quotes(para)
                })

    # Generate Markdown Report
    md_lines = [
        f"# Unmatched Quotation Marks Report: Volume {vol_num}",
        "",
        "This report lists all paragraphs containing an odd number of double quotes.",
        "Some of these may be legitimate (e.g., multi-paragraph quotes where only the last paragraph gets a closing quote),",
        "while others may indicate dropped words, OCR defects, or punctuation errors.",
        "",
        f"- **Total Paragraphs Checked:** {total_paragraphs}",
        f"- **Unmatched Paragraphs Found:** {total_unmatched}",
        "",
        "---",
        ""
    ]

    if not unmatched_paras:
        md_lines.append("## No unmatched quotation marks found!")
    else:
        for idx, item in enumerate(unmatched_paras, 1):
            md_lines.extend([
                f"### {idx}. Chapter: *{item['chapter']}* (Paragraph {item['paragraph_index']})",
                f"* **Quotation Marks Count:** {item['quote_count']}",
                "* **Paragraph Text (Quotes Highlighted):**",
                "",
                f"{item['highlighted_text']}",
                "",
                "---",
                ""
            ])

    output_md_path.parent.mkdir(parents=True, exist_ok=True)
    output_md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Report generated successfully: {output_md_path}")

    # Write JSON companion report
    output_json_path = output_md_path.with_suffix(".json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "volume": vol_num,
            "total_paragraphs_checked": total_paragraphs,
            "unmatched_quotes_count": total_unmatched,
            "unmatched_paragraphs": unmatched_paras
        }, f, indent=2)
    print(f"JSON summary written to: {output_json_path}")
    print(f"Found {total_unmatched} paragraphs with unmatched quotes (excluding whitelisted).")


if __name__ == "__main__":
    main()
