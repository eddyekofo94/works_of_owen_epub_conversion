# Whitelist Trace & Audit Report: Volume 14

This report tracks and validates every whitelist entry to prevent greedy silencing of real anomalies.

## Summary

* **Total Whitelisted Entries:** 105
* **Clean/Exact Matches (1 issue silenced):** 91
* **Greedy Entries (silences multiple issues):** 14
* **Unused Entries (silences 0 issues - safe to remove):** 0

### ⚠️ Greedy Whitelist Entries
These entries are too broad and matched multiple distinct anomalies. Consider making them more specific.

| Whitelist Path / Entry | Match Count |
|-------------------------|-------------|
| `anomalies -> Hyphenation Anomalies -> 'Syro-Chaldean'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'V. ... VII.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '4.'` | 9 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 4.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '4. ... 11.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '9. ... 754.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '6. ... 794.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'II. ... XII.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '1. ... 5.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '1. ... 4.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'III.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'II.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '4. ... 490.'` | 2 |
| `text_integrity -> paragraph_splits -> READER,` | 2 |

---

## Detailed Trace by Category

### 1. Anomalies Whitelist

#### Category: `OCR & Bracket Residues`

##### Entry: `te est` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21 - Pope.* — `Split word anomaly (rejoins to 'teest')`
      * Context: `... s saepe in se transmovet, qui habet salem, Qui in **te est**." [Ter. Eun. 3:1, 10.] All the glory and renown ...`

##### Entry: `hum et` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7.* — `Split word anomaly (rejoins to 'humet')`
      * Context: `... e scirem an verum diceret? quod si et hoc scirem, **hum et** ab illo scirem? Intus utique mihi, intus in domic ...`

##### Entry: `e contrario` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 19.* — `Split word anomaly (isolated letter 'e')`
      * Context: `... nt, nequit in ipsa consecratione consistere, quin **e contrario** consecratio ad rationem sacramenti potius quam ad ...`

##### Entry: `P. L` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `Stray lowercase 'l' following citation abbreviation 'P' (likely typo for '1' or 'i')`
      * Context: `... uoted, who hath placed them as on a pillar, U. D. **P. L**. P.,' — "Where they may be easily read by all me ...`


#### Category: `Hyphenation Anomalies`

##### Entry: `law-maker` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 5 - Obscurity of God, Etc.* — `Splittable word (rejoins to valid word 'lawmaker')`
      * Context: `... know of. He proceeds: — 4. "If Christ be not our **law-maker** and director of doing well, as well as our Redeem ...`
      * Context: `... ts or Presbyterians teach that "Christ is not our **law-maker** and director of doing well," etc.? I dare say he ...`

##### Entry: `open-hearted` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7 - Use of Reason.* — `Splittable word (rejoins to valid word 'openhearted')`
      * Context: `... men into a good humor, and, knowing them free and **open-hearted**, he plies them whilst they are warm. We have ind ...`

##### Entry: `a-work` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 9 - Protestant Pleas.* — `Splittable word (rejoins to valid word 'awork')`
      * Context: `... efense against the Presbyterians. He that set him **a-work** may pay him his wages. Protestants only tell him ...`

##### Entry: `Ro-manists` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 13 - Popish Contradictions.* — `Capitalized hyphenation with unrecognized right particle`
      * Context: `... that no trouble ever was raised amongst us by the **Ro-manists**, here, at unawares, he informs us that his own gr ...`

##### Entry: `top-gallant` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 13 - Popish Contradictions.* — `Splittable word (rejoins to valid word 'topgallant')`
      * Context: `... uiet life; another, that they carry their top and **top-gallant** so high, that they will go to heaven without Chri ...`

##### Entry: `Syro-Chaldean` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 17 - Latin Service.* — `Capitalized hyphenation with unrecognized left particle`
      * Context: `... eir people, who began to take in a mixture of the **Syro-Chaldean** language with their own, the Targums were found ...`
    * **Chapter:** *Chapter 22.* — `Capitalized hyphenation with unrecognized left particle`
      * Context: `... their own tongue, and most of them understood the **Syro-Chaldean**, wherein about that time some small parts of the ...`
      * Context: `... soon as their language began to be mixed with the **Syro-Chaldean**, and the purity of it to grow into disuse, made u ...`

##### Entry: `far-fetched` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 18 - Communion.* — `Splittable word (rejoins to valid word 'farfetched')`
      * Context: `... it doth seem plainly to do; for, setting aside a **far-fetched** false notion or two about Melchizedek, and the do ...`

##### Entry: `bed-staff` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 18 - Communion.* — `Splittable word (rejoins to valid word 'bedstaff')`
      * Context: `... let such things as these down our throats, but a **bed-staff**, to cram them down, or they will choke us in the ...`

##### Entry: `non-necessity` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 18 - Communion.* — `Splittable word (rejoins to valid word 'nonnecessity')`
      * Context: `... emises, to erect his triumphant conclusion of the **non-necessity** of participation of the blessed cup by the people ...`

##### Entry: `Peace-making` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21 - Pope.* — `Splittable word (rejoins to valid word 'Peacemaking')`
      * Context: `... e series of men going under that name. Instead of **Peace-making** and reconciliation, they tell us of fierce and cr ...`

##### Entry: `after-game` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21 - Pope.* — `Splittable word (rejoins to valid word 'aftergame')`
      * Context: `... desired, though they were many of them wise at an **after-game**, and turned their remoteness from them into their ...`

##### Entry: `Christian-like` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1.* — `Splittable word (rejoins to valid word 'Christianlike')`
      * Context: `... l submit; and, therefore, that it is rational and **Christian-like** to leave these endless contentions, and resign ou ...`

##### Entry: `fore-named` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7.* — `Splittable word (rejoins to valid word 'forenamed')`
      * Context: `... stionable. You may at your leisure, besides those **fore-named**, consult Psalm 19:8; Isaiah 8:20; Ezekiel 36:27; ...`

##### Entry: `wire-draw` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8.* — `Splittable word (rejoins to valid word 'wiredraw')`
      * Context: `... and it brings no small gains unto you. Hence you **wire-draw** his cathedral infallibility, legislative authorit ...`

##### Entry: `Vice-Deus` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8.* — `Capitalized hyphenation with unrecognized right particle`
      * Context: `... e Vicar of Christ, Head and Spouse of his Church, **Vice-Deus**, Deus alter in Terris," and the like, whereby you ...`

##### Entry: `un-acquaintedness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 11.* — `Splittable word (rejoins to valid word 'unacquaintedness')`
      * Context: `... larly your assertions and inferences, or, through **un-acquaintedness** with the stories of some things that you referred ...`

##### Entry: `un-impeached` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Splittable word (rejoins to valid word 'unimpeached')`
      * Context: `... lst the formal reason of faith remains absolutely **un-impeached**, different apprehensions about particular things ...`

##### Entry: `hard-hearted` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Splittable word (rejoins to valid word 'hardhearted')`
      * Context: `... len into somewhat an unhappy age, wherein men are **hard-hearted**, and will not give away their faith and reason to ...`

##### Entry: `over-confident` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 13.* — `Splittable word (rejoins to valid word 'overconfident')`
      * Context: `... that you back your request with nothing but some **over-confident** asseverations, subscribed with "Teste meipso," I ...`

##### Entry: `pre-eminences` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 17.* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... of your pope, with the authority, privileges, and **pre-eminences** which by virtue thereof he lays claim unto, but h ...`

##### Entry: `hear-say` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21.* — `Splittable word (rejoins to valid word 'hearsay')`
      * Context: `... es they talked of, so that they had them all upon **hear-say**. Acts 4:1 4. Αλλὰ, saith he, μήτις εἴτῃ τίνος ἕν ...`

##### Entry: `not-withstanding` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21.* — `Splittable word (rejoins to valid word 'notwithstanding')`
      * Context: `... olten statue," Judges 18:Would it not, think you, **not-withstanding** the gaiety of all this provision, have been a mad ...`

##### Entry: `high-handed` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note (Chapter 3 - Motive, Matter, and Method of Our Authorìs Book.)* — `Splittable word (rejoins to valid word 'highhanded')`
      * Context: `... rch, and more especially with the abettors of the **high-handed** measures adopted by the Court for discountenancin ...`

##### Entry: `statesman-like` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note (Chapter 3 - Motive, Matter, and Method of Our Authorìs Book.)* — `Splittable word (rejoins to valid word 'statesmanlike')`
      * Context: `... e calm and nervous dignity of its reasonings; the **statesman-like** view it gives of the condition and prospects of t ...`

##### Entry: `birth-right` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The State and Fate of the Protestant Religion.* — `Splittable word (rejoins to valid word 'birthright')`
      * Context: `... ountries, did secure unto them as a part of their **birth-right** inheritance. And in some places, though the name ...`

##### Entry: `re-introduction` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The State and Fate of the Protestant Religion.* — `Splittable word (rejoins to valid word 'reintroduction')`
      * Context: `... s inducements, may comply with any of them in the **re-introduction** of Popery into any of their territories, will qui ...`


