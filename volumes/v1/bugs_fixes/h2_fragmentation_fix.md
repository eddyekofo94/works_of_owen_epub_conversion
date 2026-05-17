# Bug Report: Fragmented h2 Tags on Treatise Title Pages

## Issue ID
- **Type**: Rendering Bug
- **Affected Volumes**: All (v1, v4, v6, and likely all 16 Owen volumes)
- **Severity**: Medium (visual/formatting issue, no content loss)

---

## Description

Multi-line subtitles on treatise title pages are being output as **multiple separate `<h2>` elements** instead of a single merged heading with line breaks.

### Example - Current (Broken) Output

```html
<section class="treatise-title-page" epub:type="titlepage">
  <h1>TWO SHORT CATECHISMS:</h1>
  <h2>WHEREIN THE</h2>
  <h2>PRINCIPLES OF THE DOCTRINE OF CHRIST,</h2>
  <h2>ARE</h2>
  <h2>UNFOLDED AND EXPLAINED.</h2>
  <p class="descriptive">Proper for all persons...</p>
</section>
```

### Expected (Correct) Output

```html
<section class="treatise-title-page" epub:type="titlepage">
  <h1>TWO SHORT CATECHISMS:</h1>
  <h2>WHEREIN THE<br/>PRINCIPLES OF THE DOCTRINE OF CHRIST,<br/>ARE<br/>UNFOLDED AND EXPLAINED.</h2>
  <p class="descriptive">Proper for all persons...</p>
</section>
```

---

## Affected Chapters (Volume 1)

| Chapter | Subtitle Fragment |
|---------|-------------------|
| ch002.xhtml | "OR", "A DECLARATION OF THE GLORIOUS MYSTERY", "OF", "THE PERSON OF CHRIST — GOD AND MAN:", "WITH" |
| ch025.xhtml | "ON", "THE GLORY OF CHRIST,", "IN", "HIS PERSON, OFFICE, AND GRACE:", "WITH", "THE DIFFERENCES BETWEEN FAITH AND SIGHT;", etc. |
| ch046.xhtml | "WHEREIN THE", "PRINCIPLES OF THE DOCTRINE OF CHRIST,", "ARE", "UNFOLDED AND EXPLAINED." |

---

## Root Cause Analysis

### Location
- **File**: `render.py`
- **Function**: `format_treatise_title_page()` (lines 1835-1914)
- **Problem Area**: Lines 1869-1885 (title merging logic)

### Technical Cause

1. **Strict size tolerance** (line 1877):
   ```python
   if (next_line['size'] > 15 or next_line['has_bold']) and abs(next_line['size'] - line['size']) < 5:
   ```
   - The 5-point size difference threshold is too strict
   - When subtitle lines have even modest size variation (e.g., 14pt vs 20pt), they fail to merge and become separate h2 elements

2. **Separator logic flaw** (lines 1887-1891):
   ```python
   if text.upper() in {'OR', 'OF', 'WITH', 'AS ALSO,'}:
       parts.append(f'<p class="separator"><b>{_html_escape(text)}</b></p>')
   ```
   - Words like "OR", "OF", "WITH" are treated as standalone elements
   - They should be merged into the subtitle as line separators

---

## Secondary Issue: Oversized h2 Font

### Location
- **File**: `shared.py`
- **Line**: 1113

### Current CSS
```css
.treatise-title-page h2 {
    font-size: 1.45em;  /* ~23px at 16px base - larger than h1! */
    margin: 0.8em 0;
    line-height: 1.3;
    font-weight: bold;
    text-transform: uppercase;
}
```

### Problem
- `1.45em` equals approximately 23px at 16px base font
- Standard h2 is `1.15em` (~18px)
- The title page h2 is actually larger than h1, which is visually incorrect

---

## Solution Specification

### Part A: Fix Fragmented h2 Merging

**File**: `render.py`, function `format_treatise_title_page`

