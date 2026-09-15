"""Render/master the opera. Python stdlib, clang++, FFmpeg/FFprobe only.
Use --scene N for one scene. Existing completed scenes are checked and reused.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,math,subprocess,time
ROOT=Path(__file__).resolve().parent.parent
TARGET=[-18.5,-18,-17,-15.8,-21,-16,-15.8,-22,-17,-19,-15.5,-17]
def run(args):return subprocess.run(list(map(str,args)),cwd=ROOT,check=True,capture_output=True,text=True)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def render(s):
 stem=s['stem'];check=ROOT/'checks'/f'{stem}.json';wav=ROOT/'wav'/f'{stem}.wav';mp3=ROOT/'mp3'/f'{stem}.mp3';raw=ROOT/'work'/f'{stem}-raw.wav'
 signature=sha(ROOT/'source/engine.cpp')+sha(ROOT/'scores'/f'{stem}.tsv')+sha(Path(__file__))+''.join(sha(p) for p in sorted((ROOT/'source/legacy').glob('*.hpp')))
 if check.exists() and wav.exists() and mp3.exists():
  d=json.loads(check.read_text())
  if d.get('source_signature')==signature and all(sha(ROOT/d[k])==d['sha256'][k] for k in ['wav','mp3']):return d
 start=time.monotonic();print('Rendering',s['number'],s['title'],flush=True)
 p=run([ROOT/'work/astra-engine',ROOT/'scores'/f'{stem}.tsv',raw,ROOT/'work'/stem])
 (ROOT/'checks'/f'{stem}-engine.log').write_text(p.stderr)
 synthesis=json.loads(p.stdout)
 measured=run(['ffmpeg','-hide_banner','-nostats','-i',raw,'-af','loudnorm=I=-18:TP=-1.4:LRA=20:print_format=json','-f','null','-'])
 stats=json.JSONDecoder().raw_decode(measured.stderr[measured.stderr.rfind('{'):])[0]
 # One static gain preserves the written large-scale dynamics. No brickwall master.
 gain=min(TARGET[s['number']-1]-float(stats['input_i']),-1.4-float(stats['input_tp']))
 run(['ffmpeg','-v','error','-y','-i',raw,'-af',f'volume={gain:.6f}dB','-ar','44100','-ac','2','-c:a','pcm_s24le',wav])
 args=['ffmpeg','-v','error','-y','-i',wav]
 cover=ROOT/'art/cover.png'
 if cover.exists():args+=['-i',cover,'-map','0:a','-map','1:v','-c:v','png','-disposition:v','attached_pic']
 args+=['-c:a','libmp3lame','-b:a','320k','-id3v2_version','3','-metadata','artist=Cairn','-metadata','album=The Heaven Between Signals','-metadata','title='+s['title'],'-metadata',f'track={s["number"]}/12','-metadata','genre=Cairn-Bach-Astra','-metadata','date=2026','-metadata','comment=Original abduction opera in three acts. Procedural instruments and phonetic singing; no sampled voices. Code MIT; music CC BY 4.0.',mp3]
 run(args)
 stems=[]
 for kind in ['orchestra','soloists','choirs']:
  dest=ROOT/'stems'/f'{stem}-{kind}-dry.flac'
  run(['ffmpeg','-v','error','-y','-i',ROOT/'work'/f'{stem}-{kind}-dry.wav','-c:a','flac','-compression_level','8',dest]);stems.append(str(dest.relative_to(ROOT)))
 run(['ffmpeg','-v','error','-i',mp3,'-map','0:a:0','-f','null','-'])
 probe=json.loads(run(['ffprobe','-v','error','-select_streams','a:0','-show_entries','format=duration:stream=sample_rate,channels','-of','json',mp3]).stdout)
 d={**s,'artist':'Cairn','wav':str(wav.relative_to(ROOT)),'mp3':str(mp3.relative_to(ROOT)),'midi':f'midi/{stem}.mid','score':f'scores/{stem}.json','stems':stems,'source_signature':signature,'synthesis':synthesis,'mastering':{'method':'Static gain; retain compositional dynamics','source_lufs':float(stats['input_i']),'source_true_peak_db':float(stats['input_tp']),'gain_db':gain,'estimated_output_lufs':float(stats['input_i'])+gain,'estimated_output_true_peak_db':float(stats['input_tp'])+gain},'encoded_seconds':float(probe['format']['duration']),'sha256':{k:sha(ROOT/path) for k,path in [('wav',str(wav.relative_to(ROOT))),('mp3',str(mp3.relative_to(ROOT))),('midi',f'midi/{stem}.mid')]},'verification':{'mp3_decodes':True,'sample_rate':probe['streams'][0]['sample_rate'],'channels':probe['streams'][0]['channels']},'render_elapsed_seconds':round(time.monotonic()-start,2)}
 check.write_text(json.dumps(d,indent=2)+'\n');print('Finished',s['number'],s['title'],f'{d["mastering"]["estimated_output_lufs"]:.1f} LUFS',flush=True);return d
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--scene',type=int);p.add_argument('--workers',type=int,default=2);args=p.parse_args()
 for folder in ['work','checks','wav','mp3','stems']: (ROOT/folder).mkdir(exist_ok=True)
 run(['clang++','-O3','-std=c++17',ROOT/'source/engine.cpp','-o',ROOT/'work/astra-engine'])
 m=json.loads((ROOT/'scores/manifest.json').read_text());selected=[s for s in m['scenes'] if not args.scene or s['number']==args.scene]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:records=list(pool.map(render,selected))
 if not args.scene:
  m.update({'artist':'Cairn','date':'2026-09-14','recording_edition':1,'localOnly':True,'tracks':records,'licenses':{'code':'MIT','music_sources':'CC-BY-4.0','original_vector_art':'CC-BY-4.0'},'artwork':'art/cover.svg'})
  (ROOT/'album.json').write_text(json.dumps(m,indent=2)+'\n')
