import json
vo=json.load(open('vo/vo.json'))
plan=[('dawn',[(0,0.9)],0.6),('years',[(1,0.2)],0.7),('heart',[(2,0.2)],0.8),('past',[(3,0.2)],1.0),('seen',[(4,0.4)],1.0),('build',[(5,0.3)],1.2),('oneday',[(6,0.3)],0.9),('first',[(7,0.1)],1.4),('why',[(8,0.3)],1.0),('trust',[(9,0.3)],0.9),('cta',[(10,0.4)],1.2),('logo',[(11,0.5)],2.0)]
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
