"""Eight original trance compositions. Timing is in quarter-note beats.

Melodies, harmony, form, and sound design are authored here; deterministic
variation is limited to percussion dynamics, stereo position, and ornaments.
No borrowed MIDI, audio samples, or third-party musical material.
"""
from pathlib import Path
import json, math, random, struct

ROOT=Path(__file__).resolve().parent.parent
ALBUM='The Distance Turns to Light'
MINOR=[0,2,3,5,7,8,10]
MAJOR=[0,2,4,5,7,9,11]

# Each cell is one bar: (beat within bar, scale degree, held beats).
OPENING=[
 [(0,7,1.4),(1.5,9,.85),(2.5,8,.4),(3,7,.8)],
 [(0,4,.9),(1,7,.65),(1.75,8,.65),(2.5,9,1.2)],
 [(0,12,1.4),(1.5,11,.85),(2.5,9,1.2)],
 [(0,7,.65),(.75,9,.65),(1.5,12,1.3),(3,11,.8)],
 [(0,9,1.85),(2,11,.85),(3,9,.85)],
 [(0,7,.85),(1,6,.4),(1.5,7,.65),(2.25,9,1.5)],
 [(0,10,1.4),(1.5,8,.85),(2.5,6,1.2)],
 [(0,8,.85),(1,7,.85),(2,6,.65),(3.25,4,.5)],
]
TRACKS=[
 dict(title='Carrier at Midnight',slug='carrier-at-midnight',bpm=132,pc=2,mode='minor',chords=[0,5,2,6],hook=OPENING,
      form=[('intro',16),('foundation',16),('tease',16),('first',16),('break',16),('rise',8),('peak',24),('outro',16)],
      color='#7DCFE3',mood='A signal takes shape: glass pulses, a restrained lead, and the first view of the city.',bass='offbeat',lead=7),
 dict(title='Sodium Halo',slug='sodium-halo',bpm=136,pc=5,mode='minor',chords=[0,3,5,6],
      hook=[[(0,7,.4),(.75,9,.4),(1.5,11,.4),(2.25,9,.65),(3,7,.65)],
            [(0,4,.4),(.75,7,.4),(1.5,9,.65),(2.5,8,.4),(3.25,7,.5)],
            [(0,10,.65),(.75,12,.4),(1.5,14,.65),(2.5,12,.4),(3.25,10,.5)],
            [(0,12,.65),(1,10,.65),(2,7,.65),(3,10,.7)],
            [(0,12,.4),(.75,9,.4),(1.5,7,.65),(2.5,9,.4),(3.25,12,.5)],
            [(0,11,.65),(1,12,.65),(2,14,1.4)],
            [(0,13,.65),(.75,10,.65),(1.5,8,.65),(2.5,10,1.1)],
            [(0,8,.65),(1,6,.65),(2,4,.4),(2.75,6,.65),(3.5,7,.35)]],
      form=[('intro',16),('foundation',16),('tease',16),('first',32),('break',24),('rise',8),('peak',32),('outro',16)],
      color='#F4B65C',mood='Amber streetlight, short syncopated phrases, and a springy offbeat bass.',bass='offbeat',lead=7),
 dict(title='Glass Motorway',slug='glass-motorway',bpm=138,pc=8,mode='major',chords=[5,3,0,4],register=-12,
      hook=[[(0,12,.65),(.75,14,.65),(1.5,16,1.2),(3,14,.65)],
            [(0,12,.65),(1,9,.65),(2,11,.4),(2.75,12,.8)],
            [(0,10,1.25),(1.5,12,.65),(2.5,14,1.2)],
            [(0,12,.65),(.75,10,.65),(1.5,7,1.25),(3,10,.65)],
            [(0,14,1.4),(1.5,16,.85),(2.5,18,1.2)],
            [(0,16,.65),(.75,14,.65),(1.5,11,.65),(2.5,9,.4),(3.25,7,.5)],
            [(0,11,1.25),(1.5,13,.65),(2.5,15,1.2)],
            [(0,13,.65),(1,11,.65),(2,8,.65),(3,11,.65)]],
      form=[('intro',16),('foundation',32),('first',32),('break',24),('rise',8),('peak',48),('outro',16)],
      color='#9BD8CC',mood='Rolling sixteenths and a broad major-key horizon; the harmony still begins in the relative minor.',bass='rolling',lead=7),
 dict(title='A Map of the Strobe',slug='a-map-of-the-strobe',bpm=140,pc=1,mode='minor',chords=[0,0,5,6],
      hook=[[(0,7,.4),(.75,7,.4),(1.5,9,.4),(2.25,7,.4),(3,11,.65)],
            [(0,10,.4),(.75,9,.4),(1.5,7,.65),(2.5,4,.4),(3.25,6,.4)],
            [(0,7,.4),(.5,9,.4),(1.25,7,.4),(2,11,.65),(3,9,.65)],
            [(0,7,1.4),(2,6,.65),(3,4,.65)],
            [(0,12,.65),(1,9,.4),(1.75,7,.4),(2.5,9,1.1)],
            [(0,7,.4),(.75,9,.4),(1.5,12,.65),(2.5,11,.4),(3.25,9,.4)],
            [(0,10,.65),(1,8,.65),(2,6,.65),(3,8,.65)],
            [(0,10,.4),(.75,8,.4),(1.5,6,.4),(2.25,4,.4),(3,6,.7)]],
      form=[('intro',16),('foundation',32),('first',32),('break',16),('rise',16),('peak',48),('outro',16)],
      color='#E991C4',mood='The tunnel section: resonant acid, dry percussion, and a compact, insistent hook.',bass='sparse',lead=11,acid=True),
 dict(title='Where the Air Opens',slug='where-the-air-opens',bpm=136,pc=11,mode='minor',chords=[0,5,2,6],register=-12,
      hook=[[(0,14,1.8),(2,16,1.6)],[(0,18,1.35),(1.5,16,.85),(2.5,14,1.2)],
            [(0,16,2.5),(3,19,.7)],[(0,18,1.4),(1.5,16,1.85)],
            [(0,16,1.4),(1.5,18,.85),(2.5,20,1.2)],[(0,18,1.8),(2,16,.65),(3,14,.65)],
            [(0,17,1.4),(1.5,15,.85),(2.5,13,1.2)],[(0,15,1.35),(1.5,13,1.1),(3,11,.7)]],
      form=[('intro',16),('foundation',16),('first',24),('break',32),('rise',8),('peak',48),('outro',16)],
      color='#BEADF1',mood='A suspended glass melody, the longest quiet space so far, then the pulse returns underneath it.',bass='offbeat',lead=10),
 dict(title='Held Above the City',slug='held-above-the-city',bpm=140,pc=4,mode='minor',chords=[0,5,2,6],
      hook=[[(0,7,.65),(.75,9,.65),(1.5,11,1.2),(3,14,.65)],
            [(0,13,.65),(.75,11,.65),(1.5,9,.65),(2.25,11,1.4)],
            [(0,12,1.25),(1.5,14,.65),(2.5,16,1.2)],
            [(0,14,.65),(.75,12,.65),(1.5,9,1.2),(3,12,.65)],
            [(0,16,1.4),(1.5,14,.85),(2.5,11,1.2)],
            [(0,9,.65),(.75,11,.65),(1.5,14,.65),(2.5,16,1.2)],
            [(0,17,1.4),(1.5,15,.85),(2.5,13,1.2)],
            [(0,15,.65),(.75,13,.65),(1.5,10,.65),(2.5,8,.4),(3.25,6,.45)]],
      form=[('intro',16),('foundation',32),('first',32),('break',32),('rise',16),('peak',48),('outro',16)],
      color='#F0D18D',mood='The summit: a long melodic ascent, an almost empty breakdown, and a full-width final statement.',bass='offbeat',lead=7),
 dict(title='The Last Train Is a Satellite',slug='the-last-train-is-a-satellite',bpm=142,pc=9,mode='minor',chords=[0,6,5,6],register=-12,
      hook=[[(0,14,.4),(.5,14,.4),(1.25,16,.4),(2,18,.65),(3,16,.65)],
            [(0,14,.4),(.75,11,.4),(1.5,14,.65),(2.5,16,1.1)],
            [(0,17,.4),(.5,17,.4),(1.25,15,.4),(2,13,.65),(3,15,.65)],
            [(0,17,.65),(.75,15,.65),(1.5,13,.65),(2.5,10,1.1)],
            [(0,19,.4),(.75,16,.4),(1.5,14,.65),(2.5,16,1.1)],
            [(0,19,.65),(1,21,.65),(2,19,.65),(3,16,.65)],
            [(0,20,.65),(.75,17,.65),(1.5,15,.65),(2.5,13,1.1)],
            [(0,15,.4),(.5,13,.4),(1.25,10,.4),(2,13,.65),(3,11,.65)]],
      form=[('intro',16),('foundation',32),('first',32),('break',16),('rise',16),('peak',48),('outro',16)],
      color='#F1977B',mood='The fastest passage: clipped leads, rolling bass, and a second crest with gated formants.',bass='rolling',lead=7,acid=True),
 dict(title='Daybreak, Without an Answer',slug='daybreak-without-an-answer',bpm=132,pc=2,mode='major',chords=[0,4,5,3],
      hook=OPENING,
      form=[('intro',16),('foundation',16),('first',32),('break',32),('rise',8),('peak',40),('outro',16)],
      color='#F4C7BB',mood='The opening signal returns in major, warms into a final dance, and leaves as glass and air.',bass='offbeat',lead=7),
]

