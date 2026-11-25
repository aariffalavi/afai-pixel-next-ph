import json
vo=json.load(open('vo/vo.json'))
starts=[0.4,3.75,8.3,13.5,14.85,21.95,26.6,33.2,36.5,41.4]
caps=[0,1,1,1,1,1,1,0,1,0]   # 0 = scene text already says it
for v,s,c in zip(vo,starts,caps): v['start']=s; v['cap']=c
scenes=[["hook",0,3.95],["push",3.95,8.05],["chart",8.05,13.3],["example",13.3,26.3],["real",26.3,33.0],["toggle",33.0,36.2],["comment",36.2,41.3],["outro",41.3,45.6]]
impact=43.62
json.dump({"total":45.6,"impact":impact,"vo":vo,"scenes":scenes},open('timeline.json','w'),indent=1)
