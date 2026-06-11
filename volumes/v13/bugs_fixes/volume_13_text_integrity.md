# Text Integrity Audit: Volume 13

- Status: **WARN**
- Warnings: 13
- PDF pages: 749
- EPUB text files: 84
- EPUB paragraphs/headings: 2253

## Coverage

- PDF content tokens: 250067
- EPUB content tokens: 250552
- Approximate PDF-to-EPUB coverage ratio: 0.9957
- Pages checked: 737
- Weak page matches: 8
- Dense source windows checked: 33508
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 2
- Top-of-page body windows checked: 720
- Top-of-page windows skipped as unstable: 8
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 679
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 1

## Paragraphs

- Body paragraphs checked: 1810
- Possible faulty paragraph splits: 29
- Structural starts excluded from split warnings: 112
- Short fragments: 37
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 13
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 4
- Roman heading candidates: 4
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 80
- EPUB enumerator markers: 92
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1046
- EPUB Greek words: 1058
- Greek word coverage ratio: 0.9922
- PDF Hebrew words: 12
- EPUB Hebrew words: 12
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 59
- Missing Greek clauses: 0
- Hebrew clauses checked: 0
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 3056
- EPUB Latin words: 3102
- EPUB Tagged Latin words: 1652
- Latin word coverage ratio: 0.9935
- Latin word tagging ratio: 0.5326
- Latin clauses checked: 210
- Missing Latin clauses: 0
- Tagged Latin runs checked: 409
- Translated Latin runs: 173
- Latin translation ratio: 0.423

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans
- `low_latin_translation_coverage`: Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py

## Missing Dense Source Windows

- page: 3; sample: contents of the duty of pastors and people distinguished preface of the administration of
- page: 4; sample: of schism aggravations of the evil of schism from the authority of the ancients
- page: 5; sample: of schism the ground of sin and disorder objections against the former discourse proposed
- page: 6; sample: their apostasy proved by instances their grand argument in this case proposed answered consequences
- page: 7; sample: of elijah the last objection waived inferences upon the whole review of the true
- page: 8; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory
- page: 9; sample: alleged evils from the free exercise of conscience charges of parker against noncomformists mischief
- page: 11; sample: the duty of pastors and people distinguished or brief discourse touching the administration of
- page: 12; sample: and independency he afterwards changed his views on church government but in the work
- page: 14; sample: to the truly noble and my ever honored friend sir edward scot of scot's

## Missing Front CONTENTS Pages

- page: 3; hit_ratio: 0.25; sample: contents of the duty of pastors and people distinguished preface of the administration of holy things among the patriarchs before the law of the same among the jews
- page: 8; hit_ratio: 0.5; sample: an answer etc brief vindication of the nonconformists from the charge of schism prefatory note by the editor brief vindication etc truth and innocence vindicated prefatory note by

## Missing Top-Of-Page Body Windows

- page: 8; sample: An Answer, etc., A BRIEF VINDICATION OF THE NONCONFORMISTS FROM
- page: 14; sample: TO THE TRULY NOBLE AND MY EVER HONORED FRIEND, SIR EDWARD SCOT,

## Missing Bottom-Of-Page Body Windows

- page: 9; sample: PREFATORY NOTE BY THE EDITOR, The Grounds and Reasons, etc.,

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: ays of mercy and grace which are necessary to carry you along through all your engagements, until you arrive at the haven of everlasting glory, where you would be. I rest your most; next: obliged servant in Jesus Christ, our common Master
- file: EPUB/ch003.xhtml; previous: obliged servant in Jesus Christ, our common Master; next: John Owen
- file: EPUB/ch011.xhtml; previous: From these and the like places it appears to me, that, —; next: There is a general obligation on all Christians to promote the conversion and instruction of sinners, and men erring from the right way.
- file: EPUB/ch011.xhtml; previous: At least, we may deduce from them, by the way of analogy, that, —; next: Whatsoever necessary truth is revealed to any out of the word of God, not before known, he ought to have an uncontradicted liberty of declaring that truth, provided that he use suc
- file: EPUB/ch011.xhtml; previous: Whence.it appears, that, —; next: Truth revealed unto any carries along with it an unmovable persuasion of conscience (which is powerfully obligatory) that it ought to be published and spoken to others.
- file: EPUB/ch011.xhtml; previous: ved, yet a right belief whereof is necessary to salvation; and, farther, out of the same word shall discover unto him the wickedness of that apostasy, and the means to remove it, —; next: I demand whether that man, without expecting any call from the fomenters and maintainers of those errors with which the church at that time is only not destroyed, may not preach, p
- file: EPUB/ch012.xhtml; previous: easily discernible both what the people of God, distinct from their pastors, in a well-ordered church, may do in this kind whereof we treat, and how. In general, then, I assert, —; next: That, for the improving of knowledge, the increasing of Christian charity, for the furtherance of a strict and holy communion of that spiritual love and amity which ought to be amo
- file: EPUB/ch012.xhtml; previous: ll, they have not an equal respect unto all God's ordinances. Wherefore, that the coming together in this sort may be for the better, and not for the worse, observe these things: —; next: Now, for what gifts (that are, as before, freely bestowed) whose exercise is permitted unto such men so assembled; I mean in a private family, or two or three met ὁμοθμυαδόν , in o
- file: EPUB/ch012.xhtml; previous: , with opening my desire for the increasing of knowledge among the people, of which I take this to be an effectual means, yet I will give brief answers to the several objections: —; next: Objection 1. "Then this seems to favor all allowance of licentious conventicles, which in all places the laws have condemned, and learned men in all ages have abhorred, as the semi
- file: EPUB/ch015.xhtml; previous: To The Reader; next: THERE are, Christian reader, certain principles in church affairs generally consented unto by all men aiming at reformation and the furtherance of the power of godliness therein, h

