def post_extract_hook(intermediate: dict) -> dict:
    chapters = intermediate.get('chapters', [])
    
    # Clean up Prefatory Note titles
    for ch in chapters:
        if ch['title'].startswith('Prefatory Note (Chapter 2'):
            ch['title'] = 'Prefatory Note'
            
    # Remove fragments and duplicates
    # We will identify them by exact titles since they are known artifacts of this volume
    drop_titles = {'II. and III.', 'An Answer Unto Two Questions.', 'Of Infant Baptism and Dipping.'}
    new_chapters = []
    
    for idx, ch in enumerate(chapters):
        t = ch.get('title', '')
        
        if t in drop_titles:
            continue
            
        if t == 'Answers and Questions':
            ch['title'] = 'An Answer Unto Two Questions.'
            ch['is_treatise'] = True
            
        if t == 'I.':
            # This contains the prefatory note for the Answers and Questions treatise
            ch['title'] = 'Prefatory Note'
            # Also drop the [[ROMAN_HEAD]] I. from the text
            ch['raw_text'] = ch['raw_text'].replace('[[ROMAN_HEAD]] I.\n\n', '')

        # Fix "Prefatory Note" chapter that has no text (it's split before I.)
        if t == 'Prefatory Note' and len(ch.get('raw_text', '')) < 50:
            continue
            
        new_chapters.append(ch)
        
    intermediate['chapters'] = new_chapters
    return intermediate

import json
with open('volumes/v16/intermediate/volume_16.json') as f:
    data = json.load(f)

data = post_extract_hook(data)
for idx, ch in enumerate(data['chapters']):
    if 18 <= idx <= 32:
        print(f"[{idx}] {ch['title']} ({len(ch.get('raw_text', ''))})")
