Created At: 2026-05-29T22:18:21Z
Completed At: 2026-05-29T22:18:22Z

				The command completed successfully.
				Output:
				--- a/render.py
+++ b/render.py
-    r'Application\.?\s*\d+\.?)'
+    r'Application\.?\s*\d+\.?|'
+    r'Obs(?:ervation)?\.?\s*\d*\.?)'  # Issue: "Observation [n]" — bold like Obj./Ans.
-    r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application)\s+\.',
+    r'\b(Obj(?:ection)?|Ans(?:wer)?|Sol(?:ution)?|Use|Usus|Application|Obs(?:ervation)?)\s+\.',
+      3b. Standalone study phrase                — "From my Study," (split from initials line)
-      6. Place + year                            — "Edinburgh, 1682.", "London, 1682"
+      6. Place + bare year                       — "Edinburgh, 1682.", "London, 1682"
+      6b. Place + month + year                   — "Edinburgh, August 1850."
-    if re.match(r'^[A-Z]\.[A-Z]\.\s+From\s+my\s+study', plain, re.I):
+    # Allow optional space between initials: "J.O." or "J. O."
+    if re.match(r'^[A-Z]\.\s*[A-Z]\.\s+From\s+my\s+study', plain, re.I):
+        return True
+    # Pattern 3b — standalone "From my Study," (occurs when PDF splits the J.O. signature
+    # into separate paragraphs: "J.O." / "From my Study," / "September the last, [1645].")
+    # Short guard (< 60 chars) prevents false-positives in body prose.
+    if re.match(r'^From\s+my\s+[Ss]tudy\b', plain) and len(plain) < 60:
-    # Pattern 6 — place + year: "Edinburgh, 1682", "London, 1677."
+    # Pattern 6 — place + bare year: "Edinburgh, 1682", "London, 1677."
+    # Pattern 6b — place + month + year: "Edinburgh, August 1850." (W.H.G. second line)
+    if re.match(
+        r'^[A-Z][a-z]+,\s*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?'
+        r'|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\.?$',
+        plain,
+    ):
+        return True
+PLAIN_INLINE_ROMAN_SECTION_HTML_RE = re.compile(
+    r'(?P<marker>(?<![A-Za-z])(?!(?:LXX|MT|OT|NT|DV|KJV|AV|NIV|ESV|NRSV)\.)'
+    r'[IVXLCDM]{1,6}\.\
<truncated 826 bytes>
text
+    return re.sub(
+        r'\b(THIS\s+sermon,\s+from)\s*\n\n\[\[SUMMARY\]\]\s*([^\n]+?)\s*\n\n([a-z])',
+        lambda m: f'{m.group(1)} {m.group(2).strip()} {m.group(3)}',
+        text,
+        flags=re.I,
+    )
+
+
+def _repair_markdown_tables(text: str) -> str:
+    """Convert Markdown pipe-table paragraphs into [[BLOCKQUOTE]] / plain paragraph pairs.
+
+    Owen's S.S. / Lib. Arbit. comparison tables use two columns:
+      Left  = Scripture references (S.S.)          → plain paragraphs
+      Right = Arminian / Remonstrant quotes         → [[BLOCKQUOTE]] markers
+
+    Tables extracted from the PDF arrive as a single paragraph where cells contain
+    ``<br>`` for in-cell line-breaks and rows are separated by ``| |``::
+
+        |cell_a|cell_b| |---|---| |cell_c|cell_d|
+
+    Special case — unclosed preceding blockquote:
+      If the paragraph immediately before the table is a [[BLOCKQUOTE]] whose
+      content ends with a comma (quote cut off mid-sentence), the right cell of
+      the FIRST data row is appended to that blockquote to complete it, and the
+      left cell of the first row becomes a plain paragraph as normal.
+    """
+    if not text or ('|---|' not in text and '|--' not in text):
+        return text
+
+    paras = text.split('\n\n')
+    out: list[str] = []
+
+    for para in paras:
+        stripped = para.strip()
+
+        # Quick bail — paragraph has no table separator row
+        if not re.search(r'\|[\-]+\|', stripped):
+            out.append(para)
+            continue
+
+        # Normalise <br> tags → space so cell text reads as a single line
+        normalised = re.sub(r'<br\s*/?>', ' ', stripped)
+
+        # Split inline-concatenated rows.  Each row ends with '|' and the next
+        # starts with '|' with only whitespace between them.
+        row_texts = re.split(r'(?<=\|)\s+(?=\|)', normalised)
+
+        rows: list[tuple[str, str]] = []
+        parse_ok = True
+        for rt in row_texts:
+            rt = rt.strip()
+            if not rt:

