# Text Integrity Audit: Volume 3

- Status: **WARN**
- Warnings: 8
- PDF pages: 789
- EPUB text files: 45
- EPUB paragraphs/headings: 2507

## Coverage

- PDF content tokens: 282216
- EPUB content tokens: 278727
- Approximate PDF-to-EPUB coverage ratio: 0.9851
- Pages checked: 787
- Weak page matches: 15
- Dense source windows checked: 812
- Missing dense source-window pages: 783
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 766
- Top-of-page windows skipped as unstable: 31
- Missing top-of-page body windows: 0
- Bottom-of-page body windows checked: 748
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 6

## Paragraphs

- Body paragraphs checked: 2116
- Possible faulty paragraph splits: 153
- Structural starts excluded from split warnings: 319
- Short fragments: 13
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 0
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 626
- EPUB enumerator markers: 708
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 23

## Greek / Hebrew

- PDF Greek words: 809
- EPUB Greek words: 815
- Greek word coverage ratio: 0.9936
- PDF Hebrew words: 238
- EPUB Hebrew words: 238
- Hebrew word coverage ratio: 0.9454
- Greek clauses checked: 42
- Missing Greek clauses: 0
- Hebrew clauses checked: 23
- Missing Hebrew clauses: 3

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB

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

- page: 129; sample: 2. The quickening principle added thereunto; and, 3. The effect of their conjunction and union.
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
- file: EPUB/ch007.xhtml; previous: God walked in the garden" לְ רוּחַ [6] הַיוֹם , "in the cool of the day;" that is, when the evening air began to breathe gently, and moderate the heat of the day. So in the poet, —; next: "At the going down of the sun, when the cold evening tempers the heat of the air." And some think this to be the sense of that place, Psalm 104:4, "Who maketh his angels רוּחוֹת ,
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
- file: EPUB/ch027.xhtml; text: And, —

## Enumerator Sequence Candidates

- file: EPUB/ch006.xhtml; marker: [3]; family: bracket_decimal; context: discourse declare: Verse 1, "Now, concerning spiritual gifts," — Περὶ δὲ τῶν πνευματικῶν [3] that is χαρισμάτων as his ensuing declaration doth evince. And the imagination of some, concerning spiritual persons to be here intended, contra...
- file: EPUB/ch006.xhtml; marker: [8]; family: bracket_decimal; context: e which he proposed to treat of, and had done so accordingly, verse 31. The τὰ πνευματικὰ [8] of verse 1 are the τὰ χαρίσματα [9] of verse 31; as it is expressed, chap. 14:1, Ζηλοῦτε δὲ τὰ πνευματικά [2] — that is, χαρίσματα , — "'Desire...
- file: EPUB/ch006.xhtml; marker: [12]; family: bracket_decimal; context: pronunciation of his name: for instead of יֵשׁוּעַ [10] , they write and call him יֵשׁוּ [12] , the initial letters of יִמַח שְׁמוֹ וְזִכְרוֹ , — that is, "Let his name and memory be blotted out;" the same with "Jesus anathema" And this ...
- file: EPUB/ch006.xhtml; marker: [6]; family: bracket_decimal; context: Treating, therefore, περὶ τῶν πνευματικῶν [6] , of these spiritual things or gifts in the church, he first declares their author, from whom they come, and by whom they are wrought and bestowed. Him he calls the "Spirit," vers
- file: EPUB/ch006.xhtml; marker: [18]; family: bracket_decimal; context: before them, — namely, the old scoffing heathens; for so doth Lucian, in his Philopatris [18], speak in imitation of a Christian by way of scorn, Λέγε παρὰ τοῦ Πνεύματος δύναμιν τοῦ λόγου λαβών — "Speak out now, receiving power or abilit...
- file: EPUB/ch007.xhtml; marker: [5]; family: bracket_decimal; context: Of the name of the Holy Spirit — Various uses of the words יוּחַ [5] and πνεῦμα — יוּחַ [5] for the wind or anything invisible with a sensible agitation, Amos 4:13 — Mistakes of the ancients rectified by Hierom רוּח metaphorically for va...
- file: EPUB/ch007.xhtml; marker: [5]; family: bracket_decimal; context: Of the name of the Holy Spirit — Various uses of the words יוּחַ [5] and πνεῦμα — יוּחַ [5] for the wind or anything invisible with a sensible agitation, Amos 4:13 — Mistakes of the ancients rectified by Hierom רוּח metaphorically for va...
- file: EPUB/ch007.xhtml; marker: [3]; family: bracket_decimal; context: ense, sometimes it signifies a "great and strong wind," — that is, רוּחַ נְדוֹלָה וְחָזָק [3] , 1 Kings 19:11; and sometimes a cool and soft wind, or a light easy agitation of the air, such as often ariseth in the evenings of the spring ...
- file: EPUB/ch007.xhtml; marker: [6]; family: bracket_decimal; context: appellation of him in the New Testament; and it is derived from the Old: Psalm 51, רוּחַ [6] קָדְשְׁך , "The Spirit of thy Holiness," or "Thy Holy Spirit" Isaiah 63:10, 11, רוּחַ [6] קָדְשׁוֹ , "The Spirit of his Holiness," or "His Holy ...
- file: EPUB/ch007.xhtml; marker: [6]; family: bracket_decimal; context: [6] קָדְשְׁך , "The Spirit of thy Holiness," or "Thy Holy Spirit" Isaiah 63:10, 11, רוּחַ [6] קָדְשׁוֹ , "The Spirit of his Holiness," or "His Holy Spirit." Hence are רוּחַ [6] הַקָּדוֹשׁ and רוּחַ [6] הַקֹּדֶשׁ , "The Holy Spirit," and ...

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

- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 9; epub: 18
- word: greek; pdf: 1; epub: 9
- word: ii; pdf: 6; epub: 13
- word: hebrew; pdf: 2; epub: 9
- word: edition; pdf: 3; epub: 9
- word: iii; pdf: 2; epub: 8
- word: iv; pdf: 2; epub: 8
- word: footnotes; pdf: 0; epub: 6

## Missing Hebrew Word Samples

- word: לְרוּחַ; pdf: 2; epub: 0

## Missing Hebrew Clauses

- page: 80; word_count: 3; sample: רוּחַ־רָעָה מֵאֵת יְהוָֹה
- page: 109; word_count: 5; sample: שַׁדַּי תְחַיֵנִי רוּחַ־אֵל עָצָתְנִי וְנִשְׁמַת
- page: 130; word_count: 3; sample: רֹאצ עַפְרוֹת חֵבֵל

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
