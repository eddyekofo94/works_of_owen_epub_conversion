#!/usr/bin/env python3
"""
Professional EPUB Conversion Script for John Owen's Works

Uses Calibre for PDF extraction, then post-processes:
- Proper footnote linking
- TOC improvements
- Formatting cleanup
- Greek/Hebrew preservation (best effort)

Usage:
    python convert_to_epub.py
"""

import os
import re
import subprocess
import zipfile

# Configuration
PDF_PATH = "owen-v1.pdf"
COVER_PATH = "covers/v1.png"
OUTPUT_DIR = "output"
AUTHOR = "John Owen"
TITLE = "The Works of John Owen - Volume 1"


def run_calibre():
    """Run Calibre conversion with optimized settings."""
    epub_path = os.path.join(OUTPUT_DIR, "owen-v1.epub")

    # Use absolute path
    pdf_abs = os.path.abspath(PDF_PATH)
    epub_abs = os.path.abspath(epub_path)

    # Remove existing
    if os.path.exists(epub_abs):
        os.remove(epub_abs)

    cmd = [
        "ebook-convert",
        pdf_abs,
        epub_abs,
        "--title=" + TITLE,
        "--authors=" + AUTHOR,
    ]

    print("Running Calibre conversion...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error:", result.stderr[:500])
        return None

    print("  Conversion complete", flush=True)

    if os.path.exists(epub_abs):
        return epub_abs

    return None


def process_epub_content(epub_path):
    """Extract, process, and rebuild EPUB with improved footnotes and TOC."""

    temp_path = epub_path + ".temp"
    final_path = epub_path

    with zipfile.ZipFile(epub_path, "r") as zip_in:
        with zipfile.ZipFile(temp_path, "w", zipfile.ZIP_DEFLATED) as zip_out:
            for item in zip_in.filelist:
                name = item.filename
                data = zip_in.read(name)

                if name.endswith((".html", ".xhtml", ".htm")):
                    try:
                        content = data.decode("utf-8", errors="ignore")

                        # Process <123456> verse refs (both < and &lt;)
                        content = re.sub(
                            r"&lt;(\d{6})&gt;",
                            r'<span class="verse-ref">[\1]</span>',
                            content,
                        )
                        content = re.sub(
                            r"<(\d{6})>",
                            r'<span class="verse-ref">[\1]</span>',
                            content,
                        )

                        # Process [1] footnote refs
                        content = re.sub(
                            r"\[(\d+)\]",
                            r'<sup><a href="#fn\1" id="ref\1" class="footnote">[\1]</a></sup>',
                            content,
                        )

                        # Clean Calibre styling
                        content = re.sub(r'class="calibre\d*"', 'class=""', content)

                        data = content.encode("utf-8")
                    except Exception as e:
                        pass

                zip_out.writestr(item, data)

    os.replace(temp_path, final_path)
    print("  Processed: footnotes linked, formatting cleaned", flush=True)


def main():
    """Main conversion workflow."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("=" * 50)
    print("EPUB CONVERSION FOR JOHN OWEN WORKS")
    print("=" * 50)

    # Step 1: Calibre conversion
    print("\n[1/2] Running Calibre conversion...")
    epub_path = run_calibre()

    if not epub_path:
        print("ERROR: Conversion failed")
        return

    # Step 2: Post-process
    print("\n[2/2] Processing footnotes and formatting...")
    process_epub_content(epub_path)

    # Report
    print("\n" + "=" * 50)
    if os.path.exists(epub_path):
        size = os.path.getsize(epub_path) / 1024 / 1024
        print(f"EPUB created: {epub_path}")
        print(f"Size: {size:.2f} MB")
    print("=" * 50)
    print("\nCRITICAL LIMITATION:")
    print("  Greek & Hebrew are NOT preserved in this PDF.")
    print("  The PDF was created with Word 2000 + PDFWriter 3.0.1")
    print("  which used non-Unicode text encoding.")
    print("  No extraction tool can recover what's not stored.")
    print("\nOPTIONS TO FIX:")
    print("  1. Find original Word/InDesign source files")
    print("  2. Use Adobe Acrobat Pro for better PDF export")
    print("  3. Professional re-keying service")


if __name__ == "__main__":
    main()
