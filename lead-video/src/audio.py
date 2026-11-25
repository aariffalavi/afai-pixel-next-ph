import numpy as np, json, wave, subprocess
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.2; N=int(T*SR)
rng=np.random.default_rng(1)
def env(n,a,d):
    t=np.arange(n)/SR; return np.minimum(1,t/max(a,1e-4))*np.exp(-t/d)
mus=np.zeros(N)
bpm=112; beat=60/bpm
def add(buf,sig,t):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if i<len(buf): buf[i:j]+=sig[:j-i]
# kick
def kick():
    n=int(.35*SR);t=np.arange(n)/SR;f=45+90*np.exp(-t*30);ph=2*np.pi*np.cumsum(f)/SR;return np.sin(ph)*np.exp(-t*9)
def hat():
    n=int(.06*SR);x=rng.standard_normal(n);x=np.diff(np.concatenate([[0],x]));return x*np.exp(-np.arange(n)/SR*70)*.25
def clap():
    n=int(.18*SR);x=rng.standard_normal(n);x=x-np.convolve(x,np.ones(30)/30,'same');return x*np.exp(-np.arange(n)/SR*22)*.35
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
mf=lambda m:440*2**((m-69)/12)
def pad(notes,dur):
    n=int(dur*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for m in notes:
        for det in (-0.08,0.08): s+=np.sin(2*np.pi*mf(m+12)*(1+det/100)*t)+0.3*np.sin(2*np.pi*mf(m+24)*t)
    e=np.minimum(1,t/0.4)*np.minimum(1,(dur-t)/0.4);return s*e*0.035
def bass(m,dur):
    n=int(dur*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*mf(m-12)*t)+0.25*np.sin(2*np.pi*mf(m)*t))*np.exp(-t*2.5)*0.22
bar=beat*4; nb=int(T/bar)+1
start_drums=0.0
for b in range(nb):
    t0=b*bar; c=chords[b%4]
    add(mus,pad(c,bar),t0)
    for k in range(4):
        tb=t0+k*beat
        add(mus,kick()*0.55,tb)
        add(mus,bass(c[0],beat*0.9),tb+beat*0.5)
        if k in(1,3): add(mus,clap(),tb)
        add(mus,hat(),tb+beat/2); 
        if b%2: add(mus,hat()*.6,tb+beat*0.75)
# fade in/out, duck under VO
fade=np.ones(N); fi=int(.15*SR); fade[:fi]=np.linspace(0,1,fi); fo=int(1.5*SR); fade[-fo:]=np.linspace(1,0,fo)
mus*=fade
# VO track
vo=np.zeros(N)
def readwav(p):
    w=wave.open(p);a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768;return a
for c in tl['clips']: add(vo,readwav(f"vo/{c['i']}.wav")*1.0,c['t'])
# sidechain duck
absv=np.abs(vo); k=int(.25*SR); envv=np.convolve(absv,np.ones(k)/k,'same'); duck=1-0.55*np.clip(envv*12,0,1)
mus*=duck
# sfx
sfx=np.zeros(N)
def whoosh(d=.45):
    n=int(d*SR);x=rng.standard_normal(n);t=np.arange(n)/SR
    # sweeping lowpass via cumulative one-pole with varying coeff
    y=np.zeros(n);a=np.linspace(.02,.35,n)**1.2;a=np.concatenate([a[:n//2],a[n//2::-1]])[:n] if False else np.interp(t,[0,d*.6,d],[.02,.4,.05]);s=0
    for i in range(n): s+=a[i]*(x[i]-s); y[i]=s
    e=np.sin(np.pi*t/d)**2; return y*e*0.9
def pop():
    n=int(.12*SR);t=np.arange(n)/SR;f=500+900*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*35)*0.25
def tick():
    n=int(.03*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*2400*t)*np.exp(-t*200)*0.18
def ding():
    n=int(.8*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1318*t)+.5*np.sin(2*np.pi*1975*t))*np.exp(-t*5)*0.18
W=whoosh()
for s_ in tl['scenes'][1:]: add(sfx,W,s_['s']-0.12)
def buzz():
    n=int(.22*SR);t=np.arange(n)/SR;x=np.sign(np.sin(2*np.pi*140*t))*0.5+np.sin(2*np.pi*70*t)*0.5;return x*np.exp(-t*10)*0.16
caps=tl['caps']
def wt(line,w):
    for c in caps:
        if c['line']==line and c['w'].lower().replace("'","").startswith(w): return c['s']
sc={s_['id']:s_ for s_ in tl['scenes']}
for i in range(6): add(sfx,pop()*1.2,caps[i]['s'])
add(sfx,pop()*2,sc['signs']['s']+0.05)
for k in ('s1','s2','s3'): add(sfx,buzz(),sc[k]['s']+0.1)
add(sfx,pop(),wt(2,'slow'));add(sfx,buzz()*0.8,wt(4,'nobody'))
for j in range(5): add(sfx,pop()*0.8,wt(3,'see')-0.3+j*0.35)
for i in range(14): add(sfx,tick()*0.6,sc['s3']['s']+0.45+i*0.06)
for w in ('fast','clear','enquiries'): add(sfx,pop()*1.3,wt(5,w))
for i in range(4): add(sfx,pop()*0.9,sc['proof']['s']+i*40/30)
for i in range(5): add(sfx,tick()*1.5,sc['reviews']['s']+0.35+i*0.12)
add(sfx,pop()*1.8,wt(8,'back'))
t0=sc['comment']['s']+0.75
for i in range(5): add(sfx,tick(),t0+i*0.1)
sent=t0+0.85; add(sfx,pop()*1.4,sent); add(sfx,ding(),max(sent+1.1,wt(9,'send')-0.2))
mix=vo*0.95+mus*0.3+sfx*0.6
mix/=max(1,np.abs(mix).max()/0.95)
pcm=(mix*32767).astype(np.int16)
w=wave.open('mix.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes());w.close()
print('ok',T)
