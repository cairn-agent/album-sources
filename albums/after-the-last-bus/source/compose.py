"""Compose After the Last Bus. Standard library only; fixed seeds reproduce every note.

TSV event columns: at, length (beats), voice, MIDI note, gain, pan,
brightness, expression, tape-delay send, diffuse-reverb send.
"""
from pathlib import Path
import json, random, struct
ROOT=Path(__file__).resolve().parent.parent
VOICES=['soft kick','paper snare','closed shuffle','open shuffle','rim','metal scrap','sine sub','moving reese','haze pad','ghost vowel','shelter tine','granular caller','folded sonar','concrete chord','glass resonator','service acid','spectral choir','reed memory','rain','reverse breath','contact click']
TRACKS=[
 dict(title='Shelter Glass',slug='shelter-glass',bpm=132,root=41,key='F minor',voice=10,swing=.15,style='garage',
      harmony=[(0,'m9'),(-2,'maj9'),(-4,'maj7'),(3,'maj7')],
      motif=[(.5,12,.65),(1.75,15,.4),(3.25,10,.5),(4.5,7,1.2),(6.75,10,.7),(8.25,12,1.5),(10.75,19,.6),(12.5,15,1.4),(15,10,.65)],
      form=[('intro',8),('approach',16),('first',24),('break',16),('rebuild',8),('peak',32),('outro',8)],
      instrument='Shelter Tine: softened two-operator FM, unstable tuning, dotted-eighth tape echo.',
      description='A few notes on wet glass. Crooked two-step grows around a small, warm signal.'),
 dict(title='Someone on the Other Line',slug='someone-on-the-other-line',bpm=134,root=39,key='E-flat minor',voice=11,swing=.19,style='garage',
      harmony=[(0,'m9'),(-4,'maj7'),(5,'m9'),(-2,'maj9')],
      motif=[(.25,19,.45),(1.5,15,.7),(3,12,.35),(4.75,10,.9),(7.25,7,.45),(8.5,12,.4),(9.25,15,.6),(11.5,19,.8),(13.25,17,.6),(14.75,15,.9)],
      form=[('intro',8),('approach',16),('first',32),('break',24),('rebuild',8),('peak',40),('outro',16)],
      instrument='Granular Caller: a three-formant glottal synth under 87 ms grains, glides and reverse envelopes; five-sixteenth echo.',
      description='A call that never quite becomes a sentence; loose shuffles, missing kicks, and fragments answering across the stereo field.'),
 dict(title='Underpass Pressure',slug='underpass-pressure',bpm=140,root=38,key='D minor',voice=12,swing=.11,style='half',
      harmony=[(0,'m9'),(0,'m9'),(-4,'maj7'),(-2,'sus9')],
      motif=[(0,12,1.1),(3.25,7,.5),(5.5,10,1.3),(8.75,12,.8),(11.25,15,.5),(14,7,1.25)],
      form=[('intro',16),('approach',16),('first',32),('break',24),('rebuild',8),('peak',40),('outro',16)],
      instrument='Folded Sonar: sine-wave phase modulation through a changing wavefolder; restrained filtered Reese beneath, long cross-fed echo.',
      description='Half-time weight and a distant sonar motif. The second passage lets the garage rhythm leak back through.'),
 dict(title='Estate of Echoes',slug='estate-of-echoes',bpm=130,root=43,key='G minor',voice=13,swing=.14,style='dub',
      harmony=[(0,'m9'),(5,'m9'),(-4,'maj7'),(-2,'sus9')],
      motif=[(.75,12,.2),(2.5,19,.25),(4.25,15,.3),(7,10,.2),(8.75,12,.35),(11.5,7,.2),(13.25,10,.25),(15,14,.4)],
      form=[('intro',8),('approach',24),('first',32),('break',16),('rebuild',8),('peak',40),('outro',16)],
      instrument='Concrete Chord: detuned band-limited saw pairs with a closing resonant filter; high-feedback, high-passed dub tape returns.',
      description='Short chord stabs ricochet between buildings. Two-step periodically straightens into a muted four-beat pulse.'),
 dict(title='03:17, No Reply',slug='0317-no-reply',bpm=120,root=36,key='C minor',voice=14,swing=.08,style='interlude',
      harmony=[(0,'m9'),(-4,'maj7'),(3,'maj9'),(5,'m9')],
      motif=[(1,19,2.4),(5.5,15,1.8),(9,12,2.8),(14,14,1.5)],
      form=[('intro',8),('first',16),('break',24),('peak',24),('outro',8)],
      instrument='Glass Resonator: three inharmonic modes with independent damping; reverse swells and a large, slow, dark room.',
      description='A short shelter from the drums: glass resonance, wordless air, rain and a nearly submerged pulse.'),
 dict(title='Service Tunnel',slug='service-tunnel',bpm=136,root=42,key='F-sharp minor',voice=15,swing=.075,style='techno',
      harmony=[(0,'m9'),(0,'m9'),(-2,'sus9'),(-4,'maj7')],
      motif=[(0,0,.2),(.75,12,.2),(1.5,7,.3),(2.75,10,.2),(3.5,7,.25),(4.25,0,.2),(5,12,.25),(6.5,15,.3),(7.25,10,.2),(8,0,.2),(9.25,7,.2),(10,12,.25),(11.75,10,.2),(12.5,7,.3),(14,3,.25),(15.25,0,.3)],
      form=[('intro',16),('approach',24),('first',32),('break',16),('rebuild',16),('peak',40),('outro',16)],
      instrument='Service Acid: band-limited saw, nonlinear drive and an accented resonant envelope; shorter room and half-beat tape.',
      description='The machine room: a dry, impatient acid line, metallic syncopation and a four-on-the-floor crest with broken edges.'),
 dict(title='Borrowed Dawn',slug='borrowed-dawn',bpm=138,root=45,key='A minor',voice=16,swing=.17,style='garage',
      harmony=[(0,'m9'),(3,'maj9'),(-4,'maj7'),(5,'m9')],
      motif=[(.5,19,1.2),(2.75,15,.8),(5,12,1.5),(7.25,14,.6),(8.5,19,1.8),(11.25,22,.9),(13,19,1.2),(15,15,.7)],
      form=[('intro',16),('approach',16),('first',32),('break',32),('rebuild',8),('peak',40),('outro',16)],
      instrument='Spectral Choir: nine additive partials with moving weights and subtle beating; wide, modulated late reflections.',
      description='The most open track: wide choir harmonics, a high wordless response, then the heaviest shuffle on the record.'),
 dict(title='Footsteps Home',slug='footsteps-home',bpm=128,root=41,key='F minor',voice=17,swing=.16,style='home',
      harmony=[(0,'m9'),(-4,'maj7'),(3,'maj9'),(-2,'sus9')],
      motif=[(.5,12,1.3),(3.25,15,.8),(5.5,10,1.4),(8.25,7,2.0),(11.5,10,1.2),(14,12,1.6)],
      form=[('intro',8),('approach',16),('first',24),('break',24),('rebuild',8),('peak',24),('outro',24)],
      instrument='Reed Memory: four sine drawbars, tremolo, tape-like pitch drift and long alternating echoes; opening FM motif returns in the coda.',
      description='A warmer, slower walk back. The first track leaves a small reflection in the final bars.'),
]
CHORD={'m9':[0,3,7,10,14],'maj9':[0,4,7,11,14],'maj7':[0,4,7,11],'sus9':[0,5,7,10,14]}
def vlq(n):
 b=[n&127]
 while n>>7:n>>=7;b.insert(0,(n&127)|128)
 return bytes(b)
