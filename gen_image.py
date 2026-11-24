#!/usr/bin/env python3
"""Draw the front page of THE WORLD IN ONE DAY for Tuesday 24 November 2026.

A newspaper poster: masthead, the date in red, one lead story about the war
spilling into Poland, two mid stories (Nvidia, COP31) and three short items
(ECB, O'Hare, Norway). Every headline and standfirst comes from wire reports
of 24 November 2026. All pictures are flat shapes drawn here with Pillow, so
the file is deterministic: the same script always writes the same bytes.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (176, 30, 36)
BLUE = (31, 58, 95)
GREY = (90, 86, 78)
NIGHT = (18, 32, 64)
GREEN = (22, 120, 70)
GOLD = (198, 148, 28)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, max_w):
    """Largest font size at or below start that fits text on one line."""
    size = start
    while size > 10:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 2
    return font(path, 10)


def rule(d, y, x0, x1, width=2, colour=INK):
    d.line([(x0, y), (x1, y)], fill=colour, width=width)


def draw_jet(d, cx, cy, scale, colour):
    """A small fighter-jet silhouette, nose pointing right."""
    pts = [
        (cx - 52 * scale, cy),
        (cx - 20 * scale, cy - 8 * scale),
        (cx + 30 * scale, cy - 6 * scale),
        (cx + 52 * scale, cy),
        (cx + 30 * scale, cy + 6 * scale),
        (cx - 20 * scale, cy + 8 * scale),
    ]
    d.polygon(pts, fill=colour)
    d.polygon(
        [(cx - 8 * scale, cy - 6 * scale), (cx + 6 * scale, cy - 6 * scale),
         (cx + 2 * scale, cy - 20 * scale), (cx - 14 * scale, cy - 20 * scale)],
        fill=colour,
    )
    d.polygon(
        [(cx - 8 * scale, cy + 6 * scale), (cx + 6 * scale, cy + 6 * scale),
         (cx + 2 * scale, cy + 20 * scale), (cx - 14 * scale, cy + 20 * scale)],
        fill=colour,
    )


def draw_lead_scene(d, x0, y0, x1, y1):
    """Night sky over the border: radar rings, two jets, a dashed border."""
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
    # stars
    for sx, sy in [(40, 24), (120, 60), (210, 18), (300, 44), (370, 70),
                   (80, 110), (250, 120), (330, 130), (160, 140)]:
        d.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                  fill=(220, 220, 220))
    # radar rings
    cx, cy = x0 + 90, y0 + 105
    for r in (26, 48, 70):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 160, 110), width=2)
    d.line([(cx, cy), (cx + 52, cy - 44)], fill=(120, 220, 140), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(120, 220, 140))
    # dashed border line across the lower half
    by = y0 + 150
    for bx in range(x0 + 10, x1 - 10, 18):
        d.line([(bx, by), (bx + 10, by)], fill=(240, 240, 240), width=2)
    d.text((x0 + 12, by + 6), "POLAND", font=font(SANS_B, 15), fill=(240, 240, 240))
    # drone: small red dot with a warning ring
    dx, dy = x0 + 300, y0 + 46
    d.ellipse([dx - 12, dy - 12, dx + 12, dy + 12], outline=RED, width=2)
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED)
    # jets
    draw_jet(d, x0 + 300, y0 + 108, 0.85, (225, 225, 225))
    draw_jet(d, x0 + 360, y0 + 76, 0.6, (180, 180, 180))


def draw_chip(d, x0, y0, w, h):
    """A microchip: dark square, gold pins, green up-arrow."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 24, 24))
    for px in range(x0 + 14, x0 + w - 8, 22):
        d.line([(px, y0), (px, y0 - 8)], fill=GOLD, width=3)
        d.line([(px, y0 + h), (px, y0 + h + 8)], fill=GOLD, width=3)
    for py in range(y0 + 14, y0 + h - 8, 22):
        d.line([(x0, py), (x0 - 8, py)], fill=GOLD, width=3)
        d.line([(x0 + w, py), (x0 + w + 8, py)], fill=GOLD, width=3)
    d.rectangle([x0 + 26, y0 + 24, x0 + w - 26, y0 + h - 24],
                outline=GREEN, width=3)
    f_pct = font(SANS_B, 25)
    label = "+31%"
    lw = d.textlength(label, font=f_pct)
    d.text((x0 + (w - lw) / 2, y0 + (h - 34) / 2), label, font=f_pct,
           fill=(120, 230, 150))


