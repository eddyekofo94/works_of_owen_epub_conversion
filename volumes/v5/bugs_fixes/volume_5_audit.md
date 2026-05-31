# EPUB Audit: volume_5.epub

- Status: **FAIL**
- Errors: 1
- Warnings: 1

## Summary

- OPF: EPUB/content.opf
- OPF version: 3.0
- Files: 66
- Manifest items: 57
- Spine items: 38
- XHTML files: 39
- Embedded fonts: 14
- NAV links: 41

## Content Checks

- Greek chars: 6350
- Untagged Greek chars: 0
- Hebrew chars: 980
- Untagged Hebrew chars: 0
- Noteref links: 1
- Endnote anchors: 0
- Boilerplate hits: 0
- Possible Beta Code files: 0
- Escaped language-tag files: 0
- Empty bracket noise files: 0
- Missing chapter initialization files: 0
- Repeated phrase hits: 3

## Errors

- `noteref_targets_missing`: Some noteref targets do not have matching endnote anchors

## Warnings

- `repeated_phrases`: Potential repeated phrases detected

## Samples

### repeated_phrase

- `combined_text`: chapter 3 the use of faith in justification
- `combined_text`: chapter 17 testimonies out of the evangelists considered
- `combined_text`: chapter 19 objections against the doctrine of justification

### chapter_heading_in_paragraph

- `EPUB/contents_2.xhtml`: CHAPTER 1

### lowercase_paragraph_start

- `EPUB/ch004.xhtml`: and the other is that of our Savior, Luke 17:10,
- `EPUB/ch010.xhtml`: who yet disclaims any confidence therein as unto his justification before God; fo
- `EPUB/ch011.xhtml`: attempts the sense of the word, but confounds it with "reputare:"
- `EPUB/ch012.xhtml`: and also Serm. 16 "Caput nostrum Dominus Jesus Christus omnia in se corporis sui
- `EPUB/ch022.xhtml`: injustus", 1 Peter 3:18. "Quod si ergo justi effecti sumus per vitam illius, caus
