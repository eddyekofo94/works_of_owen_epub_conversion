import json
import glob
import re

typos = {}

for file in glob.glob('volumes/*/intermediate/volume_*.json'):
    with open(file, 'r') as f:
        data = json.load(f)
        
    for ch in data.get('chapters', []) + data.get('front_matter_items', []):
        text = ch.get('raw_text', '')
        # Find words that contain letters and numbers mixed together, but ignore pure numbers
        # e.g. Athanasiu6, l1ght, etc.
        # But we must avoid actual citations like 1st, 2nd, 3rd, 1John, etc.
        matches = re.finditer(r'\b([a-zA-Z]+[0-9]+[a-zA-Z]*|[0-9]+[a-zA-Z]+)\b', text)
        for m in matches:
            word = m.group(1)
            # Filter out valid ordinals and common biblical patterns
            lower_word = word.lower()
            if re.match(r'^\d+(st|nd|rd|th)$', lower_word): continue
            if lower_word in ['1john', '2john', '3john', '1peter', '2peter', '1samuel', '2samuel', '1kings', '2kings', '1chronicles', '2chronicles', '1corinthians', '2corinthians', '1thessalonians', '2thessalonians', '1timothy', '2timothy']: continue
            
            # Common OCR error: a single letter followed by number (e.g. v1, p2, though those might be valid in notes)
            # Let's collect them
            if word not in typos:
                typos[word] = 0
            typos[word] += 1

# Sort by frequency
sorted_typos = sorted(typos.items(), key=lambda x: x[1], reverse=True)

with open('scratch/ocr_typos_report.txt', 'w') as f:
    for word, count in sorted_typos:
        f.write(f"{word}: {count}\n")
