# Volume 2 — Textual Blemishes: Root Cause Analysis & Fix Plan

Generated: 2026-05-19

---

## Table of Contents

1. [Blemish 1: ANALYSIS poorly formatted](#blemish-1-analysis-poorly-formatted)
2. [Blemish 2: Fused footnote marker "Himsel[f2]"](#blemish-2-fused-footnote-marker-himsel)
3. [Blemish 3: Ordinal spacing "1st ." / "2ndly ."](#blemish-3-ordinal-spacing)
4. [Blemish 4a: Bracketed enumerator formatting](#blemish-4a-bracketed-enumerator-formatting)
5. [Blemish 4b: Space after opening parenthesis "( John"](#blemish-4b-space-after-opening-parenthesis)
6. [Blemish 5: False breaks before Scripture references](#blemish-5-false-breaks-before-scripture-references)
7. [Blemish 6: Part 3 title page missing "Part 3"](#blemish-6-part-3-title-page)
8. [Blemish 7: A VINDICATION badly extracted](#blemish-7-a-vindication-badly-extracted)
9. [Blemish 8: "p. 280" and "sec. 14" false breaks](#blemish-8-p-280-and-sec-14-false-breaks)
10. [Blemish 9: Scripture reference inside blockquote](#blemish-9-scripture-reference-inside-blockquote)
11. [Blemish 10: "Aen. 10. 846." false break](#blemish-10-aen-10-846-false-break)
12. [Blemish 11: "Liv., Hist. viii. 9." false break](#blemish-11-liv-hist-viii-9-false-break)
13. [Bonus: "I a will" OCR error](#bonus-i-a-will-ocr-error)
14. [Summary: Fix Priority Order](#summary-fix-priority-order)

---

## Blemish 1: ANALYSIS poorly formatted

### Symptom

The ANALYSIS chapter (ch005.xhtml) renders as a wall of text. The outline structure (Part I, II, III with their chapter breakdowns) is not properly distinguished. Some items render as `roman-list-item` while others are `front-matter-prose`, creating visual inconsistency. The Part I/II/III divisions should be clearly separated as sections.

**Current EPUB output** (`EPUB/ch005.xhtml`):
```html
<p class="front-matter-prose first">Part I. — The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted...</p>
<p class="roman-list-item"><b>II.</b> Communion with the FATHER is described,</p>
<p class="roman-list-item"><b>III.</b> and practical inferences deduced from it, IV.</p>
<p class="front-matter-prose">Part II . — The reality of communion with CHRIST is proved, CHAP. I....</p>
```

**Expected output**: Part I, Part II, Part III should each be distinct sections with their chapter sub-items properly nested as list items.

### Raw text (intermediate JSON)

```
[[SUBTITLE]] ANALYSIS.

Part I. — The fact of communion with God is asserted, CHAP. I Passages in Scripture are quoted to show that special mention is made of communion with all the persons of the Trinity,

II. Communion with the FATHER is described,

III. and practical inferences deduced from it, IV.

**Part II** . — The reality of communion with CHRIST is proved, CHAP. I.; and the nature of it is subsequently considered,

II. It is shown to consist in grace; and then the grace of Christ is exhibited under three divisions: — his _personal grace,_ III. — VI.; and under this branch are two long digressions, designed to unfold the glory and loveliness of Christ; _— purchased grace_,

VII. — X.; in which the mediatorial work of Christ is fully considered, in reference to our acceptance with God, VII., VIII.; sanctification, IX.; and the privileges of the covenant, X.; and _grace_ as _communicated_ by — the _Spirit,_ and conspicuous in the fruits of personal holiness. This last division is illustrated under sanctification, as contained under the head of _purchased_ _grace._ **Part III.** - Communion with the HOLY GHOST is expounded in the eight following chapters; — the foundation of it, CHAP. I; his gracious and effectual influence in believers, II.; the elements in which it consists, III.; the effects in the hearts of believers, IV.; and general iuferences and particular directions for communion with the Spirit, V.-VIII.

The arrangement of the treatise may seem involved and complicated...
```

### Root Cause

**File**: `extract.py` — `build_chapters_from_toc()` (line 1588)

The ANALYSIS TOC entry is classified as front-matter (not a treatise, not a body chapter). The raw_text contains a mix of `[[SUBTITLE]]`, body prose, and Roman numeral markers (`II.`, `III.`, `VII.`, etc.) that the render pipeline partially handles via `_coalesce_roman_list_paragraphs()` (render.py line 846), but the overall structure is treated as front-matter prose rather than a structured outline.

The key problem is that "Part I", "Part II", "Part III" markers are embedded within prose paragraphs rather than being recognized as structural section dividers. The `_coalesce_roman_list_paragraphs()` function only handles Roman numeral list items that are already on their own lines with short text, but here the Roman numerals are embedded in longer prose.

**Contributing factors**:
1. `reconstruct_paragraphs()` (extract.py line 1954) joins lines that don't end with terminal punctuation, so "Part I. — The fact..." and "II. Communion with the FATHER..." get merged into one paragraph because the first line ends with a comma.
2. `**Part II** .` has bold markers which prevent `STRUCTURAL_START_RE` from matching.
3. The front-matter rendering path (`render.py` state machine `FRONT_MATTER`) doesn't apply the same structural processing as the body text path.

### Fix Plan

**Option A (Recommended)**: Add a dedicated analysis outline renderer in `render.py`.

1. In `extract.py` `build_chapters_from_toc()`, detect chapters titled "Analysis" and set a flag: `ch["is_analysis"] = True`.
2. In `render.py` `render_volume()`, when processing a chapter with `is_analysis`, use a specialized rendering path that:
   - Splits on "Part I", "Part II", "Part III" markers
   - Renders each Part as an `<h3>` section
   - Renders Roman numeral chapter references as nested list items
3. This preserves the ANALYSIS as a structured outline rather than prose.

**Option B**: Post-process in `volumes/v2/convert.py` with a volume-specific override that rewrites the ANALYSIS chapter's raw_text to insert proper structural tokens (`[[PART]]`, `[[ROMAN_HEAD]]`) before rendering.

**Option C**: Improve `_coalesce_roman_list_paragraphs()` to handle outline-style content with mixed Part I/II/III headers. This is the most general fix but risks affecting other volumes.

**Recommendation**: **Option A** — Cleanest separation of concerns, volume-specific without being hacky.

**Estimated effort**: Medium (new rendering path, ~50-80 lines)

---

## Blemish 2: Fused footnote marker "Himsel[f2]"

### Symptom

In ch017, the text renders as:
```html
<p class="list-item"><b>1.</b> Himsel<a class="noteref" epub:type="noteref" role="doc-noteref" href="endnotes.xhtml#fn2"><sup>2</sup></a>. His kingdom.</p>
```

The word "Himself" is split into "Himsel" + noteref + ". His kingdom." — the footnote marker `[f2]` was glued to "Himsel" without a space, so the footnote conversion turned `Himsel[f2]` into `Himsel<a...>2</a>`, breaking the word.

**Expected**: `<b>1.</b> Himself.<a class="noteref"...><sup>2</sup></a> His kingdom.`

### Raw text (intermediate JSON, Chapter 16)

```
Now, the things which in this communion Christ reveals to them that he delights in, may be referred to these two heads: —

1. Himsel[f2]. His kingdom.

1. Himself.

John 14:21, "He that loveth me shall be loved of my Father...
```

### Root Cause

**File**: `extract.py` — `_normalize_extracted_footnote_markers()` (line 1828)

The PDF extraction produced `Himsel[f2]` without a space between the word and the footnote marker. The normalization function at line 1835:
```python
text = re.sub(r'(\[f\d+\])(?=[A-Za-z])', r'\1 ', text)
```
This adds a space AFTER the marker when followed by a letter, but does NOT add a space BEFORE the marker when it's glued to a preceding word. So `Himsel[f2]` stays as `Himsel[f2]`, and later when footnote markers are converted to noteref links, the word is split.

The regex `LOOSE_FOOTNOTE_MARKER_RE` (render.py lines 73-80) catches loose markers like `f2` or `[ f2]` but not `word[fN]`.

### Fix Plan

**File**: `extract.py` line 1835

Add a space BEFORE the footnote marker when it's glued to a word character:

```python
def _normalize_extracted_footnote_markers(text):
    """Normalize AGES inline markers before paragraph healing can merge words."""
    def repl(match):
        fn = next(group for group in match.groups() if group)
        return f'[f{fn}]'

    text = LOOSE_FOOTNOTE_MARKER_RE.sub(repl, text)
    # Insert space between word character and footnote marker: word[fN] -> word [fN]
    text = re.sub(r'([A-Za-z])(\[f\d+\])', r'\1 \2', text)
    # Insert space after footnote marker when followed by letter: [fN]word -> [fN] word
    text = re.sub(r'(\[f\d+\])(?=[A-Za-z])', r'\1 ', text)
    return text
```

**Why this works**: The new regex `r'([A-Za-z])(\[f\d+\])'` captures any letter immediately followed by a footnote marker and inserts a space between them. This handles `Himsel[f2]` → `Himsel [f2]`.

**Side effects to check**: Ensure this doesn't affect cases where footnote markers are intentionally adjacent to punctuation (e.g., `word.[f1]` — the `.` is not `[A-Za-z]`, so this won't match, which is correct).

**Estimated effort**: Low (2-line fix)

---

## Blemish 3: Ordinal spacing "1st ." / "2ndly ."

### Symptom

Multiple chapters have ordinal markers with a space before the period:
- `**1st** . Resolution, and a zealous, violent casting off...`
- `**2ndly** . Diligence. "I will now take another course...`

This renders as `<b>1st .</b>` instead of `<b>1st.</b>`.

**Affected chapters**: ch009, ch010, ch014, ch015, ch016, ch017, ch021, ch022, ch023, and others — pervasive throughout the volume.

### Raw text (intermediate JSON, Chapter 16)

```
It carries, —

**1st** . Resolution, and a zealous, violent casting off that frame wherein she had lost her love. "'I a will arise;' I will not rest in this frame: I am undone if I do." So, sometimes God calls his church to arise and shake itself out of the dust. Abide not in this condition.

**2ndly** . Diligence. "I will now take another course; I will leave no way unattempted, no means untried, whereby I may possibly recover communion with my Beloved."
```

### Root Cause

**File**: `extract.py` — `clean_text()` (line 1881)

The `clean_text()` function has a regex to fix ordinal spacing:
```python
text = re.sub(r'\b(\d+(?:st|nd|rd|th))\s+([,.;])', r'\1\2', text)
```

This handles `1st ,` → `1st,` for plain ordinals, but when the ordinal is wrapped in bold markers (`**1st** .`), the `\b` word boundary doesn't match because `**` intervenes between the ordinal and the space. The regex sees `**1st** .` and the `\b` before `1st` matches, but the pattern expects the ordinal to be followed directly by `\s+([,.;])`, not by `**\s+.`.

Additionally, the regex doesn't handle adverbial ordinals like `2ndly`, `3rdly` — it only matches `st|nd|rd|th`, not `ly` or `dly` suffixes.

### Fix Plan

**File**: `extract.py` line 1881

Replace the ordinal spacing fix with a more comprehensive version:

```python
# Fix ordinal spacing: "1st ." -> "1st.", "**1st** ." -> "**1st**.", "2ndly ," -> "2ndly,"
# Handles both plain and bold-wrapped ordinals, including adverbial forms
text = re.sub(
    r'(\*\*)?(\d+(?:(?:st|nd|rd|th)ly|dly|ly|st|nd|rd|th))(\*\*)?\s+([,.;])',
    r'\1\2\3\4',
    text
)
```

This regex:
1. Optionally matches `**` prefix
2. Matches the ordinal number with suffix (including `ly`, `dly` for adverbial forms)
3. Optionally matches `**` suffix
4. Matches one or more spaces followed by punctuation
5. Reconstructs without the space

**Test cases**:
- `1st .` → `1st.`
- `**1st** .` → `**1st**.`
- `2ndly .` → `2ndly.`
- `**2ndly** .` → `**2ndly**.`
- `3rd ,` → `3rd,`

**Estimated effort**: Low (1-line fix)

---

## Blemish 4a: Bracketed enumerator formatting

### Symptom

Bracketed enumerators like `[1].` and `[2.]` are not consistently bolded. In the raw text:
```
[1]. In respect of sanctification;
[2.] In respect of consolation: —
```

These should render as bold list items like `<p class="list-item"><b>[1].</b> In respect of sanctification;</p>` but the formatting is inconsistent.

### Root Cause

**File**: `render.py` — `STRUCTURAL_START_RE` (line 90) and `emphasize_structural_prefix()` (line 648)

`STRUCTURAL_START_RE` at line 90 matches `\[\d+\.?\]\s+` which handles `[1.] ` and `[2.] `. However, `[1].` (bracket around number only, period outside) doesn't match this pattern — the regex expects the period INSIDE the brackets.

The `[1].` and `[2.]` markers in the raw text don't have bold markdown (`**`) around them, so they pass through as plain text. The `emphasize_structural_prefix()` function wraps markers in `<b>` tags, but only when they're at the START of a paragraph matched by `STRUCTURAL_PREFIX_HTML_RE`. If the paragraph starts with something else, the marker won't be bolded.

### Fix Plan

**File**: `render.py` — `emphasize_structural_prefix()` (line 648)

Ensure that bracketed enumerators `[N.]` and `[N].` are consistently bolded:

1. Verify `STRUCTURAL_PREFIX_HTML_RE` includes both `[N.]` and `[N].` patterns
2. Add a post-processing step to bold any remaining unbolded bracketed enumerators in list-item paragraphs

```python
def _bold_bracketed_enumerators(html):
    """Bold bracketed enumerators that weren't caught by structural prefix emphasis."""
    return re.sub(
        r'<p class="list-item">(?!<b>)(\[\d+\.?\])\s+',
        r'<p class="list-item"><b>\1</b> ',
        html
    )
```

**Priority**: LOW — Structural markers are detected, just not bolded consistently. The visual impact is minor.

**Estimated effort**: Low

---

## Blemish 4b: Space after opening parenthesis "( John"

### Symptom

In ch021, the text renders as:
```html
<p class="list-item">(2.)<b> He sends them his Holy Spirit, to quicken them, </b>( John 6:63, to cause them that are "dead to hear his voice," John 5:25; ...</p>
```

The `( John 6:63` has an unnecessary space after the opening parenthesis. This is a known issue that has been occurring since Volume 1.

### Raw text (intermediate JSON, Chapter 20)

```
Therefore, —

**(2.)** He sends them his Holy Spirit, to quicken them, **( John 6:63, to cause them that are "dead to hear his voice," John 5:25; and to work in them whatever is required of them, to make them partakers of his righteousness and accepted with God. Thus does Christ deal with his: — he lives and dies with an intention to work out and complete righteousness f
```

### Root Cause

**File**: `extract.py` — `clean_text()` (line 1864)

The `clean_text()` function has a regex to remove spaces after opening parentheses before scripture references:
```python
text = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', text, flags=re.I)
```

This should remove the space in `( John 6:63`, but the raw text still shows `**( John 6:63`. The most likely explanation is that the bold markers `**` are added during extraction (in `build_chapters_from_toc()` or `post_process_paragraphs()`), and the regex at line 1864 doesn't account for `**` before the parenthesis.

Actually, the regex `\(\s+(?=...)` matches `(` followed by whitespace, regardless of what comes before. The `**` before `(` doesn't affect the match. So why isn't it working?

The answer: the regex at line 1864 uses `SCRIPTURE_BOOK_RE` which is defined in `render.py` (line 314-323). If `extract.py` doesn't properly import or define this variable, the regex would fail silently or not match as expected.

### Fix Plan

**File**: `extract.py` line 1864

1. First, verify that `SCRIPTURE_BOOK_RE` is properly available in `extract.py` at line 1864.
2. Add a more general fix for `( ` → `(` that doesn't depend on scripture book detection:

```python
# Remove space after opening parenthesis (general case)
text = re.sub(r'\(\s+([A-Z])', r'(\1', text)
# Remove space after opening parenthesis before scripture references (specific case)
text = re.sub(rf'\(\s+(?=(?:[1-3]\s+)?{SCRIPTURE_BOOK_RE}\b)', '(', text, flags=re.I)
```

3. Also handle the bold-wrapped case explicitly:
```python
text = re.sub(r'\*\*\(\s+([A-Z])', r'**(\1', text)
```

**Priority**: HIGH — Affects readability and has been present since v1.

**Estimated effort**: Low (1-2 line fix)

---

## Blemish 5: False breaks before Scripture references

### Symptom

Sentences ending with terminal punctuation followed by a Scripture reference on the next line get split into separate paragraphs. The Scripture reference appears as the start of a new paragraph instead of continuing the previous one.

**Examples from the blemish file**:
```
"He looks upon them sometimes in distress, and considers what is the state of the world in reference to them.
Zechariah 1:11, "We have walked to and fro through the earth, and, behold, all the earth sitteth still, and is at rest," say his messengers to him..."

"to bear their sins."
Isaiah 53:11, "He shall bear their iniquities;"

"or put to death for it, are the same.
Ezekiel 18:20,"
```

### Root Cause

**File**: `extract.py` — `reconstruct_paragraphs()` (line 1954)

The paragraph healer processes lines one at a time. When it encounters:
1. A line ending with terminal punctuation (`.`, `!`, `?`, optionally followed by `"`)
2. Followed by a blank line
3. Followed by a line starting with an uppercase letter

It treats this as a paragraph boundary (line 2064: "Terminal punctuation + uppercase start → new paragraph").

Scripture references that start with book names (Zechariah, Isaiah, Ezekiel, etc.) are uppercase and get false-split. The healer has no awareness that a line starting with a Bible book name is likely a scripture citation continuing the previous thought, not a new paragraph.

The existing guards in `reconstruct_paragraphs()` include:
- `CONNECTOR_STARTERS_RE`: checks if the next line starts with connector words ("Wherefore", "But", "And", etc.)
- `starts_lower`: checks if the line starts with lowercase (join)
- `is_inside_quote`: checks for unclosed quotes (join)
- `starts_with_connector`: checks for connector words (join)

None of these catch scripture book names.

### Fix Plan

**File**: `extract.py` — `reconstruct_paragraphs()`, around line 2038-2063

Add a check for scripture book names before the new-paragraph decision:

```python
# In the main merge-or-break decision (around line 2038):
starts_with_scripture = bool(re.match(
    rf'^(?:[1-3]\s+)?(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
    r'Samuel|Kings|Chronicles|Ezra|Nehemiah|Esther|Job|Psalms|Proverbs|Ecclesiastes|'
    r'Song|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|'
    r'Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|'
    r'Acts|Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|'
    r'Thessalonians|Timothy|Titus|Philemon|Hebrews|James|Peter|Jude|Revelation)\b',
    stripped, re.I
))

# Also check for bare scripture references like "1:5" or "12:4-6"
starts_with_bare_ref = bool(re.match(r'^\d+:\d+', stripped))

if starts_with_scripture or starts_with_bare_ref:
    # Scripture reference continuing previous thought → join
    current.append(stripped)
    continue
```

This should be added in the decision block at line 2050-2066, before the "Terminal punctuation + uppercase start → new paragraph" fallback.

**Important**: This fix should only apply when the previous line ends with terminal punctuation AND the current line starts with a scripture reference. We don't want to join ALL scripture references to their preceding text — only those that are clearly continuations (i.e., the previous sentence introduced a quote or claim that the scripture supports).

A more conservative approach: only join when the previous line ends with a quote mark or the current line starts with a scripture reference followed by a quote:

```python
prev_ends_with_quote = bool(re.search(r'["\u201d]\s*$', prev))
current_starts_with_scripture_and_quote = bool(re.match(
    rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\s+\d+:\d+.*["\u201c]',
    stripped, re.I
))

if prev_ends_with_quote or current_starts_with_scripture_and_quote:
    current.append(stripped)
    continue
```

**Priority**: HIGH — Occurs frequently throughout the text, affecting readability.

**Estimated effort**: Medium (new logic in paragraph healer, ~15-25 lines)

---

## Blemish 6: Part 3 title page missing "Part 3"

### Symptom

Part 3's title page (ch024.xhtml) only contains:
```html
<h4 class="chapter-subtitle">OF COMMUNION WITH THE HOLY GHOST.</h4>
```

It's missing "Part 3" or "PART III" as a heading. Compare with Part 1 (ch006.xhtml) which has:
```html
<p class="title-line title-line-major">PART 1.</p>
```

And Part 2 (ch011.xhtml) which has a proper title page with "PART 2."

### Raw text (intermediate JSON, Chapter 23)

```
[[SUBTITLE]] OF COMMUNION WITH THE HOLY GHOST.
```

The TOC entry title is "Part 3 - Of Communion With the Holy Ghost." but the raw_text only contains the subtitle portion.

### Root Cause

**File**: `extract.py` — `build_chapters_from_toc()` (line 1588)

The TOC entry for Part 3 is "Part 3 - Of Communion With the Holy Ghost." The chapter extraction pulls text from the PDF pages assigned to this TOC entry. The PDF's Part 3 title page apparently only contains "OF COMMUNION WITH THE HOLY GHOST" without the "PART III" text, or the "PART III" text is on a separate page that's assigned to a different TOC entry.

Comparing with Part 1 and Part 2:
- Part 1's PDF title page has "PART 1." prominently displayed
- Part 2's PDF title page has "PART 2." prominently displayed
- Part 3's PDF title page may have "PART III" in a different format or on a different page

The `build_chapters_from_toc()` function assigns pages to chapters based on TOC entry page numbers. If the "PART III" text is on a page that's assigned to a different TOC entry (e.g., the last chapter of Part 2), it won't appear in Part 3's raw_text.

### Fix Plan

**Option A (Recommended)**: Add a volume-specific override in `volumes/v2/convert.py` to inject the Part 3 title:

```python
def _fix_part3_title(raw_text):
    """Ensure Part 3 title page includes 'PART III' heading."""
    if raw_text.strip().startswith('[[SUBTITLE]] OF COMMUNION WITH THE HOLY GHOST'):
        return '[[PART]] PART III.\n\n[[SUBTITLE]] OF COMMUNION WITH THE HOLY GHOST.'
    return raw_text
```

Apply this as a post-processing step on the intermediate JSON before rendering.

**Option B**: Fix in `render.py` — when rendering a chapter whose title contains "Part N" but the raw_text doesn't include a corresponding title line, inject a `[[PART]]` marker.

**Option C**: Fix in `extract.py` — improve page assignment logic to ensure Part title pages include the Part number.

**Recommendation**: **Option A** — Simplest, most targeted fix. Part 3's title page issue is volume-specific.

**Estimated effort**: Low (volume-specific override)

---

## Blemish 7: A VINDICATION badly extracted

### Symptom

The VINDICATION treatise has three chapters in the intermediate JSON:
- **ch032**: Title page only (610 chars) — contains pre-rendered HTML with malformed CSS classes: `title-line -major` (missing prefix)
- **ch033**: Prefatory Note (4,387 chars) — proper content
- **ch034**: Full text (254,853 chars) — starts with ANOTHER title page, also with malformed CSS

The title page chapters have malformed CSS class names like `<p class="title-line -major">` instead of `<p class="title-line-major">`. The word "title-line-" is followed by a space and then the size class, creating invalid CSS classes.

### Raw text (intermediate JSON, Chapter 32)

```html
<section class="treatise-title-page" epub:type="titlepage"> <p class="title-line -major">A VINDICATION</p> <p class="title-line -medium">OF</p> <p class="title-line -medium">SOME PASSAGES</p> <p class="title-line -medium">IN A</p> <p class="title-line -medium">DISCOURSE CONCERNING</p> <p class="title-line -medium">COMMUNION WITH GOD</p> <p class="title-line -medium">BY</p> <p class="title-line -medium">JOHN OWEN</p> <p class="descriptive">A Vindication of some Passages in a Discourse concerning Communion with God, from the Exceptions of William Sherlock, rector of St. George, Botolph Lane</p> </section>
```

Note: `title-line -major` should be `title-line-major`.

### Root Cause

**File**: `extract.py` — title page extraction for VINDICATION

The VINDICATION title page is extracted as pre-rendered HTML (not markdown). This happens when the PDF's title page is detected as a structured title page and the extraction produces HTML directly instead of markdown text. The HTML is then stored in `raw_text` as-is.

The malformed CSS classes (`title-line -major` instead of `title-line-major`) come from the PDF extraction. The PyMuPDF4LLM or span extraction is producing `title-line` and `-major` as separate tokens that get joined with a space.

The deeper issue is that ch032 and ch034 both contain title page content for the same treatise. The TOC has two entries that map to the VINDICATION treatise:
1. "A Vindication of Some Passages in a Discourse Concerning Communion" → ch032 (title page)
2. "A Vindication" → ch034 (full text, which ALSO starts with a title page)

This duplication suggests the TOC parsing is creating two chapters for what should be one treatise with a single title page.

### Fix Plan

**Step 1**: Fix malformed CSS classes in `extract.py` or `render.py`.

Add a cleanup step for pre-rendered HTML in `raw_text`:

```python
def _fix_title_page_css(raw_text):
    """Fix malformed CSS classes in pre-rendered title page HTML."""
    # Fix "title-line -major" -> "title-line-major"
    raw_text = re.sub(r'class="title-line\s+(-(?:major|medium|minor|small))"',
                      r'class="title-line\1"', raw_text)
    return raw_text
```

**Step 2**: Merge duplicate title pages.

In `build_chapters_from_toc()`, detect when consecutive chapters for the same treatise both contain title page content, and merge them or skip the duplicate.

Alternatively, add a volume-specific override in `volumes/v2/convert.py`:

```python
def _fix_vindication_title(chapters):
    """Fix VINDICATION title page issues."""
    for ch in chapters:
        if 'vindication' in ch.get('title', '').lower():
            ch['raw_text'] = _fix_title_page_css(ch.get('raw_text', ''))
    return chapters
```

**Step 3**: Ensure the VINDICATION title page in ch034 is properly rendered.

The ch034 raw_text starts with a title page section that has the same malformed CSS. After fixing the CSS, ensure the title page renders correctly as a `treatise-title-page` section.

**Priority**: MEDIUM — Affects one treatise's presentation.

**Estimated effort**: Medium (CSS fix is easy, TOC merge is more complex)

---

## Blemish 8: "p. 280" and "sec. 14" false breaks

### Symptom

Page and section references are split across paragraphs:

**Example 1** (Chapter 34, raw_text):
```
which he treats of, p.

280. "As for example," saith he, "Christ is called a husband, the church his spouse; — and what other men call believing the gospel of Christ, these
```

**Example 2** (Chapter 34, raw_text):
```
unto the law of God whereunto we were subject and obliged, p. 181,' sec.

14. And it is strange to apprehend how he came to imagine that I said he did it not as our mediator, but as a private man.
```

The `p.` and `sec.` abbreviations end with periods (terminal punctuation), and the following line starts with a number. The paragraph healer treats this as a paragraph boundary.

### Root Cause

**File**: `extract.py` — `reconstruct_paragraphs()` (line 1954)

The paragraph healer's decision logic at line 2064:
```python
# Terminal punctuation + uppercase start → new paragraph
paragraphs.append(' '.join(current))
current = [stripped]
```

When the previous line ends with `p.` or `sec.` (terminal punctuation) and the next line starts with a number like `280` or `14`, the healer creates a new paragraph. It has no awareness that `p. 280` is a page reference that should stay attached to the preceding text.

The existing guards don't cover this case:
- `ends_terminal`: True (`p.` ends with `.`)
- `starts_lower`: False (`280` starts with a digit, not lowercase)
- `is_dangling`: False (no dangling connector)
- `is_semantic_connector`: False
- `is_inside_quote`: Depends on context
- `starts_with_connector`: False

So the fallback "Terminal punctuation + uppercase start → new paragraph" triggers.

### Fix Plan

**File**: `extract.py` — `reconstruct_paragraphs()`, around line 2038-2063

Add a check for reference abbreviations before the new-paragraph decision:

```python
# Check if previous line ends with a reference abbreviation
ref_abbrevs = r'(?:p|pp|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))

# Check if current line starts with a reference number
starts_with_ref_number = bool(re.match(r'^\d{1,4}\b', stripped))

# Check if current line starts with a Roman numeral (for classical refs like "viii. 9")
starts_with_roman = bool(re.match(r'^[ivxlcdm]+\.\s+\d', stripped, re.I))

if prev_is_ref_abbrev and (starts_with_ref_number or starts_with_roman):
    # Reference number continuing previous thought → join
    current.append(stripped)
    continue
```

This should be added in the decision block at line 2050-2066, before the "Terminal punctuation + uppercase start → new paragraph" fallback.

**Additional fix**: Handle the case where the reference abbreviation and number are on the SAME line but separated by a blank line in the PDF extraction. The `reconstruct_paragraphs()` function processes blank lines as potential paragraph boundaries (line 1963-1982). We need to ensure that `p.\n\n280` is joined, not split.

In the blank-line handling section (line 1963-1982), add:

```python
if current:
    prev = current[-1]
    prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
    # Look ahead for reference number
    if prev_is_ref_abbrev and next_nonempty is not None:
        if re.match(r'^\d{1,4}\b', next_nonempty):
            # Don't break — reference number continues
            continue
```

**Priority**: HIGH — Occurs multiple times in the VINDICATION treatise and affects readability.

**Estimated effort**: Medium (new logic in paragraph healer, ~20-30 lines)

---

## Blemish 9: Scripture reference inside blockquote

### Symptom

In ch040, the raw text has:
```
[[BLOCKQUOTE]] 1 Corinthians 10:9, "Neither let us tempt Christ, as some of them also tempted, and were destroyed of serpents;" compared with Numbers 21:6.
```

The scripture reference "1 Corinthians 10:9" is part of the blockquote content, but it should be outside the blockquote as a standalone reference that introduces the quoted text.

**Expected**:
```
1 Corinthians 10:9,
[[BLOCKQUOTE]] "Neither let us tempt Christ, as some of them also tempted, and were destroyed of serpents;" compared with Numbers 21:6.
```

### Root Cause

**File**: `extract.py` — blockquote detection in `clean_text()` or `build_chapters_from_toc()`

The PDF has the scripture reference on the same line as the blockquote marker `>`. During extraction, the `>` marker is converted to `[[BLOCKQUOTE]]`, and the scripture reference gets included in the blockquote content.

In `render.py` `markdown_to_html()` (line 1138), lines starting with `>` are converted to `[[BLOCKQUOTE]]` tokens. The entire line after `>` becomes the blockquote content, including the scripture reference.

### Fix Plan

**File**: `render.py` — `markdown_to_html()`, in the `[[BLOCKQUOTE]]` handling (around line 1233)

When processing `[[BLOCKQUOTE]]` content, check if the content starts with a scripture reference. If so, extract it as a separate paragraph before the blockquote:

```python
def _extract_scripture_from_blockquote(content):
    """Extract leading scripture reference from blockquote content."""
    match = re.match(
        rf'^((?:[1-3]\s+)?(?:Genesis|Exodus|...|Revelation)\s+\d+:\d+(?:[-,]\s*\d+)*)\s*,?\s*(.+)$',
        content, re.I | re.S
    )
    if match:
        ref = match.group(1)
        rest = match.group(2)
        return ref, rest
    return None, content

# Usage in markdown_to_html():
if token.startswith('[[BLOCKQUOTE]]'):
    content = token[len('[[BLOCKQUOTE]]'):].strip()
    ref, content = _extract_scripture_from_blockquote(content)
    if ref:
        # Render scripture ref as separate paragraph
        html_parts.append(f'<p class="scripture-ref">{ref},</p>')
    # Render blockquote with remaining content
    html_parts.append(f'<blockquote epub:type="z3998:quotation"><p>{_render_blockquote_content(content)}</p></blockquote>')
```

**Priority**: LOW — Affects one instance in v2, but the pattern may recur in other volumes.

**Estimated effort**: Low (~15 lines)

---

## Blemish 10: "Aen. 10. 846." false break

### Symptom

In ch042 (Appendix), the raw text has:
```
was slain Aeneas: —

[[BLOCKQUOTE]] "Tantane me tenuit vivendi, nate, voluptas, Ut pro me hostile paterer succedere dextrae Quem genui? tuane haec genitor per vulnera servor, Morte tua vivens?" — Aen.

10. 846.
```

The Virgil reference "Aen. 10. 846." is split across paragraphs. "Aen." ends with a period, and "10" starts with a digit, so the paragraph healer splits them.

### Root Cause

**File**: `extract.py` — `reconstruct_paragraphs()` (line 1954)

Same root cause as Blemish 8. "Aen." (Aeneid) is a classical reference abbreviation that ends with a period. The following line "10. 846." starts with a number. The paragraph healer treats this as a paragraph boundary.

### Fix Plan

**File**: `extract.py` — `reconstruct_paragraphs()`

The fix for Blemish 8 already covers this case. The `ref_abbrevs` pattern includes `aen\.?` and `liv\.?` for classical references:

```python
ref_abbrevs = r'(?:p|pp|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
```

When "Aen." is the previous line and "10" is the current line, `prev_is_ref_abbrev` will be True and `starts_with_ref_number` will be True, so they'll be joined.

**Note**: The "10. 846." part also needs to be joined. After "Aen." and "10" are joined, we have "Aen. 10." which ends with a period, and "846." starts with a digit. The same logic should apply — but "10." is not a reference abbreviation. We need an additional check:

```python
# If previous line ends with a number followed by period (like "10."),
# and current line starts with a number, join them
prev_ends_with_number_period = bool(re.search(r'\d+\.\s*$', prev))
if prev_ends_with_number_period and starts_with_ref_number:
    current.append(stripped)
    continue
```

**Priority**: LOW — Only affects classical references in the Appendix.

**Estimated effort**: Covered by Blemish 8 fix + 3 additional lines.

---

## Blemish 11: "Liv., Hist. viii. 9." false break

### Symptom

In ch042 (Appendix), the raw text has:
```
to appease the anger of the gods, and to transfer destruction from their own army to the enemies," Liv., Hist. viii.

9. His son, in like manner, in a great and dangerous battle against the Gauls and Samnites...
```

The Livy reference "Liv., Hist. viii." is split, and "9." is incorrectly treated as a structural list marker (a numbered list item).

### Root Cause

**File**: `extract.py` — `reconstruct_paragraphs()` (line 1954) and `STRUCTURAL_START_RE` (render.py line 84)

Two issues compound here:
1. **False paragraph break**: "viii." ends with a period, "9" starts with a digit → new paragraph (same as Blemish 8)
2. **False structural marker**: "9." at the start of a line matches `STRUCTURAL_START_RE`'s pattern `(?!\d{4}\.)\d{1,3}\.\s+` (line 87), which treats it as a numbered list item.

### Fix Plan

**File**: `extract.py` — `reconstruct_paragraphs()`

The fix for Blemish 8 covers the false paragraph break. The `ref_abbrevs` pattern includes `liv\.?` and `hist\.?` for Livy references.

For the false structural marker issue, we need to add a guard in `reconstruct_paragraphs()` to prevent bare decimal numbers from being treated as structural markers when they follow a classical/historical reference abbreviation:

```python
# In the structural start handling (around line 1994):
if STRUCTURAL_START_RE.match(stripped):
    # Check if this is a false positive: a bare number following a reference abbreviation
    if current:
        prev = current[-1]
        prev_is_classical_ref = bool(re.search(
            r'\b(?:liv|aen|hist|tac|plut|cic|sen|aug)\.?\s+(?:hist\.?\s+)?[ivxlcdm]+\.\s*$',
            prev, re.I
        ))
        is_bare_decimal = bool(re.match(r'^\d{1,2}\.\s+[A-Z]', stripped))
        if prev_is_classical_ref and is_bare_decimal:
            # This is a classical reference number, not a list marker → join
            current.append(stripped)
            continue
```

**Priority**: LOW — Only affects one instance in the Appendix.

**Estimated effort**: Covered by Blemish 8 fix + ~10 additional lines.

---

## Bonus: "I a will" OCR error

### Symptom

In ch017, the raw text has:
```
"'I a will arise;' I will not rest in this frame: I am undone if I do."
```

The word "will" is corrupted to "a will". This is a PDF extraction OCR error.

### Root Cause

**File**: PDF extraction (PyMuPDF4LLM or span extraction)

The PDF's text for this passage contains an OCR artifact where "I will" is read as "I a will". This is not caught by the existing OCR repair functions.

The existing `_repair_owen_ocr_errors()` function (render.py line 289) handles:
- `]y` → `ly` (e.g., "on]y" → "only")
- `]e` → `le`
- `]` before "earn/earning/earned/earnt/edge" → `l`
- Volume-specific text replacements from config

It does NOT handle "I a will" → "I will".

### Fix Plan

**File**: `volumes/v2/convert.py` — Add volume-specific text replacement

```python
OVERRIDES = {
    'text_replacements': {
        'I a will': 'I will',
    },
}
```

Alternatively, add a general regex in `_repair_owen_ocr_errors()`:

```python
# Fix "I a will" → "I will" (OCR artifact)
text = re.sub(r'\bI a will\b', 'I will', text)
```

**Check other volumes**: Search for "I a will" in other Owen volumes to see if this is a v2-only issue or a general OCR problem.

**Priority**: MEDIUM — Clear OCR error that affects readability.

**Estimated effort**: Low (1-line fix)

---

## Summary: Fix Priority Order

### HIGH Priority (fix first)

| # | Blemish | Root File | Fix Type | Lines | Impact |
|---|---------|-----------|----------|-------|--------|
| 2 | Fused footnote marker `Himsel[f2]` | `extract.py:1835` | Regex | 2 | Word corruption |
| 4b | Space after paren `( John` | `extract.py:1864` | Regex | 2 | Readability, v1+ issue |
| 5 | False breaks before Scripture refs | `extract.py:2063` | Logic | 20 | Frequent, pervasive |
| 8 | `p. N` / `sec. N` false breaks | `extract.py:2063` | Logic | 25 | VINDICATION treatise |

### MEDIUM Priority

| # | Blemish | Root File | Fix Type | Lines | Impact |
|---|---------|-----------|----------|-------|--------|
| 3 | Ordinal spacing `1st .` | `extract.py:1881` | Regex | 1 | Pervasive, readability |
| 6 | Part 3 title page | `v2/convert.py` | Override | 5 | Visual inconsistency |
| 7 | VINDICATION title page CSS | `extract.py` | CSS fix + merge | 20 | One treatise |
| OCR | "I a will" | `v2/convert.py` | Text replacement | 1 | OCR error |

### LOW Priority

| # | Blemish | Root File | Fix Type | Lines | Impact |
|---|---------|-----------|----------|-------|--------|
| 4a | Bracketed enumerator bolding | `render.py` | Regex | 5 | Minor visual |
| 9 | Scripture ref in blockquote | `render.py` | Logic | 15 | One instance |
| 10 | Classical ref false break | `extract.py` | Same as #8 | 3 | Appendix only |
| 11 | Livy ref false break | `extract.py` | Same as #8 | 10 | Appendix only |
| 1 | ANALYSIS formatting | `render.py` | New renderer | 60 | Front matter |

### Shared Fixes

Blemishes **5, 8, 10, and 11** all share the same root cause — `reconstruct_paragraphs()` splitting on terminal punctuation + uppercase/digit start. A single comprehensive fix in that function (adding scripture/reference continuation awareness) would resolve all four.

The combined fix for these would be:

```python
# In reconstruct_paragraphs(), before the "Terminal punctuation + uppercase start → new paragraph" fallback:

# Scripture reference continuation
starts_with_scripture = bool(re.match(rf'^(?:[1-3]\s+)?(?:{SCRIPTURE_BOOK_RE})\b', stripped, re.I))
starts_with_bare_ref = bool(re.match(r'^\d+:\d+', stripped))

# Reference abbreviation continuation (p. 280, sec. 14, Aen. 10, etc.)
ref_abbrevs = r'(?:p|pp|sec|chap|vol|cf|see|ibid|id|op\.?|cit\.?|fol\.?|col\.?|liv\.?|aen\.?|hist\.?)\.?'
prev_is_ref_abbrev = bool(re.search(rf'\b{ref_abbrevs}\s*$', prev, re.I))
starts_with_ref_number = bool(re.match(r'^\d{1,4}\b', stripped))
prev_ends_with_number_period = bool(re.search(r'\d+\.\s*$', prev))

# Classical reference continuation (Liv., Hist. viii. 9)
prev_is_classical_ref = bool(re.search(
    r'\b(?:liv|aen|hist|tac|plut|cic|sen|aug)\.?\s+(?:hist\.?\s+)?[ivxlcdm]+\.\s*$',
    prev, re.I
))
is_bare_decimal = bool(re.match(r'^\d{1,2}\.\s+[A-Z]', stripped))

if starts_with_scripture or starts_with_bare_ref:
    current.append(stripped)
    continue
if prev_is_ref_abbrev and (starts_with_ref_number or prev_ends_with_number_period):
    current.append(stripped)
    continue
if prev_is_classical_ref and is_bare_decimal:
    current.append(stripped)
    continue
```

This single addition (~25 lines) would resolve blemishes 5, 8, 10, and 11 simultaneously.

---

## Implementation Order Recommendation

1. **Phase 1**: Fix blemishes 2, 4b, 3 (regex fixes in `extract.py`) — quick wins, high impact
2. **Phase 2**: Fix blemishes 5, 8, 10, 11 (combined paragraph healer fix) — medium effort, high impact
3. **Phase 3**: Fix blemishes 6, 7, OCR (volume-specific overrides in `v2/convert.py`) — targeted fixes
4. **Phase 4**: Fix blemishes 4a, 9, 1 (rendering improvements) — polish

Total estimated effort: ~150 lines of code changes across 3 files (`extract.py`, `render.py`, `volumes/v2/convert.py`).
