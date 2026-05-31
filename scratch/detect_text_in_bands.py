from PIL import Image

def analyze_band_colors(band_path, band_index):
    img = Image.open(band_path)
    w, h = img.size
    
    # We define three categories of pixels:
    # 1. Background Teal: (0, 85, 85) or similar
    # 2. Cream/Off-white: (250-255, 250-255, 240-255)
    # 3. Light Cyan/White (text in teal areas): (100-255, 200-255, 200-255) where R > 80 and not cream
    # 4. Dark Teal/Text (text in cream areas): (0-60, 50-100, 50-100)
    
    bg_teal_count = 0
    cream_count = 0
    light_text_count = 0
    dark_text_count = 0
    
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            
            # Check for Background Teal
            if r < 30 and 70 <= g <= 95 and 70 <= b <= 95:
                bg_teal_count += 1
            # Check for Cream/Off-white
            elif r >= 240 and g >= 240 and b >= 230:
                cream_count += 1
            # Check for Light Cyan / White text (in teal area)
            elif r >= 100 and g >= 180 and b >= 180:
                light_text_count += 1
            # Check for Dark Teal / Text (in cream area)
            elif r < 40 and 60 <= g <= 82 and 60 <= b <= 82:
                dark_text_count += 1
                
    total = w * h
    print(f"Band {band_index} (y={band_index*100} to {(band_index+1)*100}):")
    print(f"  Bg Teal:    {bg_teal_count:5d} pixels ({bg_teal_count/total*100:5.1f}%)")
    print(f"  Cream/White: {cream_count:5d} pixels ({cream_count/total*100:5.1f}%)")
    print(f"  Light Text:  {light_text_count:5d} pixels ({light_text_count/total*100:5.1f}%)")
    print(f"  Dark Text:   {dark_text_count:5d} pixels ({dark_text_count/total*100:5.1f}%)")

if __name__ == "__main__":
    for i in range(8):
        analyze_band_colors(f"/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/band_{i}.png", i)
