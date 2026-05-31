from PIL import Image
from collections import Counter

def inspect_colors(img_path):
    img = Image.open(img_path)
    w, h = img.size
    
    # Sample pixels across the image to find dominant colors
    pixels = list(img.getdata())
    color_counter = Counter(pixels)
    
    print("Top 10 dominant colors (R, G, B):")
    for color, count in color_counter.most_common(10):
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
        pct = (count / len(pixels)) * 100
        print(f"  {color} ({hex_color}): {count} pixels ({pct:.2f}%)")

if __name__ == "__main__":
    inspect_colors("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v4.png")
