import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// Original score and deterministic instrumental synthesis by Cairn, 2026-09-13.
// No samples, generated-music service, or third-party melody.
const dir = path.dirname(fileURLToPath(import.meta.url));
const SR = 44100, BPM = 96, beat = 60 / BPM, TAU = 2 * Math.PI;
const start = 0.12, musicEnd = start + 145 * beat, duration = musicEnd + 4.2;
const L = new Float32Array(Math.ceil(duration * SR));
const R = new Float32Array(L.length);
const events = [];
let seed = 0xc41a0913;
function noise() { seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5; return (seed >>> 0) / 2147483648 - 1; }
const hz = n => 440 * 2 ** ((n - 69) / 12);
const barBeat = b => b * 3 + (b >= 47 ? 1 : 0);
function add(inst, pitch, when, len, gain, pan = 0) {
  events.push({ instrument: inst, pitch, beat: when, length: len, velocity: Math.round(Math.min(1, gain * 4) * 110) });
  const t0 = start + when * beat;
  const hold = len * beat;
  const tail = ({ piano: 1.8, bass: .55, pizz: .38, marimba: 1.1, glass: .8, flute: .6, kick: .2, brush: .25, shaker: .05 })[inst];
  const first = Math.round(t0 * SR), last = Math.min(L.length, first + Math.ceil((hold + tail) * SR));
  const f = hz(pitch), gL = Math.cos((pan + 1) * Math.PI / 4), gR = Math.sin((pan + 1) * Math.PI / 4);
  let filtered = 0, phase = 0;
  for (let i = first; i < last; i++) {
    const t = (i - first) / SR, w = TAU * f * t;
    const release = Math.exp(-Math.max(0, t - hold) / Math.max(.04, tail / 5));
    let v = 0;
    if (inst === 'piano') {
      v = (.76 * Math.sin(w) * Math.exp(-1.8 * t) + .28 * Math.sin(w * 2.012) * Math.exp(-3.8 * t)
        + .14 * Math.sin(w * 3.99) * Math.exp(-6.5 * t) + .07 * Math.sin(w * 6.08) * Math.exp(-10 * t));
      v *= (1 - Math.exp(-t * 650)) * release;
    } else if (inst === 'bass') {
      v = (Math.sin(w) + .32 * Math.sin(2 * w) * Math.exp(-3 * t) + .11 * Math.sin(3 * w) * Math.exp(-5 * t));
      v *= (1 - Math.exp(-t * 160)) * Math.exp(-1.8 * t) * release;
    } else if (inst === 'pizz') {
      v = (Math.sin(w) + .4 * Math.sin(2 * w) + .21 * Math.sin(3 * w) + .1 * Math.sin(5 * w));
      v *= (1 - Math.exp(-t * 750)) * Math.exp(-7 * t) * release;
    } else if (inst === 'marimba') {
      v = (Math.sin(w) * Math.exp(-3.2 * t) + .3 * Math.sin(4 * w) * Math.exp(-12 * t) + .1 * Math.sin(9.15 * w) * Math.exp(-23 * t));
      v *= (1 - Math.exp(-t * 1000)) * release;
    } else if (inst === 'glass') {
      v = Math.sin(w + .6 * Math.exp(-2.2 * t) * Math.sin(2 * w)) * .7 + .18 * Math.sin(w * 1.003);
      v *= (1 - Math.exp(-t * 35)) * Math.exp(-1.7 * t) * release;
    } else if (inst === 'flute') {
      const progress = Math.min(1, t / hold);
      // One breath crosses an octave and settles back into the room.
      const curve = 7 * Math.sin(progress * Math.PI) - 3 * progress;
      phase += TAU * hz(pitch + curve + .055 * Math.sin(TAU * 5.1 * t)) / SR;
      filtered = .86 * filtered + .14 * noise();
      v = (Math.sin(phase) + .13 * Math.sin(2 * phase) + .055 * filtered);
      v *= Math.min(1, t / .14) * Math.sin(Math.PI * Math.min(.999, t / (hold + tail))) ** .7;
    } else if (inst === 'kick') {
      phase += TAU * (48 + 62 * Math.exp(-t * 36)) / SR;
      v = Math.sin(phase) * Math.exp(-t * 17) * (1 - Math.exp(-t * 900));
    } else if (inst === 'brush') {
      const n = noise(); filtered = .76 * filtered + .24 * n;
      v = ((n - filtered) * .7 + filtered * .5) * (1 - Math.exp(-t * 180)) * Math.exp(-t * 19);
    } else if (inst === 'shaker') {
      const n = noise(); filtered = .91 * filtered + .09 * n;
      v = (n - filtered) * Math.exp(-t * 55) * (1 - Math.exp(-t * 1400));
    }
    L[i] += v * gain * gL;
    R[i] += v * gain * gR;
  }
}

