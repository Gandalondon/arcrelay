const fs = require('fs'), SP = require('path').join(__dirname, 'source');
const rowsOf = m => JSON.parse(fs.readFileSync(SP + '/rows-' + m + '.json')).filter(r => r[0] === 'q');
global.window = {}; require(require('path').join(__dirname, '../../www/') + 'data-dam.js');
const R = { dam: window.DAM.rows.filter(r => r[0] === 'q') }; const rowsIn = m => R[m] || (R[m] = rowsOf(m));
const MAPID = process.argv[2] || 'dam', FILES = process.argv.length > 3 ? process.argv.slice(3) : ['q1.json', 'q2.json', 'q3.json'];
const Q = [].concat(...FILES.map(f => JSON.parse(fs.readFileSync(SP + '/' + f))));
const host = u => u.replace(/^https?:\/\/(www\.)?/, '').split('/')[0];
const bad = [];
const out = Q.map(q => {
  const steps = q.steps.map(s => { const st = { t: s.t, go: s.go, show: s.show };
    if (s.pin) { const m = s.pm || MAPID; if (!(m === 'dam' ? R.dam : rowsIn(m)).some(r => r[1] === q.id && r[2] === s.pin)) bad.push(q.id + ': ' + s.pin + ' on ' + m); st.p = s.pin; if (s.pm) st.pm = s.pm; st.label = s.pin.replace(/^.* - /, '').replace(/^Step \d+: /, '').replace(/ \(.*\)$/, ''); }
    if (s.enemy) st.enemy = s.enemy; if (s.map) st.map = s.map; return st; });
  const txt = JSON.stringify(steps); if (/[—]/.test(txt)) bad.push(q.id + ': em dash');
  const src = [...new Set(q.sources.map(host))].join(', ');
  /* the full name always works; drop short forms that would fire by accident (inside other words, too common, or a wake word) */
  const BAN = new Set(['recon', 'unexpected', 'spotter quest', 'paving', 'harvest', 'source', 'enelica', 'monument', 'league', 'echoes', 'divided', 'last entry', 'cold storage', 'movie night', 'with a view', 'lidar quest']);
  const full = q.name.toLowerCase().replace(/’/g, "'"), al = [...new Set([full, full.replace(/^(a|the) /, ''), ...q.aliases.map(a => a.toLowerCase())])].filter(a => a.length >= 5 && !BAN.has(a) || a === full);
  return { id: q.id, n: q.name, al, who: q.who, note: 'Steps checked against ' + src + ' (5 Nov 2026)' + (q.agree ? '' : '; not fully settled: ' + q.notes) + '. Positions: MetaForge.', steps };
});
if (bad.length) { console.log('BAD', bad); process.exit(1); }
const head = `/* Dam Battlegrounds quests (and the Dam step of Taking Stock), 23 in all. Steps in the game's order, each quest checked
   against at least two guides (named in note), with "go" and "show" in our own words. Pins: MetaForge's quest markers in
   data-dam.js, matched by quest (id) and step name (p). Steps on other maps say so and have no pin (5 Nov 2026). */
`;
const NAME = { dam: 'Dam Battlegrounds', 'buried-city': 'Buried City', spaceport: 'Spaceport', 'stella-montis': 'Stella Montis', 'riven-tides': 'Riven Tides', 'pendola-pass': 'Pendola Pass' }[MAPID];
const head2 = MAPID === 'dam' ? head : `/* ${NAME} quests, ${out.length} in all. Steps in the game's order, each quest checked against at least two guides (named in note;
   "not fully settled" says what's open), with "go" and "show" in our own words. Pins: MetaForge's quest markers in data-${MAPID}.js,
   matched by quest (id) and step name (p); pm: a pin on another map. Steps on other maps say so (5 Nov 2026). */
`;
fs.writeFileSync(require('path').join(__dirname, '../../www/') + 'data-' + MAPID + '-quests.js', head2 + (MAPID === 'dam' ? 'window.DAM_QUESTS = ' : '(window.MAP_QUESTS = window.MAP_QUESTS || {})["' + MAPID + '"] = ') + JSON.stringify(out, null, 0).replace(/\},\{"id"/g, '},\n{"id"') + ';\n');
console.log(out.length, 'quests,', out.reduce((s, q) => s + q.steps.length, 0), 'steps,', out.reduce((s, q) => s + q.steps.filter(x => x.p).length, 0), 'pinned');