#### Category: `Structural Nesting Sequence Jumps`

##### Entry: `V. ... VII.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 8.* — `List sequence jump (skipped from 5 to 7)`
    * **Chapter:** *Chapter 17.* — `List sequence starts at 2 instead of 1`
      * Context: `... as did one at Rome, under Otho the emperor, John X**II.**, a sweet bishop, anno 963; another at Sutrinum, a ...`
      * Context: `... ainst the usurpations and innovations of Gregory V**II.**, as at Worms, Papia, Brixia, Mentz, and elsewhere ...`
      * Context: `... is with their pope's now claimed authority. Henry **II.** of Germany both deposed popes and limited their p ...`

##### Entry: `3. ... 5.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3 - Motive, Matter, and Method of Our AuthorÌs Book.* — `List sequence jump (skipped from 3 to 5)`

##### Entry: `41.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 2.* — `List sequence starts at 41 instead of 1`
      * Context: `... hurch explained by Suarez, tom. 1 in Thom. 3, d. **41.** "A supernatural work," saith he, "proceeding from ...`

##### Entry: `4.` (⚠️ Greedy)
  * Silenced 9 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 2 to 4)`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 4 to 11)`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 9 to 754)`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 6 to 794)`
    * **Chapter:** *Chapter 13.* — `List sequence jump (skipped from 2 to 4)`
    * **Chapter:** *Chapter 16.* — `List sequence jump (skipped from 1 to 4)`
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 4 to 490)`
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 2 to 4)`

##### Entry: `2. ... 4.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 2 to 4)`
    * **Chapter:** *Chapter 13.* — `List sequence jump (skipped from 2 to 4)`
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 2 to 4)`

##### Entry: `3. ... 6.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 3 to 6)`

##### Entry: `6. ... 381.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 6 to 381)`

##### Entry: `4. ... 11.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 4 to 11)`

##### Entry: `5. ... 7.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 5 to 7)`

##### Entry: `7. ... 9.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 7 to 9)`

##### Entry: `9. ... 754.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 9 to 754)`

##### Entry: `6. ... 794.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 6 to 794)`

##### Entry: `II. ... XII.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 2 to 12)`
    * **Chapter:** *Chapter 17.* — `List sequence starts at 2 instead of 1`
      * Context: `... as did one at Rome, under Otho the emperor, John X**II.**, a sweet bishop, anno 963; another at Sutrinum, a ...`
      * Context: `... ainst the usurpations and innovations of Gregory V**II.**, as at Worms, Papia, Brixia, Mentz, and elsewhere ...`
      * Context: `... is with their pope's now claimed authority. Henry **II.** of Germany both deposed popes and limited their p ...`

##### Entry: `1. ... 3.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8.* — `List sequence jump (skipped from 1 to 3)`

##### Entry: `1. ... 5.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 12.* — `List sequence jump (skipped from 1 to 5)`
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 1 to 5)`

##### Entry: `5. ... 9.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 13.* — `List sequence jump (skipped from 5 to 9)`

##### Entry: `1. ... 4.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 16.* — `List sequence jump (skipped from 1 to 4)`

##### Entry: `III.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 16.* — `List sequence starts at 3 instead of 1`
      * Context: `... 9? and whether Queen Elizabeth, King James, Henry **III.** and IV. of France, had cause to believe it? and w ...`
    * **Chapter:** *Chapter 17.* — `List sequence starts at 2 instead of 1`
      * Context: `... as did one at Rome, under Otho the emperor, John X**II.**, a sweet bishop, anno 963; another at Sutrinum, a ...`
      * Context: `... ainst the usurpations and innovations of Gregory V**II.**, as at Worms, Papia, Brixia, Mentz, and elsewhere ...`
      * Context: `... is with their pope's now claimed authority. Henry **II.** of Germany both deposed popes and limited their p ...`

##### Entry: `II.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence jump (skipped from 2 to 12)`
    * **Chapter:** *Chapter 8.* — `List sequence jump (skipped from 5 to 7)`
    * **Chapter:** *Chapter 16.* — `List sequence starts at 3 instead of 1`
      * Context: `... 9? and whether Queen Elizabeth, King James, Henry **III.** and IV. of France, had cause to believe it? and w ...`
    * **Chapter:** *Chapter 17.* — `List sequence starts at 2 instead of 1`
      * Context: `... as did one at Rome, under Otho the emperor, John X**II.**, a sweet bishop, anno 963; another at Sutrinum, a ...`
      * Context: `... ainst the usurpations and innovations of Gregory V**II.**, as at Worms, Papia, Brixia, Mentz, and elsewhere ...`
      * Context: `... is with their pope's now claimed authority. Henry **II.** of Germany both deposed popes and limited their p ...`

##### Entry: `4. ... 490.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 4.* — `List sequence starts at 4 instead of 1`
      * Context: `[[CHAPTER]] CHAPTER **4.** [[SUMMARY]] Farther vindication of second chapte ...`
      * Context: `... ermines which is the heaviest, 22ae q. 94, a. ad **4.** The church in the wilderness fell by its μοσχοποι ...`
      * Context: `... ocate only him in whom we do believe," Romans 10:1**4.** It believed that the "command to abstain from me ...`
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 4 to 490)`

##### Entry: `2. ... 19.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21.* — `List sequence jump (skipped from 2 to 19)`


#### Category: `Unmatched Quotation Marks`

##### Entry: `**VIII.** "The Scripture, upon sundry accounts, is insufficient to settle us in the truth of religion, or to bring us to an agreement amongst ourselves; seeing it is, —` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**VIII. "The Scripture, upon sundry accounts, is insufficient to settle us in the truth of religion, or to bring us to an ...**`

##### Entry: `**3.** Is in itself obscure; and, **4.** We have none to determine of the sense of it."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**3. Is in itself obscure; and, 4. We have none to determine of the sense of it."**`

##### Entry: `**VIII.** "That the Scripture, on sundry accounts, is insufficient to settle us in the truth of religion, or to bring us to an agreement amongst ourselves; and that, —` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**VIII. "That the Scripture, on sundry accounts, is insufficient to settle us in the truth of religion, or to bring us to ...**`

##### Entry: `**4.** We have no way to determine of what is its proper sense."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 2 - Heathen Pleas - General Principles.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**4. We have no way to determine of what is its proper sense."**`

##### Entry: `Other things mentioned by him are ambiguous; as, "If the seven sacraments be deemed vain, most of them," etc. Of the things themselves, which they term "sacraments," there is scarce any of them by Protestants esteemed vain; that one of Unction, which they judge now useless, they only say is an unwarrantable imitation of that which was useful. Of the rest which they reject, not the things, but those things from being sacraments; and a practice in religion is not presently condemned as vain which is not esteemed a sacrament, There is no less ambiguity in that other supposition, "If the real body of our Lord be not bequeathed to his spouse in his last will and testament; which no Protestant ever questioned, though there be great contests about the manner of the mental participation of that real body. The same may be said of some other of his supposals. But I need not go over them in particular; I shall only say in general, that take from amongst them what is acknowledged to be the doctrine of the Papists, and as such is opposed by the church of England or by Presbyterians (as papal supremacy, sacrifice of the mass, monasteries of votaries under special and peculiar vows and rules, necessity of auricular confession, transubstantiation, which are the things gilded over by our author), and prove that they were the doctrines, all or any of them, whereby and wherewith the first preachers of Christianity in this nation, or any where else in the old known world, displaced Paganism, and, for my part, I will immediately become his proselyte. What, then, can be bound with this rope of sand? — "The first preachers of Christianity preached the pope's supremacy, the mass, etc.; by these doctrines Paganism was displaced: if these doctrines now be decried as lies, why may not Christ himself be esteemed a romance?" — for neither did the first preachers of Christianity preach these doctrines, nor was Paganism displaced by them: nor is there any ground to question the authority and truth of Christ, in case those that do first preach him do therewithal preach somewhat that is not true, when they bring along with them an authentic conviction of their own mistakes, as was manifested before, and might be made good by innumerable other instances.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 5 - Obscurity of God, Etc.* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**Other things mentioned by him are ambiguous; as, "If the seven sacraments be deemed vain, most of them," etc. Of the thi...**`

##### Entry: `[[BLOCKQUOTE]] "In any age of the Christian church a Jew might say thus to the Christians then living, 'Your Lord and Master was born a Jew, and under the jurisdiction of the high priests; these he opposed, and taught a religion contrary to Moses (otherwise how comes there to be a faction?) But how could he justly do it? no human power is of force against God's, who spake (as you also grant) by Moses and the prophets; and divine power it could not be, for God is not contrary to himself. And although your Lord might say, as indeed he did, that Moses spake of him as of a prophet to come, greater than himself, yet who shall judge that such a thing was meant of his person? For since that prophet is neither specified by his name nor characteristical properties' (well said, Jew), 'who could say it was he more than any other to come? And if there were a greater to` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Jews' Objections.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] "In any age of the Christian church a Jew might say thus to the Christians then living, 'Your Lord and Ma...**`

