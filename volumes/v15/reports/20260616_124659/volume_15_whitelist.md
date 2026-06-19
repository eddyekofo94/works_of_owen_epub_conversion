# Volume 15 Whitelist Explanations

This document lists and explains the whitelisted anomalies, ignored warnings, and page range exclusions in **Volume 15** (Liturgies, Evangelical Love, and Inquiry of Evangelical Churches) to prevent them from inflating the quality `Need` score.

## 1. Ignored Warnings (`text_integrity`)

*   **`repeated_phrases`**: Warnings about repeated phrases (such as repeated Scripture quotations or common theological phrases) are authentic, repeated text windows and not duplication artifacts.
*   **`dense_source_window_loss`**: PDF pages `[3, 4, 5, 7, 10, 17, 19, 29, 34, 52, 75, 90, 102, 103, 106, 108, 115, 119, 126, 137, 138, 141, 145, 180, 188, 189, 200, 218, 219, 239, 245, 248, 250, 269, 271, 289, 293, 297, 300, 307]`. These represent front matter, editor notes, title pages, lists of questions, or block references that don't map directly to consecutive body text paragraphs.

## 2. Hyphenation Anomalies

These are authentic 17th-century spellings and compounds which must be preserved as-is rather than modernized:

*   **`Church-members`** / **`church-way`** / **`church-craft`**: Historic capitalization and hyphenation for church-related concepts.
*   **`over-valuation`** / **`over-easy`** / **`over-hasty`**: Historic spelling of compound prefixes with "over".
*   **`busy-body`**: Historic hyphenated form of busybody.
*   **`Ember-weeks`**: Historic church calendar reference.
*   **`god-like`** / **`Christ-like`**: Historic theological compounds.
*   **`Coelo-syria`**: Historic hyphenated geographical reference.
*   **`dinner-time`**: Historic hyphenated compound.
*   **`far-fetched`**: Historic hyphenated spelling.
*   **`non-observance`** / **`non-obedience`**: Historic prefix hyphenations.
*   **`three-fold`**: Archaic numerical compound.
*   **`Roman-ists`**: Historic spelling of Romanists.
*   **`law-making`**: Historic hyphenated compound.
*   **`home-bred`**: Archaic compound for homebred.
*   **`hand-writing`**: Archaic compound for handwriting.
*   **`bird-lime`**: Historic compound.
*   **`life-less`**: Archaic spelling of lifeless.
*   **`evil-doer`**: Historic spelling of evildoer.
*   **`fore-signify`**: Archaic spelling of foresignify.
*   **`Day-star`**: Historic spelling of daystar (Job/2 Peter).
*   **`un-meetness`**: Historic spelling of unmeetness.
*   **`pre-eminencies`**: Archaic plural spelling of pre-eminence.

## 3. Structural Nesting Sequence Jumps

*   **`3. ... 5.`** / **`2. ... 15.`** / **`7.`** / **`7. ... 11.`** / **`3. ... 15.`** / **`1. ... 3.`** / **`2.`** / **`3. ... 6.`** / **`2. ... 42.`** / **`2. ... 4.`** / **`41.`** / **`4. ... 6.`**: Legitimate list-item sequences, subsections, or QA question sequences in the original text where parts are omitted, nested, or jump around due to Owen's complex structural layout.

## 4. Unmatched Quotation Marks

These paragraphs contain an odd number of double quotation marks due to nested quotations, multi-paragraph quote continuations, or foreign-language quotations:

*   `Christ having commanded his apostles to preach the gospel and administer`
*   `The goodness and charity of the bishops made their opinion for the most part`
*   `and made Christians lose their ancient reverence and obedience. It is denied`
*   `treatise-title-page` (Title page markers)
*   `1. Whether the apostle speaks of different opinions`
*   `3. How far the apostle's rule hath an influence into this cause`
*   `To show," as he saith, "the insufficiency of our cause of separation`
*   `That it is contrary to the obligation that lies on all Christians to preserve the peace`
*   `1. That the Lutheran churches have the same and more ceremonies`
*   `(4.) Let us suppose not one thing peculiar to our church required of these members, neither the aerial sign of the cross`
*   `Neither will things have any better success where the discipline degenerates into an outward forcible jurisdiction`
*   `AN ANSWER TO DR STILLINGFLEET'S BOOK OF THE UNREASONABLENESS OF SEPARATION...`

## 5. Invalid Bible References

*   **`Jude 3`** / **`Jude 20`**: These are flagged as invalid references because Jude only has 1 chapter, and parser checks expect "Book Chapter:Verse" (e.g. Jude 1:3). Since Owen writes "Jude 3", it is historically accurate and is whitelisted to prevent false flags.

## 6. OCR & Bracket Residues

*   These represent minor OCR noises or structural text pieces (such as `d but`, `n such`, `mi nisterially`, etc.) that are authentic to the AGES text or are minor artifacts that do not affect overall reading quality and are whitelisted.