#### Change 1: Increase size tolerance (line ~1877)
```python
# BEFORE:
if (next_line['size'] > 15 or next_line['has_bold']) and abs(next_line['size'] - line['size']) < 5:

# AFTER:
if (next_line['size'] > 15 or next_line['has_bold']) and abs(next_line['size'] - line['size']) < 8:
```

#### Change 2: Add subtitle merging logic (after line ~1885)

After extracting the main h1 title, collect and merge all subsequent all-caps subtitle lines into a single h2 element:

```python
# After processing main title (h1)...

# Collect subtitle lines (all remaining uppercase lines before descriptive text)
subtitle_parts = []
subtitle_started = False
i = current_position  # position after h1 processing

while i < len(lines_data):
    line = lines_data[i]
    text = line['text']

    # Stop at first descriptive/italic line (end of subtitle)
    if line['has_italic'] and not line['has_bold']:
        break

    # Skip separators, collect subtitle lines
    if text.upper() not in {'OR', 'OF', 'WITH', 'AS ALSO,', 'AND'}:
        # Include lines that are substantial (not just tiny words)
        if len(text.strip()) > 2:
            subtitle_parts.append(_html_escape(text))

    i += 1

# Output merged subtitle as single h2
if subtitle_parts:
    joined_subtitle = "<br/>".join(subtitle_parts)
    parts.append(f'<h2>{joined_subtitle}</h2>')
    current_position = i  # Update position to skip processed lines
    continue
```

#### Change 3: Modify separator handling (lines ~1887-1891)

Remove or comment out the separator output and let subtitle merging handle these words:

```python
# BEFORE:
if text.upper() in {'OR', 'OF', 'WITH', 'AS ALSO,'}:
    parts.append(f'<p class="separator"><b>{_html_escape(text)}</b></p>')

# AFTER: (comment out or remove - separators now handled in subtitle merge)
# Separator words now merged into subtitle via subtitle_parts collection
```

---

### Part B: Fix h2 Font Size

**File**: `shared.py`, line 1113

```css
/* BEFORE */
.treatise-title-page h2 {
    font-size: 1.45em;
    ...
}

/* AFTER */
.treatise-title-page h2 {
    font-size: 1.15em;  /* Match standard h2 size */
    ...
}
```

---

## Testing Plan

### 1. Regenerate Volume 1
```bash
.venv/bin/python3 volumes/v1/convert.py
# OR
.venv/bin/python3 converter.py 1
```

### 2. Verify Affected Chapters

Extract and inspect treatise title pages:

```bash
unzip -p volumes/v1/output/volume_1.epub EPUB/ch002.xhtml
unzip -p volumes/v1/output/volume_1.epub EPUB/ch025.xhtml
unzip -p volumes/v1/output/volume_1.epub EPUB/ch046.xhtml
```

### 3. Verify Fix Criteria

- [ ] Subtitle "WHEREIN THE..." is a single `<h2>` element
- [ ] Subtitle contains `<br/>` separators between lines
- [ ] Font size is visually smaller (matches h2 standard)
- [ ] No regression in other title pages

### 4. Cross-Volume Check

Test on at least one other volume to verify transfer:
```bash
.venv/bin/python3 converter.py 4
# Check v4 treatise title pages
```

---

## Risk Assessment

| Risk | Level | Mitigation |
|------|-------|------------|
| Breaking existing correct title pages | Low | Changes only affect subtitle section; main titles already merge correctly |
| Over-merging (combining wrong elements) | Low | Subtitle collection stops at first italic/descriptive line |
| Font size change affects readability | Low | 1.15em matches standard h2, which is appropriate |

---

## Dependencies

- None (no external library changes)
- Self-contained to render.py and shared.py

---

## Related Issues

- Issue 26 in extract.py: "avoid fragmented <h2> for multi-line subtitles" (partially addresses this in extraction, but rendering needs completion)
- This bug manifests in the **render** stage, not extraction

---

## Status

- **Identified**: Yes
- **Solution Designed**: Yes
- **Implementation**: IMPLEMENTED (REFINED) (2026-05-17)
- **Testing**: PASSED (Volume 1, verified structural marker separation and case-sensitivity)