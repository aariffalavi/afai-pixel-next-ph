import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Forget your mood. Stick to the plan.",
"Your business won't grow on motivation. It grows on consistency.",
"Big bursts burn out. Small steps, every week, add up.",
"Here's an example.",
"Business A posts ten times in one week, then goes quiet. Business B posts twice a week, every week.",
"Three months later, B is the one customers remember.",
"That's how we work at Afai Pixel. A clear plan, then steady work, week after week.",
"Less motivation. More discipline.",
"Want a plan for your business? Comment PLAN below.",
"One percent better, every day.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+8%",pitch="-4Hz",boundary="WordBoundary")
  words=[]; audio=open(f"vo/{i}.mp3","wb")
  async for m in c.stream():
    if m["type"]=="audio": audio.write(m["data"])
    elif m["type"]=="WordBoundary": words.append({"w":m["text"],"s":m["offset"]/1e7,"e":(m["offset"]+m["duration"])/1e7})
  audio.close()
  st=max(0,words[0]["s"]-0.05); end=words[-1]["e"]+0.18
  subprocess.run(["ffmpeg","-y","-v","error","-i",f"vo/{i}.mp3","-ss",str(st),"-t",str(end-st),"-ar","48000","-ac","1",f"vo/{i}.wav"],check=True)
  for w in words: w["s"]-=st; w["e"]-=st
  return {"text":l,"dur":end-st,"words":words}
async def main():
  out=[await one(i,l) for i,l in enumerate(lines)]
  for o in out: print(round(o["dur"],2), o["text"])
  json.dump(out,open("vo/vo.json","w"),indent=1)
asyncio.run(main())
