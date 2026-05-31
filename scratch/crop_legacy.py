import os
from PIL import Image

def crop_sections(file_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    img = Image.open(file_path)
    w, h = img.size
    
    # Crop top header area (series title)
    header = img.crop((0, 0, w, 200))
    header.save(os.path.join(out_dir, "legacy_header.png"))
    print("Saved legacy_header.png")
    
    # Crop middle title/volume area
    middle = img.crop((0, 180, w, 550))
    middle.save(os.path.join(out_dir, "legacy_middle.png"))
    print("Saved legacy_middle.png")
    
    # Crop bottom author area
    bottom = img.crop((0, 550, w, h))
    bottom.save(os.path.join(out_dir, "legacy_bottom.png"))
    print("Saved legacy_bottom.png")

if __name__ == "__main__":
    crop_sections("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png", "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch")
