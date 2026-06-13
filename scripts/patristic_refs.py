# -*- coding: utf-8 -*-
"""
patristic_refs.py — Comprehensive lookup tables for Owen's inline patristic
and classical citations.

Used by render.py to expand abbreviated citations (lib., cap., epist., etc.)
into full modern academic references.
"""

import re

# ── Location abbreviation expansion ─────────────────────────────────────────

LOC_EXPAND = {
    "lib":    "Book",
    "cap":    "Chapter",
    "chap":   "Chapter",
    "serm":   "Sermon",
    "sermo":  "Sermon",
    "epist":  "Epistle",
    "ep":     "Epistle",
    "orat":   "Oration",
    "tract":  "Tractate",
    "homil":  "Homily",
    "haer":   "Heresy",
    "dial":   "Dialogue",
    "adv":    "Against",
    "sect":   "Section",
    "tom":    "Volume",
    "t":      "Volume",
    "col":    "Column",
    "vol":    "Volume",
    "qu":     "Question",
    "q":      "Question",
    "art":    "Article",
    "dist":   "Distinction",
    "part":   "Part",
    "p":      "p.",
    "pp":     "pp.",
    "con":    "Against",
}

# ── Author abbreviation → full name ─────────────────────────────────────────

AUTHOR_ABBREV_MAP = {
    # Augustine
    "august":      "Augustine of Hippo",
    "augustine":   "Augustine of Hippo",
    "austin":      "Augustine of Hippo",
    "aug":         "Augustine of Hippo",
    # Chrysostom
    "chrysost":    "John Chrysostom",
    "chrysostom":  "John Chrysostom",
    "chrys":       "John Chrysostom",
    # Basil of Caesarea
    "basil":       "Basil of Caesarea",
    # Athanasius
    "athanas":     "Athanasius of Alexandria",
    "athan":       "Athanasius of Alexandria",
    "athanasius":  "Athanasius of Alexandria",
    # Eusebius
    "euseb":       "Eusebius of Caesarea",
    "eusebius":    "Eusebius of Caesarea",
    # Ambrose
    "ambros":      "Ambrose of Milan",
    "ambrose":     "Ambrose of Milan",
    # Hilary
    "hilary":      "Hilary of Poitiers",
    "hilar":       "Hilary of Poitiers",
    # Jerome
    "hieronym":    "Jerome (Hieronymus)",
    "jerome":      "Jerome (Hieronymus)",
    # Origen
    "origen":      "Origen of Alexandria",
    # Tertullian
    "tertull":     "Tertullian",
    "tertullian":  "Tertullian",
    # Cyprian
    "cyprian":     "Cyprian of Carthage",
    # Epiphanius
    "epiphan":     "Epiphanius of Salamis",
    "epiphanius":  "Epiphanius of Salamis",
    # Irenaeus
    "irenaeus":    "Irenaeus of Lyon",
    "iren":        "Irenaeus of Lyon",
    # Prosper
    "prosper":     "Prosper of Aquitaine",
    # Gregory of Nazianzus
    "nazianz":     "Gregory of Nazianzus",
    "greg":        "Gregory of Nazianzus",
    # Gregory the Great
    "gregory the great": "Gregory the Great (Gregorius Magnus)",
    # Gregory of Nyssa
    "nyssen":      "Gregory of Nyssa",
    # Lactantius
    "lactant":     "Lactantius",
    # Bede
    "beda":        "Bede",
    "bede":        "Bede",
    # Andradius
    "andrad":      "Andradius",
    "andradius":   "Andradius",
    # Cochlaeus
    "cochlaeus":   "Cochlaeus",
    "cochlae":     "Cochlaeus",
    # Pighius
    "pighius":     "Albertus Pighius",
    "pigh":        "Albertus Pighius",
    # Hosius
    "hosius":      "Stanislaus Hosius",
    # Clemens
    "clemens":     "Clement of Alexandria",
    # Theodoret
    "theodoret":   "Theodoret of Cyrrhus",
    # Socrates (Church historian)
    "socrat":      "Socrates Scholasticus",
    # Cyril of Alexandria
    "cyril":       "Cyril of Alexandria",
    # Leo the Great
    "leo":         "Leo the Great",
    # Maximus of Turin
    "maxim":       "Maximus of Turin",
    # Didymus
    "didymus":     "Didymus the Blind",
    # Novatian
    "novatian":    "Novatian",
    # Calvin
    "calvin":      "John Calvin",
    # Classical authors
    "aristotle":   "Aristotle",
    "aristot":     "Aristotle",
    "plato":       "Plato",
    "cicero":      "Cicero",
    "virgil":      "Virgil",
    "horace":      "Horace",
    "hor":         "Horace",
    "seneca":      "Seneca",
    "varro":       "Varro",
    "livy":        "Livy (Titus Livius)",
    "plutarch":    "Plutarch",
    # Aquinas
    "aquin":       "Thomas Aquinas",
    "aquinas":     "Thomas Aquinas",
    # Petavius (Petau)
    "petav":       "Denis Pétau (Petavius)",
    # Montacutius
    "montacu":     "Richard Montague (Montacutius)",
    # Bellarmine
    "bellar":      "Robert Bellarmine",
    # Socinus
    "socin":       "Faustus Socinus",
    # Melchior Cano
    "canus":       "Melchior Cano",
    # Sozomen
    "sozomen":     "Sozomen",
    # John of Damascus
    "damasc":      "John of Damascus",
    "damascen":    "John of Damascus",
    # Bernard of Clairvaux
    "bernard":     "Bernard of Clairvaux",
    # Constantine
    "constantine": "Constantine I",
    # Ephraim Syrus (Ephrem the Syrian)
    "ephraim":     "Ephraim Syrus (Ephrem the Syrian)",
    "ephrem":      "Ephraim Syrus (Ephrem the Syrian)",
    "ephraem":     "Ephraim Syrus (Ephrem the Syrian)",
    "syrus":       "Ephraim Syrus (Ephrem the Syrian)",
    # Fulgentius of Ruspe
    "fulgent":     "Fulgentius of Ruspe",
    "fulg":        "Fulgentius of Ruspe",
    # Clement of Alexandria
    "clement":     "Clement of Alexandria",
    "clem":        "Clement of Alexandria",
    # Theophylact of Ohrid
    "theophylact": "Theophylact of Ohrid",
    # Cassiodorus
    "cassiod":     "Cassiodorus",
    # Theophanes
    "theophanes":  "Theophanes the Confessor",
    # Peter Chrysologus
    "chrysolog":   "Peter Chrysologus",
    # Rufinus
    "rufinus":     "Rufinus of Aquileia",
    "rufin":       "Rufinus of Aquileia",
    # Pliny
    "pliny":       "Pliny the Younger",
    "plin":        "Pliny the Younger",
    # Ignatius
    "ignatius":    "Ignatius of Antioch",
    "ignat":       "Ignatius of Antioch",
    # Tacitus
    "tacitus":     "Tacitus",
    "tacit":       "Tacitus",
    # Justin
    "justin":      "Justin (Marcus Junianus Justinus)",
    "just":        "Justin (Marcus Junianus Justinus)",
    # Thucydides
    "thucydides":  "Thucydides",
    "thucyd":      "Thucydides",
    # Herodian
    "herodian":    "Herodian of Antioch",
    "herod":       "Herodian of Antioch",
    # Josephus
    "josephus":    "Flavius Josephus",
    "joseph":      "Flavius Josephus",
    # Glassius
    "glassius":    "Salomo Glassius",
    "glass":       "Salomo Glassius",
    # Drusius
    "drusius":     "Johannes Drusius",
    "drus":        "Johannes Drusius",
    # Volkelius
    "volkelius":   "Johannes Volkelius",
    "volkel":      "Johannes Volkelius",
    # Sozomen alias
    "sozom":       "Sozomen",
    # Calvin alias
    "calv":        "John Calvin",
    # Plotinus
    "plotinus":    "Plotinus",
    # Stapleton
    "stapleton":   "Thomas Stapleton",
    # Mantuanus
    "mantuanus":   "Baptista Mantuanus",
    "mantuan":     "Baptista Mantuanus",
    # Episcopius
    "episcopius":  "Simon Episcopius",
    # Sixtinus Amama
    "amama":       "Sixtinus Amama",
    # Xenophon
    "xenophon":    "Xenophon",
    "xen":         "Xenophon",
    # Dionysius of Halicarnassus
    "dionysius":   "Dionysius of Halicarnassus",
    "dion":        "Dionysius of Halicarnassus",
    # John Rainolds
    "rainolds":    "John Rainolds",
    "rainold":     "John Rainolds",
    # André Rivet
    "rivet":       "André Rivet",
    # Abraham Scultetus
    "scultetus":   "Abraham Scultetus",
    "scultet":     "Abraham Scultetus",
    # Dio Cassius
    "dio cassius": "Dio Cassius",
    "dio":         "Dio Cassius",
    "die cassius": "Dio Cassius",
    # Antonius Hulsius
    "hulsius":     "Antonius Hulsius",
    "huls":        "Antonius Hulsius",
    # Petrus Galatinus
    "galatinus":   "Petrus Galatinus",
    "galatin":     "Petrus Galatinus",
    # Martial
    "martial":     "Martial (Marcus Valerius Martialis)",
    # Stanisław Sarnicki
    "sarnicki":    "Stanisław Sarnicki",
    "sarnic":      "Stanisław Sarnicki",
    "sarricius":   "Stanisław Sarnicki",
    # Girolamo Zanchi
    "zanchius":    "Girolamo Zanchi",
    "zanch":       "Girolamo Zanchi",
    # Carolus Scribani / Clarus Bonarus
    "bonarus":     "Carolus Scribani (Clarus Bonarus)",
    "scribani":    "Carolus Scribani (Clarus Bonarus)",
    # Franciscus de Mendoza
    "mendoza":     "Franciscus de Mendoza",
    # Velleius Paterculus
    "paterculus":  "Velleius Paterculus",
    "paterc":      "Velleius Paterculus",
    # Servius
    "servius":     "Servius",
    # Joannes Stobaeus
    "stobaeus":    "Joannes Stobaeus",
    "stob":        "Joannes Stobaeus",
    # Joseph Albo
    "albo":        "Joseph Albo",
    "r. joseph":   "Joseph Albo",
    # Florimond de Raemond
    "raemond":     "Florimond de Raemond",
    "florim":      "Florimond de Raemond",
    # Melchior Cano OCR typo
    "canns":       "Melchior Cano",
    "conanus":     "François Connan",
    "menochius":   "Jacopo Menochio",
    "pighius":     "Albert Pighius",
    "cappel":      "Louis Cappel",
    "morinus":     "Jean Morin",
    "isaac":       "Johannes Isaac",
    "fuller":      "Nicholas Fuller",
    "azarias":     "Azariah de' Rossi",
    "justinian":   "Justinian I (Roman Law)",
    "themist":     "Themistius",
    "themistius":  "Themistius",
    "ammian":      "Ammianus Marcellinus",
    "ammianus":    "Ammianus Marcellinus",
    "lombard":     "Peter Lombard",
    "gregory_great": "Gregory the Great (Gregorius Magnus)",
    "bradwardine": "Thomas Bradwardine (Doctor Profundus)",
    "suarez":      "Francisco Suárez",
}

