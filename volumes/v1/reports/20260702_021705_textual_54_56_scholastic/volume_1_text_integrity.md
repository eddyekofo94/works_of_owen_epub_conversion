# Text Integrity Audit: Volume 1

- Status: **WARN**
- Warnings: 5
- PDF pages: 633
- EPUB text files: 83
- EPUB paragraphs/headings: 2693

## Coverage

- PDF content tokens: 191893
- EPUB content tokens: 205236
- Approximate PDF-to-EPUB coverage ratio: 0.9996
- Pages checked: 581
- Weak page matches: 1
- Dense source windows checked: 26608
- Missing dense source-window pages: 35
- Front CONTENTS pages checked: 0
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 586
- Top-of-page windows skipped as unstable: 6
- Missing top-of-page body windows: 2
- Bottom-of-page body windows checked: 534
- Bottom-of-page windows skipped as unstable: 0
- Missing bottom-of-page body windows: 0

## Paragraphs

- Body paragraphs checked: 2256
- Possible faulty paragraph splits: 1
- Structural starts excluded from split warnings: 121
- Short fragments: 12
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 0
- Syllabus-anchor candidates: 16
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 1
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 295
- EPUB enumerator markers: 310
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 716
- EPUB Greek words: 811
- Greek word coverage ratio: 1.0
- PDF Hebrew words: 18
- EPUB Hebrew words: 20
- Hebrew word coverage ratio: 1.0
- Greek clauses checked: 33
- Missing Greek clauses: 0
- Hebrew clauses checked: 1
- Missing Hebrew clauses: 0

## Latin

- PDF Latin words: 962
- EPUB Latin words: 1340
- EPUB Tagged Latin words: 974
- Latin word coverage ratio: 0.999
- Latin word tagging ratio: 0.7269
- Latin clauses checked: 91
- Missing Latin clauses: 0
- Tagged Latin runs checked: 258
- Translated Latin runs: 139
- Latin translation ratio: 0.5388

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `syllabus_anchor_candidates`: Some introduced scholastic syllabus runs appear unflattened or need triage

## Missing Dense Source Windows

- page: 146; sample: it is christian or evangelical may be reduced the person of christ is the
- page: 382; sample: the dark after what they cannot clearly discern acts among other cicero's book de
- page: 398; sample: so the apostle expresseth this truth where is the wise where is the scribe
- page: 402; sample: known or as it may be thence earned my present business is only to
- page: 406; sample: 2-6 isaiah 1-4 zechariah john 1-3 philippians 6-8 hebrews 1-3 14-16 revelation secondly by
- page: 411; sample: made her as the chariots of ammi nadib song of solomon it so fell
- page: 419; sample: in him unto any of the creatures is an act of self humiliation and
- page: 433; sample: brightness wherewith this glory shines in heaven the all satisfying sweetness which the view
- page: 434; sample: unto it sweet savor of the love of christ see song of solomon 2-4
- page: 451; sample: its holiness and the severity of the curse wherewith it was attended his fulfil1ing

## Missing Top-Of-Page Body Windows

- page: 398; sample: So the apostle expresseth this truth, "Where is the wise? where is the scribe? where is the disputer of
- page: 478; sample: "To reconcile all things unto himself in him, whether they be things in earth, or things in heaven."

## Possible Paragraph Splits

- file: EPUB/ch038.xhtml; previous: he apostle declares in these words, "To gather together in one all things which are in heaven, and which are on earth, even in him." And so he again expresseth it, Colossians 1:20,; next: He would no longer keep them in two distinct families; but he would, in his infinite wisdom and goodness, gather them up into one common head, on whom they should have their immedi

## Syllabus Anchor Candidates

