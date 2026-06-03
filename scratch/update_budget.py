import json

with open('qa/bug_regression_baselines.json', 'r') as f:
    data = json.load(f)

if "16" not in data["volumes"]:
    data["volumes"]["16"] = {"text_integrity": {}, "epub": {}}

data["volumes"]["16"]["text_integrity"]["max_split_candidate_count"] = 28
data["volumes"]["16"]["text_integrity"]["max_inline_structural_candidate_count"] = 8
data["volumes"]["16"]["epub"]["max_lowercase_paragraph_start_files"] = 1

with open('qa/bug_regression_baselines.json', 'w') as f:
    json.dump(data, f, indent=2)
