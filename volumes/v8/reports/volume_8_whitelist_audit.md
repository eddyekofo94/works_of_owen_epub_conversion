# Whitelist Trace & Audit Report: Volume 8

This report tracks and validates every whitelist entry to prevent greedy silencing of real anomalies.

## Summary

* **Total Whitelisted Entries:** 164
* **Clean/Exact Matches (1 issue silenced):** 107
* **Greedy Entries (silences multiple issues):** 56
* **Unused Entries (silences 0 issues - safe to remove):** 1

### ⚠️ Greedy Whitelist Entries
These entries are too broad and matched multiple distinct anomalies. Consider making them more specific.

| Whitelist Path / Entry | Match Count |
|-------------------------|-------------|
| `anomalies -> Unmatched Quotation Marks -> '**Except. III.** "But," say they again, "the Ephesians were not built upon Paul's writings, which we...'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'eye-salve'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'stout-hearted'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'stout-heartedness'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'such-like'` | 3 |
| `anomalies -> Hyphenation Anomalies -> 'top-stone'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> '..'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> '1 .'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '1st ,'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '1st .'` | 8 |
| `anomalies -> Punctuation Spacing Blemishes -> '2dly ,'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> '2dly .'` | 6 |
| `anomalies -> Punctuation Spacing Blemishes -> '3dly ,'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '3dly .'` | 7 |
| `anomalies -> Punctuation Spacing Blemishes -> '4thly ,'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> '5thly .'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> 'Ans .'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> 'Behold ,'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '1. ... 3.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '1. ... 4.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '10.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '12.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '13.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '16.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2.'` | 13 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 10.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 12.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 14.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 16.'` | 5 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 17.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 18.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 19.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 5.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 7.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '2. ... 8.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3.'` | 8 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 13.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 17.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 6.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 9.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '4.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '5.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '5. ... 15.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> '6.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> '8.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '9.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'III.'` | 2 |
| `text_integrity -> paragraph_splits -> —` | 22 |
| `text_integrity -> paragraph_splits -> John Owen` | 4 |
| `text_integrity -> paragraph_splits -> Your devoted Servant` | 2 |
| `text_integrity -> paragraph_splits -> AMPLISSIMO` | 2 |
| `text_integrity -> paragraph_splits -> SENATUI,` | 2 |
| `text_integrity -> paragraph_splits -> INCLYTISSIMO` | 2 |
| `text_integrity -> paragraph_splits -> OB` | 3 |
| `text_integrity -> paragraph_splits -> POTISSIMUM` | 2 |
| `text_integrity -> paragraph_splits -> PATRIAM (NEFARUS QUORUNDAM` | 2 |

### ❌ Unused Whitelist Entries
These entries matched zero raw issues. They should be deleted to keep the whitelist clean.

* `text_integrity -> ignored_warnings -> 'orphan_endnotes'`

---

## Detailed Trace by Category

### 1. Anomalies Whitelist

#### Category: `OCR & Bracket Residues`

No whitelist entries for this category.


#### Category: `Scanner Substring False Positives`

No whitelist entries for this category.


#### Category: `Unmatched Quotation Marks`

##### Entry: `(2.) Take heed of resting upon and trusting to the privilege` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**(2.) Take heed of resting upon and trusting to the privilege, however excellent and glorious, of the outward enjoyment o...**`

##### Entry: `SERMON 16.   AN HUMBLE TESTIMONY` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Sermon 16.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**SERMON 16.   AN HUMBLE TESTIMONY   UNTO THE GOODNESS AND SEVERITY OF GOD   IN HIS DEALING WITH SINFUL CHURCHES   AND NAT...**`

##### Entry: `The occasion on which this sermon was delivered is mentioned in the "Life the sermon, Owen appears t...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Sermon 1.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**The occasion on which this sermon was delivered is mentioned in the "Life the sermon, Owen appears to have been "ministe...**`

##### Entry: `Nothing so ill, but Christ [f58] will compensate. The greatest evil in the world is sin, and the gre...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**Nothing so ill, but Christ  will compensate. The greatest evil in the world is sin, and the greatest sin was the first; ...**`

##### Entry: `This is a seal upon their misery, without God's free mercy, like the stone laid upon the mouth of th...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**This is a seal upon their misery, without God's free mercy, like the stone laid upon the mouth of the cave by Joshua, to...**`

##### Entry: `The penal constitutions of the Judaical polity (for so they were, which yet I urge not) concerning i...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**The penal constitutions of the Judaical polity (for so they were, which yet I urge not) concerning idolaters, must be st...**`

##### Entry: `The word here used to express his sin, is "נֹקֵב, signifying also to pierce, and is twice so rendere...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**The word here used to express his sin, is "נֹקֵב, signifying also to pierce, and is twice so rendered —**`

##### Entry: `Hereupon he concludes that discourse with these two positive assertions: — First, That for what is p...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**Hereupon he concludes that discourse with these two positive assertions: — First, That for what is past, "every mouth mu...**`

##### Entry: `When God will do good for Zion, he requires that his remembrancers give him no rest, until he do it,...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Paragraph has unmatched double quotes (count: 17)`
      * Context: `**When God will do good for Zion, he requires that his remembrancers give him no rest, until he do it, Isaiah 62:7; and ye...**`

##### Entry: `When the beginning of the saints' departure from under the dominion of Antichrist was followed with...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Advantage of the Kingdom of Christ* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**When the beginning of the saints' departure from under the dominion of Antichrist was followed with wars, tumults, and d...**`

##### Entry: `See Nehemiah 4:1-6. And ever the nearer any nation is to this people, the greater is their envy. It...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**See Nehemiah 4:1-6. And ever the nearer any nation is to this people, the greater is their envy. It was Edom, and Moab, ...**`

##### Entry: `**Use 2.** Of encouragement to those that have the presence of Christ with them in the manner declar...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Paragraph has unmatched double quotes (count: 5)`
      * Context: `**Use 2. Of encouragement to those that have the presence of Christ with them in the manner declared; — they shall be safe...**`

##### Entry: `<section class="treatise-title-page" epub:type="titlepage"> <p class="title-line -major">SERMON 13.<...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**SERMON 13.   HOW WE MAY BRING OUR HEARTS   TO BEAR REPROOFS.    Let the righteous smite me, it shall be a kindness; and ...**`

##### Entry: `**Except. III.** "But," say they again, "the Ephesians were not built upon Paul's writings, which we...` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Except. III.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**Except. III. "But," say they again, "the Ephesians were not built upon Paul's writings, which were not then extant, but ...**`
    * **Chapter:** *Except. IV.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**Except. III. "But," say they again, "the Ephesians were not built upon Paul's writings, which were not then extant, but ...**`

##### Entry: `Secondly. "We cannot," say the Papists again, "know the Scripture to be the word of God _by the test...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**Secondly. "We cannot," say the Papists again, "know the Scripture to be the word of God by the testimony of the Spirit. ...**`

##### Entry: `**2.** That if the private testimony of the Spirit be questioned, it cannot be proved but by the Scr...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**2. That if the private testimony of the Spirit be questioned, it cannot be proved but by the Scripture; and so the Scrip...**`

##### Entry: `**2d** _. It is as destructive to our comfort._ When our great comfort proceeds from our faith, such...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Paragraph has unmatched double quotes (count: 17)`
      * Context: `**2d . It is as destructive to our comfort. When our great comfort proceeds from our faith, such as the one is, so will th...**`

##### Entry: `And, be sure, leave not off till thou find thy faith raised from so low a bottom as the authority of...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Paragraph has unmatched double quotes (count: 5)`
      * Context: `**And, be sure, leave not off till thou find thy faith raised from so low a bottom as the authority of men, and fixed on G...**`

