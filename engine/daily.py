"""Daily edition builder.
usage: python3 engine/daily.py data/YYYY-MM-DD.json [--no-push]
Renders the day's story clips, publishes them under d/<date>/ on GitHub Pages and writes d/latest.json
(the manifest the Make publisher reads at 08:30)."""
import sys, json, pathlib, subprocess, shutil, datetime, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = 'https://oarslanerbln-pixel.github.io/berlin-konusuyor-story'


def sh(*a):
    subprocess.run(a, check=True, cwd=ROOT)


def main():
    src = pathlib.Path(sys.argv[1]).resolve(); D = json.load(open(src))
    iso = D['iso']; ed = D.get('edition', 'sabah'); slug = iso + ('-aksam' if ed == 'aksam' else '')
    out = ROOT / 'out' / slug; dst = ROOT / 'd' / slug
    shutil.rmtree(out, ignore_errors=True)
    sh(sys.executable, str(ROOT / 'engine' / 'render.py'), str(src), str(out), 'auto')
    shutil.rmtree(dst, ignore_errors=True); dst.mkdir(parents=True)
    items = []
    for i, it in enumerate(D['items'], 1):
        mp4 = sorted(out.glob(f'{i:02d}_*.mp4'))[0]; jpg = mp4.with_suffix('.jpg')
        shutil.copy(mp4, dst / f'{i:02d}.mp4'); shutil.copy(jpg, dst / f'{i:02d}.jpg')
        items.append(dict(idx=i, title=it['title'], tag=it['tag'], source=it['source'], style=mp4.stem.split('_', 1)[1],
                          sensitive=bool(it.get('sensitive')), sources_n=it.get('sources_n', 2),
                          video_url=f'{BASE}/d/{slug}/{i:02d}.mp4', poster_url=f'{BASE}/d/{slug}/{i:02d}.jpg'))
    man = dict(date=iso, edition=ed, built=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
               needs_approval=D.get('needs_approval', True) or any(x['sensitive'] or x['sources_n'] < 2 for x in items),
               items=items)
    json.dump(man, open(dst / 'manifest.json', 'w'), ensure_ascii=False, indent=1)
    json.dump(man, open(ROOT / 'd' / ('latest-aksam.json' if ed == 'aksam' else 'latest.json'), 'w'), ensure_ascii=False, indent=1)
    cards = ''.join(f'<figure><video src="{x["idx"]:02d}.mp4" poster="{x["idx"]:02d}.jpg" controls playsinline></video>'
                    f'<figcaption><b>{html.escape(x["tag"])}</b> {html.escape(x["title"])}<br><small>Kaynak: {html.escape(x["source"])} · {x["style"]}</small></figcaption></figure>'
                    for x in items)
    (dst / 'index.html').write_text(
        f'<!doctype html><html lang="tr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{'Berlin Akşamı' if ed == 'aksam' else 'Berlin Gündemi'} · {iso}</title><style>body{{font:16px system-ui;background:#111;color:#eee;margin:0;padding:16px}}'
        f'h1{{font-size:20px}}figure{{margin:0 0 22px}}video{{width:100%;max-width:420px;border-radius:12px;display:block}}'
        f'figcaption{{margin-top:8px;max-width:420px}}b{{background:#C8102E;padding:2px 6px;border-radius:4px;margin-right:6px}}</style>'
        f'<h1>{'Berlin Akşamı' if ed == 'aksam' else 'Berlin Gündemi'} · {iso}</h1>{cards}</html>')
    print(json.dumps(dict(preview=f'{BASE}/d/{slug}/', manifest=f'{BASE}/d/latest.json', needs_approval=man['needs_approval'])))
    if '--no-push' not in sys.argv:
        sh('git', 'add', 'd', 'data')
        sh('git', '-c', 'user.name=Berlin Konusuyor Bot', '-c', 'user.email=oarslanerbln-pixel@users.noreply.github.com',
           'commit', '-qm', f'{"Akşam" if ed == "aksam" else "Gündem"} {iso}')
        sh('git', '-c', 'push.negotiate=true', 'push', '-q', 'origin', 'HEAD:main')


if __name__ == '__main__':
    main()
