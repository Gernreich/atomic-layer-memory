# Find the centre of every circle in the 2009 GIF: three hexagonal groups of seven.
# Starts from hand-placed centres and refines each against the mean of its group.
# Usage: python3 tools/find_centres.py images/atomic_i_2009.png  -> tools/centres.json
import sys, json, os
from PIL import Image; import numpy as np
A=(np.array(Image.open(sys.argv[1]).convert('L'))<128).astype(float); H,W=A.shape
R=34; PAD=60
P=np.zeros((H+2*PAD,W+2*PAD)); P[PAD:PAD+H,PAD:PAD+W]=A; P[P==0]=0
V=np.full_like(P,np.nan); V[PAD:PAD+H,PAD:PAD+W]=A   # nan outside the image
G=dict(weave=[(95,30),(215,30),(35,140),(155,140),(275,140),(95,240),(215,240)],
       fret=[(160,62),(280,62),(100,170),(225,170),(350,170),(160,280),(280,280)],
       dark=[(225,102),(345,102),(160,210),(285,210),(410,210),(215,315),(345,315)])
yy,xx=np.mgrid[-R:R+1,-R:R+1]; disk=(xx**2+yy**2)<=R*R
def crop(c): x,y=c; return V[y+PAD-R:y+PAD+R+1,x+PAD-R:x+PAD+R+1]
out={}
for name,cs in G.items():
    cs=list(cs)
    for it in range(4):
        tpl=np.nanmean([crop(c) for c in cs],0)
        new=[]
        for (x,y) in cs:
            best=None
            for dy in range(-6,7):
                for dx in range(-6,7):
                    c=crop((x+dx,y+dy)); m=~np.isnan(c)&disk
                    if m.sum()<200: continue
                    t=tpl[m]-tpl[m].mean(); s=c[m]-c[m].mean()
                    r=(t*s).sum()/np.sqrt((t*t).sum()*(s*s).sum()+1e-9)
                    if best is None or r>best[0]: best=(r,x+dx,y+dy)
            new.append((best[1],best[2],round(best[0],2)))
        cs=[(a,b) for a,b,_ in new]
    print(name,new)
    out[name]=cs
json.dump(out,open(os.path.join(os.path.dirname(__file__),'centres.json'),'w'))
