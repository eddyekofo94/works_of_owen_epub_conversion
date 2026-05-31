import os
from PIL import Image

def dump_full_xmp(file_path):
    img = Image.open(file_path)
    xmp_data = img.info.get("xmp")
    if xmp_data:
        try:
            print(xmp_data.decode("utf-8"))
        except Exception as e:
            print("Failed to decode XMP as UTF-8:", e)
            print(xmp_data)
    else:
        print("No XMP data found in", file_path)

if __name__ == "__main__":
    dump_full_xmp("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v4.png")
