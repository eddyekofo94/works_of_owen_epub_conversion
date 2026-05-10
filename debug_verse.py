import fitz, os, sys
from collections import Counter
sys.path.insert(0, os.getcwd())

doc = fitz.open('volumes/v1/input/owen-v1.pdf')
page = doc[38] # Page 39
blocks = [b for b in page.get_text("dict")["blocks"] if b.get("type") == 0 and b.get("lines")]

for i, b in enumerate(blocks):
    # Calculate centering of each line
    centered_lines = 0
    for l in b["lines"]:
        center = (l["bbox"][0] + l["bbox"][2]) / 2
        if abs(center - 205) < 15:
            centered_lines += 1
    
    is_verse = centered_lines > 1 and centered_lines >= len(b["lines"]) * 0.8
    color = b["lines"][0]["spans"][0]["color"]
    text = " ".join(s["text"] for s in b["lines"][0]["spans"])
    
    print(f"Block {i}: Verse={is_verse}, Color={color}, Text={repr(text[:40])}")

doc.close()
