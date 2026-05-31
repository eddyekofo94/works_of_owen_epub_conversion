import json
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")
output_dir = Path("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/recovered")
output_dir.mkdir(parents=True, exist_ok=True)

functions_to_find = [
    "_repair_fused_word_ordinals",
    "_repair_markdown_tables",
    "_attach_em_dash_flat_list"
]

print("Scanning conversation transcripts for file-writing payloads...")

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            try:
                step = json.loads(line)
            except Exception:
                continue
            
            tool_calls = step.get("tool_calls", [])
            for tc_idx, tc in enumerate(tool_calls):
                name = tc.get("name", "")
                args = tc.get("args", {})
                if not isinstance(args, dict):
                    continue
                
                target = args.get("TargetFile", "")
                if "render.py" in target:
                    content = args.get("CodeContent", "") or args.get("ReplacementContent", "")
                    if not content:
                        continue
                    
                    for func in functions_to_find:
                        if func in content:
                            out_fn = output_dir / f"{folder.name}_step_{step.get('step_index')}_{func}.py"
                            with open(out_fn, "w", encoding="utf-8") as out:
                                out.write(content)
                            print(f"-> Recovered {func} from {folder.name} step {step.get('step_index')} to {out_fn.name} ({len(content)} chars)")
