"""Second batch of animated story styles: U-Bahn, Extrablatt, Radar, Redaksiyon, Prismenwender."""
from common import page, brand, b2, tv, tr_upper, wrap, RED, BLK, CREAM


def count(meta, color, top=268):
    return (f'<div style="position:absolute;right:80px;top:{top}px;font:600 24px IN;letter-spacing:4px;color:{color};z-index:20">'
            f'{meta["idx"]} / {meta["total"]}</div>')


# ───────────────────────── 4 · U-BAHN (line drawing + BVG-yellow train) ─────────────────────────
def ubahn(it, meta):
    path = 'M -80 470 L 60 470 L 130 540 L 130 1480 L 200 1550 L 1160 1550'
    body = (brand(color=BLK, accent=RED, icon_top=BLK) + count(meta, '#555') +
            '<svg width="1080" height="1920" style="position:absolute;inset:0">'
            f'<path d="{path}" stroke="#E4E0D7" stroke-width="34" fill="none" stroke-linejoin="round"/>'
            f'<path id="ln" d="{path}" stroke="{RED}" stroke-width="34" fill="none" stroke-linejoin="round"/>'
            '<g id="sts"></g>'
            '<g id="tr"><rect x="-56" y="-22" width="112" height="44" rx="20" fill="#F0D722" stroke="#111" stroke-width="5"/>'
            '<rect x="-40" y="-11" width="22" height="14" rx="3" fill="#111"/><rect x="-11" y="-11" width="22" height="14" rx="3" fill="#111"/>'
            '<rect x="18" y="-11" width="22" height="14" rx="3" fill="#111"/></g></svg>'
            f'<div class="lb" data-y="640" style="top:612px"><span class="badge">{tr_upper(it["tag"])}</span></div>'
            f'<div class="lb" data-y="770" style="top:735px"><div class="next">SONRAKİ DURAK</div><h1>{it["title"]}</h1></div>'
            f'<div class="lb" data-y="1130" style="top:1102px"><p>{it["body"]}</p></div>'
            f'<div class="lb" data-y="1420" style="top:1404px"><div class="src">KAYNAK: {it["source"]}</div></div>')
    css = f"""#s{{background:#F6F4EF}}
.lb{{position:absolute;left:196px;right:60px;z-index:5}}
.badge{{display:inline-block;background:{RED};color:#fff;font:800 34px PO;letter-spacing:3px;padding:8px 22px;border-radius:12px}}
.next{{font:700 22px MO;letter-spacing:5px;color:{RED};margin-bottom:6px}}
h1{{font:800 80px/1.05 PO;color:#111;letter-spacing:-1.5px}}
p{{font:500 37px/1.5 IN;color:#2a2a2a}}
.src{{font:600 24px IN;letter-spacing:3px;color:#666}}"""
    js = r"""
const ln=document.getElementById('ln'),L=ln.getTotalLength(),tr=document.getElementById('tr'),NS='http://www.w3.org/2000/svg';
ln.style.strokeDasharray=L;
const lbs=[...document.querySelectorAll('.lb')];
const lenAtY=y=>{let lo=0,hi=L;for(let k=0;k<40;k++){const m=(lo+hi)/2;const p=ln.getPointAtLength(m);(p.y<y||p.x<120)?lo=m:hi=m}return lo};
const st=lbs.map(l=>{const y=+l.dataset.y,len=lenAtY(y);const c=document.createElementNS(NS,'circle');c.setAttribute('cx',130);c.setAttribute('cy',y);
  c.setAttribute('r',24);c.setAttribute('fill','#fff');c.setAttribute('stroke','#111');c.setAttribute('stroke-width',8);
  c.style.transformOrigin=`130px ${y}px`;document.getElementById('sts').appendChild(c);return {l,c,len}});
const V=520,DW=.45;let T=.3,P=0;const keys=[[T,0]];
st.forEach(s=>{T+=(s.len-P)/V;keys.push([T,s.len]);s.arr=T;T+=DW;keys.push([T,s.len]);P=s.len});
T+=(L-P)/V;keys.push([T,L]);window.DUR=T+1.2;
function headAt(t){if(t<=keys[0][0])return 0;for(let i=1;i<keys.length;i++){const[a,la]=keys[i-1],[b,lb]=keys[i];
  if(t<=b){return la+(lb-la)*(b>a?eio((t-a)/(b-a)):1)}}return L}
window.render=t=>{const h=headAt(t);ln.style.strokeDashoffset=L-h;
  const p=ln.getPointAtLength(Math.max(0,h-40)),q=ln.getPointAtLength(Math.min(L,h-39));
  const ang=Math.atan2(q.y-p.y,q.x-p.x)*180/Math.PI;tr.setAttribute('transform',`translate(${p.x},${p.y}) rotate(${ang})`);
  st.forEach(s=>{const k=eo(seg(t,s.arr-.15,s.arr+.2));s.c.style.transform=`scale(${k<1?k*1.25:1})`;
    const r=eo(seg(t,s.arr,s.arr+.55));s.l.style.clipPath=`inset(0 ${(1-r)*100}% 0 0)`;s.l.style.transform=`translateX(${(1-r)*-30}px)`})};
"""
    return page(body, css, js)


