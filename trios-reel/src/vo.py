# Voice-over: edge-tts (en-GB-RyanNeural) + word timings -> vo/*.wav, vo/vo.json
import asyncio, edge_tts, json, subprocess, ssl, os
import edge_tts.communicate as _c
_c._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
os.makedirs("vo", exist_ok=True)
lines = [
 ("hook", "Top ten trios in football history. And number one will start an argument."),
 ("t10", "Ten. Henry, Bergkamp and Pires. Arsenal's Invincibles went a whole league season unbeaten."),
 ("t9",  "Nine. Ronaldo, Rivaldo and Ronaldinho. The three R's fired Brazil to the 2002 World Cup."),
 ("t8",  "Eight. Best, Law and Charlton. Manchester United's holy trinity. All three won the Ballon d'Or."),
 ("t7",  "Seven. Xavi, Iniesta and Busquets. Not a goal trio. A passing machine that ran Barcelona and Spain."),
 ("t6",  "Six. Salah, Firmino and Mané. Liverpool's front three won the Champions League and the Premier League."),
 ("t5",  "Five. Messi, Eto'o and Henry. One hundred goals between them in Barcelona's 2009 treble season."),
 ("t4",  "Four. Gullit, Van Basten and Rijkaard. The Dutch trio won AC Milan back to back European Cups."),
 ("t3",  "Three. Di Stéfano, Puskás and Gento. In the 1960 final, Real Madrid beat Frankfurt seven, three."),
 ("t2",  "Two. Bale, Benzema and Cristiano. The BBC won four Champions Leagues in five years."),
 ("t1",  "And number one. Messi, Suárez and Neymar. M S N scored a hundred and twenty two goals in one season."),
 ("ex1", "Here's an example. 2015 Champions League final. Messi drives at Juventus and shoots. Buffon parries, and Suárez pounces."),
 ("ex2", "Then, deep in stoppage time, Neymar seals it. Three, one, and the treble."),
 ("cta", "Did we get it right? Comment your number one trio below."),
 ("out", "Follow for more football top tens."),
]
async def one(i, sid, l):
    c = edge_tts.Communicate(l, "en-GB-RyanNeural", rate="+20%", boundary="WordBoundary")
    words = []; audio = open(f"vo/{i}.mp3", "wb")
    async for m in c.stream():
        if m["type"] == "audio": audio.write(m["data"])
        elif m["type"] == "WordBoundary":
            words.append({"w": m["text"], "s": m["offset"]/1e7, "e": (m["offset"]+m["duration"])/1e7})
    audio.close()
    end = words[-1]["e"] + 0.18
    subprocess.run(["ffmpeg","-y","-v","error","-i",f"vo/{i}.mp3","-t",str(end),"-ar","48000","-ac","1",f"vo/{i}.wav"], check=True)
    # tighten long pauses between sentences (keep 0.26 s)
    import wave, numpy as np
    w = wave.open(f"vo/{i}.wav"); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16); w.close()
    SR = 48000; keep = 0.26; segs = []; cur = 0; shift = 0.0
    for k in range(len(words)):
        words[k]["s"] -= shift; words[k]["e"] -= shift
        if k+1 < len(words):
            g0 = words[k]["e"] + shift; g1 = words[k+1]["s"]
            if g1 - g0 > keep + 0.05:
                cut = g1 - g0 - keep; m0 = g0 + keep/2
                segs.append(a[int(cur*SR):int(m0*SR)]); cur = m0 + cut; shift += cut
    segs.append(a[int(cur*SR):])
    b = np.concatenate(segs); end = len(b)/SR
    w = wave.open(f"vo/{i}.wav", "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(b.tobytes()); w.close()
    return {"id": sid, "text": l, "dur": end, "words": words}
async def main():
    out = [await one(i, s, l) for i, (s, l) in enumerate(lines)]
    for o in out: print(o["id"], round(o["dur"], 2), o["text"])
    json.dump(out, open("vo/vo.json", "w"), indent=1)
asyncio.run(main())
