import math
S='stroke="#000" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"'
F=f'fill="#fff" {S}'
N=f'fill="none" {S}'
def star(cx,cy,r): return f'<path {F} d="M{cx} {cy-r} Q{cx} {cy} {cx+r} {cy} Q{cx} {cy} {cx} {cy+r} Q{cx} {cy} {cx-r} {cy} Q{cx} {cy} {cx} {cy-r}Z"/>'
def leaf(x,y,ang,L):
    return f'<g transform="translate({x} {y}) rotate({ang})"><path {F} d="M0 0 Q{L/2} {-L/3} {L} 0 Q{L/2} {L/3} 0 0Z"/><path {N} d="M4 0 L{L*0.8} 0"/></g>'
def rose(cx,cy,r):
    pts=[(cx+r*math.cos(math.radians(a-90)),cy+r*math.sin(math.radians(a-90))) for a in range(0,360,72)]
    d=f'M{pts[0][0]:.1f} {pts[0][1]:.1f} '+' '.join(f'A{r*0.62:.1f} {r*0.62:.1f} 0 0 1 {pts[(i+1)%5][0]:.1f} {pts[(i+1)%5][1]:.1f}' for i in range(5))+'Z'
    i=r*0.5
    return (f'<path {F} d="{d}"/><circle {F} cx="{cx}" cy="{cy}" r="{i:.1f}"/>'
            f'<path {N} d="M{cx-i*0.5:.1f} {cy+i*0.1:.1f} A{i*0.45:.1f} {i*0.45:.1f} 0 1 1 {cx+i*0.4:.1f} {cy+i*0.2:.1f} A{i*0.25:.1f} {i*0.25:.1f} 0 1 1 {cx:.1f} {cy:.1f}"/>'
            f'<path {N} d="M{cx-r*0.55:.1f} {cy+r*0.35:.1f} Q{cx} {cy+r*0.8:.1f} {cx+r*0.55:.1f} {cy+r*0.35:.1f}"/>')
def crescent(cx,cy,r,dx,dy,rr,cid):
    return (f'<defs><clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath></defs><circle {F} cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<circle {F} cx="{cx+dx}" cy="{cy+dy}" r="{rr}" clip-path="url(#{cid})"/><circle fill="none" stroke="#000" stroke-width="5" cx="{cx}" cy="{cy}" r="{r}"/>')
def bat(x,y,s):
    return f'<path {F} d="M{x} {y} Q{x-15*s} {y-15*s} {x-40*s} {y-5*s} Q{x-30*s} {y+2*s} {x-30*s} {y+12*s} Q{x-15*s} {y+2*s} {x} {y+10*s} Q{x+15*s} {y+2*s} {x+30*s} {y+12*s} Q{x+30*s} {y+2*s} {x+40*s} {y-5*s} Q{x+15*s} {y-15*s} {x} {y}Z"/>'
def tube(d,w=22): return f'<path d="{d}" fill="none" stroke="#000" stroke-width="{w}" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#fff" stroke-width="{w-10}" stroke-linecap="round"/>'
def arch(x1,x2,y,yb):
    m=(x1+x2)/2; h=(x2-x1)*0.7
    return f'<path {F} d="M{x1} {yb} L{x1} {y} Q{x1} {y-h} {m} {y-h*1.15} Q{x2} {y-h} {x2} {y} L{x2} {yb}Z"/>'
def txt(x,y,t,sz,sp=6): return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Georgia,serif" font-size="{sz}" letter-spacing="{sp}" fill="#fff" stroke="#000" stroke-width="2.5">{t}</text>'

P={}
# 1 raven & moon
raven='M232 322 L284 310 Q296 276 332 270 Q372 266 390 300 Q436 322 458 378 Q474 424 490 476 L548 530 L522 538 L488 512 Q452 506 418 496 Q362 484 340 440 Q322 398 328 356 Q306 340 282 336 Z'
P['raven']=(crescent(306,380,250,95,-60,220,'c1')+f'<path {N} d="M150 560 Q350 540 590 575"/>'+leaf(200,553,-150,60)+leaf(250,549,-40,55)+leaf(520,566,-30,60)+
  f'<path {F} d="{raven}"/><circle {F} cx="336" cy="296" r="9"/><path {N} d="M358 352 Q426 380 456 468"/><path {N} d="M372 392 Q420 420 440 470"/><path {N} d="M396 500 L392 550 M424 505 L424 556"/>'
  +star(120,120,26)+star(500,110,20)+star(90,640,18)+star(540,680,24)+star(470,210,12))
