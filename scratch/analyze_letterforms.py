import os
from PIL import Image

def analyze_legacy_header(img_path):
    img = Image.open(img_path).convert("L")
    w, h = img.size
    
    # Binarize: background is around 30-60, text is around 180-255
    threshold = 120
    bin_img = img.point(lambda p: 255 if p > threshold else 0)
    
    bin_img.save("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_header.png")
    print("Saved binarized header to bin_header.png")
    
    # Horizontal projection
    histogram_y = [0] * h
    for y in range(h):
        for x in range(w):
            if bin_img.getpixel((x, y)) == 255:
                histogram_y[y] += 1
                
    # Find active text line vertical span
    active_y = [y for y, count in enumerate(histogram_y) if count > 2] # smaller threshold to catch faint lines
    if not active_y:
        print("No text pixels found!")
        return
        
    y_min, y_max = min(active_y), max(active_y)
    print(f"Detected text line vertical span: y={y_min} to y={y_max}")
    
    # Crop the exact text line segment
    line_img = bin_img.crop((0, y_min, w, y_max + 1))
    line_w, line_h = line_img.size
    print(f"Cropped text line size: {line_w}x{line_h}")
    
    # Vertical projection (find spacing along X axis)
    histogram_x = [0] * line_w
    for x in range(line_w):
        for y in range(line_h):
            if line_img.getpixel((x, y)) == 255:
                histogram_x[x] += 1
                
    # Bounding boxes of individual letters
    in_letter = False
    letters = []
    start_x = 0
    for x, count in enumerate(histogram_x):
        if count > 0 and not in_letter:
            in_letter = True
            start_x = x
        elif count == 0 and in_letter:
            in_letter = False
            letters.append((start_x, x - 1))
    if in_letter:
        letters.append((start_x, line_w - 1))
        
    print(f"Found {len(letters)} letter segments along X axis:")
    for idx, (lx1, lx2) in enumerate(letters):
        lw = lx2 - lx1 + 1
        # Crop each letter
        letter_img = line_img.crop((lx1, 0, lx2 + 1, line_h))
        letter_img.save(f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/letter_{idx}.png")
        print(f"  Letter {idx}: x1={lx1}, x2={lx2}, width={lw}, aspect_ratio={lw/line_h:.3f}")

if __name__ == "__main__":
    analyze_legacy_header("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/legacy_header.png")
