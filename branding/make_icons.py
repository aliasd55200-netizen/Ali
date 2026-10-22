"""Generate launcher icons for the Shahin rebrand from branding/logo.webp.

Crops the baked rounded corners off the source artwork, samples its dark
background colour, and writes legacy + round + adaptive-foreground icons
for every density bucket.
"""
import os

from PIL import Image

src = Image.open("branding/logo.webp").convert("RGB")
w, h = src.size
box = (int(w * 0.055), int(h * 0.055), int(w * 0.945), int(h * 0.945))
art = src.crop(box)
bg = art.getpixel((15, 15))

DENSITIES = {
    "mdpi": (48, 108),
    "hdpi": (72, 162),
    "xhdpi": (96, 216),
    "xxhdpi": (144, 324),
    "xxxhdpi": (192, 432),
}

for name, (legacy, fg) in DENSITIES.items():
    d = os.path.join("app/src/main/res", f"mipmap-{name}")
    art.resize((legacy, legacy), Image.LANCZOS).save(
        os.path.join(d, "ic_launcher.webp"), "WEBP", quality=92
    )
    art.resize((legacy, legacy), Image.LANCZOS).save(
        os.path.join(d, "ic_launcher_round.webp"), "WEBP", quality=92
    )
    canvas = Image.new("RGB", (fg, fg), bg)
    inner = int(fg * 0.90)
    a = art.resize((inner, inner), Image.LANCZOS)
    off = (fg - inner) // 2
    canvas.paste(a, (off, off))
    canvas.save(os.path.join(d, "ic_launcher_foreground.webp"), "WEBP", quality=92)

print("icons generated, bg =", bg)
