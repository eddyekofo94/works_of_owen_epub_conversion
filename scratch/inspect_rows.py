from PIL import Image

def inspect_rows(img_path):
    img = Image.open(img_path)
    w, h = img.size
    print(f"Image: {img_path} - Size: {w}x{h}")
    
    for y in range(h):
        row_pixels = sum(1 for x in range(w) if img.getpixel((x, y)) == 255)
        pct = (row_pixels / w) * 100
        print(f"Row {y:02d}: {row_pixels:3d} pixels ({pct:5.1f}%)")

if __name__ == "__main__":
    inspect_rows("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_series_title_cropped.png")
