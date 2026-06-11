#!/usr/bin/env python3
"""
Hebrews Volume 3 — An Exposition of the Epistle to the Hebrews, Volume 3
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h3'

_H3_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 3.</h1>

<h2 class="contents-treatise-title">EXPOSITION OF HEBREWS 1:1 – 3:6</h2>

<h3 class="contents-part-title">Chapter I</h3>
<p class="contents-item"><b>Hebrews 1:1, 2.</b> <a href="ch002.xhtml">God, who at sundry times and in divers manners...</a></p>
<p class="contents-item"><b>Hebrews 1:3.</b> <a href="ch003.xhtml">Who being the brightness of his glory...</a></p>
<p class="contents-item"><b>Hebrews 1:4.</b> <a href="ch004.xhtml">Being made so much better than the angels...</a></p>
<p class="contents-item"><b>Hebrews 1:5.</b> <a href="ch005.xhtml">For unto which of the angels said he at any time...</a></p>
<p class="contents-item"><b>Hebrews 1:6.</b> <a href="ch006.xhtml">And again, when he bringeth in the first-begotten...</a></p>
<p class="contents-item"><b>Hebrews 1:7.</b> <a href="ch007.xhtml">And of the angels he saith, Who maketh his angels...</a></p>
<p class="contents-item"><b>Hebrews 1:8, 9.</b> <a href="ch008.xhtml">But unto the Son he saith, Thy throne, O God...</a></p>
<p class="contents-item"><b>Hebrews 1:10–12.</b> <a href="ch009.xhtml">And, Thou, Lord, in the beginning hast laid...</a></p>
<p class="contents-item"><b>Hebrews 1:13.</b> <a href="ch010.xhtml">But to which of the angels said he at any time...</a></p>
<p class="contents-item"><b>Hebrews 1:14.</b> <a href="ch011.xhtml">Are they not all ministering spirits...</a></p>

<h3 class="contents-part-title">Chapter II</h3>
<p class="contents-item"><b>Hebrews 2:1.</b> <a href="ch013.xhtml">Therefore we ought to give the more earnest heed...</a></p>
<p class="contents-item"><b>Hebrews 2:2–4.</b> <a href="ch014.xhtml">For if the word spoken by angels was stedfast...</a></p>
<p class="contents-item"><b>Hebrews 2:5–9.</b> <a href="ch015.xhtml">For unto the angels hath he not put in subjection...</a></p>
<p class="contents-item"><b>Hebrews 2:10.</b> <a href="ch016.xhtml">For it became him, for whom are all things...</a></p>
<p class="contents-item"><b>Hebrews 2:11–13.</b> <a href="ch017.xhtml">For both he that sanctifieth and they who are...</a></p>
<p class="contents-item"><b>Hebrews 2:14, 15.</b> <a href="ch018.xhtml">Forasmuch then as the children are partakers...</a></p>
<p class="contents-item"><b>Hebrews 2:16.</b> <a href="ch019.xhtml">For verily he took not on him the nature of angels...</a></p>
<p class="contents-item"><b>Hebrews 2:17, 18.</b> <a href="ch020.xhtml">Wherefore in all things it behoved him to be made...</a></p>

<h3 class="contents-part-title">Chapter III</h3>
<p class="contents-item"><b>Hebrews 3:1, 2.</b> <a href="ch022.xhtml">Wherefore, holy brethren, partakers of the heavenly...</a></p>
<p class="contents-item"><b>Hebrews 3:3–6.</b> <a href="ch023.xhtml">For this man was counted worthy of more glory...</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H3_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H3_CONTENTS_PAGE,
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
