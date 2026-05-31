<!--  -->  TODO: (2026-05-26 13:33) 
## 1
Observation [n]

Fix:
This should be bold, all the "Observations [n]", add this to the scholastic-anchor

## 2
On each sermon I am seeing "Prefatory Note" twice? This is possibly inherited from other volume fix but the extraction or rendering though there's a global rule for the sake of generalising but it should also be per each volume

## 3
“Lord with fear, and rejoice with trembling," Psalm 10, 11.”

Fix:
11 here is "bold", verses should be excluded from bolding. It's a false possitive.

## 4
“ +Ω Βάθος, "O the depth," etc.”
“Τρέμει δ ὄρη, καὶ πελώριος Βυθὸς ζαλάσσης, κᾠρέων ὕψος μέγα, {Οταν ἐπεβλέψῃ γοργὸν ὄμμα δεσπότου.”


Fix:
Faulty greek rendering
Note: I tried fixing all the Greek on v1, create a thorough map of Gideon characters and I expected all the Greek after should be perfectly rendered. If I am still having problems then it was not thorough.
Can we search online and find all the Greek characters and Hebrew and fix it now so that when I run v9-19 I should not expect any greek errors there?

## 5
“warning all,  using all appointed means to draw them to Jesus Christ and the faith of the gospel; waiting with all patience on them”
“ all thy sins pardoned, — ”


Fix: Faulty extraction of rendering:  " using" 

## 6
“1. That God hath done it.
2. That he hath promised he wall yet do it.
3. Why he will so do.”

Fix:
“Now, concerning this, observe, — 1. That God hath done it. 2. That he hath promised he wall yet do it. 3. Why he will so do.”

This is how this should be a "flat" list, can we review the scholastic-anchor and rules that I am painstakingly trying to get right?

This is what you proposed earlier:
Revised Plan: Blemish #16 — Em-dash Flat List
The core rule (multi-signal, no single point of failure)
A list run following a —-ending paragraph is flattened only if it clears the hard veto AND satisfies at least one positive signal:
HARD VETO (blocks flattening regardless of signals):
  • ANY item has > 8 content words AND does not itself end with —
    → leave as block, do not touch

POSITIVE SIGNALS (any one is sufficient):
  A. Grammar continuation: any non-final item ends with ; or ,
  B. Grammar continuation: any item ends with ' and' or ' or' (word boundary)
  C. Label list: ALL items are ≤ 3 words
  D. Short parallel run: run has ≥ 3 items AND all items ≤ 7 words
Traced against every example
CaseMax wordsSignalResultSweetness. / Delight. / Safety. / Comfort.1C (all ≤ 3) + D (4 items, all ≤ 7)flat ✓Powerfully, or effectually; / Voluntarily; / Freely.3A (; on non-final) + C + Dflat ✓The desert of it. / …impotency… / The death of it. / A new end…6D (4 items, all ≤ 7)flat ✓Of the person… / Of the penalty…62 items, no ;/,, not all ≤ 3 → no signal firesleft as block (safe)Per benevolam condolentiam… (13 words on item 2)13hard veto firesleft as block (safe)Powerfully: and therefore does comfort…25hard vetoblock ✓1. Temptations. / 2. Afflictions.1C + Dflat ✓
The 2-item [1.] Of the person / [2.] Of the penalty case is intentionally left for now — it has 2 items, 5-6 words each, no continuation markers. That's genuinely ambiguous without deeper semantic analysis, and leaving it as a block is the safe choice.
Implementation
New function _attach_em_dash_flat_list(html) in render.py:
python_EM_DASH_FLAT_HARD_CAP = 8   # items beyond this are block, full stop

def _attach_em_dash_flat_list(html):
    """Absorb short list runs into a preceding paragraph that ends with —.

    A list introduced by an em-dash is flat (inline enumeration) when the
    items are clearly labels or short parallel phrases — not full scholastic
    expansions. Multi-signal detection avoids false positives.
    """
Logic inside the function — same split/accumulate loop pattern as _merge_short_inline_lists:

Split on list-item / roman-list-item paragraphs
For each run:

Extract (marker, content) pairs (bold marker + content text)
Hard veto: if any item's word count > 8 → skip (leave unchanged)
Find preceding <p>: look back in out[] for the last non-whitespace token; check if it ends with — (possibly —  or , —)
If no em-dash preceding paragraph → skip
Check signals: evaluate A/B/C/D against the item list
If at least one signal fires → absorb: strip </p> from preceding paragraph, append all items inline (marker + content, space-separated), close with </p>
Otherwise → pass run through unchanged



Call site in markdown_to_html() line 2082:
pythonresult_html = _attach_colon_introduced_list(result_html)
result_html = _attach_em_dash_flat_list(result_html)   # new
result_html = _merge_short_inline_lists(result_html)
Why this ordering matters
After _attach_em_dash_flat_list absorbs items into the preceding <p>, those items disappear from the list-item pool. _merge_short_inline_lists (Rules A/B) then operates on whatever list-item runs remain — there's no conflict or double-processing.
Tests to add (5 new)

Em-dash + single-word items → fully merged into preceding <p> ✓
Em-dash + semicolon items → merged (all 3 items absorbed into preceding <p>) ✓
Em-dash + 4-item short-phrase run (all ≤ 7 words) → merged ✓
Em-dash + 2-item run (6 words each, no semicolons) → NOT merged (safe) ✓
Em-dash + long items (>8 words) → NOT merged ✓

Does your own rules not catch this example? If it doesn't then it should.


## 7
Each sermon has a verse and it should be formatted differently than the body.
