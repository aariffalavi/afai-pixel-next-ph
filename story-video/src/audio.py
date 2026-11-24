import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.3; N=int(T*SR)
rng=np.random.default_rng(11)
sc={s['id']:s for s in tl['scenes']}
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]*g
mf=lambda m:440*2**((m-69)/12)
def piano(m,d=3.0,v=1.0):
    n=int(d*SR);t=np.arange(n)/SR;f=mf(m);s=np.zeros(n)
    for h,a in ((1,1),(2,.45),(3,.22),(4,.12),(5,.06)):
        s+=a*np.sin(2*np.pi*f*h*t*(1+0.0004*h))*np.exp(-t*(1.6+h*0.7))
    return s*np.minimum(1,t/0.005)*0.12*v
def strings(notes,d,v=1.0):
    n=int(d*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for m in notes:
        for det in (-0.15,0.0,0.15):
            f=mf(m)*(1+det/100);vib=1+0.003*np.sin(2*np.pi*5*t)
            for h,a in ((1,1),(2,.3),(3,.12)): s+=a*np.sin(2*np.pi*f*h*np.cumsum(vib)/SR)
    e=np.minimum(1,t/1.5)*np.minimum(1,(d-t)/1.2);return s*e*0.012*v
bpm=68;beat=60/bpm;bar=beat*4
prog=[[48,55,64],[43,50,59],[45,52,60],[41,48,57]]  # C G Am F
mel=[76,74,72,74, 71,72,74,67, 72,71,69,72, 69,67,65,72]
mus=np.zeros(N)
def intensity(t):
    k=0.35
    if t>sc['heart']['s']:k=0.5
    if t>sc['past']['s']:k=0.4
    if t>sc['seen']['s']:k=0.55
    if t>sc['build']['s']:k=0.8
    if t>sc['oneday']['s']:k=0.3
    if t>sc['first']['s']:k=1.0
    if t>sc['why']['s']:k=0.85
    if t>sc['cta']['s']:k=0.95
    if t>sc['logo']['s']+2:k=0.5
    return k
nb=int(T/bar)+1
for b in range(nb):
    t0=b*bar;c=prog[b%4];I=intensity(t0+0.1)
    # left hand
    add(mus,piano(c[0]-12,4.0,0.8),t0);add(mus,piano(c[0],3.0,0.5*I),t0+beat*2)
    # arpeggio
    if I>=0.4:
        for k,m in enumerate([c[0]+12,c[1]+12,c[2]+12,c[1]+12]):add(mus,piano(m,2.0,0.45*I),t0+k*beat)
    # melody
    if t0>sc['dawn']['s']+2 and I>=0.35:
        for k in range(4):add(mus,piano(mel[(b%4)*4+k],2.5,0.7),t0+k*beat+0.02)
    # strings
    if I>=0.5:add(mus,strings([c[0]+12,c[1]+12,c[2]+12],bar+1.2,(I-0.4)*2.2),t0)
    if I>=0.95:add(mus,strings([c[0]-12,c[0]],bar+1.2,1.4),t0)
sfx=np.zeros(N)
# rain
ps=sc['past'];n=int((ps['e']-ps['s']+3)*SR);x=rng.standard_normal(n);x=np.convolve(x,np.ones(6)/6,'same');tt=np.arange(n)/SR;env=np.minimum(1,tt/1.2)*np.minimum(1,(tt[-1]-tt)/1.5)
add(sfx,x*env*0.05,ps['s']+0.3)
# heartbeat in seen
def thump():
    n=int(.35*SR);t=np.arange(n)/SR;f=45+30*np.exp(-t*20);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*10)*0.5
se=sc['seen']
k=0
while se['s']+0.6+k*1.21<sc['build']['s']+0.5:
    tb=se['s']+0.6+k*1.21;add(sfx,thump(),tb);add(sfx,thump()*0.6,tb+0.25);k+=1
# pixel shimmer swirl
def shimmer(d=2.5):
    n=int(d*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for i,m in enumerate([84,88,91,95,96,100]):
        tt2=np.clip(t-i*0.15,0,None);s+=np.sin(2*np.pi*mf(m)*tt2)*np.exp(-tt2*2)*(t>i*0.15)
    return s*0.04
add(sfx,shimmer(),sc['build']['s']+0.1)
# chimes for notifications
def chime():
    n=int(1.2*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1046*t)+0.6*np.sin(2*np.pi*1568*t*1.0))*np.exp(-t*4)*0.10
caps=tl['caps']
def wt(l,w):
    for c in caps:
        if c['line']==l and c['w'].lower().startswith(w):return c['s']
for w in ('message','order','stranger'):add(sfx,chime(),wt(7,w)-0.05)
# door bell when people enter
def bell():
    n=int(1.6*SR);t=np.arange(n)/SR;return sum(np.sin(2*np.pi*f*t)*np.exp(-t*3) for f in (1318,1760,2637))*0.05
add(sfx,bell(),sc['first']['s']+4.6+2.0)
add(sfx,bell()*0.7,sc['first']['s']+4.6+2.55)
# soft impact at cta and logo
def swell(d=1.5):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);x=np.convolve(x,np.ones(200)/200,'same');return x*(t/d)**2*0.6
add(sfx,swell(),sc['build']['s']-1.4);add(sfx,swell(),sc['first']['s']-1.4);add(sfx,shimmer(),sc['logo']['s']+1.2)
vo=np.zeros(N)
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
for c in tl['clips']:add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
envv=np.convolve(np.abs(vo),np.ones(int(.3*SR))/int(.3*SR),'same');duck=1-0.35*np.clip(envv*12,0,1)
fade=np.ones(N);fi=int(1.0*SR);fade[:fi]=np.linspace(0,1,fi);fo=int(3*SR);fade[-fo:]=np.linspace(1,0,fo)
bed=(mus*duck*0.75+sfx*0.8)*fade
g=max(1,np.abs(vo+bed).max()/0.95)
for nm,xx in (('vo.wav',vo/g),('bed.wav',bed/g)):
    w=wave.open(nm,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((xx*32767).astype(np.int16).tobytes());w.close()
mask=envv>0.01;r=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
print('vo',r(vo[mask]),'bed under vo',r(bed[mask]))