# ───────────────────────── 5 · EXTRABLATT (newspaper front page, stamped) ─────────────────────────
def extrablatt(it, meta):
    words = it['title'].split()
    hl = ' '.join(f'<span class="hw">{w}</span>' for w in words)
    body = ('<div id="cam">'
            '<div id="pg"><canvas id="nz" width="245" height="322"></canvas>'
            '<div class="mh">Berlin Gündemi</div>'
            f'<div class="dl"><span>SAYI {meta["idx"]:03d}</span><span>{meta["date_long"]}</span><span>BERLİN BASKISI</span></div>'
            f'<div class="kk">{tr_upper(it["tag"])}</div><h1>{hl}</h1>'
            f'<div class="cols"><p>{it["body"]}</p></div>'
            f'<div class="ft">KAYNAK: {it["source"]} · @berlin.konusuyor</div>'
            '<div id="stamp">EXTRA</div></div></div>')
    css = f"""#s{{background:radial-gradient(90% 70% at 50% 40%,#3a332c 0%,#15120f 100%)}}
#cam{{position:absolute;inset:0;transform-origin:50% 45%}}
#pg{{position:absolute;left:58px;top:300px;width:964px;height:1290px;background:#EEE7D6;padding:44px 52px;
  box-shadow:0 40px 90px rgba(0,0,0,.6);overflow:hidden}}
#nz{{position:absolute;inset:0;width:100%;height:100%;opacity:.16;mix-blend-mode:multiply;pointer-events:none}}
.mh{{font:700 118px/1 FK;text-align:center;color:#111;padding-bottom:16px}}
.dl{{display:flex;justify-content:space-between;border-top:5px double #111;border-bottom:5px double #111;padding:10px 4px;
  font:400 22px PF;letter-spacing:3px;color:#222;text-transform:uppercase}}
.kk{{font:900 28px PF;letter-spacing:6px;color:{RED};margin:34px 0 10px}}
h1{{font:900 116px/1.0 PF;color:#111;letter-spacing:-2px}}
.hw{{display:inline-block}}
.cols{{column-count:2;column-gap:42px;column-rule:1px solid #9a9080;margin-top:36px;border-top:2px solid #111;padding-top:26px}}
.cols p{{font:400 36px/1.42 PF;color:#1c1c1c;text-align:justify;hyphens:auto}}
.cols p::first-letter{{float:left;font:900 118px/.86 PF;margin:6px 12px 0 0;color:{RED}}}
.ft{{position:absolute;left:52px;right:52px;bottom:36px;border-top:1px solid #111;padding-top:12px;font:400 20px PF;letter-spacing:3px;color:#444}}
#stamp{{position:absolute;right:46px;top:150px;font:800 74px PO;letter-spacing:10px;color:{RED};border:8px solid {RED};padding:2px 22px 0;
  outline:3px solid {RED};outline-offset:6px;transform:rotate(-14deg);mix-blend-mode:multiply;
  -webkit-mask-image:radial-gradient(circle at 30% 40%,#000 55%,rgba(0,0,0,.55) 75%,#000 90%)}}"""
    js = r"""
const $=i=>document.getElementById(i),hw=[...document.querySelectorAll('.hw')];
{const g=$('nz').getContext('2d'),im=g.createImageData(245,322);for(let i=0;i<im.data.length;i+=4){const v=180+rnd(i)*75;im.data[i]=im.data[i+1]=im.data[i+2]=v;im.data[i+3]=255}g.putImageData(im,0,0)}
const TH=1.45,TB=TH+hw.length*.13+.25,TS=TB+1.1;window.DUR=Math.max(8,TS+3);
const fx=(el,p,blur)=>{el.style.opacity=p;el.style.filter=p<1?`blur(${(1-p)*blur}px)`:'none'};
window.render=t=>{
  const pp=eo(seg(t,0,.85));$('pg').style.transform=`translateY(${(1-pp)*1500}px) rotate(${(1-pp)*9-1.2}deg)`;
  let sh=0;if(t>TS&&t<TS+.18)sh=(rnd(Math.floor(t*60))-.5)*14;
  $('cam').style.transform=`scale(${1+.055*seg(t,.8,window.DUR)}) translate(${sh}px,${sh*.6}px)`;
  const pm=seg(t,.7,1.1);fx(document.querySelector('.mh'),pm<1?(Math.floor(t*40)%3?pm:pm*.4):1,6);
  fx(document.querySelector('.dl'),eo(seg(t,1.0,1.3)),3);fx(document.querySelector('.kk'),eo(seg(t,1.25,1.45)),3);
  hw.forEach((w,i)=>{const a=TH+i*.13,p=eo(seg(t,a,a+.28));w.style.opacity=p;w.style.transform=`scale(${1.7-.7*p})`;w.style.filter=p<1?`blur(${(1-p)*8}px)`:'none'});
  const pb=eio(seg(t,TB,TB+1));document.querySelector('.cols').style.clipPath=`inset(0 0 ${(1-pb)*100}% 0)`;
  document.querySelector('.ft').style.opacity=seg(t,TB+.6,TB+1);
  const ps=seg(t,TS,TS+.16);$('stamp').style.opacity=ps*.9;$('stamp').style.transform=`rotate(-14deg) scale(${2.4-1.4*eo(ps)})`};
"""
    return page(body, css, js)


