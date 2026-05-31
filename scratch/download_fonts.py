import os
import urllib.request

FONT_URLS = {
    "Montserrat-Black.ttf": "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Black.ttf",
    "Montserrat-ExtraBold.ttf": "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-ExtraBold.ttf",
    "LeagueSpartan-Bold.otf": "https://github.com/theleagueof/league-spartan/raw/master/LeagueSpartan-Bold.otf"
}

def download_fonts(target_dir):
    os.makedirs(target_dir, exist_ok=True)
    for name, url in FONT_URLS.items():
        dest = os.path.join(target_dir, name)
        if os.path.exists(dest):
            print(f"Font {name} already exists.")
            continue
        print(f"Downloading {name} from {url}...")
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Successfully downloaded {name} to {dest}")
        except Exception as e:
            # Try alternate branch (e.g. main instead of master)
            alt_url = url.replace("/master/", "/main/")
            print(f"Error downloading from main URL, trying branch fallback: {alt_url}...")
            try:
                req = urllib.request.Request(
                    alt_url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
                )
                with urllib.request.urlopen(req) as response, open(dest, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"Successfully downloaded {name} from branch fallback")
            except Exception as e2:
                print(f"Failed to download {name}: {e2}")

if __name__ == "__main__":
    download_fonts("/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts")
