import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); T=tl['total']+0.3; N=int(T*SR)
rng=np.random.default_rng(7)
def add(buf,sig,t):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]
mf=lambda m:440*2**((m-69)/12)
sc={s['id']:s for s in tl['scenes']}
mus=np.zeros(N)
bpm=80; beat=60/bpm; bar=beat*4
chords=[[57,60,64,71],[53,57,60,64],[48,52,55,62],[55,59,62,64]]
def pad(notes,dur):
    n=int(dur*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for m in notes:
        for det in (-0.12,0,0.12):
            f=mf(m)*(1+det/100);s+=np.sin(2*np.pi*f*t)+0.18*np.sin(2*np.pi*2*f*t+1)
    e=np.minimum(1,t/1.2)*np.minimum(1,(dur-t)/1.0);return s*e*0.018
def pluck(m,d=1.6):
    n=int(d*SR);t=np.arange(n)/SR;f=mf(m)
    return (np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*2*f*t)+0.12*np.sin(2*np.pi*3*f*t))*np.exp(-t*3.2)*np.minimum(1,t/0.004)*0.08
def sub(d=0.5):
    n=int(d*SR);t=np.arange(n)/SR;f=38+40*np.exp(-t*25);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7)*0.32
def boom():
    n=int(2.5*SR);t=np.arange(n)/SR;f=30+60*np.exp(-t*6);x=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*1.6)
    nz=rng.standard_normal(n);nz=np.convolve(nz,np.ones(80)/80,'same')*np.exp(-t*4)*0.6;return (x+nz)*0.45
def riser(d=1.2):
    n=int(d*SR);t=np.arange(n)/SR;x=rng.standard_normal(n);y=np.zeros(n);s=0;a=np.linspace(0.01,0.25,n)
    for i in range(n): s+=a[i]*(x[i]-s);y[i]=s
    return y*(t/d)**2*0.5
def shimmer():
    n=int(2.2*SR);t=np.arange(n)/SR;s=np.zeros(n)
    for k,m in enumerate([84,88,91,96]):
        tt=np.clip(t-k*0.12,0,None);s+=np.sin(2*np.pi*mf(m)*tt)*np.exp(-tt*2.5)*(t>k*0.12)
    return s*0.05
def msgpop():
    n=int(.15*SR);t=np.arange(n)/SR;f=700+500*np.exp(-t*50);return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.18
for b in range(int(T/bar)+1):
    c=chords[b%4];add(mus,pad(c,bar+1.0),b*bar)
# plucks from brand scene
for k in range(int((T-sc['brand']['s'])/(beat/2))):
    tt=sc['brand']['s']+k*beat/2
    if tt>sc['logo']['s']+1.5: break
    b=int(tt/bar);c=chords[b%4];arp=[c[0]+12,c[1]+12,c[2]+12,c[3]+12,c[2]+12,c[1]+12]
    add(mus,pluck(arp[k%6]),tt)
# pulse
k=0;tt=sc['design']['s']
while tt<sc['dm']['e']-0.5:
    add(mus,sub(),tt);add(mus,sub()*0.5,tt+0.22);tt+=beat
sfx=np.zeros(N)
for sid in ('design','world','logo'):
    add(sfx,riser(),sc[sid]['s']-1.2)
for sid,off in (('brand',0.35),('world',0.0),('logo',0.2),('rating',0.05)):
    add(sfx,boom()*(0.7 if sid=='rating' else 1),sc[sid]['s']+off)
add(sfx,shimmer(),sc['logo']['s']+1.3)
t0=sc['dm']['s']+0.9;msg='Hi! I need a new website for my business 👋';sent=t0+len(msg)*0.045+0.3
for i in range(len(msg)):
    if i%2==0: add(sfx,np.sin(2*np.pi*2600*np.arange(int(.02*SR))/SR)*np.exp(-np.arange(int(.02*SR))/SR*250)*0.05,t0+i*0.045)
for tt in (sent,sent+1.8,sent+2.6): add(sfx,msgpop(),tt)
vo=np.zeros(N)
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
for c in tl['clips']: add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
env=np.convolve(np.abs(vo),np.ones(int(.3*SR))/int(.3*SR),'same');duck=1-0.45*np.clip(env*12,0,1)
fade=np.ones(N);fi=int(.8*SR);fade[:fi]=np.linspace(0,1,fi);fo=int(2.5*SR);fade[-fo:]=np.linspace(1,0,fo)
bed=(mus*duck)*0.55*fade+sfx*0.6*fade
mix=vo+bed
# simple reverb on music/sfx feel: add short delays
mix/=max(1,np.abs(mix).max()/0.95)
g=max(1,np.abs(vo+bed).max()/0.95)
for nm,x in (('vo.wav',vo/g),('bed.wav',bed/g)):
    w=wave.open(nm,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype(np.int16).tobytes());w.close()
m=mus*0.55;mask=env>0.01
r=lambda x:20*np.log10(np.sqrt(np.mean(x**2))+1e-9)
print('vo',r(vo[mask]),'music under vo',r((m*duck)[mask]))
