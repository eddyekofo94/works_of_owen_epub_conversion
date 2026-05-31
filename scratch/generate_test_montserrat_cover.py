import os
import math
from PIL import Image, ImageDraw, ImageFont

# Colors
COLOR_TEAL = (0, 85, 85)       # #005555
COLOR_CYAN = (130, 214, 235)   # #82d6eb
COLOR_WHITE = (255, 255, 255)  # #ffffff
COLOR_MUTED_CYAN = (40, 115, 115) # #287373

# Font Paths
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_SNELL = "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc"

def draw_tracked_text(draw, text, position, font, color, tracking=10):
    chars = list(text)
    char_widths = []
    total_width = 0
    
    for c in chars:
        bbox = draw.textbbox((0, 0), c, font=font)
        w = bbox[2] - bbox[0]
        char_widths.append(w)
        total_width += w
        
    total_width += tracking * (len(chars) - 1)
    
    start_x = position[0] - total_width / 2
    curr_x = start_x
    
    for c, w in zip(chars, char_widths):
        draw.text((curr_x, position[1]), c, fill=color, font=font)
        curr_x += w + tracking

def draw_pattern(draw, w, h, color):
    # Sinusoidal Waves for Volume 4
    for y_start in range(50, h, 90):
        points = []
        for x in range(0, w + 20, 15):
            y = y_start + 30 * math.sin(x * 0.012)
            points.append((x, y))
        draw.line(points, fill=color, width=2)

def draw_volume_block(draw, vol_num, y_pos, font_cursive, font_number, w_canvas):
    v_text = "v."
    num_text = str(vol_num)
    
    v_bbox = draw.textbbox((0, 0), v_text, font=font_cursive)
    w_v = v_bbox[2] - v_bbox[0]
    h_v = v_bbox[3] - v_bbox[1]
    
    num_bbox = draw.textbbox((0, 0), num_text, font=font_number)
    w_num = num_bbox[2] - num_bbox[0]
    h_num = num_bbox[3] - num_bbox[1]
    
    num_x = w_canvas // 2 - w_num // 2
    
    draw.text(
        (num_x, y_pos),
        num_text,
        fill=COLOR_WHITE,
        font=font_number
    )
    
    overlap = 15
    v_x = num_x - w_v + overlap
    v_y = y_pos + h_num - h_v - 5
    
    draw.text(
        (v_x, v_y),
        v_text,
        fill=COLOR_MUTED_CYAN,
        font=font_cursive
    )

def generate_test_cover(font_path, font_name, output_path):
    print(f"Generating test cover for Volume 4 using font: {font_name}...")
    w, h = 1024, 1600
    img = Image.new("RGB", (w, h), COLOR_WHITE)
    draw = ImageDraw.Draw(img)
    
    # 1. Teal block temporary canvas (1024x1200)
    teal_w, teal_h = 1024, 1200
    teal_img = Image.new("RGB", (teal_w, teal_h), COLOR_TEAL)
    teal_draw = ImageDraw.Draw(teal_img)
    draw_pattern(teal_draw, teal_w, teal_h, COLOR_MUTED_CYAN)
    img.paste(teal_img, (0, 0))
    
    # 2. Teal separation stripe
    draw.rectangle([(0, 1244), (w, 1260)], fill=COLOR_TEAL)
    
    # Fonts
    font_series = ImageFont.truetype(FONT_ARIAL_BOLD, 32)
    # We use the selected font path for the giant volume number to test its shape as well!
    font_vol_num = ImageFont.truetype(font_path, 380)
    font_vol_v = ImageFont.truetype(FONT_ARIAL_ITALIC, 95)
    font_author = ImageFont.truetype(FONT_ARIAL_BOLD, 72)
    
    base_size = 112 # split size for Vol 4 longest line (SPIRIT is 6 chars)
    font_title = ImageFont.truetype(font_path, base_size)
    font_cursive = ImageFont.truetype(FONT_SNELL, int(base_size * 1.25))
    
    # Draw Series Title
    series_text = "THE WORKS OF JOHN OWEN"
    draw_tracked_text(draw, series_text, (w // 2, 110), font_series, COLOR_WHITE, tracking=15)
    
    # Draw Volume Number Block
    draw_volume_block(draw, 4, 190, font_vol_v, font_vol_num, w)
    
    # Draw Title Lines
    title_lines = [("the", True), ("WORK", False), ("of the", True), ("SPIRIT", False)]
    spacing = 15
    lines_data = []
    
    for text, is_cursive in title_lines:
        font = font_cursive if is_cursive else font_title
        formatted_text = text.lower() if is_cursive else text.upper()
        
        bbox = draw.textbbox((0, 0), formatted_text, font=font)
        line_h = bbox[3] - bbox[1]
        
        if is_cursive:
            line_h = int(line_h * 0.8)
            
        lines_data.append((formatted_text, is_cursive, font, line_h))
        
    total_height = sum(item[3] for item in lines_data) + spacing * (len(lines_data) - 1)
    
    center_y = 850
    start_y = center_y - total_height // 2
    
    curr_y = start_y
    for formatted_text, is_cursive, font, line_h in lines_data:
        if is_cursive:
            bbox = draw.textbbox((0, 0), formatted_text, font=font)
            w_text = bbox[2] - bbox[0]
            draw.text(
                (w // 2 - w_text // 2, curr_y), 
                formatted_text, 
                fill=COLOR_WHITE, 
                font=font,
                stroke_width=2,
                stroke_fill=COLOR_WHITE
            )
        else:
            draw_tracked_text(draw, formatted_text, (w // 2, curr_y), font, COLOR_CYAN, tracking=10)
            
        curr_y += line_h + spacing
        
    # Draw Author name
    author_text = "JOHN OWEN"
    draw_tracked_text(draw, author_text, (w // 2, 1360), font_author, COLOR_TEAL, tracking=20)
    
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    generate_test_cover(
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-Black.ttf",
        "Montserrat Black",
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/v4_test_black.png"
    )
    generate_test_cover(
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/fonts/Montserrat-ExtraBold.ttf",
        "Montserrat ExtraBold",
        "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/scratch/v4_test_extrabold.png"
    )
