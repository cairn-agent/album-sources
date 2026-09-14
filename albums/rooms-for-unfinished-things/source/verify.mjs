import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {tracks,compose} from './scores.mjs';
import {clock} from './synth.mjs';

const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const assert=(ok,msg)=>{if(!ok)throw Error(msg);};
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const run=(cmd,args)=>{const p=spawnSync(cmd,args,{cwd:root,encoding:'utf8',maxBuffer:8*1024*1024});assert(p.status===0,p.stderr||p.stdout);return p;};
function wave(p){
  const b=fs.readFileSync(p);assert(b.toString('ascii',0,4)==='RIFF'&&b.toString('ascii',8,12)==='WAVE','Invalid WAV');
  let data,fmt;for(let at=12;at+8<=b.length;){const tag=b.toString('ascii',at,at+4),size=b.readUInt32LE(at+4);assert(at+8+size<=b.length,'Truncated WAV chunk');if(tag==='fmt ')fmt=b.subarray(at+8,at+8+size);if(tag==='data')data=b.subarray(at+8,at+8+size);at+=8+size+(size%2);}
  assert(data&&fmt,'Missing WAV chunks');assert(fmt.readUInt16LE(0)===1&&fmt.readUInt16LE(2)===2&&fmt.readUInt32LE(4)===44100&&fmt.readUInt16LE(14)===16,'Wrong master format');
  let peak=0,energy=0,first=-1,last=-1,maxQuiet=0,quiet=0;
  const block=44100*4/2;
  for(let at=0;at<data.length;at+=block){let power=0,count=0;
    for(let i=at;i<Math.min(at+block,data.length);i+=2){const v=data.readInt16LE(i)/32768;peak=Math.max(peak,Math.abs(v));power+=v*v;energy+=v*v;count++;}
    if(Math.sqrt(power/count)>10**(-65/20)){if(first<0)first=at/(44100*4);last=(at+Math.min(block,data.length-at))/(44100*4);maxQuiet=Math.max(maxQuiet,quiet);quiet=0;}else if(first>=0)quiet+=count/88200;
  }
  const seconds=data.length/(44100*4),peakDb=20*Math.log10(peak);
  assert(first>=0&&last>first,'Silent master');assert(first<1.2,'Unexpected long leading silence');assert(maxQuiet<5,'Unexpected long internal silence');assert(peakDb< -1.0,'Insufficient peak headroom');
  return{seconds,peakDb,rmsDb:20*Math.log10(Math.sqrt(energy/(data.length/2))),leadingSilence:first,trailingSilence:seconds-last,maxInternalQuiet:maxQuiet};
}
function midiCheck(p){
  const b=fs.readFileSync(p);assert(b.toString('ascii',0,4)==='MThd','Missing MIDI header');const count=b.readUInt16BE(10);let at=8+b.readUInt32BE(4),ons=0,offs=0,tempo=0;
  for(let tr=0;tr<count;tr++){
    assert(b.toString('ascii',at,at+4)==='MTrk','Missing MIDI track');const end=at+8+b.readUInt32BE(at+4);at+=8;let active=new Map();
    const readVar=()=>{let n=0,k=0,v;do{assert(at<end&&k++<4,'Bad MIDI delta');v=b[at++];n=(n<<7)|(v&127);}while(v&128);return n;};
    while(at<end){readVar();const status=b[at++];assert(status>=128,'Unexpected running status');
      if(status===255){const type=b[at++],len=readVar();if(type===81)tempo++;at+=len;}
      else if(status===240||status===247)at+=readVar();
      else{const kind=status&240,ch=status&15,n=b[at++];if(kind===192||kind===208)continue;const v=b[at++];if(kind===144&&v>0){ons++;const key=ch+':'+n;active.set(key,(active.get(key)||0)+1);}else if(kind===128||(kind===144&&v===0)){offs++;const key=ch+':'+n;assert((active.get(key)||0)>0,'MIDI note-off without note-on');active.set(key,active.get(key)-1);}}
      assert(at<=end,'Truncated MIDI event');
    }
    assert([...active.values()].every(n=>n===0),'Hanging MIDI notes');
  }
  assert(at===b.length&&ons>0&&ons===offs&&tempo>0,'MIDI validation failed');return{tracks:count,noteOns:ons,noteOffs:offs,tempoEvents:tempo};
}

