const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
 await p.goto('file://' + process.cwd() + '/shot.html'); await p.waitForTimeout(800);
 await (await p.$('#s1')).screenshot({ path: 'raw-1.png' }); await (await p.$('#s2')).screenshot({ path: 'raw-2.png' }); await (await p.$('#fg')).screenshot({ path: 'raw-fg.png' });
 await b.close(); })();
