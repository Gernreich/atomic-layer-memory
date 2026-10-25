# atomic_i in colour: two outer groups of seven are the bits (0 red, 1 blue),
# the middle group is the spacer (green) that sits between every bit.
# Usage: python3 tools/redraw_rgb.py images/atomic_i_rgb.png
import json, math, os, sys
from PIL import Image, ImageDraw, ImageFont
C=json.load(open(os.path.join(os.path.dirname(__file__),'centres.json')))
S=4; W,H=428,440                      # extra height for the legend + example strip
D=120; RAD=33
HEX=[(0,0)]+[(D*math.cos(math.radians(a)),D*math.sin(math.radians(a))) for a in range(0,360,60)]
COL={'zero':(214,40,40),'spacer':(30,150,60),'one':(40,80,214)}
GROUP={'zero':'weave','spacer':'fret','one':'dark'}
INK=(20,20,20)

def tile(kind,col,n):
    t=Image.new('RGB',(n*S,n*S),col); d=ImageDraw.Draw(t); u=S
    light=tuple(int(c+(255-c)*.55) for c in col); dark=tuple(int(c*.45) for c in col)
    if kind=='weave':
        for k in range(-2,4):
            y=k*n*S/3; d.line([(0,y+n*S/3),(n*S/2,y),(n*S,y+n*S/3)],fill=light,width=3*u)
    elif kind=='fret':
        t.paste(light,[0,0,n*S,n*S])
        for x0,y0,x1,y1 in [(2,2,22,2),(22,2,22,12),(22,12,8,12),(8,12,8,7),(8,7,14,7),
                            (2,2,2,22),(2,22,16,22),(16,22,16,17)]:
            d.line([(x0*u,y0*u),(x1*u,y1*u)],fill=col,width=u)
    else:
        h=n*S/2
        d.polygon([(h,2*u),(n*S-2*u,h),(h,n*S-2*u),(2*u,h)],fill=light)
        d.polygon([(h,7*u),(n*S-7*u,h),(h,n*S-7*u),(7*u,h)],fill=col)
    return t,dark

TEX={}
def texture(role,size):
    if role not in TEX:
        kind=GROUP[role]; T,dark=tile(kind,COL[role],{'weave':18,'fret':24,'dark':20}[kind])
        tex=Image.new('RGB',size)
        for y in range(0,size[1],T.height):
            for x in range(0,size[0],T.width): tex.paste(T,(x,y))
        TEX[role]=(tex,dark)
    return TEX[role]

def atom(img,role,x,y,r):
    tex,dark=texture(role,img.size)
    m=Image.new('L',img.size,0); ImageDraw.Draw(m).ellipse([x-r,y-r,x+r,y+r],fill=255)
    img.paste(tex,(0,0),m)
    ImageDraw.Draw(img).ellipse([x-r,y-r,x+r,y+r],outline=dark,width=2*S)

img=Image.new('RGB',(W*S,H*S),'white')
for role in ('zero','spacer','one'):                       # back to front
    pts=C[GROUP[role]]; cx=sum(p[0] for p in pts)/7; cy=sum(p[1] for p in pts)/7
    for hx,hy in HEX: atom(img,role,(cx+hx)*S,(cy+hy)*S,RAD*S)

# legend + example: 0 spacer 0 spacer 0 spacer 1 spacer 0
d=ImageDraw.Draw(img)
try: F=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',11*S)
except OSError: F=ImageFont.load_default()
y0=362*S
d.line([(10*S,y0-6*S),(418*S,y0-6*S)],fill=(200,200,200),width=S)
x=18*S
for role,label in (('zero','0'),('spacer','spacer'),('one','1')):
    atom(img,role,x+8*S,y0+10*S,8*S); d.text((x+20*S,y0+3*S),label,fill=INK,font=F); x+=90*S
seq='0s0s0s1s0'; r=14*S; step=26*S; x=(W*S-step*(len(seq)-1))/2; y=y0+48*S
for ch in seq:
    atom(img,{'0':'zero','1':'one','s':'spacer'}[ch],x,y,r)
    if ch!='s': d.text((x,y+r+3*S),ch,fill=INK,font=F,anchor='mt')
    x+=step
img.resize((W*2,H*2),Image.LANCZOS).save(sys.argv[1])