# ───────────────────────── 6 · GÜNDEM RADARI (Berlin sweep + decrypt headline) ─────────────────────────
def radar(it, meta):
    title = tr_upper(it['title'])
    hl = ' '.join('<span style="white-space:nowrap;display:inline-block">' + ''.join(f'<span class="d" data-c="{c}">{c}</span>' for c in w) + '</span>' for w in title.split())
    body = (brand() + count(meta, 'rgba(255,255,255,.55)') +
            '<canvas id="c" width="1080" height="1920" style="position:absolute;inset:0"></canvas>'
            '<div id="ro1" class="ro" style="left:80px;top:985px"></div><div id="ro2" class="ro" style="right:80px;top:985px;text-align:right"></div>'
            '<div class="ro" style="left:80px;top:350px;color:#F05A6E">GÜNDEM RADARI</div>'
            f'<div id="tg">{tr_upper(it["tag"])}</div><h1 id="h">{hl}</h1><p id="b">{it["body"]}</p>'
            f'<div id="src">KAYNAK: {it["source"]}</div>')
    css = f"""#s{{background:#0a0a0b}}
.ro{{position:absolute;font:500 22px MO;letter-spacing:3px;color:rgba(255,255,255,.6);z-index:5}}
#tg{{position:absolute;left:80px;top:1050px;font:700 26px MO;letter-spacing:5px;color:#fff;background:{RED};padding:8px 16px}}
h1{{position:absolute;left:80px;right:70px;top:1110px;font:800 70px/1.08 PO;color:#fff;letter-spacing:-1px}}
.d{{display:inline-block;min-width:.2em}}
#b{{position:absolute;left:80px;right:80px;top:1300px;font:500 34px/1.45 IN;color:#BDBDBD}}
#src{{position:absolute;left:80px;top:1545px;font:600 22px IN;letter-spacing:3px;color:rgba(255,255,255,.45)}}"""
    js = r"""
const cv=document.getElementById('c'),x=cv.getContext('2d'),CX=540,CY=660,R=300,W=2*Math.PI/2.6,TAU=2*Math.PI;
const SH=[[-.95,-.1],[-.82,-.42],[-.5,-.52],[-.25,-.8],[.12,-.76],[.38,-.58],[.64,-.52],[.76,-.22],[.96,.04],[.98,.34],[.8,.6],[.55,.54],[.36,.76],[.06,.62],[-.2,.5],[-.42,.6],[-.62,.44],[-.76,.2],[-.92,.14]];
const blips=[...Array(16)].map((_,i)=>{const a=rnd(i+1)*TAU,r=(.25+rnd(i+40)*.6)*R;return {x:CX+Math.cos(a)*r,y:CY+Math.sin(a)*r*.82}});
const TG={x:CX+6,y:CY-14};const tgA=(Math.atan2(TG.y-CY,TG.x-CX)+TAU)%TAU;
const sweep=t=>(t*W-Math.PI/2)%TAU;let lock=null;for(let t=.6;t<6;t+=1/120){if(Math.abs(((sweep(t)-tgA)+TAU)%TAU)<.03){lock=t;break}}
const ds=[...document.querySelectorAll('.d')],GL='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ#%&@0123456789';
const TH=lock+.5,TB=TH+ds.length*.025+.4;window.DUR=Math.max(8,TB+3);
const $=i=>document.getElementById(i);
window.render=t=>{x.clearRect(0,0,1080,1920);const on=eo(seg(t,0,.7));x.save();x.globalAlpha=on;
  x.strokeStyle='rgba(200,16,46,.45)';x.lineWidth=2;for(let k=1;k<=4;k++){x.beginPath();x.arc(CX,CY,R*k/4*(.85+.15*on),0,TAU);x.stroke()}
  x.beginPath();x.moveTo(CX-R,CY);x.lineTo(CX+R,CY);x.moveTo(CX,CY-R);x.lineTo(CX,CY+R);x.stroke();
  for(let d=0;d<360;d+=5){const a=d*Math.PI/180,l=d%30?10:22;x.beginPath();x.moveTo(CX+Math.cos(a)*R,CY+Math.sin(a)*R);x.lineTo(CX+Math.cos(a)*(R+l),CY+Math.sin(a)*(R+l));x.stroke()}
  x.beginPath();SH.forEach(([a,b],i)=>{const px=CX+a*R*.82,py=CY+b*R*.82;i?x.lineTo(px,py):x.moveTo(px,py)});x.closePath();
  x.fillStyle='rgba(200,16,46,.07)';x.fill();x.strokeStyle='rgba(255,255,255,.55)';x.lineWidth=3;x.setLineDash([10,7]);x.stroke();x.setLineDash([]);
  const sa=sweep(t);if(t>.3){for(let k=0;k<46;k++){x.beginPath();x.moveTo(CX,CY);x.arc(CX,CY,R,sa-(k+1)*.022,sa-k*.022);x.closePath();
    x.fillStyle=`rgba(200,16,46,${.42*(1-k/46)})`;x.fill()}
    x.strokeStyle='#ff2d4a';x.lineWidth=4;x.beginPath();x.moveTo(CX,CY);x.lineTo(CX+Math.cos(sa)*R,CY+Math.sin(sa)*R);x.stroke()}
  const glow=(px,py,b,r)=>{x.fillStyle=`rgba(255,255,255,${b})`;x.shadowColor='#ff2d4a';x.shadowBlur=18*b;x.beginPath();x.arc(px,py,r,0,TAU);x.fill();x.shadowBlur=0};
  blips.forEach(b=>{const a=(Math.atan2(b.y-CY,b.x-CX)+TAU)%TAU,dt=(((sa-a)%TAU)+TAU)%TAU/W;if(t>.4)glow(b.x,b.y,Math.exp(-dt*1.6)*.9,5)});
  if(t>=lock){const p=eo(seg(t,lock,lock+.5));glow(TG.x,TG.y,1,9);
    for(let k=0;k<2;k++){const ph=((t-lock)*1.2+k*.5)%1;x.strokeStyle=`rgba(255,45,74,${1-ph})`;x.lineWidth=3;x.beginPath();x.arc(TG.x,TG.y,10+ph*60,0,TAU);x.stroke()}
    const s=34+(1-p)*80;x.strokeStyle='#fff';x.lineWidth=4;
    [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([u,v])=>{x.beginPath();x.moveTo(TG.x+u*s,TG.y+v*s-v*14);x.lineTo(TG.x+u*s,TG.y+v*s);x.lineTo(TG.x+u*s-u*14,TG.y+v*s);x.stroke()});
    const q=eo(seg(t,lock+.3,lock+.8));x.strokeStyle='rgba(255,255,255,.8)';x.lineWidth=2;x.beginPath();x.moveTo(TG.x+s,TG.y-s);
    x.lineTo(TG.x+s+q*150,TG.y-s-q*150);x.lineTo(TG.x+s+q*150+q*120,TG.y-s-q*150);x.stroke();
    if(q>.95){x.fillStyle='#fff';x.font='500 22px MO';x.fillText('52.52°N 13.40°E',TG.x+s+60,TG.y-s-160)}}
  x.restore();
  const deg=((sa+Math.PI/2)*180/Math.PI+360)%360;$('ro1').textContent='AÇI '+deg.toFixed(0).padStart(3,'0')+'°';
  $('ro2').textContent='08:30:'+String(Math.floor(t)).padStart(2,'0')+(t>=lock?'  ● HEDEF':'  ○ TARANIYOR');
  $('tg').style.opacity=seg(t,lock+.2,lock+.5);
  ds.forEach((d,i)=>{const a=TH+i*.025;if(t<a-.4)d.style.opacity=0;else{d.style.opacity=1;
    d.textContent=t<a?GL[Math.floor(rnd(i*13+Math.floor(t*24))*GL.length)]:d.dataset.c;d.style.color=t<a?'#ff2d4a':'#fff'}});
  const pb=eo(seg(t,TB,TB+.8));$('b').style.opacity=pb;$('b').style.transform=`translateY(${(1-pb)*24}px)`;$('src').style.opacity=seg(t,TB+.6,TB+1.1)};
"""
    return page(body, css, js)


