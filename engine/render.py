"""Render animated story clips.
usage: python3 engine/render.py gundem.json outdir [style|auto] [--still]
Writes NN_<style>.mp4 per item (and NN_<style>.jpg poster frame)."""
import sys, json, asyncio, pathlib, subprocess, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from styles import STYLES

FPS = 30
ROTATION = ['bauhaus', 'fallblatt', 'telex']
AY = 'Ocak Şubat Mart Nisan Mayıs Haziran Temmuz Ağustos Eylül Ekim Kasım Aralık'.split()
GUN = 'Pazartesi Salı Çarşamba Perşembe Cuma Cumartesi Pazar'.split()


async def clip(pg, html, out_mp4, out_jpg):
    tmp = out_mp4.with_suffix('.html'); tmp.write_text(html)
    await pg.goto('file://' + str(tmp)); await pg.evaluate('document.fonts.ready')
    dur = await pg.evaluate('window.DUR')
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                           str(out_mp4)], stdin=subprocess.PIPE)
    n = int(dur * FPS)
    for i in range(n):
        await pg.evaluate(f'window.render({i / FPS})')
        shot = await pg.screenshot(type='jpeg', quality=90)
        ff.stdin.write(shot)
        if i == n - 1: pathlib.Path(out_jpg).write_bytes(shot)
    ff.stdin.close(); ff.wait(); tmp.unlink()
    return dur


async def main():
    src, out = sys.argv[1], pathlib.Path(sys.argv[2]).resolve(); out.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[3] if len(sys.argv) > 3 else 'auto'
    D = json.load(open(src)); items = D['items']
    d = datetime.date.fromisoformat(D.get('iso', datetime.date.today().isoformat()))
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, it in enumerate(items, 1):
            style = it.get('style') or (mode if mode != 'auto' else ROTATION[(d.toordinal() + i) % 3])
            meta = dict(idx=i, total=len(items), date_num=d.strftime('%d.%m.%Y'), date_long=f'{d.day} {AY[d.month-1]} {d.year} · {GUN[d.weekday()]}')
            dur = await clip(pg, STYLES[style](it, meta), out / f'{i:02d}_{style}.mp4', out / f'{i:02d}_{style}.jpg')
            print(f'{i:02d}_{style}.mp4  {dur:.1f}s')
        await b.close()

asyncio.run(main())
