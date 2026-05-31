import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

def binarize_and_crop(img, threshold=120):
    gray = img.convert("L")
    bin_img = gray.point(lambda p: 255 if p > threshold else 0)
    bbox = bin_img.getbbox()
    if bbox:
        return bin_img.crop(bbox)
    return bin_img

def render_candidate(text, font_path, size, tracking=15):
    temp_img = Image.new("RGB", (2000, 200), (0, 0, 0))
    draw = ImageDraw.Draw(temp_img)
    
    try:
        font = ImageFont.truetype(font_path, size)
    except Exception as e:
        print(f"Error loading font {font_path}: {e}")
        return None
        
    chars = list(text)
    char_widths = []
    total_width = 0
    
    for c in chars:
        bbox = draw.textbbox((0, 0), c, font=font)
        w = bbox[2] - bbox[0]
        char_widths.append(w)
        total_width += w
        
    total_width += tracking * (len(chars) - 1)
    
    start_x = 100
    curr_x = start_x
    
    for c, w in zip(chars, char_widths):
        draw.text((curr_x, 50), c, fill=(255, 255, 255), font=font)
        curr_x += w + tracking
        
    gray_temp = temp_img.convert("L")
    bin_temp = gray_temp.point(lambda p: 255 if p > 100 else 0)
    bbox = bin_temp.getbbox()
    if bbox:
        return bin_temp.crop(bbox)
    return bin_temp

def compare_images(legacy_bin, candidate_bin, name):
    # Resize candidate to match legacy dimensions
    cand_resized = candidate_bin.resize(legacy_bin.size, Image.Resampling.LANCZOS)
    cand_resized = cand_resized.point(lambda p: 255 if p > 120 else 0)
    
    diff = ImageChops.difference(legacy_bin, cand_resized)
    
    w, h = diff.size
    diff_data = list(diff.getdata())
    mismatched = sum(1 for val in diff_data if val == 255)
    total_pixels = w * h
    pct_diff = (mismatched / total_pixels) * 100
    
    print(f"Comparison with {name}: {pct_diff:.3f}% pixel difference")
    
    compare_strip = Image.new("RGB", (w * 3 + 20, h), (100, 100, 100))
    compare_strip.paste(legacy_bin.convert("RGB"), (0, 0))
    compare_strip.paste(cand_resized.convert("RGB"), (w + 10, 0))
    compare_strip.paste(diff.convert("RGB"), (w * 2 + 20, 0))
    
    out_path = f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/compare_{name.lower().replace(' ', '_')}.png"
    compare_strip.save(out_path)
    
    return pct_diff

def run_comparison():
    legacy_path = "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_series_title_cropped.png"
    if not os.path.exists(legacy_path):
        print(f"Legacy cropped header image not found at {legacy_path}")
        return
        
    legacy_bin = Image.open(legacy_path)
    print(f"Legacy binarized size: {legacy_bin.size}")
    
    text = "THE WORKS OF JOHN OWEN"
    
    fonts = {
        "Arial Black": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "Trebuchet MS Bold": "/System/Library/Fonts/Supplemental/Trebuchet MS Bold.ttf",
        "Montserrat ExtraBold": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-ExtraBold.ttf",
        "Montserrat Black": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-Black.ttf",
    }
    
    results = {}
    for name, font_path in fonts.items():
        if not os.path.exists(font_path):
            print(f"Font file for {name} does not exist at {font_path}")
            continue
        print(f"\nComparing {name}...")
        # Since tracking spacing can vary, let's try different tracking values to find the best match
        best_pct = 100.0
        for track in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
            cand_bin = render_candidate(text, font_path, size=32, tracking=track)
            if cand_bin is not None:
                pct = compare_images(legacy_bin, cand_bin, f"{name}_track_{track}")
                if pct < best_pct:
                    best_pct = pct
        results[name] = best_pct
            
    print("\n=== Final Ranking (Lower is Better) ===")
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    for idx, (name, val) in enumerate(sorted_results):
        print(f"{idx+1}. {name}: {val:.3f}% mismatch")

if __name__ == "__main__":
    run_comparison()
