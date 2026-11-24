import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Hey! Is your website actually bringing you customers?",
"Meet Afai Pixel. Web design, branding and digital marketing for businesses worldwide.",
"This is the real site. Fast, clean, and built to turn visitors into enquiries.",
"Websites, logos, branding, social media, Google Ads, hosting and custom systems. All under one roof.",
"Here's a real example. Transfood Grosshandel supplies wholesale food across Germany, covering Indian, Asian, African and more.",
"We built their online store, so shops can browse the brands, see what's new, and order in bulk, right from their phone.",
"Rated five stars from twenty-five Google reviews.",
"Want a free quote? Comment WEBSITE below, and we'll reply within one working day.",
"Afai Pixel. Make your ideas a reality.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+10%",boundary="WordBoundary")
  words=[]; audio=open(f"vo/{i}.mp3","wb")
  async for m in c.stream():
    if m["type"]=="audio": audio.write(m["data"])
    elif m["type"]=="WordBoundary": words.append({"w":m["text"],"s":m["offset"]/1e7,"e":(m["offset"]+m["duration"])/1e7})
  audio.close()
  # wav, trimmed to last word end + 0.15s
  end=words[-1]["e"]+0.18
  subprocess.run(["ffmpeg","-y","-v","error","-i",f"vo/{i}.mp3","-t",str(end),"-ar","48000","-ac","1",f"vo/{i}.wav"],check=True)
  return {"text":l,"dur":end,"words":words}
async def main():
  out=[await one(i,l) for i,l in enumerate(lines)]
  for o in out: print(round(o["dur"],2), round(o["words"][0]["s"],2), o["text"])
  json.dump(out,open("vo/vo.json","w"),indent=1)
asyncio.run(main())
