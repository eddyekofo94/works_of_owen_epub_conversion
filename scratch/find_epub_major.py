import zipfile
import re

epub_path = 'volumes/v10/output/volume_10.epub'
with zipfile.ZipFile(epub_path, 'r') as z:
    for name in z.namelist():
        if name.endswith('.xhtml'):
            html = z.read(name).decode('utf-8')
            if '-major' in html or '-medium' in html:
                print(f"Found in {name}:")
                for line in html.splitlines():
                    if '-major' in line or '-medium' in line:
                        print(f"  {line}")
