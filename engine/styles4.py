"""Batch 4: U-Bahn Einfahrt, Neon, Mauer (graffiti), Kiez (isometric city)."""
from common import page, brand, tr_upper, wrap, RED, BLK


def count(meta, color):
    return (f'<div style="position:absolute;right:80px;top:268px;font:600 24px IN;letter-spacing:4px;color:{color};z-index:20">'
            f'{meta["idx"]} / {meta["total"]}</div>')


# ───────────── U-BAHN EINFAHRT: train arrives, stops, leaves → wipes in the wall poster ─────────────
def ubahn2(it, meta):
    cars = ''.join(f'<div class="car" style="left:{k*820}px"><div class="led"><span class="mq">'
                   f'{tr_upper(it["tag"])} · {tr_upper(it["title"])} · BERLİN GÜNDEMİ · </span></div>'
                   + ''.join(f'<i class="win" style="left:{40+w*190}px"></i>' for w in range(4))
                   + '<b class="door" style="left:250px"></b><b class="door" style="left:560px"></b></div>' for k in range(3))
    body = (brand(color=BLK, accent=RED, icon_top=BLK) + count(meta, '#444') +
            f'<div id="sign"><span class="u">U</span>{it["tag"]}</div>'
            f'<div id="po"><span class="tg">{tr_upper(it["tag"])}</span><h1>{it["title"]}</h1><i class="bar"></i><p>{it["body"]}</p>' + (f'<div class="et"><b>SANA ETKİSİ</b>{it["etki"]}</div>' if it.get('etki') else '') +
            f'<div class="src">KAYNAK: {it["source"]}</div></div>'
            f'<div id="tr">{cars}</div><div id="edge"></div><div id="fl"></div>')
    css = f"""#s{{background:#E8E1CC;background-image:linear-gradient(#cfc6ad 2px,transparent 2px),linear-gradient(90deg,#cfc6ad 2px,transparent 2px);
  background-size:64px 64px}}
#s::before{{content:'';position:absolute;left:0;right:0;top:500px;height:46px;background:{RED}}}
#s::after{{content:'';position:absolute;left:0;right:0;top:556px;height:12px;background:#111}}
#sign{{position:absolute;left:50%;top:370px;transform:translateX(-50%);background:#14284B;color:#fff;font:800 58px PO;padding:14px 46px 10px 26px;
  border:5px solid #fff;outline:4px solid #14284B;display:flex;align-items:center;gap:22px;z-index:3;white-space:nowrap}}
.u{{display:inline-grid;place-items:center;width:62px;height:62px;background:#1F5BA8;border-radius:8px;font:800 50px PO}}
#po{{position:absolute;left:60px;right:60px;top:640px;height:850px;background:#FBF9F3;padding:58px 60px;box-shadow:0 14px 30px rgba(0,0,0,.25);z-index:2}}
.tg{{display:inline-block;background:{RED};color:#fff;font:800 30px PO;letter-spacing:4px;padding:10px 22px;border-radius:6px}}
#po h1{{font:800 82px/1.06 PO;color:#111;letter-spacing:-1.5px;margin:30px 0 28px}}
.bar{{display:block;width:120px;height:10px;background:{RED};border-radius:5px;margin-bottom:30px}}
#po p{{font:500 35px/1.46 IN;color:#262626}}
.et{{margin-top:22px;border-left:8px solid {RED};background:rgba(200,16,46,.07);padding:12px 18px;font:600 30px/1.4 IN;color:#111}}
.et b{{display:block;font:800 19px PO;letter-spacing:4px;color:{RED}}}
.src{{position:absolute;left:60px;bottom:44px;font:600 24px IN;letter-spacing:3px;color:#777}}
#tr{{position:absolute;top:610px;left:0;height:900px;width:2460px;z-index:6}}
.car{{position:absolute;top:0;width:812px;height:900px;background:linear-gradient(#F6DC2A,#E9C813 70%,#C9A70A);border-radius:30px 30px 0 0;
  box-shadow:inset 0 -120px 0 #2b2b2b,inset 0 6px 0 rgba(255,255,255,.4)}}
.led{{position:absolute;left:40px;top:40px;width:420px;height:70px;background:#0b0b0b;border-radius:6px;overflow:hidden}}
.mq{{position:absolute;top:12px;left:0;white-space:nowrap;font:700 40px MO;color:#FF9E1B;text-shadow:0 0 10px rgba(255,158,27,.8);letter-spacing:2px}}
.win{{position:absolute;top:160px;width:150px;height:250px;background:linear-gradient(160deg,#e9eef0,#9fb0b6 60%,#7d8e95);border:8px solid #222;border-radius:14px}}
.door{{position:absolute;top:140px;width:110px;height:640px;background:#B9B9B4;border:6px solid #333;box-shadow:inset 0 -470px 0 #A9A9A3}}
#edge{{position:absolute;left:0;right:0;top:1510px;height:410px;background:#3a3a3a;z-index:7;
  box-shadow:inset 0 22px 0 #f2f2f2,inset 0 40px 0 #d9d9d9}}
#fl{{position:absolute;inset:0;background:#000;z-index:30;pointer-events:none}}"""
    js = r"""
const $=i=>document.getElementById(i),mq=[...document.querySelectorAll('.mq')];
const A0=.35,A1=1.75,D0=2.75,D1=3.75;window.DUR=8.4;
window.fit=()=>{const po=$('po'),h=po.querySelector('h1'),ps=[...po.querySelectorAll('p,.et')];let k=1;  // shrink type until text clears the source line
  const last=()=>{const e=ps[ps.length-1];return e.offsetTop+e.offsetHeight};
  while(last()>po.clientHeight-100&&k>.6){k-=.04;h.style.fontSize=82*k+'px';h.style.margin=`${30*k}px 0 ${28*k}px`;
    ps.forEach(e=>e.style.fontSize=(e.tagName=='P'?35:30)*Math.max(k,.78)+'px')}};
window.SFX=[{t:A0,k:'train',d:A1-A0+.3,dir:-1},{t:A1-.55,k:'brake',d:.6},{t:2.15,k:'chime'},{t:D0,k:'train',d:D1-D0+.6,dir:1}];
window.render=t=>{
  const f=t<.25?(Math.floor(t*30)%3==0?.6:.2):0;$('fl').style.opacity=t<.3?f:0;
  let x;if(t<A1)x=1200+(-660-1200)*eo(seg(t,A0,A1));else if(t<D0)x=-660;else x=-660-(2600)*Math.pow(seg(t,D0,D1),2.2);
  const v=t<A1?(1-seg(t,A0,A1)):(t>D0?seg(t,D0,D1):0);
  $('tr').style.transform=`translate(${x}px,${t>A1&&t<D0?Math.sin(t*20)*1.5*(1-seg(t,A1,A1+.4)):0}px)`;
  $('tr').style.filter=v>.05?`blur(${(v*3).toFixed(1)}px)`:'none';
  $('po').style.opacity=t>A1-.3?1:0;
  mq.forEach(m=>m.style.transform=`translateX(${-((t*160)%(m.offsetWidth/2+400))+400}px)`)};
"""
    return page(body, css, js)


