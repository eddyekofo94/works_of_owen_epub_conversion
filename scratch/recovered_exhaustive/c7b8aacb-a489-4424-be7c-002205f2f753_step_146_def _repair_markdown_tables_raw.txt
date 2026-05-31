Created At: 2026-05-29T09:20:29Z
Completed At: 2026-05-29T09:20:29Z
File Path: `file:///Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/render.py`
Total Lines: 5012
Total Bytes: 224934
Showing lines 820 to 860
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
820:     re.I | re.S,
821: )
822: 
823: 
824: def _repair_scholastic_blockquote_boundaries(text):
825:     """Move blockquote markers back over quoted Objection/Obj. openings."""
826:     if not text:
827:         return text
828: 
829:     def repl(match):
830:         quote = match.group("quote").strip()
831:         rest = re.sub(r'\s+', ' ', match.group("rest").strip())
832:         return f'{match.group("intro")}\n\n[[BLOCKQUOTE]] {quote} {rest}'
833: 
834:     return _SCHOLASTIC_QUOTED_OBJECTION_RE.sub(repl, text)
835: 
836: 
837: def _repair_sermon_prefatory_note_splits(text):
838:     """Join sermon prefatory note openings split around scripture text."""
839:     if not text:
840:         return text
841:     return re.sub(
842:         r'\b(THIS\s+sermon,\s+from)\s*\n\n\[\[SUMMARY\]\]\s*([^\n]+?)\s*\n\n([a-z])',
843:         lambda m: f'{m.group(1)} {m.group(2).strip()} {m.group(3)}',
844:         text,
845:         flags=re.I,
846:     )
847: 
848: 
849: _TOKEN_STRIP_RE = re.compile(r'\[\[[A-Z_]+\]\]\s*')
850: 
851: 
852: def _repair_markdown_tables(text: str) -> str:
853:     """Convert Markdown pipe-table paragraphs into [[BLOCKQUOTE]] / plain paragraph pairs.
854: 
855:     Owen's S.S. / Lib. Arbit. comparison tables use two columns:
856:       Left  = Scripture references (S.S.)          → plain paragraphs
857:       Right = Arminian / Remonstrant quotes         → [[BLOCKQUOTE]] markers
858: 
859:     Tables extracted from the PDF arrive as a single paragraph where cells contain
860:     ``<br>`` for in-cell line-breaks and rows are separated by ``| |``::
The above content does NOT show the entire file contents. If you need to view any lines of the file which were not shown to complete your task, call this tool again to view those lines.
