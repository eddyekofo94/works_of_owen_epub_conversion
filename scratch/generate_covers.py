#!/usr/bin/env python3
"""
Dynamic Cover Generator for the Works of John Owen.
Generates 16 high-quality, professional, and visually stunning book covers 
in the covers directory. This edition features:
- Complete protection against 'white area bleed': All patterns are drawn on a 
  clipped temporary canvas (1024x1200) and pasted onto the background, leaving 
  the lower white area (1200-1600) perfectly clean and solid white.
- Kept the exact patterns for the user's favorites: 4, 7, 8, 13, 16.
- Upgraded all other volumes with highly structured, clean, modern, and elegant 
  linear pinstripe/grid/frame/panel textures that match the favorite styles.
- Connective words rendered in Snell Roundhand cursive in White (#ffffff) with a 2px stroke,
  drawn with a refined 0.98x vertical height multiplier and tight 12px spacing to overlap 
  and weave ON TOP of the cyan letters using a 5px Teal halo for absolute legibility.
- Major words dynamically scaled *per line* using an upgraded high-contrast scale:
  the top bold word is always sleek and small, the connector delicate and smaller (135px), 
  and the bottom bold word colossal (up to 220px) to anchor the cover graphically.
- Extremely long bottom words (>= 10 letters, e.g. FELLOWSHIP) are capped at 118px to prevent margin bleed.
- The Volume Number made slightly smaller (340px) and shifted up (y=125) with a 5px deep 
  teal-black cast shadow (shade) and a 2px background separation shadow behind the 'v.' prefix.
- Extra bold Author Name anchored at the bottom in the white block using Montserrat ExtraBold.
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Define directory paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "covers"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Volume Subtitles with their precise mixed-typography splits.
VOLUME_TITLE_SPLITS = {
    1: [("the", True), ("GLORY", False), ("of", True), ("CHRIST", False)],
    2: [("COMMUNION", False), ("with", True), ("GOD", False)],
    3: [("the", True), ("HOLY", False), ("SPIRIT", False)],
    4: [("the", True), ("WORK", False), ("of the", True), ("SPIRIT", False)],
    5: [("FAITH", False), ("and its", True), ("EVIDENCES", False)],
    6: [("TEMPTATION", False), ("and", True), ("SIN", False)],
    7: [("SIN", False), ("and", True), ("GRACE", False)],
    8: [("SERMONS", False), ("to the", True), ("NATION", False)],
    9: [("SERMONS", False), ("to the", True), ("CHURCH", False)],
    10: [("the", True), ("DEATH", False), ("of", True), ("CHRIST", False)],
    11: [("CONTINUING", False), ("in the", True), ("FAITH", False)],
    12: [("the", True), ("GOSPEL", False), ("DEFENDED", False)],
    13: [("MINISTRY", False), ("and", True), ("FELLOWSHIP", False)],
    14: [("TRUE", False), ("and", True), ("FALSE", False), ("RELIGION", False)],
    15: [("CHURCH", False), ("PURITY", False), ("and", True), ("UNITY", False)],
    16: [("the", True), ("CHURCH", False), ("and the", True), ("BIBLE", False)]
}

# Colors
COLOR_TEAL = (0, 85, 85)       # #005555
COLOR_CYAN = (130, 214, 235)   # #82d6eb
COLOR_WHITE = (255, 255, 255)  # #ffffff
COLOR_MUTED_CYAN = (40, 115, 115) # #287373 - for ultra-subtle watermark look!
COLOR_SHADOW = (0, 45, 45)     # #002d2d - dark teal-black shadow for white numbers!

# Font Paths
FONT_MONTSERRAT_EXTRABOLD = "fonts/Montserrat/Montserrat-ExtraBold.ttf"
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ARIAL_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
FONT_SNELL = "/System/Library/Fonts/Supplemental/SnellRoundhand.ttc"

def draw_tracked_text(draw, text, position, font, color, tracking=3):
    """Draws centered text with custom tracking (letter spacing) in pixels."""
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

def draw_background_pattern(draw, vol_num, w, h, color):
    """
    Draws a unique, highly structured, clean vector pattern on the temporary teal canvas.
    - w = 1024, h = 1200 (strictly bounded to the teal block to prevent bleeding).
    """
    if vol_num == 1:
        # Clean Triple Border Frame (highly classical/structural)
        draw.rectangle([(40, 40), (w - 40, h - 40)], outline=color, width=2)
        draw.rectangle([(52, 52), (w - 52, h - 52)], outline=color, width=1)
        draw.rectangle([(64, 64), (w - 64, h - 64)], outline=color, width=1)
        
    elif vol_num == 2:
        # Horizontal Pinstripes (horizontal clean weave)
        for y in range(40, h, 40):
            draw.line([(0, y), (w, y)], fill=color, width=1)
            
    elif vol_num == 3:
        # Windowpane Grid (clean minimal grid)
        step_x, step_y = 128, 120
        for x in range(step_x, w, step_x):
            draw.line([(x, 0), (x, h)], fill=color, width=1)
        for y in range(step_y, h, step_y):
            draw.line([(0, y), (w, y)], fill=color, width=1)
            
    elif vol_num == 4:
        # Sinusoidal Waves (KEEP - User favorite)
        for y_start in range(50, h, 90):
            points = []
            for x in range(0, w + 20, 15):
                y = y_start + 30 * math.sin(x * 0.012)
                points.append((x, y))
            draw.line(points, fill=color, width=2)
            
    elif vol_num == 5:
        # Vertical Wave Pinstripes (vertical clean waves)
        for x_start in range(50, w, 90):
            points = []
            for y in range(0, h + 20, 15):
                x = x_start + 30 * math.sin(y * 0.012)
                points.append((x, y))
            draw.line(points, fill=color, width=2)
            
    elif vol_num == 6:
        # Triple-Line Pinstripe Columns
        step = 120
        for x in range(step, w, step):
            draw.line([(x - 8, 0), (x - 8, h)], fill=color, width=1)
            draw.line([(x, 0), (x, h)], fill=color, width=1)
            draw.line([(x + 8, 0), (x + 8, h)], fill=color, width=1)
            
    elif vol_num == 7:
        # Spaced Vertical Pinstripes (KEEP - User favorite)
        for x in range(40, w, 40):
            draw.line([(x, 0), (x, h)], fill=color, width=1)
            
    elif vol_num == 8:
        # Fine Cross-Hatch Grid (KEEP - User favorite)
        step = 60
        for offset in range(0, h, step):
            draw.line([(0, offset), (w, offset)], fill=color, width=1)
        for offset in range(0, w, step):
            draw.line([(offset, 0), (offset, h)], fill=color, width=1)
            
    elif vol_num == 9:
        # Wide Diamond Line Lattice (Minimalist diagonal grid)
        step = 160
        for offset in range(-800, h + 800, step):
            draw.line([(0, offset), (w, offset + w)], fill=color, width=1)
            draw.line([(0, offset), (w, offset - w)], fill=color, width=1)
            
    elif vol_num == 10:
        # Horizontal Triple-Line Pinstripes
        step = 120
        for y in range(step, h, step):
            draw.line([(0, y - 8), (w, y - 8)], fill=color, width=1)
            draw.line([(0, y), (w, y)], fill=color, width=1)
            draw.line([(0, y + 8), (w, y + 8)], fill=color, width=1)
            
    elif vol_num == 11:
        # Concentric Inset Rectangles (Classical panels)
        for offset in [40, 80, 120, 160]:
            draw.rectangle([(offset, offset), (w - offset, h - offset)], outline=color, width=1)
            
    elif vol_num == 12:
        # Grid of Inset Quadrant Panels
        cx, cy = w // 2, h // 2
        for qx_start, qx_end in [(40, cx - 10), (cx + 10, w - 40)]:
            for qy_start, qy_end in [(40, cy - 10), (cy + 10, h - 40)]:
                draw.rectangle([(qx_start, qy_start), (qx_end, qy_end)], outline=color, width=1)
                draw.rectangle([(qx_start + 10, qy_start + 10), (qx_end - 10, qy_end - 10)], outline=color, width=1)
                
    elif vol_num == 13:
        # Interwoven Double Pinstripes (KEEP - User favorite)
        step = 100
        for offset in range(50, w, step):
            draw.line([(offset - 8, 0), (offset - 8, h)], fill=color, width=1)
            draw.line([(offset + 8, 0), (offset + 8, h)], fill=color, width=1)
        for offset in range(50, h, step):
            draw.line([(0, offset - 8), (w, offset - 8)], fill=color, width=1)
            draw.line([(0, offset + 8), (w, offset + 8)], fill=color, width=1)
            
    elif vol_num == 14:
        # Alternating Thick and Thin Pinstripes
        for idx, x in enumerate(range(40, w, 40)):
            width = 2 if idx % 2 == 0 else 1
            draw.line([(x, 0), (x, h)], fill=color, width=width)
            
    elif vol_num == 15:
        # Clean Horizontal Chevron Inset Grid
        step = 120
        for y_start in range(60, h, step):
            draw.line([(0, y_start), (w // 2, y_start - 30)], fill=color, width=1)
            draw.line([(w // 2, y_start - 30), (w, y_start)], fill=color, width=1)
            draw.line([(0, y_start + 20), (w // 2, y_start - 10)], fill=color, width=1)
            draw.line([(w // 2, y_start - 10), (w, y_start + 20)], fill=color, width=1)
            
    elif vol_num == 16:
        # Classical Frame with double-notched corners (KEEP - User favorite)
        draw.rectangle([(45, 45), (w - 45, h - 45)], outline=color, width=2)
        draw.rectangle([(57, 57), (w - 57, h - 57)], outline=color, width=1)
        draw.rectangle([(32, 32), (68, 68)], outline=color, width=1)
        draw.rectangle([(w - 68, 32), (w - 32, 68)], outline=color, width=1)
        draw.rectangle([(32, h - 68), (68, h - 32)], outline=color, width=1)
        draw.rectangle([(w - 68, h - 68), (w - 32, h - 32)], outline=color, width=1)

def draw_volume_block(draw, vol_num, y_pos, font_cursive, font_number, w_canvas):
    """
    Draws Volume block:
    - The giant White Arial Black number is perfectly centered (no displacement).
    - A 5px deep teal-black shadow is drawn behind the giant white number.
    - A smaller, much thinner, muted slanted cursive 'v.' (Arial Italic) 
      is drawn overlapping the left edge with a 2px background teal separation shadow.
    """
    v_text = "v."
    num_text = str(vol_num)
    
    # Calculate widths and heights
    v_bbox = draw.textbbox((0, 0), v_text, font=font_cursive)
    w_v = v_bbox[2] - v_bbox[0]
    h_v = v_bbox[3] - v_bbox[1]
    
    num_bbox = draw.textbbox((0, 0), num_text, font=font_number)
    w_num = num_bbox[2] - num_bbox[0]
    h_num = num_bbox[3] - num_bbox[1]
    
    num_x = w_canvas // 2 - w_num // 2
    
    # 1. Draw 5px deep teal-black cast shadow (shade) behind the white number
    draw.text(
        (num_x + 5, y_pos + 5),
        num_text,
        fill=COLOR_SHADOW,
        font=font_number
    )
    
    # 2. Draw the main huge Volume number in solid White
    draw.text(
        (num_x, y_pos),
        num_text,
        fill=COLOR_WHITE,
        font=font_number
    )
    
    # Calculate position for slanted 'v.'
    overlap = 15
    v_x = num_x - w_v + overlap
    v_y = y_pos + h_num - h_v - 5
    
    # 3. Draw 2px background teal separation shadow behind the 'v.' prefix
    draw.text(
        (v_x + 2, v_y + 2),
        v_text,
        fill=COLOR_TEAL,
        font=font_cursive
    )
    
    # 4. Draw thin slanted "v." in muted Cyan-Teal Arial Italic
    draw.text(
        (v_x, v_y),
        v_text,
        fill=COLOR_MUTED_CYAN,
        font=font_cursive
    )

def generate_cover(vol_num, subtitle):
    """Generates a high-quality 1024x1600 EPUB cover for the given volume."""
    print(f"Generating Cover for Volume {vol_num}: {subtitle}...")
    
    # Create blank image with white background
    w, h = 1024, 1600
    img = Image.new("RGB", (w, h), COLOR_WHITE)
    draw = ImageDraw.Draw(img)
    
    # 1. Create a temporary image for the Teal block (size 1024x1200)
    teal_w, teal_h = 1024, 1200
    teal_img = Image.new("RGB", (teal_w, teal_h), COLOR_TEAL)
    teal_draw = ImageDraw.Draw(teal_img)
    
    # Draw pattern on temporary block
    draw_background_pattern(teal_draw, vol_num, teal_w, teal_h, COLOR_MUTED_CYAN)
    img.paste(teal_img, (0, 0))
    
    # 2. Draw Teal separation stripe
    draw.rectangle([(0, 1244), (w, 1260)], fill=COLOR_TEAL)
    
    # Load fonts
    font_series = ImageFont.truetype(FONT_MONTSERRAT_EXTRABOLD, 32)
    font_vol_num = ImageFont.truetype(FONT_ARIAL_BLACK, 340)
    font_vol_v = ImageFont.truetype(FONT_ARIAL_ITALIC, 85)
    font_author = ImageFont.truetype(FONT_MONTSERRAT_EXTRABOLD, 72)
    
    # Draw Series Title (shifted up to y=80)
    series_text = "THE WORKS OF JOHN OWEN"
    draw_tracked_text(draw, series_text, (w // 2, 80), font_series, COLOR_WHITE, tracking=15)
    
    # Draw Volume Number Block with shadows (shifted up to y=125)
    draw_volume_block(draw, vol_num, 125, font_vol_v, font_vol_num, w)
    
    # Calculate heights and layout for Book Title Block
    title_lines = VOLUME_TITLE_SPLITS[vol_num]
    spacing = 12 # tight vertical spacing
    lines_data = []
    
    # Identify the first and last non-cursive (bold) line indices
    first_bold_idx = -1
    last_bold_idx = -1
    for idx, (text, is_cursive) in enumerate(title_lines):
        if not is_cursive:
            if first_bold_idx == -1:
                first_bold_idx = idx
            last_bold_idx = idx
            
    for idx, (text, is_cursive) in enumerate(title_lines):
        if is_cursive:
            # Connective cursive connectors are 135px (delicate & compact)
            font = ImageFont.truetype(FONT_SNELL, 135)
            formatted_text = text.lower()
            
            bbox = draw.textbbox((0, 0), formatted_text, font=font)
            # Increased vertical multiplier slightly from 0.90 to 0.98 to clear the connector!
            line_h = int((bbox[3] - bbox[1]) * 0.98)
        else:
            # Base sizes dynamically scaled by character length
            word_len = len(text)
            if word_len <= 3:
                base_size = 155
            elif word_len <= 5:
                base_size = 135
            elif word_len <= 7:
                base_size = 120
            else:
                base_size = 100
                
            # Upgraded position-based weight scaling for absolute visual balance:
            if idx == first_bold_idx:
                # FIRST bold word is made sleeker and smaller:
                if word_len <= 3:
                    line_size = 125
                elif word_len <= 5:
                    line_size = 110     # e.g. "FAITH" in Vol 5 gets size 110px
                elif word_len <= 7:
                    line_size = 100     # e.g. "SERMONS" in Vol 8/9 gets size 100px
                else:
                    line_size = 85      # e.g. "TEMPTATION" in Vol 6, "MINISTRY" in Vol 13 gets size 85px!
            elif idx == last_bold_idx:
                # LAST bold word is made colossal and grounded at the bottom:
                if word_len <= 3:
                    line_size = 220     # e.g. "SIN", "GOD" get size 220px
                elif word_len <= 5:
                    line_size = 190     # e.g. "FAITH" in Vol 11 gets size 190px
                elif word_len <= 7:
                    line_size = 170     # e.g. "SPIRIT", "CHRIST" get size 170px
                elif word_len <= 9:
                    line_size = 135     # e.g. "EVIDENCES" in Vol 5 gets size 135px (fits beautifully)
                else:
                    # Capped at a compact 118px for extremely long bottom words (>= 10 letters, e.g. FELLOWSHIP)
                    # This prevents margin bleed while keeping it balanced!
                    line_size = 118     
            else:
                # Intermediary bold words (if any) use the standard base size
                line_size = base_size
                
            # Custom sizing overrides for Volume 6
            if vol_num == 6:
                if text.upper() == "TEMPTATION":
                    line_size = 85
                elif text.upper() == "SIN":
                    line_size = 220
                
            if vol_num == 6:
                font = ImageFont.truetype("fonts/Proxima_Nova/Proxima Nova Extrabold.ttf", line_size)
                tracking_val = 2
            else:
                font = ImageFont.truetype(FONT_MONTSERRAT_EXTRABOLD, line_size)
                tracking_val = 3
                
            formatted_text = text.upper()
            bbox = draw.textbbox((0, 0), formatted_text, font=font)
            line_h = bbox[3] - bbox[1]
            
        lines_data.append({
            'text': formatted_text,
            'is_cursive': is_cursive,
            'font': font,
            'height': line_h,
            'y_pos': 0,
            'tracking': tracking_val if not is_cursive else 0
        })
        
    total_height = sum(item['height'] for item in lines_data) + spacing * (len(lines_data) - 1)
    
    # Shift title block center up to y=810 for bottom clearance
    center_y = 810
    start_y = center_y - total_height // 2
    
    # Assign y coordinates
    curr_y = start_y
    for item in lines_data:
        item['y_pos'] = curr_y
        curr_y += item['height'] + spacing
        
    # --- Two-Pass Render for Cursive Overlapping Layering ---
    # Pass 1: Render all non-cursive bold text (Light Cyan)
    for item in lines_data:
        if not item['is_cursive']:
            draw_tracked_text(draw, item['text'], (w // 2, item['y_pos']), item['font'], COLOR_CYAN, tracking=item['tracking'])
            
    # Pass 2: Render all cursive connectors (White) ON TOP with a 5px Teal separator halo
    for item in lines_data:
        if item['is_cursive']:
            bbox = draw.textbbox((0, 0), item['text'], font=item['font'])
            w_text = bbox[2] - bbox[0]
            
            # 1. Background Masking (5px Teal Halo)
            draw.text(
                (w // 2 - w_text // 2, item['y_pos']), 
                item['text'], 
                fill=COLOR_TEAL, 
                font=item['font'],
                stroke_width=5.0,
                stroke_fill=COLOR_TEAL
            )
            
            # 2. Foreground Overlay
            draw.text(
                (w // 2 - w_text // 2, item['y_pos']), 
                item['text'], 
                fill=COLOR_WHITE, 
                font=item['font'],
                stroke_width=2.0,
                stroke_fill=COLOR_WHITE
            )
        
    # Draw Author name
    author_text = "JOHN OWEN"
    draw_tracked_text(draw, author_text, (w // 2, 1360), font_author, COLOR_TEAL, tracking=15)
    
    # Save the image
    output_path = OUTPUT_DIR / f"v{vol_num}.png"
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Saved: {output_path.name}")

if __name__ == "__main__":
    print("=== STARTING OWEN WORKS COVER GENERATION (CURSIVE CONNECTOR CLEARANCE ADJUSTED) ===")
    for vol, splits in VOLUME_TITLE_SPLITS.items():
        subtitle = " ".join(text for text, is_cursive in splits)
        generate_cover(vol, subtitle)
    print("=== COVER GENERATION COMPLETED SUCCESSFULLY ===")
