import fitz, os, sys, re
from collections import Counter
sys.path.insert(0, os.getcwd())

def normalize_comp(text):
    return re.sub(r'\W+', '', text).lower()

doc = fitz.open('volumes/v1/input/owen-v1.pdf')
page = doc[38] # Page 39
blocks = [b for b in page.get_text("dict")["blocks"] if b.get("type") == 0 and b.get("lines")]

verse_texts = []
for b in blocks:
    if len(b["lines"]) <= 1: continue
    
    # Check if all lines are centered and short
    is_verse = True
    for l in b["lines"]:
        center = (l["bbox"][0] + l["bbox"][2]) / 2
        width = l["bbox"][2] - l["bbox"][0]
        if abs(center - 205) > 15 or width > 310:
            is_verse = False
            break
            
    if is_verse:
        text = "\n".join([" ".join(s["text"] for s in l["spans"]) for l in b["lines"]])
        verse_texts.append(text)
        print(f"Found Verse Block: {repr(text[:50])}...")

# Test match against Markdown
import pymupdf4llm
pages_md = pymupdf4llm.to_markdown('volumes/v1/input/owen-v1.pdf', pages=[38], page_chunks=True, show_progress=False)
md_text = pages_md[0]['text']
paragraphs = md_text.split('\n\n')

for p in paragraphs:
    p_norm = normalize_comp(p)
    for v in verse_texts:
        v_norm = normalize_comp(v)
        if v_norm == p_norm:
            print(f"MATCHED: {repr(p[:30])}")
        elif v_norm in p_norm:
            print(f"SUB-MATCH: {repr(p[:30])}")

doc.close()
