import re
import os
import subprocess

def get_pdf_chunk(page_start, page_end):
    cmd = ['pdftotext', '-f', str(page_start), '-l', str(page_end), 'books/Owen/pdfs/owen-v1.pdf', '-']
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout

def find_missing_lines(intro_text, pdf_text):
    # Try to find the intro_text in pdf_text (ignoring line breaks)
    # Owen's text in ThML might have slight diffs from PDF (OCR errors)
    # So we'll look for a fuzzy match of the last 20 chars
    search_anchor = intro_text.strip()[-30:].rstrip(':— ')
    
    # Escape for regex
    search_anchor = re.escape(search_anchor)
    
    match = re.search(search_anchor, pdf_text)
    if not match:
        return "COULD NOT LOCATE IN PDF"
    
    # Get the text following the match
    following = pdf_text[match.end():].strip()
    
    # We want the lines until the next "major" paragraph or a few hundred chars
    # Usually Owen's lists are short lines.
    lines = following.split('\n')
    extracted = []
    for line in lines[:15]: # Take first 15 lines max
        line = line.strip()
        if not line: continue
        # If we hit a very long line that looks like the start of the next section, stop?
        # Actually, let's just take the first 5 non-empty lines that look like list items
        extracted.append(line)
        if len(extracted) >= 6: break
        
    return "\n".join(extracted)

def heal_volume(vol_num):
    thml_path = f'books/Owen/reference/epubs_intermediates/volume_{vol_num}.thml.xml'
    output_path = f'books/Owen/volumes/v{vol_num}/intermediate/volume_{vol_num}.thml.xml'
    
    with open(thml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    intro_regex = r'<p[^>]*>([^<]*?(?:heads|ways|parts|reasons|following|ensuing|reduce|distribute).*?[:—])\s*<\/p>'
    
    # We need to iterate and replace. 
    # To keep it safe, I'll just print the findings for now and we can decide.
    
    matches = list(re.finditer(intro_regex, content, re.IGNORECASE))
    print(f"Found {len(matches)} potential list intros.")
    
    # For Volume 1, I'll try to heal the first few.
    # Page estimation: (line_number / total_lines) * total_pages
    # Volume 1 has ~500 content pages. Total lines ~8000.
    
    for m in matches:
        line_num = content[:m.start()].count('\n') + 1
        intro_text = m.group(1)
        
        # Look ahead to see if already present
        next_chunk = content[m.end():m.end()+1500]
        if re.search(r'<b>\s*(?:[IVXLCDM]+|[1-9]\d*)\.?\s*<\/b>', next_chunk) or re.search(r'<div1[^>]*title="I\."', next_chunk):
            continue
            
        print(f"\n[OMISSION] Line {line_num}: {intro_text}")
        
        # Estimate page
        est_page = int((line_num / 8000) * 500) + 10 # Offset for front matter
        pdf_chunk = get_pdf_chunk(max(1, est_page - 20), min(500, est_page + 20))
        
        missing = find_missing_lines(intro_text, pdf_chunk)
        print(f"Extracted from PDF:\n{missing}")

if __name__ == "__main__":
    heal_volume(1)
