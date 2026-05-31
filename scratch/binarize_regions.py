from PIL import Image

def binarize_series_title(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    
    # We want to binarize: if pixel is dark teal (R < 50, G < 120, B < 120), it is text (255), else background (0)
    bin_img = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r < 50 and g < 120 and b < 120:
                bin_img.putpixel((x, y), 255)
                
    bin_img.save(out_path)
    print(f"Saved binarized series title to {out_path}")

def binarize_author(img_path, out_path):
    img = Image.open(img_path)
    w, h = img.size
    
    # Let's binarize: if pixel is dark teal (R < 50, G < 120, B < 120), it is text (255), else background (0)
    bin_img = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r < 50 and g < 120 and b < 120:
                bin_img.putpixel((x, y), 255)
                
    bin_img.save(out_path)
    print(f"Saved binarized author to {out_path}")

if __name__ == "__main__":
    binarize_series_title("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/region_series_title.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_series_title.png")
    binarize_author("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/region_author.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_author.png")