def meta(k,s):
 s=s.encode();return bytes([255,k])+vlq(len(s))+s
def miditrack(es):
 out=bytearray();last=0
 for tick,order,b in sorted(es,key=lambda x:(x[0],x[1])):out+=vlq(tick-last)+b;last=tick
 out+=b'\x00\xff\x2f\x00';return b'MTrk'+struct.pack('>I',len(out))+out
def midi(s,path):
 ppq=960;tempo=round(60e6/s['bpm']);chunks=[miditrack([(0,0,meta(3,s['title'])),(0,0,b'\xff\x51\x03'+tempo.to_bytes(3,'big')),(0,0,b'\xff\x58\x04\x04\x02\x18\x08')]+[(round(x['bar']*4*ppq),0,meta(6,x['name'])) for x in s['sections']])]
 melodic=[v for v in sorted(set(e[2] for e in s['events'])) if v>5 and v!=20];channels=[x for x in range(16) if x!=9]
 programs={6:38,7:38,8:89,9:54,10:4,11:54,12:98,13:90,14:10,15:80,16:91,17:19,18:122,19:95}
 for v in sorted(set(e[2] for e in s['events'])):
  drum=v<=5 or v==20;ch=9 if drum else channels[melodic.index(v)];out=[(0,0,meta(3,VOICES[v]))]
  if not drum:out.append((0,0,bytes([192|ch,programs[v]])))
  for at,dur,voice,note,gain,pan,tone,motion,delay,reverb in s['events']:
   if voice!=v:continue
   n={0:36,1:38,2:42,3:46,4:37,5:51,20:76}.get(v,round(note));vel=max(1,min(115,round(gain*320)))
   out += [(round(at*ppq),1,bytes([144|ch,n,vel])),(round((at+dur)*ppq),-1,bytes([128|ch,n,0]))]
  chunks.append(miditrack(out))
 path.write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),ppq)+b''.join(chunks))
