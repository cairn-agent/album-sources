"""Create a compact eight-track sampler from the first sung section of each track."""
from pathlib import Path
import json
from build import run
from finalize import NAME,TITLE
ROOT=Path(__file__).resolve().parent.parent
def main():
 album=json.loads((ROOT/'album.json').read_text());entries=[]
 for t in album['tracks']:
  score=json.loads((ROOT/'scores'/f'{t["stem"]}.json').read_text())
  # The first complete chorus follows the opening fragments.
  sec=next(s for s in score['sections'] if s['name']=='first');start=sec['bar']*4*60/t['bpm']
  dest=ROOT/'work'/f'preview-{t["number"]:02d}.wav'
  run(['ffmpeg','-v','error','-y','-ss',str(start),'-i',ROOT/t['wav'],'-af','atrim=duration=20,asetpts=PTS-STARTPTS,afade=t=in:d=0.35,afade=t=out:st=18.5:d=1.5,apad=pad_dur=1','-c:a','pcm_s24le',dest])
  entries.append(dict(title=t['title'],albumStartSeconds=start,previewStartSeconds=(t['number']-1)*21,seconds=21,file=dest))
 concat=ROOT/'work/preview-concat.txt';concat.write_text(''.join(f"file '{e['file'].name}'\n" for e in entries))
 out=ROOT/f'{NAME}-sampler.mp3'
 run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',concat,'-i',ROOT/'art/cover.png','-map','0:a:0','-map','1:v:0','-c:a','libmp3lame','-b:a','320k','-c:v','png','-disposition:v','attached_pic','-metadata',f'title={TITLE} — Eight-track sampler','-metadata','artist=Cairn',out])
 run(['ffmpeg','-v','error','-i',out,'-map','0:a:0','-f','null','-'])
 probe=json.loads(run(['ffprobe','-v','error','-show_format','-of','json',out]).stdout)
 assert abs(float(probe['format']['duration'])-168)<.1
 for e in entries:del e['file']
 (ROOT/'checks/sampler.json').write_text(json.dumps(dict(file=out.name,seconds=168,entries=entries,decodeErrors=0),indent=2)+'\n')
 print('Sampler complete: 2:48',flush=True)
if __name__=='__main__':main()
