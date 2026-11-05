"""Puts the earlier captures' map areas into the fresh captures (see recapture.js), then saves screen-*.webp for shot.html."""
import json
from PIL import Image
rects = json.load(open("rects.json"))
for k in ["3-exit", "4-find", "5-pin", "2-listening"]:
    new = Image.open("new-%s.png" % k).convert("RGB")
    r = rects.get("new-" + k)
    if r:
        old = Image.open("screen-%s.webp" % k).convert("RGB").resize(new.size)
        box = tuple(int(round(v * 2)) for v in (r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"]))
        new.paste(old.crop(box), box[:2])
    new.save("screen-%s.webp" % k, quality=92)
    print(k, new.size)

# the pin screen's "I'm here" pill sits on the map: take it from the fresh capture so it is in the current font
pin = Image.open("new-5-pin.png").convert("RGB"); comp = Image.open("screen-5-pin.webp").convert("RGB")
r = rects["new-5-pin"]; x0, y0, x1, y1 = [int(v * 2) for v in (r["x"], r["y"], r["x"] + r["w"], r["y"] + r["h"])]
px = pin.load(); amber = lambda c: c[0] > 220 and 150 < c[1] < 205 and c[2] < 100
rows = [y for y in range(y1 - int((y1 - y0) * .25), y1) if sum(amber(px[x, y]) for x in range(x0, x1)) > 120]  # the pill is the only wide amber run
pts = [(x, y) for y in rows for x in range(x0, x1) if amber(px[x, y])]
if pts:
    box = (min(p[0] for p in pts) - 3, min(p[1] for p in pts) - 3, max(p[0] for p in pts) + 4, max(p[1] for p in pts) + 4)
    comp.paste(pin.crop(box), box[:2]); comp.save("screen-5-pin.webp", quality=92); print("pill", box)

# "Maps by MetaForge" sits on the map too: take it from the fresh captures (its backing is near-opaque charcoal)
for k in ["3-exit", "4-find", "5-pin"]:
    c = rects.get("new-%s-credit" % k)
    if not c: continue
    fresh = Image.open("new-%s.png" % k).convert("RGB"); comp = Image.open("screen-%s.webp" % k).convert("RGB")
    box = tuple(int(round(v * 2)) for v in (c["x"], c["y"], c["x"] + c["w"], c["y"] + c["h"]))
    comp.paste(fresh.crop(box), box[:2]); comp.save("screen-%s.webp" % k, quality=92); print("credit", k, box)
