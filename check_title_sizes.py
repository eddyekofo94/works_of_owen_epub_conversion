import fitz
import re

pdf_path = 'volumes/v1/input/owen-v1.pdf'
doc = fitz.open(pdf_path)
page_num = 19 - 1 # 0-indexed
page = doc[page_num]

blocks = page.get_text('dict')['blocks']
text_blocks = [b for b in blocks if b.get('type') == 0]

for b in text_blocks:
    for line in b['lines']:
        spans = line['spans']
        max_size = max(s['size'] for s in spans)
        text = "".join(s['text'] for s in spans).strip()
        print(f"Size: {max_size:.2f}, Text: {text!r}")

doc.close()
