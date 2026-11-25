const { chromium } = require('playwright');
const fs=require('fs');
const sites=[['tf','https://transfoodgrosshandel.com/'],['wd','https://windoors.lk/'],['sm','https://smeraldomilano.eu/'],['agl','https://aglsrilanka.com/']];
const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
(async()=>{const b=await chromium.launch();fs.rmSync('rec_proof',{recursive:true,force:true});fs.mkdirSync('rec_proof');let n=0;
for(const [k,u] of sites){
 const ctx=await b.newContext({viewport:{width:430,height:932},deviceScaleFactor:2,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'});
 const p=await ctx.newPage();
 try{await p.goto(u,{waitUntil:'networkidle',timeout:45000})}catch(e){console.log(k,'goto timeout')}
 for(const nm of ['Accept','Accept All','Accept all','I agree','Allow all','OK','Got it']){try{await p.getByRole('button',{name:nm,exact:true}).first().click({timeout:600})}catch(e){}}
 await p.waitForTimeout(3000);
 for(let i=0;i<40;i++){await p.evaluate(y=>scrollTo(0,y),260*ease(i/39));await p.waitForTimeout(20);await p.screenshot({path:`rec_proof/${String(n++).padStart(4,'0')}.jpg`,type:'jpeg',quality:90})}
 console.log(k,n);await ctx.close();}
await b.close();})();
