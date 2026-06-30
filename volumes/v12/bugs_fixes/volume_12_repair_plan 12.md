# Volume 12 Repair Plan

This plan details the steps to repair paragraph splits, punctuation spacing blemishes, missing list markers, and other OCR anomalies in **Volume 12** to maintain its **PRISTINE** quality status and further reduce its Need score (currently 8.3).

## 1. Punctuation Spacing Blemishes
Add the following to `text_replacements` in `volumes/v12/convert.py`:
- [ ] `"True ,"` -> `"True,"`
- [ ] `"is ,"` -> `"is,"`
- [ ] `"also ."` -> `"also."`
- [ ] `"ejus ;"` -> `"ejus;"`
- [ ] `"est ,"` -> `"est,"`
- [ ] `"t )"` -> `"t)"`
- [ ] `"fieri ,"` -> `"fieri,"`
- [ ] `"not ,"` -> `"not,"`

## 2. Missing Enumerator Markers
- [ ] Restore missing `(1.)` marker near "them to Palaeologus. f75 By this course of behavior, the man had these two advantages: — (1.)"
- [ ] Restore missing `(8.)` marker near "f is as high a pitch of blasphemy as any creature in this world can possibly arrive unto. (8.)"

## 3. Missing Latin Clauses & Tagging
- [ ] Check missing Latin clause on page 593: `oppressus et affiictus fuit et non`. If it's a false positive, whitelist it.
- [ ] Whitelist the "Untranslated Latin Samples" which are mostly names (Grotius, Socinus, Smalcius, Crellius, Petavius, etc.) or short non-translatable Latin phrases.

## 4. Other
- [ ] Check missing front CONTENTS page 5. If it's just the book title or front matter misidentified, whitelist it.
- [ ] Check the 1 mismatched footnote (1091 noteref vs 1090 endnote anchors).
