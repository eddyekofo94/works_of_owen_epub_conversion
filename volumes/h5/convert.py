#!/usr/bin/env python3
"""
Hebrews Volume 5 — An Exposition of the Epistle to the Hebrews, Volume 5
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h5'

_H5_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 5.</h1>

<h2 class="contents-treatise-title">EXPOSITION OF HEBREWS 6:1 – 7:28</h2>

<h3 class="contents-part-title">Chapter VI</h3>
<p class="contents-item"><b>Hebrews 6:1, 2.</b> <a href="ch003.xhtml">Therefore leaving the principles of the doctrine...</a></p>
<p class="contents-item"><b>Hebrews 6:3.</b> <a href="ch004.xhtml">And this will we do, if God permit.</a></p>
<p class="contents-item"><b>Hebrews 6:4–6.</b> <a href="ch005.xhtml">For it is impossible for those who were once enlightened...</a></p>
<p class="contents-item"><b>Hebrews 6:7, 8.</b> <a href="ch006.xhtml">For the earth which drinketh in the rain that cometh...</a></p>
<p class="contents-item"><b>Hebrews 6:9–12.</b> <a href="ch007.xhtml">But, beloved, we are persuaded better things of you...</a></p>
<p class="contents-item"><b>Hebrews 6:13–16.</b> <a href="ch010.xhtml">For when God made promise to Abraham, because...</a></p>
<p class="contents-item"><b>Hebrews 6:17–20.</b> <a href="ch011.xhtml">Wherein God, willing more abundantly to shew...</a></p>

<h3 class="contents-part-title">Chapter VII</h3>
<p class="contents-item"><b>Hebrews 7:1–3.</b> <a href="ch013.xhtml">For this Melchisedec, king of Salem, priest...</a></p>
<p class="contents-item"><b>Hebrews 7:4, 5.</b> <a href="ch014.xhtml">Now consider how great this man was, unto whom...</a></p>
<p class="contents-item"><b>Hebrews 7:6–10.</b> <a href="ch015.xhtml">But he whose descent is not counted from them...</a></p>
<p class="contents-item"><b>Hebrews 7:11.</b> <a href="ch020.xhtml">If therefore perfection were by the Levitical priesthood...</a></p>
<p class="contents-item"><b>Hebrews 7:12–14.</b> <a href="ch021.xhtml">For the priesthood being changed, there is made...</a></p>
<p class="contents-item"><b>Hebrews 7:15–17.</b> <a href="ch023.xhtml">And it is yet far more evident: for that after...</a></p>
<p class="contents-item"><b>Hebrews 7:18, 19.</b> <a href="ch012.xhtml">For there is verily a disannulling of the commandment...</a></p>
<p class="contents-item"><b>Hebrews 7:20–22.</b> <a href="ch024.xhtml">And inasmuch as not without an oath he was made...</a></p>
<p class="contents-item"><b>Hebrews 7:23–25.</b> <a href="ch025.xhtml">And they truly were many priests, because they...</a></p>
<p class="contents-item"><b>Hebrews 7:26.</b> <a href="ch026.xhtml">For such an high priest became us, who is holy...</a></p>
<p class="contents-item"><b>Hebrews 7:27, 28.</b> <a href="ch027.xhtml">Who needeth not daily, as those high priests...</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H5_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H5_CONTENTS_PAGE,
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
