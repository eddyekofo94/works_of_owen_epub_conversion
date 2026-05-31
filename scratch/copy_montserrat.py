import os
import shutil

def copy_montserrat():
    src_dir = "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts"
    dest_dir = "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/fonts/Montserrat"
    
    os.makedirs(dest_dir, exist_ok=True)
    
    files = ["Montserrat-ExtraBold.ttf", "Montserrat-Black.ttf"]
    for f in files:
        src = os.path.join(src_dir, f)
        dest = os.path.join(dest_dir, f)
        if os.path.exists(src):
            shutil.copy2(src, dest)
            print(f"Copied {f} to {dest_dir}")
        else:
            print(f"Source font {f} not found in scratch.")

if __name__ == "__main__":
    copy_montserrat()
