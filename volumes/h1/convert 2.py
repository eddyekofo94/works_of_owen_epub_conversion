#!/usr/bin/env python3
"""
Hebrews Volume 1 — An Exposition of the Epistle to the Hebrews, Volume 1
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h1'

_H1_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 1.</h1>

<p class="contents-general-preface"><a href="ch001.xhtml">General Preface by the Editor</a></p>
<p class="contents-general-preface"><a href="ch002.xhtml">The Epistle Dedicatory</a></p>
<p class="contents-general-preface"><a href="ch003.xhtml">Prefatory Notices</a></p>

<h2 class="contents-treatise-title">PART I. CONCERNING THE EPISTLE TO THE HEBREWS</h2>
<p class="contents-item"><b>Exercitation I.</b> <a href="ch005.xhtml">The canonical authority of the Epistle to the Hebrews</a></p>
<p class="contents-item"><b>Exercitation II.</b> <a href="ch006.xhtml">Of the penman of the Epistle to the Hebrews</a></p>
<p class="contents-item"><b>Exercitation III.</b> <a href="ch007.xhtml">The time [and occasion] of the writing of the Epistle to the Hebrews</a></p>
<p class="contents-item"><b>Exercitation IV.</b> <a href="ch008.xhtml">The language wherein the Epistle to the Hebrews was originally written</a></p>
<p class="contents-item"><b>Exercitation V.</b> <a href="ch009.xhtml">Testimonies cited by the apostle out of the Old Testament</a></p>
<p class="contents-item"><b>Exercitation VI.</b> <a href="ch010.xhtml">Oneness of the church</a></p>
<p class="contents-item"><b>Exercitation VII.</b> <a href="ch011.xhtml">Of the Judaical distribution of the Old Testament</a></p>

<h2 class="contents-treatise-title">PART II. CONCERNING THE MESSIAH</h2>
<p class="contents-item"><b>Exercitation VIII.</b> <a href="ch013.xhtml">The first dissertation concerning the Messiah, proving him to be promised of old</a></p>
<p class="contents-item"><b>Exercitation IX.</b> <a href="ch014.xhtml">Promises of the Messiah vindicated</a></p>
<p class="contents-item"><b>Exercitation X.</b> <a href="ch015.xhtml">Appearances of the Son of God under the Old Testament</a></p>
<p class="contents-item"><b>Exercitation XI.</b> <a href="ch016.xhtml">Faith of the ancient church of the Jews concerning the Messiah</a></p>
<p class="contents-item"><b>Exercitation XII.</b> <a href="ch017.xhtml">The promised Messiah long since come</a></p>
<p class="contents-item"><b>Exercitation XIII.</b> <a href="ch018.xhtml">Other testimonies proving the Messiah to be come</a></p>
<p class="contents-item"><b>Exercitation XIV.</b> <a href="ch019.xhtml">Daniel's prophecy vindicated</a></p>
<p class="contents-item"><b>Exercitation XV.</b> <a href="ch020.xhtml">Computation of Daniel's weeks</a></p>
<p class="contents-item"><b>Exercitation XVI.</b> <a href="ch021.xhtml">Jewish traditions about the coming of the Messiah</a></p>
<p class="contents-item"><b>Exercitation XVII.</b> <a href="ch022.xhtml">Jesus of Nazareth the only true and promised Messiah</a></p>
<p class="contents-item"><b>Exercitation XVIII.</b> <a href="ch023.xhtml">Jews' objections against Christian religion answered</a></p>

<h2 class="contents-treatise-title">PART III. CONCERNING THE INSTITUTIONS OF THE JEWISH CHURCH</h2>
<p class="contents-item"><b>Exercitation XIX.</b> <a href="ch025.xhtml">State and ordinances of the church before the giving of the law</a></p>
<p class="contents-item"><b>Exercitation XX.</b> <a href="ch026.xhtml">The law and precepts thereof</a></p>
<p class="contents-item"><b>Exercitation XXI.</b> <a href="ch027.xhtml">The sanction of the law in promises and threatenings</a></p>
<p class="contents-item"><b>Exercitation XXII.</b> <a href="ch028.xhtml">Of the tabernacle and ark</a></p>
<p class="contents-item"><b>Exercitation XXIII.</b> <a href="ch029.xhtml">Of the office of the priesthood</a></p>
<p class="contents-item"><b>Exercitation XXIV.</b> <a href="ch030.xhtml">Sacrifices of the old law</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H1_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H1_CONTENTS_PAGE,
    },
    'text_replacements': {
        "concerned in in it": "concerned in, in it"
    }
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
