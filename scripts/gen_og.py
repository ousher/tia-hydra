#!/usr/bin/env python3
"""Generate the HYDRA OG share banner (1200x630 PNG) in brand style."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 630

# HYDRA palette
BG       = (5, 5, 7)
SURFACE  = (10, 10, 18)
TEXT     = (235, 232, 227)
TEXT_DIM = (138, 133, 128)
TEXT_MUT = (85, 80, 72)
HYDRA    = (196, 30, 30)
EMBER    = (255, 107, 53)
GOLD     = (201, 162, 89)

img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img, "RGBA")

# --- radial red glow top-right ---
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
cx, cy = int(W * 0.72), int(H * 0.18)
maxr = 620
for r in range(maxr, 0, -4):
    a = int(46 * (1 - r / maxr) ** 2)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 30, 30, a))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")

# --- scanlines ---
for y in range(0, H, 3):
    draw.line([(0, y), (W, y)], fill=(196, 30, 30, 7))

# --- top accent bar (hydra -> ember gradient) ---
for x in range(W):
    t = x / W
    r = int(HYDRA[0] + (EMBER[0] - HYDRA[0]) * t)
    g = int(HYDRA[1] + (EMBER[1] - HYDRA[1]) * t)
    b = int(HYDRA[2] + (EMBER[2] - HYDRA[2]) * t)
    draw.line([(x, 0), (x, 5)], fill=(r, g, b))

# --- border frame ---
draw.rectangle([24, 24, W - 25, H - 25], outline=(26, 26, 42), width=1)

# --- fonts ---
def load(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

SANS = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]
SANS_R = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"]
MONO = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"]
MONO_R = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"]

f_logo   = load(MONO, 40)
f_mark   = load(MONO_R, 19)
f_h1     = load(SANS, 76)
f_sub    = load(SANS_R, 27)
f_strip  = load(MONO, 22)
f_strip_l= load(MONO_R, 15)

PAD = 70

def spaced(t, n=1):
    return (" " * n).join(list(t))

# --- logo row ---
# Drawn "blade" mark instead of emoji (no emoji font available)
mx, my = PAD + 16, 96
draw.polygon([(mx, my - 22), (mx + 16, my), (mx, my + 22), (mx - 16, my)],
             fill=HYDRA)
draw.polygon([(mx, my - 11), (mx + 8, my), (mx, my + 11), (mx - 8, my)],
             fill=(120, 16, 16))
draw.text((PAD + 56, 76), spaced("HYDRA"), font=f_logo, fill=HYDRA)

# eyebrow mark
draw.text((PAD, 150), "◢  TIA · HYDRA OSINT · CZ/EU", font=f_mark, fill=TEXT_MUT)

# --- headline ---
draw.text((PAD, 210), "Intelligence cuts", font=f_h1, fill=(255, 255, 255))
# second line: "that " white + "close cases." red
y2 = 300
seg1 = "that "
draw.text((PAD, y2), seg1, font=f_h1, fill=(255, 255, 255))
w1 = draw.textlength(seg1, font=f_h1)
# subtle glow behind accent
draw.text((PAD + w1, y2), "close cases.", font=f_h1, fill=(120, 16, 16))
draw.text((PAD + w1 - 1, y2 - 1), "close cases.", font=f_h1, fill=HYDRA)

# --- subline ---
draw.text((PAD, 410),
          "OSINT & Threat Intelligence — know what an attacker knows.",
          font=f_sub, fill=TEXT_DIM)

# --- bottom status strip ---
strip_y = 500
draw.line([(PAD, strip_y - 18), (W - PAD, strip_y - 18)], fill=(26, 26, 42), width=1)

items = [
    ("TIER 1 FROM", "CZK 12,000", HYDRA),
    ("DELIVERY", "2–15 days", TEXT),
    ("METHOD", "Passive only", TEXT),
    ("COMPLIANCE", "GDPR · NDA", TEXT),
]
col_w = (W - 2 * PAD) / len(items)
for i, (label, val, col) in enumerate(items):
    x = PAD + int(i * col_w)
    draw.text((x, strip_y), label, font=f_strip_l, fill=TEXT_MUT)
    draw.text((x, strip_y + 24), val, font=f_strip, fill=col)

img.save("/home/user/tia-hydra/og-image.png", "PNG", optimize=True)
print("saved og-image.png", img.size)
