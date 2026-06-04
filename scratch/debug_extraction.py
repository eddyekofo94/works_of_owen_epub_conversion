import fitz, pymupdf4llm
import re
from shared import SCRIPTURE_BOOK_RE, STRUCTURAL_START_RE

# Copy-paste reconstruct_paragraphs but add print debug
def debug_reconstruct(text):
    lines = text.split('\n')
    paragraphs = []
    current = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if current:
                prev = current[-1]
                ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
                if ends_terminal:
                    paragraphs.append(' '.join(current))
                    current = []
            continue
        
        if STRUCTURAL_START_RE.match(stripped):
            if current:
                prev = current[-1]
                ends_terminal = bool(re.search(r'[.!?]"?\s*$', prev))
                if not ends_terminal:
                    print(f"DEBUG: joining structural [{stripped[:20]}] to current because prev [{prev[-20:]}] is not terminal")
                    current.append(stripped)
                    continue
                paragraphs.append(' '.join(current))
            current = [stripped]
            continue
        current.append(stripped)
    if current:
        paragraphs.append(' '.join(current))
    return paragraphs

doc = fitz.open("pdfs/owen-v2.pdf")
pages_md = pymupdf4llm.to_markdown(doc, page_chunks=True)
raw154 = "... we ask amiss."
raw155 = "Two things are required, that we may pray for the things in the promise,\nas they are in the promise: —\n\n(1st.) That we look upon them as promised, ... and Christ as the procurer of them."

from extract import clean_text
joined = raw154 + "\n\n" + raw155
cleaned = clean_text(joined)
print("--- CLEANED ---")
print(cleaned)

healed = debug_reconstruct(cleaned)
print("\n--- HEALED ---")
for p in healed:
    print(f"[{p}]")