# ───────────── NEON: Kneipe sign flickers on over a brick wall ─────────────
def neon(it, meta):
    body = ('<canvas id="br" width="540" height="960" style="position:absolute;inset:0;width:1080px;height:1920px"></canvas>'
            + brand() + count(meta, 'rgba(255,255,255,.55)') +
            f'<div id="tg" class="nn">{it["tag"].replace("İ", "i").replace("I", "ı").lower()}</div><h1 id="h" class="nn">{tr_upper(it["title"])}</h1>'
            f'<div id="lb"><p>{it["body"]}</p>' + (f'<div class="et"><b>SANA ETKİSİ</b>{it["etki"]}</div>' if it.get('etki') else '') + f'<div class="src">KAYNAK: {it["source"]}</div></div>')
    css = f"""#s{{background:#120e10}}
#tg{{position:absolute;left:80px;top:470px;font:700 120px/1 HW;color:#fff;transform:rotate(-6deg);
  --g:0 0 4px #fff,0 0 12px #ff4a64,0 0 28px #ff2d4a,0 0 60px #ff2d4a,0 0 110px #C8102E}}
#h{{position:absolute;left:80px;right:70px;top:640px;font:800 86px/1.12 PO;color:#fff;letter-spacing:1px;
  --g:0 0 3px #fff,0 0 10px #ffd9df,0 0 24px #ff2d4a,0 0 56px #ff2d4a,0 0 100px #C8102E}}
.nn{{text-shadow:var(--g);z-index:5}}
#lb{{position:absolute;left:80px;right:80px;top:1130px;background:#F7F3EA;padding:40px 46px 78px;border-radius:10px;z-index:5;
  box-shadow:0 0 0 6px #1c1c1c,0 0 50px rgba(255,240,220,.35)}}
#lb p{{font:500 39px/1.46 IN;color:#1a1a1a}}
.et{{margin-top:20px;border-left:8px solid {RED};padding:6px 0 6px 18px;font:600 34px/1.4 IN;color:#111}}
.et b{{display:block;font:800 19px PO;letter-spacing:4px;color:{RED}}}
.src{{position:absolute;left:46px;bottom:26px;font:600 24px IN;letter-spacing:3px;color:#777}}"""
    js = r"""
const $=i=>document.getElementById(i);
window.fit=()=>{const h=$('h'),lb=$('lb'),ps=[...lb.querySelectorAll('p,.et')];let k=1;  // place the card under the title, shrink if it runs off
  const place=()=>{lb.style.top=Math.max(1000,h.offsetTop+h.offsetHeight+70)+'px'};place();
  while(lb.offsetTop+lb.offsetHeight>1690&&k>.7){k-=.03;h.style.fontSize=86*k+'px';ps.forEach(e=>e.style.fontSize=(e.tagName=='P'?39:34)*k+'px');place()}};
{const g=$('br').getContext('2d');g.fillStyle='#1b1517';g.fillRect(0,0,540,960);
 for(let r=0;r<60;r++)for(let c=-1;c<12;c++){const x=c*50+(r%2)*25,y=r*16,v=24+rnd(r*31+c)*16;
  g.fillStyle=`rgb(${v+10},${v-2},${v})`;g.fillRect(x+1.5,y+1.5,47,13)}
 const gr=g.createRadialGradient(270,380,40,270,420,560);gr.addColorStop(0,'rgba(200,16,46,.22)');gr.addColorStop(1,'rgba(0,0,0,.85)');g.fillStyle=gr;g.fillRect(0,0,540,960)}
const pat=(seed,t0,n)=>{const on=[];let tt=t0;for(let k=0;k<n;k++){on.push([tt,rnd(seed+k)<.55]);tt+=.04+rnd(seed+k+50)*.09}on.push([tt,true]);return on};
const P={tg:pat(3,.5,9),h:pat(11,1.35,11)},LB=2.4;window.DUR=8;
window.SFX=[{t:.5,k:'buzz',d:7.4,v:.5},{t:1.35,k:'buzz',d:6.5,v:.7},{t:LB,k:'click',v:1}];
const st=(p,t)=>{if(t<p[0][0])return 0;let s=0;for(const[a,o]of p){if(t>=a)s=o?1:0}return s};
window.render=t=>{
  ['tg','h'].forEach(id=>{let s=st(P[id],t);if(s&&rnd(Math.floor(t*30)+id.length*7)<.03)s=.55;
    $(id).style.opacity=s?1:.08;$(id).style.textShadow=s?'var(--g)':'none';$(id).style.color=s?'#fff':'#5a3a40';$(id).style.filter=`brightness(${s||.4})`});
  const pl=seg(t,LB,LB+.08);$('lb').style.opacity=pl>0?(pl<1?(Math.floor(t*60)%2?.3:1):1):0;
  document.getElementById('br').style.filter=`brightness(${.75+.25*st(P.h,t)})`};
"""
    return page(body, css, js)


