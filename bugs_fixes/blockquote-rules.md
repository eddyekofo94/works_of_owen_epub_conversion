# Owenian Blockquote Rules

Status: agent instruction and implementation design note.

Blockquotes in the Owen pipeline should represent real displayed quotations in
the source, not merely paragraphs that mention Scripture or begin with a
Scripture reference.

## Core distinction

The safest rule is:

```text
PDF indentation + quotation continuity => blockquote
Scripture-looking prose alone          => not a blockquote
```

Earlier text-only heuristics promoted too many long Scripture-reference
paragraphs into blockquotes. Those false positives were removed. The live
standard is geometry-backed extraction plus conservative render repair.

## What passes as a blockquote

A paragraph should become `[[BLOCKQUOTE]]` / semantic `<blockquote>` when the
source evidence shows displayed quotation behavior:

- The first substantive line is inset relative to the body text left edge.
- The right edge is also inset enough to avoid ordinary body text width.
- The block begins with an explicit quote mark, or it is an allowed continuation
  of an already-open quote run.
- Adjacent inset blocks continue until sentence or quote closure.
- A short scripture reference tail can remain attached to the quote when it is
  visually part of the displayed quotation.
- In sermon volumes, the first blockquote after a sermon chapter heading is
  usually the opening text and may receive `class="sermon-opening-scripture"`.

Known good examples from regression coverage:

- General Preface displayed quotation beginning `"The divines of the Puritan
  school..."`
- Peter's confession displayed as a quotation, while following body exposition
  remains prose.
- Long displayed Scripture quotations such as Revelation 1:5-6, Romans 8:17-18,
  Hebrews 1:10-12.
- Scholastic objection text where the quoted objection begins before the
  extracted `[[BLOCKQUOTE]]` marker and must be pulled inside the blockquote.

## What must not pass as a blockquote

Do not promote prose to blockquote merely because it has one of these features:

- It starts with a Scripture reference.
- It contains a long quotation inline.
- It is a normal body paragraph whose wrapped continuation lines are indented.
- It begins with a list marker, scholastic marker, chapter/part marker, or other
  structural token.
- It is an explanatory paragraph after a displayed quote.
- It is a body paragraph that begins flush left but has later wrapped lines
  aligned with quote indentation.

Known false-positive classes:

- Long Scripture-reference prose blocks.
- Normal body paragraphs where only wrapped lines appear inset.
- List paragraphs such as `1. The faith of Peter...`.
- Body exposition after Peter's confession, including names such as Baronius.
- Lowercase prose following a closed quote plus Scripture reference.

## Boundary rules

Blockquote boundaries matter as much as blockquote detection.

Keep inside the blockquote:

- The displayed quote text.
- Continuation lines while quote punctuation is still open.
- Reference tails that complete the displayed quote, such as `Romans 8:17, 18.`
- Parenthesized reference tails that close an open parenthesis in the quote.

Move outside the blockquote:

- Leading Scripture references that introduce the quote, e.g.
  `1 Corinthians 10:9, "Neither..."` should render the reference separately and
  quote only the quotation.
- Lowercase body prose after a closed quote plus reference.
- Scholastic/list anchors that belong to the surrounding argument.

Special repair:

When a scholastic objection sentence says something like:

```text
Objection 1. But some may say, "Alas! how shall I...

[[BLOCKQUOTE]] and shall I venture...
```

the quoted sentence belongs inside the blockquote. The anchor remains a
list-item paragraph, and the whole quoted objection becomes one blockquote.

## Implementation standard

Extraction-side detection lives in `extract.py`:

- `_line_is_blockquote_candidate()`
- `_text_block_is_blockquote()`
- `_page_starts_with_blockquote_continuation()`
- `_merge_adjacent_blockquote_paragraphs()`

Render-side boundary cleanup lives in `render.py`:

- `_repair_scholastic_blockquote_boundaries()`
- `[[BLOCKQUOTE]]` handling inside `markdown_to_html()`
- leading Scripture-reference extraction from blockquote content
- trailing prose split after closed quoted Scripture

Future fixes should preserve the core posture:

```text
Prefer geometry evidence.
Use text shape only as a boundary repair, not as a primary blockquote detector.
```

## Required regression guards

Any new blockquote fix should add or preserve pytest coverage for:

- A true displayed quote rendered as `<blockquote epub:type="z3998:quotation">`.
- Ordinary body wraps not becoming blockquotes.
- Adjacent blockquote tokens merging until quote/sentence closure.
- Leading Scripture reference split out of blockquote content.
- Trailing prose after a closed quote staying outside the blockquote.
- Scholastic objection quote boundary repair.
- Empty blockquotes never being emitted.
- Sermon-volume first blockquote styling without applying that styling to
  treatise volumes.

Use one volume at a time for validation. For a blockquote extraction change,
prefer the volume that contains the reported sample and run extract only when
the cached JSON must change:

```bash
.venv/bin/python3 volumes/vN/convert.py --extract-only
.venv/bin/python3 volumes/vN/convert.py --render-only
OWEN_REGRESSION_VOLUMES=N .venv/bin/python3 -m pytest tests/test_bug_regressions.py
```
