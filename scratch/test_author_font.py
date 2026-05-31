import os
from PIL import Image, ImageDraw, ImageFont

def print_candidate_char_shape(font_path, font_name, text, char_indices):
    # Render the text
    temp_img = Image.new("RGB", (600, 100), (0, 0, 0))
    draw = ImageDraw.Draw(temp_img)
    
    try:
        font = ImageFont.truetype(font_path, 48)
    except Exception as e:
        print(f"Error loading {font_name}: {e}")
        return
        
    draw.text((20, 20), text, fill=(255, 255, 255), font=font)
    
    # Binarize
    gray = temp_img.convert("L")
    bin_img = gray.point(lambda p: 255 if p > 100 else 0)
    
    # Segment columns
    w, h = bin_img.size
    col_counts = [0] * w
    for x in range(w):
        for y in range(h):
            if bin_img.getpixel((x, y)) == 255:
                col_counts[x] += 1
                
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
        
    print(f"\n==========================================")
    print(f"Font: {font_name} (Segments found: {len(segments)})")
    print(f"==========================================")
    
    for idx in char_indices:
        if idx < len(segments):
            x1, x2 = segments[idx]
            seg_w = x2 - x1 + 1
            # Crop to active bounding box vertically
            char_crop = bin_img.crop((x1, 0, x2 + 1, h))
            bbox = char_crop.getbbox()
            if bbox:
                char_crop = char_crop.crop(bbox)
                
            cw, ch = char_crop.size
            print(f"\nCharacter at Segment {idx} (Size: {cw}x{ch}, aspect_ratio={cw/ch:.3f}):")
            
            # Print console shape
            step_y = 1 if ch <= 24 else 2
            step_x = 1 if cw <= 24 else 2
            for y in range(0, ch, step_y):
                line = ""
                for x in range(0, cw, step_x):
                    val = char_crop.getpixel((x, y))
                    line += "#" if val == 255 else "."
                print(line)

if __name__ == "__main__":
    text = "John Owen"
    
    # Let's inspect the shapes of segment 0 (J), segment 1 (o), segment 2 (h)
    char_indices = [0, 1, 2, 4] # J, o, h, O
    
    fonts = {
        "Arial Black": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "Trebuchet MS Bold": "/System/Library/Fonts/Supplemental/Trebuchet MS Bold.ttf",
        "Montserrat ExtraBold": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-ExtraBold.ttf",
        "Montserrat Black": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-Black.ttf",
    }
    
    for name, path in fonts.items():
        if os.path.exists(path):
            print_candidate_char_shape(path, name, text, char_indices)