def compose(t,num):
 rng=random.Random(9173+num*1701);ev=[];sections=[];bar=0;root=t['root'];beat=60/t['bpm']
 def add(at,dur,v,n,g,pan=0,tone=.4,motion=0,ds=0,rv=0):
  if g<=.0001:return
  assert at>=0 and dur>0 and 0<=n<=127 and -1<=pan<=1
  ev.append([round(at,6),round(dur,6),v,round(n,4),round(g,6),round(pan,4),round(tone,4),round(motion,4),round(ds,4),round(rv,4)])
 def human(at):
  # A swung sixteenth grid plus small independent millisecond deviations.
  off=at%1;sw=t['swing'] if abs(off-.5)<.08 else t['swing']*.5 if abs(off-.25)<.08 or abs(off-.75)<.08 else 0
  return max(0,at+sw+rng.uniform(-.007,.011)/beat)
 for scene,count in t['form']:
  sections.append(dict(name=scene,bar=bar,bars=count))
  for local in range(count):
   b=bar+local;at=b*4;u=local/max(1,count-1);quiet=scene=='break';full=scene in ['first','peak'];peak=scene=='peak';intro=scene=='intro';outro=scene=='outro';inter=t['style']=='interlude'
   energy=.20 if intro else .66 if scene=='approach' else .98 if full else .17 if quiet else .35+.4*u if scene=='rebuild' else .68*(1-u)+.1
   active=not quiet and not (intro and local<count-4) and not (outro and local>=count//2) and not(scene=='rebuild' and local>=count-2)
   if inter:active=peak and local>=8 and local%2==0
   base,quality=t['harmony'][(b//4)%4];bassnote=root+base
   while bassnote<33:bassnote+=12
   chord=[root+base+12+i for i in CHORD[quality]]
   if local%4==0:
    padgain=.016 if quiet else .020 if intro else .025 if full else .021
    if inter:padgain=.014 if quiet else .025
    if outro:padgain*=1-u*.75
    for j,n in enumerate(chord[1:]):add(at,14.5,8,n,padgain,(-.65+j*.38),.22+num*.025,0,.06,.50)
    add(at,15.9,18,60,.015 if quiet or intro else .009,-.6 if b%8==0 else .6,ds=0,rv=.10)
   # Sparse contact noise is composed into the groove, not a constant crackle bed.
   if b%2==1:add(human(at+3.35),.03,20,76,.011,rng.uniform(-.8,.8),ds=.3,rv=.18)
   if active:
    half=t['style']=='half' and not(peak and local>=24)
    straight=t['style']=='techno' and (peak or (full and local>=16)) or t['style']=='dub' and peak and 16<=local<32
    if inter:kicks=[0];snares=[]
    elif straight:kicks=[0,1,2,3];snares=[1.025,3.018]
    elif half:kicks=[[0,2.75],[.0,1.5],[0,3.25],[.5,1.75]][b%4];snares=[2.018]
    else:
     kicks=[[0,1.75,2.5],[0,2.25],[.25,1.5,3.5],[0,1.75,2.75]][(b+num)%4]
     snares=[1.025,3.018]
    if b%16==15:kicks=kicks[:-1]
    if intro:kicks=kicks[:1];snares=[]
    for x in kicks:add(human(at+x),.1,0,36,(.41 if peak else .37)*rng.uniform(.94,1.02)*( .7 if inter else 1),tone=.28 if half else .48)
    for x in snares:
     add(human(at+x),.08,1,38,(.20 if half else .15)*rng.uniform(.90,1.04),-.07,tone=.25+num*.05,ds=.05 if t['style']!='dub' else .17,rv=.24)
     add(human(at+x+.013),.03,4,37,.045,.22,.22,ds=.05,rv=.10)
    if not inter:
     hats=[.0,.5,.75,1.5,2.0,2.5,3.25,3.5] if not half else [.5,1.25,1.5,2.75,3.5]
     if intro:hats=[.5,2.5]
     for j,x in enumerate(hats):
      if rng.random()<.13:continue
      add(human(at+x),.035,2,42,rng.uniform(.028,.054)*(1 if full else .78),-.4 if j%2 else .30,.35,ds=.07 if j%3==0 else 0,rv=.07)
     if full and b%2==0:add(human(at+2.5),.1,3,46,.041,.32,.4,ds=.12,rv=.14)
     if full or scene=='approach':
      for x in ([.75,2.75] if b%2==0 else [1.5,3.75]):add(human(at+x),.05,4,37,rng.uniform(.025,.046),rng.choice([-.55,.45]),.6,ds=.25,rv=.24)
     if b%8==7:
      for x in [2.75,3.375,3.75]:add(human(at+x),.05,1,38,.046,pan=rng.uniform(-.4,.4),tone=.3,ds=.25,rv=.28)
     if (t['style'] in ['techno','dub'] and full) or (peak and b%4==2):
      for x in ([.75,2.25,3.5] if t['style']=='techno' else [3.25]):add(human(at+x),.06,5,51,.021 if t['style']=='techno' else .018,rng.uniform(-.7,.7),.55,ds=.20,rv=.31)
    # Sub phrases follow harmony; breathing room around the snare is intentional.
    if half:bp=[(0,1.45,0),(2.75,.85,0)] if b%2==0 else [(.25,.8,0),(1.5,.4,7),(3.25,.6,-2)]
    elif straight:bp=[(.5,.32,0),(1.5,.33,0),(2.5,.34,0),(3.5,.3,7 if b%4==3 else 0)]
    else:bp=[(.05,.65,0),(1.75,.42,0),(2.5,.8,7 if b%4==3 else 0)] if b%2==0 else [(.25,1.0,0),(2.25,.55,0),(3.5,.35,10 if b%4==3 else 0)]
    if inter:bp=[(0,2.8,0)]
    for x,d,n in bp:
     add(human(at+x),d,6,bassnote+n,.235 if half else .19 if not inter else .085,tone=.3,motion=.25 if b%4==3 else 0)
     if t['style']=='half' and full:add(human(at+x+.018),d,7,bassnote+n,.075,0,.35+.22*(local/count),.5 if b%4<2 else 1,ds=.025,rv=.025)
   elif quiet and local%8==0 and not inter:add(at+.15,4.5,6,bassnote,.056)
   # Stabs articulate the harmonic rhythm away from the kick.
   if (full or scene=='approach') and not inter and t['voice']!=13:
    offsets=[.75,2.5] if b%2==0 else [1.75]
    if t['style']=='techno':offsets=[.75] if b%3==0 else []
    for x in offsets:
     for j,n in enumerate(chord[1:4]):add(human(at+x),.22,13,n,.032*energy,(-.25+j*.25),.25+.15*energy,ds=.43,rv=.40)
   # Each hook spans four bars and alternates with a second, sparser answer.
   hook_on=full or quiet and local%8<4 or scene=='rebuild' or intro and local>=4 or outro and local<count-4
   if hook_on:
    for when,degree,length in t['motif']:
     if int(when//4)!=b%4:continue
     x=when%4
     if quiet and rng.random()<.45:continue
     if scene=='approach' and b%8>=4:continue
     if full and (local//4)%4==3 and x>1.5:continue
     gain=(.079 if t['voice'] in [10,12,14,17] else .11 if t['voice']==11 else .065 if t['voice']==16 else .073)*(.34 if quiet else .55 if intro else .68 if outro else 1)
     if outro:gain*=1-u*.75
     note=root+12+degree
     if t['voice']==15:note=root+12+degree
     if t['voice']==13:
      for j,n in enumerate(chord):add(human(at+x),length,13,n,.038*(.45 if quiet else 1),(-.5+j*.25),.25+.32*energy,ds=.70,rv=.39)
     else:
      # High-register answer on selected four-bar phrases, not a repeated octave stack.
      if peak and local>=count-16 and b%8>=4 and t['voice']!=15:note+=12;gain*=.70
      motion=-.85 if t['voice']==11 and (b+int(x))%7==0 else .4 if t['voice'] in [11,15] else 0
      add(human(at+x),length*(1.35 if quiet else 1),t['voice'],note,gain,rng.uniform(-.26,.26),.26+.38*energy+(rng.random()-.5)*.08,motion,ds=.42 if t['voice']!=15 else .27,rv=.55 if t['voice']!=15 else .17)
   # Wordless call/response: never a continuous lead running over every bar.
   if b%8 in [2,6] and (full or quiet or scene=='rebuild'):
    degrees=[12,15,10,7,19,15,14,10];deg=degrees[(b//8+num)%8]
    vg=.046 if quiet else .064 if peak else .053
    if t['voice']==11:vg*=.5
    add(at+(2.25 if b%8==2 else .75),1.3 if b%8==2 else .6,9,root+24+deg,vg,-.36 if b%8==2 else .36,.2+.55*rng.random(),-.8 if b%16==6 else .4,ds=.53,rv=.65)
   if local==count-1 and scene not in ['outro','break']:
    add(at+1.8,1.8,19,root+24+7,.05,.2,.4,ds=.42,rv=.7)
   if t['style']=='home' and outro and local>=8 and b%4==0:
    for x,deg,d in TRACKS[0]['motif'][:4]:add(at+x,d*1.7,10,root+12+deg,.039*(1-u*.55),-.25,.25,ds=.5,rv=.75)
  bar+=count
 ev.sort(key=lambda e:(e[0],e[2]));stem=f'{num:02d}-{t["slug"]}'
 score=dict(title=t['title'],number=num,stem=stem,bpm=t['bpm'],key=t['key'],seed=13092026+num*197,engine='Shelter Engine 1',engineTrack=num,endBeat=bar*4,sections=sections,description=t['description'],instrument=t['instrument'],swingSixteenth=t['swing'],eventColumns=['at','length','voice','note','gain','pan','tone','motion','delay','reverb'],voices=VOICES,events=ev)
 (ROOT/'scores'/f'{stem}.json').write_text(json.dumps(score,indent=2)+'\n')
 (ROOT/'scores'/f'{stem}.tsv').write_text(f'{t["bpm"]}\t{bar*4}\t{score["seed"]}\t{num}\n'+''.join('\t'.join(map(str,e))+'\n' for e in ev))
 midi(score,ROOT/'midi'/f'{stem}.mid')
 return {k:v for k,v in score.items() if k not in ['events','voices']}
def main():
 for d in ['scores','midi']:(ROOT/d).mkdir(exist_ok=True)
 scores=[compose(t,i) for i,t in enumerate(TRACKS,1)];(ROOT/'scores'/'manifest.json').write_text(json.dumps(scores,indent=2)+'\n')
 for s in scores:print(s['number'],s['title'],s['endBeat']/4,'bars',round(s['endBeat']*60/s['bpm']+6,1),'seconds')
if __name__=='__main__':main()
