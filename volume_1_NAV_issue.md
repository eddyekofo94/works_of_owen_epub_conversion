# EPUB NAV Hierarchy Issue - Analysis

## Date: May 5, 2026
## Volume: 1

## THE PROBLEM
User wants hierarchical NAV:
- Level 1: Treatise title ("A DECLARATION OF THE GLORIOUS MYSTERY OF THE PERSON OF CHRIST")
- Level 2: Chapters as children (CHAPTER 1, CHAPTER 2, etc.)

Currently getting: All entries flat at same level.

## CONVERTER FILE: converter.py

### Current (broken) state around lines 1585-1600:
```python
        for ht in ('h1', 'h2', 'h3'):
            if div1.find(ht) is not None:
                h_tag_found = ht
                break
toc_level = level_map.get(h_tag_found, 2) if h_tag_found else 2
        split = _split_nav_title(chapter_title)
        if split:
            treatise, unit = split
            # Treatise at level 2
            toc_entries.append((2, treatise, f'{chapter_id}.xhtml'))
        else:
            # All other entries at level 2 as well
            toc_entries.append((2, chapter_title, f'{chapter_id}.xhtml'))
```

**PROBLEM**: Variable `toc_level` has wrong indentation - not indented inside the for loop. This is a syntax error.

### Lines 1114-1130 (NAV generator):
```python
depth = 0

    for level, text, href in toc_entries:
        while level > depth:
            lines.append('<ol>')
            depth += 1
        while level < depth:
            lines.append('</li>')
            lines.append('</ol>')
            depth -= 1

    lines.append(f'<li><a href="{_html_escape(href)}">{_html_escape(text)}</a>')
```

The code looks syntactically correct here but produces flat output because:
- Both treatise AND chapters get level=2 from the logic above
- So there's no depth change, no nesting

### The `_split_nav_title` function (lines 1058-1071):
```python
def _split_nav_title(title):
    m = re.match(r'^(.+?)\s+((?:CHAPTER|BOOK|PART|SECTION)\s+\d+\.?)$', title.strip(), re.IGNORECASE)
    if m:
        before_unit = m.group(1).rstrip()
        if before_unit.endswith('—') or before_unit.endswith('—'):
            return None
        treatise = before_unit.rstrip('.—:— ')
        unit = m.group(2).strip().rstrip('.')
        return (treatise, unit)
    return None
```

This detects combined titles like "A DECLARATION... CHAPTER 1" and returns (treatise, "CHAPTER 1") tuple.

**THE FIX NEEDED**:
1. Fix the indentation error around line 1589
2. When split is detected:
   - Emit treatise at level 1
   - Emit chapter at level 2
3. Normal chapters (CHAPTER 2, CHAPTER 3, etc.) should also be level 2

## ThML STRUCTURE (volume_1.thml.xml)
- ch008: title="A DECLARATION... CHAPTER 1" (has h1 tag + 40 paragraph content - THIS IS BOTH TITLE + CHAPTER 1 CONTENT!)
- ch009: title="CHAPTER 2" (has h2 tag)
- ch010: title="CHAPTER 3"

The ThML has combined title for ch008 - that's why split() triggers. But all content is in ch008.

## FILES IN EPUB:
- ch008.xhtml: Shows treatise heading + Chapter 1 content
- ch009.xhtml: Chapter 2 content
- All separate .xhtml files exist

## SUMMARY
The issue is in the converter.py code - the level assignment logic. The function should be:
1. If title matches "CHAPTER X" pattern → split into (treatise, chapter)
   - treatise = level 1, chapter = level 2
2. Otherwise all entries at level 2

Current code has syntax error and wrong level assignments.