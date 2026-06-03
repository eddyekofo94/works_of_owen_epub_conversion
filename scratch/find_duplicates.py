import json
import re

with open('volumes/v16/intermediate/volume_16.json') as f:
    data = json.load(f)

# Collect paragraphs
paragraphs = []
for ch_idx, ch in enumerate(data.get('chapters', [])):
    text = ch.get('raw_text', '')
    for p in text.split('\n\n'):
        p = p.strip()
        if len(p.split()) > 40:
            paragraphs.append({'ch': ch_idx, 'title': ch.get('title', ''), 'text': p})

seen = {}
duplicates = []
for p in paragraphs:
    norm_text = re.sub(r'\s+', ' ', p['text'].lower())
    if norm_text in seen:
        duplicates.append((seen[norm_text], p))
    else:
        seen[norm_text] = p

print(f"Found {len(duplicates)} exact duplicate paragraphs (>40 words).")
for d1, d2 in duplicates:
    print(f"DUPLICATE:")
    print(f" 1. Chapter '{d1['title']}'")
    print(f" 2. Chapter '{d2['title']}'")
    print(f" Text: {d1['text'][:100]}...")
