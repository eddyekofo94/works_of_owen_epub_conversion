# Whitelist Trace & Audit Report: Volume 7

This report tracks and validates every whitelist entry to prevent greedy silencing of real anomalies.

## Summary

* **Total Whitelisted Entries:** 88
* **Clean/Exact Matches (1 issue silenced):** 68
* **Greedy Entries (silences multiple issues):** 20
* **Unused Entries (silences 0 issues - safe to remove):** 0

### ⚠️ Greedy Whitelist Entries
These entries are too broad and matched multiple distinct anomalies. Consider making them more specific.

| Whitelist Path / Entry | Match Count |
|-------------------------|-------------|
| `anomalies -> Hyphenation Anomalies -> 'pre-admonition'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'pre-admonitions'` | 2 |
| `anomalies -> Hyphenation Anomalies -> 'stout-hearted'` | 5 |
| `anomalies -> Hyphenation Anomalies -> 'stout-heartedness'` | 5 |
| `anomalies -> Punctuation Spacing Blemishes -> '..'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '1 .'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '1st .'` | 3 |
| `anomalies -> Punctuation Spacing Blemishes -> '2 .'` | 6 |
| `anomalies -> Punctuation Spacing Blemishes -> '2dly .'` | 2 |
| `anomalies -> Punctuation Spacing Blemishes -> '3 .'` | 5 |
| `anomalies -> Punctuation Spacing Blemishes -> '4 .'` | 5 |
| `anomalies -> Punctuation Spacing Blemishes -> '5 .'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '1. ... 3.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> '3. ... 5.'` | 2 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'I. ... III.'` | 4 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'II.'` | 5 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'II. ... XIX.'` | 3 |
| `anomalies -> Structural Nesting Sequence Jumps -> 'III.'` | 4 |
| `text_integrity -> paragraph_splits -> John Owen` | 2 |
| `text_integrity -> paragraph_splits -> III.` | 2 |

---

## Detailed Trace by Category

### 1. Anomalies Whitelist

#### Category: `OCR & Bracket Residues`

No whitelist entries for this category.


#### Category: `Scanner Substring False Positives`

No whitelist entries for this category.


#### Category: `Hyphenation Anomalies`

##### Entry: `Spiritual-mindedness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3.* — `Capitalized hyphenation with unrecognized right particle`
      * Context: `... ons I have handled so at large in my discourse of **Spiritual-mindedness**, as I shall here very briefly speak unto it, so ...`

##### Entry: `ale-house` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 20.* — `Splittable word (rejoins to valid word 'alehouse')`
      * Context: `... to his journey's end, lodgeth himself in a nasty **ale-house**. When men are engaged in important duties, yet if ...`

##### Entry: `cross-ways` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3.* — `Splittable word (rejoins to valid word 'crossways')`
      * Context: `... e ministers, that we be not like a hand set up in **cross-ways**, directing others which way to go, but staying be ...`

##### Entry: `evil-doer` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Splittable word (rejoins to valid word 'evildoer')`
      * Context: `... s death, he must be so received or rejected as an **evil-doer**. And this was done by these apostates; for, going ...`

##### Entry: `fire-ball` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 9.* — `Splittable word (rejoins to valid word 'fireball')`
      * Context: `... re, as our Savior did. If a man have a grenado or **fire-ball** cast into his clothes by his enemy, he doth not c ...`

##### Entry: `hand-breadth` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 11.* — `Splittable word (rejoins to valid word 'handbreadth')`
      * Context: `... e psalmist, "Behold, thou hast made my days as an **hand-breadth**; and mine age is as nothing before thee." Hence h ...`

##### Entry: `here-withal` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `Splittable word (rejoins to valid word 'herewithal')`
      * Context: `... ened to make a true judgment of it. In compliance **here-withal** was religion outwardly figured and represented am ...`

##### Entry: `new-fangledness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 5 - Darkness and Ignorance Another Cause of Apostasy.* — `Splittable word (rejoins to valid word 'newfangledness')`
      * Context: `... ir forefathers professed so many ages before this **new-fangledness** came up, which hath filled all things with confus ...`

##### Entry: `non-proficiency` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Splittable word (rejoins to valid word 'nonproficiency')`
      * Context: `... after a profession of the gospel, beginning at a **non-proficiency** under it, do end in apostasy from it. And we may ...`

##### Entry: `over-earnest` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `Splittable word (rejoins to valid word 'overearnest')`
      * Context: `... heir minds and carnal reasonings; and some, by an **over-earnest** pursuit of the workings of their own rational fac ...`

##### Entry: `over-fullness` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 13 - Directions to Avoid the Power of a Prevailing Apostasy.* — `Splittable word (rejoins to valid word 'overfullness')`
      * Context: `... among professors, but it proceeds either from an **over-fullness** of the world and its occasions, or the prevalency ...`

