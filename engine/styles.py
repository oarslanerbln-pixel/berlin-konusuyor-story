"""Animated story styles. Each builder returns an HTML page exposing window.DUR and window.render(t)."""
from common import page, brand, b2, tr_upper, wrap, RED, BLK, CREAM


def count(meta, color):
    return (f'<div style="position:absolute;right:80px;top:268px;font:600 24px IN;letter-spacing:4px;color:{color};z-index:20">'
            f'{meta["idx"]} / {meta["total"]}</div>')


# ───────────────────────── A · FALLBLATT (split-flap departure board) ─────────────────────────
def fallblatt(it, meta):
    cols = 12
    rows = wrap(tr_upper(it['title']), cols)[:4]
    data = dict(tag=tr_upper(it['tag']), rows=[r.ljust(cols) for r in rows], cols=cols)
    y_end = 770 + len(rows) * 128
    body = (brand() + count(meta, 'rgba(255,255,255,.55)') +
            '<canvas id="c" width="1080" height="1920" style="position:absolute;inset:0"></canvas>'
            f'<p id="b" style="position:absolute;left:40px;right:40px;top:{y_end+56}px;font:500 38px/1.5 IN;color:#D6D6D6">{it["body"]}</p>'
            f'<div id="src" style="position:absolute;left:40px;bottom:350px;font:600 24px IN;letter-spacing:3px;color:rgba(255,255,255,.5)">KAYNAK: {it["source"]}</div>')
    css = '#s{background:radial-gradient(120% 80% at 50% 30%,#1b1b1b 0%,#0b0b0b 70%)}'
    js = r"""
const cv=document.getElementById('c'),x=cv.getContext('2d');
const CH='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ0123456789';
const cw=78,chh=114,gap=6,COLS=D.cols,x0=(1080-(COLS*cw+(COLS-1)*gap))/2, FD=.062;
const cells=[];
function addRow(str,y,ri,red){[...str].forEach((c,i)=>{const id=ri*40+i;
  cells.push({c,x:x0+i*(cw+gap),y,red,st:.45+ri*.2+i*.035+rnd(id)*.12,n:c===' '?0:5+Math.floor(rnd(id+7)*8),id})})}
addRow(D.tag.padEnd(COLS),630,0,true);
D.rows.forEach((r,i)=>addRow(r,770+i*128,i+1,false));
const DONE=Math.max(...cells.map(c=>c.st+c.n*FD));
window.DUR=Math.max(8,DONE+4.2);
function seq(c,k){if(k<=0)return ' ';if(k>=c.n)return c.c;return CH[Math.floor(rnd(c.id*31+k)*CH.length)]}
function half(ch,c,top,sc){const bg=c.red?(top?'#D81733':'#B80E29'):(top?'#232323':'#1B1B1B');
  x.save();x.beginPath();x.rect(c.x,top?c.y:c.y+chh/2,cw,chh/2);x.clip();
  if(sc!==1){x.translate(0,c.y+chh/2);x.scale(1,sc);x.translate(0,-(c.y+chh/2))}
  x.fillStyle=bg;x.beginPath();x.roundRect(c.x,c.y,cw,chh,7);x.fill();
  if(sc!==1){x.fillStyle=`rgba(0,0,0,${(1-sc)*.45})`;x.fillRect(c.x,c.y,cw,chh)}
  x.fillStyle=c.red?'#fff':'#F3EEE2';x.font='800 74px PO';x.textAlign='center';x.textBaseline='middle';
  x.fillText(ch,c.x+cw/2,c.y+chh/2+5);x.restore()}
function clock(t){const cx=920,cy=470,r=86;x.save();x.translate(cx,cy);
  x.fillStyle='#F4F1EA';x.beginPath();x.arc(0,0,r,0,7);x.fill();x.lineWidth=7;x.strokeStyle='#2a2a2a';x.stroke();
  for(let i=0;i<60;i++){x.save();x.rotate(i*Math.PI/30);x.fillStyle='#111';
    if(i%5==0)x.fillRect(-3.5,-r+10,7,20);else x.fillRect(-1.2,-r+10,2.4,7);x.restore()}
  const m=29.2+eo(seg(t,.2,1.6))*.8, h=8+m/60;
  const hand=(a,w,l,b)=>{x.save();x.rotate(a);x.fillStyle='#111';x.fillRect(-w/2,-l,w,l+b);x.restore()};
  hand(h/12*2*Math.PI,10,48,14);hand(m/60*2*Math.PI,8,72,16);
  const s=(t*6)%60;x.save();x.rotate(s/60*2*Math.PI);x.fillStyle='#C8102E';x.fillRect(-1.5,-60,3,82);
  x.beginPath();x.arc(0,-60,9,0,7);x.fill();x.restore();x.fillStyle='#111';x.beginPath();x.arc(0,0,5,0,7);x.fill();x.restore()}
const B=document.getElementById('b'),S=document.getElementById('src');
window.render=t=>{x.clearRect(0,0,1080,1920);clock(t);
  for(const c of cells){
    if(t<c.st||c.n===0){half(seq(c,0),c,true,1);half(seq(c,0),c,false,1)}
    else{const f=(t-c.st)/FD,k=Math.floor(f),p=f-k;
      if(k>=c.n){half(c.c,c,true,1);half(c.c,c,false,1)}
      else{const a=seq(c,k),b=seq(c,k+1);half(b,c,true,1);half(a,c,false,1);
        if(p<.5)half(a,c,true,1-p*2);else half(b,c,false,(p-.5)*2)}}
    x.fillStyle='#000';x.fillRect(c.x,c.y+chh/2-1.5,cw,3)}
  const pb=eo(seg(t,DONE+.2,DONE+1.2));B.style.clipPath=`inset(0 0 ${(1-pb)*100}% 0)`;B.style.opacity=Math.min(1,pb*2);
  S.style.opacity=seg(t,DONE+1.1,DONE+1.7)};
"""
    return page(body, css, js, data)


