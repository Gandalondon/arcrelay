"""Flattens the rendered art to 24-bit PNG (Play wants no alpha) under its final names."""
from PIL import Image
names = {"s1": "arcrelay-play-screenshot-1-evac", "s2": "arcrelay-play-screenshot-2-ask", "s3": "arcrelay-play-screenshot-3-find",
         "s4": "arcrelay-play-screenshot-4-where", "fg": "arcrelay-play-feature-graphic"}
for k, n in names.items():
    im = Image.open("raw-%s.png" % k).convert("RGB"); im.save("../%s.png" % n, optimize=True); print(n, im.size)
