import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Black Friday at Afai Pixel. Twenty percent off every new website.",
"Custom, mobile-friendly websites, built to bring you enquiries.",
"Starter websites. Business websites. Online stores.",
"S E O ready, fast and secure, with a fixed quote in one working day.",
"Limited time only. Send us a message, and claim twenty percent off your website.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+8%",pitch="-2Hz",boundary="WordBoundary")
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
