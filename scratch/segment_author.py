from PIL import Image

def segment_author(img_path):
    img = Image.open(img_path)
    w, h = img.size
    print(f"Segmenting {img_path} ({w}x{h}):")
    
    # Vertical projection (find columns with active pixels)
    col_counts = [0] * w
    for x in range(w):
        for y in range(h):
            if img.getpixel((x, y)) == 255:
                col_counts[x] += 1
                
    # Detect letter segments
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
        
    print(f"Found {len(segments)} character segments:")
    for idx, (x1, x2) in enumerate(segments):
        seg_w = x2 - x1 + 1
        aspect = seg_w / h
        
        # Save cropped segment
        seg_img = img.crop((x1, 0, x2 + 1, h))
        seg_path = f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/author_char_{idx}.png"
        seg_img.save(seg_path)
        print(f"  Segment {idx:02d}: x1={x1:3d}, x2={x2:3d}, width={seg_w:2d}, aspect_ratio={aspect:.3f} -> Saved to {seg_path}")

if __name__ == "__main__":
    segment_author("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_block_10_dark_cropped.png")
