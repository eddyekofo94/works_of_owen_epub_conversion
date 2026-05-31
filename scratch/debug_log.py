import json
from pathlib import Path

brain_dir = Path("/Users/eddyekofo/.gemini/antigravity/brain")

for folder in brain_dir.iterdir():
    if not folder.is_dir() or folder.name.startswith("."):
        continue
    transcript_path = folder / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        continue
    
    print(f"\n--- Checking {folder.name} ---")
    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                step = json.loads(line)
            except Exception:
                continue
            
            tool_calls = step.get("tool_calls", [])
            if not tool_calls:
                continue
                
            for tc in tool_calls:
                name = tc.get("name", "")
                if name in ["replace_file_content", "write_to_file"]:
                    args = tc.get("args", {})
                    if isinstance(args, dict):
                        target = args.get("TargetFile", "")
                        print(f"Found {name} targeting: {target}")
                        content = args.get("CodeContent", "") or args.get("ReplacementContent", "")
                        print(f"  Content length: {len(content)} chars")
                        # Print first few lines of content
                        first_lines = "\n".join(content.splitlines()[:5])
                        print(f"  Snippet:\n{first_lines}")
