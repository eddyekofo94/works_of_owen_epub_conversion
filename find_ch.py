import json
data = json.load(open("volumes/v2/intermediate/volume_2.json"))
for i, ch in enumerate(data["chapters"]):
    if "forgave them" in ch["raw_text"]:
        print(f"CH {i}: {ch['cid']}, {ch['title']}")
