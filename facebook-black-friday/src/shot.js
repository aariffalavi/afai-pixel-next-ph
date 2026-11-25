const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
const jobs=[[1080,1350,'dark','feed-4x5'],[1080,1350,'green','feed-4x5-green'],[1080,1080,'dark','square-1x1'],[1080,1080,'green','square-1x1-green'],[1080,1920,'dark','story-9x16']];
for(const [w,h,v,n] of jobs){const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(`file://${process.cwd()}/post.html?w=${w}&h=${h}&v=${v}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
 const m=await p.evaluate(()=>[...document.querySelectorAll('#root *')].map(e=>e.getBoundingClientRect().right).reduce((a,b)=>Math.max(a,b)));console.log(n,Math.round(m));
 await p.screenshot({path:`post_${n}.png`});await p.close()}
await b.close()})();
