# Text Integrity Audit: Volume 16

- Status: **WARN**
- Warnings: 11
- PDF pages: 672
- EPUB text files: 81
- EPUB paragraphs/headings: 2684

## Coverage

- PDF content tokens: 219816
- EPUB content tokens: 219888
- Approximate PDF-to-EPUB coverage ratio: 0.9959
- Pages checked: 662
- Weak page matches: 11
- Dense source windows checked: 741
- Missing dense source-window pages: 653
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 631
- Top-of-page windows skipped as unstable: 34
- Missing top-of-page body windows: 5
- Bottom-of-page body windows checked: 605
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 6

## Paragraphs

- Body paragraphs checked: 2331
- Possible faulty paragraph splits: 28
- Structural starts excluded from split warnings: 280
- Short fragments: 17
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 8
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 3
- Roman heading candidates: 1
- Overlong heading candidates: 1
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 509
- EPUB enumerator markers: 532
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 2

## Greek / Hebrew

- PDF Greek words: 1037
- EPUB Greek words: 1039
- Greek word coverage ratio: 0.993
- PDF Hebrew words: 268
- EPUB Hebrew words: 266
- Hebrew word coverage ratio: 0.9901
- Greek clauses checked: 51
- Missing Greek clauses: 0
- Hebrew clauses checked: 19
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 3; sample: publishers note to 1968 reprint of volume sixteen the goold edition of john owen's
- page: 6; sample: formerly asserted by others reasons of the opposition made to them of the putty
- page: 7; sample: text the most probable instants considered of various lections in the greek copies of
- page: 8; sample: cause the concision about the necessity of the points of the קְרִי וּכְתִיב their
- page: 9; sample: faith's answer to divine reproofs habakkuk 1-4 spiritual strength its reality decay and renovation
- page: 10; sample: 10 the true nature of gospel church and its government the second part wherein
- page: 11; sample: 11 prefatory note on the ground of some statements in the following treatise which
- page: 12; sample: 12 evidence that in his last days he was more of presbyterian than an
- page: 13; sample: 13 no recantation of the principle so copiously urged in the former that the
- page: 14; sample: 14 the preface to the reader the church of christ according as it is

## Missing Top-Of-Page Body Windows

