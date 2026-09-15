import fs from 'node:fs';

// Cairn's small instrumental room. All waveforms are computed; no sample assets.
export const SR = 44100;
const TAU = 2 * Math.PI;
export const instruments = {
  toy: {channel:0, program:10, tail:1.6}, felt:{channel:1,program:0,tail:2.4},
  bass:{channel:2,program:32,tail:.55}, pizz:{channel:3,program:45,tail:.4},
  marimba:{channel:4,program:12,tail:1.1}, glass:{channel:5,program:89,tail:1.2},
  flute:{channel:6,program:73,tail:.6}, vibes:{channel:7,program:11,tail:2.8},
  reed:{channel:8,program:71,tail:.5}, pad:{channel:10,program:89,tail:2.6},
  pluck:{channel:11,program:24,tail:1.0}, organ:{channel:12,program:16,tail:.3},
  kick:{channel:9,pitch:36,tail:.22}, brush:{channel:9,pitch:38,tail:.28},
  hat:{channel:9,pitch:42,tail:.08}, wood:{channel:9,pitch:76,tail:.12},
};
export function random(seed) {return ()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)/4294967296;};}
export function pitch(n) {
  if(typeof n==='number')return n;
  const m=/^([A-G])([#b]?)(-?\d)$/.exec(n);
  if(!m)throw Error('Bad pitch '+n);
  return 12*(Number(m[3])+1)+({C:0,D:2,E:4,F:5,G:7,A:9,B:11})[m[1]]+(m[2]==='#'?1:m[2]==='b'?-1:0);
}
export function clock(score) {
  const changes=[{beat:0,bpm:score.bpm},...(score.tempoChanges||[])].sort((a,b)=>a.beat-b.beat);
  return b=>{let seconds=0;for(let i=0;i<changes.length;i++){const from=changes[i].beat,to=changes[i+1]?.beat??Infinity;if(b<=from)break;seconds+=(Math.min(b,to)-from)*60/changes[i].bpm;}return seconds;};
}
export function validate(score) {
  if(!score.events.length)throw Error('Empty score');
  for(const e of score.events){if(!instruments[e.voice]||![e.at,e.len,e.pitch,e.gain,e.pan].every(Number.isFinite)||e.at<0||e.len<=0||e.pitch<0||e.pitch>127||e.pan < -1||e.pan>1)throw Error('Invalid event '+JSON.stringify(e));}
}
export function render(score, destination) {
  validate(score);
  const seconds=clock(score), duration=seconds(score.endBeat)+score.tail+0.12;
  const L=new Float32Array(Math.ceil(duration*SR)),R=new Float32Array(L.length);
  const rand=random(score.seed^0xcafe9121),hz=n=>440*2**((n-69)/12);
  for(const e of score.events){
    const p=instruments[e.voice],hold=seconds(e.at+e.len)-seconds(e.at),tail=p.tail;
    const begin=Math.round((seconds(e.at)+.12)*SR),stop=Math.min(L.length,begin+Math.ceil((hold+tail)*SR));
    const f=hz(e.pitch),left=Math.cos((e.pan+1)*Math.PI/4),right=Math.sin((e.pan+1)*Math.PI/4);
    let phase=0,low=0;
    for(let i=begin;i<stop;i++){
      const t=(i-begin)/SR,w=TAU*f*t,release=Math.exp(-Math.max(0,t-hold)/Math.max(.035,tail/5));
      let v=0;
      switch(e.voice){
      case 'toy':
        v=(.76*Math.sin(w)*Math.exp(-1.8*t)+.28*Math.sin(w*2.012)*Math.exp(-3.8*t)+.14*Math.sin(w*3.99)*Math.exp(-6.5*t)+.07*Math.sin(w*6.08)*Math.exp(-10*t))*(1-Math.exp(-650*t))*release;break;
      case 'felt':
        v=(Math.sin(w)*Math.exp(-.8*t)+.25*Math.sin(w*2.001)*Math.exp(-2.1*t)+.08*Math.sin(w*3.007)*Math.exp(-4.5*t))*(1-Math.exp(-180*t))*release;break;
      case 'bass':
        v=(Math.sin(w)+.32*Math.sin(2*w)*Math.exp(-3*t)+.11*Math.sin(3*w)*Math.exp(-5*t))*(1-Math.exp(-160*t))*Math.exp(-1.35*t)*release;break;
      case 'pizz':
        v=(Math.sin(w)+.4*Math.sin(2*w)+.21*Math.sin(3*w)+.1*Math.sin(5*w))*(1-Math.exp(-750*t))*Math.exp(-7*t)*release;break;
      case 'marimba':
        v=(Math.sin(w)*Math.exp(-3.2*t)+.3*Math.sin(4*w)*Math.exp(-12*t)+.1*Math.sin(9.15*w)*Math.exp(-23*t))*(1-Math.exp(-1000*t))*release;break;
      case 'glass':
        v=(.7*Math.sin(w+.6*Math.exp(-2.2*t)*Math.sin(2*w))+.18*Math.sin(w*1.003))*(1-Math.exp(-35*t))*Math.exp(-1.25*t)*release;break;
      case 'vibes':
        v=(Math.sin(w)+.14*Math.sin(w*3.99)*Math.exp(-3*t))*(.88+.12*Math.sin(TAU*5.2*t))*(1-Math.exp(-500*t))*Math.exp(-.55*t)*release;break;
      case 'flute':{
        const glide=e.glide?e.glide*Math.sin(Math.PI*Math.min(1,t/hold)):0;
        phase+=TAU*hz(e.pitch+glide+.045*Math.sin(TAU*5.1*t))/SR;
        low=.88*low+.12*(rand()*2-1);
        v=(Math.sin(phase)+.13*Math.sin(2*phase)+.035*low)*(1-Math.exp(-24*t))*release;break;}
      case 'reed':
        phase+=TAU*f*(1+.0016*Math.sin(TAU*4.7*t))/SR;
        v=(Math.sin(phase)+.24*Math.sin(3*phase)+.08*Math.sin(5*phase))*(1-Math.exp(-34*t))*release;break;
      case 'pad':
        v=(.45*Math.sin(w*.9987)+.45*Math.sin(w*1.0013)+.12*Math.sin(w*2.001))*(1-Math.exp(-2.7*t))*release;break;
      case 'pluck':
        v=(Math.sin(w)+.33*Math.sin(w*2)*Math.exp(-2*t)+.16*Math.sin(w*3)*Math.exp(-4*t)+.07*Math.sin(w*4)*Math.exp(-7*t))*(1-Math.exp(-700*t))*Math.exp(-2.7*t)*release;break;
      case 'organ':
        v=(.7*Math.sin(w)+.2*Math.sin(2*w)+.12*Math.sin(3*w)+.06*Math.sin(4*w))*(1-Math.exp(-75*t))*release;break;
      case 'kick':
        phase+=TAU*(46+65*Math.exp(-36*t))/SR;v=Math.sin(phase)*Math.exp(-17*t)*(1-Math.exp(-900*t));break;
      case 'brush':{
        const n=rand()*2-1;low=.76*low+.24*n;v=((n-low)*.7+low*.5)*(1-Math.exp(-180*t))*Math.exp(-19*t);break;}
      case 'hat':{
        const n=rand()*2-1;low=.91*low+.09*n;v=(n-low)*Math.exp(-55*t)*(1-Math.exp(-1400*t));break;}
      case 'wood':v=(Math.sin(TAU*780*t)+.32*Math.sin(TAU*1171*t))*Math.exp(-55*t)*(1-Math.exp(-1400*t));break;
      }
      L[i]+=v*e.gain*left;R[i]+=v*e.gain*right;
    }
  }
  const wet=score.room??.04;
  for(const [data,delays] of [[L,[.0371,.0533,.0717,.0893]],[R,[.0413,.0599,.0739,.0971]]]){
    const combs=delays.map(d=>({buf:new Float32Array(Math.round(d*SR)),at:0,low:0}));let prev=0,high=0;
    for(let i=0;i<data.length;i++){
      const dry=data[i];let room=0;
      for(const c of combs){const z=c.buf[c.at];c.low=.68*c.low+.32*z;c.buf[c.at]=dry+c.low*.61;c.at=(c.at+1)%c.buf.length;room+=z;}
      const x=dry*.89+room*wet;high=x-prev+.997*high;prev=x;data[i]=Math.tanh(high*1.1)/1.1;
    }
  }
  let peak=0,energy=0;
  for(let i=0;i<L.length;i++){if(!Number.isFinite(L[i]+R[i]))throw Error('Non-finite audio');peak=Math.max(peak,Math.abs(L[i]),Math.abs(R[i]));energy+=L[i]*L[i]+R[i]*R[i];}
  if(peak<1e-5)throw Error('Silent render');
  const scale=.8/peak,out=Buffer.alloc(44+L.length*4);
  out.write('RIFF',0);out.writeUInt32LE(out.length-8,4);out.write('WAVEfmt ',8);out.writeUInt32LE(16,16);out.writeUInt16LE(1,20);out.writeUInt16LE(2,22);out.writeUInt32LE(SR,24);out.writeUInt32LE(SR*4,28);out.writeUInt16LE(4,32);out.writeUInt16LE(16,34);out.write('data',36);out.writeUInt32LE(L.length*4,40);
  for(let i=0;i<L.length;i++){const fade=Math.min(1,i/(SR*.012),(L.length-i)/(SR*.5));out.writeInt16LE(Math.round(L[i]*scale*fade*32767),44+i*4);out.writeInt16LE(Math.round(R[i]*scale*fade*32767),46+i*4);}
  fs.writeFileSync(destination,out);
  return {duration,events:score.events.length,sampleRate:SR,rawPeak:.8,rawRmsDb:20*Math.log10(Math.sqrt(energy/(L.length*2))*scale)};
}

function vlq(n){const b=[n&127];while((n>>>=7)>0)b.unshift((n&127)|128);return b;}
function chunk(events){events.sort((a,b)=>a.t-b.t||(a.order||0)-(b.order||0));let last=0,bytes=[];for(const e of events){bytes.push(...vlq(e.t-last),...e.b);last=e.t;}bytes.push(0,255,47,0);const h=Buffer.alloc(8);h.write('MTrk');h.writeUInt32BE(bytes.length,4);return Buffer.concat([h,Buffer.from(bytes)]);}
const textEvent=(type,s)=>{const b=Buffer.from(s,'utf8');return[255,type,...vlq(b.length),...b];};
export function midi(score,destination){
  const ppq=480,meta=[{t:0,b:textEvent(3,score.title)},{t:0,b:[255,88,4,score.meter[0],Math.log2(score.meter[1]),24,8]}];
  for(const c of [{beat:0,bpm:score.bpm},...(score.tempoChanges||[])]){const us=Math.round(60000000/c.bpm);meta.push({t:Math.round(c.beat*ppq),b:[255,81,3,(us>>16)&255,(us>>8)&255,us&255]});}
  for(const s of score.sections||[])meta.push({t:Math.round(s.beat*ppq),b:textEvent(6,s.name)});
  const tracks=[chunk(meta)];
  for(const voice of [...new Set(score.events.map(e=>e.voice))]){
    const inst=instruments[voice],ch=inst.channel,es=[{t:0,b:textEvent(3,voice)}];
    if(ch!==9)es.push({t:0,b:[192|ch,inst.program]});
    for(const e of score.events.filter(e=>e.voice===voice)){const velocity=Math.max(1,Math.min(112,Math.round(e.gain*420)));const n=inst.pitch??e.pitch;es.push({t:Math.round(e.at*ppq),order:1,b:[144|ch,n,velocity]},{t:Math.round((e.at+e.len)*ppq),order:-1,b:[128|ch,n,0]});}
    tracks.push(chunk(es));
  }
  const h=Buffer.alloc(14);h.write('MThd');h.writeUInt32BE(6,4);h.writeUInt16BE(1,8);h.writeUInt16BE(tracks.length,10);h.writeUInt16BE(ppq,12);fs.writeFileSync(destination,Buffer.concat([h,...tracks]));
}
