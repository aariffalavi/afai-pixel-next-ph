// usage: node render.js preview t1 t2 ...   |   node render.js range A B
const { chromium } = require('playwright');
const fs=require('fs'),http=require('http'),path=require('path');
const root=__dirname;
const srv=http.createServer((q,r)=>{const f=path.join(root,decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f,(e,d)=>{if(e){r.writeHead(404);r.end();return}
  r.writeHead(200,{'Content-Type':f.endsWith('.js')?'text/javascript':f.endsWith('.html')?'text/html':'application/octet-stream'});r.end(d)})});
(async()=>{
  await new Promise(ok=>srv.listen(0,ok));const port=srv.address().port;
  const tl=JSON.parse(fs.readFileSync(root+'/timeline.json'));
  const args=process.argv.slice(2);
  const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  p.on('console',m=>{if(m.type()==='error')console.log('PAGE',m.text())});p.on('pageerror',e=>console.log('ERR',e.message));
  await p.goto(`http://localhost:${port}/reel.html`);
  await p.waitForFunction(()=>window.ready===true);
  await p.evaluate(tl=>init(tl),tl);
  await p.evaluate(()=>document.fonts.ready);
  if(args[0]==='events'){const ev=[];let prev=0;const N=Math.ceil(tl.total*30);
    for(let f=0;f<N;f++){const o=await p.evaluate(t=>{render(t);const e=document.getElementById('rp_goal');return e.offsetParent?+getComputedStyle(e).opacity:0},f/30);if(o>0&&prev===0)ev.push(+(f/30).toFixed(3));prev=o}
    fs.writeFileSync(root+'/goals.json',JSON.stringify(ev));console.log(ev);}
  else if(args[0]==='preview'){
    fs.mkdirSync(root+'/prev',{recursive:true});
    for(const t of args.slice(1).map(Number)){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${root}/prev/t${t.toFixed(2)}.jpg`,type:'jpeg',quality:80});}
  } else {
    fs.mkdirSync(root+'/frames',{recursive:true});
    const N=Math.ceil(tl.total*30);const A=+(args[1]||0),B=Math.min(+(args[2]||N),N);
    for(let f=A;f<B;f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:`${root}/frames/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});if(f%100==0)console.log(f,'/',N);}
  }
  await b.close();srv.close();
})();
