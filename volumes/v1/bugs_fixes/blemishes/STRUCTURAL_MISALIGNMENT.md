# Blemish: Structural Misalignment (Summary Head Fragmentation)

## Issue
The initial PDF-to-ThML extraction failed to maintain the logical hierarchy of the text. Specifically, whenever the author provided a summary list of points or "heads" using bold Roman numerals (I., II., III., IV.), the extractor incorrectly promoted each item in that list to a new, standalone `div1` chapter. This fragmented the content and created redundant navigational entries.

## Evidence
- **Chapter 9 (*Christologia*):** A summary of Section IV was inserted as a new chapter (`ch019`) before Section I.
- **The Preface:** The four "reasons" for the work were split into four separate chapters (`ch048`-`ch051`).
- **Chapter 19 & 20:** Introductory summary lists were detached from their parent chapters and turned into siblings.

## Solution Plan
1.  **Surgical Consolidation:** Merge the fragmented list items back into their logical parent chapters.
2.  **Removal of Redundant Wrappers:** Delete the `div1` tags for the summary items and convert their titles into bold inline markers.
3.  **Flow Restoration:** Ensure the text transitions naturally from the introduction of a list (e.g., "reduced unto these four heads:") into the items themselves.

## Implementation
- Created a restoration script (`safe_fix_structure.py`) to surgically reorder the `volume_1.thml.xml` file.
- Consolidated the Preface and several Chapters in the *Christologia* and *Meditations* treatises.
- Regenerated the EPUB and verified the improved flow and navigational purity.
