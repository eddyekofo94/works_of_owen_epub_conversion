# -*- coding: utf-8 -*-
"""
translation_db.py — High-fidelity database of modern translations and expanded academic citations
for Greek, Hebrew, Latin, and Patristic passages in John Owen's Works (Volume 1 and Volume 3).
Includes classical philosophers and modern explanations of archaic terms.
"""

# Dictionary mapping global footnote identifier keys (e.g. "v3_fn1") to their modernized translations and citations.
# These will be cleanly appended beneath the original footnote in the endnotes file.
# Formatted precisely in modern academic standards (NPNF1, NPNF2, ANF, PL, PG).
FOOTNOTE_TRANSLATIONS = {
    "v3_fn6": (
        "<b>Modern Citation:</b> Desiderius Erasmus, <i>Annotations on the New Testament</i>, on 1 Corinthians 5:4.<br/><b>Translation:</b> &ldquo;From this chapter and the next, one may surmise what were the gifts of that ancient Christian Church before it was burdened with so many ceremonies, riches, empires, forces, wars, and other things of that kind. Now, almost all these eminent offices are reduced to a single Power: that is, a Tyranny cloaked under the name of Christ. For what else is power unless an apostolic mind be present?&rdquo;"
    ),
    "v3_fn8": (
        "<b>Modern Citation:</b> Tertullian, <i>Against Heretics</i> (De Praescriptione Haereticorum), Chapter 28 [ANF 3:256; PL 2.40]. Novatian, <i>On the Trinity</i> (De Trinitate), Chapter 29 [ANF 5:640; PL 3.943]. Pseudo-Cyprian (Spurious), <i>On the Holy Spirit</i> [PL 4.843] (historically attributed to Cyprian, a medieval treatise).<br/><b>Translation:</b> (Tertullian) &ldquo;The Holy Spirit was sent by Christ for this purpose, and asked of the Father for this purpose, to be the teacher of truth, the vicar of Christ.&rdquo; / (Novatian) &ldquo;Since the Lord was about to depart into the heavens, He necessarily gave the Paraclete to the disciples, lest He should leave them in a manner orphans, which was by no means fitting, and desert them without an advocate and a tutor. For this is He who strengthened their minds and souls, who was the illuminator of divine things within them; strengthened by whom, they feared neither prisons nor chains for the name of the Lord; indeed, they trampled upon the very powers of the world and its torments, being now armed and strengthened through Him, having in themselves those gifts which this same Spirit distributes and directs as ornaments, as it were, for the church, the bride of Christ.&rdquo; / (Pseudo-Cyprian) &ldquo;The whole consists of the guidance of the Holy Spirit, that those who err are directed, the ungodly are converted, and the weak are strengthened. The right Spirit, the Holy Spirit, the principal Spirit rules, guides, consumes, and perfects, inhabits our minds, and possesses the hearts which He owns; neither does He suffer those whom He has taught, whom He has possessed, whom He has girded with the sword of the most powerful truth, to err, or be corrupted, or be overcome.&rdquo;"
    ),
    "v3_fn10": (
        "<b>Modern Citation:</b> Novatian, <i>On the Trinity</i>, Chapter 29 [ANF 5:641; PL 3.944] (historically attributed to Tertullian).<br/><b>Translation:</b> &ldquo;This is He who appoints prophets in the church, instructs teachers, directs tongues, works virtues and sanctities, performs wonderful deeds, grants discernments of spirits, contributes governments, suggests counsels, and arranges and disposes whatever other gifts of grace there are; and thereby makes the church consummated and perfected in all things and on every side for the Lord.&rdquo;"
    ),
    "v3_fn11": (
        "<b>Modern Citation:</b> Novatian, <i>On the Trinity</i>, Chapter 29 [ANF 5:641; PL 3.944].<br/><b>Translation:</b> &ldquo;This is He who works from the waters a second birth, a seed of a divine race, and the consecrator of a heavenly birth; the pledge of the promised inheritance and, as it were, a handwriting of eternal salvation; who makes us the temple of God and makes us His house; who intercedes before the divine ears for us with groanings unutterable, performing the duties of advocacy and offering the gifts of defense, an inhabitant dwelling in our bodies, and the effecter of holiness; this is He who restrains insatiable desires,&rdquo; etc."
    ),
    "v3_fn15": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i> (De Spiritu Sancto), Book 1, Prologue (translated into Latin by Jerome) [PL 23.103].<br/><b>Translation:</b> &ldquo;Since some, by rashness rather than the right path, raise themselves even to heavenly heights, and boast these things of the Holy Spirit which are neither read in the Scriptures nor used by any of the ancient church writers, we have been compelled to yield to the frequent exhortation of the brethren, and to prove our opinion of Him also by the testimonies of the Scriptures; lest by ignorance of so great a doctrine, those who oppose contrary views may deceive those who are immediately drawn into the opinion of adversaries without careful discussion.&rdquo;"
    ),
    "v3_fn16": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 1 [PL 23.104].<br/><b>Translation:</b> &ldquo;The name of the Holy Spirit, and the substance shown by the name itself, is completely ignored by those who philosophize outside of the sacred Scripture; for only in our writings is both the notion of Him and the name recorded, both among ourselves and the ancients.&rdquo;"
    ),
    "v3_fn17": (
        "<b>Modern Citation:</b> Pseudo-Cyprian (Spurious), <i>On the Holy Spirit</i> [PL 4.843] (medieval treatise).<br/><b>Translation:</b> &ldquo;Come, Holy Spirit, and descend from heaven upon those who expect Your consolation; sanctify the temple of our body and consecrate it as Your habitation; gladden with Your presence the souls that desire You; prepare a house worthy of You as its inhabitant; adorn Your bridal chamber, and surround the couch of Your rest with the varieties of virtues; strew the pavements with pigments; let Your mansion shine with flaming carbuncles and the splendors of gems; and let the fragrances of all ointments breathe from within; let the liquid balsam imbue its chamber with its sweet fragrance; and driving away from there whatever is decayed, whatever is the seed of corruption, make this our stable and perpetual joy, and solidify the renewal of Your creation in fadeless beauty forever.&rdquo;"
    ),
    "v3_fn18": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 3, Sections 31–41 [PL 23.125–130].<br/><b>Translation Summary:</b> A comprehensive philological and theological analysis of the word &ldquo;spirit&rdquo; (Hebrew: <i>ruach</i>; Greek: <i>pneuma</i>) in the Holy Scriptures. Didymus enumerates its various biblically attested meanings: (1) physical wind or draft (Ezek. 5, Ps. 48); (2) the vital breath of the human soul (James 2, Acts 7, Eccl. 3); (3) the human intellect or mind (1 Cor. 2:11); (4) the Holy Spirit, as distinguished from the human spirit (Rom. 8, 1 Thess. 5); (5) angelic and heavenly rational powers (Heb. 1); (6) unclean demonic spirits (Matt. 12); (7) the human will and internal affection (1 Cor. 7, Isa. 29); and (8) the deeper, mystical sense of Scripture as opposed to the letter (2 Cor. 3). He concludes by refuting the heretical Arians who wrongly cited Amos 4:13 (&ldquo;He who creates the wind/spirit&rdquo;) to argue that the Holy Spirit is a created creature, demonstrating that in Amos the word <i>spirit</i> signifies physical wind."
    ),
    "v3_fn19": (
        "<b>Modern Citation:</b> Editorial Note by William H. Goold on Amos 4:13.<br/><b>Translation Summary:</b> Goold notes that the letter <i>yod</i> is uniformly elided from modern Hebrew editions, so that the word stands as מַה־שֵּׂחוֹ (his thought/utterance) instead of מַה־צִיחוֹ, and that Owen's spelling follows older, less authoritative prints."
    ),
    "v3_fn20": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Habakkuk</i>, on Chapter 2 [PL 25.1310].<br/><b>Translation:</b> &ldquo;Let men learn the custom of Holy Scripture, that a perverse spirit is never called &lsquo;spirit&rsquo; absolutely, but always with some addition, such as: &lsquo;they are seduced by a spirit of fornication&rsquo; (Hos. 4:12), and in the Gospel, &lsquo;when the unclean spirit has gone out of a man&rsquo; (Matt. 12:43), and other things similar to these.&rdquo;"
    ),
    "v3_fn24": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 3, Section 43 [PL 23.131].<br/><b>Translation:</b> &ldquo;The name of sanctification and goodness is referred equally to the Father, to the Son, and to the Holy Spirit; as is also the very appellation of Spirit. For the Father is called Spirit: &lsquo;God is a Spirit&rsquo; (John 4:24); and the Son is called Spirit: &lsquo;Now the Lord is that Spirit&rsquo; (2 Cor. 3:17). But the Holy Spirit is always designated by the title of Holy Spirit; not that He is placed with the Father and the Son merely by a sharing of the name &lsquo;Spirit,&rsquo; but because one nature possesses also one name.&rdquo;"
    ),
    "v3_fn25": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 99.6 [NPNF1, 7:382; PL 35.1888].<br/><b>Translation:</b> &ldquo;There are many testimonies by which this is evidently shown, that He is the Spirit of both the Father and the Son, who in the Trinity is called the Holy Spirit. Nor for any other reason do I think He is properly called &lsquo;Spirit,&rsquo; since even if we are asked about each person individually, we cannot but call both the Father and the Son &lsquo;Spirit&rsquo;; because God is a Spirit—that is, God is not a body, but a Spirit. He ought properly to be called so who is not one of them, but in whom the common union of both appears.&rdquo;"
    ),
    "v3_fn27": (
        "<b>Modern Citation:</b> John Chrysostom (Spurious), <i>On the Holy Spirit</i> [PG 52.813].<br/><b>Translation:</b> &ldquo;He is therefore called the Holy Spirit. For this is the primary and proper designation which most clearly expresses His meaning and surrounds the nature of the Holy Spirit.&rdquo;"
    ),
    "v3_fn29": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 7 [PL 23.107].<br/><b>Translation:</b> &ldquo;Lest anyone suspect that there was one Holy Spirit in the Saints, namely before the advent of the Lord, and another in the apostles and other disciples, and that it is homonymous, as it were, in different substances; we can indeed exhibit testimonies from the divine scriptures that the same Spirit was in both the apostles and the prophets. Paul, in the epistle which he writes to the Hebrews, bringing a testimony from the book of Psalms, mentions that it was spoken by the Holy Spirit.&rdquo;"
    ),
    "v3_fn30": (
        "<b>Modern Citation:</b> John Chrysostom (Spurious), <i>On the Holy Spirit</i> (De Spiritu Sancto) [PG 52.813–814] (historically attributed to Chrysostom, also cited as Pseudo-Chrysostom).<br/><b>Translation:</b> &ldquo;Lest we, hearing of the &lsquo;Spirit of God,&rsquo; should think it is spoken of merely as a friendly relation to God, the Scripture introduces &lsquo;the Holy Spirit&rsquo; and adds &lsquo;of God,&rsquo; &lsquo;that which is of God.&rsquo; But &lsquo;that of God&rsquo; is one thing, and &lsquo;that which is from God&rsquo; is another. For heaven and earth are of God as things made by Him; but nothing is said to be &lsquo;from God&rsquo; unless it is of His very essence.&rdquo;"
    ),
    "v3_fn31": (
        "<b>Modern Citation:</b> John Chrysostom (Spurious), <i>On the Holy Spirit</i> [PG 52.814].<br/><b>Translation:</b> &ldquo;&lsquo;If the Spirit of God dwells in you&rsquo; (Rom. 8:9)—behold, the Spirit of God! &lsquo;But if anyone does not have the Spirit of Christ&rsquo;—indeed, he ought to have said, &lsquo;but if anyone does not have the Spirit of God,&rsquo; yet he said, &lsquo;the Spirit of Christ.&rsquo; He spoke of the Spirit of God, and then brought in the Spirit of Christ: &lsquo;But if anyone does not have the Spirit of Christ, he is none of His.&rsquo; But he said this to show that there is one Spirit, and it is equal to say the Spirit of God and the Spirit of Christ.&rdquo;"
    ),
    "v3_fn32": (
        "<b>Modern Citation:</b> Arnold of Bonneval (historically attributed to Cyprian of Carthage), <i>On the Baptism of Christ</i> (De Baptismo Christi), Section 4 [PL 189.1685].<br/><b>Translation:</b> &ldquo;In this school of divine learning, it is the Father who teaches and instructs; the Son who reveals and opens the secrets of God to us; and the Holy Spirit who fills and endues us. From the Father we receive power, from the Son wisdom, and from the Holy Spirit innocence. The Father elects, the Son loves, the Holy Spirit conjoins and unites.&rdquo;"
    ),
    "v3_fn33": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 2, Section 28 [PL 23.120].<br/><b>Translation:</b> &ldquo;&lsquo;But all these things are worked by one and the self-same Spirit, dividing to each one as He wills&rsquo; (1 Cor. 12:11); wherefore, when speaking of the operative and, so to speak, distributive nature of the Holy Spirit, let us not be led away by those who say that the Holy Spirit is merely an operation and not a substance of God. And from many other places also, the subsisting nature of the Holy Spirit is demonstrated.&rdquo;"
    ),
    "v3_fn34": (
        "<b>Modern Citation:</b> John Chrysostom (Spurious), <i>On the Holy Spirit</i> [PG 52.815]. Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 13 [PL 23.109].<br/><b>Translation:</b> (Chrysostom) &ldquo;Since the Giver is the Holy Spirit, that which is given is also homonymously called the gift.&rdquo; / (Didymus) &ldquo;Nor ought we to think that the Holy Spirit is divided according to substances because a multitude of good things is spoken of—for He is impassible, indivisible, and immutable—but He is called by many names of good things according to different operations and understandings; because He grants communion of Himself to His partakers, not according to one and the same virtue, since indeed He is adapted to the utility of each one.&rdquo;"
    ),
    "v3_fn37": (
        "<b>Modern Citation:</b> Arethas of Caesarea, <i>Commentary on the Apocalypse</i>, on Chapter 1 [PG 106.505].<br/><b>Translation:</b> &ldquo;All things spoken in a manner worthy of God concerning the super-essential Trinity are individualized and harmonized with each of the three Persons (hypostases), except those things which produce their origin—that is, their hypostatic characteristic.&rdquo;"
    ),
    "v3_fn38": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Against Maximinus the Arian</i> (Contra Maximinum), Book 2, Chapter 14.8 (formerly Book 3, Chapter 14) [PL 42.775].<br/><b>Translation:</b> &ldquo;This is not inequality of substance, but order of nature; not that one is prior to the other, but that one is from the other.&rdquo;"
    ),
    "v3_fn40": (
        "<b>Modern Citation:</b> Jobius the Monk, <i>On the Incarnation</i> (De Verbi Incarnatione), preserved in Photius, <i>Bibliotheca</i>, Codex 222, Chapter 18 [PG 103.752].<br/><b>Translation:</b> &ldquo;For under the Old Testament, the Father is preached primarily as the initiator of all things; and secondly, the Son is manifested as the creative cause; and thirdly, the Holy Spirit appears as the perfecter. For the perfecting works are shown in accordance with the end by the progress and growth of things and times, like a crown of proclamation placed upon athletic sweat at the end. Therefore also, having fashioned man first, God then finally breathed into his face the breath of life.&rdquo;"
    ),
    "v3_fn41": (
        "<b>Modern Citation:</b> Editorial Note by William H. Goold on Job 26:13.<br/><b>Translation Summary:</b> Goold notes that the Hebrew reading for &lsquo;by His Spirit&rsquo; (בְרוחוֹ) contains a redundant preposition (<i>bet</i>), which some medieval rabbinic commentators like Abraham Ibn Ezra regarded as redundant, while modern critics translate it directly as &lsquo;By His Spirit the heavens are beauty&rsquo; (<i>shifrah</i>)."
    ),
    "v3_fn42": (
        "<b>Modern Citation:</b> Arnold of Bonneval (historically attributed to Cyprian), <i>On the Holy Spirit</i> (De Spiritu Sancto) [PL 189.1685–1686].<br/><b>Translation:</b> &ldquo;This Holy Spirit is read to have been poured over the waters from the very beginning of the world; not needing material waters as a vehicle, but rather He Himself was bearing them, and gave to the encompassing firmament its proper motion and a pre-defined limit. His eternal power and divinity, although it could not be properly investigated in its own nature by the ancient philosophers... called this life, this motion, this essence of things, the &lsquo;soul of the world&rsquo; (<i>anima mundi</i>)... This is the Spirit of life whose vivifying heat animates all things, cherishes them, promotes them, and makes them fruitful. He is the soul of all living things...&rdquo;"
    ),
    "v3_fn46": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 15 [PL 23.109].<br/><b>Translation:</b> &ldquo;But the word &lsquo;effusion&rsquo; (pouring out) signifies a large and rich abundance of the gift; therefore, when one or two receive the Holy Spirit in any place, it is not said, &lsquo;I will pour out of my Spirit,&rsquo; but only when the gift of the Holy Spirit has overflowed unto all nations.&rdquo;"
    ),
    "v3_fn48": (
        "<b>Modern Citation:</b> Pseudo-Justin Martyr, <i>Exposition of the Right Faith</i> (Expositio Rectae Fidei), Section 1 [PG 6.1208].<br/><b>Translation:</b> &ldquo;For it is not because the Divine is entirely incomprehensible that we should therefore altogether refrain from seeking after Him, spending our life-time in ease; but according to the measure distributed to each by the Lord of knowledge, we ought to make our inquiry with diligent labor, being fully persuaded that He is indeed incomprehensible, yet, so far as we can reach through contemplation, joining ourselves to Him.&rdquo;"
    ),
    "v3_fn52": (
        "<b>Modern Citation:</b> Origen of Alexandria, <i>Commentary on the Gospel of Matthew</i>, Book 15, Section 24 [PG 13.1328].<br/><b>Translation:</b> &ldquo;Among those deemed worthy of the Holy Spirit, there is a difference, with some of the believers receiving more and others less of the Holy Spirit.&rdquo;"
    ),
    "v3_fn53": (
        "<b>Modern Citation:</b> Eusebius of Caesarea, <i>Proof of the Gospel</i> (Demonstratio Evangelica), Book 6, Prologue [PG 22.417].<br/><b>Translation:</b> &ldquo;And note that some things are spoken in riddles, and some more clearly. The things spoken in cover, I think, are given in a veiled manner for the sake of those of the circumcision, because of the gloomy things foretold against them; for which reason it was likely they might even have blotted out the Scripture if it had openly signified their ultimate rejection.&rdquo;"
    ),
    "v3_fn54": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on the Epistle to the Romans</i>, on Chapter 2 (historically attributed to Jerome, actually matching Pelagius's Commentary on Romans) [PL 30.655].<br/><b>Translation:</b> &ldquo;All the prophets knew only those things which had been revealed to them by the Lord. Whence also the king asks Jeremiah in doubt if in that hour in which he was speaking with him the word of the Lord was present with him. But also Elisha says, &lsquo;How has the Lord hidden this from me?&rsquo; and Elijah was ignorant that there were others besides himself who worshipped God.&rdquo;"
    ),
    "v3_fn56": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Habakkuk</i>, on Chapter 2 [PL 25.1293].<br/><b>Translation:</b> &ldquo;But this is also to be noted from what he had said, &lsquo;that I may see what he will speak in me&rsquo;; that prophecy, vision, and the utterance of God do not happen to the prophets from without, but from within, responding to the inner man. Whence also Zechariah says, &lsquo;and the angel who spoke in me said&rsquo; (Zech. 1:9).&rdquo;"
    ),
    "v3_fn58": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Isaiah</i>, Book 1, Prologue [PL 24.19].<br/><b>Translation:</b> &ldquo;Neither did air struck by a voice reach their ears, but God spoke in the soul of the prophets.&rdquo;"
    ),
    "v3_fn60": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Jeremiah</i>, on Chapter 23 [PL 24.817].<br/><b>Translation:</b> &ldquo;But there are many kinds of prophesying, of which one is that of dreams, such as was in Daniel.&rdquo;"
    ),
    "v3_fn61": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Against Adimantus the Manichaean Disciple</i> (Contra Adimantum), Chapter 28 [PL 42.171].<br/><b>Translation:</b> &ldquo;A prophet sees God, who is physically invisible, not physically but spiritually. For many kinds of vision are found in the Holy Scriptures. One is according to the eyes of the body, as Abraham saw three men under the oak of Mamre; another is according to that by which we imagine those things which we perceive through the body... The third kind of vision is according to the intuition of the mind, by which truth and wisdom are beheld by the intellect; without which kind those two which I placed first are either unfruitful or even lead into error.&rdquo;"
    ),
    "v3_fn62": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on the Epistle to Titus</i>, on Chapter 1 [PL 26.564].<br/><b>Translation:</b> &ldquo;There were prophets of Baal, and prophets of confusion, and others of offenses, and whatever vicious prophets the Scripture commemorates.&rdquo;"
    ),
    "v3_fn65": (
        "<b>Modern Citation:</b> Pseudo-Augustine (Spurious), <i>On the Miracles of Holy Scripture</i> (De Mirabilibus Sacrae Scripturae), Book 2, Chapter 10 [PL 35.2177].<br/><b>Translation:</b> &ldquo;Saul, excited by the stimulus of envy and often seized by an evil spirit, when he wished to kill David, and David himself was then prophesying with Samuel and the company of the other prophets, Saul sent messengers and commanded him to be seized from the midst of the prophets to be killed. But he also, when he came among the prophets, prophesied... But indeed, some in this place think that Saul prophesied throughout that whole day not by the Divine Spirit but by that evil spirit by which he was often seized... But how can this be understood when it is written: &lsquo;and the Spirit of the Lord came upon him, and he went on and prophesied&rsquo;? unless perhaps the Spirit of the Lord in this place is understood in the same way as in another place &lsquo;an evil Spirit of the Lord&rsquo; seized Saul...&rdquo;"
    ),
    "v3_fn73": (
        "<b>Modern Citation:</b> Editorial Note by William H. Goold on Job 36:8.<br/><b>Translation Summary:</b> Goold explains that the Hebrew word in the original text is חֶבֶל (cord/rope) or חֵבֶל (pain), noting that Owen's discussion hinges on a difference in vowel points (tsere vs seghol), and references Job 36:8 where the plural in composition with &lsquo;in&rsquo; means &lsquo;cords of affliction&rsquo;."
    ),

    # --- VOLUME 1 FOOTNOTES ---
    "v1_fn10": (
        "Hebrews 4:14. The Greek phrase <span lang=\"el\" xml:lang=\"el\">διεληλυθότα τοὺς οὐρανούς</span> "
        "transliterates as <i>dielylythota tous ouranous</i>, meaning &ldquo;having passed through the heavens,&rdquo; "
        "rather than &ldquo;into the heavens.&rdquo;"
    ),
    
    # --- VOLUME 12 FOOTNOTES ---
    "v12_fn111": (
        "<b>Modern Citation:</b> John Calvin, <i>Institutes of the Christian Religion</i>, ed. John T. McNeill, "
        "trans. Ford Lewis Battles, Library of Christian Classics, vols. 20&ndash;21 (Philadelphia: Westminster Press, 1960), "
        "1.13.3 (discussing the distinction of the Persons in the Trinity). Heinrich Alting, <i>Theologia Elenctica Nova</i>, "
        "Locus 2 (De Deo).<br/>"
        "<b>Translation:</b> &ldquo;See Calvin, <i>Institutes</i>, Book 1, Chapter 13, Section 3; Heinrich Alting, <i>Elenctic Theology</i>, "
        "Locus 2 (On God).&rdquo;"
    ),
    
    # --- VOLUME 3 FOOTNOTES ---
    "v3_fn1": (
        "<b>Modern Citation:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29.1 [NPNF1, 12:168; PG 61.239]. "
        "Ambrose of Milan, <i>On the Holy Spirit</i>, 2.2 [NPNF2, 10:114; PL 16.732]. Theophylact of Ohrid, <i>Explanation of the First Epistle to the Corinthians</i> [PG 124.713].<br/>"
        "<b>Translation:</b> &ldquo;Calling the signs &lsquo;spiritual&rsquo; because these are the works of the Spirit alone, "
        "with no human effort contributing to the performing of such wonders.&rdquo;"
    ),
    "v3_fn2": (
        "<b>Modern Citation:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29.1 [NPNF1, 12:168; PG 61.240].<br/>"
        "<b>Translation:</b> &ldquo;For some had lesser gifts and others greater, and this became a cause of division for them, "
        "not by its own nature, but because of the lack of consideration of those who received them; for those who had the greater "
        "were puffed up against those who had the lesser, and these on the other hand grieved and envied those who had the greater.&rdquo;"
    ),
    "v3_fn3": (
        "<b>Modern Citation:</b> Ambrosiaster (traditionally ascribed to Ambrose), <i>Commentary on the First Epistle to the Corinthians</i>, on 1 Cor. 12:2 [PL 17.257].<br/>"
        "<b>Translation:</b> &ldquo;Being about to deliver spiritual things to them, he recalls the example of their former behavior; "
        "so that just as they were worshiping idols under the form of images, and were led under the guidance and will of demons, "
        "so also they who worship God might do so according to the form of the Lord's law.&rdquo;"
    ),
    "v3_fn4": (
        "<b>Modern Citation:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29.2 [NPNF1, 12:169; PG 61.242].<br/>"
        "<b>Translation:</b> &ldquo;Why, then, does no demon call God Lord? Did not the demoniacs say, &lsquo;We know who you are, "
        "the Son of God&rsquo;? Did they not say to Paul, &lsquo;These men are servants of the Most High God&rsquo;? Indeed they did, "
        "but under scourging, under compulsion, whereas of their own free will and uncoerced, never.&rdquo;"
    ),
    "v3_fn7": (
        "<b>Modern Citation:</b> Basil of Caesarea, <i>Homily 15 (On Faith)</i>, Section 3 [PG 31.468].<br/>"
        "<b>Translation:</b> &ldquo;He is sent according to the divine plan (economically), but acts by His own sovereign power.&rdquo;"
    ),
    "v3_fn9": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 106.2 [NPNF1, 7:397; PL 35.1909]. "
        "Hilary of Poitiers, <i>On the Trinity</i>, Book 2, Chapter 35 [NPNF2, 9:60; PL 10.71].<br/>"
        "<b>Translation:</b> (Augustine) &ldquo;By His spiritual presence He was to be with them everywhere after His ascension, "
        "and with His whole church in this world until the end of the age...&rdquo; / (Hilary) &ldquo;This gift which is in Christ "
        "remains with us unto the end of the age; this is the consolation of our expectation, this is the pledge of our future hope "
        "in the operations of the gifts; this is the light of minds, this is the splendor of souls.&rdquo;"
    ),
    "v3_fn12": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 1 (translated into Latin by Jerome) [PL 23.109].<br/>"
        "<b>Translation:</b> &ldquo;It is indeed necessary to attend to all divine things with reverence and great care, "
        "but especially to those spoken concerning the divinity of the Holy Spirit, particularly since blasphemy against Him is without "
        "forgiveness; so that the blasphemer's punishment is extended not only in the present age, but also in the future. "
        "As the Savior says, blasphemy against the Holy Spirit has no remission, &lsquo;neither in this age nor in the future.&rsquo; "
        "Wherefore it behooves us more and more to attend to what the Scriptures report concerning Him, lest any error of blasphemy "
        "should creep in, at least through ignorance.&rdquo;"
    ),
    "v3_fn13": (
        "<b>Modern Citation:</b> John Chrysostom, <i>Homilies on First Corinthians</i>, Homily 29.1 [NPNF1, 12:168; PG 61.240].<br/>"
        "<b>Translation:</b> &ldquo;For when someone by certain rites and incantations bound a demon in a man, and that man prophesied, "
        "and while prophesying was thrown down and torn, unable to bear the onset of the demon, but was about to perish miserably, "
        "he says to those who perform such incantations: &lsquo;Release at last the king; a mortal no longer has room for God!&rsquo;&rdquo; "
        "(quoting a pagan oracle)."
    ),
    "v3_fn21": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i> (De Spiritu Sancto), Book 1, Chapters 3.39 and 4.55 [NPNF2, 10:97, 99; PL 16.711, 713].<br/>"
        "<b>Translation:</b> &ldquo;He who has denied the Spirit, has denied also God the Father and the Son; since the Spirit of God is the same as the Spirit of Christ... That the Spirit is one, indeed, no one will doubt; although many have doubted concerning the one God.&rdquo;"
    ),
    "v3_fn22": (
        "<b>Modern Citation:</b> Pseudo-Chrysostom (Spurious), <i>On the Adoration of the Holy Spirit</i> [PG 52.813].<br/>"
        "<b>Translation:</b> &ldquo;His name is the Holy Spirit, the Spirit of Truth, the Spirit of God, the Spirit of the Lord, "
        "the Spirit of the Father, the Spirit of Christ, and thus the Scripture calls Him; or rather, He Himself calls Himself both "
        "the Spirit of God and the Spirit that is from God.&rdquo;"
    ),
    "v3_fn26": (
        "<b>Modern Citation:</b> Pseudo-Justin Martyr, <i>Cohortatio ad Graecos (Address to the Greeks)</i>, Chapter 32 [ANF 1:287; PG 6.301].<br/>"
        "<b>Translation:</b> &ldquo;The gift which descends from God from above upon holy men, which the holy prophets call the Holy Spirit.&rdquo;"
    ),
    "v3_fn35": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 1, Chapter 4.43 [NPNF2, 10:98; PL 16.712].<br/>"
        "<b>Translation:</b> &ldquo;Baptize the nations in the name of the Father and of the Son and of the Holy Spirit. He said &lsquo;in the name,&rsquo; not &lsquo;in the names.&rsquo; Therefore, there is not one name of the Father, another name of the Son, another name of the Holy Spirit, but one God.&rdquo;"
    ),
    "v3_fn36": (
        "<b>Modern Citation:</b> Athanasius of Alexandria, <i>First Epistle to Serapion</i>, Section 31 [PG 26.605]. Basil of Caesarea, <i>Homily 17 (On Holy Baptism)</i>, Section 3 [PG 31.432]; <i>Against Eunomius</i>, Book 4 [PG 29.673]. Ambrose of Milan, <i>Exposition of the Apostles' Creed</i> (Expositio in Symbolum Apostolorum), Chapter 9 [PL 17.1162].<br/>"
        "<b>Translation:</b> (Athanasius) &ldquo;Thus from these things also, the one activity of the Trinity is demonstrated. For the apostle does not mean that the things given are different and divided as if from each person; rather, that the things given are given in the Trinity, and all things are from the one God.&rdquo; / (Basil) &ldquo;We see one activity of the Father, the Son, and the Holy Spirit.&rdquo; / (Ambrose) &ldquo;Whatever we have spoken concerning the Holy Spirit, we wish this to be understood likewise commonly and undivided concerning the Father and the Son; because the holy and inseparable Trinity has never known how to operate individually in anything.&rdquo;"
    ),
    "v3_fn39": (
        "<b>Modern Citation:</b> Gregory of Nyssa, <i>On 'Not Three Gods' (To Ablabius)</i> [NPNF2, 5:334; PG 45.125]. Basil of Caesarea, <i>On the Holy Spirit</i> (De Spiritu Sancto), Chapter 16.38 [NPNF2, 8:23; PG 32.136].<br/>"
        "<b>Translation:</b> (Gregory Nyssen) &ldquo;Every activity which reaches from God to the creation, and is named according to various conceptions, begins from the Father, proceeds through the Son, and is perfected in the Holy Spirit.&rdquo; / (Basil) &ldquo;And in the creation of these (angels), think for me of the pre-existent cause of things made, the Father; the creative cause, the Son; the perfecting cause, the Spirit.&rdquo;"
    ),
    "v3_fn43": (
        "<b>Modern Citation:</b> Basil of Caesarea, <i>Homily 15 (On Faith)</i>, Section 3 [PG 31.468].<br/>"
        "<b>Translation:</b> &ldquo;The Holy Spirit is sent economically, but acts by His own sovereign power.&rdquo;"
    ),
    "v3_fn44": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 1, Chapter 11.120 [NPNF2, 10:108; PL 16.725].<br/>"
        "<b>Translation:</b> &ldquo;For if the Spirit proceeds from a place and passes to a place, both the Father Himself and the Son will be found in a place; if He goes out from a place whom the Father or the Son sends, indeed the Spirit passing from a place and proceeding, seems to leave the Father (as a body, according to impious interpretations) and the Son... He comes not from place to place, but from the disposition of His constitution into the salvation of redemption.&rdquo;"
    ),
    "v3_fn45": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 1, Chapter 7.89 [NPNF2, 10:104; PL 16.718].<br/>"
        "<b>Translation:</b> &ldquo;What therefore is more divine than the operation of the Holy Spirit, since God Himself testifies that the Spirit is the author of His blessings, saying, &lsquo;I will pour my Spirit upon thy seed, and my blessings upon thy children.&rsquo; For there can be no full blessing except through the infusion of the Holy Spirit.&rdquo;"
    ),
    "v3_fn47": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>Expositio in Symbolum Apostolorum (Explanation of the Apostles' Creed)</i>, Chapter 3 [PL 17.1158]. "
        "Augustine of Hippo (often attributed to Caesarius of Arles), <i>Sermon 212 (De Tempore)</i> [PL 39.1818].<br/>"
        "<b>Translation:</b> (Ambrose) &ldquo;The Holy Spirit who proceeds from the Father and the Son, Himself has no beginning; because "
        "His procession is continual, and from Him who has no beginning.&rdquo; / (Augustine) &ldquo;The Holy Spirit is neither unbegotten "
        "nor begotten, lest if He were said to be unbegotten like the Father, we should understand two Fathers in the Holy Trinity; "
        "or if He were said to be begotten like the Son, we should judge two Sons to be in the same Holy Trinity; but He is said only "
        "to proceed from the Father and the Son in accordance with the safe faith... but He proceeds from both simultaneously...&rdquo;"
    ),
    "v3_fn49": (
        "<b>Modern Citation:</b> Hilary of Poitiers, <i>On the Trinity</i>, Book 1, Chapter 6 [NPNF2, 9:41; PL 10.29].<br/>"
        "<b>Translation:</b> &ldquo;There is no place without God, nor is there any place that is not in God. He is in the heavens, "
        "He is in hell, He is beyond the seas. Inside He is within, outside He exceeds. Thus while He possesses and is possessed, "
        "He is neither inside anyone in particular, nor is He absent from anything.&rdquo;"
    ),
    "v3_fn51": (
        "<b>Modern Citation:</b> Pseudo-Justin Martyr, <i>Cohortatio ad Graecos (Address to the Greeks)</i>, Chapter 32 [ANF 1:287; PG 6.301] (quoting Plato). "
        "Cyprian of Carthage (Arnold of Bonneval), <i>De Spiritu Sancto (On the Holy Spirit)</i> [PL 189.1648].<br/>"
        "<b>Translation:</b> (Justin Martyr) &ldquo;I think that Plato, having clearly learned these things concerning the Holy Spirit from the prophets, "
        "appears to have transferred them to the name of virtue. For just as the holy prophets say that the one and the selfsame Spirit "
        "is divided into seven spirits, so also he, naming one and the same virtue, says that it is divided into four virtues.&rdquo; / "
        "(Cyprian) &ldquo;This is the Holy Spirit whom the magicians in Egypt, convicted by the third sign, called the finger of God... "
        "And although the Platonists had some conceptions concerning the Father and the Son, yet their spirit, puffed up and desirous "
        "of human favor, was unable to merit the sanctification of the divine mind; and when they came to the depth of the sacraments, "
        "all their subtlety became blind, nor could infidelity draw near to holiness.&rdquo;"
    ),
    "v3_fn55": (
        "<b>Modern Citation:</b> Theophilus of Antioch, <i>To Autolycus</i>, Book 2, Chapter 9 [ANF 2:97; PG 6.1064]. Tertullian, <i>Apology</i>, Chapter 18 [ANF 3:32; PL 1.376]. "
        "Plotinus (classical philosopher), <i>Enneads</i>, Ennead 3, Book 3, Section 6.<br/>"
        "<b>Translation:</b> (Theophilus) &ldquo;But the men of God, being filled with the Holy Spirit and becoming prophets, inspired "
        "and made wise by God Himself, became taught of God, holy and righteous.&rdquo; / (Tertullian) &ldquo;The prophets uttered words "
        "and likewise performed miracles to establish faith in the divinity.&rdquo; / (Plotinus) &ldquo;For this is not the work of a man, "
        "even a wise or divine one; rather, one might say a god would have this privilege. For it is not the prophet's role to explain the "
        "&lsquo;why,&rsquo; but only to state the &lsquo;that.&rsquo;&rdquo;"
    ),
    "v3_fn57": (
        "<b>Modern Citation:</b> Epiphanius of Salamis, <i>Panarion (Adversus Haereses)</i>, Book 2, Tomus 1 (Haeres. 48, Against the Montanists) [PG 41.856]. "
        "Jerome, <i>Commentary on Isaiah</i>, Prologue [PL 24.18]. Augustine of Hippo, <i>The City of God</i>, Book 7, Chapter 32 [NPNF1, 2:140; PL 41.221].<br/>"
        "<b>Translation:</b> (Epiphanius) &ldquo;For these are truly of prophets who, in the Holy Spirit, have their minds, their teaching, "
        "and their discourse in full vigor.&rdquo; / (Augustine's commentator) &ldquo;The prophets neither understood all their own prophecies, "
        "nor did those who understood understand everything; for they spoke not of themselves but from a higher divine inspiration, "
        "whose counsels were not all manifest to them; and God used them not as consultants of future things, but as instruments through "
        "which He spoke to men.&rdquo;"
    ),
    "v3_fn59": (
        "<b>Modern Citation:</b> Tatian the Syrian, <i>Address to the Greeks</i>, Chapter 13 [ANF 2:70; PG 6.833].<br/>"
        "<b>Translation:</b> &ldquo;The Spirit of God is not present in all men, but descending upon some who live righteously and "
        "being conjoined with their soul, by revelations it announced what was hidden to other souls.&rdquo;"
    ),
    "v3_fn63": (
        "<b>Modern Citation:</b> Origen of Alexandria, <i>Commentary on the Gospel of John</i>, Book 30 [PG 14.745]. Jerome (Pseudo-Jerome), <i>Commentary on Job</i>, "
        "Chapter 33 [PL 26.758]. Cyprian of Carthage, <i>On the Unity of the Church</i>, Section 15 [ANF 5:426; PL 4.513].<br/>"
        "<b>Translation:</b> (Origen) &ldquo;But you will inquire whether everyone who prophesies does so by the Holy Spirit; and how is it "
        "not worthy of inquiry, seeing that David, after his sin against Uriah, feared that the Holy Spirit would be taken from him, "
        "whether the Holy Spirit can indeed reside in a sinful soul?&rdquo; / (Jerome) &ldquo;They also used the mystery of prophecy who "
        "had gone astray from true religion, because God gave them His word that they might announce future mysteries to men.&rdquo; / "
        "(Cyprian) &ldquo;For both to prophesy and to cast out demons and to perform great miracles on earth is indeed a high and wonderful "
        "thing, yet not everyone who is found in all these things obtains the heavenly kingdom unless he walks in the observance of "
        "the right and just path.&rdquo;"
    ),
    "v3_fn64": (
        "<b>Modern Citation:</b> Origen of Alexandria, <i>Commentary on the Gospel of John</i>, Book 30, Section 30 [PG 14.756].<br/>"
        "<b>Translation:</b> &ldquo;If anyone indeed is a Prophet, he by all means prophesies; but if anyone prophesies, he is not "
        "by all means a Prophet. And from what is recorded about Caiaphas prophesying concerning the Savior, it is clear that even "
        "a wicked soul sometimes receives the gift of prophecy.&rdquo;"
    ),
    "v3_fn68": (
        "<b>Modern Citation:</b> Athanasius of Alexandria, <i>Orations Against the Arians</i>, Oration 3, Section 43 [NPNF2, 4:417; PG 26.413]. "
        "John Chrysostom (Pseudo-Chrysostom), Sermon 117 [PG 59.620]. Leontius of Byzantium, <i>On Sects</i>, Act 8 [PG 86.1249].<br/>"
        "<b>Translation:</b> (Athanasius) &ldquo;It is clear that as the Word He knows the hour of the end of all things, but as man "
        "He is ignorant of it. For ignorance is proper to man, especially in these matters. But this also belongs to the Savior's love "
        "for mankind. For since He became man, He was not ashamed, on account of the ignorant flesh, to say &lsquo;I do not know,&rsquo; "
        "in order to show that while knowing as God, He is ignorant in a human/fleshly way.&rdquo; / (Chrysostom) &ldquo;He is ignorant, "
        "therefore, according to the form of His humanity, who knows all things according to the power of His divinity.&rdquo; / "
        "(Leontius) &ldquo;But it must be known that many of the Fathers, indeed almost all, appear to say that He was ignorant. "
        "For if He is said to be in all things consubstantial with us, and we are ignorant, it is clear that He also was ignorant.&rdquo;"
    ),
    "v3_fn70": (
        "<b>Modern Citation:</b> <i>Canons of the Home Synod of Constantinople (A.D. 543)</i>, Canon 1 (against the Origenists).<br/>"
        "<b>Translation:</b> &ldquo;If anyone says that the body of our Lord Jesus Christ was first formed in the womb of the holy Virgin "
        "and that afterward God the Word and the soul, as having pre-existed, were united with it, let him be anathema.&rdquo;"
    ),
    "v3_fn71": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Mystery of the Lord's Incarnation</i>, Chapter 7 [NPNF2, 10:270; PL 16.832]. "
        "Didymus the Blind, <i>On the Holy Spirit</i>, Book 2, Section 2 [PL 23.131].<br/>"
        "<b>Translation:</b> (Ambrose) &ldquo;How did He grow in the wisdom of God? Let the order of words teach you. It was a growth of "
        "age, a growth of wisdom, but of human wisdom. Therefore he placed age first, that you might believe it was spoken according "
        "to men; for age is not of the divinity but of the body. Therefore if He grew in the age of man, He grew in the wisdom of man.&rdquo; / "
        "(Didymus) &ldquo;For the Lord as man also received the communication of the Holy Spirit; as we read in the Gospels, &lsquo;Jesus "
        "therefore, full of the Holy Spirit, returned from the Jordan.&rsquo; These things indeed, without any calumny, we ought to receive "
        "with a sense of piety concerning the Lord's humanity...&rdquo;"
    ),
    "v3_fn72": (
        "<b>Modern Citation:</b> Pseudo-Chrysostom (Spurious), <i>Homily on the Holy Spirit</i> [PG 52.815].<br/>"
        "<b>Translation:</b> &ldquo;If therefore the sovereign flesh, the creation of the Lord, the strange man, the heavenly one, the new "
        "offshoot that blossomed from a strange birth, receives the Holy Spirit...&rdquo;"
    ),
    "v3_fn75": (
        "<b>Modern Citation:</b> Jobius the Monk, <i>Treatise on the Incarnation</i>, preserved in Photius, <i>Bibliotheca</i>, Codex 222 [PG 103.748].<br/>"
        "<b>Translation:</b> &ldquo;And indeed, for those who are remade to enjoy sanctification, and to remain in this recreation, "
        "belongs to the creation and preservation of the All-Holy Spirit.&rdquo;"
    ),
    "v3_fn76": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 1, Chapter 6 [NPNF2, 10:102; PL 16.714].<br/>"
        "<b>Translation:</b> &ldquo;If in grace, it is not from the nature of water, but from the presence of the Holy Spirit; do we "
        "indeed live in water as in the Spirit? Are we indeed sealed in water as in the Spirit?&rdquo;"
    ),
    "v3_fn77": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 2, Chapter 9 [NPNF2, 10:114; PL 16.732].<br/>"
        "<b>Translation:</b> &ldquo;Likewise, that we are reborn of the Spirit according to grace, the Lord Himself testifies, saying: "
        "&lsquo;That which is born of the flesh is flesh, because it is born of the flesh; and that which is born of the Spirit is spirit, "
        "because Spirit is God.&rsquo; It is clear, therefore, that the author of spiritual generation is also the Holy Spirit, because "
        "we are created according to God and are children of God...&rdquo;"
    ),
    "v3_fn95": (
        "<b>Modern Citation:</b> <i>Canons of the Second Council of Orange (A.D. 529)</i>, Canon 7 [PL 45.1787; Mansi 8:713].<br/>"
        "<b>Translation:</b> &ldquo;If anyone asserts that by the power of nature man can think as he ought, or choose any good thing that pertains to the salvation of eternal life, or consent to the salutary—that is, the Evangelical—preaching, without the illumination and inspiration of the Holy Spirit... let him be anathema.&rdquo;"
    ),
    "v3_fn97": (
        "<b>Modern Citation:</b> Fulgentius of Ruspe, <i>On Faith, to Peter</i> (De Fide ad Petrum), Chapter 41 [PL 65.704] (traditionally ascribed to Augustine).<br/>"
        "<b>Translation:</b> &ldquo;Hold most firmly and doubt in no way, that a man whom neither ignorance of letters, nor any other weakness or adversity prevents, can indeed either read or hear from the mouth of another the words of the holy Law and Gospel... but he cannot understand it spiritually without the aid of divine grace.&rdquo;"
    ),
    "v3_fn98": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On Grace and Free Will</i>, Chapter 16.32 [NPNF1, 5:458; PL 44.900].<br/>"
        "<b>Translation:</b> &ldquo;The Pelagians think they know something great when they say: &lsquo;God would not command what He knows cannot be done by man.&rsquo; Who does not know this? But He commands some things which we cannot do, so that we may know what we ought to seek from Him.&rdquo;"
    ),
    "v3_fn99": (
        "<b>Modern Citation:</b> Cyprian of Carthage, <i>Three Books of Testimonies Against the Jews</i>, Book 3, Chapter 4 [ANF 5:528; PL 4.734]. "
        "Prosper of Aquitaine, <i>On the Call of All Nations</i> (De Vocatione Omnium Gentium), Book 1, Chapter 7 [PL 51.652].<br/>"
        "<b>Translation:</b> (Cyprian) &ldquo;We must glory in nothing, because nothing is ours.&rdquo; / (Prosper) &ldquo;With faith lost, hope abandoned, understanding blinded, and will captive, man finds no way in himself by which he may be restored.&rdquo;"
    ),
    "v3_fn103": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On Grace and Free Will</i>, Chapter 16.32 [NPNF1, 5:458; PL 44.900].<br/>"
        "<b>Translation:</b> &ldquo;The Pelagians think they know something great when they say: &lsquo;God would not command what He knows cannot be done by man.&rsquo; Who does not know this? But He commands some things which we cannot do, so that we may know what we ought to seek from Him.&rdquo;"
    ),
    "v3_fn104": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Against the Cassianist Collator</i> (Contra Collatorem), Chapter 13.3 [PL 51.249B]; <i>Poem on the Ungrateful</i> (Carmen de Ingratis), lines 407–409 [PL 51.121]; <i>Letter to Rufus on Free Will</i> (Epistola ad Rufinum), Section 15 [PL 51.85].<br/>"
        "<b>Translation:</b> &ldquo;It is most manifest that no virtue dwells in the souls of the ungodly; but all their works are unclean and defiled, they having a wisdom not spiritual but natural... For every work of uprightness, unless it arises from the seed of true faith, is sin, and is turned into guilt; and a sterile glory heaps up punishment for itself... Many praiseworthy and wonderful things can be found in man, which without the marrow of charity indeed have the appearance of piety, but do not have its truth.&rdquo;"
    ),
    "v3_fn106": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Grace of Christ and on Original Sin</i>, Book 1, Chapter 3.3 [NPNF1, 5:218; PL 44.362].<br/>"
        "<b>Translation:</b> &ldquo;Therefore, the grace of God is not in the nature of free will, nor in the law and teaching as Pelagius foolishly raves, but is given for individual acts by the will of Him of whom it is written: &lsquo;You, O God, did send a plentiful rain...&rsquo;&rdquo;"
    ),
    "v3_fn107": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Sermons on Selected Lessons of the Gospels</i>, Sermon 152.3 [NPNF1, 6:426; PL 38.820].<br/>"
        "<b>Translation:</b> &ldquo;But what is that by which the senses of our bodies are struck? In the field of the heart where this cultivation is bestowed, it can neither take root nor send out a shoot, unless that highest and true Husbandman by the power of His operation provides the growth.&rdquo;"
    ),
    "v3_fn108": (
        "<b>Modern Citation:</b> Thomas Aquinas, <i>Summa Theologiae</i>, Prima Secundae (I-II), Q. 109, Art. 3 (discussing whether man can love God above all things by natural powers alone without grace).<br/>"
        "<b>Translation:</b> &ldquo;The will can conform itself to every dictate of right reason; but to love God above all things is a dictate of right reason; for reason dictates that among all things to be loved, there is something to be loved in the highest degree, and this is God.&rdquo;"
    ),
    "v3_fn109": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 86 [NPNF1, 7:353; PL 35.1850].<br/>"
        "<b>Translation:</b> &ldquo;This is the mark of godly minds, that they attribute nothing to themselves, but everything to the grace of God; hence, however much anyone gives to the grace of God, even if he subtracts from the power of nature or free will, he does not depart from piety.&rdquo;"
    ),
    "v3_fn110": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Against the Cassianist Collator</i>, Prologue [PL 51.213].<br/>"
        "<b>Translation:</b> &ldquo;By what dogma the Pelagian heresy attempted to destroy the Catholic faith, and with what poisons of impieties it wished to occupy the bowels of the Church and the very vitals of the body of Christ, are too well known to need prolonged description.&rdquo;"
    ),
    "v3_fn111": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Gift of Perseverance</i>, Chapter 2.3 [NPNF1, 5:522; PL 45.996].<br/>"
        "<b>Translation:</b> &ldquo;In vain and perfunctorily rather than truly do we pour out prayers to God for them, that they may consent by believing to the doctrine which they oppose, if it does not belong to His grace to turn to His faith those whose will is hostile.&rdquo;"
    ),
    "v3_fn112": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Sentences Selected from the Works of St. Augustine</i>, Sentence 120 (historically Sentence 106) [PL 51.442].<br/>"
        "<b>Translation:</b> &ldquo;The first grace of the divine gift is that it instructs us to the confession of our humility, and makes us recognize that if we do any good, we can do it only through Him without whom we can do nothing.&rdquo;"
    ),
    "v3_fn113": (
        "<b>Modern Citation:</b> Jerome (Pseudo-Jerome), <i>Commentary on Proverbs</i>, on Chapter 16 [PL 23.983].<br/>"
        "<b>Translation:</b> &ldquo;Whoever attributes to himself the good that he does, even if he seems to work no evil with his hands, has already lost the innocence of his heart, in which he has preferred himself to the Giver of all good things.&rdquo;"
    ),
    "v3_fn114": (
        "<b>Modern Citation:</b> Bernard of Clairvaux (Pseudo-Bernard), <i>Meditations on the Human Condition</i> (Meditaciones de cognitione humanae conditionis), Chapter 14 [PL 184.505].<br/>"
        "<b>Translation:</b> &ldquo;O good Lord Jesus, although I have committed that for which You can condemn me, You have not lost that by which You are accustomed to save... It is true that my conscience deserves condemnation, and my penitence does not suffice for satisfaction; but Your mercy exceeds all my offenses.&rdquo;"
    ),
    "v3_fn115": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Poem on the Ungrateful</i> (Carmen de Ingratis), lines 435–440 [PL 51.123].<br/>"
        "<b>Translation:</b> &ldquo;The grace by which we are Christ's people is confined by this limit according to you, and you ascribe this form to it: that it indeed calls and invites all, and passing by no one, strives to bring common salvation to everyone... but this denies the sovereign efficacy of special grace.&rdquo;"
    ),
    "v3_fn116": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Sermons on Selected Lessons of the Gospels</i>, Sermon 169.11 [NPNF1, 6:464; PL 38.922].<br/>"
        "<b>Translation:</b> &ldquo;Let us weep before the Lord who made us both men and saved. For if He made us men, but we made ourselves saved, we have made something better than He did; for a saved man is better than any man whatsoever.&rdquo;"
    ),
    "v3_fn117": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Poem on the Ungrateful</i>, lines 450–454 [PL 51.124].<br/>"
        "<b>Translation:</b> &ldquo;But indeed, when the omnipotent grace saves a man, it completes its own work, for which the time of acting is always present for what it wishes done: it is not delayed by morals, nor suspended by any doubtful causes.&rdquo;"
    ),
    "v3_fn118": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Predestination of the Saints</i>, Chapter 8.13 [NPNF1, 5:504; PL 44.970].<br/>"
        "<b>Translation:</b> &ldquo;What is &lsquo;Everyone who has heard from the Father, and has learned, comes to me,&rsquo; except that there is no one who hears from the Father and learns and does not come to me? For if everyone who has heard from the Father and has learned comes, certainly everyone who does not come has not heard from the Father nor learned.&rdquo;"
    ),
    "v3_fn119": (
        "<b>Modern Citation:</b> Gregory the Great, <i>Homilies on the Gospels</i>, Book 2, Homily 30, Section 2 [PL 76.1220].<br/>"
        "<b>Translation:</b> &ldquo;Oh, what a master is that Spirit! There is no delay in learning anything He wills. For as soon as "
        "He has chosen a mind, He teaches it; and merely to have touched it is to have taught it. For He suddenly shines upon and "
        "changes the human heart; suddenly it denies what it was, suddenly it displays what it was not.&rdquo;"
    ),
    "v3_fn120": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 26.2–4 [NPNF1, 7:168; PL 35.1607].<br/>"
        "<b>Translation:</b> &ldquo;Christ does not say &lsquo;leads,&rsquo; so that we might in some way understand that the will precedes; but He says &lsquo;draws.&rsquo; Who, however, is drawn if he was already willing? And yet no one comes unless he is willing; he is drawn, therefore, in wonderful ways...&rdquo;"
    ),
    "v3_fn121": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Predestination of the Saints</i>, Chapter 3.7 [NPNF1, 5:501; PL 44.964].<br/>"
        "<b>Translation:</b> &ldquo;It remains that we must attribute faith itself, from which all righteousness takes its beginning, not to human choice (by which these men are puffed up), nor to any preceding merits (since from it begin whatever merits are good), but to the sovereign gift of God.&rdquo;"
    ),
    "v3_fn122": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Grace of Christ and on Original Sin</i>, Book 1, Chapter 14.15 [NPNF1, 5:223; PL 44.368].<br/>"
        "<b>Translation:</b> &ldquo;When God teaches through the grace of the Spirit, He teaches in such a way that whatever anyone has learned, he not only sees by knowing it, but also seeks by willing it and performs by doing it. And by this divine way of teaching, even the will itself is aided.&rdquo;"
    ),
    "v3_fn123": (
        "<b>Modern Citation:</b> <i>Canons of the Second Council of Orange (A.D. 529)</i>, Canon 6 [PL 45.1786; Mansi 8:713].<br/>"
        "<b>Translation:</b> &ldquo;If anyone asserts that mercy is divinely conferred upon us when we believe, will, desire, or strive without the grace of God; but does not confess that it is through the infusion and inspiration of the Holy Spirit in us that we believe, will, desire... let him be anathema.&rdquo;"
    ),
    "v3_fn124": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Predestination of the Saints</i>, Chapter 3.7 [NPNF1, 5:501; PL 44.964].<br/>"
        "<b>Translation:</b> &ldquo;It remains that we must attribute faith itself, from which all righteousness takes its beginning, not to human choice (by which these men are puffed up), nor to any preceding merits (since from it begin whatever merits are good), but to the sovereign gift of God.&rdquo;"
    ),
    "v3_fn125": (
        "<b>Modern Citation:</b> <i>Canons of the Second Council of Orange</i>, Canon 3 [PL 45.1785; Mansi 8:713].<br/>"
        "<b>Translation:</b> &ldquo;The aid of grace is indeed always to be sought from God, but neither should we assign even what we can do to our own strength. For not even the very desire of prayer can be had unless it has been divinely granted.&rdquo;"
    ),
    "v3_fn126": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Spirit and the Letter</i>, Chapter 24.40 [NPNF1, 5:99; PL 44.225].<br/>"
        "<b>Translation:</b> &ldquo;For this is it: God promises what He Himself does; for He does not promise and another perform, which would no longer be to promise but to foretell. Therefore it is not of works, but of Him who calls, lest it should be of themselves, and not of God.&rdquo;"
    ),
    "v3_fn128": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Sermons on Selected Lessons of the Gospels</i>, Sermon 156.11 [NPNF1, 6:435; PL 38.855].<br/>"
        "<b>Translation:</b> &ldquo;Truly, if the aid of God is lacking, you will be able to do nothing good; you indeed act by free will when He does not aid, but evilly; to this your will (which is called free) is suited, and by doing evilly it becomes damnable.&rdquo;"
    ),
    "v3_fn129": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Tractates on the Gospel of John</i>, Tractate 2.7 [NPNF1, 7:15; PL 35.1392].<br/>"
        "<b>Translation:</b> &ldquo;He was the true light who enlightens every man coming into this world; therefore it was said, because no man is enlightened, except by that light of truth which is God, lest anyone should think he is enlightened by another.&rdquo;"
    ),
    "v3_fn130": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Letter 186</i> (formerly Letter 89 to Paulinus) [NPNF1, 1:568; PL 33.816].<br/>"
        "<b>Translation:</b> &ldquo;Liberty without grace is nothing but stubbornness, not liberty.&rdquo;"
    ),
    "v3_fn131": (
        "<b>Modern Citation:</b> Prosper of Aquitaine, <i>Letter to Rufus on Free Will</i>, Section 18 [PL 51.87].<br/>"
        "<b>Translation:</b> &ldquo;Who changed their hearts, except He who fashioned their hearts individually? Who softened the hardness of this rigor into the disposition of obedience, except He who is able to raise up children to Abraham from these stones?&rdquo;"
    ),
    "v3_fn133": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Confessions</i>, Books 1–13 [NPNF1, 1:45; PL 32.659].<br/>"
        "<b>Context:</b> Augustine's spiritual autobiography (written c. A.D. 397). Owen draws copiously from the <i>Confessions</i> "
        "throughout this chapter to illustrate the nature of the spiritual change implied in conversion."
    ),
    "v3_fn134": (
        "<b>Modern Citation:</b> Bernard of Clairvaux (Pseudo-Bernard), <i>Meditations on the Human Condition</i>, Chapter 14 [PL 184.506].<br/>"
        "<b>Translation:</b> &ldquo;Deliver me, O Lord, from these my enemies, from whom I am not able to deliver myself. Perverse and very evil is my heart; for deploring my own sins it is stony and dry, but for resisting those who insult it, it is soft.&rdquo;"
    ),
    "v3_fn135": (
        "<b>Modern Citation:</b> Bernard of Clairvaux, <i>Meditations on the Human Condition</i>, Chapter 14 [PL 184.506].<br/>"
        "<b>Translation:</b> &ldquo;Truly my sins are an abyss, because they are incomprehensible in depth, and inestimable in number and immensity. O abyss calling to abyss! O my sins, the torments for which you keep me are an abyss.&rdquo;"
    ),
    "v3_fn136": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Good of Widowhood</i> (De Bono Viduitatis), Chapter 6.9 [NPNF1, 3:344; PL 40.435].<br/>"
        "<b>Translation:</b> &ldquo;It is impossible that a body should not be holy when it is used by a sanctified Spirit.&rdquo;"
    ),
    "v3_fn67": (
        "<b>Modern Citation:</b> Cyprian of Carthage (Arnold of Bonneval), <i>On the Baptism of Christ</i> (De Baptismo Christi) [PL 189.1654].<br/>"
        "<b>Translation:</b> &ldquo;I give thanks to You, most merciful God, because what I sought in the morning, You Yourself have first given to me.&rdquo;"
    ),
    "v3_fn69": (
        "<b>Modern Citation:</b> Athanasius of Alexandria, <i>On the Creed of Nicaea</i> [PG 28.1601]. Didymus the Blind, <i>On the Holy Spirit</i>, Book 2 [PL 23.125].<br/>"
        "<b>Translation:</b> (Athanasius) &ldquo;The greatest testimony of the divinity of the Holy Spirit in all creation is the body of the Lord, which is believed to be from the Holy Spirit according to the Evangelist Matthew...&rdquo; / (Didymus) &ldquo;The creative power of the Most High, the Holy Spirit coming upon the Virgin Mary, fashioned Christ's body, which temple He used and was born without the seed of man.&rdquo;"
    ),
    "v3_fn78": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On Original Sin</i>, Chapter 18.20 [NPNF1, 5:244; PL 44.395]; <i>On the Grace of Christ</i>, Book 1, Chapter 3.3 [NPNF1, 5:218; PL 44.362].<br/>"
        "<b>Translation:</b> &ldquo;Observe how he replies, and see how the hiding places of ambiguity prepare refugees for falsehood... He had almost persuaded me to confess that this was the very grace in question...&rdquo;"
    ),
    "v3_fn79": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On Original Sin</i>, Chapter 8.9 [NPNF1, 5:240; PL 44.389].<br/>"
        "<b>Translation:</b> &ldquo;He deceived the Palestinian judgment, and therefore seemed to be cleared there; but the Roman Church... he could not deceive in any way, although he tried both...&rdquo;"
    ),
    "v3_fn81": (
        "<b>Modern Citation:</b> John Davenant, <i>A Treatise on Justification</i> (De Justitia Habituali), Chapter 3 [1631]. Origen of Alexandria, <i>Commentary on the Epistle to the Romans</i>, Book 4, Section 1 [PG 14.960].<br/>"
        "<b>Translation:</b> (Davenant) &ldquo;By inherent righteousness we understand a supernatural gift of sanctifying grace, opposed to original sin, and in individual faculties of the soul repairing and renewing that image of God which by original sin was defiled and scattered...&rdquo; / (Origen) &ldquo;Faith, like a root that has received rain, clings to the soil of the soul; so that when it begins to be cultivated through the law of God, branches rise in it which bear the fruit of works...&rdquo;"
    ),
    "v3_fn82": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 1, Section 10 [PL 23.111].<br/>"
        "<b>Translation:</b> &ldquo;He who is made a partaker of the Holy Spirit, through His communion becomes spiritually co-equal and holy.&rdquo;"
    ),
    "v3_fn83": (
        "<b>Modern Citation:</b> Fulgentius of Ruspe, <i>On the Incarnation and Grace of Christ</i>, Chapters 20 and 29 [PL 65.584, 590].<br/>"
        "<b>Translation:</b> &ldquo;Just as in carnal birth the shaping of the divine work precedes every will of the man being born, so in spiritual birth by which we begin to lay aside the old man... The pattern has preceded in the flesh of Christ, which we spiritually recognize in our faith; for Christ the Son of God, according to the flesh, was conceived and born of the Holy Spirit...&rdquo;"
    ),
    "v3_fn84": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Grace of Christ</i>, Book 1, Chapter 7.8 [NPNF1, 5:220; PL 44.364] (quoting Pelagius).<br/>"
        "<b>Translation:</b> &ldquo;God helps us (the words of Pelagius), through His teaching and revelation, while He opens the eyes of our heart, while He points out the future to us lest we should be occupied with the present...&rdquo;"
    ),
    "v3_fn86": (
        "<b>Modern Citation:</b> <i>Acts of the Synod of Dort (1618&ndash;1619)</i>, Suffrages of the British Theologians on the Fourth Article, Theses 1 &amp; 2.<br/>"
        "<b>Translation:</b> &ldquo;There are certain external works, ordinarily required of men, before they are brought to the state of regeneration or conversion, which are sometimes freely done and sometimes freely omitted; such as going to church, hearing the preaching of the Word... There are certain internal effects previous to conversion or regeneration, which are excited by the power of the Word and the Spirit in the hearts of those not yet regenerated...&rdquo;"
    ),
    "v3_fn87": (
        "<b>Modern Citation:</b> Pseudo-Augustine, <i>On Contrition of Heart</i> (De Contritione Cordis), Chapter 1 [PL 40.943].<br/>"
        "<b>Translation:</b> &ldquo;Alas, wretched and too wretched is he whom his own conscience tortures, which he cannot flee; too wretched whom his own condemnation awaits, unless God snatches him away...&rdquo;"
    ),
    "v3_fn88": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>To Simplician, on Diverse Questions</i>, Book 2, Question 2.3 [PL 40.138].<br/>"
        "<b>Translation:</b> &ldquo;Do we not observe many of our faithful walking the way of God, in no part compared in intellect&mdash;I will not say to certain heretics, but even to lesser men?...&rdquo;"
    ),
    "v3_fn90": (
        "<b>Modern Citation:</b> Johann Ferus (Wild), <i>Commentary on the Gospel of John</i>, on Chapter 1 [1552]. Prosper of Aquitaine, <i>On the Call of All Nations</i>, Book 1, Chapter 7 [PL 51.652].<br/>"
        "<b>Translation:</b> (Ferus) &ldquo;I say that the old birth, and indeed all powers of nature which are transfused into offspring by natural propagation, are condemned in Scripture...&rdquo; / (Prosper) &ldquo;With faith lost, hope abandoned, understanding blinded, and will captive, man finds no way in himself by which he may be restored.&rdquo;"
    ),
    "v3_fn96": (
        "<b>Translation:</b> &ldquo;To the cold ones,&rdquo; from the Paris edition, 1733. &mdash; ED."
    ),
    "v3_fn105": (
        "<b>Modern Citation:</b> Pseudo-Athanasius, <i>On Sowing</i> (De Semente) [PG 28.160].<br/>"
        "<b>Translation:</b> &ldquo;What is the use if the word is well-composed but the behavior is ill-composed? For if the Church were a school of sophistry, it would be the time for eloquence; but since the combat of behaviors and bearing fruit is what lies before us, seek not details but the walk of life.&rdquo;"
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
    
    # --- KEY VOLUME 1 BODY LATIN THEOLOGIAN QUOTATIONS ---
    "Quaero abs te, quando aut quomodo putes filium esse generatum? Mihi enim impossibile est scire generationis secretum Mens deficit, vox silet, non mea tantum, sed et angelorum. Supra potestates, supra angelos, supra cherubim, supra seraphim, supra omnem sensum est. Tu quoque manum ori admovere; scrutari non licet superna mysteria. Licet scire quod ntus sit, non licet discutere quomodu ntus sit; illud negare mihi non licet, hoc quaerere metus est. Nam si Paulus ea quae audivit, raptus in tertium coelu, ineffabilia dicit, quomodo nos exprimere possumus paternae generationis arcanum, quod nec sentire potuimus nec audire? Quid te ista questionum tormenta delectant?": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>Of the Christian Faith</i> (De Fide), Book 1, Chapter 10, Section 64 [NPNF2, 10:212; PL 16.566].<br/>"
        "<b>Translation:</b> &ldquo;I inquire of you when or how the Son was begotten? For me it is impossible to know the secret of this generation. "
        "The mind fails, the voice is silent, not mine only, but even that of angels. It is above powers, above angels, above cherubim, above seraphim, "
        "above all understanding. Lay your hand upon your mouth; it is not permitted to search into these heavenly mysteries. It is permitted to know that He was begotten, "
        "it is not permitted to discuss how He was begotten; the former I am not permitted to deny, the latter I fear to inquire into. For if Paul says that "
        "the things he heard, when caught up into the third heaven, are ineffable, how can we express the mystery of the Father's generation, which we could neither "
        "perceive nor hear? Why do these tortures of questions delight you?&rdquo;"
    ),
    
    "Super hanc Petram, quam confessus es, super meipsum filium Dei vivi, aedificabo ecclesiam meam. Super me aedificabo te, non me super te:": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>Sermons on Selected Lessons of the Gospels</i>, Sermon 76.1 (formerly De Verbis Domini, Sermon 13) [NPNF1, 6:340; PL 38.479].<br/>"
        "<b>Translation:</b> &ldquo;Upon this rock which you have confessed—upon myself, the Son of the living God—I will build my church. I will build you upon myself, not myself upon you.&rdquo;"
    ),
    
    "Ea gratia fit ab initio fidei suae homo quicunque Christianus, qua gratia homo ille ab initio factus est Christus,": (
        "<b>Modern Citation:</b> Augustine of Hippo, <i>On the Predestination of the Saints</i>, Chapter 15.31 [NPNF1, 5:505; PL 44.981].<br/>"
        "<b>Translation:</b> &ldquo;By the same grace every man is made a Christian from the beginning of his faith, as that Man from His beginning was made Christ.&rdquo;"
    ),
    
    "הִשְׁתַחֲוָה": "to bow down, do obeisance, or worship (Hebrew root: <i>hishtachavah</i>).",
    "השְׁתֲחֲווּ־λοֹ כָּλ־אלֹהֲים": "&ldquo;Worship Him, all you gods&rdquo; (Psalm 97:7 / Hebrews 1:6).",
    "בְּנֵι נֵכָר Yְכחֲשׁוּ־لְי": "&ldquo;Foreigners shall submit to me&rdquo; or &ldquo;shall feign obedience to me&rdquo; (Psalm 18:44).",
    "בְּנֵι נֵכָר יְכחֲשׁו־لְי": "&ldquo;Foreigners shall submit to me&rdquo; or &ldquo;shall feign obedience to me&rdquo; (Psalm 18:44).",
    "חֶμְדַּת כָּח־הַגּוֹים": "&ldquo;the desire of all nations&rdquo; (Haggai 2:7).",
    "שִׁיר Yְδִיδְֹת": "&ldquo;a song of loves&rdquo; or &ldquo;a love song&rdquo; (Psalm 45:1).",
    "שִׁיר יְδִיδְֹת": "&ldquo;a song of loves&rdquo; or &ldquo;a love song&rdquo; (Psalm 45:1).",
    "צִֹירֵI הַמַעְלוֹת": "&ldquo;the shadows of the steps&rdquo; or &ldquo;degrees&rdquo; (2 Kings 20:9-11).",
    "צִֹירֵי הַמַעְלוֹת": "&ldquo;the shadows of the steps&rdquo; or &ldquo;degrees&rdquo; (2 Kings 20:9-11).",
    "צִֹירֵי המעְλοֹת": "&ldquo;the shadows of the steps&rdquo; or &ldquo;degrees&rdquo; (2 Kings 20:9-11).",
    "גְדִיבֵI עַמִים": "&ldquo;the princes of the people&rdquo; or &ldquo;noble ones of the nations&rdquo; (Psalm 47:9).",
    "גְדִיβֵי עַמִים": "&ldquo;the princes of the people&rdquo; or &ldquo;noble ones of the nations&rdquo; (Psalm 47:9).",
    "גְדִיבֵי עַמִים": "&ldquo;the princes of the people&rdquo; or &ldquo;noble ones of the nations&rdquo; (Psalm 47:9).",
    "אַתָה הוּα": "&ldquo;You are He&rdquo; (Psalm 102:27 / Hebrews 1:12).",
    "חִידוֹת": "riddles, dark sayings, or mysterious utterances (Hebrew plural of <i>chidah</i>).",
    "מֵצִיץ": "peering, looking, or glancing through the lattice (Song of Solomon 2:9).",

    # --- VOLUME 3 BODY PHRASES ---
    "(Crell. de Natur. Spir. Sanc.)": (
        "<b>Modern Citation:</b> Johannes Crellius (John Crell), <i>Liber de Spiritu Sancto</i> "
        "(On the Holy Spirit, 1631); also known as <i>De Natura Spiritus Sancti</i>, "
        "later compiled in the <i>Bibliotheca Fratrum Polonorum</i> (BFP, 1656), Vol. 4. "
        "Crellius was a leading Socinian theologian who argued that the Holy Spirit is "
        "not a divine Person but a divine energy or power."
    ),
    "Crell. Prolegom., p. 7": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>Prolegomena</i> (Preface) to "
        "<i>Liber de Spiritu Sancto</i> (1631), p. 7 [BFP, Vol. 4]."
    ),
    "Crell. Prolegom., pp. 13, 14": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>Prolegomena</i> to "
        "<i>Liber de Spiritu Sancto</i> (1631), pp. 13–14 [BFP, Vol. 4]."
    ),
    "Crellius, de Spir. Sanc.": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>Liber de Spiritu Sancto</i> (1631) [BFP, Vol. 4]."
    ),
    "Crell. de Spir. Sanc., cap. 5": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>Liber de Spiritu Sancto</i> (1631), Chapter 5 [BFP, Vol. 4]."
    ),
    "Εκ τῶν θείων γραφᾶν θεολογοῦμεν κἇν θέλωσιν οἱ ἐχθροὶ κἆν μή": (
        "&ldquo;We speak of theology from the divine Scriptures, whether our enemies want it or not&rdquo; "
        "(Early Greek patristic maxim, frequently quoted by Athanasius and Chrysostom)."
    ),
    "De Spiritu Sancto, lib. 2 cap. 6": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i> (De Spiritu Sancto), "
        "Book 2, Chapter 6 [NPNF2, 10:121; PL 16.753]."
    ),
    "Didym. lib. 2 de Spiritu Sancto": (
        "<b>Modern Citation:</b> Didymus the Blind, <i>On the Holy Spirit</i>, Book 2 "
        "(translated into Latin by Jerome) [PL 23.125]."
    ),
    "Basil. lib. 4. contra Eunom.": (
        "<b>Modern Citation:</b> Basil of Caesarea, <i>Against Eunomius</i>, Book 4 [PG 29.673] "
        "(historically attributed to Basil, now sometimes regarded as spurious)."
    ),
    "Concil. Sardicen. in Socrat. lib. 2 cap. 20": (
        "<b>Modern Citation:</b> <i>Creed of the Council of Sardica</i> (A.D. 343), preserved in "
        "Socrates Scholasticus, <i>Ecclesiastical History</i>, Book 2, Chapter 20 [NPNF2, 2:47; PG 67.236]."
    ),
    "Siquis propheticum dictum, ideo derivandum putet ad interpretationem Spiritus Sancti; quia habet, 'annuncians in homines Christum suum,' is ad incarnationis Dominicae mysteria dictum facilius derivabit. Nam si te movet quia Spiritum dixit, et hoc non putas derivandum ad mysterium assumptionis humanae; prosequere scripturas et invenies optime congruere de Christo, de quo bene convenit aestimari, quia firmavit tonitrua adventu suo; vim videlicet et sonum coelestium scripturarum; quarum velut quodam tonitru mentes nostrae redduntur attonitae, ut timere discamus, et reverntiam coelestibus deferamus oraculis. Denique, in Evangelio fratres Domini filii tonitru dicebantur. Et cum vox Patris facta esset dicentis ad Filim, 'Et honorificavi te, et iterum honorificabo,' Judaei dicebant, 'Tonitruum factum est illi.'": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 2, Chapter 6, Sections 49–50 [NPNF2, 10:121; PL 16.753].<br/>"
        "<b>Translation:</b> &ldquo;If anyone thinks that this prophetic saying is to be referred to the interpretation of the Holy Spirit "
        "because it contains &lsquo;announcing His Christ unto men,&rsquo; he will more easily refer the saying to the mysteries of the Lord's Incarnation. "
        "For if it troubles you that he said &lsquo;spirit,&rsquo; and you do not think this should be referred to the mystery of the assumption "
        "of human nature, follow the Scriptures and you will find it agrees best with Christ, of whom it is well suitable to think "
        "that He established the thunders by His coming—namely, the power and sound of the heavenly Scriptures, by whose thunder, as it were, "
        "our minds are struck with awe, so that we learn to fear and offer reverence to the heavenly oracles. Finally, in the Gospel, "
        "the brothers of the Lord were called &lsquo;sons of thunder.&rsquo; And when the voice of the Father came, saying to the Son, "
        "&lsquo;I have both glorified it, and will glorify it again,&rsquo; the Jews said, &lsquo;It thundered unto Him.&rsquo;&rdquo;"
    ),
    "Ergo tonitrua ad sermones Domini retulit, quorum in omnem terram exivit sonus; Spiritum autem hoc loco animam, quam suscepit rationabilem et perfectam intelligimus.": (
        "<b>Modern Citation:</b> Ambrose of Milan, <i>On the Holy Spirit</i>, Book 2, Chapter 6, Section 54 [NPNF2, 10:121; PL 16.754].<br/>"
        "<b>Translation:</b> &ldquo;Therefore, he referred the thunders to the words of the Lord, the sound of which went out into "
        "all the earth; and by &lsquo;spirit&rsquo; in this place, we understand the soul, rational and perfect, which He assumed.&rdquo;"
    ),
    "Quia ecce formans montes, et creans ventum, et annuncians homini eloquium suum,": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Amos</i>, on Amos 4:13 [PL 25.1033] (translating the verse).<br/>"
        "<b>Translation:</b> &ldquo;For behold, He who forms the mountains, and creates the wind, and declares to man His utterance.&rdquo;"
    ),
    "Pro montibus qui Hebraicè dicuntur הָריִם soli LXX βροντήν, id est, tontitruum, verterunt. Cur autem illi Spiritum et nos dixerimus ventum, qui Hebraice רוּחַ vocatur, causa manifesta est: quodque sequitur, 'Annuncians homini eloquium suum,' LXX. transtulerunt, 'Απαγγέλλων εἰς ἀνθρώπους τὸν Χριστὸν αὐτοῦ, verbi similitudine, et ambiguitate decepti.": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Amos</i>, on Amos 4:13 [PL 25.1033].<br/>"
        "<b>Translation:</b> &ldquo;For &lsquo;mountains,&rsquo; which in Hebrew are called <i>harim</i>, only the Septuagint translated as &lsquo;thunder&rsquo; "
        "(<i>brontēn</i>). But why they translated it as &lsquo;Spirit&rsquo; and we as &lsquo;wind,&rsquo; which in Hebrew is called <i>ruach</i>, "
        "the reason is manifest; and what follows, &lsquo;declares to man His utterance,&rsquo; the Septuagint translated as &lsquo;announcing "
        "His Christ unto men,&rsquo; being deceived by the similarity and ambiguity of the word.&rdquo;"
    ),
    "juxta Aquilam, ὁμιλίαν αὐτοῦ Symmachum, τὸ φώημα αὐτοῦ juxta Theodotionem, τὸν λόγον αὐτοῦ juxta quintam editionem, τὴν ἀδολεσχίαν αὐτοῦ.": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Amos</i>, on Amos 4:13 [PL 25.1033] (citing ancient Greek translations).<br/>"
        "<b>Translation:</b> &ldquo;according to Aquila, &lsquo;his speech/conversation&rsquo; (<i>homilian autou</i>); according to Symmachus, "
        "&lsquo;his utterance/voice&rsquo; (<i>to phōnēma autou</i>); according to Theodotion, &lsquo;his word&rsquo; (<i>ton logon autou</i>); "
        "according to the Fifth Edition, &lsquo;his discourse/meditation&rsquo; (<i>tēn adoleschian autou</i>).&rdquo;"
    ),
    "Qui confirmat montes, ad cujus vocem coelorum cardines et terrae fundamenta quatiuntur. Ipse qui creat spiritum, quem in hoc loco non Spiritum Sanctum, ut haeretici suspicantur, sed venture intelligimus, sive spiritum hominis, annuncians homini eloquium ejus, qui cogitationum secreta cognoscit,": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Amos</i>, on Amos 4:13 [PL 25.1034].<br/>"
        "<b>Translation:</b> &ldquo;Who establishes the mountains, at whose voice the hinges of the heavens and the foundations of the earth are shaken. "
        "He who creates the wind [or spirit], which in this place we understand not as the Holy Spirit, as heretics suspect, but as the wind, "
        "or the spirit of man, declaring to man his utterance, who knows the secrets of thoughts.&rdquo;"
    ),
    "Hieron. in loc.": (
        "<b>Modern Citation:</b> Jerome, <i>Commentary on Amos</i>, on Amos 4:13 [PL 25.1033–1034]."
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
    "יִΜַח שְׁמוֹ וְזִכְροֹ": "&ldquo;May his name and memory be blotted out&rdquo; (Hebrew polemical phrase: <i>yimach shemo ve-zichro</i>).",
    "יִΜַח שְׁמוֹ וְזִכְרוֹ": "&ldquo;May his name and memory be blotted out&rdquo; (Hebrew polemical phrase: <i>yimach shemo ve-zichro</i>).",
    "יְהוָֹה": "Jehovah (the sacred Tetragrammaton, the personal name of God in Hebrew).",
    "נליινא דרוחה": "revelation of the Spirit (Aramaic/Syriac phrase).",
    "יוּחַ": "spirit, wind, or breath (originally written Hebrew/Aramaic term).",
    "רוּחַ": "spirit, breath, or wind (Hebrew: <i>ruach</i>).",
    "רוּחַ עַל־הָאָρֶץ וַיַעֲβֵר ־אלֹהִיַם": "&ldquo;And God caused a wind to pass over the earth&rdquo; (Genesis 8:1).",
    "רוּחַ עַל־הָאָρֶץ וַיַעֲβֵר ־אלֹηִיַם": "&ldquo;And God caused a wind to pass over the earth&rdquo; (Genesis 8:1).",
    "רוּחַ עַל־הָאָρֶץ וַYַעֲבֵר ־אֱלֹהִיַם": "&ldquo;And God caused a wind to pass over the earth&rdquo; (Genesis 8:1).",
    "רוּחַ נְדוֹλָה וְχָζָκ": "&ldquo;a great and strong wind&rdquo; (1 Kings 19:11).",
    "רוּחַ נְדוֹלָה וְחָזָק": "&ldquo;a great and strong wind&rdquo; (1 Kings 19:11).",

    # --- SCHOLASTIC / HISTORICAL INLINE CITATIONS ---
    "Aquin. 22 q. 81, a. 3, ad prim., and q. 84, a. 1, ad tertium": (
        "<b>Modern Citation:</b> Thomas Aquinas, <i>Summa Theologiae</i>, Secunda Secundae (II-II), Q. 81, Art. 3, ad 1 (unity of the virtue of religion), "
        "and Q. 84, Art. 1, ad 3 (adoration as an act of religion)."
    ),
    "Alexand. Alens. p. 3, q. 30, m. 1, a. 3": (
        "<b>Modern Citation:</b> Alexander of Hales, <i>Summa Universae Theologiae</i>, Part 3, Q. 30, Member 1, Art. 3."
    ),
    "proposed by the Master of the Sentences": (
        "<b>Modern Citation &amp; Historical Context:</b> Peter Lombard (c. 1096–1164), traditionally called the &ldquo;Master of the Sentences&rdquo; (<i>Magister Sententiarum</i>). "
        "In his seminal <i>Sentences</i> (Book III, Distinctions 5–7), he proposed three distinct opinions/theories on the hypostatic union. "
        "Thomas Aquinas critiques these three views in detail in the <i>Summa Theologiae</i>, Tertia Pars (III), Q. 2, Art. 6, arguing that they fall short of orthodoxy."
    ),
    "after Aquinas, 22. q. 174, a. 1,": (
        "<b>Modern Citation:</b> Thomas Aquinas, <i>Summa Theologiae</i>, Secunda Secundae (II-II), Q. 174, Art. 1 (discussing the division and degrees of prophecy)."
    ),

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
    ),
    "subordination": (
        "<b>Editorial Explanation &amp; Scholastic Context:</b> In 17th-century Reformed scholastic theology, "
        "the term &ldquo;subordination&rdquo; (Latin: <i>subordinatio</i>) possesses a highly precise, technical "
        "meaning that must not be confused with modern notions of ontological inferiority or inequality (which is the "
        "ancient heresy of Subordinationism). Instead, the Puritans distinguished between: (1) <i>Subordination of "
        "Order (Subordinatio Ordinis)</i>, which denotes the eternal personal relations of origin within the co-equal Trinity "
        "(the Son eternally begotten of the Father, and the Spirit eternally proceeding from both); and (2) <i>Economical "
        "Subordination (Subordinatio Officii)</i>, which refers to the voluntary, covenantal submission of the Son to assume "
        "human nature and act as the Mediator under the Father's administration in the economy of salvation, and the Spirit's "
        "mission to apply that redemption. In both aspects, there is perfect equality of divine essence, power, and glory."
    )
}
