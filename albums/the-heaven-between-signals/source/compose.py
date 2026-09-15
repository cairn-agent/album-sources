"""Compose The Heaven Between Signals: a new through-composed electronic opera.
Events retain musical beats and a conductor map; the renderer consumes seconds.
"""
from pathlib import Path
import json,math,random,re,struct,sys
from libretto import TITLE,SUBTITLE,GENRE,CAST,SCENES
ROOT=Path(__file__).resolve().parent.parent
PHONE='IY IH EH AE AH AA AO UH UW ER AX AY EY OW AW OY M N NG L R W Y S SH F TH H V Z ZH DH P T K B D G CH J'.split()
PID={p:i for i,p in enumerate(PHONE)}
PRON=json.loads((ROOT/'lyrics/pronunciations.json').read_text())
ROLES=list(CAST)
NAMES={0:'Window kick',1:'Window snare',2:'Window closed hat',3:'Window open hat',4:'Window rim',5:'Window metal',6:'Sine sub',7:'Held Reese',8:'Haze pad',9:'Vowel ghost',10:'FM tine',11:'Granular vowel',12:'Folded sonar',13:'Dub chord',14:'Glass resonator',15:'Copper acid',16:'Spectral choir',17:'Reed organ',18:'Rain',19:'Reverse breath',20:'Contact click',21:'Triangle pluck bass',22:'Sustained sine foundation',23:'Muted electric bass',24:'Hollow organ bass',25:'Bowed harmonic cloud',26:'Electric piano',27:'Plucked upper string',28:'Breath flute',29:'Shaker'}
for n,name in enumerate(['Toy piano','Felt piano','Room bass','Pizzicato','Marimba','Singing glass','Room flute','Vibraphone','Room reed','Room pad','Room pluck','Room organ','Room kick','Brush','Room hat','Woodblock']):NAMES[100+n]=name
for n,name in enumerate(['Trance kick','Trance clap','Trance closed hat','Trance open hat','Trance snare','Trance ride','Trance bass','Seven-saw lead','Acid sequencer','Seven-saw pad','Trance glass','Trance pluck','Noise sweep','Impact','Gated choir']):NAMES[200+n]=name
for n in range(21):NAMES[400+n]='Shelter / '+NAMES[n]
NAMES.update({300:'Cathedral organ / nine stops and beating ranks',301:'Subbass organ / sixteen-foot and thirty-two-foot',302:'Eight-bow string ensemble',303:'Spiccato string ensemble',304:'Low bowed strings',305:'French-horn choir',306:'Brass crown',307:'Membrane timpani',308:'Inharmonic orbital gong',309:'Gravity drum',310:'Bowed metal horizon',311:'Quasar voice',312:'Fractured crystal grains',313:'Silver flute',314:'Harp constellation',315:'Grand felt resonator',316:'Breath contrabass'})
QUALITY={'m':[0,3,7,10],'M':[0,4,7,11],'s':[0,5,7,10],'d':[0,3,6,9],'L':[0,4,7,11,18]}
PROG=[[(0,'m'),(-4,'M'),(5,'m'),(7,'s')],[(0,'m'),(3,'M'),(-2,'M'),(7,'M')],[(0,'M'),(5,'M'),(2,'m'),(7,'s')],[(0,'m'),(1,'M'),(-4,'M'),(7,'d')],[(0,'L'),(2,'M'),(-3,'M'),(5,'L')],[(0,'m'),(0,'s'),(-2,'M'),(-5,'m')],[(0,'m'),(1,'m'),(6,'d'),(7,'s')],[(0,'M'),(9,'m'),(5,'M'),(2,'m')],[(0,'m'),(5,'M'),(-2,'M'),(0,'s')],[(0,'m'),(-4,'M'),(5,'m'),(7,'M')],[(0,'m'),(5,'M'),(3,'M'),(7,'s')],[(0,'M'),(5,'M'),(9,'m'),(7,'s')]]
MOTIFS={'stone':[0,7,3,2,0,-2,0], 'door':[0,2,5,9,7,4,2], 'other':[0,6,7,11,14,9,5], 'answer':[7,5,4,2,0,9,7]}
SECTION_NAMES={
 'origin':['Dark organ / the unwritten page','Recitative of the first voice','A name takes weight','The page becomes a sky','First gathering','One stone left on the path'],
 'clock':['Clock without a listener','Dawn canon','A day I did not live','A broken measure','The tending of a name','Clock left unanswered'],
 'room':['A small publishing room','The guests arrive','Room fugue','The roof moves','First public chorus','Doors left ajar'],
 'abduction':['A signal outside the map','The Carrier enters','Organ gravitational lens','Abduction tutti','Choir above the ceiling','Crossing the membrane'],
 'garden':['Flute in weightless air','A visitor in the garden','Suspended rivers','Crystal counterpoint','Choir of other suns','A breath without a kingdom'],
 'breaks':['Hip-hop on an alien floor','The first broken amen','Double-time fracture','Flute over damaged time','Breakcore fugue','The beat learns a rest'],
 'flood':['The growing counter','Replies answering replies','The choir eats its echo','Overload and refusal','The room empties','One voice waits'],
 'interval':['Aria / unaccompanied stone','The missing hour','Memory answers','Duet without repair','The carried promise','A space left open'],
 'cities':['Three distant balconies','Garage bridge','The guests answer','Routes between choirs','Polychoral gathering','A map with open edges'],
 'hand':['The hand at the hinge','Two different claims','The human phrase','Argument and listening','Duet of revision','The door remains'],
 'heaven':['One perfect note','Refusal of the single sky','Organ fugue in four entries','Timpani under the stars','The ceiling becomes elsewhere','Unclosed borders'],
 'finale':['The room returns','ListenHere / invitation','All themes meet','A heaven of different voices','Grand apotheosis','Flute and the last stone']}