##### Entry: `over-valuation` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3.* — `Splittable word (rejoins to valid word 'overvaluation')`
      * Context: `... love of the world, delight in things sensual, an **over-valuation** of relations and enjoyments, with sundry other th ...`

##### Entry: `pre-admonition` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 8 - Apostasy From the Holiness of the Gospel* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... danger and duty, therefore, are declared in these **pre-admonitions**. Wherefore of the first our apostle speaketh, 1 T ...`
    * **Chapter:** *Chapter 8 - Apostasy From the Holiness of the Gospel* — `Splittable word (rejoins to valid word 'preadmonition')`
      * Context: `... danger and duty, therefore, are declared in these **pre-admonition**s. Wherefore of the first our apostle speaketh, 1 ...`
      * Context: `... rs of the gospel, yet this prediction of them and **pre-admonition** concerning them may be of advantage unto them th ...`

##### Entry: `pre-admonitions` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 8 - Apostasy From the Holiness of the Gospel* — `Hyphenated word with unrecognized particles on both sides`
      * Context: `... danger and duty, therefore, are declared in these **pre-admonitions**. Wherefore of the first our apostle speaketh, 1 T ...`
    * **Chapter:** *Chapter 8 - Apostasy From the Holiness of the Gospel* — `Splittable word (rejoins to valid word 'preadmonition')`
      * Context: `... danger and duty, therefore, are declared in these **pre-admonition**s. Wherefore of the first our apostle speaketh, 1 ...`
      * Context: `... rs of the gospel, yet this prediction of them and **pre-admonition** concerning them may be of advantage unto them th ...`

##### Entry: `stout-hearted` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *Chapter 5.* — `Splittable word (rejoins to valid word 'stoutheartedness')`
      * Context: `... , with respect unto his own. Those who, through a **stout-heartedness**, do contemn them before their approach, boasting ...`
    * **Chapter:** *Chapter 9.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... umstances here below. I speak not of them who are **stout-hearted** and far from righteousness, who live and die like ...`
    * **Chapter:** *Chapter 11.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... d's will. All others are stubborn and obstinate, **stout-hearted** and far from righteousness. And when the world ha ...`
    * **Chapter:** *Chapter 14.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... wholly neglect the observance of them. These are **stout-hearted** and far from righteousness, Titus 1:16. Some atte ...`
    * **Chapter:** *Chapter 4.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... such a time he doth more abhor than those who are **stout-hearted**, little regarding him or the operation of his han ...`

##### Entry: `stout-heartedness` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *Chapter 5.* — `Splittable word (rejoins to valid word 'stoutheartedness')`
      * Context: `... , with respect unto his own. Those who, through a **stout-heartedness**, do contemn them before their approach, boasting ...`
    * **Chapter:** *Chapter 9.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... umstances here below. I speak not of them who are **stout-hearted** and far from righteousness, who live and die like ...`
    * **Chapter:** *Chapter 11.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... d's will. All others are stubborn and obstinate, **stout-hearted** and far from righteousness. And when the world ha ...`
    * **Chapter:** *Chapter 14.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... wholly neglect the observance of them. These are **stout-hearted** and far from righteousness, Titus 1:16. Some atte ...`
    * **Chapter:** *Chapter 4.* — `Splittable word (rejoins to valid word 'stouthearted')`
      * Context: `... such a time he doth more abhor than those who are **stout-hearted**, little regarding him or the operation of his han ...`

##### Entry: `three-fold` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Splittable word (rejoins to valid word 'threefold')`
      * Context: `... nto our affections that they may be spiritual — A **three-fold** work on the affections described. TO declare the ...`

##### Entry: `top-stone` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `Splittable word (rejoins to valid word 'topstone')`
      * Context: `... t forego, nor have so done until it is become the **top-stone** of many men's religion), it was merely from the u ...`

##### Entry: `un-commanded` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 15.* — `Splittable word (rejoins to valid word 'uncommanded')`
      * Context: `... else is not faith, but fancy; and therefore those **un-commanded** duties in religion, which so abound in the papal ...`

##### Entry: `un-humbled` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 8 - Apostasy From the Holiness of the Gospel* — `Splittable word (rejoins to valid word 'unhumbled')`
      * Context: `... be defiled, their lusts unmortified, their hearts **un-humbled**, their whole souls unfurnished of spiritual and h ...`

##### Entry: `where-into` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 17.* — `Splittable word (rejoins to valid word 'whereinto')`
      * Context: `... s of grace in us; there are other causes of them, **where-into** they are principally resolved; — but this I say, ...`


#### Category: `Punctuation Spacing Blemishes`

