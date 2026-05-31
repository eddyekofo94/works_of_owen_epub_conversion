# Text Integrity Audit: Volume 8

- Status: **WARN**
- Warnings: 9
- PDF pages: 774
- EPUB text files: 70
- EPUB paragraphs/headings: 3283

## Coverage

- PDF content tokens: 257154
- EPUB content tokens: 257223
- Approximate PDF-to-EPUB coverage ratio: 0.9937
- Pages checked: 764
- Weak page matches: 15
- Dense source windows checked: 782
- Missing dense source-window pages: 756
- Front CONTENTS pages checked: 2
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 739
- Top-of-page windows skipped as unstable: 22
- Missing top-of-page body windows: 15
- Bottom-of-page body windows checked: 712
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 11

## Paragraphs

- Body paragraphs checked: 2852
- Possible faulty paragraph splits: 127
- Structural starts excluded from split warnings: 262
- Short fragments: 35
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 2
- Roman heading candidates: 18
- Overlong heading candidates: 28
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 770
- EPUB enumerator markers: 776
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 303
- EPUB Greek words: 303
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 54
- EPUB Hebrew words: 54
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 12
- Missing Greek clauses: 0
- Hebrew clauses checked: 4
- Missing Hebrew clauses: 0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `suspicious_large_number_starts`: Some paragraphs begin with large bare numbers that may be broken reference continuations
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `overlong_heading_candidates`: Some chapter headings are long enough to suggest swallowed body text
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication

## Missing Dense Source Windows

- page: 5; sample: preface the two following volumes contain it is believed the most complete collection of
- page: 6; sample: posthumous sermons which had then for the first time been given to the public
- page: 7; sample: records the cases of two individuals dorothy emett and major mainwaring who ascribed their
- page: 8; sample: with parliament that they settled lands of inheritance of the clear value of 100
- page: 9; sample: the disadvantage of never having been intended for the press than the skill with
- page: 10; sample: 10 sermon vision of unchangeable free mercy in sending the means of grace to
- page: 11; sample: 11 previous month hopton and astley the last generals who kept the field in
- page: 12; sample: 12 agree with either of the two forms of church government which were then
- page: 13; sample: 13 amplissimo senatui inclytissimo populi anglicani conventui ob prisca anglo-britannorum jura strenue et fideliter
- page: 14; sample: 14 die mecurij 29 aprilis 1646 ordered by the commons assembled in parliament that

## Missing Top-Of-Page Body Windows

