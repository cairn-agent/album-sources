"""Compile Night Engine, render scores, master WAVs, and validate loudness.

Uses only Python's standard library, clang++, and ffmpeg. Re-run safely to
resume missing tracks; delete only a chosen generated WAV/check to rebuild it.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, re, subprocess, time, hashlib

ROOT=Path(__file__).resolve().parent.parent
def run(args):
    p=subprocess.run(list(map(str,args)),capture_output=True,text=True)
    if p.returncode:raise RuntimeError(' '.join(map(str,args))+'\n'+p.stderr[-5000:])
    return p
def loudness(path):
    p=run(['ffmpeg','-hide_banner','-i',path,'-af','loudnorm=I=-14:TP=-1.2:LRA=18:print_format=json','-f','null','-'])
    matches=re.findall(r'\{\s*"input_i"[\s\S]*?\}',p.stderr)
    if not matches:raise RuntimeError('No loudness report')
    return json.loads(matches[-1])

def render(s):
    start=time.monotonic();stem=s['stem'];raw=ROOT/'work'/f'{stem}-raw.wav';dest=ROOT/'wav'/f'{stem}.wav';check=ROOT/'checks'/f'{stem}.json'
    fingerprint=hashlib.sha256((ROOT/'scores'/f'{stem}.tsv').read_bytes()+(ROOT/'source'/'engine.cpp').read_bytes()).hexdigest()
    marker=ROOT/'work'/f'{stem}-fingerprint.txt'
    if dest.exists() and check.exists() and json.loads(check.read_text()).get('renderFingerprint')==fingerprint and json.loads(check.read_text()).get('masteringRevision')==2:
        print('Verified render already exists:',stem,flush=True);return
    print('Rendering:',s['title'],flush=True)
    if not raw.exists() or not marker.exists() or marker.read_text()!=fingerprint:
        p=run([ROOT/'source'/'night-engine',ROOT/'scores'/f'{stem}.tsv',raw])
        (ROOT/'work'/f'{stem}-render.json').write_text(p.stdout)
        marker.write_text(fingerprint)
    measure=loudness(raw)
    nominal=s['endBeat']*60/s['bpm']+6.04
    # Remove only final near-silence, never musical rests inside the arrangement.
    tail=run(['ffmpeg','-hide_banner','-sseof','-15','-i',raw,'-af','silencedetect=n=-72dB:d=0.3','-f','null','-']).stderr
    starts=re.findall(r'silence_start: ([0-9.]+)',tail)
    ends=re.findall(r'silence_end: ([0-9.]+)',tail)
    trim_to=nominal
    if starts and ends and float(ends[-1])>=14.95:
        trim_to=min(nominal,nominal-15+float(starts[-1])+.6)
    filt=('loudnorm=I=-14:TP=-1.2:LRA=18:linear=true:'
          f'measured_I={measure["input_i"]}:measured_TP={measure["input_tp"]}:'
          f'measured_LRA={measure["input_lra"]}:measured_thresh={measure["input_thresh"]}:'
          f'offset={measure["target_offset"]}:print_format=json')
    filt+=f',afade=t=out:st={max(0,trim_to-.2)}:d=0.2'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',raw,'-t',f'{trim_to:.6f}','-af',filt,'-ar','44100','-c:a','pcm_s24le',dest])
    master=loudness(dest)
    probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',dest]).stdout)
    audio=probe['streams'][0];seconds=float(probe['format']['duration'])
    assert int(audio['sample_rate'])==44100 and audio['channels']==2
    assert abs(seconds-trim_to)<.05
    assert -30<float(master['input_i'])<-8
    assert float(master['input_tp'])<=-.7
    check.write_text(json.dumps(dict(title=s['title'],stem=stem,seconds=seconds,bpm=s['bpm'],key=s['key'],renderFingerprint=fingerprint,masteringRevision=2,trimmedTailSeconds=round(nominal-seconds,4),rawLoudness=measure,masterLoudness=master,format='44.1 kHz / 24-bit PCM stereo',renderWallSeconds=round(time.monotonic()-start,2)),indent=2)+'\n')
    print('Mastered:',s['title'],f'{seconds:.1f}s, {master["input_i"]} LUFS, {master["input_tp"]} dBTP',flush=True)

def main():
    for d in ['work','checks','wav']:(ROOT/d).mkdir(exist_ok=True)
    run(['clang++','-O3','-std=c++17',ROOT/'source'/'engine.cpp','-o',ROOT/'source'/'night-engine'])
    scores=json.loads((ROOT/'scores'/'manifest.json').read_text())
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,scores))
    print('All eight masters complete.',flush=True)

if __name__=='__main__':main()
