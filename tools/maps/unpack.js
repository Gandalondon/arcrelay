// node unpack.js <map-id> : rebuild rows from raw-<id>.txt, print count and checksum
const fs = require('fs'), SP = require('path').join(__dirname, 'source'), id = process.argv[2];
const rows = [];
for (const l of fs.readFileSync(SP + '/raw-' + id + '.txt', 'utf8').trim().split('\n')) {
  if (l.startsWith('A|')) { const [, sub, list] = l.split('|'); list.split(',').forEach(p => { const [i, y, x] = p.split('.').map(Number); rows[i] = ['a', sub, '', y, x]; }); }
  else { const [i, k, sub, n, y, x] = l.split('|'); rows[+i] = [k, sub, n, +y, +x]; }
}
const holes = []; for (let i = 0; i < rows.length; i++) if (!rows[i]) holes.push(i);
console.log(id, rows.length, rows.reduce((a, r, i) => a + (r ? r[3] * (i + 1) + r[4] : 0), 0), holes.length ? 'HOLES ' + holes : 'complete');
fs.writeFileSync(SP + '/rows-' + id + '.json', JSON.stringify(rows));
