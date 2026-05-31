from PIL import Image

def find_all_elements(img_path):
    img = Image.open(img_path)
    w, h = img.size
    print(f"Analyzing entire image: {img_path} ({w}x{h})")
    
    # Create mask images for visualization
    light_text_mask = Image.new("L", (w, h), 0)
    dark_text_mask = Image.new("L", (w, h), 0)
    
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            
            # Check for Light Cyan / White text in teal blocks (R > 100, G > 180, B > 180)
            if r > 100 and g > 180 and b > 180:
                # Exclude the solid cream background area
                if not (r >= 240 and g >= 240 and b >= 230):
                    light_text_mask.putpixel((x, y), 255)
                    
            # Check for Dark Teal text/lines in cream blocks (R < 60, G between 40 and 120, B between 40 and 120)
            if r < 60 and 40 <= g <= 120 and 40 <= b <= 120:
                dark_text_mask.putpixel((x, y), 255)
                
    # Save mask images
    light_text_mask.save("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/mask_light_text.png")
    dark_text_mask.save("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/mask_dark_text.png")
    
    # Find bounding boxes of active regions
    # For light text, find distinct vertical blocks
    print("\n--- Light Text Mask (Teal Area) ---")
    bbox_light = light_text_mask.getbbox()
    if bbox_light:
        print(f"Global bounding box for light text: {bbox_light}")
    else:
        print("No light text detected.")
        
    # For dark text, find distinct vertical blocks
    print("\n--- Dark Text Mask (Cream Area) ---")
    bbox_dark = dark_text_mask.getbbox()
    if bbox_dark:
        print(f"Global bounding box for dark text: {bbox_dark}")
    else:
        print("No dark text detected.")
        
    # Let's find vertical projections of both masks to see where individual lines are
    project_y_light = [0] * h
    project_y_dark = [0] * h
    
    for y in range(h):
        for x in range(w):
            if light_text_mask.getpixel((x, y)) == 255:
                project_y_light[y] += 1
            if dark_text_mask.getpixel((x, y)) == 255:
                project_y_dark[y] += 1
                
    # Find and print active rows for light text
    in_block = False
    blocks = []
    start_y = 0
    for y, count in enumerate(project_y_light):
        if count > 5 and not in_block:
            in_block = True
            start_y = y
        elif count <= 5 and in_block:
            in_block = False
            blocks.append(("LIGHT", start_y, y - 1))
    if in_block:
        blocks.append(("LIGHT", start_y, h - 1))
        
    # Find and print active rows for dark text
    in_block = False
    for y, count in enumerate(project_y_dark):
        if count > 5 and not in_block:
            in_block = True
            start_y = y
        elif count <= 5 and in_block:
            in_block = False
            blocks.append(("DARK", start_y, y - 1))
    if in_block:
        blocks.append(("DARK", start_y, h - 1))
        
    # Sort blocks by vertical position
    blocks.sort(key=lambda x: x[1])
    print("\n--- Detected Vertical Text Blocks ---")
    for idx, (btype, y1, y2) in enumerate(blocks):
        block_h = y2 - y1 + 1
        # Crop the block and save it
        block_img = img.crop((0, y1, w, y2 + 1))
        block_path = f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/detected_block_{idx}_{btype.lower()}.png"
        block_img.save(block_path)
        print(f"Block {idx:02d} ({btype}): y={y1} to {y2} (height={block_h}) -> Saved to {block_path}")

if __name__ == "__main__":
    find_all_elements("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png")
