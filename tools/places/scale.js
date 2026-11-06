/* Fits each map's scale (map units per metre) from published place-to-place distances (6 Nov 2026).
   Input: tools/places/dist/<map>.json  {"map","source_pages":[...],"pairs":[[from,to,metres,"place"|"return"]]}
   Positions: our own map data (MetaForge labels for places, MetaForge markers for exits and hatches).
   Each pair gives units/metre = map distance / published metres; the scale is the median, and the spread says
   how far to trust it. Pairs under 60 m are skipped: label positions are the middle of a place, so short
   distances are mostly label offset.
   node tools/places/scale.js */
const fs = require("fs"), path = require("path");
global.window = {};
const W = path.join(__dirname, "../../www");
for (const f of fs.readdirSync(W).filter(f => /^data-.*\.js$/.test(f))) require(path.join(W, f));
const MAPS = Object.values(window).filter(v => v && v.rows && v.id);
const key = s => s.toLowerCase().replace(/^the /, "").replace(/['’&.]/g, "").replace(/\band\b/g, "").replace(/[^a-z0-9]+/g, " ").trim();
const DIR = path.join(__dirname, "dist"), out = {};
for (const f of fs.readdirSync(DIR).filter(f => f.endsWith(".json") && f !== "scales.json")) {
  const D = JSON.parse(fs.readFileSync(path.join(DIR, f), "utf8")), id = D.map;
  const M = MAPS.find(m => m.id === id), PL = (window.MAP_PLACES || {})[id] || {};
  if (!M) { console.log(id + ": no map data"); continue; }
  const pos = {};
  for (const a of PL.areas || []) pos[key(a.n)] = a;  /* not regions: a big area's label is only a rough centre */
  for (const r of M.rows) { const n = r[2], y = r[3], x = r[4]; if (r[1] === "extraction" || r[1] === "hatch") pos[key(n)] = { n, y, x }; }
  const r = [], miss = new Set();
  for (const [a, b, m] of D.pairs || []) {
    const A = pos[key(a)], B = pos[key(b)];
    if (!A) miss.add(a); if (!B) miss.add(b);
    if (!A || !B || m < 60) continue;
    r.push(Math.hypot(A.y - B.y, A.x - B.x) / m);
  }
  if (r.length < 6) { console.log(`${id}: ${r.length} usable pairs, not enough${D.note ? " (" + D.note + ")" : ""}`); continue; }
  r.sort((a, b) => a - b);
  const q = p => r[Math.floor(p * (r.length - 1))], med = q(.5), spread = (q(.75) - q(.25)) / med;
  out[id] = { unitsPerMetre: +med.toFixed(4), pairs: r.length, iqrPct: Math.round(spread * 100) };
  console.log(`${id.padEnd(14)} ${med.toFixed(4)} units/m  from ${r.length} pairs, middle half within ±${Math.round(spread * 50)}%` + (miss.size ? `  (unmatched: ${[...miss].slice(0, 8).join(", ")})` : ""));
}
fs.writeFileSync(path.join(DIR, "scales.json"), JSON.stringify(out, null, 1));
