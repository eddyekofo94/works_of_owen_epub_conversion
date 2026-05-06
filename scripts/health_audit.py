import re
import os

def audit_volume(vol_num):
    thml_path = f'books/Owen/reference/epubs_intermediates/volume_{vol_num}.thml.xml'
    if not os.path.exists(thml_path):
        return None
    
    with open(thml_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find list introductions: any paragraph ending in a colon or dash-colon
    # and containing keywords for lists.
    intro_regex = r'<p[^>]*>[^<]*?(?:heads|ways|parts|reasons|following|ensuing|reduce|distribute).*?[:—]\s*<\/p>'
    
    matches = re.finditer(intro_regex, content, re.IGNORECASE)
    issues = []
    for m in matches:
        start_idx = m.end()
        # Look at next 1000 chars
        next_chunk = content[start_idx:start_idx+1500]
        # Skip if we see a list marker like I. II. III. IV. or 1. 2. 3. 4.
        # But wait, sometimes they are inside <div1> headers now.
        # Let's check for the *expanded* sections too.
        
        # If the NEXT chunk doesn't contain a list marker AND doesn't start with a <div1 title="I."
        # then it might be an omission.
        
        has_list = re.search(r'<b>\s*(?:[IVXLCDM]+|[1-9]\d*)\.?\s*<\/b>', next_chunk)
        has_div1_i = re.search(r'<div1[^>]*title="I\."', next_chunk)
        
        if not has_list and not has_div1_i:
             issues.append({
                'line': content[:m.start()].count('\n') + 1,
                'text': m.group(0).strip()
            })
                
    return issues

if __name__ == "__main__":
    for i in range(1, 2):
        print(f"Auditing Volume {i}...")
        issues = audit_volume(i)
        if issues:
            for issue in issues:
                print(f"  [POTENTIAL OMISSION] Line {issue['line']}: {issue['text']}")
        else:
            print("  No issues found.")
