import json
import glob
import re

citation_keywords = [
    r'\bOrat\.',
    r'\bEpist\.',
    r'\bLib\.',
    r'\bcap\.',
    r'\bIbid\.',
    r'\bApol\.',
    r'\bAdvers\.',
    r'\bHomil\.',
    r'\bTract\.'
]

pattern = re.compile('(' + '|'.join(citation_keywords) + ')')

# Find all citations and extract the sentence or full clause.
# A clause can be bounded by sentences, colons, or parentheses.
split_pattern = re.compile(r'([.?!:]\s|\[\[BLOCKQUOTE\]\]|\(|\))')

results = set()

for file in glob.glob('volumes/*/intermediate/volume_*.json'):
    with open(file, 'r') as f:
        data = json.load(f)
        
    for ch in data.get('chapters', []) + data.get('front_matter_items', []):
        text = ch.get('raw_text', '')
        
        # We split the text into chunks by common delimiters
        # To avoid splitting inside citations like "lib. 1. cap. 2", we can just extract the whole text and use a smarter regex
        
        # Find matches and expand them to sensible boundaries
        for m in pattern.finditer(text):
            # heuristic: expand backwards to the nearest sentence boundary, capital letter after space, or blockquote
            start = m.start()
            while start > 0 and text[start-1] not in ['\n', ';', ':', '(', ')']:
                # if we hit ". " where the previous word is not an abbreviation
                if start > 2 and text[start-2:start] == '. ' and text[start-3].islower():
                    break
                if text[start-2:start] == '] ':
                    break
                start -= 1
                
            # expand forwards
            end = m.end()
            while end < len(text) and text[end] not in ['\n', ';', '(', ')']:
                if end < len(text) - 1 and text[end:end+2] == '. ' and text[end-1] != '.':
                    break
                end += 1
                
            snippet = text[start:end].strip()
            
            if '[[FOOTNOTE]]' in snippet or '[f' in snippet:
                continue
                
            # Clean up snippet
            snippet = snippet.strip(',.:;() \n')
            if snippet:
                results.add(snippet)

with open('scratch/unique_full_citations.txt', 'w') as f:
    for r in sorted(results):
        f.write(r + '\n')

print(f"Found {len(results)} unique citations.")
