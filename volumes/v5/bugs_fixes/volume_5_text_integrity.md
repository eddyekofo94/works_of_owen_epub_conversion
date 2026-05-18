# Text Integrity Audit: Volume 5

- Status: **WARN**
- Warnings: 11
- PDF pages: 576
- EPUB text files: 38
- EPUB paragraphs/headings: 2295

## Coverage

- PDF content tokens: 199515
- EPUB content tokens: 197605
- Approximate PDF-to-EPUB coverage ratio: 0.9889
- Pages checked: 571
- Weak page matches: 16
- Dense source windows checked: 952
- Missing dense source-window pages: 562
- Front CONTENTS pages checked: 6
- Missing front CONTENTS pages: 0
- Top-of-page body windows checked: 564
- Top-of-page windows skipped as unstable: 24
- Missing top-of-page body windows: 7
- Bottom-of-page body windows checked: 536
- Bottom-of-page windows skipped as unstable: 24
- Missing bottom-of-page body windows: 14

## Paragraphs

- Body paragraphs checked: 2180
- Possible faulty paragraph splits: 100
- Structural starts excluded from split warnings: 269
- Short fragments: 40
- Adjacent duplicate paragraphs: 0
- Inline structural marker candidates: 1
- Reference continuation splits: 0
- Citation continuation splits: 0
- Suspicious large-number starts: 0
- Roman heading candidates: 10
- Overlong heading candidates: 0
- Front-matter heading/body candidates: 0
- Repeated word windows: 25
- PDF enumerator markers: 436
- EPUB enumerator markers: 436
- Missing enumerator marker forms: 0
- Enumerator sequence candidates: 0

## Greek / Hebrew

- PDF Greek words: 1161
- EPUB Greek words: 1135
- Greek word coverage ratio: 0.9752
- PDF Hebrew words: 149
- EPUB Hebrew words: 149
- Hebrew word coverage ratio: 0.4823
- Greek clauses checked: 64
- Missing Greek clauses: 64
- Hebrew clauses checked: 20
- Missing Hebrew clauses: 19

## Warnings

- `weak_page_coverage`: Some PDF pages have no strong text-window match in the EPUB
- `dense_source_window_loss`: Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors
- `top_of_page_text_loss`: Some first body lines near the top of PDF pages are not found in the EPUB
- `bottom_of_page_text_loss`: Some last body lines near the bottom of PDF pages are not found in the EPUB
- `paragraph_split_candidates`: Some adjacent EPUB paragraphs look like possible faulty line or page breaks
- `inline_structural_markers`: Some list or roman markers appear embedded in prose instead of starting their own paragraph
- `roman_heading_candidates`: Some roman numeral headings appear in body paragraphs instead of centered heading elements
- `repeated_windows`: Repeated word windows may indicate ghost-layer duplication
- `low_hebrew_word_coverage`: EPUB Hebrew word coverage against PDF extraction is lower than expected
- `missing_greek_clauses`: Some dense Greek passages from the PDF are missing from the EPUB
- `missing_hebrew_clauses`: Some dense Hebrew passages from the PDF are missing from the EPUB

## Missing Dense Source Windows

- page: 5; sample: by it from jus and justum justus filius who the hebrew עהחְעדּיק use and
- page: 9; sample: romans l2-21 boasting excluded in ourselves asserted in god the design and sum of
- page: 10; sample: 10 the exception removed righteousness before conversion not intended by the apostle chapter 19
- page: 11; sample: 11 counted unto him for righteousness when he offered his son on the altar
- page: 13; sample: 13 prefatory note there is pregnant and striking passage in one of the charges
- page: 14; sample: 14 aut cadentis ecclesiae it had to encounter accordingly strong opposition from all who
- page: 15; sample: 15 made transition from the ground of justification by faith to views clearly opposed
- page: 16; sample: 16 should be carefully examined before they were embraced his work therefore is not
- page: 17; sample: 17 first under an inquiry into the meaning of the different terms commonly employed
- page: 18; sample: 18 here the three objections of socinius that such an imputation of christ's obedience

## Missing Top-Of-Page Body Windows