##### Entry: `But Christ dealt not so with his apostles, though he were Lord of all, when he sent them to teach an...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.* — `Paragraph has unmatched double quotes (count: 13)`
      * Context: `**But Christ dealt not so with his apostles, though he were Lord of all, when he sent them to teach and baptize all nation...**`

##### Entry: `II. In the agitation which shook the country in consequence of this attempt, "a whole year," says Ma...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note (Sermon 7 — Advantage of the Kingdom of Christ)* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**II. In the agitation which shook the country in consequence of this attempt, "a whole year," says Macaulay, "elapsed, — ...**`

##### Entry: `Thirdly. Materials themselves will not serve: they must be fitly framed, and wisely disposed...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**Thirdly. Materials themselves will not serve: they must be fitly framed, and wisely disposed, or they will be a heap, no...**`

##### Entry: `**(1.)** _I will sup with him;"_ — I will delight and satisfy myself with him...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**(1.) I will sup with him;" — I will delight and satisfy myself with him. Jesus Christ takes abundance of delight and con...**`

##### Entry: `Use 2. Learn hence the vanity of resting upon outward church privileges, if we are not withal...` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**Use 2. Learn hence the vanity of resting upon outward church privileges, if we are not withal interested in this spiritu...**`

##### Entry: `In publico discrimine omnis homo miles est."` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Sermon 16.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**In publico discrimine omnis homo miles est."**`


#### Category: `Hyphenation Anomalies`

##### Entry: `ANGLO-BRITANNORUM` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note.* — `Capitalized hyphenation with unrecognized left particle`
      * Context: `... LYTISSIMO POPULI ANGLICANI CONVENTUI, OB PRISCA **ANGLO-BRITANNORUM** JURA STRENUE ET FIDELITER ASSERTA; LIBERTATEM PAT ...`

##### Entry: `Beerlahai-roi` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Capitalized hyphenation with unrecognized left particle`
      * Context: `... They may call every spring of their refreshment, **Beerlahai-roi** [The well of Him that liveth and seeth me]. (2dl ...`

##### Entry: `Christ-purchased` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Capitalized hyphenation with unrecognized right particle`
      * Context: `... sad reckoning. (2.) In point of ordinances, and **Christ-purchased** privileges. Here it is dangerous encroaching inde ...`

##### Entry: `Jehovah-nissi` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Capitalized hyphenation with unrecognized right particle`
      * Context: `... in that work, did never sacrifice at the altar of **Jehovah-nissi**, nor consider that the Lord hath sworn to have wa ...`

##### Entry: `Sabbath-breaker` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Splittable word (rejoins to valid word 'Sabbathbreaker')`
      * Context: `... mpieties; for were a man a drunkard, a swearer, a **Sabbath-breaker**, an unclean person, so he were no Puritan, and ha ...`

##### Entry: `after-reckoning` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Splittable word (rejoins to valid word 'afterreckoning')`
      * Context: `... promote the service of God. Let them not fear an **after-reckoning** who use the discipline of Christ according to his ...`

##### Entry: `busy-body` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `Splittable word (rejoins to valid word 'busybody')`
      * Context: `... so to do, unless he design the just reproach of a **busy-body** for his reward. The command is general, with resp ...`

##### Entry: `co-action` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Splittable word (rejoins to valid word 'coaction')`
      * Context: `... s discourse, I shall, as to any ways of corporeal **co-action** and restraint, oppose some few things. 1st . The ...`

##### Entry: `co-partner` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Splittable word (rejoins to valid word 'copartner')`
      * Context: `... le. That herein the Holy One of Israel is no ways **co-partner** with the guilt of the sons of men, will appear by ...`

##### Entry: `deutero-canonical` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Splittable word (rejoins to valid word 'deuterocanonical')`
      * Context: `... Papists to the Old Testament, and called by them "**deutero-canonical**," and by us no better still than "apocryphal," su ...`

##### Entry: `evil-doer` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'evildoer')`
      * Context: `... God, wound Jesus Christ, and prosecute him as an **evil-doer**? I know the usual colors, the common pleas, that ...`

##### Entry: `eye-salve` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Splittable word (rejoins to valid word 'eyesalve')`
      * Context: `... en know not that they are blind, and seek not for **eye-salve**; they know not that they are dead, and seek not f ...`
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Splittable word (rejoins to valid word 'eyesalve')`
      * Context: `... dviseth the church of Laodicea to come to him for **eye-salve**, that she might see, Revelation 3:18. At his comi ...`

##### Entry: `foot-breadth` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.* — `Splittable word (rejoins to valid word 'footbreadth')`
      * Context: `... rights or enjoyments, nor gave to his apostles a **foot-breadth** of inheritance among them. But upon this grant, t ...`

##### Entry: `fore-cited` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'forecited')`
      * Context: `... odus 14:21; which the prophet also admires in the **fore-cited** psalm: "The sea saw it, and fled. What ailed thee ...`

##### Entry: `fore-named` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Splittable word (rejoins to valid word 'forenamed')`
      * Context: `... d let this be spoken to the third argument of the **fore-named** reverend persons, from the analogy of delinquenci ...`

##### Entry: `fore-signify` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'foresignify')`
      * Context: `... unt of these things, as they were to foretell and **fore-signify** the fatal destruction of Jerusalem, is given us b ...`

##### Entry: `god-like` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.* — `Splittable word (rejoins to valid word 'godlike')`
      * Context: `... st, and good: but, since the ascription of such a **god-like** authority unto men, as to secure blind obedience ...`
      * Context: `... emolish this cursed image, or the ascription of a **god-like** power unto men to require blind obedience unto th ...`

##### Entry: `hard-heartedness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Splittable word (rejoins to valid word 'hardheartedness')`
      * Context: `... s their actual unbelief to be the effect of their **hard-heartedness**; which, though it might be judicial, they being l ...`

##### Entry: `hog-sty` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Splittable word (rejoins to valid word 'hogsty')`
      * Context: `... dwells in a stately palace of his own, show him a **hog-sty**, tell him, "This is your house; here you dwell; t ...`

##### Entry: `home-bred` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'homebred')`
      * Context: `... have wanted them one day longer. Farther, these **home-bred** eruptions were timely seasoned, to rouse the disc ...`

##### Entry: `how-ever` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.* — `Splittable word (rejoins to valid word 'however')`
      * Context: `... be its efficacy unto all the proper ends of it — **how-ever** it be ordered according unto the prescription of ...`

##### Entry: `lion-like` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'lionlike')`
      * Context: `... iver me from the mouth of the lion," — Nero, that **lion-like** tyrant. And what then? "He shall deliver me from ...`

##### Entry: `mitred-confirmations` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... g and pursuing their unjust conquests, or foolish **mitred-confirmations** of sword-purchases, he got them all framed to his ...`

##### Entry: `non-submission` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Splittable word (rejoins to valid word 'nonsubmission')`
      * Context: `... them with any civil penalty in case of refusal or **non-submission**; nor yet did I ever in my life meet with any thin ...`

##### Entry: `over-neglect` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'overneglect')`
      * Context: `... zeal, what exercise of all gospel grace, with the **over-neglect** of these things among many, — it would take up a ...`

##### Entry: `over-numerous` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Chamber of Imagery in the Church of Rome Laid Open.* — `Splittable word (rejoins to valid word 'overnumerous')`
      * Context: `... ey call them, or a surcharge of friars from their **over-numerous** fraternities, upon their errands into remote nati ...`

##### Entry: `pole-star` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Splittable word (rejoins to valid word 'polestar')`
      * Context: `... ll not wonder if you err in your ways. It is your **pole-star**, and will be so, by which your whole course is to ...`
      * Context: `... my directions: — (2.) Make this work of God your **pole-star**, that you may steer and guide your course by it. ...`

