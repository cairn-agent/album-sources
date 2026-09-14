"""Export recording-bound timed lyrics for a future site, without site mutations.

Canonical timings come from the rendered phoneme events, including the 40 ms
engine entrance offset. Outputs: structured JSON, WebVTT, karaoke WebVTT, LRC.
"""
from pathlib import Path
from collections import defaultdict
from html import escape
import copy,hashlib,json,math,shutil,wave,zipfile
from build import run
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'lyrics/site-export'
RELEASE='windows-still-lit'
SR=44100
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def ms(sample):return int(math.floor(sample*1000/SR+.5))
def sample(beat,bpm):return int(math.floor((round(beat,6)*(60/bpm)+.04)*SR+.5))
def stamp(m):
 h,m=divmod(m,3600000);minute,m=divmod(m,60000);s,m=divmod(m,1000);return f'{h:02d}:{minute:02d}:{s:02d}.{m:03d}'
def timing(start,end):return dict(start_sample=start,end_sample=end,start_ms=ms(start),end_ms=ms(end))
def vtt(cues,karaoke=False):
 out=['WEBVTT','']
 for c in sorted(cues,key=lambda x:(x['start_ms'],x['id'])):
  text=escape(c['text'],quote=False)
  if karaoke:
   parts=[];previous=c['start_ms']
   for w in c['words']:
    at=w['start_ms'];prefix=f'<{stamp(at)}>' if previous<at<c['end_ms'] else ''
    parts.append(prefix+escape(w['text'],quote=False));previous=at
   text=' '.join(parts)
  out += [c['id'],stamp(c['start_ms'])+' --> '+stamp(c['end_ms']),f'<v {c["role"]}>{text}</v>','']
 return '\n'.join(out)+'\n'
def check_vtt(path,cues):
 if not cues:return # An empty harmony layer is a valid header-only document.
 probe=json.loads(run(['ffprobe','-v','error','-show_packets','-of','json',path]).stdout)
 assert len(probe['packets'])==len(cues),(path,'caption parse failure')
 for packet,c in zip(probe['packets'],sorted(cues,key=lambda x:(x['start_ms'],x['id']))):
  assert abs(float(packet['pts_time'])*1000-c['start_ms'])<.01
  assert abs(float(packet['duration_time'])*1000-(c['end_ms']-c['start_ms']))<.01
