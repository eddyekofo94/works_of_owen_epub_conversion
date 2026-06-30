# Volume 5 Repair Plan

## 1. Text Integrity & Fragment Healing
- [ ] Fix missing top window on page 126 (`verse 47, "He that be1ieveth on me has everlasting life;" chapter 7:38,`). Note: contains OCR error `be1ieveth`.
- [ ] Fix missing dense window on page 473 (`tantum religio potuit suadere malorum`).
- [ ] Heal lowercase page fragments:
  - `consciences of believers, unto their supportment and comfort under all their conf`
  - `itself and all grace in due exercise in all ordinances of divine worship, private`
  - `will evidence itself, — not always, but on some occasions: and this is by bringin`
- [ ] Fix punctuation spacing anomalies (`Answer .` -> `Answer.`, `Ans .` -> `Ans.`).
- [ ] Fix OCR typo `A. full comprehension` -> `"A full comprehension` if it's a quote.

## 2. Structural Fixes
- [ ] Fix inline structural candidates:
  - `Lastly, the concluding chapter is devoted...` (ch002.xhtml)
  - `All men in those days were either kept in bondage...` (ch004.xhtml)
- [ ] Fix Roman heading candidate embedded in prose: `III. There is a justification of convinced sinners on their believing.` (ch014.xhtml)
- [ ] Fix overlong chapter headings containing text/scripture:
  - `IMPUTATION OF THE SINS OF THE CHURCH UNTO CHRIST...` (ch012)
  - `THE NATURE OF JUSTIFICATION AS DECLARED IN THE EPISTLES OF ST. PAUL...` (ch022)
  - Apply `treatise_title_overrides` if these are treatise title pages, or `chapter_title_overrides` otherwise.

## 3. Latin Tagging & Translation
- [ ] Map missing Latin phrase: `non solum illa opera legis quae sunt in veteribus sacramentis et nunc`
- [ ] Map untranslated Latin phrases: `Articulus stantis`, `cadentis ecclesiae`, `Albertus Pighius`, `Casparus Ulenbergius`, etc.

## 4. Regressions
- [ ] Fix `Noteref leading spaces` regression: Address the spacing issue with `<a class="noteref noteref-trans"` injections.