##### Entry: `come than Moses were, surely born a Jew, he would, being come into the world, rather exalt that law to more ample glory than diminish it. And if you will farther contest that such a prophet was to abrogate the first law and bring in a new one, who shall judge in this case? — the whole church of the Hebrews, who never dreamed of any such thing? or one member thereof who was born a subject to their judgments?' This," saith he, "is the great oecumenical difficulty; and he that in any age of Christianity could either answer it, or find any bulwark to set against it, so that it should do no harm, would easily either salve or prevent all other difficulties," etc.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Jews' Objections.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**come than Moses were, surely born a Jew, he would, being come into the world, rather exalt that law to more ample glory ...**`

##### Entry: `But our author, foreseeing that even those with whom he intends chiefly to deal might possibly remember that St Paul had long ago stated this case in 1 Corinthians 14, he finds it necessary to cast a blind before them, — that if they will but fix their eyes upon it, and not be at the pains to turn to their Bibles, as it may be some will not, he may escape that sword which he knows is in the way ready drawn against him; — and therefore tells us that "if any yet will be obstinate,'' (and which, afar so many good words spent in this business, he seems to marvel that they should,) "and object what the apostle there writes against praying and prophesying in an unknown tongue," he hath three answers in readiness for him, whereof the first is that doughty one last mentioned, — namely, "That the prayers which the apostle, when he was at Corinth, requested of the Romans for him, were to be in an nnknown tongue to them that lived in Corinth;" when the only question is, whether they were in an unknown tongue to them that lived in Rome, who were desired to join in those supplications? Surely this argument, — that because we may pray for a man when and where he knows not, and in a tongue which he understands not, that therefore the worship of a church, all assembled together in one place, all to join together in it unto the edification of that whole society, may be performed in a language unknown to them so assembled, — is not of such cogency as so suddenly to be called over again. Wherefore, letting that pass, he tells us the design of the apostle in that place is "to prevent the abuse of spiritual gifts, which in those days men had received, and especially that of tongues; which he lets them know was liable to greater inconveniences than the rest there mentioned by him." But what, I pray, if this be the design of the apostle, doth it follow that in the pursuit of this design he teaches nothing concerning the use of an unknown tongue in the worship of God? Could I promise myself that every reader did either retain in his memory what is there delivered by the apostle, or would be at the pains on this occasion to read over the chapter, I should have no need to add one word in this case more; for what are the words of a poor weak man to those of the Holy Ghost speaking directly to the same purpose?` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 17 - Latin Service.* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**But our author, foreseeing that even those with whom he intends chiefly to deal might possibly remember that St Paul had...**`

##### Entry: `Things of this nature are always done soon enough when they are done well enough, or as well as they are capable of berg done. But it is no small disappointment to find ἄνθρακας ἀντὶ τοῦ ζησαυροῦ, a fruitless flourish of words, where a serious debate of an impotent cause was expected and looked for. Nor is it a justification of any man, when he has done a thing amiss, to say he did it speedily, if he were no way necessitated so to do. You are engaged in a cause, unto whose tolerable defense, "opus est Zephyis et hirundine multa," Hor. Ep. 7:13: though you cannot pretend so short a time to be used in it which will not by many be esteemed more than it deserves; for all time and pains taken to give countenance to error is undoubtedly misspent. Οὐ δυνάμεθά τι κατὰ τῆς ἀληθείας, ἀλλ ὑπὲρ τῆς ἀληθείας, saith the great apostle [ 2 Corinthians 13:8]; — "We can do nothing against the truth, but for the truth: which role had you obeyed, you might have spared your whole time and labor in this business. However, I shall be glad to find that you have given me just cause to believe what you say, of your not seeing the "Animadversions" on your book before February. As I find you observant of truth in your progress, or falling therein, so shall I judge of your veracity in this unlikely story; for every man gives the best measure of himself. And though I cannot see how possibly a man could spend much time in trussing up such a fardel of trifles and quibbles as your epistle is, yet it is somewhat strange, on the other side, that you should not in eight months' space — for so long were the "Animadversions" made public before February — set eye on that which, being your own especial concernment, was, to my knowledge, in the hands of many of your party. To deal friendly with you, "Nolim caeterarum rerum to socordem eodem modo." Yea, I doubt not but you use more diligence in your other affairs; though in general the matter in debate between us seems to be your principal concernment. But now you have seen that discourse, and, as you inform me, "have read it over;" which I believe, and take not only upon the same score of present trust, but upon the evidence also which you give unto your assertion, by your careful avoiding to take any farther notice of the things that you found too difficult for you to reply unto. For any impartial reader, that shall seriously consider the "Animadversions" with your epistle, will quickly find that the main artifice wherein you confide is a pretense of saying somewhat in general, whilst you pass over the things of most importance, and which most press the cause you defend, with a perpetual silence: these you turn from, and fall upon the person of the author of the "Animadversions." If ever you debated this procedure with yourself, had I been present with you when you said with him in the poet, "Dubius sum quid faciam — Tene relinquam an rem?" I should have replied with him, "Me sodes;" but you were otherwise minded, and are gone before, — _—— "Ego (ut contendere durum est_ _Cure victore) sequar." Hor. Sat. 1:9, 42._ I will follow you with what patience I can, and make the best use I am able of what offers itself in your discourse.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1.* — `Paragraph has unmatched double quotes (count: 19)`
      * Context: `**Things of this nature are always done soon enough when they are done well enough, or as well as they are capable of berg...**`

##### Entry: `Bellarmine seems to place it in "Creaturam aeque colere ac Deum;" — "To worship the creature as much or equally with the Creator:" which description of it, though it be vain and groundless (for his "aeque" is neither in the Scripture nor any approved author of old required to the constituting of the worship of any creature idolatrous), yet is not this heresy neither, but that which differs from it "toto genere." We know it to be "Cultus religiosus creaturae exhibitus,' — "Any religious worship of that which by nature is not God;" and so doth your Thomas grant it to be. Gregory de Valentia, another of your great champions, contends that "tanquam Deo," "as unto God," is to be added unto the definition; as though religious worship could be given unto any thing, and not as unto God really and indeed, though not intentionally as to the worshipper. Where a man gives religious worship, there he doth, "ipso facto," assign a divine eminency, say he what he will to the contrary. Neither will his intention of not doing it "as unto God," any more free him from idolatry than an adulteress will be free by not looking on her adulterer as her husband. I confess he adds afterward a distinction that is of great use for you, and indispensably he-cessary for your defense, De Idol., lib. 2, cap.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `Paragraph has unmatched double quotes (count: 19)`
      * Context: `**Bellarmine seems to place it in "Creaturam aeque colere ac Deum;" — "To worship the creature as much or equally with the...**`

##### Entry: `7. St Peter, he tells us, insinuates some "worship of idols, — "cultum aliquem simulachrorun," — to wit, that of the holy images, to be right or lawful, when he deterreth believers "ab illicitis idolorum cultibus," — "from the unlawful worship of idols," 1 Peter 4:3: Αθεμίτοις εἰδωλολατρείαις. This were somewhat, indeed, if all epithets were distinguishing, none aggravating or declarative. When Virgil said, "Dulcia mella premes," Geor. 4, he did not insinuate that there was any bitter honey. Nor is it allowable only for poets, to use explaining and declaring epithets; but Aristotle allows it in the best orators also, so they use not μακροῖς ἥ ἀκαίροις ἧ πυκνοῖς, "long or unseasonable ones," or the same frequently: and the use of this here by Peter is free from all those vices. When the Roman orator cried out, "O scelus detestandum!" — "O wickedness to be abhorred!" he did not intend to insinuate that there was a wickedness not to be abhorred, or to be approved. But if it will follow hence that your church is guilty only of lawful idolatry, I shall not much contend about it; yet I must tell you, that as the poor woman, when the physicians in her sickness told her still that what she complained of was a good sign, cried out, Οἴμοι ὐπ ἀγαθῶν ἀπόλλυμι, — "Good signs have undone me," — your lawful idolatry, if you take not better heed, will undo you. In the meantime, as to the coincidence you imagine between idolatry and heresy, I wish you would advise with your "angelical doctor," who will show you how they are contradistinct evils; which he therefore weighs in his scales, and determines which is the heaviest, 22ae q. 94, a. ad` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `Paragraph has unmatched double quotes (count: 19)`
      * Context: `**7. St Peter, he tells us, insinuates some "worship of idols, — "cultum aliquem simulachrorun," — to wit, that of the hol...**`

