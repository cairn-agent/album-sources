"""Original code-drawn sleeve, exported as editable SVG and a matching ID3 PNG.

No generated-image service or stock image. Pillow only rasterizes our geometry.
"""
from pathlib import Path
from html import escape
import math, random
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent.parent
W=1200
im=Image.new('RGB',(W,W));dr=ImageDraw.Draw(im)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1200" viewBox="0 0 1200 1200">',
     '<title>The Distance Turns to Light - Cairn</title>',
     '<desc>Original geometric artwork: a striped rising sun and converging colored paths beneath a midnight sky.</desc>']
def rgb(h):return tuple(int(h.lstrip('#')[i:i+2],16) for i in (0,2,4))
def hx(t):return '#'+''.join(f'{int(max(0,min(255,v))):02x}' for v in t)
def blend(a,b,u):return hx([x*(1-u)+y*u for x,y in zip(rgb(a),rgb(b))])
def line(pts,color,width=1):
    dr.line(pts,fill=color,width=max(1,round(width)))
    svg.append('<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
def poly(pts,color):
    dr.polygon(pts,fill=color);svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+f'" fill="{color}"/>')
def circle(x,y,r,color):
    dr.ellipse((x-r,y-r,x+r,y+r),fill=color);svg.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
def text(s,x,y,size=20,color='#E8ECF4',bold=False,spacing=0):
    f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',size)
    if spacing:
        xpos=x
        for c in s:dr.text((xpos,y),c,font=f,fill=color,anchor='ls');xpos+=dr.textlength(c,font=f)+spacing
    else:dr.text((x,y),s,font=f,fill=color,anchor='ls')
    svg.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{"bold" if bold else "normal"}" letter-spacing="{spacing}">{escape(s)}</text>')

for y in range(W):
    u=y/(W-1);c=blend('#090F2C','#263760',u**1.6)
    line([(0,y),(W,y)],c)
rng=random.Random(2000)
for i in range(140):
    x,y=rng.uniform(50,1150),rng.uniform(95,910)
    if y<505 and x<1070:continue
    circle(x,y,rng.choice([.65,.85,1.1]),rng.choice(['#61728D','#769EB7','#B3BDC5']))
text('CAIRN',66,87,25,spacing=7)
text('NIGHT ENGINE / 001',822,83,15,'#8DA9C9',spacing=2)
line([(66,118),(1134,118)],'#3E5474')
text('THE DISTANCE',59,238,88,bold=True,spacing=-2)
text('TURNS',60,343,108,bold=True,spacing=-1)
text('TO LIGHT',60,455,108,bold=True,spacing=-1)
text('EIGHT ORIGINAL TRANSMISSIONS',67,510,15,'#91BDD0',spacing=3)

# A rising circle is assembled from individual warm horizontal stripes.
cx,cy,radius=789,758,168
for y in range(590,923,8):
    rel=y-cy
    if abs(rel)>=radius:continue
    half=math.sqrt(radius*radius-rel*rel)
    color=blend('#FFF0CB','#E880AB',(y-590)/333)
    poly([(cx-half,y),(cx+half,y),(cx+half,y+3.6),(cx-half,y+3.6)],color)

# Two incomplete orbit outlines retain a deliberate opening toward the title.
for rx,ry,start,end,col in [(263,98,-26,221,'#71BACD'),(334,119,3,178,'#AB90C7')]:
    pts=[]
    for degree in range(start,end+1):
        a=math.radians(degree);x=rx*math.cos(a);y=ry*math.sin(a)
        rot=-.24;pts.append((cx+x*math.cos(rot)-y*math.sin(rot),cy+x*math.sin(rot)+y*math.cos(rot)))
    line(pts,col,1.4)

poly([(0,941),(1200,907),(1200,1200),(0,1200)],'#101B37')
for i in range(11):
    y=937+(i/10)**2*263;line([(0,y+18),(1200,y-16)],'#293851',1)
for x in range(-1600,2501,190):line([(782,929),(x,1200)],'#283A59',1)

# Three routes become nearly one at the horizon; they remain differently colored.
for x1,x2,delta,col in [(80,250,-18,'#68B9CC'),(448,597,0,'#B0A0D2'),(919,1110,18,'#E9A693')]:
    poly([(x1,1200),(x2,1200),(790+delta,927),(783+delta,927)],col)
    line([(x1+9,1200),(785+delta,927)],'#DBE8E7',1.3)
line([(50,934),(1148,905)],'#769BB2',1.2)
circle(787,925,3,'#FFF5DC')

# Footer sits in a solid label band, keeping the road image uncluttered.
poly([(0,1127),(1200,1127),(1200,1200),(0,1200)],'#0A122A')
text('132-142 BPM / STEREO',65,1172,15,'#B1BED0',spacing=2)
text('THE LOCAL HOURS / 2026',813,1172,14,'#B1BED0',spacing=1)
svg.append('</svg>')
(ROOT/'art').mkdir(exist_ok=True)
(ROOT/'art'/'cover.svg').write_text('\n'.join(svg)+'\n')
im.save(ROOT/'art'/'cover.png',optimize=True)
print('Original sleeve exported as SVG and PNG.')
