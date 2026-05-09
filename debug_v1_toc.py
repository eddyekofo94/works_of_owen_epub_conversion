import fitz
import sys, os

# Add current dir to path to import converter
sys.path.insert(0, os.getcwd())
from converter import detect_page_type, extract_ages_nav

pdf_path = 'volumes/v1/input/owen-v1.pdf'
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

# Check first 15 pages
for pg in range(15):
    page = doc[pg]
    ptype = detect_page_type(page, pg + 1)
    print(f"Page {pg+1}: {ptype}")

# Check navigation
nav = extract_ages_nav(doc)
print(f"\nFound {len(nav)} nav entries.")
for level, title, pg in nav[:10]:
    print(f"Level {level}: {title} (Page {pg+1})")

doc.close()
