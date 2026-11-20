#!/usr/bin/env python3
"""Render the news-image-20261119 entry poster (1024x1024).

One image summing up Thursday 19 November 2026: a banner naming the day,
one wide hero panel (Shenzhen trilateral) and a 2x3 grid of six panels
(Crimea Bridge, Anthropic IPO debut, Riyadh missile strike, Bangladesh
lockdown violence, Gaza ground operation, ICJ Rohingya verdict).

Flat editorial illustration, deep indigo base with amber accents, white
bold labels. Drawn with Pillow only. No network, no clock, no randomness:
running this script twice produces byte-identical PNG output.

Usage: python3 draw_image.py   (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ---- palette: deep indigo base, amber accents, white text ----
INK = (23, 16, 46)        # deep indigo, page background
INDIGO = (36, 27, 77)     # panel base
INDIGO2 = (46, 35, 112)   # lighter indigo
VIOLET = (74, 52, 143)    # mid violet
AMBER = (245, 166, 35)    # amber accent
AMBER2 = (255, 184, 71)   # light amber
CREAM = (242, 237, 255)   # off-white text
WHITE = (255, 255, 255)
DUSK = (58, 32, 86)       # dusk purple
DUSK_ORANGE = (214, 106, 48)
WATER = (14, 27, 51)      # dark water
FIRE = (255, 107, 53)
FIRE2 = (229, 87, 46)
SMOKE = (120, 116, 138)
STEEL = (94, 104, 138)
DARKBAND = (16, 11, 34)   # label band
GREEN = (55, 201, 120)
TAN = (196, 164, 120)
MAPLAND = (122, 106, 74)


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, max_w, start, minimum=12):
    """Largest font size at which text fits max_w, never below minimum."""
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def smoke(draw, cx, cy, scale, color=SMOKE):
    """A flat cluster of circles read as a smoke puff."""
    blobs = [(0, 0, 26), (-22, 10, 18), (22, 12, 19), (-8, -18, 17),
             (14, -16, 15), (-30, -6, 12), (30, -4, 12)]
    for dx, dy, r in blobs:
        rr = r * scale
        draw.ellipse([cx + dx * scale - rr, cy + dy * scale - rr,
                      cx + dx * scale + rr, cy + dy * scale + rr], fill=color)


def person(draw, cx, base_y, scale, suit, skin=(214, 178, 148)):
    """A faceless seated figure: head circle + shoulders, flat style."""
    hr = 13 * scale
    draw.ellipse([cx - hr, base_y - 62 * scale - hr,
                  cx + hr, base_y - 62 * scale + hr], fill=skin)
    draw.rounded_rectangle(
        [cx - 26 * scale, base_y - 46 * scale,
         cx + 26 * scale, base_y + 4 * scale],
        radius=int(12 * scale), fill=suit)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 34, 52))
    for i in range(0, 7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(255, 255, 255) if i % 2 == 1 else (178, 34, 52))
    draw.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(36, 54, 120))


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    s = h * 0.16
    draw.regular_polygon((x + w * 0.2, y + h * 0.28, s), 5, fill=AMBER2)


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def label_band(draw, x, y, w, h, label, sub):
    """Bottom band of a grid panel: bold label + small sub-label."""
    draw.rectangle([x, y, x + w, y + h], fill=DARKBAND)
    draw.rectangle([x, y, x + w, y + 4], fill=AMBER)
    pad = 12
    lf = fit(draw, label, BOLD, w - 2 * pad, 30)
    draw.text((x + pad, y + 10), label, font=lf, fill=WHITE)
    sf = fit(draw, sub, REG, w - 2 * pad, 20)
    draw.text((x + pad, y + h - 30), sub, font=sf, fill=CREAM)


# ---------------------------------------------------------------- banner
def draw_banner(draw):
    draw.rectangle([0, 0, W, 90], fill=INK)
    draw.rectangle([0, 86, W, 90], fill=AMBER)
    # small globe icon at left
    cx, cy, r = 46, 45, 27
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=AMBER2, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=None)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=AMBER2, width=3)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=AMBER2, width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=AMBER2, width=2)
    draw.ellipse([cx - 13, cy - r, cx + 13, cy + r], outline=AMBER2, width=2)
    f = fit(draw, "19 NOVEMBER 2026", BOLD, 860, 62)
    draw.text((92, 16), "19 NOVEMBER 2026", font=f, fill=WHITE)


# ---------------------------------------------------------------- hero: Shenzhen trilateral
def draw_hero(draw):
    x0, y0, x1, y1 = 0, 90, W, 410
    vgrad(draw, (x0, y0, x1, y1), (58, 38, 110), (26, 18, 58))
    # skyline silhouette along the bottom
    skyline = [(0, 330, 60, 410), (60, 300, 110, 410), (110, 340, 170, 410),
               (170, 285, 205, 410), (205, 320, 270, 410), (760, 310, 810, 410),
               (810, 285, 850, 410), (850, 330, 920, 410), (920, 300, 1024, 410)]
    for bx0, by0, bx1, by1 in skyline:
        draw.rectangle([bx0, by0, bx1, by1], fill=(18, 12, 40))
    # lit windows, deterministic pattern
    for i, (bx0, by0, bx1, by1) in enumerate(skyline):
        for wy in range(by0 + 12, by1 - 8, 18):
            for wx in range(bx0 + 8, bx1 - 8, 16):
                if (wx * 7 + wy * 13 + i) % 5 == 0:
                    draw.rectangle([wx, wy, wx + 5, wy + 7], fill=AMBER2)
    # floor band behind the table
    draw.rectangle([x0, 372, x1, y1], fill=(30, 22, 66))
    # three leaders seated at a long table
    draw.rectangle([250, 348, 774, 372], fill=(122, 82, 42))
    draw.rectangle([250, 348, 774, 356], fill=AMBER)
    person(draw, 350, 352, 1.0, (36, 54, 120))
    person(draw, 512, 352, 1.0, (150, 30, 30))
    person(draw, 674, 352, 1.0, (52, 52, 64))
    # three small flags on the table front
    flag_us(draw, 318, 372, 34, 22)
    flag_cn(draw, 495, 372, 34, 22)
    flag_ru(draw, 672, 372, 34, 22)
    # label top-left
    lf = fit(draw, "TRUMP \u00b7 XI \u00b7 PUTIN MEET", BOLD, 640, 44)
    draw.text((28, 108), "TRUMP \u00b7 XI \u00b7 PUTIN MEET", font=lf, fill=WHITE)
    draw.rectangle([28, 160, 28 + 210, 166], fill=AMBER)
    sf = fit(draw, "First trilateral \u2014 4-point pact, no Ukraine deal",
             REG, 640, 25)
    draw.text((28, 178), "First trilateral \u2014 4-point pact, no Ukraine deal",
              font=sf, fill=CREAM)


# ---------------------------------------------------------------- grid panels
def panel_bridge(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (58, 32, 86), (214, 106, 48))
    # dark water, lower third
    draw.rectangle([x, y + h * 0.66, x + w, y + h], fill=WATER)
    # bridge deck across
    dy = y + h * 0.52
    draw.rectangle([x, dy, x + w, dy + 12], fill=STEEL)
    # towers
    for tx in (x + 70, x + w - 90):
        draw.rectangle([tx, y + h * 0.28, tx + 12, dy], fill=STEEL)
        draw.rectangle([tx - 6, y + h * 0.28 - 10, tx + 18, y + h * 0.28],
                       fill=AMBER)
    # collapsed span: broken deck falling into the water
    draw.polygon([(x + 150, dy + 12), (x + 175, dy + 12), (x + 205, y + h * 0.78),
                  (x + 185, y + h * 0.80)], fill=STEEL)
    draw.polygon([(x + 205, y + h * 0.78), (x + 225, y + h * 0.76),
                  (x + 250, y + h * 0.86), (x + 232, y + h * 0.88)],
                 fill=STEEL)
    # smoke over the break
    smoke(draw, x + 190, y + h * 0.34, 0.7)
    # closed-road barrier, amber stripes
    bx, by = x + 24, y + h * 0.52 - 26
    draw.rectangle([bx, by, bx + 56, by + 10], fill=AMBER)
    draw.rectangle([bx, by + 10, bx + 56, by + 14], fill=(30, 30, 30))
    label_band(draw, x, y + h - 82, w, 82,
               "BRIDGE HIT AGAIN", "3rd attack in 3 days \u2014 rail halted")


def panel_anthropic(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 20, 62))
    # AI chip motif, top-right
    cx, cy, s = x + w - 78, y + 66, 44
    draw.rounded_rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                           radius=8, fill=INDIGO2, outline=AMBER, width=3)
    draw.rounded_rectangle([cx - 13, cy - 13, cx + 13, cy + 13],
                           radius=4, fill=AMBER)
    for k in range(3):
        off = -16 + k * 16
        draw.line([(cx + off, cy - s // 2 - 10), (cx + off, cy - s // 2)],
                  fill=AMBER, width=3)
        draw.line([(cx + off, cy + s // 2), (cx + off, cy + s // 2 + 10)],
                  fill=AMBER, width=3)
    # rising chart arrow
    pts = [(x + 22, y + 118), (x + 90, y + 106), (x + 150, y + 112),
           (x + 210, y + 82), (x + 268, y + 56)]
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    draw.polygon([(x + 268, y + 56), (x + 246, y + 52), (x + 262, y + 76)],
                 fill=GREEN)
    # big figure
    bf = fit(draw, "$81.3BN", BOLD, w - 40, 56)
    draw.text((x + 20, y + 142), "$81.3BN", font=bf, fill=AMBER2)
    label_band(draw, x, y + h - 82, w, 82,
               "BIGGEST IPO EVER", "Anthropic debuts on Nasdaq")


def panel_riyadh(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (12, 12, 34), (40, 26, 78))
    # stars
    for sx, sy in [(30, 22), (80, 48), (150, 18), (230, 40), (300, 24),
                   (55, 78), (280, 70)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=CREAM)
    # missile trail arcing across the sky
    trail = [(x + 18, y + 96), (x + 90, y + 62), (x + 170, y + 44),
             (x + 240, y + 46)]
    draw.line(trail, fill=AMBER2, width=4, joint="curve")
    draw.ellipse([x + 232, y + 38, x + 248, y + 54], fill=FIRE)
    draw.ellipse([x + 236, y + 42, x + 244, y + 50], fill=AMBER2)
    # district buildings
    for bx0, by0, bx1 in [(x + 8, y + 150, x + 58), (x + 66, y + 176, x + 112),
                          (x + 268, y + 168, x + 322)]:
        draw.rectangle([bx0, by0, bx1, y + h - 82], fill=(20, 16, 48))
        for wy in range(by0 + 10, y + h - 92, 16):
            for wx in range(bx0 + 6, bx1 - 6, 12):
                if (wx * 3 + wy * 5) % 4 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=AMBER2)
    # PIF Tower: tall glass skyscraper, centre
    tx0, tx1 = x + 138, x + 218
    draw.rectangle([tx0, y + 40, tx1, y + h - 82], fill=(52, 68, 128))
    draw.rectangle([tx0, y + 40, tx1, y + 40 + 6], fill=AMBER)
    for wy in range(y + 56, y + h - 92, 14):
        for wx in range(tx0 + 8, tx1 - 8, 14):
            if (wx + wy) % 3 == 0:
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=AMBER2)
    # damage: blown-out windows, bent facade near the top
    for wy in range(y + 62, y + 110, 12):
        draw.rectangle([tx0 + 10, wy, tx0 + 34, wy + 8], fill=(24, 20, 44))
    draw.polygon([(tx1 - 6, y + 96), (tx1 + 8, y + 108), (tx1 - 2, y + 118)],
                 fill=STEEL)
    # smoke and debris at the strike point
    smoke(draw, x + 178, y + 88, 0.55, color=(150, 146, 168))
    draw.polygon([(x + 150, y + 118), (x + 158, y + 132), (x + 144, y + 134)],
                 fill=FIRE)
    # warning lights on the side buildings' rooftops
    for wx, wy in [(x + 33, y + 150), (x + 295, y + 168)]:
        draw.ellipse([wx - 4, wy - 4, wx + 4, wy + 4], fill=(255, 60, 60))
    label_band(draw, x, y + h - 82, w, 82,
               "MISSILE HITS RIYADH TOWER",
               "Houthis claim strike \u2014 PIF tower hit")


def panel_bangladesh(draw, x, y, w, h):
    vgrad(draw, (x, y, x + w, y + h), (46, 30, 74), (24, 16, 48))
    # street
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=(18, 14, 38))
    # burning house, left
    hx, hy = x + 26, y + 92
    draw.rectangle([hx, hy, hx + 110, hy + 84], fill=(96, 58, 40))
    draw.polygon([(hx - 8, hy), (hx + 55, hy - 34), (hx + 118, hy)],
                 fill=(70, 40, 30))
    draw.rectangle([hx + 44, hy + 40, hx + 66, hy + 84], fill=(30, 20, 16))
    # flames above the roof
    flames = [(hx + 18, hy - 6), (hx + 34, hy - 34), (hx + 48, hy - 10),
              (hx + 62, hy - 40), (hx + 76, hy - 12), (hx + 92, hy - 30),
              (hx + 104, hy - 4)]
    draw.polygon(flames, fill=FIRE)
    draw.polygon([(hx + 34, hy - 4), (hx + 48, hy - 22), (hx + 62, hy - 6),
                  (hx + 76, hy - 20), (hx + 88, hy - 4)], fill=AMBER2)
    smoke(draw, hx + 55, hy - 46, 0.6)
    # crowd silhouettes with banners, right
    suits = [(196, 120, 40), (220, 200, 160), (150, 60, 60), (90, 140, 120)]
    for (px, ph), suit in zip(
            [(x + 180, 1.0), (x + 216, 0.92), (x + 250, 1.04),
             (x + 284, 0.95)], suits):
        person(draw, px, y + h - 82, ph, suit)
    # banner placards on sticks
    draw.rectangle([x + 168, y + 96, x + 236, y + 122], fill=AMBER)
    draw.line([(x + 202, y + 122), (x + 202, y + 168)], fill=AMBER2, width=3)
    draw.rectangle([x + 248, y + 88, x + 312, y + 112], fill=CREAM)
    draw.line([(x + 280, y + 112), (x + 280, y + 168)], fill=AMBER2, width=3)
    label_band(draw, x, y + h - 82, w, 82,
               "BANGLADESH BURNS",
               "Lockdown violence \u2014 Yunus home torched")


def panel_gaza(draw, x, y, w, h):
    # simplified map: tan land, darker border
    draw.rectangle([x, y, x + w, y + h], fill=(52, 44, 66))
    draw.rounded_rectangle([x + 14, y + 14, x + w - 14, y + h - 96],
                           radius=14, fill=MAPLAND)
    draw.rounded_rectangle([x + 14, y + 14, x + w - 14, y + h - 96],
                           radius=14, outline=AMBER, width=2)
    # the Yellow Line: dashed amber line across the map
    ly = y + 92
    for dx in range(0, w - 28, 24):
        draw.line([(x + 14 + dx, ly), (x + 14 + dx + 14, ly)],
                  fill=AMBER, width=4)
    # tanks crossing the line
    for tx, ty in [(x + 96, ly + 26), (x + 196, ly + 44)]:
        draw.rectangle([tx - 26, ty - 8, tx + 26, ty + 8], fill=(40, 42, 46))
        draw.rectangle([tx - 12, ty - 18, tx + 12, ty - 8], fill=(52, 54, 60))
        draw.line([(tx + 12, ty - 14), (tx + 34, ty - 18)],
                  fill=(40, 42, 46), width=4)
        draw.ellipse([tx - 20, ty + 8, tx - 10, ty + 18], fill=(30, 30, 34))
        draw.ellipse([tx + 10, ty + 8, tx + 20, ty + 18], fill=(30, 30, 34))
    # flood water at the bottom of the map + tents
    draw.rounded_rectangle([x + 14, y + h - 150, x + w - 14, y + h - 96],
                           radius=10, fill=(38, 90, 140))
    for tx in (x + 60, x + 140, x + 230):
        draw.polygon([(tx, y + h - 138), (tx + 22, y + h - 112),
                      (tx + 44, y + h - 138)], fill=CREAM)
    label_band(draw, x, y + h - 82, w, 82,
               "ISRAEL PUSHES PAST LINE", "Rare ground move in Gaza")


def panel_icj(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 34, 76))
    # court building: pediment + columns
    bx0, bx1 = x + 52, x + w - 52
    by = y + 66
    draw.polygon([(bx0 - 8, by), ((bx0 + bx1) // 2, by - 34), (bx1 + 8, by)],
                 fill=CREAM)
    draw.ellipse([((bx0 + bx1) // 2) - 8, by - 28, ((bx0 + bx1) // 2) + 8,
                  by - 12], fill=AMBER)
    for cx in range(bx0 + 16, bx1 - 8, 44):
        draw.rectangle([cx, by + 6, cx + 12, y + 158], fill=CREAM)
    draw.rectangle([bx0 - 8, y + 158, bx1 + 8, y + 168], fill=CREAM)
    # scales of justice, centre, in front of the steps
    sx, sy = x + w // 2, y + 118
    draw.line([(sx, sy - 34), (sx, sy + 44)], fill=AMBER, width=4)
    draw.line([(sx - 44, sy - 26), (sx + 44, sy - 26)], fill=AMBER, width=4)
    for ex in (sx - 44, sx + 44):
        draw.line([(ex, sy - 26), (ex, sy + 6)], fill=AMBER, width=3)
        draw.polygon([(ex - 18, sy + 6), (ex + 18, sy + 6), (ex, sy + 26)],
                     fill=AMBER2)
    draw.ellipse([sx - 6, sy - 40, sx + 6, sy - 28], fill=AMBER)
    label_band(draw, x, y + h - 82, w, 82,
               "MYANMAR GUILTY OF GENOCIDE",
               "ICJ rules 9\u20136 \u2014 historic first")


# ---------------------------------------------------------------- compose
def main():
    img = Image.new("RGB", (W, H), INK)
    draw = ImageDraw.Draw(img)

    draw_banner(draw)
    draw_hero(draw)

    grid_y = 422
    col_w, row_h, gap = 330, 292, 12
    panels = [panel_bridge, panel_anthropic, panel_riyadh,
              panel_bangladesh, panel_gaza, panel_icj]
    for i, fn in enumerate(panels):
        row, col = divmod(i, 3)
        px = 5 + col * (col_w + gap)
        py = grid_y + row * (row_h + gap)
        # panel frame
        draw.rounded_rectangle([px - 2, py - 2, px + col_w + 2, py + row_h + 2],
                               radius=8, outline=VIOLET, width=2)
        fn(draw, px, py, col_w, row_h)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
