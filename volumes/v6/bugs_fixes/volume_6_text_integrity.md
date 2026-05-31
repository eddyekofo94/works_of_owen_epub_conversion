# Text Integrity Audit: Volume 6

- Status: **WARN**
- Warnings: 10
- PDF pages: 787
- EPUB text files: 111
- EPUB paragraphs/headings: 3137

## Coverage

- PDF content tokens: 274707
- EPUB content tokens: 274287
- Approximate PDF-to-EPUB coverage ratio: 0.9954
- Pages checked: 781
- Weak page matches: 11
- Dense source windows checked: 1054
- Missing dense source-window pages: 762
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 775
- Top-of-page windows skipped as unstable: 19
- Missing top-of-page body windows: 1
- Bottom-of-page body windows checked: 730
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 2

## Paragraphs

- Body paragraphs checked: 2645
- Possible faulty paragraph splits: 193
- Structural starts excluded from split warnings: 357
- Short fragments: 15
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 4
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 19
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 631
- EPUB enumerator markers: 630
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 4

## Greek / Hebrew

- PDF Greek words: 250
- EPUB Greek words: 250
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 113
- EPUB Hebrew words: 116
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 10
- Missing Greek clauses: 0
- Hebrew clauses checked: 8
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

- page: 9; sample: practical exposition upon psalm 130 prefatory note by the editor to the reader psalm
- page: 10; sample: 10 the sending of the son of god to die for sin and from
- page: 14; sample: 14 corruption are at the farthest remove from all the arts and practices of
- page: 15; sample: 15 preface christian reader shall in few words acquaint thee with the reasons that
- page: 16; sample: 16 with such additions and alterations as should judge necessary under the inducement of
- page: 17; sample: 17 chapter the foundation of the whole ensuing discourse laid in romans 13 the
- page: 18; sample: 18 thirdly there is in them promise annexed to that duty ye shall live
- page: 19; sample: 19 obtain that end if you do mortify you shall live and herein lies
- page: 20; sample: 20 three things are here to be inquired into what is meant by the
- page: 21; sample: 21 passions and lusts of the flesh galatians 24 whence the deeds and fruits

## Missing Top-Of-Page Body Windows