##### Entry: `The great and famous council of Chalcedon, anno 451, condemned the same heresy, and plainly overthrew the whole foundation of your papal plea, act 15, can. 18, as the canons of that council are collected by Balsamon and Zonaras; though some of them, with intolerable partiality, would separate this and some others from the body of the canons of that council, giving them a place by themselves. The decree contains the reasons of the council's assigning privileges next unto, and equally with, the Roman, unto the Oonstantinopolitan church: Τῷ ζρόνῳ, say they, τῆς πρεσζυτέρας Ρώμης, διὰ τὸ βασιλέυειν τὴν πόλιν ἐκείνην, οἱ πατέρες εἰκότως ἀποδεδώκασι τὰ πρεσζεῖα? — The fathers" (our predecessors) "granted privileges to the see of ancient Rome, because that was the imperial city." Do you see from whence proceeded all the privileges of the Roman throne? — merely from the grants and concessions of former bishops; and I wish they had been liberal only of what was their own. And what was the reason of their so doing? Because the city was "imperial:" in which one sentence, beth their supremacy and the grounds of it are discarded and virtually condemned; for their pretensions are utterly inconsistent with this synodical determination. They proceed: For the same reason, Τὰ ῖσα πρεσζεῖα ἀπένειμαν τῷ τῆς νέας Ρώμης ἁγιωτάτῳ ζρόνῳ, εὐλόγως κρίναντες τὴν βασιλείᾳ καὶ συγκλήτῳ τιμηθεῖσαν πόλιν, καὶ τῶν ἴσων ἀπολαύουσαν πρεσζείων τῇ πρεσζυτέρᾳ βασιλίδι Ρώμῃ, καὶ ἐν τοῖς ἐκκλησιαστικοῖς́? — "They" (the hundred and fifty bishops) "assigned the same or equal privileges unto the holy see of new Rome; rightly determining that the city which is honored with the empire and senate should enjoy equal privileges in things ecclesiastical with the ancient queen-Rome," [f25] or Rome-regent of old. Is not your present supremacy here sufficiently condemned, and that by as famous a council as ever the Christian world enjoyed? And it will not avail you that you fell into this heresy fully afterward, and not before the determination of this council: for he that falls into a heresy after the determination of a council is no less condemned therein than he that fell into it before, and gave occasion to the sentence; yea, his guilt is the greater of the two, because he despised the sentence which he knew, which the other, it may be, neither did nor could foresee. I gave you an instance before how it is condemned and written against by the British church here in this island, and many more instances of the same nature might be added. The Hildebrandine branch of your supremacy, — I mean the power that you challenge over kings and potentates, "in online ad spiritualia," — which, having made some progress by insensible degrees, was enthroned by Pope Gregory VII., hath as little escaped opposition, censure, and condemnation, as any heresy whereinto your church is fallen This Gregory may be accounted the chief father of this heresy; for he licked the unshapen monster into that terrible form wherein it hath since ranged about on the earth. What this man's principles and practices were, I shall not desire you to learn of Cardinal Benno, whom yet I have reason to judge the more impartial writer of the two, but of Cardinal Baronius, who makes it his business to extol him to the skies: "Facit eum apud nos deum, virtutes narrat," — "He makes almost a god of him;" or at least ζεῖον ἄνδρα, as Socrates tells us the Lacedemonians called an excellent man, Plato in Menn. The chief kingdoms of Europe, as England and Spain, with Sicilia and Sardinia, and sundry other principalities, he claimed as his own unquestionable fee. The empire he accounted his proper care, making the deposing of emperors much of his business. The principles he proceeded upon, the same cardinal informs us of in his Annals, ad an. 1076, n.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `Paragraph has unmatched double quotes (count: 15)`
      * Context: `**The great and famous council of Chalcedon, anno 451, condemned the same heresy, and plainly overthrew the whole foundati...**`

##### Entry: `Yea, and it is a kindness if he kick not their crowns from their heads with his foot, as one did our King John's; or tread upon their necks, as another did on the Emperor Frederic's."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**Yea, and it is a kindness if he kick not their crowns from their heads with his foot, as one did our King John's; or tre...**`

##### Entry: `YOU proceed unto the fourth assertion gathered out of your "Fiat," which you thus lay down: "'It is,' say you, 'frequently pleaded by our author that all things, as to religion, were ever quiet and in peace before the Protestants' relinquishment of the Roman see.' That 'ever' is your own addition, but let it pass; what say you hereunto? This principle you pretend is drawn out of 'Fiat Lux,' not because it is there, but only to open a door to yourself to expatiate into some wide general discourse about the many wars, distractions, altercations, that have been aforetime up and down in the world, in some several ages of Christianity. And you therefore say, it is frequently pleaded by me, because indeed I never spake one word of it, and it is in truth a false and fond assertion; though neither you nor I can deny that such as keep unity of faith with the church can never, so long as they hold it, fall out upon that account." Sir, I take you to be the author of "Fiat Lux;" and if you are so, I cannot but think you were asleep when you talked at this rate. "The assertion is false and fond; you speak not one word of it!" Pray, sir, take a little advice of your son, "Fiat," not to talk on this manner; and you will wonder yourself how you came to swallow so much confidence as in the face of the world to vent such things as these. He tells us from you, pp. 234-236, chap. 4, second edition, that "After the conversion of this land by the children of blessed St Bene't, notwithstanding the interposition of the Norman conquest, that all men lived peaceably together, without any the least disturbance upon the account of religion, until the end of King Henry VIII.'s reign, about five hundred years after the conquest." See also what in general you discourse of all places to this purpose, pp. 221, 222. And, p. 227, you do in express terms lay down the position which here you so exclaim against as "false and fond;" but you may make as bold with it as you please, for it is your own. "Never had this land," say you, "for so many hundred years as it was Catholic, upon the account of religion any disturbance at all; whereas, after the exile of the Catholic belief in our land, from the period of King Henry VIII.'s reign to these days, we have been in actual disquiet, or at least in fears." "Estne haec tunica filii tui?" Are not these your words? Doth not your son "Fiat" wear this livery? And do you not speak to this purpose in twenty other places? Is it not one of the main suppositions you proceed upon in your whole discourse? You do well now, indeed, to acknowledge that what you spake was "fond and false," and you might do as much for the most that you have written in that whole discourse; but now openly to deny what you have asserted, and that in so many places, that is not so well done of yore. There are, sir, many ways to free yourself from that damage you feel or fear from the "Animadversions." When any thing is charged on you or proved against you which you are not able to defend, you may ingenuously acknowledge your mistake, and that without any dishonor to you at all: good men have done so; so may you or I when we have just occasion. It is none of your tenets that you are all of you infallible, or that your personal mistakes or miscarriages will prejudice your cause. Or you might pass it by in silence, as you have done with the things of the most importance in the "Animadversions;" and so keep up your reputation that you could reply to them if you would, or were free from flies. And we know Πολλοῖς ἀπόκρισις ἡ σιωπὴ τυγχάνει, as Menander speak; — "Silence is with many the best answer." Or you might attempt to disprove or answer, as the case requires. But this that you have fixed upon, of denying your own words, is the very worst course that you could have chosen, upon the account either of conscience or reputation. However, thus much we have obtained, — one of the chief pretenses of your "Fiat" is, by your own confession, "false and fond." It is indeed no wonder that it should be so; it was fully proved to be so in the "Animadversions: but that you should acknowledge it to be so is somewhat strange; and it would have been very welcome news had you plainly owned your conviction of it, and not renounced your own offspring. But I see you have a mind to the benefit you aimed at by it, though you are ashamed of the way you used for the obtaining of it; and therefore add, "That neither you nor I can deny that such as keep the unity of faith with that church can never, so long as they hold it, fall out on that account." But this, on the fhrst consideration, seems to me no very singular privilege; methinks a Turk, a Jew, an Arian, may say the same of their societies: it being no more but this, — "So long as you agree with us, you shall be sure to agree with us!" They must be very unfriendly minded towards you that will call these κυρίας δόξας into question. Yet there remains still one scruple on my mind in reference unto what you assert. I am not satisfied that there is in your church any such unity of faith as can keep men from falling out or differing in and about the doctrines and opinions they profess If there be, the children of your church are marvellous morose, that they have not all this while learned to be quiet, but are at this very day writing volumes against one another, [f29] and procuring the books of one another to be prohibited and condemned; which the writings of one of the most learned of you in this nation have lately not escaped. I know you will say sometimes, that though you differ, yet you differ not in things belonging unto the unity of faith. But I fear this is but a blind, an apron of fig-leaves. What you cannot agree in, be it of never so great importance, you will agree to say that it belongs not unto the unity of faith; when things no way to be compared in weight and use with them, so you agree about them, shall be asserted so to do. Andin what you differ, whilst the scales of interest on the part of the combatants hang even, all your differences are but in school and disputable points; — but if one party prevail in interest and reputation, and render their antagonists inconsiderable as to any outward trouble, those very points that before were disputable shall be made necessary, and to belong to the unity of faith; as it lately happened in the case of the Jansenists. And here you are safe again: the unity of the faith is that which you agree in; and that which you cannot agree about belongs not unto it, as you tell us, though you talk at another rate among yourselves But we must think that the unity of faith is bounded by the confines of your wranglements, and your agreement is the rule of it. This, it may be, you think suits your turn: but whether it be so well suited unto the interest of the gospel and of truth, you must give men leave to inquire, or they will do it "ingratiis," whether you will or no. But if by the unity of faith you intend the substantial doctrines of the gospel proposed in the Scripture to be believed on necessity unto salvation, it is unquestionably among all the churches in the world, and might possibly be brought forth into some tolerable communion in profession and practice, did not your schismatical interest and principles interpose themselves to the contrary. [f29] The fifth supposition in your "Fiat," observed in the "Animadversions," is, "That the first reformers were most of them contemptible persons, their means indirect, and their ends sinister;" to which you reply, "Where is it, sir, where is it, that I meddle with any men's persons, or say they are contemptible? What and how many are those persons? and where did they live? But this you add of your own is in a vast universal notion, to the end you may bring in the apostles and prophets, and some kings, into the list of persons by me surnamed 'contemptible,' and liken my speech, who never spake any such thing, to the sarcasms of Celsus, Lucian, Porphyry, Julian, and other Pagans." So you begin; but "ne saevi, magne Sacerdos!" Have a little patience, and I will direct you to the places where you display in many words that which in a few I represented. They are in your "Fiat," chap. 4, sect. 18, second edition, from p. 239, unto sect. 20, p. 251. Had you lost your "Fiat," that you make such an outcry after that which in a moment he could have supplied you withal? "Calvin, and a tailor's widow, — Luther and Catharine Bore, — pleased with a naked unicorn, — swarms of reformers as thick as grasshoppers, fallen priests and votaries, — ambitious heads, emulating one another, — if not the worst, yet none of the best that ever were, — so eagerly quarrelling among themselves, that a sober man would not have patience to hear their sermons or read their books;" with much more to the same purpose, you will find in the places which I have now directed you unto. But I see you love to say what you please, but not to hear of it again. But he that can, in no more words, more truly express the full and genuine sense of your 18th and 19th chapters than I have done, in the assertion you so cry out against, shall have my thanks for his pains; only, I must mind you that you have perverted it, in placing the last words as if they referred unto the reformers you talk of, that they did their work for "sinister ends," when I only said that "their doctrine, according to your insinuations, was received for sinister ends;" wherein I comprised your foul reflections upon King Henry VIII., and Queen Elizabeth his daughter, — not placing them, as you now feign, among the number of them whom I affirmed to be reported by you as a company of contemptible persons. But now, upon a confidence that you have shifted your hands of a necessity to reinforce this assertion, which you find, it may be, in yourself an incompetency for, you reflect back upon some former passages in the "Animadversions," wherein the general objections that you lay against Protestancy are observed to be the same for substance that long ago were by Celsus objected unto Christianity, and say, "So likewise, in the very beginning of this your second chapter, you spend four leaves in a parallel betwixt me and the pagan Celsus; whereof there is not any member of it true. 'Doth Fiat Lux,' say you, 'lay the cause of all the troubles, disorders, tumults, wars, within the nations of Europe, upon Protestants? doth he charge the Protestants, that by their schisms and seditions they make a way for other revolts? doth he gather a rhapsody of insignificant words? doth he insist upon their divisions? doth he manage the arguments of the Jews against Christ, etc.? — so doth Celsus, who is confuted by Origen.' Where does 'Fiat Lux,' where does, does he, does he any such thing? Are you not ashamed to talk at this rate? I give a hint, indeed, of the divisions that be amongst us, and the frequent argumentations that are made to embroil and puzzle one another, with our much evil, and little appearance of any good in order unto unity and peace; which is the end of my discourse. But must I therefore be Celsus? Did Celsus any such thing to such an end? It is the end that moralizeth, and specifies the action. To diminish Christianity, by upbraiding our frailties, is paganish; to exhort to unity, by representing the inconvenience of faction, is a Christian and pious work. When honest Proestants in the pulpit speak ten times more full and vehemently against the divisions, wars, and contentions that be amongst us, than ever came into my thoughts, must they therefore every one of them be a Celsus, a pagan Celsus? What stuff is this? But it is not only my defamation you aim at; your own glory comes in the rear. If I be Celsus, the pagan Celsus, you then, forsooth, must be Origen that wrote against him, honest Origen; that is the thing. Pray, sir, — it is but a word, — let me advise you, by the way, that you do not forget yourself in your heat, and give your wife occasion to fall out with you. However you may, yet will not your wife like it perhaps so well that her husband should be Origen." Such trash as this must he consider who is forced to have to do with you. These, it seems, are the meditations you are conversant with in your retirements. What little regard you have in them unto truth or honesty shall quickly be discovered unto yore` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 5.* — `Paragraph has unmatched double quotes (count: 65)`
      * Context: `**YOU proceed unto the fourth assertion gathered out of your "Fiat," which you thus lay down: "'It is,' say you, 'frequent...**`

