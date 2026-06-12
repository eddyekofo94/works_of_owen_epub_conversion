#!/usr/bin/env python3
"""
Hebrews Volume 7 — An Exposition of the Epistle to the Hebrews, Volume 7
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h7'

_H7_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 7.</h1>

<h2 class="contents-treatise-title">EXPOSITION OF HEBREWS 11:1 – 13:25</h2>

<h3 class="contents-part-title">Chapter XI</h3>
<p class="contents-item"><b>Hebrews 11:1.</b> <a href="ch002.xhtml">Now faith is the substance of things hoped for...</a></p>
<p class="contents-item"><b>Hebrews 11:2.</b> <a href="ch003.xhtml">For by it the elders obtained a good report.</a></p>
<p class="contents-item"><b>Hebrews 11:3.</b> <a href="ch004.xhtml">Through faith we understand that the worlds...</a></p>
<p class="contents-item"><b>Hebrews 11:4.</b> <a href="ch005.xhtml">By faith Abel offered unto God a more excellent...</a></p>
<p class="contents-item"><b>Hebrews 11:5.</b> <a href="ch006.xhtml">By faith Enoch was translated that he should not...</a></p>
<p class="contents-item"><b>Hebrews 11:6.</b> <a href="ch007.xhtml">But without faith it is impossible to please him...</a></p>
<p class="contents-item"><b>Hebrews 11:7.</b> <a href="ch008.xhtml">By faith Noah, being warned of God of things...</a></p>
<p class="contents-item"><b>Hebrews 11:8.</b> <a href="ch009.xhtml">By faith Abraham, when he was called to go out...</a></p>
<p class="contents-item"><b>Hebrews 11:9.</b> <a href="ch010.xhtml">By faith he sojourned in the land of promise...</a></p>
<p class="contents-item"><b>Hebrews 11:10.</b> <a href="ch011.xhtml">For he looked for a city which hath foundations...</a></p>
<p class="contents-item"><b>Hebrews 11:11.</b> <a href="ch012.xhtml">Through faith also Sara herself received strength...</a></p>
<p class="contents-item"><b>Hebrews 11:12.</b> <a href="ch013.xhtml">Therefore sprang there even of one, and him...</a></p>
<p class="contents-item"><b>Hebrews 11:13.</b> <a href="ch014.xhtml">These all died in faith, not having received...</a></p>
<p class="contents-item"><b>Hebrews 11:14.</b> <a href="ch015.xhtml">For they that say such things declare plainly...</a></p>
<p class="contents-item"><b>Hebrews 11:15.</b> <a href="ch016.xhtml">And truly, if they had been mindful of that...</a></p>
<p class="contents-item"><b>Hebrews 11:16.</b> <a href="ch017.xhtml">But now they desire a better country, that...</a></p>
<p class="contents-item"><b>Hebrews 11:17–19.</b> <a href="ch018.xhtml">By faith Abraham, when he was tried, offered...</a></p>
<p class="contents-item"><b>Hebrews 11:20.</b> <a href="ch019.xhtml">By faith Isaac blessed Jacob and Esau concerning...</a></p>
<p class="contents-item"><b>Hebrews 11:21.</b> <a href="ch020.xhtml">By faith Jacob, when he was a dying, blessed...</a></p>
<p class="contents-item"><b>Hebrews 11:22.</b> <a href="ch021.xhtml">By faith Joseph, when he died, made mention...</a></p>
<p class="contents-item"><b>Hebrews 11:23.</b> <a href="ch022.xhtml">By faith Moses, when he was born, was hid...</a></p>
<p class="contents-item"><b>Hebrews 11:24–26.</b> <a href="ch023.xhtml">By faith Moses, when he was come to years...</a></p>
<p class="contents-item"><b>Hebrews 11:27.</b> <a href="ch024.xhtml">By faith he forsook Egypt, not fearing the...</a></p>
<p class="contents-item"><b>Hebrews 11:28.</b> <a href="ch025.xhtml">Through faith he kept the passover, and the...</a></p>
<p class="contents-item"><b>Hebrews 11:29.</b> <a href="ch026.xhtml">By faith they passed through the Red sea...</a></p>
<p class="contents-item"><b>Hebrews 11:30.</b> <a href="ch027.xhtml">By faith the walls of Jericho fell down...</a></p>
<p class="contents-item"><b>Hebrews 11:31.</b> <a href="ch028.xhtml">By faith the harlot Rahab perished not with...</a></p>
<p class="contents-item"><b>Hebrews 11:32.</b> <a href="ch029.xhtml">And what shall I more say? for the time...</a></p>
<p class="contents-item"><b>Hebrews 11:33.</b> <a href="ch030.xhtml">Who through faith subdued kingdoms, wrought...</a></p>
<p class="contents-item"><b>Hebrews 11:34, 35.</b> <a href="ch031.xhtml">Quenched the violence of fire, escaped the...</a></p>
<p class="contents-item"><b>Hebrews 11:35–37.</b> <a href="ch032.xhtml">Women received their dead raised to life...</a></p>

<h3 class="contents-part-title">Chapter XII</h3>
<p class="contents-item"><b>Hebrews 12:1.</b> <a href="ch034.xhtml">Wherefore seeing we also are compassed about...</a></p>
<p class="contents-item"><b>Hebrews 12:2.</b> <a href="ch035.xhtml">Looking unto Jesus the author and finisher...</a></p>
<p class="contents-item"><b>Hebrews 12:3.</b> <a href="ch036.xhtml">For consider him that endured such contradiction...</a></p>
<p class="contents-item"><b>Hebrews 12:4.</b> <a href="ch037.xhtml">Ye have not yet resisted unto blood, striving...</a></p>
<p class="contents-item"><b>Hebrews 12:5.</b> <a href="ch038.xhtml">And ye have forgotten the exhortation which...</a></p>
<p class="contents-item"><b>Hebrews 12:6.</b> <a href="ch039.xhtml">For whom the Lord loveth he chasteneth...</a></p>
<p class="contents-item"><b>Hebrews 12:7.</b> <a href="ch040.xhtml">If ye endure chastening, God dealeth with...</a></p>
<p class="contents-item"><b>Hebrews 12:8.</b> <a href="ch041.xhtml">But if ye be without chastisement, whereof...</a></p>
<p class="contents-item"><b>Hebrews 12:9, 10.</b> <a href="ch042.xhtml">Furthermore we have had fathers of our flesh...</a></p>
<p class="contents-item"><b>Hebrews 12:11.</b> <a href="ch043.xhtml">Now no chastening for the present seemeth...</a></p>
<p class="contents-item"><b>Hebrews 12:12, 13.</b> <a href="ch044.xhtml">Wherefore lift up the hands which hang down...</a></p>
<p class="contents-item"><b>Hebrews 12:14.</b> <a href="ch045.xhtml">Follow peace with all men, and holiness...</a></p>
<p class="contents-item"><b>Hebrews 12:15.</b> <a href="ch046.xhtml">Looking diligently lest any man fail of the...</a></p>
<p class="contents-item"><b>Hebrews 12:16, 17.</b> <a href="ch047.xhtml">Lest there be any fornicator, or profane person...</a></p>
<p class="contents-item"><b>Hebrews 12:18–29.</b> <a href="ch048.xhtml">For ye are not come unto the mount that...</a></p>

<h3 class="contents-part-title">Chapter XIII</h3>
<p class="contents-item"><b>Hebrews 13:1.</b> <a href="ch050.xhtml">Let brotherly love continue.</a></p>
<p class="contents-item"><b>Hebrews 13:2.</b> <a href="ch051.xhtml">Be not forgetful to entertain strangers...</a></p>
<p class="contents-item"><b>Hebrews 13:3.</b> <a href="ch052.xhtml">Remember them that are in bonds, as bound...</a></p>
<p class="contents-item"><b>Hebrews 13:4.</b> <a href="ch053.xhtml">Marriage is honourable in all, and the bed...</a></p>
<p class="contents-item"><b>Hebrews 5:5, 6.</b> <a href="ch054.xhtml">Let your conversation be without covetousness...</a></p> <!-- Note: fixed a minor typo in verse label: Hebrews 13:5, 6 -->
<p class="contents-item"><b>Hebrews 13:7.</b> <a href="ch055.xhtml">Remember them which have the rule over you...</a></p>
<p class="contents-item"><b>Hebrews 13:8.</b> <a href="ch056.xhtml">Jesus Christ the same yesterday, and to-day...</a></p>
<p class="contents-item"><b>Hebrews 13:9–17.</b> <a href="ch057.xhtml">Be not carried about with divers and strange...</a></p>
<p class="contents-item"><b>Hebrews 13:18–25.</b> <a href="ch058.xhtml">Pray for us: for we trust we have a good...</a></p>
</section>'''

# Let's fix that minor typo 'Hebrews 5:5, 6' in the string:
_H7_CONTENTS_PAGE = _H7_CONTENTS_PAGE.replace('Hebrews 5:5, 6.', 'Hebrews 13:5, 6.')

OVERRIDES = {
    'contents_page_overrides': _H7_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H7_CONTENTS_PAGE,
    },
    'text_replacements': {
        "them s strangers": "them as strangers"
    }
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