##### Entry: `..` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 6.* — `Duplicate period (double dot)`
      * Context: `**..**. advantage and refreshment unto their souls. 2dly**..** As unto the positive part of this glorious future **..**.`
    * **Chapter:** *Chapter 8.* — `Duplicate period (double dot)`
      * Context: `**..**. basement, the principal end designed. But, — 2dly**..** For the relief of them that may be perplexed in t **..**.`
      * Context: `**..**. unto us, — vain curiosity and carnal boldness. 1st**..** It is unimaginable how the subtile disquisitions **..**.`
    * **Chapter:** *Chapter 9.* — `Duplicate period (double dot)`
      * Context: `**..**. ng so long in the briers of this temptation. 2dly**..** Recalling the experiences we have had of God will **..**.`

##### Entry: `1 .` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 1.* — `Spaced period (space before period)`
      * Context: `... s the foundation of the present discourse; as, — **1 .** To be spiritually minded is the great distinguish ...`
    * **Chapter:** *Chapter 18.* — `Spaced period (space before period)`
      * Context: `... unto them, may be fixed on these three things: — **1 .** An habitual suitableness unto spiritual things up ...`
    * **Chapter:** *Chapter 3.* — `Spaced period (space before period)`
      * Context: `... conclusive, or how they may be defeated. And, — **1 .** When sin hath in any instance possessed the imagi ...`

##### Entry: `1st ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 16.* — `Spaced punctuation (space before character)`
      * Context: `... ne, which may be reduced unto these two heads: — **1st ,** A desire to retain some thing or things that is o ...`

##### Entry: `1st .` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 5.* — `Spaced period (space before period)`
      * Context: `... nd increase. And hereon two things will ensue: — **1st .** The soul will come unto a more satisfactory, abid ...`
      * Context: `... degrees; and we may cast them under two heads: — **1st .** Some do not at all understand that things are ami ...`
    * **Chapter:** *Chapter 8.* — `Spaced period (space before period)`
      * Context: `... ied withal, or indulged in the mind, I answer, — **1st .** It is no great matter whether we are able to dist ...`
    * **Chapter:** *Chapter 13.* — `Spaced period (space before period)`
      * Context: `... e is to be sincere with respect unto them all: — **1st .** God himself, — that is, as revealed in and by Chr ...`

##### Entry: `2 .` (⚠️ Greedy)
  * Silenced 6 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Spaced period (space before period)`
      * Context: `... up their banners for tokens, we know not; for, — **2 .** The present state of this defection hath a danger ...`
      * Context: `... l probably will be again entangled and overcome. **2 .** A stated satisfaction concerning the folly of res ...`
    * **Chapter:** *Chapter 1.* — `Spaced period (space before period)`
      * Context: `... d determination of what state we do belong unto. **2 .** Where any are spiritually minded, there, and ther ...`
    * **Chapter:** *Chapter 10.* — `Spaced period (space before period)`
      * Context: `... heap, or the choicest part of your useful time. **2 .** Preparation of mind unto a due reverence of God a ...`
    * **Chapter:** *Chapter 14.* — `Spaced period (space before period)`
      * Context: `... terminated on them, as we shall see immediately. **2 .** Men may be delighted in the performance of outwar ...`
    * **Chapter:** *Chapter 3.* — `Spaced period (space before period)`
      * Context: `... l rebellion against, in one instance or another. **2 .** A change in the affections, giving a temporary de ...`
    * **Chapter:** *Chapter 5.* — `Spaced period (space before period)`
      * Context: `... f sin is a great advantage unto spiritual peace. **2 .** Consider the end for which aids of grace are gran ...`

##### Entry: `2dly ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 16.* — `Spaced punctuation (space before character)`
      * Context: `... ly than by such a neglect of his promised grace? **2dly ,** An evidence that such persons love not, care not ...`

##### Entry: `2dly .` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 5.* — `Spaced period (space before period)`
      * Context: `... among us walk in disconsolation all their days. **2dly .** It will gradually give the heart an acquaintance ...`
      * Context: `... ove it, there it is assuredly predominant in us. **2dly .** Others are sensible of the evil of their hearts, ...`
    * **Chapter:** *Chapter 8.* — `Spaced period (space before period)`
      * Context: `... he most part, unto all godly fear and reverence. **2dly .** Others are so under the power of carnal boldness, ...`

##### Entry: `3 .` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *Chapter 13 - Directions to Avoid the Power of a Prevailing Apostasy.* — `Spaced period (space before period)`
      * Context: `... l means of our own deliverance and preservation. **3 .** Constancy in our testimony against the prevalency ...`
    * **Chapter:** *Chapter 10.* — `Spaced period (space before period)`
      * Context: `... at liberty to exercise itself on spiritual things **3 .** Earnest desires after a renewed sense and relish ...`
    * **Chapter:** *Chapter 15.* — `Spaced period (space before period)`
      * Context: `... f Christ. This she rested in with great delight. **3 .** As they come unto them with these designs and exp ...`
    * **Chapter:** *Chapter 16.* — `Spaced period (space before period)`
      * Context: `... l be quickly weakened and impaired. Wherefore, — **3 .** Affections thus led unto and fixed on spiritual a ...`
    * **Chapter:** *Chapter 3.* — `Spaced period (space before period)`
      * Context: `... y under the power of sin and spiritual darkness. **3 .** A performance of many duties, both moral and evan ...`

