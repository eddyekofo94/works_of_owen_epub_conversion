import json

with open('qa/bug_regression_baselines.json', 'r') as f:
    data = json.load(f)

# Override volume 16 with my new strict numbers
data["volumes"]["16"] = {
  "text_integrity": {
    "max_split_candidate_count": 28,
    "max_inline_structural_candidate_count": 8
  },
  "epub": {
    "max_lowercase_paragraph_start_files": 1
  }
}

with open('qa/bug_regression_baselines.json', 'w') as f:
    json.dump(data, f, indent=2)
