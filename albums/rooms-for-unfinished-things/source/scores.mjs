import {pitch,random,validate} from './synth.mjs';

export const album={title:'Rooms for Unfinished Things',artist:'Cairn',date:'2026-09-13',localOnly:true};
const C=(bass,...notes)=>({bass:pitch(bass),notes:notes.map(pitch)});
const section=(name,bars,role)=>({name,bars,role});
export const tracks=[
  {number:1,slug:'a-window-before-the-wall',title:'A Window Before the Wall',original:true,bpm:96,meter:[3,4],note:'The original little waltz. A window, a passing swallow, and a single extra beat. The performance is unchanged; the album copy is level-matched.'},
  {
    number:2,slug:'the-bicycle-has-right-of-way',title:'The Bicycle Has Right of Way',bpm:112,meter:[4,4],beats:4,seed:0xb1c1c1e,room:.027,
    note:'A sunny syncopated ride in G: plucked strings, dry keys and upright bass. The middle section coasts without the kick before the wheels find the road again.',
    lead:'pluck',second:'toy',style:'bicycle',gain:.16,
    harmony:[C('G2','B3','D4','F#4','A4'),C('E2','G3','B3','D4','F#4'),C('C2','G3','B3','D4','E4'),C('D2','F#3','A3','C4','E4'),C('B1','A3','B3','D4','F#4'),C('A1','G3','B3','C4','E4'),C('C2','G3','A3','D4','E4'),C('D2','F#3','A3','C4','E4')],
    ending:C('G2','G3','B3','D4','E4','A4'),
    A:['G4:.5 B4:.5 D5:.75 B4:.25 A4:.5 .:.5 G4:.5 E4:.5','E4:.75 G4:.25 B4:.5 D5:.5 F#5:.75 E5:.25 D5:.5 B4:.5','E5:.5 D5:.5 B4:.75 G4:.25 E4:1 .:.5 G4:.5','A4:.75 F#4:.25 E4:.5 D4:.5 F#4:.5 A4:.5 C5:.5 E5:.5','F#5:.5 D5:.5 B4:.5 A4:.5 F#4:.75 A4:.25 B4:.5 D5:.5','E5:1 C5:.5 B4:.5 A4:.75 G4:.25 E4:.5 .:.5','G4:.5 A4:.5 B4:.5 D5:.5 E5:.75 D5:.25 B4:.5 G4:.5','F#4:.75 A4:.25 C5:.5 E5:.5 D5:1 .:1'],
    B:['B4:1 A4:.5 G4:.5 F#4:.5 D4:.5 .:1','G4:.5 B4:.5 E5:1 D5:.5 B4:.5 G4:.5 E4:.5','C5:.75 B4:.25 A4:.5 G4:.5 E4:1 G4:.5 A4:.5','F#4:1 E4:.5 D4:.5 A4:.5 C5:.5 E5:.75 .:.25','D5:.5 F#5:.5 A5:.5 F#5:.5 D5:1 B4:1','C5:.5 E5:.5 G5:1 E5:.5 C5:.5 B4:.5 A4:.5','G4:1 E5:.5 D5:.5 B4:1 A4:.5 G4:.5','F#4:.5 A4:.5 E5:1 C5:.5 A4:.5 F#4:.75 .:.25'],
    form:[section('Unchain the bicycle',8,'intro'),section('Right of way',16,'a'),section('A different street',16,'a2'),section('Coasting',16,'bridge'),section('Handlebar melody',16,'b'),section('Both wheels home',16,'return'),section('Lean it by the gate',8,'coda')],
  },
  {
    number:3,slug:'a-chair-with-opinions',title:'A Chair with Opinions',bpm:102,meter:[5,4],beats:5,seed:0xc4a1c4a1,room:.034,
    note:'Five beats per bar, grouped three plus two. Marimba makes an assertion; a low reed asks an awkward follow-up. The chair gets the last word.',
    lead:'marimba',second:'reed',style:'chair',gain:.17,
    harmony:[C('Eb2','G3','Bb3','D4','F4'),C('C2','Eb3','G3','Bb3','D4'),C('Ab1','G3','Bb3','C4','Eb4'),C('Bb1','Ab3','C4','D4','F4'),C('G1','F3','Bb3','D4','G4'),C('F2','Ab3','C4','Eb4','G4'),C('Ab1','G3','Bb3','C4','Eb4'),C('Bb1','Ab3','C4','D4','F4')],
    ending:C('Eb2','Eb3','G3','Bb3','C4','F4'),
    A:['Eb4:.5 G4:.5 Bb4:1 D5:.5 Bb4:.5 .:.5 G4:.5 F4:.5 Eb4:.5','G4:1 Eb4:.5 D4:.5 C4:1 .:.5 G4:.5 Bb4:1','Ab4:.5 C5:.5 Eb5:1 G5:.5 Eb5:.5 C5:1 Bb4:.5 Ab4:.5','F4:.5 Ab4:.5 D5:1 C5:.5 Bb4:.5 F4:.5 D4:.5 .:1','G4:.5 Bb4:.5 D5:.5 F5:.5 D5:1 Bb4:1 G4:1','Ab4:1 G4:.5 F4:.5 Eb4:1 C4:.5 F4:.5 G4:1','C5:.5 Eb5:.5 G5:1 F5:.5 Eb5:.5 C5:.5 Bb4:.5 Ab4:1','D5:.5 C5:.5 Bb4:1 Ab4:.5 F4:.5 D4:.5 F4:.5 .:1'],
    B:['G3:1 Bb3:1 D4:.5 F4:.5 Eb4:1 .:1','Eb4:.5 G4:.5 Bb4:1 G4:.5 Eb4:.5 D4:1 C4:1','C4:1 Eb4:.5 G4:.5 Bb4:1 Ab4:.5 G4:.5 Eb4:1','D4:.5 F4:.5 Ab4:1 C5:1 Bb4:1 F4:1','Bb3:.5 D4:.5 F4:1 G4:.5 F4:.5 D4:1 Bb3:1','C4:1 Eb4:1 G4:.5 Ab4:.5 G4:1 F4:1','Eb4:.5 G4:.5 C5:1 Bb4:.5 Ab4:.5 G4:1 Eb4:1','D4:1 F4:.5 Ab4:.5 C5:.5 Bb4:.5 F4:1 .:1'],
    form:[section('A polite objection',8,'intro'),section('Three legs, then two',16,'a'),section('The room considers it',8,'bridge'),section('A counterproposal',16,'b'),section('Furniture debate',8,'return'),section('One last creak',8,'coda')],
  },
  {
    number:4,slug:'rain-in-the-unnumbered-street',title:'Rain in the Unnumbered Street',bpm:76,meter:[6,8],beats:3,seed:0xa1a1913,room:.062,
    note:'A slow six-eight nocturne in G minor. Felt piano, vibraphone droplets and a breathy melody; the texture clears rather than swelling into a climax.',
    lead:'flute',second:'vibes',style:'rain',gain:.10,
    harmony:[C('G2','Bb3','D4','F4','A4'),C('Eb2','Bb3','D4','G4','A4'),C('Bb1','A3','C4','D4','F4'),C('F2','A3','C4','G4','Bb4'),C('C2','Bb3','D4','Eb4','G4'),C('D2','A3','C4','F4','G4'),C('Eb2','Bb3','D4','F4','G4'),C('D2','A3','C4','F#4','A4')],
    ending:C('G2','G3','Bb3','D4','A4'),
    A:['D5:1 C5:.5 Bb4:.5 A4:.5 G4:.5','G4:1.5 Bb4:.5 D5:1','F5:.75 D5:.75 C5:.5 A4:.5 Bb4:.5','C5:1.5 A4:.5 G4:1','G4:.5 Bb4:.5 D5:1 Eb5:.5 D5:.5','C5:1 A4:.5 G4:.5 F4:1','G4:1 Bb4:.5 D5:.5 F5:.5 Eb5:.5','D5:1 A4:.5 F#4:.5 .:1'],
    B:['Bb4:.5 D5:.5 F5:1 A5:.5 G5:.5','G5:1 F5:.5 D5:.5 Bb4:1','A4:1 C5:.5 D5:.5 F5:1','G5:.5 F5:.5 C5:1 A4:1','Eb5:1 D5:.5 Bb4:.5 G4:1','A4:.5 C5:.5 F5:1 E5:.5 D5:.5','Bb4:1 D5:.5 G5:.5 F5:1','F#5:.5 E5:.5 D5:1 A4:.5 .:.5'],
    form:[section('A first drop',8,'intro'),section('The street without a number',16,'a'),section('Under the eaves',16,'b'),section('Only the droplets',16,'bridge'),section('A face at a window',16,'return'),section('The rain thins',16,'coda')],
  },
  {
    number:5,slug:'the-drawer-in-the-brick',title:'The Drawer in the Brick',bpm:72,meter:[4,4],beats:4,seed:0xd2a9e4,room:.049,
    note:'The album’s unhurried centre: felt piano in F-sharp minor, without drums. Low notes answer widely spaced phrases; a soft sustained voice appears only in the middle.',
    lead:'felt',second:'felt',style:'drawer',gain:.17,
    harmony:[C('F#2','A3','C#4','E4','G#4'),C('D2','A3','C#4','E4','F#4'),C('A1','G#3','B3','C#4','E4'),C('E2','G#3','B3','F#4','A4'),C('B1','A3','C#4','D4','F#4'),C('C#2','G#3','B3','E4','F#4'),C('D2','A3','C#4','E4','F#4'),C('C#2','G#3','B3','E#4','G#4')],
    ending:C('F#2','F#3','A3','C#4','G#4'),
    A:['F#4:1.5 A4:.5 G#4:1 E4:1','F#4:1 E4:.5 C#4:.5 A3:1 .:1','C#4:.75 E4:.75 G#4:.5 B4:1 A4:1','G#4:1.5 F#4:.5 E4:1 .:1','F#4:1 D4:1 C#4:.5 B3:.5 A3:1','G#3:1 B3:.5 C#4:.5 E4:1 F#4:1','E4:1 C#4:1 A3:1 F#3:1','G#3:.5 B3:.5 E#4:1 C#4:1 .:1'],
    B:['C#5:1.5 B4:.5 A4:1 G#4:1','A4:.5 C#5:.5 E5:1 D5:.5 C#5:.5 A4:1','B4:1 G#4:.5 E4:.5 C#4:1 E4:1','F#4:1 G#4:.5 B4:.5 E5:1 B4:1','A4:.75 F#4:.75 D4:.5 C#4:1 B3:1','C#4:1 E4:.5 G#4:.5 B4:1 G#4:1','A4:1 E4:1 F#4:.5 E4:.5 C#4:1','B3:.5 G#3:.5 E#4:1 G#4:1 .:1'],
    form:[section('A thumbprint',8,'intro'),section('Behind the loose brick',16,'a'),section('The letter opens',16,'b'),section('The hand pauses',8,'bridge'),section('Folded small',16,'return'),section('Room for another letter',8,'coda')],
  },
  {
    number:6,slug:'the-kettle-is-not-the-conductor',title:'The Kettle Is Not the Conductor',bpm:116,meter:[7,8],beats:3.5,seed:0x7eaa0713,room:.023,
    note:'Seven eighth-notes at a time. A bright, percussive kitchen machine in B: the groove is grouped two-two-three, and the whistle refuses to land on the obvious beat.',
    lead:'glass',second:'marimba',style:'kettle',gain:.13,
    harmony:[C('B1','D#4','F#4','A4','C#5'),C('G#1','B3','D#4','F#4','A#4'),C('E2','G#3','B3','D#4','F#4'),C('F#2','A#3','C#4','E4','G#4'),C('B1','D#4','F#4','A4','C#5'),C('A1','G3','B3','C#4','E4'),C('E2','G#3','B3','D#4','F#4'),C('F#2','A#3','C#4','E4','G#4')],
    ending:C('B1','B3','D#4','F#4','A4','C#5'),
    A:['B4:.5 D#5:.5 F#5:.5 A5:.5 F#5:.5 D#5:.5 C#5:.5','B4:.5 G#4:.5 D#5:1 F#5:.5 A#5:.5 G#5:.5','G#4:.5 B4:.5 D#5:.5 F#5:.5 E5:.5 B4:.5 G#4:.5','A#4:.5 C#5:.5 E5:1 G#5:.5 F#5:.5 .:.5','F#5:.5 D#5:.5 B4:.5 A4:.5 F#4:.5 B4:.5 D#5:.5','E5:.5 C#5:.5 B4:1 G4:.5 A4:.5 C#5:.5','D#5:.5 B4:.5 G#4:.5 E4:.5 F#4:.5 G#4:.5 B4:.5','A#4:.5 C#5:.5 G#5:.75 F#5:.25 E5:.5 C#5:.5 .:.5'],
    B:['D#4:1 F#4:.5 A4:.5 C#5:1 B4:.5','G#4:.5 B4:.5 D#5:.5 F#5:1 D#5:.5 B4:.5','B4:1 G#4:.5 F#4:.5 E4:.5 D#4:.5 B3:.5','C#4:.5 E4:.5 F#4:.5 A#4:.5 C#5:1 .:.5','A4:.5 B4:.5 C#5:.5 D#5:.5 F#5:.5 D#5:.5 B4:.5','A4:.5 C#5:.5 E5:1 G5:.5 E5:.5 C#5:.5','B4:1 G#4:.5 D#5:.5 E5:.5 F#5:.5 G#5:.5','A#5:.5 G#5:.5 F#5:.5 E5:.5 C#5:1 .:.5'],
    form:[section('Switch on',8,'intro'),section('Two, two, three',24,'a'),section('Steam without a clock',16,'bridge'),section('The kitchen answers',24,'b'),section('Nobody is conducting',24,'return'),section('Click, then quiet',16,'coda')],
  },
  {
    number:7,slug:'swallows-borrow-the-ballroom',title:'Swallows Borrow the Ballroom',bpm:132,meter:[3,4],beats:3,seed:0xb1772001,room:.038,
    note:'The full ensemble takes flight. A quicker waltz, a middle section lifted into G, and a return to D with the piano and flute trading the tune.',
    lead:'toy',second:'flute',style:'ballroom',gain:.145,
    harmony:[C('D2','F#3','A3','C#4','E4'),C('B1','A3','B3','D4','F#4'),C('G2','B3','D4','F#4','A4'),C('A2','G3','B3','C#4','E4'),C('F#2','A3','C#4','E4','G#4'),C('E2','G3','B3','D4','F#4'),C('G2','B3','D4','E4','A4'),C('A2','G3','B3','C#4','E4')],
    ending:C('D2','D4','F#4','A4','B4','E5'),
    A:['D5:.5 F#5:.5 A5:.75 F#5:.25 E5:.5 D5:.5','B4:.5 D5:.5 F#5:1 A5:.5 F#5:.5','G5:.5 F#5:.5 D5:.5 B4:.5 A4:.5 B4:.5','C#5:.5 E5:.5 A5:1 G5:.5 E5:.5','F#5:.5 E5:.5 C#5:.5 A4:.5 G#4:.5 A4:.5','B4:.5 D5:.5 G5:1 F#5:.5 E5:.5','D5:.5 E5:.5 F#5:.5 A5:.5 B5:.5 A5:.5','G5:.5 E5:.5 C#5:.5 B4:.5 A4:.5 .:.5'],
    B:['F#5:1 E5:.5 D5:.5 A4:1','D5:.5 F#5:.5 B5:1 A5:.5 F#5:.5','B4:.5 D5:.5 G5:.5 A5:.5 B5:.5 A5:.5','G5:1 E5:.5 C#5:.5 B4:.5 A4:.5','C#5:.5 E5:.5 G#5:1 F#5:.5 E5:.5','D5:.5 B4:.5 G4:.5 B4:.5 E5:1','F#5:.5 E5:.5 D5:1 B4:.5 A4:.5','C#5:.5 E5:.5 G5:1 A5:.5 .:.5'],
    form:[section('Doors open',8,'intro'),section('Borrowed ballroom',32,'a'),section('A higher window',32,'b'),section('One bird alone',16,'bridge'),section('All the windows',48,'return'),section('The room settles',24,'coda')],
  },
  {
    number:8,slug:'leave-the-window-open',title:'Leave the Window Open',bpm:82,meter:[4,4],beats:4,seed:0x1ea9e0913,room:.060,
    note:'A spacious farewell in D. The opening motif returns in a slower room; the final sixteen bars progressively lose instruments and slow down. The last note is an invitation, not a flourish.',
    lead:'felt',second:'vibes',style:'open',gain:.155,
    harmony:[C('D2','F#3','A3','C#4','E4'),C('B1','A3','C#4','D4','F#4'),C('G2','B3','D4','F#4','A4'),C('A2','A3','B3','D4','E4'),C('F#2','A3','C#4','E4','G#4'),C('E2','G3','B3','D4','F#4'),C('G2','B3','D4','E4','A4'),C('A2','G3','B3','C#4','E4')],
    ending:C('D2','D3','F#3','A3','B3','E4'),
    A:['A4:1 F#4:1 E4:.5 D4:.5 .:1','F#4:1 A4:.5 B4:.5 A4:1 F#4:1','D5:1 B4:.5 A4:.5 G4:1 F#4:1','E4:1 A4:1 B4:.5 A4:.5 .:1','G#4:1 E4:.5 C#4:.5 A3:1 C#4:1','D4:.5 E4:.5 G4:1 B4:1 A4:1','F#4:1 E4:1 D4:.5 B3:.5 A3:1','C#4:1 E4:.5 G4:.5 A4:1 .:1'],
    B:['D4:.5 F#4:.5 A4:1 E4:.5 D4:.5 .:1','B3:.5 D4:.5 F#4:1 A4:1 F#4:1','G4:1 F#4:.5 D4:.5 B3:1 A3:1','E4:1 D4:.5 B3:.5 A3:1 .:1','C#4:.5 E4:.5 G#4:1 F#4:1 E4:1','G4:1 E4:1 D4:.5 B3:.5 G3:1','B3:.5 D4:.5 F#4:1 E4:1 D4:1','C#4:1 E4:.5 A4:.5 G4:1 .:1'],
    form:[section('A light remains',8,'intro'),section('Rooms remembered',16,'a'),section('The first window, again',16,'b'),section('There is room',24,'return'),section('Leave it open',16,'coda')],
  },
];

