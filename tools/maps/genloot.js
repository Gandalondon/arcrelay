/* node genloot.js : www/data-loot.js from source/loot.json (6 Nov 2026).
   source/loot.json: MetaForge's map markers (nature, containers and a few location types) for all seven maps,
   read from each map page in Chrome. Kept: the types Relay can name (KEEP below), inside the map's bounds. */
const fs = require('fs'), path = require('path');
const KEEP = ["locker", "raider_cache", "arc_probe", "arc_courier", "candleberries", "car", "moss", "great-mullein", "ammo_crate", "suitcase", "field_crate", "weapon_case", "breachable_container", "bag", "mushroom", "agave", "utility_crate", "basket", "med_crate", "rocketeer_husk", "fertilizer", "supply_station", "fuel-cell", "security_breach", "frozen_raider_cache", "prickly-pear", "apricot", "combat_supplies", "lemons", "olive", "roots", "field_depot", "baron_husk"];
const W = path.join(__dirname, '../../www'); global.window = {};
for (const f of fs.readdirSync(W).filter(f => /^data-[a-z-]+\.js$/.test(f) && !/quests|places|loot/.test(f))) require(path.join(W, f));
const L = JSON.parse(fs.readFileSync(path.join(__dirname, 'source/loot.json'), 'utf8')), out = {};
let total = 0;
for (const M of Object.values(window).filter(v => v && v.rows && v.id)) {
  const ys = M.rows.map(r => r[3]), xs = M.rows.map(r => r[4]), pad = 300;
  const b = [Math.min(...ys) - pad, Math.max(...ys) + pad, Math.min(...xs) - pad, Math.max(...xs) + pad];
  const d = L[M.id], o = out[M.id] = {};
  for (const k of KEEP) { const p = (d.pts[k] || []), q = [];
    for (let i = 0; i < p.length; i += 3) if (p[i] >= b[0] && p[i] <= b[1] && p[i + 1] >= b[2] && p[i + 1] <= b[3]) q.push(p[i], p[i + 1], p[i + 2] & 1);
    if (q.length) { o[k] = q; total += q.length / 3; } }
}
fs.writeFileSync(path.join(W, 'data-loot.js'), '/* Loot spots on every map: MetaForge map markers (nature and containers), 6 Nov 2026. Built by tools/maps/genloot.js.\n   Per map, per type: flat [y, x, locked, ...]; locked 1 = behind a locked door. */\nwindow.MAP_LOOT = ' + JSON.stringify(out) + ';\n');
console.log(total + ' spots, ' + fs.statSync(path.join(W, 'data-loot.js')).size + ' bytes');
