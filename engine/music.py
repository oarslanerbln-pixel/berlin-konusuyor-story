"""Procedural background music for story clips (no samples, no licensing).
Warm lo-fi bed: Rhodes-style electric piano, soft pad, sine bass, brushed beat, a sparse pluck melody
and a little vinyl crackle. Morning = bright major progression, evening = mellow minor one.
music(dur, edition, seed) -> float array (n, 2) at 48 kHz, peak ~0.35, faded in/out."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BPM = 78
BEAT = 60 / BPM

# chord voicings as MIDI notes (bass root first)
PROG = {
    'sabah': [[48, 64, 67, 71, 74],    # Cmaj9
              [45, 60, 64, 67, 71],    # Am9
              [41, 57, 60, 64, 67],    # Fmaj7 (add9 colour from the pluck)
              [43, 59, 62, 65, 69]],   # G13sus-ish
    'aksam': [[45, 60, 64, 67, 71],    # Am9
              [41, 57, 60, 64, 67],    # Fmaj7
              [48, 59, 64, 67, 71],    # Cmaj7
              [40, 55, 59, 62, 66]],   # Em9
}


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, 'high', fs=SR, output='sos'), x)


def music(dur, edition='sabah', seed=1):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); L = np.zeros(n); R = np.zeros(n)
    prog = PROG.get(edition, PROG['sabah'])
    bar = 4 * BEAT

    def add(sig, t, pan=0.0, g=1.0):
        i = int(t * SR)
        if i >= n: return
        j = min(n, i + len(sig)); s = sig[:j - i] * g
        L[i:j] += s * np.sqrt((1 - pan) / 2) * 1.414; R[i:j] += s * np.sqrt((1 + pan) / 2) * 1.414

    def rhodes(f, t, d=2.2, g=1.0, pan=0.0):  # 2-op FM electric piano, slight tremolo
        m = int(d * SR); tt = np.arange(m) / SR
        idx = 1.6 * np.exp(-tt / .35) + .25
        sig = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * tt))
        sig += .18 * np.sin(2 * np.pi * 2 * f * tt) * np.exp(-tt / .25)  # tine bark
        sig *= env(m, .004, .9) * (1 + .12 * np.sin(2 * np.pi * 4.2 * tt))
        add(sig, t, pan, g)

    def pad(notes, t, d, g=.06):
        m = int(d * SR); tt = np.arange(m) / SR; sig = np.zeros(m)
        for k, mn in enumerate(notes):
            f = hz(mn + 12)
            for det in (-.11, .0, .12):
                sig += np.sin(2 * np.pi * f * (1 + det / 100) * tt + rng.uniform(0, 6.28))
        shape = np.minimum(1, tt / 1.2) * np.minimum(1, (d - tt) / .8)
        add(lp(sig, 1800) * shape, t, rng.uniform(-.3, .3), g)

    bars = int(np.ceil(dur / bar)) + 1
    mel_scale = sorted({x % 12 for ch in prog for x in ch[1:]})
    for b in range(bars):
        t0 = b * bar; ch = prog[b % len(prog)]
        pad(ch[1:], t0, bar + .6)
        # bass: root on 1, fifth/octave pickup on the "and" of 3
        for tb, mn, gg in ((0, ch[0] - 12, .55), (2.5 * BEAT, ch[0] - 12 + (7 if b % 2 else 12), .32)):
            m = int(1.1 * SR); tt = np.arange(m) / SR; f = hz(mn)
            add((np.sin(2 * np.pi * f * tt) + .25 * np.sin(4 * np.pi * f * tt)) * env(m, .01, .45), t0 + tb, 0, gg)
        # electric piano: chord on 1 (rolled), soft repeat on the "and" of 2
        for k, mn in enumerate(ch[1:]):
            rhodes(hz(mn), t0 + k * .018, g=.085, pan=-.25 + k * .12)
            rhodes(hz(mn), t0 + 1.5 * BEAT + k * .012, d=1.2, g=.04, pan=.25 - k * .12)
        # sparse pluck melody (two-bar phrase, repeats with small variation)
        for s in range(8):
            if rng.random() < (.42 if s % 2 == 0 else .2):
                base = ch[1 + rng.integers(0, 4)] + 12
                mn = base + (2 if rng.random() < .25 and (base + 2) % 12 in mel_scale else 0)
                m = int(.9 * SR); tt = np.arange(m) / SR; f = hz(mn)
                sig = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 3 * f * tt) * np.exp(-tt / .05)) * env(m, .002, .28)
                add(sig, t0 + s * BEAT / 2 + rng.uniform(0, .012), rng.uniform(-.6, .6), .05)
        # drums: soft kick on 1 & 3, brushed snare on 2 & 4, shuffled hats
        for bt in range(4):
            tb = t0 + bt * BEAT
            if bt in (0, 2) or (bt == 3 and b % 2):
                m = int(.35 * SR); tt = np.arange(m) / SR; f = 48 + 70 * np.exp(-tt / .03)
                add(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(m, .002, .12), tb + (BEAT / 2 if bt == 3 else 0), 0, .42)
            if bt in (1, 3):
                m = int(.25 * SR); x = hp(lp(rng.standard_normal(m), 5200), 900)
                add(x * env(m, .003, .07), tb, .1, .07)
            for sw in (0, .62):  # swung 8ths
                m = int(.06 * SR); x = hp(rng.standard_normal(m), 7000)
                add(x * env(m, .0005, .015), tb + sw * BEAT, rng.uniform(-.5, .5), .045 if sw else .03)

    mix = np.stack([L, R], 1)
    # warm it up, add a short room reverb
    mix = np.stack([lp(mix[:, c], 7500) for c in (0, 1)], 1)
    irn = int(1.6 * SR); ir = rng.standard_normal((irn, 2)) * np.exp(-np.arange(irn) / SR / .45)[:, None]
    ir = np.stack([lp(ir[:, c], 3500) for c in (0, 1)], 1); ir /= np.sqrt((ir ** 2).sum(0))
    wet = np.stack([fftconvolve(mix[:, c], ir[:, c])[:n] for c in (0, 1)], 1)
    mix = mix * .85 + wet * .35
    # vinyl crackle + hiss
    cr = (rng.random((n, 2)) < 1.2e-4) * rng.standard_normal((n, 2)) * .25
    mix += hp(cr[:, 0], 1500)[:, None] * [1, .7] + rng.standard_normal((n, 2)) * .0018
    # fades & level
    tt = np.arange(n) / SR
    mix *= (np.minimum(1, tt / 1.0) * np.minimum(1, (dur - tt) / 1.4))[:, None]
    rms = np.sqrt(np.mean(mix ** 2)) + 1e-9
    mix *= .11 / rms
    return .42 * np.tanh(mix / .42)  # gentle soft-clip limiter
