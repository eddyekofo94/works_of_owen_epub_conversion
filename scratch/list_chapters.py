import json

with open('volumes/v16/intermediate/volume_16.json') as f:
    data = json.load(f)

for idx, ch in enumerate(data.get('chapters', [])):
    print(f"[{idx}] {ch.get('title', '')} (page {ch.get('page_num', '?')})")
