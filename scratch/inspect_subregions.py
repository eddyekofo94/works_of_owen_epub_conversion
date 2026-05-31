from PIL import Image
from collections import Counter

def inspect_region(img_path, box, name):
    img = Image.open(img_path)
    cropped = img.crop(box)
    cropped.save(f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/region_{name}.png")
    
    # Analyze colors in this region
    pixels = list(cropped.getdata())
    counter = Counter(pixels)
    
    print(f"\n--- Subregion: {name} (Box: {box}) ---")
    print("Top 5 colors:")
    for color, count in counter.most_common(5):
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        print(f"  {color} ({hex_color}): {count} pixels")

if __name__ == "__main__":
    # In a 512x800 image, let's check:
    # 1. Series Title (around y=40 to y=80)
    inspect_region("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png", (50, 30, 462, 90), "series_title")
    
    # 2. Author Name (around y=660 to y=720)
    inspect_region("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png", (50, 660, 462, 730), "author")
