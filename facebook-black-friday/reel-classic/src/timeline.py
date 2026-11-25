import json,math
vo=json.load(open('vo/vo.json'))
BPM=128;beat=60/BPM
# (scene, line, earliest start in beats after previous line end, tail beats)
plan=[('hook',0,1),('bf',1,1),('pct',2,0),('pct',3,1),('feat',4,1),('trust',5,1),('cta',6,0),('cta',7,1)]
t=beat*0.25;clips=[];caps=[];scenes={};prev_end=0
for sid,li,gap in plan:
    st=math.ceil((max(t,prev_end+0.15))/beat)*beat
    clips.append({'i':li,'t':round(st,3)})
    for w in vo[li]['words']:caps.append({'w':w['w'],'s':round(st+w['s'],3),'e':round(st+w['e'],3),'line':li})
    end=st+vo[li]['dur'];prev_end=end;t=end+gap*beat*0.5
    scenes.setdefault(sid,[st,end]);scenes[sid][1]=end
order=['hook','bf','pct','feat','trust','cta'];sc=[]
for i,s in enumerate(order):
    a=0 if i==0 else scenes[s][0]-beat*0.5
    sc.append({'id':s,'s':round(a,3)})
for i in range(len(sc)-1):sc[i]['e']=sc[i+1]['s']
total=math.ceil((scenes['cta'][1]+beat*6)/beat)*beat;sc[-1]['e']=round(total,3)
json.dump({'total':round(total,3),'bpm':BPM,'scenes':sc,'clips':clips,'caps':caps,'lines':[v['text'] for v in vo]},open('timeline.json','w'),indent=1)
for s in sc:print(s,round(s['e']-s['s'],2))
print('total',total)
