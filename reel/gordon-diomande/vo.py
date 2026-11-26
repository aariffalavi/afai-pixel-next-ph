import asyncio, edge_tts, json, subprocess, ssl
import edge_tts.communicate as _c
_c._SSL_CTX=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
lines=[
"Anthony Gordon versus Yan Diomande. Barcelona against Real Madrid. Who is the better winger right now?",
"Anthony Gordon. Twenty-five, English, and a seventy-million euro signing for Barcelona.",
"Yan Diomande. Just twenty, Ivorian, and already scoring for Real Madrid.",
"Gordon's last three goals. First, off the bench in a six-one win over Alavés.",
"Then a brace in Baku. Two rebounds against Sabah, pounced on before anyone else moved.",
"Diomande's last three. A cross-shot to beat Villarreal, his first goal for Madrid.",
"A late volley against his old club, RB Leipzig.",
"And a stunning volley at Racing Santander, nominated for LaLiga goal of the month.",
"Here's an example. Same Clásico, same chance. Gordon attacks the space and gambles on the second ball.",
"Diomande takes it early, and hits it from distance.",
"So it's poacher's instinct against highlight-reel strikes.",
"Who are you taking? Comment GORDON or DIOMANDE below.",
"Follow for the next face-off.",
]
async def one(i,l):
  c=edge_tts.Communicate(l,"en-GB-RyanNeural",rate="+8%",boundary="WordBoundary")
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
