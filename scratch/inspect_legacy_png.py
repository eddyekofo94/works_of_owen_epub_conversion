import os
from PIL import Image
from PIL.PngImagePlugin import PngImageFile

def inspect_png(file_path):
    print(f"=== Inspecting PNG metadata for: {file_path} ===")
    img = Image.open(file_path)
    
    # 1. Standard Info dictionary
    print("\n--- Image Info ---")
    for k, v in img.info.items():
        # Avoid printing huge raw bytes if any, truncate if long
        val_str = str(v)
        if len(val_str) > 500:
            val_str = val_str[:500] + "... (truncated)"
        print(f"{k}: {val_str}")
        
    # 2. Check if there is XMP metadata or specific chunks
    if isinstance(img, PngImageFile):
        print("\n--- PNG Chunks ---")
        # Access private/undocumented chunks structure if helpful
        try:
            for k in img.custom_mimetype:
                print(f"Custom mimetype key: {k}")
        except Exception as e:
            pass
            
    print("\n=== End of Inspection ===")

if __name__ == "__main__":
    inspect_png("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v4.png")
    inspect_png("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png")
