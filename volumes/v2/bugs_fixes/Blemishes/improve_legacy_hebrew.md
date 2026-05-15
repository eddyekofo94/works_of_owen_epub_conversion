To improve the Hebrew extraction and rendering in your conversion pipeline, you should focus on the Gideon font mapping and the HTML/CSS structure of the final EPUB.
Based on the ENGINEERING_LOG.md and the existing shared.py logic, here is how you can refine the code:
1. Update the Gideon Map in shared.py
The "Ages Digital Library" PDFs use legacy encoding where Latin characters represent Hebrew glyphs. Your shared.py likely has a dictionary for convert_gideon_hebrew. You need to add the specific mappings for characters that are currently failing, such as the µ for Mem Final.
# In shared.py, expand your Hebrew map
GIDEON_MAP = {
    'a': 'א', 'b': 'ב', 'g': 'ג', 'd': 'ד',
    'h': 'ה', 'w': 'ו', 'z': 'ז', 'j': 'ח',
    'f': 'ט', 'y': 'י', 'k': 'כ', 'l': 'ל',
    'm': 'מ', 'n': 'נ', 's': 'ס', 'i': 'ע',
    'p': 'פ', 'x': 'צ', 'q': 'ק', 'r': 'ר',
    'v': 'ש', 't': 'ת',
    'µ': 'ם',  # Mem Final - Common failure point in Vol 2
    'Y': 'י',  # Often extracted for Yod with specific pointing
    # Add any other artifacts found in the ENGINEERING_LOG.md Issue 84
}

2. Implement RTL (Right-to-Left) Guardrails
Even if the characters are correct, e-readers will often scramble the order of Hebrew words unless they are wrapped in a container that forces the reading direction. Update your converter.py to ensure that any text identified as Hebrew is wrapped in a <span dir="rtl">.
# In converter.py, within the text processing loop:
def wrap_hebrew(text):
    # This ensures the e-reader handles the bidirectional text correctly
    return f'<span dir="rtl" lang="he" style="font-family: \'Ezra SIL\', serif;">{text}</span>'

3. Add a Unicode Normalization Step
Legacy fonts often include "pre-composed" characters that look correct but aren't searchable or accessible. In shared.py, you can use the unicodedata library to normalize the Hebrew after it has been mapped from Gideon.
import unicodedata

def clean_hebrew(text):
    # Map from Gideon characters to Hebrew Unicode
    converted = "".join([GIDEON_MAP.get(c, c) for c in text])
    # Normalize to ensure vowel points and accents are combined correctly
    return unicodedata.normalize('NFC', converted)

4. Enhance the CSS in shared.py
To ensure the Hebrew looks professional (like the Goold edition) and is legible on all devices, include a specific block in your EPUB_STYLESHEET.
/* In shared.py stylesheet string */
[lang="he"] {
    direction: rtl;
    unicode-bidi: embed;
    font-size: 1.2em; /* Hebrew often needs to be slightly larger to be legible */
    line-height: 1.4;
    -webkit-font-smoothing: antialiased;
}

5. Automated Validation Gate
As noted in your ENGINEERING_LOG.md under Issue 84, you should extend your audit script (audit_epub.py) to flag any "non-native" characters inside a Hebrew span. If the auditor sees a µ or a Y inside a tag marked lang="he", the conversion should fail the validation gate so you can update the map in shared.py.
By implementing these steps, you ensure that the text is not only visually correct but also structurally sound for digital readers, maintaining the integrity of the 16-volume collection.