def vlq(n):
    b=[n&127]
    while n>>7:
        n>>=7;b.insert(0,(n&127)|128)
    return bytes(b)
def meta(kind,s):
    s=s.encode();return bytes([255,kind])+vlq(len(s))+s
def miditrack(events):
    events.sort(key=lambda x:(x[0],x[1]));out=bytearray();last=0
    for tick,order,b in events:out+=vlq(tick-last)+b;last=tick
    out+=b'\x00\xff\x2f\x00';return b'MTrk'+struct.pack('>I',len(out))+out
def midi(score,path):
    ppq=480;us=round(60e6/score['bpm'])
    mt=[(0,0,meta(3,score['title'])),(0,0,b'\xff\x51\x03'+us.to_bytes(3,'big')),(0,0,b'\xff\x58\x04\x04\x02\x18\x08')]
    mt += [(round(s['bar']*4*ppq),0,meta(6,s['name'])) for s in score['sections']]
    chunks=[miditrack(mt)]
    names=['kick','clap','closed hat','open hat','snare','ride','pulse bass','seven-saw lead','resonant acid','horizon pad','FM glass','envelope pluck','noise lift','impact','gated formants']
    pitches=[36,39,42,46,38,51];programs={6:38,7:81,8:80,9:89,10:10,11:81,12:103,13:119,14:91}
    for v in range(15):
        es=[e for e in score['events'] if e[2]==v]
        if not es:continue
        ch=9 if v<=5 else (v-6 if v<=14 else 8)
        out=[(0,0,meta(3,names[v]))]
        if v>5:out.append((0,0,bytes([192|ch,programs[v]])))
        for at,dur,voice,note,gain,pan,tone,motion in es:
            n=pitches[v] if v<6 else round(note);vel=max(1,min(120,round(gain*155)))
            out.append((round(at*ppq),1,bytes([144|ch,n,vel])))
            out.append((round((at+dur)*ppq),-1,bytes([128|ch,n,0])))
        chunks.append(miditrack(out))
    path.write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),ppq)+b''.join(chunks))

