import json
from pathlib import Path

transcript_path = Path("/Users/eddyekofo/.gemini/antigravity/brain/6b2d2bef-b94b-4dca-a8fc-22bed9bc0586/.system_generated/logs/transcript.jsonl")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        step = json.loads(line)
        if step.get("step_index") == 22:
            print(f"Type: {step.get('type')}")
            print(f"Source: {step.get('source')}")
            print(f"Tool calls:")
            for tc in step.get("tool_calls", []):
                print(f"  Name: {tc.get('name')}")
                print(f"  Args keys: {list(tc.get('args', {}).keys())}")
                print(f"  TargetFile: {tc.get('args', {}).get('TargetFile')}")