- page: 3; sample: PUBLISHERS' NOTE TO 1968 REPRINT OF VOLUME SIXTEEN
- page: 9; sample: 3. — Faith's answer to divine reproofs. — Habakkuk 2:1-4, 4. — Spiritual strength; — its reality, decay, and renovation.
- page: 43; sample: CHAPTER 2. OF THE FORMAL CAUSE OF A PARTICULAR CHURCH.
- page: 333; sample: OF INFANT BAPTISM AND DIPPING. OF INFANT BAPTISM.
- page: 363; sample: TO MY REVEREND AND WORTHY FRIENDS, THE PREBENDS OF CHRIST CHURCH COLLEGE

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 311; sample: published in the folio volume of "Sermons and Tracts" by Owen, which was printed in 1721. — ED.
- page: 365; sample: of it (which how vast and extensive it is no man knows; — for the Jews have given us their deuterw>seiv in their Mishna and Gemara; these kept
- page: 372; sample: Rabbins; and the other, that without them the understanding of the Hebrew is ejk tw~n ajduna>twn: though they look diverse ways, there is a
- page: 398; sample: determined the times before appointed, and the bounds of their habitation," zhtei~n to<n Ku>rion eji a]rage yhlafh>seian aujto<n kai<
- page: 593; sample: And there is another word that signifies also what weight he lays on it, We have rendered it here, "Furthermore then." It is to< loipo<n ou+n, — "for

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: d his fullness, and, by union with him, Christ mystical, Ephesians 2:2 2:23; and this is that πανήγυρις (the only word most fully expressing the catholic church used in Scripture),; next: In order, therefore, unto the completing this great and mystical body, Christ hath his particular visible churches and assemblies in this world; wherein he hath ordained ordinances
- file: EPUB/ch003.xhtml; previous: nd the court which is without the temple, namely, the generality of visible professors, and the external part of worship, which hath been so long trod down by Gentilism. Wherefore,; next: Men, it may be, have thought they have got, or at least saved, by not troubling themselves with the care, charge, and trouble of gathering churches and walking in gospel order; but
- file: EPUB/ch008.xhtml; previous: d the same spirit, the same mind herein, ought, according to their measure, to be in all that have the pastoral office committed unto them. So the apostle expresseth it in himself,; next: And unless this compassion and goodness do run through the discharge of their whole office, men cannot be said to be evangelical shepherds, nor the sheep said in any sense to be th
- file: EPUB/ch025.xhtml; previous: 3. It is contrary to the rule delivered, Malachi 1:13, 14,; next: We are obliged, by all divine laws, natural, moral, and positive, to serve God always with our best. The obligations hereunto are inseparable from all just conceptions of the divin
- file: EPUB/ch029.xhtml; previous: marry who is maliciously and obstinately deserted, alarming that the Christian religion doth not prejudice the natural right and privilege of men in such cases: 1 Corinthians 7:15,; next: If a person obstinately depart, on pretense of religion or otherwise, and will no more cohabit with a husband or wife, it is known that, by the law of nature and the usage of all n
- file: EPUB/ch044.xhtml; previous: es; which show the work of the law written in their hearts, their conscience also bearing witness, and their thoughts the mean while accusing or else excusing one another." (Romans; next: 2:14, 15.) By the light that God hath indelibly implanted in the minds of men — accompanied with a moral instinct of good and evil, seconded by that selfjudgment which he hath plac
- file: EPUB/ch052.xhtml; previous: ause this thing is much insisted on by Galatinus to prove the Jews' corrupting of the text, it may not be amiss to set down the words of that great master of all Jewish learning: —; next: The עיטור סופרים are insisted on by the same Galatinus; but these are only about the use of the letter ו four or five times, which seem to be of the same rise with them foregoing.
- file: EPUB/ch062.xhtml; previous: or in the LORD JEHOVAH is everlasting strength." Ye know that God doth often invite us to trust in his name; and they that know his name will put their trust in him: Psalm 9:9, 10,; next: Is there any one that "walketh in darkness, and hath no light? let him trust in the name of the LORD," Isaiah 1:10.
- file: EPUB/ch062.xhtml; previous: 2. God, to show it to be our duty and wisdom, doth immediately propose the very properties of his nature for our relief: Isaiah 40:27,; next: — words whose sense are often ready to possess our hearts: I am sure they often lie at the door of mine; I know not how it is with you. What doth God propose to relieve them in tha
- file: EPUB/ch063.xhtml; previous: Consider ourselves as men: Job 4:17-19,; next: If God chargeth his very angels with folly, that is, an unanswerableness unto his infinite holiness and wisdom, — what can poor mortal men expect, that dwell in houses of clay, tha

## Inline Structural Marker Candidates

- file: EPUB/ch004.xhtml; text: The neglect of this duty brings inconceivable prejudice unto churches, and if continued in will prove their ruin; for they are not to be preserved, propagated, and continued, at the easy rate of a constant supply by the carnal baptized p...
- file: EPUB/ch006.xhtml; text: Unto the attaining of this wisdom are required, — 1. Fervent prayer for it, James 1:5. 2. Diligent study of the Scripture, to find out and understand the rules given by Christ unto this purpose, Ezra 7:10; 2 Timothy 2:1, 15. 3. Humble wa...
- file: EPUB/ch012.xhtml; text: Nor was this a temporary institution, for that season, and so the officers appointed extraordinary, but it was to abide in the church throughout a!! generations; for, — 1. The work itself, as a distinct work of ministry in the church, wa...
- file: EPUB/ch013.xhtml; text: The whole of what we plead for is here exemplified; as, — [1.] The cause of excommunication, which is a scandalous sin unrepented of. [2.] The preparation for its execution, which is the church's sense of the sin and scandal, with humili...
- file: EPUB/ch033.xhtml; text: But I say, — 1. It doth not signify properly "to dip" or "plunge," for that in Greek is ἐμζάπτω and ἐμζαπτίζω . 2. it nowhere signifies "to dip," but as a mode of and in order to washing. 3. It signifies the "dipping" of a finger, or the...
- file: EPUB/ch043.xhtml; text: By the assertion, then, laid down, of God "speaking in the prophets of old," from the beginning to the end of that long tract of time (consisting of one thousand years) wherein he gave out the writings of the Old Testament, two things ar...
- file: EPUB/ch063.xhtml; text: Then we have the adjuncts of this vision, which I will but name: — 1. It is certain: "Write it." It is a certain vision. 2. It is evident: "Make it plain upon tables, that he may run that readeth it." 3. It is determined: "The vision is ...
- file: EPUB/ch070.xhtml; text: Why, saith he, — 1. "No man layeth it to heart." And, 2. "None considering that they are taken away from the evil to come." The meaning of it is this, that in those strange and wonderful dispensations of God, there are very few that eith...

## Suspicious Large-Number Starts

- file: EPUB/ch007.xhtml; text: 124. in Johan.: "Peter the apostle bare, in a general figure, the person of the church; for as unto what belonged unto himself, he was by nature one man, by grace one Christian, and of special, more abounding grace one a
- file: EPUB/ch055.xhtml; text: 14. Let any man consider those two racks of the Rabbins and swords of Judaical unbelief, Isaiah 53 and Daniel 9, as they are now pointed and accented in our Bibles, and compare them with the translation of the LXX, and t
- file: EPUB/ch057.xhtml; text: 22. But this is only to question whether Ezra, Nehemiah, Joshua, Zechariah, Haggai, and the rest of the leaders of the people, on their return from the captivity, did set a sanhedrim, according to the institution of God,

## Roman Heading Candidates

- file: EPUB/ch056.xhtml; text: L. One, none, note, etc. — oe velca. O rotund.

## Overlong Heading Candidates

- file: EPUB/ch024.xhtml; tag: h3; text: QUESTION 1. WHETHER persons who have engaged unto reformation and another way of divine worship, according to the word of God, as they believe, may lawfully go unto and attend on the us of the prayer book in divine worship?

## Short Fragments

- file: EPUB/ch004.xhtml; text: I answer, therefore, —
- file: EPUB/ch013.xhtml; text: I answer, —
- file: EPUB/ch016.xhtml; text: I.
- file: EPUB/ch016.xhtml; text: II.
- file: EPUB/ch044.xhtml; text: So Job 37-39, throughout.
- file: EPUB/ch050.xhtml; text: - ED.
- file: EPUB/ch056.xhtml; text: Double. Diphthongs.
- file: EPUB/ch056.xhtml; text: Shi, di; thy, my.
- file: EPUB/ch056.xhtml; text: Alive, give, drive, title, thine.
- file: EPUB/ch056.xhtml; text: I Live, give, driven.

## Enumerator Sequence Candidates

- file: EPUB/ch011.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] Personal holiness, in gracious moral obedience.
- file: EPUB/ch013.xhtml; marker: (2dly.); family: paren_ordinal; context: unto it for its administration in the name of our Lord Jesus Christ, and with his power; (2dly.) The declarative cause of the equity of this sentence, which was the spirit of the apostle, or the authoritative declaration of his judgment ...

## Repeated Windows

- phrase: the various readings of ben asher and ben naphtali of; count: 4
- phrase: various readings of ben asher and ben naphtali of the; count: 4
- phrase: of ben asher and ben naphtali of the eastern and; count: 4
- phrase: ben asher and ben naphtali of the eastern and western; count: 4
- phrase: asher and ben naphtali of the eastern and western jews; count: 4
- phrase: will say unto me and what shall answer when am; count: 4
- phrase: say unto me and what shall answer when am reproved; count: 4
- phrase: let this mind be in you which was also in; count: 4
- phrase: this mind be in you which was also in christ; count: 4
- phrase: mind be in you which was also in christ jesus; count: 4

## Missing Word Samples

- word: pre; pdf: 5; epub: 0
- word: eminence; pdf: 5; epub: 0
- word: sixteen; pdf: 4; epub: 1
- word: seventeen; pdf: 3; epub: 0
- word: ; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 8; epub: 17
- word: footnotes; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
