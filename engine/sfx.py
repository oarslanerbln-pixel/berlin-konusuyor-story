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
            add(sig, t, 0, .85 * e.get('v', 1))
        elif k == 'train':  # wheels on rails: low rumble + rhythmic joints, panning with direction
            m = int(e['d'] * SR); tt = np.arange(m) / SR; x = _lp(rng.standard_normal(m), .03); x /= np.abs(x).max() + 1e-9
            sp = np.linspace(1, .15, m) if e.get('dir', -1) < 0 else np.linspace(.15, 1, m) ** 1.5
            joints = (np.sin(2 * np.pi * np.cumsum(6 * sp) / SR) > .97) * _lp(rng.standard_normal(m), .3) * 2.5
            env = np.sin(np.pi * np.minimum(1, tt / e['d'])) ** .6
            sig = (x * (.6 + .4 * sp) + joints) * env; pan = np.linspace(.7, -.3, m) if e.get('dir', -1) < 0 else np.linspace(0, -.8, m)
            i = int(t * SR); j = min(n, i + m); L[i:j] += (sig * np.sqrt(1 - pan) * .35)[:j - i]; R[i:j] += (sig * np.sqrt(1 + pan) * .35)[:j - i]
        elif k == 'brake':  # squeal
            m = int(e['d'] * SR); tt = np.arange(m) / SR; f = 2900 + 120 * np.sin(2 * np.pi * 7 * tt)
            add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / e['d']) ** 2, t, .2, .05)
        elif k == 'chime':  # two-tone station gong
            for dt, f in ((0, 784), (.42, 622)):
                m = int(1.2 * SR); tt = np.arange(m) / SR
                add((np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * _env(m, .004, .45), t + dt, 0, .16)
        elif k == 'buzz':  # neon transformer hum
            m = int(e['d'] * SR); tt = np.arange(m) / SR
            sig = sum(np.sin(2 * np.pi * 100 * h * tt) / h for h in (1, 2, 3, 5)) + _lp(rng.standard_normal(m), .5) * .3
            add(sig * np.minimum(1, tt / .05), t, 0, .035 * e.get('v', 1))
        elif k == 'spray':  # aerosol hiss
            m = int(e['d'] * SR); tt = np.arange(m) / SR; x = rng.standard_normal(m); x -= _lp(x, .25)
            add(x * np.minimum(1, tt / .03) * np.minimum(1, (e['d'] - tt) / .05), t, rng.uniform(-.3, .3), .22)
        elif k == 'rattle':  # shaking the can
            for q in range(6):
                m = int(.05 * SR); add(rng.standard_normal(m) * _env(m, .0005, .01), t + q * .11, .3, .25)
        elif k == 'tick':  # light UI tick
            m = int(.04 * SR); tt = np.arange(m) / SR
            add(np.sin(2 * np.pi * 1800 * tt) * _env(m, .0004, .008), t, rng.uniform(-.4, .4), .12 * e.get('v', 1))
    mix = np.stack([L, R], 1); pk = np.abs(mix).max()
    if pk > .98: mix *= .98 / pk
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype('<i2').tobytes())
