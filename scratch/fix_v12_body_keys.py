import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
translation_db_path = os.path.join(_ROOT, 'translation_db.py')

# Keys to remove (incorrect ones we added previously)
KEYS_TO_REMOVE = [
    "Difficilis in perfecto mora est; naturaliterque, quod procedere non potest, recedit; et ut primo ad consequendos, quos priores ducimus, accendimur: ita, ubi aut praeteriri, aut aequari cos posse desperavimus, studium cum spe senescit; et quod adsequi non potest, sequi desinit; et, velut occupatam relinquens materiam, quaerit novam: praeteritoque eo in quo eminere non possumus, aliquid in quo nitamur conquirimus; sequiturque, ut frequens ac mobilis transitus maximum perfecti operis impedimentum sit.",
    "Θὔτε δέμας θνητοῖσιν ὁμοίι`ος οὐδὲ νόημα.",
    "Χωρεῖτε θνητῶν τὸν Θεὸν καὶ μὴ δόκει",
    "Καὶ νῦν δόξασόν με σύ, Πάτερ, παρὰ σεαυτῷ τῇ δόξῃ ῇ εῖχον πρὸ τοῦ τὸν κόσμον εῖναι παρὰ σοί",
    "Παρὰ σοί, refer ad illud εῖχον, et intellige, ut diximus, in decreto tuo.",
    "Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ",
    "Θεὸς ἐφανερώθη ἐν σαρκί. \"Suspectam nobis hanc lectionem faciunt interpretes veteres, Latinus, Syrus, Arabs, et Ambrosius, qui omnes legunt, quod manifestatum est in carne.\"",
    "Συντάμνω μὲν ἅπανta, τάδ ἐξείρηκα γεραίρων: Τριὰς ἁγία, τριὰς εἷς Θεός, ὦ μέγα χάρμα.",
    "Οτι ἄν tis ἐκτημένος ῇ, καὶ κατὰ νόμον, τοῦτο δίκαιον καλεῖται, ὡς ἑκάστου αὐτῶν ἴδιον εῖναι προσῆκον.",
    "Justificati gratis per gratiam ipsius. Intellige ex eo, quod Christus perfectissime Deo obediendo, voluntatem ejus perfectissime executioni mandaverit.",
    "id minime eo sensu dici, quasi loco nostri legem impleverlt, sic ut nobis deinceps ipsius justitia imputetur.",
    "est actus Dei absolventis terminatus in conscientia hominis, citati et tracti ad tribunale tremendi judicis; qui actus et sententia in Scriptura promulgatur.",
    "Τικτει τοι κόρος ὕβριν ὅταν κακῷ ὄλβος ἕπηται Ανθρώπῳ καὶ ο\\τω μὴ νόος ἄρτιος ῇ. — Theogn.",
    "ὁ λόγος τοῦ Θεοῦ is threefold, — λόγος ὑποστατικός, ἐνδιάθετος, and προφορικός.",
    "Tui nominis studiosissimus, 10 Maii. M.DC.XXVI. H.G. —— Tam pro epistola (vir clarissime) quam pro transmisso libro, gratias ago maximas"
]

