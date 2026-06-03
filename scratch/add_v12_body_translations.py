import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, '..')
translation_db_path = os.path.join(_ROOT, 'translation_db.py')

NEW_BODY_TRANSLATIONS = {
    "Difficilis in perfecto mora est; naturaliterque, quod procedere non potest, recedit; et ut primo ad consequendos, quos priores ducimus, accendimur: ita, ubi aut praeteriri, aut aequari cos posse desperavimus, studium cum spe senescit; et quod adsequi non potest, sequi desinit; et, velut occupatam relinquens materiam, quaerit novam: praeteritoque eo in quo eminere non possumus, aliquid in quo nitamur conquirimus; sequiturque, ut frequens ac mobilis transitus maximum perfecti operis impedimentum sit.": (
        "<b>Modern Citation:</b> Velleius Paterculus, <i>Historia Romana</i>, Book 1, Chapter 17.<br/>"
        "<b>Translation:</b> &ldquo;It is difficult to stand still at the point of perfection; and naturally, that which cannot advance, recedes. And just as we are at first fired with the ambition of overtaking those whom we regard as leaders, so, when we have despaired of being able either to surpass or to equal them, our enthusiasm languishes along with our hope; it ceases to follow what it cannot overtake, and, abandoning the field as if it were already occupied, it seeks a new one. Passing over that in which we cannot excel, we look for some other object for our efforts; and it follows that this frequent and restless changing of direction is the greatest impediment to the perfection of any work.&rdquo;"
    ),
    "Θὔτε δέμας θνητοῖσιν ὁμοίι`ος οὐδὲ νόημα.": (
        "<b>Modern Citation:</b> Xenophanes of Colophon, Fragment 23 (cited in Clement of Alexandria, <i>Stromata</i>, Book 5, Chapter 14).<br/>"
        "<b>Translation:</b> &ldquo;Neither in body nor in mind is He like unto mortals.&rdquo;"
    ),
    "Χωρεῖτε θνητῶν τὸν Θεὸν καὶ μὴ δόκει": (
        "<b>Modern Citation:</b> Aeschylus, Fragment (cited in Clement of Alexandria, <i>Stromata</i>, Book 5, Chapter 14).<br/>"
        "<b>Translation:</b> &ldquo;Distinguish God from mortals, and do not think Him to be fleshly.&rdquo;"
    ),
    "Καὶ νῦν δόξασόν με σύ, Πάτερ, παρὰ σεαυτῷ τῇ δόξῃ ῇ εῖχον πρὸ τοῦ τὸν κόσμον εῖναι παρὰ σοί": (
        "<b>Modern Citation:</b> John 17:5.<br/>"
        "<b>Translation:</b> &ldquo;And now, Father, glorify me in your own presence with the glory that I had with you before the world existed.&rdquo;"
    ),
    "Παρὰ σοί, refer ad illud εῖχον, et intellige, ut diximus, in decreto tuo.": (
        "<b>Modern Citation:</b> Faustus Socinus, <i>De Jesu Christo Servatore</i>.<br/>"
        "<b>Translation:</b> &ldquo;Refer the words 'with you' to 'I had,' and understand it, as we have said, 'in your decree.'&rdquo;"
    ),
    "Φέρων τε τὰ πάντα τῷ ῥήματι τῆς δυνάμεως αὑτοῦ": (
        "<b>Modern Citation:</b> Hebrews 1:3.<br/>"
        "<b>Translation:</b> &ldquo;Upholding all things by the word of his power.&rdquo;"
    ),
    "Θεὸς ἐφανερώθη ἐν σαρκί. \"Suspectam nobis hanc lectionem faciunt interpretes veteres, Latinus, Syrus, Arabs, et Ambrosius, qui omnes legunt, quod manifestatum est in carne.\"": (
        "<b>Modern Citation:</b> Hugo Grotius, <i>Annotationes in Novum Testamentum</i>, on 1 Timothy 3:16.<br/>"
        "<b>Translation:</b> &ldquo;'God was manifested in the flesh.' The ancient translators make this reading suspected by us — the Latin, Syriac, Arabic, and Ambrose — who all read: 'which was manifested in the flesh.'&rdquo;"
    ),
    "Συντάμνω μὲν ἅπανta, τάδ ἐξείρηκα γεραίρων: Τριὰς ἁγία, τριὰς εἷς Θεός, ὦ μέγα χάρμα.": (
        "<b>Modern Citation:</b> Gregory Nazianzen, <i>Carmina Dogmatica</i>, Book 1, Section 1, Poem 3 (On the Spirit).<br/>"
        "<b>Translation:</b> &ldquo;To sum up all, I have spoken these things in praise: Holy Trinity, Trinity one God, O what great joy!&rdquo;"
    ),
    "Οτι ἄν τις ἐκτημένος ῇ, καὶ κατὰ νόμον, τοῦτο δίκαιον καλεῖται, ὡς ἑκάστου αὐτῶν ἴδιον εῖναι προσῆκον.": (
        "<b>Modern Citation:</b> Aristotle, <i>Rhetoric</i>, Book 1, Chapter 9, 1366b.<br/>"
        "<b>Translation:</b> &ldquo;Whatever a man has acquired, even according to law, this is called just, as fitting to be each one's own property.&rdquo;"
    ),
    "Justificati gratis per gratiam ipsius. Intellige ex eo, quod Christus perfectissime Deo obediendo, voluntatem ejus perfectissime executioni mandaverit.": (
        "<b>Modern Citation:</b> Faustus Socinus, <i>De Jesu Christo Servatore</i>.<br/>"
        "<b>Translation:</b> &ldquo;Justified freely by his grace. Understand it from this, that Christ, by obeying God most perfectly, executed His will most perfectly.&rdquo;"
    ),
    "id minime eo sensu dici, quasi loco nostri legem impleverlt, sic ut nobis deinceps ipsius justitia imputetur.": (
        "<b>Modern Citation:</b> Faustus Socinus, <i>De Jesu Christo Servatore</i>.<br/>"
        "<b>Translation:</b> &ldquo;That this is by no means said in the sense as if he had fulfilled the law in our place, so that his righteousness should henceforth be imputed to us.&rdquo;"
    ),
    "est actus Dei absolventis terminatus in conscientia hominis, citati et tracti ad tribunale tremendi judicis; qui actus et sententia in Scriptura promulgatur.": (
        "<b>Modern Citation:</b> Conrad Vorstius, <i>Amica Collatio</i>.<br/>"
        "<b>Translation:</b> &ldquo;It is the act of God absolving, terminated in the conscience of the man summoned and dragged to the tribunal of the fearful judge; which act and sentence is promulgated in the Scripture.&rdquo;"
    ),
    "Τικτει τοι κόρος ὕβριν ὅταν κακῷ ὄλβος ἕπηται Ανθρώπῳ καὶ ο\\τω μὴ νόος ἄρτιος ῇ. — Theogn.": (
        "<b>Modern Citation:</b> Theognis of Megara, <i>Elegies</i>, lines 153–154.<br/>"
        "<b>Translation:</b> &ldquo;Fullness breeds insolence, when wealth follows a bad man, and one whose mind is not sound.&rdquo;"
    ),
    "ὁ λόγος τοῦ Θεοῦ is threefold, — λόγος ὑποστατικός, ἐνδιάθετος, and προφορικός.": (
        "<b>Modern Citation:</b> Scholastic Distinction (essential/hypostatic Word, internal/conceived Word, and spoken/uttered Word).<br/>"
        "<b>Translation:</b> &ldquo;The Word of God is threefold: the essential/hypostatic Word, the internal/conceived Word, and the spoken/uttered Word.&rdquo;"
    ),
    "Tui nominis studiosissimus, 10 Maii. M.DC.XXVI. H.G. —— Tam pro epistola (vir clarissime) quam pro transmisso libro, gratias ago maximas": (
        "<b>Modern Citation:</b> Hugo Grotius, Letter to Valentin Smalcius, 10 May 1626.<br/>"
        "<b>Translation:</b> &ldquo;Your most devoted friend, 10 May 1626. H. G. — I return my greatest thanks, most distinguished sir, both for your letter and for the book you sent...&rdquo;"
    )
}

with open(translation_db_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate BODY_TRANSLATIONS = {
target_str = "BODY_TRANSLATIONS = {"
idx = content.find(target_str)
if idx == -1:
    print("Error: BODY_TRANSLATIONS dictionary start not found!")
    sys.exit(1)

insert_idx = idx + len(target_str)

# Build string to insert
entries_str = "\n"
for key, val in sorted(NEW_BODY_TRANSLATIONS.items()):
    key_escaped = key.replace('"', '\\"')
    val_escaped = val.replace('"', '\\"')
    entries_str += f'    "{key_escaped}": (\n        "{val_escaped}"\n    ),\n'

new_content = content[:insert_idx] + entries_str + content[insert_idx:]

with open(translation_db_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully added 15 new Volume 12 body translations to translation_db.py!")
