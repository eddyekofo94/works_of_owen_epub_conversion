from PIL import Image, ImageDraw, ImageFont
import os

# Apple Books high-quality standard dimensions
WIDTH, HEIGHT = 1600, 2560

# Prototype Color Palette (Collection-wide coherence)
COLOR_TEAL_BG = "#0b464a"      
COLOR_WHITE_BG = "#ffffff"     
COLOR_TITLE = "#7ac4d8"        
COLOR_MUTED_V = "#638f92"      
COLOR_NUMBER = "#ffffff"       
COLOR_AUTHOR = "#0b464a"       
COLOR_CONNECTOR = "#b2ecf2"    

# Bespoke, hand-crafted configurations for each individual volume.
# Every cover is treated as a unique canvas with custom-tailoring.
# Changed Vol 9 to giant_right + bebas to resolve the overlap completely!
# Kept unique configurations for other volumes, but resolved all spilling/bleeding/overlapping.
VOL_CONFIGS = {
    "1": {
        "lines": ["THE", "GLORY", "OF", "CHRIST"],
        "layout": "giant_right",
        "font": "league_gothic",
        "start_y": 220,
        "num_offset_x": -230,
        "num_offset_y": -30,
        "line_scales": [0.65, 0.75, 0.55, 1.3]
    },
    "2": {
        "lines": ["COMMUNION", "WITH", "GOD"],
        "layout": "bottom_left",
        "font": "anton",
        "start_y": 350
    },
    "3": {
        "lines": ["THE", "HOLY", "SPIRIT"],
        "layout": "giant_right_3line",
        "font": "bebas",
        "start_y": 220
    },
    "4": {
        "lines": ["THE", "REASON", "OF", "FAITH"],
        "layout": "giant_right",
        "font": "impact",
        "start_y": 220,
        "line_scales": [0.85, 0.85, 0.75, 0.85]
    },
    "5": {
        "lines": ["JUSTIFICATION", "BY", "FAITH"],
        "layout": "giant_left",
        "font": "oswald",
        "start_y": 550,
        "line_scales": [0.85, 0.85, 0.9]
    },
    "6": {
        "lines": ["MORTIFICATION", "OF", "SIN"],
        "layout": "giant_left",
        "font": "league_gothic",
        "start_y": 200,
        "line_scales": [1.25, 0.95, 0.95],
        "num_offset_x": 100,
        "num_offset_y": 580,
        "right_col_width": 1050
    },
    "7": {
        "lines": ["SIN", "AND", "GRACE"],
        "layout": "giant_right_3line",
        "font": "anton",
        "start_y": 500,
        "left_col_width": 800,
        "num_offset_x": -250,
        "line_scales": [0.9, 0.8, 0.85]
    },
    "8": {
        "lines": ["SERMONS", "TO", "THE", "NATION"],
        "layout": "bottom_left_4line",
        "font": "bebas",
        "start_y": 350
    },
    "9": {
        "lines": ["SERMONS", "TO", "THE", "CHURCH"],
        "layout": "giant_right",
        "font": "bebas",
        "start_y": 220,
        "line_scales": [0.9, 0.8, 0.8, 0.9]
    },
    "10": {
        "lines": ["THE", "DEATH", "OF", "DEATH"],
        "layout": "giant_right",
        "font": "oswald",
        "start_y": 220,
        "left_col_width": 750,
        "line_scales": [0.75, 0.75, 0.75, 0.85]
    },
    "11": {
        "lines": ["PERSEVERANCE", "OF", "THE", "SAINTS"],
        "layout": "bottom_left_4line",
        "font": "league_gothic",
        "start_y": 350,
        "line_scales": [0.9, 0.8, 0.8, 0.9]
    },
    "12": {
        "lines": ["SOCINIANISM", "EXAMINED"],
        "layout": "style_c",
        "font": "anton",
        "num_x_align": "left",
        "num_offset_x": -50
    },
    "13": {
        "lines": ["SCHISM", "&", "CHURCH", "FELLOWSHIP"],
        "layout": "giant_right",
        "font": "bebas",
        "start_y": 380,
        "line_scales": [0.85, 0.7, 0.85, 0.8]
    },
    "14": {
        "lines": ["FIAT", "LUX", "EXAMINED"],
        "layout": "giant_right_3line",
        "font": "impact",
        "start_y": 220,
        "line_scales": [0.9, 0.9, 0.8]
    },
    "15": {
        "lines": ["EVANGELICAL", "CHURCHES"],
        "layout": "giant_left",
        "font": "oswald",
        "start_y": 200,
        "line_scales": [1.25, 1.25],
        "num_offset_x": -50,
        "num_offset_y": 740,
        "right_col_width": 1100
    },
    "16": {
        "lines": ["A", "GOSPEL", "CHURCH"],
        "layout": "giant_right_3line",
        "font": "bebas",
        "start_y": 600,
        "line_scales": [0.8, 0.8, 0.8],
        "num_offset_x": -90
    }
}

