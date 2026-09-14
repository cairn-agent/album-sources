"""Windows Still Lit: eight independent arrangements and an original phonetic singer.
No external speech model, vocoder code, sample library, or voice bank is used.
"""
from pathlib import Path
import json, random, struct, math
ROOT=Path(__file__).resolve().parent.parent
PHONE='IY IH EH AE AH AA AO UH UW ER AX AY EY OW AW OY M N NG L R W Y S SH F TH H V Z ZH DH P T K B D G CH J'.split()
PID={p:40+i for i,p in enumerate(PHONE)}
LEX={
 'leave':'L IY V','a':'AX','light':'L AY T','on':'AA N','i':'AY','can':'K AE N','find':'F AY N D','my':'M AY','way':'W EY',
 'in':'IH N','the':'DH AX','soft':'S AO F T','rain':'R EY N','let':'L EH T','night':'N AY T','stay':'S T EY',
 'line':'L AY N','current':'K ER AX N T','flow':'F L OW','hear':'H IY R','you':'Y UW','take':'T EY K','it':'IH T','slow':'S L OW',
 'and':'AE N D','room':'R UW M','of':'AX V','blue':'B L UW','time':'T AY M','wait':'W EY T','am':'AE M','here':'H IY R','with':'W IH DH',
 'glass':'G L AE S','no':'N OW','need':'N IY D','to':'T UW','run':'R AH N','me':'M IY','till':'T IH L','morning':'M AO R N IH NG','comes':'K AH M Z',
 'step':'S T EH P','into':'IH N T UW','door':'D AO R','ajar':'AX J AA R','we':'W IY','our':'AW R','are':'AA R','where':'W EH R',
 'low':'L OW','water':'W AO T ER','moves':'M UW V Z','under':'AH N D ER','moon':'M UW N','hold':'H OW L D','sound':'S AW N D','will':'W IH L','be':'B IY','home':'H OW M','soon':'S UW N',
 'there':'DH EH R','is':'IH Z','place':'P L EY S','for':'F AO R','close':'K L OW Z','your':'Y AO R','eyes':'AY Z','through':'TH R UW','after':'AE F T ER','all':'AO L',
 'windows':'W IH N D OW Z','still':'S T IH L','lit':'L IH T','street':'S T R IY T','gone':'G AO N','quiet':'K W AY AX T','keep':'K IY P','small':'S M AO L','flame':'F L EY M','beside':'B IH S AY D','silence':'S AY L AX N S',
 'warm':'W AO R M','glow':'G L OW','turn':'T ER N','dial':'D AY AX L','not':'N AA T','far':'F AA R','now':'N AW','breathe':'B R IY DH','once':'W AH N S','more':'M AO R',
}
NAMES={0:'short kick',1:'soft clap snare',2:'closed hat',3:'open hat',4:'rim',5:'metal',6:'unused old sub',7:'held reese',8:'haze',9:'vowel ghost',10:'FM tine',11:'granular vowel',12:'folded sonar',13:'dub chord',14:'glass resonator',15:'copper acid',16:'spectral choir',17:'reed organ',18:'rain',19:'reverse breath',20:'contact click',21:'triangle pluck bass',22:'continuous sine foundation',23:'muted electric bass',24:'hollow organ bass',25:'bowed upper cloud',26:'electric piano',27:'plucked upper string',28:'breath flute',29:'shaker'}
NAMES.update({v:'singer / '+k for k,v in PID.items()})
CHORD={'m9':[0,3,7,10,14],'maj9':[0,4,7,11,14],'maj7':[0,4,7,11],'sus9':[0,5,7,10,14]}
TRACKS=[
 dict(title='Soft Return',slug='soft-return',bpm=124,root=41,key='F minor',swing=.045,voice=10,
  form=[('intro',12),('verse',20),('first',24),('break',16),('peak',32),('outro',16)],harmony=[(0,'m9'),(-4,'maj7'),(3,'maj9'),(-2,'sus9')],
  lyrics=['Leave a light on','I can find my way','In the soft rain','Let the night stay'],choruses=[32,80,96],vocalIntro=True,
  instrument='FM tines, electric-piano responses, flute; smooth eight-beat bass holds. Gentle four-beat garage.',
  description='A vocal and glass opening gives way to a grounded, warm garage groove. The bass holds beneath it.'),
 dict(title='Copper Current',slug='copper-current',bpm=128,root=40,key='E minor',swing=.018,voice=15,
  form=[('intro',8),('verse',24),('first',32),('break',16),('bridge',16),('peak',32),('outro',16)],harmony=[(0,'m9'),(0,'m9'),(-4,'maj7'),(-2,'sus9')],
  lyrics=['Stay on the line','Let the current flow','I can hear you','Take it slow'],choruses=[32,48,96,112],vocalIntro=True,
  instrument='Copper acid: the Service Tunnel oscillator with simpler eighth-note phrasing, a long filter arc and no separate bass line.',
  description='A steady machine groove, a talking acid synth, bright metallic answers and clipped sung hooks.'),
 dict(title='Blue Hour Conversation',slug='blue-hour-conversation',bpm=122,root=46,key='B-flat major',swing=.065,voice=26,
  form=[('intro',8),('verse',24),('first',16),('break',16),('bridge',16),('peak',24),('outro',16)],harmony=[(0,'maj9'),(-3,'m9'),(5,'maj9'),(7,'sus9')],
  lyrics=['You and I','In a room of blue','Time can wait','I am here with you'],choruses=[32,80,96],vocalIntro=False,
  instrument='Electric piano and muted electric-string bass with a melodic quarter-note phrase; brushed noise and a relaxed backbeat.',
  description='A brighter room, rounded keys, a walking reply from the bass and a duet that leaves room between phrases.'),
 dict(title='The Room Above the Rain',slug='the-room-above-the-rain',bpm=116,root=38,key='D minor',swing=0,voice=14,
  form=[('intro',12),('first',20),('break',16),('peak',20),('outro',12)],harmony=[(0,'m9'),(-4,'maj7'),(3,'maj9'),(5,'m9')],
  lyrics=['Rain on glass','No need to run','Stay with me','Till the morning comes'],choruses=[12,48],vocalIntro=True,
  instrument='Glass resonators, breath flute, bowed high harmonics and slow phonetic singing; no drums or bass instrument.',
  description='The quiet centre: a full song for glass, breath and a synthetic voice, with no beat to hurry it.'),
 dict(title='Landing Light',slug='landing-light',bpm=126,root=39,key='E-flat major',swing=.045,voice=17,
  form=[('intro',8),('verse',16),('first',24),('bridge',16),('break',16),('peak',32),('outro',16)],harmony=[(0,'maj9'),(5,'maj9'),(7,'sus9'),(0,'maj7')],
  lyrics=['Step into the light','Leave the door ajar','We can take our time','We are where we are'],choruses=[24,40,80,96],vocalIntro=False,
  instrument='Reed-organ chords, hollow organ bass with held roots and a rising pickup, plucked strings and shaker.',
  description='A light organ-led four-beat track, with a small ascending bass phrase and open, plainspoken lyrics.'),
 dict(title='Low Water',slug='low-water',bpm=132,root=36,key='C minor',swing=.02,voice=12,
  form=[('intro',16),('verse',24),('first',24),('break',24),('peak',24),('outro',16)],harmony=[(0,'m9'),(0,'m9'),(-4,'maj7'),(-2,'sus9')],
  lyrics=['Low water moves','Under the moon','Hold the sound','I will be home soon'],choruses=[40,88,104],vocalIntro=True,
  instrument='Slow unmodulated Reese swells and long rests, half-time backbeat, folded sonar, muted bells and a low vocal answer.',
  description='The one heavy passage: long bass pressure, sparse drums and two voices across a large empty space.'),
 dict(title='A Place to Stay',slug='a-place-to-stay',bpm=128,root=44,key='A-flat major',swing=.055,voice=16,
  form=[('intro',8),('verse',24),('first',24),('break',24),('bridge',16),('peak',32),('outro',16)],harmony=[(0,'maj9'),(5,'maj9'),(-3,'m9'),(7,'sus9')],
  lyrics=['There is a place for you','Close your eyes','Through the rain','After all this time'],choruses=[32,48,96,112],vocalIntro=False,
  instrument='Spectral choir, bright picked strings, a sparse triangle-pluck bass melody and layered sung octaves.',
  description='An open chorus and an easy two-step pulse. The choir widens while the bass leaves whole bars free.'),
 dict(title='Windows Still Lit',slug='windows-still-lit',bpm=120,root=41,key='F major',swing=.025,voice=28,
  form=[('intro',16),('first',24),('break',16),('peak',24),('outro',16)],harmony=[(0,'maj9'),(5,'maj9'),(9,'m9'),(0,'maj9')],
  lyrics=['Windows still lit','The street has gone quiet','Keep a small flame','Beside the silence'],choruses=[16,56,72],vocalIntro=True,
  instrument='Breath flute, bowed cloud, electric piano and glass; no bass line, a soft backbeat only in the middle passages.',
  description='A sung closing piece, rising from air into a gentle pulse and leaving as a voice beside the window.'),
]
LEX.update({'this':'DH IH S','has':'H AE Z'})
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
def midi(score,path):
 ppq=960;us=round(60e6/score['bpm']);chunks=[miditrack([(0,0,meta(3,score['title'])),(0,0,b'\xff\x51\x03'+us.to_bytes(3,'big')),(0,0,b'\xff\x58\x04\x04\x02\x18\x08')]+[(round(s['bar']*4*ppq),0,meta(6,s['name'])) for s in score['sections']])]
 drums={0:36,1:38,2:42,3:46,4:37,5:51,20:76,29:70}
 pitched=sorted(set(e[2] for e in score['events'] if e[2]<40 and e[2] not in drums));chs=[n for n in range(16) if n not in [9,14,15]]
 assert len(pitched)<=len(chs)
 for v in sorted(set(e[2] for e in score['events'] if e[2]<40)):
  ch=9 if v in drums else chs[pitched.index(v)];out=[(0,0,meta(3,NAMES[v]))]
  if ch!=9:out.append((0,0,bytes([192|ch,{7:38,8:89,10:4,11:54,12:98,13:90,14:10,15:80,16:91,17:19,18:122,19:95,21:38,22:38,23:33,24:19,25:48,26:4,27:24,28:73}.get(v,89)])))
  for e in score['events']:
   at,d,vv,n,g,*_=e
   if vv!=v:continue
   pitch=drums.get(v,round(n));vel=max(1,min(116,round(g*420)))
   out.extend([(round(at*ppq),1,bytes([144|ch,pitch,vel])),(round((at+d)*ppq),-1,bytes([128|ch,pitch,0]))])
  chunks.append(miditrack(out))
 for channel,part in [(14,'lead'),(15,'harmony')]:
  out=[(0,0,meta(3,'Phonetic singer / '+part)),(0,0,bytes([192|channel,54]))]
  for word in score['vocalWords']:
   if word['part']!=part:continue
   start=round(word['at']*ppq);end=round((word['at']+word['length'])*ppq);n=round(word['note'])
   out.extend([(start,0,meta(5,word['word'])),(start,1,bytes([144|channel,n,82])),(end,-1,bytes([128|channel,n,0]))])
  chunks.append(miditrack(out))
 path.write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),ppq)+b''.join(chunks))
