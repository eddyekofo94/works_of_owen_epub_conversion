#!/usr/bin/env python3
"""
Volume 4 — The Works of John Owen, Volume 4: The Reason of Faith; Holy Spirit (Books 5–7)
Per-volume converter script.

Usage:
    python3 volumes/v4/convert.py                   # full pipeline (extract + render)
    python3 volumes/v4/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v4/convert.py --render-only     # Stage 2 only (JSON → EPUB)
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 4

# ---------------------------------------------------------------------------
# Treatise title pages
# Title strings must match the EXACT chapter title from
# volumes/v4/intermediate/volume_4.json (including punctuation).
# ---------------------------------------------------------------------------

_V4_HS_CONTINUED_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Discourse</p>
<p class="title-connector">Concerning the</p>
<p class="title-line-major">Holy Spirit:</p>
<p class="title-connector">Continued.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">Books V, VI, and VII: Treating of the Work of the Holy Spirit in the Illumination of the Mind, the Sanctification of the Will, and the Renovation of the Whole Soul.</p>
</section>'''

_V4_REASON_OF_FAITH_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">The Reason of Faith;</p>
<p class="title-connector">or, an Answer Unto That Inquiry,</p>
<p class="title-line-medium">Wherefore We Believe the Scripture</p>
<p class="title-line-medium">to Be the Word of God</p>
<p class="title-connector">with the Sure Foundation of Our Faith Therein Asserted and Explained.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"For I am not ashamed of the gospel of Christ: for it is the power of God unto salvation to every one that believeth." — Romans 1:16.</p></div>
</section>'''

_V4_CAUSES_WAYS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Causes, Ways, and Means</p>
<p class="title-connector">of</p>
<p class="title-line-medium">Understanding the Mind of God</p>
<p class="title-connector">as Revealed in His Word,</p>
<p class="title-line-medium">with Assurance Therein.</p>
<p class="title-rule" aria-hidden="true"></p>
<p class="descriptive">And a Declaration of the Perspicuity of the Scriptures, with the External Means of the Interpretation of Them.</p>
</section>'''

_V4_HS_PRAYER_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Discourse</p>
<p class="title-connector">of the Work of the</p>
<p class="title-line-medium">Holy Spirit in Prayer;</p>
<p class="title-connector">with a Brief Inquiry into the Nature and Use of</p>
<p class="title-line-medium">Mental Prayer and Forms.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Likewise the Spirit also helpeth our infirmities: for we know not what we should pray for as we ought: but the Spirit itself maketh intercession for us with groanings which cannot be uttered." — Romans 8:26.</p></div>
</section>'''

_V4_TWO_DISCOURSES_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">Two Discourses</p>
<p class="title-connector">Concerning the</p>
<p class="title-line-medium">Holy Spirit and His Work:</p>
<p class="title-connector">The First, of</p>
<p class="title-line-medium">The Spirit as a Comforter;</p>
<p class="title-connector">The Second, of</p>
<p class="title-line-medium">The Work of the Holy Spirit</p>
<p class="title-line-medium">in the New Creation.</p>
</section>'''

_V4_SPIRITUAL_GIFTS_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-major">A Discourse</p>
<p class="title-connector">Concerning the</p>
<p class="title-line-medium">Holy Spirit,</p>
<p class="title-connector">His Gifts:</p>
<p class="title-line-medium">Their Nature, Distributions,</p>
<p class="title-line-medium">Excellency, Use, and Abuse.</p>
</section>'''

OVERRIDES = {
    'treatise_title_overrides': {
        'A Discourse Concerning the Holy Spirit, Continued:': _V4_HS_CONTINUED_TITLE_PAGE,
        'The Reason of Faith;': _V4_REASON_OF_FAITH_TITLE_PAGE,
        'The Causes, Ways, and Means of Understanding the Mind of God as': _V4_CAUSES_WAYS_TITLE_PAGE,
        'A Discourse of the Work of the Holy Spirit in Prayer': _V4_HS_PRAYER_TITLE_PAGE,
        'Two Discourses Concerning the Holy Spirit and His Work:': _V4_TWO_DISCOURSES_TITLE_PAGE,
        # OCR typo in JSON: "Glfts" instead of "Gifts" — keep the key exactly as it appears in JSON
        'A Discourse of Spiritual Glfts.': _V4_SPIRITUAL_GIFTS_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair OCR chapter-title typo so it renders correctly in the body
        'Spiritual Glfts': 'Spiritual Gifts',
        'Glfts': 'Gifts',
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()
