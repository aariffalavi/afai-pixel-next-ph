import json
vo=json.load(open('vo/vo.json'))
# (scene id, [vo lines], min duration)
plan=[("hook",[0],8.1),("gcard",[1],6.5),("dcard",[2],6.2),("g1",[3],7.2),("g23",[4],9.6),
      ("d1",[5],6.8),("d2",[6],5.4),("d3",[7],6.2),("ex",[8,9],11.8),("verdict",[10],4.6),
      ("comment",[11],6.8),("outro",[12],3.6)]
t=0;scenes=[];clips=[];caps=[]
for sid,ls,mind in plan:
    s=t; c=t+0.3
    for i in ls:
        if sid=="ex" and i==9: c=max(c,s+8.0)
        clips.append({"i":i,"t":round(c,3)})
        txt=vo[i]["text"];pos=0
        for w in vo[i]["words"]:
            j=txt.find(w["w"],pos);pos=j+len(w["w"]) if j>=0 else pos
            br=pos<len(txt) and txt[pos] in ".,?!"
            caps.append({"w":w["w"],"s":round(c+w["s"],3),"e":round(c+w["e"],3),"line":i,"br":br})
        c+=vo[i]["dur"]+0.25
    e=max(s+mind,c+0.2); scenes.append({"id":sid,"s":round(s,3),"e":round(e,3)}); t=e
json.dump({"total":round(t,3),"scenes":scenes,"clips":clips,"caps":caps},open('timeline.json','w'),indent=0)
for s in scenes: print(s)
print("total",t)
