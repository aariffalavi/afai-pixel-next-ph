import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Every successful business starts with a dream. A vision to grow. A passion to create. And a determination to achieve something greater.",
"But in today's competitive digital world, having a great business isn't enough. You need a powerful online presence. You need to stand out. You need to be remembered.",
"That's where Afai Pixel comes in. We're more than a creative agency. We're your digital growth partner, turning ambitious ideas into powerful digital experiences.",
"From stunning website design and development, to creative branding, graphic design, social media marketing, video editing, SEO, and complete digital marketing solutions, we bring your entire digital vision together.",
"Whether you're building your business in Sri Lanka, or taking your dreams across borders, Afai Pixel is here to help. We proudly work with Sri Lankan businesses, and Sri Lankans living worldwide, across Australia, Europe, the UK, the USA, Canada, the Middle East, and beyond.",
"Your business deserves creativity, commitment, and a team that understands your vision. Let's create something that makes your brand impossible to ignore.",
"Your next chapter of business growth starts here. Don't wait for the right opportunity. Create it. Get in touch with Afai Pixel today. Let's make your ideas a reality.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+21%",pitch="-2Hz",boundary="WordBoundary")
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
