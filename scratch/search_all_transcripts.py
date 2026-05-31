import json
import re
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")
output_dir = Path("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/recovered_exhaustive")
output_dir.mkdir(parents=True, exist_ok=True)

functions_to_find = [
    "def _repair_fused_word_ordinals",
    "def _repair_markdown_tables"
]

print("Exhaustively scanning all past transcripts for function definitions...")

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            for func in functions_to_find:
                if func in line:
                    try:
                        step = json.loads(line)
                    except Exception:
                        continue
                    
                    # Pull content
                    content = step.get("content", "")
                    
                    # Pull from tool calls if any
                    for tc in step.get("tool_calls", []):
                        args = tc.get("args", {})
                        if isinstance(args, dict):
                            content += "\n" + str(args.get("CodeContent", "")) + "\n" + str(args.get("ReplacementContent", ""))
                            # Also check replacement chunks
                            for chunk in args.get("ReplacementChunks", []):
                                if isinstance(chunk, dict):
                                    content += "\n" + str(chunk.get("ReplacementContent", ""))
                    
                    # Find python code blocks
                    code_blocks = re.findall(r"```python(.*?)```", content, re.S)
                    if code_blocks:
                        for idx, cb in enumerate(code_blocks):
                            if func in cb:
                                out_fn = output_dir / f"{folder.name}_step_{step.get('step_index')}_{func}_{idx}.py"
                                with open(out_fn, "w", encoding="utf-8") as out:
                                    out.write(cb.strip())
                                print(f"-> Extracted Python block for {func} from {folder.name} step {step.get('step_index')} to {out_fn.name} ({len(cb)} chars)")
                    else:
                        out_fn = output_dir / f"{folder.name}_step_{step.get('step_index')}_{func}_raw.txt"
                        with open(out_fn, "w", encoding="utf-8") as out:
                            out.write(content)
                        print(f"-> Saved raw match for {func} from {folder.name} step {step.get('step_index')} to {out_fn.name} ({len(content)} chars)")
