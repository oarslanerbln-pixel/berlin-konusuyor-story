"""Procedural sound design for story clips (no samples needed).
events: [{t, k: amb|whirr|click|thud|tick, d?, v?}] -> 48 kHz stereo WAV."""
import numpy as np, wave

SR = 48000


def _env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


def _lp(x, a):  # one-pole low-pass
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc); y[i] = acc
    return y


def synth(events, dur, path, seed=7):
    rng = np.random.default_rng(seed)
    n = int(dur * SR); L = np.zeros(n); R = np.zeros(n)

    def add(sig, t, pan=0.0, g=1.0):
        i = int(t * SR); j = min(n, i + len(sig))
        if i >= n or j <= i: return
        L[i:j] += sig[:j - i] * g * (1 - pan) ** .5; R[i:j] += sig[:j - i] * g * (1 + pan) ** .5

    for e in events:
        k, t = e['k'], e['t']
        if k == 'amb':  # distant city: brown noise + slow swell
            m = int(e['d'] * SR); w = np.cumsum(rng.standard_normal(m)); w -= _lp(w, .0015)
            w /= np.abs(w).max() + 1e-9; sw = .7 + .3 * np.sin(np.arange(m) / SR * .7)
            fade = np.minimum(1, np.arange(m) / (SR * .8)) * np.minimum(1, (m - np.arange(m)) / (SR * .6))
            add(w * sw * fade, t, 0, .05)
        elif k == 'whirr':  # mechanical motor under the prism turn
            m = int(e['d'] * SR); x = _lp(rng.standard_normal(m), .08); tt = np.arange(m) / SR
            x *= (1 + .5 * np.sin(2 * np.pi * 38 * tt)); x /= np.abs(x).max() + 1e-9
            add(x * np.sin(np.pi * tt / e['d']) ** .7, t, 0, .10)
        elif k == 'click':  # each slat locking into place
            v = e.get('v', 1); m = int(.09 * SR); tt = np.arange(m) / SR
            sig = rng.standard_normal(m) * _env(m, .0005, .006) * .8
            f = 150 + rng.uniform(-20, 20); sig += np.sin(2 * np.pi * f * tt) * _env(m, .001, .03) * .9
            add(sig, t, rng.uniform(-.6, .6), .22 * v)
        elif k == 'thud':  # rubber stamp hitting the paper
            m = int(.6 * SR); tt = np.arange(m) / SR; f = 46 + 40 * np.exp(-tt / .05)
            sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(m, .002, .16)
            sig += _lp(rng.standard_normal(m), .35) * _env(m, .0008, .025) * 1.4
            add(sig, t, 0, .85)
        elif k == 'tick':  # light UI tick
            m = int(.04 * SR); tt = np.arange(m) / SR
            add(np.sin(2 * np.pi * 1800 * tt) * _env(m, .0004, .008), t, rng.uniform(-.4, .4), .12 * e.get('v', 1))
    mix = np.stack([L, R], 1); pk = np.abs(mix).max()
    if pk > .98: mix *= .98 / pk
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype('<i2').tobytes())
