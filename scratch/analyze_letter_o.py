from PIL import Image

def analyze_letter_segments(img_path):
    img = Image.open(img_path)
    w, h = img.size
    
    # Project vertically to segment characters
    col_counts = [0] * w
    for x in range(w):
        for y in range(h):
            if img.getpixel((x, y)) == 255:
                col_counts[x] += 1
                
    # Detect segments
    in_segment = False
    segments = []
    start_x = 0
    for x, count in enumerate(col_counts):
        if count > 0 and not in_segment:
            in_segment = True
            start_x = x
        elif count == 0 and in_segment:
            in_segment = False
            segments.append((start_x, x - 1))
    if in_segment:
        segments.append((start_x, w - 1))
        
    print(f"Total letter segments detected: {len(segments)}")
    
    # We want to find segments that look like the letter 'O'.
    # In "THE WORKS OF JOHN OWEN", letters are:
    # 0:T, 1:H, 2:E, (space)
    # 3:W, 4:O, 5:R, 6:K, 7:S, (space)
    # 8:O, 9:F, (space)
    # 10:J, 11:O, 12:H, 13:N, (space)
    # 14:O, 15:W, 16:E, 17:N
    # Note that due to spacing/binarization, some letters might merge. Let's print all widths and aspect ratios!
    for idx, (x1, x2) in enumerate(segments):
        seg_w = x2 - x1 + 1
        aspect = seg_w / h
        
        # Crop segment
        seg_img = img.crop((x1, 0, x2 + 1, h))
        seg_img.save(f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/seg_{idx}.png")
        print(f"Segment {idx:02d}: x1={x1:03d}, x2={x2:03d}, width={seg_w:02d}, aspect_ratio={aspect:.3f}")

if __name__ == "__main__":
    analyze_letter_segments("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_series_title_cropped.png")
