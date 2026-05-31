# Text Integrity Audit: Volume 3

- Status: **WARN**
- Warnings: 9
- PDF pages: 789
- EPUB text files: 44
- EPUB paragraphs/headings: 2500

## Coverage

- PDF content tokens: 282216
- EPUB content tokens: 278672
- Approximate PDF-to-EPUB coverage ratio: 0.9855
- Pages checked: 787
- Weak page matches: 13
- Dense source windows checked: 812
- Missing dense source-window pages: 783
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 766
- Top-of-page windows skipped as unstable: 31
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 748
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 5

## Paragraphs

- Body paragraphs checked: 2114
- Possible faulty paragraph splits: 152
- Structural starts excluded from split warnings: 317
- Short fragments: 12
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 12
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 626
- EPUB enumerator markers: 636
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 809
- EPUB Greek words: 816
- Greek word coverage ratio: 0.9949
- PDF Hebrew words: 238
- EPUB Hebrew words: 235
- Hebrew word coverage ratio: 0.9874
- Greek clauses checked: 42
- Missing Greek clauses: 0
- Hebrew clauses checked: 23
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `flat_analysis_chapters`: 1 ANALYSIS chapter(s) appear under-structured — fewer outline markers than expected. Check extraction quality for these chapters.

## Missing Dense Source Windows

- page: 3; sample: contents of πνευματολογια discourse concerning the holy spirit prefatory note by the editor to
- page: 4; sample: open vanity of their pretenses matthew 28 19 pleaded appearance of the spirit under-the
- page: 5; sample: of god and his glory how this revelation is made in particular herein work
- page: 6; sample: book work of the holy spirit in the new creation by regeneration the new
- page: 7; sample: the distinct faculties of the soul the mind the will the affections the manner
- page: 8; sample: the filth of sin puroed by the spirit and blood of christ purification of
- page: 9; sample: of christ as applied by the holy spirit into the mortification of sin book
- page: 10; sample: 10 πνευματολογια or discourse concerning the holy spirit wherein an account is given of
- page: 11; sample: 11 prefatory note the year 1674 saw issuing from the press some of the
- page: 12; sample: 12 books embraced in this volume to all of them the general designation πνευματολογια

## Missing Bottom-Of-Page Body Windows

- page: 206; sample: operation of the Holy Ghost, it seems purposely to be hid from us in that expression, Du>namis Uyi>stou ejpiskia>sei soi, — "The power of the
- page: 318; sample: yucikou>v, "natural men," but rather a]logs zw~a fusika>, 2 Peter 2:12,
- page: 320; sample: spiritual things is doubly expressed: — [1.] By ouj de>cetai, — "He receiveth them not;"
- page: 537; sample: fountain opened for sin and uncleanness," Zechariah 13:1. And he who
- page: 706; sample: glory, that therein we shall be ijsa>ggeloi, Luke 20:36, like or "equal

## Possible Paragraph Splits

