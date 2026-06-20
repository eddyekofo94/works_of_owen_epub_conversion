# John Owen Project — Fonts Checklist

This checklist tracks the status of the font files required by the EPUB conversion pipeline.
Each font should be located in `fonts/<font_folder>/` so that the symlink in the `Owen` project resolves to it correctly.

## Core Project Fonts Checklist

### 1. SBL and Ancient Language Fonts (Society of Biblical Literature / GFS)
- [x] **SBL BibLit** (`fonts/sbl-blit/SBL_BLit.ttf`) — *Primary polyglot support*
- [x] **SBL Greek** (`fonts/sbl-blit/SBL_grk.ttf`) — *Greek text formatting fallback*
- [x] **SBL Hebrew** (`fonts/sbl-blit/SBL_Hbrw.ttf`) — *Hebrew text formatting*
- [x] **GFS Porson** (`fonts/gfs-porson/GFSPorson.ttf`) — *Primary polyglot Greek text formatting*

### 2. Ezra SIL (Society of Biblical Literature / SIL)
- [x] **Ezra SIL** (`fonts/ezra-sil-2-51/SILEOT.ttf`) — *Hebrew text rendering fallback*

### 3. Open-Source Serif Fonts (OFL / Google Fonts)
- [x] **Baskervville**
  - [x] Regular (`fonts/baskerville/BaskervilleBT.ttf`)
  - [x] Italic (`fonts/baskerville/BaskervilleItalicBT.ttf`)
- [x] **Cardo**
  - [x] Regular (`fonts/cardo/Cardo-Regular.ttf`)
  - [x] Bold (`fonts/cardo/Cardo-Bold.ttf`)
  - [x] Italic (`fonts/cardo/Cardo-Italic.ttf`)
- [x] **Gentium Plus**
  - [x] Regular (`fonts/gentium-plus-2/GentiumPlus-R.ttf`)
  - [x] Italic (`fonts/gentium-plus-2/GentiumPlus-I.ttf`)
- [x] **STIX Two Text**
  - [x] Regular (`fonts/stix-two-text/STIXTwoText.ttf`)
  - [x] Italic (`fonts/stix-two-text/STIXTwoText-Italic.ttf`)
- [x] **Libertinus Serif**
  - [x] Regular (`fonts/libertinus/LibertinusSerif-Regular.ttf`)
  - [x] Italic (`fonts/libertinus/LibertinusSerif-Italic.ttf`)
  - [x] Bold (`fonts/libertinus/LibertinusSerif-Bold.ttf`)
  - [x] Bold Italic (`fonts/libertinus/LibertinusSerif-BoldItalic.ttf`)

### 4. High-Quality Academic / Commercial Fonts (Pre-packaged)
- [x] **Brill Font** (Academic use only, copied from backup)
  - [x] Roman/Regular (`fonts/brill-font/Brill-Roman.ttf`)
  - [x] Italic (`fonts/brill-font/Brill-Italic.ttf`)
  - [x] Bold (`fonts/brill-font/Brill-Bold.ttf`)
  - [x] Bold Italic (`fonts/brill-font/Brill-BoldItalic.ttf`)
- [x] **Minion Pro** (Commercial, copied from backup)
  - [x] Regular (`fonts/minion-pro/MinionPro-Regular.otf`)
  - [x] Italic (`fonts/minion-pro/MinionPro-It.otf`)
  - [x] Bold (`fonts/minion-pro/MinionPro-Bold.otf`)
  - [x] Bold Italic (`fonts/minion-pro/MinionPro-BoldIt.otf`)
  - [x] Semibold (`fonts/minion-pro/MinionPro-Semibold.otf`)
  - [x] Semibold Italic (`fonts/minion-pro/MinionPro-SemiboldIt.otf`)
  - [x] Medium (`fonts/minion-pro/MinionPro-Medium.otf`)
  - [x] Medium Italic (`fonts/minion-pro/MinionPro-MediumIt.otf`)
