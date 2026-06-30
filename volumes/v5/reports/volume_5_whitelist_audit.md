# Whitelist Trace & Audit Report: Volume 5

This report tracks and validates every whitelist entry to prevent greedy silencing of real anomalies.

## Summary

* **Total Whitelisted Entries:** 50
* **Clean/Exact Matches (1 issue silenced):** 34
* **Greedy Entries (silences multiple issues):** 5
* **Unused Entries (silences 0 issues - safe to remove):** 11

### ⚠️ Greedy Whitelist Entries
These entries are too broad and matched multiple distinct anomalies. Consider making them more specific.

| Whitelist Path / Entry | Match Count |
|-------------------------|-------------|
| `anomalies -> Hyphenation Anomalies -> 'non-imputation'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 4.'` | 2 |
| `text_integrity -> paragraph_splits -> To The Reader` | 2 |
| `text_integrity -> paragraph_splits -> hence we argue, —` | 2 |

### ❌ Unused Whitelist Entries
These entries matched zero raw issues. They should be deleted to keep the whitelist clean.

* `anomalies -> Hyphenation Anomalies -> 'sub-distinguished'`
* `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 5.'`
* `anomalies -> Unmatched Quotation Marks -> 'The first inquiry in this matter, in a way of duty, is after the proper relief'`
* `anomalies -> Unmatched Quotation Marks -> 'Credisne te non posse salvari'`
* `anomalies -> Unmatched Quotation Marks -> 'Whence the prophet says in the psalm'`
* `anomalies -> Unmatched Quotation Marks -> 'A full comprehension of it no creature'`
* `anomalies -> Unmatched Quotation Marks -> '3. "Ex injuria; or,'`
* `anomalies -> Unmatched Quotation Marks -> 'originally included no merit'`
* `anomalies -> Unmatched Quotation Marks -> 'Si obedientia vitae Christi nobis'`
* `text_integrity -> ignored_warnings -> 'repeated_phrases'`
* `text_integrity -> ignored_warnings -> 'low_latin_tagging'`

---

## Detailed Trace by Category

### 1. Anomalies Whitelist

#### Category: `OCR & Bracket Residues`

##### Entry: `qui et` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ* — `Split word anomaly (rejoins to 'quiet')`
      * Context: `... t of the eucharist, "Nos omnes portabat Christus; **qui et** peccata nostra portabet"; — "He bare us", or suff ...`


#### Category: `Hyphenation Anomalies`

##### Entry: `wire-draw` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *To the Reader (The Doctrine of Justification by Faith)* — `Splittable word (rejoins to valid word 'wiredraw')`
      * Context: `... iness to cavil at expressions, to wrest my words, **wire-draw** inferences and conclusions from them not expressl ...`

##### Entry: `dikaio-oo` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4 - of Justification* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... y no man was ever yet so fond as to pretend that "**dikaio-oo**" did signify to pardon sin, yet is it the only wo ...`

##### Entry: `non-imputation` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *Chapter 4 - of Justification* — `Splittable word (rejoins to valid word 'nonimputation')`
      * Context: `... nishment due unto sin;" for it comprises both the **non-imputation** of sin and the imputation of righteousness, with ...`
    * **Chapter:** *Chapter 7 - Imputation, & the Nature of It* — `Splittable word (rejoins to valid word 'nonimputation')`
      * Context: `... ation, or, that our justification consists in the **non-imputation** of sin, and the imputation of righteousness. But ...`
      * Context: `... tation, in both branches of it, — negative in the **non-imputation** of sin, and positive in the imputation of righteo ...`
    * **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ* — `Splittable word (rejoins to valid word 'nonimputation')`
      * Context: `... tever be imputed unto them. And where that is, no **non-imputation** of sin, as unto punishment, can free the person i ...`
      * Context: `... y he escaped present punishment, yet did not that **non-imputation** free him formally from being a sinner. Wherefore ...`
    * **Chapter:** *Chapter 18 - the Nature of Justification* — `Splittable word (rejoins to valid word 'nonimputation')`
      * Context: `... , in that the imputation of righteousness and the **non-imputation** of sin (both which the apostle mentions distinctl ...`