# 2 candles
def candle(x,top,w,base):
    L,R=x-w/2,x+w/2
    return (f'<rect {F} x="{L}" y="{top}" width="{w}" height="{base-top}"/>'
      f'<path {F} d="M{L} {top} L{L} {top+50} Q{L+9} {top+68} {L+18} {top+50} L{L+18} {top+22} L{x+6} {top+22} L{x+6} {top+85} Q{x+15} {top+102} {x+24} {top+85} L{x+24} {top+22} L{R} {top+22} L{R} {top}Z"/>'
      f'<ellipse {F} cx="{x}" cy="{top}" rx="{w/2}" ry="10"/><path {N} d="M{x} {top} L{x} {top-18}"/>'
      f'<path {F} d="M{x} {top-16} Q{x-24} {top-52} {x} {top-104} Q{x+24} {top-52} {x} {top-16}Z"/><path {F} d="M{x} {top-26} Q{x-10} {top-46} {x} {top-70} Q{x+10} {top-46} {x} {top-26}Z"/>')
P['candles']=(f'<ellipse {F} cx="306" cy="660" rx="240" ry="34"/><path {F} d="M66 660 L66 684 Q306 740 546 684 L546 660 Q306 716 66 660Z"/>'
  +candle(186,410,76,660)+candle(306,300,86,665)+candle(426,460,70,660)+rose(120,640,38)+rose(492,640,34)+leaf(80,610,-120,50)+leaf(530,610,-60,50)
  +star(100,200,22)+star(520,240,26)+star(420,150,14)+star(190,120,16))
# 3 skull & roses
P['skull']=(crescent(306,112,52,30,-18,46,'c3')+f'<path {F} d="M206 380 Q206 200 306 200 Q406 200 406 380 Q406 420 378 436 L378 482 L234 482 L234 436 Q206 420 206 380Z"/>'
  f'<ellipse {F} cx="262" cy="362" rx="32" ry="36"/><ellipse {F} cx="350" cy="362" rx="32" ry="36"/><path {F} d="M306 392 L290 424 L322 424Z"/>'
  f'<path {N} d="M254 440 L254 482 M278 440 L278 486 M306 440 L306 488 M334 440 L334 486 M358 440 L358 482 M240 440 L372 440"/><path {N} d="M340 214 L326 250 L346 266 L334 296"/>'
  +leaf(150,520,-160,70)+leaf(460,520,-20,70)+leaf(250,600,120,60)+leaf(362,600,60,60)+rose(190,520,52)+rose(422,520,52)+rose(306,570,60)+star(110,300,22)+star(500,300,22)+star(140,700,16)+star(480,700,16))
# 4 haunted house
hh=(f'<circle {F} cx="470" cy="160" r="62"/>'+bat(150,140,1.2)+bat(250,90,0.8)+bat(540,280,0.9)
  +f'<rect {F} x="200" y="360" width="230" height="300"/><path {F} d="M180 360 L315 232 L450 360Z"/><rect {F} x="140" y="300" width="80" height="360"/><path {F} d="M128 300 L180 150 L232 300Z"/>'
  +arch(160,200,390,440)+arch(160,200,520,570)+arch(240,290,420,480)+arch(340,390,420,480)+arch(285,345,570,660)+f'<circle {F} cx="315" cy="300" r="26"/><path {N} d="M315 274 L315 326 M289 300 L341 300"/>'
  +f'<path {N} d="M60 660 Q180 645 306 662 Q430 676 552 658"/>')
for gx,gh in [(470,70),(530,55),(95,60)]:
    hh+=arch(gx-24,gx+24,660-gh+18,700)
P['house']=hh+f'<path {N} d="M60 715 L552 715"/>'
# 5 cat on moon
P['cat']=(crescent(306,390,260,-100,-50,225,'c5')+f'<path {F} d="M296 560 Q250 640 270 700 Q320 722 372 700 Q394 640 350 560Z"/>'
  f'<circle {F} cx="324" cy="540" r="44"/><path {F} d="M290 520 L286 474 L316 500Z"/><path {F} d="M334 500 L364 474 L360 520Z"/>'+tube('M370 698 Q448 712 438 650 Q432 612 458 600')
  +star(90,90,22)+star(520,110,28)+star(560,420,16)+star(470,250,14)+star(60,720,18))