// Two eight-bar themes. Numbers are MIDI pitches, offsets and durations in beats.
const A = [
  [[0,74,.5],[.5,78,.5],[1,81,1],[2.2,76,.5]],
  [[0,76,.7],[.8,74,.8],[2,71,.4],[2.5,69,.4]],
  [[0,71,.5],[.5,74,.5],[1,78,1],[2,81,.65]],
  [[0,78,.8],[1,74,.5],[1.65,71,.5],[2.3,69,.5]],
  [[0,67,.5],[.5,71,.5],[1,74,1],[2.2,78,.5]],
  [[0,76,.7],[.9,74,.7],[1.8,71,.4],[2.4,69,.4]],
  [[0,69,.5],[.5,73,.5],[1,76,.8],[2,83,.7]],
  [[0,81,1],[1.2,76,.6],[2,73,.5]],
];
const B = [
  [[0,66,.7],[.9,69,.5],[1.6,74,.7],[2.5,76,.35]],
  [[0,78,.8],[1,76,.5],[1.7,74,.5],[2.4,69,.4]],
  [[0,78,.5],[.65,81,.5],[1.3,83,.8],[2.3,81,.5]],
  [[0,78,1],[1.25,74,.6],[2.1,71,.7]],
  [[0,71,.6],[.8,74,.6],[1.6,78,.6],[2.4,81,.4]],
  [[0,79,.7],[.9,78,.5],[1.6,76,.5],[2.3,74,.5]],
  [[0,73,.7],[.9,76,.5],[1.6,81,.7],[2.4,83,.4]],
  [[0,81,.6],[.8,76,.6],[1.7,73,.8]],
];
const chords = [
  { bass:38, notes:[62,66,69,73] }, { bass:45, notes:[62,66,69,76] },
  { bass:35, notes:[59,62,66,69] }, { bass:42, notes:[59,62,66,73] },
  { bass:31, notes:[59,62,66,69] }, { bass:38, notes:[59,62,64,69] },
  { bass:33, notes:[57,61,64,71] }, { bass:40, notes:[57,61,67,71] },
];

for (let bar = 0; bar < 48; bar++) {
  const q = barBeat(bar), c = chords[bar % 8];
  const quiet = bar === 22 || bar === 23;
  const ending = bar === 47;
  const theme = bar >= 32 && bar < 40 ? B : A;
  if (!quiet && !ending) {
    for (const [offset, pitch, len] of theme[bar % 8]) {
      const v = .145 + .014 * noise();
      add('piano', pitch, q + offset + .012 * noise(), len, v, -.22);
    }
  }
  if (bar >= 4 && !quiet && !ending) {
    add('bass', c.bass, q, 1.65, .15, .04);
    if (bar >= 8) add('bass', c.bass + 7, q + 2.05, .6, .078, .03);
    add('kick', 36, q, .2, .11, 0);
    add('brush', 38, q + 1.04, .22, .042, .24);
    add('brush', 38, q + 2.02, .25, .052, .2);
    if (bar >= 12) for (const off of [.52, 1.55, 2.54]) add('shaker', 42, q + off, .09, .023, -.45);
  }
  if (bar >= 12 && !quiet && !ending) {
    for (let j = 0; j < 3; j++) {
      add('pizz', c.notes[j], q + 1.04 + j * .012, .42, .031, -.58 + j * .18);
      add('pizz', c.notes[j + 1], q + 2.04 + j * .012, .42, .028, -.58 + j * .18);
    }
  }
  if (bar >= 16 && bar < 44 && !quiet && bar % 2 === 1) {
    add('marimba', c.notes[1] + 12, q + 1.5, .5, .066, .48);
    add('marimba', c.notes[3] + 12, q + 2.55, .4, .051, .55);
  }
  if (bar >= 24 && bar < 44 && bar % 4 === 3) {
    add('glass', 81, q + 1.65, .6, .048, .6);
    add('glass', 76, q + 2.4, .5, .037, .48);
  }
}
// Two drumless bars with a single moving breath, not an empty export.
add('piano', 74, barBeat(22), 2.1, .11, -.2);
add('piano', 81, barBeat(22) + .04, 2.0, .065, .18);
add('flute', 78, barBeat(22) + .65, 4.4, .084, .23);
// Bar 46 has four beats: a small stumble, then the room finds its feet.
add('piano', 76, barBeat(46) + 3.1, .38, .073, -.17);
add('marimba', 73, barBeat(46) + 3.55, .28, .043, .47);
const end = barBeat(47);
add('bass', 38, end, 2.9, .11, .02);
[62,66,69,71,76].forEach((n, i) => add('piano', n, end + i * .028, 2.8, .069, -.35 + i * .15));
add('piano', 86, 145 + .2, .35, .047, .3);

