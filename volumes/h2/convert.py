#!/usr/bin/env python3
"""
Hebrews Volume 2 — An Exposition of the Epistle to the Hebrews, Volume 2
Per-volume converter script.
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 'h2'

_H2_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF HEBREWS VOLUME 2.</h1>

<h2 class="contents-treatise-title">PART IV. CONCERNING THE SACERDOTAL OFFICE OF CHRIST</h2>
<p class="contents-item"><strong>Exercitation XXV.</strong> <a href="ch002.xhtml">The office of priesthood</a></p>
<p class="contents-item"><strong>Exercitation XXVI.</strong> <a href="ch003.xhtml">Of the origin of the priesthood of Christ</a></p>
<p class="contents-item"><strong>Exercitation XXVII.</strong> <a href="ch004.xhtml">The original of the priesthood of Christ in the counsel of God</a></p>
<p class="contents-item"><strong>Exercitation XXVIII.</strong> <a href="ch005.xhtml">Federal transactions between the Father and the Son</a></p>
<p class="contents-item"><strong>Exercitation XXIX.</strong> <a href="ch006.xhtml">The necessity of the priesthood of Christ on the supposition of sin and grace</a></p>
<p class="contents-item"><strong>Exercitation XXX.</strong> <a href="ch007.xhtml">The necessity of the priesthood of Christ on the supposition of sin and grace</a></p>
<p class="contents-item"><strong>Exercitation XXXI.</strong> <a href="ch008.xhtml">The nature of the priesthood of Christ</a></p>
<p class="contents-item"><strong>Exercitation XXXII.</strong> <a href="ch009.xhtml">The nature of the priesthood of Christ</a></p>
<p class="contents-item"><strong>Exercitation XXXIII.</strong> <a href="ch010.xhtml">Of the acts of the priesthood of Christ, their object, with the time and place of its discharge</a></p>
<p class="contents-item"><strong>Exercitation XXXIV.</strong> <a href="ch011.xhtml">Prefigurations of the priesthood and sacrifice of Christ</a></p>
<p class="contents-item"><a href="ch012.xhtml">An Advertisement unto the Reader</a></p>

<h2 class="contents-treatise-title">PART V. CONCERNING A DAY OF SACRED REST</h2>
<p class="contents-item"><a href="ch014.xhtml">To the Reader</a></p>
<p class="contents-item"><strong>Exercitation I.</strong> <a href="ch015.xhtml">Differences concerning a day of sacred rest — Principles directing to the observance of it — The pre-eminence of the Lord's Day</a></p>
<p class="contents-item"><strong>Exercitation II.</strong> <a href="ch016.xhtml">Of the original of the Sabbath</a></p>
<p class="contents-item"><strong>Exercitation III.</strong> <a href="ch017.xhtml">Of the causes of the Sabbath</a></p>
<p class="contents-item"><strong>Exercitation IV.</strong> <a href="ch018.xhtml">Of the Judaical Sabbath</a></p>
<p class="contents-item"><strong>Exercitation V.</strong> <a href="ch019.xhtml">Of the Lord's Day</a></p>
<p class="contents-item"><strong>Exercitation VI.</strong> <a href="ch020.xhtml">The practical observance of the Lord's Day</a></p>

<h2 class="contents-treatise-title">SUMMARY OF OBSERVATIONS</h2>
<p class="contents-item"><strong>Chapters I, II.</strong> <a href="ch022.xhtml">Pre-eminent dignity of Christ, both absolutely and comparatively</a></p>
<p class="contents-item"><strong>Chapters III, IV:1–13.</strong> <a href="ch023.xhtml">Christ's superiority to Moses, the agent in founding the old dispensation</a></p>
<p class="contents-item"><strong>Chapters IV:14–16, V–VIII.</strong> <a href="ch024.xhtml">Superiority of Christ as priest to the Levitical priesthood</a></p>
<p class="contents-item"><strong>Chapters IX, X:1–18.</strong> <a href="ch025.xhtml">Superiority of Christ's priesthood from the superior value of his sacrifice</a></p>
<p class="contents-item"><strong>Chapters X:19–39, XI.</strong> <a href="ch026.xhtml">The obligation, advantage, and necessity of steadfast adherence to the gospel</a></p>
</section>'''

OVERRIDES = {
    'contents_page_overrides': _H2_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _H2_CONTENTS_PAGE,
    },
}

def main():
    run_volume_cli(VOL, overrides=OVERRIDES)

if __name__ == '__main__':
    main()
