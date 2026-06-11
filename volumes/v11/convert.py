#!/usr/bin/env python3
"""
Volume 11 — The Works of John Owen, Volume 11: The Saints' Perseverance
Per-volume converter script.

Usage:
    python3 volumes/v11/convert.py                   # full pipeline (extract + render)
    python3 volumes/v11/convert.py --extract-only    # Stage 1 only (PDF → JSON)
    python3 volumes/v11/convert.py --render-only     # Stage 2 only (JSON → EPUB)

Note: The JSON chapter title reads "The Doctrine of the Saints Perseverance" —
the apostrophe in "Saints'" is missing due to OCR. The title page uses the
correct form; the text_replacement below also repairs it in the body text.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..', '..')
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from shared import run_volume_cli

VOL = 11

# ---------------------------------------------------------------------------
# Treatise title pages
# The key must match the EXACT (OCR-corrupted) chapter title from the JSON.
# ---------------------------------------------------------------------------

_V11_PERSEVERANCE_TITLE_PAGE = '''<section class="treatise-title-page" epub:type="titlepage">
<p class="title-line-medium">The Doctrine of the</p>
<p class="title-line-major">Saints' Perseverance,</p>
<p class="title-connector">Explained and Confirmed;</p>
<p class="title-connector">or, the</p>
<p class="title-line-medium">Certain Permanency of Their</p>
<p class="title-line-medium">Acceptance with God</p>
<p class="title-connector">and</p>
<p class="title-line-medium">Sanctification Considered and Proved.</p>
<p class="title-rule" aria-hidden="true"></p>
<div class="quote-block"><p>"Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ." — Philippians 1:6.</p></div>
</section>'''

_V11_CONTENTS_PAGE = '''<section class="contents-page" epub:type="toc">
<h1 class="contents-volume-title">CONTENTS OF VOLUME 11.</h1>

<h2 class="contents-treatise-title">THE DOCTRINE OF THE SAINTS' PERSEVERANCE EXPLAINED AND CONFIRMED</h2>
<p class="contents-item"><a href="ch002.xhtml">Prefatory Note by the Editor</a></p>
<p class="contents-item"><a href="ch003.xhtml">Analysis of the Treatise</a></p>
<p class="contents-item"><a href="ch004.xhtml">Epistle Dedicatory to Oliver Cromwell</a></p>
<p class="contents-item"><a href="ch005.xhtml">Epistle Dedicatory to the Heads and Governors of the Colleges and Halls in the University of Oxford</a></p>
<p class="contents-item"><a href="ch006.xhtml">A Preface to the Reader</a></p>
<p class="contents-item"><a href="ch007.xhtml">Note by the Editor on the Epistles</a></p>
<p class="contents-item"><b>Chapter I.</b> <a href="ch008.xhtml">The state of the controversy</a></p>
<p class="contents-item"><b>Chapter II.</b> <a href="ch009.xhtml">The perseverance of the saints argued from the immutability of the divine nature</a></p>
<p class="contents-item"><b>Chapter III.</b> <a href="ch010.xhtml">The immutability of the purposes of God</a></p>
<p class="contents-item"><b>Chapter IV.</b> <a href="ch011.xhtml">The argument from the covenant of grace</a></p>
<p class="contents-item"><b>Chapter V.</b> <a href="ch012.xhtml">Argument from the promises of God</a></p>
<p class="contents-item"><b>Chapter VI.</b> <a href="ch013.xhtml">Particular promises illustrated</a></p>
<p class="contents-item"><b>Chapter VII.</b> <a href="ch014.xhtml">The mediation of Christ</a></p>
<p class="contents-item"><b>Chapter VIII.</b> <a href="ch015.xhtml">The indwelling of the Spirit</a></p>
<p class="contents-item"><b>Chapter IX.</b> <a href="ch016.xhtml">The intercession of Christ</a></p>
<p class="contents-item"><b>Chapter X.</b> <a href="ch017.xhtml">The improvement of the doctrine</a></p>
<p class="contents-item"><b>Chapter XI.</b> <a href="ch018.xhtml">Arguments against the doctrine considered</a></p>
<p class="contents-item"><b>Chapter XII.</b> <a href="ch019.xhtml">Objections to the doctrine refuted</a></p>
<p class="contents-item"><b>Chapter XIII.</b> <a href="ch020.xhtml">The assertors and adversaries of the doctrine compared</a></p>
<p class="contents-item"><b>Chapter XIV.</b> <a href="ch021.xhtml">Argument against the doctrine from the apostasy of the saints</a></p>
<p class="contents-item"><b>Chapter XV.</b> <a href="ch022.xhtml">Argument against the doctrine from the sins of believers</a></p>
<p class="contents-item"><b>Chapter XVI.</b> <a href="ch023.xhtml">The bearing of the doctrine of the saints' perseverance on their peace and holiness</a></p>
<p class="contents-item"><b>Chapter XVII.</b> <a href="ch024.xhtml">A review of passages in Scripture alleged against the perseverance of the saints</a></p>
</section>'''

def post_extract_hook(intermediate: dict) -> dict:
    """Post-extraction adjustments for Volume 11."""
    # Move the prefix text of ch003 to the end of ch002
    ch002 = next((c for c in intermediate.get('chapters', []) if c['cid'] == 'ch002'), None)
    ch003 = next((c for c in intermediate.get('chapters', []) if c['cid'] == 'ch003'), None)
    if ch002 and ch003:
        prefix_to_move = (
            'Goodwin;" and Mr. John Pawson, in a sermon under the title of "A Vindication of Free Grace."\n\n'
            'In 1658 Goodwin replied to most of these publications in a quarto of five hundred pages, entitled "Triumviri," etc. In regard to the following treatise, "he returns," says Owen, in an epistle dedicatory to his work on the Divine Original of the Scriptures, "a scoffing reply to so much of it as was written in a quarter of an hour."'
        )
        if ch003['raw_text'].startswith(prefix_to_move):
            # Append to ch002 (keeping space or newline)
            ch002['raw_text'] = ch002['raw_text'].rstrip() + " " + prefix_to_move
            # Remove from ch003
            ch003['raw_text'] = ch003['raw_text'][len(prefix_to_move):].lstrip()
    return intermediate


OVERRIDES = {
    'post_extract_hook': post_extract_hook,
    'contents_page_overrides': _V11_CONTENTS_PAGE,
    'front_matter_overrides': {
        'Contents': _V11_CONTENTS_PAGE,
    },
    'treatise_title_overrides': {
        # Key matches the OCR-corrupted JSON title (no apostrophe)
        'The Doctrine of the Saints Perseverance': _V11_PERSEVERANCE_TITLE_PAGE,
    },
    'text_replacements': {
        # Repair missing apostrophe where it appears in body text
        "Saints Perseverance": "Saints' Perseverance",
        "saints perseverance": "saints' perseverance",
        "packed in in a": "packed in a",
        "Noah is is said": "Noah it is said",
        "upon it it should": "upon it, it should",
        "intercedes for for believers": "intercedes for, for believers",
        "cometh in in the": "cometh in the",
        "without it it will": "without it, it will",
        "whom it is is tempted": "whom it is, is tempted",
        "walk in in reference": "walk in, in reference",
        "tendency of it it is": "tendency of it, it is",
        "put in in our behalf": "put in, in our behalf",
        "brought in in this place": "brought in, in this place",
        # OCR and hyphenation errors
        "Hebrews 42:5": "Hebrews 13:5",
        "John 41:31": "John 12:31",
        "figurasLaudatur": "figuras laudatur",
        "semiPelagians": "semi-Pelagians",
        "solvi[to]": "solvite",
        "Pela-gins": "Pelagius",
        "exer-citatus": "exercitatus",
        "Calvinis-mum": "Calvinismum",
        "multitu-dinis": "multitudinis",
        "praedestina-tionis": "praedestinationis",
        "I-chabod": "Ichabod",
        "interveni-nces": "interveniences",
    },
}


def main():
    run_volume_cli(VOL, overrides=OVERRIDES)


if __name__ == '__main__':
    main()