##### Entry: `sub-distinguished` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `non-solvent` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ* — `Splittable word (rejoins to valid word 'nonsolvent')`
      * Context: `... noxius", — liable to payments for others that are **non-solvent**. 2. God can, therefore, have no surety properly, ...`

##### Entry: `blood-guiltiness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Imputation of the Sins of the Church Unto Christ* — `Splittable word (rejoins to valid word 'bloodguiltiness')`
      * Context: `... ver me" מִדָּמִים, "from blood"; which we render "**blood-guiltiness**," Psalm 51:14. And this was because, by the const ...`

##### Entry: `co-interest` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 18 - the Nature of Justification* — `Splittable word (rejoins to valid word 'cointerest')`
      * Context: `... heir merit, as inconsistent with grace, but their **co-interest** on our part with, or subsequent interest unto fai ...`


#### Category: `Structural Nesting Sequence Jumps`

##### Entry: `2.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 3 - the Use of Faith in Justification* — `List sequence starts at 2 instead of 1`
      * Context: `... ξ ἀκοῆς πίστεως are directly opposed, Galatians 3:**2.** But when it is said that a man is not justified ἐ ...`
      * Context: `... se itself being the formal object of its assent. **2.** We cannot so receive Christ in the promise, as in ...`
      * Context: `... their faith in their justification before God. (**2.**) The Scripture plainly declares that faith as jus ...`
    * **Chapter:** *Chapter 20 - Doctrine of the Apostle James Concerning Faith* — `List sequence jump (skipped from 2 to 4)`

##### Entry: `5. ... 7.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 11 - the Nature of the Obedience That God Requires* — `List sequence jump (skipped from 5 to 7)`

##### Entry: `3. ... 5.` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `2. ... 4.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 3 - the Use of Faith in Justification* — `List sequence starts at 2 instead of 1`
      * Context: `... ξ ἀκοῆς πίστεως are directly opposed, Galatians 3:**2.** But when it is said that a man is not justified ἐ ...`
      * Context: `... se itself being the formal object of its assent. **2.** We cannot so receive Christ in the promise, as in ...`
      * Context: `... their faith in their justification before God. (**2.**) The Scripture plainly declares that faith as jus ...`
    * **Chapter:** *Chapter 20 - Doctrine of the Apostle James Concerning Faith* — `List sequence jump (skipped from 2 to 4)`


#### Category: `Unmatched Quotation Marks`

##### Entry: `The first inquiry in this matter, in a way of duty, is after the proper relief` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `Credisne te non posse salvari` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `Whence the prophet says in the psalm` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `The excellent words of Justin Martyr` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *General Considerations,* — `Paragraph has unmatched double quotes (count: 19)`
      * Context: `**The excellent words of Justin Martyr deserve the first place: Αὑτὸς τὸν ἴδιον υἱὸν ἀπέδοτο λύτρον ὑπέρ ἡμῶν, τὸν ἅγιον ὑ...**`

##### Entry: `A full comprehension of it no creature` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `But the true and genuine signification of these words` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 4 - of Justification* — `Paragraph has unmatched double quotes (count: 5)`
      * Context: `**But the true and genuine signification of these words is to be determined from those in the original languages of the Sc...**`

##### Entry: `3. "Ex injuria; or,` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `(1.) "Injuriarum," of wrongs:` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7 - Imputation, & the Nature of It* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**(1.) "Injuriarum," of wrongs: Εἰ δέ τι ἡδίκησέ σε? — If he has dealt unjustly with thee, or by thee, if he has so wronge...**`

##### Entry: `In this state the apostle interposes himself` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 7 - Imputation, & the Nature of It* — `Paragraph has unmatched double quotes (count: 9)`
      * Context: `**In this state the apostle interposes himself by a voluntary sponsion, to undertake for Onesimus: "I Paul have written it...**`

##### Entry: `(1.) The Lord Christ, our mediator and surety` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12 - the Imputation of the Obedience of Christ* — `Paragraph has unmatched double quotes (count: 9)`
      * Context: `**(1.) The Lord Christ, our mediator and surety, was, in his human nature, made ὑπὸ νόμον, — "under the law," Galatians 4:...**`

##### Entry: `We shall take our fourth argument from the express exclusion` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 14 - the Exclusion of All Sorts of Works* — `Paragraph has unmatched double quotes (count: 11)`
      * Context: `**We shall take our fourth argument from the express exclusion of all works, of what sort soever, from our justification b...**`