##### Entry: `pre-conceptions` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Short Defensative* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... able, if men would but a little lay aside beloved **pre-conceptions**. But the printer stays for every line; only I mus ...`

##### Entry: `pre-discoveries` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... r. The prophet having had visions from God, and **pre-discoveries** of many approaching judgments, in the first and s ...`

##### Entry: `pre-imaginations` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... yet being come, because not accommodated to their **pre-imaginations**, they rejected him, as having neither form nor co ...`

##### Entry: `pre-required` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... itherto taken care for us. This, then, I say, is **pre-required**, as a qualification of any person to the performa ...`

##### Entry: `pre-supposeth` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... f the gospel, but not the sending of it, which it **pre-supposeth**: secondly, Against the covenant they are under, a ...`

##### Entry: `sea-shore` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `Splittable word (rejoins to valid word 'seashore')`
      * Context: `... ied like the stars of heaven and the sands of the **sea-shore**, shall possess the gates of their enemies, and sh ...`

##### Entry: `shittim-wood` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Splittable word (rejoins to valid word 'shittimwood')`
      * Context: `... r remission were offered. The other less, made of **shittim-wood**, all overlaid with pure gold, and a crown of beat ...`

##### Entry: `short-sighted` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Splittable word (rejoins to valid word 'shortsighted')`
      * Context: `... ence to them may lie therein. Alas! we are poor, **short-sighted** creatures; we know nothing that is before us, — m ...`

##### Entry: `sick-bed` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'sickbed')`
      * Context: `... mfortable and full of joy. Store thy cottage, thy **sick-bed**, by faith, with all sorts of mercies; they are th ...`

##### Entry: `slaughter-house` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'slaughterhouse')`
      * Context: `... o a prison, a crown into a cottage, Christ into a **slaughter-house**. And this arises, — [1.] From the nature of fait ...`

##### Entry: `stout-hearted` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'stoutheartedness')`
      * Context: `... ections may be made use of: — First. Take heed of **stout-heartedness**, and a contempt or neglect thereby of divine warn ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... ections may be made use of: — First. Take heed of **stout-hearted**ness, and a contempt or neglect thereby of divine ...`
      * Context: `... either really or in pretense, are bold, fearless, **stout-hearted**, regardless of these things; they seem to provoke ...`

##### Entry: `stout-heartedness` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'stoutheartedness')`
      * Context: `... ections may be made use of: — First. Take heed of **stout-heartedness**, and a contempt or neglect thereby of divine warn ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... ections may be made use of: — First. Take heed of **stout-hearted**ness, and a contempt or neglect thereby of divine ...`
      * Context: `... either really or in pretense, are bold, fearless, **stout-hearted**, regardless of these things; they seem to provoke ...`

##### Entry: `such-like` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Splittable word (rejoins to valid word 'suchlike')`
      * Context: `... ss of blood: — all these, I say, and sundry other **such-like** things as these, are "the Lord's doing, and marve ...`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Splittable word (rejoins to valid word 'suchlike')`
      * Context: `... there a backsliding upon your spirit to these, or **such-like** things as these, the Lord will walk contrary to y ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `Splittable word (rejoins to valid word 'suchlike')`
      * Context: `... ng the best cause, as they suppose; and with many **such-like** notions are the minds of men possessed. But the t ...`

##### Entry: `top-stone` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Splittable word (rejoins to valid word 'topstone')`
      * Context: `... maninvented worship, but either the foundation or **top-stone** is laid in the blood of God's people. "The wisdom ...`
    * **Chapter:** *The Laboring Saint's Dismission to Rest.* — `Splittable word (rejoins to valid word 'topstone')`
      * Context: `... as very rare, who saw the foundation and also the **top-stone** of the temple laid; and yet the work of Jerusalem ...`

##### Entry: `under-propping` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Splittable word (rejoins to valid word 'underpropping')`
      * Context: `... antics under the windows, that make some show of **under-propping** it: — here you have a magistrate, there an army, ...`


#### Category: `Punctuation Spacing Blemishes`

##### Entry: `..` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Duplicate period (double dot)`
      * Context: `**..**. ith their only supporters and means of deliverance**..** Jeremiah had labored with God for them, and with **..**.`
    * **Chapter:** *Of Toleration;* — `Duplicate period (double dot)`
      * Context: `**..**. and Eunomians, Sozom. Ecclesiastes Hist., lib. vii**..** cap. 1. Many more the like examples might be pro **..**.`

##### Entry: `1 .` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced period (space before period)`
      * Context: `... example. These things being presupposed, — Use **1 .** Let no flesh glory in themselves, but let every m ...`
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Spaced period (space before period)`
      * Context: `... n part touched before; I shall add but two more. **1 .** Discontentment with our peculiar lot and portion ...`
    * **Chapter:** *The Testimony of the Church Is Not the Only Nor the Chief Reaso* — `Spaced period (space before period)`
      * Context: `... agree with them; 2. In some we differ from them. **1 .** In some we agree. (1.) That the scripture of the ...`

##### Entry: `1st ,` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced punctuation (space before character)`
      * Context: `... iration, and a little after violently assaulted. **1st ,** In the first way, how do we find the Jews putting ...`
    * **Chapter:** *Of Toleration;* — `Spaced punctuation (space before character)`
      * Context: `... rranted zeal. Now, concerning these, I affirm, — **1st ,** That the magistrate ought not to make provision o ...`
      * Context: `... truth so owned, as before, and act accordingly. **1st ,** For the first of these, or such as dissent about ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced punctuation (space before character)`
      * Context: `... offense, in these few ensuing considerations: — **1st ,** Then, I shall willingly lay this down for a princ ...`

##### Entry: `1st .` (⚠️ Greedy)
  * Silenced 8 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced period (space before period)`
      * Context: `... f, there are sundry things gratis assumed; as, — **1st .** That it is known and confessed what articles in r ...`
      * Context: `... co-action and restraint, oppose some few things. **1st .** The non-constitution of a judge in case of heresy ...`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Spaced period (space before period)`
      * Context: `... is often spoken of, seldom driven to any close! **1st .** Pray. "Pray the Lord of the harvest, that he woul ...`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced period (space before period)`
      * Context: `... greatness or power; which he sets out two ways. **1st .** Absolutely, as he is God, to be "blessed for ever ...`
      * Context: `... ly , Sinful follies; 4thly , Sinful negligence. **1st .** Sinful cares, — anxious and dubious thoughts abou ...`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `Spaced period (space before period)`
      * Context: `... the present, these brief directions following: — **1st .** Labor to be fully persuaded in your own minds, th ...`
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced period (space before period)`
      * Context: `... few things that are signally required thereunto. **1st .** That they inquire of God, ask counsel at his hand ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced period (space before period)`
      * Context: `... ended as to the substance of the mercy promised. **1st .** For the figure; by the "glory" and "defense," a d ...`
      * Context: `... uation pleaded for be cast? To this I answer, — **1st .** Some do say so, and plead thus, it cannot be deni ...`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `Spaced period (space before period)`
      * Context: `... nsidered, that it may not be unuseful unto us: — **1st .** The circumstances of the reprover; as, first, Whe ...`
    * **Chapter:** *Except.* — `Spaced period (space before period)`
      * Context: `... aith, and comfort, and obedience, all at once: — **1st .** It is destructive to our faith. It leaves us no f ...`

##### Entry: `2 .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced period (space before period)`
      * Context: `... te's duty can be stretched to cover them. Reason **2 .** Neither party, I am persuaded, in their retired t ...`

##### Entry: `2d .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Spaced period (space before period)`
      * Context: `... eived them, when the rest are, because she hath. **2d .** It is as destructive to our comfort. When our gre ...`

