import sys
sys.path.insert(0, '.')
from render import render_volume
import render
from volumes.v1.convert import OVERRIDES

orig_merge = render._merge_titlepage_override
def mock_merge(override, frags):
    # we don't know the title here easily without inspecting globals,
    # but we can just let it print
    return orig_merge(override, frags)

render._merge_titlepage_override = mock_merge

print("Running...")
render_volume(1, overrides=OVERRIDES)
