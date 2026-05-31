from PIL import Image

def scan_column(img_path, x_coord):
    img = Image.open(img_path)
    print(f"Scanning column x={x_coord} in {img_path}:")
    for y in range(img.height):
        r, g, b = img.getpixel((x_coord, y))
        is_dark = r < 50 and g < 120 and b < 120
        status = "DARK (text/line)" if is_dark else "LIGHT (bg)"
        print(f"  y={y:02d}: ({r:3d}, {g:3d}, {b:3d}) - {status}")

if __name__ == "__main__":
    scan_column("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/region_series_title.png", 200)