class Song:
 def __init__(self,t,n):
  self.t=t;self.n=n;self.rng=random.Random(44401+n*913);self.events=[];self.words=[];self.lines=[];self.sections=[];self.beat=60/t['bpm'];self.root=t['root']
  bar=0
  for name,bars in t['form']:self.sections.append(dict(name=name,bar=bar,bars=bars));bar+=bars
  self.bars=bar
 def add(self,at,length,voice,note,gain,pan=0,tone=.35,motion=0,ds=0,rv=0):
  if gain<=0:return
  assert at>=0 and length>0,(self.t['title'],at,length)
  if at>=self.bars*4-.03:return
  length=min(length,self.bars*4-at-.015)
  self.events.append([round(at,6),round(length,6),voice,round(note,4),round(gain,6),round(pan,4),round(tone,4),round(motion,4),round(ds,4),round(rv,4)])
 def h(self,at):
  return max(0,at+(self.t['swing'] if abs(at%1-.5)<.02 else 0)+self.rng.uniform(-.003,.004)/self.beat)
 def harmony(self,b):
  shift,qual=self.t['harmony'][(b//4)%len(self.t['harmony'])];return self.root+shift,[self.root+12+shift+n for n in CHORD[qual]]
 def chord(self,at,notes,voice=26,length=2,gain=.036,ds=.22,rv=.32):
  for j,n in enumerate(notes):self.add(at+j*.009,length,voice,n,gain,(-.4+.2*j),.35,ds=ds,rv=rv)
 def word(self,at,length,word,note,gain=.20,pan=-.08,singer=.3,part='lead',chop=False):
  phones=LEX[word.lower()].split();vowels=[i for i,p in enumerate(phones) if PID[p]<56]
  assert vowels,word
  conslen={p:(.046 if PID[p]>=72 else .065)/self.beat for p in phones if PID[p]>=56}
  cs=sum(conslen.get(p,0) for p in phones);cs=min(cs,length*.46);rawcs=sum(conslen.values()) or 1
  durations=[(length-cs)/len(vowels) if i in vowels else conslen[p]*cs/rawcs for i,p in enumerate(phones)]
  cursor=at
  for i,(phone,dur) in enumerate(zip(phones,durations)):
   v=PID[phone];isv=v<56;level=gain*(1 if isv else .64 if v>=63 else .83)
   self.add(cursor,max(.018,dur+.004),v,note,level,pan,singer,(-.28 if isv and i==vowels[0] else 0),ds=.16 if not chop else .40,rv=.22 if part=='lead' else .44)
   cursor+=dur
  self.words.append(dict(at=at,length=length,word=word,note=note,phonemes=phones,part=part,chop=chop))
 def line(self,at,text,notes,length=8,gain=.20,part='lead',pan=-.08):
  words=text.lower().split();weights=[.60 if w in ['a','the','of','to','is','it','has'] else 1.15 if w==words[-1] else 1 for w in words];unit=(length-.35)/sum(weights);cursor=at
  self.lines.append(dict(at=at,length=length,text=text,part=part))
  for i,(word,w) in enumerate(zip(words,weights)):
   dur=w*unit;note=notes[i%len(notes)];self.word(cursor,dur-.055,word,note,gain,pan,.34 if part=='lead' else .06,part);cursor+=dur
 def vocals(self):
  t=self.t;root=self.root+24;major='major' in t['key'];third=4 if major else 3;sixth=9 if major else 8
  tunes={
   1:[[7,5,3,0],[3,5,7,5,3],[0,3,5,7],[5,3,2,0]],
   2:[[0,0,7,7],[3,3,5,2],[7,7,5,3],[2,2,0]],
   3:[[4,7,9],[7,4,2,0,2],[4,2,0],[0,2,4,7,4,2]],
   4:[[12,10,7],[7,5,3,2],[3,7,5],[5,3,2,0]],
   5:[[0,4,7,9,7],[5,4,2,0,2],[4,5,7,4,2],[2,4,7,5,4,0]],
   6:[[0,3,0],[7,5,3],[3,2,0],[0,0,3,2,0,0]],
   7:[[7,9,12,11,9,7],[9,7,4],[4,5,7],[7,4,2,0,2]],
   8:[[7,4,2],[0,2,4,5,4],[7,9,7,4],[4,2,0]]
  }[self.n]
  linebeats=12 if self.n in [4,6,8] else 8
  if self.n==6:root-=12
  for cycle,bar in enumerate(t['choruses']):
   for j,line in enumerate(t['lyrics']):
    at=bar*4+j*linebeats
    if at+linebeats>=self.bars*4:continue
    ns=[root+k for k in tunes[(j+cycle%2)%4]]
    self.line(at,line,ns,length=linebeats,gain=.18 if self.n in [4,8] else .205)
    if cycle>=1 and j in [1,3] and self.n in [1,3,5,7,8]:self.line(at+.08,line,[n-12 for n in ns],length=linebeats-.2,gain=.067,part='harmony',pan=.3)
  # Voice-led starts nod to the favourite opening; phrasing differs by track.
  if t['vocalIntro']:
   self.line(3 if self.n!=4 else 6,t['lyrics'][0],[root+7,root+third,root,root+5],length=9 if self.n in [4,8] else 7,gain=.115)
   if self.n not in [4,8]:
    self.word(20,1.3,t['lyrics'][0].split()[-1],root+7,.105,.36,chop=True)
    self.word(23,1.8,t['lyrics'][0].split()[-1],root+3,.085,-.40,chop=True)
  # On-beat lyric chops: words and syllables, with long spaces between replies.
  if self.n in [1,2,3,5,7]:
   chosen=['light','line','blue','light','stay'][[1,2,3,5,7].index(self.n)]
   for sec in self.sections:
    if sec['name'] not in ['verse','bridge','outro']:continue
    for b in range(sec['bar']+4,sec['bar']+sec['bars']-4,8):
     for j,x in enumerate([0,1,3]):self.word(b*4+x,.42 if j<2 else .9,chosen,root+[7,7,third][j],.11 if self.n==2 else .085,(-.4 if j%2 else .4),chop=True)
 def drums(self,b,kind,level=1,full=False):
  at=b*4
  if kind=='none':return
  if kind=='four':ks=[0,1,2,3];ss=[1,3]
  elif kind=='half':ks=[0] if b%4!=3 else [0,3];ss=[2]
  elif kind=='light':ks=[0,2] if b%2==0 else [0];ss=[1,3]
  else:ks=[0,2] if b%4!=3 else [0,2.5];ss=[1,3]
  for x in ks:self.add(at+x,.07,0,36,.24*level,ds=0,rv=.015)
  for x in ss:self.add(self.h(at+x),.09,1,38,.105*level,pan=-.08,tone=.15+self.n*.06,ds=.04 if self.n!=6 else .18,rv=.14 if self.n!=6 else .35)
  hats=[.5,1.5,2.5,3.5] if kind!='half' else [1,3]
  for j,x in enumerate(hats):self.add(self.h(at+x),.04,2,42,(.027 if j%2 else .032)*level,.30 if j%2 else -.25,ds=.04,rv=.05)
  if full and self.n in [1,3,5,7]:
   for x in [0,.5,1,1.5,2,2.5,3,3.5]:self.add(self.h(at+x),.07,29,70,.018*level,-.38,.4,rv=.06)
  if full and b%4==3:self.add(at+3.5,.04,4,37,.021*level,.45,ds=.17,rv=.12)
  if self.n in [2,6] and b%2==0:self.add(at+3,.08,5,51,.018,.45,.7,ds=.30,rv=.4)
 def compose(self):
  # Each arrangement has an explicit rhythm, bass, harmony and foreground recipe.
  for sec in self.sections:
   for j in range(sec['bars']):
    b=sec['bar']+j;at=b*4;scene=sec['name'];u=j/max(1,sec['bars']-1);full=scene in ['first','peak'];quiet=scene=='break';intro=scene=='intro';outro=scene=='outro'
    root,ch=self.harmony(b);fade=1-u*.8 if outro else 1
    if j%4==0:
     self.add(at,15.8,18,60,.008 if quiet or intro else .0035,.6 if b%8 else -.6,rv=.10)
    if self.n==1:
     active=not quiet and not(intro and j<8) and not(outro and j>=8)
     if active:self.drums(b,'four',.82 if intro or outro else 1,full)
     if b%4==0:self.chord(at,ch[1:],8,14,.012*fade,.07,.36)
     if active and b%2==0:self.add(at+.08,7.6,22,root,.071*fade)
     if b%2==0:
      for x,n,d in [(0,ch[2]+12,1.2),(2,ch[1]+12,.9),(4,ch[0]+12,2.2)]:self.add(at+x,d,10,n,.064*fade,pan=-.18,ds=.27,rv=.34)
     if full and b%4==2:self.chord(at+1,ch[1:4],26,1.6,.030,.2,.25)
     if scene=='peak' and b%8==4:self.add(at,6,28,ch[2]+12,.048,.3,ds=.22,rv=.42)
    elif self.n==2:
     active=not quiet and not(intro and j<4) and not(outro and j>=8)
     if active:self.drums(b,'four',1,full)
     # Acid provides the lower-mid movement; no separate bass voice.
     if not(intro and j<4) and not(outro and j>=12):
      pitches=[0,0,7,10,7,5,3,5] if b%4<2 else [0,3,7,12,10,7,5,3]
      for k in range(4 if quiet else 8):
       x=k*(1 if quiet else .5);n=root+12+pitches[k]
       self.add(at+x,.40 if not quiet else .85,15,n,.060 if quiet else .087,pan=.04,tone=.22+.45*(.5+.5*math.sin(b*.083)),motion=.15 if k==0 else 0,ds=.19,rv=.10)
     if b%8==0:self.chord(at,ch[1:],25,15,.018,.05,.50)
     if full and b%4==2:self.add(at+2,1.8,12,ch[-1]+12,.044,-.40,.45,ds=.42,rv=.3)
     if b%8==7:self.add(at+2,1.8,19,ch[2]+12,.031,.4,ds=.22,rv=.45)
    elif self.n==3:
     active=not quiet and not(intro and j<4) and not(outro and j>=8)
     if active:self.drums(b,'two',.86,full)
     if b%2==0:self.chord(at,ch,26,3.4,.033*fade,.16,.23)
     elif full:self.chord(at+2,ch[1:4],26,1.7,.028,.12,.25)
     if active:
      # A melodic bass reply, distinct from the held and sub-only arrangements.
      phrase=[(0,1.4,0),(2,1.1,7)] if b%4==0 else [(0,2.8,0)] if b%4==1 else [(0,1.7,ch[1]-ch[0]),(2,1.4,2)] if b%4==2 else [(0,1.5,0),(2,.7,-2),(3,.65,-1)]
      for x,d,n in phrase:self.add(at+x,d,23,root+n,.100*fade)
     if b%4==2:
      for k,n in enumerate([ch[2]+12,ch[1]+12,ch[0]+12]):self.add(at+k,1.1,27,n,.046*fade,.35,ds=.25,rv=.25)
     if quiet and b%4==0:self.add(at+1,5.5,28,ch[2]+12,.041,-.25,ds=.28,rv=.40)
    elif self.n==4:
     # No kick, low bass, or percussion. Phrases cross the implied grid.
     if b%4==0:self.chord(at,ch[1:],25,14,.019*fade,.08,.58)
     if b%3==0:
      for x,n,d in [(0,ch[1]+12,3.2),(2.7,ch[3]+12,2.9),(6.1,ch[2]+12,3.8)]:self.add(at+x,d,14,n,(.035 if quiet else .064)*fade,-.3 if x==0 else .3,.2,ds=.37,rv=.60)
     if b%8==4:self.add(at+1.5,7.7,28,ch[2]+12,.030*fade,.15,ds=.25,rv=.65)
     if scene=='peak' and b%4==0:self.chord(at+1,ch[1:],16,9,.018,.1,.6)
    elif self.n==5:
     active=not quiet and not(intro and j<4) and not(outro and j>=8)
     if active:self.drums(b,'four',.9,full)
     if b%2==0:self.chord(at,ch,17,2.6,.028*fade,.22,.27)
     if full and b%2==1:self.chord(at+2,ch[1:4],17,1.3,.021,.2,.3)
     if active:
      if b%4<3:self.add(at,2.7,24,root,.087*fade)
      else:
       for x,n in [(0,0),(2,2),(3,4)]:self.add(at+x,.8,24,root+n,.073*fade)
     if b%4==1:
      for x,n in [(0,ch[1]+12),(1,ch[2]+12),(2,ch[3]+12)]:self.add(at+x,1.3,27,n,.049*fade,.38,ds=.19,rv=.24)
     if quiet and b%4==0:self.add(at,7,28,ch[2]+12,.045,.2,ds=.3,rv=.45)
    elif self.n==6:
     active=not quiet and not(intro and j<12) and not(outro and j>=8)
     if active:self.drums(b,'half',.92,full)
     if b%4==0:self.chord(at,ch[1:],8,14,.012*fade,.1,.55)
     if active and b%4==0:self.add(at+.10,5.7 if not full else 9.6,7,root,.060*fade,tone=.25,ds=.03,rv=.06)
     if b%4==2:self.add(at,4.5,12,ch[0]+12,.056*fade,-.22,.2,ds=.50,rv=.45)
     if b%8==4:self.add(at+1,3.1,14,ch[3]+12,.035*fade,.36,ds=.43,rv=.48)
     if quiet and b%8==0:self.add(at,9,16,ch[2]+12,.034,pan=.1,ds=.16,rv=.60)
    elif self.n==7:
     active=not quiet and not(intro and j<4) and not(outro and j>=8)
     if active:self.drums(b,'two',1,full)
     if b%4==0:self.chord(at,ch[1:],16,12,.026*fade,.13,.46)
     if active and b%4 in [0,2]:
      for x,d,n in ([(0,1.3,0),(2,.8,7)] if b%4==0 else [(0,1.2,ch[1]-ch[0]),(1,.7,2),(2,1.0,0)]):self.add(at+x,d,21,root+n,.12*fade)
     if b%2==0:
      for x,n in [(0,ch[2]+12),(1,ch[3]+12),(2,ch[1]+12)]:self.add(at+x,1.4,27,n,.055*fade,.30,ds=.24,rv=.38)
     if full and b%4==3:self.chord(at,ch[1:4],26,2.4,.027,.16,.28)
     if quiet and b%8==0:self.add(at,10,28,ch[2]+12,.049,-.15,ds=.25,rv=.52)
    else:
     active=scene in ['first','peak'] and j>=8
     if active:self.drums(b,'light',.61,False)
     # Entire closer has no bass voice, including its short groove.
     if b%4==0:self.chord(at,ch[1:],25,14,.019*fade,.14,.5)
     if b%4==1:self.chord(at,ch[1:4],26,4.8,.024*fade,.15,.4)
     if b%4==2:self.add(at+1,6.7,28,ch[2]+12,.063*fade,.13,ds=.31,rv=.47)
     if b%8==0:
      for x,n in [(0,ch[1]+12),(3,ch[3]+12),(6,ch[2]+12)]:self.add(at+x,2.7,14,n,.040*fade,-.3 if x<4 else .3,ds=.29,rv=.53)
    if scene not in ['outro'] and j==sec['bars']-1 and self.n not in [4,8]:self.add(at+2,1.7,19,ch[2]+12,.027,.3,ds=.2,rv=.43)
  self.vocals()
  self.events.sort(key=lambda e:(e[0],e[2]));stem=f'{self.n:02d}-{self.t["slug"]}'
  score=dict(title=self.t['title'],stem=stem,number=self.n,bpm=self.t['bpm'],key=self.t['key'],endBeat=self.bars*4,seed=44110+self.n*313,engineTrack=self.n,engine='Window Engine 1 / phonetic singer',sections=self.sections,description=self.t['description'],instrument=self.t['instrument'],lyrics=self.t['lyrics'],vocalLines=self.lines,vocalWords=self.words,voices=NAMES,eventColumns=['at','length','voice','note','gain','pan','tone','motion','delay','reverb'],events=self.events)
  (ROOT/'scores'/f'{stem}.json').write_text(json.dumps(score,indent=2)+'\n')
  header=f'{self.t["bpm"]}\t{self.bars*4}\t{score["seed"]}\t{self.n}\n'
  (ROOT/'scores'/f'{stem}.tsv').write_text(header+''.join('\t'.join(map(str,e))+'\n' for e in self.events))
  # Separate vocal score supports a cappella renders without another voice engine.
  (ROOT/'scores'/f'{stem}-vocals.tsv').write_text(header+''.join('\t'.join(map(str,e))+'\n' for e in self.events if e[2]>=40))
  # Portable LRC, WebVTT and detailed lyrics are written after audio finalization
  # by export_lyrics.py, including the engine's 40 ms entrance offset.
  midi(score,ROOT/'midi'/f'{stem}.mid')
  return {k:v for k,v in score.items() if k not in ['events','voices','vocalWords','vocalLines']}
def main():
 for d in ['scores','midi','lyrics']:(ROOT/d).mkdir(exist_ok=True)
 scores=[Song(t,i).compose() for i,t in enumerate(TRACKS,1)]
 (ROOT/'scores'/'manifest.json').write_text(json.dumps(scores,indent=2)+'\n')
 (ROOT/'lyrics'/'phonemes.json').write_text(json.dumps(dict(phones=PID,lexicon=LEX),indent=2)+'\n')
 for s in scores:print(s['number'],s['title'],s['endBeat']/4,'bars',round(s['endBeat']*60/s['bpm']+6,1),'seconds')
if __name__=='__main__':main()