# ───────────────────────── 7 · REDAKSİYON MASASI (collage: Dymo, torn paper, tape, marker) ─────────────────────────
def redaksiyon(it, meta):
    words = it['title'].split()
    hl = ' '.join(words[:-1]) + f' <span id="hw">{words[-1]}</span>'
    body = (brand() + count(meta, 'rgba(255,255,255,.55)') +
            '<canvas id="nz" width="270" height="480" style="position:absolute;inset:0;width:1080px;height:1920px;opacity:.08"></canvas>'
            f'<div id="dy">{tr_upper(it["tag"])}</div>'
            f'<div id="st"><h1>{hl}</h1></div><div class="tp" id="t1"></div><div class="tp" id="t2"></div>'
            f'<div id="cd"><p>{it["body"]}</p><div id="pin"></div></div>'
            '<svg id="mk" width="1080" height="1920" style="position:absolute;inset:0;z-index:9;pointer-events:none">'
            f'<path id="ci" fill="none" stroke="{RED}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity=".92"/>'
            '<path id="ar" fill="none" stroke="#FF4D63" stroke-width="6" stroke-linecap="round"/></svg>'
            f'<div id="nt">kaynak: {it["source"]} ✓</div>')
    torn = 'polygon(' + ','.join(
        [f'{x}% {1.6 + ((x * 37) % 7) / 3:.1f}%' for x in range(0, 101, 4)] +
        [f'{x}% {98.4 - ((x * 53) % 7) / 3:.1f}%' for x in range(100, -1, -4)]) + ')'
    css = f"""#s{{background:#262629}}
#dy{{position:absolute;left:90px;top:560px;background:linear-gradient(#1a1a1a,#0c0c0c);color:#F2F2F2;font:700 40px MO;letter-spacing:9px;
  padding:14px 30px;border-radius:8px;z-index:6;text-shadow:0 1px 0 rgba(255,255,255,.35),0 -1px 0 #000;box-shadow:0 8px 20px rgba(0,0,0,.5)}}
#st{{position:absolute;left:44px;right:44px;top:660px;background:#F7F4ED;padding:46px 56px 50px;clip-path:{torn};z-index:4;
  filter:drop-shadow(0 18px 24px rgba(0,0,0,.45))}}
h1{{font:800 84px/1.08 PO;color:#111;letter-spacing:-1.5px}}
.tp{{position:absolute;width:180px;height:56px;background:rgba(236,224,186,.62);z-index:7;
  clip-path:polygon(3% 0,97% 4%,100% 50%,96% 100%,2% 96%,0 50%)}}
#t1{{left:20px;top:640px;transform:rotate(-28deg)}}#t2{{right:24px;top:640px;transform:rotate(24deg)}}
#cd{{position:absolute;left:96px;right:96px;top:1060px;background:#FFFDF6 repeating-linear-gradient(#FFFDF6 0 52px,#9EC3E6 52px 54px);
  background-position:0 34px;padding:34px 46px 46px 92px;z-index:3;box-shadow:0 18px 30px rgba(0,0,0,.45)}}
#cd::before{{content:'';position:absolute;left:66px;top:0;bottom:0;width:2px;background:#E8797F}}
#cd p{{font:500 31px/54px MO;color:#1b1b1b}}
#pin{{position:absolute;left:50%;top:-14px;width:40px;height:40px;margin-left:-20px;border-radius:50%;
  background:radial-gradient(circle at 35% 30%,#ff7a8a,{RED} 55%,#7d0a1d);box-shadow:4px 8px 10px rgba(0,0,0,.45)}}
#nt{{position:absolute;right:90px;top:1500px;font:700 58px HW;color:#FF4D63;transform:rotate(-6deg);z-index:9}}"""
    js = r"""
const $=i=>document.getElementById(i);
{const g=$('nz').getContext('2d'),im=g.createImageData(270,480);for(let i=0;i<im.data.length;i+=4){const v=rnd(i*.7)*255;im.data[i]=im.data[i+1]=im.data[i+2]=v;im.data[i+3]=255}g.putImageData(im,0,0)}
const cd=$('cd'),st=$('st');let CL=1,AL=1,ready=false;function init(){cd.style.top=(st.offsetTop+st.offsetHeight+60)+'px';
st.style.transform='rotate(-1.5deg)';cd.style.transform='rotate(1.2deg)';$('dy').style.transform='rotate(-4deg)';
const r=$('hw').getBoundingClientRect();const cx=r.left+r.width/2,cy=r.top+r.height/2+4,rx=r.width/2+34,ry=r.height/2+18;
let d='';for(let k=0;k<=86;k++){const a=-2.4+k/86*2.25*Math.PI,j=1+(rnd(k)-.5)*.06;d+=(k?'L':'M')+(cx+Math.cos(a)*rx*j).toFixed(1)+' '+(cy+Math.sin(a)*ry*j*(1+k/300)).toFixed(1)}
$('ci').setAttribute('d',d);CL=$('ci').getTotalLength();$('ci').style.strokeDasharray=CL;
const nt=$('nt'),nb=nt.getBoundingClientRect();const ax=nb.left+60,ay=nb.top-10;
$('ar').setAttribute('d',`M${ax} ${ay} Q ${ax-60} ${ay-80} ${ax-20} ${ay-150} M${ax-20} ${ay-150} l -26 22 M${ax-20} ${ay-150} l 30 14`);
AL=$('ar').getTotalLength();$('ar').style.strokeDasharray=AL;ready=true}window.DUR=8;
const back=p=>{const c1=1.7,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
window.render=t=>{if(!ready)init();
  const pd=seg(t,.25,.75);$('dy').style.transform=`translateY(${(1-back(pd))*-420}px) rotate(${-4-(1-pd)*30}deg)`;$('dy').style.opacity=pd>0?1:0;
  const ps=seg(t,.55,1.2);st.style.transform=`translateX(${(1-back(ps))*-1300}px) rotate(${-1.5-(1-ps)*9}deg)`;
  [['t1',1.25],['t2',1.38]].forEach(([id,a])=>{const p=eo(seg(t,a,a+.22));const base=id=='t1'?-28:24;
    $(id).style.opacity=p;$(id).style.transform=`rotate(${base}deg) scale(${1.6-.6*p})`});
  const pc=seg(t,1.6,2.25);cd.style.transform=`translateY(${(1-back(pc))*1100}px) rotate(${1.2+(1-pc)*8}deg)`;
  const pp=eo(seg(t,2.25,2.45));$('pin').style.transform=`translateY(${(1-pp)*-60}px) scale(${1.5-.5*pp})`;$('pin').style.opacity=pp;
  $('ci').style.strokeDashoffset=CL*(1-eio(seg(t,2.7,3.5)));
  $('nt').style.clipPath=`inset(-20% ${(1-seg(t,3.6,4.3))*100}% -20% 0)`;$('ar').style.strokeDashoffset=AL*(1-eo(seg(t,4.2,4.7)));
  document.getElementById('s').style.transform=`scale(${1+.03*seg(t,0,8)}) rotate(${.3*Math.sin(t*.6)}deg)`};
"""
    return page(body, css, js)


