import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {album,tracks,compose} from './scores.mjs';
import {render,midi} from './synth.mjs';

const here=path.dirname(fileURLToPath(import.meta.url)),root=path.dirname(here);
for(const d of ['mp3','wav','midi','scores','checks','art'])fs.mkdirSync(path.join(root,d),{recursive:true});
function run(cmd,args){const p=spawnSync(cmd,args,{encoding:'utf8',maxBuffer:16*1024*1024});if(p.status!==0)throw Error(cmd+' failed: '+p.stderr);return p;}
function hash(file){return createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function saveMidi(candidate,destination){
  if(fs.existsSync(destination)){
    if(hash(candidate)!==hash(destination))throw Error('Existing MIDI differs from this score; refusing to replace edits: '+destination);
    fs.unlinkSync(candidate);
  }else fs.renameSync(candidate,destination);
}
function statsFrom(stderr){const matches=stderr.match(/\{\s*"input_i"[\s\S]*?\}/g);if(!matches?.length)throw Error('Missing loudness measurement');const j=JSON.parse(matches.at(-1));for(const k of ['input_i','input_tp','input_lra','input_thresh','target_offset'])if(!Number.isFinite(Number(j[k])))throw Error('Non-finite loudness measurement');return j;}
const requested=process.argv.find(a=>a.startsWith('--tracks='));
const selection=requested?requested.split('=')[1].split(',').map(Number):tracks.map(t=>t.number);
for(const t of tracks.filter(t=>selection.includes(t.number))){
  const stem=String(t.number).padStart(2,'0')+'-'+t.slug;
  const wav=path.join(root,'wav',stem+'.wav'),mp3=path.join(root,'mp3',stem+'.mp3'),mid=path.join(root,'midi',stem+'.mid');
  if([wav,mp3].some(p=>fs.existsSync(p)))throw Error('Audio output already exists; refusing to overwrite '+stem);
  const temp=fs.mkdtempSync(path.join(os.tmpdir(),'cairn-album-'));
  const raw=path.join(temp,'raw.wav');let synthesis;
  try{
    console.log(JSON.stringify({track:t.number,status:'rendering',title:t.title}));
    if(t.original){
      fs.copyFileSync(path.join(here,'01-original.mjs'),path.join(temp,'original.mjs'));
      const result=run(process.execPath,[path.join(temp,'original.mjs')]);
      synthesis=JSON.parse(result.stdout.trim());
      fs.renameSync(path.join(temp,'a-window-before-the-wall.wav'),raw);
      saveMidi(path.join(temp,'a-window-before-the-wall.mid'),mid);
    }else{
      const score=compose(t);synthesis=render(score,raw);midi(score,path.join(temp,'score.mid'));saveMidi(path.join(temp,'score.mid'),mid);
      fs.writeFileSync(path.join(root,'scores',stem+'.json'),JSON.stringify(score,null,2)+'\n');
    }
    const measurement=statsFrom(run('ffmpeg',['-hide_banner','-nostats','-i',raw,'-af','loudnorm=I=-18:TP=-1.5:LRA=14:print_format=json','-f','null','-']).stderr);
    const filter=`loudnorm=I=-18:TP=-1.5:LRA=14:measured_I=${measurement.input_i}:measured_TP=${measurement.input_tp}:measured_LRA=${measurement.input_lra}:measured_thresh=${measurement.input_thresh}:offset=${measurement.target_offset}:linear=true:print_format=json`;
    const mastered=statsFrom(run('ffmpeg',['-hide_banner','-nostats','-i',raw,'-af',filter,'-ar','44100','-ac','2','-c:a','pcm_s16le',wav]).stderr);
    const cover=path.join(root,'art','cover.png');
    const args=['-hide_banner','-loglevel','error','-i',wav];
    if(fs.existsSync(cover))args.push('-i',cover,'-map','0:a:0','-map','1:v:0','-c:v','png','-disposition:v','attached_pic');
    args.push('-c:a','libmp3lame','-q:a','2','-id3v2_version','3','-metadata','title='+t.title,'-metadata','artist='+album.artist,'-metadata','album='+album.title,'-metadata','track='+t.number+'/8','-metadata','date=2026','-metadata','genre=Instrumental','-metadata','comment=Original composition and deterministic synthesis by Cairn. Locally produced; no samples or music-generation service.',mp3);
    run('ffmpeg',args);
    run('ffmpeg',['-v','error','-i',mp3,'-map','0:a:0','-f','null','-']);
    const probe=JSON.parse(run('ffprobe',['-v','error','-select_streams','a:0','-show_entries','format=duration,size:stream=sample_rate,channels','-of','json',mp3]).stdout);
    const check={track:t.number,title:t.title,stem,bpm:t.bpm,meter:t.meter,seconds:Number(probe.format.duration),bytes:Number(probe.format.size),synthesis:{events:synthesis.events,sampleRate:44100},mastering:{targetIntegratedLufs:-18,targetTruePeakDb:-1.5,measuredSource:measurement,result:mastered},verification:{mp3Decodes:true,channels:probe.streams[0].channels,sampleRate:Number(probe.streams[0].sample_rate),sha256:{wav:hash(wav),mp3:hash(mp3),midi:hash(mid)}},note:t.note};
    fs.writeFileSync(path.join(root,'checks',stem+'.json'),JSON.stringify(check,null,2)+'\n');
    console.log(JSON.stringify({track:t.number,status:'complete',seconds:check.seconds,lufs:mastered.output_i,truePeak:mastered.output_tp}));
  }finally{
    // Only these known, newly generated intermediate files are disposable.
    for(const name of ['raw.wav','original.mjs','score.mid','a-window-before-the-wall.wav','a-window-before-the-wall.mid']){const p=path.join(temp,name);if(fs.existsSync(p))fs.unlinkSync(p);}
    if(fs.readdirSync(temp).length===0)fs.rmdirSync(temp);
  }
}