# ───────────── MAUER: stencil graffiti sprayed on Berlin Wall concrete, wheat-paste poster ─────────────
def mauer(it, meta):
    lines = wrap(tr_upper(it['title']), 13)[:4]
    data = dict(lines=lines, tag=tr_upper(it['tag']))
    body = ('<canvas id="wl" width="1080" height="1920" style="position:absolute;inset:0"></canvas>'
            '<canvas id="sp" width="1080" height="1920" style="position:absolute;inset:0;z-index:3"></canvas>'
            + brand(color=BLK, accent=RED, icon_top=BLK) + count(meta, '#333') +
            '<span style="position:absolute;opacity:0;font:800 20px PO">AİŞĞÇÖÜ</span>' +
            f'<div id="ps"><p>{it["body"]}</p>' + (f'<div class="et"><b>SANA ETKİSİ</b>{it["etki"]}</div>' if it.get('etki') else '') + f'<div class="src">KAYNAK: {it["source"]}</div></div>')
    top = 600 + len(lines) * 112 + 60
    css = f"""#s{{background:#BDBAB2}}
#ps{{position:absolute;left:90px;right:110px;top:{top}px;background:#F2EFE6;padding:40px 44px 74px;z-index:4;transform:rotate(-1.2deg);
  transform-origin:50% 0;box-shadow:0 6px 0 rgba(0,0,0,.08)}}
#ps::after{{content:'';position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(0,0,0,.05) 32%,transparent 34%,transparent 70%,rgba(0,0,0,.06) 72%,transparent 74%)}}
#ps p{{font:500 35px/1.48 IN;color:#1c1c1c}}
#ps .et{{margin-top:20px;border-left:8px solid {RED};background:rgba(200,16,46,.07);padding:12px 18px;font:600 30px/1.4 IN;color:#111}}
#ps .et b{{display:block;font:800 19px PO;letter-spacing:4px;color:{RED}}}
.src{{position:absolute;left:44px;bottom:24px;font:600 22px IN;letter-spacing:3px;color:#777}}"""
    js = r"""
const $=i=>document.getElementById(i);
{const g=$('wl').getContext('2d');g.fillStyle='#BDBAB2';g.fillRect(0,0,1080,1920);const im=g.getImageData(0,0,1080,1920),d=im.data;
 for(let i=0;i<d.length;i+=4){const n=(rnd(i*.13)-.5)*26;d[i]+=n;d[i+1]+=n;d[i+2]+=n}g.putImageData(im,0,0);
 for(let k=0;k<4;k++){const x=k*360-40;g.fillStyle='rgba(0,0,0,.18)';g.fillRect(x,0,6,1920);g.fillStyle='rgba(255,255,255,.18)';g.fillRect(x+6,0,3,1920)}
 g.fillStyle='#A9A69E';g.fillRect(0,300,1080,40);g.fillStyle='rgba(0,0,0,.2)';g.fillRect(0,340,1080,8);
 g.filter='blur(14px)';for(let k=0;k<18;k++){g.fillStyle=`rgba(70,60,50,${.02+rnd(k)*.03})`;g.beginPath();g.ellipse(rnd(k+3)*1080,400+rnd(k+5)*1400,30+rnd(k+7)*120,10+rnd(k+9)*60,0,0,7);g.fill()}}
let sp,M,m,mk,A,jobs,drips,DONE;window.fit=()=>{sp=$('sp').getContext('2d');M=document.createElement('canvas');M.width=1080;M.height=1920;m=M.getContext('2d');
const LH=112,Y0=600;jobs=[];
m.font='800 46px PO';const tw=m.measureText(D.tag).width;m.fillStyle='#000';m.fillRect(80,505,tw+44,70);
m.globalCompositeOperation='destination-out';m.fillText(D.tag,102,557);m.globalCompositeOperation='source-over';
jobs.push({x0:70,x1:tw+140,y0:500,y1:580,c:'200,16,46',t0:.5,t1:.95});
m.font='800 100px PO';D.lines.forEach((l,i)=>{const w=m.measureText(l).width,y=Y0+i*LH;m.fillText(l,80,y+90);
  jobs.push({x0:60,x1:100+w,y0:y,y1:y+LH,c:'17,17,17',t0:1.1+i*.75,t1:1.1+i*.75+.7})});
mk=m.getImageData(0,0,1080,1920).data;A=(x,y)=>mk[((y|0)*1080+(x|0))*4+3];
drips=[];jobs.slice(1).forEach((j,i)=>{for(let k=0;k<5;k++){const x=j.x0+30+rnd(i*9+k)*(j.x1-j.x0-60);
  for(let y=j.y1;y>j.y0;y--){if(A(x,y)>200){drips.push({x,y,t:j.t1+rnd(k+i)*.6,L:25+rnd(k*3+i)*70,c:j.c});break}}}});
DONE=jobs[jobs.length-1].t1;window.DUR=Math.max(8,DONE+4.2);
window.SFX=[{t:.15,k:'rattle'},...jobs.map(j=>({t:j.t0,k:'spray',d:j.t1-j.t0})),{t:DONE+.35,k:'click',v:.8}]};
let fr=0;
window.render=t=>{fr++;
  jobs.forEach((j,ji)=>{if(t<j.t0||j.done)return;const p=seg(t,j.t0,j.t1),nx=j.x0+(j.x1-j.x0)*p;
    for(let k=0;k<2600;k++){const a=rnd(fr*7.1+k*1.37+ji)*6.283,r=Math.sqrt(rnd(fr*3.3+k*.71+ji))*58,x=nx+Math.cos(a)*r,y=j.y0+rnd(fr*5.9+k*.53)*(j.y1-j.y0);
      if(x<0||x>=1080)continue;const on=A(x,y)>128;if(!on&&rnd(k*1.9+fr)>.06)continue;
      sp.fillStyle=`rgba(${j.c},${on?.85:.10})`;const s=on?2.6:1.6;sp.fillRect(x,y,s,s)}
    if(p>=1){sp.save();sp.beginPath();sp.rect(j.x0-10,j.y0-6,j.x1-j.x0+20,j.y1-j.y0+12);sp.clip();
      const tmp=document.createElement('canvas');tmp.width=1080;tmp.height=1920;const tg=tmp.getContext('2d');tg.drawImage(M,0,0);
      tg.globalCompositeOperation='source-in';tg.fillStyle=`rgb(${j.c})`;tg.fillRect(0,0,1080,1920);sp.globalAlpha=.9;sp.drawImage(tmp,0,0);sp.restore();j.done=true}});
  drips.forEach(d=>{if(t<d.t)return;const L=d.L*eo(seg(t,d.t,d.t+1.2));sp.fillStyle=`rgba(${d.c},.9)`;sp.fillRect(d.x-1.5,d.y,3,L);
    sp.beginPath();sp.arc(d.x,d.y+L,2.6,0,7);sp.fill()});
  const pp=eo(seg(t,DONE+.3,DONE+.9));$('ps').style.transform=`rotate(-1.2deg) scaleY(${pp})`;$('ps').style.opacity=pp>0?1:0};
"""
    return page(body, css, js, data)


