import json
import re

with open('volumes/v16/intermediate/volume_16.json') as f:
    data = json.load(f)

for ch in data['chapters']:
    text = ch.get('raw_text', '')
    
    # Check for missing words
    for word in ['pre', 'eminence', 'sixteen', 'seventeen']:
        if re.search(r'.{0,30}' + word + r'.{0,30}', text, re.IGNORECASE):
            print(f"Found {word} in {ch['title']}: {re.search(r'.{0,30}' + word + r'.{0,30}', text, re.IGNORECASE).group(0)}")
            
