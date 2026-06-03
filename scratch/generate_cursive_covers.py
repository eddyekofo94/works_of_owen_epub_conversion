from PIL import Image, ImageDraw, ImageFont
import os

WIDTH, HEIGHT = 1600, 2560
COLOR_TEAL_BG = "#0b464a"      
COLOR_WHITE_BG = "#ffffff"     
COLOR_TITLE = "#7ac4d8"        
COLOR_MUTED_V = "#638f92"      
COLOR_NUMBER = "#ffffff"       
COLOR_AUTHOR = "#0b464a"       

FONT_PATHS = {
    "bebas": "/Users/eddyekofo/Library/Fonts/BebasNeue-Regular.ttf",
    "snell": "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc",
    "oswald": "/Users/eddyekofo/Library/Fonts/Oswald-Bold.ttf",
    "helvetica": "/System/Library/Fonts/Helvetica.ttc"
}

def get_dynamic_line_font(line_text, font_path, target_width, max_height=500, start_size=700):
    size = min(start_size, 700)
    img_temp = Image.new("RGB", (10, 10))
    draw_temp = ImageDraw.Draw(img_temp)
    while size > 30:
        font = ImageFont.truetype(font_path, size)
        bbox = draw_temp.textbbox((0, 0), line_text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= target_width and h <= max_height:
            return font, size
        size -= 5
    return ImageFont.truetype(font_path, size), size

def test_generate(vol_num, title_lines):
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_WHITE_BG)
    draw = ImageDraw.Draw(img)
    
    teal_bottom_y = 1750
    draw.rectangle([0, 0, WIDTH, teal_bottom_y], fill=COLOR_TEAL_BG)

    left_margin = 65
    right_margin = 65
    max_w = WIDTH - left_margin - right_margin
    left_col_width = 1000

    # 1. Get massive Oswald Bold sizes for number
    # Almost 100% bigger: let us use colossal sizes!
    if len(vol_num) == 1:
        num_size = 850  # Huge!
    else:
        num_size = 700  # Massive for double-digits!

    font_num = ImageFont.truetype(FONT_PATHS["oswald"], num_size)
    
    # Snell Roundhand for "Volume"
    font_v = ImageFont.truetype(FONT_PATHS["snell"], 160) # Elegant cursive

    # Measure volume text and giant number
    num_bbox = draw.textbbox((0, 0), vol_num, font=font_num)
    num_w = num_bbox[2] - num_bbox[0]
    num_h = num_bbox[3] - num_bbox[1]
    
    # For Snell Roundhand, let us measure "Volume" ink carefully
    v_bbox = draw.textbbox((0, 0), "Volume", font=font_v)
    v_w = v_bbox[2] - v_bbox[0]
    v_h = v_bbox[3] - v_bbox[1]

    # Stacking and centering:
    # Volume is right-aligned flush with right margin, and "Volume" is centered EXACTLY on the number!
    right_align_x = WIDTH - right_margin # 1535
    num_x = right_align_x - num_w
    
    # Snell Roundhand can have a slight italic slant or left overshoot, let us center exactly on the giant number
    v_x = num_x + (num_w / 2) - (v_w / 2)
    
    v_y = 150
    v_gap = 10
    num_y = v_y + (v_bbox[3] - v_bbox[1]) + v_gap

    # Draw number and Volume cursive
    # Offset by bbox[1] for exact vertical control of cursive and numbers
    draw.text((v_x - v_bbox[0], v_y - v_bbox[1]), "Volume", fill=COLOR_MUTED_V, font=font_v)
    draw.text((num_x - num_bbox[0], num_y - num_bbox[1]), vol_num, fill=COLOR_NUMBER, font=font_num)

    # Draw left title (do not move, keep y coordinate at 160)
    target_widths = [left_col_width, left_col_width, max_w]
    drawn_lines = []
    for i, line in enumerate(title_lines):
        font, size = get_dynamic_line_font(line, FONT_PATHS["bebas"], target_widths[i], max_height=420)
        bbox = draw.textbbox((0, 0), line, font=font)
        drawn_lines.append({
            "text": line,
            "font": font,
            "w": bbox[2]-bbox[0],
            "h": bbox[3]-bbox[1],
            "bbox": bbox
        })

    curr_y = 160
    for line in drawn_lines:
        y_pos = curr_y - line["bbox"][1]
        draw.text((left_margin, y_pos), line["text"], fill=COLOR_TITLE, font=line["font"])
        curr_y += line["h"] + 25

    # Author and line
    line_margin = 150
    line_y = teal_bottom_y + 150
    draw.rectangle([line_margin, line_y, WIDTH - line_margin, line_y + 25], fill=COLOR_AUTHOR)
    
    font_author = ImageFont.truetype(FONT_PATHS["helvetica"], 170)
    author_text = "John Owen"
    author_bbox = draw.textbbox((0, 0), author_text, font=font_author)
    author_x = (WIDTH - (author_bbox[2]-author_bbox[0])) / 2
    draw.text((author_x, line_y + 90), author_text, fill=COLOR_AUTHOR, font=font_author)

    output_path = f"covers/test_v{vol_num}.png"
    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

test_generate("3", ["THE", "HOLY", "SPIRIT"])
test_generate("16", ["A", "GOSPEL", "CHURCH"])
