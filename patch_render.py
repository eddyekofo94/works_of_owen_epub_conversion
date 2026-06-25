import re

with open("render.py", "r") as f:
    content = f.read()

# I need to add the len(body_text) > 2000 check back.
old_str = """        if titlepage_override:
            title_block, body_text = _split_raw_title_body(raw_text)
            foreign_frags = _foreign_fragments_in_section(title_block or raw_text)
            overridden_title = _merge_titlepage_override(titlepage_override, foreign_frags)
            if body_text:
                raw_text = f"{overridden_title}\\n\\n{body_text}"
            else:
                raw_text = overridden_title"""

new_str = """        if titlepage_override:
            title_block, body_text = _split_raw_title_body(raw_text)
            foreign_frags = _foreign_fragments_in_section(title_block or raw_text)
            overridden_title = _merge_titlepage_override(titlepage_override, foreign_frags)
            if body_text and len(body_text) > 2000:
                raw_text = f"{overridden_title}\\n\\n{body_text}"
            else:
                raw_text = overridden_title"""

if old_str in content:
    content = content.replace(old_str, new_str)
    with open("render.py", "w") as f:
        f.write(content)
    print("Patched render.py successfully!")
else:
    print("Could not find old string.")