##### Entry: `This is that we say, — the Scripture, the Old and New Testament, is the principle of our faith. This is proved by itself to be of the Lord, who is its author; and if we cause it to depend on any thing else, it is no longer the principle of our faith and profession. And a little after, where he hath showed that a principle ought not to be disputed, nor to be the τὸ κρινόμενον of any debate, he adds, Εικότως τοίνυν πίστει περιλαζόντες ἀναπόδεικτον τὴν ἀρχὴν, ἐκ περιουσίας καὶ τὰς ἀποδείξεις παρ αὐτῆς τῆς ἀρχῆς λαζόντες, φωνῇ Κυρίου παιδευόμεθα πρὸς τὴν ἐπίγνωσιν τῆς ἀληθείας — "It is meet, then, that receiving by faith the most absolute principle without other demonstration, and taking demonstrations [f32]` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**This is that we say, — the Scripture, the Old and New Testament, is the principle of our faith. This is proved by itself...**`

##### Entry: `[[BLOCKQUOTE]] of the principle from the principle itself, we be instructed by the voice of the Lord unto the knowledge of the truth;"` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] of the principle from the principle itself, we be instructed by the voice of the Lord unto the knowledge ...**`

##### Entry: `I have given you sundry instances already, undeniably evincing that some opinions of them who first bring the news of Christian religion unto any may be afterward rejected, without the least impeachment of the _truth_ of the whole or of our faith therein; yea, men may be necessitated so to reject them, to keep entire the truth of the whole. But the rejection supposed is of _men's_ opinions that bring Christian religion, and not of any parts of Christian religion itself; for the _mistakes_ of any men whatever, whether in speculation or practice about religion, are no parts of religion, much less substantial parts of it. Such was the opinion of the necessity of the observation of Mosaical rites, taught, with a suitable practice, by many believers of the Circumcision, who first preached the gospel in sundry places in the world; and such were the rites and opinions brought into England by Austin that are rejected by Protestants, — if any such there were, which as yet you have not made to appear. There is no such affinity between truth and error, however any men may endeavor to blend them together, but that others may separate between them, and reject the one without any prejudice unto the other: "Male sarta Gratia nequicquam coit,' Hor. Ep. 1:3,31. Yea, the truth and light of the gospel is of that nature, as that, if it be once sincerely received in the mind and embraced, it will work out all those false notions which by any means together with it may be instilled, as "rectum" is "index sui et obliqui." Whilst, then, we know and are persuaded that in any system of religion which is proposed unto us it is only error which we reject, having an infallible rule for the guidance of our judgment therein, there is no danger of weakening our assent unto the truth which we retain. Truth and falsehood can never stand upon the same bottom, nor have the same evidence, though they may be proposed at the same time unto us, and by the same persons; so that there is no difficulty in apprehending how the one may be received and the other rejected. Nor may it be granted (though your concernment lie not therein at all), that if a man reject or disbelieve any point of truth that is delivered unto him in an entire system of truths, that he is thereby made inclinable to reject the rest also, or disenabled to give a firm assent unto them; unless he reject or disbelieve it upon a notion that is common to them all. For instance, he that rejects any truth revealed in the Scripture on this ground, that the Scripture is not an infallible revelation of divine and supernatural truth, cannot but, in the pursuit of that apprehension of his, reject also all other truths therein revealed, at least so far as they are knowable only by that revelation; but he that shall disbelieve any truth revealed in the Scripture, because it is not manifest unto him to be so revealed, and is in a readiness to receive it when it shall be so manifest, upon the authority of the author of the whole, is not in the least danger to be induced by that disbelief to question any thing of that which he is convinced so to be revealed. But, as I said, your concernment lies not therein, who are not able to prove that Protestants have rejected any one part, much less "substantial part" of religion; and your conclusion, upon a supposition of the rejection of errors and practices of the contrary to the gospel or principles of religion, is very infirm. The ground of all your sophistry lies in this, that men who receive Christian religion are bound to resolve their faith into the authority of them that preach it first unto them; whereupon, it being impossible for them to question any thing they teach without an impeachment of their absolute infallibility, and so far the authority which they are to rest upon, they have no firm foundation left for their assent unto the things which as yet they do not question; and consequently, in process of time, may easily be induced so to do. But this presumption is perfectly destructive to all the certainty of Christian religion; for whereas it proposeth the subject-matter of it to be believed with divine faith and supernatural, it leaves no formal reason or cause of any such faith, no foundation for it to be built upon, or principle to be resolved into: for how can divine faith arise out of human authority? For acts being specificated by their objects, such as is the authority on which a man believes, such is his faith; — human, if that be human; divine, if it be divine. But resolving, as we ought, all our faith into the authority of God revealing things to be believed, and knowing that revelation to be entirely contained in the Scriptures, by which we are to examine and try whatever is, by any man or men, proposed unto us as an object of our faith, — they proposing it only upon this consideration, that it is a part of that which is revealed by God in the Scripture for us to believe, without which they have no ground nor warrant to propose any thing at all unto us in that kind, — we may reject any of their proposals which we find and discern not to be so revealed, or not to be agreeable to what is so revealed, without the least weakening of our assent unto what is revealed indeed, or making way for any man so to do. For whilst the formal reason of faith remains absolutely un-impeached, different apprehensions about particular things to be believed have no efficacy to weaken faith itself; as we shall farther see in the examination of your ensuing discourse: —` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**I have given you sundry instances already, undeniably evincing that some opinions of them who first bring the news of Ch...**`