##### Entry: `originally included no merit` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `Si obedientia vitae Christi nobis` (❌ Unused)
  * Silenced 0 raw issues.

##### Entry: `injustus", 1 Peter 3:18` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 18 - the Nature of Justification* — `Paragraph has unmatched double quotes (count: 5)`
      * Context: `**injustus", 1 Peter 3:18. "Quod si ergo justi effecti sumus per vitam illius, causa nulla relicta fuit cur pro nobis more...**`

##### Entry: `This treatise, entitled Gospel Grounds and Evidences` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note (Evidences of the Faith of God's Elect)* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**This treatise, entitled Gospel Grounds and Evidences of the Faith of God's Elect," was given to the world in 1695. The r...**`

##### Entry: `Isaiah 13:6, 7; — "When the day` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *General Considerations,* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**Isaiah 13:6, 7; — "When the day of judgment or of death shall come, all hands will be dissolved" (that is, faint or fall...**`


#### Category: `Invalid Bible References`

##### Entry: `John 22` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *General Considerations,* — `Invalid Bible reference (chapter 22 exceeds max 21 for John)`
      * Context: `... elieve that Jesus is the Christ, the Son of God," **John 22**:30,31. Unto this end every thing is recorded by ...`


### 2. Text Integrity Whitelist

#### Paragraph Splits

##### Split Entry: `To The Reader` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... To The Reader`
      * Next: `I shall not need to detain the reader with an account of the nature and moment of that doctrine which is the entire subject of the ensuing discourse; for although sundry persons, e ...`
    * **File:** `EPUB/ch027.xhtml`
      * Previous: `... To The Reader`
      * Next: `As faith is the first vital act that every true Christian puts Forth, and the life which he lives is by the faith of the Son of God, so it is his next and great concern to know tha ...`

##### Split Entry: `was this, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch005.xhtml`
      * Previous: `... nd by their propositions, they were not to be attained? Hence the principal controversy in this matter, which the reformed divines had with those of the church of Rome, was this, —`
      * Next: `Whether there be, according unto and by the gospel, a state of rest and assured peace with God to be attained in his life? And having all advantages imaginable for the proof hereof ...`

##### Split Entry: `Whence I argue, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch007.xhtml`
      * Previous: `... set forth to be a propitiation through faith in his blood, to declare his righteousness for the remission of sins that are past, through the forbearance of God." Whence I argue, —`
      * Next: `That which a guilty, condemned sinner, finding no hope nor relief from the law of God, the sole rule of all his obedience, does retake himself unto by faith, that he may be deliver ...`

##### Split Entry: `the inquiry is, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch009.xhtml`
      * Previous: `... in the sight of God. Whatever, therefore, is the means, condition, or cause hereof, is pleadable before God, and ought to be pleaded unto that purpose. So, then, the inquiry is, —`
      * Next: `What it is that, when a justified person is guilty of sin (as guilty he is more or less every day), and his conscience is pressed with a sense thereof, as that only thing which can ...`

##### Split Entry: `Justification by the law is this, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... has not the nature of any justification that is mentioned in the Scripture, — that is, neither that by the law, nor that provided in the gospel. Justification by the law is this, —`
      * Next: `The man that does the works of it shall live in them. This it does not pretend unto. And as unto evangelical justification, it is every way contrary unto it. For therein the charge ...`

##### Split Entry: `various inquiries are made, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch012.xhtml`
      * Previous: `... But hereon sundry discourses do ensue, and various inquiries are made, —`
      * Next: `What a person is? In what sense, and in how many senses, that word may be used? What is the true notion of it? What is a natural person? What a legal, civil, or political person? I ...`

##### Split Entry: `hence we argue, —` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch014.xhtml`
      * Previous: `... ence, but upon the righteousness of Christ, and our interest therein by faith; as is too evident to be modestly denied. Notwithstanding this exception, therefore, hence we argue, —`
      * Next: `If the most holy of the servants of God, in and after a course of sincere, fruitful obedience, testified unto by God himself, and witnessed in their own consciences, — that is, whi ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... eousness of the law. "By the obedience of one many are made righteous," Romans 5:19. "That the righteousness of the law might be fulfilled in us," Romans 8:4. And hence we argue, —`
      * Next: `If there be no other way whereby the righteousness of the law may be fulfilled in us, without which we cannot be justified, but must fall inevitably under the penalty threatened un ...`

