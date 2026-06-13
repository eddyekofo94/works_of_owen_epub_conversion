# Volume 9 Whitelist Report

This document records all whitelisted warnings, structural anomalies, and gaps in **Volume 9**.

## 1. Missing Front Table of Contents Pages
* **Pages:** PDF pages 3, 4, 5, 6
* **Reason:** These pages are the original noisy PDF Table of Contents. They are entirely suppressed and overridden by a custom, premium HTML Table of Contents (`_V9_CONTENTS_PAGE`) defined in `volumes/v9/convert.py`.
* **Configuration:** Whitelisted by setting `"max_front_toc_missing_pages": 4` in the `qa/bug_regression_baselines.json` config.

## 2. Footnote Mismatch Delta
* **Mismatch Delta:** 1
* **Reason:** The EPUB contains 94 noteref links but only 93 endnotes in `endnotes.xhtml` because one endnote is validly referenced multiple times from the chapter body.
* **Configuration:** Whitelisted under `ALLOWED_FOOTNOTE_ANOMALIES` with `'mismatch_delta': 1` in `tests/test_footnote_integrity.py`.

## 3. Structural Sequence Gaps
The following sequence gaps are present in the source printed text and are whitelisted in `tests/test_structural_symmetry.py`:

| File | Level Class | Marker | Predecessor | Reason |
|---|---|---|---|---|
| `EPUB/ch029.xhtml` | `list-level-1` | `III.` | `I.` | Sermon 24: Predecessor was `I.` and skipped `II.` in the original printed text. |
| `EPUB/ch030.xhtml` | `list-level-1` | `IV.` | `II.` | Sermon 25: Predecessor was `II.` and skipped `III.` in the original printed text. |
| `EPUB/ch090.xhtml` | `list-level-1` | `3.` | `1.` | Sacramental Discourse 20: Predecessor was `1.` and skipped `2.` in the original printed text. |
| `EPUB/ch091.xhtml` | `list-level-1` | `3.` | `1.` | Sacramental Discourse 21: Predecessor was `1.` and skipped `2.` in the original printed text. |
