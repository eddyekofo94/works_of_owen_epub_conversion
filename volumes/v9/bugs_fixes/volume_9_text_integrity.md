# Text Integrity Audit: Volume 9

- Status: **WARN**
- Warnings: 10
- PDF pages: 778
- EPUB text files: 100
- EPUB paragraphs/headings: 3489

## Coverage

- PDF content tokens: 257225
- EPUB content tokens: 256752
- Approximate PDF-to-EPUB coverage ratio: 0.9961
- Pages checked: 771
- Weak page matches: 6
- Dense source windows checked: 961
- Missing dense source-window pages: 749
- Front CONTENTS pages checked: 5
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 752
- Top-of-page windows skipped as unstable: 28
- Missing top-of-page body windows: 9
- Bottom-of-page body windows checked: 701
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2958
- Possible faulty paragraph splits: 186
- Structural starts excluded from split warnings: 399
- Short fragments: 43
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 5
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 7
- Overlong heading candidates: 28
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 834
- EPUB enumerator markers: 831
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 140
- EPUB Greek words: 140
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 34
- EPUB Hebrew words: 34
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 3
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 8; sample: that city and country are crying watchman what of the night watchman what of
- page: 10; sample: 10 whose destruction is so solemnly prophesied of in this and the foregoing chapter
- page: 11; sample: 11 upon these three accounts which is that would observe the name of babylon
- page: 12; sample: 12 danger of the same desolation and destruction from new babylon upon the same
- page: 13; sample: 13 distinct titles of god unto the two distinct considerations of the people first
- page: 14; sample: 14 ii gather up what evidences we have that england is not yet utterly
- page: 15; sample: 15 filled with sin as that god's decree of absolute and universal desolation should
- page: 16; sample: 16 determination what will be the issue judgment is deserved and there is nothing
- page: 17; sample: 17 land is so filled with sin when all sorts of provoking sins do
- page: 18; sample: 18 brethren you know my mind full well in this matter have been for

## Missing Top-Of-Page Body Windows

- page: 151; sample: Philippians 4:11, "I have learned it," saith he; This was Paul's frame,
- page: 273; sample: SERMON 17. F16 THE DIVINE POWER OF THE GOSPEL.
- page: 370; sample: SERMON 24. F26 GOD'S WITHDRAWING HIS PRESENCE, THE CORRECTION OF
- page: 385; sample: SERMON 25. F27 THE BEAUTY AND STRENGTH OF ZION.
- page: 419; sample: SERMON 27. F31 THE CHRISTIAN'S WORK OF DYING DAILY.
- page: 441; sample: SERMON 30. F37 THE EVIL AND DANGER OF OFFENCES.
- page: 612; sample: SERMON 10.F64 THE USE AND ADVANTAGE OF FAITH
- page: 622; sample: SERMON 11.F65 THE USE OF FAITH UNDER REPROACHES AND
- page: 705; sample: are invited to feast upon the sacrifice. The sacrifice is offered; Christ is the sacrifice, — God's passover; God makes a feast upon it, and invites his

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 159; sample: apostle, "that was in Jesus Christ," Philippians 2:5. What mind was

## Possible Paragraph Splits