- page: 9; sample: Romans 5:l2-21 — Boasting excluded in ourselves, asserted in God — The design and sum of the apostle's argument — Objection of Socinus removed —
- page: 10; sample: The exception removed — Righteousness before conversion, not intended by the apostle
- page: 430; sample: was not a mere preparation or qualification of his person for his suffering, yet its efficacy unto our justification did depend on his suffering that was
- page: 520; sample: In particular, faith herein rejoices in the manifestation of the infinite wisdom of God. A view of the wisdom of God acting itself by his power
- page: 533; sample: forbidden in the law, and it passes an acquitting or condemning judgment and sentence, according to what men have done.
- page: 551; sample: without self-abasement on the performance of them, will hardly find any other clear evidence of saving faith in himself.
- page: 559; sample: the diligent performance of several duties. And this is that which is here intended, — namely, a peculiar, constant, prevalent exercise of the grace

## Missing Bottom-Of-Page Body Windows

- page: 9; sample: with respect unto the law and gospel — External righteousness only required by the law, an impious imagination — Works wrought before faith only rejected —
- page: 10; sample: and causes; the other, as unto its signs and evidence — Proved by the instances insisted on — How the Scripture was fulfilled, that Abraham believed in God, and it was
- page: 108; sample: Acts 16:30,31. believe for his deliverance,
- page: 127; sample: Isaiah 53:6. So he was "raised for therein "laid all our sins upon him,"
- page: 151; sample: Galatians 3:14; — the 26:18; — the "promise of the Spirit,"
- page: 170; sample: 1 Kings 8:31,32, expressed in the former antithesis.
- page: 193; sample: Romans 8:1,33,34. not be so in them. See
- page: 198; sample: justification, as that which is by the same means only, 10:38,39,
- page: 200; sample: Hebrews 6:12,15. Wherefore, there is accomplishment of the promises,
- page: 429; sample: actual obedience would justify sinners from the condemnation that was passed on them for the sin of Adam; so, although the obedience of Christ

## Possible Paragraph Splits

- file: EPUB/ch004.xhtml; previous: PREVIOUSLY NECESSARY UNTO THE EXPLANATION OF THE DOCTRINE OF JUSTIFICATION; next: That we may treat of the doctrine of justification usefully unto its proper ends, which are the glory of God in Christ, with the peace and furtherance of the obedience of believers
- file: EPUB/ch005.xhtml; previous: JUSTIFYING FAITH; THE CAUSES AND OBJECT OF IT DECLARED; next: The means of justification on our part is faith. That we are justified by faith, is so frequently and so expressly affirmed in the Scripture, as that it cannot directly and in term
- file: EPUB/ch006.xhtml; previous: THE NATURE OF JUSTIFYING FAITH; next: That which we shall now inquire into, is the nature of justifying faith; or of faith in that act and exercise of it whereby we are justified, or whereon justification, according un
- file: EPUB/ch007.xhtml; previous: THE USE OF FAITH IN JUSTIFICATION; ITS ESPECIAL OBJECT FARTHER CLEARED; next: The description before given of justifying faith does sufficiently manifest of what use it is in justification; nor shall I in general add much unto what may be thence observed unt
- file: EPUB/ch008.xhtml; previous: OF JUSTIFICATION; THE NOTION AND SIGNIFICATION OF THE WORD IN SCRIPTURE; next: Unto the right understanding of the nature of justification, the proper sense and signification of these words themselves, justification and to justify, is to be inquired into; for
- file: EPUB/ch009.xhtml; previous: THE DISTINCTION OF A FIRST AND SECOND JUSTIFICATION EXAMINED — THE CONTINUATION OF JUSTIFICATION: — WHEREON IT DOES DEPEND; next: Before we inquire immediately into the nature and causes of justification, there are some things yet previously to be considered, that we may prevent all ambiguity and misunderstan
- file: EPUB/ch009.xhtml; previous: at this grace and the works of it need no farther respect unto the righteousness of Christ, to deserve our second justification and life eternal, as does Vasquez expressly, in 1,2,; next: q. 114, disp. 222, cap. 3; yet many of them affirm that it is still from the consideration of the merit of Christ that they are so meritorious. And the same, for the substance of i
- file: EPUB/ch010.xhtml; previous: EVANGELICAL PERSONAL RIGHTEOUSNESS, THE NATURE AND USE OF IT — FINAL JUDGMENT, AND ITS RESPECT UNTO JUSTIFICATION; next: The things which we have discoursed concerning the first and second justification, and concerning the continuation of justification, have no other design but only to clear the prin
- file: EPUB/ch011.xhtml; previous: IMPUTATION, AND THE NATURE OF IT; WITH THE IMPUTATION OF THE RIGHTEOUSNESS OF CHRIST IN PARTICULAR; next: The first express record of the justification of any sinner is of Abraham.
- file: EPUB/ch012.xhtml; previous: OF THE SINS OF THE CHURCH UNTO CHRIST — GROUNDS OF IT — THE NATURE OF HIS SURETISHIP — CAUSES OF THE NEW COVENANT — CHRIST AND THE CHURCH ONE MYSTICAL PERSON — CONSEQUENTS THEREOF; next: Those who believe the imputation of the righteousness of Christ unto believers, for the justification of life, do also unanimously profess that the sins of all believers were imput