##### Entry: `Here, first, you deny that these principles are popish; but, sir, there are some Jews, even at this day, who will deny any such man as Pontius Pilate to have ever been in Jewry. I have other things to do than to fill volumes with useless texts, which here I might easily do out of the books both of the first reformers, and Catholic divines and councils." What acquaintance you have with the Jews we have in part seen already, and shall have occasion hereafter to examine a little farther. In the meantime, you may be pleased to take notice that men who know what they say are not easily affrighted from it by a show of such mormoes, as he in the comedian was from his own house by his servant's pretense that it was haunted by sprites, when there were none in it but his own debauched companions. I denied those opinions to be popish, and should do so still, were I accused for so doing before a Roman judge as corrupt and wicked as Pontius Pilate; for I can prove them to be more ancient than any part of Popery, in the sense explained in the "Animadversions," and admitted generally by Protestants. We never esteem every thing popish that Papists hold or believe. Some things in your profession belong unto your _Christianity;_ some things to your _Popery._ And I am persuaded you do not think this proposition, "Jesus Christ is the Son of God," to be heretical, because those whom you account heretics do profess and believe it. Prove the principles you mention to be invented by yourselves, without any foundation in the Scripture or constant suffrage of the ancient churches, and you prove them to be popish, to be your own. If you cannot do so, though Papists profess them, yet they may be Christian. This is spoken as to the principles themselves, not unto your explanation of them, which in sundry particulars is popish, which was never owned by prelate Protestants. You proceed: "You challenge me to prove that these principles were ever denied by our prelate Protestants; and this you do wittily and like yourself. You therefore bid me prove that those principles were ever denied by our prelate Protestants, because I say that our prelate Protestants here in England, as soon as they became such, took up again those forenamed principles, which Protestants, their forefathers, beth here in England and beyond seas, before our prelacy was set up, had still rejected. When I say, then, that our prelate Protestants affirmed and asserted those principles which former Protestants denied, you bid me prove that our prelate Protestants ever denied them." But whatever you can prove or cannot prove, you have made it very easy for any man to prove that you have very little regard unto truth and sobriety in what you aver, so that you may acquit yourself from that which presseth you, and which, according to the rules of them, you cannot stand before. You tell us, in the entrance of this discourse, that you said "that prelate Protestants, for their own preservation, took up some of those principles again which former Protestants had cast down for popish;" and here expressly, that you "said not that they took up the principles which themselves had cast down, but only those which other before them had so dealt withal." Now, pray take a view of your own words, whereby you express yourself in this matter, chap. 3 sect. 14, p. 189, second edition. Are they not these: "The prelate Protestant, to defend himself against them" (the Presbyterians and Independents), "is forced to make use of those very principles which himself aforetime" (not other Protestants but himself), "when he" (not others) "first contended against Popery, destroyed. So that upon him falls most heavily, even like thunder and lightning from heaven, utterly to kill and cut him asunder, that great oracle delivered by St Paul, 'If I build up again the things I'" (not another) "'formerly destroyed, I make myself a prevaricator, an impostor, a reprobate?'" What think you of these words? Do you charge the prelate Protestant with building up what others had pulled down, or what he had destroyed himself? Is your rule out of St. Paul applicable unto him upon any other account but that he himself was both the _builder_ and _destroyer?_ Sir, such miscarriages as these Protestants know to be mortal sins; and if, without contrition for them, you have celebrated any sacrament of your church, it cannot be avoided but that you have brought a great inconvenience on some of your disciples. Besides, suppose you had spoken as you now feign yourself to have done, I desire to know who they are whom you intend when you say, "Our prelate Protestants, so soon as they became such;" as though they were first Protestants at large, and destroyed those principles which afterward they built up when they became prelate Protestants; seeing all men know that our reformation was begun by prelates themselves, and such as never disclaimed the principles by you instanced in.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 15.* — `Paragraph has unmatched double quotes (count: 23)`
      * Context: `**Here, first, you deny that these principles are popish; but, sir, there are some Jews, even at this day, who will deny a...**`

##### Entry: `[[BLOCKQUOTE]] "By the laws of our land, our series of government ecclesiastical stands thus:` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 16.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] "By the laws of our land, our series of government ecclesiastical stands thus:**`

##### Entry: `[[BLOCKQUOTE]] "The Presbyterian predicament is thus:` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 16.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] "The Presbyterian predicament is thus:**`

##### Entry: `[[BLOCKQUOTE]] "qui putant rationem sacrificii totam constitui in verbis, precibus, ceremoniis, et ritibus, qui in consecratione adhibentur, eo quod sacrificii ratio, inquiunt, nequit in ipsa consecratione consistere, quin e contrario consecratio ad rationem sacramenti potius quam ad naturam sacrificii pertinet. Alii existimant sacrificii rationem tribus sacerdotis actionibus constare, consecratione, oblatione, et sumptione. Alii quidem sensere ad rationem hujus sacrificii quatuor imo quinque actiones concurrere, cousecrationem, oblationem, fractionem, sumptionem. Alii rationem sacrificli ponunt in duobus actibus, consecratione et oblatione.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 19.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] "qui putant rationem sacrificii totam constitui in verbis, precibus, ceremoniis, et ritibus, qui in conse...**`

##### Entry: `Alii constituunt totam rationem sacrificil in una actione, viz., consecratione;" — "There are who think the nature of the sacrifice to consist in the words, prayers, ceremonies, and rites which are used in the consecration, because, they say, the nature of the sacrifice cannot consist in the consecration itself, which rather belong unto the nature of a sacrament than of a sacrifice. Others think that the sacrifice consists in three actions of the priest, — consecration, oblation, and sumption, or receiving of the host. Others in four or five, — as consecration, oblation, fraction, sumption. Others in two, — consecration and oblation; and some in one, — consecration." And is not this a brave business, to impose on the consciences of all men, when you know not yourselves what it is that you would so impose! A sacrifice must be believed, and they are all accursed by you that believe it not; but what the sacrifice is, and wherein it doth consist, you cannot tell! And an easy matter it were to manifest that all the particulars which you assign as those that either belong necessarily unto the integrity of a sacrifice, or those wherein some of you, or any of you, would have its essence to consist, are indeed of no such nature or importance; but that is not my present business. I am only inquiring what your sacrifice is, according unto your own sense and imagination; and that we may not mistake, I shall set down such a general description of it as the canon of the mass, the general rubric of the missal, the rites and cautels of its celebration, will afford unto us. Now, in these it is represented as a sacred action, wherein a proper priest or sacrificer, arrayed with various consecrated attire, standing at the altar, taketh bread and wine, — about which he useth great variety of postures and gestures, inclinations, bowings, kneelings, stretching out and gathering in his arms, with a multitude of crossings at the end and in the midst of his pronunciation of certain words of Scripture, — turns them into the real natural body and blood of Christ the Son of God; worshipping them so converted with religious adoration, showing them to the people for the same purpose; and then offering the body and blood unto God, praying for his acceptance of them so offered, and that it may be available for the living and the dead, for the pardoning of their sins and saving of their souls: after which he takes that body of Christ, so made, worshipped, and offered, and eats and devours it! By all which Christ is truly and properly sacrificed!` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 19.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**Alii constituunt totam rationem sacrificil in una actione, viz., consecratione;" — "There are who think the nature of th...**`

