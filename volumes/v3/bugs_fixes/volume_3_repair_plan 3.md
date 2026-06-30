# Volume 3 Repair Plan

## 1. Punctuation Spacing Blemishes (OCR)
Fix the following spaced punctuation blemishes in `volumes/v3/convert.py` using `text_replacements`:
- `1 .` -> `1.`
- `2dly .` -> `2dly.`
- `3dly .` -> `3dly.`
- `4thly .` -> `4thly.`
- `Ans .` -> `Ans.`
- `end .` -> `end.`
- `idem .` -> `idem.`
- `habit .` -> `habit.`
- `Assimilation :` -> `Assimilation:`
- `transgression :` -> `transgression:`
- `free ;` -> `free;`
- `n )` -> `n)`
- `sin :` -> `sin:`

## 2. Paragraph Split Candidates
Address 14 faulty paragraph splits located in:
- EPUB/ch008.xhtml
- EPUB/ch010.xhtml
- EPUB/ch012.xhtml
- EPUB/ch015.xhtml
- EPUB/ch020.xhtml
- EPUB/ch022.xhtml
- EPUB/ch025.xhtml
- EPUB/ch026.xhtml
Use `paragraph_hooks` or list item corrections in `convert.py` to heal these.

## 3. Whitelist Cleanup
Remove unused items from `volumes/v3/bugs_fixes/volume_3_whitelist.json` and `volume_3_whitelist.md`.
