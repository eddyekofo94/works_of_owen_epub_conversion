import json
import re
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")
output_dir = Path("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/recovered")
output_dir.mkdir(parents=True, exist_ok=True)

functions_to_find = [
    "def _repair_fused_word_ordinals",
    "def _repair_markdown_tables",
    "def _attach_em_dash_flat_list"
]

print("Scanning all past conversation transcripts for function definitions...")

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    print(f"Checking {folder.name}...")
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            # Fast check first before expensive JSON parsing
            has_any = any(func in line for func in functions_to_find)
            if not has_any:
                continue
                
            try:
                step = json.loads(line)
            except Exception:
                continue
            
            # Extract content fields
            content = step.get("content", "")
            
            # Extract from tool_calls
            tool_calls = step.get("tool_calls", [])
            for tc in tool_calls:
                args = tc.get("args", {})
                if isinstance(args, dict):
                    content += "\n" + str(args.get("CodeContent", "")) + "\n" + str(args.get("ReplacementContent", ""))
            
            for func in functions_to_find:
                if func in content:
                    # Find code block or full definition
                    # Let's extract the python code block if present
                    code_blocks = re.findall(r"```python(.*?)```", content, re.S)
                    if code_blocks:
                        for idx, cb in enumerate(code_blocks):
                            if func in cb:
                                out_fn = output_dir / f"{folder.name}_step_{step.get('step_index')}_{func.replace(' ', '_')}_{idx}.py"
                                with open(out_fn, "w", encoding="utf-8") as out:
                                    out.write(cb.strip())
                                print(f"  -> Extracted python block for {func} from {folder.name} step {step.get('step_index')} to {out_fn.name} ({len(cb)} chars)")
                    else:
                        # Otherwise write the raw content containing it
                        out_fn = output_dir / f"{folder.name}_step_{step.get('step_index')}_{func.replace(' ', '_')}_raw.py"
                        with open(out_fn, "w", encoding="utf-8") as out:
                            out.write(content)
                        print(f"  -> Saved raw payload containing {func} from {folder.name} step {step.get('step_index')} to {out_fn.name} ({len(content)} chars)")
