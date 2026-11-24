import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.3; N=int(T*SR)
rng=np.random.default_rng(5); sc={s['id']:s for s in tl['scenes']}
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]*g
mf=lambda m:440*2**((m-69)/12)
def piano(m,d=2.5,v=1.0):
    n=int(d*SR);t=np.arange(n)/SR;f=mf(m);s=sum(a*np.sin(2*np.pi*f*h*t)*np.exp(-t*(1.8+h*0.8)) for h,a in ((1,1),(2,.4),(3,.18),(4,.08)))
    return s*np.minimum(1,t/0.004)*0.11*v
def pad(notes,d,v=1.0):
    n=int(d*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for m in notes:
        for det in (-0.14,0,0.14):
            f=mf(m)*(1+det/100);s+=np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*2*f*t)+0.1*np.sin(2*np.pi*3*f*t)
    e=np.minimum(1,t/1.0)*np.minimum(1,(d-t)/0.8);return s*e*0.011*v
def kick():
    n=int(.45*SR);t=np.arange(n)/SR;f=42+110*np.exp(-t*28);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)*0.6
def snare():
    n=int(.3*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);x=x-np.convolve(x,np.ones(20)/20,'same');return (x*0.6+np.sin(2*np.pi*190*t)*0.5)*np.exp(-t*14)*0.32
def hat(o=False):
    n=int((.2 if o else .05)*SR);x=rng.standard_normal(n);x=np.diff(np.concatenate([[0],x]));return x*np.exp(-np.arange(n)/SR*(18 if o else 70))*0.13
def boom():
    n=int(3*SR);t=np.arange(n)/SR;f=28+70*np.exp(-t*5);x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*1.4)
    nz=np.convolve(rng.standard_normal(n),np.ones(60)/60,'same')*np.exp(-t*3)*0.7;return (x+nz)*0.55
def riser(d=1.5):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=np.zeros(n);s=0;a=np.linspace(0.01,0.3,n)
    for i in range(n): s+=a[i]*(x[i]-s);y[i]=s
    sw=np.sin(2*np.pi*np.cumsum(np.linspace(200,1200,n))/SR)*0.15
    return (y+sw)*(t/d)**2.2*0.55
def whoosh(d=.6):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=np.zeros(n);s=0;a=np.interp(t,[0,d*.5,d],[.02,.35,.03])
    for i in range(n): s+=a[i]*(x[i]-s);y[i]=s
    return y*np.sin(np.pi*t/d)**2*0.6
def shimmer():
    n=int(2.5*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for k,m in enumerate([84,88,91,96,100]):
        tt=np.clip(t-k*0.1,0,None);s+=np.sin(2*np.pi*mf(m)*tt)*np.exp(-tt*2.2)*(t>k*0.1)
    return s*0.045
def tick():
    n=int(.03*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*2400*t)*np.exp(-t*220)*0.12
bpm=100;beat=60/bpm;bar=beat*4
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]
mus=np.zeros(N);drums=np.zeros(N)
def level(t):
    if t<sc['s2']['s']:return 0
    if t<sc['s3']['s']:return 1
    if t<sc['s4']['s']:return 2
    if t<sc['s6']['s']:return 3
    if t<sc['s7']['s']+3:return 4
    return 2
for b in range(int(T/bar)+1):
    t0=b*bar;c=prog[b%4];L=level(t0+0.01)
    add(mus,pad([c[0]-12,c[0],c[1],c[2]],bar+0.9,1.0+0.3*L),t0)
    add(mus,piano(c[0]-24,3.0,0.9),t0)
    arp=[c[0]+12,c[1]+12,c[2]+12,c[1]+24,c[2]+12,c[1]+12,c[0]+12,c[2]+12]
    for k in range(8):add(mus,piano(arp[k],1.6,0.55+0.1*L),t0+k*beat/2)
    if L>=1:
        for k in range(4):add(drums,kick()*(0.6 if L==1 else 1),t0+k*beat) if (L>=2 or k%2==0) else None
    if L>=2:
        for k in (1,3):add(drums,snare(),t0+k*beat)
        for k in range(8):add(drums,hat(k%2==1),t0+k*beat/2)
    if L>=3:
        for k in range(16):
            if k%4==2:add(drums,hat(),t0+k*beat/4)
fx=np.zeros(N)
for sid in ('s2','s3','s4','s5','s6','s7'):add(fx,whoosh(),sc[sid]['s']-0.3)
add(fx,riser(),sc['s3']['s']-1.5);add(fx,boom(),sc['s3']['s']+0.2);add(fx,shimmer(),sc['s3']['s']+1.0)
caps=tl['caps']
def wt(l,w):
    for c in caps:
        if c['line']==l and c['w'].lower().replace("'","").startswith(w):return c['s']
add(fx,boom()*0.7,wt(1,'stand')-0.05)
add(fx,riser(1.2),sc['s7']['s']-0.2);add(fx,boom(),sc['s7']['s']+1.0);add(fx,shimmer(),sc['s7']['s']+1.8)
slot=(sc['s4']['e']-0.3-(sc['s4']['s']+0.4))/6
for i in range(6):add(fx,whoosh(.4)*0.7,sc['s4']['s']+0.4+i*slot-0.1)
for w in ('australia','europe','uk','usa','canada','middle'):
    t=wt(4,w)
    if t: add(fx,shimmer()*0.5,t+0.4)
for i in range(18):add(fx,tick(),sc['s1']['s']+0.8+i*0.06)
vo=np.zeros(N)
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
for c in tl['clips']:add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
env=np.convolve(np.abs(vo),np.ones(int(.3*SR))/int(.3*SR),'same');duck=1-0.5*np.clip(env*12,0,1)
fade=np.ones(N);fi=int(1.0*SR);fade[:fi]=np.linspace(0,1,fi);fo=int(2.0*SR);fade[-fo:]=np.linspace(1,0,fo)
bed=((mus*0.3+drums*0.22)*duck+fx*0.28)*fade
g=max(1,np.abs(vo+bed).max()/0.95)
for nm,xx in (('vo.wav',vo/g),('bed.wav',bed/g)):
    w=wave.open(nm,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((xx*32767).astype(np.int16).tobytes());w.close()
mask=env>0.01;r=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
print('vo',round(r(vo[mask]),1),'bed under vo',round(r(bed[mask]),1))
