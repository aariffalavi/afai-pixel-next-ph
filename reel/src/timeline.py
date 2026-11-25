import json
vo=json.load(open('vo/vo.json'))
plan=[('hook',[(0,0.45)],0.3),('brand',[(1,0.25)],0.9),('hero',[(2,0.3)],0.3),('services',[(3,0.2)],0.3),('case',[(4,0.25),(5,0.3)],0.35),('reviews',[(6,0.3)],0.4),('comment',[(7,0.25)],1.3),('outro',[(8,0.35)],1.2)]
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
