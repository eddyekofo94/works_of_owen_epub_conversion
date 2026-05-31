#!/bin/bash
# Double-click to rebuild Volume 10 and verify all recent fixes.
cd "$(dirname "$0")"
echo "=== Rebuilding Volume 10 ==="
echo ""
cd volumes/v10
python3 convert.py
STATUS=$?
cd ../..
if [ $STATUS -ne 0 ]; then
    echo "Build FAILED (exit $STATUS)"
    read -p "Press Enter to close..."
    exit $STATUS
fi
echo ""
echo "=== Verifying fixes in rendered EPUB ==="
python3 - <<'PY'
import zipfile, re, sys

ok = True

with zipfile.ZipFile("volumes/v10/output/volume_10.epub") as zf:
    xhtml = {n: zf.read(n).decode("utf-8") for n in zf.namelist() if n.endswith(".xhtml")}

def text_of(html):
    return re.sub(r'<[^>]+>', '', html)

# Fix 1: Chapter 4 end (ch008) -- blockquote/plain pairs from pipe table
tail = xhtml.get("EPUB/ch008.xhtml", "")[-3000:]
if "Secondly" in tail and "[[BLOCKQUOTE]]" not in tail:
    print("OK  Fix 1: ch008 table rendered as blockquote/plain pairs")
else:
    print("FAIL Fix 1: ch008 table not rendered correctly")
    ok = False

# Fix 2: Fused word ordinals split (ch007 had "certainty...Secondly" fused)
ch007_text = text_of(xhtml.get("EPUB/ch007.xhtml", ""))
if re.search(r'certainty[^\n]{1,60}Secondly', ch007_text):
    print("FAIL Fix 2: fused 'Secondly' still present in ch007 text")
    ok = False
else:
    print("OK  Fix 2: fused word ordinals split correctly")

# Fix 3: Stray ** in ch048 removed (no double-space before scripture refs)
ch048_text = text_of(xhtml.get("EPUB/ch048.xhtml", ""))
if "enemies,  Luke" in ch048_text or "propitiation,  Romans" in ch048_text:
    print("FAIL Fix 3: stray ** double-space still present in ch048")
    ok = False
else:
    print("OK  Fix 3: stray ** markers cleaned in ch048")

# Fix 4: Footnote [f1] not raw-text in ch003 heading
if "[f1]" in xhtml.get("EPUB/ch003.xhtml", ""):
    print("FAIL Fix 4: raw [f1] still in ch003 heading")
    ok = False
else:
    print("OK  Fix 4: no raw [fN] in ch003 heading")

# Fix 5: APRI -> APRIL in ch059
ch059_text = text_of(xhtml.get("EPUB/ch059.xhtml", ""))
if ch059_text and re.search(r'\bAPRI\b', ch059_text):
    print("FAIL Fix 5: 'APRI' not corrected to 'APRIL' in ch059")
    ok = False
else:
    print("OK  Fix 5: APRI/APRIL check passed")

# Bonus: count chapters with fused word ordinals remaining
from sys import path as syspath
syspath.insert(0, '.')
try:
    import json
    data = json.load(open("volumes/v10/intermediate/volume_10.json"))
    split_re = re.compile(
        r'(?<=[.!?]) +(?=(?:Firstly|Secondly|Thirdly|Fourthly|Fifthly|'
        r'Sixthly|Seventhly|Eighthly|Ninthly|Lastly)[,. ])'
    )
    fused_count = 0
    for ch in data["chapters"]:
        for para in ch.get("raw_text", "").split("\n\n"):
            if not para.lstrip().startswith("[[") and split_re.search(para):
                fused_count += 1
    print(f"\nFused word ordinals remaining in JSON source: {fused_count} paragraphs")
    print("(These are split at render time by _repair_fused_word_ordinals)")
except Exception as e:
    print(f"(Could not count fused ordinals: {e})")

print()
if ok:
    print("All checks passed.")
else:
    print("Some checks FAILED -- see above.")
    sys.exit(1)
PY

echo ""
echo "Done."
read -p "Press Enter to close..."