## Inline Structural Marker Candidates

- file: EPUB/ch009.xhtml; text: Now, three ways may a man receive, and be assured that he hath received, this divine mission, or know that he is called of God to the preaching of the word; I mean not that persuasion of divine concurrence which is necessary also for the...
- file: EPUB/ch016.xhtml; text: Motives to the observance of this rule are: — 1. The name wherein they speak and administer, 2 Corinthians 5:20. 2. The work which they do, 1 Corinthians 3:9; 2 Corinthians 6:1; Timothy 4:16. 3. The return that they make, Hebrews 8:1 8:1...
- file: EPUB/ch016.xhtml; text: Explication III. The greatness of the work (for which who is sufficient? 2 Corinthians 2:16); — the strength of the opposition which lies against it, 1 Corinthians 16:9; Revelation 12:12; 2 Timothy 4:3-5; — the concernment of men's souls...
- file: EPUB/ch016.xhtml; text: Let motives hereunto be, — 1. God's command. 2. Our own preservation from sin and protection from punishment, that with others we be not infected and plagued. 3. Christ's delight in the purity of his ordinances. 4. His distinguishing lov...
- file: EPUB/ch016.xhtml; text: Now, to a right performance of this duty, and in the discharge of it, are required, — 1. A due valuation, strong desire, and high esteem of the church's prosperity, in every member of it, Psalm 122:6. 2. Bowels of compassion as a fruit o...
- file: EPUB/ch016.xhtml; text: Motives to this duty are: — 1. The love of God unto us, 1 John 3:16. 2. The glory of the gospel, exceedingly exalted thereby, Titus 3:8,14; Matthew 5:7. 3. The union whereinto we are brought in Christ, with the common inheritance promise...
- file: EPUB/ch016.xhtml; text: Now, to a close adhering to the church wherein we walk in fellowship, in all conditions whatsoever, without dismission attained upon just and equitable grounds, for the embracing of communion in some other churches. Motives are, — 1. The...
- file: EPUB/ch016.xhtml; text: Motives hereunto are, — 1. Christ's example; 2. Scripture precepts; 3. God's not accepting persons; 4. Joint participation of the same common faith, hope, etc; 5. The unprofitableness of all causes of outward differences in the things of...
- file: EPUB/ch016.xhtml; text: Now, admonition is twofold: — 1. Authoritative, by the way of power; 2. Fraternal, by the way of love. The first, again, is twofold: —
- file: EPUB/ch016.xhtml; text: These and the like things being duly weighed, let every brother, with Christian courage, admonish from the word every one whom he judgeth to walk disorderly in any particular whatsoever, not to suffer sin upon him, being ready to receive...

## Suspicious Large-Number Starts

- file: EPUB/ch005.xhtml; text: 12. ae. quest.
- file: EPUB/ch022.xhtml; text: 10. I no way doubt of the perpetual existence of innumerable believers in every age, and such as made the profession that is absolutely necessary to salvation, one way or other, though I question a regular association of
- file: EPUB/ch022.xhtml; text: 22. In what sense this church is visible was before declared. Men elected, redeemed, justified, as such, are not visible, for that which makes them so is not; but this hinders not but they may be so upon the other consid
- file: EPUB/ch023.xhtml; text: 29. There being, then, in the world a great multitude, which no man can number, of all nations, kindreds, people, and language, professing the doctrine of the gospel, not tied to mountains or hills, John 4:21, 23, but wo

