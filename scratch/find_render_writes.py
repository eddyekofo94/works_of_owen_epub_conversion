import json
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")

print("Scanning for all render.py writes in logs...")

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                step = json.loads(line)
            except Exception:
                continue
            
            tool_calls = step.get("tool_calls", [])
            for tc in tool_calls:
                name = tc.get("name", "")
                if name in ["replace_file_content", "write_to_file", "multi_replace_file_content"]:
                    args = tc.get("args", {})
                    target = args.get("TargetFile", "")
                    if "render.py" in target:
                        # Extract content from both single replacements, file writes, and multi replacement chunks
                        content = args.get("CodeContent", "") or args.get("ReplacementContent", "")
                        if not content and "ReplacementChunks" in args:
                            chunks = args.get("ReplacementChunks", [])
                            if isinstance(chunks, list):
                                content = "\n\n# CHUNK SPLIT #\n\n".join(
                                    chunk.get("ReplacementContent", "") for chunk in chunks if isinstance(chunk, dict)
                                )
                        if content:
                            out_fn = f"scratch/render_write_{folder.name}_{step.get('step_index')}.py"
                            with open(out_fn, "w", encoding="utf-8") as out_f:
                                out_f.write(content)
                            print(f"-> [{folder.name} step {step.get('step_index')}] Saved write to {out_fn} ({len(content)} chars)")
