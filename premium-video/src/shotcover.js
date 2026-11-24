const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/cover.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
await p.screenshot({path:'cover_new.jpg',type:'jpeg',quality:94});await b.close();})();
