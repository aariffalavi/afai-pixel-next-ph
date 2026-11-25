# Music: the song from the reference reel, extended with a seamless 2-bar loop (4.58 s, 9.70->14.28 s),
# then its original ending + impact. Ducked under the voice-over, loudness-normalised.
import numpy as np, json, subprocess, wave
SR=48000
def load(path,ch=2):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac",str(ch),"-ar",str(SR),"-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,ch).astype(np.float64)
song=load("song_ref.m4a")
tl=json.load(open("timeline.json")); N=int(tl["total"]*SR)
s=lambda t:int(round(t*SR))
LS,LE=9.70,14.28
plan=[(0,LE)]+[(LS,LE)]*6+[(LE,len(song)/SR)]
X=np.zeros((N+SR,2)); pos=0; xf=s(0.03)
for a,b in plan:
    seg=song[s(a):s(b)].copy()
    if pos>0:  # equal-power crossfade into previous segment's tail
        pre=song[s(a)-xf:s(a)] if s(a)>=xf else np.zeros((xf,2))
        r=np.linspace(0,1,xf)[:,None]
        X[pos-xf:pos]=X[pos-xf:pos]*np.cos(r*np.pi/2)+pre*np.sin(r*np.pi/2)*0  # fade out old
        seg[:xf]*=np.sin(r*np.pi/2)
        X[pos-xf:pos]+=seg[:xf]; seg=seg[xf:]
    X[pos:pos+len(seg)]+=seg[:len(X)-pos]; pos+=len(seg)
print("music length",pos/SR)
X=X[:N]
# ducking envelope
g=np.ones(N)*0.9
for v in tl["vo"]:
    a=s(v["start"]-0.12); b=s(v["start"]+v["dur"]+0.1); g[max(0,a):b]=0.32
k=s(0.12); g=np.convolve(g,np.ones(k)/k,"same")
X*=g[:,None]
V=np.zeros(N)
for i,v in enumerate(tl["vo"]):
    w=load(f"vo/{i}.wav",1)[:,0]; a=s(v["start"]); V[a:a+len(w)]+=w[:N-a]*1.0
fo=s(0.6); X[-fo:]*=np.linspace(1,0,fo)[:,None]
M=X+V[:,None]
M/=max(1e-9,np.abs(M).max())/0.89
wave_out=(np.clip(M,-1,1)*32767).astype(np.int16)
with wave.open("mix_raw.wav","wb") as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(wave_out.tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","48000","mix.wav"],check=True)
# no-music version (voice only) for posting with Instagram's own audio
Vn=V/np.abs(V).max()*0.89
with wave.open("vo_only.wav","wb") as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((Vn*32767).astype(np.int16).tobytes())