- file: EPUB/ch006.xhtml; previous: anions, saying, "These men are the servants of the most high God," Acts 16:17. So also did the man who abode in the tombs, possessed with an unclean spirit, who cried out unto him,; next: And other testimonies to the like purpose among the heathen, and from their oracles, might be produced.
- file: EPUB/ch006.xhtml; previous: great importance, he repeats it frequently unto them, and inculcates it upon them. Consider somewhat of what he says to this purpose in his last discourse with them: John 14:16-18,; next: whom the world cannot receive, because it seeth him not, neither knoweth him: but ye know him; for he dwelleth with you, and shall be in you. I will not leave you comfortless: I wi
- file: EPUB/ch006.xhtml; previous: John 20:17, to wean her from any carnal consideration of him, so he instructs them all now to look after and trust unto the promise of the Holy Ghost. Hence is that of our apostle,; next: for although it was a great privilege to have known Christ in this world after the flesh, yet it was much greater to enjoy him in the dispensation of the Spirit. And this was spoke
- file: EPUB/ch006.xhtml; previous: nstructed in what concerns him; for there is somewhat that doth so, which is accompanied with irrecoverable and eternal ruin; and so is nothing else in the world. So Mark 3:28, 29,; next: Or, "Whosoever speaketh against the Holy Ghost, it shall not be forgiven him, neither in this world, neither in the world to come," Matthew 12:32.
- file: EPUB/ch006.xhtml; previous: pleaded in its justification, it is to be rejected, as they also are by whom it is declared. This rule the apostle Paul confirms by the highest instance imaginable: Galatians 1:8,; next: And the apostle shows that, for our advantage in this trial we are to make of spirits, it is good to have a clear conviction of, and a constant adherence unto, some fundamental pri
- file: EPUB/ch007.xhtml; previous: :8, "God walked in the garden" לְרוּחַ הַיוֹם , "in the cool of the day;" that is, when the evening air began to breathe gently, and moderate the heat of the day. So in the poet, —; next: "At the going down of the sun, when the cold evening tempers the heat of the air." And some think this to be the sense of that place, Psalm 104:4, "Who maketh his angels רוּחוֹת ,
- file: EPUB/ch007.xhtml; previous: "establishing the thunder;" and yet, when he hath done all, he can scarce free himself of the objection about the creation of the Spirit, which he designs to answer. His words are,; next: And hereon, with some observations to the same purpose, he adds,
- file: EPUB/ch007.xhtml; previous: And hereon, with some observations to the same purpose, he adds,; next: The substance of his discourse is, that treating of Christ (who indeed is neither mentioned nor intended in the text), he speaks of "confirming the thunder" (which nowhere here app
- file: EPUB/ch007.xhtml; previous: The other person intended is Hierom, who, consulting the original, as he was well able to do, first translated the words,; next: declares the mistake of the LXX. and the occasion of it: —
- file: EPUB/ch007.xhtml; previous: declares the mistake of the LXX. and the occasion of it: —; next: So he shows that it is not מְשִׁיחוֹ in the text, but מַה־צִיחוֹ ; — that is, saith he,

## Inline Structural Marker Candidates

- file: EPUB/ch012.xhtml; text: Not that God intended much to make use of this way of dreams and nocturnal visions under the New Testament; but the intention of the words is, to show that there should be a plentiful effusion of that Spirit which acted by these various ...
- file: EPUB/ch016.xhtml; text: That spirit which revealeth anything, or pretendeth to reveal anything, any doctrine, any grace, any truth, that is contrary unto, that is not consonant to, yea, that is not the doctrine, grace, or truth of Christ, as now revealed in the...
- file: EPUB/ch020.xhtml; text: Some, indeed, give such an account of this text as if the apostle had said, "Do not ye live after the manner of the heathens, in the vileness of those practices, and in their idol-worship. That long course of sin having blinded their und...
- file: EPUB/ch028.xhtml; text: This uncleanness as it is habitual, respecting our natural defilement, is equal in and unto every one that is born into the world; we are by nature all alike polluted, and that to the utmost of what our nature is capable. But with respec...
- file: EPUB/ch030.xhtml; text: It is by all confessed that examples are most effectual ways of instruction, and, if seasonably proposed, do secretly solicit the mind unto imitation, and almost unavoidably incline it thereunto. But when unto this power which examples h...

## Overlong Heading Candidates

- file: EPUB/ch012.xhtml; tag: h4; text: I. 1. The first eminent gift and work of the Holy Ghost under the Old Testament, and which had the most direct and immediate respect unto Jesus Christ, was that of _prophecy:_ for the chief and principal end hereof in the church was to f...
- file: EPUB/ch012.xhtml; tag: h4; text: II. The next sort of the operations of the Holy Ghost under the Old Testament, whose explanation was designed, is of those whereby he improved, through immediate impressions of his own power, the natural faculties and abilities of the mi...
- file: EPUB/ch014.xhtml; tag: h4; text: I. But yet, before we enter upon the first sort of his works which we shall begin withal, an objection of seeming weight and difficulty must be removed out of our way; which I shall the rather do because our answer unto it will make the ...
- file: EPUB/ch015.xhtml; tag: h4; text: II. There is yet another work of the Holy Spirit, not immediately in and upon the person of the Lord Christ, but _towards him,_ and on his behalf, with respect unto his work and office; and it compriseth the head and fountain of the whol...
- file: EPUB/ch029.xhtml; tag: h4; text: I. That we are purged and purified from sin by the Spirit of God communicated unto us hath been before in general confirmed by many testimonies of the holy Scriptures.
- file: EPUB/ch029.xhtml; tag: h4; text: II. It is, therefore, the _blood of Christ,_ in the second place, which is the _meritorious_ procuring, and so the effective cause, that _immediately purgeth_ us from our sins, by an especial application of it unto our souls by the Holy ...
- file: EPUB/ch030.xhtml; tag: h4; text: I. The first of these assertions I affirm not only to be true, but of so great weight and importance that our hope of life and salvation depends thereon; and it is the second great principle constituting our Christian profession.
- file: EPUB/ch031.xhtml; tag: h4; text: II. THE second part of the work of the Spirit of God in our sanctification respects the acts and duties of holy obedience; for what we have before treated of chiefly concerns the principle of it as habitually resident in our souls, and t...
- file: EPUB/ch034.xhtml; tag: h4; text: I. First, then, The nature of God as revealed unto us, with our dependence on him, the obligation that is upon us to live unto him, with the nature of our blessedness in the enjoyment of him, do require indispensably that we should be holy.
- file: EPUB/ch036.xhtml; tag: h4; text: III. WE have evinced the necessity of holiness from the nature and the decrees of God; our next argument shall be taken from his word or commands, as the nature and order of these things do require.

## Short Fragments

- file: EPUB/ch007.xhtml; text: — and the Spirit of Christ:
- file: EPUB/ch008.xhtml; text: The other is chapter 20:28,
- file: EPUB/ch016.xhtml; text: and verse 8,
- file: EPUB/ch020.xhtml; text: And another:
- file: EPUB/ch023.xhtml; text: This again he repeats, cap. 7:
- file: EPUB/ch023.xhtml; text: So saith the same person,
- file: EPUB/ch023.xhtml; text: And a little after,
- file: EPUB/ch025.xhtml; text: Yea, —
- file: EPUB/ch027.xhtml; text: Ans.
- file: EPUB/ch032.xhtml; text: Now, this the Holy Ghost doth, —

## Enumerator Sequence Candidates

- file: EPUB/ch006.xhtml; marker: [18]; family: bracket_decimal; context: before them, — namely, the old scoffing heathens; for so doth Lucian, in his Philopatris [18], speak in imitation of a Christian by way of scorn, Λέγε παρὰ τοῦ Πνεύματος δύναμιν τοῦ λόγου λαβών — "Speak out now, receiving power or abilit...
- file: EPUB/ch030.xhtml; marker: [2dly.]; family: bracket_ordinal; context: [2dly.] Salvation, or deliverance from sin and punishment. "Look unto me," saith he, "and be ye saved."
- file: EPUB/ch030.xhtml; marker: (3.); family: paren_decimal; context: (3.) The immediate efficient cause of all gospel holiness is the Spirit of God. This we have sufficiently proved already. And although many cavils have been raised against the manner o
- file: EPUB/ch032.xhtml; marker: (3.); family: paren_decimal; context: (3.) That which remains farther to be demonstrated is, that the Holy Spirit is the author of this work in us, so that although it is our duty, it is his grace and strength whereby it i

## Repeated Windows

- phrase: both to will and to do of his good pleasure; count: 7
- phrase: the name of the father and of the son and; count: 6
- phrase: in us both to will and to do of his; count: 6
- phrase: us both to will and to do of his good; count: 6
- phrase: name of the father and of the son and of; count: 5
- phrase: of the father and of the son and of the; count: 5
- phrase: the father and of the son and of the holy; count: 5
- phrase: father and of the son and of the holy ghost; count: 5
- phrase: the new man which after god is created in righteousness; count: 5
- phrase: new man which after god is created in righteousness and; count: 5

## Missing Word Samples

- word: self; pdf: 14; epub: 6

## Excess Word Samples

- word: digital; pdf: 0; epub: 8
- word: ii; pdf: 6; epub: 13
- word: iii; pdf: 2; epub: 8
- word: iv; pdf: 2; epub: 8

## Flat ANALYSIS Chapters

**1 ANALYSIS chapter(s)** appear under-structured — fewer outline markers than expected.  Extraction may have failed to parse the outline.

## Flat Analysis Details

- file: EPUB/contents_2.xhtml; paragraph_count: 37; structural_line_count: 0; note: ANALYSIS chapter appears flat — fewer structural outline lines than expected. Check extraction quality.

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