##### Entry: `(3.) I told you before, but now begin to fear that you are too old to learn what you do not like, that the LXX. never translated זֶ־בח sacrifice," or to sacrifice, by λειτουργία or λειτουργῶ, nor intimate any sacrifice anywhere by that word. And you may, if you please, now learn, by the instance of Samuel, that what men perform in the worship of God according to his command, they may be said therein to "minister unto or before the Lord in."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 19.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**(3.) I told you before, but now begin to fear that you are too old to learn what you do not like, that the LXX. never tr...**`

##### Entry: `The first thing you reflect upon is my censure of that passage in your _"Fiat,"_ that "the sight of images in the church is apt to cast the minds of men on that meditation of the apostle, Hebrews 12, 'You are come to mount Sion, to the city of the living God, to the heavenly Jerusalem, the society of angels, and church of the first-born, written in heaven, to God the judge of all, to the spirits of just men made perfect, to Jesus the mediator of the new covenant:'" — "These, I tell you, upon the sight of a house full of images, may be the thoughts of a man distracted of his wits, not of any that are sober and wise." To which you reply, "Madmen, it seems, can tell what figures represent; sober and wise men cannot." But who told you that your images represent the things mentioned by the apostle, — for instance, "God the judge of all, the spirits of just men, angels, and the church of the first-born?" or can any man, unless he be greatly distempered in his imagination, fancy any such thing? The house of Micah, Judges 17; was notably furnished with images of all sorts. Judges 17; he had בֵּית אֶלֹהִים, "a house full of gods," or a chapel adorned with images; for there was in it פֶסֶל "a carved image," and אֵפוֹד, a sacred ornament" for it, and תְרָפִים, "lesser portable images," and ־מסֵּכָה, a "molten statue," Judges 18:Would it not, think you, not-withstanding the gaiety of all this provision, have been a mad thought in the Danites if, upon their entrance into this house, they had apprehended themselves to be come to the communion of the catholic church, and therein to the invisible God, to angels, and saints departed? The truth is, there is "aliquid dementise," a tincture of madness, in all idolatry, whence the Scripture testifies that men are "mad upon their idols;" but yet we do not find that these Danites, though resolved upon false worship, were so mad as to entertain such vain thoughts as you imagine the chapel full of images might have suggested unto them. Or do you think Ezekiel had any such thoughts when God showed him in vision the imagery of the house of Israel, with all the deities "pourtrayed on the wall," and the elders worshipping before them? Ezekiel 8. God and the prophet discover other thoughts in reference unto them. Besides, sir, the Holy Ghost tells us that "a graven image is a teacher of lies," Habakkuk 2:18; and how likely it is that a man should learn any truth from that whose work it is only to teach lies, I do not as yet understand. You proceed to another exception. "'The violation of an image,' say you, 'redounds to the prototype, if it be rightly and duly represented, not else.'" To which you reply, "And when, then, for example, is Christ crucified rightly and duly represented? Are you one of those that can tell what figures represent or not?"` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21.* — `Paragraph has unmatched double quotes (count: 31)`
      * Context: `**The first thing you reflect upon is my censure of that passage in your "Fiat," that "the sight of images in the church i...**`

##### Entry: `Do you consider what you say? God hath given us his whole word for our use and benefit. "Nine parts in ten of it," say you, "do not concern us. Can possibly any man break forth into a higher reflection upon the wisdom and love of the holy God? or do you think you could have made a more woful discovery of your unacquaintedness with your own duty, the nature of faith and obedience evangelical, than you have done in these words? You will not make thus bold with the books that Aristotle hath left us in philosophy, or Galen in medicine. But the wisdom of God, in that writing which he hath given us for the revelation of his will, it seems, may be despised. Such fruit, in the depraved nature of man, will ἀμετρία τῆς ἀνθολκῆς produce. The practice we blame in you is not worse than the reasonings you use in its confirmation. I pray God neither of them may be ever laid unto your charge. Your following words are a commendation of the zeal and piety of the days and times before the Reformation, with reflections upon all things amongst us since; and this I shall pass by, so to avoid the occasion of representing unto you the true state of things, both here and elsewhere, in the ages you so much extol. Neither, indeed, is it to any great purpose to lay open anew that darkness and wickedness which the world groaned under, and all sober men complained of. You proceed to other exceptions, and say: —` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 22.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**Do you consider what you say? God hath given us his whole word for our use and benefit. "Nine parts in ten of it," say y...**`

##### Entry: `[[BLOCKQUOTE]] "Where 'Fiat Lux' says that the Pentateuch or hagiography was never, by any high priest among the Jews, put into a vulgar tongue, nor the gospel or liturgy out of Greek in the eastern part of the Christian church, or Latin in the western, you slight this discourse of mine, because Hebrew, Greek, and Latin were vulgar tongues in themselves. I know this well enough; but when, and how long ago, were they so? Not for some thousand years, to my knowledge. And was the Bible, Psalms, or Christian liturgy, then put into vulgar tongues when those they were first written in ceased to be vulgar? This you should have spoken unto if you had meant to say any thing or gainsay me. Nor is it to purpose to tell me that St.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 22.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] "Where 'Fiat Lux' says that the Pentateuch or hagiography was never, by any high priest among the Jews, p...**`

##### Entry: `[[BLOCKQUOTE]] Jerome translated the Bible into Dalmatian. I know well enough it hath been translated by some special persons into Gothish, Armenian, Ethiopian, and other particular dialects; but did the church, either of the Hebrews or the Christians, either Greek or Latin, ever deliver it so translated to the generality of people, or use it in their service, or command it so to be done, as a thing of general concernment and necessity? So far is it from that, that they would never permit it."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 22.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**[[BLOCKQUOTE]] Jerome translated the Bible into Dalmatian. I know well enough it hath been translated by some special pe...**`

##### Entry: `3. You suppose that in the language wherein Rabshakeh and the princes conferred, their Syriac was an abbreviation of Assyriac, because in sound it was so near the other that they would have him speak in; so that the Jews, speaking Syriac, when the princes desired Rabshakeh to speak Syriac, they meant another language, as much differing from that as French from English. But you are in the dark, and know not how you wander up and down to no purpose. There is nothing of the words that you pretend to be an abbreviation the one of the other in the text; nor is there any such relation between them as you imagine, that they should be near in sound, though not in nature. Eliakim entreats Rabshakeh that he would speak אֲרָמִית, "Aramith, Aramice;" that is, as the Greeks and Latins express that people and language "Syriace," in Syriac, — that he would speak the language of Aram; which language was spoken also by אֲשׁוּר, the king and people of Assyria And truly אֲרָם, "Aram, is no abbreviation of אָשׁוּר, "Ashur," as I suppose.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 22.* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**3. You suppose that in the language wherein Rabshakeh and the princes conferred, their Syriac was an abbreviation of Ass...**`

##### Entry: `6. So you think that Shibboleth and Sibboleth may differ more in "signification than sound." But, pray, what do you think is the signification of סִבֹּלֶת as the Ephraimites pronounced שִׁבֹּלֶת? Just as much a word falsely pronounced signifieth, and no more, — that is, of itself njust nothing at all; for סִבֹּלֶת, "Sibboleth," is no Hebrew word, but merely שִׁבֹּלֶת, "Shibboleth, falsely pronounced.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 22.* — `Paragraph has unmatched double quotes (count: 5)`
      * Context: `**6. So you think that Shibboleth and Sibboleth may differ more in "signification than sound." But, pray, what do you thin...**`

##### Entry: `<section class="treatise-title-page" epub:type="titlepage"> <p class="title-line title-line-medium">THE</p> <p class="title-line title-line-major">CHURCH OF ROME NO SAFE</p> <p class="title-line title-line-major">GUIDE;</p> <p class="title-line title-line-medium">OR</p> <p class="title-line title-line-medium">REASONS TO PROVE THAT NO RATIONAL MAN,</p> <p class="title-line title-line-medium">WHO TAKES DUE CARE OF HIS OWN ETERNAL</p> <p class="title-line title-line-medium">SALVATION, CAN GIVE HIMSELF UP UNTO</p> <p class="title-line title-line-medium">THE CONDUCT OF THAT CHURCH IN</p> <p class="title-line title-line-medium">MATTERS OF RELIGION.</p> </section> Trust ye not in lying words, saying, The temple of the LORD, are these. Will ye steal, murder, and commit adultery, and swear falsely, and burn incense unto Baal, and walk after other gods whom ye know not; and come and stand before me in this house, which is called by my name?" — JEREMIAH 7:4,9,10.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Church of Rome No Safe Guide* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**THE   CHURCH OF ROME NO SAFE   GUIDE;   OR   REASONS TO PROVE THAT NO RATIONAL MAN,   WHO TAKES DUE CARE OF HIS OWN ETER...**`


### 2. Text Integrity Whitelist

#### Paragraph Splits

##### Split Entry: `READER,` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... READER,`
      * Next: `THE treatise entitled "Fiat Lux," which thou wilt find examined in the ensuing discourse, was lent unto me, not long since, by an honorable person, with a request to return an answ ...`
    * **File:** `EPUB/ch029.xhtml`
      * Previous: `... CHRISTIAN READER,`
      * Next: `ALTHOUGH our Lord Jesus Christ hath laid blessed and stable foundations of unity, peace, and agreement in judgment and affection amongst all his disciples, and given forth command ...`