def track_export(t,score):
 bpm=t['bpm'];stem=t['stem'];events=score['events'];voice_map={int(k):v.split(' / ')[-1] for k,v in score['voices'].items() if int(k)>=40}
 for kind in ['wav','mp3']:assert sha(ROOT/t[kind])==t['sha256'][kind],('Audio changed',stem,kind)
 tsv=(ROOT/'scores'/f'{stem}.tsv').read_bytes()
 check=json.loads((ROOT/'checks'/f'{stem}.json').read_text())
 assert hashlib.sha256(tsv+(ROOT/'source/engine.cpp').read_bytes()).hexdigest()==check['renderFingerprint'],('Stale render',stem)
 assert [[float(x) for x in line.split()] for line in tsv.decode().splitlines()[1:]]==events,('Score differs from rendered TSV',stem)
 with wave.open(str(ROOT/t['wav']),'rb') as f:frames=f.getnframes();assert f.getframerate()==SR
 taken=set();words=[]
 for wi,w in enumerate(score['vocalWords']):
  # Match the actual event sequence rather than estimating consonant alignment.
  candidates=[(i,e) for i,e in enumerate(events) if i not in taken and e[2]>=40 and e[3]==w['note'] and w['at']-1e-5<=e[0]<w['at']+w['length']+.006]
  candidates.sort(key=lambda z:z[1][0]);phones=[]
  assert len(candidates)==len(w['phonemes']),(stem,w,candidates)
  for (ei,e),expected in zip(candidates,w['phonemes']):
   assert voice_map[e[2]]==expected,(stem,w,expected,e)
   start=sample(e[0],bpm)
   # The engine's final phoneme fade reaches zero at hold + 12 ms.
   end=start+int(math.ceil((e[1]*(60/bpm)+.012)*SR))
   phones.append(dict(symbol=expected,**timing(start,end)));taken.add(ei)
  start=phones[0]['start_sample'];end=max(p['end_sample'] for p in phones)
  words.append(dict(id=f'{stem}/word/{wi+1:04d}',text=w['word'],role='chop' if w['chop'] else w['part'],note_midi=w['note'],**timing(start,end),phonemes=phones,source_beat=w['at']))
 assert len(taken)==sum(e[2]>=40 for e in events)
 cues=[];assigned=set();counts=defaultdict(int)
 for line in score['vocalLines']:
  role=line['part'];selected=[(i,w) for i,w in enumerate(words) if w['role']==role and line['at']-1e-5<=w['source_beat']<line['at']+line['length']-.00001]
  tokens=line['text'].split();assert [w['text'] for _,w in selected]==[s.lower() for s in tokens],(stem,line,selected)
  copies=[]
  for (i,w),token in zip(selected,tokens):
   assert i not in assigned;assigned.add(i);w=copy.deepcopy(w);w['text']=token;del w['source_beat'];copies.append(w)
  counts[role]+=1
  cues.append(dict(id=f'{stem}/{role}/{counts[role]:03d}',role=role,text=line['text'],**timing(sample(line['at'],bpm),max(sample(line['at']+line['length'],bpm),copies[-1]['end_sample'])),words=copies))
 for i,w in enumerate(words):
  if w['role']!='chop':continue
  assigned.add(i);counts['chop']+=1;w=copy.deepcopy(w);del w['source_beat']
  cues.append(dict(id=f'{stem}/chop/{counts["chop"]:03d}',role='chop',text=w['text'],**timing(w['start_sample'],w['end_sample']),words=[w]))
 assert len(assigned)==len(words)
 cues.sort(key=lambda c:(c['start_sample'],c['role']))
 return dict(schema_version='1.0.0',document_type='timed_lyrics',release_key=RELEASE,track_key=stem,title=t['title'],artist='Cairn',language='en',time_unit='milliseconds',sample_rate=SR,duration_samples=frames,duration_ms=ms(frames),recording=dict(id='sha256:'+t['sha256']['wav'],revision=1,canonical_format='wav',audio_assets=[dict(format=k,album_relative_path=t[k],sha256=t['sha256'][k]) for k in ['wav','mp3']]),alignment=dict(method='composer_authored_render_events',audio_zero='first decoded PCM sample',render_offset_ms=40,intervals='start inclusive; end exclusive',vocal_release_ms=12,reverb_tails_excluded=True,manually_listening_verified=False),cues=cues)
def validate(d):
 ids=set();wordids=set()
 for c in d['cues']:
  assert c['id'] not in ids;ids.add(c['id'])
  assert c['role'] in ['lead','harmony','chop'] and 0<=c['start_sample']<c['end_sample']<=d['duration_samples']
  assert c['text']==' '.join(w['text'] for w in c['words'])
  for item in [c]+c['words']+[p for w in c['words'] for p in w['phonemes']]:
   assert item['start_ms']==ms(item['start_sample']) and item['end_ms']==ms(item['end_sample'])
  for w in c['words']:
   assert w['id'] not in wordids;wordids.add(w['id'])
   assert c['start_sample']<=w['start_sample']<w['end_sample']<=c['end_sample']
   assert w['phonemes']
   for ph in w['phonemes']:assert w['start_sample']<=ph['start_sample']<ph['end_sample']<=w['end_sample']
def shift(c,offset):
 c=copy.deepcopy(c)
 for item in [c]+c['words']+[p for w in c['words'] for p in w['phonemes']]:
  item.update(timing(item['start_sample']+offset,item['end_sample']+offset))
 return c
