const fs = require('fs'), SP = require('path').join(__dirname, 'source');
global.window = {}; require(require('path').join(__dirname, '../../www/') + 'data-zones.js');
const THE = { OUTSKIRTS: "the Outskirts", "NEW DISTRICT": "the New District", "THE SPACEPORT": "the Spaceport", "HOTEL COMPLEX": "the Hotel Complex", HARBOR: "the Harbor", SWAMP: "the Swamp" };
const nice = s => THE[s] || (s === s.toUpperCase() ? s.toLowerCase().replace(/\b[a-z]/g, c => c.toUpperCase()).replace(/^The /, "the ") : s);
/* spoken short forms players use, on top of the full name */
const EXTRA = {
  "Space Travel": ["space travel building"], "Research": ["research building"], "Grandioso Apartments": ["grandioso"], "Market Ruins": ["the market"], "Dune's End": ["dunes end"],
  "Su Durante Warehouses": ["su durante"], "Gas Station": ["petrol station"], "Piazza Arbusto": ["arbusto"], "Santa Maria Houses": ["santa maria"], "Corso da Vinci": ["da vinci"],
  "Church Ruins": ["the church"], "Abandoned Highway Camp": ["highway camp"], "Parking Garage": ["multi storey", "multistorey"],
  "Departure Building": ["departures"], "Launch Towers": ["launch tower", "launch pad"], "Control Tower A6": ["control tower"], "Arrival Building": ["arrivals"], "Jiangsu Warehouse": ["jiangsu"],
  "Communications Tower": ["comms tower", "comm tower"], "Electrical Substation": ["substation"], "the Trench": ["trench"],
  "Cultural Archives": ["archives"], "Business Center": ["business centre"], "Medical Research": ["medical"], "Robotic Sandbox A": ["sandbox a"], "Robotic Sandbox B": ["sandbox b"], "Cafeteria": ["canteen"], "Communications": ["comms"],
  "Hotel Panorama Azzurro": ["the hotel", "hotel azzurro"], "Port Authority Building": ["port authority"], "Customs House": ["customs"], "Seabed": ["sea bed"], "Wavebreaker": ["wave breaker", "breakwater"],
  "Azzurro Beach": ["the beach"], "Poolside": ["the pool"], "Tennis Court": ["tennis courts"], "Dried Riverbed": ["riverbed", "river bed"], "Railyard": ["rail yard"], "the Harbor": ["harbour", "the harbour"],
  "Commissary Supermarket": ["supermarket", "commissary"], "Cielo Sereno Observatory": ["observatory", "cielo sereno"], "Fallen Emperor": ["the emperor"], "Deep-Space Telescope": ["deep space telescope", "telescope"],
  "Mulatierra Hill": ["mulatierra"], "Alberi Hills": ["alberi"]
};
const EXITS = { "Reckless Transceiver": ["reckless"], "Glacial Transceiver": ["glacial"], "Northern Transceiver": ["northern transceiver"], "Seed Vault Airshaft": ["seed vault shaft"], "Hiltop hatch": ["hilltop hatch"] };
const base = n => { const l = n.toLowerCase().replace(/’/g, "'"); const a = [l, l.replace(/^the /, ""), l.replace(/&/g, "and"), l.replace(/'/g, ""), l.replace(/-/g, " ")]; return a.filter(x => x.length >= 4); };
for (const id of ['buried-city', 'spaceport', 'stella-montis', 'riven-tides', 'pendola-pass']) {
  const L = window.ZONES[id].labels || [], rows = JSON.parse(fs.readFileSync(SP + '/rows-' + id + '.json'));
  const seen = new Set(), areas = [], regions = [];
  L.filter(c => c.key !== 'region').concat(L.filter(c => c.key === 'region')).forEach(c => c.labels.forEach(l => { const n = nice(l.n); const k = n.toLowerCase().replace(/^the /, ''); if (seen.has(k)) return; seen.add(k); (c.key === 'region' ? regions : areas).push({ n, y: l.y, x: l.x, al: [...base(n), ...(EXTRA[n] || [])] }); }));
  const ways = {}; rows.filter(r => r[1] === 'extraction' || r[1] === 'hatch').forEach(r => { ways[r[2]] = [...base(r[2]), ...(EXITS[r[2]] || [])]; });
  /* a short form two places share is ambiguous on this map: drop it (full names always stay) */
  const own = {}; [...areas, ...regions].forEach(p => p.al.forEach(a => (own[a] = own[a] || new Set()).add(p.n))); Object.entries(ways).forEach(([n, al]) => al.forEach(a => (own[a] = own[a] || new Set()).add(n)));
  const keep = (n, al) => [...new Set(al)].filter(a => own[a].size === 1 || a === n.toLowerCase());
  areas.forEach(p => p.al = keep(p.n, p.al)); regions.forEach(p => p.al = keep(p.n, p.al));
  const exits = {}, hatches = {}; rows.forEach(r => { if (r[1] === 'extraction') exits[r[2]] = keep(r[2], ways[r[2]]); if (r[1] === 'hatch') hatches[r[2]] = keep(r[2], ways[r[2]]); });
  const NAME = { 'buried-city': 'Buried City', spaceport: 'Spaceport', 'stella-montis': 'Stella Montis', 'riven-tides': 'Riven Tides', 'pendola-pass': 'Pendola Pass' }[id];
  const head = `/* ${NAME} named places, for working out where a player is. Names and positions: MetaForge's map labels (metaforge.app/arc-raiders,
   read 4 Nov 2026, used with their OK): loot zones and landmarks (areas, drawn) and regions (said, not drawn). Exits and hatches come
   from the markers in data-${id}.js; these are what players call them. al = what people say; a short form two places share is dropped (5 Nov 2026). */
`;
  fs.writeFileSync(require('path').join(__dirname, '../../www/') + 'data-' + id + '-places.js', head + `(window.MAP_PLACES = window.MAP_PLACES || {})["${id}"] = ` + JSON.stringify({ areas, regions, exits, hatches }) + ';\n');
  console.log(id, areas.length, 'areas', regions.length, 'regions', Object.keys(exits).length, 'exits', Object.keys(hatches).length, 'hatches');
}