## Roman Heading Candidates

- file: EPUB/ch030.xhtml; text: C. hardly refrain from calling a man Satan for speaking the truth? It is well if we know of what Spirit we are.
- file: EPUB/ch032.xhtml; text: C. knows how easy it were to make his own words dress him up in all those ornaments wherein he labors to make me appear in the world, by such glosses, inversions, additions, and interpositions, as he is pleased to make u
- file: EPUB/ch039.xhtml; text: C. himself is bound to come into it, and yet I do not think that his not so doing makes him a schismatic; and as for relinquishment, I assert no more than what he himself concludes to be lawful. And thus, Christian reade
- file: EPUB/ch059.xhtml; text: IV. The payment of tithes, —

## Short Fragments

- file: EPUB/ch002.xhtml; text: M AY 11, 1644.
- file: EPUB/ch002.xhtml; text: JOSEPH CARYL.
- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch007.xhtml; text: and again,
- file: EPUB/ch007.xhtml; text: Whence I conclude, —
- file: EPUB/ch011.xhtml; text: to which add that of the apostle,
- file: EPUB/ch011.xhtml; text: Whence.it appears, that, —
- file: EPUB/ch012.xhtml; text: Τῷ Θεῷ ἀριστομεγίστῳ δόζα .
- file: EPUB/ch015.xhtml; text: To The Reader
- file: EPUB/ch016.xhtml; text: 2 Thessalonians 3:1,2,

## Enumerator Sequence Candidates

- file: EPUB/ch023.xhtml; marker: (2.); family: paren_decimal; context: (2.) That doing so, in the course of our lives we manifest and declare a principle that is utterly inconsistent with the belief of those truths which outwardly we profess; or, —
- file: EPUB/ch042.xhtml; marker: [16]; family: bracket_decimal; context: Nor did I, as is pretended, plead for their presbyterian way in the year [16]46; all the ministers almost in the county of Essex know the contrary, one especially, being a man of great ability and moderation of spirit, and for his knowle...

## Repeated Windows

- phrase: brief vindication of the nonconformists from the charge of schism; count: 3
- phrase: an account of the grounds and reasons on which protestant; count: 3
- phrase: account of the grounds and reasons on which protestant dissenters; count: 3
- phrase: of the grounds and reasons on which protestant dissenters desire; count: 3
- phrase: the lion hath roared who will not fear the lord; count: 3
- phrase: lion hath roared who will not fear the lord god; count: 3
- phrase: hath roared who will not fear the lord god hath; count: 3
- phrase: roared who will not fear the lord god hath spoken; count: 3
- phrase: who will not fear the lord god hath spoken who; count: 3
- phrase: will not fear the lord god hath spoken who can; count: 3

## Missing Word Samples

- word: self; pdf: 13; epub: 6
- word: fellow; pdf: 3; epub: 0
- word: re; pdf: 3; epub: 1

## Excess Word Samples

- word: ii; pdf: 15; epub: 31
- word: volume; pdf: 6; epub: 18
- word: digital; pdf: 0; epub: 10
- word: theological; pdf: 0; epub: 9
- word: historical; pdf: 0; epub: 8
- word: modern; pdf: 5; epub: 12
- word: greek; pdf: 2; epub: 9
- word: footnotes; pdf: 0; epub: 7
- word: bill; pdf: 7; epub: 13
- word: conventicle; pdf: 5; epub: 11

## Untagged Latin Word Samples

- word: magistrate; epub: 232; tagged: 1
- word: dissent; epub: 70; tagged: 0
- word: relate; epub: 21; tagged: 0
- word: door; epub: 17; tagged: 0
- word: ago; epub: 16; tagged: 0
- word: pleas; epub: 15; tagged: 0
- word: iii; epub: 14; tagged: 0
- word: tract; epub: 14; tagged: 0
- word: nowhere; epub: 14; tagged: 0
- word: superior; epub: 15; tagged: 1

## Untranslated Latin Samples

- phrase: Medio tutissimus
- phrase: Sixtus Senensis
- phrase: in causa facili
- phrase: bonum oritur ex integris
- phrase: prophetae de Christo quam de ecclesia: puto propterea quia
- phrase: contra ecclesiam
- phrase: facturos esse particulas; et de Christo non tantam
- phrase: habituros, de ecclesia magnas
- phrase: non qua itur, sed qua eundum est
- phrase: Consuetudo sine veritate est vetustas erroris

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
