"""Render animated story clips.
usage: python3 engine/render.py gundem.json outdir [style|auto] [--still]
Writes NN_<style>.mp4 per item (and NN_<style>.jpg poster frame)."""
import sys, json, asyncio, pathlib, subprocess, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from styles import STYLES
from styles3 import STYLES3
from styles4 import STYLES4
from sfx import synth
STYLES.update(STYLES3); STYLES.update(STYLES4)

FPS = 30
ROTATION = ['bauhaus', 'fallblatt', 'telex']
AY = 'Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık'.split()
GUN = 'Pazartesi Salı Çarşamba Perşembe Cuma Cumartesi Pazar'.split()


async def clip(pg, html, out_mp4, out_jpg):
    tmp = out_mp4.with_suffix('.html'); tmp.write_text(html)
    await pg.goto('file://' + str(tmp)); await pg.evaluate('document.fonts.ready'); await pg.evaluate('window.fit && window.fit()')
    dur = await pg.evaluate('window.DUR'); sfx = await pg.evaluate('window.SFX || null')
    vid = out_mp4.with_name('_v_' + out_mp4.name) if sfx else out_mp4
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                           str(vid)], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        await pg.evaluate(f'window.render({i / FPS})')
        shot = await pg.screenshot(type='jpeg', quality=90)
        ff.stdin.write(shot)
        if i == n - 1: pathlib.Path(out_jpg).write_bytes(shot)
    ff.stdin.close(); ff.wait(); tmp.unlink()
    if sfx:
        wav = out_mp4.with_suffix('.wav'); synth(sfx, dur, wav)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', str(vid), '-i', str(wav), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                        '-shortest', '-movflags', '+faststart', str(out_mp4)], check=True)
        vid.unlink(); wav.unlink()
    return dur


EDITION = 'sabah'


def monthly_style(d):
    cfg = json.load(open(pathlib.Path(__file__).resolve().parent.parent / 'config.json'))
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
            dur = await clip(pg, STYLES[style](it, meta), out / f'{i:02d}_{style}.mp4', out / f'{i:02d}_{style}.jpg')
            print(f'{i:02d}_{style}.mp4  {dur:.1f}s')
        await b.close()

asyncio.run(main())
