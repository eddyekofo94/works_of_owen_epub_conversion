import json
data = json.load(open("volumes/v2/intermediate/volume_2.json"))
ch = [c for c in data["chapters"] if c["cid"] == "ch019"][0]
print(ch["raw_text"].count("2ndly"))
