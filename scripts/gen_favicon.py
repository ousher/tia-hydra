#!/usr/bin/env python3
"""Generate HYDRA favicons from the brand logo (logo.png at repo root).

Source of truth = /logo.png (the Architect-approved brand icon). Produces the
PNG set + multi-size ICO + apple-touch icon. Re-run after changing logo.png.
"""
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "logo.png")

master = Image.open(SRC).convert("RGBA")
# square-safe: if not square, center-crop to the shorter side
w, h = master.size
if w != h:
    s = min(w, h)
    master = master.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def save(size, name):
    master.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name))


save(512, "icon-512.png")
save(192, "icon-192.png")
save(180, "apple-touch-icon.png")
save(32, "favicon-32.png")
save(16, "favicon-16.png")

# multi-size .ico (16/32/48) derived from the master
master.save(os.path.join(ROOT, "favicon.ico"), format="ICO",
            sizes=[(16, 16), (32, 32), (48, 48)])

print(f"favicons generated from {SRC} (master {master.size})")