# ── Canonical Author Normalization ──────────────────────────────────────────
# Maps alias abbreviation keys to their primary canonical keys in WORK_MAP.
# This prevents duplicate work mapping entries and resolves lookups using aliases.
CANONICAL_AUTHOR_MAP = {
    "augustine":   "august",
    "austin":      "august",
    "aug":         "august",
    "chrysostom":  "chrysost",
    "chrys":       "chrysost",
    "athan":       "athanas",
    "athanasius":  "athanas",
    "eusebius":    "euseb",
    "ambrose":     "ambros",
    "hilar":       "hilary",
    "jerome":      "hieronym",
    "tertullian":  "tertull",
    "iren":        "irenaeus",
    "greg":        "nazianz",
    "gregory the great": "gregory_great",
    "aristot":     "aristotle",
    "aquinas":     "aquin",
    "damascen":    "damasc",
    "ephrem":      "ephraim",
    "ephraem":     "ephraim",
    "syrus":       "ephraim",
    "fulg":        "fulgent",
    "clement":     "clem",
    "clemens":     "clem",
    "beda":        "bede",
    "andrad":      "andradius",
    "cochlae":     "cochlaeus",
    "pigh":        "pighius",
    "sozom":       "sozomen",
    "rufin":       "rufinus",
    "plin":        "pliny",
    "ignat":       "ignatius",
    "tacit":       "tacitus",
    "just":        "justin",
    "thucyd":      "thucydides",
    "herod":       "herodian",
    "joseph":      "josephus",
    "glass":       "glassius",
    "drus":        "drusius",
    "volkel":      "volkelius",
    "calv":        "calvin",
    "xen":         "xenophon",
    "dion":        "dionysius",
    "rainold":     "rainolds",
    "scultet":     "scultetus",
    "dio":         "dio cassius",
    "die cassius": "dio cassius",
    "huls":        "hulsius",
    "galatin":     "galatinus",
    "sarnic":      "sarnicki",
    "sarricius":   "sarnicki",
    "zanch":       "zanchius",
    "scribani":    "bonarus",
    "paterc":      "paterculus",
    "stob":        "stobaeus",
    "r. joseph":   "albo",
    "florim":      "raemond",
    "canns":       "canus",
    "epiphanius":  "epiphan",
    "conan":       "conanus",
    "menoch":      "menochius",
    "pighio":      "pighius",
    "morin":       "morinus",
    "themistius":  "themist",
    "ammianus":    "ammian",
    "bradwardin":  "bradwardine",
}

# ── Work abbreviation → full citation data ───────────────────────────────────
# Keys: (author_key, work_abbrev_normalized)
# author_key:  lowercase key from AUTHOR_ABBREV_MAP (first match)
# work_abbrev: normalized lowercase work fragment (first 4+ chars, no punctuation)
# Values: dict with keys: full_title, latin_title, std_ref (list), pl, pg, notes