##### Entry: `2dly ,` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced punctuation (space before character)`
      * Context: `... the martyrs of Jesus that suffered amongst them! **2dly ,** After some continuance. So the Church of Laodicea ...`
      * Context: `... and glorious fancies, became head of that fatal **2dly ,** After some continuance. So the Church of Laodicea ...`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced punctuation (space before character)`
      * Context: `... lly in four sinful things: — 1st, Sinful cares; **2dly ,** Sinful fears; 3dly , Sinful follies; 4thly , Si ...`

##### Entry: `2dly .` (⚠️ Greedy)
  * Silenced 6 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced period (space before period)`
      * Context: `... t do. Now, it cannot be his duty to further sin. **2dly .** Outward monuments — ways of declaring and holding ...`
      * Context: `... tions sufficient to make an article fundamental. **2dly .** That the persons holding the error are convinced, ...`
      * Context: `... ed in this case, I refer to another opportunity. **2dly .** Gospel constitutions in the case of heresy or err ...`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Spaced period (space before period)`
      * Context: `... into the fields that are white for the harvest. **2dly .** Make such provision, that those who will go may b ...`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced period (space before period)`
      * Context: `... into the hands of the living God," chap. 10:31. **2dly .** Comparatively, as he is the mediator of the new c ...`
      * Context: `... quaintedness with the work and mind of the Lord. **2dly .** Sinful fears. Luke 21:28, our Savior having told ...`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `Spaced period (space before period)`
      * Context: `... ion of them whom God will spew out of his mouth. **2dly .** Know that error and falsehood have no fight or ti ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced period (space before period)`
      * Context: `... hat is here expressed as to the type and figure; **2dly .** What is here intended as to the substance of the ...`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `Spaced period (space before period)`
      * Context: `... are reproved for that whereof we are not guilty. **2dly .** Consider aright the difference between a reproof ...`

##### Entry: `3d .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Spaced period (space before period)`
      * Context: `... tainties for the very foundation of their faith. **3d .** It is as destructive to our obedience as to eithe ...`

##### Entry: `3dly ,` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced punctuation (space before character)`
      * Context: `... ot professedly found in any party amongst us. **3dly ,** Which was worst of all, they had centred in their ...`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced punctuation (space before character)`
      * Context: `... ngs: — 1st, Sinful cares; 2dly , Sinful fears; **3dly ,** Sinful follies; 4thly , Sinful negligence. 1st ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced punctuation (space before character)`
      * Context: `... om owning the portion and inheritance of Christ! **3dly ,** It cannot be denied, but that many of them who do ...`

##### Entry: `3dly .` (⚠️ Greedy)
  * Silenced 7 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced period (space before period)`
      * Context: `... ht forth to the joy of all the children of Zion. **3dly .** Sundry other arguments, taken from the nature of ...`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Spaced period (space before period)`
      * Context: `... is be the business of an unpursued order. But, — **3dly .** Let some be appointed (generals die and sink by t ...`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced period (space before period)`
      * Context: `... ll things working together to the appointed end. **3dly .** Sinful follies. Toil and labor in vain is, of all ...`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `Spaced period (space before period)`
      * Context: `... nor morally they are a disturbance unto others. **3dly .** Know that in things of practice, so of persuasion ...`
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced period (space before period)`
      * Context: `... sting of him in reference to special protection. **3dly .** A third thing I should fix upon is, a people's un ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced period (space before period)`
      * Context: `... ," they will flourish again in peace and beauty. **3dly .** Let not Satan cheat you of your duty by this triv ...`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `Spaced period (space before period)`
      * Context: `... and if it be false, it is, moreover, a calumny. **3dly .** Where a man, in such cases, is fully justified by ...`

##### Entry: `4thly ,` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced punctuation (space before character)`
      * Context: `... s; 2dly , Sinful fears; 3dly , Sinful follies; **4thly ,** Sinful negligence. 1st . Sinful cares, — anxious ...`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced punctuation (space before character)`
      * Context: `... miscarriages of others, have most of their own. **4thly ,** That differences of judgments, in civil affairs o ...`

##### Entry: `4thly .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced period (space before period)`
      * Context: `... r;" and all because they discern not the season. **4thly .** Sinful negligence. You are no way able to do the ...`

##### Entry: `5thly ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced punctuation (space before character)`
      * Context: `... on such accounts, it is because they will be so. **5thly ,** This hath ever been the way of the men of the wor ...`

##### Entry: `5thly .` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Spaced period (space before period)`
      * Context: `... his own, — hardening whom he will, Romans 9:18. **5thly .** He positively sends upon their understandings tha ...`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `Spaced period (space before period)`
      * Context: `... rience what will be the issue of such allowance. **5thly .** I shall only propose one thing more to your consi ...`

##### Entry: `6 ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced punctuation (space before character)`
      * Context: `... accordingly performed this duty, 2 Chronicles 17:**6 ,** 30:14, are enough to confirm it, and to bottom th ...`

##### Entry: `6thly ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `Spaced punctuation (space before character)`
      * Context: `... power of grace, harden themselves to their ruin. **6thly ,** This remnant of Christ, with whom his presence is ...`

##### Entry: `6thly .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Spaced period (space before period)`
      * Context: `... give them up to contend with their only helpers. **6thly .** Suitably upon the will and affections he hath sev ...`

##### Entry: `Ans .` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Except. III.* — `Spaced period (space before period)`
      * Context: `... g, together with the apostles', they were built. **Ans .** The preaching [of] the truth, or writing it, make ...`
    * **Chapter:** *Except. IV.* — `Spaced period (space before period)`
      * Context: `... g, together with the apostles', they were built. **Ans .** The preaching [of] the truth, or writing it, make ...`

##### Entry: `Behold ,` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced punctuation (space before character)`
      * Context: `... 13:41, Paul concludes his sermon to thorn with, "**Behold ,** ye despisers, and wonder, and perish;" — and vers ...`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Spaced punctuation (space before character)`
      * Context: `... e curse of a professing people at the same time. "**Behold ,** I and the children whom God hath given me, are fo ...`

##### Entry: `Colchester ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Spaced punctuation (space before character)`
      * Context: `... neral mercies we have received . The surrender of **Colchester ,** the particular celebrated this day, though marchi ...`

##### Entry: `D .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Prefatory Note.* — `Spaced period (space before period)`
      * Context: `... nder their handwriting. H. ELSYINGE, Cler. Parl. **D .** Com.`

##### Entry: `First .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced period (space before period)`
      * Context: `... gs are, then, principally to be inquired into: — **First .** What it is for God to be with any people. Secondl ...`

##### Entry: `Obj .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `Spaced period (space before period)`
      * Context: `... their own deliverers, if ever they be delivered. **Obj .** But is not a people's contending with the instrum ...`

##### Entry: `Observation .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced period (space before period)`
      * Context: `... ristian consideration this following position: — **Observation .** The Lord Jesus Christ, by his mighty power, in th ...`

##### Entry: `Secondly .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced period (space before period)`
      * Context: `... First . What it is for God to be with any people. **Secondly .** What it is for a people to be or abide with God. ...`

##### Entry: `V .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `Spaced period (space before period)`
      * Context: `... church, because she says she is the church. Arg. **V .** If we are to believe the divinity of the Scriptur ...`

##### Entry: `Zion ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Spaced punctuation (space before character)`
      * Context: `... the work of God. "The Lord hath founded Zion;" — **Zion ,** that is, his church, his people, his chosen ones, ...`

##### Entry: `continuance .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced period (space before period)`
      * Context: `... patience, long-suffering, and forbearance in the **continuance .** He bears with our manners, whilst we grieve his S ...`

##### Entry: `e  )` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Vision of Unchangeable, Free Mercy, in Sending the Means of G* — `Spaced closing parenthesis`
      * Context: `... g how this vial was poured out upon the very throne ), and then let us all be ashamed and confounded in ...`

##### Entry: `experience .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Of Toleration;* — `Spaced period (space before period)`
      * Context: `... uthority. It is but too clearly made out by daily **experience .** If they close with them, they are "custodes utriu ...`

##### Entry: `founded ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `Spaced punctuation (space before character)`
      * Context: `... rdinances of worship. This God "hath founded;" — **founded ,** or established, strengthened, that it shall not b ...`

##### Entry: `in ;` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `Spaced punctuation (space before character)`
      * Context: `... the vine. "God," saith he, "is able to graft them **in ;**" though now they seem as dead bones, yet the Lord ...`

##### Entry: `peace .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced period (space before period)`
      * Context: `... f Christ: our being with God is in him who is our **peace .** Two cannot walk together, unless they be agreed, ...`

##### Entry: `pieces .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `Spaced period (space before period)`
      * Context: `... hidden, against which they dash themselves all to **pieces .** I say, then, Christ, as the foundation of this ho ...`

##### Entry: `pretences ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `Spaced punctuation (space before character)`
      * Context: `... e Pharisees' hypocrisy, notwithstanding all their **pretences ,** and possession of Moses' chair, that they were wi ...`

##### Entry: `received .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `Spaced period (space before period)`
      * Context: `... our trust. I speak of the general mercies we have **received .** The surrender of Colchester , the particular cele ...`

##### Entry: `s  )` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Country Essay* — `Spaced closing parenthesis`
      * Context: `... nasius and others in the east deposed by the Arians ). Now, who would not have thought, that his standi ...`

##### Entry: `say ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced punctuation (space before character)`
      * Context: `... ffice as an instance in every kind. But you will **say ,** How shall we inquire of God? The nations had the ...`

##### Entry: `supposition :` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `Spaced punctuation (space before character)`
      * Context: `... hetical propositions, or promissory assertions on **supposition :** — "If you abide with the Lord, he will be with yo ...`

##### Entry: `you ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *To the Worthy and Honored Sir William Masham, Sir William Rowe,* — `Spaced punctuation (space before character)`
      * Context: `... fear but that that God who hath so appeared with **you ,** and for you, will so indulge to your spirits the ...`


#### Category: `Structural Nesting Sequence Jumps`

##### Entry: `1. ... 20.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 1 to 20)`

##### Entry: `1. ... 3.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *Of Toleration;* — `List sequence jump (skipped from 1 to 3)`

##### Entry: `1. ... 4.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 1 to 4)`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `List sequence starts at 4 instead of 1`
      * Context: `SERMON **4.** THE STEADFASTNESS OF THE PROMISES, AND THE SI ...`
      * Context: `... and conclusions, to the end of verse 17, chapter **4.** Having laid down this, in the next place he give ...`
      * Context: `... ll, to lie down quietly in God's allsufficiency. **4.** The last is, that "he staggered not," verse 20. T ...`

##### Entry: `10.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 10)`
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `List sequence starts at 10 instead of 1`
      * Context: `SERMON **10.** GOD'S WORK IN FOUNDING ZION, AND HIS PEOPLE'S ...`

##### Entry: `11.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *God's Presence With a People the Spring of Their Prosperity.* — `List sequence starts at 11 instead of 1`
      * Context: `SERMON **11.** GOD'S PRESENCE WITH A PEOPLE THE SPRING OF TH ...`

##### Entry: `12.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 12)`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `List sequence starts at 12 instead of 1`
      * Context: `SERMON **12.** THE GLORY AND INTEREST OF NATIONS PROFESSING ...`
      * Context: `... number; yea, very few, and strangers," Psalm 105:**12.** You know what it cost David in being seduced by S ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `13.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 13)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `List sequence starts at 13 instead of 1`
      * Context: `SERMON **13.** HOW WE MAY BRING OUR HEARTS TO BEAR REPROOFS. ...`
      * Context: `... and cutting manner," 2 Corinthians 13:10; Titus 1:**13.** But with respect unto their use, benefit, and adv ...`

