# Volume 6 Repair Plan

This plan tracks quality repairs to bring John Owen's Works, Volume 6, into the `PRISTINE` tier (Need score < 20).

## Checklist

### 1. Patristic & Classical Citations
- [x] Map and resolve all 0 unresolved patristic/classical citations (none found).

### 2. OCR Corrections & Typos
- [x] Fix `Proper-ties` -> `Properties` (Chapter 3)
- [x] Fix `fiuctibus` -> `fluctibus` (Austin quote, Psalm 130 Exposition)
- [x] Fix `legera` -> `legem` (Psalm 130 Exposition)
- [x] Fix `axe come in` -> `are come in` (Psalm 69 quote)
- [x] Fix `east into` -> `cast into` (Psalm 88 quote)
- [x] Fix `suaxum` -> `suarum` (Austin quote)
- [x] Fix `seasonlHow` -> `season! How` (Chapter 8)
- [x] Fix `Adam)were` -> `Adam) were` (First Promise chapter)
- [x] Fix `the]east` -> `the least` (Testimonies chapter)
- [x] Fix `the]ate` -> `the late` (Application chapter)

### 3. Latin Translation Database Additions
- [x] Add all 20 missing Latin phrase translations to `scripts/translation_db.py`:
  - `saepius morti proximus`
  - `Vindiciae Evangelicae`
  - `as a "causa sine qua non`
  - `probatum est`
  - `mihi plaudo`
  - `ingentia decora`
  - `actus primo primi`
  - `Cogitatio morosa cum`
  - `sub ratione boni`
  - `juris" or "facti`
  - `profundus fuit`
  - `sub molibus et fluctibus`
  - `Deprecationum mearum`
  - `Gratiosus fuit`
  - `Condonatio ipsa`
  - `Propter legem tuam`
  - `Ut sis terribilis`
  - `Quo fugis`
  - `accesseris oras`
  - `semper eris`

### 4. Layout & Structural False Positives
- [x] Whitelist front-matter TOC page and metadata page omissions.
- [x] Whitelist signature/salutation paragraph splits.
- [x] Whitelist roman/list numeral starts.
- [x] Whitelist legitimate thematic repetitions of Psalm 130 verses.
