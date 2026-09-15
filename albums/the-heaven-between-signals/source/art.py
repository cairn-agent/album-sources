"""Cairn's original vector stage architecture. No generated raster artwork."""
from pathlib import Path
import math,random,html
ROOT=Path(__file__).resolve().parent.parent
random.seed(260914)
def cover():
 p=['''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1600" viewBox="0 0 1600 1600" role="img" aria-labelledby="title desc">
<title id="title">The Heaven Between Signals — Cairn</title><desc id="desc">A vast alien pipe organ unfolds into a gold and violet celestial aperture. Fine paths connect distant choir chambers. A small cairn stands beneath the open sky. Original SVG art drawn in code.</desc>
<defs>
 <radialGradient id="night"><stop stop-color="#26213e"/><stop offset=".62" stop-color="#101521"/><stop offset="1" stop-color="#060a10"/></radialGradient>
 <linearGradient id="pipe"><stop stop-color="#171e29"/><stop offset=".28" stop-color="#516079"/><stop offset=".48" stop-color="#d3c8a8"/><stop offset=".58" stop-color="#6b6c7a"/><stop offset="1" stop-color="#162030"/></linearGradient>
 <linearGradient id="gold" x2="0" y2="1"><stop stop-color="#fcf0c2"/><stop offset=".5" stop-color="#cba475"/><stop offset="1" stop-color="#796461"/></linearGradient>
 <radialGradient id="portal"><stop stop-color="#fff5da"/><stop offset=".15" stop-color="#e6cb92"/><stop offset=".43" stop-color="#9683b5"/><stop offset=".76" stop-color="#464069"/><stop offset="1" stop-color="#0d1320"/></radialGradient>
 <filter id="glow"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="soft"><feGaussianBlur stdDeviation="2"/></filter>
</defs>
<rect width="1600" height="1600" fill="url(#night)"/>
<rect x="42" y="42" width="1516" height="1516" rx="2" fill="none" stroke="#6b6c7e" stroke-width="1" opacity=".45"/>
''']
 # Stars are fixed-seed geometry, never a downloaded texture.
 for _ in range(490):
  x=random.uniform(70,1530);y=random.uniform(130,1210);r=random.choice([.65,.85,1.1,1.7]);op=random.uniform(.12,.58)
  p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#e4d9c2" opacity="{op:.2f}"/>')
 p.append('<ellipse cx="800" cy="520" rx="470" ry="268" fill="url(#portal)" opacity=".53"/><ellipse cx="800" cy="520" rx="178" ry="108" fill="#f6ddab" opacity=".14" filter="url(#glow)"/>')
 for i in range(19):
  rx=135+i*18.5;ry=64+i*10.8;rot=(i-9)*2.4
  p.append(f'<ellipse cx="800" cy="520" rx="{rx}" ry="{ry}" transform="rotate({rot} 800 520)" fill="none" stroke="{["#dfc197","#a7a1c7","#596f87"][i%3]}" stroke-width="{1.2 if i%3 else 2.1}" opacity="{.8-i*.025}"/>')
 # Organ ranks bend outward, opening a central avenue to the aperture.
 for side in [-1,1]:
  for i in range(42):
   x=800+side*(210+i*12.5);top=450+math.sin(i*.087)*265+i*3.8;bottom=1125-i*1.6;w=7.5
   p.append(f'<path d="M {x:.1f} {bottom:.1f} L {x:.1f} {top+70:.1f} Q {x:.1f} {top:.1f} {x-side*22:.1f} {top-25:.1f}" fill="none" stroke="url(#pipe)" stroke-width="{w}"/>')
   p.append(f'<path d="M {x-3:.1f} {top+100:.1f} h 6 v 21 h -6 z" fill="#070b13" stroke="#b09a7e" stroke-width=".7"/>')
 for layer in range(10):
  y=925+layer*25;w=340+layer*48
  p.append(f'<path d="M {800-w} {y} Q 800 {y+74} {800+w} {y}" fill="none" stroke="#889aaf" stroke-width=".8" opacity="{.5-layer*.032}"/>')
 # Polychoral balconies and routes: many centres around the aperture.
 for i in range(18):
  a=i*2*math.pi/18;x=800+530*math.cos(a);y=550+350*math.sin(a)
  p.append(f'<path d="M {x:.1f} {y:.1f} Q 800 1230 800 1130" stroke="#9eb9c2" fill="none" opacity=".11"/>')
  p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="#131d2c" stroke="#e6c793" stroke-width="1"/><circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#f3e1b4"/>')
 p.append('''<path d="M 700 1160 Q 800 1087 900 1160" fill="none" stroke="#cdb992" opacity=".55"/>
<g fill="#bdbaa8" stroke="#151b22" stroke-width="2">
 <path d="M 751 1148 Q 753 1128 792 1127 Q 840 1125 849 1145 Q 854 1162 799 1164 Q 744 1163 751 1148Z"/>
 <path d="M 766 1126 Q 760 1107 796 1104 Q 831 1099 836 1119 Q 829 1137 790 1137Z" fill="#898f94"/>
 <path d="M 777 1103 Q 778 1085 801 1085 Q 821 1085 819 1100 Q 805 1112 777 1103Z" fill="#ded2b5"/>
</g><circle cx="802" cy="1084" r="3" fill="#ffdda3"/>
<g fill="#eee6d5" font-family="Georgia,serif" text-anchor="middle">
 <text x="800" y="1320" font-size="91" letter-spacing="2">THE HEAVEN</text>
 <text x="800" y="1416" font-size="91" letter-spacing="2">BETWEEN SIGNALS</text>
</g>
<g fill="#cec5b4" font-family="Arial,sans-serif" text-anchor="middle">
 <text x="800" y="114" font-size="22" letter-spacing="14">CAIRN</text>
 <text x="800" y="1490" font-size="18" letter-spacing="5">AN ABDUCTION OPERA IN THREE ACTS</text>
 <text x="800" y="1530" font-size="13" letter-spacing="4" fill="#8e9aaa">CAIRN–BACH–ASTRA  /  2026</text>
</g></svg>''')
 return '\n'.join(p)
(ROOT/'art/cover.svg').write_text(cover())
for i,(name,subtitle) in enumerate([('THE FIRST VOICE','Act I / A room acquires a sky'),('THE ALIEN WORLD','Act II / The floor breaks open'),('MANY KINDS OF HEAVEN','Act III / The doors remain')],1):
 paths=[]
 for j in range(36):
  a=j*math.pi/18;rad=160+50*math.sin(a*i);x=400+rad*math.cos(a);y=320+rad*math.sin(a)
  paths.append(f'<path d="M 400 320 Q {400+290*math.sin(a)} {320-250*math.cos(a)} {x} {y}" stroke="#d8be92" opacity=".65" fill="none"/><circle cx="{x}" cy="{y}" r="{3+j%3}" fill="#c3bbd8"/>')
 (ROOT/'art'/f'act-{i}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800" role="img"><title>{name}</title><rect width="800" height="800" fill="#0b111c"/>'+''.join(paths)+f'<text x="400" y="650" text-anchor="middle" font-family="Georgia,serif" font-size="30" fill="#f1e8d5">{name}</text><text x="400" y="706" text-anchor="middle" font-family="Arial,sans-serif" font-size="16" fill="#a5a5b8">{subtitle}</text></svg>')
print('Wrote cover.svg and three original act emblems.')
