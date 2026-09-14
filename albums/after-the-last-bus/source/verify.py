"""Check complete decodes, PCM signal health, tags, timing, and score identity.

This is technical verification, not a substitute for a human listening review.
Requires NumPy. Writes durable evidence into checks/verification.json.
"""
from pathlib import Path
import hashlib, json, math, struct, subprocess, zipfile
import numpy as np
from build import run, loudness
from finalize import sha, NAME

ROOT=Path(__file__).resolve().parent.parent
def pcm_stats(path,sections,bpm):
    blocks=[];peak=0.;sm=np.zeros(2);ss=np.zeros(2);cross=0.;count=0
    with path.open('rb') as f:
        assert f.read(4)==b'RIFF';f.read(4);assert f.read(4)==b'WAVE'
        while True:
            header=f.read(8)
            if len(header)!=8:raise AssertionError('Missing PCM data')
            tag,n=struct.unpack('<4sI',header)
            if tag==b'data':break
            f.seek(n+(n%2),1)
        left=n
        # 100 ms analysis blocks, preserving exact channel order and signed 24-bit.
        while left:
            b=f.read(min(left,4410*6));left-=len(b)
            a=np.frombuffer(b,dtype=np.uint8).reshape(-1,3).astype(np.int32)
            x=(a[:,0]|(a[:,1]<<8)|(a[:,2]<<16));x=np.where(x&0x800000,x-0x1000000,x).astype(np.float64)/8388608
            x=x.reshape(-1,2)
            assert np.isfinite(x).all()
            peak=max(peak,float(np.abs(x).max()));sm+=x.sum(axis=0);ss+=(x*x).sum(axis=0);cross+=float((x[:,0]*x[:,1]).sum());count+=len(x)
            blocks.append(float(np.sqrt(np.mean(x*x))))
    ar=np.array(blocks);audible=np.flatnonzero(ar>10**(-60/20));assert len(audible)
    first=float(audible[0]*.1);last=float(audible[-1]*.1)
    runlen=longest=0
    for value in ar[20:-20]:
        runlen=runlen+1 if value<10**(-65/20) else 0;longest=max(longest,runlen)
    ranges={}
    for s in sections:
        start=(s['bar']*4*60/bpm+.04);end=((s['bar']+s['bars'])*4*60/bpm+.04)
        seg=ar[round((start+1)*10):round((end-1)*10)]
        ranges[s['name']]=round(20*math.log10(max(1e-12,float(np.sqrt(np.mean(seg*seg))))),2)
    out=dict(samplePeakDb=round(20*math.log10(peak),3),dcMean=sm.tolist(),firstAudibleSeconds=first,lastAudibleSeconds=last,longestInteriorSilenceSeconds=round(longest*.1,2),stereoCorrelation=round(cross/math.sqrt(ss[0]*ss[1]),4),sectionRmsDb=ranges)
    out['dcMean']=[float(v/count) for v in sm]
    assert first<.5,('Late start',path,first)
    assert peak<.96,('Clipping risk',path,peak)
    assert max(map(abs,out['dcMean']))<.002
    assert longest*.1<2,('Unexpected silence',path,longest*.1)
    assert ranges['peak']>ranges['break']+2,('Insufficient dynamic contrast',ranges)
    return out

def main():
    album=json.loads((ROOT/'album.json').read_text());results=[]
    for t in album['tracks']:
        print('Checking:',t['title'],flush=True)
        for kind in ['wav','mp3','midi']:assert sha(ROOT/t[kind])==t['sha256'][kind]
        for kind in ['wav','mp3']:run(['ffmpeg','-v','error','-i',ROOT/t[kind],'-map','0:a:0','-f','null','-'])
        probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',ROOT/t['mp3']]).stdout)
        tags=probe['format']['tags'];assert tags['title']==t['title'] and tags['artist']=='Cairn' and tags['album']==album['title']
        assert abs(float(probe['format']['duration'])-t['seconds'])<.1
        assert any(s.get('disposition',{}).get('attached_pic')==1 for s in probe['streams'])
        data=(ROOT/t['midi']).read_bytes();assert data[:4]==b'MThd' and data.count(b'MTrk')>=8
        stats=pcm_stats(ROOT/t['wav'],t['sections'],t['bpm']);mp3=loudness(ROOT/t['mp3'])
        assert float(mp3['input_tp'])<0,('Lossy overs',mp3)
        results.append(dict(title=t['title'],signal=stats,mp3IntegratedLufs=mp3['input_i'],mp3TruePeakDb=mp3['input_tp'],decodeErrors=0,hashesMatch=True,artworkEmbedded=True))
        print(t['title'],stats['sectionRmsDb'],mp3['input_tp'],'dBTP',flush=True)
    full=ROOT/album['completeAlbum'];assert sha(full)==album['completeAlbumSha256']
    run(['ffmpeg','-v','error','-i',full,'-map','0:a:0','-f','null','-'])
    probe=json.loads(run(['ffprobe','-v','error','-show_format','-show_chapters','-of','json',full]).stdout)
    assert abs(float(probe['format']['duration'])-album['totalSeconds'])<.1
    assert len(probe['chapters'])==8
    report=dict(album=album['title'],tracks=results,completeAlbum=dict(seconds=probe['format']['duration'],chapters=8,decodeErrors=0,sha256=sha(full)),verification='Complete audio decodes, signed PCM analysis, hashes, MIDI headers, metadata, duration, chapters, and loudness/true-peak checks. No claim of a human listening review.')
    (ROOT/'checks'/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    # Portable listening edition excludes the redundant complete-album MP3.
    files=[ROOT/p for p in ['album.json','album.m3u8','index.html','tracklist.txt','LINER-NOTES.md','README.md']]
    files += sorted((ROOT/'mp3').glob('*.mp3'))+sorted((ROOT/'art').glob('*'))
    with zipfile.ZipFile(ROOT/f'{NAME}-listening-edition.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,p.relative_to(ROOT))
    files=[ROOT/'LINER-NOTES.md',ROOT/'README.md',ROOT/'tracklist.txt',ROOT/'album.json']
    for folder in ['source','midi','scores','art','checks']:
        files += [p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='shelter-engine']
    with zipfile.ZipFile(ROOT/f'{NAME}-studio-sources.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:z.write(p,p.relative_to(ROOT))
    for name in ['listening-edition','studio-sources']:
        with zipfile.ZipFile(ROOT/f'{NAME}-{name}.zip') as z:assert z.testzip() is None
    print('All checks passed. Listening and studio-source archives verified.',flush=True)

if __name__=='__main__':main()
