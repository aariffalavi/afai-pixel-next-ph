import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Is your website losing you customers?",
"Here are three signs.",
"One. It's slow on mobile.",
"Two. Visitors can't see what to do next.",
"Three. Nobody finds you on Google.",
"We fix all three. Fast, clear websites, built to bring in enquiries.",
"Like these, for clients around the world.",
"Rated five stars on Google.",
"Want to know what's holding your site back? Get a free website audit.",
"Comment AUDIT, and we'll send you practical fixes. Free, with no obligation.",
"Afai Pixel. Make your ideas a reality.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+10%",boundary="WordBoundary")
  words=[]; audio=open(f"vo/{i}.mp3","wb")
  async for m in c.stream():
    if m["type"]=="audio": audio.write(m["data"])
    elif m["type"]=="WordBoundary": words.append({"w":m["text"],"s":m["offset"]/1e7,"e":(m["offset"]+m["duration"])/1e7})
  audio.close()
  end=words[-1]["e"]+0.18
  subprocess.run(["ffmpeg","-y","-v","error","-i",f"vo/{i}.mp3","-t",str(end),"-ar","48000","-ac","1",f"vo/{i}.wav"],check=True)
  return {"text":l,"dur":end,"words":words}
async def main():
  out=[await one(i,l) for i,l in enumerate(lines)]
  for o in out: print(round(o["dur"],2), o["text"])
  json.dump(out,open("vo/vo.json","w"),indent=1)
asyncio.run(main())