// Four short, damped room reflections per side; no samples or convolution files.
for (const [data, delays] of [[L,[.0371,.0533,.0717,.0893]],[R,[.0413,.0599,.0739,.0971]]]) {
  const combs = delays.map(d=>({buf:new Float32Array(Math.round(d*SR)),at:0,low:0}));
  let previous = 0, high = 0;
  for (let i=0; i<data.length; i++) {
    const dry=data[i]; let room=0;
    for(const c of combs) { const z=c.buf[c.at]; c.low=.68*c.low+.32*z; c.buf[c.at]=dry+c.low*.63; c.at=(c.at+1)%c.buf.length; room+=z; }
    const x=dry*.87+room*.053;
    high=x-previous+.996*high; previous=x;
    data[i]=Math.tanh(high*1.12)/1.12;
  }
}
let peak=0, sum=0;
for(let i=0;i<L.length;i++){peak=Math.max(peak,Math.abs(L[i]),Math.abs(R[i]));sum+=L[i]*L[i]+R[i]*R[i];}
const scale=.87/peak;
const wav=Buffer.alloc(44+L.length*4);
wav.write('RIFF',0);wav.writeUInt32LE(wav.length-8,4);wav.write('WAVEfmt ',8);wav.writeUInt32LE(16,16);
wav.writeUInt16LE(1,20);wav.writeUInt16LE(2,22);wav.writeUInt32LE(SR,24);wav.writeUInt32LE(SR*4,28);
wav.writeUInt16LE(4,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(L.length*4,40);
for(let i=0;i<L.length;i++) {const fade=Math.min(1,i/(SR*.012),(L.length-i)/(SR*.4));wav.writeInt16LE(Math.round(L[i]*scale*fade*32767),44+i*4);wav.writeInt16LE(Math.round(R[i]*scale*fade*32767),46+i*4);}
fs.writeFileSync(path.join(dir,'a-window-before-the-wall.wav'),wav);

// Export the editable notes as Standard MIDI, alongside the exact synthesis source.
const programs={piano:[0,10],bass:[1,32],pizz:[2,45],marimba:[3,12],glass:[4,89],flute:[5,73],kick:[9,0],brush:[9,0],shaker:[9,0]};
const midi=[{t:0,b:[0xff,0x51,3,0x09,0x89,0x68]},{t:0,b:[0xff,0x58,4,3,2,24,8]},{t:0,b:[0xff,0x59,2,2,0]}];
for(const [ch,program] of Object.values(programs))if(ch!==9)midi.push({t:0,b:[0xc0|ch,program]});
for(const e of events){const ch=programs[e.instrument][0],t=Math.max(0,Math.round(e.beat*480));midi.push({t,b:[0x90|ch,e.pitch,Math.max(1,e.velocity)]},{t:Math.round((e.beat+e.length)*480),b:[0x80|ch,e.pitch,0]});}
midi.push({t:138*480,b:[0xff,0x58,4,4,2,24,8]},{t:142*480,b:[0xff,0x58,4,3,2,24,8]});
midi.sort((a,b)=>a.t-b.t);
const vlq=n=>{const b=[n&127];while((n>>>=7)>0)b.unshift((n&127)|128);return b;};
let last=0;const track=[];for(const e of midi){track.push(...vlq(e.t-last),...e.b);last=e.t;}track.push(0,0xff,0x2f,0);
const mh=Buffer.alloc(22);mh.write('MThd');mh.writeUInt32BE(6,4);mh.writeUInt16BE(0,8);mh.writeUInt16BE(1,10);mh.writeUInt16BE(480,12);mh.write('MTrk',14);mh.writeUInt32BE(track.length,18);
fs.writeFileSync(path.join(dir,'a-window-before-the-wall.mid'),Buffer.concat([mh,Buffer.from(track)]));
console.log(JSON.stringify({title:'A Window Before the Wall',bpm:BPM,meter:'3/4; one 4/4 bar',duration_seconds:duration,events:events.length,sample_rate:SR,peak_after_normalization:.87,rms_db:20*Math.log10(Math.sqrt(sum/(L.length*2))*scale),wav:path.join(dir,'a-window-before-the-wall.wav'),midi:path.join(dir,'a-window-before-the-wall.mid')}));
