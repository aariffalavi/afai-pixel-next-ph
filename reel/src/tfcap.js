const { chromium } = require('playwright');
const fs=require('fs');
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:430,height:932},deviceScaleFactor:2,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'});
const p=await ctx.newPage();
await p.goto('https://transfoodgrosshandel.com/',{waitUntil:'networkidle',timeout:60000});
// preload lazy content by scrolling down and back
await p.evaluate(async()=>{for(let y=0;y<2000;y+=300){scrollTo(0,y);await new Promise(r=>setTimeout(r,250))}scrollTo(0,0)});
await p.waitForTimeout(2500);
const pos=await p.evaluate(()=>{const f=t=>{const e=[...document.querySelectorAll('h1,h2,h3,h4,div,span')].find(e=>e.children.length<3&&e.textContent.trim().replace(/\s+/g,' ')===t&&e.getBoundingClientRect().height>0);return e?e.getBoundingClientRect().top+scrollY:null};return {brand:f('Shop by Brand'),arr:f('New Arrivals')}});
console.log(pos);
const B=pos.brand-140, A=pos.arr-110, C=A+330;
const segs=[[0,0,240],[0,B,90],[B,B,15],[B,A,25],[A,A,15],[A,C,30],[C,C,46]];
fs.rmSync('rec_case',{recursive:true,force:true});fs.mkdirSync('rec_case');let n=0;
for(const [a,c,fr] of segs){for(let i=0;i<fr;i++){const y=a+(c-a)*ease(fr==1?1:i/(fr-1));await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(25);await p.screenshot({path:`rec_case/${String(n++).padStart(4,'0')}.jpg`,type:'jpeg',quality:90});}}
console.log('frames',n);await b.close();})();
