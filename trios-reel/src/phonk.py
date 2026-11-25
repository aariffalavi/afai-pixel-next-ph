# Original drift-phonk bed (synthesised): cowbell riff, distorted 808 slides, kick, clap, hat rolls.
import numpy as np
def phonk(T, SR, drop, rng):
    N = int(T*SR); mus = np.zeros(N); low = np.zeros(N)
    bpm = 140; beat = 60/bpm; s16 = beat/4; bar = beat*4
    t0 = drop - np.ceil(drop/bar)*bar          # grid aligned so a bar starts exactly at the drop
    mf = lambda m: 440*2**((m-69)/12)
    def add(buf, sig, t):
        i = int(round(t*SR))
        if i < 0: sig = sig[-i:]; i = 0
        j = min(len(buf), i+len(sig))
        if i < len(buf): buf[i:j] += sig[:j-i]
    def sq(f, t, h=7):  # band-limited square
        return sum(np.sin(2*np.pi*f*k*t)/k for k in range(1, h*2, 2))
    def cowbell(m, d=.32):
        n = int(d*SR); t = np.arange(n)/SR; f = mf(m)
        s = sq(f, t, 4) + .8*sq(f*1.4836, t, 3)
        e = np.exp(-t*14) + .25*np.exp(-t*4)
        return np.tanh(s*e*1.8)*.16
    def kick():
        n = int(.32*SR); t = np.arange(n)/SR; f = 50+170*np.exp(-t*38)
        return np.tanh(np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*2.5)*.75
    def b808(m0, m1, d):  # 808 with glide m0->m1, distorted
        n = int(d*SR); t = np.arange(n)/SR
        f = mf(m0-24) + (mf(m1-24)-mf(m0-24))*np.clip((t-.04)/.09, 0, 1)
        s = np.sin(2*np.pi*np.cumsum(f)/SR)
        e = np.minimum(1, t/.005)*np.exp(-t*1.6)*np.minimum(1, (d-t)/.02)
        return np.tanh(s*e*3.2)*.42
    def clap():
        n = int(.25*SR); t = np.arange(n)/SR; x = rng.standard_normal(n)
        x = x - np.convolve(x, np.ones(18)/18, 'same')
        e = np.exp(-t*18)*(1+.8*((t < .03) & (np.sin(2*np.pi*110*t) > 0)))
        snap = np.sin(2*np.pi*190*t)*np.exp(-t*40)*.6
        return np.tanh((x*.6+snap)*e*2)*.4
    def hat(o=False):
        n = int((.18 if o else .04)*SR); t = np.arange(n)/SR
        x = np.diff(np.concatenate([[0], rng.standard_normal(n)])); x = np.diff(np.concatenate([[0], x]))
        return x*np.exp(-t*(14 if o else 90))*.12
    def pad(ms, d):
        n = int(d*SR); t = np.arange(n)/SR
        s = sum(np.sin(2*np.pi*mf(m)*t*(1+dt)) for m in ms for dt in (-.003, .003))
        return s*np.minimum(1, t/.5)*np.minimum(1, (d-t)/.4)*.018
    # F# minor riff (16 steps per bar, None = rest); two-bar phrase
    R = 66  # F#4
    riffA = [R+12,None,R+12,R+10, None,R+7,None,R+5, R+7,None,R+12,None, R+10,R+7,R+5,None]
    riffB = [R+12,None,R+12,R+15, None,R+14,None,R+12, R+10,None,R+7,None, R+10,None,R+5,R+7]
    roots = [42, 42, 38, 40]   # F#, F#, D, E (808 roots, MIDI before -24 octave shift in b808 → +24 here)
    nb = int((T-t0)/bar)+2
    for b in range(nb):
        tb = t0+b*bar
        intro = tb < drop - 1e-6
        r = roots[b % 4]+24
        add(mus, pad([r+12, r+15, r+19], bar), tb)
        riff = riffA if b % 2 == 0 else riffB
        for k, m in enumerate(riff):
            if m is not None: add(mus, cowbell(m)*(1.5 if intro else 1), tb+k*s16)
        if intro:
            # filtered intro: soft hats + riser on the last bar
            for k in range(8): add(mus, hat()*1.2, tb+k*2*s16)
            add(low, b808(r, r, bar*.9)*.5, tb)
            continue
        # drums (half-time feel: kick 1 & the "and" of 2, clap on 3)
        for st in (0, 6, 10):
            add(low, kick(), tb+st*s16)
        add(mus, clap(), tb+8*s16)
        if b % 4 == 3: add(mus, clap()*.6, tb+14*s16)
        for k in range(16):
            if k % 2 == 0 or (b % 2 == 1 and k >= 12): add(mus, hat(), tb+k*s16)
        if b % 2 == 1:  # triplet hat roll
            for k in range(6): add(mus, hat()*.8, tb+12*s16+k*(2*s16/3))
        add(mus, hat(True), tb+4*s16)
        # 808 pattern with slides
        nxt = roots[(b+1) % 4]+24
        add(low, b808(r, r, 6*s16), tb)
        add(low, b808(r, r+12, 4*s16), tb+6*s16)
        add(low, b808(r+12, nxt, 6*s16), tb+10*s16)
    # riser into the drop
    n = int(bar*SR); t = np.arange(n)/SR; x = rng.standard_normal(n)
    rise = (x - np.convolve(x, np.ones(6)/6, 'same'))*(t/bar)**2*.25
    add(mus, rise, drop-bar)
    # impact at drop
    n = int(1.2*SR); t = np.arange(n)/SR
    add(low, np.tanh(np.sin(2*np.pi*np.cumsum(40+90*np.exp(-t*12))/SR)*np.exp(-t*2.5)*3)*.6, drop)
    return mus, low
