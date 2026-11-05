global.window = {}; require(require('path').join(__dirname, '../../www/') + 'data-zones.js');
const THE = { "SWAMP": "the Swamp" };  /* said with "the" */
const L = window.ZONES.dam.labels, nice = s => THE[s] || (s === s.toUpperCase() ? s.toLowerCase().replace(/\b[a-z]/g, c => c.toUpperCase()).replace(/^The /, "the ") : s);
const AL = {
  "Power Generation Complex": ["power generation complex", "power generation", "power plant", "power station", "generation complex"],
  "Hydroponic Dome Complex": ["hydroponic dome complex", "hydroponic domes", "hydroponic dome", "hydroponics", "the domes", "dome complex"],
  "Control Tower": ["control tower"],
  "Research & Administration": ["research and administration", "research administration", "research building", "admin building", "administration building", "administration"],
  "Testing Annex": ["testing annex", "the annex", "annex"],
  "Electrical Substation": ["electrical substation", "substation", "sub station"],
  "Water Treatment Control": ["water treatment control", "water treatment plant", "water treatment building", "water treatment"],
  "Old Battleground": ["old battleground", "old battlefield", "battleground", "battlefield"],
  "Controlled Access Zone": ["controlled access zone", "controlled access", "access zone"],
  "Pale Apartments": ["pale apartments", "pale apartment"],
  "Ruby Residence": ["ruby residence", "ruby"],
  "Ben Welder's Sunroof": ["ben welder's sunroof", "ben welders sunroof", "welder's sunroof", "welders sunroof"],
  "South Swamp Outpost": ["south swamp outpost", "swamp outpost"],
  "Water Towers": ["water towers", "water tower"],
  "Scrap Yard": ["scrap yard", "scrapyard", "junkyard", "junk yard"],
  "Small Creek": ["small creek", "the creek", "creek"],
  "Floodgates": ["floodgates", "flood gates", "floodgate", "flood gate"],
  "Red Lakes Balcony": ["red lakes balcony", "red lake balcony", "the balcony", "balcony"],
  "Electrical Tower": ["electrical tower", "electric tower", "pylon"],
  "East Broken Bridge": ["east broken bridge", "east bridge", "broken bridge east"],
  "Pipeline Tower": ["pipeline tower", "pipeline"],
  "Pattern House": ["pattern house"],
  "West Broken Bridge": ["west broken bridge", "west bridge", "broken bridge west"],
  "Wreckage": ["wreckage", "the wreck"],
  "Formicai Outpost": ["formicai outpost", "formica outpost", "formicai"],
  "Raider Outpost East": ["raider outpost east", "east raider outpost", "raider outpost"],
  "Generator Hall": ["generator hall", "generator room"],
  "The Breach": ["the breach"],
  "Primary Facility": ["primary facility", "main facility"],
  "VICTORY RIDGE": ["victory ridge", "the ridge"],
  "SWAMP": ["the swamp", "swamp", "swamps", "marsh"],
  "THE DAM": ["the dam", "dam wall", "top of the dam"],
  "RED LAKES": ["red lakes", "red lake"],
  "FORMICAI HILLS": ["formicai hills", "formica hills"]
};
const out = { areas: [], regions: [] };
L.forEach(c => c.labels.forEach(l => { const a = AL[l.n]; if (!a) throw new Error("no aliases: " + l.n); (c.key === "region" ? out.regions : out.areas).push({ n: nice(l.n), y: l.y, x: l.x, al: a }); }));
const extra = Object.keys(AL).filter(k => !L.some(c => c.labels.some(l => l.n === k))); if (extra.length) throw new Error("unused: " + extra);
out.exits = { "Central Swamp Lift": ["central swamp lift", "swamp lift", "central swamp"], "North Complex Elevator": ["north complex elevator", "north complex lift", "north complex", "north elevator"], "Red Lakes Balcony Lift": ["red lakes balcony lift", "balcony lift", "red lakes lift"], "Water Treatment Elevator": ["water treatment elevator", "water treatment lift", "treatment elevator"] };
out.hatches = { "Spillway Hatch": ["spillway hatch", "spillway"], "Pump House Hatch": ["pump house hatch", "pumphouse hatch", "pump house", "pump hatch"], "Good Old Baron's Hatch": ["good old baron's hatch", "baron's hatch", "barons hatch", "baron hatch", "old baron"], "Sunroof Hatch": ["sunroof hatch"] };
const all = {}; [...out.areas, ...out.regions].forEach(p => p.al.forEach(a => (all[a] = all[a] || []).push(p.n))); Object.entries(out.exits).concat(Object.entries(out.hatches)).forEach(([n, al]) => al.forEach(a => (all[a] = all[a] || []).push(n)));
const dup = Object.entries(all).filter(([, v]) => v.length > 1); if (dup.length) throw new Error("dup " + JSON.stringify(dup));
const head = `/* Dam Battlegrounds named places, for working out where a player is. Names and positions: MetaForge's map labels
   (metaforge.app/arc-raiders, read 4 Nov 2026, used with their OK): 9 loot zones and 20 landmarks (areas, drawn on the map)
   and 5 regions (big areas: said, not drawn). Exits and hatches come from the markers in data-dam.js; these are just what
   players call them. al = what people say (5 Nov 2026). Positions are label positions, so roughly the middle of each place. */
`;
require('fs').writeFileSync(require('path').join(__dirname, '../../www/') + 'data-dam-places.js', head + "(window.MAP_PLACES = window.MAP_PLACES || {})[\"dam\"] = " + JSON.stringify(out) + ";\n");
console.log(out.areas.length, "areas", out.regions.length, "regions");