# ───────────── KIEZ: isometric mini-Berlin rises, pin drops on Mitte ─────────────
def kiez(it, meta):
    words = it['title'].split()
    hl = ' '.join(f'<span class="w"><span>{w}</span></span>' for w in words)
    body = ('<canvas id="c" width="1080" height="1920" style="position:absolute;inset:0"></canvas>'
            + brand(color=BLK, accent=RED, icon_top=BLK) + count(meta, '#444') +
            f'<div id="pin"><i></i><span>{tr_upper(it["tag"])}</span></div>'
            f'<h1 id="h">{hl}</h1><div id="b"><p>{it["body"]}</p>' + (f'<div class="et"><b>SANA ETKİSİ</b>{it["etki"]}</div>' if it.get('etki') else '') + f'</div><div id="src">KAYNAK: {it["source"]}</div>')
    css = f"""#s{{background:linear-gradient(#F3EEE3,#E6DDCB)}}
#pin{{position:absolute;left:0;top:0;z-index:5;display:flex;flex-direction:column;align-items:center}}
#pin span{{order:-1;background:{RED};color:#fff;font:800 28px PO;letter-spacing:4px;padding:8px 18px;border-radius:6px;margin-bottom:8px;white-space:nowrap}}
#pin i{{width:4px;height:70px;background:#111}}
#h{{position:absolute;left:70px;right:70px;top:1060px;font:800 80px/1.08 PO;color:#111;letter-spacing:-1.5px}}
.w{{display:inline-block;overflow:hidden;vertical-align:top}}.w span{{display:inline-block}}
#b{{position:absolute;left:70px;right:70px;font:500 35px/1.46 IN;color:#2a2a2a}}
.et{{margin-top:22px;border-left:8px solid {RED};background:rgba(200,16,46,.08);padding:14px 20px;font:600 31px/1.4 IN;color:#111}}
.et b{{display:block;font:800 20px PO;letter-spacing:4px;color:{RED};margin-bottom:4px}}
#src{{position:absolute;left:70px;font:600 22px IN;letter-spacing:3px;color:#777}}"""
    js = r"""
const $=i=>document.getElementById(i),cv=$('c'),x=cv.getContext('2d'),N=8,S=60,CX=540,CY=500;
const P=(i,j,z)=>[CX+(i-j)*S*.866,CY+(i+j)*S*.5-z];
const B=[];for(let i=0;i<N;i++)for(let j=0;j<N;j++){const c=i==4&&j==4,d=Math.hypot(i-3.5,j-3.5),park=rnd(i*13+j)<.12;
  B.push({i,j,h:c?0:(park?6:40+rnd(i*7+j*3)*(150-d*12)),park,tw:c,t0:.25+d*.11,col:rnd(i*5+j*11)<.13?'red':'n'})}
const fill=(pts,c)=>{x.fillStyle=c;x.beginPath();pts.forEach((p,k)=>k?x.lineTo(...p):x.moveTo(...p));x.closePath();x.fill()};
const pal={n:['#FBF8F1','#D9D2C2','#B7AE9A'],red:['#E43A52','#C8102E','#8E0B21'],park:['#9DB98A','#7E9A6C','#617B52']};
const back=p=>{const c1=1.6,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
function box(b,h){const g=.1,i=b.i+g,j=b.j+g,w=1-2*g,c=pal[b.park?'park':b.col];
  fill([P(i,j+w,0),P(i+w,j+w,0),P(i+w,j+w,h),P(i,j+w,h)],c[1]);fill([P(i+w,j,0),P(i+w,j+w,0),P(i+w,j+w,h),P(i+w,j,h)],c[2]);
  fill([P(i,j,h),P(i+w,j,h),P(i+w,j+w,h),P(i,j+w,h)],c[0])}
const TT=1.5;const tip=P(4.5,4.5,360);const ball=P(4.5,4.5,300);
const ws=[...document.querySelectorAll('.w span')],TH=2.4,TB=TH+ws.length*.07+.4;window.DUR=Math.max(8,TB+3.6);
window.SFX=[...B.filter(b=>!b.tw&&rnd(b.i*3+b.j)<.35).map(b=>({t:b.t0+.3,k:'tick',v:.6})),{t:TT+.5,k:'thud',v:.3},{t:2.2,k:'click',v:1}];
window.render=t=>{x.clearRect(0,0,1080,1920);
  fill([P(0,0,0),P(N,0,0),P(N,N,0),P(0,N,0)],'rgba(0,0,0,.06)');
  B.sort((a,b)=>(a.i+a.j)-(b.i+b.j)).forEach(b=>{if(b.tw){const p=eo(seg(t,TT,TT+.8)),bx=P(4.5,4.5,0);
      x.fillStyle='#111';x.fillRect(bx[0]-7,bx[1]-360*p,14,360*p);if(p>.75){const q=back(seg(t,TT+.6,TT+1));x.fillStyle='#C8102E';
      x.beginPath();x.arc(ball[0],ball[1],34*q,0,7);x.fill();x.fillStyle='#111';x.fillRect(tip[0]-2,tip[1]-70*q,4,70*q)}return}
    const p=seg(t,b.t0,b.t0+.55);if(p<=0)return;box(b,b.h*back(p))});
  const pd=seg(t,2.0,2.4),tg=P(5.5,3.5,120);$('pin').style.transform=`translate(${tg[0]-$('pin').offsetWidth/2}px,${tg[1]-120-(1-back(pd))*600}px)`;
  $('pin').style.opacity=pd>0?1:0;
  ws.forEach((w,i)=>{const p=eo(seg(t,TH+i*.07,TH+i*.07+.5));w.style.transform=`translateY(${(1-p)*110}%)`});
  const hb=$('h').offsetTop+$('h').offsetHeight;$('b').style.top=(hb+30)+'px';$('src').style.top=(hb+30+$('b').offsetHeight+24)+'px';
  const pb=eo(seg(t,TB,TB+.7));$('b').style.opacity=pb;$('b').style.transform=`translateY(${(1-pb)*24}px)`;$('src').style.opacity=seg(t,TB+.5,TB+1)};
"""
    return page(body, css, js)


STYLES4 = dict(ubahn2=ubahn2, neon=neon, mauer=mauer, kiez=kiez)