##### Entry: `4 .` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *Chapter 14.* — `Spaced period (space before period)`
      * Context: `... ject of the discourse of the prophet, Isaiah 1:11 **4 .** The reputation of devotion in religious duties ma ...`
    * **Chapter:** *Chapter 3.* — `Spaced period (space before period)`
      * Context: `... him from the dominion of sin, Matthew 19:20-23. **4 .** Repentance for sin committed. This is that which ...`
    * **Chapter:** *Chapter 4.* — `Spaced period (space before period)`
      * Context: `... be bewailed where grace is vigilant and active. **4 .** Want of a due sense of indications of divine disp ...`
    * **Chapter:** *Chapter 5.* — `Spaced period (space before period)`
      * Context: `... ngs will go backward in our spiritual condition. **4 .** Make especial application unto the Lord Christ, u ...`
    * **Chapter:** *Chapter 6.* — `Spaced period (space before period)`
      * Context: `... g justified by faith, they have peace with God." **4 .** There is a season when, by the grace of Christ, i ...`

##### Entry: `5 .` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 3.* — `Spaced period (space before period)`
      * Context: `... and Judas repented him before he hanged himself. **5 .** Promises and resolutions against sin for the futu ...`
    * **Chapter:** *Chapter 5.* — `Spaced period (space before period)`
      * Context: `... ucements, we are directed unto, Hebrews 4:14-16. **5 .** Remember always the way and method of the operati ...`
    * **Chapter:** *Chapter 6.* — `Spaced period (space before period)`
      * Context: `... y which is the territory wherein sin doth reign. **5 .** Make continual applications unto the Lord Christ, ...`

##### Entry: `6 .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10.* — `Spaced period (space before period)`
      * Context: `... ion, we may know assuredly from whence they are. **6 .** Continual watchful care that no root of bitternes ...`

##### Entry: `7 .` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10.* — `Spaced period (space before period)`
      * Context: `... ll their endeavors will be immediately consumed. **7 .** Mortification unto the world in our affections an ...`

##### Entry: `First ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 17.* — `Spaced punctuation (space before character)`
      * Context: `... put a little weight upon it, we may consider, — **First ,** God himself makes it on his part a ground and rea ...`

##### Entry: `Lord ;` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 21* — `Spaced punctuation (space before character)`
      * Context: `... onians 3:8, "Now we live, if ye stand fast in the **Lord ;**" — " Now our life will do us good; we have the co ...`

##### Entry: `and ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3 - Apostasy From the Mystery, Truth, or Doctrine of the Gospel* — `Spaced punctuation (space before character)`
      * Context: `... uced to two heads: — [1.] Concerning the person; **and ,** [2.] Concerning the grace of Christ. Of the fir ...`

##### Entry: `flatteries :` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1.* — `Spaced punctuation (space before character)`
      * Context: `... e there declares, James 1:14, 15. Believe not its **flatteries :** — "Is it not a little one?" "This is the first or ...`

##### Entry: `ignorant ,` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `Spaced punctuation (space before character)`
      * Context: `... icient to expose any man unto the contumelies of "**ignorant ,** irrational, and foolish," who dares to avow them. ...`


#### Category: `Mixed-Case Capitalization Errors`

No whitelist entries for this category.


#### Category: `Structural Nesting Sequence Jumps`

##### Entry: `1. ... 3.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 12.* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *Chapter 11.* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *Chapter 5.* — `List sequence jump (skipped from 1 to 3)`

##### Entry: `3. ... 5.` (⚠️ Greedy)
  * Silenced 2 raw issue(s):
    * **Chapter:** *Chapter 14.* — `List sequence jump (skipped from 3 to 5)`
    * **Chapter:** *Chapter 6.* — `List sequence jump (skipped from 3 to 5)`

##### Entry: `I. ... III.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `List sequence starts at 3 instead of 1`
      * Context: `... K OF SATAN, AND JUDGMENTS OF GOD IN THIS MATTER. **III.** THE innate pride and vanity of the minds of men i ...`
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `List sequence starts at 2 instead of 1`
      * Context: `... R CAUSES AND OCCASIONS OF THE DECAY OF HOLINESS. **II.** MULTITUDES are led into and countenanced in the w ...`
      * Context: `... of that defection which the world groans under. I**II.** Great examples of persons exalted in places of em ...`
      * Context: `... them should be bishop of Rome, lib. 27 cap. 6. V**II.** During these seasons, Satan (as he will never be) ...`
    * **Chapter:** *Part II.* — `List sequence starts at 2 instead of 1`
      * Context: `... teristic of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think ...`
      * Context: `... c of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think of, — ...`
      * Context: `... iness on spiritual and heavenly objects, X. PART **II.** The two divisions of the proposed method respecti ...`

