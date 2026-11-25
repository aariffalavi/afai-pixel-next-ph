import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Every morning, before the world wakes up, you open the door to your dream.",
"Years of early mornings. Missed dinners. Quiet sacrifices.",
"You poured your heart into every single detail.",
"But online, the world just walks right past.",
"Your story deserves to be seen.",
"At Afai Pixel, we turn your hard work into a brand people feel, and a website people trust.",
"And then, one day, it happens.",
"The first message. The first order. The first stranger who believes in you.",
"That moment is why we do what we do.",
"Trusted by businesses around the world. Rated five stars.",
"Your dream deserves to be seen. Send us a message, and let's tell your story, together.",
"Afai Pixel. Make your ideas a reality.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-SoniaNeural",rate="-8%",pitch="-1Hz",boundary="WordBoundary")
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