WORK_MAP = {
    # Augustine works
    ("august", "de trin"):   {"full_title": "On the Trinity", "latin_title": "De Trinitate",
                               "std_ref": ["NPNF1, 3"], "pl": "PL 42"},
    ("august", "trin"):      {"full_title": "On the Trinity", "latin_title": "De Trinitate",
                               "std_ref": ["NPNF1, 3"], "pl": "PL 42"},
    ("austin",  "de trin"):  {"full_title": "On the Trinity", "latin_title": "De Trinitate",
                               "std_ref": ["NPNF1, 3"], "pl": "PL 42"},
    ("august", "confess"):   {"full_title": "Confessions", "latin_title": "Confessiones",
                               "std_ref": ["NPNF1, 1:45–207"], "pl": "PL 32"},
    ("august", "de civ"):    {"full_title": "The City of God", "latin_title": "De Civitate Dei",
                               "std_ref": ["NPNF1, 2"], "pl": "PL 41"},
    ("august", "civ dei"):   {"full_title": "The City of God", "latin_title": "De Civitate Dei",
                               "std_ref": ["NPNF1, 2"], "pl": "PL 41"},
    ("august", "de praed"):  {"full_title": "On the Predestination of the Saints",
                               "latin_title": "De Praedestinatione Sanctorum",
                               "std_ref": ["NPNF1, 5:493–519"], "pl": "PL 44"},
    ("august", "de corr"):   {"full_title": "On Rebuke and Grace",
                               "latin_title": "De Correptione et Gratia",
                               "std_ref": ["NPNF1, 5:469–491"], "pl": "PL 44"},
    ("august", "de grat"):   {"full_title": "On Grace and Free Will",
                               "latin_title": "De Gratia et Libero Arbitrio",
                               "std_ref": ["NPNF1, 5:435–465"], "pl": "PL 44"},
    ("august", "enchir"):    {"full_title": "Enchiridion on Faith, Hope, and Love",
                               "latin_title": "Enchiridion ad Laurentium",
                               "std_ref": ["NPNF1, 3:229–276"], "pl": "PL 40"},
    ("august", "enchirid"):  {"full_title": "Enchiridion on Faith, Hope, and Love",
                               "latin_title": "Enchiridion ad Laurentium",
                               "std_ref": ["NPNF1, 3:229–276"], "pl": "PL 40"},
    ("august", "qu"):        {"full_title": "Eighty-Three Questions",
                               "latin_title": "De Diversis Quaestionibus LXXXIII",
                               "std_ref": ["FC 70"], "pl": "PL 40"},
    ("august", "83 qu"):     {"full_title": "Eighty-Three Questions",
                               "latin_title": "De Diversis Quaestionibus LXXXIII",
                               "std_ref": ["FC 70"], "pl": "PL 40"},
    ("august", "in johan"):  {"full_title": "Tractates on the Gospel of John",
                               "latin_title": "In Evangelium Johannis Tractatus",
                               "std_ref": ["NPNF1, 7"], "pl": "PL 35"},
    ("august", "tract in"):  {"full_title": "Tractates on the Gospel of John",
                               "latin_title": "In Evangelium Johannis Tractatus",
                               "std_ref": ["NPNF1, 7"], "pl": "PL 35"},
    ("august", "de verb"):   {"full_title": "Sermons on the Words of the Lord",
                               "latin_title": "Sermones de Verbis Domini",
                               "std_ref": ["NPNF1, 6:259–545"], "pl": "PL 38"},
    ("august", "serm"):      {"full_title": "Sermons", "latin_title": "Sermones",
                               "std_ref": ["NPNF1, 6:259–545"], "pl": "PL 38"},
    ("august", "epist"):     {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF1, 1:209–593"], "pl": "PL 33"},
    ("august", "contra fau"): {"full_title": "Against Faustus the Manichean",
                                "latin_title": "Contra Faustum Manichaeum",
                                "std_ref": ["NPNF1, 4:155–345"], "pl": "PL 42"},
    ("august", "retract"):   {"full_title": "Retractations", "latin_title": "Retractationes",
                               "std_ref": ["FC 60"], "pl": "PL 32"},
    # Chrysostom works
    ("chrysost", "homil"):   {"full_title": "Homilies", "latin_title": None,
                               "std_ref": ["NPNF1, 9–14"], "pg": "PG 47–64"},
    ("chrysost", "in johan"): {"full_title": "Homilies on the Gospel of John",
                                "latin_title": "In Johannem Homiliae",
                                "std_ref": ["NPNF1, 14"], "pg": "PG 59"},
    ("chrysost", "in rom"):  {"full_title": "Homilies on Romans",
                               "latin_title": "In Epistolam ad Romanos Homiliae",
                               "std_ref": ["NPNF1, 11"], "pg": "PG 60"},
    ("chrysost", "epist"):   {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF1, 9:169–304"], "pg": "PG 52"},
    # Basil works
    ("basil",  "adv eunom"): {"full_title": "Against Eunomius",
                               "latin_title": "Adversus Eunomium",
                               "std_ref": ["NPNF2, 8:35–66"], "pg": "PG 29"},
    ("basil",  "de spir"):   {"full_title": "On the Holy Spirit",
                               "latin_title": "De Spiritu Sancto",
                               "std_ref": ["NPNF2, 8:1–50"], "pg": "PG 32"},
    ("basil",  "epist"):     {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 8:109–327"], "pg": "PG 32"},
    # Athanasius works
    ("athanas", "orat"):     {"full_title": "Orations Against the Arians",
                               "latin_title": "Orationes Contra Arianos",
                               "std_ref": ["NPNF2, 4:303–447"], "pg": "PG 26"},
    ("athanas", "de incarn"): {"full_title": "On the Incarnation",
                                "latin_title": "De Incarnatione Verbi Dei",
                                "std_ref": ["NPNF2, 4:31–66"], "pg": "PG 25"},
    ("athanas", "epist"):    {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 4:495–581"], "pg": "PG 26"},
    # Eusebius of Caesarea
    ("euseb",  "hist eccles"): {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 1"], "pg": "PG 20"},
    ("euseb",  "chron"):       {"full_title": "Chronicle",
                                 "latin_title": "Chronicon",
                                 "std_ref": ["PG 19"], "pg": "PG 19"},
    ("euseb",  "eccles hist"): {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 1"], "pg": "PG 20"},
    ("euseb",  "hist"):        {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 1"], "pg": "PG 20"},
    ("euseb",  "lib"):         {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 1"], "pg": "PG 20"},
    ("euseb",  "praep evang"): {"full_title": "Preparation for the Gospel",
                                 "latin_title": "Praeparatio Evangelica",
                                 "std_ref": ["trans. Gifford, Oxford 1903"], "pg": "PG 21"},
    ("euseb",  "preparat ev"): {"full_title": "Preparation for the Gospel",
                                 "latin_title": "Praeparatio Evangelica",
                                 "std_ref": ["trans. Gifford, Oxford 1903"], "pg": "PG 21"},
    # Hilary works
    ("hilary", "de trin"):   {"full_title": "On the Trinity", "latin_title": "De Trinitate",
                               "std_ref": ["NPNF2, 9:40–233"], "pl": "PL 10"},
    ("hilar",  "de trin"):   {"full_title": "On the Trinity", "latin_title": "De Trinitate",
                               "std_ref": ["NPNF2, 9:40–233"], "pl": "PL 10"},
    # Ambrose works
    ("ambros", "de fid"):    {"full_title": "Of the Christian Faith",
                               "latin_title": "De Fide",
                               "std_ref": ["NPNF2, 10:201–314"], "pl": "PL 16"},
    ("ambros", "de spir"):   {"full_title": "On the Holy Spirit",
                               "latin_title": "De Spiritu Sancto",
                               "std_ref": ["NPNF2, 10:91–158"], "pl": "PL 16"},
    ("ambros", "de vocat"):  {"full_title": "On the Calling of the Gentiles",
                               "latin_title": "De Vocatione Gentium",
                               "notes": "(often attributed to Prosper of Aquitaine)", "pl": "PL 51"},
    ("ambros", "epist"):     {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 10:411–476"], "pl": "PL 16"},
    ("prosper", "de vocat"): {"full_title": "On the Calling of the Gentiles",
                               "latin_title": "De Vocatione Gentium",
                               "std_ref": ["FC 14:339–435"], "pl": "PL 51"},
    ("prosper", "lib"):      {"full_title": "On the Calling of the Gentiles",
                               "latin_title": "De Vocatione Gentium",
                               "std_ref": ["FC 14:339–435"], "pl": "PL 51"},
    # Jerome works
    ("hieronym", "epist"):   {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 6:1–295"], "pl": "PL 22"},
    ("jerome",   "epist"):   {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 6:1–295"], "pl": "PL 22"},
    # Cyprian works
    ("cyprian", "epist"):    {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["ANF 5:275–409"], "pl": "PL 4"},
    ("cyprian", "serm"):     {"full_title": "Sermons (Pseudo-Cyprian)", "latin_title": "De cardinalibus operibus Christi",
                               "std_ref": ["PL 189:1609-1678"]},
    ("cyprian", "de unit"):  {"full_title": "On the Unity of the Church",
                               "latin_title": "De Unitate Ecclesiae",
                               "std_ref": ["ANF 5:419–429"], "pl": "PL 4"},
    # Origen works
    ("origen", "con cels"):  {"full_title": "Against Celsus", "latin_title": "Contra Celsum",
                               "std_ref": ["ANF 4:395–669"], "pg": "PG 11"},
    ("origen", "adv cels"):  {"full_title": "Against Celsus", "latin_title": "Contra Celsum",
                               "std_ref": ["ANF 4:395–669"], "pg": "PG 11"},
    # Irenaeus
    ("irenaeus", "adv haer"):{"full_title": "Against Heresies",
                               "latin_title": "Adversus Haereses",
                               "std_ref": ["ANF 1"], "pg": "PG 7"},
    ("irenaeus", "lib"):     {"full_title": "Against Heresies",
                               "latin_title": "Adversus Haereses",
                               "std_ref": ["ANF 1"], "pg": "PG 7"},
    ("iren", "adv haer"):    {"full_title": "Against Heresies",
                               "latin_title": "Adversus Haereses",
                               "std_ref": ["ANF 1"], "pg": "PG 7"},
    ("iren", "lib"):         {"full_title": "Against Heresies",
                               "latin_title": "Adversus Haereses",
                               "std_ref": ["ANF 1"], "pg": "PG 7"},
    ("tertull", "adv marc"): {"full_title": "Against Marcion",
                               "latin_title": "Adversus Marcionem",
                               "std_ref": ["ANF 3:269–474"], "pl": "PL 2"},
    ("tertull", "de praes"): {"full_title": "Prescriptions Against Heretics",
                               "latin_title": "De Praescriptione Haereticorum",
                               "std_ref": ["ANF 3:243–265"], "pl": "PL 2"},
    ("tertull", "de idol"):  {"full_title": "On Idolatry",
                               "latin_title": "De Idololatria",
                               "std_ref": ["ANF 3:61–76"], "pl": "PL 2"},
    # Socrates Scholasticus
    ("socrat", "hist eccles"): {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("socrat", "eccles hist"): {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("socrat", "hist"):        {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("socrat", "lib"):         {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    # Sozomen
    ("sozomen", "hist eccles"):{"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("sozomen", "eccles hist"):{"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("sozomen", "hist"):       {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    ("sozomen", "lib"):        {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 2"], "pg": "PG 67"},
    # Theodoret
    ("theodoret", "hist eccles"):{"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 3"], "pg": "PG 82"},
    ("theodoret", "eccles hist"):{"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 3"], "pg": "PG 82"},
    ("theodoret", "hist"):       {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 3"], "pg": "PG 82"},
    ("theodoret", "lib"):        {"full_title": "Ecclesiastical History",
                                 "latin_title": "Historia Ecclesiastica",
                                 "std_ref": ["NPNF2, 3"], "pg": "PG 82"},
    # Calvin
    ("calvin", "institut"):  {"full_title": "Institutes of the Christian Religion",
                               "latin_title": "Institutio Christianae Religionis",
                               "std_ref": ["Battles ed. (LCC 20–21)"]},
    ("calvin", "instit"):    {"full_title": "Institutes of the Christian Religion",
                               "latin_title": "Institutio Christianae Religionis",
                               "std_ref": ["Battles ed. (LCC 20–21)"]},
    # Aristotle
    ("aristot", "ethic"):    {"full_title": "Nicomachean Ethics",
                               "latin_title": "Ethica Nicomachea",
                               "std_ref": ["trans. Ross (Oxford)"]},
    ("aristotle", "ethic"):  {"full_title": "Nicomachean Ethics",
                               "latin_title": "Ethica Nicomachea",
                               "std_ref": ["trans. Ross (Oxford)"]},
    # Aquinas
    ("aquin", "summ"):       {"full_title": "Summa Theologica",
                               "latin_title": "Summa Theologiae",
                               "std_ref": ["trans. Fathers of the English Dominican Province"]},
    # Epiphanius
    ("epiphan", "haer"):     {"full_title": "Panarion (Against Heresies)",
                               "latin_title": "Panarion (Adversus Haereses)",
                               "std_ref": ["GCS; trans. Williams"], "pg": "PG 41–42"},
    # Leo the Great
    ("leo", "serm"):         {"full_title": "Sermons", "latin_title": "Sermones",
                               "std_ref": ["NPNF2, 12:115–205"], "pl": "PL 54"},
    ("leo", "epist"):        {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["NPNF2, 12:1–114"], "pl": "PL 54"},
    # Horace
    ("hor", "sat"):          {"full_title": "Satires", "latin_title": "Satirae",
                               "std_ref": ["Loeb Classical Library"]},
    ("hor", "ep"):           {"full_title": "Epistles", "latin_title": "Epistulae",
                               "std_ref": ["Loeb Classical Library"]},
    # Seneca
    ("seneca", "ep"):        {"full_title": "Letters to Lucilius",
                               "latin_title": "Epistulae Morales ad Lucilium",
                               "std_ref": ["Loeb Classical Library"]},
    # Varro
    ("varro", "de ling"):    {"full_title": "On the Latin Language",
                               "latin_title": "De Lingua Latina",
                               "std_ref": ["Loeb Classical Library"]},
    # Ephraim Syrus (Ephrem the Syrian)
    # Owen uses the Latin translations of Ephraim's Syriac works
    ("ephraim", "cap"):      {"full_title": "On Those Who Search Out the Nature of the Son",
                               "latin_title": "Adversus Scrutatores",
                               "notes": "Ephraim Syrus (Ephrem the Syrian), c. 306–373. "
                                        "Owen cites the Latin translation of this homily "
                                        "against speculative theology.",
                               "std_ref": ["Opera Omnia, Rome 1732–1746 (ed. Assemani)"]},
    ("ephraem", "cap"):      {"full_title": "On Those Who Search Out the Nature of the Son",
                               "latin_title": "Adversus Scrutatores",
                               "std_ref": ["Opera Omnia, Rome 1732–1746 (ed. Assemani)"]},
    ("syrus",  "cap"):       {"full_title": "On Those Who Search Out the Nature of the Son",
                               "latin_title": "Adversus Scrutatores",
                               "std_ref": ["Opera Omnia, Rome 1732–1746 (ed. Assemani)"]},
    # Lactantius
    ("lactant", "institut"): {"full_title": "Divine Institutes",
                               "latin_title": "Divinae Institutiones",
                               "std_ref": ["ANF 7"], "pl": "PL 6"},
    ("lactant", "lib"):      {"full_title": "Divine Institutes",
                               "latin_title": "Divinae Institutiones",
                               "std_ref": ["ANF 7"], "pl": "PL 6"},
    # Fulgentius of Ruspe
    ("fulg", "lib"):         {"full_title": "Ad Thrasimundum (To King Thrasimund)",
                               "latin_title": "Ad Thrasimundum Regem Vandalorum libri III",
                               "std_ref": ["FC; PL 65"], "pl": "PL 65"},
    ("fulgent", "lib"):      {"full_title": "To King Thrasimund",
                               "latin_title": "Ad Thrasimundum Regem Vandalorum",
                               "std_ref": ["FC; PL 65"], "pl": "PL 65"},
    # Clement of Alexandria
    ("clement", "stromat"):  {"full_title": "Stromata (Miscellanies)",
                               "latin_title": "Stromata",
                               "std_ref": ["ANF 2"], "pg": "PG 8"},
    ("clement", "strom"):    {"full_title": "Stromata (Miscellanies)",
                               "latin_title": "Stromata",
                               "std_ref": ["ANF 2"], "pg": "PG 8"},
    ("clem", "stromat"):     {"full_title": "Stromata (Miscellanies)",
                               "latin_title": "Stromata",
                               "std_ref": ["ANF 2"], "pg": "PG 8"},
    ("clem", "strom"):       {"full_title": "Stromata (Miscellanies)",
                               "latin_title": "Stromata",
                               "std_ref": ["ANF 2"], "pg": "PG 8"},
    ("clem",    "stromat"):  {"full_title": "Stromata (Miscellanies)",
                               "latin_title": "Stromata",
                               "std_ref": ["ANF 2:299–567"], "pg": "PG 8–9"},
    # Clement of Alexandria: Exhortation to the Heathen (Adhortatio ad Gentes / Protrepticus)
    ("clem", "adhort"):      {"full_title": "Exhortation to the Heathen", "latin_title": "Protrepticus (Adhortatio ad Gentes)", "std_ref": ["ANF 2:171–206"], "pg": "PG 8.49–246"},
    ("clem", "adhortatio"):  {"full_title": "Exhortation to the Heathen", "latin_title": "Protrepticus (Adhortatio ad Gentes)", "std_ref": ["ANF 2:171–206"], "pg": "PG 8.49–246"},
    ("clem", "gentes"):      {"full_title": "Exhortation to the Heathen", "latin_title": "Protrepticus (Adhortatio ad Gentes)", "std_ref": ["ANF 2:171–206"], "pg": "PG 8.49–246"},
    # Bellarmine works
    ("bellar", "de justif"): {"full_title": "On Justification",
                               "latin_title": "De Iustificatione",
                               "std_ref": ["Disputationes de Controversiis, Tom. IV"]},
    ("bellar", "de amiss"):  {"full_title": "On the Loss of Grace and State of Sin",
                               "latin_title": "De Amissione Gratiae et Statu Peccati",
                               "std_ref": ["Disputationes de Controversiis, Tom. IV"]},
    ("bellar", "de amiss grat"): {"full_title": "On the Loss of Grace and State of Sin",
                               "latin_title": "De Amissione Gratiae et Statu Peccati",
                               "std_ref": ["Disputationes de Controversiis, Tom. IV"]},
    ("bellar", "de grat"):   {"full_title": "On Grace and Free Will",
                               "latin_title": "De Gratia et Libero Arbitrio",
                               "std_ref": ["Disputationes de Controversiis, Tom. IV"]},
    ("bellar", "de pont"):   {"full_title": "On the Roman Pontiff",
                               "latin_title": "De Romano Pontifice",
                               "std_ref": ["Disputationes de Controversiis, Tom. I"]},
    ("bellar", "de justificat"): {"full_title": "On Justification",
                               "latin_title": "De Iustificatione",
                               "std_ref": ["Disputationes de Controversiis, Tom. IV"]},
    ("bellar", "de rom pontif"): {"full_title": "On the Roman Pontiff",
                               "latin_title": "De Romano Pontifice",
                               "std_ref": ["Disputationes de Controversiis, Tom. I"]},
    ("bellar", "de pont rom"): {"full_title": "On the Roman Pontiff",
                               "latin_title": "De Romano Pontifice",
                               "std_ref": ["Disputationes de Controversiis, Tom. I"]},
    # Socinus works
    ("socin", "de servat"):  {"full_title": "On Jesus Christ the Savior",
                               "latin_title": "De Iesu Christo Servatore",
                               "std_ref": ["Bibliotheca Fratrum Polonorum"]},
    # Melchior Cano
    ("canus", "loc theol"):  {"full_title": "Loci Theologici",
                               "latin_title": "De Locis Theologicis",
                               "std_ref": ["Opera Theologica"]},
    ("canus", "loci theol"): {"full_title": "Loci Theologici",
                               "latin_title": "De Locis Theologicis",
                               "std_ref": ["Opera Theologica"]},
    # Cyril of Alexandria works
    ("cyril", "in joan"):    {"full_title": "Commentary on John",
                               "latin_title": "Commentarii in Joannem",
                               "std_ref": ["Pusey ed. (Oxford)"], "pg": "PG 73–74"},
    # Theodoret works
    ("theodoret", "hist eccles"): {"full_title": "Ecclesiastical History",
                                    "latin_title": "Historia Ecclesiastica",
                                    "std_ref": ["NPNF2, 3:33–159"], "pg": "PG 82"},
    # Sozomen
    ("sozomen", "hist eccles"): {"full_title": "Ecclesiastical History",
                                  "latin_title": "Historia Ecclesiastica",
                                  "std_ref": ["NPNF2, 2:233–427"], "pg": "PG 67"},
    # John of Damascus
    ("damasc", "de fide"):   {"full_title": "Exact Exposition of the Orthodox Faith",
                               "latin_title": "De Fide Orthodoxa",
                               "std_ref": ["NPNF2, 9:1–101"], "pg": "PG 94"},
    ("damascen", "de fide"): {"full_title": "Exact Exposition of the Orthodox Faith",
                               "latin_title": "De Fide Orthodoxa",
                               "std_ref": ["NPNF2, 9:1–101"], "pg": "PG 94"},
    # Bernard of Clairvaux
    ("bernard", "epist"):    {"full_title": "Letters", "latin_title": "Epistulae",
                               "std_ref": ["trans. B.S. James"], "pl": "PL 182"},
    # Bellarmine new works
    ("bellar", "de ecclesiastes"): {"full_title": "On the Church Militant", "latin_title": "De Ecclesia Militante", "std_ref": ["Disputationes de Controversiis, Tom. II"]},
    ("bellar", "de eccles"):       {"full_title": "On the Church Militant", "latin_title": "De Ecclesia Militante", "std_ref": ["Disputationes de Controversiis, Tom. II"]},
    ("bellar", "de ecclea"):       {"full_title": "On the Church Militant", "latin_title": "De Ecclesia Militante", "std_ref": ["Disputationes de Controversiis, Tom. II"]},
    ("bellar", "de ecclea triumph"): {"full_title": "On the Church Militant", "latin_title": "De Ecclesia Militante", "std_ref": ["Disputationes de Controversiis, Tom. II"]},
    ("bellar", "de verb dei"):     {"full_title": "On the Word of God", "latin_title": "De Verbo Dei", "std_ref": ["Disputationes de Controversiis, Tom. I"]},
    ("bellar", "de verbo dei"):    {"full_title": "On the Word of God", "latin_title": "De Verbo Dei", "std_ref": ["Disputationes de Controversiis, Tom. I"]},
    ("bellar", "de concil"):       {"full_title": "On the Councils", "latin_title": "De Conciliis et Ecclesia", "std_ref": ["Disputationes de Controversiis, Tom. II"]},

    # Clement of Alexandria new works
    ("clem", "pedag"):            {"full_title": "The Tutor", "latin_title": "Paedagogus", "std_ref": ["ANF 2:209–298"], "pg": "PG 8.249–684"},
    ("clem", "paedag"):           {"full_title": "The Tutor", "latin_title": "Paedagogus", "std_ref": ["ANF 2:209–298"], "pg": "PG 8.249–684"},

    # Theodoret new works
    ("theodoret", "epist"):        {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["NPNF2, 3:293–348"], "pg": "PG 83.1313–1316"},
    ("theodoret", "ep"):           {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["NPNF2, 3:293–348"], "pg": "PG 83.1313–1316"},

    # Epiphanius new works
    ("epiphan", "lib"):           {"full_title": "Panarion (Against Heresies)", "latin_title": "Panarion (Adversus Haereses)", "std_ref": ["GCS; trans. Williams"], "pg": "PG 41–42"},
    ("epiphan", "tom"):           {"full_title": "Panarion (Against Heresies)", "latin_title": "Panarion (Adversus Haereses)", "std_ref": ["GCS; trans. Williams"], "pg": "PG 41–42"},
    ("epiphan", "panario"):       {"full_title": "Panarion (Against Heresies)", "latin_title": "Panarion (Adversus Haereses)", "std_ref": ["GCS; trans. Williams"], "pg": "PG 41–42"},

    # Sozomen new works
    ("sozomen", "hist"):          {"full_title": "Ecclesiastical History", "latin_title": "Historia Ecclesiastica", "std_ref": ["NPNF2, 2:233–427"], "pg": "PG 67.843–1630"},

    # Rufinus new works
    ("rufinus", "hist eccles"):   {"full_title": "Ecclesiastical History", "latin_title": "Historia Ecclesiastica", "std_ref": ["NPNF2, 3:33–159"], "pl": "PL 21.465–540"},
    ("rufinus", "eccles hist"):   {"full_title": "Ecclesiastical History", "latin_title": "Historia Ecclesiastica", "std_ref": ["NPNF2, 3:33–159"], "pl": "PL 21.465–540"},
    ("rufinus", "hist"):          {"full_title": "Ecclesiastical History", "latin_title": "Historia Ecclesiastica", "std_ref": ["NPNF2, 3:33–159"], "pl": "PL 21.465–540"},
    ("rufinus", "lib"):           {"full_title": "Ecclesiastical History", "latin_title": "Historia Ecclesiastica", "std_ref": ["NPNF2, 3:33–159"], "pl": "PL 21.465–540"},

    # Pliny new works
    ("pliny", "epist"):           {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["Loeb Classical Library (LCL 55, 59)"]},
    ("pliny", "ep"):              {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["Loeb Classical Library (LCL 55, 59)"]},

    # Ignatius new works
    ("ignatius", "epist"):        {"full_title": "Epistles", "latin_title": "Epistulae", "std_ref": ["ANF 1:45–96"], "pg": "PG 5.643–938"},
    ("ignatius", "ep"):           {"full_title": "Epistles", "latin_title": "Epistulae", "std_ref": ["ANF 1:45–96"], "pg": "PG 5.643–938"},

    # Tacitus new works
    ("tacitus", "hist"):          {"full_title": "Histories", "latin_title": "Historiae", "std_ref": ["Loeb Classical Library (LCL 111, 249)"]},
    ("tacitus", "annal"):         {"full_title": "Annals", "latin_title": "Annales", "std_ref": ["Loeb Classical Library (LCL 249, 312, 322)"]},
    ("tacitus", "lib"):           {"full_title": "Histories/Annals", "latin_title": "Historiae/Annales", "std_ref": ["Loeb Classical Library"]},

    # Justin (historian) new works
    ("justin", "lib"):            {"full_title": "Epitome of the Philippic History of Pompeius Trogus", "latin_title": "Epitome Historiarum Philippicarum", "std_ref": ["trans. J.S. Watson (London, 1853)"]},
    ("justin", "hist"):           {"full_title": "Epitome of the Philippic History of Pompeius Trogus", "latin_title": "Epitome Historiarum Philippicarum", "std_ref": ["trans. J.S. Watson (London, 1853)"]},

    # Thucydides new works
    ("thucydides", "lib"):        {"full_title": "History of the Peloponnesian War", "latin_title": "Historiae", "std_ref": ["Loeb Classical Library (LCL 108–110)"]},
    ("thucydides", "hist"):       {"full_title": "History of the Peloponnesian War", "latin_title": "Historiae", "std_ref": ["Loeb Classical Library (LCL 108–110)"]},

    # Herodian new works
    ("herodian", "lib"):          {"full_title": "History of the Empire from the Death of Marcus", "latin_title": "Historia de Imperio post Marcum", "std_ref": ["Loeb Classical Library (LCL 454–455)"]},
    ("herodian", "hist"):         {"full_title": "History of the Empire from the Death of Marcus", "latin_title": "Historia de Imperio post Marcum", "std_ref": ["Loeb Classical Library (LCL 454–455)"]},

    # Josephus new works
    ("josephus", "antiq"):        {"full_title": "Jewish Antiquities", "latin_title": "Antiquitates Judaicae", "std_ref": ["Loeb Classical Library (LCL 242, 453, etc.)"]},
    ("josephus", "bell"):         {"full_title": "The Jewish War", "latin_title": "De Bello Judaico", "std_ref": ["Loeb Classical Library (LCL 203, 210)"]},
    ("josephus", "lib"):          {"full_title": "Jewish Antiquities/War", "latin_title": "Antiquitates/De Bello Judaico", "std_ref": ["Loeb Classical Library"]},

    # Glassius new works
    ("glassius", "lib"):          {"full_title": "Philologia Sacra", "latin_title": "Philologia Sacra", "std_ref": ["Leipzig, 1705"]},
    ("glassius", "tract"):         {"full_title": "Philologia Sacra", "latin_title": "Philologia Sacra", "std_ref": ["Leipzig, 1705"]},

    # Drusius new works
    ("drusius", "observat"):      {"full_title": "Observations on Holy Scripture", "latin_title": "Observationes Sacrae", "std_ref": ["Franeker, 1584"]},
    ("drusius", "lib"):           {"full_title": "Observations on Holy Scripture", "latin_title": "Observationes Sacrae", "std_ref": ["Franeker, 1584"]},

    # Volkelius new works
    ("volkelius", "de vera"):     {"full_title": "On the True Religion", "latin_title": "De Vera Religione", "std_ref": ["Raków, 1630"]},
    ("volkelius", "lib"):          {"full_title": "On the True Religion", "latin_title": "De Vera Religione", "std_ref": ["Raków, 1630"]},

    # Plotinus new works
    ("plotinus", "ennead"):       {"full_title": "Enneads", "latin_title": "Enneades", "std_ref": ["Loeb Classical Library"]},
    ("plotinus", "lib"):          {"full_title": "Enneads", "latin_title": "Enneades", "std_ref": ["Loeb Classical Library"]},

    # Stapleton new works
    ("stapleton", "de prin"):     {"full_title": "On the Principles of the Faith", "latin_title": "De Principiis Fidei Doctrinalibus", "std_ref": ["Paris, 1579"]},
    ("stapleton", "lib"):          {"full_title": "On the Principles of the Faith", "latin_title": "De Principiis Fidei Doctrinalibus", "std_ref": ["Paris, 1579"]},

    # Mantuanus new works
    ("mantuanus", "de pat"):      {"full_title": "On Patience", "latin_title": "De Patientia", "std_ref": ["Bologna, 1497"]},
    ("mantuanus", "lib"):          {"full_title": "On Patience", "latin_title": "De Patientia", "std_ref": ["Bologna, 1497"]},

    # Episcopius new works
    ("episcopius", "ep"):         {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["Opera Theologica (Amsterdam, 1650)"]},
    ("episcopius", "lib"):         {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["Opera Theologica (Amsterdam, 1650)"]},

    # Sixtinus Amama new works
    ("amama", "anti"):            {"full_title": "Anti-Barbarus Biblicus", "latin_title": "Anti-Barbarus Biblicus", "std_ref": ["Franeker, 1628"]},
    ("amama", "lib"):             {"full_title": "Anti-Barbarus Biblicus", "latin_title": "Anti-Barbarus Biblicus", "std_ref": ["Franeker, 1628"]},

    # Xenophon works
    ("xenophon", "cyrop"):        {"full_title": "Cyropaedia (The Education of Cyrus)", "latin_title": "Cyropaedia", "std_ref": ["Loeb Classical Library (LCL 51–52)"]},
    ("xenophon", "lib"):         {"full_title": "Cyropaedia (The Education of Cyrus)", "latin_title": "Cyropaedia", "std_ref": ["Loeb Classical Library (LCL 51–52)"]},

    # Dionysius of Halicarnassus works
    ("dionysius", "antiq"):       {"full_title": "Roman Antiquities", "latin_title": "Antiquitates Romanae", "std_ref": ["Loeb Classical Library (LCL 319, 347, etc.)"]},
    ("dionysius", "lib"):         {"full_title": "Roman Antiquities", "latin_title": "Antiquitates Romanae", "std_ref": ["Loeb Classical Library (LCL 319, 347, etc.)"]},

    # John Rainolds works
    ("rainolds", "de idol"):      {"full_title": "On the Idolatry of the Roman Church", "latin_title": "De Romanae Ecclesiae Idolatria", "std_ref": ["Oxford, 1596"]},
    ("rainolds", "lib"):          {"full_title": "On the Idolatry of the Roman Church", "latin_title": "De Romanae Ecclesiae Idolatria", "std_ref": ["Oxford, 1596"]},

    # André Rivet works
    ("rivet", "crit sac"):        {"full_title": "Sacred Criticism", "latin_title": "Critica Sacra", "std_ref": ["Rotterdam, 1612"]},
    ("rivet", "lib"):             {"full_title": "Sacred Criticism", "latin_title": "Critica Sacra", "std_ref": ["Rotterdam, 1612"]},

    # Abraham Scultetus works
    ("scultetus", "medul"):       {"full_title": "Marrow of the Fathers", "latin_title": "Medulla Theologiae Patrum", "std_ref": ["Amberg, 1598"]},
    ("scultetus", "lib"):         {"full_title": "Marrow of the Fathers", "latin_title": "Medulla Theologiae Patrum", "std_ref": ["Amberg, 1598"]},

    # Dio Cassius works
    ("dio cassius", "hist"):      {"full_title": "Roman History", "latin_title": "Historia Romana", "std_ref": ["Loeb Classical Library (LCL 32, 37, etc.)"]},
    ("dio cassius", "lib"):       {"full_title": "Roman History", "latin_title": "Historia Romana", "std_ref": ["Loeb Classical Library (LCL 32, 37, etc.)"]},

    # Antonius Hulsius works
    ("hulsius", "theolog"):       {"full_title": "Theologia Judaica", "latin_title": "Theologia Judaica", "std_ref": ["Breda, 1653"]},
    ("hulsius", "lib"):          {"full_title": "Theologia Judaica", "latin_title": "Theologia Judaica", "std_ref": ["Breda, 1653"]},

    # Petrus Galatinus works
    ("galatinus", "arcan"):       {"full_title": "On the Secrets of Catholic Truth", "latin_title": "De Arcanis Catholicae Veritatis", "std_ref": ["Ortona, 1518"]},
    ("galatinus", "lib"):         {"full_title": "On the Secrets of Catholic Truth", "latin_title": "De Arcanis Catholicae Veritatis", "std_ref": ["Ortona, 1518"]},

    # Martial works
    ("martial", "lib"):           {"full_title": "Epigrams", "latin_title": "Epigrammata", "std_ref": ["Loeb Classical Library (LCL 94–95)"]},
    ("martial", "ep"):            {"full_title": "Epigrams", "latin_title": "Epigrammata", "std_ref": ["Loeb Classical Library (LCL 94–95)"]},

    # Stanisław Sarnicki works
    ("sarnicki", "annal"):        {"full_title": "Annals of Poland", "latin_title": "Annales Poloniae", "std_ref": ["Cracow, 1587"]},
    ("sarnicki", "lib"):          {"full_title": "Annals of Poland", "latin_title": "Annales Poloniae", "std_ref": ["Cracow, 1587"]},

    # Girolamo Zanchi works
    ("zanchius", "de tribus"):    {"full_title": "On the Three Elohim", "latin_title": "De Tribus Elohim", "std_ref": ["Neustadt, 1589"]},
    ("zanchius", "lib"):          {"full_title": "On the Three Elohim", "latin_title": "De Tribus Elohim", "std_ref": ["Neustadt, 1589"]},

    # Carolus Scribani / Clarus Bonarus works
    ("bonarus", "amphitheatr"):   {"full_title": "Amphitheater of Honor", "latin_title": "Amphitheatrum Honoris", "std_ref": ["Antwerp, 1605"]},
    ("bonarus", "amphitrial"):    {"full_title": "Amphitheater of Honor", "latin_title": "Amphitheatrum Honoris (Amphitrial)", "std_ref": ["Antwerp, 1605"]},
    ("bonarus", "lib"):           {"full_title": "Amphitheater of Honor", "latin_title": "Amphitheatrum Honoris", "std_ref": ["Antwerp, 1605"]},

    # Franciscus de Mendoza works
    ("mendoza", "viridarium"):    {"full_title": "Garden of Both Kinds of Erudition", "latin_title": "Viridarium Utriusque Eruditionis", "std_ref": ["Cologne, 1633"]},
    ("mendoza", "lib"):           {"full_title": "Garden of Both Kinds of Erudition", "latin_title": "Viridarium Utriusque Eruditionis", "std_ref": ["Cologne, 1633"]},

    # Velleius Paterculus works
    ("paterculus", "hist"):       {"full_title": "Roman History", "latin_title": "Historia Romana", "std_ref": ["Loeb Classical Library (LCL 152)"]},
    ("paterculus", "lib"):        {"full_title": "Roman History", "latin_title": "Historia Romana", "std_ref": ["Loeb Classical Library (LCL 152)"]},

    # Servius works
    ("servius", "in"):            {"full_title": "Commentary on Virgil's Aeneid", "latin_title": "In Vergilii Aeneidem Commentarii", "std_ref": ["Harvard Edition"]},
    ("servius", "lib"):           {"full_title": "Commentary on Virgil's Aeneid", "latin_title": "In Vergilii Aeneidem Commentarii", "std_ref": ["Harvard Edition"]},

    # Joannes Stobaeus works
    ("stobaeus", "serm"):         {"full_title": "Anthology", "latin_title": "Florilegium (Anthologium)", "std_ref": ["ed. Wachsmuth & Hense"]},
    ("stobaeus", "lib"):          {"full_title": "Anthology", "latin_title": "Florilegium (Anthologium)", "std_ref": ["ed. Wachsmuth & Hense"]},

    # Joseph Albo works
    ("albo", "orat"):             {"full_title": "Book of Principles", "latin_title": "Sefer ha-Ikkarim", "std_ref": ["trans. Husik"]},
    ("albo", "lib"):              {"full_title": "Book of Principles", "latin_title": "Sefer ha-Ikkarim", "std_ref": ["trans. Husik"]},

    # Florimond de Raemond works
    ("raemond", "hist"):          {"full_title": "History of the Rise, Progress, and Ruin of the Heresies of this Age", "latin_title": "Historia de Origine, Progressu, et Ruina Haeresum huius Saeculi", "std_ref": ["Cologne, 1614"]},
    ("raemond", "lib"):           {"full_title": "History of the Rise, Progress, and Ruin of the Heresies of this Age", "latin_title": "Historia de Origine, Progressu, et Ruina Haeresum huius Saeculi", "std_ref": ["Cologne, 1614"]},

    # Pliny the Elder natural history
    ("pliny", "nat hist"):        {"full_title": "Natural History", "latin_title": "Naturalis Historia", "std_ref": ["Loeb Classical Library (LCL 330, etc.)"]},
    ("pliny", "naturalis"):       {"full_title": "Natural History", "latin_title": "Naturalis Historia", "std_ref": ["Loeb Classical Library"]},

    # Augustine to Dardanus letter
    ("august", "ad dardan"):      {"full_title": "Letter to Dardanus (On the Presence of God)", "latin_title": "Epistula 187 (ad Dardanum)", "std_ref": ["NPNF1, 1; PL 33.832"]},
    ("august", "dardan"):         {"full_title": "Letter to Dardanus (On the Presence of God)", "latin_title": "Epistula 187 (ad Dardanum)", "std_ref": ["NPNF1, 1; PL 33.832"]},

    # Faustus Socinus additional works
    ("socin", "ep"):              {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["Bibliotheca Fratrum Polonorum"]},
    ("socin", "respon"):          {"full_title": "Answer to Niemojevium", "latin_title": "Responsio ad Niemojevium", "std_ref": ["Bibliotheca Fratrum Polonorum"]},

    # Seneca additional works
    ("seneca", "natural"):        {"full_title": "Natural Questions", "latin_title": "Naturales Quaestiones", "std_ref": ["Loeb Classical Library"]},
    ("seneca", "nat"):            {"full_title": "Natural Questions", "latin_title": "Naturales Quaestiones", "std_ref": ["Loeb Classical Library"]},

    # Cyprian additional work
    ("cyprian", "adver"):         {"full_title": "Three Books of Testimonies Against the Jews", "latin_title": "Ad Quirinum adversus Judaeos", "std_ref": ["ANF 5:507–553", "PL 4"]},

    # Newly added classical/theological/juridical works (Issue 91 resolution)
    ("aristotle", "rhet"):        {"full_title": "Rhetoric", "latin_title": "Ars Rhetorica", "std_ref": ["Loeb Classical Library (LCL 193)"]},
    ("aristot", "rhet"):          {"full_title": "Rhetoric", "latin_title": "Ars Rhetorica", "std_ref": ["Loeb Classical Library (LCL 193)"]},
    ("conanus", "comment"):       {"full_title": "Commentaries on the Civil Law", "latin_title": "Commentaria Juris Civilis", "std_ref": ["Paris, 1553"]},
    ("justinian", "instit"):      {"full_title": "Institutes", "latin_title": "Institutiones", "std_ref": ["Corpus Juris Civilis, Vol. I"]},
    ("justinian", "digest"):      {"full_title": "Digest", "latin_title": "Digesta (Pandectae)", "std_ref": ["Corpus Juris Civilis, Vol. I"]},
    ("volkelius", "de relig"):    {"full_title": "On the True Religion", "latin_title": "De Vera Religione", "std_ref": ["Raków, 1630"]},
    ("volkelius", "de relig."):   {"full_title": "On the True Religion", "latin_title": "De Vera Religione", "std_ref": ["Raków, 1630"]},
    ("august", "de bapt"):        {"full_title": "On Baptism, Against the Donatists", "latin_title": "De Baptismo contra Donatistas", "std_ref": ["NPNF1, 4:411–514"], "pl": "PL 43"},
    ("menochius", "de arbit"):    {"full_title": "On the Arbitrary Decisions of Judges", "latin_title": "De Arbitrariis Judicum Quaestionibus et Causis", "std_ref": ["Venice, 1569"]},
    ("pighius", "de coelest"):    {"full_title": "On the Celestial Hierarchy", "latin_title": "De Caelesti Hierarchia", "std_ref": ["Cologne, 1538"]},
    ("cappel", "critica"):        {"full_title": "Critica Sacra", "latin_title": "Critica Sacra", "std_ref": ["Paris, 1650"]},
    ("morinus", "exercit"):       {"full_title": "Biblical Exercises", "latin_title": "Exercitationes Biblicae", "std_ref": ["Paris, 1633"]},
    ("josephus", "contra apionem"): {"full_title": "Against Apion", "latin_title": "Contra Apionem", "std_ref": ["Loeb Classical Library (LCL 186)"]},
    ("isaac", "ad lindan"):       {"full_title": "Defense of the Hebrew Truth against Lindanus", "latin_title": "Defensio Veritatis Hebraicae adversus Lindanum", "std_ref": ["Cologne, 1559"]},
    ("fuller", "miscellan"):      {"full_title": "Theological Miscellanies", "latin_title": "Miscellaneorum Theologicorum", "std_ref": ["Oxford, 1616"]},
    ("azarias", "re binah"):      {"full_title": "The Understanding of Binah", "latin_title": "Imrei Binah", "std_ref": ["Mantua, 1573"]},
    ("nazianz", "spir"):          {"full_title": "On the Holy Spirit", "latin_title": "De Spiritu Sancto", "std_ref": ["NPNF2, 7:318–328"], "pg": "PG 36"},
    ("nazianz", "spirit"):        {"full_title": "On the Holy Spirit", "latin_title": "De Spiritu Sancto", "std_ref": ["NPNF2, 7:318–328"], "pg": "PG 36"},
    ("nazianz", "orat"):          {"full_title": "Orations", "latin_title": "Orationes", "std_ref": ["NPNF2, 7"], "pg": "PG 35–36"},
    ("bernard", "ep"):            {"full_title": "Letters", "latin_title": "Epistulae", "std_ref": ["PL 182"]},
    ("irenaeus", "haer"):         {"full_title": "Against Heresies", "latin_title": "Adversus Haereses", "std_ref": ["ANF 1"], "pg": "PG 7"},
    ("livy", "hist"):             {"full_title": "History of Rome", "latin_title": "Ab Urbe Condita", "std_ref": ["Ab Urbe Condita"]},
    ("livy", "lib"):              {"full_title": "History of Rome", "latin_title": "Ab Urbe Condita", "std_ref": ["Ab Urbe Condita"]},
    ("themist", "orat"):          {"full_title": "Orations", "latin_title": "Orationes", "std_ref": ["Themistii Orationes"]},
    ("ammian", "hist"):           {"full_title": "Roman History", "latin_title": "Res Gestae", "std_ref": ["Loeb Class. Lib."]},
    ("lombard", "sent"):          {"full_title": "Sentences", "latin_title": "Sententiae", "pl": "PL 192"},
    ("prosper", "epist ad rufi"): {"full_title": "Letter to Rufinus", "latin_title": "Epistola ad Rufinum", "pl": "PL 51"},
    ("gregory_great", "moralia"): {"full_title": "Morals on the Book of Job", "latin_title": "Moralia in Job", "pl": "PL 75/76"},
    ("gregory_great", "moral"):   {"full_title": "Morals on the Book of Job", "latin_title": "Moralia in Job", "pl": "PL 75/76"},
    ("gregory_great", "epist"):   {"full_title": "Registrum Epistolarum (Letters)", "latin_title": "Registrum Epistolarum", "std_ref": ["NPNF2, 12–13"]},
    ("bede", "hist"):             {"full_title": "Ecclesiastical History of the English People", "latin_title": "Historia Ecclesiastica Gentis Anglorum"},
    ("andradius", "explic"):      {"full_title": "Orthodoxae Explicationes (Orthodox Explanations)", "latin_title": "Orthodoxarum Explicationum Libri Decem"},
    ("andradius", "defens"):      {"full_title": "Defense of the Council of Trent", "latin_title": "Defensio Tridentinae Fidei"},
    ("cochlaeus", "de author"):   {"full_title": "On the Authority of the Church and Scripture", "latin_title": "De Auctoritate Ecclesiae et Scripturae"},
    ("cochlaeus", "de authoritate"): {"full_title": "On the Authority of the Church and Scripture", "latin_title": "De Auctoritate Ecclesiae et Scripturae"},
    ("pighius", "hierarch"):      {"full_title": "Hierarchiae Ecclesiasticae Assertio (Defense of the Ecclesiastical Hierarchy)", "latin_title": "Hierarchiae Ecclesiasticae Assertio"},
    ("pighius", "ecclesiast"):    {"full_title": "Hierarchiae Ecclesiasticae Assertio (Defense of the Ecclesiastical Hierarchy)", "latin_title": "Hierarchiae Ecclesiasticae Assertio"},
    ("hosius", "de auth"):        {"full_title": "On the Authority of Scripture", "latin_title": "De Auctoritate Scripturae"},
    ("hosius", "de authoritat"):  {"full_title": "On the Authority of Scripture", "latin_title": "De Auctoritate Scripturae"},
    ("bradwardine", "de causa dei"): {"full_title": "On the Cause of God against Pelagius", "latin_title": "De Causa Dei contra Pelagium"},
    ("suarez", "de perpetuitat"): {"full_title": "On the Perpetuity or Loss of Grace", "latin_title": "De Perpetuitate vel Amissione Gratiae"},
    ("didymus", "de spir sanc"):  {"full_title": "On the Holy Spirit", "latin_title": "De Spiritu Sancto", "pl": "PL 39"},
    ("canus", "lee theol"):       {"full_title": "Loci Theologici", "latin_title": "Loci Theologici", "std_ref": ["Salamanca, 1563"]},
    ("damasc", "lib"):            {"full_title": "Exact Exposition of the Orthodox Faith", "latin_title": "De Fide Orthodoxa", "std_ref": ["NPNF2, 9"], "pg": "PG 94"},
}

# ── Detection regex ──────────────────────────────────────────────────────────
# Design constraints:
#   - MUST end with dot after abbreviation (prevents "Epistle" matching "Epist.")
#   - Single Roman-numeral letters (c, d, l, etc.) must not be followed by
#     non-Roman word chars (prevents "c" in "chap." matching as Roman 100)
#   - Digit numbers must not be followed by colon+digit (prevents "2:4" scripture)
#   - Abbreviation must not be preceded by a digit (prevents "41Epist." from OCR)

_ROMAN_MULTI = r'[IVXLCDMivxlcdm]{2,}'          # safe: 2+ Roman chars (lXXXvii, VII)
_ROMAN_SINGLE = r'[IVXLivxl](?![a-zA-Z])'       # single char not followed by letter
_ROMAN_NUM = rf'(?:{_ROMAN_MULTI}|{_ROMAN_SINGLE})'
_DIGIT_NUM = r'\d+(?!:\d)(?:[-–]\d+)?'           # digit not followed by colon+digit
_NUM_BASE = rf'(?:{_ROMAN_NUM}|{_DIGIT_NUM})'
_MULTI_NUM = rf'{_NUM_BASE}(?:\s*[,;]\s*{_NUM_BASE})*'

_STRONG_ABBREV = r'(?:lib|serm(?:o)?|epist|ep|orat|tract|homil|haer|dial|adv)'
_WEAK_ABBREV   = r'(?:cap|chap|sect|t(?:om)?|col|vol)'

# Full citation unit: strong abbreviation + dot + num(s) + optional weak-abbrev chain
# (?<!\d) prevents "41Epist." OCR artefacts from matching
PATRISTIC_CITATION_RE = re.compile(
    rf'(?<!\d)\b(?P<abbrev>{_STRONG_ABBREV})\.(?!\w)'
    rf'\s*(?:ad\s+\w+\.?\s*)?'
    rf'(?P<nums>{_MULTI_NUM})'
    rf'(?:\s*[:;,]?\s*(?:{_WEAK_ABBREV})\.(?!\w)\s*{_MULTI_NUM})*',
    re.I
)

# ── Author detection from preceding plain text ───────────────────────────────

# Strip HTML tags for context analysis
_TAG_RE = re.compile(r'<[^>]+>')

def _strip_tags(html: str) -> str:
    return _TAG_RE.sub('', html)


def _find_author_in_context(plain_context: str) -> str | None:
    """
    Look for a known author abbreviation in the 120-char plain-text window
    preceding the citation match. Returns the AUTHOR_ABBREV_MAP key, or None.
    """
    ctx_full = plain_context.lower()
    if 'idem' in ctx_full or 'the same' in ctx_full:
        if 'johan' in ctx_full:
            return 'august'
        if 'cardinal works' in ctx_full:
            return 'cyprian'

    # If the context contains a '|' separator (indicating before/after boundary),
    # only search the 'before' part for authors to avoid false positives.
    if ' | ' in plain_context:
        plain_context = plain_context.split(' | ')[0]

    # Normalize: lowercase
    ctx = plain_context.lower()
    # Find ALL author matches with their positions, then return the MOST RECENT
    # (rightmost in the context window) — this handles cases like
    # "…Augustine says…Calvin, Institut. lib. 2" where both are in context but
    # Calvin is the actual citing author for that reference.
    # The pattern allows the abbreviation to be followed by additional letters
    # (so "ambros" matches "ambrose", "ambrosian"; "tertull" matches "tertullian").
    best_pos = -1
    best_key = None
    for abbrev in sorted(AUTHOR_ABBREV_MAP, key=len, reverse=True):
        pattern = re.compile(rf'\b{re.escape(abbrev)}\w*\.?', re.I)
        for m in pattern.finditer(ctx):
            if m.start() > best_pos:
                best_pos = m.start()
                best_key = abbrev
    if best_key:
        best_key = CANONICAL_AUTHOR_MAP.get(best_key, best_key)
            
    return best_key


def _find_work_in_context(plain_context: str, author_key: str | None) -> dict | None:
    """
    After finding an author, look for a matching work in WORK_MAP by scanning
    the work-fragment section of the context for known work abbreviation fragments.

    Owen writes work abbreviations with internal periods: "Hist. Eccles.", "De Trin.",
    "Institut." — so we normalize dots away before matching against WORK_MAP keys.
    """
    if author_key is None:
        return None
    ctx_lower = plain_context.lower()
    # Normalize: strip internal abbreviation dots so "hist. eccles." → "hist eccles"
    ctx_norm = re.sub(r'\.+\s*', ' ', ctx_lower).strip()
    candidates = [(k, v) for k, v in WORK_MAP.items() if k[0] == author_key]
    candidates.sort(key=lambda x: len(x[0][1]), reverse=True)
    for (auth, work_frag), work_data in candidates:
        # Try both raw and normalized context
        if work_frag in ctx_lower or work_frag in ctx_norm:
            return work_data
    return None


def _expand_location_string(loc_text: str) -> str:
    """
    Expand 'lib. 2 cap. 3' → 'Book 2, Chapter 3'.
    Handles chains of abbreviation+number pairs.
    Uses strict Roman numeral matching (same as PATRISTIC_CITATION_RE) so that
    single-letter Roman chars like c/d/m don't generate false location expansions.
    """
    # Strict Roman: 2+ chars OR single I/V/X/L/i/v/x/l not followed by a letter
    _ROM = r'(?:[IVXLCDMivxlcdm]{2,}|[IVXLivxl](?![a-zA-Z]))'
    _DIG = r'\d+(?:[-–]\d+)?'
    _NUMPART = rf'(?:{_ROM}|{_DIG})'
    _NUMS = rf'{_NUMPART}(?:\s*[,;]\s*{_NUMPART})*'
    _loc_item_re = re.compile(
        rf'\b(lib|cap|chap|serm(?:o)?|epist|ep|orat|tract|homil|haer|dial|adv|'
        rf'sect|t(?:om)?|col|vol|qu|q|art|dist|part|p{{1,2}})'
        rf'\.(?!\w)\s*'
        rf'({_NUMS})',
        re.I
    )
    parts = []
    for m in _loc_item_re.finditer(loc_text):
        abbrev_raw = m.group(1).lower()
        abbrev_norm = re.sub(r'o$', '', abbrev_raw) if abbrev_raw == 'sermo' else abbrev_raw
        full_word = LOC_EXPAND.get(abbrev_norm, abbrev_raw.capitalize())
        nums = m.group(2).strip()
        parts.append(f"{full_word} {nums}")
    return ", ".join(parts) if parts else loc_text


def is_bible_citation_ref(matched_text: str, plain_context: str) -> bool:
    """Check if a matched citation looks like a Bible citation (e.g. 1 Epist. 2, 29)."""
    ctx_before = plain_context.split(' | ')[0] if ' | ' in plain_context else plain_context
    if re.search(r'\b[1-3]\s+$', ctx_before) and not re.search(r'\b(?:lib|cap|chap|vol|t|p|pp)\.?\s+[1-3]\s*$', ctx_before, re.I):
        return True
    return False


def build_citation_note(
    matched_text: str,
    plain_context: str,
    force_work_frag: str | None = None,
) -> str | None:
    """
    Build a Modern Citation footnote string for a matched citation.

    matched_text:    raw citation from the HTML (e.g. "lib. 2 cap. 3")
    plain_context:   plain text (HTML-stripped) before the match
    force_work_frag: when set, try WORK_MAP[(author, force_work_frag)] directly
                     before falling back to context scanning.

    Returns an HTML string, or None if the citation cannot be resolved to a
    specific work — caller should skip annotation rather than emit a vague note.
    A note without the work title (e.g. "Eusebius, Book 7, Chapter 29") is
    worse than silence: it creates the impression of scholarship while telling
    the reader nothing they cannot see for themselves.
    """
    # Skip Bible citations (e.g., "1 Epist. 2, 29", "2 Epist. 3") to avoid pointless footnotes
    if is_bible_citation_ref(matched_text, plain_context):
        return None

    author_key = _find_author_in_context(plain_context)
    work_data = None
    if force_work_frag and author_key:
        work_data = WORK_MAP.get((author_key, force_work_frag))
    if work_data is None:
        work_data = _find_work_in_context(plain_context, author_key)

    if work_data is None:
        # Unique work inference fallback (Issue 91 / unresolved citations resolution)
        # We strip dots and normalize spacing to avoid dot-matching failures
        ctx_to_check = (plain_context + " " + matched_text).lower()
        ctx_to_check = ctx_to_check.replace('.', '')
        ctx_to_check = re.sub(r'\s+', ' ', ctx_to_check)
        inferences = [
            (r'\brhet\w*\b', 'aristotle', 'rhet'),
            (r'\bde\s+orthod\w*\b', 'damasc', 'de fide'),
            (r'\bde\s+jes\w*\s+christ\w*\s+serv\w*\b', 'socin', 'de servat'),
            (r'\bde\s+servat\w*\b', 'socin', 'de servat'),
            (r'\bcomment\w*\s+ju[rt]\s+civil\b|\bconan\w*\b', 'conanus', 'comment'),
            (r'\binstit\w*\b', 'justinian', 'instit'),
            (r'\bquibus\s+modis\s+tollitur\s+obligatio\b', 'justinian', 'instit'),
            (r'\bdig\b|\bulpian\b|\bpaulus\b', 'justinian', 'digest'),
            (r'\bnatural\w*\s+quaest\w*\b', 'seneca', 'natural'),
            (r'\bep\w*\s+ad\s+niemojev\w*\b', 'socin', 'respon'),
            (r'\bpanarion\b|\bpanar\w*\b', 'epiphan', 'haer'),
            (r'\bde\s+relig\w*\b', 'volkelius', 'de vera'),
            (r'\bde\s+vera\s+relig\w*\b', 'volkelius', 'de vera'),
            (r'\bcon\w*\s+faust\w*\b', 'august', 'contra fau'),
            (r'\bde\s+bapt\w*\b', 'august', 'de bapt'),
            (r'\bde\s+arbit\w*\b|\bmenoch\w*\b', 'menochius', 'de arbit'),
            (r'\bde\s+coelest\w*\b|\bpighius\b', 'pighius', 'de coelest'),
            (r'\bcrit\w*\s+sacr\w*\b', 'cappel', 'critica'),
            (r'\bexercit\w*\b', 'morinus', 'exercit'),
            (r'\bcontra\s+apion\w*\b', 'josephus', 'contra apionem'),
            (r'\bisaac\b', 'isaac', 'ad lindan'),
            (r'\bmiscellan\w*\b', 'fuller', 'miscellan'),
            (r'\bcyrop\w*\b', 'xenophon', 'cyrop'),
            (r'\bre\s+binah\b', 'azarias', 're binah'),
            (r'\bthemist\w*\b', 'themist', 'orat'),
            (r'\bursicinus\b|\bsicinus\b|\bursinus\b', 'ammian', 'hist'),
            (r'\bsanct\w*\s+spir\w*\b', 'nazianz', 'spir'),
            (r'\bepist\w*\s+ad\s+evagrium\b|\bad\s+evagrium\b|\bevagrius\b', 'hieronym', 'epist'),
            (r'\brecapitulat\w*\b', 'irenaeus', 'haer'),
            (r'\borat\w*\b.*\b(greg|nazian)', 'nazianz', 'orat'),
            (r'\b(greg|nazian).*\borat\w*\b', 'nazianz', 'orat'),
            (r'\bde\s+verbo\s+dei\b', 'bellar', 'de verbo dei'),
            (r'\bex\s+mortuis\b|\bprior\s+omnium\b|\bmystagog\w*\b', 'irenaeus', 'haer'),
            (r'\b(?:adv(?:er)?|con(?:tra)?|ad)?\s*cels?\w*\b', 'origen', 'con cels'),
            (r'\banthropomorph\w*\b', 'theodoret', 'hist eccles'),
            (r'\brend\s+and\s+divide\s+the\s+glorious\s+body\b|\bmischief\s+of\s+schism\b', 'irenaeus', 'haer'),
            (r'\bconcio\w*\b', 'livy', 'hist'),
            (r'\blombard\b|\bsent\b|\bsen\s+d\b', 'lombard', 'sent'),
            (r'\b(?:congruere|hujus\s+viri)\b.*\bepist\w*\s+ad\s+rusti\b', 'prosper', 'epist ad rufi'),
            (r'\bmoral\w*\b', 'gregory_great', 'moralia'),
            (r'\b(?:bradwardin|causa\s+dei|de\s+cau\b|petri\s+navicula\s+dormiat|pervigil\s+laborabat)\b', 'bradwardine', 'de causa dei'),
            (r'\b(?:suarez|perpetuitat\w*|amissione|amis\b)\b', 'suarez', 'de perpetuitat'),
            (r'\bde\s+idol\b', 'tertull', 'de idol'),
            (r'\bgregory\b.*\bepist\b|\bepist\b.*\bgregory\b', 'gregory_great', 'epist'),
            (r'\bgregory\b.*\blib\s+\d+\b', 'gregory_great', 'epist'),
            (r'\bhosius\b.*\bde\s+auth\w*\b', 'hosius', 'de auth'),
            (r'\bantiq\w*\s+rom\b', 'dionysius', 'antiq'),
            (r'\bde\s+grat\w*\s+et\s+lib\w*\s+arbit\w*\b', 'bellar', 'de grat'),
            (r'\b(?:loc|loci|lee)\s+theol\w*\b', 'canus', 'loc theol'),
            (r'\b_?(?:holy\s+one|spirit\s+himself)_?\b.*\bde\s+spir\w*\s+sanc', 'didymus', 'de spir sanc'),
            (r'\bliv\b|\bliv\.', 'livy', 'hist'),
        ]
        for pattern, inferred_author, inferred_work in inferences:
            if re.search(pattern, ctx_to_check, re.I):
                author_key = inferred_author
                work_data = WORK_MAP.get((inferred_author, inferred_work))
                if work_data:
                    break

    if work_data is None and author_key:
        # Fallback: try WORK_MAP[(author, cite_abbrev)] — covers cases where
        # the work is implied by the citation type itself, e.g.
        # "CYPRIAN, Epist. 62" → ("cyprian", "epist") → Letters (Epistulae).
        # The cite_abbrev is extracted from the matched_text.
        abbrev_m = re.match(r'^\(?\s*([a-z]+)\.', matched_text.lower())
        if abbrev_m:
            cite_abbrev = abbrev_m.group(1).rstrip('o')  # sermo → serm
            work_data = WORK_MAP.get((author_key, cite_abbrev))

    if work_data is None:
        # Cannot identify the specific work → return None so the caller stays silent
        return None

    expanded_loc = _expand_location_string(matched_text)
    author_full = AUTHOR_ABBREV_MAP.get(author_key, author_key.capitalize())
    title_html = (
        f"<i>{work_data['full_title']}</i>"
        + (f" ({work_data['latin_title']})" if work_data.get('latin_title') else "")
    )
    refs = []
    if work_data.get('std_ref'):
        refs.extend(work_data['std_ref'])
    if work_data.get('pl'):
        refs.append(work_data['pl'])
    if work_data.get('pg'):
        refs.append(work_data['pg'])
    ref_str = f" [{'; '.join(refs)}]" if refs else ""
    note_str = f"<b>Modern Citation:</b> {author_full}, {title_html}, {expanded_loc}{ref_str}."
    if work_data.get('notes'):
        note_str += f" <i>{work_data['notes']}</i>"
    return note_str


# ── Self-reference detection ─────────────────────────────────────────────────

# Patterns indicating Owen is citing his own earlier/later text, not a patristic source.
# When these words appear within 80 chars before a citation, skip annotation.
SELF_REF_PATTERNS = re.compile(
    r'\b(?:my\s+(?:treatise|discourse|book|volume|work)|'
    r'as\s+(?:I\s+have|i\s+have)|'
    r'I\s+have\s+(?:shown|proved|demonstrated|discussed|treated)|'
    r'already\s+(?:shown|discussed|proved)|'
    r'in\s+(?:that|the)\s+treatise|'
    r'of\s+(?:that|this)\s+treatise|'
    r'confuted)\b|'
    r'\betc\.,?\s*(?:\||$)',
    re.I
)

# ── HTML-level expansion pass ────────────────────────────────────────────────

# Detects a footnote sup already attached to a citation (already resolved)
_ALREADY_ANNOTATED_RE = re.compile(
    r'(?:lib|serm(?:o)?|epist|ep|orat|tract|homil|haer|dial|adv)\.'
    r'[^<]{0,40}<sup',
    re.I
)

# Minimum number of chars in the citation string to annotate (avoids "lib. I" noise)
_MIN_CITE_LEN = 6

# Parenthetical standalone chapter reference: "(cap. 2:)" or "(chap. 4.)"
# Owen uses this form when citing individual chapters of a patristic work named
# in the surrounding sentence — e.g. "(cap. 2:)" after naming Ephraim Syrus.
# Kept SEPARATE from PATRISTIC_CITATION_RE to avoid inflating _bt_covered
# (cap. appears heavily in BODY_TRANSLATIONS long-phrase keys).
PAREN_CHAPTER_RE = re.compile(
    r'\(\s*(?P<abbrev>cap|chap)\.(?!\w)\s*(?P<nums>\d+(?:[,;]\s*\d+)*)\s*:?\s*\)',
    re.I
)


def expand_inline_citations(
    html: str,
    cid: str,
    trans_notes: list,
    trans_counter: int,
) -> tuple[str, list, int]:
    """
    Find every un-annotated patristic citation in *html* and add an inline
    footnote reference plus an entry in *trans_notes*.

    Returns (updated_html, updated_trans_notes, updated_trans_counter).
    Called once per chapter, AFTER _apply_translations() so that citations
    already resolved by BODY_TRANSLATIONS are not double-annotated.
    """
    from html import escape as _esc

    # Collect all matches with their positions, processing in reverse order
    # so that string insertions don't shift earlier positions.
    from scripts.translation_db import BODY_TRANSLATIONS as _bt

    # Pre-compute which citation strings are already "owned" by BODY_TRANSLATIONS.
    # _apply_translations() resolved LONGER phrases that CONTAIN these citation
    # strings as substrings; the text still appears in the HTML (with <sup> at the
    # end of the full phrase), so our regex would find it again. We must skip those.
    _bt_covered: set[str] = set()
    for _phrase in _bt:
        for _bm in PATRISTIC_CITATION_RE.finditer(_phrase):
            _norm = re.sub(r'\s+', ' ', _bm.group(0).strip().lower())
            _bt_covered.add(_norm)

    # Pattern: our own translation immediately after a citation
    _OUR_SUP_RE = re.compile(r'<a[^>]*class="noteref noteref-trans"', re.I)

    matches = []
    for m in PATRISTIC_CITATION_RE.finditer(html):
        cite_str = m.group(0)
        # Skip very short hits — likely false positives
        if len(cite_str.strip()) < _MIN_CITE_LEN:
            continue
        # Skip if this citation text is already handled inside a BODY_TRANSLATIONS
        # phrase (those longer phrases have already been annotated by pass 1)
        cite_norm = re.sub(r'\s+', ' ', cite_str.strip().lower())
        if cite_norm in _bt_covered:
            continue
        # Skip if immediately followed by our own <sup> (already annotated)
        tail = html[m.end():m.end() + 30]
        if _OUR_SUP_RE.search(tail):
            continue
        # Verify this match is in text, not inside an HTML tag:
        # check that the match doesn't contain '<' or '>'
        if '<' in cite_str or '>' in cite_str:
            continue
        # Extract ~150 chars of plain-text context before and 100 chars after the match
        ctx_start = max(0, m.start() - 150)
        ctx_end = min(len(html), m.end() + 100)
        plain_ctx_before = _strip_tags(html[ctx_start:m.start()])
        plain_ctx_after = _strip_tags(html[m.end():ctx_end])
        plain_ctx = plain_ctx_before + " | " + plain_ctx_after
        # Skip self-references (Owen citing his own work)
        if SELF_REF_PATTERNS.search(plain_ctx_before):
            continue
        matches.append((m.start(), m.end(), cite_str, plain_ctx))

    # Process in reverse to preserve string positions
    for start, end, cite_str, plain_ctx in reversed(matches):
        note_body = build_citation_note(cite_str, plain_ctx)
        # Skip if the specific work could not be identified — a vague note
        # ("Eusebius, Book 7, Chapter 29") is worse than no note at all.
        if note_body is None:
            continue
        trans_counter += 1
        fn_id = f"fntrans_{cid}_{trans_counter}"
        fn_link = (
            f'<sup><a class="noteref noteref-trans" epub:type="noteref" '
            f'role="doc-noteref" href="endnotes.xhtml#{fn_id}">*</a></sup>'
        )
        # Scan forward past any trailing punctuation to place footnote after it (Rule 11)
        actual_end = end
        while actual_end < len(html) and html[actual_end] in ',.:;?!"\'”’ ':
            actual_end += 1
        trans_notes.append({
            'id': fn_id,
            'num': trans_counter,
            'phrase': _esc(cite_str),
            'translation': note_body,
            'type': 'citation',
        })
        html = html[:actual_end] + fn_link + html[actual_end:]

    # ── Pass B: parenthetical standalone chapter refs "(cap. N)" ────────────
    # Collected separately so they are NOT subject to the _bt_covered filter
    # (cap. appears frequently inside long BODY_TRANSLATIONS keys, which would
    # otherwise block every standalone chapter reference).
    paren_matches = []
    for m in PAREN_CHAPTER_RE.finditer(html):
        # Skip if already annotated (sup within 30 chars after the closing paren)
        tail = html[m.end():m.end() + 30]
        if _OUR_SUP_RE.search(tail):
            continue
        if '<' in m.group(0) or '>' in m.group(0):
            continue
        # Use a wider context window (300 chars) because the author name is often
        # named at the start of the sentence, which can be > 150 chars earlier.
        ctx_start = max(0, m.start() - 300)
        plain_ctx = _strip_tags(html[ctx_start:m.start()])
        if SELF_REF_PATTERNS.search(plain_ctx):
            continue
        paren_matches.append((m.start(), m.end(), m.group(0), plain_ctx))

    for start, end, cite_str, plain_ctx in reversed(paren_matches):
        note_body = build_citation_note(cite_str, plain_ctx, force_work_frag="cap")
        if note_body is None:
            continue
        trans_counter += 1
        fn_id = f"fntrans_{cid}_{trans_counter}"
        fn_link = (
            f'<sup><a class="noteref noteref-trans" epub:type="noteref" '
            f'role="doc-noteref" href="endnotes.xhtml#{fn_id}">*</a></sup>'
        )
        # Scan forward past any trailing punctuation to place footnote after it (Rule 11)
        actual_end = end
        while actual_end < len(html) and html[actual_end] in ',.:;?!"\'”’ ':
            actual_end += 1
        trans_notes.append({
            'id': fn_id,
            'num': trans_counter,
            'phrase': _esc(cite_str),
            'translation': note_body,
            'type': 'citation',
        })
        html = html[:actual_end] + fn_link + html[actual_end:]

    return html, trans_notes, trans_counter