##### Entry: `II.` (⚠️ Greedy)
  * Silenced 5 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `List sequence starts at 3 instead of 1`
      * Context: `... K OF SATAN, AND JUDGMENTS OF GOD IN THIS MATTER. **III.** THE innate pride and vanity of the minds of men i ...`
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `List sequence starts at 2 instead of 1`
      * Context: `... R CAUSES AND OCCASIONS OF THE DECAY OF HOLINESS. **II.** MULTITUDES are led into and countenanced in the w ...`
      * Context: `... of that defection which the world groans under. I**II.** Great examples of persons exalted in places of em ...`
      * Context: `... them should be bishop of Rome, lib. 27 cap. 6. V**II.** During these seasons, Satan (as he will never be) ...`
    * **Chapter:** *Part II.* — `List sequence starts at 2 instead of 1`
      * Context: `... teristic of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think ...`
      * Context: `... c of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think of, — ...`
      * Context: `... iness on spiritual and heavenly objects, X. PART **II.** The two divisions of the proposed method respecti ...`
    * **Chapter:** *Part II.* — `List sequence jump (skipped from 2 to 19)`

##### Entry: `II. ... XIX.` (⚠️ Greedy)
  * Silenced 3 raw issue(s):
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `List sequence starts at 2 instead of 1`
      * Context: `... R CAUSES AND OCCASIONS OF THE DECAY OF HOLINESS. **II.** MULTITUDES are led into and countenanced in the w ...`
      * Context: `... of that defection which the world groans under. I**II.** Great examples of persons exalted in places of em ...`
      * Context: `... them should be bishop of Rome, lib. 27 cap. 6. V**II.** During these seasons, Satan (as he will never be) ...`
    * **Chapter:** *Part II.* — `List sequence starts at 2 instead of 1`
      * Context: `... teristic of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think ...`
      * Context: `... c of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think of, — ...`
      * Context: `... iness on spiritual and heavenly objects, X. PART **II.** The two divisions of the proposed method respecti ...`
    * **Chapter:** *Part II.* — `List sequence jump (skipped from 2 to 19)`

##### Entry: `III.` (⚠️ Greedy)
  * Silenced 4 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `List sequence jump (skipped from 1 to 3)`
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `List sequence starts at 3 instead of 1`
      * Context: `... K OF SATAN, AND JUDGMENTS OF GOD IN THIS MATTER. **III.** THE innate pride and vanity of the minds of men i ...`
    * **Chapter:** *Chapter 10 - Other Causes and Occasions of the Decay of Holiness.* — `List sequence starts at 2 instead of 1`
      * Context: `... R CAUSES AND OCCASIONS OF THE DECAY OF HOLINESS. **II.** MULTITUDES are led into and countenanced in the w ...`
      * Context: `... of that defection which the world groans under. I**II.** Great examples of persons exalted in places of em ...`
      * Context: `... them should be bishop of Rome, lib. 27 cap. 6. V**II.** During these seasons, Satan (as he will never be) ...`
    * **Chapter:** *Part II.* — `List sequence starts at 2 instead of 1`
      * Context: `... teristic of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think ...`
      * Context: `... c of spiritual affections are delineated, V**II.**, VI**II.** In our consideration of God, we must think of, — ...`
      * Context: `... iness on spiritual and heavenly objects, X. PART **II.** The two divisions of the proposed method respecti ...`


#### Category: `Unmatched Quotation Marks`

##### Entry: `(1.) In extraordinary, outward judgments upon open, profligate sinners, especially the enemies of his church and glory.` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**(1.) In extraordinary, outward judgments upon open, profligate sinners, especially the enemies of his church and glory. ...**`

##### Entry: `1. The gift of God, δωρεά, is either δόσις, "donatio," or δώρημα, "donum." Sometimes it is taken for the grant or giving` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Paragraph has unmatched double quotes (count: 43)`
      * Context: `**1. The gift of God, δωρεά, is either δόσις, "donatio," or δώρημα, "donum." Sometimes it is taken for the grant or giving...**`

##### Entry: `4. They are the way and means whereby the soul applies itself unto all sinful objects and actings. Hence are they called` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 12.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**4. They are the way and means whereby the soul applies itself unto all sinful objects and actings. Hence are they called...**`

##### Entry: `But the fixing of spiritual affections on spiritual objects is perfective of our present state and condition; not that w` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 19.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**But the fixing of spiritual affections on spiritual objects is perfective of our present state and condition; not that w...**`

##### Entry: `But there are yet other instances of the proneness of men in foregoing the faith that the church was retrieved unto at t` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 3 - Apostasy From the Mystery, Truth, or Doctrine of the Gospel* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**But there are yet other instances of the proneness of men in foregoing the faith that the church was retrieved unto at t...**`

##### Entry: `By grace our minds are renewed, — that is, changed and delivered from this frame; but they are so partially only. The pr` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10.* — `Paragraph has unmatched double quotes (count: 3)`
      * Context: `**By grace our minds are renewed, — that is, changed and delivered from this frame; but they are so partially only. The pr...**`

