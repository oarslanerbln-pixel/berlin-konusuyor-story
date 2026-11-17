"""Render animated story clips.
usage: python3 engine/render.py gundem.json outdir [style|auto] [--still]
Writes NN_<style>.mp4 per item (and NN_<style>.jpg poster frame)."""
import sys, json, asyncio, pathlib, subprocess, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from styles import STYLES
from styles3 import STYLES3
from styles4 import STYLES4
from styles5 import STYLES5
from sfx import synth
from music import music
STYLES.update(STYLES3); STYLES.update(STYLES4); STYLES.update(STYLES5)

FPS = 30
ROTATION = ['bauhaus', 'fallblatt', 'telex']
AY = 'Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık'.split()
GUN = 'Pazartesi Salı Çarşamba Perşembe Cuma Cumartesi Pazar'.split()


READ_WPS = 2.4      # comfortable story reading speed (words per second, Turkish, on a phone)
MIN_DUR, MAX_DUR = 15.0, 45.0

TIMER_JS = r"""(()=>{const s=document.getElementById('s');const d=document.createElement('div');d.id='bk-timer';
d.innerHTML='<svg viewBox="0 0 64 64" width="64" height="64"><circle cx="32" cy="32" r="29" fill="rgba(17,17,17,.62)"/>'
+'<circle cx="32" cy="32" r="25" fill="none" stroke="rgba(255,255,255,.22)" stroke-width="4"/>'
+'<circle id="bk-arc" cx="32" cy="32" r="25" fill="none" stroke="#E8304A" stroke-width="4" stroke-linecap="round" transform="rotate(-90 32 32)"/>'
+'<text id="bk-num" x="32" y="33" text-anchor="middle" dominant-baseline="central" fill="#fff" style="font:700 22px IN,sans-serif"></text></svg>';
d.style.cssText='position:absolute;right:74px;top:312px;width:64px;height:64px;z-index:60;opacity:0';s.appendChild(d);
const C=2*Math.PI*25,arc=document.getElementById('bk-arc'),num=document.getElementById('bk-num');arc.style.strokeDasharray=C;
window.__timer=t=>{const D=window.DUR,left=Math.max(0,D-t);d.style.opacity=Math.min(1,Math.max(0,(t-.4)/.5));
  arc.style.strokeDashoffset=C*(1-left/D);num.textContent=Math.ceil(left-1e-6)}})()"""


def reading_time(it):
    words = sum(len(str(it.get(k, '')).split()) for k in ('title', 'body', 'etki'))
    return words / READ_WPS


async def clip(pg, html, out_mp4, out_jpg, it, edition='sabah', seed=1):
    tmp = out_mp4.with_suffix('.html'); tmp.write_text(html)
    await pg.goto('file://' + str(tmp)); await pg.evaluate('document.fonts.ready'); await pg.evaluate('window.fit && window.fit()')
    base = await pg.evaluate('window.DUR'); sfx = await pg.evaluate('window.SFX || null') or []
    # the animation itself only needs `base` seconds; hold the finished card long enough to read it
    dur = round(min(MAX_DUR, max(MIN_DUR, base, base - 3 + reading_time(it) + 2)), 1)
    await pg.evaluate(f'window.DUR={dur}'); await pg.evaluate(TIMER_JS)
    for e in sfx:  # stretch ambience beds to the new length
        if e.get('k') == 'amb' and e.get('d', 0) >= base - .5: e['d'] = dur - e.get('t', 0)
    vid = out_mp4.with_name('_v_' + out_mp4.name)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                           str(vid)], stdin=subprocess.PIPE)
    n = int(dur * FPS); poster = int(min(base, dur) * FPS)
    for i in range(n):
        await pg.evaluate(f'window.render({i / FPS});window.__timer({i / FPS})')
        shot = await pg.screenshot(type='jpeg', quality=90)
        ff.stdin.write(shot)
        if i == poster: pathlib.Path(out_jpg).write_bytes(shot)
    ff.stdin.close(); ff.wait(); tmp.unlink()
    wav = out_mp4.with_suffix('.wav'); synth(sfx, dur, wav, music=music(dur, edition, seed))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(vid), '-i', str(wav), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                    '-shortest', '-movflags', '+faststart', str(out_mp4)], check=True)
    vid.unlink(); wav.unlink()
    return dur


EDITION = 'sabah'


def monthly_style(d):
    cfg = json.load(open(pathlib.Path(__file__).resolve().parent.parent / 'config.json'))
    fixed = cfg.get('edition_styles', {}).get(EDITION)
    if fixed: return fixed
    y0, m0 = map(int, cfg['start_month'].split('-'))
    off = cfg.get('evening_offset', 1) if EDITION == 'aksam' else 0
    return cfg['monthly_styles'][((d.year * 12 + d.month) - (y0 * 12 + m0) + off) % len(cfg['monthly_styles'])]


async def main():
    src, out = sys.argv[1], pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[3] if len(sys.argv) > 3 else 'auto'
    global EDITION
    D = json.load(open(src)); items = D['items']; EDITION = D.get('edition', 'sabah')
    import common; common.BRAND_SUB = 'AKŞAMI' if EDITION == 'aksam' else 'GÜNDEMİ'
    d = datetime.date.fromisoformat(D.get('iso', datetime.date.today().isoformat()))
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, it in enumerate(items, 1):
            style = it.get('style') or (mode if mode != 'auto' else monthly_style(d))
            meta = dict(idx=i, total=len(items), date_num=d.strftime('%d.%m.%Y'), date_long=f'{d.day} {AY[d.month-1]} {d.year} · {GUN[d.weekday()]}', titles=[x['title'] for x in items])
            dur = await clip(pg, STYLES[style](it, meta), out / f'{i:02d}_{style}.mp4', out / f'{i:02d}_{style}.jpg', it, EDITION,
                             seed=d.toordinal() * 10 + i)
            print(f'{i:02d}_{style}.mp4  {dur:.1f}s')
        await b.close()

asyncio.run(main())
