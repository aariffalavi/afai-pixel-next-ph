const { chromium } = require('playwright');
const fs=require('fs');
const ease=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
async function setup(ctx,url){
  const p=await ctx.newPage();
  await p.goto(url,{waitUntil:'networkidle',timeout:60000});
  try{ await p.getByRole('button',{name:'Accept'}).first().click({timeout:5000}); }catch(e){console.log('no accept')}
  await p.waitForTimeout(500);
  // close top announcement bar if present
  await p.evaluate(()=>{ for(const b of document.querySelectorAll('button,a,span')){ const t=(b.getAttribute('aria-label')||b.textContent||'').trim(); if((t==='×'||t==='✕'||/close|dismiss/i.test(t)) && b.getBoundingClientRect().top<60 && b.getBoundingClientRect().width<60){ b.click(); break; } } });
  return p;
}
async function pos(p,txt){ return await p.evaluate(t=>{ const els=[...document.querySelectorAll('h1,h2,h3,p,span,div')]; const e=els.find(e=>e.children.length<3 && e.textContent.trim().startsWith(t) && e.offsetParent!==null && e.getBoundingClientRect().height>0 && !e.closest('nav,header,.menu,[class*=offcanvas],[class*=sidebar]')); return e? e.getBoundingClientRect().top+scrollY : null; },txt); }
async function shoot(p,dir,segs){
  fs.mkdirSync(dir,{recursive:true}); let n=0;
  for(const [a,b,frames] of segs){ for(let i=0;i<frames;i++){ const y=a+(b-a)*ease(frames==1?1:i/(frames-1)); await p.evaluate(y=>window.scrollTo(0,y),y); await p.waitForTimeout(25); await p.screenshot({path:`${dir}/${String(n++).padStart(4,'0')}.jpg`,type:'jpeg',quality:90}); } }
  console.log(dir,n);
}
(async()=>{
  const b=await chromium.launch();
  const ctx=await b.newContext({viewport:{width:430,height:932},deviceScaleFactor:2,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'});
  await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#afp-pop{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st));});
  let p=await setup(ctx,'https://afaipixel.com/');
  await p.screenshot({path:'chk_home.png'});
  const P={services:await pos(p,'Everything your business'), tools:await pos(p,'Tools and platforms'), reviews:await pos(p,'What clients say'), cta:await pos(p,'Have a project in mind')};
  console.log(P);
  // reload to catch hero intro animation
  await p.evaluate(()=>window.scrollTo(0,0)); await p.reload({waitUntil:'domcontentloaded'});
  await shoot(p,'rec_hero',[[0,0,100],[0,560,60],[560,560,20]]);
  await shoot(p,'rec_services',[[P.services-120,P.services-120,15],[P.services-120,P.services+1500,216],[P.services+1500,P.services+1500,15]]);
  await shoot(p,'rec_reviews',[[P.reviews-140,P.reviews-140,10],[P.reviews-140,P.reviews+520,88],[P.reviews+520,P.reviews+520,10]]);
  await p.close();
  p=await setup(ctx,'https://afaipixel.com/global-supermarket-eu/');
  await p.screenshot({path:'chk_case.png',fullPage:true});
  const C={approach:await pos(p,'Our approach'), result:await pos(p,'The result')};
  console.log(C);
  await shoot(p,'rec_case',[[0,0,30],[0,C.approach-100,150],[C.approach-100,C.approach-100,30],[C.approach-100,C.result-150,140],[C.result-150,C.result-150,34]]);
  await b.close();
})();