# ───────────────────────── B · TELEX (news-agency teleprinter) ─────────────────────────
def telex(it, meta):
    head = f'ZCZC BKN{meta["idx"]:03d}  {meta["date_num"]}  08:30'
    data = dict(blocks=[
        dict(cls='h0', txt=head, cps=80, pause=.15),
        dict(cls='h0', txt='BERLİN (BK) —', cps=60, pause=.25),
        dict(cls='tg', txt=tr_upper(it['tag']), cps=40, pause=.3),
        dict(cls='hd', txt=tr_upper(it['title']), cps=24, pause=.45),
        dict(cls='bd', txt=it['body'], cps=72, pause=.35),
        dict(cls='h0', txt=f'KAYNAK: {tr_upper(it["source"])}', cps=50, pause=.25),
        dict(cls='h0', txt='NNNN', cps=12, pause=0)])
    body = (brand() + count(meta, 'rgba(255,255,255,.7)') +
            '<canvas id="g" width="270" height="480" style="position:absolute;inset:0;width:1080px;height:1920px;opacity:.10;mix-blend-mode:overlay;z-index:15"></canvas>'
            '<div id="win"><div id="pp"><div class="perf l"></div><div class="perf r"></div><div id="tx"></div><span id="cur"></span></div></div>')
    css = f"""#s{{background:{RED}}}
#win{{position:absolute;left:60px;right:60px;top:360px;bottom:300px;overflow:hidden;
  -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 140px,#000 100%)}}
#pp{{position:absolute;left:0;right:0;top:0;min-height:3200px;background:#F4EFE4;padding:760px 92px 400px;
  box-shadow:0 30px 80px rgba(0,0,0,.35)}}
.perf{{position:absolute;top:0;bottom:0;width:46px;background:radial-gradient(circle at 23px 23px,#7d0a1d 7px,transparent 8px) 0 0/46px 46px repeat-y}}
.perf.l{{left:8px}}.perf.r{{right:8px}}
#tx{{font-family:MO;color:#141414}}
.blk{{display:block;margin-bottom:22px}}
.h0{{font:500 27px/1.5 MO;letter-spacing:2px;color:#4a4a4a}}
.tg{{display:inline-block;background:{RED};color:#fff;font:700 30px/1 MO;letter-spacing:4px;padding:12px 18px;margin:10px 0 26px}}
.hd{{font:700 72px/1.12 MO;letter-spacing:-1px;color:#111;margin-bottom:34px}}
.bd{{font:500 37px/1.55 MO;color:#1d1d1d}}
.c{{visibility:hidden}}
#cur{{position:absolute;width:.6em;height:1.05em;background:#111;font-size:34px}}"""
    js = r"""
const tx=document.getElementById('tx'),pp=document.getElementById('pp'),cur=document.getElementById('cur');
let t0=.5;const chars=[];
D.blocks.forEach((b,bi)=>{const el=document.createElement('span');el.className='blk '+b.cls;
  [...b.txt].forEach((ch,i)=>{const s=document.createElement('span');s.className='c';s.textContent=ch;
    const id=bi*500+i;s.style.opacity=(.74+rnd(id)*.26).toFixed(2);s.style.position='relative';s.style.top=((rnd(id+3)-.5)*1.6).toFixed(1)+'px';
    el.appendChild(s);chars.push({s,t:t0,blk:el});t0+=ch===' '?.35/b.cps:1/b.cps});
  t0+=b.pause;tx.appendChild(el)});
const END=t0;window.DUR=END+2.6;let y=0,last=-1;
window.render=t=>{let n=0;for(const c of chars){const v=t>=c.t;c.s.style.visibility=v?'visible':'hidden';if(v)n++}
  const lc=chars[Math.max(0,n-1)].s;const cs=getComputedStyle(lc);
  cur.style.fontSize=cs.fontSize;cur.style.left=(lc.offsetLeft+(n?lc.offsetWidth:0)+lc.offsetParent.offsetLeft)+'px';
  cur.style.top=(lc.offsetTop+lc.offsetParent.offsetTop+2)+'px';
  cur.style.opacity=t>END?((Math.floor(t*2.2)%2)?0:1):1;
  const target=Math.min(0,860-(lc.offsetTop+lc.offsetParent.offsetTop));
  y+= (target-y)*.18; pp.style.transform=`translateY(${y.toFixed(1)}px)`;
  const g=document.getElementById('g').getContext('2d'),im=g.createImageData(270,480);
  for(let i=0;i<im.data.length;i+=4){const v=rnd(i+Math.floor(t*30)*7)*255;im.data[i]=im.data[i+1]=im.data[i+2]=v;im.data[i+3]=255}
  g.putImageData(im,0,0)};
"""
    return page(body, css, js, data)