# 6 crystal ball
cb='<defs><clipPath id="c6"><circle cx="306" cy="340" r="175"/></clipPath></defs>'+f'<circle {F} cx="306" cy="340" r="175"/><g clip-path="url(#c6)">'+crescent(250,290,60,30,-20,52,'c6b')+star(370,250,22)+star(390,380,14)+star(230,420,16)+f'<path {N} d="M150 440 Q230 400 306 440 Q382 480 462 430"/><path {N} d="M150 470 Q230 430 306 470 Q382 510 462 460"/></g>'
cb+=f'<path {N} d="M196 250 Q220 200 262 186"/>'
cb+=f'<path {F} d="M196 486 Q306 540 416 486 L450 600 Q306 648 162 600Z"/><ellipse {F} cx="306" cy="630" rx="170" ry="34"/><path {N} d="M230 540 L220 610 M306 552 L306 622 M382 540 L392 610"/>'
P['crystal']=cb+rose(120,660,34)+rose(492,660,34)+star(90,150,24)+star(525,170,20)+star(540,420,14)+star(70,420,14)
# 7 potions
po=f'<path {N} d="M40 640 L572 640"/>'
po+=f'<circle {F} cx="170" cy="540" r="96"/><rect {F} x="150" y="380" width="40" height="80"/><rect {F} x="142" y="350" width="56" height="34" rx="6"/><path {N} d="M84 560 Q130 530 170 560 Q210 590 256 555"/>'
po+=f'<circle {F} cx="150" cy="600" r="10"/><circle {F} cx="190" cy="590" r="7"/>'
po+=f'<rect {F} x="266" y="330" width="90" height="310" rx="20"/><rect {F} x="288" y="270" width="46" height="64"/><rect {F} x="280" y="240" width="62" height="34" rx="6"/><rect {F} x="276" y="420" width="70" height="120" rx="6"/>'+txt(311,470,'✦',26,0)+txt(311,515,'NIGHT',16,2)
po+=f'<path {F} d="M452 640 Q376 580 380 530 Q384 488 426 488 Q448 488 452 510 Q456 488 478 488 Q520 488 524 530 Q528 580 452 640Z"/><rect {F} x="436" y="440" width="32" height="54"/><rect {F} x="428" y="414" width="48" height="30" rx="6"/>'+star(452,555,16)
P['potions']=po+star(90,200,24)+star(530,220,24)+star(306,120,20)+f'<path {N} d="M100 700 Q306 680 512 700"/>'+leaf(60,700,-10,50)+leaf(552,700,190,50)
# 8 gothic window
gw=f'<path {F} d="M140 720 L140 330 Q140 140 306 72 Q472 140 472 330 L472 720Z"/><path {F} d="M166 700 L166 336 Q166 172 306 106 Q446 172 446 336 L446 700Z"/>'
gw+=f'<circle {F} cx="306" cy="250" r="96"/>'
for k in range(8):
    a=math.radians(k*45); x=306+58*math.cos(a); y=250+58*math.sin(a)
    gw+=f'<circle {F} cx="{x:.1f}" cy="{y:.1f}" r="30"/>'
gw+=f'<circle {F} cx="306" cy="250" r="26"/>'+star(306,250,16)
gw+=arch(186,296,440,690)+arch(316,426,440,690)
gw+=f'<path {N} d="M241 400 L241 690 M361 400 L361 690 M186 520 L296 520 M316 520 L426 520 M186 605 L296 605 M316 605 L426 605"/>'
gw+=f'<path {N} d="M120 740 L492 740"/>'+star(80,120,22)+star(535,140,22)+star(70,500,16)+star(545,520,16)
P['window']=gw
# 9 moon mandala
mm=f'<circle {F} cx="306" cy="396" r="272"/><circle {F} cx="306" cy="396" r="250"/>'
for k in range(24):
    a=math.radians(k*15); x=306+261*math.cos(a); y=396+261*math.sin(a)
    mm+=f'<circle {F} cx="{x:.1f}" cy="{y:.1f}" r="9"/>'
for k in range(8):
    a=k*45; x=306+195*math.cos(math.radians(a)); y=396+195*math.sin(math.radians(a))
    mm+=f'<circle {F} cx="{x:.1f}" cy="{y:.1f}" r="36"/>'
    if k%4: mm+=f'<defs><clipPath id="m{k}"><circle cx="{x:.1f}" cy="{y:.1f}" r="36"/></clipPath></defs><circle {F} cx="{x+ (k-4)*16:.1f}" cy="{y:.1f}" r="36" clip-path="url(#m{k})"/><circle fill="none" stroke="#000" stroke-width="5" cx="{x:.1f}" cy="{y:.1f}" r="36"/>'
mm+=f'<circle {F} cx="306" cy="396" r="148"/>'
for k in range(12):
    mm+=f'<ellipse {F} cx="306" cy="{396-100}" rx="22" ry="46" transform="rotate({k*30} 306 396)"/>'
