import re

with open("scratch/chunk_1.txt", "r") as f:
    text = f.read()

def get_match(prefix):
    for line in text.split('\n'):
        if prefix in line:
            return line[line.find(prefix):]
    return prefix # fallback

items = [
    ("Epist. 57 ad Dardan.", "Jerome, <i>Epistulae</i>, 57 (ad Dardanum)."),
    ("lib. 7. epist. 63.", "Cyprian, <i>Epistulae</i>, 63."),
    ("Alcuinus, Amatorius, Rabanus, Lib. P. P. tom. 10", "Alcuin, Amalarius, Rabanus, in <i>Bibliotheca Patrum</i>, vol. 10."),
    ("Origen, Homil. 11. in Hierimes:", "Origen, <i>Homiliae in Jeremiam</i>, 11:"),
    ("Apol., cap.  30.", "Tertullian, <i>Apologeticus</i>, 30."),
    ("again, cap. 39:", "Tertullian, <i>Apologeticus</i>, 39:"),
    ("Socrates on this matter, lib. 5 cap. 21.", "Socrates Scholasticus, <i>Historia Ecclesiastica</i>, 5.21."),
    ("lib. 3 cap. 29.", "Eusebius, <i>Historia Ecclesiastica</i>, 3.29."),
    ("in 1 ad Timoth. cap. 5.", "Ambrose (Ambrosiaster), <i>In Epistolam ad Timotheum primam</i>, 5."),
    ("Eusebius lib. 4 cap. 15.", "Eusebius, <i>Historia Ecclesiastica</i>, 4.15."),
    ("Eusebius, lib. 4 cap. 22.", "Eusebius, <i>Historia Ecclesiastica</i>, 4.22."),
    ("Eusebius, lib. 4 cap. 26.", "Eusebius, <i>Historia Ecclesiastica</i>, 4.26."),
    ("Hist., lib. 7 cap. 19.", "Eusebius, <i>Historia Ecclesiastica</i>, 7.19."),
    ("Eusebius, lib. 5 cap. 23.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.23."),
    ("lib. 3 cap. 3.", "Irenaeus, <i>Adversus Haereses</i>, 3.3."),
    ("Eccles. Hist., lib. 3 cap. 16.", "Eusebius, <i>Historia Ecclesiastica</i>, 3.16."),
    ("lib. 5 cap. 7.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.7."),
    ("Eusebius Ecclesiast. Hist., lib. 4 cap. 23.", "Eusebius, <i>Historia Ecclesiastica</i>, 4.23."),
    ("Epist. ad Magnes. [cap. 7]", "Ignatius, <i>Epistula ad Magnesios</i>, 7."),
    ("Philadelphians [cap. 2]: Οπου ὁ ποιμήν ἐστιν ἐκεῖ ὡς πρόβατα ἀκολουθεῖ", "Ignatius, <i>Epistula ad Philadelphenses</i>, 2: \"Οπου ὁ ποιμήν ἐστιν ἐκεῖ ὡς πρόβατα ἀκολουθεῖτε\"."),
    ("[cap.4]: Θαῤῥῶν γράφω τῂ ἀξιοθέῳ ἀγάπῃ ὑμῶν παρακαλῶν ὑ", "Ignatius, <i>Epistula ad Philadelphenses</i>, 8: \"Θαῤῥῶν γράφω τῂ ἀξιοθέῳ ἀγάπῃ ὑμῶν παρακαλῶν ὑμᾶς μηδὲν κατ' ἐρίθειαν πράσσειν\"."),
    ("[cap. 10]: Πρέπον ἐστὶν ὑμῖν ὡς ἐκκλησίᾳ Θεοῦ χειροτονῆ", "Ignatius, <i>Epistula ad Philadelphenses</i>, 10: \"Πρέπον ἐστὶν ὑμῖν ὡς ἐκκλησίᾳ Θεοῦ χειροτονῆσαι διάκονον\"."),
    ("[cap. 5]: Εἰ γὰρ ἑνὸς καὶ δευτέρου προσευχὴ τοσαύτην ἱσ", "Ignatius, <i>Epistula ad Ephesios</i>, 5: \"Εἰ γὰρ ἑνὸς καὶ δευτέρου προσευχὴ τοσαύτην ἱσχὺν ἔχει\"."),
    ("[cap. 13]: Σπουδάζετε οῦν πυκνότερον συνέρχεσθαι ὅταν γ", "Ignatius, <i>Epistula ad Ephesios</i>, 13: \"Σπουδάζετε οῦν πυκνότερον συνέρχεσθαι ὅταν γὰρ\"."),
    ("Eusebius, Hist., lib. 5 cap. 1.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.1."),
    ("cap. 4.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.4."),
    ("Eusebius himself, cap. 8", "Eusebius, <i>Historia Ecclesiastica</i>, 5.8"),
    ("Justin Martyr, Apol. ad Genesis cap. 39.", "Tertullian, <i>Apologeticus</i>, 39."),
    ("Hist. Eccl., lib. 5 cap. 14.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.14."),
    ("lib. 7 cap. 27, 28, 29.", "Eusebius, <i>Historia Ecclesiastica</i>, 7.27-29."),
    ("Euseb., lib. 4 cap. 22;", "Eusebius, <i>Historia Ecclesiastica</i>, 4.22;"),
    ("Tertul ad Valentine, cap. 4;", "Tertullian, <i>Adversus Valentinianos</i>, 4;"),
    ("Epiphan. Haeres.  42.", "Epiphanius, <i>Panarion</i>, 42."),
    ("Euseb., lib. 6 cap. 43", "Eusebius, <i>Historia Ecclesiastica</i>, 6.43"),
    ("Lactantius, lib. 4 cap. 30:", "Lactantius, <i>Divinae Institutiones</i>, 4.30:"),
    ("Epist. 113", "Theodoret, <i>Epistulae</i>, 113"),
    ("Sozomen declares, lib. 6 cap. 20.", "Sozomen, <i>Historia Ecclesiastica</i>, 6.20."),
    ("Euseb., lib. 6 cap. 33.", "Eusebius, <i>Historia Ecclesiastica</i>, 6.33."),
    ("Clem. Pedag., lib. 3 cap.  12.", "Clement of Alexandria, <i>Paedagogus</i>, 3.12."),
    ("Clem. Epist. ad Cor. pp. 2-4;", "Clement of Rome, <i>Epistula I ad Corinthios</i>, 2-4;"),
    ("Justin Mart. Apol. 2;", "Justin Martyr, <i>Apologia Secunda</i>;"),
    ("Tertullian in his Algol, and lib. 2 ad Uxor. e", "Tertullian, <i>Apologeticus</i>, and <i>Ad Uxorem</i> 2, and <i>De Cultu Feminarum</i>;"),
    ("Cyprian, Epist. 2 et 12;", "Cyprian, <i>Epistulae</i>, 2 and 12;"),
    ("Euseb. Hist. lib. 9, cap. 8;", "Eusebius, <i>Historia Ecclesiastica</i>, 9.8;"),
    ("Athanas. Epist. ad Solit.,", "Athanasius, <i>Historia Arianorum ad Monachos</i>,"),
    ("et Epiphan. lib. 3 t. 2, sect. 24;", "Epiphanius, <i>Panarion</i>, 3.2.24;"),
    ("Eusebius, lib. 5 cap. 21-23;", "Eusebius, <i>Historia Ecclesiastica</i>, 5.21-23;"),
    ("Socrates on this occasion, lib. 5 cap. 21,", "Socrates Scholasticus, <i>Historia Ecclesiastica</i>, 5.21,"),
    ("Euseb., lib. 6 cap. 43;", "Eusebius, <i>Historia Ecclesiastica</i>, 6.43;"),
    ("Cyprian, Epist. 51, ad Antonianum.", "Cyprian, <i>Epistulae</i>, 51 (ad Antonianum)."),
    ("Cyprian ad Jubaianum, Epist. 71,", "Cyprian, <i>Epistulae</i>, 71 (ad Jubaianum),"),
    ("Euseb., lib. 7 cap. 8.", "Eusebius, <i>Historia Ecclesiastica</i>, 7.8."),
    ("Euseb. lib. 7 cap. 8,", "Eusebius, <i>Historia Ecclesiastica</i>, 7.8,"),
    ("Epist. 51.", "Cyprian, <i>Epistulae</i>, 51."),
    ("Socrat., lib. 1 cap. 7", "Socrates Scholasticus, <i>Historia Ecclesiastica</i>, 1.7"),
    ("lib. 3 cap. 6.", "Theodoret, <i>Historia Ecclesiastica</i>, 3.6."),
    ("Theod. Hist., lib. 1 cap. 8;", "Theodoret, <i>Historia Ecclesiastica</i>, 1.8;"),
    ("lib. 4 cap. 10.", "Socrates Scholasticus, <i>Historia Ecclesiastica</i>, 4.10."),
    ("Socrat. Hist., lib. 2 cap. 3.", "Socrates Scholasticus, <i>Historia Ecclesiastica</i>, 2.3."),
    ("lib. 4 cap. 62.", "Augustine, <i>De Haeresibus</i>, 62."),
    ("Euseb., lib. 7 cap. 22.", "Eusebius, <i>Historia Ecclesiastica</i>, 7.22."),
    ("Euseb. lib. 4 cap.  15.", "Eusebius, <i>Historia Ecclesiastica</i>, 4.15."),
    ("Euseb. lib. 5 cap. 1.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.1."),
    ("Clemens, Stromat. lib. 7,", "Clement of Alexandria, <i>Stromata</i>, 7,"),
    ("Augustin. Lib. de Ovib. cap. 15,", "Augustine, <i>De Ovibus</i>, 15,"),
    ("lib. 3 Con. Cel, cap. 1;", "Origen, <i>Contra Celsum</i>, 3.1;"),
    ("Beda, lib. 2 cap. 2.", "Bede, <i>Historia Ecclesiastica</i>, 2.2."),
    ("August. de Civit. Dei, lib. 28 cap. ult.", "Augustine, <i>De Civitate Dei</i>, 22.ult."),
    ("Euseb. Eccleas. Hist., lib. 5 cap. 22-25.", "Eusebius, <i>Historia Ecclesiastica</i>, 5.22-25."),
    ("Tertullian, Apol. cap. 23.", "Tertullian, <i>Apologeticus</i>, 23."),
    ("council of Sardis, Epist. ad Alexaud.,", "Council of Sardica, <i>Epistula ad Alexandrinos</i>,"),
    ("council at Toledo, cap. de Judae. distinct, 45:", "Council of Toledo, <i>De Judaeis</i>, dist. 45:"),
    ("Ambrose declare himself to have done, Epist. 27;", "Ambrose, <i>Epistulae</i>, 27;"),
    ("Epist. ad Cornel.", "Cyprian, <i>Epistulae</i>, ad Cornelium."),
    ("ozomen tells you expressly that he did so, lib. 4 cap. 15;", "Sozomen, <i>Historia Ecclesiastica</i>, 4.15;"),
    ("Athanasius, Epist. ad Solitarios,", "Athanasius, <i>Historia Arianorum ad Monachos</i>,"),
    ("Cyprian condemns it, Epist. ad Demetriad.", "Cyprian, <i>Ad Demetrianum</i>."),
    ("Epist. ad Johan. Hierosol.", "Jerome, <i>Epistula ad Johannem Hierosolymitanum</i>."),
    ("Lib. de Morib. Ecclea Cathol. cap. 34.", "Augustine, <i>De Moribus Ecclesiae Catholicae</i>, 34.")
]

d = {}
for prefix, trans in items:
    match = get_match(prefix)
    d[match] = f"<b>Modern Citation:</b> {trans}"

with open("scratch/chunk_1_dict.py", "w") as f:
    f.write("CHUNK_DICT = {\n")
    for k, v in d.items():
        f.write(f'    {repr(k)}: {repr(v)},\n')
    f.write("}\n")
print("Done writing scratch/chunk_1_dict.py")
