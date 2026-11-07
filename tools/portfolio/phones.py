"""Four app screens in Tony's Pixel 8 frame (exported from Figma at 2x), laid out like the relay_app frame.
Run from the repo root: python3 tools/portfolio/phones.py
Writes marketing/portfolio/relay_app.png at 1x (3560 x 1717, transparent background)."""
from PIL import Image, ImageChops
import os
D = os.path.join(os.path.dirname(__file__), "../../marketing/portfolio")
SCREENS = ["relay-1-listening.png", "relay-2-find.png", "relay-3-exit.png", "relay-4-loot.png"]  # from tools/captures (7 Nov)
# From the Figma file (1x): phone 837.457 x 1714.983, screen at 44.077, 42.073, size 751.307 x 1626.830; phones at these x.
PX = [0, 907.514, 1815.029, 2722.543]
S = 2  # work at 2x, then halve
frame = Image.open(os.path.join(D, "pixel8-frame@2x.png")).convert("RGBA")
# Screen mask from the frame itself: bezel is (46,48,54), screen is (26,26,26); edge pixels blend between them.
r = frame.getchannel("R")
mask = r.point(lambda v: max(0, min(255, round((46 - v) / 20 * 255))))
mask = ImageChops.multiply(mask, frame.getchannel("A"))
sx, sy, sw, sh = [round(v * S) for v in (44.077, 42.073, 751.307, 1626.830)]
canvas = Image.new("RGBA", (round(3560 * S), round(1717 * S)), (0, 0, 0, 0))
for x, f in zip(PX, SCREENS):
    phone = frame.copy()
    shot = Image.open(os.path.join(D, f)).convert("RGBA").resize((sw, sh), Image.LANCZOS)
    layer = Image.new("RGBA", phone.size, (0, 0, 0, 0)); layer.paste(shot, (sx, sy))
    phone.paste(layer, (0, 0), ImageChops.multiply(mask, layer.getchannel("A")))
    canvas.alpha_composite(phone, (round(x * S), 0))
out = canvas.resize((3560, 1717), Image.LANCZOS)
out.save(os.path.join(D, "relay_app.png"), optimize=True)
print(out.size)
