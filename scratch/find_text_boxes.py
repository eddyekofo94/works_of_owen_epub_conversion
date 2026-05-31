from PIL import Image

def find_active_box(img_path):
    img = Image.open(img_path)
    bbox = img.getbbox()
    if bbox:
        print(f"File: {img_path} - Bounding Box: {bbox} (width: {bbox[2] - bbox[0]}, height: {bbox[3] - bbox[1]})")
        # Crop and save
        cropped = img.crop(bbox)
        cropped_path = img_path.replace(".png", "_cropped.png")
        cropped.save(cropped_path)
        print(f"  Saved cropped version to {cropped_path}")
    else:
        print(f"File: {img_path} - No text pixels detected.")

if __name__ == "__main__":
    find_active_box("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_series_title.png")
    find_active_box("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/bin_author.png")
