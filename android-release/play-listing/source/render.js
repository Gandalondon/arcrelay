// Renders shot.html into the Play listing art: raw-s1..s4.png (1080 x 1920) and raw-fg.png (1024 x 500).
// Then: python3 finish.py (flattens to 24-bit PNG, no alpha, with the final names in ../)
const { chromium } = require(require.resolve('playwright', { paths: [process.env.PW || process.cwd()] }));
(async () => { const b = await chromium.launch({ executablePath: process.env.CHROME || undefined }); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 await p.goto('file://' + process.cwd() + '/shot.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(800);
 for (const id of ['s1','s2','s3','s4','fg']) await (await p.$('#' + id)).screenshot({ path: 'raw-' + id + '.png' });
 await b.close(); })();