- action: likely_false_positive; file: EPUB/ch006.xhtml; anchor_index: 299; item_range: p300-p302; marker_family: unknown; item_count: 3; announced_count: None; anchor: at did not relate thereunto. Such bold inquiries, with futilous § answers annexed unto them, sufficiently manifest what acquaintance their authors have either with Christ himself, which in others they despise, or with his Gospel, which t...; items: [{'marker': '(2.)', 'text': 'A mock scheme of religion is framed, to represent the folly of them who design to learn the mind and will of God in and by him.'}, {'marker': '(3.)', 'text': 'Reproachful reflections are made on such as plead...; whitelist_key: EPUB/ch006.xhtml#p299-syllabus-1-it-is-scandalously-proposed-and-answered-of-what-use-is-the
- action: likely_false_positive; file: EPUB/ch010.xhtml; anchor_index: 458; item_range: p459-p461; marker_family: unknown; item_count: 3; announced_count: 2; anchor: 1. There are two things wherein the glory of truth does consist.; items: [{'marker': '(1.)', 'text': 'Its light.'}, {'marker': '(2.)', 'text': 'Its efficacy or power. And both these do all supernatural truths derive from this relation unto Christ.'}, {'marker': '(1.)', 'text': 'No truth whatever brings any sp...; whitelist_key: EPUB/ch010.xhtml#p458-syllabus-1-there-are-two-things-wherein-the-glory-of-truth-does-consist
- action: likely_false_positive; file: EPUB/ch014.xhtml; anchor_index: 615; item_range: p616-p618; marker_family: arabic; item_count: 3; announced_count: None; anchor: And nothing can be more derogatory unto the wisdom and holiness of God, than to imagine that he would grant other ways of salvation unto them who had rejected that only one which he had provided; which was by faith in Christ, as revealed...; items: [{'marker': '8.', 'text': 'From these considerations, which are all of them unquestionable principles of truth, two things are evident.'}, {'marker': '(1.)', 'text': 'That there was no way of the justification and salvation of sinners re...; whitelist_key: EPUB/ch014.xhtml#p615-syllabus-7-those-who-voluntarily-through-the-contempt-of-god-and-divine-grace
- action: likely_false_positive; file: EPUB/ch014.xhtml; anchor_index: 616; item_range: p617-p618; marker_family: unknown; item_count: 2; announced_count: 2; anchor: 8. From these considerations, which are all of them unquestionable principles of truth, two things are evident.; items: [{'marker': '(1.)', 'text': 'That there was no way of the justification and salvation of sinners revealed and proposed from the foundation of the world, but only by Jesus Christ, as declared in the first promise.'}, {'marker': '(2.)', 't...; whitelist_key: EPUB/ch014.xhtml#p616-syllabus-8-from-these-considerations-which-are-all-of-them-unquestionable-principles-of
- action: likely_false_positive; file: EPUB/ch022.xhtml; anchor_index: 1054; item_range: p1055-p1056; marker_family: unknown; item_count: 2; announced_count: None; anchor: the immediate principle of all such operations. The wisdom, power, grace, and goodness exerted therein, are essential properties of the divine nature. Wherefore the acting of them originally belongs equally unto each person, equally part...; items: [{'marker': '(1.)', 'text': 'As unto authoritative designation, it was the act of the Father. Hence is he said to send "his Son in the likeness of sinful flesh," Romans 8:3; Galatians 4:4.'}, {'marker': '(2.)', 'text': 'As unto the forma...; whitelist_key: EPUB/ch022.xhtml#p1054-syllabus-1-as-unto-original-efficiency-it-was-the-act-of-the-divine
- action: likely_false_positive; file: EPUB/ch022.xhtml; anchor_index: 1058; item_range: p1059-p1062; marker_family: arabic; item_count: 4; announced_count: None; anchor: 2. This assumption was the only immediate act of the divine nature on the human in the person of the Son. All those that follow, in subsistence, sustentation, with all others that are communicative, do ensue thereon.; items: [{'marker': '3.', 'text': 'This assumption and the hypostatical union are distinct and different in the formal reason of them.'}, {'marker': '(1.)', 'text': 'Assumption is the immediate act of the divine nature in the person of the Son o...; whitelist_key: EPUB/ch022.xhtml#p1058-syllabus-2-this-assumption-was-the-only-immediate-act-of-the-divine-nature
- action: likely_false_positive; file: EPUB/ch022.xhtml; anchor_index: 1060; item_range: p1061-p1062; marker_family: unknown; item_count: 2; announced_count: None; anchor: (1.) Assumption is the immediate act of the divine nature in the person of the Son on the human; union is mediate, by virtue of that assumption.; items: [{'marker': '(2.)', 'text': 'Assumption is unto personality; it is that act whereby the Son of God and our nature became one person. Union is an act or relation of the natures subsisting in that one person.'}, {'marker': '(3.)', 'text': ...; whitelist_key: EPUB/ch022.xhtml#p1060-syllabus-1-assumption-is-the-immediate-act-of-the-divine-nature-in-the
- action: likely_false_positive; file: EPUB/ch023.xhtml; anchor_index: 1150; item_range: p1151-p1153; marker_family: unknown; item_count: 3; announced_count: None; anchor: as unto the outward manner of it, was one and the same, and at once accomplished; but as unto the end of it, which is the exercise of all his offices, it had various respects, various prefiguration, and is distinctly proposed unto us wit...; items: [{'marker': '(1.)', 'text': 'In his ascension, as it was triumphant, three things may be considered:'}, {'marker': '1st', 'text': ', The manner of it, With its representation of old; 2ndly , The place whereinto he ascended; 3rdly , The e...; whitelist_key: EPUB/ch023.xhtml#p1150-syllabus-his-ascension-as-unto-change-of-place-from-earth-to-heaven-and
- action: likely_false_positive; file: EPUB/ch023.xhtml; anchor_index: 1151; item_range: p1152-p1153; marker_family: ordinal; item_count: 2; announced_count: 3; anchor: (1.) In his ascension, as it was triumphant, three things may be considered:; items: [{'marker': '1st', 'text': ', The manner of it, With its representation of old; 2ndly , The place whereinto he ascended; 3rdly , The end of it, or what was the work which he had to do thereon.'}, {'marker': '[1.]', 'text': 'As unto the m...; whitelist_key: EPUB/ch023.xhtml#p1151-syllabus-1-in-his-ascension-as-it-was-triumphant-three-things-may-be
- action: audit_only_weak_anchor; file: EPUB/ch028.xhtml; anchor_index: 1347; item_range: p1348-p1349; marker_family: arabic; item_count: 2; announced_count: None; anchor: But it is from our own sloth and darkness that we do not enjoy more visits of this grace, and that the dawnings of glory do not more shine on our souls. Such things as these may excite us to diligence in the duty proposed unto us. And I ...; items: [{'marker': '1.', 'text': 'What is that glory of Christ which we do or may behold by faith?'}, {'marker': '2.', 'text': 'How do we behold it?'}]; whitelist_key: EPUB/ch028.xhtml#p1347-syllabus-but-it-is-from-our-own-sloth-and-darkness-that-we-do

## Roman Heading Candidates

- file: EPUB/ch033.xhtml; text: I. 1. What he did, what obedience he yielded unto the law of God in the discharge of his office (with respect whereunto he said, "Lo, I come to do thy will, O God; yea, thy law is in my heart"), it was all on his own fre

## Short Fragments

- file: EPUB/ch001.xhtml; text: Edinburgh, August 1850
- file: EPUB/ch009.xhtml; text: All this himself instructs us in.
- file: EPUB/ch011.xhtml; text: This must be declared.
- file: EPUB/ch027.xhtml; text: Christian Reader,
- file: EPUB/ch029.xhtml; text: For, —
- file: EPUB/ch035.xhtml; text: The sum is,
- file: EPUB/ch037.xhtml; text: And, —
- file: EPUB/ch041.xhtml; text: END.
- file: EPUB/ch042.xhtml; text: To The Reader
- file: EPUB/ch045.xhtml; text: END OF PART 2.

## Repeated Windows

- phrase: the glory of god in the face of jesus christ; count: 12
- phrase: unto us child is born unto us son is given; count: 6
- phrase: of the glory of god in the face of jesus; count: 6
- phrase: us child is born unto us son is given and; count: 5
- phrase: the brightness of his glory and the express image of; count: 5
- phrase: brightness of his glory and the express image of his; count: 5
- phrase: of his glory and the express image of his person; count: 5
- phrase: are changed into the same image from glory to glory; count: 5
- phrase: both which are in heaven and which are on earth; count: 5
- phrase: the only-begotten son who is in the bosom of the; count: 5

## Missing Word Samples

- word: greeks; pdf: 3; epub: 0

## Excess Word Samples

- word: preface; pdf: 7; epub: 16
- word: super; pdf: 4; epub: 12
- word: historical; pdf: 2; epub: 10
- word: theological; pdf: 1; epub: 9
- word: digital; pdf: 0; epub: 8
- word: text; pdf: 8; epub: 15
- word: modern; pdf: 3; epub: 10
- word: footnotes; pdf: 0; epub: 7
- word: volume; pdf: 7; epub: 13
- word: dr; pdf: 7; epub: 13

## Untagged Latin Word Samples

- word: incarnate; epub: 35; tagged: 0
- word: nestorius; epub: 8; tagged: 0
- word: consummate; epub: 8; tagged: 0
- word: invocate; epub: 7; tagged: 0
- word: inanimate; epub: 6; tagged: 0
- word: indicate; epub: 5; tagged: 0
- word: serm; epub: 5; tagged: 0
- word: affectionate; epub: 4; tagged: 0
- word: folio; epub: 3; tagged: 0
- word: orat; epub: 3; tagged: 0

## Untranslated Latin Samples

- phrase: quarto (Amsterdam
- phrase: nobis a praelo a capite
- phrase: operis absentibus
- phrase: Salus Electorum Sanguis
- phrase: quam conspici
- phrase: Quod si super unum illum Petrum tantum
- phrase: quid dicturus
- phrase: et apostolorum
- phrase: Num audebimus dicere quod adversus Petrum unum non prevaliturae sunt portae inferorum
- phrase: Unum hoc est

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
