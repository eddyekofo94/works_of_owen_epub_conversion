# Owen Project — Font Rendering Bug & Solution

## Bug: Embedded Fonts Not Respected by Apple Books

### Symptoms
- Apple Books on macOS renders Owen EPUBs with system fallback fonts (Baskerville, Georgia) instead of the embedded primary fonts (Adobe Garamond Pro, Brill, Sabon Next LT, etc.)
- Some font variants (Bold, Italic) fail to display entirely
- The Apple Books font selection menu shows the user's global preference but the actual rendered text doesn't match

### Root Causes (3 issues identified)

#### 1. Font-family name mismatch (CRITICAL)
The CSS `@font-face` declarations used **directory names** as `font-family` values, but the actual internal font-family names embedded in the `.ttf`/`.otf` files are different. Apple Books/WebKit requires these to match.

| Directory name | Internal font name (nameID 1) |
|---|---|
| `Adobe-garamond-pro-2` | `Adobe Garamond Pro` |
| `Minion_pro` | `Minion Pro` (first file was `Minion Pro Cond`) |
| `Libertinus` | `Libertinus Sans` (first file), but should be `Libertinus Serif` |
| `sabon-next-lt` | `Sabon Next LT` |
| `Gentium-plus` | `Gentium Plus` |
| `Brill_font` | `Brill` |
| `Baskervville` | `Baskervville` |
| `Cardo` | `Cardo` |

The `select_primary_font()` function returned the directory name as the font family name, causing a mismatch between the CSS `font-family` declaration and the actual embedded font's internal metadata.

#### 2. Multi-family font directories (Libertinus, Minion_pro)
Some font directories contain **multiple font families**:
- `Libertinus/` has 14 files across 8 families (Serif, Sans, Math, Mono, Keyboard, etc.)
- `Minion_pro/` has 10 files across 4 families (Regular, Condensed, Medium, Semibold)

The old code grabbed ALL files regardless of family, mixing incompatible variants into the same `@font-face` declarations.

#### 3. Missing Proxima Nova heading font
Proxima Nova was available in `fonts/Proxima_Nova/` but was never declared as `@font-face` or used in the CSS. Headings should use Proxima Nova for display purposes.

#### 4. Primary `@font-face` missing weight/style (partial fix already applied)
The primary (regular) font face declaration in `EPUB3_FONT_STYLES` was missing `font-weight: normal; font-style: normal;`. The dynamic variants (bold, italic, bold-italic) were fixed previously.

---

## Solution

### Changes made to `shared.py`

#### 1. Added `FONT_FAMILY_MAP` (line ~1412)
Static mapping from directory names to internal font-family names. Used as fallback when `fontTools` is not available.

#### 2. Added `_get_internal_family_name()` (line ~1443)
Reads the actual `nameID 1` (Font Family) from `.ttf`/`.otf` files using `fontTools.ttLib.TTFont`.

#### 3. Added `_filter_font_files()` (line ~1454)
Filters font files to only include those belonging to the detected primary family. Prevents mixing Libertinus Sans with Libertinus Serif, etc.

#### 4. Rewrote `select_primary_font()` (line ~1471)
Now:
- Reads the internal font-family name from the first file in the directory
- Filters files to only include that family
- Falls back to `FONT_FAMILY_MAP` if `fontTools` is unavailable
- Returns `{'name': internal_family_name, 'files': {...}}`

#### 5. Updated `EPUB3_FONT_STYLES` template (line ~2246)
- Added Proxima Nova `@font-face` declarations (4 variants)
- Split body and heading font rules:
  ```css
  /* Body text uses primary embedded font */
  body, div, p, span {
      font-family: "{primary_font}", "SBL BibLit", serif !important;
  }
  /* Headings use Proxima Nova */
  h1, h2, h3, h4, h5, h6 {
      font-family: "Proxima Nova Rg", "{primary_font}", "SBL BibLit", serif !important;
  }
  ```

#### 6. Added `PROXIMA_NOVA_FILES` constant (line ~1541)
Maps Proxima Nova font files for inclusion in EPUB manifest.

### Changes made to `render.py`

#### 1. Updated import (line 32)
Added `PROXIMA_NOVA_FILES` to the import from `shared`.

#### 2. Updated font embedding loop (line ~2909)
Added `PROXIMA_NOVA_FILES` to the supplemental font embedding:
```python
for _font_dict in (SBL_SUPPLEMENTS, EZRA_SIL_FILES, PROXIMA_NOVA_FILES, TITLE_PAGE_FONTS):
```

---

## What Still Needs Work

### 1. Adobe Garamond Pro detection
The first file sorted alphabetically is `AGaramondPro-Bold.otf`, so the internal name detected is `"Adobe Garamond Pro Bold"` instead of `"Adobe Garamond Pro"`. The `_font_sort_key` in `generate_font_styles()` sorts Regular/Roman first, but `select_primary_font()` picks the **first file** from `os.listdir()` which is unordered. The fix should sort files before picking the first one to detect the family name.

**Fix needed**: In `select_primary_font()`, sort files before detecting the internal name, or scan ALL files to find the most common family prefix.

### 2. Minion Pro detection
Same issue — first file is `MinionPro-Bold.otf` → internal name `"Minion Pro Cond"`. Should detect `"Minion Pro"`.

### 3. Libertinus detection
First file is `LibertinusKeyboard-Regular.otf` → `"Libertinus Keyboard"`. Should detect `"Libertinus Serif"` (the intended body font).

### 4. Rebuild and verify
No volume has been rebuilt yet with these changes. A test rebuild (e.g., `volumes/v1/convert.py`) is needed to verify:
- CSS `font-family` matches internal font names
- All 4 variants (Regular, Bold, Italic, BoldItalic) are properly declared
- Proxima Nova appears in heading rules
- EPUB opens correctly in Apple Books with embedded fonts

### 5. Volume config review
Check each volume's `body_font` setting in `VOLUME_CONFIG` to ensure it maps to a valid directory and the new detection returns the correct family name.

---

## Files Modified
- `shared.py`: `FONT_FAMILY_MAP`, `_get_internal_family_name()`, `_filter_font_files()`, `select_primary_font()`, `EPUB3_FONT_STYLES`, `PROXIMA_NOVA_FILES`
- `render.py`: import of `PROXIMA_NOVA_FILES`, supplemental font embedding loop