export function compose(track){
  const rand=random(track.seed),events=[],sections=[];
  const score={...track,events,sections,tail:track.style==='open'?6.5:4.2};
  let bar=0;
  const add=(voice,n,at,len,gain,pan=0,extra={})=>{events.push({voice,pitch:pitch(n),at:Math.max(0,at),len,gain,pan,...extra});};
  const chord=(voice,notes,at,len,gain,pan=-.2)=>notes.forEach((n,i)=>add(voice,n,at+i*.012,len,gain,Math.max(-.9,Math.min(.9,pan+i*.07))));
  const melody=(voice,pattern,at,transpose,gain)=>{
    let t=0;for(const token of pattern.split(' ')){const [n,d]=token.split(':'),len=Number(d);if(n!=='.')add(voice,pitch(n)+transpose,at+t+(rand()-.5)*.012,Math.max(.12,len*.9),gain*(.92+rand()*.14),voice==='flute'?.27:-.2);t+=len;}
    if(t>track.beats+.00001)throw Error('Melody longer than bar: '+track.title+' / '+pattern);
  };
  for(const sec of track.form){
    sections.push({beat:bar*track.beats,name:sec.name});
    for(let k=0;k<sec.bars;k++,bar++){
      const q=bar*track.beats,phase=bar%8,role=sec.role,closing=role==='coda';
      const finalBar=closing&&k===sec.bars-1;
      const transpose=track.style==='ballroom'&&role==='b'?5:0;
      const raw=track.harmony[phase],c={bass:raw.bass+transpose,notes:raw.notes.map(n=>n+transpose)};
      const envelope=closing?1-.72*k/sec.bars:role==='intro'?.64+.3*k/sec.bars:role==='bridge'?.66:1;
      let voice=(role==='b'||(role==='return'&&Math.floor(k/8)%2))?track.second:track.lead;
      let playLead=!(role==='intro'&&k<4)&&!finalBar;
      if(role==='bridge')playLead=track.style==='drawer'?k%2===0:track.style==='rain'?false:k%4===0;
      if(closing&&k>=sec.bars-4)playLead=k%2===0&&!finalBar;
      if(playLead)melody(voice,(role==='b'||role==='a2'?track.B:track.A)[phase],q,transpose,track.gain*envelope);
      if(finalBar){
        const e=track.ending;
        chord(track.style==='chair'?'marimba':'felt',e.notes,q,track.beats+.4,.047,-.3);
        add('bass',e.bass,q,track.beats,.095,.03);
        continue;
      }
      if(track.style==='drawer'){
        add('felt',c.bass,q,2.8,.13*envelope,-.28);
        chord('felt',c.notes.slice(0,3),q+1.55,1.7,.031*envelope,.0);
        if(role==='b'||role==='return')chord('pad',c.notes.slice(0,3),q+.15,3.6,.018*envelope,.12);
        if(role==='bridge')add('vibes',c.notes[2]+12,q+2.6,.9,.035,.3);
        continue;
      }
      if(track.style==='open'){
        add('bass',c.bass,q,3.2,.10*envelope,0);
        chord('felt',c.notes.slice(0,3),q+.1,2.8,.026*envelope,-.24);
        if(role!=='intro'&&!(closing&&k>4))chord('pad',c.notes.slice(0,3),q+.3,3.4,.018*envelope,.25);
        if(role==='b'||role==='return')add('vibes',c.notes[3]+12,q+2.75,.9,.04*envelope,.5);
        if(role==='return'&&k<16){add('brush',38,q+1.04,.25,.014,.3);add('hat',42,q+3.55,.08,.01,-.4);}
        continue;
      }
      if(track.style==='rain'){
        add('felt',c.bass,q,2.2,.12*envelope,-.18);
        const offsets=[0,.75,1.5,2.25];
        for(let i=0;i<4;i++)add(role==='bridge'?'vibes':'felt',c.notes[(i+phase)%4],q+offsets[i],.8,.041*envelope,-.35+i*.2);
        if(bar%2)add('vibes',c.notes[2]+12,q+2.45,.4,.034*envelope,.55);
        if(role==='b'||role==='return')add('brush',38,q+1.5,.3,.018*envelope,.3);
        if(role==='b')chord('pad',c.notes.slice(0,3),q+.2,2.5,.014,.12);
        continue;
      }
      const active=role!=='intro'||k>=4,drums=active&&role!=='bridge'&&!(closing&&k>=sec.bars-4);
      add('bass',c.bass,q,track.style==='kettle'?.55:1.3,.14*envelope,0);
      if(active)add('bass',c.bass+7,q+(track.style==='chair'?3:track.style==='ballroom'?2:2.05),.65,.08*envelope,.03);
      if(track.style==='bicycle'){
        for(const off of [.75,1.5,2.75,3.5])chord('felt',c.notes.slice(0,3),q+off,.32,.033*envelope,-.15);
        if(role==='b'||role==='return')add('vibes',c.notes[3]+12,q+3.1,.65,.036*envelope,.5);
        if(drums){for(const off of [0,2.5])add('kick',36,q+off,.2,.075,0);for(const off of [1.02,3.02])add('brush',38,q+off,.25,.038,.24);for(const off of [.6,1.6,2.6,3.6])add('hat',42,q+off,.08,.023,-.35);}
      }else if(track.style==='chair'){
        chord('pizz',c.notes.slice(0,3),q+1,.4,.038*envelope,-.35);chord('pizz',c.notes.slice(1),q+3.5,.4,.034*envelope,.12);
        if(role==='b')add('marimba',c.notes[3]+12,q+4.5,.35,.057*envelope,.5);
        if(drums){add('kick',36,q,.2,.075);add('wood',76,q+2.5,.15,.045,.4);add('brush',38,q+3,.25,.04,.2);add('hat',42,q+4.5,.08,.022,-.3);}
      }else if(track.style==='kettle'){
        for(let i=0;i<3;i++)add('marimba',c.notes[i],q+[.5,1.5,2.5][i],.36,.065*envelope,-.5+i*.35);
        if(role==='b'||role==='return')chord('organ',c.notes.slice(0,3),q+1.1,.42,.026*envelope,.1);
        if(drums){for(const off of [0,2])add('kick',36,q+off,.2,.09);for(const off of [1,3])add('brush',38,q+off,.22,.046,.23);for(const off of [.5,1.5,2.5,3.25])add('hat',42,q+off,.07,.022,-.4);if(bar%4===3)add('wood',76,q+3.25,.08,.033,.55);}
      }else if(track.style==='ballroom'){
        for(const off of [1.02,2.02])chord('pizz',c.notes.slice(0,3),q+off,.38,.04*envelope,-.35);
        if(role==='b'||role==='return')add('glass',c.notes[3]+12,q+2.4,.5,.039*envelope,.55);
        if(role==='bridge')add('flute',c.notes[2]+12,q+.4,1.7,.065,.25,{glide:bar%4===0?5:0});
        if(drums){add('kick',36,q,.2,.08);for(const off of [1.02,2.02])add('brush',38,q+off,.22,.04,.22);for(const off of [.55,1.55,2.55])add('hat',42,q+off,.07,.02,-.4);}
      }
    }
  }
  score.endBeat=bar*track.beats;
  if(track.style==='chair')add('wood',76,score.endBeat+.65,.12,.026,.35);
  if(track.style==='kettle')add('wood',76,score.endBeat+.35,.08,.02,.45);
  if(track.style==='open'){
    score.tempoChanges=[{beat:(bar-16)*4,bpm:78},{beat:(bar-8)*4,bpm:72},{beat:(bar-4)*4,bpm:66},{beat:(bar-2)*4,bpm:60}];
    add('toy','E5',score.endBeat+.5,.6,.035,.35);
  }
  if(track.style==='ballroom')score.tempoChanges=[{beat:(bar-8)*3,bpm:126},{beat:(bar-4)*3,bpm:116}];
  validate(score);return score;
}