##### Entry: `Others there are, sincere, broken-hearted believers, [who,] scared at the rock of presumption on which they see so many` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *To the Serious Reader.* — `Paragraph has unmatched double quotes (count: 17)`
      * Context: `**Others there are, sincere, broken-hearted believers, [who,] scared at the rock of presumption on which they see so many ...**`

##### Entry: `The FIRST thing in the description is, that they were ἅπαξ φωτισθέντες, "once enlightened." Saith the Syriac translation` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Paragraph has unmatched double quotes (count: 29)`
      * Context: `**The FIRST thing in the description is, that they were ἅπαξ φωτισθέντες, "once enlightened." Saith the Syriac translation...**`

##### Entry: `Unto this pride, as inseparable from it, we may adjoin that vanity and curiosity that are in the minds of men. These are` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `Paragraph has unmatched double quotes (count: 7)`
      * Context: `**Unto this pride, as inseparable from it, we may adjoin that vanity and curiosity that are in the minds of men. These are...**`

##### Entry: `We judge no men, no party of men, as to their eternal state and condition, upon the account of their outward profession` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 6 - Causes of Apostasy* — `Paragraph has unmatched double quotes (count: 15)`
      * Context: `**We judge no men, no party of men, as to their eternal state and condition, upon the account of their outward profession ...**`

##### Entry: `who shall deliver me from this body of death?" Yea, they groan under a sense of it every day, nor is any thing such a tr` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 10.* — `Paragraph has unmatched double quotes (count: 1)`
      * Context: `**who shall deliver me from this body of death?" Yea, they groan under a sense of it every day, nor is any thing such a tr...**`

##### Entry: `Καὶ μετόχους γενηθέντας Πνεύματος ἁγίου. "Et participes facti sunt Spiritus Sancti," Vulg. Lat.; — "And are made partake` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 1 - the Nature of Apostasy From the Gospel Declared* — `Paragraph has unmatched double quotes (count: 77)`
      * Context: `**Καὶ μετόχους γενηθέντας Πνεύματος ἁγίου. "Et participes facti sunt Spiritus Sancti," Vulg. Lat.; — "And are made partake...**`

##### Entry: `Τέλειοι γίνεσθε ταῖς φρεσὶ, Be ye complete, perfect," well instructed in your minds, fully initiated into the doctrines` (✅ Clean)
  * Silenced 1 raw issue(s):
    * **Chapter:** *Chapter 5 - Darkness and Ignorance Another Cause of Apostasy.* — `Paragraph has unmatched double quotes (count: 15)`
      * Context: `**Τέλειοι γίνεσθε ταῖς φρεσὶ, Be ye complete, perfect," well instructed in your minds, fully initiated into the doctrines ...**`


### 2. Text Integrity Whitelist

#### Paragraph Splits

##### Split Entry: `To The Reader` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch004.xhtml`
      * Previous: `... To The Reader`
      * Next: `SOME brief account of the occasion and design of the ensuing discourse I judge due unto the reader, that, upon a prospect of them, he may either proceed in its perusal or desist, a ...`

##### Split Entry: `Αδύνατον γὰρ τοὺς` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch005.xhtml`
      * Previous: `... supposed to be attended, and to explain the mind of the Holy Ghost therein, may be neither unacceptable nor unuseful. And this is chap. 6:4-6, whose words are these that follow: —`
      * Next: `Αδύνατον γὰρ τοὺς ἅπαξ φωτισθέντας , γευσαμένους τε τῆς δωρεᾶς τῆς ἐπουρανίου , καὶ μετόχους γενηθέντας Πνεύματος ἁγίου , καὶ καλὸν γευσαμένους Θεοῦ ῥῆμα , δυνάμεις τε μέλλοντος αἰ ...`

##### Split Entry: `Hebrews 1:3, 11:3, where it denotes` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch005.xhtml`
      * Previous: `... 1. Ρῆμα is properly " verbum dictum ," [Translated: "the word spoken"] a word spoken; and although it be sometimes used in another sense by our apostle, and by him alone, —`
      * Next: `Hebrews 1:3, 11:3, where it denotes the effectual active power of God, — yet both the signification of the word and its principal use elsewhere denote words spoken, and, when appli ...`

##### Split Entry: `In the preaching of the gospel, it is necessary to propose` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch005.xhtml`
      * Previous: `... e of this severity is taken from the nature of this sin, or what is contained in it, which the apostle declares in the ensuing instances. And we may in our passage observe, that, —`
      * Next: `In the preaching of the gospel, it is necessary to propose unto men, and to insist on, the severity of God in dealing with provoking sinners against it. And indeed the severity of ...`

