# Redraw atomic_i: three hexagonal groups of seven circles, offset (ABC layers).
# Usage: python3 tools/redraw.py images/atomic_i_redrawn.png
import json, math, os, sys
from PIL import Image, ImageDraw
C=json.load(open(os.path.join(os.path.dirname(__file__),'centres.json')))
S=4                                   # supersample
W,H=428,348
D=120; RAD=33                         # neighbour spacing, circle radius (px)
HEX=[(0,0)]+[(D*math.cos(math.radians(a)),D*math.sin(math.radians(a))) for a in range(0,360,60)]

def centre(group):                    # a hexagon of seven is symmetric, so its centre is the mean of the seven
    pts=C[group]
    mx=sum(p[0] for p in pts)/7; my=sum(p[1] for p in pts)/7
    return mx,my

def tile(kind,n=24):
    t=Image.new('L',(n*S,n*S),255); d=ImageDraw.Draw(t); u=S
    if kind=='weave':                 # herringbone chevrons
        for k in range(-2,4):
            y=k*n*S/3
            d.line([(0,y+n*S/3),(n*S/2,y),(n*S,y+n*S/3)],fill=0,width=3*u)
    elif kind=='fret':                # Greek-key / fret lines on white
        L=[(2,2,22,2),(22,2,22,12),(22,12,8,12),(8,12,8,7),(8,7,14,7),
           (2,2,2,22),(2,22,16,22),(16,22,16,17)]
        for x0,y0,x1,y1 in L: d.line([(x0*u,y0*u),(x1*u,y1*u)],fill=0,width=u)
    else:                             # dark: black with white diamonds
        d.rectangle([0,0,n*S,n*S],fill=0); h=n*S/2
        d.polygon([(h,2*u),(n*S-2*u,h),(h,n*S-2*u),(2*u,h)],fill=255)
        d.polygon([(h,7*u),(n*S-7*u,h),(h,n*S-7*u),(7*u,h)],fill=0)
    return t

img=Image.new('L',(W*S,H*S),255)
for group,kind in (('weave','weave'),('fret','fret'),('dark','dark')):   # back to front
    cx,cy=centre(group); T=tile(kind,{'weave':18,'fret':24,'dark':20}[kind])
    tex=Image.new('L',img.size,255)
    for y in range(0,H*S,T.height):
        for x in range(0,W*S,T.width): tex.paste(T,(x,y))
    for hx,hy in HEX:
        x,y=(cx+hx)*S,(cy+hy)*S; r=RAD*S
        m=Image.new('L',img.size,0); ImageDraw.Draw(m).ellipse([x-r,y-r,x+r,y+r],fill=255)
        img.paste(tex,(0,0),m)
        ImageDraw.Draw(img).ellipse([x-r,y-r,x+r,y+r],outline=0,width=2*S)
out=img.resize((W*2,H*2),Image.LANCZOS)
out.save(sys.argv[1])
print({g:tuple(round(v) for v in centre(g)) for g in C})
