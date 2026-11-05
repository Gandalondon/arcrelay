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
console.log(`${checked} maps with markers checked` + (fails.length ? "\n" + fails.map(f => "  ✗ " + f).join("\n") : ", all good"));
process.exit(fails.length ? 1 : 0);
