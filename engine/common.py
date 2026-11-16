"""Shared brand assets for the Berlin Konuşuyor story engine."""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / 'fonts'
P = json.load(open(ROOT / 'assets' / 'logo_paths.json'))
RED, BLK, CREAM = '#C8102E', '#111111', '#EEE7D8'

LAT = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2212'
EXT = 'U+0100-0130,U+0132-02BA,U+02BD-02C5,U+1E00-1EFF'


def _ff(fam, stem, w):
    return ''.join(
        f"@font-face{{font-family:{fam};src:url('file://{FONTS}/{stem.format(s)}');font-weight:{w};unicode-range:{r}}}"
        for s, r in (('latin', LAT), ('latin-ext', EXT)))


FONT_CSS = (_ff('PO', 'poppins-{}-800-normal.woff2', 800)
            + _ff('IN', 'inter-{}-500-normal.woff2', 500) + _ff('IN', 'inter-{}-600-normal.woff2', 600)
            + _ff('MO', 'ibm-plex-mono-{}-500-normal.woff2', 500) + _ff('MO', 'ibm-plex-mono-{}-700-normal.woff2', 700)
            + _ff('PF', 'playfair-display-{}-400-normal.woff2', 400) + _ff('PF', 'playfair-display-{}-900-normal.woff2', 900)
            + _ff('HW', 'caveat-{}-700-normal.woff2', 700)
            + f"@font-face{{font-family:FK;src:url('file://{FONTS}/unifrakturcook-latin-700-normal.woff2');font-weight:700}}")


def _svg(keys, fills, bbox, h):
    w = h * (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])
    vb = f'{bbox[0]} {bbox[1]} {bbox[2]-bbox[0]} {bbox[3]-bbox[1]}'
    ps = ''.join(f'<path fill="{c}" fill-rule="evenodd" d="{P[k]}"/>' for k, c in zip(keys, fills))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" style="width:{w:.0f}px;height:{h}px;display:block">{ps}</svg>'


def b2(h, top='#fff', b=RED):
    return _svg(['b2_icon_black', 'b2_icon_red'], [top, b], P['b2_icon_bbox'], h)


def tv(h, c='#fff'):
    return _svg(['tv2_white'], [c], P['tv2_bbox'], h)


def tr_upper(s):
    return s.replace('i', 'İ').replace('ı', 'I').upper()


def wrap(text, n):
    lines, cur = [], ''
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return lines + [cur] if cur else lines


def brand(color='#fff', accent='#F05A6E', icon_top='#fff'):
    return (f'<div class="brand" style="position:absolute;left:80px;top:250px;display:flex;align-items:center;gap:18px;'
            f'color:{color};font:600 22px/1.25 IN;letter-spacing:5px;z-index:20">{b2(78, icon_top)}'
            f'<span>BERLİN<i style="font-style:normal;color:{accent};display:block">GÜNDEMİ</i></span></div>')


def page(body, css='', js='', data=None):
    return ('<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>' + FONT_CSS +
            '*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden}'
            '#s{position:relative;width:1080px;height:1920px;overflow:hidden}' + css +
            '</style></head><body><div id="s">' + body + '</div><script>const D=' + json.dumps(data or {}, ensure_ascii=False) +
            ';\nconst cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)), seg=(t,a,b)=>cl((t-a)/(b-a)),'
            'eo=p=>1-Math.pow(1-p,3), eio=p=>p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2,'
            'rnd=i=>{const s=Math.sin(i*12.9898+78.233)*43758.5453;return s-Math.floor(s)};\n' + js + '</script></body></html>')
