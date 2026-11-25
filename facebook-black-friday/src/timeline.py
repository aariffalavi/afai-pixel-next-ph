import json
vo=json.load(open('vo/vo.json'))
plan=[('s1',[(0,0.5)],0.5),('s2',[(1,0.2)],0.6),('s3',[(2,0.2)],1.4),('s4',[(3,0.2)],0.8),('s5',[(4,0.3)],2.6)]
t=0;scenes=[];clips=[];caps=[]
for sid,items,tail in plan:
  st=t
  for vi,lead in items:
    t+=lead; clips.append({'i':vi,'t':round(t,3)})
    for w in vo[vi]['words']: caps.append({'w':w['w'],'s':round(t+w['s'],3),'e':round(t+w['e'],3),'line':vi})
    t+=vo[vi]['dur']
  t+=tail; scenes.append({'id':sid,'s':round(st,3),'e':round(t,3)})
json.dump({'total':round(t,3),'scenes':scenes,'clips':clips,'caps':caps,'lines':[v['text'] for v in vo]},open('timeline.json','w'),indent=1)
for s in scenes: print(s, round(s['e']-s['s'],2))
print('total',t)
