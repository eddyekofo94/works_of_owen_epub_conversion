import fitz
import sys
from extract import _extract_text_with_fonts_and_colors

doc = fitz.open('volumes/v8/input/volume_8.pdf')
# Let's find the page where Sermon I starts.
for i in range(15, 30):
    page = doc[i]
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if b.get('type') == 0:
            for l in b['lines']:
                for s in l['spans']:
                    text = s['text'].strip()
                    if 'SERMON' in text:
                        print(f"Page {i+1}: '{text}', color={s['color']}, size={s['size']}")
