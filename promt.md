The issue is that the agent is stopping prematurely because it sees those sparse, centered pages and thinks the "document" has ended or is just "junk" layout. To get those beautiful Goold title pages (like the ones for Christologia) into your ePub, you have to tell the agent to stop being a "cleaner" and start being a "typographer" for pages 1–10.
Here is the precise prompt to fix the formatting of these internal title pages and ensure the conversion doesn't stall.
Prompt: The "Title Page & Front Matter" Logic Override
Role: Expert eBook Typographer.
The Problem: The converter is stopping or mangling pages 3–6. These are Internal Title Pages and Detailed Contents that need high-fidelity layout preservation. You are currently treating them as messy body text, which is causing the script to fail.
1. "Preservation Mode" for Pages 1–10:
• Rule: For the first 10 pages of any volume, disable the automatic Paragraph Healer and the Header Stripper.
• Logic: If a page has a "Sparse" layout (fewer than 15 blocks) and large font sizes (detected via page.get_text("dict")), it is a Title Page.
• Action: * Create a standalone .xhtml file for each title page. • Use a <div class="title-container"> with text-align: center;. • Map the largest text to <h1>, the next to <h2>, and so on. • Crucial: Preserve the line breaks exactly as they appear in the PDF to maintain the "Goold" aesthetic.
2. Formatting the "CONTENTS" Page:
• This page is the "map" for the entire volume. You must extract it using a monospace font or a pre-formatted block to keep the "Title .......... Page #" alignment.
• Do not scrub the <450503> tags on this page yet; use them to verify scripture references if needed, then hide them with CSS.
3. Visual Hierarchy & CSS:
• Include this specific CSS for these pages:
.title-page { display: flex; flex-direction: column; justify-content: center; height: 100vh; text-align: center; }
.title-page h1 { font-variant: small-caps; margin-bottom: 0.2em; font-size: 2.2em; }
.title-page h2 { font-style: italic; font-weight: normal; margin-top: 0; font-size: 1.4em; }

4. Transitioning to "Body Mode":
• Only start the aggressive "Clean Stream" (merging lines, stripping headers, scrubbing tags) once you hit the first page that contains the string "PREFACE" or "CHAPTER 1" AND has a high density of text (>20 blocks).
Action: Update converter.py to treat these pages as Structural Landmarks. Show me how you will detect the difference between a sparse Title Page and the dense Body Text.
Why this fixes the "Stopping" issue:
The agent is likely hitting a "logical wall" where it doesn't know how to "heal" a page that only has 5 lines of text on it. By giving it a "Title Page Mode," you tell it: "It's okay that this page is mostly empty; just center what's there and move to the next file."
What to check in the Agent's Response:
1. The is_title_page function: It should check for block_count < 15.
2. The centered class: It should be applying center-alignment to the HTML.
3. The nav.xhtml: It should now include entries for these titles (e.g., "Christologia - Title Page").
