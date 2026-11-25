# Music only: the reference reel's song, extended with a seamless 2-bar loop (9.70->14.28 s, played twice),
# then the original ending + impact. Loudness-normalised to -14 LUFS.
import numpy as np, subprocess, wave
SR=48000
def load(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac","2","-ar",str(SR),"-"],capture_output=True,check=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).astype(np.float64)
song=load("song_ref.m4a"); s=lambda t:int(round(t*SR))
LS,LE=9.70,14.28
plan=[(0,LE),(LS,LE),(LS,LE),(LE,len(song)/SR)]
X=np.zeros((s(40),2)); pos=0; xf=s(0.03); r=np.linspace(0,1,xf)[:,None]
for a,b in plan:
    seg=song[s(a):s(b)].copy()
    if pos>0:
        X[pos-xf:pos]*=np.cos(r*np.pi/2); seg[:xf]*=np.sin(r*np.pi/2)
        X[pos-xf:pos]+=seg[:xf]; seg=seg[xf:]
    X[pos:pos+len(seg)]=seg; pos+=len(seg)
X=X[:s(27.2)]; fo=s(0.4); X[-fo:]*=np.linspace(1,0,fo)[:,None]
print("music length",pos/SR)
X/=np.abs(X).max()/0.89
with wave.open("mix_raw.wav","wb") as w: w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((X*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg","-y","-v","error","-i","mix_raw.wav","-af","loudnorm=I=-14:TP=-1.5:LRA=11","-ar","48000","mix.wav"],check=True)
