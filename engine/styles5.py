"""Batch 5: SABAH — clean, airy morning style (warm paper, soft rising sun, calm type)."""
from common import page, brand, tr_upper, RED, BLK


def sabah(it, meta):
    words = it['title'].split()
    hl = ' '.join(f'<span class="w"><span>{w}</span></span>' for w in words)
    et = (f'<div id="et"><b>SANA ETKİSİ</b><span>{it["etki"]}</span></div>' if it.get('etki') else '')
    body = ('<div id="sun"></div><div id="sun2"></div>'
            + brand(color='#1a1a1a', accent=RED, icon_top='#1a1a1a') +
            f'<div id="cnt">{meta["idx"]:02d}<i>/{meta["total"]:02d}</i></div>'
            f'<div id="col"><div id="dt">{tr_upper(meta["date_long"])}</div>'
            f'<div id="tg"><i></i>{tr_upper(it["tag"])}</div>'
            f'<h1 id="h">{hl}</h1><div id="rl"></div><p id="b">{it["body"]}</p>{et}'
            f'<div id="src">Kaynak · {it["source"]}</div></div>')
    css = f"""#s{{background:linear-gradient(170deg,#FBF8F3 0%,#F5EFE6 55%,#EFE6DA 100%)}}
#sun{{position:absolute;width:760px;height:760px;right:-230px;top:0;border-radius:50%;
  background:radial-gradient(circle,rgba(255,196,150,.95) 0%,rgba(255,176,140,.55) 38%,rgba(255,170,150,0) 70%);filter:blur(6px)}}
#sun2{{position:absolute;width:520px;height:520px;left:-260px;bottom:120px;border-radius:50%;
  background:radial-gradient(circle,rgba(200,16,46,.10) 0%,rgba(200,16,46,0) 70%)}}
#cnt{{position:absolute;right:80px;top:262px;font:600 30px IN;color:#1a1a1a;letter-spacing:2px;z-index:20}}
#cnt i{{font-style:normal;color:#a39a8c}}
#col{{position:absolute;left:80px;right:80px;top:450px;display:flex;flex-direction:column;align-items:flex-start}}
#dt{{font:500 25px MO;letter-spacing:5px;color:#8f8676}}
#tg{{margin-top:44px;display:flex;align-items:center;gap:16px;font:600 29px IN;letter-spacing:7px;color:{RED}}}
#tg i{{width:14px;height:14px;border-radius:50%;background:{RED}}}
#h{{margin-top:22px;font:800 98px/1.05 PO;color:#141414;letter-spacing:-2px}}
.w{{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:6px}}.w span{{display:inline-block}}
#rl{{margin-top:40px;height:4px;width:110px;background:{RED};border-radius:2px;transform-origin:0 50%}}
#b{{margin-top:40px;font:500 42px/1.5 IN;color:#3b3833}}
#et{{margin-top:44px;align-self:stretch;background:rgba(255,255,255,.72);border-radius:28px;padding:30px 34px;
  box-shadow:0 18px 40px rgba(120,90,60,.10),0 0 0 1px rgba(120,90,60,.08)}}
#et b{{display:block;font:700 22px IN;letter-spacing:6px;color:{RED};margin-bottom:10px}}
#et span{{font:600 36px/1.42 IN;color:#1a1a1a}}
#src{{margin-top:38px;font:500 26px IN;letter-spacing:2px;color:#9a9182}}"""
    js = r"""
const $=i=>document.getElementById(i),ws=[...document.querySelectorAll('.w span')];
const TH=.9,TB=TH+ws.length*.08+.55;window.DUR=Math.max(8,TB+3.4);
window.SFX=[{t:.1,k:'amb',d:window.DUR},...ws.map((w,i)=>({t:TH+i*.08+.05,k:'tick',v:.35})),{t:TB+.55,k:'click',v:.5}];
window.fit=()=>{const col=$('col'),h=$('h'),b=$('b'),e=$('et');let k=1;
  while(col.offsetTop+col.offsetHeight>1640&&k>.62){k-=.03;h.style.fontSize=98*k+'px';b.style.fontSize=42*Math.max(k,.8)+'px';
    if(e)e.querySelector('span').style.fontSize=36*Math.max(k,.82)+'px'}};
const fade=(el,t0,t,dy=26)=>{if(!el)return;const p=eo(seg(t,t0,t0+.7));el.style.opacity=p;el.style.transform=`translateY(${(1-p)*dy}px)`};
window.render=t=>{
  const r=eo(seg(t,0,2.6));$('sun').style.transform=`translateY(${560-520*r+Math.sin(t*.35)*14}px) scale(${.85+.15*r})`;$('sun').style.opacity=.2+.8*r;
  $('sun2').style.transform=`translate(${Math.sin(t*.25)*30}px,${Math.cos(t*.2)*20}px)`;
  fade($('dt'),.25,t,14);fade($('tg'),.45,t,14);
  ws.forEach((w,i)=>{const p=eo(seg(t,TH+i*.08,TH+i*.08+.6));w.style.transform=`translateY(${(1-p)*105}%)`});
  $('rl').style.transform=`scaleX(${eo(seg(t,TB-.3,TB+.4))})`;
  fade($('b'),TB,t);fade($('et'),TB+.45,t,34);fade($('src'),TB+.8,t,10);};
"""
    return page(body, css, js)


STYLES5 = dict(sabah=sabah)