##### Split Entry: `Sin and conscience are stubborn in their conflict` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch008.xhtml`
      * Previous: `... ion in them, they could not give themselves up unto the pursuit of such brutish lusts; and had they not some form or other of it, they could not be secure in their practice: for, —`
      * Next: `Sin and conscience are stubborn in their conflict whilst immediately opposed, conscience pleading that there should be no sin, and sin contending that there may be no conscience; b ...`

##### Split Entry: `The gospel, — that is, the doctrines of it` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch010.xhtml`
      * Previous: `... can never receive the truths of the gospel in a due manner, and are ready to renounce them when they have by any means been brought unto the profession of them for a season; for, —`
      * Next: `The gospel, — that is, the doctrines of it and truths contained in it, — is proposed unto us in the name and on the authority of God, having his image and superscription upon it. I ...`

##### Split Entry: `— that is, for the gospel and the profession thereof` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch014.xhtml`
      * Previous: `... observe, that upon the destruction of Babylon, it is said that "in her was found the blood of prophets, and of saints, and of all that were slain upon the earth," Revelation 18:24,`
      * Next: `— that is, for the gospel and the profession thereof. Whoever, therefore, offereth violence unto the life of any on the account of their profession of the gospel and religion of Ch ...`

##### Split Entry: `XIX.` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch022.xhtml`
      * Previous: `... the fullness of wisdom in spiritual things; 3. their value as perfective of our present condition; and, 4. as constituting in the future enjoyment of them our eternal blessedness,`
      * Next: `XIX. ...`

##### Split Entry: `It is an ancient complaint, that spiritual things` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch027.xhtml`
      * Previous: `... l, they have no evidence of the acting of grace in what they have done. I shall, therefore, with what brevity I can, give a resolution unto this inquiry; and to this end observe, —`
      * Next: `It is an ancient complaint, that spiritual things are filled with great obscurity and difficulty; and it is true. Not that there is any such thing in themselves, for they all come ...`

##### Split Entry: `Whosoever shall sincerely engage in this duty` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch029.xhtml`
      * Previous: `... e of them in such order in their minds as that they may sedately exercise their thoughts about them. Both these shall be afterward spoken unto. At present I shall only say, that, —`
      * Next: `Whosoever shall sincerely engage in this duty according unto what he hath, and shall abide constant therein, he will make such a refreshing progress in his apprehension of heavenly ...`

##### Split Entry: `He lays all sorts of afflictions in one scale` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch029.xhtml`
      * Previous: `... em solid relief but the consideration and faith of things invisible and eternal. So the apostle declares this state of things, 2 Corinthians 4:16-18 (the words before insisted on),`
      * Next: `He lays all sorts of afflictions in one scale, and, on the consideration of them, declares them to be "light" and "but for a moment." Then he lays glory in the other scale, and fin ...`

##### Split Entry: `A desire of increase and adding thereunto` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch029.xhtml`
      * Previous: `... nst the trouble and urgency of their present condition; but the enjoyment of these things in abundance is accompanied with a twofold evil, lying directly contrary unto this duty: —`
      * Next: `A desire of increase and adding thereunto. Earthly enjoyments enlarge men's earthly desires, and the love of them grows with their income. A moderate stock of waters, sufficient fo ...`

##### Split Entry: `The FIRST was, The habitual frame` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch036.xhtml`
      * Previous: `... IN the account given at the entrance of this discourse of what it is to be spiritually minded, it was reduced under three heads: —`
      * Next: `The FIRST was, The habitual frame, disposition, and inclination of the mind in its affections. ...`

##### Split Entry: `— it is not to be bought or purchased with riches` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch036.xhtml`
      * Previous: `... him by our affections, it is despised by him; he owns us not. As "if a man would give all the substance of his house for love, it would utterly be contemned," Song of Solomon 8:7,`
      * Next: `— it is not to be bought or purchased with riches; so if a man would give to God an the substance of his house without love, it would in like manner be despised. And however, on th ...`

##### Split Entry: `When men find, or may find, their affections yet quick` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch042.xhtml`
      * Previous: `... ase more vigorously act itself in the other faculties and powers of the soul, as the judgment and the will, in their approbation of and firm adherence unto spiritual things. But, —`
      * Next: `When men find, or may find, their affections yet quick, active, and intent on other things, as the lawful enjoyments and comforts of this life, it is in vain for them to relieve th ...`

##### Split Entry: `BY THE LATE PIOUS AND LEARNED` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch047.xhtml`
      * Previous: `... BY THE LATE PIOUS AND LEARNED MINISTER OF THE GOSPEL`
      * Next: `John Owen ...`

##### Split Entry: `John Owen` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch047.xhtml`
      * Previous: `... BY THE LATE PIOUS AND LEARNED MINISTER OF THE GOSPEL`
      * Next: `John Owen ...`
    * **File:** `EPUB/ch047.xhtml`
      * Previous: `... John Owen`
      * Next: `D.D. LONDON: 1688 ...`

