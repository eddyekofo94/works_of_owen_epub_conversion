from PIL import Image

def print_char_shape(img_path, threshold=128):
    img = Image.open(img_path)
    w, h = img.size
    print(f"\n=== Shape of {img_path.split('/')[-1]} ({w}x{h}) ===")
    
    # Scale down horizontally for better terminal aspect ratio if needed,
    # but since it's 30-40 pixels, we can just print every pixel or every second pixel.
    step_y = 1
    step_x = 1
    if h > 30:
        step_y = 2
    if w > 30:
        step_x = 2
        
    for y in range(0, h, step_y):
        line = ""
        for x in range(0, w, step_x):
            val = img.getpixel((x, y))
            line += "#" if val == 255 else "."
        print(line)

if __name__ == "__main__":
    import glob
    files = sorted(glob.glob("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/author_char_*.png"))
    for f in files:
        print_char_shape(f)