##### Entry: `16.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 16)`
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `List sequence starts at 6 instead of 1`
      * Context: `SERMON **6.** THE BRANCH OF THE LORD THE BEAUTY OF ZION: OR ...`
      * Context: `... ious corner-stone, a sure foundation," Isaiah 28:1**6.** Now, this foundation is no other but the rock upo ...`
      * Context: `... his own house, whose house are we," Hebrews 3:5, **6.** And that you may see that he doth not own it as ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence starts at 16 instead of 1`
      * Context: `SERMON **16.** AN HUMBLE TESTIMONY UNTO THE GOODNESS AND SEV ...`
      * Context: `... te described by the apostle, 1 Thessalonians 2:14-**16.** But it may be said, If their destruction was so ...`
      * Context: `... ith his people as the angel dealt with Lot, verse **16.** They are apt to linger, and know not how to leave ...`

##### Entry: `2.` (⚠️ Greedy)
  * Silenced 13 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 17)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 5)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 7)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 8)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 10)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 12)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 14)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 16)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 18)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 19)`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `List sequence starts at 12 instead of 1`
      * Context: `SERMON **12.** THE GLORY AND INTEREST OF NATIONS PROFESSING ...`
      * Context: `... number; yea, very few, and strangers," Psalm 105:**12.** You know what it cost David in being seduced by S ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 10.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 10)`
    * **Chapter:** *God's Work in Founding Zion, and His Peopleìs Duty Thereupon.* — `List sequence starts at 10 instead of 1`
      * Context: `SERMON **10.** GOD'S WORK IN FOUNDING ZION, AND HIS PEOPLE'S ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 12.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 12)`
    * **Chapter:** *The Glory and Interest of Nations Professing the Gospel.* — `List sequence starts at 12 instead of 1`
      * Context: `SERMON **12.** THE GLORY AND INTEREST OF NATIONS PROFESSING ...`
      * Context: `... number; yea, very few, and strangers," Psalm 105:**12.** You know what it cost David in being seduced by S ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 14.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 14)`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `List sequence starts at 4 instead of 1`
      * Context: `SERMON **4.** THE STEADFASTNESS OF THE PROMISES, AND THE SI ...`
      * Context: `... and conclusions, to the end of verse 17, chapter **4.** Having laid down this, in the next place he give ...`
      * Context: `... ll, to lie down quietly in God's allsufficiency. **4.** The last is, that "he staggered not," verse 20. T ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 16.` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 16)`
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `List sequence starts at 6 instead of 1`
      * Context: `SERMON **6.** THE BRANCH OF THE LORD THE BEAUTY OF ZION: OR ...`
      * Context: `... ious corner-stone, a sure foundation," Isaiah 28:1**6.** Now, this foundation is no other but the rock upo ...`
      * Context: `... his own house, whose house are we," Hebrews 3:5, **6.** And that you may see that he doth not own it as ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence starts at 16 instead of 1`
      * Context: `SERMON **16.** AN HUMBLE TESTIMONY UNTO THE GOODNESS AND SEV ...`
      * Context: `... te described by the apostle, 1 Thessalonians 2:14-**16.** But it may be said, If their destruction was so ...`
      * Context: `... ith his people as the angel dealt with Lot, verse **16.** They are apt to linger, and know not how to leave ...`

