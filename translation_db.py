# -*- coding: utf-8 -*-
"""
translation_db.py — High-fidelity database of modern translations and expanded academic citations
for Greek, Hebrew, Latin, and Patristic passages in John Owen's Works (Volume 1 and Volume 3).
Includes classical philosophers and modern explanations of archaic terms.
"""

# Dictionary mapping global footnote identifier keys (e.g. "v3_fn1") to their modernized translations and citations.
# These will be cleanly appended beneath the original footnote in the endnotes file.
FOOTNOTE_TRANSLATIONS = {
    # --- VOLUME 1 FOOTNOTES ---
    "v1_fn10": (
        "Hebrews 4:14. The Greek phrase <span lang=\"el\" xml:lang=\"el\">διεληλυθότα τοὺς οὐρανούς</span> "
        "transliterates as <i>dielylythota tous ouranous</i>, literally meaning &ldquo;having passed through the heavens,&rdquo; "
        "rather than &ldquo;into the heavens.&rdquo;"
    ),
    
    # --- VOLUME 3 FOOTNOTES ---
    "v3_fn1": (
        "<b>Patristic Source:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29, Section 1 (on 1 Cor. 12:1-2). "
        "Ambrose, <i>On the Holy Spirit</i>, Book 2, Chapter 2. Theophylact of Ohrid, <i>Explanation of the First Epistle to the Corinthians</i>.<br/>"
        "<b>Translation:</b> &ldquo;Calling the signs &lsquo;spiritual&rsquo; because these are the works of the Spirit alone, "
        "with no human effort contributing to the performing of such wonders.&rdquo;"
    ),
    "v3_fn2": (
        "<b>Patristic Source:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29, Section 1 (on 1 Cor. 12:1-2).<br/>"
        "<b>Translation:</b> &ldquo;For some had lesser gifts and others greater, and this became a cause of division for them, "
        "not by its own nature, but because of the lack of consideration of those who received them; for those who had the greater "
        "were puffed up against those who had the lesser, and these on the other hand grieved and envied those who had the greater.&rdquo;"
    ),
    "v3_fn3": (
        "<b>Patristic Source:</b> Ambrose of Milan (Ambrosiaster), <i>Commentary on Paul's Epistles</i>, on 1 Cor. 12:2.<br/>"
        "<b>Translation:</b> &ldquo;Being about to deliver spiritual things to them, he recalls the example of their former behavior; "
        "so that just as they were worshiping idols under the form of images, and were led under the guidance and will of demons, "
        "so also they who worship God might do so according to the form of the Lord's law.&rdquo;"
    ),
    "v3_fn4": (
        "<b>Patristic Source:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29, Section 2 (on 1 Cor. 12:3).<br/>"
        "<b>Translation:</b> &ldquo;Why, then, does no demon call God Lord? Did not the demoniacs say, &lsquo;We know who you are, "
        "the Son of God&rsquo;? Did they not say to Paul, &lsquo;These men are servants of the Most High God&rsquo;? Indeed they did, "
        "but under scourging, under compulsion, whereas of their own free will and uncoerced, never.&rdquo;"
    ),
    "v3_fn7": (
        "<b>Patristic Source:</b> Basil of Caesarea, <i>Homily 15 (On Faith)</i>, Section 3.<br/>"
        "<b>Translation:</b> &ldquo;He is sent according to the divine plan (economically), but acts by His own sovereign power.&rdquo;"
    ),
    "v3_fn9": (
        "<b>Patristic Source:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 106, Section 2 (on John 17:11). "
        "Hilary of Poitiers, <i>On the Trinity</i>, Book 2, Chapter 35.<br/>"
        "<b>Translation:</b> (Augustine) &ldquo;By His spiritual presence He was to be with them everywhere after His ascension, "
        "and with His whole church in this world until the end of the age...&rdquo; / (Hilary) &ldquo;This gift which is in Christ "
        "remains with us unto the end of the age; this is the consolation of our expectation, this is the pledge of our future hope "
        "in the operations of the gifts; this is the light of minds, this is the splendor of souls.&rdquo;"
    ),
    "v3_fn12": (
        "<b>Patristic Source:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 1 (translated into Latin by Jerome).<br/>"
        "<b>Translation:</b> &ldquo;It is indeed necessary to attend to all divine things with reverence and great care, "
        "but especially to those spoken concerning the divinity of the Holy Spirit, particularly since blasphemy against Him is without "
        "forgiveness; so that the blasphemer's punishment is extended not only in the present age, but also in the future. "
        "As the Savior says, blasphemy against the Holy Spirit has no remission, &lsquo;neither in this age nor in the future.&rsquo; "
        "Wherefore it behooves us more and more to attend to what the Scriptures report concerning Him, lest any error of blasphemy "
        "should creep in, at least through ignorance.&rdquo;"
    ),
    "v3_fn13": (
        "<b>Patristic Source:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29, Section 1 (on 1 Cor. 12:1-2).<br/>"
        "<b>Translation:</b> &ldquo;For when someone by certain rites and incantations bound a demon in a man, and that man prophesied, "
        "and while prophesying was thrown down and torn, unable to bear the onset of the demon, but was about to perish miserably, "
        "he says to those who perform such incantations: &lsquo;Release at last the king; a mortal no longer has room for God!&rsquo;&rdquo; "
        "(quoting a pagan oracle)."
    ),
    "v3_fn22": (
        "<b>Patristic Source:</b> Pseudo-Chrysostom (Spurious), <i>On the Adoration of the Holy Spirit</i>.<br/>"
        "<b>Translation:</b> &ldquo;His name is the Holy Spirit, the Spirit of Truth, the Spirit of God, the Spirit of the Lord, "
        "the Spirit of the Father, the Spirit of Christ, and thus the Scripture calls Him; or rather, He Himself calls Himself both "
        "the Spirit of God and the Spirit that is from God.&rdquo;"
    ),
    "v3_fn26": (
        "<b>Patristic Source:</b> Pseudo-Justin Martyr, <i>Cohortatio ad Graecos (Address to the Greeks)</i>, Chapter 32.<br/>"
        "<b>Translation:</b> &ldquo;The gift which descends from God from above upon holy men, which the holy prophets call the Holy Spirit.&rdquo;"
    ),
    "v3_fn51": (
        "<b>Classical &amp; Patristic Source:</b> Pseudo-Justin Martyr, <i>Cohortatio ad Graecos (Address to the Greeks)</i>, Chapter 32 (quoting Plato). "
        "Cyprian of Carthage (or Arnold of Bonneval), <i>De Spiritu Sancto (On the Holy Spirit)</i>.<br/>"
        "<b>Translation:</b> (Justin Martyr) &ldquo;I think that Plato, having clearly learned these things from the prophets "
        "concerning the Holy Spirit, appears to have transferred them to the name of virtue. For just as the holy prophets say "
        "that the one and the selfsame Spirit is divided into seven spirits, so also he, naming one and the selfsame virtue, "
        "says that it is divided into four virtues.&rdquo; / (Cyprian) &ldquo;This is the Holy Spirit whom the magicians in Egypt, "
        "convicted by the display of the third sign, when they confessed that their spells had failed, called the finger of God; "
        "and they intimated to the ancient philosophers that His presence was lacking to them. And although the Platonists had "
        "some conceptions concerning the Father and the Son, yet their spirit, puffed up and desirous of human favor, was unable "
        "to merit the sanctification of the divine mind; and when they came to the depth of the sacraments, all their subtlety "
        "became blind, nor could infidelity draw near to holiness.&rdquo;"
    ),
    "v3_fn55": (
        "<b>Patristic &amp; Philosophical Source:</b> Theophilus of Antioch, <i>To Autolycus</i>, Book 2, Chapter 9. Tertullian, <i>Apology</i>, Chapter 18. "
        "Plotinus (classical philosopher), <i>Enneads</i>, Ennead 3, Book 3, Section 6.<br/>"
        "<b>Translation:</b> (Theophilus) &ldquo;But the men of God, being filled with the Holy Spirit and becoming prophets, inspired "
        "and made wise by God Himself, became taught of God, holy and righteous.&rdquo; / (Tertullian) &ldquo;The prophets uttered words "
        "and likewise performed miracles to establish faith in the divinity.&rdquo; / (Plotinus) &ldquo;For this is not the work of a man, "
        "even a wise or divine one; rather, one might say a god would have this privilege. For it is not the prophet's role to explain the "
        "&lsquo;why,&rsquo; but only to state the &lsquo;that.&rsquo;&rdquo;"
    ),
    "v3_fn57": (
        "<b>Patristic Source:</b> Epiphanius of Salamis, <i>Panarion (Adversus Haereses)</i>, Book 2, Tomus 1 (Haeres. 48, Against the Montanists). "
        "Jerome, <i>Commentary on Isaiah</i>, Prologue. Augustine of Hippo, <i>The City of God</i>, Book 7, Chapter 32.<br/>"
        "<b>Translation:</b> (Epiphanius) &ldquo;For these are truly of prophets who, in the Holy Spirit, have their minds, their teaching, "
        "and their discourse in full vigor.&rdquo; / (Augustine's commentator) &ldquo;The prophets neither understood all their own prophecies, "
        "nor did those who understood understand everything; for they spoke not of themselves but from a higher divine inspiration, "
        "whose counsels were not all manifest to them; and God used them not as consultants of future things, but as instruments through "
        "which He spoke to men.&rdquo;"
    ),
    "v3_fn59": (
        "<b>Patristic Source:</b> Tatian the Syrian, <i>Address to the Greeks</i>, Chapter 13.<br/>"
        "<b>Translation:</b> &ldquo;The Spirit of God is not present in all men, but descending upon some who live righteously and "
        "being conjoined with their soul, by revelations it announced what was hidden to other souls.&rdquo;"
    ),
    "v3_fn63": (
        "<b>Patristic Source:</b> Origen of Alexandria, <i>Commentary on the Gospel of John</i>, Book 30. Jerome, <i>Commentary on Job</i>, "
        "Chapter 33. Cyprian of Carthage, <i>On the Unity of the Church</i>, Section 15.<br/>"
        "<b>Translation:</b> (Origen) &ldquo;But you will inquire whether everyone who prophesies does so by the Holy Spirit; and how is it "
        "not worthy of inquiry, seeing that David, after his sin against Uriah, feared that the Holy Spirit would be taken from him, "
        "whether the Holy Spirit can indeed reside in a sinful soul?&rdquo; / (Jerome) &ldquo;They also used the mystery of prophecy who "
        "had gone astray from true religion, because God gave them His word that they might announce future mysteries to men.&rdquo; / "
        "(Cyprian) &ldquo;For both to prophesy and to cast out demons and to perform great miracles on earth is indeed a high and wonderful "
        "thing, yet not everyone who is found in all these things obtains the heavenly kingdom unless he walks in the observance of "
        "the right and just path.&rdquo;"
    ),
    "v3_fn64": (
        "<b>Patristic Source:</b> Origen of Alexandria, <i>Commentary on the Gospel of John</i>, Book 30, Section 30.<br/>"
        "<b>Translation:</b> &ldquo;If anyone indeed is a Prophet, he by all means prophesies; but if anyone prophesies, he is not "
        "by all means a Prophet. And from what is recorded about Caiaphas prophesying concerning the Savior, it is clear that even "
        "a wicked soul sometimes receives the gift of prophecy.&rdquo;"
    ),
    "v3_fn68": (
        "<b>Patristic Source:</b> Athanasius of Alexandria, <i>Orations Against the Arians</i>, Oration 3, Section 43 (formerly referred to as Oration 4). "
        "John Chrysostom, <i>Spurious/Pseudo-Chrysostom</i>, Sermon 117. Leontius of Byzantium, <i>On Sects</i>.<br/>"
        "<b>Translation:</b> (Athanasius) &ldquo;It is clear that as the Word He knows the hour of the end of all things, but as man "
        "He is ignorant of it. For ignorance is proper to man, especially in these matters. But this also belongs to the Savior's love "
        "for mankind. For since He became man, He was not ashamed, on account of the ignorant flesh, to say &lsquo;I do not know,&rsquo; "
        "in order to show that while knowing as God, He is ignorant in a human/fleshly way.&rdquo; / (Chrysostom) &ldquo;He is ignorant, "
        "therefore, according to the form of His humanity, who knows all things according to the power of His divinity.&rdquo; / "
        "(Leontius) &ldquo;But it must be known that many of the Fathers, indeed almost all, appear to say that He was ignorant. "
        "For if He is said to be in all things consubstantial with us, and we are ignorant, it is clear that He also was ignorant.&rdquo;"
    ),
    "v3_fn70": (
        "<b>Patristic Source:</b> <i>Canons of the Home Synod of Constantinople (A.D. 543)</i>, Canon 1 (against the Origenists).<br/>"
        "<b>Translation:</b> &ldquo;If anyone says that the body of our Lord Jesus Christ was first formed in the womb of the holy Virgin "
        "and that afterward God the Word and the soul, as having pre-existed, were united with it, let him be anathema.&rdquo;"
    ),
    "v3_fn72": (
        "<b>Patristic Source:</b> Pseudo-Chrysostom (Spurious), <i>Homily on the Holy Spirit</i>.<br/>"
        "<b>Translation:</b> &ldquo;If therefore the sovereign flesh, the creation of the Lord, the strange man, the heavenly one, the new "
        "offshoot that blossomed from a strange birth, receives the Holy Spirit...&rdquo;"
    ),
    "v3_fn75": (
        "<b>Patristic Source:</b> Jobius the Monk, <i>Treatise on the Incarnation</i>, preserved in Photius, <i>Bibliotheca</i>, Codex 222.<br/>"
        "<b>Translation:</b> &ldquo;And indeed, for those who are remade to enjoy sanctification, and to remain in this recreation, "
        "belongs to the creation and preservation of the All-Holy Spirit.&rdquo;"
    )
}

