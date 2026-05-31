from PIL import Image

def isolate_main_title(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    
    # We crop the main title area (y=200 to y=520)
    title_area = img.crop((0, 200, w, 520))
    ta_w, ta_h = title_area.size
    
    # Binarize: text in this region is either white or light cyan.
    # In RGB, white or light cyan has high values for G and B (e.g. G > 180, B > 180).
    # Background teal is dark (G < 100, B < 100).
    bin_img = Image.new("L", (ta_w, ta_h), 0)
    
    for y in range(ta_h):
        for x in range(ta_w):
            r, g, b = title_area.getpixel((x, y))
            # Text check (high intensity in Green and Blue)
            if g > 160 and b > 160:
                bin_img.putpixel((x, y), 255)
                
    # Save the binarized image
    bin_img.save(out_path)
    print(f"Saved binarized main title area to {out_path}")
    
    # Find bounding box to crop away margins
    bbox = bin_img.getbbox()
    if bbox:
        cropped = bin_img.crop(bbox)
        cropped_path = out_path.replace(".png", "_cropped.png")
        cropped.save(cropped_path)
        print(f"  Saved cropped binarized title to {cropped_path} (Size: {cropped.size})")

if __name__ == "__main__":
    isolate_main_title("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_main_title.png")
