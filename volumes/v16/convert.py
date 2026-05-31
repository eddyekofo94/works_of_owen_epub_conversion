#!/usr/bin/env python3
"""
Volume 16 — The Works of John Owen, Volume 16: Gospel Church, Scripture, and Posthumous Sermons
Per-volume converter script.

Usage:
    python3 volumes/v16/convert.py                   # full pipeline (extract + render)
    python3 volumes/v16/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v16/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Volume 16 contains:
  - The True Nature of a Gospel Church and Its Government
  - A Letter and a Discourse (on excommunication and church censures)
  - Various shorter tracts on baptism, divorce, marriage, the Scriptures
  - Treatises Concerning the Scriptures
  - Hebrew and Greek Text of the Scripture (integrity and purity of the text)
  - Posthumous Sermons
  - Three Discourses Suitable to the Lord's Supper

Note: "A Letter Concerining the Matter of the Present Excommunications" —
"Concerining" is an OCR misspelling of "Concerning"; corrected in text_replacements.
"Three Discourses Suitable to the Lordìs Supper" — "Lordìs" is an OCR artifact
for "Lord's"; corrected below.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 16

# ---------------------------------------------------------------------------
# Treatise title pages
# ---------------------------------------------------------------------------

_V16_GOSPEL_CHURCH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The True Nature of a</p>
<p class="title-line-major">Gospel Church</p>
<p class="title-connector">and Its Government.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"And I say also unto thee, That thou art Peter, and upon this rock I will build my church; and the gates of hell shall not prevail against it." — Matthew 16:18.</p></div>
</section>'''

_V16_LETTER_DISCOURSE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">A Letter and a Discourse</p>
<p class="title-connector">Concerning</p>
<p class="title-line-medium">Excommunication</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Church Censures.</p>
</section>'''

_V16_TREATISES_SCRIPTURES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Treatises</p>
<p class="title-connector">Concerning the</p>
<p class="title-line-major">Scriptures.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Including: The Scriptures: An Answer to That Inquiry, Wherefore We Believe Them to Be the Word of God.</p>
</section>'''

_V16_HEBREW_GREEK_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Hebrew and Greek Text</p>
<p class="title-connector">of the</p>
<p class="title-line-major">Scripture:</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Integrity and Purity of the Hebrew</p>
<p class="title-line-medium">and Greek Text of the Scripture</p>
<p class="title-line-medium">Vindicated.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">In Exercitations on the Prolegomena, and Appendix, to the Late Biblia Polyglotta.</p>
</section>'''

_V16_POSTHUMOUS_SERMONS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Posthumous Sermons.</p>
</section>'''

_V16_THREE_DISCOURSES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">Three Discourses</p>
<p class="title-connector">Suitable to the</p>
<p class="title-line-major">Lord's Supper.</p>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'The True Nature of a Gospel Church and Its Government.': _V16_GOSPEL_CHURCH_TITLE_PAGE,
        'A Letter and a Discourse': _V16_LETTER_DISCOURSE_TITLE_PAGE,
        'Treatises Concerning the Scriptures.': _V16_TREATISES_SCRIPTURES_TITLE_PAGE,
        'Hebrew and Greek Text of the Scripture;': _V16_HEBREW_GREEK_TITLE_PAGE,
        'Posthumous Sermons:': _V16_POSTHUMOUS_SERMONS_TITLE_PAGE,
        # OCR artifact "Lordìs" in JSON title — match exact corrupted string
        'Three Discourses Suitable to the Lordìs Supper.': _V16_THREE_DISCOURSES_TITLE_PAGE,
    },
    'text_replacements': {
        # OCR misspelling in JSON title and body
        'Concerining': 'Concerning',
        # OCR i-grave apostrophe artifact in body
        'Lordìs Supper': "Lord's Supper",
        'lordìs supper': "lord's supper",
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