# ───────────────────────── 8 · PRISMENWENDER (rotating prism billboard, 3D) ─────────────────────────
def prisma(it, meta):
    N, W, H = 22, 44, 1208
    face_a = (f'<div class="fa">{tv(400)}<div class="w1">BERLİN</div><div class="w2">KONUŞUYOR</div>'
              '<div class="w3">HER SABAH 08:30 · GÜNDEM</div></div>')
    face_b = (f'<div class="fb"><span class="tg">{tr_upper(it["tag"])}</span><h1>{it["title"]}</h1><i class="bar"></i>'
              f'<p>{it["body"]}</p>' + (f'<div class="et"><b>SANA ETKİSİ</b>{it["etki"]}</div>' if it.get('etki') else '') + f'<div class="src">KAYNAK: {it["source"]}</div>'
              f'<div class="ft">{b2(52, "#111")}<span>BERLİN GÜNDEMİ · {meta["idx"]}/{meta["total"]}</span></div></div>')
    face_c = '<div class="fc0"></div>'
    slats = ''.join(
        f'<div class="sl" style="left:{i*W}px">' +
        ''.join(f'<div class="fc" style="transform:rotateY({k*120}deg) translateZ(12.7px)"><div class="cnt" style="left:{-i*W}px">{f}</div><div class="sh"></div></div>'
                for k, f in enumerate([face_a, face_b, face_c])) + '</div>' for i in range(N))
    body = (brand() + count(meta, 'rgba(255,255,255,.6)') +
            f'<div id="fr"><div id="in">{slats}</div><div id="gl"></div></div>')
    css = f"""#s{{background:radial-gradient(70% 45% at 50% 52%,#3a3a40 0%,#101012 75%)}}
#fr{{position:absolute;left:40px;top:360px;width:1000px;height:1240px;padding:16px;background:linear-gradient(#8d8d92,#55555a);
  box-shadow:0 30px 80px rgba(0,0,0,.7),inset 0 0 0 2px #2a2a2e}}
#in{{position:relative;width:{N*W}px;height:{H}px;perspective:2600px;background:#000;overflow:hidden}}
.sl{{position:absolute;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}}
.fc{{position:absolute;inset:0;overflow:hidden;backface-visibility:hidden}}
.cnt{{position:absolute;top:0;width:{N*W}px;height:{H}px}}
.sh{{position:absolute;inset:0;background:#000;opacity:0}}
.fa{{position:absolute;inset:0;background:{RED};display:flex;flex-direction:column;align-items:center;padding-top:150px}}
.w1{{font:800 120px/1 PO;color:#fff;margin-top:60px;letter-spacing:2px}}.w2{{font:800 96px/1.05 PO;color:#111}}
.w3{{position:absolute;bottom:90px;font:600 28px IN;letter-spacing:6px;color:#fff}}
.fb{{position:absolute;inset:0;background:#F7F5F0;padding:90px 70px}}
.tg{{display:inline-block;background:{RED};color:#fff;font:800 30px PO;letter-spacing:4px;padding:10px 22px;border-radius:6px}}
.fb h1{{font:800 84px/1.06 PO;color:#111;letter-spacing:-1.5px;margin:34px 0 30px}}
.bar{{display:block;width:120px;height:10px;background:{RED};border-radius:5px;margin-bottom:34px}}
.fb p{{font:500 38px/1.48 IN;color:#262626}}
.fb .et{{margin-top:24px;border-left:8px solid {RED};background:rgba(200,16,46,.07);padding:14px 20px;font:600 32px/1.4 IN;color:#111}}
.fb .et b{{display:block;font:800 20px PO;letter-spacing:4px;color:{RED}}}
.src{{position:absolute;left:70px;bottom:160px;font:600 24px IN;letter-spacing:3px;color:#777}}
.ft{{position:absolute;left:70px;right:70px;bottom:60px;display:flex;align-items:center;gap:16px;font:600 22px IN;letter-spacing:4px;color:#111;
  border-top:2px solid #111;padding-top:18px}}
.fc0{{position:absolute;inset:0;background:#111}}
#gl{{position:absolute;inset:16px;pointer-events:none;background:linear-gradient(115deg,transparent 40%,rgba(255,255,255,.28) 50%,transparent 60%) no-repeat;
  background-size:300% 100%;mix-blend-mode:screen}}"""
    js = r"""
const sls=[...document.querySelectorAll('.sl')],N=sls.length,r=12.7;window.DUR=8;
const back=p=>{const c1=1.3,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
window.render=t=>{
  sls.forEach((s,i)=>{const a=1.5+i*.05,p=seg(t,a,a+.75),ang=120*(p>0?back(p):0);
    s.style.transform=`translateZ(${-r}px) rotateY(${-ang}deg)`;
    [...s.children].forEach((f,k)=>{const fa=(k*120-ang)*Math.PI/180;f.querySelector('.sh').style.opacity=Math.min(.85,Math.abs(Math.sin(fa))*.9+(Math.cos(fa)<0?.6:0))})});
  const g=seg(t,.2,1.3);document.getElementById('gl').style.backgroundPosition=`${120-g*140}% 0`;
  document.getElementById('gl').style.opacity=g>0&&g<1?1:0};
"""
    return page(body, css, js)


STYLES2 = dict(ubahn=ubahn, extrablatt=extrablatt, radar=radar, redaksiyon=redaksiyon, prisma=prisma)
