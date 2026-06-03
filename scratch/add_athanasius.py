import json

path = 'translation_db.py'
with open(path, 'r') as f:
    content = f.read()

target = 'BODY_TRANSLATIONS = {\n'
replacement = target + '''    "Orat. 5 con. Arian., and Epist. ad African.": (
        "<b>Modern Citation:</b> Athanasius of Alexandria, <i>Orations against the Arians</i>, 5; and <i>Epistle to the Bishops of Africa</i>."
    ),
'''

if target in content:
    content = content.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(content)