##### Entry: `2. ... 17.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 17)`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 18.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 18)`
    * **Chapter:** *The Laboring Saint's Dismission to Rest.* — `List sequence starts at 8 instead of 1`
      * Context: `SERMON **8.** THE LABORING SAINT'S DISMISSION TO REST. "But ...`
      * Context: `... a man to be "weary and heavy laden," Matthew 11:2**8.** This oftentimes makes the inhabitants of Zion say ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 19.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 19)`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `List sequence starts at 9 instead of 1`
      * Context: `SERMON **9.** CHRIST'S KINGDOM AND THE MAGISTRATE'S POWER. ...`
      * Context: `... pt of the gospel, 2 Corinthians 2:16; Hebrews 10:2**9.** He sends his Spirit to convince even the perishin ...`
      * Context: `... gh never so glorious and excellent, Revelation 22:**9.** 2dly. For Satan, as he came to bind the strong m ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 5.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 5)`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `List sequence starts at 5 instead of 1`
      * Context: `SERMON **5.** THE SHAKING AND TRANSLATING OF HEAVEN AND EAR ...`
      * Context: `... al states; as Isaiah 14:12-15; Jeremiah 15:9, 51:2**5.** (Isaiah 13:13; Psalm 68:8; Joel 2:10; Revelation ...`
      * Context: `... lation 1:14-17, as also chapter 4 and chapter 11:1**5.** And both these may be again considered two ways. ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 7.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 7)`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `2. ... 8.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence starts at 2 instead of 1`
      * Context: `SERMON **2.** A MEMORIAL OF THE DELIVERANCE OF ESSEX COUNTY ...`
      * Context: `... Secondly, The prophet's main request in it, verse **2.** Thirdly, Arguments to sustain his faith in that ...`
      * Context: `... is way to the rock of our salvation. Observation **2.** Prophets' discoveries of fearful judgments must b ...`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 8)`
    * **Chapter:** *The Laboring Saint's Dismission to Rest.* — `List sequence starts at 8 instead of 1`
      * Context: `SERMON **8.** THE LABORING SAINT'S DISMISSION TO REST. "But ...`
      * Context: `... a man to be "weary and heavy laden," Matthew 11:2**8.** This oftentimes makes the inhabitants of Zion say ...`
    * **Chapter:** *Except. II.* — `List sequence starts at 2 instead of 1`
      * Context: `... prophets and Moses did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and ...`
      * Context: `... es did say should come," Acts 26:2**2.** So Acts 17. **2.** The preaching of the apostles and prophets did la ...`
      * Context: `... the good knowledge of the Lord," 2 Chronicles 30:2**2.**`

##### Entry: `3.` (⚠️ Greedy)
  * Silenced 8 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 9)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 13)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 17)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence jump (skipped from 3 to 6)`
    * **Chapter:** *Of Toleration;* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `List sequence starts at 13 instead of 1`
      * Context: `SERMON **13.** HOW WE MAY BRING OUR HEARTS TO BEAR REPROOFS. ...`
      * Context: `... and cutting manner," 2 Corinthians 13:10; Titus 1:**13.** But with respect unto their use, benefit, and adv ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence jump (skipped from 3 to 9)`

##### Entry: `3. ... 13.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 13)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *How We May Bring Our Hearts to Bear Reproofs.* — `List sequence starts at 13 instead of 1`
      * Context: `SERMON **13.** HOW WE MAY BRING OUR HEARTS TO BEAR REPROOFS. ...`
      * Context: `... and cutting manner," 2 Corinthians 13:10; Titus 1:**13.** But with respect unto their use, benefit, and adv ...`

##### Entry: `3. ... 17.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 17)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`

##### Entry: `3. ... 6.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence jump (skipped from 3 to 6)`
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `List sequence starts at 6 instead of 1`
      * Context: `SERMON **6.** THE BRANCH OF THE LORD THE BEAUTY OF ZION: OR ...`
      * Context: `... ious corner-stone, a sure foundation," Isaiah 28:1**6.** Now, this foundation is no other but the rock upo ...`
      * Context: `... his own house, whose house are we," Hebrews 3:5, **6.** And that you may see that he doth not own it as ...`

##### Entry: `3. ... 9.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 9)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence starts at 3 instead of 1`
      * Context: `SERMON **3.** RIGHTEOUS ZEAL ENCOURAGED BY DIVINE PROTECTIO ...`
      * Context: `... s just and righteous See verse 6 of this chapter. **3.** Because the people, by virtue of their retained s ...`
      * Context: `... s for Baal, and a grove, as did Ahab," 2 Kings 21:**3.** (2.) Cruelty: "He shed innocent blood very much, ...`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `List sequence starts at 9 instead of 1`
      * Context: `SERMON **9.** CHRIST'S KINGDOM AND THE MAGISTRATE'S POWER. ...`
      * Context: `... pt of the gospel, 2 Corinthians 2:16; Hebrews 10:2**9.** He sends his Spirit to convince even the perishin ...`
      * Context: `... gh never so glorious and excellent, Revelation 22:**9.** 2dly. For Satan, as he came to bind the strong m ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence jump (skipped from 3 to 9)`

##### Entry: `4.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 1 to 4)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 14)`
    * **Chapter:** *The Steadfastness of the Promises, and the Sinfulness of Stagge* — `List sequence starts at 4 instead of 1`
      * Context: `SERMON **4.** THE STEADFASTNESS OF THE PROMISES, AND THE SI ...`
      * Context: `... and conclusions, to the end of verse 17, chapter **4.** Having laid down this, in the next place he give ...`
      * Context: `... ll, to lie down quietly in God's allsufficiency. **4.** The last is, that "he staggered not," verse 20. T ...`

##### Entry: `5.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 5)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 5 to 15)`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `List sequence starts at 5 instead of 1`
      * Context: `SERMON **5.** THE SHAKING AND TRANSLATING OF HEAVEN AND EAR ...`
      * Context: `... al states; as Isaiah 14:12-15; Jeremiah 15:9, 51:2**5.** (Isaiah 13:13; Psalm 68:8; Joel 2:10; Revelation ...`
      * Context: `... lation 1:14-17, as also chapter 4 and chapter 11:1**5.** And both these may be again considered two ways. ...`

##### Entry: `5. ... 15.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 5 to 15)`
    * **Chapter:** *The Shaking and Translating of Heaven and Earth* — `List sequence starts at 5 instead of 1`
      * Context: `SERMON **5.** THE SHAKING AND TRANSLATING OF HEAVEN AND EAR ...`
      * Context: `... al states; as Isaiah 14:12-15; Jeremiah 15:9, 51:2**5.** (Isaiah 13:13; Psalm 68:8; Joel 2:10; Revelation ...`
      * Context: `... lation 1:14-17, as also chapter 4 and chapter 11:1**5.** And both these may be again considered two ways. ...`

##### Entry: `6.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 16)`
    * **Chapter:** *Righteous Zeal Encouraged by Divine Protection.* — `List sequence jump (skipped from 3 to 6)`
    * **Chapter:** *The Branch of the Lord the Beauty of Zion: Or, the Glory of the* — `List sequence starts at 6 instead of 1`
      * Context: `SERMON **6.** THE BRANCH OF THE LORD THE BEAUTY OF ZION: OR ...`
      * Context: `... ious corner-stone, a sure foundation," Isaiah 28:1**6.** Now, this foundation is no other but the rock upo ...`
      * Context: `... his own house, whose house are we," Hebrews 3:5, **6.** And that you may see that he doth not own it as ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence starts at 16 instead of 1`
      * Context: `SERMON **16.** AN HUMBLE TESTIMONY UNTO THE GOODNESS AND SEV ...`
      * Context: `... te described by the apostle, 1 Thessalonians 2:14-**16.** But it may be said, If their destruction was so ...`
      * Context: `... ith his people as the angel dealt with Lot, verse **16.** They are apt to linger, and know not how to leave ...`

