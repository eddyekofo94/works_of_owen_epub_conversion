from PIL import Image

def binarize_light_block(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    bin_img = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Light text is cyan/white in the teal block
            if g > 160 and b > 160 and r > 100:
                bin_img.putpixel((x, y), 255)
    
    # Save the binarized mask
    bin_img.save(out_path)
    print(f"Saved light mask: {out_path}")
    
    # Save cropped version
    bbox = bin_img.getbbox()
    if bbox:
        cropped = bin_img.crop(bbox)
        cropped_path = out_path.replace(".png", "_cropped.png")
        cropped.save(cropped_path)
        print(f"  Cropped light mask: {cropped_path} (Size: {cropped.size})")

def binarize_dark_block(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    bin_img = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            # Dark text is teal in the cream block (R < 80, G < 120, B < 120)
            if r < 80 and g < 120 and b < 120:
                bin_img.putpixel((x, y), 255)
                
    # Save the binarized mask
    bin_img.save(out_path)
    print(f"Saved dark mask: {out_path}")
    
    # Save cropped version
    bbox = bin_img.getbbox()
    if bbox:
        cropped = bin_img.crop(bbox)
        cropped_path = out_path.replace(".png", "_cropped.png")
        cropped.save(cropped_path)
        print(f"  Cropped dark mask: {cropped_path} (Size: {cropped.size})")

if __name__ == "__main__":
    binarize_light_block("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/detected_block_1_light.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_block_1_light.png")
    binarize_light_block("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/detected_block_2_light.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_block_2_light.png")
    binarize_dark_block("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/detected_block_10_dark.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_block_10_dark.png")
