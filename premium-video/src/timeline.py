import json
vo=json.load(open('vo/vo.json'))
plan=[('deserve',[(0,0.15)],0.5),('brand',[(1,0.3)],1.4),('design',[(2,0.3)],2.2),('marketing',[(3,0.3)],1.8),('world',[(4,0.3)],1.6),('rating',[(5,0.3)],0.9),('next',[(6,0.3)],0.8),('dm',[(7,0.3)],2.4),('logo',[(8,0.6)],1.6)]
t=0;scenes=[];clips=[];caps=[]
for sid,items,tail in plan:
  st=t
  for vi,lead in items:
    t+=lead; clips.append({'i':vi,'t':round(t,3)})
    for w in vo[vi]['words']: caps.append({'w':w['w'],'s':round(t+w['s'],3),'e':round(t+w['e'],3),'line':vi})
    t+=vo[vi]['dur']
  t+=tail; scenes.append({'id':sid,'s':round(st,3),'e':round(t,3)})
json.dump({'total':round(t,3),'scenes':scenes,'clips':clips,'caps':caps},open('timeline.json','w'),indent=1)
for s in scenes: print(s, round(s['e']-s['s'],2))
print('total',t)
