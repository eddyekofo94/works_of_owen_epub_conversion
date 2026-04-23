# John Owen Works — PDF to EPUB Converter

Converts AGES Digital Library PDFs of John Owen's 16-volume Works into EPUBs.

## Scripts

- `python3 convert_owen_to_epub.py` — older converter, PDF → EPUB directly via pypdf
- `python3 convert_owen_v2.py` — current converter, PDF → ThML XML → EPUB via pdfminer.six and ebooklib

Run either script from the working directory containing PDFs and a `covers/` subfolder.

## Dependencies

```bash
pip install pdfminer.six ebooklib
```

## Expected layout

```
work_dir/
├── owen-v1.pdf … owen-v16.pdf   (AGES PDFs)
├── covers/
│   ├── v1.jpg (or .png)
│   └── …
└── (outputs: volume_N.epub, volume_N.thml.xml)
```

## Key details

- PDFs use the AGES Koine-Medium font (Beta Code → Unicode Greek) and Gideon-Medium font (Hebrew RTL reversal)
- Both scripts handle Greek conversion via Beta Code mapping tables
- `convert_owen_v2.py` also handles Hebrew via Gideon encoding tables
- Footnotes are in a trailing FT section, extracted and linked as endnotes
- `convert_owen_to_epub.py` skips existing EPUBs; delete them to reconvert
- `convert_owen_v2.py` skips volumes where both `.thml.xml` and `.epub` already exist