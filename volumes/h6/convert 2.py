#!/usr/bin/env python3
"""
Hebrews Volume 6 — An Exposition of the Epistle to the Hebrews, Volume 6
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h6'

_H6_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 6.</h1>

<h2 class="contents-treatise-title">EXPOSITION OF HEBREWS 8:1 – 10:39</h2>

<h3 class="contents-part-title">Chapter VIII</h3>
<p class="contents-item"><b>Hebrews 8:1.</b> <a href="ch002.xhtml">Now of the things which we have spoken this is the sum...</a></p>
<p class="contents-item"><b>Hebrews 8:2.</b> <a href="ch003.xhtml">A minister of the sanctuary, and of the true tabernacle...</a></p>
<p class="contents-item"><b>Hebrews 8:3.</b> <a href="ch004.xhtml">For every high priest is ordained to offer gifts...</a></p>
<p class="contents-item"><b>Hebrews 8:4.</b> <a href="ch005.xhtml">For if he were on earth, he should not be a priest...</a></p>
<p class="contents-item"><b>Hebrews 8:5.</b> <a href="ch006.xhtml">Who serve unto the example and shadow of heavenly...</a></p>
<p class="contents-item"><b>Hebrews 8:6.</b> <a href="ch007.xhtml">But now hath he obtained a more excellent ministry...</a></p>
<p class="contents-item"><b>Hebrews 8:7.</b> <a href="ch008.xhtml">For if that first covenant had been faultless...</a></p>
<p class="contents-item"><b>Hebrews 8:8.</b> <a href="ch009.xhtml">For finding fault with them, he saith, Behold...</a></p>
<p class="contents-item"><b>Hebrews 8:9.</b> <a href="ch010.xhtml">Not according to the covenant that I made with their...</a></p>
<p class="contents-item"><b>Hebrews 8:10–12.</b> <a href="ch011.xhtml">For this is the covenant that I will make with...</a></p>
<p class="contents-item"><b>Hebrews 8:13.</b> <a href="ch012.xhtml">In that he saith, A new covenant, he hath made...</a></p>

<h3 class="contents-part-title">Chapter IX</h3>
<p class="contents-item"><b>Hebrews 9:1.</b> <a href="ch014.xhtml">Then verily the first covenant had also ordinances...</a></p>
<p class="contents-item"><b>Hebrews 9:2.</b> <a href="ch015.xhtml">For there was a tabernacle made; the first...</a></p>
<p class="contents-item"><b>Hebrews 9:3–5.</b> <a href="ch016.xhtml">And after the second veil, the tabernacle...</a></p>
<p class="contents-item"><b>Hebrews 9:6, 7.</b> <a href="ch017.xhtml">Now when these things were thus ordained...</a></p>
<p class="contents-item"><b>Hebrews 9:8.</b> <a href="ch018.xhtml">The Holy Ghost this signifying, that the way...</a></p>
<p class="contents-item"><b>Hebrews 9:9, 10.</b> <a href="ch019.xhtml">Which was a figure for the time then present...</a></p>
<p class="contents-item"><b>Hebrews 9:11.</b> <a href="ch020.xhtml">But Christ being come an high priest of good...</a></p>
<p class="contents-item"><b>Hebrews 9:12.</b> <a href="ch021.xhtml">Neither by the blood of goats and calves, but...</a></p>
<p class="contents-item"><b>Hebrews 9:13, 14.</b> <a href="ch022.xhtml">For if the blood of bulls and of goats, and...</a></p>
<p class="contents-item"><b>Hebrews 9:15.</b> <a href="ch023.xhtml">And for this cause he is the mediator of the...</a></p>
<p class="contents-item"><b>Hebrews 9:16, 17.</b> <a href="ch024.xhtml">For where a testament is, there must also of...</a></p>
<p class="contents-item"><b>Hebrews 9:18–22.</b> <a href="ch025.xhtml">Whereupon neither the first testament was dedicated...</a></p>
<p class="contents-item"><b>Hebrews 9:23.</b> <a href="ch026.xhtml">It was therefore necessary that the patterns of...</a></p>
<p class="contents-item"><b>Hebrews 9:24.</b> <a href="ch027.xhtml">For Christ is not entered into the holy places...</a></p>
<p class="contents-item"><b>Hebrews 9:25.</b> <a href="ch028.xhtml">Nor yet that he should offer himself often, as...</a></p>
<p class="contents-item"><b>Hebrews 9:26.</b> <a href="ch029.xhtml">For then must he often have suffered since the...</a></p>
<p class="contents-item"><b>Hebrews 9:27, 28.</b> <a href="ch030.xhtml">And as it is appointed unto men once to die...</a></p>

<h3 class="contents-part-title">Chapter X</h3>
<p class="contents-item"><b>Hebrews 10:1.</b> <a href="ch032.xhtml">For the law having a shadow of good things to come...</a></p>
<p class="contents-item"><b>Hebrews 10:2, 3.</b> <a href="ch033.xhtml">For then would they not have ceased to be offered...</a></p>
<p class="contents-item"><b>Hebrews 10:4.</b> <a href="ch034.xhtml">For it is not possible that the blood of bulls...</a></p>
<p class="contents-item"><b>Hebrews 10:5–10.</b> <a href="ch035.xhtml">Wherefore when he cometh into the world, he saith...</a></p>
<p class="contents-item"><b>Hebrews 10:11–14.</b> <a href="ch036.xhtml">And every priest standeth daily ministering and...</a></p>
<p class="contents-item"><b>Hebrews 10:15–18.</b> <a href="ch037.xhtml">Whereof the Holy Ghost also is a witness to us...</a></p>
<p class="contents-item"><b>Hebrews 10:19–23.</b> <a href="ch038.xhtml">Having therefore, brethren, boldness to enter...</a></p>
<p class="contents-item"><b>Hebrews 10:24.</b> <a href="ch039.xhtml">And let us consider one another to provoke...</a></p>
<p class="contents-item"><b>Hebrews 10:25.</b> <a href="ch040.xhtml">Not forsaking the assembling of ourselves...</a></p>
<p class="contents-item"><b>Hebrews 10:26, 27.</b> <a href="ch041.xhtml">For if we sin wilfully after that we have received...</a></p>
<p class="contents-item"><b>Hebrews 10:28, 29.</b> <a href="ch042.xhtml">He that despised Moses' law died without mercy...</a></p>
<p class="contents-item"><b>Hebrews 10:30, 31.</b> <a href="ch043.xhtml">For we know him that hath said, Vengeance...</a></p>
<p class="contents-item"><b>Hebrews 10:32–34.</b> <a href="ch044.xhtml">But call to remembrance the former days, in...</a></p>
<p class="contents-item"><b>Hebrews 10:35, 36.</b> <a href="ch045.xhtml">Cast not away therefore your confidence, which...</a></p>
<p class="contents-item"><b>Hebrews 10:37–39.</b> <a href="ch046.xhtml">For yet a little while, and he that shall come...</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H6_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H6_CONTENTS_PAGE,
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
