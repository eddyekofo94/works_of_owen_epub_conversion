import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
translation_db_path = os.path.join(_ROOT, 'translation_db.py')

NEW_V12_TRANSLATIONS = {
    "v12_fn104": (
        "<b>Modern Citation:</b> Joseph Justus Scaliger.<br/>"
        "<b>Translation:</b> &ldquo;Many defects have been admitted here and there from the highest antiquity, which no one besides me will point out.&rdquo;"
    ),
    "v12_fn165": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>De Vera Religione</i>, Book 1, Chapter 24, p. 201.<br/>"
        "<b>Translation:</b> &ldquo;Therefore they act inconsiderately who say that God determinately knows future contingent events, because otherwise He would not be omniscient; whereas on the contrary, He does not conceive of those events as determinately future precisely because He is omniscient.&rdquo;"
    ),
    "v12_fn166": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>De Vera Religione</i>, Book 1, Chapter 24, p. 201.<br/>"
        "<b>Translation:</b> &ldquo;For if you contend that all future events, of whatever kind they may be, were determinately known by God from all eternity, it is necessary that you also establish that all things are determinately future, since otherwise such divine knowledge would have been false.&rdquo;"
    ),
    "v12_fn167": (
        "<b>Modern Citation:</b> Conrad Vorstius.<br/>"
        "<b>Translation:</b> &ldquo;Repentance implies ignorance of the past, present, and future, a change of the will, and error in action.&rdquo;"
    ),
    "v12_fn168": (
        "<b>Modern Citation:</b> Conrad Vorstius, on Genesis 22:12.<br/>"
        "<b>Translation:</b> &ldquo;From this action, on account of which you shall be called a God-fearing man by all, all will know how great is the fear of God within you.&rdquo;"
    ),
    "v12_fn170": (
        "<b>Modern Citation:</b> Johannes Crellius, <i>De Vera Religione</i>, ubi supra.<br/>"
        "<b>Translation:</b> &ldquo;One must depart too far from the proper meaning of the words, and the force of the sentences must be weakened, if you drag them into a divine application.&rdquo;"
    ),
    "v12_fn220": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;Since you said at the beginning that this path which leads to immortality was divinely revealed, I would like to know why you spoke thus? — For the reason that before the coming of Christ this path was by no means so revealed that men could establish anything certain concerning it; for although some suspected that the souls of men do not perish after this life, and that it goes well with the good and ill with the bad, yet this was so weakly and doubtfully conceived by them that none of them could persuade others, nor could they fully satisfy themselves in it.&rdquo;"
    ),
    "v12_fn271": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;Explain to me, therefore, by what testimonies they contend to prove that Christ created heaven and earth? — Chiefly by these: John 1:3; Colossians 1:16; Hebrews 1:2, 10.&rdquo;"
    ),
    "v12_fn272": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;But what do you answer to the second? — First, that John does not write here that the world was 'created,' but 'made'; for the word which is here read as 'made' does not designate anything other than what is read by John elsewhere where 'made/became' is used: as, for example, in the same chapter, verse 6, and Luke 24:19, 'There was a man sent from God,' etc., and 'Who was a prophet,' etc.&rdquo;"
    ),
    "v12_fn273": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;But what do you understand by this: 'The world was made through him'? A twofold sense of these words can be given: First, that the entire assembly of men, which is designated by the name 'world,' was raised by him into a more perfect state; second, that through him He made that part of those things which pertain to this world, which pertains to the preaching of the gospel.&rdquo;"
    ),
    "v12_fn274": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;From which testimonies of Scripture indeed do they endeavor to demonstrate that Christ was (as they speak) incarnate? — From those where according to their version it is read: 'The Word was made flesh,' John 1:14; Philippians 2:6, 7; 1 Timothy 3:16, etc. 'How do you answer to the first?' — For the reason that in that testimony it is not held that God (as they speak) was incarnate, or that the divine nature assumed the human. For it is one thing that 'the Word was made flesh,' and another that 'God was incarnate' (as they speak) or 'the divine nature assumed the human.' Furthermore, these words, 'the Word was made flesh,' or rather, 'the Speech was made flesh,' can and ought to be thus rendered: 'the Speech was flesh.' That it can be so rendered is apparent from testimonies in which the word <i>egeneto</i> (which is here translated as 'was made') is found rendered by the verb 'was'; as in the same chapter, verse 6, and Luke 24:19: 'There was a man sent from God,' etc.; and 'Who was a prophet,' etc. That it ought to be rendered by the verb 'was,' the order of John's words teaches, who would have spoken very inconveniently in saying that the Speech was made flesh, — that is, as the adversaries interpret it, that the divine nature assumed the human, — after he had already set forth those things concerning that Speech which followed the birth of the man Jesus Christ: such as these, that John the Baptist bore witness of him; that he was in the world; that he was not received by his own; and that he gave power to those by whom he was received to become the sons of God.&rdquo;"
    ),
    "v12_fn275": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;In what manner is it to be understood that the Word was flesh? — That he through whom God had perfectly set forth His entire will, and was therefore called 'the Word' by John, was a man, subject to all miseries and afflictions, and finally to death; for the Scripture uses the word 'flesh' in that sense, as is clear from those places where God speaks: 'My Spirit shall not strive with man forever, because he is flesh,' Genesis 6:3; and Peter: 'All flesh is as grass,' 1 Peter 1:24.&rdquo;"
    ),
    "v12_fn276": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;But what do you answer to the second? — Neither is any mention of pre-eternity expressly made here; for in this place Scripture testifies that the Son of man, that is, a man, was in heaven, whom it is certain beyond all controversy did not exist from pre-eternity.&rdquo;"
    ),
    "v12_fn277": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;But where Scripture says of Christ that he descended from heaven, went out from the Father, and came into the world, John 3:13, 10:36, 16:28, 17:18, what do you answer to these? — That the divine nature is not proved from them appears from this, that the words of the first testimony, 'He descended from heaven,' can be taken figuratively; just as in James 1:17, 'Every good gift and every perfect gift is from above, coming down from the Father of lights'; and Revelation 21:2, 10, 'I saw the holy city, new Jerusalem, coming down out of heaven from God,' etc. But if they must be taken properly, which we very gladly admit, it appears that those things were said of no other than the Son of man, who since he necessarily has a human person, cannot be God by nature. Furthermore, as to what Scripture testifies of Christ, that the Father sent him into the world, we read the same concerning the apostles of Christ in the very words cited above: 'As you sent me into the world, so have I sent them into the world,' John 17:18. But those words, that Christ 'went out from the Father,' have the same force as 'he descended from heaven.' But 'to come into the world' is of such a kind as the Scripture shows to have occurred after the birth of Christ, John 18:37, where the Lord Himself says: 'For this I was born, and for this I came into the world, to bear witness to the truth'; and in 1 John 4:1 it is written: 'Many false prophets have gone out into the world.' Therefore, a divine nature in Christ cannot be proved from such modes of speaking. In all these expressions, only how divine the origin of Christ's office was is described.&rdquo;"
    ),
    "v12_fn281": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;What are the testimonies which seem to attribute certain things to the Lord Jesus from eternity? — They are those from which they endeavor to construct that Christ was begotten from eternity out of the essence of the Father.&rdquo;"
    ),
    "v12_fn282": (
        "<b>Modern Citation:</b> <i>Racovian Catechism</i>, Chapter 1.<br/>"
        "<b>Translation:</b> &ldquo;From which places indeed do they endeavor to construct that Christ was begotten from eternity out of the essence of the Father? — Chiefly from these: Micah 5:2; Psalm 2:7, 110:8; Proverbs 8:23.&rdquo;"
    ),
    "v12_fn417": (
        "<b>Modern Citation:</b> Valentin Smalcius, <i>Refutatio Thesium de Hypocritarum Disputatione</i>.<br/>"
        "<b>Translation:</b> &ldquo;Hence it is gathered that the death of Christ alone was by no means that perfect and absolute offering of His which is treated of in the Epistle to the Hebrews; but that it was a beginning and a certain preparation of that priesthood to be administered at length in heaven.&rdquo;"
    ),
    "v12_fn419": (
        "<b>Modern Citation:</b> Valentin Smalcius, <i>Refutatio Thesium</i>, p. 7.<br/>"
        "<b>Translation:</b> &ldquo;For He neither introduced it Himself, nor was He sent by us to execute the covenant between God and us; but He was the minister and messenger of God, who had sent Him for this purpose, in this part.&rdquo;"
    ),
    "v12_fn420": (
        "<b>Modern Citation:</b> Valentin Smalcius, <i>Refutatio Thesium</i>, p. 7.<br/>"
        "<b>Translation:</b> &ldquo;But when He is considered as a priest, — although He bears the likeness of one who performs something before God on behalf of men, — yet if you look closely into the matter itself, you will find that He is such a priest as performs something for us in the name of God.&rdquo;"
    ),
    "v12_fn426": (
        "<b>Modern Citation:</b> Christopher Ostorod and Andrzej Wojdowski, <i>Compendium Religionis</i>.<br/>"
        "<b>Translation:</b> &ldquo;What is the difference between the expiation of sins of the old and the new covenant? — The expiation of sins under the new covenant not only differs greatly from the expiation of sins under the old, but is also far more excellent and outstanding; and that chiefly for two reasons. The first is, that under the old covenant, expiation through those legal sacrifices was established only for those sins which were committed through ignorance or weakness, whence they were also called infirmities and ignorances. But for more serious sins, which were manifest transgressions of the commandment of God, no sacrifices had been established, but the penalty of death was set forth. But if God pardoned such things in anyone, it did not happen by virtue of the covenant, but by a singular mercy of God, which God exhibited apart from the covenant, both when and to whom He pleased. But under the new covenant, sins are expiated not only when committed through ignorance and weakness, but also those which are transgressions of the most open commandments of God, provided that he to whom it happens to fall in that manner does not persevere in it, but repents through true repentance, and does not fall back into that sin any further. The latter reason is, that under the ancient covenant, the expiation of sins was performed in such a way that only a temporary punishment was removed from those whose sins were expiated; but under the new, the expiation is such that it removes not only temporary but also eternal punishments, and in place of punishments, offers eternal life, promised in the covenant, to those whose sins have been expiated.&rdquo;"
    ),
    "v12_fn445": (
        "<b>Modern Citation:</b> Classical Rabbinic anecdote, recorded in various anti-Socinian writings.<br/>"
        "<b>Translation:</b> &ldquo;Some Jews confessed to me that their rabbis could easily have extricated themselves from the prophetic writings, provided Isaiah had kept silent.&rdquo;"
    ),
    "v12_fn456": (
        "<b>Modern Citation:</b> Polybius, <i>Histories</i>, Book 3; Livy, <i>Ab Urbe Condita</i>, Book 1, Chapter 24; Virgil, <i>Aeneid</i>, Book 8, Line 640, with Servius' Commentary.<br/>"
        "<b>Translation:</b> &ldquo;The herald [fetial], taking a stone in his hands, after he had agreed on the treaty between the parties, spoke these words: 'If I make this treaty and this oath rightly and without deceit, may the gods grant me all things happy; but if I act or think otherwise, all others being safe, in my own laws, in my own house, in my own temples, in my own tombs, may I alone perish, as this stone falls from my hands.' — Polybius, Book 3. 'Hear, O Jupiter; hear, O father patrate; as those things have been publicly recited from first to last from those tablets or wax without deceit, and as they have been today most correctly understood here, the Roman people will not be the first to depart from those laws. If they depart first by public counsel and with evil intent, then do you, O Jupiter, strike the Roman people just as I strike this pig here today; and strike them so much the more as you are more able and powerful.' When he said this, he struck the pig with a flint stone. — Livy, Book 1, Chapter 24. 'Armed, they stood before the altars of Jupiter, holding cups, and joined treaties over a slain sow.' — Virgil, <i>Aeneid</i>, 8:640. To which place Servius: 'Treaties [foedera] are named from a sow slain in a foul [foede] and cruel manner; for whereas before they were pierced with swords, it was invented by the heralds that they should be struck with a flint, for the reason that they thought the flint stone was an ancient statue of Jupiter.'&rdquo;"
    )
}

with open(translation_db_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate FOOTNOTE_TRANSLATIONS = {
target_str = "FOOTNOTE_TRANSLATIONS = {"
idx = content.find(target_str)
if idx == -1:
    print("Error: FOOTNOTE_TRANSLATIONS dictionary start not found!")
    sys.exit(1)

insert_idx = idx + len(target_str)

# Build string to insert
entries_str = "\n"
for key, val in sorted(NEW_V12_TRANSLATIONS.items()):
    val_escaped = val.replace('"', '\\"')
    entries_str += f'    "{key}": (\n        "{val_escaped}"\n    ),\n'

new_content = content[:insert_idx] + entries_str + content[insert_idx:]

with open(translation_db_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully added 22 new Volume 12 translations to translation_db.py!")