# Database mapping unique Greek, Hebrew, and Latin strings inside the text body of Volume 1 and Volume 3
# to their English translations. If one of these keys is found in the body prose, a bracketed footnote ref (e.g. `[1]`)
# will be injected immediately after it.
BODY_TRANSLATIONS = {
    # --- VOLUME 1 BODY PHRASES ---
    "ΘΕΟΛΟΓΟΥΜΕΝΑ ΠΑΝΤΟΔΑΠA": "Various Theological Writings (Owen's Latin title for his massive Latin work on the history of theology).",
    "ΘΕΟΛΟΓΟΥΜΕΝΑ ΠΑΝΤΟΔΑΠΆ": "Various Theological Writings.",
    "ΘΕΟΛΟΓΟΥΜΕΝΑ ΠΑΝΤΟΔΑΙΙΑ": "Various Theological Writings (originally parsed as Greek/Latin hybrid).",
    
    "υτος εστιν ηε προς τον Πατερα αγουσα ηοσος, ηε πετρα, ηε κλεις, ηε ποιμεν": (
        "&ldquo;This is the way leading to the Father, the rock, the key, the shepherd&rdquo; "
        "(Ignatius of Antioch, <i>Epistle to the Philadelphians</i>, Chapter 9)."
    ),
    
    "Ητε ὀνομαστὶ προθεσπισθεῖσα ἐκκλησία αὐτοῦ ἕστηκε κατὰ βάθους ἐῤῥιζωμένη, καὶ μέχρις οὐρανίων ἁψίδων εὐχηαῖς ὀσίων καὶ θεοφιλῶν ἀνδρῶν μετεωριζομένη διὰ μίαν ἐκείνην, ἥν αὐτὸς ἀπεφήνατο λέξιν, εἴπων, Επὶ τὴν πέτραν οἰκοδομήσω μου τὴν ἐηκκλησίαν, καὶ πύλαι ᾅδου οὐ κατισχύσουσιν αὐτῆς": (
        "&ldquo;His church, foretold by name, stands rooted in the deep, and lifted up to the heavenly vaults by the prayers of holy "
        "and God-loving men, because of that one word which He Himself declared, saying: &lsquo;Upon this rock I will build My church, "
        "and the gates of Hades shall not prevail against it.&rsquo;&rdquo; (Eusebius of Caesarea, <i>Ecclesiastical History</i>, Book 10, Chapter 4)."
    ),
    
    "Επὶ τῇ πέτρᾳ ταυτῃ τῆς ἀσφαλοῦς πίστεως οἰκοδομήσω μοῦ τὴν ἐκκλεσίαν": (
        "&ldquo;Upon this rock of secure faith I will build My church&rdquo; (Commonly attributed to Origen or early Greek commentators on Matthew 16:18)."
    ),
    
    "ὁμοιούσιος, ἑτερούσιος, ἐξ οὐκ ὀ": (
        "<i>homoiousios</i> (of similar substance), <i>heterousios</i> (of different substance), <i>ex ouk onton</i> (from things that do not exist)."
    ),
    
    "μίαν φύσιν": "&ldquo;one nature&rdquo; (Cyril of Alexandria's christological formula).",
    
    "ὅτι κατ' ἀλήθειαν ἐστὶ μία φύσις τοῦ λόγου σεσαρκωμένη": (
        "&ldquo;that in truth there is one incarnate nature of the Word&rdquo; "
        "(Cyril of Alexandria, <i>Epistle 46 to Succensus</i>; also cited at the Council of Ephesus)."
    ),
    
    "Τὸν Θεοῦ μεσίτην καὶ ἀνθρώπων, κατὰ τὰς γραφὰς συγκεῖσθαι φάμεν ἔκ τε τῆς καθ' ἡμᾶς ἀνθρώποτητος τελείως ἐχοῦσας κατὰ τὸν ἴδιον λόγον, καὶ ἐκ τοῦ πεφηνότος, ἐκ Θεοῦ κατὰ φύσιν υἱοῦ": (
        "&ldquo;We say that the Mediator between God and men, according to the Scriptures, is composed both of our humanity, "
        "which is perfect according to its own character, and of Him who appeared, who is by nature the Son of God&rdquo; "
        "(Cyril of Alexandria, <i>Scholia on the Incarnation of the Only-Begotten</i>)."
    ),
    
    "ἔνωσιν φυσικὴν": "natural union (Greek: <i>henōsin physikēn</i>).",
    "ἕνωσιν κατὰ σύνθεσιν": "union by composition (Greek: <i>henōsin kata synthesin</i>).",
    
    "הִשְׁתַחֲוָה": "to bow down, do obeisance, or worship (Hebrew root: <i>hishtachavah</i>).",
    "השְׁתֲחֲווּ־λοֹ כָּλ־אלֹהֲים": "&ldquo;Worship Him, all you gods&rdquo; (Psalm 97:7 / Hebrews 1:6).",
    "בְּנֵι נֵכָר יְכחֲשׁו־لְי": "&ldquo;Foreigners shall submit to me&rdquo; or &ldquo;shall feign obedience to me&rdquo; (Psalm 18:44).",
    "חֶמְדַּת כָּח־הַגּוֹים": "&ldquo;the desire of all nations&rdquo; (Haggai 2:7).",
    "שִׁיר יְדִיδְֹת": "&ldquo;a song of loves&rdquo; or &ldquo;a love song&rdquo; (Psalm 45:1).",
    "צִֹירֵי המעְλοֹת": "&ldquo;the shadows of the steps&rdquo; or &ldquo;degrees&rdquo; (2 Kings 20:9-11).",
    "גְדִיβֵי עַמִים": "&ldquo;the princes of the people&rdquo; or &ldquo;noble ones of the nations&rdquo; (Psalm 47:9).",
    "אַתָה הוּα": "&ldquo;You are He&rdquo; (Psalm 102:27 / Hebrews 1:12).",
    "חִידוֹת": "riddles, dark sayings, or mysterious utterances (Hebrew plural of <i>chidah</i>).",
    "מֵצִיץ": "peering, looking, or glancing through the lattice (Song of Solomon 2:9).",

    # --- VOLUME 3 BODY PHRASES ---
    "Εκ τῶν θείων γραφᾶν θεολογοῦμεν κἇν θέλωσιν οἱ ἐχθροὶ κἆν μή": (
        "&ldquo;We speak of theology from the divine Scriptures, whether our enemies want it or not&rdquo; "
        "(Early Greek patristic maxim, frequently quoted by Athanasius and Chrysostom)."
    ),
    
    "Περὶ δὲ τῶν πνευματικῶν": "&ldquo;Now concerning spiritual gifts&rdquo; (1 Corinthians 12:1).",
    "Ζηλοῦτε δὲ τὰ χαρίσματα τὰ κρείττνα": "&ldquo;But earnestly desire the greater gifts&rdquo; (1 Corinthians 12:31).",
    "τὰ πνευματικὰ": "spiritual things, or spiritual gifts (Greek: <i>ta pneumatika</i>).",
    "τὰ χαρίσματα": "gifts of grace, or charismatic endowments (Greek: <i>ta charismata</i>).",
    "Ζηλοῦτε δὲ τὰ πνευματικά": "&ldquo;And earnestly desire spiritual gifts&rdquo; (1 Corinthians 14:1).",
    "ὠς ἆν ἤγεσθε ἀπαγόμενοι": "&ldquo;however you were led, being carried away&rdquo; (1 Cor. 12:2).",
    "περὶ τῶν πνευματικῶν": "concerning spiritual gifts (Greek: <i>peri tōn pneumatikōn</i>).",
    "Φανέρωσις τοῦ Πνεύματος": "&ldquo;the manifestation of the Spirit&rdquo; (1 Corinthians 12:7).",
    "Πρὸς τὸ δυμφέρον": "&ldquo;for the common good&rdquo; or &ldquo;for that which is profitable&rdquo; (1 Cor. 12:7; misspelled in original text as <i>dumpheron</i> for <i>sympheron</i>).",
    "Πρὸς τὸ συμφέρον": "&ldquo;for the common good&rdquo; (1 Corinthians 12:7).",
    
    "יֵשׁוּעַ": "Jesus (Hebrew name: <i>Yeshua</i>, meaning &ldquo;He will save&rdquo;).",
    "יֵשׁוּ": "Yeshu (a Rabbinic polemical abbreviation/anagram for Jesus).",
    "יִΜַח שְׁמוֹ וְזִכְרוֹ": "&ldquo;May his name and memory be blotted out&rdquo; (Hebrew polemical phrase: <i>yimach shemo ve-zichro</i>).",
    "יְהוָֹה": "Yahweh / Jehovah (the sacred Tetragrammaton, the personal name of God in Hebrew).",
    "נלינא דרוחה": "revelation of the Spirit (Aramaic/Syriac phrase).",
    "יוּחַ": "spirit, wind, or breath (originally written Hebrew/Aramaic term).",
    "רוּחַ": "spirit, breath, or wind (Hebrew: <i>ruach</i>).",
    "רוּחַ עַל־הָאָרֶץ וַיַעֲβֵר ־אלֹהִיַם": "&ldquo;And God caused a wind to pass over the earth&rdquo; (Genesis 8:1).",
    "רוּחַ נְדוֹλָה וְχָזָκ": "&ldquo;a great and strong wind&rdquo; (1 Kings 19:11).",

    # --- ARCHAIC PURITAN TERMS (VOLUME 1 & 3) ---
    "preventing the singular and individual subsistence": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Preventing&rdquo; in 17th-century English "
        "signified &ldquo;preceding,&rdquo; &ldquo;anticipating,&rdquo; or &ldquo;going before&rdquo; (Latin: <i>praeveniens</i>). "
        "Here, Owen means that Christ's divine Personhood anticipated and assumed the human nature in the instant of its formation, "
        "so that the human nature never existed as an independent individual prior to the Union."
    ),
    "preventing grace": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Preventing&rdquo; here means &ldquo;preceding&rdquo; "
        "or &ldquo;going before&rdquo; (Latin: <i>gratia praeveniens</i>). It refers to the theological concept of "
        "prevenient grace—the grace of God that acts on a sinner's heart prior to any human decision or merit."
    ),
    "prevented the same honor": (
        "<b>Editorial Explanation:</b> Standard usage. &ldquo;Prevented&rdquo; here has its modern meaning of "
        "&ldquo;hindered&rdquo; or &ldquo;stopped.&rdquo;"
    ),
    "prevented many from purchasing": (
        "<b>Editorial Explanation:</b> Standard usage. &ldquo;Prevented&rdquo; here has its modern meaning of "
        "&ldquo;hindered&rdquo; or &ldquo;stopped.&rdquo;"
    ),
    "prevent the fraud of those": (
        "<b>Editorial Explanation:</b> Standard usage. &ldquo;Prevent&rdquo; here means &ldquo;forestall&rdquo; "
        "or &ldquo;thwart.&rdquo;"
    ),
    "life and conversation": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Conversation&rdquo; in 17th-century theological English "
        "refers to one's entire conduct, behavior, manner of life, or spiritual citizenship (from Latin <i>conversatio</i> "
        "and Greek <i>anastrophē</i>), rather than verbal speech."
    ),
    "whole conversation on the earth": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Conversation&rdquo; refers to Christ's entire conduct, "
        "lifestyle, manner of life, and moral walk on earth."
    ),
    "midst of my bowels": (
        "<b>Editorial Explanation:</b> Archaic usage. In Puritan and Elizabethan English, &ldquo;bowels&rdquo; "
        "(translating Hebrew <i>me'im</i>) was the standard term for the seat of deep affections, enlivened desires, "
        "innermost compassion, and the heart."
    ),
    "bowels and compassion": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Bowels&rdquo; refers to the heart, deep seat of emotions, "
        "or tender mercy."
    ),
    "express our resentment": (
        "<b>Editorial Explanation:</b> Archaic usage. In the 17th century, &ldquo;resentment&rdquo; (from French "
        "<i>ressentiment</i>) indicated a deep, lively sense of gratitude, appreciation, or reciprocated feeling in "
        "response to a favor, completely opposite to its modern negative connotation of bitter anger."
    ),
    "constantly admire as the most": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Admire&rdquo; in early modern English meant to wonder at, "
        "marvel, or contemplate with awe and astonishment."
    ),
    "is admired by Leo": (
        "<b>Editorial Explanation:</b> Archaic usage. &ldquo;Admired&rdquo; here means held in marveling awe or "
        "contemplated with sacred wonder."
    )
}
