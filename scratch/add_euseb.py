import json

path = 'translation_db.py'
with open(path, 'r') as f:
    content = f.read()

target = 'BODY_TRANSLATIONS = {\n'
replacement = target + '''    "Euseb. Preparat. Evang., lib. 1 cap. 3:": (
        "<b>Modern Citation:</b> Eusebius of Caesarea, <i>Preparation for the Gospel</i>, book 1, chapter 3."
    ),
'''

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(content)