- page: 9; sample: A PRACTICAL EXPOSITION UPON PSALM 130. PREFATORY NOTE BY THE EDITOR

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 613; sample: know little or nothing of the infinite largeness of his heart in this matter. He that he speaks of is [v;r;, "an impiously wicked man," and ˆw,a; vyai,

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: tribute to the carrying on of the work of mortification in believers may receive order and perspicuity, I shall lay the foundation of it in those words of the apostle, Romans 8:13,; next: The apostle having made a recapitulation of his doctrine of justification by faith, and the blessed estate and condition of them who are made by grace partakers thereof, verses 1-3
- file: EPUB/ch005.xhtml; previous: when they are still, so ought our contrivances against it to be vigorous at all times and in all conditions, even where there is least suspicion. Sin doth not only abide in us, but; next: If sin be subtle, watchful, strong, and always at work in the business of killing our souls, and we be slothful, negligent, foolish, in proceeding to the ruin thereof, can we expec
- file: EPUB/ch005.xhtml; previous: one, if not continually mortified, it will bring forth great, cursed, scandalous, soul-destroying sins. The apostle tells us what the works and fruits of it are, Galatians 5:19-21,; next: You know what it did in David and sundry others. Sin aims always at the utmost; every time it rises up to tempt or entice, might it have its own course, it would go out to the utmo
- file: EPUB/ch007.xhtml; previous: THE last principle I shall insist on (omitting, first, the necessity of mortification unto life, and, secondly, the certainty of life upon mortification) is, —; next: Strength and comfort, and power and peace, in our walking with God, are the things of our desires. Were any of us asked seriously, what it is that troubles us, we must refer it to
- file: EPUB/ch010.xhtml; previous: refining will do them no good. The prophet gives us the sad issue of wicked men's utmost attempts for mortification, by what means soever that God affords them: Jeremiah 6:29, 30,; next: And what is the reason hereof? Verse 28, They were "brass and iron" when they were put into the furnace. Men may refine brass and iron long enough before they will be good silver.
- file: EPUB/ch011.xhtml; previous: n work that will not do God's. God's work consists in universal obedience; to be freed of the present perplexity is their own only. Hence is that of the apostle, 2 Corinthians 7:1,; next: If we will do anything, we must do all things. So, then, it is not only an intense opposition to this or that peculiar lust, but a universal humble frame and temper of heart, with
- file: EPUB/ch012.xhtml; previous: ll I do this great evil," saith he, "and sin against the LORD?" my good and gracious God. (Genesis 39:9.) And Paul, "The love of Christ constraineth us;" (2 Corinthians 5:14.) and,; next: But now if a man be so under the power of his lust that he hath nothing but law to oppose it withal, if he cannot fight against it with gospel weapons, but deals with it altogether
- file: EPUB/ch012.xhtml; previous: 6. When thy lust hath already withstood particular dealings from God against it. This condition is described, Isaiah 57:17,; next: God had dealt with them about their prevailing lust, and that several ways, — by affliction and desertion; but they held out against all. This is a sad condition, which nothing but
- file: EPUB/ch013.xhtml; previous: t have it, that sin shall not have dominion over them as it hath over others, yet the guilt of sin that doth yet abide and remain is aggravated and heightened by it: Romans 6:1, 2,; next: — "How shall we, that are dead?" The emphasis is on the word "we."
- file: EPUB/ch013.xhtml; previous: (1.) Of being hardened by the deceitfulness. This the apostle sorely charges on the Hebrews, Hebrews 3:12, 13,; next: "Take heed," saith he, "use all means, consider your temptations, watch diligently; there is a treachery, a deceit in sin, that tends to the hardening of your hearts from the fear

## Inline Structural Marker Candidates

- file: EPUB/ch021.xhtml; text: Before I descend to other particulars, having now entered hereon, I shall show in general, — 1st. How or by what means commonly any temptation attains its hour;
- file: EPUB/ch049.xhtml; text: The Nature Of The Forgiveness Of Sin Is Declared; The Truth And Reality Of It Asserted; And The Case Of A Soul Distressed With The Guilt Of Sin, And Relieved By A Discovery Of Forgiveness With God, Is At Large Discoursed. "Search the Scr...
- file: EPUB/ch060.xhtml; text: In the supposition there is, — 1. The name of God, that is fixed on as suited unto it; and, 2. The thing itself supposed.
- file: EPUB/ch061.xhtml; text: In the supposition there is, — 1. The name of God, that is fixed on as suited unto it; and, 2. The thing itself supposed.

## Roman Heading Candidates

- file: EPUB/ch074.xhtml; text: II. God revealed this sacred truth by his institution of sacrifices.

## Overlong Heading Candidates

- file: EPUB/ch006.xhtml; tag: h4; text: II. He only is sufficient for this work; all ways and means without him are as a thing of nought; and he is the great efficient of it, — he works in us as he pleases.
- file: EPUB/ch008.xhtml; tag: h4; text: I. 1. (1.) To mortify a sin is not utterly to _kill,_ root it out, and destroy it, that it should have no more hold at all nor residence in our hearts.
- file: EPUB/ch010.xhtml; tag: h4; text: II. THE ways and means whereby a soul may proceed to the mortification of any particular lust and sin, which Satan takes advantage by to disquiet and weaken him, come next under consideration.
- file: EPUB/ch012.xhtml; tag: h4; text: III. THE foregoing general rules being supposed, particular directions to the soul for its guidance under the sense of a disquieting lust or distemper, being the main thing I aim at, come next to be proposed.
- file: EPUB/ch020.xhtml; tag: h4; text: I. First, For the general nature of tempting and temptation, it lies among things indifferent; to try, to experiment, to prove, to pierce a vessel, that the liquor that is in it may be known, is as much as is signified by it.
- file: EPUB/ch059.xhtml; tag: h4; text: II. THE words of these two first verses declare also the deportment of the soul in the condition that we have described; that is, what it doth, and what course it steers for relief." I have cried unto thee, O LORD.
- file: EPUB/ch062.xhtml; tag: h4; text: WHAT FIRST PRESENTS ITSELF TO A SOUL IN DISTRESS ON THE ACCOUNT OF SIN — THIS OPENED IN FOUR PROPOSITIONS — THOUGHTS OF GOD'S MARKING SIN ACCORDING TO THE TENOR OF THE LAW FULL OF DREAD AND TERROR.
- file: EPUB/ch063.xhtml; tag: h4; text: THE FIRST PARTICULAR ACTINGS OF A SOUL TOWARDS A RECOVERY OUT OF THE DEPTHS OF SIN—SENSE OF SIN, WHEREIN IT CONSISTS, HOW IT IS WROUGHT -ACKNOWLEDGMENT OF SIN; ITS NATURE AND PROPERTIES — SELF-CONDEMNATION.
- file: EPUB/ch067.xhtml; tag: h4; text: PROPOSITIONS OR OBSERVATIONS FROM THE FORMER EXPOSITION OF THE WORDS—THE FIRST PROPOSED TO CONFIRMATION—NO ENCOURAGEMENT FOR ANY SINNER TO APPROACH UNTO GOD WITHOUT A DISCOVERY OF FORGIVENESS.
- file: EPUB/ch070.xhtml; tag: h4; text: THE TRUE NATURE OF GOSPEL FORGIVENESS — ITS RELATION TO THE GOODNESS, GRACE, AND WILL OF GOD; TO THE BLOOD OF CHRIST; TO THE PROMISE OF THE GOSPEL — THE CONSIDERATIONS OF FAITH ABOUT IT.

## Short Fragments

- file: EPUB/ch015.xhtml; text: Eighthly,
- file: EPUB/ch015.xhtml; text: To which I answer, —
- file: EPUB/ch019.xhtml; text: John Owen.
- file: EPUB/ch022.xhtml; text: To which I answer, —
- file: EPUB/ch028.xhtml; text: Remember Peter!
- file: EPUB/ch047.xhtml; text: Let us take some few instances: —
- file: EPUB/ch049.xhtml; text: Dom. Episc. Lond. à Sac. Dom.
- file: EPUB/ch053.xhtml; text: GENERAL SCOPE OF THE WHOLE PSALM.
- file: EPUB/ch067.xhtml; text: This also is stated, Isaiah 33:14,
- file: EPUB/ch082.xhtml; text: And, —

## Enumerator Sequence Candidates

- file: EPUB/ch085.xhtml; marker: (9.); family: paren_decimal; context: (9.) Deep sorrow for sin, is consistent with assurance of forgiveness; yea, it is a great means of preservation of it. Godly sorrow, mourning, humiliation, contriteness of spirit, are
- file: EPUB/ch085.xhtml; marker: (3.); family: paren_decimal; context: (3.) A deep sense of the indwelling power of sin is consistent with gospel assurance. Sense of indwelling sin will cause manifold perplexities in the soul. Trouble, disquietments, sorr
- file: EPUB/ch086.xhtml; marker: (4.); family: paren_decimal; context: (4.) As it will do many other things, so, that I may give one comprehensive instance, it will carry them out, in whom it is, to die for Christ. Death, unto men who saw not one step bey
- file: EPUB/ch088.xhtml; marker: (2.); family: paren_decimal; context: (2.) In that part of our lives which, upon the call of God, we have given up unto him, there are two sorts of sins that do effectually impeach our future peace and comfort; which ought

## Repeated Windows

- phrase: there is forgiveness with thee that thou mayest be feared; count: 6
- phrase: the lord hath forsaken me and my lord hath forgotten; count: 6
- phrase: lord hath forsaken me and my lord hath forgotten me; count: 6
- phrase: the lust of the flesh the lust of the eyes; count: 5
- phrase: from the lord and my judgment is passed over from; count: 5
- phrase: the lord and my judgment is passed over from my; count: 5
- phrase: lord and my judgment is passed over from my god; count: 5
- phrase: lord hear my voice let thine ears be attentive to; count: 5
- phrase: hear my voice let thine ears be attentive to the; count: 5
- phrase: my voice let thine ears be attentive to the voice; count: 5

## Missing Word Samples

- word: stout; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 6

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
