import xml.etree.ElementTree as ET
import re

def extract_subtitle(div1):
    subtitle_parts = []
    # Look for the first few <p> tags, extract <b> text
    for p in div1.findall('p')[:5]:
        for b in p.findall('b'):
            if b.text and b.text.strip():
                # Avoid single letters or numbers maybe?
                subtitle_parts.append(b.text.strip())
        if subtitle_parts and not p.findall('b'): # If we found some but this p doesn't have any, maybe we reached the end of the subtitle block
            break
    
    if subtitle_parts:
        subtitle = " ".join(subtitle_parts)
        # title case it
        return subtitle.title()
    return ""

tree = ET.parse('books/Owen/volumes/v1/intermediate/volume_1.thml.xml')
root = tree.getroot()

div1s = root.findall('.//div1')
for div1 in div1s[:20]:
    title = div1.get('title')
    subtitle = extract_subtitle(div1)
    if title:
        print(f"Title: {title}")
        print(f"Subtitle: {subtitle}\n")
