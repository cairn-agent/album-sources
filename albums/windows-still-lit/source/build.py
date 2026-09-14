"""Compile original Window Engine and render/master without rhythmic gain pumping.
Only Python standard library, clang++, ffmpeg and ffprobe are required.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,re,subprocess,time,sys
ROOT=Path(__file__).resolve().parent.parent
def run(args):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True)
 if p.returncode:raise RuntimeError(' '.join(map(str,args))+'\n'+p.stderr[-4000:])
 return p
def loudness(path,target=-16.5):
 p=run(['ffmpeg','-hide_banner','-i',path,'-af',f'loudnorm=I={target}:TP=-1.5:LRA=22:print_format=json','-f','null','-'])
 return json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}',p.stderr)[-1])
def render(s):
 start=time.monotonic();stem=s['stem'];raw=ROOT/'work'/f'{stem}-raw.wav';dest=ROOT/'wav'/f'{stem}.wav';check=ROOT/'checks'/f'{stem}.json'
 fingerprint=hashlib.sha256((ROOT/'scores'/f'{stem}.tsv').read_bytes()+(ROOT/'source/engine.cpp').read_bytes()).hexdigest()
 marker=ROOT/'work'/f'{stem}-fingerprint.txt'
 if dest.exists() and check.exists():
  c=json.loads(check.read_text())
  if c['renderFingerprint']==fingerprint and c.get('masteringRevision')==1:print('Current:',s['title'],flush=True);return
 print('Rendering:',s['title'],flush=True)
 if not raw.exists() or not marker.exists() or marker.read_text()!=fingerprint:
  p=run([ROOT/'source/window-engine',ROOT/'scores'/f'{stem}.tsv',raw]);(ROOT/'work'/f'{stem}-render.json').write_text(p.stdout);marker.write_text(fingerprint)
 target=-20 if s['number']==4 else -18.5 if s['number']==8 else -16.5
 measure=loudness(raw,target);nominal=s['endBeat']*60/s['bpm']+6.04
 tail=run(['ffmpeg','-hide_banner','-sseof','-15','-i',raw,'-af','silencedetect=n=-72dB:d=0.3','-f','null','-']).stderr
 starts=re.findall(r'silence_start: ([0-9.]+)',tail);ends=re.findall(r'silence_end: ([0-9.]+)',tail);trim=nominal
 if starts and ends and float(ends[-1])>=14.95:trim=min(nominal,nominal-15+float(starts[-1])+.5)
 # Static gain preserves held bass and vocal envelopes. The loudnorm filter
 # above is used as a meter only; it is never in the mastering signal path.
 gain=min(target-float(measure['input_i']),-1.5-float(measure['input_tp']))
 filt=f'volume={gain:.6f}dB,afade=t=out:st={max(0,trim-.35)}:d=0.35'
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',raw,'-t',f'{trim:.6f}','-af',filt,'-ar','44100','-c:a','pcm_s24le',dest])
 master=loudness(dest,target);probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',dest]).stdout)
 seconds=float(probe['format']['duration']);audio=probe['streams'][0]
 assert abs(seconds-trim)<.03 and audio['channels']==2 and int(audio['sample_rate'])==44100
 assert -28<float(master['input_i'])<-10 and float(master['input_tp'])<=-1.35
 check.write_text(json.dumps(dict(title=s['title'],stem=stem,seconds=seconds,bpm=s['bpm'],key=s['key'],renderFingerprint=fingerprint,masteringRevision=1,targetLufs=target,masteringMethod='static gain, true-peak constrained; no compressor or sidechain',gainDb=gain,rawLoudness=measure,masterLoudness=master,format='44.1 kHz / 24-bit PCM stereo',renderWallSeconds=round(time.monotonic()-start,2)),indent=2)+'\n')
 print('Mastered:',s['title'],f'{seconds:.1f}s, {master["input_i"]} LUFS, {master["input_tp"]} dBTP',flush=True)
def main():
 for d in ['work','checks','wav']:(ROOT/d).mkdir(exist_ok=True)
 run(['clang++','-O3','-std=c++17',ROOT/'source/engine.cpp','-o',ROOT/'source/window-engine'])
 scores=json.loads((ROOT/'scores/manifest.json').read_text())
 if len(sys.argv)>1:scores=[s for s in scores if s['number'] in list(map(int,sys.argv[1:]))]
 with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,scores))
 print('Requested masters complete.',flush=True)
if __name__=='__main__':main()
