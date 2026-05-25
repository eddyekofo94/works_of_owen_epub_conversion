import re
from extract import clean_text, reconstruct_paragraphs

page154 = """154
... we ask amiss."""

page155 = """155


Two things are required, that we may pray for the things in the promise,
as they are in the promise: —


**(1st.)** That we look upon them as promised, and promised in Christ; that
"""

def extract_page_markdown_mock(text):
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if any(h in stripped for h in ['THE AGES DIGITAL LIBRARY', 'JOHN OWEN COLLECTION']):
            continue
        if stripped.isdigit() and len(stripped) <= 4:
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

raw_154 = extract_page_markdown_mock(page154)
raw_155 = extract_page_markdown_mock(page155)

joined = raw_154 + "\n" + raw_155
print("--- JOINED RAW ---")
print(joined)

cleaned = clean_text(joined)
print("\n--- CLEANED ---")
print(cleaned)

healed = reconstruct_paragraphs(cleaned)
print("\n--- HEALED ---")
for p in healed:
    print(f"[{p}]")
