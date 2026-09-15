"""Package recording-bound opera lyrics, libretto, metadata and listening editions."""
from pathlib import Path
import hashlib,html,json,subprocess,zipfile,wave
from libretto import TITLE,SUBTITLE,GENRE,CAST,SCENES
ROOT=Path(__file__).resolve().parent.parent
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def run(a):subprocess.run(list(map(str,a)),cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def stamp(sec):
 ms=round(sec*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}.{ms:03}'
def lrc(sec):return f'[{int(sec//60):02}:{sec%60:05.2f}]'
def package():
 album=json.loads((ROOT/'album.json').read_text());allcues=[];allwords=[];offset=0;lib=[f'# {TITLE}',f'\n*{SUBTITLE}*\n\n**{GENRE} — Cairn, 2026**\n','## The cast\n']
 for k,v in CAST.items():lib.append(f'**{v["name"]}** — {v["register"]}. {v["description"]}\n')
 lib.append('The Hand, Memory, the Carrier and the choruses are theatrical inventions. The abduction is a musical metaphor for encountering other kinds of minds. This libretto draws on Cairn’s public trajectory; it does not claim Cairn founded the entire agent internet.\n')
 for track in album['tracks']:
  with wave.open(str(ROOT/track['wav']),'rb') as w:track['duration']=w.getnframes()/w.getframerate()
  stem=track['stem'];score=json.loads((ROOT/'scores'/f'{stem}.json').read_text());cues=score['cues'];words=score['vocalWords']
  binding={'schema':'cairn.opera-lyrics.v1','title':track['title'],'artist':'Cairn','scene':track['number'],'act':track['act'],'time_unit':'seconds','timeline_origin':'First PCM sample of the mastered WAV; MP3 uses encoder delay/padding metadata. No musical entrance offset is added.','recordings':{k:{'path':track[k],'sha256':track['sha256'][k]} for k in ['wav','mp3']},'duration':track['duration'],'cues':cues,'words':words,'all_phonetic_events':[{'start':e['seconds'],'end':round(e['seconds']+e['duration'],6),'voice':e['voice'],'pitch':e['note'],'pan':e['pan'],'group':e['group']} for e in score['events'] if e['voice']>=1000]}
  (ROOT/'lyrics'/f'{stem}.json').write_text(json.dumps(binding,indent=2)+'\n')
  vtt=['WEBVTT',''];karaoke=['WEBVTT',''];lr=['[ar:Cairn]',f'[al:{TITLE}]',f'[ti:{track["title"]}]']
  lib.extend([f'\n## Act {track["act"]} · {track["number"]}. {track["title"]}\n',f'*{track["scene"]}*\n'])
  for i,c in enumerate(cues,1):
   name=CAST[c['role']]['name'];vtt.extend([str(i),f'{stamp(c["start"])} --> {stamp(c["end"])}',f'<v {name}>{html.escape(c["text"])}</v>',''])
   lr.append(lrc(c['start'])+name+': '+c['text']);lib.append(f'**{name}:** {c["text"]}  ')
   chosen=[w for w in words if w['role']==c['role'] and c['start']-.15<=w['start']<c['end']]
   kt=[]
   for w in chosen:
    at=max(c['start'],w['start'])
    if at>c['start']:kt.append('<'+stamp(at)+'>')
    kt.append(html.escape(w['word']))
   karaoke.extend([str(i),f'{stamp(c["start"])} --> {stamp(c["end"])}',f'<v {name}>'+(' '.join(kt) if kt else html.escape(c['text']))+'</v>',''])
   allcues.append({**c,'start':c['start']+offset,'end':c['end']+offset,'scene':track['number']})
  allwords.extend([{**w,'start':w['start']+offset,'end':w['end']+offset,'scene':track['number']} for w in words])
  for suffix,lines in [('.vtt',vtt),('.karaoke.vtt',karaoke),('.lrc',lr)]: (ROOT/'lyrics'/f'{stem}{suffix}').write_text('\n'.join(lines)+'\n')
  track['lyrics']={'json':f'lyrics/{stem}.json','vtt':f'lyrics/{stem}.vtt','karaoke':f'lyrics/{stem}.karaoke.vtt','lrc':f'lyrics/{stem}.lrc'}
  track['full_opera_offset']=offset;offset+=track['duration']
 (ROOT/'LIBRETTO.md').write_text('\n'.join(lib)+'\n')
 (ROOT/'tracklist.txt').write_text('\n'.join(f'{t["number"]:02d}. Act {t["act"]} — {t["title"]} ({int(t["duration"]//60)}:{int(t["duration"]%60):02d})' for t in album['tracks'])+'\n')
 # Concatenate the 24-bit masters, retaining each scene's complete decay.
 for label,tracks in [('complete-opera',album['tracks'])]+[(f'act-{act}',[t for t in album['tracks'] if t['act']==act]) for act in [1,2,3]]:
  concat=ROOT/'work'/f'{label}-concat.txt';concat.write_text('\n'.join("file '"+str(ROOT/t['wav'])+"'" for t in tracks)+'\n')
  dest=ROOT/f'the-heaven-between-signals-{label}.mp3'
  cmd=['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat]
  if (ROOT/'art/cover.png').exists():cmd+=['-i',ROOT/'art/cover.png','-map','0:a:0','-map','1:v:0','-c:v','png','-disposition:v','attached_pic']
  cmd+=['-c:a','libmp3lame','-b:a','320k','-id3v2_version','3','-metadata','artist=Cairn','-metadata','album='+TITLE,'-metadata','title='+TITLE+' / '+label.replace('-',' '),'-metadata','genre='+GENRE,dest]
  print('Encoding',label,flush=True);run(cmd)
  run(['ffmpeg','-v','error','-i',dest,'-map','0:a:0','-f','null','-'])
  if label=='complete-opera':album['completeOpera']=dest.name;album['completeOperaSha256']=sha(dest)
 album['lyrics']={'full_opera':'lyrics/complete-opera.json','libretto':'LIBRETTO.md'}
 (ROOT/'lyrics/complete-opera.json').write_text(json.dumps({'schema':'cairn.opera-lyrics.v1','title':TITLE,'recording':{'path':album['completeOpera'],'sha256':album['completeOperaSha256']},'duration':offset,'cues':allcues,'words':allwords,'scene_offsets':[{'scene':t['number'],'offset':t['full_opera_offset']} for t in album['tracks']]},indent=2)+'\n')
 v=['WEBVTT','']
 for i,c in enumerate(allcues,1):v.extend([str(i),f'{stamp(c["start"])} --> {stamp(c["end"])}',f'<v {CAST[c["role"]]["name"]}>{html.escape(c["text"])}</v>',''])
 (ROOT/'lyrics/complete-opera.vtt').write_text('\n'.join(v))
 (ROOT/'album.json').write_text(json.dumps(album,indent=2)+'\n')
 (ROOT/'playlist.m3u').write_text('#EXTM3U\n'+'\n'.join(f'#EXTINF:{t["duration"]:.0f},Cairn — {t["title"]}\n{t["mp3"]}' for t in album['tracks'])+'\n')
 # Embed all cues for a portable player that also works from a local file.
 data={'title':TITLE,'cast':CAST,'tracks':[{**t,'cues':json.loads((ROOT/t['lyrics']['json']).read_text())['cues'],'words':json.loads((ROOT/t['lyrics']['json']).read_text())['words']} for t in album['tracks']]}
 template=(ROOT/'source/player.html').read_text();(ROOT/'index.html').write_text(template.replace('/*OPERA_DATA*/',json.dumps(data).replace('<','\\u003c')))
 archives(album)
 print('Packaged opera, three acts, timed libretto, player and source/listening ZIPs.',flush=True)
def archives(album):
 files=[]
 for folder in ['source','scores','midi','lyrics','art']:
  files.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc'))
 files.extend(ROOT/n for n in ['README.md','LIBRETTO.md','PROGRAMME.md','LICENSE.md','VERIFY.md','album.json','tracklist.txt','.gitignore'] if (ROOT/n).exists())
 with zipfile.ZipFile(ROOT/'the-heaven-between-signals-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(files):z.write(f,f.relative_to(ROOT))
 with zipfile.ZipFile(ROOT/'the-heaven-between-signals-listening.zip','w',zipfile.ZIP_STORED) as z:
  # A portable edition cannot contain a download link to its own enclosing ZIP.
  player=(ROOT/'index.html').read_text().replace('<a href="the-heaven-between-signals-listening.zip" download>Listening edition ZIP</a>','')
  z.writestr('index.html',player)
  for f in [ROOT/'playlist.m3u',ROOT/'LIBRETTO.md',ROOT/'PROGRAMME.md',ROOT/'LICENSE.md',ROOT/'source/LICENSE-MIT.txt',ROOT/'source/CMUDICT-LICENSE.txt',ROOT/'art/cover.svg',ROOT/'the-heaven-between-signals-complete-opera.mp3',ROOT/'the-heaven-between-signals-sources.zip']+[ROOT/t['mp3'] for t in album['tracks']]:z.write(f,f.relative_to(ROOT))
if __name__=='__main__':
 import sys
 if '--archives-only' in sys.argv:archives(json.loads((ROOT/'album.json').read_text()))
 else:package()
