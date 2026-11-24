const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
  const tl=JSON.parse(fs.readFileSync('timeline.json'));const dots=JSON.parse(fs.readFileSync('dots.json'));const lm='data:image/png;base64,'+fs.readFileSync('../assets/logo_white.png').toString('base64');
  const [mode,W,H,...rest]=process.argv.slice(2);const w=+W,h=+H;
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  p.on('console',m=>{if(m.type()==='warning'||m.type()==='error')console.log('PAGE',m.text())});
  await p.goto(`file://${process.cwd()}/brand.html?w=${w}&h=${h}`);
  await p.evaluate(([tl,d,l])=>init(tl,d,l),[tl,dots,lm]);
  await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
  if(mode==='preview'){const dir=`prev_${w}x${h}`;fs.mkdirSync(dir,{recursive:true});
    for(const t of rest.map(Number)){await p.evaluate(t=>render(t),t);await p.waitForTimeout(60);await p.screenshot({path:`${dir}/t${t.toFixed(2)}.jpg`,type:'jpeg',quality:85});}}
  else{const dir=`frames_${w}x${h}`;fs.mkdirSync(dir,{recursive:true});const N=Math.ceil(tl.total*30);const A=+(rest[0]||0),B=+(rest[1]||N);
    for(let f=A;f<Math.min(B,N);f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});if(f%300==0)console.log(f,'/',N);}}
  await b.close();})();
