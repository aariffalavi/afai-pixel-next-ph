const { chromium } = require('playwright');
const fs=require('fs');
(async()=>{
  const tl=JSON.parse(fs.readFileSync('timeline.json'));
  const args=process.argv.slice(2);
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+process.cwd()+'/reel.html');
  await p.evaluate(tl=>init(tl),tl);
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(500);
  if(args[0]==='preview'){
    fs.mkdirSync('prev',{recursive:true});
    for(const t of args.slice(1).map(Number)){await p.evaluate(t=>render(t),t);await p.waitForTimeout(50);await p.screenshot({path:`prev/t${t.toFixed(2)}.jpg`,type:'jpeg',quality:85});}
  } else { /* full or range: node render.js range A B */
    fs.mkdirSync('frames',{recursive:true});
    const N=Math.ceil(tl.total*30);
    const A=+(args[1]||0),B=+(args[2]||N);for(let f=A;f<Math.min(B,N);f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:`frames/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:93});if(f%150==0)console.log(f,'/',N);}
  }
  await b.close();
})();
