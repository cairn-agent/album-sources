import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {album,tracks} from './scores.mjs';

const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const run=(cmd,args)=>{const p=spawnSync(cmd,args,{cwd:root,encoding:'utf8',maxBuffer:8*1024*1024});if(p.status!==0)throw Error(p.stderr||p.stdout);return p;};
const checks=tracks.map(t=>{const stem=String(t.number).padStart(2,'0')+'-'+t.slug;return JSON.parse(fs.readFileSync(path.join(root,'checks',stem+'.json'),'utf8'));});
const seconds=checks.reduce((s,t)=>s+t.seconds,0);
const fmt=s=>`${Math.floor(s/60)}:${String(Math.round(s%60)).padStart(2,'0')}`;
fs.writeFileSync(path.join(root,'album.m3u8'),'#EXTM3U\n'+checks.map(t=>`#EXTINF:${t.seconds.toFixed(3)},Cairn - ${t.title}\nmp3/${t.stem}.mp3`).join('\n')+'\n');
fs.writeFileSync(path.join(root,'tracklist.txt'),album.title+' — '+album.artist+'\n\n'+checks.map(t=>`${String(t.track).padStart(2,'0')}  ${fmt(t.seconds)}  ${t.title}`).join('\n')+`\n\nTotal: ${fmt(seconds)}\n`);
fs.writeFileSync(path.join(root,'checks','mp3-sha256.txt'),checks.map(t=>t.verification.sha256.mp3+'  mp3/'+t.stem+'.mp3').join('\n')+'\n');
fs.writeFileSync(path.join(root,'checks','concat.txt'),checks.map(t=>`file '../mp3/${t.stem}.mp3'`).join('\n')+'\n');
const full='rooms-for-unfinished-things-full-album.mp3';
if(fs.existsSync(path.join(root,full)))throw Error('Full album already exists; refusing overwrite.');
run('ffmpeg',['-hide_banner','-loglevel','error','-f','concat','-safe','0','-i','checks/concat.txt','-i','art/cover.png','-map','0:a:0','-map','1:v:0','-c:a','copy','-c:v','png','-disposition:v','attached_pic','-id3v2_version','3','-metadata','title=Rooms for Unfinished Things — Complete Album','-metadata','artist=Cairn','-metadata','album=Rooms for Unfinished Things','-metadata','date=2026',full]);
const manifest={...album,totalSeconds:seconds,tracks:checks.map(t=>({
  number:t.track,title:t.title,durationSeconds:t.seconds,bpm:t.bpm,meter:t.meter,
  mp3:'mp3/'+t.stem+'.mp3',wav:'wav/'+t.stem+'.wav',midi:'midi/'+t.stem+'.mid',
  sha256:t.verification.sha256
})),completeAlbum:full};
fs.writeFileSync(path.join(root,'album.json'),JSON.stringify(manifest,null,2)+'\n');
for(const file of ['rooms-for-unfinished-things-listening-edition.zip','rooms-for-unfinished-things-studio-sources.zip'])if(fs.existsSync(path.join(root,file)))throw Error('Archive already exists: '+file);
run('zip',['-q','-r','rooms-for-unfinished-things-listening-edition.zip','mp3','art','album.m3u8','tracklist.txt','LINER-NOTES.md','checks/mp3-sha256.txt']);
run('zip',['-q','-r','rooms-for-unfinished-things-studio-sources.zip','source','midi','scores','art','LINER-NOTES.md','tracklist.txt']);
console.log(JSON.stringify({album:album.title,tracks:checks.length,totalSeconds:seconds,displayDuration:fmt(seconds),completeAlbum:full,archives:'listening edition and studio sources'}));
