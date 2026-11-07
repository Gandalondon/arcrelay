"""Two app screens in Tony's Pixel 8 frame, centred on the same canvas as relay_app.png (3560 x 1717) with the same gap.
Run from the repo root: python3 tools/portfolio/phones2.py   -> marketing/portfolio/relay_pair-*.jpg (white, for the portfolio)"""
from PIL import Image, ImageChops
import os
D = os.path.join(os.path.dirname(__file__), "../../marketing/portfolio")
O = os.path.join(os.path.dirname(__file__), "../../tools/captures/out")
PAIRS = {"relay_pair-heard": ["listening", "exit"], "relay_pair-find": ["cache", "moss"]}
S, W, H, PW, STEP = 2, 3560, 1717, 837.457, 907.514   # same phone width and spacing as phones.py
frame = Image.open(os.path.join(D, "pixel8-frame@2x.png")).convert("RGBA")
r = frame.getchannel("R")
mask = ImageChops.multiply(r.point(lambda v: max(0, min(255, round((46 - v) / 20 * 255)))), frame.getchannel("A"))
sx, sy, sw, sh = [round(v * S) for v in (44.077, 42.073, 751.307, 1626.830)]
for name, shots in PAIRS.items():
    canvas = Image.new("RGBA", (W * S, H * S), (255, 255, 255, 255))
    x0 = (W - (STEP + PW)) / 2
    for i, s in enumerate(shots):
        phone = frame.copy()
        shot = Image.open(os.path.join(O, s + ".png")).convert("RGBA").resize((sw, sh), Image.LANCZOS)
        layer = Image.new("RGBA", phone.size, (0, 0, 0, 0)); layer.paste(shot, (sx, sy))
        phone.paste(layer, (0, 0), ImageChops.multiply(mask, layer.getchannel("A")))
        canvas.alpha_composite(phone, (round((x0 + i * STEP) * S), 0))
    canvas.resize((W, H), Image.LANCZOS).convert("RGB").save(os.path.join(D, name + ".jpg"), quality=90)
    print(name)
