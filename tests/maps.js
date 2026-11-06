/* Checks each map's marker data: every row is well formed and inside the map's bounds, and maps with markers have exits.
   node tests/maps.js   (no browser needed) */
const path = require("path");
global.window = {};
const MAPS = { "blue-gate": "BLUE_GATE", "dam": "DAM", "buried-city": "BURIED_CITY", "spaceport": "SPACEPORT", "stella-montis": "STELLA_MONTIS", "riven-tides": "RIVEN_TIDES", "pendola-pass": "PENDOLA_PASS" };
const fails = []; let checked = 0;
for (const [file, key] of Object.entries(MAPS)) {
  try { require(path.join(__dirname, "../www/data-" + file.replace("blue-gate", "bluegate") + ".js")); } catch (e) { fails.push(file + ": data file missing"); continue; }
  const M = Object.values(window).find(m => m && m.id === file);
  if (!M) { fails.push(file + ": no map object (" + key + ")"); continue; }
  const rows = M.rows || [];
  if (!rows.length) continue;  /* markers not pulled yet */
  checked++;
  const [[y0, x0], [y1, x1]] = M.bounds;
  rows.forEach((r, i) => {
    if (r.length !== 5 || !"laq".includes(r[0]) || typeof r[3] !== "number" || typeof r[4] !== "number") fails.push(`${file} row ${i}: badly formed ${JSON.stringify(r)}`);
    else if (r[3] < y0 || r[3] > y1 || r[4] < x0 || r[4] > x1) fails.push(`${file} row ${i}: outside bounds ${JSON.stringify(r)}`);
  });
  const exits = rows.filter(r => r[1] === "extraction").length, hatches = rows.filter(r => r[1] === "hatch").length;
  if (!exits) fails.push(file + ": no exits");
  console.log(`${M.name}: ${rows.length} markers, ${exits} exits, ${hatches} hatches`);
}
/* every quest pin points at a real marker on its map (5 Nov) */
for (const id of ["dam", "buried-city", "spaceport", "stella-montis", "riven-tides", "pendola-pass"]) {
  try { require(path.join(__dirname, "../www/data-" + id + "-quests.js")); } catch (e) { fails.push(id + ": no quest file"); continue; }
  const M = Object.values(window).find(m => m && m.id === id), Q = id === "dam" ? window.DAM_QUESTS || [] : (window.MAP_QUESTS || {})[id] || [];
  let pins = 0; Q.forEach(q => q.steps.forEach(st => { if (!st.p) return; pins++; const PM = st.pm ? Object.values(window).find(m => m && m.id === st.pm) : M;  /* pm: a pin on another map */
    if (!PM || !PM.rows.some(r => r[0] === "q" && r[1] === q.id && r[2] === st.p)) fails.push(`${id} quest ${q.n}: no marker "${st.p}"` + (st.pm ? " on " + st.pm : "")); }));
  console.log(`${M.name}: ${Q.length} quests, ${pins} pinned steps`);
}
/* no two quests share a spoken name */
{ const all = [...(window.DAM_QUESTS || []), ...[].concat(...Object.values(window.MAP_QUESTS || {}))], by = {};
  all.forEach(q => q.al.forEach(a => (by[a] = by[a] || new Set()).add(q.n)));
  Object.entries(by).filter(([, v]) => v.size > 1).forEach(([k, v]) => fails.push(`quest name "${k}" means ${[...v].join(" and ")}`)); }
/* every map but Blue Gate has a fitted scale, and it still matches the published distances it came from (6 Nov) */
{ const fs = require("fs"), src = fs.readFileSync(path.join(__dirname, "../www/index.html"), "utf8");
  const U = JSON.parse(src.match(/const UNITS_PER_METRE = (\{[^}]*\})/)[1]);
  const key = s => s.toLowerCase().replace(/^the /, "").replace(/['’&.]/g, "").replace(/\band\b/g, "").replace(/[^a-z0-9]+/g, " ").trim();
  for (const id of ["dam", "buried-city", "spaceport", "stella-montis", "riven-tides", "pendola-pass"]) {
    require(path.join(__dirname, "../www/data-" + id + "-places.js"));
    const M = Object.values(window).find(m => m && m.id === id), PL = window.MAP_PLACES[id], pos = {};
    if (!U[id]) { fails.push(id + ": no scale, so no distances"); continue; }
    PL.areas.forEach(a => pos[key(a.n)] = a); M.rows.forEach(r => { if (r[1] === "extraction" || r[1] === "hatch") pos[key(r[2])] = { y: r[3], x: r[4] }; });
    const errs = JSON.parse(fs.readFileSync(path.join(__dirname, "../tools/places/dist/" + id + ".json"), "utf8")).pairs
      .filter(([a, b, m]) => pos[key(a)] && pos[key(b)] && m >= 60).map(([a, b, m]) => Math.abs(Math.hypot(pos[key(a)].y - pos[key(b)].y, pos[key(a)].x - pos[key(b)].x) / U[id] - m) / m).sort((a, b) => a - b);
    const med = errs[errs.length >> 1];
    if (med > 0.15) fails.push(`${id}: distances off by ${Math.round(med * 100)}% typically`);
    console.log(`${M.name}: distances within ${Math.round(med * 100)}% typically, ${errs.length} published pairs`);
  } }
console.log(`${checked} maps with markers checked` + (fails.length ? "\n" + fails.map(f => "  ✗ " + f).join("\n") : ", all good"));
process.exit(fails.length ? 1 : 0);
