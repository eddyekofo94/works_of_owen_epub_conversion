# Owenian Flat-List Rules

Status: agent instruction and implementation design note.

This repository uses "flat list" in a specific Owenian sense. A flat list is
not merely a short list. It is a compact syllabus that Owen attaches to an
anchor sentence before he begins the real scholastic exposition.

## Core distinction

Owen often writes in two movements:

1. An anchor sentence announces a count or category and ends with `: —` or `—`.
2. A compact numbered syllabus gives the heads to be discussed.
3. The exposition restarts the same or a related marker family and treats each
   head in full.

The syllabus should be rendered inline with the anchor sentence. The exposition
should remain as block list paragraphs.

Example:

```text
For the first, there are four things in sin that clearly shine out in the
cross of Christ: —
(1.) The desert of it.
(2.) Man's impotency by reason of it.
(3.) The death of it.
(4.) A new end put to it.

(1.) The desert of sin does clearly shine in the cross of Christ...
```

Correct rendering:

```text
For the first, there are four things in sin that clearly shine out in the
cross of Christ: — (1.) The desert of it. (2.) Man's impotency by reason of it.
(3.) The death of it. (4.) A new end put to it.

(1.) The desert of sin does clearly shine in the cross of Christ...
```

## What qualifies as a flat syllabus

The strongest positive signal is an explicit anchor plus a short marker run.
The anchor should usually contain one or more of these features:

- A count: `two`, `three`, `four`, `six`, etc.
- A category noun: `things`, `heads`, `parts`, `ways`, `accounts`, `regards`,
  `sorts`, `considerations`, `observations`.
- A summary verb or formula: `observe`, `required`, `consists in`, `reduced
  unto`, `may be referred to`, `I understand`, `there are`.
- A terminal introduction: `: —` or `—`.

The candidate list items should look like labels or syllabus heads:

- Short noun phrases or brief clauses.
- Parallel grammar across items.
- Items ending with periods, semicolons, commas, or colons.
- Count matching the anchor when the anchor gives an explicit count.
- No item reads like a full exposition paragraph.

Known correct flat cases:

```text
may be referred to two heads: — 1. Temptations. 2. Afflictions.

I shall briefly observe four things therein: — (1.) Sweetness. (2.) Delight.
(3.) Safety. (4.) Comfort.

For the first, there are four things in sin that clearly shine out in the cross
of Christ: — (1.) The desert of it. (2.) Man's impotency by reason of it.
(3.) The death of it. (4.) A new end put to it.

The desert of sin does clearly shine in the cross of Christ upon a twofold
account: — [1.] Of the person suffering for it. [2.] Of the penalty he
underwent.

Now, that one may walk with another, six things are required: — 1. Agreement.
2. Acquaintance. 3. A way. 4. Strength. 5. Boldness. 6. An aiming at the same
end.
```

## What must remain block

Block lists are the actual scholastic exposition. They normally have one or
more of these features:

- They restart the marker sequence after a flat syllabus.
- They contain developed sentences, proofs, scripture chains, or argumentation.
- A marker paragraph begins to explain a previously announced head.
- The paragraph is long enough to carry prose rather than a label.
- The preceding phrase is explanatory rather than syllabic, especially
  `whereby ... : —`.

Known block-preserving case:

```text
(1.) For their sanctification;
(2.) For their consolation: to which two all the particular acts ... may be
referred. So there be two ways whereby we may grieve him: —
[1.] In respect of sanctification;
[2.] In respect of consolation: —
```

Here `[1.]` and `[2.]` are not a new anchor-sentence syllabus. They are an
explanatory nested list introduced by `whereby`, and they must stay blocky.

## Implementation standard

The renderer currently implements this in `render.py` with
`_attach_em_dash_flat_list()`. Future refinements should move toward an
explicit classifier:

```text
flat_summary = anchor_is_syllabus_intro
               and items_are_label_like
               and not expansion_context
```

Do not rely only on item word counts. Word caps are useful as guard rails, but
the real decision is rhetorical:

- Is this the announced syllabus?
- Or is this the explanatory treatment of one head?

When a run contains both, flatten only the valid prefix and leave the remaining
items as block paragraphs.

## Required regression guards

Any new fix in this area should add or preserve pytest coverage for:

- A multi-item flat syllabus followed by a marker restart.
- A two-item `twofold account` or `two heads` syllabus.
- An OCR-split flat tail such as `2.` followed by `Afflictions.`
- A long explanatory item that remains block.
- A `whereby ... : —` nested list that remains block.
- Roman outline heads that must not be flattened as ordinary labels.
- Scripture verse continuations and author initials that must not be promoted
  to list markers.

Use one volume at a time for validation. For Volume 2:

```bash
.venv/bin/python3 volumes/v2/convert.py --render-only
.venv/bin/python3 scripts/audit_bug_regressions.py 2
OWEN_REGRESSION_VOLUMES=2 .venv/bin/python3 -m pytest tests/test_bug_regressions.py
```