## Inline Structural Marker Candidates

- file: EPUB/ch022.xhtml; text: This is observed also by the apostle in the New Testament; for twice, expressing the sin-offering by this word, he uses that phrase περὶ ἁμαρτίας , Romans 8:3, Hebrews 10:6; but nowhere uses ἁμαρτία to that purpose. If it be, therefore, ...

## Roman Heading Candidates

- file: EPUB/ch013.xhtml; text: II. Answer the most important general objections against it.
- file: EPUB/ch013.xhtml; text: III. Prove the truth of it by arguments and testimonies of the holy Scripture.
- file: EPUB/ch013.xhtml; text: I. As to the first of these, or what is necessary unto the explanation of this assertion, it has been sufficiently spoken unto in our foregoing discourses. The heads of some things only shall at present be called over.
- file: EPUB/ch013.xhtml; text: II. These things being premised, I proceed unto the consideration of the general objections that are urged against the imputation we plead for: and I shall insist only on some of the principal of them, and whereinto all
- file: EPUB/ch016.xhtml; text: II. It is pretended to be useless from hence, because all "our sins of omission and commission being pardoned in our justification on the account of the death and satisfaction of Christ, we are thereby made completely ri
- file: EPUB/ch016.xhtml; text: III. Pernicious also they say it is, as that which takes away "the necessity of our own personal obedience, introducing antinomianism, libertinism, and all manner of evils."
- file: EPUB/ch016.xhtml; text: I. The first part of this charge, concerning the impossibility of the imputation of the obedience of Christ unto us, is insisted on by Socinus de Servat., part 3 cap. 5. And there has been nothing since pleaded unto the
- file: EPUB/ch016.xhtml; text: II. The second part of the objection or charge against the imputation of the obedience of Christ unto us is, "That it is useless unto the persons that are to be justified; for whereas they have in their justification the
- file: EPUB/ch028.xhtml; text: I. How does saving faith approve of this way? on what accounts, and unto what ends?
- file: EPUB/ch028.xhtml; text: II. How it does evidence and manifest itself hereby unto the comfort of believers.

## Short Fragments

- file: EPUB/ch004.xhtml; text: As, —
- file: EPUB/ch005.xhtml; text: Hebrews 6:18, "Fled for refuge."
- file: EPUB/ch006.xhtml; text: THE NATURE OF JUSTIFYING FAITH
- file: EPUB/ch006.xhtml; text: And, —
- file: EPUB/ch008.xhtml; text: Luke 7:29, ΕδικαίΩσαν τὸν Θεόν ?
- file: EPUB/ch008.xhtml; text: Ans. But, —
- file: EPUB/ch009.xhtml; text: For, —
- file: EPUB/ch010.xhtml; text: I answer, —
- file: EPUB/ch011.xhtml; text: And, —
- file: EPUB/ch011.xhtml; text: Wherefore, —

## Repeated Windows

- phrase: of justification by the imputation of the righteousness of christ; count: 12
- phrase: doctrine of justification by the imputation of the righteousness of; count: 11
- phrase: the doctrine of justification by the imputation of the righteousness; count: 10
- phrase: set forth to be propitiation through faith in his blood; count: 10
- phrase: freely by his grace through the redemption that is in; count: 9
- phrase: justified freely by his grace through the redemption that is; count: 8
- phrase: by his grace through the redemption that is in christ; count: 8
- phrase: his grace through the redemption that is in christ jesus; count: 8
- phrase: whom god has set forth to be propitiation through faith; count: 8
- phrase: god has set forth to be propitiation through faith in; count: 8

## Missing Word Samples

- word: חַfָאט; pdf: 4; epub: 0
- word: חַfָעאים; pdf: 3; epub: 0
- word: תוֹרָה; pdf: 3; epub: 0
- word: δικαιοσυνη; pdf: 3; epub: 1
- word: selves; pdf: 3; epub: 1

