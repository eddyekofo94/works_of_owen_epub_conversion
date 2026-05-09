import fitz
import re

pdf_path = 'volumes/v1/input/owen-v1.pdf'
doc = fitz.open(pdf_path)

for p_num in [20, 22]:
    page = doc[p_num - 1]
    text = page.get_text()
    print(f"--- Page {p_num} ---")
    print(text[:300] + "...")
    
    blocks = page.get_text('dict')['blocks']
    text_blocks = [b for b in blocks if b.get('type') == 0]
    
    total_chars = 0
    large_chars = 0
    for b in text_blocks:
        for line in b['lines']:
            for s in line['spans']:
                c = len(s['text'])
                total_chars += c
                if s['size'] > 14:
                    large_chars += c
                    
    print(f"Total chars: {total_chars}")
    print(f"Large chars (>14): {large_chars}")
    
    # Check first few blocks
    for i, b in enumerate(text_blocks[:3]):
        b_max = 0
        b_text = ""
        for line in b['lines']:
            for s in line['spans']:
                b_max = max(b_max, s['size'])
                b_text += s['text']
        print(f"Block {i} max font: {b_max:.2f}, text snippet: {b_text.strip()[:50]!r}")

doc.close()