- page: 5; sample: PREFACE. The two following volumes contain, it is believed, the most complete
- page: 6; sample: posthumous sermons, which had then for the first time been given to the public.
- page: 7; sample: records the cases of two individuals, Dorothy Emett and Major Mainwaring, who ascribed their conversion to the preaching of Owen
- page: 8; sample: with Parliament, that they settled "lands of inheritance of the clear value of £100 per annum in Ireland on John Owen, Doctor of Divinity, and his
- page: 9; sample: the disadvantage of never having been intended for the press, — than the skill with which he can scrutinize character and motives, till his hearers
- page: 94; sample: TO THE WORTHY AND HONORED SIR WILLIAM MASHAM, SIR WILLIAM ROWE,
- page: 160; sample: TO THE RIGHT HONORABLE THE COMMONS OF ENGLAND,
- page: 187; sample: 1. Because of his own engagement. And that is twofold.
- page: 216; sample: Acts 16:21, "They teach customs which was plausibly pretended.
- page: 239; sample: 2 Chronicles 17:6, 30:14, Judah who accordingly performed this duty,

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 5; sample: transcribed from his own copies, and the rest taken from his mouth by a gentleman f2 of honor and known integrity," it is ranked among the
- page: 6; sample: preaching in some instances attest his usefulness in this department of his public labors. John Rogers, in his singular work, "The Heavenly Nymph,"
- page: 7; sample: the aspect of a vote of censure from the House; although we learn, from certain entries elsewhere in its journals, that he was so much of a favorite
- page: 8; sample: indeed, in his sermons is more prominent and remarkable, — especially in the sermons delivered towards the close of his life, and which labor under
- page: 117; sample: where the people were, but to continue firm to the world's end, as both the words here used, d[æ and µl;wO[ , "perpetuity" and "everlasting," do in
- page: 165; sample: indigencies; so there is ojrgh< teqhsaurisme>nh, Romans 2:5, — stored,
- page: 234; sample: churches, was seen of old. Hence that caution or canon of the Council of Chalcedon, cap. vi., Mhdei<v ceirotonei>sqw ajpolelume>nov, "Let none
- page: 338; sample: One Preached At Berwick, The Other At Edinburgh.
- page: 373; sample: w=| hJ do>xa eijv tou<v aijw~nav. jAmh>n.

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: difications which appear in the Congregationalism of Owen, are conspicuous elements in the first scheme of ecclesiastical polity which he ever broached. See also his "Review of the; next: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως
- file: EPUB/ch003.xhtml; previous: JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως; next: Αρχὴν IN ECCLESIASTICIS ἀνιεροτυραννικὴν DISSOLUTAM, RITUS PONTIFICIOS, NOVITIOS, ANTICHRISTIANOS ABOLITOS; PRIVILEGIA PLEBIS CHRISTIANAE POSTLIMINIO RESTITUTA;
- file: EPUB/ch003.xhtml; previous: S, EX ORDINE COMMUNIUM IN SUPREMA CURIA PARLIAM, CONGREGATIS, CONCIONEM HANC SACRAM, HUMILEM ILLAM QUIDEM, IPSORUM TAMEN VOTO JUSSUQUE PRIUS CORAM IPSIS HABITAM, NUNC LUCE DONATAM,; next: Die Mecurij 29 Aprilis, 1646.
- file: EPUB/ch004.xhtml; previous: ce fourteen generations. They alone were in Goshen, and all the world besides in thick darkness; — the dew of heaven was on them as the fleece, when else all the earth was dry. God; next: The prerogative of the Jews was chiefly in this, that to them were committed the oracles of God, Romans 3:1. To them pertained
- file: EPUB/ch004.xhtml; previous: The prerogative of the Jews was chiefly in this, that to them were committed the oracles of God, Romans 3:1. To them pertained; next: But when the fullness (Galatians 4:4; John 12:32; Acts 17:30; Mark 16:15; Malachi 3:4; Proverbs 8:31) of time came, the Son of God being sent in the likeness of sinful flesh, drew
- file: EPUB/ch004.xhtml; previous: in with another reckoning, and make them know that all things without Christ are but as ciphers without a figure, — of no value. In all their banquets, where Christ is not a guest,; next: — their palaces, where Christ is not, are but habitations of ziim and ochim, dragons and unclean beasts; — their prosperity is putting them into full pasture, that they may be fatt
- file: EPUB/ch008.xhtml; previous: arrant in itself, can never obtain any from its success. The rule of the goodness of any cause is the eternal law of reason, with the legal rights and interests of men." See Owen's; next: SIR, ALMIGHTY GOD having made you the instrument of that deliverance and peace which in the county of Essex we do enjoy, next to his own goodness, the remembrance thereof is due un
- file: EPUB/ch010.xhtml; previous: e word signifies, — and the wounding of the dragon, that great and crooked afflicter, Pharaoh, is remembered, and urged for a motive to a new needed deliverance. So Psalm 74:13,14,; next: Leviathan, — the same dragon, oppressing, persecuting Pharaoh, — thou brakest his heads, his counsels, armies, power; and gavest him for meat, that the people for forty years toget
- file: EPUB/ch010.xhtml; previous: Use. The use of this we are led unto, Isaiah 43:16-18,; next: Let former mercies be an anchor of hope in time of present distresses.
- file: EPUB/ch010.xhtml; previous: e them effectual. There is no flying from his armies, for they are every where, and himself with them. Who would not fear this King of nations? He that contends with him shall find; next: No flying, no hiding, no contending. Worms kill Herod; a fly choked Adrian, etc.

## Suspicious Large-Number Starts

- file: EPUB/ch015.xhtml; text: 14. Ignatius's epistles are full of the like expressions. Irenaeus says, he would have no words with them, lib. iii. cap. 3. Tertullian's books testify for him at large, with what keenness of spirit he pursued the hereti
- file: EPUB/ch015.xhtml; text: 11. And when this knack was once found out of promoting a sect by imperial favor, it is admirable to consider how those good princes, Constantine and his sons, were abused, misled, enraged, engaged into mutual dissension

## Roman Heading Candidates

- file: EPUB/ch023.xhtml; text: III. The last head remaineth under two particulars: —
- file: EPUB/ch035.xhtml; text: I. In the first I shall consider two things: —
- file: EPUB/ch038.xhtml; text: II. The cause of this perturbation of mind and spirit was from the visions of his head: "The visions of his head troubled him."
- file: EPUB/ch038.xhtml; text: III. There is the means that Daniel used for redress in that sad condition whereunto he was brought by the consideration of this vision: "He drew near to one of them that stood by, and asked him the truth of all this."
- file: EPUB/ch060.xhtml; text: V. Application: —
- file: EPUB/ch066.xhtml; text: I. The time when the things mentioned did fall out, and wherein our Savior passed his judgment on them.
- file: EPUB/ch066.xhtml; text: II. The providential accidents spoken of are two, and of two sorts.
- file: EPUB/ch066.xhtml; text: III. In the interpretation and application made of these severe accidents by our Savior, in his divine wisdom, we may observe, —
- file: EPUB/ch066.xhtml; text: I. When doth a church, a nation, a people, or city, so abound in sin, as to be immediately and directly concerned in his divine warning; and what, in particular, is the case of the nation wherein we live, and our own the
- file: EPUB/ch066.xhtml; text: II. Of what sort are those desolating judgments, which, in one way and sense or another, are impendent with respect unto such a church or nation, and, consequently, unto ourselves, at this season?

