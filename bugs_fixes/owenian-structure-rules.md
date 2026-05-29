# Owenian Structure Rules

## Editor Problem:
This is for trying to solve the problem bellow:
“In common with the authors of that age, Owen indulged freely in divisions and subdivisions of any topic under his consideration. The numerals employed to indicate the progress of thought were found in much confusion, — omissions occurring even in the early editions which appeared before the author's death, and changes having been subsequently introduced (of course without the author's sanction), which often destroy the connection and force of his statements, and bewilder his readers in a labyrinthine maze of numeration. Care has been taken to rectify these errors, and the subdivisions are denoted by the usual gradation in the numerals — I, 1, (1), [1], first, and first . It would have been an advantage if we could have dispensed with this cumbrous and complex apparatus; but such a course would have been questionable in principle, and indeed, on a little examination, will be seen to have been impossible.”
-William H. Goold, v1, General Preface.


Status: master agent instruction and implementation standard.

This file defines the structural reading model for Owen volumes. It supersedes
one-off rules for flat lists, block lists, nested markers, and blockquotes.
Future fixes should preserve this model unless the user explicitly changes the
standard.

## Core Principle

Owen's typography is not modern outline typography. The converter should render
his structure by rhetorical function:

```text
announced syllabus      -> inline with its anchor sentence
exposition of a head    -> block paragraph
nested proof/subpoint   -> modestly indented block paragraph
displayed quotation     -> semantic blockquote
ordinary prose          -> ordinary paragraph
```

Marker shape is a clue, not a final decision. Owen reuses `1.`, `(1.)`,
`[1.]`, `1st.`, `2dly.`, and Roman numerals in multiple roles.

## Flat Syllabus Lists

A flat syllabus is a compact list of heads attached to an anchor sentence.
It should render inline in the same paragraph as the anchor.

Typical pattern:

```text
For the first, there are four things in sin that clearly shine out in the
cross of Christ: —
(1.) The desert of it.
(2.) Man's impotency by reason of it.
(3.) The death of it.
(4.) A new end put to it.
```

Correct rendering:

```text
For the first, there are four things in sin that clearly shine out in the
cross of Christ: — (1.) The desert of it. (2.) Man's impotency by reason of it.
(3.) The death of it. (4.) A new end put to it.
```

Strong flat-syllabus anchors include:

- Count words: `two`, `three`, `four`, `six`, etc.
- Category words: `things`, `heads`, `parts`, `ways`, `accounts`, `regards`,
  `sorts`, `considerations`, `observations`.
- Introductory formulas: `observe`, `required`, `consists in`, `reduced unto`,
  `may be referred to`, `I understand`, `there are`, `these following`.
- Terminal forms: `: —` or `—`.

Flat syllabus items normally look like labels:

- Short noun phrases or brief clauses.
- Parallel grammar across items.
- Items ending with periods, semicolons, commas, or colons.
- Count matching the anchor when a count is explicit.
- No item reads like a developed proof or exposition paragraph.

Known flat examples:

```text
may be referred to two heads: — 1. Temptations. 2. Afflictions.

I shall briefly observe four things therein: — (1.) Sweetness. (2.) Delight.
(3.) Safety. (4.) Comfort.

The desert of sin does clearly shine in the cross of Christ upon a twofold
account: — [1.] Of the person suffering for it. [2.] Of the penalty he
underwent.

Now, that one may walk with another, six things are required: — 1. Agreement.
2. Acquaintance. 3. A way. 4. Strength. 5. Boldness. 6. An aiming at the same
end.
```

## Block Exposition Lists

Block exposition lists are where Owen begins to explain one of the announced
heads. They should remain separate paragraphs.

Typical pattern:

```text
(1.) The desert of sin does clearly shine in the cross of Christ upon a
twofold account: —
[1.] Of the person suffering for it.
[2.] Of the penalty he underwent.

[1.] Of the person suffering for it. This the Scripture oftentimes...
```

The first `[1.]` / `[2.]` pair is a flat syllabus under `(1.)`; the second
`[1.]` restarts the exposition and should remain a block paragraph.

Block indicators:

- Marker sequence restarts after a flat syllabus.
- Paragraph contains developed sentences, proofs, scripture chains, or
  argumentation.
- Paragraph explains a previously announced head.
- Preceding phrase is explanatory, especially `whereby ... : —`.
- Item length or syntax reads like prose rather than a label.

## Nested Marker Levels

Use paragraph classes, not real HTML ordered lists. Owen's outlines are too
rhetorical and irregular for strict `<ol>` nesting.

Recommended semantic levels (Three-Level Visual Hierarchy):

```text
flat-syllabus        inline, no paragraph class (syllabus introductions)
list-level-1         Level 1: Main exposition block (e.g. bare decimals '1.' or Roman 'I.')
list-level-2         Level 2: Nested proof/subdivision (e.g. parenthesized '(1.)' or bracketed '[1.]')
list-level-3         Level 3: Local rhetorical subpoints (e.g. ordinals '1st.' or '2ndly.')
roman-subheading     major Roman section heading
```

