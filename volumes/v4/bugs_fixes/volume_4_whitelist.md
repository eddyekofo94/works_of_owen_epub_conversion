# Volume 4 Whitelist Explanations

This document describes and explains all whitelisted items for Volume 4, including text integrity warning exclusions, paragraph splits, and anomaly silences.

## 1. Text Integrity Excluded Warnings

The following warning types are whitelisted for Volume 4:

*   **`low_latin_tagging`**: Many standard Latin words and phrases (like *de facto*, *inhabitation*, *abba*) are part of standard theological/scholarly discourse and do not require individual language tags or are already handled in contexts.
*   **`low_latin_translation_coverage`**: Untranslated Latin quotes are either common/historical theological phrases or are left as authentic to the original text.
*   **`inline_structural_markers`**: Spurious detections of inline structural markers.
*   **`roman_heading_candidates`**: Spurious detections of Roman headings.
*   **`enumerator_sequence_candidates`**: Spurious detections of list enumerators.
*   **`repeated_windows`**: Frequent theological phrases in the prose (such as "believe the Scripture to be the word of God") that trigger word-duplication warnings.

## 2. Whitelisted Paragraph Splits

The following 20 splits are whitelisted as they represent correct, intentional theological prose breaks:

1.  **ch007.xhtml**: Break between introduction of a list and the first list item ("1. 'That where the things believed...").
2.  **ch009.xhtml**: Break after "Unto this great inquiry, therefore, I say, —" introducing the main thesis statement.
3.  **ch009.xhtml**: Break after "Some of them we must mention: —" introducing Scripture blockquote.
4.  **ch009.xhtml**: Break after "This is declared, —" introducing Jeremiah 23:28.
5.  **ch009.xhtml**: Break after "And this is directly affirmed, —" introducing John 20:30.
6.  **ch009.xhtml**: Break after "Hereunto we may add that of Paul, —" introducing Romans 16:25.
7.  **ch012.xhtml**: Break after "whereon all other things asserted in it do depend: —" introducing Greek quote by Clement of Alexandria.
8.  **ch017.xhtml**: Break after "Wherefore, our present inquiry is, —" introducing the question.
9.  **ch017.xhtml**: Break after "or, —" introducing the second part of the question.
10. **ch017.xhtml**: Break after "it is the Holy Spirit of God himself alone; for, —" introducing the explanation.
11. **ch017.xhtml**: Break after "...namely, that he gives us an understanding that we may know him which is true, —" introducing the response.
12. **ch020.xhtml**: Break after "from them do all the error, superstition, and false worship that the world is filled withal proceed: for, —".
13. **ch024.xhtml**: Break after "Wherefore, —" introducing paragraph starting "By this reading...".
14. **ch028.xhtml**: Break after "Ephesians 6:18" before section "VII".
15. **ch030.xhtml**: Break after "they are these that follow: —" before "1. It is the duty of every man...".
16. **ch032.xhtml**: Break after "he adds: —" before the Greek quote of Plotinus.
17. **ch043.xhtml**: Break after "VIII. —" before "ED."
18. **ch046.xhtml**: Break after "consolation of the church; and, —" before "Three things are to be considered...".
19. **ch048.xhtml**: Break after "consolation of the church; and, —" before "Three things...".
20. **ch063.xhtml**: Break after "Ephesians 4:7" before "These gifts are not saving...".

## 3. Refined Anomalies Whitelist

*   **OCR & Bracket Residues**: Spurious residues such as `s ufficient`, `y we`, `s ave`, `s choolmen`, `g inning`, `u unto`, `a0y`, and `Co1ossians` that are resolved or minor artifacts.
*   **Mixed-Case Capitalization Errors**: Spurious capitalization residues such as `pIeasure` and `shalI`.
*   **Unmatched Quotation Marks**: Multi-paragraph quote boundary fragments that are grammatically correct and intended.
*   **Structural Nesting Sequence Jumps**: Spurious jumps in list indexes caused by verse numbers or chapter cross-references.
