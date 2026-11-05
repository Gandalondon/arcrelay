// Re-captures the four listing screens from the current app (www/index.html), so their text is in the app's current font.
// The workspace can't load MetaForge's map tiles, so each map area is taken from the earlier capture of the same screen
// (pixel-4nov/screen-*.webp, 780 x 1688, taken on the Pixel): the answer text, buttons, credit and dock come from the live app.
// Run from this folder:  cp pixel-4nov/screen-*.webp . && node recapture.js && python3 composite.py && node render.js && python3 finish.py
// Then copy the four screen-*.webp to site/beta/screens/ so the site matches.
const path = require('path');
const { chromium } = require('playwright');
const APP = 'file://' + path.resolve(__dirname, '../../../www/index.html');
const SHOTS = [
  { out: 'new-3-exit', place: 'Village', ask: "where's the nearest exit", word: 'Forest Airshaft, south-east.' },
  { out: 'new-4-find', place: 'Village', ask: "where's the nearest rocketeer", word: 'Nearest Rocketeer: west.' },
  { out: 'new-5-pin', pin: true },
  { out: 'new-2-listening', listen: true },
];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, timezoneId: 'Europe/London' });
  const rects = {};
  for (const s of SHOTS) {
    const p = await ctx.newPage();
    await p.route(/^https?:/, r => r.abort());
    await p.goto(APP); await p.waitForTimeout(1500);
    await p.evaluate(() => { const el = document.getElementById('sppack'); if (el) el.hidden = true; });
    await p.evaluate(async (s) => {
      speak = (t, cb) => { if (cb) setTimeout(cb, 0); };  // no audio, no follow-up listen
      listen = () => {};
      S = Object.assign({}, EMPTY); S.voiceV = 2;
      if (s.place) { const pl = PLACES.find(p => p.n === s.place); S.place = { n: pl.n, y: pl.y, x: pl.x }; S.placeAt = Date.now(); S.raidAt = Date.now(); }
      if (s.ask) await handle(s.ask);
      if (s.pin) await handle('where am i');
      if (s.listen) { micOn(true); renderListening(); }
    }, s);
    await p.waitForTimeout(900);
    await p.evaluate((s) => {
      document.body.classList.remove('speaking');
      if (s.word) document.getElementById('word').textContent = s.word;
      if (s.pin) { const k = document.getElementById('pinok'); if (k) k.hidden = false; const h = document.getElementById('maphint'); if (h) h.hidden = true; }  // the confirm pill, as after a tap  // the same answer as the earlier capture, so the map matches
      const el = document.getElementById('sppack'); if (el) el.hidden = true;
    }, s);
    await p.waitForTimeout(300);
    rects[s.out] = await p.evaluate(() => { const m = document.querySelector('.mapwrap'); if (!m) return null; const r = m.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
    rects[s.out + '-credit'] = await p.evaluate(() => { const m = document.querySelector('.leaflet-control-attribution'); if (!m) return null; const r = m.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; });
    await p.screenshot({ path: s.out + '.png' });
    console.log(s.out, await p.evaluate(() => document.getElementById('word').textContent), JSON.stringify(rects[s.out]));
    await p.close();
  }
  require('fs').writeFileSync('rects.json', JSON.stringify(rects));
  await b.close();
})();
