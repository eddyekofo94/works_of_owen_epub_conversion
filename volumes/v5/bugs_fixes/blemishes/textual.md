# Imptant
fix bugs, now I don't want partial fixes, I want thorough revisiting of algorithms/regex and audits why are these bugs here and how can they be
fixed or rewritten that these bugs are not leaking on other volumes also.


## 1
d the same, Bellar., lib 5 cap.† l;
Fix:
d the same, Bellar., lib 5 cap.† 1;
Note: do we not have audits that check for these blemishes? This is a clear case of a misread "1" as "l", and the audit should be able to catch this.

## 2
. So Albertus Pighius‡‡
Fix:
. So Albertus Pighius‡.
Note: Why is the footnote symbol displayed as "‡‡" instead of "‡"? This is a clear case of a misread footnote symbol, and the audit should be able to catch this.

## 3
“<span lang="la" xml:lang="la">Tu hinc o rosea martyrum turba offer pro me nunc et in hora mortis mee, merita, fidelitatum, constantiae, et pretiosi sanguinis, cum sanguine agni immaculati, pro omnium salute effusi.†</span>" Jerome,‡ long before Anselm, spake to the same purpose: "<span lang="la" xml:lang="la">Cum dies judicii aut dormitionis advenerit, omnes manus dissolventur; quibus dicitur in alio loco, confortamini manus dissolutae; dissolventur autem manus, quia nullum opus dignum Dei justitia reperiatur, et non justificabitur in conspectu ejus omnis vivens, unde propheta dicit in psalmo, 'Si iniquitates attends Domine, quis sustinebit'†</span>", lib. 6 in”
"<span lang="la" xml:lang="la">Christus omnia mundi peccata in se recepit, tantumque pro illis ultro sibi assumpsis dolerem cordis, ac si ipse ea perpetrasset;†</span>"
"<span lang="la" xml:lang="la">Itaque non quia utrumque Scripture dicat, propterea haec inter se non pugnare concludendum est; sed potius quia haec inter se pugnant, ideo alterutrum a Scriptura non dici statuendum est†</span>",
Fix:
Why is the Latin text not rendered properly? This is a clear case of a rendering issue, and the audit should be able to catch this.

## 4
"O the depth of the riches both of the wisdom and knowledge of God! How unsearchable are his judgments, and his ways past finding Romans 11:33-36
Fix:
"O the depth of the riches both of the wisdom and knowledge of God! How unsearchable are his judgments, and his ways past finding out!" Romans 11:33-36
Note: Missing closing quotation mark and the word "out" at the end of the verse. This is a clear case of a formatting issue, and the audit should be able to catch this.
