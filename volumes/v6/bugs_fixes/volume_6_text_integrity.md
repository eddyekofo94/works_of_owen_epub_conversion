# Text Integrity Audit: Volume 6

- Status: **WARN**
- Warnings: 11
- PDF pages: 787
- EPUB text files: 112
- EPUB paragraphs/headings: 3122

## Coverage

- PDF content tokens: 271940
- EPUB content tokens: 270717
- Approximate PDF-to-EPUB coverage ratio: 0.9926
- Pages checked: 781
- Weak page matches: 7
- Dense source windows checked: 36659
- Missing dense source-window pages: 40
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 1
- Top-of-page body windows checked: 773
- Top-of-page windows skipped as unstable: 19
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 729
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 4

## Paragraphs

- Body paragraphs checked: 2671
- Possible faulty paragraph splits: 15
- Structural starts excluded from split warnings: 360
- Short fragments: 35
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 3
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 631
- EPUB enumerator markers: 634
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

## Latin

- PDF Latin words: 2327
- EPUB Latin words: 2349
- EPUB Tagged Latin words: 0
- Latin word coverage ratio: 0.9901
- Latin word tagging ratio: 0.0
- Latin clauses checked: 14
- Missing Latin clauses: 0
- Tagged Latin runs checked: 0
- Translated Latin runs: 0
- Latin translation ratio: 1.0

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `front_matter_toc_loss`: Some early CONTENTS pages have no strong text-window match in the EPUB
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `enumerator_sequence_candidates`: Some EPUB enumerators look like possible sequence jumps and need triage
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_latin_tagging`: A significant portion of Latin words in the EPUB are not wrapped in language spans

## Missing Dense Source Windows

- page: 3; sample: contents of vol of the mortification of sin in believers etc prefatory note by
- page: 4; sample: eruption of sin in time of danger or trouble chapter the mortification of sin
- page: 5; sample: actings of sin vigorously to be opposed chapter the eighth direction thoughtfulness of the
- page: 6; sample: professors of the choicest saints adam abraham david self consideration as to our own
- page: 7; sample: remainders of indwelling sin in believers prefatory note by the editor preface chapter indwelling
- page: 8; sample: of obedience instanced in meditation and prayer chapter the deceit of sin in drawing
- page: 9; sample: practical exposition upon psalm prefatory note by the editor to the reader psalm verses
- page: 10; sample: is on us to forgive one another properties of forgiveness the greatness and freedom
- page: 19; sample: spirit ει δε πνευματι if by the spirit the spirit here is the spirit
- page: 28; sample: of the heart grows worse and worse and the lord knows what desperate and

## Missing Front CONTENTS Pages

- page: 6; hit_ratio: 0.25; sample: chapter the doctrine grounds of it our savior's direction in this case his promise of preservation issues of men entering into temptation of ungrounded professors of the choicest

## Missing Top-Of-Page Body Windows

- page: 3; sample: CONTENTS OF VOL. 6. OF THE MORTIFICATION OF SIN IN BELIEVERS, ETC.
- page: 9; sample: A PRACTICAL EXPOSITION UPON PSALM 130. PREFATORY NOTE BY THE EDITOR

## Missing Bottom-Of-Page Body Windows

- page: 2; sample: This Edition of first published by Johnstone & Hunter, 1850-53
- page: 198; sample: Romans 7:24, 25 death? I thank God through Jesus Christ our Lord" –
- page: 403; sample: ROB. GROVE, R. P. Humph. Dom. Episc. Lond. à Sac. Dom.
- page: 613; sample: know little or nothing of the infinite largeness of his heart in this matter. He that he speaks of is [v;r;, "an impiously wicked man," and ˆw,a; vyai,

## Possible Paragraph Splits

- file: EPUB/ch003.xhtml; previous: CHRISTIAN READER,; next: I SHALL in a few words acquaint thee with the reasons that obtained my consent to the publishing of the ensuing discourse. The consideration of the present state and condition of t
- file: EPUB/ch003.xhtml; previous: s is the sum of the account I shall give) may in anything be useful to the least of the saints, it will be looked on as a return of the weak prayers wherewith it is attended by its; next: unworthy author
- file: EPUB/ch003.xhtml; previous: unworthy author; next: John Owen
- file: EPUB/ch019.xhtml; previous: CHRISTIAN READER,; next: If thou art in any measure awake in these days wherein we live, and hast taken notice of the manifold, great, and various temptations wherewith all sorts of persons that know the L
- file: EPUB/ch022.xhtml; previous: ty of such indispensable necessity to them who intend to walk with God in any peace, or with any faithfulness, — are to be considered and removed. And they are these that follow: —; next: Obj. 1. "Why should we so fear and labor to avoid temptation? James 1:2, we are commanded to 'count it all joy when we fall into divers temptations.' Now, certainly I need not soli
- file: EPUB/ch027.xhtml; previous: en of by reason of him; that he is concerned in love to his soul, having that design upon him to "present him holy, and unblamable, and unreprovable in his sight," Colossians 1:22,; next: — and his Spirit is grieved where he is interrupted in this work; concerned on the account of his gospel, the progress and acceptation of it in the world, — its beauty would be slu
- file: EPUB/ch051.xhtml; previous: To The Reader; next: CHRISTIAN READER,
- file: EPUB/ch051.xhtml; previous: CHRISTIAN READER,; next: THE ensuing exposition and discourses are intended for the benefit of those whose spiritual state and condition is represented in the psalm here explained. That these are not a few
- file: EPUB/ch075.xhtml; previous: God's countenance, and say unto him, "Did we not know you some while since to be full of sadness and great anxiety of spirit; yea, sorrowful almost to death, and bitter in soul?" —; next: Ans. "Yes," saith he, "so it was, indeed. My days were consumed with mourning, and my life with sorrow; and I walked heavily, in fear and bitterness of spirit, all the day long."
- file: EPUB/ch075.xhtml; previous: "Why, what ailed you, what was the matter with you, seeing as to outward things you were in peace?" —; next: Ans. "The law of God had laid hold upon me and slain me. I found myself thereby a woful sinner, yea, overwhelmed with the guilt of sin. Every moment I expected tribulation and wrat

## Inline Structural Marker Candidates

- file: EPUB/ch025.xhtml; text: Such was the state of the church or Sardis, (3.) A season of great spiritual enjoyments is often, by the malice of Satan and the weakness of our hearts, turned into a season of danger as to this business of temptation.
- file: EPUB/ch076.xhtml; text: Indeed, if we should go upon our own heads, without his warranty and authority, to ask any thing at his hand, we might well expect to meet with disappointment; for what should encourage us unto any such boldness? but now, when God himsel...
- file: EPUB/ch082.xhtml; text: Gospel pardon is a thing of another nature; it hath its spring in the gracious heart of the Father, is made out by a sovereign act of his will, rendered consistent with the glory of his justice and holiness by the blood of Christ, by whi...

## Roman Heading Candidates

- file: EPUB/ch074.xhtml; text: II. God revealed this sacred truth by his institution of sacrifices.

## Short Fragments

- file: EPUB/ch003.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch003.xhtml; text: unworthy author
- file: EPUB/ch003.xhtml; text: John Owen
- file: EPUB/ch015.xhtml; text: To which I answer, —
- file: EPUB/ch019.xhtml; text: CHRISTIAN READER,
- file: EPUB/ch019.xhtml; text: John Owen
- file: EPUB/ch022.xhtml; text: To which I answer, —
- file: EPUB/ch027.xhtml; text: And, therefore, I shall show, —
- file: EPUB/ch028.xhtml; text: Remember Peter!
- file: EPUB/ch044.xhtml; text: and with the prophet, Hosea 14:9,

## Enumerator Sequence Candidates

- file: EPUB/ch085.xhtml; marker: (9.); family: paren_decimal; context: (9.) Deep sorrow for sin, is consistent with assurance of forgiveness; yea, it is a great means of preservation of it. Godly sorrow, mourning, humiliation, contriteness of spirit, are
- file: EPUB/ch085.xhtml; marker: (3.); family: paren_decimal; context: (3.) A deep sense of the indwelling power of sin is consistent with gospel assurance. Sense of indwelling sin will cause manifold perplexities in the soul. Trouble, disquietments, sorr
- file: EPUB/ch086.xhtml; marker: (4.); family: paren_decimal; context: (4.) As it will do many other things, so, that I may give one comprehensive instance, it will carry them out, in whom it is, to die for Christ. Death, unto men who saw not one step bey
- file: EPUB/ch088.xhtml; marker: (2.); family: paren_decimal; context: (2.) In that part of our lives which, upon the call of God, we have given up unto him, there are two sorts of sins that do effectually impeach our future peace and comfort; which ought

## Repeated Windows

- phrase: there is forgiveness with thee that thou mayest be feared; count: 6
- phrase: the lust of the flesh the lust of the eyes; count: 5
- phrase: from the lord and my judgment is passed over from; count: 5
- phrase: the lord and my judgment is passed over from my; count: 5
- phrase: lord and my judgment is passed over from my god; count: 5
- phrase: lord hear my voice let thine ears be attentive to; count: 5
- phrase: hear my voice let thine ears be attentive to the; count: 5
- phrase: my voice let thine ears be attentive to the voice; count: 5
- phrase: voice let thine ears be attentive to the voice of; count: 5
- phrase: let thine ears be attentive to the voice of my; count: 5

## Missing Word Samples

- word: editor; pdf: 4; epub: 1
- word: stout; pdf: 3; epub: 1

## Excess Word Samples

- word: digital; pdf: 0; epub: 10
- word: modern; pdf: 2; epub: 11
- word: greek; pdf: 0; epub: 8
- word: hebrew; pdf: 1; epub: 8
- word: theological; pdf: 0; epub: 7
- word: edition; pdf: 6; epub: 12
- word: footnotes; pdf: 0; epub: 6

## Untagged Latin Word Samples

- word: nor; epub: 349; tagged: 0
- word: yea; epub: 182; tagged: 0
- word: poor; epub: 153; tagged: 0
- word: jesus; epub: 130; tagged: 0
- word: endeavor; epub: 56; tagged: 0
- word: terror; epub: 53; tagged: 0
- word: thereunto; epub: 49; tagged: 0
- word: mere; epub: 47; tagged: 0
- word: door; epub: 46; tagged: 0
- word: vigor; epub: 44; tagged: 0

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