const manifest=JSON.parse(fs.readFileSync(path.join(root,'album.json'),'utf8')),results=[];
assert(manifest.tracks.length===8&&manifest.localOnly===true,'Wrong album scope');
for(const t of manifest.tracks){
  for(const ext of ['wav','mp3','midi'])assert(hash(path.join(root,t[ext]))===t.sha256[ext],'Hash mismatch: '+t.title+' '+ext);
  const w=wave(path.join(root,t.wav)),m=midiCheck(path.join(root,t.midi));
  assert(Math.abs(w.seconds-t.durationSeconds)<.1,'Unexpected track duration');
  if(t.number!==1){const s=compose(tracks.find(x=>x.number===t.number));assert(m.noteOns===s.events.length,'MIDI lost score notes');assert(Math.abs(clock(s)(s.endBeat)+s.tail+.12-w.seconds)<.01,'Score duration mismatch');}
  run('ffmpeg',['-v','error','-i',t.mp3,'-map','0:a:0','-f','null','-']);
  const metadata=JSON.parse(run('ffprobe',['-v','error','-show_entries','format_tags=title,artist,album,track:stream=codec_type:stream_disposition=attached_pic','-of','json',t.mp3]).stdout);
  assert(metadata.format.tags.title===t.title&&metadata.format.tags.artist==='Cairn'&&metadata.format.tags.album===manifest.title,'Incorrect MP3 tags');
  assert(metadata.streams.some(s=>s.codec_type==='video'&&s.disposition.attached_pic===1),'Missing embedded cover');
  const measured=run('ffmpeg',['-hide_banner','-nostats','-i',t.mp3,'-map','0:a:0','-af','loudnorm=I=-18:TP=-1.5:LRA=14:print_format=json','-f','null','-']).stderr.match(/\{\s*"input_i"[\s\S]*?\}/g);
  const loud=JSON.parse(measured.at(-1));assert(Math.abs(Number(loud.input_i)+18)<.65,'Unexpected MP3 loudness');assert(Number(loud.input_tp)< -1,'MP3 true peak too high');
  results.push({track:t.number,title:t.title,wave:w,midi:m,mp3:{decoded:true,integratedLufs:Number(loud.input_i),truePeakDb:Number(loud.input_tp),metadataVerified:true,coverVerified:true}});
  console.log(JSON.stringify({track:t.number,verified:true,seconds:w.seconds,lufs:loud.input_i}));
}
run('ffmpeg',['-v','error','-i',manifest.completeAlbum,'-map','0:a:0','-f','null','-']);
const full=JSON.parse(run('ffprobe',['-v','error','-show_entries','format=duration','-of','json',manifest.completeAlbum]).stdout);
assert(Math.abs(Number(full.format.duration)-manifest.totalSeconds)<1,'Continuous album duration mismatch');
for(const zip of ['rooms-for-unfinished-things-listening-edition.zip','rooms-for-unfinished-things-studio-sources.zip'])run('unzip',['-t',zip]);
const verification={status:'passed',scope:'Local files only; no network or uploads',tracks:results,totalSeconds:manifest.totalSeconds,continuousAlbum:{decoded:true,seconds:Number(full.format.duration)},archives:'Both archives passed integrity checks',listening:'Technical verification, not a claim of human listening review.'};
fs.writeFileSync(path.join(root,'checks','verification.json'),JSON.stringify(verification,null,2)+'\n');
console.log(JSON.stringify({status:'passed',tracks:8,totalSeconds:manifest.totalSeconds,continuousAlbumSeconds:Number(full.format.duration)}));
