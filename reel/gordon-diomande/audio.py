import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); goals=json.load(open('goals.json'))
T=tl['total']+0.2; N=int(T*SR); rng=np.random.default_rng(3)
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]*g
def lp(x,a):  # one-pole lowpass, vectorised via cumulative filter approximation
    from scipy.signal import lfilter; return lfilter([a],[1,a-1],x)
mf=lambda m:440*2**((m-69)/12)
# ---- music: driving 4/4 at 124 bpm, minor key
bpm=124;beat=60/bpm;bar=beat*4
def kick():
    n=int(.32*SR);t=np.arange(n)/SR;f=48+110*np.exp(-t*32);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)
def snare():
    n=int(.2*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);x=x-np.convolve(x,np.ones(20)/20,'same');return (x*.5+np.sin(2*np.pi*190*t)*.5)*np.exp(-t*20)*.4
def hat(o=False):
    n=int((.18 if o else .05)*SR);x=np.diff(np.concatenate([[0],rng.standard_normal(n)]));return x*np.exp(-np.arange(n)/SR*(18 if o else 80))*.18
def saw(f,n):
    t=np.arange(n)/SR;return 2*((t*f)%1)-1
def bassn(m,d):
    n=int(d*SR);s=saw(mf(m-24),n)*.6+np.sin(2*np.pi*mf(m-24)*np.arange(n)/SR);return lp(s,.08)*np.exp(-np.arange(n)/SR*3)*.35
def pad(ns,d):
    n=int(d*SR);t=np.arange(n)/SR;s=sum(saw(mf(m)*(1+dt),n) for m in ns for dt in(-.003,.003))
    s=lp(s,.04);e=np.minimum(1,t/.3)*np.minimum(1,(d-t)/.3);return s*e*.05
def pluck(m,d=.25):
    n=int(d*SR);t=np.arange(n)/SR;return lp(saw(mf(m),n),.25)*np.exp(-t*14)*.09
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
arp=[0,1,2,1]
mus=np.zeros(N);nb=int(T/bar)+1
for b in range(nb):
    t0=b*bar;c=prog[b%4];add(mus,pad([x+12 for x in c],bar),t0)
    for k in range(4):
        tb=t0+k*beat;add(mus,kick(),tb,.6)
        if k in(1,3):add(mus,snare(),tb)
        add(mus,hat(),tb+beat/2);add(mus,hat(),tb+beat*.25,.5);add(mus,hat(),tb+beat*.75,.5)
        add(mus,bassn(c[0],beat*.45),tb);add(mus,bassn(c[0],beat*.45),tb+beat/2)
        for q in range(2):add(mus,pluck(c[arp[(k*2+q)%4]]+24),tb+q*beat/2)
fade=np.ones(N);fi=int(.1*SR);fade[:fi]=np.linspace(0,1,fi);fo=int(2*SR);fade[-fo:]=np.linspace(1,0,fo);mus*=fade
# ---- VO
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
vo=np.zeros(N)
for c in tl['clips']:add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
env=np.convolve(np.abs(vo),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-.6*np.clip(env*12,0,1)
# ---- crowd: ambience during pitch scenes + roars at goals
crowd=lp(rng.standard_normal(N),.06)*.5+lp(rng.standard_normal(N),.2)*.15
lvl=np.zeros(N)
for s in tl['scenes']:
    g=.25 if s['id'] in('hook','g1','g23','d1','d2','d3','ex') else .1
    i,j=int(s['s']*SR),int(s['e']*SR);lvl[i:j]=g
lvl=np.convolve(lvl,np.ones(int(.3*SR))/int(.3*SR),'same')
for gt in goals:
    n=int(3.2*SR);t=np.arange(n)/SR;roar=np.minimum(1,t/.15)*np.exp(-np.maximum(0,t-.6)*1.3)
    i=int((gt-.05)*SR);j=min(N,i+n);lvl[i:j]+=roar[:j-i]*1.1
crowd*=lvl
sfx=np.zeros(N)
def whoosh(d=.5):
    n=int(d*SR);x=rng.standard_normal(n);t=np.arange(n)/SR;return lp(x,.15)*np.sin(np.pi*t/d)**2*.7
def boom():
    n=int(1.2*SR);t=np.arange(n)/SR;f=60*np.exp(-t*2)+30;return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)*.8
def pop():
    n=int(.12*SR);t=np.arange(n)/SR;f=500+900*np.exp(-t*40);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*35)*.25
def tick():
    n=int(.03*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*2400*t)*np.exp(-t*200)*.18
for s in tl['scenes'][1:]:add(sfx,whoosh(),s['s']-.15)
add(sfx,boom(),0.0);add(sfx,boom(),1.2,.7)
for gt in goals:add(sfx,boom(),gt,.6)
sc={s['id']:s for s in tl['scenes']}
for k in range(4):add(sfx,pop(),sc['gcard']['s']+1.0+k*.6);add(sfx,pop(),sc['dcard']['s']+1.0+k*.6)
c0=sc['comment']['s'];add(sfx,pop()*1.5,c0+.6);add(sfx,pop()*1.5,c0+.85)
for k in range(19):add(sfx,tick(),c0+3.1+k*.07)
add(sfx,pop()*1.4,c0+3.1+19*.07+.3)
mix=vo*1.0+mus*duck*.22+crowd*.35+sfx*.5
mix/=max(1,np.abs(mix).max()/.95)
pcm=(mix*32767).astype(np.int16)
w=wave.open('mix.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes());w.close()
print('ok',T,'peak',np.abs(mix).max())