Marker-family hints:

```text
I. II. III.          major Roman section or formal outline head
1. 2. 3.             primary heads or compact syllabus
(1.) (2.) (3.)       exposition heads or secondary syllabus
[1.] [2.] [3.]       nested subpoints under a parent item
1st. 2dly. 3dly.    local rhetorical subpoints
```

### 1. Robust Casing Safety for Digit Ordinals
To prevent asymmetric nesting errors where one ordinal (e.g., `1st`) is grouped at `list-level-3` while another (e.g., `2ndly`) falls back to `list-level-1` (which ruins reading continuity and breaks the layout on mobile), the classification engine (`_owen_marker_level`) must use an **uppercase-safe regex**:
```python
is_digit_ordinal = bool(re.search(r'\d(?:ST|ND|RD|TH|DLY|LY)', clean_upper))
```
This guarantees that all adjacent digit ordinals are matched and grouped together at the exact same semantic nesting level (`list-level-3`).

### 2. Three-Level Hierarchy Nesting Rules
* **First Level (list-level-1):** Bare decimals `1.` and Roman numerals `I.` are top-level and serve as the main expository anchors.
* **Second Level (list-level-2):** Parenthesized Arabic `(1.)` and bracketed Arabic `[1.]` represent secondary developments and are nested under the active Level 1 branch.
* **Third Level (list-level-3):** Local rhetorical subpoints (ordinals like `1st.`, `Secondly`) represent local lists or logical lists. They are nested under the active Level 2 branch. This prevents Owen's outlines from going deeper than 3 levels, ensuring text remains highly legible on narrow mobile displays.

Context overrides marker shape. For example:

- `(1.)` after a flat syllabus restart is usually `list-level-1`.
- `[1.]` after a `twofold account` anchor may be flat syllabus.
- `[1.]` after `whereby ... : —` should usually remain block/nested.
- `1st.`, `2dly.`, `3dly.` inside an argument are local subpoints, usually
  nested under their active parent item.

To prevent "patchy" disconnected borders and margin jump-backs when a nested point spans multiple paragraphs or blockquotes, we wrap the entire scope of a subdivision in a nested `<div class="owen-branch owen-level-X">` container. 

The vertical margins, padding, and vertical borders are shifted from the `<p>` tags to these `.owen-branch` parent containers, which creates a single, unbroken vertical hairline down the entire subdivision.

Reader-facing CSS uses compact, mobile-friendly spacing to prevent text from being crushed on narrow iPhone screens:

```css
/* Container for a nested branch (allows natural page breaks inside) */
div.owen-branch {
    margin-top: 0.6em;
    margin-bottom: 0.6em;
    break-inside: auto !important;
    page-break-inside: auto !important;
    -webkit-column-break-inside: auto !important;
}

/* Level 1: Outer major division (no left-border/indent, logical group only) */
div.owen-level-1 {
    margin-left: 0;
    border-left: none;
    padding-left: 0;
}

/* Level 2: Nested proof/subdivision under current exposition. Uses soft Owen Blue */
div.owen-level-2 {
    margin-left: 0.75em !important;
    border-left: 1.5px solid rgba(42, 85, 160, 0.12) !important;
    padding-left: 0.6em !important;
}

/* Level 3: Local subpoints (clean indent, no double border) */
div.owen-level-3 {
    margin-left: 0.75em !important;
    border-left: none !important;
    padding-left: 0 !important;
}

/* Individual list-item paragraphs inside the container sit flush */
.list-item.list-level-1,
.roman-list-item.list-level-1,
.list-item.list-level-2,
.list-item.list-level-3,
.roman-list-item.list-level-2,
.roman-list-item.list-level-3 {
    margin-left: 0 !important;
    border-left: none !important;
    padding-left: 0 !important;
}

/* Nested blockquotes alignment */
div.owen-branch blockquote {
    margin-left: 0.8em !important;
    border-left: 1.5px solid rgba(0, 0, 0, 0.06) !important;
    padding-left: 0.8em !important;
}
```

Paragraphs that have absorbed a flat syllabus inline receive the additional
class `syllabus-anchor`. The bold markers (`(1.)`, `(2.)`, etc.) remain as
inline `<b>` text so readers can parse the enumeration boundaries.

## Blockquote Rules

Blockquotes should represent real displayed quotations in the source, not
paragraphs that merely mention Scripture or begin with Scripture references.

Core rule:

```text
PDF indentation + quotation continuity => blockquote
Scripture-looking prose alone          => not a blockquote
```

What passes as a blockquote:

- The first substantive line is inset relative to the body text left edge.
- The right edge is also inset enough to avoid ordinary body text width.
- The block begins with an explicit quote mark, or is an allowed continuation
  of an open quote run.
- Adjacent inset blocks continue until sentence or quote closure.
- A short Scripture reference tail can remain attached when it visually
  completes the displayed quote.
- In sermon volumes, the first blockquote after a sermon chapter heading is
  usually the opening text and may receive `class="sermon-opening-scripture"`.

