from PIL import Image

def get_bin(img):
    w, h = img.size
    bin_img = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if g > 150 and b > 150:
                bin_img.putpixel((x, y), 255)
    return bin_img

def print_shapes(legacy_path, test_path):
    legacy = Image.open(legacy_path)
    test = Image.open(test_path).resize(legacy.size, Image.Resampling.LANCZOS)
    
    # Crop the y=380 to y=490 region
    legacy_crop = legacy.crop((50, 380, 462, 490))
    test_crop = test.crop((50, 380, 462, 490))
    
    leg_bin = get_bin(legacy_crop)
    test_bin = get_bin(test_crop)
    
    leg_bbox = leg_bin.getbbox()
    test_bbox = test_bin.getbbox()
    
    if leg_bbox:
        leg_final = leg_bin.crop(leg_bbox)
        lw, lh = leg_final.size
        print(f"\n=== Legacy crop shape ({lw}x{lh}) ===")
        # Print shape at small scale
        step_y = max(1, lh // 15)
        step_x = max(1, lw // 40)
        for y in range(0, lh, step_y):
            line = ""
            for x in range(0, lw, step_x):
                line += "#" if leg_final.getpixel((x, y)) == 255 else "."
            print(line)
            
    if test_bbox:
        test_final = test_bin.crop(test_bbox)
        tw, th = test_final.size
        print(f"\n=== Test crop shape ({tw}x{th}) ===")
        step_y = max(1, th // 15)
        step_x = max(1, tw // 40)
        for y in range(0, th, step_y):
            line = ""
            for x in range(0, tw, step_x):
                line += "#" if test_final.getpixel((x, y)) == 255 else "."
            print(line)

if __name__ == "__main__":
    print_shapes(
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v4.png",
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/v4_test_extrabold.png"
    )
