import numpy as np, json, wave
SR=48000; tl=json.load(open('timeline.json')); goals=json.load(open('goals.json'))
T=tl['total']+0.2; N=int(T*SR); rng=np.random.default_rng(3)
def add(buf,sig,t,g=1.0):
    i=int(t*SR); j=min(len(buf),i+len(sig))
    if 0<=i<len(buf): buf[i:j]+=sig[:j-i]*g
def lp(x,a):  # one-pole lowpass, vectorised via cumulative filter approximation
    from scipy.signal import lfilter; return lfilter([a],[1,a-1],x)
mf=lambda m:440*2**((m-69)/12)
# ---- music: original drift-phonk beat, 130 bpm
from scipy.signal import butter,sosfilt
def bp(x,lo,hi):return sosfilt(butter(2,[lo,hi],'bandpass',fs=SR,output='sos'),x)
def hp(x,f):return sosfilt(butter(2,f,'highpass',fs=SR,output='sos'),x)
bpm=130;st=60/bpm/4;bar=st*16;ROOT=42  # F#2
def sq(f,n):t=np.arange(n)/SR;return np.sign(np.sin(2*np.pi*f*t))
def cowbell(semi,d=.32):
    n=int(d*SR);r=2**(semi/12);x=sq(587*r,n)*.6+sq(845*r,n)*.6
    x=bp(x,500*r,2600*r);t=np.arange(n)/SR;return np.tanh(x*2)*np.exp(-t*9)*.32
def kick():
    n=int(.45*SR);t=np.arange(n)/SR;f=40+170*np.exp(-t*28);return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*6)*3)*.9
def clap():
    n=int(.25*SR);t=np.arange(n)/SR;x=hp(rng.standard_normal(n),900)
    e=sum(np.exp(-np.maximum(0,t-o)*60)*(t>=o) for o in(0,.012,.024))*.5+np.exp(-t*14)*.6
    return np.tanh(x*e*2)*.45
def hat(d=.04):n=int(d*SR);return hp(rng.standard_normal(n),7000)*np.exp(-np.arange(n)/SR*90)*.2
def b808(semi,d,glide_to=None):
    n=int(d*SR);t=np.arange(n)/SR;f0=mf(ROOT+semi)
    f=np.full(n,f0) if glide_to is None else f0*2**((glide_to-semi)/12*np.clip((t-d*.55)/(d*.3),0,1))
    x=np.sin(2*np.pi*np.cumsum(f)/SR);e=np.minimum(1,t/.004)*np.exp(-t*1.4)
    return np.tanh(x*e*4)*.5
riff=[0,None,0,3, None,0,5,None, 3,None,0,7, None,5,3,None,
      0,None,0,3, None,0,5,None, 10,None,8,7, None,5,3,2]
bassline=[(0,None),(0,None),(-4,None),(-2,0)]
mus=np.zeros(N);nb=int(T/bar)+1
sc_={s['id']:s for s in tl['scenes']}
brk=(sc_['ex']['s']-bar,sc_['ex']['s'])  # one-bar breakdown before the example
for b in range(nb):
    t0=b*bar;intro=b==0;inbrk=brk[0]-.01<=t0<brk[1]
    for i in range(16):
        n=riff[(b%2)*16+i]
        if n is not None:add(mus,cowbell(n+12),t0+i*st,.8 if inbrk else 1)
    if inbrk:continue
    bn,gl=bassline[b%4];add(mus,b808(bn,bar*.95,gl),t0,.9)
    if intro:continue
    for i in(0,6,10):add(mus,kick(),t0+i*st)
    add(mus,clap(),t0+8*st)
    for i in range(16):
        if b%2==1 and i>=12:
            for k in range(3):add(mus,hat(.03),t0+i*st+k*st/3,.9)
        else:add(mus,hat(),t0+i*st,1 if i%2==0 else .6)
mus=np.tanh(mus*1.6)*.8  # tape-style saturation
fade=np.ones(N);fo=int(2*SR);fade[-fo:]=np.linspace(1,0,fo);mus*=fade
# ---- VO
def readwav(p):
    w=wave.open(p);return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)/32768
vo=np.zeros(N)
for c in tl['clips']:add(vo,readwav(f"vo/{c['i']}.wav"),c['t'])
env=np.convolve(np.abs(vo),np.ones(int(.25*SR))/int(.25*SR),'same');duck=1-.5*np.clip(env*12,0,1)
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
mix=vo*1.0+mus*duck*.42+crowd*.35+sfx*.5
mix/=max(1,np.abs(mix).max()/.95)
pcm=(mix*32767).astype(np.int16)
w=wave.open('mix.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm.tobytes());w.close()
print('ok',T,'peak',np.abs(mix).max())