mm+=f'<circle {F} cx="306" cy="396" r="62"/>'+crescent(306,396,48,22,-12,42,'c9')
P['mandala']=mm
# 10 spider web
sw=''
cx,cy=306,320
spokes=[math.radians(k*30+15) for k in range(12)]
for a in spokes: sw+=f'<path {N} d="M{cx} {cy} L{cx+260*math.cos(a):.1f} {cy+260*math.sin(a):.1f}"/>'
for r in [40,80,125,170,215,255]:
    d=''
    for i,a in enumerate(spokes):
        b=spokes[(i+1)%12]; x1,y1=cx+r*math.cos(a),cy+r*math.sin(a); x2,y2=cx+r*math.cos(b),cy+r*math.sin(b)
        m=(a+b)/2 if i<11 else a+math.radians(15); qx,qy=cx+r*0.85*math.cos(m),cy+r*0.85*math.sin(m)
        d+=(f'M{x1:.1f} {y1:.1f} ' if i==0 else '')+f'Q{qx:.1f} {qy:.1f} {x2:.1f} {y2:.1f} '
    sw+=f'<path {N} d="{d}"/>'
sw+=f'<path {N} d="M306 575 L306 612"/>'
sp=f'<ellipse {F} cx="306" cy="660" rx="30" ry="38"/><circle {F} cx="306" cy="610" r="20"/>'
legs=''
for s in (-1,1):
    for j,(a,b) in enumerate([(40,-20),(46,5),(44,30),(36,52)]):
        legs+=f'<path {N} d="M{306+s*22} {640+j*10} L{306+s*a*1.4} {640+j*10+b*0.4-14} L{306+s*(a*1.4+26)} {640+j*14+b}"/>'
P['web']=sw+legs+sp+rose(110,690,34)+rose(502,690,34)+star(80,90,20)+star(535,90,20)
# 11 coffin & roses
co=f'<path {F} d="M236 90 L376 90 L436 240 L392 720 L220 720 L176 240Z"/><path {F} d="M244 116 L368 116 L416 244 L374 696 L238 696 L196 244Z"/>'
co+=f'<rect {F} x="290" y="170" width="32" height="170" rx="4"/><rect {F} x="246" y="214" width="120" height="30" rx="4"/>'
for (x,y,r) in [(230,420,40),(306,440,48),(382,420,40),(260,500,34),(352,500,34)]: co+=leaf(x-r,y+r*0.3,-150,56)+leaf(x+r,y+r*0.3,-30,56)
for (x,y,r) in [(230,420,40),(306,440,48),(382,420,40),(260,500,34),(352,500,34)]: co+=rose(x,y,r)
P['coffin']=co+crescent(100,140,50,30,-18,44,'c11')+star(520,150,24)+star(80,560,18)+star(540,600,18)+bat(510,360,0.9)
# 12 the moon tarot
tm=f'<rect {F} x="120" y="60" width="372" height="672" rx="18"/><rect {F} x="140" y="80" width="332" height="632" rx="10"/>'
tm+=f'<rect {F} x="140" y="640" width="332" height="72"/>'+txt(306,690,'THE MOON',34)+txt(306,130,'XVIII',30)
for k in range(16):
    tm+=f'<path {F} d="M306 150 L318 186 L294 186Z" transform="rotate({k*22.5} 306 270)"/>'
tm+=f'<circle {F} cx="306" cy="270" r="80"/>'+crescent(306,270,60,-24,-8,52,'c12')
tm+=f'<rect {F} x="160" y="420" width="56" height="150"/><path {N} d="M160 420 L160 404 L174 404 L174 420 M188 420 L188 404 L202 404 L202 420 M216 420 L216 404"/>'+arch(178,198,470,500)
tm+=f'<rect {F} x="396" y="420" width="56" height="150"/><path {N} d="M396 420 L396 404 L410 404 L410 420 M424 420 L424 404 L438 404 L438 420 M452 420 L452 404"/>'+arch(414,434,470,500)
tm+=f'<path {F} d="M280 640 Q300 560 306 470 Q312 560 332 640Z"/><path {N} d="M140 600 Q180 585 220 600 Q260 615 300 600 M312 600 Q352 585 392 600 Q432 615 472 600"/>'
tm+=f'<path {N} d="M140 625 Q180 610 220 625 Q260 640 290 625 M322 625 Q352 610 392 625 Q432 640 472 625"/>'
P['tarot']=tm+star(230,380,12)+star(382,380,12)+star(306,400,10)
names=[('raven','Raven & Moon'),('candles','Midnight Candles'),('skull','Skull & Roses'),('house','The Haunted Manor'),('cat','Moon Cat'),('crystal','Crystal Ball'),('potions','Potion Shelf'),('window','Gothic Window'),('mandala','Moon Phase Mandala'),('web','Spider Web'),('coffin','Coffin & Roses'),('tarot','The Moon Card')]
def svg(k): return f'<svg viewBox="0 0 612 792" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><rect width="612" height="792" fill="#fff"/>{P[k]}</svg>'
import json
json.dump({'names':names,'svgs':{k:svg(k) for k in P}},open('pages.json','w'))
