// Render poster.html to a vector PDF (A3) and/or a PNG preview with the preinstalled Chromium.
//   PDF=out.pdf node render.js
//   PNG=out.png SCALE=0.5 [CLIP=x,y,w,h] node render.js
const { chromium } = require('playwright');
const path = require('path');

const W = 1122.52, H = 1587.4; // A3: 297mm x 420mm at 96dpi

(async () => {
  const browser = await chromium.launch();
  const scale = parseFloat(process.env.SCALE || '0.5');
  const page = await browser.newPage({ viewport: { width: Math.ceil(W), height: Math.ceil(H) }, deviceScaleFactor: scale });
  await page.goto('file://' + path.resolve(__dirname, process.env.SRC || 'poster.html'));
  await page.evaluate(() => document.fonts.ready);
  const bad = await page.evaluate(() => [...document.fonts].filter(f => f.status !== 'loaded').map(f => f.family + ' ' + f.weight + ' ' + f.status));
  if (bad.length) console.log('fonts not loaded:', bad.join(', '));
  if (process.env.PNG) {
    let clip = { x: 0, y: 0, width: W, height: H };
    if (process.env.CLIP) { const [x, y, w, h] = process.env.CLIP.split(',').map(Number); clip = { x, y, width: w, height: h }; }
    await page.screenshot({ path: process.env.PNG, clip });
  }
  if (process.env.PDF) {
    await page.pdf({ path: process.env.PDF, width: '297mm', height: '420mm', printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  }
  await browser.close();
})();