##### Split Entry: `writing? — so doth Celsus.` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch006.xhtml`
      * Previous: `... writing? — so doth Celsus. Doth he deride and scoff at the first reformers, with no less witty and biting sarcasms than those wherewith Aristophanes jeered Socrates on the stage? —`
      * Next: `Celsus deals no otherwise with the first propagators of Christianity. Hath he taken pains to palliate and put new glosses and interpretations upon those opinions and practices in h ...`

##### Split Entry: `It is Protestants —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... rned with England. He would quickly tell us that this is our mistake; he intended not Roman Catholics, and the differences we have with them, in this discourse. It is Protestants —`
      * Next: `Presbyterians, Independents, Anabaptists, Quakers — that he deals withal, and them only; and that upon this ground, that none of them have any title or pretense of reason to impose ...`

##### Split Entry: `Dubius sum quid faciam` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... you said with him in the poet, " Dubius sum quid faciam — Tene relinquam an rem?" I should have replied with him, "Me sodes;" but you were otherwise minded, and are gone before, —`
      * Next: `—— " Ego (ut contendere durum est Cure victore) sequar." Hor. Sat. 1:9, 42. I will follow you with what patience I can, and make the best use I am able of what offers itself in you ...`

##### Split Entry: `discipline of your own thoughts: —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... unto this fiction (for " malum semper habitat in alieno fundo "), I shall have occasion afterward to consider. For the present I leave you to the discipline of your own thoughts: —`
      * Next: `—— " Prima est haec ultio, quod se Judice, nemo nocens absolvitur." Juv. 13:2. And I the rather mind you of your failure at this entrance of our discourse, that I may only remit yo ...`

##### Split Entry: `Φήμη δ οὔ ` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... rd speak any thing of that discourse, of what persuasion in religion soever they were. And Aristotle thought it worth while to remember out of Hesiod, Moral. Nicom. lib. 7, that, —`
      * Next: `Φήμη δ οὔ τις πάμπαν ἀπόλλυται ἥν τινα πολλοὶ Λαοὶ φημίζουσιν . ...`

##### Split Entry: `Let. 15. 20` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... s, though grounded on absolute falsities, but hath also given us such pestilent instances of their practice, according to that principle, as Paganism was never acquainted withal. —`
      * Next: `Let. 15. 20 In their steps you set out in this your first reason, wherein there is not one word of truth. I had formerly told you that I Aid not think you could yourself believe so ...`

##### Split Entry: `Major tandem parcas` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... And, —`
      * Next: `—— "Major tandem parcas insane minori." — Hor . Sat. 2:3, 325. ...`

##### Split Entry: `Εχθρὸς γάρ μοι` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... duce them to a naked fanatical "credo?" or is it your interest to court them with fine words, though your intention be far otherwise? But we in England like not such proceedings: —`
      * Next: `Εχθρὸς γάρ μοι κεῖνος ὁμῶς ἀΐδαο πύλῃσιν , Ος χ ἕτερον μὲν κεύθει ἐνὶ φρεσίν , ἅλλο δὲ βάζει . ...`

##### Split Entry: `Furiarum maxima` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch030.xhtml`
      * Previous: `... world? Do we disallow or forbid them any means that may tend to their furtherance in the knowledge and profession of religion? Where is it that, if they do but look upon a Bible, —`
      * Next: `—— " Furiarum maxima juxta Accubat, et manibus prohibet contingere mensas ;" Virg. AEn. 6:605. — the inquisitor lays hold upon them, and bids them be contented with a rosary, or ou ...`

##### Split Entry: `Scripture it was instructed: —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch033.xhtml`
      * Previous: `... tasy, desiring only that you would grant me that the primitive church of Rome believed and faithfully retained the doctrine of truth wherein from the Scripture it was instructed: —`
      * Next: `That church believed expressly that all they "who die in the Lord do rest from all their labors," Revelation 14:13; — which truth you have forsaken, by sending many of them into th ...`

##### Split Entry: `worth the recital: —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch036.xhtml`
      * Previous: `... ffirms that the church proved the Scripture by itself; and other things, as the unity of the Deity, by the Scripture. But his own words in the former place are worth the recital: —`
      * Next: `Ἔχομεν , saith he, τὴν ἀρχὴν τῆς πίστεως , 32 τὸν Κύριον , διά τε τῶν προφητῶν , διά τε τοῦ εὐαγγελίου , καὶ διὰ τῶν μακαρίων ἀποστόλων πολυτρόπως καὶ πολυμερῶς ἐξ ἀρχῆς εἰς τέλος ...`

##### Split Entry: `Well said he of old, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch037.xhtml`
      * Previous: `... Well said he of old, —`
      * Next: `Εὐήθειά μοι φαίνεται δηλουμένη Τὸ νοεῖν μὲν δεῖ , φυλάττεσθαι δ ἅ δεῖ . ...`

##### Split Entry: `fight on, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch038.xhtml`
      * Previous: `... ation, as the world is only as yet in secret acquainted withal. When this is done, the way for a farther agreement will be open and facile; and until it be so, men will fight on, —`
      * Next: `—— "Ipsique, nepotesque Et nati natorum, et qui nascentur ab illis ;" we shall have no end of our quarrels. Could I see a heroic temper fall on the minds of men of the several part ...`

##### Split Entry: `make sport: —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch040.xhtml`
      * Previous: `... words in the "Animadversions," cut off from that coherence wherein they are placed, are the chief ingredients of it. With these you aim, with your wonted success, to make sport: —`
      * Next: `—— "Venite in ignem Pleni ruris et inficetiarum Annales Volusi." ...`

##### Split Entry: `and cry out, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch040.xhtml`
      * Previous: `... ded that there is not the least tincture of any solid metaphysics in your whole discourse. It may be, indeed, you would be angry with them that should undeceive you, and cry out, —`
      * Next: `— "Pol, me occidistis, amici , Non servastis ;" as he did, — ...`

##### Split Entry: `says of him, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch041.xhtml`
      * Previous: `... unto it. Then your consequence you say you "deem strong and good." I doubt not but you do so: so did Suffenus of his poems; but another was not of the same mind, who says of him, —`
      * Next: `—— " Qui modo scurra , Ant si quid hac re trititus, videbatur , Idem inficeto est inficetior rure, Simul poemata attigit; neque idem unquam A Eque est beatus, ac poema cum scribit: ...`

##### Split Entry: `a common error, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch042.xhtml`
      * Previous: `... es of it; partly in a repetition, in other words, of what you had before insisted on. The former I shall no farther endeavor to disturb your contentment in. It is a common error, —`
      * Next: `—— "Neque est quisquam Quem non in aliqua re videre Suffenum Possis ." Catull. 22:19. ...`

##### Split Entry: `secure from adversaries, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch045.xhtml`
      * Previous: `... ians. It may be you will scarcely ever obtain such another opportunity of showing the fertility of your invention. So did he flourish who thought himself secure from adversaries, —`
      * Next: `—— " Caput altum in praelia tollit, Ostenditque humeros latos , alternaque jactat Brachia protendens, et verberat ictibus auras ." Virg. AEn. 5:375. ...`

##### Split Entry: `The very same instances are given` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch045.xhtml`
      * Previous: `... r thou be an apostle, or an evangelist, or a prophet, or whatever thou be; for subjection overthrows not piety. And he saith not simply, 'Let him obey,' but, 'Let him be subject.'"`
      * Next: `The very same instances are given by Theodoret, Oecumenius, and Theophylact. Bernard, Epist. 42, ad Archiepisc. Senonena, meets with your exception, which in his days began to be b ...`

##### Split Entry: `object unto them, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch045.xhtml`
      * Previous: `... h Protestants unanimously ascribe unto them, especially those in England to his royal majesty. And from hence you may see the frivolousness of sundry things you object unto them, —`
      * Next: `As, first, of the scheme or series of ecclesiastical power which you ascribe to prelate Protestants and the laws of the land, from which you say the Presbyterians dissent; which yo ...`

##### Split Entry: `And yet the misadventure of it is` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch050.xhtml`
      * Previous: `... τεύουσι — "But if any should say, 'Why do our images work no miracles?' to them we answer, 'Because,' as the apostle saith, 'signs are for unbelievers, not for them that believe.'"`
      * Next: `And yet the misadventure of it is, that the most of the miracles which they report and build their faith upon were wrought as by, so amongst, their chiefest believers. And what wer ...`


#### Ignored Warnings

##### Warning Entry: `low_latin_tagging` (✅ Clean)
  * Silenced warning message(s):
    * `A significant portion of Latin words in the EPUB are not wrapped in language spans`

##### Warning Entry: `low_latin_translation_coverage` (✅ Clean)
  * Silenced warning message(s):
    * `Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py`