def draw_globe(d, x0, y0, w, h):
    """A globe with a crack: climate talks failing."""
    cx, cy, r = x0 + w // 2, y0 + h // 2, min(w, h) // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180))
    d.ellipse([cx - r + 14, cy - r + 10, cx - r + 44, cy - r + 34], fill=GREEN)
    d.ellipse([cx + 6, cy + 2, cx + 34, cy + 26], fill=GREEN)
    d.ellipse([cx - 30, cy + 14, cx - 2, cy + 40], fill=GREEN)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.line([(cx - 8, cy - r + 4), (cx + 2, cy - 12), (cx - 4, cy + 6),
            (cx + 8, cy + 22), (cx - 2, cy + r - 4)], fill=RED, width=3)


def draw_bank(d, x0, y0, w, h):
    """A central bank: pediment and columns, sized to its box."""
    top = y0 + int(h * 0.42)
    base = y0 + h - 6
    d.polygon([(x0 + 6, top), (x0 + w // 2, y0 + 2), (x0 + w - 6, top)],
              fill=BLUE)
    d.rectangle([x0 + 4, top, x0 + w - 4, top + 5], fill=BLUE)
    for i in range(4):
        cx = x0 + 16 + i * (w - 32) // 3
        d.rectangle([cx - 5, top + 8, cx + 5, base - 6], fill=BLUE)
    d.rectangle([x0 + 2, base - 6, x0 + w - 2, base], fill=BLUE)


def draw_plane(d, x0, y0, w, h):
    """A small airliner in side view over runway dashes."""
    mid = y0 + h // 2 - 6
    d.polygon([(x0 + 4, mid), (x0 + w - 30, mid - 7),
               (x0 + w - 2, mid), (x0 + w - 30, mid + 7)],
              fill=BLUE)
    d.polygon([(x0 + 8, mid - 5), (x0 + 20, mid - 5),
               (x0 + 14, mid - 20), (x0 + 6, mid - 20)], fill=BLUE)
    d.polygon([(x0 + w // 2 - 2, mid + 5), (x0 + w // 2 + 12, mid + 5),
               (x0 + w // 2 + 4, mid + 18), (x0 + w // 2 - 8, mid + 18)],
              fill=BLUE)
    for rx in range(x0 + 4, x0 + w - 4, 16):
        d.line([(rx, y0 + h - 6), (rx + 8, y0 + h - 6)], fill=RED, width=3)


def draw_gavel(d, x0, y0, w, h):
    """A judge's gavel above an oil drop."""
    d.rectangle([x0 + 4, y0 + 6, x0 + w - 24, y0 + 20], fill=(90, 60, 30))
    d.line([(x0 + w // 2 - 4, y0 + 20), (x0 + w // 2 + 8, y0 + h - 14)],
           fill=(90, 60, 30), width=6)
    d.polygon([(x0 + w - 16, y0 + h - 26), (x0 + w - 6, y0 + h - 12),
               (x0 + w - 26, y0 + h - 12)], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    X1 = W - M

    # ---- Masthead ----
    f_name = fit(d, "THE WORLD IN ONE DAY", SERIF, 56, W - 2 * M)
    d.text((W // 2, 22), "THE WORLD IN ONE DAY", font=f_name, fill=INK,
           anchor="ma")
    rule(d, 92, M, X1, 3)
    rule(d, 97, M, X1, 1)
    f_date = font(SANS_B, 32)
    d.text((W // 2, 106), "TUESDAY, 24 NOVEMBER 2026", font=f_date, fill=RED,
           anchor="ma")
    f_tag = font(SERIF_R, 19)
    d.text((W // 2, 146), "One day. One page. The world.",
           font=f_tag, fill=GREY, anchor="ma")
    rule(d, 172, M, X1, 1)
    rule(d, 176, M, X1, 3)

    # ---- Lead story: Poland ----
    y = 190
    d.text((M, y), "EUROPE  •  WAR IN UKRAINE", font=font(SANS_B, 19), fill=RED)
    y = 214
    f_lead = fit(d, "WAR SPILLS INTO POLAND", SERIF, 64, W - 2 * M)
    d.text((M, y), "WAR SPILLS INTO POLAND", font=f_lead, fill=INK)
    y = 292
    draw_lead_scene(d, M, y, M + 430, y + 176)
    tx = M + 452
    tw = X1 - tx
    f_sub = font(SANS, 22)
    lead = ("A Russian drone crosses into Polish airspace overnight and "
            "Warsaw scrambles its jets. NATO calls an emergency meeting. "
            "Russian strikes kill 12 in the Kyiv region.")
    ly = y + 2
    for line in wrap(d, lead, f_sub, tw):
        d.text((tx, ly), line, font=f_sub, fill=INK)
        ly += 29
    rule(d, 486, M, X1, 2)

    # ---- Middle row: two stories ----
    y = 502
    cols = [
        (M, 470, "TECH  •  BUSINESS", "HUANG RETURNS TO NVIDIA",
         "Jensen Huang is back as chief executive after the board clears "
         "him. Nvidia shares jump 31% in a day. A US Senate hearing is "
         "set for 3 December.", draw_chip),
        (M + 494, 470, "CLIMATE  •  COP31", "CLIMATE TALKS COLLAPSE",
         "Negotiators in Turkey fail to agree on fossil fuels. Pacific "
         "nations call it the worst COP yet and go it alone.", draw_globe),
    ]
    for cx, cw, kicker, head, body, art in cols:
        d.text((cx, y), kicker, font=font(SANS_B, 17), fill=RED)
        hy = y + 24
        f_head = fit(d, head, SERIF, 34, cw)
        d.text((cx, hy), head, font=f_head, fill=INK)
        by = hy + 46
        art(d, cx, by, 118, 92)
        bx = cx + 134
        bw = cx + cw - bx
        f_body = font(SANS, 18)
        ly = by
        for line in wrap(d, body, f_body, bw):
            d.text((bx, ly), line, font=f_body, fill=INK)
            ly += 23
    rule(d, 736, M, X1, 2)

    # ---- Bottom row: three short items ----
    y = 748
    bw3 = 308
    items = [
        ("EUROPE  •  ECONOMY", "LAGARDE RESIGNS; ECB HUNT BEGINS",
         "Brussels hunts for a new central bank chief as Christine "
         "Lagarde steps down.", draw_bank),
        ("USA  •  TRAVEL", "O'HARE GROUND STOP",
         "Staffing shortage forces a brief ground stop at Chicago "
         "airport, 10:40–12:15, in the Thanksgiving rush.", draw_plane),
        ("EUROPE  •  ENERGY", "NORWAY VOIDS OIL LICENCES",
         "The top court rules climate-disputed oil licences invalid.",
         draw_gavel),
    ]
    for i, (kicker, head, body, art) in enumerate(items):
        cx = M + i * (bw3 + 20)
        d.text((cx, y), kicker, font=font(SANS_B, 15), fill=RED)
        art(d, cx, y + 22, 74, 44)
        hy = y + 74
        for line in wrap(d, head, font(SERIF, 25), bw3):
            f_head = fit(d, line, SERIF, 25, bw3)
            d.text((cx, hy), line, font=f_head, fill=INK)
            hy += 30
        f_body = font(SANS, 16)
        ly = hy + 4
        for line in wrap(d, body, f_body, bw3):
            d.text((cx, ly), line, font=f_body, fill=INK)
            ly += 20
    rule(d, 962, M, X1, 1)
    d.text((W // 2, 972),
           "All stories from Tuesday 24 November 2026 — compiled from wire reports",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
