# Music bed + chalk/whistle/crowd SFX + voice-over mix -> mix.wav
import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.3; N=int(T*SR)
rng=np.random.default_rng(3)
def add(buf,sig,t):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]
mf=lambda m:440*2**((m-69)/12)
def lp(x,a):  # one-pole lowpass (vectorised via lfilter-like loop on chunks)
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
# ---- music: original drift-phonk bed (see phonk.py); drops at the #10 scene
from phonk import phonk
drop=[x for x in tl['scenes'] if x['id']=='t10'][0]['s']
mus_hi,mus_lo=phonk(T,SR,drop,rng)
mus=mus_hi+mus_lo
fade=np.ones(N);fo=int(2.0*SR);fade[-fo:]=np.linspace(1,0,fo);mus*=fade
# ---- VO
vo=np.zeros(N)
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
for c in tl['clips']: add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
k=int(.2*SR);envv=np.convolve(np.abs(vo),np.ones(k)/k,'same');mus*=1-0.7*np.clip(envv*14,0,1)
# ---- SFX
sfx=np.zeros(N)
def chalk(d):  # scratchy chalk stroke
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);x=np.diff(np.concatenate([[0],x]));x=np.diff(np.concatenate([[0],x]))
    am=(0.5+0.5*np.sin(2*np.pi*(9+4*rng.random())*t+rng.random()*6))**2;e=np.minimum(1,t/.03)*np.minimum(1,(d-t)/.05)
    return x*am*e*.035
def erase(d=.42):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=lp(x,.12);am=.6+.4*np.sin(2*np.pi*14*t)
    return y*am*np.sin(np.pi*t/d)**1.5*.9
def whistle(d=.7):
    n=int(d*SR);t=np.arange(n)/SR;f=2900+120*np.sin(2*np.pi*30*t);s=np.sin(2*np.pi*np.cumsum(f)/SR)
    s*= (0.7+0.3*(np.sin(2*np.pi*30*t)>0));return s*np.minimum(1,t/.02)*np.minimum(1,(d-t)/.08)*.12
def crowd(d=2.4):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=lp(x,.08)-lp(x,.008)
    return y*np.minimum(1,t/.25)*np.exp(-np.maximum(0,t-.6)*1.4)*1.6
def pop():
    n=int(.12*SR);t=np.arange(n)/SR;f=380+800*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*.22
def kickball():
    n=int(.12*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*np.cumsum(120+200*np.exp(-t*60))/SR)+.4*rng.standard_normal(n)*np.exp(-t*80))*np.exp(-t*30)*.35
for s in tl['scenes']:
    t0=s['s'];m=s['marks']
    if s['id']!='hook': add(sfx,erase(),t0)
    add(sfx,pop(),t0+.1)
    if s['id'].startswith('t') and m:
        for x in m[:3]: add(sfx,chalk(1.1),t0+x-.35)
        add(sfx,chalk(.7),t0+m[3])
    if s['id']=='hook': add(sfx,chalk(1.2),.1);add(sfx,chalk(1.4),1.3)
    if s['id']=='ex1':
        tS=t0+m[4]+.25;tF=t0+m[8]+.35;add(sfx,kickball(),tS);add(sfx,kickball()*.6,t0+m[6]);add(sfx,kickball(),tF)
        add(sfx,crowd(),tF+.1);add(sfx,whistle(.25),tF+.15)
    if s['id']=='ex2':
        tF=t0+m[2]+.25;add(sfx,kickball(),tF);add(sfx,crowd(2.8),tF+.1)
        add(sfx,whistle(.35),t0+m[4]-.2);add(sfx,whistle(.35),t0+m[4]+.25);add(sfx,whistle(.9),t0+m[4]+.7)
mix=mus*0.26+vo*1.3+sfx
mix/=max(1,np.max(np.abs(mix))/0.97)
w=wave.open('mix.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
print('ok',T,np.max(np.abs(mix)))