What must not pass as a blockquote:

- Prose merely starting with a Scripture reference.
- A long inline quotation inside normal prose.
- A normal body paragraph whose wrapped continuation lines are indented.
- List items, scholastic markers, chapter/part markers, or other structural
  tokens.
- Exposition after a closed displayed quote.

Boundary rules:

- Keep displayed quote text and closing reference tails inside the blockquote.
- Move leading Scripture references outside when they introduce the quote.
- Move lowercase body prose after a closed quote plus reference outside.
- Repair scholastic objection boundaries when a quoted objection begins before
  the extracted `[[BLOCKQUOTE]]` marker.

## Implementation Standard: Two-Stage Visual Nesting Pipeline

We implement structural visual nesting in two clean stages at the end of the post-processing pipeline in `render.py`:

1. **Paragraph Classification (`_add_owen_list_level_classes`):**
   * Identifies structural markers (`(1.)`, `[1.]`, `1st.`, etc.) and adds the corresponding reader-facing classes (`list-level-1`, `list-level-2`, `list-level-3`) to the individual paragraphs.
2. **DOM-Tree Nesting Parser (`_nest_owen_list_hierarchies`):**
   * Processes the flat HTML block elements (paragraphs, blockquotes, headings, horizontal rules, tables) and wraps them in nested `<div class="owen-branch owen-level-X">` containers.
   * **Stack State Machine:** Uses an integer stack (`active_levels`) to track nesting depths.
     * *Ascend (`L > current_active`):* Opens intermediate `<div class="owen-branch owen-level-L">` containers and pushes `L` to stack.
     * *Descend/Sibling (`L <= current_active`):* Closes active branches down to and including level `L`, and opens a new sibling container at level `L`.
     * *Continuation Blocks:* Elements with no list level (continuation prose paragraphs, blockquotes) inherit the active nesting level and are appended directly inside the active container.
     * *Reset boundaries:* Structural headings (`h1`–`h6`), signatures, footnotes (`aside`), and horizontal rules (`hr`) have level `0`, which resets the nesting stack entirely (closes all open branches).
   * **Fidelity Protection:** Uses an exact regex span scanner to capture and preserve all unmatched intermediate or trailing text fragments, ensuring zero content or comment loss.

Do not rely only on word counts. Word caps are guard rails. The primary
question is rhetorical:

```text
Is this the announced syllabus, or the explanatory treatment of one head?
```

When a run contains both, flatten only the valid syllabus prefix and leave the
remaining items as block paragraphs.

## False-Positive Guards

Preserve these guards:

- `whereby ... : —` nested lists remain block/nested.
- Scripture verse continuations are not list anchors.
- Author initials such as `R. D. Kimchi` are not Roman/list markers.
- Roman outline headings are not flattened as ordinary labels.
- Long explanatory paragraphs remain block.
- Text-only Scripture-looking prose is not promoted to blockquote.
- Body wraps are not promoted to blockquote merely because continuation lines
  are indented.

### Signal F word cap

Signal F (explicit binary introduction) allows a higher per-item word ceiling
than the global hard cap, but the allowance is deliberately tight:

```text
_EM_DASH_FLAT_HARD_CAP + 8  (= 20 words per item)
```

Owen's genuine binary flat labels ("Of the person suffering for it. / Of the
penalty he underwent.") are comfortably under 15 words. Items reaching 21+
words after a "twofold account" introduction are almost always exposition
openings and must remain block paragraphs. The hard veto is bypassed for
Signal F, so the cap here is the only safety valve — do not raise it without a
concrete corpus example.

### Anchor paragraph word cap

A list-item paragraph ending with `—` may serve as an anchor for a following
flat sub-list. It allows attachment when:

- It contains at most one bold structural marker, AND
- Its plain-text word count is ≤ 80 (raised from the original 45), OR
- Its tail matches an explicit-count pattern (count word + category word), OR
- Its tail matches a formula pattern ("these following", "I shall observe",
  "may be considered", "as follows", etc.).

The 80-word general limit prevents a long merged list paragraph from
accidentally absorbing an unrelated following run. The formula patterns catch
Owen phrasings that do not contain explicit count words but still introduce a
genuine flat syllabus.

## Required Regression Coverage

Any structural refactor should include tests for:

- Multi-item flat syllabus followed by marker restart.
- `twofold account` and `two heads` flat pairs.
- OCR-split flat tail such as `2.` followed by `Afflictions.`
- Long explanatory item remaining block.
- `whereby ... : —` nested list remaining block.
- `[1.]` nested subpoints receiving a reader-facing level class.
- `1st.`, `2dly.`, `3dly.` local markers receiving a deeper level when
  context indicates nesting.
- Roman headings remaining headings.
- Scripture verse continuations and author initials staying prose.
- True displayed blockquotes rendering semantically.
- Body wraps and Scripture-looking prose not becoming blockquotes.

Validate one volume at a time. For the current refactor, Volume 2 is the
proving volume.