- [x] **Arno Pro** (Commercial, copied from backup)
  - [x] Regular (`fonts/arno-pro/fonnts.com-Arno-Pro-.otf`)

### 5. Other Mentioned/Commercial Fonts
- [x] **Adobe Garamond Pro** (`fonts/adobe-garamond-pro/` — commercial)
- [x] **Sabon Next LT** (`fonts/sabon-next-lt/` — commercial)
- [x] **Proxima Nova** (Heading-only font, commercial)
  - [x] Regular (`fonts/proxima-nova/Proxima Nova Regular.ttf`)
  - [x] Extrabold (`fonts/proxima-nova/Proxima Nova Extrabold.ttf`)
  - [x] Light (`fonts/proxima-nova/Proxima Nova Light.ttf`)
  - [x] Semibold (`fonts/proxima-nova/Proxima Nova Semibold.ttf`)

### 6. Elegant display & heading additions (New)
- [x] **Cormorant Garamond**
  - [x] Regular (`fonts/cormorant-garamond/CormorantGaramond-Regular.ttf`)
  - [x] Italic (`fonts/cormorant-garamond/CormorantGaramond-Italic.ttf`)
- [x] **IM Fell English**
  - [x] Regular (`fonts/im-fell-english/IMFellEnglish-Regular.ttf`)
  - [x] Italic (`fonts/im-fell-english/IMFellEnglish-Italic.ttf`)
- [x] **Libre Caslon Text**
  - [x] Regular/Variable (`fonts/libre-caslon-text/LibreCaslonText-VariableFont_wght.ttf`)
  - [x] Italic/Variable (`fonts/libre-caslon-text/LibreCaslonText-Italic-VariableFont_wght.ttf`)
- [x] **Playfair Display**
  - [x] Regular/Variable (`fonts/playfair-display/PlayfairDisplay-VariableFont_wght.ttf`)
  - [x] Italic/Variable (`fonts/playfair-display/PlayfairDisplay-Italic-VariableFont_wght.ttf`)

---

## Restoring Progress

| Font Family | Status | Restoration Source / Note |
|---|---|---|
| **SBL BibLit** | ✅ Restored | Copied from system |
| **SBL Greek** | ✅ Restored | BibLit copy fallback |
| **SBL Hebrew** | ✅ Restored | BibLit copy fallback |
| **GFS Porson** | ✅ Restored | Copied from GFS GFS_Porson subfolders |
| **Ezra SIL** | ✅ Restored | Copied from Downloads |
| **Baskervville** | ✅ Restored | Downloaded from web |
| **Cardo** | ✅ Restored | Downloaded from web |
| **Gentium Plus** | ✅ Restored | Copied from system |
| **STIX Two Text** | ✅ Restored | Copied from system |
| **Libertinus Serif** | ✅ Restored | Downloaded from web |
| **Brill Font** | ✅ Restored | Copied from Theology/fonts backup |
| **Minion Pro** | ✅ Restored | Copied from Theology/fonts backup |
| **Arno Pro** | ✅ Restored | Copied from Theology/fonts backup |
| **Adobe Garamond Pro** | ✅ Restored | Copied AGaramondPro-Regular from system |
| **Cormorant Garamond** | ✅ Restored | Downloaded from web |
| **IM Fell English** | ✅ Restored | Downloaded from web |
| **Libre Caslon Text** | ✅ Restored | Downloaded from web |
| **Playfair Display** | ✅ Restored | Downloaded from web |
| **Sabon Next LT** | ✅ Restored | Copied from Downloads (commercial) |
| **Proxima Nova** | ✅ Restored | Copied from Downloads (commercial) |
| **Inter** | ✅ Downloaded | Downloaded from Google Fonts |
| **Roboto** | ✅ Downloaded | Downloaded from Google Fonts |
| **Merriweather** | ✅ Downloaded | Downloaded from Google Fonts |
| **Cinzel** | ✅ Downloaded | Downloaded from Google Fonts |
| **Montserrat** | ✅ Downloaded | Downloaded from Google Fonts |
| **EB Garamond** | ✅ Downloaded | Downloaded from Google Fonts |
| **Literata** | ✅ Downloaded | Downloaded from Google Fonts |

