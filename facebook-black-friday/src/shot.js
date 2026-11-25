const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();
for(const [w,h,n] of [[1080,1350,'feed-4x5'],[1080,1080,'square-1x1'],[1080,1920,'story-9x16']]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
 await p.goto(`file://${process.cwd()}/post.html?w=${w}&h=${h}`);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
 await p.screenshot({path:`post_${n}.png`});await p.close()}
await b.close()})();