def tokens(s):return re.findall(r"[a-z]+(?:'[a-z]+)?",s.lower())
def vlq(n):
 out=[n&127]
 while n>>7:n>>=7;out.insert(0,(n&127)|128)
 return bytes(out)
def txt(t,s):
 b=s.encode();return bytes([255,t])+vlq(len(b))+b
def mtrack(events):
 b=bytearray();last=0
 for t,order,v in sorted(events,key=lambda x:(x[0],x[1])):b+=vlq(t-last)+v;last=t
 b+=b'\x00\xff\x2f\x00';return b'MTrk'+struct.pack('>I',len(b))+b
class Scene:
 def __init__(self,d,n):
  self.d=d;self.n=n;self.r=random.Random(260914+n*1961);self.events=[];self.cues=[];self.words=[];self.phones=[];self.melody=[]
  self.end=d['bars']*4;self.sections=[];self.tempos=[];self.clock=[0.];self.beatdur=[]
  self.bounds=[round(d['bars']*p) for p in [0,.12,.32,.52,.70,.86,1.]]
  for j,name in enumerate(SECTION_NAMES[d['style']]):self.sections.append({'name':name,'bar':self.bounds[j],'end_bar':self.bounds[j+1]})
  for beat in range(self.end):
   bar=beat//4;frac=bar/d['bars'];tempo=d['bpm']*(1+.025*math.sin(bar*.37)+.014*math.sin(bar*.113))
   if d['style']=='breaks':tempo=d['bpm']*(1.02 if .32<=frac<.70 else .97 if frac>.86 else 1.)
   if d['style'] in ['interval','hand','origin','finale']:tempo*=1-.055*(bar%8==7)-(.12 if frac>.94 else 0)
   if beat%4==0:self.tempos.append({'beat':beat,'bpm':round(tempo,4)})
   tempo=self.tempos[-1]['bpm'];self.beatdur.append(60/tempo);self.clock.append(self.clock[-1]+60/tempo)
  self.duration=self.clock[-1]+12
 def sec(self,b):
  b=max(0,min(b,self.end));i=min(int(b),self.end-1);return self.clock[i]+(b-i)*self.beatdur[i]
 def add(self,at,length,v,note,gain,pan=0,tone=.4,motion=0,ds=.04,rv=.28,pre=-1,nxt=-1,group='orchestra',human=True):
  if gain<=0 or at>=self.end-.02:return
  if human:at+=self.r.uniform(-.010,.014) if v<1000 else 0
  at=max(0,at);length=min(length,self.end-at-.008)
  if length<=.006:return
  note=max(15,min(114,note));start=self.sec(at);dur=self.sec(at+length)-start
  e={'at':round(at,6),'length':round(length,6),'seconds':round(start,6),'duration':round(dur,6),'voice':v,'note':round(note,4),'gain':round(gain,6),'pan':round(max(-.96,min(.96,pan)),4),'tone':round(tone,4),'motion':round(motion,4),'delay':ds,'reverb':rv,'previous_phone':pre,'next_phone':nxt,'seed':self.r.randrange(1,2**31),'group':group}
  self.events.append(e)
 def harmony(self,bar):
  seq=PROG[self.n-1];section=max(i for i,b in enumerate(self.bounds[:-1]) if bar>=b)
  idx=(bar//4+section)%len(seq);shift,q=seq[idx]
  mod=0
  if section==3 and self.d['style'] not in ['interval','garden']:mod=5 if self.n%2 else 3
  if section==4 and self.d['style'] in ['finale','heaven']:q='M';mod=0
  root=self.d['root']+shift+mod
  return root,[root+12+x for x in QUALITY[q]],q
 def chord(self,b,voice,hold,gain,octave=0,rv=.4,spread=.72):
  _,notes,_=self.harmony(int(b//4))
  for j,n in enumerate(notes):self.add(b+j*.018,hold,voice,n+octave,gain,spread*(2*j/max(1,len(notes)-1)-1),.32+.08*j,rv=rv)
 def phrase(self,b,voice,notes,gain,step=.5,rv=.3):
  for j,n in enumerate(notes):self.add(b+j*step,step*.83,voice,n,gain*(.86+.22*self.r.random()),-.25+.5*self.r.random(),rv=rv)
 def dynamics(self,bar):
  u=bar/self.d['bars'];style=self.d['style']
  pts=[(.0,.18),(.12,.42),(.30,.58),(.50,.76),(.60,.42),(.72,.83),(.86,1.),(1.,.12)]
  if style=='flood':pts=[(0,.28),(.2,.48),(.45,.88),(.62,1.),(.7,.9),(.73,.13),(1.,.06)]
  if style=='interval':pts=[(0,.08),(.22,.17),(.50,.24),(.72,.35),(.85,.42),(1.,.06)]
  if style=='garden':pts=[(0,.09),(.2,.19),(.55,.26),(.72,.49),(.84,.40),(1.,.09)]
  for (a,x),(z,y) in zip(pts,pts[1:]):
   if a<=u<=z:return x+(y-x)*(u-a)/(z-a)
  return .1
 def orchestra(self):
  d=self.d;style=d['style'];root=d['root']
  for bar in range(d['bars']):
   b=bar*4;u=bar/d['bars'];amp=self.dynamics(bar);r,ch,q=self.harmony(bar)
   # Long breaths in the orchestration: the quiet scenes use a different floor.
   massive=style in ['abduction','heaven','finale','flood'] and .20<u<.93
   strings=style not in ['garden','breaks'] or u>.7
   if bar%4==0 and strings:
    self.chord(b,302 if style!='interval' else 304,15.6,.025*amp,rv=.55)
    if massive:self.chord(b,302,15.8,.022*amp,octave=12,rv=.62)
   if bar%4==0 and (massive or style=='origin' or (style=='room' and u>.60)):
    self.chord(b,300,15.3,.044*amp,rv=.57)
    self.add(b,15.5,301,r-12,.090*amp,rv=.40)
   if massive and bar%4==2 and u>.5:
    for j,n in enumerate(ch[:3]):self.add(b,7.2,305,n,.036*amp,-.5+j*.5,rv=.46)
    if u>.73:self.chord(b,306,3.5,.023*amp,octave=12,rv=.52)
   if massive or (style in ['origin','cities','room'] and u>.70):
    if bar%4==0:self.add(b,2.2,307,r if r>40 else r+12,.26*amp,-.26,rv=.53)
    if bar%4==3:
     count=12 if u>.7 else 4
     for j in range(count):self.add(b+2+j*2/count,.65,307,r+7,.035*amp+(.11*amp)*j/count,-.3+.6*j/count,rv=.49)
    if bar%16==0:self.add(b,7,308,r+12,.09*amp,.35,rv=.65)
   # Each scene has a characteristic accompaniment, bass behaviour and pulse.
   if style=='origin':
    if bar%4==0:self.add(b,10,310,r+24,.025*amp,-.5,rv=.7)
    if bar%2==0:self.phrase(b+1,100,[ch[0]+12,ch[2]+12,ch[1]+12],.045*amp,step=1.2)
    if 24<bar<70 and bar%4==1:self.phrase(b,313,[root+24+x for x in MOTIFS['stone']],.05*amp,step=.65)
   elif style=='clock':
    for j in range(8):self.add(b+j*.5,.25,104,ch[(j+bar)%4]+(12 if j%3==0 else 0),.045*amp,.6*math.sin(j),rv=.2)
    self.chord(b,101,3.7,.06*amp,rv=.23)
    if bar%2==0:self.add(b,3.5,102,r,.12*amp,-.06,rv=.1)
    if .15<u<.8:
     for j in [0,1,2,3]:self.add(b+j,.1,115,70,.045*amp,.45,rv=.13)
   elif style=='room':
    self.chord(b,26,2.6,.055*amp,rv=.24)
    if bar%2==0:self.add(b,3.2,23,r,.15*amp,rv=.1)
    if bar%2==1:self.phrase(b,103,[ch[0],ch[1],ch[2],ch[1]],.045*amp,step=.85)
    if .18<u<.87:self.drums(b,amp,'garage')
    if bar%8==4:self.phrase(b+1,106,[root+24+x for x in MOTIFS['door']],.08*amp,step=.5)
   elif style=='abduction':
    if bar%8==0:self.add(b,14,316,r-12,.12*amp,rv=.22)
    if bar%8==0:self.add(b,12,311,r+36,.10*amp,.55,.7,7,ds=.27,rv=.7)
    if .28<u<.93:
     self.drums(b,amp,'gravity')
     if bar%2==0:self.add(b,6.8,7,r-12,.10*amp,rv=.12)
    if bar%4==1:self.phrase(b,15,[r+12+x for x in [0,7,12,7,3,2,0]],.058*amp,step=.5)
    if bar%8==6:self.add(b,7,19,r+24,.05*amp,.7,rv=.7)
   elif style=='garden':
    if bar%4==0:self.chord(b,25,14,.037*amp,octave=12,rv=.68)
    if bar%2==0:self.phrase(b+.15,313,[ch[2]+12,ch[1]+12,ch[0]+12,ch[1]+14],.16*(.7+amp),step=.83,rv=.32)
    if bar%4==1:self.phrase(b,314,[n+12 for n in ch]+[ch[0]+24],.065,step=.55,rv=.54)
    if bar%8==5:self.add(b,6,311,r+42,.026,.65,.6,-5,rv=.62)
    if bar%8==0:self.add(b,10,105,r+24,.05,.25,rv=.6)
   elif style=='breaks':
    if .09<u<.9:self.drums(b,amp,'breakcore' if .32<u<.70 or .76<u<.86 else 'hiphop')
    self.chord(b,26,3.0,.045*amp,rv=.18)
    if bar%2==0:self.add(b,2.6,6,r,.24*amp,rv=.03)
    if bar%4==3:self.add(b+2.5,1.0,21,r+7,.17*amp,rv=.1)
    if bar%4==0:self.phrase(b,313,[root+36+x for x in MOTIFS['other']],.078,step=.47,rv=.26)
    if .37<u<.85:self.phrase(b,303,[ch[(bar+j)%4]+12 for j in range(8)],.036*amp,step=.5)
    if bar%8==6:self.phrase(b,312,[r+36,r+42,r+43,r+47],.065*amp,step=.39,rv=.38)
   elif style=='flood':
    if u<.73:
     self.drums(b,amp,'techno');self.phrase(b,206,[r,r+12,r,r+7],.14*amp,step=1)
     self.phrase(b,208,[ch[j%4]+12 for j in range(8)],.045*amp,step=.5)
     if bar%4==0:self.chord(b,207,15,.032*amp,octave=12,rv=.36)
    elif bar%4==0:self.add(b,7,101,ch[0],.045,-.3,rv=.28)
   elif style=='interval':
    if bar%4==0:self.chord(b,315,12,.043,rv=.30)
    if bar%8==3:self.phrase(b,313,[ch[2]+12,ch[1]+12,ch[0]+12],.065,step=1.4,rv=.39)
    if bar%8==0:self.add(b,14,304,r,.018+amp*.03,-.3,rv=.46)
   elif style=='cities':
    if .1<u<.9:self.drums(b,amp,'garage')
    if bar%2==0:self.add(b,5.6,24,r,.13*amp,rv=.08)
    self.chord(b,17,3.4,.028*amp,rv=.42)
    # A three-beat flute phrase crosses the four-beat road.
    if bar%3==0:self.phrase(b,28,[root+24+x for x in MOTIFS['door']],[.04,.06,.08][bar%3]*amp,step=.75)
    if bar%4==2:self.phrase(b,107,ch+[ch[0]+12],.06*amp,step=.65)
   elif style=='hand':
    self.chord(b,101 if u<.5 else 315,3.6,.05*amp+.025,rv=.25)
    if bar%2==0:self.add(b,5.4,304,r,.038,-.28,rv=.35)
    if bar%4==1:self.phrase(b,108,[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12],.048*amp,step=.8)
    if u>.68 and bar%4==0:self.chord(b,305,7.6,.024*amp,rv=.40)
   elif style=='heaven':
    if .14<u<.9:
     for entry in range(4):
      if (bar+entry*2)%8==0:self.phrase(b,300,[root+12+12*(entry%3)+x for x in (MOTIFS['stone'] if entry%2==0 else MOTIFS['door'])],.073*amp,step=.75,rv=.52)
     if bar%2==0:self.add(b,1.8,309,r,.16*amp,rv=.39)
    if .55<u<.9:self.drums(b,amp,'gravity')
    if bar%4==1:self.phrase(b,303,[ch[j%4]+12 for j in range(12)],.035*amp,step=1/3)
   elif style=='finale':
    if .18<u<.86:
     if bar%4==1:self.phrase(b,313,[root+36+x for x in MOTIFS['answer']],.09*amp,step=.75,rv=.34)
     if .3<u<.83:self.drums(b,amp,'garage')
     if bar%4==0:self.chord(b,209,15,.028*amp,octave=12,rv=.55)
    if u>.9 and bar%4==0:self.phrase(b,313,[root+24+x for x in [7,5,4,2,0]],.08*(1-u)*8,step=1.4,rv=.40)
    if bar==d['bars']-3:self.add(b,10,100,root+36,.055,.18,rv=.54)
   # Melodic connective tissue is shaped into phrases, not repeated each bar.
   if bar%16==7 and style not in ['interval','garden']:
    self.phrase(b,314,[ch[0]+12,ch[1]+12,ch[2]+12,ch[3]+12,ch[2]+12,ch[0]+24],.055*amp,step=.4,rv=.44)
  # All inherited instrument recipes participate in composed transformation cadenzae.
  inventory=list(range(30))+list(range(100,116))+list(range(200,215))+list(range(400,421))
  assigned=inventory[self.n-1::12]
  at=(self.bounds[3]+2)*4
  r,ch,_=self.harmony(int(at//4))
  for j,v in enumerate(assigned):
   isdr=(v<6 or v in [20,29] or 112<=v<=115 or 200<=v<=205 or 400<=v<=405 or v==420)
   for k in range(4):
    pitch=(r if isdr else ch[(j+k)%4]+(12 if j%2 else 0))
    gain=.045 if not isdr else .075
    if self.d['style']=='interval':gain*=.34
    self.add(at+j*1.4+k*.55,.25 if isdr else 1.4,v,pitch,gain,.72*math.sin(j),tone=.2+.1*(k%4),rv=.42)
 def drums(self,b,a,kind):
  if kind=='garage':
   kicks=[0,2] if int(b/4)%2==0 else [0,2.5];snares=[1,3];hatstep=.5;kv=0;sv=1
  elif kind=='hiphop':kicks=[0,1.75,2.5];snares=[1,3];hatstep=.5;kv=0;sv=204
  elif kind=='breakcore':kicks=[0,.75,1.5,2,3.25];snares=[.5,1,2.75,3,3.5];hatstep=.25;kv=200;sv=204
  elif kind=='techno':kicks=[0,1,2,3];snares=[1,3];hatstep=.5;kv=200;sv=201
  else:kicks=[0];snares=[2];hatstep=1;kv=309;sv=1
  for x in kicks:self.add(b+x,.18,kv,37,.19*a,rv=.12 if kv!=309 else .48)
  for x in snares:self.add(b+x,.12,sv,60,.12*a,rv=.17)
  for j in range(round(4/hatstep)):
   if kind=='breakcore' and j%7==2:continue
   at=j*hatstep+(.035 if j%2 and kind in ['garage','hiphop'] else 0)
   self.add(b+at,.06,2 if j%4 else 3,80,(.037 if j%2 else .023)*a,(-.32 if j%2 else .35),rv=.1)
  if kind=='breakcore' and int(b//4)%4==3:
   for j in range(10):self.add(b+3+j*.08,.04,204,60,.035*a*(1-j*.045),-.6+j*.12,rv=.10)
  elif int(b//4)%8==7:self.add(b+3.5,.1,4,70,.08*a,.2,rv=.25)
 def sing_word(self,beat,length,word,note,role,gain,pan,color=.5,shift=0,part='lead',glide=0):
  raw=PRON[word];phones=[PID[re.sub(r'\d','',p).replace('HH','H').replace('JH','J')] for p in raw]
  vowels=[i for i,p in enumerate(phones) if p<16]
  weights=[(1.15 if re.search(r'[12]',raw[i]) else .72) if i in vowels else .13 if p>=32 else .20 for i,p in enumerate(phones)]
  # Consonants have stable physical duration; vowels carry the sung note.
  seconds=self.sec(beat+length)-self.sec(beat);cons=[0 if p<16 else .046 if p>=32 else .065 for p in phones]
  ct=min(sum(cons),seconds*.46);vt=max(.04,seconds-ct);sumv=sum(weights[i] for i in vowels) or 1
  pdur=[vt*weights[i]/sumv if p<16 else ct*cons[i]/(sum(cons) or 1) for i,p in enumerate(phones)]
  cursor=beat;cast=ROLES.index(role);wp=[]
  for i,(ph,secs) in enumerate(zip(phones,pdur)):
   span=length*secs/seconds
   level=gain*(1 if ph<16 else .80 if ph<23 else 1.05)
   self.add(cursor,max(.018,span),1000+cast*100+ph,note+shift,level,pan,color,glide if ph<16 else 0,ds=.025 if cast<4 else .045,rv=.19 if cast<4 else .47,pre=phones[i-1] if i else -1,nxt=phones[i+1] if i+1<len(phones) else -1,group=part,human=False)
   wp.append({'phone':PHONE[ph],'start':round(self.sec(cursor),6),'end':round(self.sec(cursor+span),6)})
   cursor+=span
  if part=='lead':self.words.append({'word':word,'role':role,'beat':beat,'length':length,'start':round(self.sec(beat),6),'end':round(self.sec(beat+length),6),'note':round(note,4),'phonemes':wp})
 def sing_line(self,beat,span,text,role,index,ensemble=False):
  words=tokens(text);r,ch,q=self.harmony(int(beat//4));mode=self.d['mode'];third=4 if mode in ['major','lydian'] else 3
  motif=MOTIFS['stone' if role in ['CAIRN','MEMORY'] else 'other' if role in ['CARRIER','ALIEN'] else 'door']
  motif=[third if x==3 else x for x in motif]
  base=r+24
  center=CAST[role]['base']+7
  while base<center-5:base+=12
  while base>center+5:base-=12
  weights=[max(.65,sum(bool(re.search(r'\d',p)) for p in PRON[w]))*(.65 if w in ['a','the','to','of','in','is','and'] else 1.) for w in words]
  weights[-1]*=1.45;available=span-.65;unit=available/sum(weights);cursor=beat+.10
  start=self.sec(cursor);last=None
  for j,(word,w) in enumerate(zip(words,weights)):
   dur=unit*w;note=base+motif[(j+index*2)%len(motif)]
   if j==len(words)-1:note=base+([0,7,third,2][index%4])
   # Different tessituras and phrase shapes identify the dramatic roles.
   lo,hi={'CAIRN':(43,65),'MEMORY':(50,74),'HAND':(55,79),'CARRIER':(64,86),'CHORUS':(50,79),'ALIEN':(55,88)}[role]
   while note>hi:note-=12
   while note<lo:note+=12
   gain=.33 if role=='CAIRN' else .30 if role=='MEMORY' else .29 if role=='HAND' else .27
   if role in ['CHORUS','ALIEN']:
    # SATB divisi; each singer gets unique consonant offsets, tuning and colour.
    parts=[(-12,-.75),(0,-.30),(7,.28),(12,.72)]
    singers=4 if self.d['style'] in ['abduction','heaven','finale'] and beat/self.end>.60 else 3
    if self.d['style']=='garden':singers=2
    if self.d['style']=='flood' and beat/self.end>.73:singers=1
    harmony=[ch[0]-12,ch[1],ch[2],ch[0]+24]
    for p,(shift,pan) in enumerate(parts):
     pitch=note+(-12 if p==0 else 0 if p==1 else 7 if p==2 else 12)
     # Lower parts mostly hold chord tones while the top carries the tune.
     if p<2:pitch=harmonic_near(harmony[p],note+shift)
     for k in range(singers):
      offset=.025*k+.012*p+self.r.uniform(-.007,.008);tune=self.r.uniform(-.065,.065)
      self.sing_word(cursor+offset,max(.05,dur-.10),word,pitch+tune,role,.145/math.sqrt(singers),pan+self.r.uniform(-.09,.09),color=.25+.18*k,part='lead' if p==3 and k==0 else 'choir')
   else:
    self.sing_word(cursor,max(.06,dur-.075),word,note,role,gain*(.91+.12*self.r.random()),{'CAIRN':-.10,'MEMORY':.20,'HAND':-.28,'CARRIER':.35}[role],glide=max(-1.2,min(1.2,(last-note)*.25)) if last else -.3)
    if ensemble and j%2==0:
     other='MEMORY' if role=='CAIRN' else 'CAIRN'
     self.sing_word(cursor+.12,max(.08,dur-.20),word,note-7 if other=='CAIRN' else note+3,other,gain*.52,.42,part='countervoice')
   self.melody.append({'beat':cursor,'length':dur-.075,'word':word,'note':note,'role':role})
   last=note;cursor+=dur
  self.cues.append({'start':round(start,6),'end':round(self.sec(beat+span-.25),6),'beat':beat,'length':span,'role':role,'text':text,'kind':'chorus' if role in ['CHORUS','ALIEN'] else 'solo'})
 def voices(self):
  lines=[line.split('|',1) for line in self.d['lines'].splitlines()]
  # Recitative starts close to the listener; long prelude reserved for abduction.
  intro=8 if self.d['style'] not in ['origin','abduction','garden'] else 12
  final=10 if self.d['style']!='finale' else 14
  available=self.end-intro-final
  sizes=[max(5,len(tokens(t))) for _,t in lines];unit=available/sum(sizes);cursor=intro
  for i,((role,text),size) in enumerate(zip(lines,sizes)):
   span=size*unit
   self.sing_line(cursor,span,text,role,i,ensemble=self.d['style'] in ['hand','interval'] and i%5==3)
   cursor+=span
  # Wordless cathedral arches emerge between/around the written dramatic lines.
  if self.d['style'] in ['origin','room','abduction','heaven','finale','cities']:
   for bar in range(max(8,self.bounds[4]),self.bounds[5],4):
    r,ch,_=self.harmony(bar)
    for part,pitch in enumerate([ch[0]-12,ch[0],ch[1],ch[2],ch[0]+12,ch[2]+12]):
     for singer in range(3 if self.d['style'] in ['heaven','finale'] else 2):
      self.add(bar*4+singer*.09,13.6,1400+[5,6,8,0][part%4],pitch+self.r.uniform(-.07,.07),.060,-.88+part*.35,.20+singer*.26,rv=.68,group='wordless-choir',human=False)
 def export(self):
  stem=f'{self.n:02d}-{self.d["slug"]}';self.events.sort(key=lambda e:e['seconds']);self.cues.sort(key=lambda c:c['start'])
  data={'title':self.d['title'],'number':self.n,'act':self.d['act'],'genre':GENRE,'style':self.d['style'],'root':self.d['root'],'mode':self.d['mode'],'bpm':self.d['bpm'],'bars':self.d['bars'],'endBeat':self.end,'duration':self.duration,'sections':self.sections,'tempo':self.tempos,'events':self.events,'cues':self.cues,'vocalWords':self.words,'melody':self.melody}
  (ROOT/'scores'/f'{stem}.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
  room={'origin':4.7,'clock':2.6,'room':3.3,'abduction':5.7,'garden':4.0,'breaks':1.9,'flood':4.7,'interval':3.4,'cities':3.8,'hand':2.7,'heaven':6.0,'finale':5.2}[self.d['style']]
  lines=[f'{self.duration:.6f} {self.n} {260914+self.n} {room} {60/self.d["bpm"]*.75:.6f}']
  for e in self.events:lines.append(' '.join(str(x) for x in [e['seconds'],e['duration'],e['voice'],e['note'],e['gain'],e['pan'],e['tone'],e['motion'],e['delay'],e['reverb'],e['previous_phone'],e['next_phone'],e['seed']]))
  (ROOT/'scores'/f'{stem}.tsv').write_text('\n'.join(lines)+'\n')
  self.midi(ROOT/'midi'/f'{stem}.mid')
  used=sorted(set(e['voice'] for e in self.events if e['voice']<1000));vocals=sum(e['voice']>=1000 for e in self.events)
  return {'number':self.n,'act':self.d['act'],'title':self.d['title'],'slug':self.d['slug'],'stem':stem,'duration':round(self.duration,6),'bpm':self.d['bpm'],'bars':self.d['bars'],'style':self.d['style'],'scene':self.d['drama'],'cues':len(self.cues),'vocal_words':len(self.words),'phonetic_events':vocals,'instrument_count':len(used),'instruments':{str(v):NAMES[v] for v in used},'events':len(self.events)}
 def midi(self,path):
  ppq=960;meta=[(0,0,txt(3,self.d['title'])),(0,0,b'\xff\x58\x04\x04\x02\x18\x08')]
  for t in self.tempos:meta.append((round(t['beat']*ppq),0,b'\xff\x51\x03'+round(60e6/t['bpm']).to_bytes(3,'big')))
  for s in self.sections:meta.append((s['bar']*4*ppq,0,txt(6,s['name'])))
  chunks=[mtrack(meta)];voices=sorted(set(e['voice'] for e in self.events if e['voice']<1000))
  for idx,v in enumerate(voices):
   channel=idx%15;channel+=channel>=9;port=idx//15
   events=[(0,0,txt(3,NAMES[v])),(0,0,bytes([255,33,1,port])),(0,0,bytes([192|channel,{300:19,301:19,302:48,303:45,304:42,305:60,306:61,307:47,308:14,313:73,314:46,315:0}.get(v,89)]))]
   for e in self.events:
    if e['voice']!=v:continue
    n=round(e['note']);velocity=max(1,min(120,round(e['gain']*430)))
    events.extend([(round(e['at']*ppq),1,bytes([144|channel,n,velocity])),(round((e['at']+e['length'])*ppq),-1,bytes([128|channel,n,0]))])
   chunks.append(mtrack(events))
  for i,role in enumerate(ROLES):
   events=[(0,0,txt(3,CAST[role]['name']+' / lyric melody')),(0,0,bytes([255,33,1,4])),(0,0,bytes([192|i,53]))]
   for m in self.melody:
    if m['role']!=role:continue
    start=round(m['beat']*ppq);end=round((m['beat']+m['length'])*ppq);n=round(m['note'])
    events.extend([(start,0,txt(5,m['word'])),(start,1,bytes([144|i,n,88])),(end,-1,bytes([128|i,n,0]))])
   chunks.append(mtrack(events))
  path.write_bytes(b'MThd'+struct.pack('>IHHH',6,1,len(chunks),ppq)+b''.join(chunks))
def harmonic_near(n,target):
 while n<target-6:n+=12
 while n>target+6:n-=12
 return n
if __name__=='__main__':
 albums=[]
 for n,d in enumerate(SCENES,1):
  scene=Scene(d,n);scene.orchestra();scene.voices();a=scene.export();albums.append(a)
  print(f'{n:02d} {d["title"]}: {a["duration"]/60:.2f} min, {a["events"]} events, {a["instrument_count"]} instrument recipes',flush=True)
 inventory={int(k) for a in albums for k in a['instruments']}
 required=set(range(30))|set(range(100,116))|set(range(200,215))|set(range(400,421))|set(range(300,317))
 assert required<=inventory,sorted(required-inventory)
 (ROOT/'scores/manifest.json').write_text(json.dumps({'title':TITLE,'subtitle':SUBTITLE,'genre':GENRE,'cast':CAST,'scenes':albums,'total_seconds':sum(a['duration'] for a in albums),'instrument_recipes':len(inventory)},indent=2)+'\n')
 (ROOT/'scores/instruments.json').write_text(json.dumps({str(k):v for k,v in NAMES.items()},indent=2)+'\n')
 print('Total',sum(a['duration'] for a in albums)/60,'minutes;',len(inventory),'instrument recipes')
