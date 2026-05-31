from PIL import Image, ImageDraw, ImageFont

def get_font_o_ratio(font_path, font_name, height=48):
    # Render a single 'O' on a temporary canvas
    temp_img = Image.new("RGB", (200, 200), (0, 0, 0))
    draw = ImageDraw.Draw(temp_img)
    
    try:
        font = ImageFont.truetype(font_path, height)
    except Exception as e:
        print(f"Error loading {font_name}: {e}")
        return None
        
    draw.text((50, 50), "O", fill=(255, 255, 255), font=font)
    
    # Binarize and crop
    gray = temp_img.convert("L")
    bin_img = gray.point(lambda p: 255 if p > 100 else 0)
    bbox = bin_img.getbbox()
    if bbox:
        cropped = bin_img.crop(bbox)
        w, h = cropped.size
        ratio = w / h
        print(f"Font: {font_name:22s} - Rendered 'O' Size: {w:2d}x{h:2d} - Aspect Ratio: {ratio:.3f}")
        return ratio
    return None

if __name__ == "__main__":
    print("=== Candidate Font Aspect Ratios for Letter 'O' ===")
    
    # Target ratio from legacy cover
    legacy_ratio = 35 / 48
    print(f"LEGACY COVER 'O' Aspect Ratio: {legacy_ratio:.3f}\n")
    
    fonts = {
        "Arial Black": "/System/Library/Fonts/Supplemental/Arial Black.ttf",
        "Trebuchet MS Bold": "/System/Library/Fonts/Supplemental/Trebuchet MS Bold.ttf",
        "Arial Bold": "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "Helvetica Neue Bold": "/System/Library/Fonts/HelveticaNeue.ttc",
        "Montserrat ExtraBold": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-ExtraBold.ttf",
        "Montserrat Black": "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-Black.ttf",
    }
    
    for name, path in fonts.items():
        get_font_o_ratio(path, name)
