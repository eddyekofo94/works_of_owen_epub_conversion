import json
with open("volumes/v8/intermediate/volume_8.json") as f:
    text = json.dumps(json.load(f))
import re
for m in re.finditer(r".{0,40}SERMON 13.{0,40}", text):
    print("MATCH:", repr(m.group(0)))