# ───────────────────────── C · BAUHAUS (geometric Fernsehturm + broadcast rings) ─────────────────────────
def bauhaus(it, meta):
    lines = wrap(tr_upper(it['title']), 12)[:4]
    words = it['body'].split()
    hl = ''.join(f'<div class="ln"><div class="band"></div><span>{l}</span></div>' for l in lines)
    bd = ' '.join(f'<span class="w">{w}</span>' for w in words)
    body = (brand(color=BLK, accent=RED, icon_top=BLK) +
            f'<div id="num">{meta["idx"]:02d}</div>'
            '<svg id="geo" width="1080" height="1920" style="position:absolute;inset:0">'
            '<g id="rings"></g>'
            f'<rect id="bar" x="967" y="540" width="26" height="490" fill="{BLK}"/>'
            f'<rect id="ant" x="977" y="300" width="6" height="150" fill="{BLK}"/>'
            f'<circle id="ball" cx="980" cy="540" r="96" fill="{RED}"/>'
            f'<path id="q" d="M0 1920 L0 1560 A360 360 0 0 1 360 1920 Z" fill="{BLK}"/>'
            f'<rect id="sq" x="900" y="1500" width="90" height="90" fill="{RED}"/>'
            '</svg>'
            f'<div id="tag">{tr_upper(it["tag"])}</div><div id="hl">{hl}</div>'
            f'<p id="bd">{bd}</p><div id="src"><i></i>KAYNAK: {it["source"]}</div>')
    css = f"""#s{{background:{CREAM}}}
#num{{position:absolute;left:40px;top:250px;font:800 400px/1 PO;color:transparent;-webkit-text-stroke:3px {BLK};opacity:.9;z-index:1}}
#geo{{z-index:2}}
#tag{{position:absolute;left:70px;top:612px;background:{RED};color:#fff;font:800 30px PO;letter-spacing:5px;padding:10px 22px;z-index:5;transform-origin:0 100%}}
#hl{{position:absolute;left:70px;top:690px;z-index:5}}
.ln{{position:relative;overflow:hidden;margin-bottom:12px;height:118px;width:fit-content}}
.band{{position:absolute;inset:0;background:{BLK};transform-origin:0 50%}}
.ln span{{position:relative;display:block;padding:4px 26px 0;font:800 98px/112px PO;color:{CREAM};letter-spacing:-1px;white-space:nowrap}}
#bd{{position:absolute;left:70px;right:90px;top:{690+len(lines)*130+40}px;font:500 37px/1.5 IN;color:#1a1a1a;z-index:5}}
.w{{display:inline-block}}
#src{{position:absolute;left:70px;bottom:400px;font:600 24px IN;letter-spacing:3px;color:#333;display:flex;align-items:center;gap:16px;z-index:5}}
#src i{{display:block;width:60px;height:4px;background:{BLK}}}"""
    js = r"""
const $=i=>document.getElementById(i),bounce=p=>{const n=7.5625,d=2.75;if(p<1/d)return n*p*p;if(p<2/d)return n*(p-=1.5/d)*p+.75;if(p<2.5/d)return n*(p-=2.25/d)*p+.9375;return n*(p-=2.625/d)*p+.984375};
const lines=[...document.querySelectorAll('.ln')],ws=[...document.querySelectorAll('.w')],NS='http://www.w3.org/2000/svg',rg=$('rings');
const rings=[...Array(6)].map(()=>{const c=document.createElementNS(NS,'circle');c.setAttribute('cx',980);c.setAttribute('cy',540);
  c.setAttribute('fill','none');c.setAttribute('stroke','#111');rg.appendChild(c);return c});
const T_BODY=1.6+lines.length*.14+.5, T_END=T_BODY+ws.length*.03+.6;window.DUR=Math.max(8,T_END+3);
window.render=t=>{
  $('ball').setAttribute('cy',(-150+690*bounce(seg(t,0,.85))).toFixed(1));
  const pb=eo(seg(t,.55,1.15));$('bar').setAttribute('y',1030-490*pb);$('bar').setAttribute('height',490*pb);
  const pa=eo(seg(t,1.0,1.35));$('ant').setAttribute('y',444-150*pa);$('ant').setAttribute('height',150*pa);
  const pn=eo(seg(t,.5,1.2));$('num').style.transform=`translateX(${(pn-1)*500}px) rotate(${(pn-1)*12}deg)`;
  const pq=eo(seg(t,.2,1.0));$('q').style.transform=`scale(${pq})`;$('q').style.transformOrigin='0px 1920px';
  $('sq').style.transform=`rotate(${t*22}deg)`;$('sq').style.transformOrigin='945px 1545px';$('sq').style.opacity=seg(t,.6,1);
  const pt=eo(seg(t,1.0,1.45));$('tag').style.transform=`rotate(${(1-pt)*-90}deg)`;$('tag').style.opacity=pt;
  lines.forEach((l,i)=>{const a=1.15+i*.14,pw=eio(seg(t,a,a+.45)),ps=eo(seg(t,a+.25,a+.8));
    l.querySelector('.band').style.transform=`scaleX(${pw})`;l.querySelector('span').style.transform=`translateY(${(1-ps)*120}px)`});
  ws.forEach((w,i)=>{const p=eo(seg(t,T_BODY+i*.03,T_BODY+i*.03+.45));w.style.opacity=p;w.style.transform=`translateY(${(1-p)*18}px)`});
  $('src').style.opacity=seg(t,T_END,T_END+.5);
  rings.forEach((c,i)=>{const ph=t-1.4-i*1.1;const p=ph<0?0:(ph%6.6)/2.6;const on=ph>=0&&p<=1;
    c.setAttribute('r',96+p*620);c.setAttribute('stroke-width',4-p*2.5);c.setAttribute('opacity',on?(1-p)*.8:0)})};
"""
    return page(body, css, js)


STYLES = dict(fallblatt=fallblatt, telex=telex, bauhaus=bauhaus)

from styles2 import STYLES2  # noqa: E402
STYLES.update(STYLES2)
