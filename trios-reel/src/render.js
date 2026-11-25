// node render.js preview t1 t2 ...   -> prev/tX.jpg
// node render.js range A B           -> frames/NNNNN.jpg (30 fps)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const tl = JSON.parse(fs.readFileSync('timeline.json'));
  const args = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  p.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()) });
  await p.goto('file://' + process.cwd() + '/reel.html');
  await p.evaluate(() => document.fonts.load('40px Sketch').then(() => document.fonts.load('40px Marker')).then(() => document.fonts.load('40px Hand')));
  await p.evaluate(tl => init(tl), tl);
  await p.waitForTimeout(300);
  if (args[0] === 'preview') {
    fs.mkdirSync('prev', { recursive: true });
    for (const t of args.slice(1).map(Number)) {
      await p.evaluate(t => render(t), t);
      await p.screenshot({ path: `prev/t${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 80 });
    }
  } else {
    fs.mkdirSync('frames', { recursive: true });
    const N = Math.ceil(tl.total * 30);
    const A = +(args[1] || 0), B = Math.min(+(args[2] || N), N);
    for (let f = A; f < B; f++) {
      await p.evaluate(t => render(t), f / 30);
      await p.screenshot({ path: `frames/${String(f).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
      if (f % 300 == 0) console.log(f, '/', N);
    }
  }
  await b.close();
})();