CORRECT_BODY_TRANSLATIONS = {
    # p_idx=114 in Preface (Velleius Paterculus)
    "Difficilis in perfecto mora est; naturaliterque, quod procedere non potest, recedit; et ut primo ad consequendos, quos priores ducimus, accendimur: ita, ubi aut praeteriri, aut aequari cos posse desperavimus, studium cum spe senescit; et quod adsequi non potest, sequi desinit; et, velut occupatam relinquens materiam, quaerit novam: praeteritoque eo in quo eminere non possumus, aliquid in quo nitamur conquirimus; sequiturque, ut frequens ac mobilis transitus maximum perfecti operis impedimentum sit.": (
        "<b>Modern Citation:</b> Velleius Paterculus, <i>Historia Romana</i>, Book 1, Chapter 17.<br/>"
        "<b>Translation:</b> &ldquo;It is difficult to stand still at the point of perfection; and naturally, that which cannot advance, recedes. And just as we are at first fired with the ambition of overtaking those whom we regard as leaders, so, when we have despaired of being able either to surpass or to equal them, our enthusiasm languishes along with our hope; it ceases to follow what it cannot overtake, and, abandoning the field as if it were already occupied, it seeks a new one. Passing over that in which we cannot excel, we look for some other object for our efforts; and it follows that this frequent and restless changing of direction is the greatest impediment to the perfection of any work.&rdquo;"
    ),
    # p_idx=33 in Ch 3 (Xenophanes)
    "Θὔτε δέμας θνητοῖσιν ὁμοίι`ος οὐδὲ νόημα.": (
        "<b>Modern Citation:</b> Xenophanes of Colophon, Fragment 23 (cited in Clement of Alexandria, <i>Stromata</i>, Book 5, Chapter 14).<br/>"
        "<b>Translation:</b> &ldquo;Neither in body nor in mind is He like unto mortals.&rdquo;"
    ),
    # p_idx=37 in Ch 3 (Aeschylus)
    "Χωρεῖτε θνητῶν τὸν Θεὸν καὶ μὴ δόκει": (
        "<b>Modern Citation:</b> Aeschylus, Fragment (cited in Clement of Alexandria, <i>Stromata</i>, Book 5, Chapter 14).<br/>"
        "<b>Translation:</b> &ldquo;Distinguish God from mortals, and do not think Him to be fleshly.&rdquo;"
    ),
    # p_idx=79 in Ch 9 (John 17:5)
    "Καὶ νῦν δόξασόν με σὺ Πάτερ παρὰ σεαυτῷ τῇ δόξῃ ῇ εῖχον πρὸ τοῦ τὸν κόσμον εῖναι παρὰ σοί": (
        "<b>Modern Citation:</b> John 17:5.<br/>"
        "<b>Translation:</b> &ldquo;And now, Father, glorify me in your own presence with the glory that I had with you before the world existed.&rdquo;"
    ),
    # p_idx=82 in Ch 9 (Socinus)
    "Παρὰ σοί, refer ad illud εῖχον, et intellige, ut diximus, in decreto tuo.": (
        "<b>Modern Citation:</b> Faustus Socinus, <i>De Jesu Christo Servatore</i>.<br/>"
        "<b>Translation:</b> &ldquo;Refer the words 'with you' to 'I had,' and understand it, as we have said, 'in your decree.'&rdquo;"
    ),
    # p_idx=3 in Ch 12 (Heb 1:3)
    "Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ": (
        "<b>Modern Citation:</b> Hebrews 1:3.<br/>"
        "<b>Translation:</b> &ldquo;Upholding all things by the word of his power.&rdquo;"
    ),
    # p_idx=93 in Ch 13 (Grotius)
    "Suspectam nobis hanc lectionem faciunt interpretes veteres, Latinus, Syrus, Arabs, et Ambrosius, qui omnes legunt": (
        "<b>Modern Citation:</b> Hugo Grotius, <i>Annotationes in Novum Testamentum</i>, on 1 Timothy 3:16.<br/>"
        "<b>Translation:</b> &ldquo;The ancient translators make this reading suspected by us — the Latin, Syriac, Arabic, and Ambrose — who all read [what was manifested/manifested]...&rdquo;"
    ),
    # p_idx=70 in Ch 25 (Gregory Nazianzen)
    "Πάντα μὲν αἰὲν ἄριστα θεοπιεπὲς ἔργα τελείσθω Η δὲ τριὰς ἐξοχά σοι μελέτω": (
        "<b>Modern Citation:</b> Gregory Nazianzen, <i>Carmina Dogmatica</i>, Poem 3.<br/>"
        "<b>Translation:</b> &ldquo;May all things ever best and divine be accomplished; but let the Trinity be thy special care.&rdquo;"
    ),
    # p_idx=4 in Ch 28 (Plato)
    "Οτι ἄν τις ἐκτημένος ῇ... καὶ μηδεὶς ἐπιλάβηται ἐὰν οὕτω τις ἐνιαυτὸν ὁτιοῦν ἐκτημένος... μὴ ἐξέστω τοιούτου κτήματος ἐπιλαβέσθαι μηδὲν ἀπελθόντος ἐνιαυτοῦ.": (
        "<b>Modern Citation:</b> Plato, <i>Laws</i> (De Legibus), Book 11, 914c.<br/>"
        "<b>Translation:</b> &ldquo;If a man has been in possession of anything whatsoever for a full year... and no one has laid claim to it, it shall not be lawful to lay claim to such property after the year has elapsed.&rdquo;"
    ),
    # p_idx=121 in Ch 28 (Socinus)
    "Justificati gratis, sensus est, partam nobis esse peccatorum nostrorum absolutionem (id enim ut scis quod ad nos attinet reipsa justificari est) non quidem per legis opera, quibus illam commeriti sumus, sed gratis per gratiam Dei": (
        "<b>Modern Citation:</b> Faustus Socinus, <i>De Jesu Christo Servatore</i>, Book 1, Part 2, Chapter 2.<br/>"
        "<b>Translation:</b> &ldquo;'Justified freely,' the sense is, that the absolution of our sins has been obtained for us (for that, as you know, as far as it concerns us, is in reality to be justified), not indeed by the works of the law, by which we have deserved it, but freely by the grace of God.&rdquo;"
    ),
    # p_idx=65 in Of Death of Christ (Schlichting)
    "id minime eo sensu dici, quasi loco nostri legem impleverlt, sic ut nobis deinceps ipsius justitia imputetur": (
        "<b>Modern Citation:</b> Jonas Schlichting, <i>De Trinitate Contra Meisnerum</i>, p. 277.<br/>"
        "<b>Translation:</b> &ldquo;...that this is by no means said in the sense as if he had fulfilled the law in our place, so that his righteousness should henceforth be imputed to us.&rdquo;"
    ),
    # p_idx=81 in Of Death of Christ (Vorstius)
    "est actus Dei absolventis terminatus in conscientia hominis, citati et tracti ad tribunale tremendi judicis; qui actus ante hoc instans": (
        "<b>Modern Citation:</b> Conrad Vorstius, <i>Amica Collatio</i>.<br/>"
        "<b>Translation:</b> &ldquo;...it is the act of God absolving, terminated in the conscience of the man summoned and dragged to the tribunal of the fearful judge; which act before this instant [was not terminated in the conscience]...&rdquo;"
    ),
    # p_idx=101 in Of Death of Christ (Theognis)
    "Τικτει τοι κόρος ὕβριν ὅταν κακῷ ὄλβος ἕπηται Ανθρώπῳ καὶ ο\\τω μὴ νόος ἄρτιος ῇ. — Theogn.": (
        "<b>Modern Citation:</b> Theognis of Megara, <i>Elegies</i>, lines 153–154.<br/>"
        "<b>Translation:</b> &ldquo;Fullness breeds insolence, when wealth follows a bad man, and one whose mind is not sound.&rdquo;"
    ),
    # p_idx=31 in A Second Consideration (Scholastic)
    "ὁ λόγος τοῦ Θεοῦ is threefold, — λόγος ὑποστατικός ἐνδιάθετος, and προφορικός.": (
        "<b>Modern Citation:</b> Scholastic Distinction (essential/hypostatic Word, internal/conceived Word, and spoken/uttered Word).<br/>"
        "<b>Translation:</b> &ldquo;The Word of God is threefold: the essential/hypostatic Word, the internal/conceived Word, and the spoken/uttered Word.&rdquo;"
    ),
    # p_idx=49 in A Second Consideration (Grotius)
    "Tui nominis studiosissimus, 10 Maii. M.DC.XXVI. H.G. —— Tam pro epistola (vir clarissime) quam pro transmisso libro, gratias ago maximas": (
        "<b>Modern Citation:</b> Hugo Grotius, Letter to Valentin Smalcius, 10 May 1626.<br/>"
        "<b>Translation:</b> &ldquo;Your most devoted friend, 10 May 1626. H. G. — I return my greatest thanks, most distinguished sir, both for your letter and for the book you sent...&rdquo;"
    )
}

