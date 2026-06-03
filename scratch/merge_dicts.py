import sys

all_dicts = {}
for i in range(5):
    try:
        # We need to import the chunk dictionary safely
        # since it's just a file with CHUNK_DICT = {...}
        local_vars = {}
        with open(f"scratch/chunk_{i}_dict.py", "r") as f:
            code = f.read()
        exec(code, {}, local_vars)
        
        # Check for CHUNK_DICT or just any dict
        chunk_dict = local_vars.get('CHUNK_DICT')
        if not chunk_dict:
            for v in local_vars.values():
                if isinstance(v, dict):
                    chunk_dict = v
                    break
                    
        if chunk_dict:
            all_dicts.update(chunk_dict)
            print(f"Loaded {len(chunk_dict)} items from chunk {i}")
        else:
            print(f"Warning: No dictionary found in chunk {i}")
            
    except Exception as e:
        print(f"Error loading chunk {i}: {e}")

print(f"Total unique items to insert: {len(all_dicts)}")

# Now read translation_db.py
with open("translation_db.py", "r") as f:
    lines = f.readlines()

# Find BODY_TRANSLATIONS = {
insert_idx = -1
for i, line in enumerate(lines):
    if line.strip() == "BODY_TRANSLATIONS = {":
        insert_idx = i + 1
        break

if insert_idx == -1:
    print("Could not find BODY_TRANSLATIONS = { in translation_db.py")
    sys.exit(1)

# Format the items
formatted_lines = []
for k, v in all_dicts.items():
    # properly escape quotes
    # Using triple quotes for both to avoid escaping hell
    k_escaped = repr(k)
    v_escaped = repr(v)
    formatted_lines.append(f"    {k_escaped}: (\n        {v_escaped}\n    ),\n")

# Insert the items
lines = lines[:insert_idx] + formatted_lines + lines[insert_idx:]

with open("translation_db.py", "w") as f:
    f.writelines(lines)

print("Successfully injected into translation_db.py")
