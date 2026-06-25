import sys
import render
orig_process = render._process_chapter
def mock_process(ch_dict, config, vol_num, footnote_map, *args, **kwargs):
    if 'Christologia' in ch_dict.get('title', ''):
        print("OVERRIDE EXISTS?", ch_dict['title'] in config.get('treatise_title_overrides', {}))
    return orig_process(ch_dict, config, vol_num, footnote_map, *args, **kwargs)

render._process_chapter = mock_process
print("Patched _process_chapter")

from render import render_volume
from volumes.v1.convert import OVERRIDES
render_volume(1, overrides=OVERRIDES)
