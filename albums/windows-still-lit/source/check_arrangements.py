"""Audit the requested differences: held/sparse bass, straighter kicks and phonetic lyrics."""
from pathlib import Path
import json,statistics,ast
ROOT=Path(__file__).resolve().parent.parent
BASS={6,7,21,22,23,24}
def main():
 results=[]
 for s in json.loads((ROOT/'scores/manifest.json').read_text()):
  d=json.loads((ROOT/'scores'/f'{s["stem"]}.json').read_text());es=d['events'];bass=[e for e in es if e[2] in BASS];kick=[e for e in es if e[2]==0];vox=[e for e in es if e[2]>=40]
  assert vox and len(d['vocalWords'])>25 and len(s['lyrics'])==4
  assert all(e[2]!=6 for e in es),'Old repeated sub voice present'
  if s['number'] in [2,4,8]:assert not bass
  if s['number']==4:assert not kick
  straight=sum(abs(e[0]-round(e[0]))<.025 for e in kick)/max(1,len(kick))
  if kick:assert straight>.85,(s['title'],straight)
  instruments=sorted(set(e[2] for e in es if e[2]<40));bvoices=sorted(set(e[2] for e in bass))
  results.append(dict(title=s['title'],instrumentVoices=instruments,instrumentCount=len(instruments),bassVoices=bvoices,bassNoteCount=len(bass),medianBassLengthBeats=statistics.median([e[1] for e in bass]) if bass else None,quarterAlignedKickFraction=round(straight,3) if kick else None,phoneticEventCount=len(vox),sungWords=len(d['vocalWords']),choppedWords=sum(w['chop'] for w in d['vocalWords'])))
 engine=(ROOT/'source/engine.cpp').read_text()
 assert '1-.3*std::exp' not in engine
 imports=set()
 for path in (ROOT/'source').glob('*.py'):
  for node in ast.walk(ast.parse(path.read_text())):
   if isinstance(node,ast.Import):imports.update(a.name.split('.')[0] for a in node.names)
   elif isinstance(node,ast.ImportFrom) and node.module:imports.add(node.module.split('.')[0])
 assert not imports.intersection({'pyworld','torch','espeak','pyttsx3'})
 report=dict(passed=True,globalKickDucking=False,externalSpeechEngine=False,tracks=results)
 (ROOT/'checks/arrangements.json').write_text(json.dumps(report,indent=2)+'\n')
 for r in results:print(r['title'],'bass',r['bassVoices'],'median beats',r['medianBassLengthBeats'],'instruments',r['instrumentCount'],'sung words',r['sungWords'])
if __name__=='__main__':main()
