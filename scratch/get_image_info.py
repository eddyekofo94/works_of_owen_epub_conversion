from PIL import Image

def get_image_info(file_path):
    img = Image.open(file_path)
    print(f"File: {file_path}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")

if __name__ == "__main__":
    get_image_info("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers_backup/v1.png")
