# Volume 1 Repair Plan

This plan details the steps to repair paragraph splits, punctuation spacing blemishes, and other OCR anomalies in **Volume 1** (The Glory of Christ) to achieve **PRISTINE** quality status (Need score < 20.0).

## 1. Paragraph Splits to be Healed
We will add `regex_replacements` to `volumes/v1/convert.py` to merge the following 5 confirmed paragraph splits:

1. **Preface split (subscribed names)**
   * **Context:** `...subscribed by other names as well as his own, —\n\nJohn Nesbitt...` in `General Preface`.
   * **Regex:** `r'subscribed by other names as well as his own,\s*—\s*\n\n\s*John Nesbitt'`
   * **Replacement:** `'subscribed by other names as well as his own, — John Nesbitt'`

2. **Preface split (Latin quote translation)**
   * **Context:** `...seeking in his duties to be under the influence of the sentiment, —\n\n_Prodesse quam conspici._` in `General Preface`.
   * **Regex:** `r'seeking in his duties to be under the influence of the sentiment,\s*—\s*\n\n\s*_Prodesse quam conspici\._'`
   * **Replacement:** `'seeking in his duties to be under the influence of the sentiment, — _Prodesse quam conspici._'`

3. **Chapter 7 split (John 1:9 scripture reference)**
   * **Context:** `...Hence is he said to lighten "every man that comets into the world,",\n\nJohn 1:9, by...` (also replacing the typo `comets` with `cometh`).
   * **Regex:** `r'lighten "every man that comets into the world,",\s*\n\n\s*John 1:9'`
   * **Replacement:** `'lighten "every man that cometh into the world," John 1:9'`

4. **Chapter 30 split (Psalm 2:7-9 false blockquote)**
   * **Context:** `...Genesis 3:15; Psalm 2:7-9,\n\n[[BLOCKQUOTE]] Psalms 68:17, 18` in `Chapter 3 - the Glory of Christ in the Mysterious Constitution of His Person`.
   * **Regex:** `r'Genesis 3:15;\s*Psalm 2:7-9,\s*\n\n\[\[BLOCKQUOTE\]\]\s*Psalms 68:17, 18'`
   * **Replacement:** `'Genesis 3:15; Psalm 2:7-9, Psalms 68:17, 18'`

5. **Chapter 38 split (Hebrew name Psalm 102:27 split)**
   * **Context:** `...That is his name, "אַתָה הוּא" —\n\nPsalm 102:27...` in `Chapter 11 - the Glory of Christ in the Recapitulation of All Things in Him`.
   * **Regex:** `r'That is his name,\s*"\s*אַתָה\s+הוּא\s*"\s*—\s*\n\n\s*P[sa]lms?\s+102:27'`
   * **Replacement:** `'That is his name, "אַתָה הוּא" — Psalm 102:27'`

## 2. Punctuation Spacing Blemishes to be Repaired
We will add `text_replacements`/`regex_replacements` to `volumes/v1/convert.py` to fix these OCR blemishes:

1. **Spaced period `first .`**
   * **Regex:** `r'first\s+\.(?=\s+It\s+would\s+have\s+been)'`
   * **Replacement:** `'first.'`

2. **Duplicate comma `apostasy,,`**
   * **Text Replacement:** `'apostasy,,': 'apostasy,'`

3. **Spaced period `Q. 2 .`**
   * **Text Replacement:** `'Q. 2 . What': 'Q. 2. What'`

## 3. Whitelisting of Historical Orthography & False Warnings
Historical spellings and acceptable hyphenated forms will be whitelisted rather than modernized:
* `Spiritual-mindedness`, `Bar-jona`, `pole-star`, `over-valuation`, `day-star`, `merchant-man`, `days-man`, `re-collected`, `re-collection`, `hundred-fold`, `two-fold`, `re-stipulation`, `TWO-FOLD`.

We will also whitelist list sequence jumps that are citations (like `Serm. 13.`, `Chap 10.`) or acceptable/historical list jumps, along with unmatched double quotes due to nesting.
