import xml.etree.ElementTree as ET
import re
import os

def fix_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Case 1: Misplaced Ghost IV (ch019)
    # Identifiable by title="IV." id="ch019"
    content = re.sub(r'<div1 title="IV\." id="ch019">.*?<\/div1>', '', content, flags=re.DOTALL)

    # Case 2: Misplaced Ghost IV (ch033)
    # Identifiable by title="IV." id="ch033"
    content = re.sub(r'<div1 title="IV\." id="ch033">.*?<\/div1>', '', content, flags=re.DOTALL)

    # Case 3: Merge Preface Reasons (ch048-ch051) into Preface (ch047)
    # I will extract the content of ch048-ch051 and append to ch047
    
    def merge_sections(match):
        preface_body = match.group(1)
        reasons_block = match.group(2)
        
        # Extract the inner paragraphs from each div1 in reasons_block
        # and turn their <h2> titles into <b> tags or similar
        reasons = re.findall(r'<div1 title="(.*?)" id="ch0\d+">\s*<h2>.*?<\/h2>(.*?)<\/div1>', reasons_block, re.DOTALL)
        
        merged_content = preface_body
        for title, body in reasons:
            # Clean up the body (remove leading/trailing space)
            body = body.strip()
            # Wrap title in bold if it's a numeral
            merged_content += f'\n      <p class="Body">\n        <b>{title} </b>\n        {body}\n      </p>'
            
        return f'<div1 title="PREFACE TO THE READER." id="ch047">{merged_content}\n    </div1>'

    # Regex to find ch047 and the following ch048-ch051
    # This is tricky because they are siblings.
    # I'll use a more manual approach.
    
    reasons_content = ""
    for cid in ['ch048', 'ch049', 'ch050', 'ch051']:
        m = re.search(fr'<div1 title="(.*?)" id="{cid}">\s*<h2>.*?<\/h2>(.*?)<\/div1>', content, re.DOTALL)
        if m:
            title, body = m.groups()
            reasons_content += f'\n      <p class="Body">\n        <b>{title} </b>\n        {body.strip()}\n      </p>'
            # Remove the original div1
            content = content.replace(m.group(0), "")
            
    # Insert reasons into ch047
    content = re.sub(r'(<div1 title="PREFACE TO THE READER\." id="ch047">.*?)(<\/div1>)', fr'\1{reasons_content}\2', content, flags=re.DOTALL)

    # Case 4: Merge Chapter 2 Summary Heads (ch081-ch084) into Chapter 2 (ch080)
    summaries_content = ""
    for cid in ['ch081', 'ch082', 'ch083', 'ch084']:
        m = re.search(fr'<div1 title="(.*?)" id="{cid}">\s*<h2>.*?<\/h2>(.*?)<\/div1>', content, re.DOTALL)
        if m:
            title, body = m.groups()
            summaries_content += f'\n      <p class="Body">\n        <b>{title} </b>\n        {body.strip()}\n      </p>'
            content = content.replace(m.group(0), "")
            
    content = re.sub(r'(<div1 title="CHAPTER 2\." id="ch080">.*?)(<\/div1>)', fr'\1{summaries_content}\2', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_structure("books/Owen/volumes/v1/intermediate/volume_1.thml.xml")
