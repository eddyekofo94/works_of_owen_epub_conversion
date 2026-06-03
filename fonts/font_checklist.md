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
- [x] **Adobe Garamond Pro** (`fonts/adobe-garamond-pro-2-2/` — commercial)
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