---

## Volume Font Assignments

Based on the current pipeline configuration (`shared.py`), here is the body font assignment for each volume:

### Owen Works (16 Volumes)
| Volume | Subtitle/Content | Assigned Body Font |
|---|---|---|
| **Volume 1** | The Glory of Christ | `adobe-garamond-pro` |
| **Volume 2** | Communion with God | `libertinus` |
| **Volume 3** | The Holy Spirit | `minion-pro` |
| **Volume 4** | The Work of the Spirit | `cardo` |
| **Volume 5** | Faith and Its Evidences | `brill-font` |
| **Volume 6** | Temptation and Sin | `baskerville` |
| **Volume 7** | Sin and Grace | `sabon-next-lt` |
| **Volume 8** | Sermons to the Nation | `palatino` |
| **Volume 9** | Sermons to the Church | `im-fell-english` |
| **Volume 10** | The Death of Christ | `eb-garamond` |
| **Volume 11** | Continuing in the Faith | `adobe-carlson-pro` |
| **Volume 12** | The Gospel Defended | `arno-pro` |
| **Volume 13** | Ministry and Fellowship | `itc-galliard` |
| **Volume 14** | True and False Religion | `centaur` |
| **Volume 15** | Church Purity and Unity | `new-caledonia-lt-std` |
| **Volume 16** | The Church and the Bible | `georgia` |

### Hebrews Commentary (7 Volumes)
| Volume | Content | Assigned Body Font |
|---|---|---|
| **Volume h1** | Preliminary Exercitations (Part 1) | `cormorant-garamond` |
| **Volume h2** | Preliminary Exercitations (Part 2) | `goudi` |
| **Volume h3** | Exposition of Hebrews 1:1 – 3:6 | `coelacanth` |
| **Volume h4** | Exposition of Hebrews 3:7 – 5:14 | `playfair-display` |
| **Volume h5** | Exposition of Hebrews 6:1 – 7:28 | `libre-caslon-text` |
| **Volume h6** | Exposition of Hebrews 8:1 – 10:39 | `merriweather` |
| **Volume h7** | Exposition of Hebrews 11:1 – 13:25 | `literata` |

---

## Font Pairings & Combinations

Below is the definitive list of typographic combinations mapped out for this project, tailored for digital/mobile reading and theological weight:

| Body Font | Ideal Heading Font | Visual Aesthetic & Best Use |
|---|---|---|
| **Garamond** | Garamond Bold or Baskerville | *Classic & Warm.* General fiction, historical fiction, memoirs. |
| **Caslon** | Caslon Bold/Semibold or Garamond Italic | *Historic Authority.* High literary fiction, historical narratives. |
| **Sabon** | Sabon Bold, Futura, or Gill Sans | *Quiet Prestige.* Poetry, premium literary, geometric contrast. |
| **Baskerville** | Baskerville Bold or Italic | *Intellectual & Crisp.* Contemporary literary, authoritative non-fiction. |
| **Minion Pro** | Minion Bold or Myriad Pro | *Invisible Workhorse.* Clean, highly functional digital-first design. |
| **Palatino** | Palatino Bold or Optima | *Open Proportions.* Generous spacing for older/younger readers. |
| **Georgia** | Georgia Bold or Arial/Helvetica | *Screen-Optimized.* Digital literature, low-resolution constraints. |
| **Bembo** | Trajan or Cinzel | *The Cathedral Aesthetic.* Uses Roman monumental capitals for a timeless, sacred appearance. |
| **SBL BibLit** | SBL BibLit Bold | *The Academic Standard.* Kept uniform, clean, and strictly focused on the text's data. |
| **Galliard** | Optima (or Classico) | *The Modern Liturgical.* Optima is a sans-serif with a humanist swell that pairs beautifully with historic serifs. |
| **Merriweather** | Montserrat | *The Modern Digital First.* Clean, highly readable, and perfectly optimized for app-based reading environments. |
