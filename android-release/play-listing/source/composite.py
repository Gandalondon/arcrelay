"""Saves the fresh captures from recapture.js as screen-*.webp (for shot.html and site/beta/screens/),
and the map areas of the exit and find screens as the app's onboarding images (www/onboard-*.webp, 684 x 962)."""
import json
from PIL import Image
rects = json.load(open("rects.json"))
for k in ["3-exit", "4-find", "5-pin", "2-listening"]:
    im = Image.open("new-%s.png" % k).convert("RGB")
    im.save("screen-%s.webp" % k, quality=92)
    print(k, im.size)
for k, out in [("3-exit", "onboard-exit"), ("4-find", "onboard-find")]:
    r = rects["new-" + k]
    box = tuple(int(round(v * 2)) for v in (r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
    Image.open("new-%s.png" % k).convert("RGB").crop(box).save("../../../www/%s.webp" % out, quality=90)
    print(out, box)
