import fitz
import re

pdf_path = 'volumes/v1/input/owen-v1.pdf'
doc = fitz.open(pdf_path)

for p_num in [3, 4, 5]:
    page = doc[p_num - 1]
    text = page.get_text()
    print(f"--- Page {p_num} ---")
    print(text[:200] + "...")
    
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if b.get('type') == 0]
    
    # Check for dot leaders or numbers at start of lines
    dot_count = text.count('....')
    print(f"Dot patterns: {dot_count}")
    
    # Check first few items
    items_count = 0
    for b in text_blocks:
        b_text = "".join(s['text'] for line in b['lines'] for s in line['spans']).strip()
        if re.match(r'^(CHAPTER\s+\d+|[IVXLC]+|\d+\.)', b_text, re.I):
            items_count += 1
    print(f"TOC-like items: {items_count}")

doc.close()
