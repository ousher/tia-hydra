#!/usr/bin/env python3
"""Generate HYDRA favicons (PNG set + ICO + apple-touch) in brand style."""
from PIL import Image, ImageDraw
import os

BG    = (5, 5, 7)
HYDRA = (196, 30, 30)
DARK  = (120, 16, 16)
EMBER = (255, 107, 53)

SS = 8          # supersample factor for crisp edges
BASE = 512
S = BASE * SS

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# rounded-square dark tile
pad = 0
rad = int(S * 0.18)
d.rounded_rectangle([pad, pad, S - 1 - pad, S - 1 - pad], radius=rad, fill=BG)

# top accent line (hydra -> ember)
bar_h = int(S * 0.045)
for x in range(pad, S - pad):
    t = (x - pad) / (S - 2 * pad)
    r = int(HYDRA[0] + (EMBER[0] - HYDRA[0]) * t)
    g = int(HYDRA[1] + (EMBER[1] - HYDRA[1]) * t)
    b = int(HYDRA[2] + (EMBER[2] - HYDRA[2]) * t)
    d.line([(x, pad + rad // 2), (x, pad + rad // 2 + bar_h)], fill=(r, g, b))

# centered "blade" diamond mark
cx, cy = S // 2, int(S * 0.56)
rw, rh = int(S * 0.27), int(S * 0.36)
d.polygon([(cx, cy - rh), (cx + rw, cy), (cx, cy + rh), (cx - rw, cy)], fill=HYDRA)
rw2, rh2 = int(rw * 0.5), int(rh * 0.5)
d.polygon([(cx, cy - rh2), (cx + rw2, cy), (cx, cy + rh2), (cx - rw2, cy)], fill=DARK)

# downscale master
master = img.resize((BASE, BASE), Image.LANCZOS)

root = "/home/user/tia-hydra"
master.save(os.path.join(root, "icon-512.png"))
master.resize((192, 192), Image.LANCZOS).save(os.path.join(root, "icon-192.png"))
master.resize((180, 180), Image.LANCZOS).save(os.path.join(root, "apple-touch-icon.png"))
master.resize((32, 32), Image.LANCZOS).save(os.path.join(root, "favicon-32.png"))
master.resize((16, 16), Image.LANCZOS).save(os.path.join(root, "favicon-16.png"))

# multi-size .ico
master.save(os.path.join(root, "favicon.ico"),
            sizes=[(16, 16), (32, 32), (48, 48)])

print("favicons generated")
