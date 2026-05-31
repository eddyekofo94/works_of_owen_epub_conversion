from PIL import Image

def slice_bands(img_path):
    img = Image.open(img_path)
    w, h = img.size
    print(f"Slicing {img_path} ({w}x{h}) into 100px vertical bands:")
    
    for i in range(8):
        y_start = i * 100
        y_end = (i + 1) * 100
        band = img.crop((0, y_start, w, y_end))
        band_path = f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/band_{i}.png"
        band.save(band_path)
        print(f"  Band {i} (y={y_start} to {y_end}): Saved to {band_path}")

if __name__ == "__main__":
    slice_bands("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png")