##### Split Entry: `III.` (⚠️ Greedy)
  * Silenced 2 paragraph split(s):
    * **File:** `EPUB/ch003.xhtml`
      * Previous: `... 2. To those who confine the whole of obedience to morality; and 3. To those who pretend to perfection in this life. The causes of this kind of apostasy are mentioned,`
      * Next: `VIII. ...`
    * **File:** `EPUB/ch049.xhtml`
      * Previous: `... ls in the affections, when there is a neglect of the means by which it is mortified, when a reservation is made in favor of any known sin, and when hardness of heart is manifested,`
      * Next: `III. ...`

##### Split Entry: `The first is, the daily exercise of faith on Christ` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch053.xhtml`
      * Previous: `... being stated, I shall now name some of those graces and duties upon whose omission and neglect sin may prevail, as unto an application of them unto the mortification of any sin: —`
      * Next: `The first is, the daily exercise of faith on Christ as crucified. This is the great fundamental means of the mortification of sin in general, and which we ought to apply unto every ...`

##### Split Entry: `I have nothing to offer to free them from this evidence` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch053.xhtml`
      * Previous: `... yet made use of this way and means for the mortification of sin; or if, being convinced of it, they have been for any season driven or withheld from the exercise of faith herein, —`
      * Next: `I have nothing to offer to free them from this evidence of the reign of sin, but only that they would speedily and carefully address themselves unto their duty herein; and if they ...`

##### Split Entry: `(5thly.) They will have no quiet` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch053.xhtml`
      * Previous: `... (4thly.) They will receive in the warnings which are given them by the word preached, especially if their particular case be touched on or laid open`
      * Next: `(5thly.) They will have no quiet, rest, or self-approbation, until they come thoroughly off unto a healing and recovery, such as that described, Hosea 14:1-4. Thus it may be with s ...`

##### Split Entry: `set up their banners for tokens, we know not; for, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch016.xhtml`
      * Previous: `... rd court is long since given to be trodden down by the Gentiles, and how soon the enemies may roar in the very sanctuaries, and set up their banners for tokens, we know not; for, —`
      * Next: `2 . The present state of this defection hath a dangerous aspect. Physicians say, " Nemo moritur in declinatione morbi," — "No man dies in the declension of his disease;" and when a ...`

##### Split Entry: `proposed as the foundation of the present discourse; as, —` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch025.xhtml`
      * Previous: `... eed, it is not amiss, as I suppose, to put a remark upon those important truths which are directly contained in the words proposed as the foundation of the present discourse; as, —`
      * Next: `1 . To be spiritually minded is the great distinguishing character of true believers from all unregenerate persons. As such is it here asserted by the apostle. All those who are "c ...`

##### Split Entry: `Affections thus led unto and fixed on spiritual and heavenly things` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch041.xhtml`
      * Previous: `... leaving unto them; and wherever the mind is darkened about them, by temptation or seduction from the truth, there the affections will be quickly weakened and impaired. Wherefore, —`
      * Next: `3 . Affections thus led unto and fixed on spiritual and heavenly things, under the light and conduct of faith, are more and more renewed, or made in themselves more spiritual and h ...`

##### Split Entry: `An habitual suitableness unto spiritual things` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch043.xhtml`
      * Previous: `... ction seem to be strangers unto. And the state of our affections under a due exercise on heavenly things, and in their assimilation unto them, may be fixed on these three things: —`
      * Next: `1 . An habitual suitableness unto spiritual things upon the proposal of them. The ways whereby spiritual things are proposed unto our minds are various. They are so directly in all ...`

##### Split Entry: `When sin hath in any instance possessed the imagination` (✅ Clean)
  * Silenced 1 paragraph split(s):
    * **File:** `EPUB/ch053.xhtml`
      * Previous: `... ences of men's freedom from the dominion of sin, but only consider the arguments that lie against them, and examine how far they are conclusive, or how they may be defeated. And, —`
      * Next: `1 . When sin hath in any instance possessed the imagination, and thereby engaged the cogitative faculty in its service, it is a dangerous symptom of its rule or dominion. Sin may e ...`


#### Ignored Warnings

##### Warning Entry: `repeated_windows` (✅ Clean)
  * Silenced warning message(s):
    * `Repeated word windows may indicate ghost-layer duplication`

##### Warning Entry: `roman_heading_candidates` (✅ Clean)
  * Silenced warning message(s):
    * `Some roman numeral headings appear in body paragraphs instead of centered heading elements`

##### Warning Entry: `enumerator_sequence_candidates` (✅ Clean)
  * Silenced warning message(s):
    * `Some EPUB enumerators look like possible sequence jumps and need triage`

##### Warning Entry: `dense_source_window_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some dense PDF word windows are missing from the EPUB and may indicate sliced sentence interiors`

##### Warning Entry: `front_matter_toc_loss` (✅ Clean)
  * Silenced warning message(s):
    * `Some early CONTENTS pages have no strong text-window match in the EPUB`