## Overlong Heading Candidates

- file: EPUB/ch004.xhtml; tag: h4; text: II. The sending of the gospel to any one nation rather than another, as the means of life and salvation, is of the mere free grace and good pleasure of God.
- file: EPUB/ch014.xhtml; tag: h4; text: III. The opposition which men cleaving to the Lord in all his ways shall find, with the issue and success of it: "They shall fight against thee; but shall not prevail."
- file: EPUB/ch015.xhtml; tag: h4; text: II. The sum of what is usually drawn from holy writ against such forbearance as I suppose may be asserted, and for the punishing heretics with capital punishments, being briefly discussed, I proceed, in the next place, to such other gene...
- file: EPUB/ch015.xhtml; tag: h4; text: III. I have only showed the weakness of those grounds which some men make the bottom of their testimonies against the toleration of any thing but what themselves conceive to be truth; as also, taken away the chief of those arguments upon...
- file: EPUB/ch015.xhtml; tag: h4; text: IV. Protection, as to peace and quietness in the use of the ordinances of the Lord Jesus Christ, from violent disturbers, either from without or within, is also incumbent on him.
- file: EPUB/ch015.xhtml; tag: h4; text: VI. It is the duty of the magistrate not to allow any public places for (in his judgment) false and abominable worship; as also, to demolish all outward appearances and demonstrations of such superstitious, idolatrous, and unacceptable s...
- file: EPUB/ch019.xhtml; tag: h4; text: I. The promise here mentioned is principally that which Abraham believing, it was said eminently that "it was accounted to him for righteousness." So the apostle tells us, verse 5 of this chapter.
- file: EPUB/ch019.xhtml; tag: h4; text: II. What is it to stagger at the promise? "He staggered not," οὐ διεκρίθη , "he disputed not." Διακρίνομαι is, properly, to make use of our own judgment and reason in discerning of things, of what sort they be.
- file: EPUB/ch031.xhtml; tag: h4; text: II. The actings of God's providence, in carrying on the interest of Christ, are and shall be exceedingly unsuited to the reasonings and expectations of the most of men.
- file: EPUB/ch035.xhtml; tag: h4; text: III. The third thing (that we may make haste) is his state and condition during the time which he lies under this dismission, in these words, "For thou shalt rest."

## Short Fragments

- file: EPUB/ch003.xhtml; text: Die Mecurij 29 Aprilis, 1646.
- file: EPUB/ch004.xhtml; text: The uses of it follow.
- file: EPUB/ch005.xhtml; text: Power is powerful to persuade.
- file: EPUB/ch010.xhtml; text: We shall treat of them in order.
- file: EPUB/ch010.xhtml; text: The reasons of this are taken, —
- file: EPUB/ch010.xhtml; text: Aesch. apud Justin., Apol.
- file: EPUB/ch010.xhtml; text: The verse hath two parts.
- file: EPUB/ch010.xhtml; text: Now, of this observe, —
- file: EPUB/ch013.xhtml; text: COGGESHALL, Feb. 38.
- file: EPUB/ch014.xhtml; text: Now, the Lord will do this, —

## Repeated Windows

- phrase: the removing of those things that are shaken as of; count: 5
- phrase: removing of those things that are shaken as of things; count: 5
- phrase: of those things that are shaken as of things that; count: 5
- phrase: those things that are shaken as of things that are; count: 5
- phrase: things that are shaken as of things that are made; count: 5
- phrase: that are shaken as of things that are made that; count: 5
- phrase: are shaken as of things that are made that those; count: 5
- phrase: shaken as of things that are made that those things; count: 5
- phrase: the testimony of the church is not the only nor; count: 4
- phrase: testimony of the church is not the only nor the; count: 4

## Missing Word Samples

- word: edition; pdf: 7; epub: 1
- word: posthumous; pdf: 6; epub: 0
- word: collection; pdf: 5; epub: 2
- word: composition; pdf: 5; epub: 2
- word: productions; pdf: 4; epub: 1
- word: journals; pdf: 3; epub: 0
- word: attention; pdf: 3; epub: 1
- word: eloquence; pdf: 3; epub: 1
- word: blemish; pdf: 3; epub: 1
- word: eminence; pdf: 3; epub: 1

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