# Resolved Font Paths
FONT_PATHS = {
    "bebas": "/Users/eddyekofo/Library/Fonts/BebasNeue-Regular.ttf",
    "snell": "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc",
    "oswald": "/Users/eddyekofo/Library/Fonts/Oswald-Bold.ttf",
    "anton": "/Users/eddyekofo/Library/Fonts/Anton-Regular.ttf",
    "league_gothic": "/Users/eddyekofo/Library/Fonts/LeagueGothic-Regular.ttf",
    "impact": "/System/Library/Fonts/Supplemental/Impact.ttf",
    "helvetica": "/System/Library/Fonts/Helvetica.ttc"
}

def get_dynamic_line_font(line_text, font_path, target_width, max_height=500, start_size=700):
    size = min(start_size, 700)
    img_temp = Image.new("RGB", (10, 10))
    draw_temp = ImageDraw.Draw(img_temp)
    while size > 30:
        try:
            font = ImageFont.truetype(font_path, size)
        except IOError:
            font = ImageFont.load_default()
            break
        
        bbox = draw_temp.textbbox((0, 0), line_text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        if w <= target_width and h <= max_height:
            return font, size
        size -= 5
    return ImageFont.truetype(font_path, size), size

def get_perfect_title_layout(lines, font_path_title, font_path_snell, target_widths, max_vertical_h, line_gap=25, line_scales=None):
    drawn_lines = []
    temp_img = Image.new("RGB", (10, 10))
    temp_draw = ImageDraw.Draw(temp_img)
    
    scale = 1.0
    for attempt in range(10):
        drawn_lines = []
        for i, line in enumerate(lines):
            target_w = target_widths[i] if i < len(target_widths) else target_widths[-1]
            line_scale = line_scales[i] if (line_scales and i < len(line_scales)) else 1.0
            
            orig_size = min(700, int(700 * scale * line_scale))
            max_h = int(420 * scale * line_scale)
            
            # Detect connector
            is_conn = line.upper() in {"THE", "OF", "WITH", "BY", "AND", "TO", "&", "A"}
            f_path = font_path_snell if is_conn else font_path_title
            display_text = line.lower() if is_conn else line
            
            # Cursive connectors look best slightly smaller and highly elegant
            cur_line_scale = line_scale * 0.85 if is_conn else line_scale
            
            font, size = get_dynamic_line_font(display_text, f_path, int(target_w * cur_line_scale), max_height=max_h, start_size=orig_size)
            bbox = temp_draw.textbbox((0, 0), display_text, font=font)
            drawn_lines.append({
                "text": display_text,
                "size": size,
                "w": bbox[2] - bbox[0],
                "h": bbox[3] - bbox[1],
                "font": font,
                "is_connector": is_conn
            })
            
        total_h = sum(line["h"] for line in drawn_lines) + line_gap * (len(lines) - 1)
        if total_h <= max_vertical_h:
            break
        scale *= (max_vertical_h / total_h)
        
    return drawn_lines, total_h

def draw_spaced_text(draw, text, x, y, font, fill, spacing=10, align="center"):
    glyphs = [char for char in text]
    sizes = []
    temp_img = Image.new("RGB", (10, 10))
    temp_draw = ImageDraw.Draw(temp_img)
    for g in glyphs:
        if g == " ":
            bbox = temp_draw.textbbox((0, 0), "A", font=font)
            sizes.append((bbox[2] - bbox[0]) * 0.5)
        else:
            bbox = temp_draw.textbbox((0, 0), g, font=font)
            sizes.append(bbox[2] - bbox[0])
    
    total_w = sum(sizes) + spacing * (len(glyphs) - 1)
    
    if align == "center":
        curr_x = x - total_w / 2
    else:
        curr_x = x
        
    for i, g in enumerate(glyphs):
        bbox = draw.textbbox((0, 0), g, font=font)
        draw.text((curr_x - bbox[0], y - bbox[1]), g, fill=fill, font=font)
        curr_x += sizes[i] + spacing

def draw_vintage_pattern(draw, width, height_limit):
    # Draw a repeating 17th-century diamond trellis with a floral rosette in each diamond center
    spacing_x = 160
    spacing_y = 160
    pattern_color = "#0e5256"  # Subtle watermark teal
    
    # 1. Draw diagonal trellis grid lines
    for offset in range(-height_limit, width, spacing_x):
        draw.line([offset, 0, offset + height_limit, height_limit], fill=pattern_color, width=2)
    for offset in range(0, width + height_limit, spacing_x):
        draw.line([offset, 0, offset - height_limit, height_limit], fill=pattern_color, width=2)
        
    # 2. Draw stylized rosettes at diamond centers
    for y in range(0, height_limit + 40, spacing_y // 2):
        row = y // (spacing_y // 2)
        shift = (spacing_x // 2) if (row % 2 == 1) else 0
        for x in range(-shift, width + shift + 40, spacing_x):
            cx = x + shift
            cy = y
            if 0 <= cy <= height_limit:
                # Center bud
                draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=pattern_color)
                # Outer petals (N, S, W, E)
                r_petal = 2
                draw.ellipse([cx - r_petal, cy - 9 - r_petal, cx + r_petal, cy - 9 + r_petal], fill=pattern_color)
                draw.ellipse([cx - r_petal, cy + 9 - r_petal, cx + r_petal, cy + 9 + r_petal], fill=pattern_color)
                draw.ellipse([cx - 9 - r_petal, cy - r_petal, cx - 9 + r_petal, cy + r_petal], fill=pattern_color)
                draw.ellipse([cx + 9 - r_petal, cy - r_petal, cx + 9 + r_petal, cy + r_petal], fill=pattern_color)

def generate_cover(vol_num):
    config = VOL_CONFIGS[vol_num]
    lines = config["lines"]
    layout = config["layout"]
    font_key = config["font"]
    
    font_path_title = FONT_PATHS[font_key]
    font_path_snell = FONT_PATHS["snell"]
    font_path_oswald = FONT_PATHS["oswald"]
    font_path_helvetica = FONT_PATHS["helvetica"]

    # 1. Create Base Image (White)
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_WHITE_BG)
    draw = ImageDraw.Draw(img)
    
    # Define author font
    try:
        font_author = ImageFont.truetype(font_path_helvetica, 170)
    except IOError as e:
        print(f"System Font error: Please verify your font files exist. Details: {e}")
        return

    # 2. Draw Dark Teal Top Section
    teal_bottom_y = 1750
    draw.rectangle([0, 0, WIDTH, teal_bottom_y], fill=COLOR_TEAL_BG)
    draw_vintage_pattern(draw, WIDTH, teal_bottom_y)

    left_margin = 130
    right_margin = 80
    max_w = WIDTH - left_margin - right_margin  # 1470

    # Snell Roundhand for "Volume" - size 160 for high eligibility in thumbnails
    v_size = 160
    
    # Colossal Oswald Bold number sizes for clear small thumbnails (almost 100% bigger!)
    if layout in ["giant_right", "giant_right_3line", "giant_left"]:
        num_size = 850 if len(vol_num) == 1 else 680
    else:  # style_c, bottom_left, bottom_left_4line
        num_size = 700 if len(vol_num) == 1 else 580

    try:
        font_v = ImageFont.truetype(font_path_snell, v_size)
        font_num = ImageFont.truetype(font_path_oswald, num_size)
    except IOError as e:
        print(f"System Font error: Please verify your font files exist. Details: {e}")
        return

    # Pre-measure Volume and Number
    v_bbox = draw.textbbox((0, 0), "Volume", font=font_v)
    num_bbox = draw.textbbox((0, 0), vol_num, font=font_num)
    v_w, v_h = v_bbox[2] - v_bbox[0], v_bbox[3] - v_bbox[1]
    num_w, num_h = num_bbox[2] - num_bbox[0], num_bbox[3] - num_bbox[1]
    
    # Tight vertical gap between "Volume" and the number
    v_gap = 10
    
    # Absolute Ink Bottom coordinate target for all bottom-aligned layouts.
    ink_bottom_target = 1640

    # -------------------------------------------------------------
    # BESPOKE LAYOUT ROUTINES
    # -------------------------------------------------------------
    start_y = config.get("start_y", 160)
    num_offset_x = config.get("num_offset_x", 0)
    num_offset_y = config.get("num_offset_y", 0)
    left_col_width = config.get("left_col_width", 950)
    right_col_width = config.get("right_col_width", 950)
    num_x_align = config.get("num_x_align", "right" if layout in ["giant_right", "giant_right_3line", "style_c"] else "left")

    if layout in ["giant_right", "giant_right_3line"]:
        target_widths = []
        for i in range(len(lines)):
            if i < 2:
                target_widths.append(left_col_width)
            else:
                target_widths.append(max_w)
                
        drawn_lines, total_title_h = get_perfect_title_layout(
            lines, font_path_title, font_path_snell, target_widths, max_vertical_h=ink_bottom_target - start_y, line_gap=25,
            line_scales=config.get("line_scales")
        )
        
        curr_y = start_y

        # Draw left-aligned title
        for line in drawn_lines:
            bbox = draw.textbbox((0, 0), line["text"], font=line["font"])
            y_pos = curr_y - bbox[1]
            fill_color = COLOR_CONNECTOR if line["is_connector"] else COLOR_TITLE
            draw.text((left_margin, y_pos), line["text"], fill=fill_color, font=line["font"])
            curr_y += line["h"] + 25

        # Draw Volume stacked block in the upper right corner (centered horizontally as a unit!)
        right_align_x = WIDTH - right_margin # 1535
        num_x = right_align_x - num_w + num_offset_x
        
        # Center "Volume" exactly on top of the giant number
        v_x = num_x + (num_w / 2) - (v_w / 2)
        
        v_y = 150 + num_offset_y
        num_y = v_y + (v_bbox[3] - v_bbox[1]) + v_gap
        
        draw.text((v_x - v_bbox[0], v_y - v_bbox[1]), "Volume", fill=COLOR_MUTED_V, font=font_v)
        draw.text((num_x - num_bbox[0], num_y - num_bbox[1]), vol_num, fill=COLOR_NUMBER, font=font_num)

    elif layout == "giant_left":
        target_widths = []
        for i in range(len(lines)):
            if i < 2:
                target_widths.append(right_col_width)
            else:
                target_widths.append(max_w)
                
        drawn_lines, total_title_h = get_perfect_title_layout(
            lines, font_path_title, font_path_snell, target_widths, max_vertical_h=ink_bottom_target - start_y, line_gap=25,
            line_scales=config.get("line_scales")
        )
        
        curr_y = start_y
        
        # Draw right-aligned title
        for line in drawn_lines:
            line_x = WIDTH - right_margin - line["w"]
            bbox = draw.textbbox((0, 0), line["text"], font=line["font"])
            y_pos = curr_y - bbox[1]
            fill_color = COLOR_CONNECTOR if line["is_connector"] else COLOR_TITLE
            draw.text((line_x, y_pos), line["text"], fill=fill_color, font=line["font"])
            curr_y += line["h"] + 25

        # Draw Volume stacked block on the Left Column
        num_x = left_margin + 50 + num_offset_x
        v_x = num_x + num_w / 2 - v_w / 2
        
        v_y = 150 + num_offset_y
        num_y = v_y + (v_bbox[3] - v_bbox[1]) + v_gap

        draw.text((v_x - v_bbox[0], v_y - v_bbox[1]), "Volume", fill=COLOR_MUTED_V, font=font_v)
        draw.text((num_x - num_bbox[0], num_y - num_bbox[1]), vol_num, fill=COLOR_NUMBER, font=font_num)

    elif layout == "style_c":
        # Style C: Volume block stacked + Bottom massive title (Only Vol 12)
        if num_x_align == "left":
            # Align with left title margin
            num_x = left_margin + 50 + num_offset_x
            v_x = num_x + num_w / 2 - v_w / 2
        else:
            # Center in right column
            right_col_w = 360
            right_col_center_x = 1175 + right_col_w / 2
            num_x = right_col_center_x - num_w / 2 + num_offset_x
            v_x = num_x + num_w / 2 - v_w / 2
        
        v_y = 150 + num_offset_y
        num_y = v_y + (v_bbox[3] - v_bbox[1]) + v_gap
        
        draw.text((v_x - v_bbox[0], v_y - v_bbox[1]), "Volume", fill=COLOR_MUTED_V, font=font_v)
        draw.text((num_x - num_bbox[0], num_y - num_bbox[1]), vol_num, fill=COLOR_NUMBER, font=font_num)

        # Title completely restricted vertically to [700, 1620]px to avoid overlap
        target_widths = [max_w] * len(lines)
        drawn_lines, total_title_h = get_perfect_title_layout(
            lines, font_path_title, font_path_snell, target_widths, max_vertical_h=920, line_gap=25,
            line_scales=config.get("line_scales")
        )
        
        curr_y = 700 + (920 - total_title_h) / 2

        # Draw left-aligned title
        for line in drawn_lines:
            bbox = draw.textbbox((0, 0), line["text"], font=line["font"])
            y_pos = curr_y - bbox[1]
            fill_color = COLOR_CONNECTOR if line["is_connector"] else COLOR_TITLE
            draw.text((left_margin, y_pos), line["text"], fill=fill_color, font=line["font"])
            curr_y += line["h"] + 25

    elif layout in ["bottom_left", "bottom_left_4line"]:
        # Right title, bottom-left volume number.
        # Restrict bottom-most lines of title to right column to prevent overlap
        start_y = config.get("start_y", 160)
        target_widths = [900] * len(lines)
                
        drawn_lines, total_title_h = get_perfect_title_layout(
            lines, font_path_title, font_path_snell, target_widths, max_vertical_h=ink_bottom_target - start_y, line_gap=25,
            line_scales=config.get("line_scales")
        )
        
        curr_y = start_y
        
        # Draw right-aligned title
        for line in drawn_lines:
            line_x = WIDTH - right_margin - line["w"]
            bbox = draw.textbbox((0, 0), line["text"], font=line["font"])
            y_pos = curr_y - bbox[1]
            fill_color = COLOR_CONNECTOR if line["is_connector"] else COLOR_TITLE
            draw.text((line_x, y_pos), line["text"], fill=fill_color, font=line["font"])
            curr_y += line["h"] + 25

        # Draw Volume stacked block on the bottom left
        # Center "Volume" exactly on top of the giant number
        num_x = left_margin + 50
        v_x = num_x + num_w / 2 - v_w / 2
        
        num_y = ink_bottom_target - num_bbox[3]
        v_y = num_y - (v_bbox[3] - v_bbox[1]) - v_gap

        draw.text((v_x - v_bbox[0], v_y - v_bbox[1]), "Volume", fill=COLOR_MUTED_V, font=font_v)
        draw.text((num_x - num_bbox[0], num_y - num_bbox[1]), vol_num, fill=COLOR_NUMBER, font=font_num)
    # Draw Series Title: "THE WORKS OF JOHN OWEN" in muted color
    try:
        font_series = ImageFont.truetype(font_path_helvetica, 34)
    except IOError:
        font_series = ImageFont.load_default()
        
    series_text = "THE WORKS OF JOHN OWEN"
    series_y = 1680
        
    draw_spaced_text(draw, series_text, WIDTH / 2, series_y, font_series, COLOR_MUTED_V, spacing=15, align="center")

    # 5. Draw Thick Author Line
    line_margin = 150
    line_y = teal_bottom_y + 150
    line_thickness = 25
    draw.rectangle(
        [line_margin, line_y, WIDTH - line_margin, line_y + line_thickness],
        fill=COLOR_AUTHOR
    )

    # 6. Draw Author Name
    author_text = "John Owen"
    author_bbox = draw.textbbox((0, 0), author_text, font=font_author)
    author_w = author_bbox[2] - author_bbox[0]
    
    author_x = (WIDTH - author_w) / 2
    author_y = line_y + 90
    
    draw.text((author_x, author_y), author_text, fill=COLOR_AUTHOR, font=font_author)

    # 7. Save as PNG
    output_dir = "/Users/eddyekofo/Documents/Theology/epub_conversion/books/Owen/covers"
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"v{vol_num}.png")
    img.save(filename, "PNG")
    print(f"Generated: {filename} (Font: {font_key}, Layout: {layout})")

if __name__ == "__main__":
    print("Generating Bespoke Art-Directed EPUB Covers (Colossal Numbers & Snell Cursive)...")
    for v in VOL_CONFIGS.keys():
        generate_cover(v)
    print("Complete. All 16 bespoke art-directed covers generated successfully.")