## Excess Word Samples

- word: חַ; pdf: 0; epub: 8

## Missing Greek Word Samples

- word: δικαιοσύνη; pdf: 3; epub: 1

## Missing Hebrew Word Samples

- word: ָאט; pdf: 4; epub: 0
- word: תוֹרָה; pdf: 3; epub: 0
- word: וַעֲוֹןֹטָם; pdf: 2; epub: 0
- word: חָדַק; pdf: 2; epub: 0
- word: עחחְעדּיק; pdf: 2; epub: 0
- word: חַעדּיק; pdf: 2; epub: 0
- word: רט; pdf: 2; epub: 0

## Missing Greek Clauses

- page: 25; word_count: 12; sample: ἀσεζής ὑπόδικος τῷ θεῷ τῷ δικαιώματι τοῦ θεοῦ κατάραν ἀναπολόγητος συγκεκλεισμένος ἁμαρτίαν
- page: 28; word_count: 5; sample: τολὺς νόμος ἔνθα καὶ ἔνθα
- page: 60; word_count: 40; sample: αὑτὸς τὸν ἴδιον υἱὸν ἀπέδοτο λύτρον ὑπέρ ἡμῶν τὸν ἅγιον ὑπὲρ ἀνόμων
- page: 60; word_count: 11; sample: ἐκείνου δικαιοσύνης ἐν τίνι δικαιωθῆναι δυνατὸν τοὺς ἀνόμους ἡμᾶς καὶ ἀσεζεῖς
- page: 60; word_count: 6; sample: ἐν μόνῳ τῷ υἱῷ τοῦ θεοῦ
- page: 60; word_count: 26; sample: τῶν ἀπροσδοκήτων εὺεργεσιῶν ἵνα ἀνομία μὲν πολλῶν ἐν δικαίῳ ἑνὶ κρυζῇ δικαιοσύνη
- page: 61; word_count: 28; sample: τῆς γλυκείας ἀνταλλαγῆς ποῖος ταῦτα λόγος ποῖος ταῦτα παραστῆσαι δυνήσεται νοῦς τὸν
- page: 61; word_count: 63; sample: πολλῷ μεῖζον ῆν οὐ γὰρ ἕξιν ἔθηκεν ἀλλ αὐτὴν τὴν ποιότηατ οὐ
- page: 148; word_count: 6; sample: πίστει λογιζόμεθα οῦν τίστει δικαιοῦσθαι ἄνθρωπον
- page: 149; word_count: 32; sample: διὰ πίστεως εκ πίστεως διὰ τῆς πίστεως εκ πίστεως καὶ διὰ τῆς

## Missing Hebrew Clauses

- page: 58; word_count: 7; sample: וְןָטַ אֹטָם עַלאראֹשׁ הַצָעעיר חַ ָאט אָשָׁם
- page: 66; word_count: 3; sample: וַעֲוֹןֹטָם הוּא עיסְבֹּל
- page: 168; word_count: 8; sample: חָדַק עכיאאֲעןי אחְדָּק עהענהאןָא עָרַכְעתי עםשְׁףָט יָדַעְעתי עחחְטַדָּק
- page: 169; word_count: 11; sample: וְעהחְדַּקְעתיו וְעהחְעדּיקוּ אטאחַחַעדּיק וְעהרְעשׁיעוּ אטאהָרָשָׁע עהרְעשׁיעַ עחחְעדּיק םַחְעדּיק רָשָׁע וּםַרְעשׁיעַ
- page: 171; word_count: 19; sample: לְהַרְעשׁיעַ רָשָׁע וּלְחַחְעדּיק חַעדּיק עָעןי וָרָשׁ הַחְדּיקוּ לֹאאאַחְעדּיק רָשָׁע חָעלילָה
- page: 219; word_count: 5; sample: חָצַב עלחְדָקָה וַעתחָ צב לוֹ
- page: 221; word_count: 3; sample: עָוִֹ אַלאיַחֲשָׁבאעלי אַדֹעןי
- page: 226; word_count: 5; sample: וְחָטָאעטי לְו כָלאהַיָעםים חַ ָעאים
- page: 239; word_count: 3; sample: עָרַב עָרַב עָרַב
- page: 240; word_count: 5; sample: ערְבָנוּ עהטְעָ רב ןָא עערָבוִֹ

## Limits

Latin word coverage is approximate. Greek/Hebrew font conversion and editorial punctuation still require targeted review.
