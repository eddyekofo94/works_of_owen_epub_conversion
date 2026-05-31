import json
import os
import re
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")
output_file = Path("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/recovered_code.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)

functions_to_find = [
    "_attach_em_dash_flat_list",
    "_repair_markdown_tables",
    "_repair_fused_word_ordinals"
]

print("Searching brain directory for discarded functions...")
recovered_data = {}

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    print(f"Reading {transcript_path.parent.parent.name}/transcript.jsonl...")
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                step = json.loads(line)
            except Exception:
                continue
            
            content = step.get("content", "")
            if not content:
                # also check tool_calls if any
                for tc in step.get("tool_calls", []):
                    args = tc.get("args", {})
                    if isinstance(args, dict):
                        content += "\n" + str(args.get("CodeContent", "")) + "\n" + str(args.get("ReplacementContent", ""))
            
            # Search for each function
            for func in functions_to_find:
                if func in content:
                    # Capture the content
                    if func not in recovered_data:
                        recovered_data[func] = []
                    recovered_data[func].append((len(content), content))

# Save the best (longest) recovered contents
with open(output_file, "w", encoding="utf-8") as out:
    for func, candidates in recovered_data.items():
        out.write("=" * 80 + "\n")
        out.write(f"RECOVERED FUNCTION: {func}\n")
        out.write("=" * 80 + "\n")
        # Sort by length descending to get the most complete snippet
        candidates.sort(key=lambda x: x[0], reverse=True)
        best_content = candidates[0][1]
        out.write(best_content)
        out.write("\n\n")

print(f"Done! Recovered code written to {output_file}")
