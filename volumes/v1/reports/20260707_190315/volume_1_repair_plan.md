# Volume 1 Repair Plan

## 1. Dense Source Window Investigation (Warnings: 1)
- **Objective:** Clear `dense_source_window_loss` warning.
- **Action:** Investigate the 30 missing windows (e.g. on pages 53, 56, 76, 78, 83, 90, 101, 105, 106, 117).
- **Fix:** Apply `text_replacements` or paragraph hooks to heal them, as these appear to be scripture strings that got incorrectly removed.

## 2. OCR & Word Loss Healing
- **Objective:** Fix compound word loss reported in Text Integrity check.
- **Action:** Address instances of `pre-eminence` and `heavenly-mindedness` being truncated or split.
- **Fix:** Add them to `text_replacements` in `volumes/v1/convert.py`.

## 3. Whitelist & Tagging Accuracy
- **Objective:** Improve Latin tagging accuracy and clear intentional omissions.
- **Action:**
  - Whitelist pseudo-Latin English words (`incarnate`, `nestorius`, `consummate`, `ultimate`, `adequate`, `invocate`, `inanimate`, `indicate`, `thomas`, `serm`).
  - Whitelist Front CONTENTS pages (pages 3, 4, 5, 6).
- **Fix:** Add these entries to `volumes/v1/bugs_fixes/volume_1_whitelist.json` and `.md`.

## 4. Citation and Latin Translation
- **Objective:** Improve Latin translation ratio from 62.4%.
- **Action:** Identify unresolved Latin phrases and Patristic citations.
- **Fix:** Add translations for the untranslated Latin phrases found (e.g., `quam conspici`, `totam eclesiam`, etc.) to the citations mapping.

## 5. Structural Adjustments
- **Objective:** Fix reported structural fragments.
- **Action:** Address the Roman Heading Candidate in `ch033.xhtml` (I. 1. What he did...) and the Short Fragments (e.g., `Edinburgh, August 1850`).
