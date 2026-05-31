from PIL import Image

def debug_pixels(img_path):
    img = Image.open(img_path)
    print("Image mode:", img.mode)
    print("Image size:", img.size)
    
    # Print the RGB values of a few pixels to see their format and actual values
    for y in range(0, img.height, img.height // 5):
        for x in range(0, img.width, img.width // 5):
            pixel = img.getpixel((x, y))
            print(f"Pixel at ({x}, {y}): {pixel}")

if __name__ == "__main__":
    debug_pixels("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/region_series_title.png")