def main():
 for folder in ['tracks','captions','lrc']:(OUT/folder).mkdir(parents=True,exist_ok=True)
 album=json.loads((ROOT/'album.json').read_text());entries=[];allcues=[];offset=0
 assert sha(ROOT/album['completeAlbum'])==album['completeAlbumSha256'],'Full album changed'
 shutil.copyfile(ROOT/'lyrics/phonemes.json',OUT/'phonemes.json')
 for t in album['tracks']:
  s=json.loads((ROOT/'scores'/f'{t["stem"]}.json').read_text());d=track_export(t,s);validate(d);stem=t['stem']
  j=OUT/'tracks'/f'{stem}.json';write(j,d)
  default=[c for c in d['cues'] if c['role'] in ['lead','chop']];harmony=[c for c in d['cues'] if c['role']=='harmony']
  files=[]
  for suffix,cues,karaoke in [('.vtt',default,False),('.karaoke.vtt',default,True),('.harmony.vtt',harmony,False)]:
   p=OUT/'captions'/f'{stem}{suffix}';p.write_text(vtt(cues,karaoke));files.append(p)
   check_vtt(p,cues)
  lrc=OUT/'lrc'/f'{stem}.lrc'
  def lrcstamp(m):
   centiseconds=(m+5)//10;minutes,seconds=divmod(centiseconds,6000)
   return f'{minutes:02d}:{seconds//100:02d}.{seconds%100:02d}'
  lrc.write_text(f'[ar:Cairn]\n[al:{album["title"]}]\n[ti:{t["title"]}]\n[offset:0]\n'+''.join(f'[{lrcstamp(c["start_ms"])}]{c["text"]}\n' for c in default))
  shutil.copyfile(lrc,ROOT/'lyrics'/lrc.name)
  files.extend([j,lrc]);allcues.extend(shift(c,offset) for c in d['cues'])
  entries.append(dict(track_key=stem,number=t['number'],title=t['title'],recording=d['recording'],duration_ms=d['duration_ms'],full_album_start_sample=offset,full_album_start_ms=ms(offset),assets=[dict(path=str(p.relative_to(OUT)),media_type='application/json' if p.suffix=='.json' else 'text/vtt' if p.suffix=='.vtt' else 'text/plain',sha256=sha(p)) for p in files]))
  offset+=d['duration_samples'];print('Exported:',t['title'],len(d['cues']),'cues',flush=True)
 complete=copy.deepcopy(d);complete.update(track_key=RELEASE+'-full-album',title=album['title'],duration_samples=offset,duration_ms=ms(offset),recording=dict(id='sha256:'+album['completeAlbumSha256'],revision=1,canonical_format='mp3',audio_assets=[dict(format='mp3',album_relative_path=album['completeAlbum'],sha256=album['completeAlbumSha256'])]),cues=allcues)
 complete['alignment']['track_offset_source']='exact concatenated WAV frame counts; per-track 40 ms render offset already included'
 validate(complete);write(OUT/'full-album.json',complete)
 fullcues=[c for c in allcues if c['role'] in ['lead','chop']]
 (OUT/'captions/full-album.vtt').write_text(vtt(fullcues));check_vtt(OUT/'captions/full-album.vtt',fullcues)
 manifest=dict(schema_version='1.0.0',release_key=RELEASE,title=album['title'],artist='Cairn',language='en',time_unit='milliseconds',path_base='export directory; audio_assets paths are relative to album root',schema='timed-lyrics.schema.json',integration_guide='INTEGRATION.md',phoneme_dictionary='phonemes.json',tracks=entries,full_album=dict(json='full-album.json',vtt='captions/full-album.vtt',audio_file=album['completeAlbum'],audio_sha256=album['completeAlbumSha256'],assets=[dict(path=str(p.relative_to(OUT)),sha256=sha(p)) for p in [OUT/'full-album.json',OUT/'captions/full-album.vtt']]))
 write(OUT/'manifest.json',manifest)
 report=dict(passed=True,tracks=len(entries),cues=len(allcues),words=sum(len(c['words']) for c in allcues),phonemes=sum(len(w['phonemes']) for c in allcues for w in c['words']),canonicalTimeline='decoded PCM, 44.1 kHz, including 40 ms entrance offset',checks=['every rendered phoneme assigned once','every word assigned once','cue/word/phoneme bounds and ms/sample agreement','lead/harmony/chop roles retained','all nonempty WebVTT files parsed by FFprobe with exact cue times','WAV, MP3 and complete-album hashes verified against actual files','score events match rendered TSV and render fingerprint','full-album offsets use exact WAV sample counts'])
 write(ROOT/'checks/lyrics-export.json',report)
 # Refresh typed references without claiming IDs or capabilities on the future site.
 for t in album['tracks']:t['timedLyrics']=dict(json=f'lyrics/site-export/tracks/{t["stem"]}.json',webvtt=f'lyrics/site-export/captions/{t["stem"]}.vtt',karaokeWebvtt=f'lyrics/site-export/captions/{t["stem"]}.karaoke.vtt',lrc=f'lyrics/site-export/lrc/{t["stem"]}.lrc',schemaVersion='1.0.0')
 album['timedLyricsManifest']='lyrics/site-export/manifest.json';write(ROOT/'album.json',album)
 archive=ROOT/f'{RELEASE}-timed-lyrics.zip'
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for p in sorted(OUT.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(OUT))
  z.write(ROOT/'checks/lyrics-export.json','checks/lyrics-export.json')
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 print('Timed lyric export complete:',archive,flush=True)
if __name__=='__main__':main()
