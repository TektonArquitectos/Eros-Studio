# Genera texturas cinematográficas minimalistas (oscuro + luz dorada + grano) para tarjetas y escenas.
import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
def lerp(a,b,t): return a+(b-a)*t
def texture(w,h,light=(0.7,0.2),col=(201,169,110),strength=.55,horizon=None,seed=0,base=(11,11,12),second=None,vignette=.55):
    r=np.random.default_rng(seed)
    yy,xx=np.mgrid[0:h,0:w].astype(np.float32); xx/=w; yy/=h
    img=np.zeros((h,w,3),np.float32); img[:]=base
    # luz principal
    d=np.hypot(xx-light[0],(yy-light[1])*(h/w)); g=np.exp(-(d**2)/0.11)*strength
    for c in range(3): img[...,c]+= g*(col[c]-base[c])
    if second:
        (lx,ly),scol,ss=second
        d2=np.hypot(xx-lx,(yy-ly)*(h/w)); g2=np.exp(-(d2**2)/0.07)*ss
        for c in range(3): img[...,c]+= g2*(scol[c]-base[c])
    # horizonte suave
    if horizon is not None:
        band=np.exp(-((yy-horizon)**2)/0.0015)*0.35
        for c in range(3): img[...,c]+= band*(col[c]-base[c])
        below=(yy>horizon).astype(np.float32)*0.5
        for c in range(3): img[...,c]-= below*(img[...,c]-base[c])*0.6
    # viñeta
    v=1-vignette*np.clip(np.hypot(xx-.5,yy-.5)*1.3-0.25,0,1)
    img*=v[...,None]
    # grano
    img+= r.normal(0,4.5,(h,w,1))
    im=Image.fromarray(np.clip(img,0,255).astype(np.uint8))
    return im
out='/home/claude/site/assets/img/'
specs={
 # pilares (tarjetas verticales)
 'pilar-01': dict(light=(.75,.25),col=(201,169,110),strength=.6,seed=1),
 'pilar-02': dict(light=(.3,.7),col=(237,235,230),strength=.32,seed=2,second=((.75,.3),(201,169,110),.35)),
 'pilar-03': dict(light=(.5,.15),col=(201,169,110),strength=.5,seed=3,horizon=.62),
 'pilar-04': dict(light=(.2,.8),col=(120,140,150),strength=.4,seed=4,second=((.8,.2),(201,169,110),.3)),
 'pilar-05': dict(light=(.5,.35),col=(214,190,140),strength=.55,seed=5,horizon=.7),
 # escenas "imagina esto"
 'escena-01': dict(light=(.5,.55),col=(232,180,110),strength=.75,seed=11,horizon=.58),   # amanecer
 'escena-02': dict(light=(.3,.3),col=(237,235,230),strength=.35,seed=12,second=((.72,.6),(201,169,110),.4)),
 'escena-03': dict(light=(.5,.5),col=(201,169,110),strength=.45,seed=13),
 'escena-04': dict(light=(.8,.2),col=(140,160,170),strength=.4,seed=14,second=((.2,.7),(201,169,110),.25)),
 'escena-05': dict(light=(.5,.4),col=(214,196,150),strength=.6,seed=15,horizon=.66),
 'manifiesto': dict(light=(.6,.5),col=(201,169,110),strength=.5,seed=21,vignette=.7),
}
for name,kw in specs.items():
    w,h=(720,960) if name.startswith('pilar') else (1200,800)
    if name=='manifiesto': w,h=1000,1000
    texture(w,h,**kw).save(out+name+'.webp','WEBP',quality=82,method=6)
print('ok')
