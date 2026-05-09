import fitz
import re

pdf_path = 'pdfs/owen-v1.pdf'
doc = fitz.open(pdf_path)
page_num = 534 - 1 # 0-indexed
page = doc[page_num]

text_upper = page.get_text().upper()
blocks = page.get_text('dict')['blocks']
text_blocks = [b for b in blocks if b.get('type') == 0]
n_blocks = len(text_blocks)

total_chars = 0
large_chars = 0
for b in text_blocks:
    for line in b['lines']:
        for s in line['spans']:
            c = len(s['text'])
            total_chars += c
            if s['size'] > 14:
                large_chars += c

print(f"Page {page_num + 1}:")
print(f"Total blocks: {len(blocks)}")
print(f"Text blocks: {n_blocks}")
print(f"Total chars: {total_chars}")
print(f"Large chars (>14): {large_chars}")

for b in text_blocks:
    b_max = 0
    b_text = ""
    for line in b['lines']:
        for s in line['spans']:
            b_max = max(b_max, s['size'])
            b_text += s['text']
    print(f"Block max font: {b_max:.2f}, text snippet: {b_text[:50]!r}")

doc.close()
