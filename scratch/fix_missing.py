import re

with open("scratch/chunk_1.txt", "r") as f:
    text = f.read()

def find_substring(prefix):
    lines = text.split('\n')
    for line in lines:
        if prefix in line:
            return line[line.find(prefix):]
    return None

missing_prefixes = [
    "Philadelphians [cap. 2]:",
    "[cap.4]: Θαῤῥῶν",
    "[cap. 10]: Πρέπον",
    "[cap. 5]: Εἰ γὰρ",
    "[cap. 13]: Σπουδάζετε",
    "Tertullian in his Algol",
    "Sozomen tells you expressly that he did so"
]

translations = [
    "Ignatius, <i>Epistula ad Philadelphenses</i>, 2:",
    "Ignatius, <i>Epistula ad Philadelphenses</i>, 8:",
    "Ignatius, <i>Epistula ad Philadelphenses</i>, 10:",
    "Ignatius, <i>Epistula ad Ephesios</i>, 5:",
    "Ignatius, <i>Epistula ad Ephesios</i>, 13:",
    "Tertullian, <i>Apologeticus</i>, and <i>Ad Uxorem</i> 2, and <i>De Cultu Feminarum</i>;",
    "Sozomen, <i>Historia Ecclesiastica</i>, 4.15;"
]

with open("scratch/chunk_1_dict.py", "a") as out:
    for prefix, trans in zip(missing_prefixes, translations):
        match = find_substring(prefix)
        if match:
            # We want to match up to the end of the greek text or relevant citation part
            # For the greek ones, let's take the whole matching substring if it's short, or up to 50 chars
            print(f"Found: {repr(match)}")
            out.write(f'    {repr(match)}: {repr("<b>Modern Citation:</b> " + trans)},\n')
        else:
            print(f"Still not found: {prefix}")
            
print("Done appending.")
