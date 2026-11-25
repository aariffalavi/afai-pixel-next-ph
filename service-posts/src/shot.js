const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for(let n=0;n<11;n++)for(const [w,h,t] of [[1080,1350,'4x5'],[1080,1080,'1x1']]){
 const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(`file://${process.cwd()}/svc.html?w=${w}&h=${h}&n=${n}`);await p.waitForFunction(()=>document.body.dataset.ok==='1');await p.waitForTimeout(300);
 const r=await p.evaluate(()=>{const R=[...document.querySelectorAll('.k div')].map(e=>e.getBoundingClientRect());return {right:Math.max(...[...document.querySelectorAll('.k div')].map(e=>e.getBoundingClientRect().left+e.scrollWidth))}});
 if(r.right>w+2)console.log('OVERFLOW',n,t,Math.round(r.right));
 await p.screenshot({path:`out_${String(n+1).padStart(2,'0')}_${t}.png`});await p.close()}
await b.close()})();