##### Entry: `8.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 8)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 18)`
    * **Chapter:** *The Laboring Saint's Dismission to Rest.* — `List sequence starts at 8 instead of 1`
      * Context: `SERMON **8.** THE LABORING SAINT'S DISMISSION TO REST. "But ...`
      * Context: `... a man to be "weary and heavy laden," Matthew 11:2**8.** This oftentimes makes the inhabitants of Zion say ...`

##### Entry: `9.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 3 to 9)`
    * **Chapter:** *A Memorial of the Deliverance of Essex County, and Committee.* — `List sequence jump (skipped from 2 to 19)`
    * **Chapter:** *Christ's Kingdom and the Magistrate's Power.* — `List sequence starts at 9 instead of 1`
      * Context: `SERMON **9.** CHRIST'S KINGDOM AND THE MAGISTRATE'S POWER. ...`
      * Context: `... pt of the gospel, 2 Corinthians 2:16; Hebrews 10:2**9.** He sends his Spirit to convince even the perishin ...`
      * Context: `... gh never so glorious and excellent, Revelation 22:**9.** 2dly. For Satan, as he came to bind the strong m ...`
    * **Chapter:** *An Humble Testimony Unto the Goodness and Severity of God in Hi* — `List sequence jump (skipped from 3 to 9)`

##### Entry: `I. ... IX.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `List sequence jump (skipped from 1 to 9)`

##### Entry: `III.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Except. III.* — `List sequence starts at 3 instead of 1`
      * Context: `Except. **III.** "But," say they again, "the Ephesians were not bu ...`
    * **Chapter:** *Except. IV.* — `List sequence starts at 3 instead of 1`
      * Context: `Except. **III.** "But," say they again, "the Ephesians were not bu ...`
      * Context: `... er, till their doctrine was first believed. Arg. **III.** The Scripture hath its authority, in relation to ...`

##### Entry: `VI.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Except.* — `List sequence starts at 6 instead of 1`
      * Context: `... e to be before the testimony of the church. Arg. **VI.** If we must believe the Scripture to be the word o ...`


### 2. Text Integrity Whitelist

#### Paragraph Splits

##### Split Entry: `—` (⚠️ Greedy)
  * Silenced 22 paragraph split(s):
    * **File:** `EPUB/ch004.xhtml`
      * Previous: `... These things being presupposed, —`
      * Next: `Use 1 . Let no flesh glory in themselves, but let every mouth be stopped; for we have all sinned and come short of the glory of God. Who hath made the possessors of the gospel to d ...`
    * **File:** `EPUB/ch006.xhtml`
      * Previous: `... the power of godliness is away, will not prevent these evils: " Tantum religio [Translated: "So much [evil] religion"] potuit suadere malorum ." [Translated: "to persuade to evil"]`
      * Next: `Others there are that press for a non-toleration of any thing that opposes or contradicts the truth in any part, themselves being in their own judgments fully possessed of all, — t ...`
    * **File:** `EPUB/ch006.xhtml`
      * Previous: `... e cannot be too cautious how we place men in that damnable series calling heaven and earth to witness the contrary. But again: To spread such errors will be destructive to souls. —`
      * Next: `So are many things, which yet are not punishable with forcible death. Let him that thinks so go kill Pagans and Mohammedans. As such heresy is a canker, but a spiritual one, let it ...`
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... ting a period to their church and state. Whether of these is more probable is not needful to insist upon: this is certain, that a certain time is pointed at; which will yield us, —`
      * Next: `Observation 6. The church's mercies and deliverance have their appointed season. ...`
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... That which I shall choose, from amongst many others that present themselves, a little to insist upon, is, that —`
      * Next: `Observation 7. — Former mercies, with their times and places, are to be had in thankful remembrance unto them who wait for future blessings. ...`
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... This might be of rich consideration could we attend it. For, —`
      * Next: `Use 1. Hence, as I said before, is apostasy from God's work. He appears not unto men; — how can they go upon his employment. Men that have no vision of God, are in the dark, and kn ...`
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... (2.) "The curtains of the land of Midian," for the Midianites dwelling in curtained tabernacles, by the same figure as before. They trembled, —`
      * Next: `יִרְגְּזוּן , "moved themselves, were moved;" that is, shaken with fear and trembling, as though they were ready to run from the appearance of the mighty God with his people. The s ...`
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... its subject and object, — the person believing and the thing believed. There needs no ascending into heaven, or descending; the word of faith makes all things nigh, even within us,`
      * Next: `He that believes in Christ, by that believing receives Christ, John 1:12; Romans 10:6-8. Some glasses will present things at a great distance very near; faith looking through the g ...`
    * **File:** `EPUB/ch014.xhtml`
      * Previous: `... That which is spoken immediately to the prophet, I shall hold out to all, acting in the name and authority of God, in this general proposition: —`
      * Next: `Observation. Plausible compliances of men in authority with those against whom they are employed, are treacherous contrivances against the God of heaven, by whom they are employed. ...`
    * **File:** `EPUB/ch014.xhtml`
      * Previous: `... Now, this revolting from principles of religion and righteousness, to a compliance with any sinful way or person, is a treacherous opposition to the God of heaven. For, —`
      * Next: `It cannot be done but by preferring the creature before the Creator, especially in those things which are the proximate causes of deviation. ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... t not this be measured by disputable consequences, no more than the other are. Let the evidence be in the things themselves, and " Actum est ," let who will plead for them. Hence —`
      * Next: `Popish religion, warming in its very bowels a fatal engine against all magistracy amongst us, cannot upon our concessions plead for forbearance; it being a known and received maxim ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... The word here used to express his sin, is " נֹקֵב , signifying also to pierce, and is twice so rendered —`
      * Next: `Isaiah 36:6; Hebrews 3:14. Desperate expressions, piercing the honor and glory of the Most High willingly and willfully, were doubtless his death-deserving crime. It is the same wo ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... briefly discussed, I proceed, in the next place, to such other general observations as may serve to the farther clearing of the business in hand; and they are these that follow: —`
      * Next: `The forbearance of or opposition unto errors, may be considered with respect either unto civil or spiritual judicature. ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... ve examples in Clem. Epist. ad Corinth. — the churches of Vienne and Lyons to those of Asia, Euseb. — of Ignatius to several persons and churches — of Irenseus to Victor., Euseb. —`
      * Next: `Dionysius to Stephen, ibid., and the like), heretics found such cold entertainment as made them ashamed, if not weary, of their chosen wanderings. But this is not my present busine ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... e of things which respecteth errors in a. real sense, as to the inflicting or not inflicting of punishment on religious delinquents. And this is the sole thing under debate, viz. —`
      * Next: `Whether persons enjoying civil authority over others — being intrusted therewithal according to the constitutions of the place and nation where the lot of them both, by providence, ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... These things premised, I assert that —`
      * Next: `Non-toleration — in the latitude which is for persons in authority enjoying the truth (or supposing they do enjoy it) to punish in an arbitrary way, according to what they shall co ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... e, which is threatened, Isaiah 9:12, two or three consectaries, added hereunto, shall close this part of the magistrate's power, or rather duty, about the things of religion. As, —`
      * Next: `Consect. 1. Positive actings, by way of supportment and assistance, maintenance, allowance of public places, and the like, in the behalf of persons deviating from the truth, in tho ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... , and the like, in the behalf of persons deviating from the truth, in those things wherein they deviate, are contrary to the rule of the word, and duty of them in authority. For, —`
      * Next: `Error hath neither right nor promise; nor is any precept given in the behalf thereof. ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... the cognizance of the magistrate, he being to attend the worship which for the main is acceptable to God in Christ; neither do any testimonies extend his duty any farther. Hence, —`
      * Next: `Corollary 1. The present differences about church society and the subject or seat of discipline, which are between those dissenters who are known by the names of Presbyterians and ...`
    * **File:** `EPUB/ch015.xhtml`
      * Previous: `... interests of men), hinder not at all, but that the magistrate is bound to the performance of the duties before mentioned unto both parties. And the reasons of this are, because, —`
      * Next: `Reason 1. The things wherein they are agreed are clearly as broad as the magistrate's duty can be stretched to cover them. ...`
    * **File:** `EPUB/ch019.xhtml`
      * Previous: `... The words may be briefly resolved into this doctrinal proposition: —`
      * Next: `Observation. All staggering at the promises of God is from unbelief. ...`
    * **File:** `EPUB/ch019.xhtml`
      * Previous: `... y shuts up the spirit from any occasion of staggering. "O ye of little faith! wherefore do ye doubt?" Ah! lest our share be not in this promise, — lest we are not intended in it. —`
      * Next: `Poor creatures! there is but this one way of keeping you off from it; that is, disputing it in yourselves by unbelief. Here lies the sincerity of God towards thee, that believing, ...`