def make(t,number):
    rng=random.Random(1998+number*271);sc=MINOR if t['mode']=='minor' else MAJOR;root=60+t['pc'];events=[];sections=[]
    def pitch(deg):return root+12*(deg//7)+sc[deg%7]
    def add(at,length,voice,note,gain,pan=0,tone=.65,motion=0):
        if gain>.0001:events.append([round(at,6),round(length,6),voice,note,round(gain,5),round(pan,4),round(tone,4),round(motion,4)])
    bar=0
    for scene,count in t['form']:
        start=bar;sections.append(dict(name=scene,bar=bar,bars=count))
        for local in range(count):
            b=bar+local;at=b*4;u=local/max(1,count-1);ch=t['chords'][(b//2)%4]
            full=scene in ['first','peak'];quiet=scene=='break';rising=scene in ['rise','tease'];outro=scene=='outro';intro=scene=='intro'
            # Eight-bar blocks breathe; rises suspend the kick before the return.
            kick=not quiet and not (intro and local<8) and not (scene=='rise' and local>=count-4)
            if outro and local>=count-8:kick=False
            if full and local%16==15:kick=True
            energy=.4 if intro else .76 if scene in ['foundation','tease'] else 1. if full else .35 if quiet else .5+.4*u if rising else 1-u*.75
            for beat in range(4):
                if kick and not (full and local%16==15 and beat==3):add(at+beat,.10,0,36,.64 if full else .59)
                if kick and (not intro or local>=12) and beat in [1,3]:add(at+beat,.10,1,39,.32 if full else .27,0)
                if kick and (full or scene in ['foundation','tease','rise']):
                    add(at+beat+.5,.10,3,46,.12 if full else .095,.2)
                    for off in [.25,.75]:add(at+beat+off,.05,2,42,(.047 if off==.25 else .061)*rng.uniform(.88,1.12),-.25)
                if full and scene=='peak' and local>=16:add(at+beat+.5,.1,5,51,.046,.37)
            if intro and local>=4:
                for beat in [0,1,2,3]:add(at+beat+.5,.05,2,42,.055,-.2)
            if full and local%8==7:
                for j in range(4):add(at+3+j*.25,.07,4,38,.075+j*.022,(-1)**j*.12)
            # Bass pattern differs by composition; the sub register stays centered.
            hasbass=not quiet and not (intro and local<8) and not (outro and local>=count-8) and not (scene=='rise' and local>=count-4)
            if hasbass:
                br=pitch(ch)-24
                if br>=48:br-=12
                positions=[.5,1.5,2.5,3.5] if t['bass']=='offbeat' else [.5,.75,1.5,1.75,2.5,2.75,3.5,3.75] if t['bass']=='rolling' else [.5,1.5,2.5,3.25,3.5]
                for j,off in enumerate(positions):
                    n=br+(12 if t['bass']=='rolling' and j%4==3 else 0)
                    add(at+off,.31 if t['bass']=='offbeat' else .16,6,n,.37 if j%2==0 else .31,0,.28 if t['bass']=='sparse' else .39)
            # Slow chord bed, voiced below the hook. It thins during busy passages.
            padon=(b%2==0) and not (outro and local>count-8)
            if padon:
                pg=.063 if quiet else .048 if full else .042
                for j,d in enumerate([ch,ch+2,ch+4,ch+7]):add(at,7.7,9,pitch(d)-12,pg,[-.55,-.18,.18,.55][j],.25 if quiet else .4)
            if intro and local==0:
                # An audible carrier from the first moment, before the drum entrance.
                add(at,2.5,10,pitch(7)+t.get('register',0),.11,-.15,.3)
                add(at+2.75,1.2,10,pitch(11)+t.get('register',0),.075,.2,.35)
            # Arpeggio cells: evolving voicing, filter, and gaps instead of one all-album loop.
            arpon=(not quiet or local>=count//2) and not (intro and local<4) and not (outro and local>=count-4)
            if arpon:
                pat=([0,4,2,7,4,9,2,4] if number in [1,5,8] else [0,2,4,7,9,7,4,2] if number in [2,6] else [0,7,4,2,7,4,9,4])
                density=.5 if number in [1,5,8] else .25
                for j in range(round(4/density)):
                    if scene=='break' and j%2:continue
                    d=ch+pat[(j+(4 if (b//8)%2 else 0))%8]
                    tone=.2+.55*u if rising or intro else .62 if full else .28
                    add(at+j*density,.15,11,pitch(d),(.085 if full else .073)*(.5 if quiet else 1),-.22 if j%2 else .22,tone)
            if t.get('acid') and (scene in ['foundation','first','peak','rise'] or (outro and local<8)):
                acidpat=[0,0,7,0,2,0,4,7,0,0,3,0,7,4,2,7]
                for j,d in enumerate(acidpat):
                    if j in [3,11] and b%2==0:continue
                    n=pitch(ch+d)-24
                    tone=.22+.55*((b%16)/15) if scene!='rise' else .2+.75*u
                    add(at+j*.25,.20 if j%4 else .34,8,n,.095 if number==7 else .14,0,tone,1 if j%4==0 else -.5)
            # Main phrases enter in different ways, with actual rests and cadences.
            leadon=full or (scene=='tease' and local>=count-8) or (quiet and local>=8 and local<count-4) or (scene=='rise' and local<count-2)
            if number==1 and intro and local>=8:leadon=True
            if number==8 and (intro or (outro and local>=4)):leadon=True
            if leadon:
                cell=t['hook'][b%8]
                voice=t['lead'] if full else 10 if quiet or intro or outro else 11
                gain=.60 if voice==7 else .30 if voice==10 else .32
                if quiet or intro or outro:gain=.13 if voice==10 else .16
                if scene=='tease':gain=.21
                if scene=='peak' and number==5 and local>=16:voice=7;gain=.38
                for j,(off,deg,length) in enumerate(cell):
                    if quiet and local<count//2 and j>1:continue
                    if scene=='rise' and local>=count-4 and off>1.5:continue
                    nn=pitch(deg)+t.get('register',0)
                    if scene=='peak' and local>=32 and b%8==7 and j==len(cell)-1:nn=pitch(7)+t.get('register',0);length=.64
                    duration=length*(.74 if number==7 and full else 1)
                    tone=.86 if scene=='peak' else .70 if full else .3+.5*u if rising else .35
                    add(at+off,duration,voice,nn,gain*(1 if j==0 else .94),0,tone,.4)
                # Sparse glass counterline above the returning statement.
                if scene=='peak' and local>=16 and b%2==1:
                    for off,d in [(1.5,ch+11),(3.25,ch+9)]:add(at+off,.45,10,pitch(d)+t.get('register',0),.082,.28,.5)
            if scene=='peak' and local>=16 and number in [3,6,7] and b%2==0:
                for d in [ch+2,ch+4]:add(at,7.65,14,pitch(d),.055,0,.6)
            if scene=='rise':
                step=.5 if u<.5 else .25 if u<.85 else .125
                for j in range(round(4/step)):
                    if local==count-1 and j*step>=3.5:continue
                    add(at+j*step,.06,4,38,.075+.16*u,0,.3+.6*u)
            if outro and local>=count-8 and b%2==0:
                for j,d in enumerate([ch+7,ch+9,ch+11]):add(at+j*.75,1.3,10,pitch(d)+t.get('register',0),.095*(1-u*.65),-.3+j*.3,.4)
        if scene in ['first','peak']:
            add(start*4,3,13,36,.30,0);add(start*4,7,12,60,.13,.2,.6,-1)
        if scene=='rise':add(start*4,count*4-.5,12,60,.17,0,.8,1)
        if scene in ['tease','foundation'] and count>=16:add((start+count-4)*4,15.5,12,60,.065,0,.5,1)
        bar+=count
    # A thin, deliberately different ending for the closing piece.
    if number==8:
        for j,d in enumerate([7,9,11,14]):add(bar*4-8+j*1.5,1.8,10,pitch(d),.07,(-1)**j*.25,.4)
    events.sort(key=lambda e:(e[0],e[2]))
    keyname=('C#' if t['pc']==1 and t['mode']=='minor' else ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B'][t['pc']])+' '+t['mode']
    return dict(title=t['title'],number=number,slug=t['slug'],album=ALBUM,artist='Cairn',bpm=t['bpm'],meter=[4,4],key=keyname,bars=bar,endBeat=bar*4,seed=19982002+number,sections=sections,description=t['mood'],color=t['color'],eventFields=['at','len','voice','note','gain','pan','tone','motion'],events=events)

def main():
    for d in ['scores','midi','wav','mp3','checks','art','work']:(ROOT/d).mkdir(parents=True,exist_ok=True)
    manifests=[]
    for number,t in enumerate(TRACKS,1):
        s=make(t,number);stem=f'{number:02d}-{t["slug"]}';s['stem']=stem
        (ROOT/'scores'/f'{stem}.json').write_text(json.dumps(s,indent=2)+'\n')
        with (ROOT/'scores'/f'{stem}.tsv').open('w') as out:
            out.write(f'{s["bpm"]} {s["endBeat"]} {s["seed"]}\n')
            for e in s['events']:out.write(' '.join(map(str,e))+'\n')
        midi(s,ROOT/'midi'/f'{stem}.mid')
        manifests.append({k:v for k,v in s.items() if k!='events'})
        print(number,t['title'],s['bars'],'bars,',len(s['events']),'events',flush=True)
    (ROOT/'scores'/'manifest.json').write_text(json.dumps(manifests,indent=2)+'\n')

if __name__=='__main__':main()
