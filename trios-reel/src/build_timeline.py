# Builds timeline.json from vo/vo.json: scene start/end, VO clip offsets, caption words, key marks
import json, re
vo = json.load(open("vo/vo.json"))
LEAD = 0.25            # VO starts this long after the scene starts
TAIL = {"ex1": 1.3, "ex2": 1.4, "cta": 1.2, "out": 1.6, "hook": 0.35}
keys = {
 "t10": ["Henry", "Bergkamp", "Pires", "Arsenal"],
 "t9":  ["Ronaldo", "Rivaldo", "Ronaldinho", "The"],
 "t8":  ["Best", "Law", "Charlton", "Manchester"],
 "t7":  ["Xavi", "Iniesta", "Busquets", "Not"],
 "t6":  ["Salah", "Firmino", "Man", "Liverpool"],
 "t5":  ["Messi", "Eto", "Henry", "One"],
 "t4":  ["Gullit", "Van", "Rijkaard", "The"],
 "t3":  ["Di", "Pusk", "Gento", "In"],
 "t2":  ["Bale", "Benzema", "Cristiano", "The"],
 "t1":  ["Messi", "Su", "Neymar", "M"],
 "ex1": ["example", "2015", "Messi", "drives", "shoots", "Buffon", "parries", "Su", "pounces"],
 "ex2": ["stoppage", "Neymar", "seals", "Three", "treble"],
 "cta": ["Comment", "below"],
}
t = 0.0; scenes = []; clips = []; caps = []
for i, v in enumerate(vo):
    sid = v["id"]; s = t; vs = s + LEAD
    words = v["words"]
    # display tokens (with punctuation) aligned to word boundaries
    toks = v["text"].split()
    if len(toks) != len(words): toks = [w["w"] for w in words]
    W = []
    k = 0
    while k < len(words):
        if words[k]["w"] == "M" and k+2 < len(words) and words[k+1]["w"] == "S" and words[k+2]["w"] == "N":
            W.append({"t": "MSN", "s": vs+words[k]["s"], "e": vs+words[k+2]["e"]}); k += 3; continue
        W.append({"t": toks[k], "s": vs+words[k]["s"], "e": vs+words[k]["e"]}); k += 1
    # key marks: first word (after previous mark) starting with the key
    marks = []; j = 0
    for key in keys.get(sid, []):
        while j < len(W) and not W[j]["t"].strip(".,!?'").startswith(key): j += 1
        marks.append(round(W[j]["s"]-s, 3) if j < len(W) else None)
        if j < len(W): j += 1
    e = vs + v["dur"] + TAIL.get(sid, 0.4)
    scenes.append({"id": sid, "s": round(s, 3), "e": round(e, 3), "marks": marks, "vo_end": round(vs+v["dur"]-s, 3)})
    clips.append({"i": i, "t": round(vs, 3)})
    # caption chunks: break at sentence end or every 4 words
    chunk = []
    for w in W:
        chunk.append(w)
        if re.search(r"[.?!,]$", w["t"]) or len(chunk) == 4:
            caps.append({"words": chunk}); chunk = []
    if chunk: caps.append({"words": chunk})
    t = e
for c in caps:
    c["s"] = c["words"][0]["s"] - 0.05; c["e"] = c["words"][-1]["e"] + 0.12
for a, b in zip(caps, caps[1:]):
    a["e"] = min(a["e"], b["s"])
json.dump({"total": round(t, 3), "scenes": scenes, "clips": clips, "caps": caps}, open("timeline.json", "w"), indent=1)
for s in scenes: print(s["id"], s["s"], s["e"], s["marks"])
print("total", round(t, 2))
