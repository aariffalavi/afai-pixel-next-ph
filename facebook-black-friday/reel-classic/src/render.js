const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
  const tl=JSON.parse(fs.readFileSync('timeline.json'));
  const [mode,W,H,...rest]=process.argv.slice(2);const w=+W,h=+H;
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  p.on('console',m=>{if(['warning','error'].includes(m.type()))console.log('PAGE',m.text())});
  await p.goto(`file://${process.cwd()}/reel.html?w=${w}&h=${h}`);const btn=JSON.parse(fs.readFileSync('btn.json'));await p.evaluate(([tl,b])=>init(tl,b),[tl,btn]);
  await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
  if(mode==='preview'){const dir=`prev_${w}x${h}`;fs.mkdirSync(dir,{recursive:true});for(const t of rest.map(Number)){await p.evaluate(t=>render(t),t);await p.waitForTimeout(50);await p.screenshot({path:`${dir}/t${t.toFixed(2)}.jpg`,type:'jpeg',quality:88})}}
  else{const dir=`frames_${w}x${h}`;fs.mkdirSync(dir,{recursive:true});const N=Math.ceil(tl.total*30);const A=+(rest[0]||0),B=+(rest[1]||N);for(let f=A;f<Math.min(B,N);f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});if(f%300==0)console.log(f,'/',N)}}
  await b.close()})();
