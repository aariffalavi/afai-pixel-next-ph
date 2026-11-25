import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.3; N=int(T*SR)
rng=np.random.default_rng(9); sc={s['id']:s for s in tl['scenes']}
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]*g
mf=lambda m:440*2**((m-69)/12)
def kick():
    n=int(.4*SR);t=np.arange(n)/SR;f=45+120*np.exp(-t*30);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)*0.7
def clap():
    n=int(.25*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);x=x-np.convolve(x,np.ones(25)/25,'same');e=np.exp(-t*18)*(1+0.6*(np.sin(2*np.pi*90*t)>0)*(t<.03));return x*e*0.3
def hat(o=False):
    n=int((.18 if o else .04)*SR);x=np.diff(np.concatenate([[0],rng.standard_normal(n)]));return x*np.exp(-np.arange(n)/SR*(20 if o else 80))*0.12
def bass(m,d):
    n=int(d*SR);t=np.arange(n)/SR;f=mf(m-24);s=np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t);return s*np.minimum(1,t/0.01)*np.exp(-t*3)*0.32
def chord(notes,d):
    n=int(d*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for m in notes:
        for det in (-0.1,0.1):s+=np.sign(np.sin(2*np.pi*mf(m)*(1+det/100)*t))*0.25+np.sin(2*np.pi*mf(m)*t)*0.6
    # low-pass
    k=40;s=np.convolve(s,np.ones(k)/k,'same');return s*np.exp(-t*4)*np.minimum(1,t/0.005)*0.05
def riser(d=1.0):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=np.zeros(n);s=0;a=np.linspace(0.02,0.35,n)
    for i in range(n): s+=a[i]*(x[i]-s);y[i]=s
    return y*(t/d)**2*0.45
def hit():
    n=int(1.2*SR);t=np.arange(n)/SR;f=40+80*np.exp(-t*12);return (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3)+np.convolve(rng.standard_normal(n),np.ones(30)/30,'same')*np.exp(-t*10)*0.8)*0.5
def tick():
    n=int(.025*SR);t=np.arange(n)/SR;return np.sin(2*np.pi*2200*t)*np.exp(-t*240)*0.14
bpm=124;beat=60/bpm;bar=beat*4
prog=[[62,65,69],[58,62,65],[60,64,67],[57,60,64]]  # Dm Bb C Am
mus=np.zeros(N)
for b in range(int(T/bar)+1):
    t0=b*bar;c=prog[b%4]
    for k in range(4):
        add(mus,kick(),t0+k*beat)
        add(mus,hat(),t0+k*beat+beat/2);add(mus,hat(True)*0.6,t0+k*beat+beat*0.75) if k%2 else None
        if k in (1,3):add(mus,clap(),t0+k*beat)
    for k in range(8):add(mus,bass(c[0],beat/2*0.9),t0+k*beat/2)
    for k in (0,3,6):add(mus,chord([c[0]+12,c[1]+12,c[2]+12],0.5),t0+k*beat/2)
fx=np.zeros(N)
for s_ in tl['scenes'][1:]:add(fx,riser(0.45),s_['s']-0.45);add(fx,hit()*0.45,s_['s'])
caps=tl['caps']
def wt(l,w):
    for c in caps:
        if c['line']==l and c['w'].lower().startswith(w):return c['s']
for tt in (wt(0,'black'),wt(0,'friday')):add(fx,hit()*0.8,tt)
add(fx,riser(0.9),wt(1,'twenty')-0.9);add(fx,hit()*1.3,wt(1,'twenty'));add(fx,hit()*0.8,wt(1,'off'))
add(fx,hit()*1.2,wt(6,'all'));add(fx,hit(),wt(8,'claim'))
for w in ('starter','business','online'):add(fx,hit()*0.6,wt(5,w)+0.25)
for w in ('custom','mobile','built'):add(fx,tick()*2.5,wt(4,w))
for i in range(int(1.9/0.25)):add(fx,tick()*1.2,tl['scenes'][5]['s']+i*0.25)
vo=np.zeros(N)
def rw(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
for c in tl['clips']:add(vo,rw(f"vo/{c['i']}.wav"),c['t'])
env=np.convolve(np.abs(vo),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-0.5*np.clip(env*12,0,1)
fade=np.ones(N);fi=int(.02*SR);fade[:fi]=np.linspace(0,1,fi);fo=int(1.5*SR);fade[-fo:]=np.linspace(1,0,fo)
bed=(mus*0.2*duck+fx*0.24)*fade
g=max(1,np.abs(vo+bed).max()/0.95)
for nm,xx in (('vo.wav',vo/g),('bed.wav',bed/g)):
    w=wave.open(nm,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((xx*32767).astype(np.int16).tobytes());w.close()
mask=env>0.01;r=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
print('vo',round(r(vo[mask]),1),'bed under vo',round(r(bed[mask]),1))
