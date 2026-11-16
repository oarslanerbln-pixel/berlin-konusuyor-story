"""Hybrid style: Prismenwender billboard that turns into an Extrablatt front page."""
from common import page, brand, tv, tr_upper, RED


def count(meta, color):
    return (f'<div style="position:absolute;right:80px;top:268px;font:600 24px IN;letter-spacing:4px;color:{color};z-index:20">'
            f'{meta["idx"]} / {meta["total"]}</div>')


def prisma_gazete(it, meta):
    N, W, H = 22, 44, 1208
    stamp = it.get('stamp', 'EXTRA' if meta['idx'] == 1 else '')
    tl = meta.get('titles', [it['title']])
    ix = ('<div class="ix"><b>BUGÜNKÜ SAYIDA</b>' + ''.join(
        f'<div class="{"on" if j + 1 == meta["idx"] else ""}"><em>{j + 1}</em>{(x[:44] + "…") if len(x) > 45 else x}</div>'
        for j, x in enumerate(tl)) + '</div>') if len(tl) > 1 else ''
    face_a = (f'<div class="fa">{tv(380)}<div class="w1">BERLİN</div><div class="w2">KONUŞUYOR</div>'
              '<div class="w3">HER SABAH 08:30 · GÜNDEM</div></div>')
    face_b = ('<div class="fb"><div class="mh">Berlin Gündemi</div>'
              f'<div class="dl"><span>SAYI {meta["idx"]:03d}</span><span>{meta["date_long"]}</span><span>BERLİN BASKISI</span></div>'
              f'<div class="kk">{tr_upper(it["tag"])}</div><h1>{it["title"]}</h1>'
              f'<div class="cols"><p>{it["body"]}</p></div>' + ix +
              f'<div class="ft"><span>KAYNAK: {it["source"]}</span><span>@berlin.konusuyor</span></div></div>')
    faces = [face_a, face_b, '<div class="fc0"></div>']
    slats = ''.join(
        f'<div class="sl" style="left:{i*W}px">' +
        ''.join(f'<div class="fc" style="transform:rotateY({k*120}deg) translateZ(12.7px)"><div class="cnt" style="left:{-i*W}px">{f}</div><div class="sh"></div></div>'
                for k, f in enumerate(faces)) + '</div>' for i in range(N))
    bolts = ''.join(f'<i class="bo" style="{p}"></i>' for p in
                    ['left:6px;top:6px', 'right:6px;top:6px', 'left:6px;bottom:6px', 'right:6px;bottom:6px'])
    lamps = ''.join(f'<div class="lp" style="left:{x}px"><i></i></div>' for x in (390, 650))
    body = ('<canvas id="bk" width="540" height="960" style="position:absolute;inset:0;width:1080px;height:1920px;filter:blur(6px)"></canvas>'
            + brand() + count(meta, 'rgba(255,255,255,.6)') +
            f'<div id="cam"><div id="fr">{bolts}<div id="in">{slats}</div><div id="gl"></div><div id="cone"></div>'
            + (f'<div id="stamp">{stamp}</div>' if stamp else '') + '</div>' + lamps + '</div>')
    css = f"""#s{{background:#0c0c0f}}
#cam{{position:absolute;inset:0;transform-origin:50% 52%}}
#fr{{position:absolute;left:40px;top:372px;width:1000px;height:1240px;padding:16px;
  background:linear-gradient(90deg,#6f7076,#b3b4b9 18%,#86878c 50%,#c4c5ca 82%,#6a6b70);
  box-shadow:0 40px 90px rgba(0,0,0,.75),inset 0 0 0 2px #2a2a2e,inset 0 0 0 5px rgba(255,255,255,.25)}}
.bo{{position:absolute;width:10px;height:10px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#eee,#555);z-index:3}}
#in{{position:relative;width:{N*W}px;height:{H}px;perspective:2600px;background:#050505;overflow:hidden}}
.sl{{position:absolute;top:0;width:{W}px;height:{H}px;transform-style:preserve-3d}}
.fc{{position:absolute;inset:0;overflow:hidden;backface-visibility:hidden;box-shadow:inset -1px 0 0 rgba(0,0,0,.22)}}
.cnt{{position:absolute;top:0;width:{N*W}px;height:{H}px}}
.sh{{position:absolute;inset:0;background:#000;opacity:0}}
.fa{{position:absolute;inset:0;background:{RED};display:flex;flex-direction:column;align-items:center;padding-top:170px}}
.w1{{font:800 124px/1 PO;color:#fff;margin-top:70px;letter-spacing:2px}}.w2{{font:800 98px/1.05 PO;color:#111}}
.w3{{position:absolute;bottom:96px;font:600 28px IN;letter-spacing:7px;color:#fff}}
.fb{{position:absolute;inset:0;background-color:#EEE7D6;padding:46px 50px}}
.mh{{font:700 112px/1 FK;text-align:center;color:#111;padding-bottom:18px}}
.dl{{display:flex;justify-content:space-between;border-top:5px double #111;border-bottom:5px double #111;padding:10px 4px;
  font:400 21px PF;letter-spacing:3px;color:#222;text-transform:uppercase}}
.kk{{font:900 28px PF;letter-spacing:6px;color:{RED};margin:36px 0 10px}}
.fb h1{{font:900 var(--hs,108px)/1.0 PF;color:#111;letter-spacing:-2px}}
.cols{{column-count:2;column-gap:40px;column-rule:1px solid #9a9080;margin-top:34px;border-top:2px solid #111;padding-top:26px}}
.cols p{{font:400 var(--bs,34px)/1.42 PF;color:#1c1c1c;text-align:left}}
.ix{{position:absolute;left:50px;right:50px;bottom:96px;border-top:2px solid #111;padding-top:16px;font:400 25px/1.55 PF;color:#555}}
.ix b{{display:block;font:900 20px PF;letter-spacing:5px;color:#111;margin-bottom:6px}}
.ix em{{font:900 25px PF;font-style:normal;color:{RED};display:inline-block;width:34px}}
.ix .on{{color:#111;font-weight:900}}
.cols p::first-letter{{float:left;font:900 116px/.86 PF;margin:6px 12px 0 0;color:{RED}}}
.ft{{position:absolute;left:50px;right:50px;bottom:40px;display:flex;justify-content:space-between;border-top:1px solid #111;padding-top:12px;
  font:400 20px PF;letter-spacing:3px;color:#444}}
.fc0{{position:absolute;inset:0;background:#111}}
#gl{{position:absolute;inset:16px;pointer-events:none;background:linear-gradient(115deg,transparent 42%,rgba(255,255,255,.30) 50%,transparent 58%) no-repeat;
  background-size:300% 100%;mix-blend-mode:screen}}
#cone{{position:absolute;inset:16px;pointer-events:none;mix-blend-mode:soft-light;
  background:radial-gradient(60% 45% at 37% 0%,rgba(255,240,210,.55),transparent 70%),radial-gradient(60% 45% at 63% 0%,rgba(255,240,210,.55),transparent 70%),
  linear-gradient(transparent 60%,rgba(0,0,0,.35))}}
.lp{{position:absolute;top:322px;width:44px;height:58px;z-index:6}}
.lp::before{{content:'';position:absolute;left:19px;top:-40px;width:6px;height:46px;background:#2b2b2f}}
.lp i{{position:absolute;left:0;top:0;width:44px;height:22px;border-radius:6px 6px 14px 14px;background:linear-gradient(#3a3a3f,#1c1c20);
  box-shadow:0 14px 30px 8px rgba(255,236,200,.35)}}
#stamp{{position:absolute;right:70px;top:210px;font:800 76px PO;letter-spacing:10px;color:{RED};border:8px solid {RED};padding:2px 22px 0;
  outline:3px solid {RED};outline-offset:6px;mix-blend-mode:multiply;opacity:0;z-index:5;
  -webkit-mask-image:radial-gradient(circle at 30% 40%,#000 55%,rgba(0,0,0,.55) 75%,#000 90%)}}"""
    js = r"""
const $=i=>document.getElementById(i),sls=[...document.querySelectorAll('.sl')],r=12.7;
{const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),im=g.createImageData(256,256);
 for(let i=0;i<im.data.length;i+=4){const v=200+rnd(i*.37)*55;im.data[i]=v;im.data[i+1]=v-6;im.data[i+2]=v-18;im.data[i+3]=60}
 g.putImageData(im,0,0);const u=c.toDataURL();document.querySelectorAll('.fb,.fa').forEach(e=>e.style.backgroundImage=`url(${u})`)}
const bk=$('bk').getContext('2d'),L=[...Array(46)].map((_,i)=>({x:rnd(i)*540,y:520+rnd(i+9)*440,r:6+rnd(i+3)*22,
  c:['255,190,90','255,120,60','120,170,255','255,255,230'][Math.floor(rnd(i+5)*4)],a:.25+rnd(i+7)*.5,s:rnd(i+11)}));
const ST=$('stamp');
window.fit=()=>{const fb=document.querySelector('.fb'),cols=fb.querySelector('.cols'),ix=fb.querySelector('.ix')||fb.querySelector('.ft');let hs=108,bs=34;
 const S=document.getElementById('s');for(let k=0;k<12&&cols.getBoundingClientRect().bottom>ix.getBoundingClientRect().top-26;k++){hs-=5;bs=Math.max(29,bs-1);
 S.style.setProperty('--hs',hs+'px');S.style.setProperty('--bs',bs+'px')}};
const T0=1.45,STEP=.055,ROT=.8,TS=T0+(sls.length-1)*STEP+ROT+.35;window.DUR=TS+5.2;
window.SFX=[{t:0,k:'amb',d:window.DUR},{t:T0,k:'whirr',d:(sls.length-1)*STEP+ROT},
  ...sls.map((_,i)=>({t:T0+i*STEP+ROT*.72,k:'click',v:.6+rnd(i)*.4})),...(ST?[{t:TS,k:'thud'}]:[])];
const back=p=>{const c1=1.35,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
window.render=t=>{
  bk.fillStyle='#0b0b0e';bk.fillRect(0,0,540,960);
  L.forEach(l=>{const fl=.85+.15*Math.sin(t*(1+l.s*2)+l.s*9);bk.fillStyle=`rgba(${l.c},${l.a*fl})`;bk.beginPath();bk.arc(l.x+Math.sin(t*.2+l.s)*6,l.y,l.r,0,7);bk.fill()});
  sls.forEach((s,i)=>{const a=T0+i*STEP,p=seg(t,a,a+ROT),ang=120*(p>0?back(p):0);
    s.style.transform=`translateZ(${-r}px) rotateY(${-ang}deg)`;
    [...s.children].forEach((f,k)=>{const fa=(k*120-ang)*Math.PI/180;f.querySelector('.sh').style.opacity=Math.min(.85,Math.abs(Math.sin(fa))*.9+(Math.cos(fa)<0?.6:0))})});
  const g=seg(t,.25,1.3);$('gl').style.backgroundPosition=`${120-g*140}% 0`;$('gl').style.opacity=g>0&&g<1?1:0;
  if(ST){const ps=seg(t,TS,TS+.16);ST.style.opacity=ps*.92;$('stamp').style.transform=`rotate(-13deg) scale(${2.5-1.5*eo(ps)})`}
  let sh=0;if(ST&&t>TS+.1&&t<TS+.32)sh=(rnd(Math.floor(t*60))-.5)*16*(1-seg(t,TS+.1,TS+.32));
  $('cam').style.transform=`scale(${1+.045*eio(seg(t,TS,window.DUR))}) translate(${sh}px,${sh*.6}px)`};
"""
    return page(body, css, js)


STYLES3 = dict(prisma_gazete=prisma_gazete)