- file: EPUB/ch002.xhtml; previous: celebrated and much-respected preacher in London, — a kind of Latimer among the Nonconformists of his time. He died in 1713, and his funeral sermon was preached by Matthew Henry: —; next: the Lord; ' — nay, now, that it is neither day nor night, as the prophet speaks; — now, that city. and country are crying, 'Watchman, what of the night? ?' — now, that the three fr
- file: EPUB/ch003.xhtml; previous: This was not now the case of Israel and Judah. It proved afterward to be their case, as the apostle describes it, 1 Thessalonians 2:15, 16,; next: How come? They have filled their measure, reached to their bounds; — "wrath is come upon them to the uttermost." I hope, I pray, that this is not, that this may not be, the state o
- file: EPUB/ch003.xhtml; previous: but let all mankind do what they will, he will not pass it by without some severe, desolating judgment. Such was their case even at this time; — you may see in 2 Chronicles 36:16,; next: It was impossible that the judgment of God should be turned away from them. In this state God saith, "Pray not for this people; my heart shall not be toward them," (until he had br
- file: EPUB/ch003.xhtml; previous: are absolutely resolved upon sovereign grace and mercy: and without relief from thence, I shall only say, as to the proof of the proposition, what the prophet saith, Isaiah 34:16,; next: To omit all the considerations and all the proof I intended, that sovereign grace and mercy must be our relief, if ever we be relieved, I proceed unto the second thing; which is, —
- file: EPUB/ch006.xhtml; previous: e first place. Eternal life is promised by God, who cannot lie, Titus 1:2; that is, who is so faithful, as that it is utterly impossible he should deceive any. So Hebrews 6:17, 18,; next: The design of God is, that we may receive encouragement in our flying for refuge to the hope set before us, — that is, in believing. What doth he propose to this end? Why, his own
- file: EPUB/ch007.xhtml; previous: unto steadfastness in believing the promises. Amongst the many that are usually insisted on to this purpose, I shall choose out some few that seem to be most effectual thereunto: —; next: Use 1. We shall begin with the consideration of God himself, even the Father; and that declaration of his love, kindness, tenderness, readiness, and willingness to receive poor bel
- file: EPUB/ch007.xhtml; previous: ainting sinners: "Give not over; let not go your hold; though you be in darkness to all other means of support and consolation, yet 'trust in the name of the LORD.' And," saith he,; next: And what this name of God, which is such a stay and safe defense, is, is declared at large, Exodus 34:6, 7. This name of his, is that glory which he promised to show to Moses, chap
- file: EPUB/ch007.xhtml; previous: requireth of us is so ordered and disposed in the revelation thereof, that when our Savior had made him and his whole will known from his bosom, he sums up his whole work in this,; next: The manifestation of the name of God to the elect was the great work of Christ on the earth, as he was the prophet and teacher of his church. He declared the name of God, — his gra
- file: EPUB/ch007.xhtml; previous: self for our good, is greatly conquering to the soul; but none so much as this, — his being love, and ready to forgive on that account. Such is the frame of the church, Micah 7:18,; next: Can it enter into the heart of man? O who is like to him! Is it possible he should be thus to sinners! This discovery overwhelms the soul, and strengthens it in faith and trust in
- file: EPUB/ch007.xhtml; previous: in the dispensation of his providence, that is too hard for the apprehensions of men when they come to be concerned in it. Poor Jonah was angry that he was so merciful, Jonah 4:2,; next: And if God be thus full of compassion to the world, which today is, and to-morrow shall be cast into the fire, is he not much more loving and tender unto you, "O ye of little faith

## Inline Structural Marker Candidates

- file: EPUB/ch011.xhtml; text: Now, surely, if God hath this delight in us in our walking before him, is it not expected that our delight should be in him in our obedience? It suits not my present business to go over the testimonies of Scripture, wherein either we are...
- file: EPUB/ch021.xhtml; text: The latter containeth, — 1. A doctrinal observation for the use of the church, from the whole, verse 7. 2. The reasons and confirmation of the doctrine so laid down, taken from the power and righteousness of God in the actions recounted,...
- file: EPUB/ch021.xhtml; text: They shall have no better issue, because, — (1.) The Lord will take away their stout hearts, whereby they are supported; (2.) He will take away their strong hands, whereby they are confirmed: and when hearts and hands are gone, they also...
- file: EPUB/ch024.xhtml; text: His estate is doubly expressed: — 1. From the place where he was, — " From the end of the earth;" and, 2. From the condition he was in, — " His heart was overwhelmed." And in the course he steered there are two things also: —
- file: EPUB/ch029.xhtml; text: There is a twofold hardening from God's fear: — 1. There is a total hardening; and, 2. A partial hardening: — 1. There is a total hardening, like that mentioned, Isaiah 6:10,

## Roman Heading Candidates

- file: EPUB/ch003.xhtml; text: I. There are three ways whereby a land may be said to be filled with sin: —
- file: EPUB/ch003.xhtml; text: III. I should now proceed to my last thing, — to show you, that in this state, wherein a land is so filled with sin as absolutely to put the determination of all things into the hand of sovereignty, and where yet there r
- file: EPUB/ch006.xhtml; text: I. As to the former of these, —
- file: EPUB/ch026.xhtml; text: III. Lay down some directions for its practice: —
- file: EPUB/ch035.xhtml; text: II. There are offenses given and taken: —
- file: EPUB/ch060.xhtml; text: I. The subject treated of: —
- file: EPUB/ch071.xhtml; text: III. We may see three things concerning ourselves: —

## Overlong Heading Candidates

- file: EPUB/ch002.xhtml; tag: h3; text: "To the Reader — Upon the desire of some interested in the publication of this sermon, I have perused it, and do communicate these my thoughts concerning it. "There appear unto me in it those two things, which do above all others commend...
- file: EPUB/ch008.xhtml; tag: h4; text: I. That believers enjoy this privilege as a fruit and effect of the death and blood of Jesus Christ, I shall confirm only with one or two places of Scripture, Hebrews 9:8, compared with Hebrews 10:19-22.
- file: EPUB/ch014.xhtml; tag: h4; text: III. Let us now proceed to prove the proposition at first laid down, and shut up the whole; viz., — Humble walking with God is the great duty and most valuable concernment of believers. "What doth the Lord thy God require of thee?" This ...
- file: EPUB/ch019.xhtml; tag: h4; text: II. All places in the world are barren, unsound, and unhealthy, before the coming of the waters of the sanctuary upon them; — or, the souls of all men are spiritually dead and full of woeful distempers, until they are quickened and heale...
- file: EPUB/ch019.xhtml; tag: h4; text: III. The waters of the sanctuary are healing waters; — or, the word of the gospel is in its own nature a quickening, healing, sanctifying, saving word, to them who receive it.
- file: EPUB/ch019.xhtml; tag: h4; text: IV. Where the waters of the sanctuary come, and the land is not healed, that land is given up of the Lord to salt or barrenness for ever; - or, where the word of the gospel is, by the infinitely wise disposal of God, preached unto a plac...
- file: EPUB/ch019.xhtml; tag: h4; text: I. God is pleased oftentimes, in his infinite wisdom, to send the preaching of the word unto some places wherein it shall not put forth its quickening and sanctifying power and virtue upon the souls of them that hear it.
- file: EPUB/ch019.xhtml; tag: h4; text: IV. Where the waters of the sanctuary come, and the land is not healed, that land is given up of the Lord to salt and barrenness for ever; — or, where the word of the gospel is preached unto a place, or persons, and they receive it not s...
- file: EPUB/ch021.xhtml; tag: h4; text: III. Though men have courage, might, and former successes to accompany them, yet when they engage themselves against the Lord, or any way of his, vanity, weakness, and disappointment will be the issue thereof. "Can your heart endure, or ...
- file: EPUB/ch024.xhtml; tag: h4; text: III. I now proceed to show what it is that, in such an overwhelming condition as I have described, faith regards in God to give it a support and relief, that it be not utterly swallowed up and overwhelmed.

## Short Fragments

- file: EPUB/ch008.xhtml; text: To this end, —
- file: EPUB/ch009.xhtml; text: I shall show in brief, —
- file: EPUB/ch011.xhtml; text: 10.
- file: EPUB/ch014.xhtml; text: The grounds of it are: —
- file: EPUB/ch015.xhtml; text: The grounds hereof are, —
- file: EPUB/ch016.xhtml; text: Come we now to the uses.
- file: EPUB/ch017.xhtml; text: Use 1. Of trial or examination.
- file: EPUB/ch017.xhtml; text: Jehu's spirit spoiled his work.
- file: EPUB/ch019.xhtml; text: The word must come and heal them.
- file: EPUB/ch020.xhtml; text: WE shall now proceed to the uses.

## Enumerator Sequence Candidates

- file: EPUB/ch013.xhtml; marker: (2.); family: paren_decimal; context: (2.) I come now to show what it is to humble ourselves to the law of his providence.
- file: EPUB/ch018.xhtml; marker: (2.); family: paren_decimal; context: (2.) That which in the next place is considerable, is the proposing of the ingredients that lie in the motive to holiness, here expressed by the apostle, "Seeing that these things shal
- file: EPUB/ch020.xhtml; marker: (2.); family: paren_decimal; context: (2.) The second thing that God doth, in giving up an unhealed land unto barrenness, is his judicial hardening of them, or leaving them to hardness and impenitency, that so they may fil
- file: EPUB/ch025.xhtml; marker: [2.]; family: bracket_decimal; context: [2.] There are some distresses that, in their own nature, refuse all relief that you can tender them, but only what is derived from the fountain itself, — the nature of God. Zion's dis

## Repeated Windows

- phrase: as often as ye eat this bread and drink this; count: 6
- phrase: often as ye eat this bread and drink this cup; count: 6
- phrase: loved us and washed us from our sins in his; count: 6
- phrase: us and washed us from our sins in his own; count: 6
- phrase: and washed us from our sins in his own blood; count: 6
- phrase: that we might be made the righteousness of god in; count: 5
- phrase: as ye eat this bread and drink this cup ye; count: 5
- phrase: ye eat this bread and drink this cup ye do; count: 5
- phrase: eat this bread and drink this cup ye do show; count: 5
- phrase: is so filled with sin against the holy one of; count: 5

## Missing Word Samples

- word: sufficiency; pdf: 3; epub: 1

## Excess Word Samples

- word: psalms; pdf: 8; epub: 19
- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
