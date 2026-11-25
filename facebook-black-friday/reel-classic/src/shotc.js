const { chromium } = require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const rects={};
for(const [w,h,v,n] of [[1080,1350,'dark','feed-4x5'],[1080,1080,'dark','square-1x1'],[1080,1920,'dark','story-9x16'],[1080,1350,'green','feed-4x5-green']]){
 const p=await b.newPage({viewport:{width:w,height:h}});await p.goto(`file://${process.cwd()}/classic.html?w=${w}&h=${h}&v=${v}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
 rects[n]=await p.evaluate(()=>{const r=document.getElementById('btn').getBoundingClientRect();return [r.x,r.y,r.width,r.height]});
 const over=await p.evaluate(()=>[...document.querySelectorAll('#root *')].map(e=>e.getBoundingClientRect().right).reduce((a,b)=>Math.max(a,b)));console.log(n,Math.round(over));
 await p.screenshot({path:`classic_${n}.png`});await p.close()}
fs.writeFileSync('btn.json',JSON.stringify(rects));await b.close()})();