##### Split Entry: `Reader,` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch005.xhtml`
      * Previous: `... Reader,`
      * Next: `THIS, be it what it will, thou hast no cause to thank or blame 61 me for. ...`

##### Split Entry: `Sir` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... Sir`
      * Next: `Your Excellency's Most humble and devoted Servant ...`

##### Split Entry: `John Owen` (⚠️ Greedy)
  * Silenced 4 paragraph split(s):
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... Your Excellency's Most humble and devoted Servant`
      * Next: `John Owen ...`
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... John Owen`
      * Next: `COGGESHALL, ESSEX, OCTOBER 5, 1648 ...`
    * **File:** `EPUB/ch013.xhtml`
      * Previous: `... Your devoted Servant In our dearest Lord,`
      * Next: `John Owen ...`
    * **File:** `EPUB/ch013.xhtml`
      * Previous: `... John Owen`
      * Next: `COGGESHALL, Feb. 38. ...`

##### Split Entry: `Your devoted Servant` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch013.xhtml`
      * Previous: `... ld give you to prove all things that come unto you in his way, and to hold fast that which is good, granting you unconquerable assistance in constant perseverance, is the prayer of`
      * Next: `Your devoted Servant In our dearest Lord, ...`
    * **File:** `EPUB/ch013.xhtml`
      * Previous: `... Your devoted Servant In our dearest Lord,`
      * Next: `John Owen ...`

##### Split Entry: `AMPLISSIMO` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... difications which appear in the Congregationalism of Owen, are conspicuous elements in the first scheme of ecclesiastical polity which he ever broached. See also his "Review of the`
      * Next: `AMPLISSIMO ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... AMPLISSIMO`
      * Next: `SENATUI, ...`

##### Split Entry: `SENATUI,` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... AMPLISSIMO`
      * Next: `SENATUI, ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... SENATUI,`
      * Next: `INCLYTISSIMO POPULI ANGLICANI CONVENTUI , [Translated: "To the most illustrious assembly of the English people"] ...`

##### Split Entry: `INCLYTISSIMO` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... SENATUI,`
      * Next: `INCLYTISSIMO POPULI ANGLICANI CONVENTUI , [Translated: "To the most illustrious assembly of the English people"] ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... INCLYTISSIMO POPULI ANGLICANI CONVENTUI , [Translated: "To the most illustrious assembly of the English people"]`
      * Next: `OB ...`

##### Split Entry: `OB` (⚠️ Greedy)
  * Silenced 3 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... INCLYTISSIMO POPULI ANGLICANI CONVENTUI , [Translated: "To the most illustrious assembly of the English people"]`
      * Next: `OB ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... OB`
      * Next: `PRISCA ANGLO-BRITANNORUM JURA [Translated: "The ancient rights of the Anglo-Britons"] STRENUE ET FIDELITER ASSERTA; LIBERTATEM PATRIAM (NEFARUS QUORUNDAM MOLITONIBUS [Translated: " ...`
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... John Owen`
      * Next: `COGGESHALL, ESSEX, OCTOBER 5, 1648 ...`

##### Split Entry: `ADMINISTRATAM;` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως`
      * Next: `ADMINISTRATAM; ...`

##### Split Entry: `POTISSIMUM` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... EBIS CHRISTIANAE POSTLIMINIO RESTITUTA ; [Translated: "dissolved, Popish, novel, and anti-Christian rites abolished; the privileges of the Christian people restored by postliminy"]`
      * Next: `POTISSIMUM ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... POTISSIMUM`
      * Next: `PROTECTIONEM DEI O.M. HIS OMNIBUS, ALUSQUE INNUMERIS, CONSILIO, BELLO, DOMI, FORAS [Translated: "innumerable [blessings], in counsel, war, at home, and abroad"] GILATIOSE POTITAM; ...`

##### Split Entry: `D.D.C. JOANNES OWEN.` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... LLAM QUIDEM, IPSORUM TAMEN VOTO [Translated: "yet by their own desire"] JUSSUQUE PRIUS CORAM IPSIS HABITAM, NUNC [Translated: "previously delivered before them, now"] LUCE DONATAM,`
      * Next: `D.D.C. JOANNES OWEN. ...`

##### Split Entry: `All these things being considered, I cannot so well close with them` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch006.xhtml`
      * Previous: `... Give another and another"] one stripe sometimes makes way for another, and how know I that men will stay at thirty-nine? " Principiis obsta ." [Translated: "Resist the beginnings"]`
      * Next: `All these things being considered, I cannot so well close with them who make the least allowance of dissent to be the mother of abominations. ...`

##### Split Entry: `PATRIAM (NEFARUS QUORUNDAM` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... OB`
      * Next: `PRISCA ANGLO-BRITANNORUM JURA [Translated: "The ancient rights of the Anglo-Britons"] STRENUE ET FIDELITER ASSERTA; LIBERTATEM PATRIAM (NEFARUS QUORUNDAM MOLITONIBUS [Translated: " ...`
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... PATRIAM (NEFARUS QUORUNDAM MOLITONIBUS [Translated: "Our country (by the nefarious machinations of some"] PAENE PESSUNDATAM) ELECUPERATAM ; [Translated: "almost ruined) recovered"]`
      * Next: `JUSTITIAM FORTITER, ἴσως , ἐπιεικῶς , ἀπροσωπολήπτως ...`


#### Ignored Warnings

##### Warning Entry: `front_matter_toc_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some early CONTENTS pages have no strong text-window match in the EPUB`

##### Warning Entry: `suspicious_large_number_starts` (✅ Clean)
  * Silenced warning message(s):
    * `Some paragraphs begin with large bare numbers that may be broken reference continuations`

##### Warning Entry: `repeated_windows` (✅ Clean)
  * Silenced warning message(s):
    * `Repeated word windows may indicate ghost-layer duplication`

##### Warning Entry: `weak_page_coverage` (✅ Clean)
  * Silenced warning message(s):
    * `Some PDF pages have no strong text-window match in the EPUB`

##### Warning Entry: `dense_source_window_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors`

##### Warning Entry: `top_of_page_text_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some first body lines near the top of PDF pages are not found in the EPUB`

##### Warning Entry: `bottom_of_page_text_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some last body lines near the bottom of PDF pages are not found in the EPUB`

##### Warning Entry: `orphan_endnotes` (❌ Unused)
  * Silenced 0 warnings.

##### Warning Entry: `roman_heading_candidates` (✅ Clean)
  * Silenced warning message(s):
    * `Some roman numeral headings appear in body paragraphs instead of centered heading elements`

##### Warning Entry: `missing_latin_clauses` (✅ Clean)
  * Silenced warning message(s):
    * `Some dense Latin passages from the PDF are missing from the EPUB`
