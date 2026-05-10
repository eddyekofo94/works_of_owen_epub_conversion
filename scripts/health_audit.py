import fitz, os, sys, re
from collections import Counter
import difflib

def normalize_text(text):
    # Remove whitespace, punctuation, and scripture codes
    text = re.sub(r'<\d+>', '', text)
    text = re.sub(r'\W+', '', text).lower()
    return text

def audit_volume(vol_num):
    from converter import VOLUME_CONFIG, get_merged_page_text, extract_page_markdown
    import pymupdf4llm
    
    config = VOLUME_CONFIG.get(vol_num)
    pdf_path = f'volumes/v{vol_num}/input/owen-v{vol_num}.pdf'
    doc = fitz.open(pdf_path)
    
    print(f"Auditing Volume {vol_num}: {config['title']}")
    pages_md = pymupdf4llm.to_markdown(pdf_path, page_chunks=True, show_progress=False)
    
    issues = []
    
    for pg_idx in range(len(doc)):
        # Method 1: Our current extraction
        extracted = get_merged_page_text(doc, pages_md, pg_idx)
        # Method 2: Raw PyMuPDF text (often messy but contains everything)
        raw = doc[pg_idx].get_text("text")
        # Method 3: Markdown skeleton
        md = extract_page_markdown(pages_md, pg_idx)
        
        n_ext = normalize_text(extracted)
        n_raw = normalize_text(raw)
        n_md = normalize_text(md)
        
        # Check for duplication: if extracted is significantly longer than MD
        if len(n_ext) > 1.2 * len(n_md) and len(n_md) > 100:
            issues.append((pg_idx + 1, "POTENTIAL DUPLICATION", f"Extracted ({len(n_ext)}) >> Markdown ({len(n_md)})"))
            
        # Check for loss: if extracted is significantly shorter than MD
        elif len(n_ext) < 0.8 * len(n_md) and len(n_md) > 100:
            issues.append((pg_idx + 1, "POTENTIAL LOSS", f"Extracted ({len(n_ext)}) << Markdown ({len(n_md)})"))

        # Local duplication check (internal sequence repetition)
        words = extracted.split()
        if len(words) > 40:
            for i in range(len(words) - 20):
                chunk = words[i:i+10]
                rest = words[i+10:i+30]
                if any(chunk == words[j:j+10] for j in range(i+10, len(words)-10)):
                    issues.append((pg_idx + 1, "SEQUENCE REPETITION", f"Phrase {repr(' '.join(chunk))} repeated"))
                    break

    if issues:
        print(f"\nFound {len(issues)} potential integrity issues:")
        for pg, type, detail in issues:
            print(f"  [Page {pg:3d}] {type:20s}: {detail}")
    else:
        print("\nNo major integrity issues found! Textual integrity is high.")
    
    doc.close()

if __name__ == "__main__":
    vol = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    # Add project root to path
    sys.path.insert(0, os.getcwd())
    audit_volume(vol)
