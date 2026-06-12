#!/usr/bin/env python3
"""
Hebrews Volume 4 — An Exposition of the Epistle to the Hebrews, Volume 4
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h4'

_H4_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 4.</h1>

<h2 class="contents-treatise-title">EXPOSITION OF HEBREWS 3:7 – 5:14</h2>

<h3 class="contents-part-title">Chapter III (Continued)</h3>
<p class="contents-item"><b>Hebrews 3:7–11.</b> <a href="ch001.xhtml">Wherefore (as the Holy Ghost saith, To-day...</a></p>
<p class="contents-item"><b>Hebrews 3:12–14.</b> <a href="ch002.xhtml">Take heed, brethren, lest there be in any of you...</a></p>
<p class="contents-item"><b>Hebrews 3:15–19.</b> <a href="ch003.xhtml">While it is said, To-day if ye will hear his voice...</a></p>

<h3 class="contents-part-title">Chapter IV</h3>
<p class="contents-item"><b>Hebrews 4:1, 2.</b> <a href="ch005.xhtml">Let us therefore fear, lest, a promise being left...</a></p>
<p class="contents-item"><b>Hebrews 4:3.</b> <a href="ch006.xhtml">For we which have believed do enter into rest...</a></p>
<p class="contents-item"><b>Hebrews 4:4.</b> <a href="ch007.xhtml">For he spake in a certain place of the seventh day...</a></p>
<p class="contents-item"><b>Hebrews 4:5.</b> <a href="ch008.xhtml">And in this place again, If they shall enter into...</a></p>
<p class="contents-item"><b>Hebrews 4:6.</b> <a href="ch009.xhtml">Seeing therefore it remaineth that some must enter...</a></p>
<p class="contents-item"><b>Hebrews 4:7.</b> <a href="ch010.xhtml">Again, he limiteth a certain day, saying in David...</a></p>
<p class="contents-item"><b>Hebrews 4:8.</b> <a href="ch011.xhtml">For if Jesus had given them rest, then would he...</a></p>
<p class="contents-item"><b>Hebrews 4:9.</b> <a href="ch012.xhtml">There remaineth therefore a rest to the people...</a></p>
<p class="contents-item"><b>Hebrews 4:10.</b> <a href="ch013.xhtml">For he that is entered into his rest, he also hath...</a></p>
<p class="contents-item"><b>Hebrews 4:11.</b> <a href="ch014.xhtml">Let us labour therefore to enter into that rest...</a></p>
<p class="contents-item"><b>Hebrews 4:12, 13.</b> <a href="ch015.xhtml">For the word of God is quick, and powerful, and...</a></p>
<p class="contents-item"><b>Hebrews 4:14–16.</b> <a href="ch016.xhtml">Seeing then that we have a great high priest...</a></p>

<h3 class="contents-part-title">Chapter V</h3>
<p class="contents-item"><b>Hebrews 5:1.</b> <a href="ch021.xhtml">For every high priest taken from among men...</a></p>
<p class="contents-item"><b>Hebrews 5:2.</b> <a href="ch022.xhtml">Who can have compassion on the ignorant...</a></p>
<p class="contents-item"><b>Hebrews 5:3.</b> <a href="ch023.xhtml">And by reason hereof he ought, as for the people...</a></p>
<p class="contents-item"><b>Hebrews 5:4.</b> <a href="ch024.xhtml">And no man taketh this honour unto himself...</a></p>
<p class="contents-item"><b>Hebrews 5:5.</b> <a href="ch025.xhtml">So also Christ glorified not himself to be made...</a></p>
<p class="contents-item"><b>Hebrews 5:6.</b> <a href="ch026.xhtml">As he saith also in another place, Thou art a priest...</a></p>
<p class="contents-item"><b>Hebrews 5:7.</b> <a href="ch027.xhtml">Who in the days of his flesh, when he had offered...</a></p>
<p class="contents-item"><b>Hebrews 5:8.</b> <a href="ch028.xhtml">Though he were a Son, yet learned he obedience...</a></p>
<p class="contents-item"><b>Hebrews 5:9.</b> <a href="ch029.xhtml">And being made perfect, he became the author...</a></p>
<p class="contents-item"><b>Hebrews 5:10.</b> <a href="ch030.xhtml">Called of God an high priest after the order...</a></p>
<p class="contents-item"><b>Hebrews 5:11.</b> <a href="ch031.xhtml">Of whom we have many things to say, and hard...</a></p>
<p class="contents-item"><b>Hebrews 5:12–14.</b> <a href="ch032.xhtml">For when for the time ye ought to be teachers...</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H4_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H4_CONTENTS_PAGE,
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