##### Split Entry: `observed, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch014.xhtml`
      * Previous: `... is personal, inherent righteousness of our own, what it is, and wherein it does consist, and of what use it may be in our justification. And unto this purpose it may be observed, —`
      * Next: `That we grant an inherent righteousness in all that do believe, as has been before declared: "For the fruit of the Spirit is in all goodness, and righteousness, and truth", Ephesia ...`

##### Split Entry: `There was עֲצֶרֶת הַדְּבָרִים , —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch018.xhtml`
      * Previous: `... (1.) There was עֲצֶרֶת הַדְּבָרִים , —`
      * Next: `Deuteronomy 4:13, "The ten words;" so also chapter 10:4; — that is, the ten commandments written upon two tables of stone. This part of the law was first given, was the foundation ...`

##### Split Entry: `I shall consider, first, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch021.xhtml`
      * Previous: `... h and resurrection of Christ, which is represented in them. Some few of the many testimonies which may be pleaded out of their writings unto that purpose I shall consider, first, —`
      * Next: `The principal design of our blessed Savior's sermon, especially that part of it which is recorded, Matthew 5, is to declare the true nature of righteousness before God. The scribes ...`

##### Split Entry: `Hence we argue, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch022.xhtml`
      * Previous: `... s natural posterity, as unto sin and death; so it is with the Lord Christ, the second Adam, and his spiritual posterity, with respect unto righteousness and life. Hence we argue, —`
      * Next: `If the actual sin of Adam was so imputed unto all his posterity as to be accounted their own sin unto condemnation, then is the actual obedience of Christ, the second Adam, imputed ...`

##### Split Entry: `Wherefore, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch022.xhtml`
      * Previous: `... be by his righteousness as we are in him, or united unto him. To be righteous in him is to be righteous with his righteousness, as we are one mystical person with him. Wherefore, —`
      * Next: `To be made the righteousness of God in Christ, as he was made sin for us, and because he was so, can be no other but to be made righteous by the imputation of his righteousness unt ...`

##### Split Entry: `Again, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch022.xhtml`
      * Previous: `... the removal of all other ways, causes, means, and conditions of it, as inconsistent with it. But the antecedent is expressly the apostle's: "Not my own, but that of God." Again, —`
      * Next: `That whereby and wherewith we are "found in Christ" is that whereby alone we are justified before God; for to be found in Christ expresseth the state of the person that is to be ju ...`

##### Split Entry: `the question proposed, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch024.xhtml`
      * Previous: `... though he be destitute of good works and live in sin, he is accepted with God, and shall be saved; — will, indeed, this faith save him? This, therefore, is the question proposed, —`
      * Next: `Whereas the gospel says plainly, that "he who believeth shall be saved," whether that faith which may and does consist with an indulgence unto sin, and a neglect of duties of obedi ...`


#### Ignored Warnings

##### Warning Entry: `repeated_phrases` (❌ Unused)
  * Silenced 0 warnings.

##### Warning Entry: `missing_latin_clauses` (✅ Clean)
  * Silenced warning message(s):
    * `Some dense Latin passages from the PDF are missing from the EPUB`

##### Warning Entry: `low_latin_tagging` (❌ Unused)
  * Silenced 0 warnings.

##### Warning Entry: `repeated_windows` (✅ Clean)
  * Silenced warning message(s):
    * `Repeated word windows may indicate ghost-layer duplication`

##### Warning Entry: `inline_structural_markers` (✅ Clean)
  * Silenced warning message(s):
    * `Some list or roman markers appear embedded in prose instead of starting their own paragraph`

##### Warning Entry: `overlong_heading_candidates` (✅ Clean)
  * Silenced warning message(s):
    * `Some chapter headings are long enough to suggest swallowed body text`

##### Warning Entry: `low_latin_translation_coverage` (✅ Clean)
  * Silenced warning message(s):
    * `Some tagged Latin phrases in the EPUB do not have matching modern translations in translation_db.py`
