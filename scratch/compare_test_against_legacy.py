import os
from PIL import Image, ImageChops

def compare_title_word(legacy_path, test_path, out_diff_path):
    legacy = Image.open(legacy_path)
    test = Image.open(test_path)
    
    # 1. Resize test image to 512x800 (legacy size)
    test_resized = test.resize(legacy.size, Image.Resampling.LANCZOS)
    
    # 2. Crop the word "SPIRIT" area from y=390 to y=480, x=50 to x=462 in both
    legacy_crop = legacy.crop((50, 390, 462, 480))
    test_crop = test_resized.crop((50, 390, 462, 480))
    
    # 3. Binarize both using green/blue thresholding
    # In both, background is dark teal, and text is white/cyan
    def get_bin(img):
        w, h = img.size
        bin_img = Image.new("L", (w, h), 0)
        for y in range(h):
            for x in range(w):
                r, g, b = img.getpixel((x, y))
                if g > 150 and b > 150:
                    bin_img.putpixel((x, y), 255)
        return bin_img
        
    leg_bin = get_bin(legacy_crop)
    test_bin = get_bin(test_crop)
    
    # Crop to active bounding boxes to align
    leg_bbox = leg_bin.getbbox()
    test_bbox = test_bin.getbbox()
    
    if not leg_bbox or not test_bbox:
        print("Error: Could not isolate word in one of the images.")
        return 100.0
        
    leg_final = leg_bin.crop(leg_bbox)
    test_final = test_bin.crop(test_bbox)
    
    # Resize test word to match legacy word dimensions for direct pixel-by-pixel comparison
    test_final_resized = test_final.resize(leg_final.size, Image.Resampling.LANCZOS)
    test_final_resized = test_final_resized.point(lambda p: 255 if p > 120 else 0)
    
    # Calculate absolute difference
    diff = ImageChops.difference(leg_final, test_final_resized)
    w, h = diff.size
    diff_data = list(diff.getdata())
    mismatched = sum(1 for val in diff_data if val == 255)
    total_pixels = w * h
    pct_diff = (mismatched / total_pixels) * 100
    
    # Save comparison strip
    compare_strip = Image.new("RGB", (w * 3 + 20, h), (100, 100, 100))
    compare_strip.paste(leg_final.convert("RGB"), (0, 0))
    compare_strip.paste(test_final_resized.convert("RGB"), (w + 10, 0))
    compare_strip.paste(diff.convert("RGB"), (w * 2 + 20, 0))
    compare_strip.save(out_diff_path)
    
    print(f"Comparison of 'SPIRIT': Mismatch = {pct_diff:.3f}%")
    return pct_diff

if __name__ == "__main__":
    legacy_path = "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v4.png"
    
    print("--- Comparing Legacy with Montserrat Black ---")
    compare_title_word(
        legacy_path,
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/v4_test_black.png",
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/diff_v4_montserrat_black.png"
    )
    
    print("\n--- Comparing Legacy with Montserrat ExtraBold ---")
    compare_title_word(
        legacy_path,
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/v4_test_extrabold.png",
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/diff_v4_montserrat_extrabold.png"
    )