with open(translation_db_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Programmatically remove old keys
for k in KEYS_TO_REMOVE:
    k_escaped = k.replace('"', '\\"')
    # We want to remove the entry from content
    # Find the line like: "Key": ( ... ),
    target_start = f'    "{k_escaped}": ('
    idx = content.find(target_start)
    if idx != -1:
        # Find closing ),\n
        end_idx = content.find("),\n", idx)
        if end_idx != -1:
            # Remove the whole entry block
            content = content[:idx] + content[end_idx + len("),\n"):]

# 2. Insert new corrected entries into BODY_TRANSLATIONS = {
target_str = "BODY_TRANSLATIONS = {"
idx = content.find(target_str)
if idx == -1:
    print("Error: BODY_TRANSLATIONS dictionary start not found!")
    sys.exit(1)

insert_idx = idx + len(target_str)

entries_str = "\n"
for key, val in sorted(CORRECT_BODY_TRANSLATIONS.items()):
    key_escaped = key.replace('"', '\\"')
    val_escaped = val.replace('"', '\\"')
    entries_str += f'    "{key_escaped}": (\n        "{val_escaped}"\n    ),\n'

new_content = content[:insert_idx] + entries_str + content[insert_idx:]

with open(translation_db_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully corrected 15 Volume 12 body translations in translation_db.py!")
