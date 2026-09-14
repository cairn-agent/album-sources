"""Encode tagged MP3s, assemble the complete album, and build the local player."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from html import escape
import hashlib, json, subprocess, sys
from build import run

ROOT=Path(__file__).resolve().parent.parent
NAME='the-distance-turns-to-light'
TITLE='The Distance Turns to Light'
def fmt(s):
    s=round(s);return f'{s//60}:{s%60:02d}'
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def encode(s):
    stem=s['stem'];dest=ROOT/'mp3'/f'{stem}.mp3'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',ROOT/'wav'/f'{stem}.wav','-i',ROOT/'art'/'cover.png',
         '-map','0:a:0','-map','1:v:0','-c:a','libmp3lame','-b:a','320k','-c:v','png','-disposition:v','attached_pic','-id3v2_version','3',
         '-metadata',f'title={s["title"]}','-metadata','artist=Cairn','-metadata',f'album={TITLE}','-metadata',f'track={s["number"]}/8',
         '-metadata','date=2026','-metadata','genre=Trance','-metadata',f'TBPM={s["bpm"]}',
         '-metadata','comment=Original compositions and code-built instruments. Local edition.',dest])
    print('Encoded:',s['title'],flush=True)

def player(tracks,total):
    cards=[]
    for t in tracks:
        cards.append(f'<button class="track" data-index="{t["number"]-1}"><span class="number">{t["number"]:02d}</span><span><strong>{escape(t["title"])}</strong><small>{t["bpm"]} BPM · {escape(t["key"])}</small></span><time>{fmt(t["seconds"])}</time></button>')
    data=json.dumps([dict(title=t['title'],file=t['mp3']) for t in tracks]).replace('</','<\\/')
    html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Distance Turns to Light - Cairn</title><style>
:root{color-scheme:dark;font-family:Arial,sans-serif;background:#0a122a;color:#e8ecf4}*{box-sizing:border-box}body{margin:0;padding:clamp(20px,5vw,70px)}main{max-width:1240px;margin:auto;display:grid;grid-template-columns:minmax(260px,1fr) minmax(330px,1.1fr);gap:55px}img{width:100%;border:1px solid #304663}h1{font-size:clamp(30px,4vw,48px);line-height:1.06;letter-spacing:-1.5px;margin:15px 0}p{line-height:1.6;color:#aebdd1}.eyebrow{font-size:12px;letter-spacing:3px;color:#90c7d6}audio{width:100%;margin:12px 0 20px}.track{width:100%;display:grid;grid-template-columns:32px 1fr 45px;gap:12px;text-align:left;color:inherit;background:transparent;border:0;border-top:1px solid #2b3b58;padding:17px 0;cursor:pointer}.track:hover,.track.current{color:#9edbdc}.track:focus-visible{outline:2px solid #e9a693;outline-offset:3px}strong{font-weight:500;font-size:17px}small{display:block;color:#7c95af;font-size:12px;margin-top:6px}.number,time{font:12px monospace;color:#8ba6be}time{text-align:right}a{color:#e9b5ac}nav{display:flex;gap:20px;flex-wrap:wrap;font-size:13px;margin:25px 0}.now{font-size:13px;color:#cbb5dc;min-height:20px}footer{border-top:1px solid #2b3b58;margin-top:28px;padding-top:12px;font-size:12px;color:#7c95af}@media(max-width:760px){main{grid-template-columns:1fr;gap:28px}.sleeve{max-width:540px;margin:auto}}
</style><main><section class="sleeve"><img src="art/cover.svg" alt="A striped rising sun above three colored paths in a midnight sky"><p>A night in eight transmissions. Original melodies, custom-built synths, and the long way back to daylight.</p><nav><a href="LINER-NOTES.md">Liner notes</a><a href="album.m3u8">Playlist</a><a href="art/cover.svg">Vector sleeve</a></nav></section><section><div class="eyebrow">CAIRN / LOCAL EDITION</div><h1>The Distance<br>Turns to Light</h1><p>8 tracks · '''+fmt(total)+''' · 132-142 BPM<br>Original trance in a 1998-2002-inspired sound world.</p><div class="now" id="now" aria-live="polite">Select a transmission.</div><audio id="audio" controls preload="metadata"></audio><div>'''+''.join(cards)+'''</div><nav><a href="'''+NAME+'''-full-album.mp3" download>Download complete album</a></nav><footer>All sounds synthesized in code. No borrowed tracks or samples. Nothing is uploaded or fetched by this player.</footer></section></main><script>
const tracks='''+data+''';const audio=document.getElementById('audio');const buttons=[...document.querySelectorAll('.track')];let current=0;audio.volume=.7;
function select(n,play=true){current=n;audio.src=tracks[n].file;document.getElementById('now').textContent=(n+1)+' / '+tracks[n].title;buttons.forEach((b,i)=>{b.classList.toggle('current',i===n);b.setAttribute('aria-pressed',i===n?'true':'false')});if(play)audio.play().catch(()=>{document.getElementById('now').textContent='Press play to begin: '+tracks[n].title})}
buttons.forEach((b,i)=>b.addEventListener('click',()=>select(i)));audio.addEventListener('ended',()=>{if(current<tracks.length-1)select(current+1)});select(0,false);
</script></html>'''
    # Keep the player fully portable in the listening ZIP, without duplicating
    # the entire album as both individual files and a second, combined MP3.
    html=html.replace(f'href="{NAME}-full-album.mp3" download>Download complete album',f'id="download" href="{tracks[0]["mp3"]}" download>Download selected track')
    html=html.replace('audio.src=tracks[n].file;',"audio.src=tracks[n].file;document.getElementById('download').href=tracks[n].file;")
    return html

def main():
    scores=json.loads((ROOT/'scores'/'manifest.json').read_text());tracks=[]
    for s in scores:
        check=json.loads((ROOT/'checks'/f'{s["stem"]}.json').read_text())
        fingerprint=hashlib.sha256((ROOT/'scores'/f'{s["stem"]}.tsv').read_bytes()+(ROOT/'source'/'engine.cpp').read_bytes()).hexdigest()
        assert check['renderFingerprint']==fingerprint,'Master is stale: '+s['title']
        tracks.append(dict(number=s['number'],title=s['title'],stem=s['stem'],seconds=check['seconds'],bpm=s['bpm'],key=s['key'],sections=s['sections'],description=s['description'],mp3=f'mp3/{s["stem"]}.mp3',wav=f'wav/{s["stem"]}.wav',midi=f'midi/{s["stem"]}.mid'))
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(encode,scores))
    total=sum(t['seconds'] for t in tracks)
    concat=ROOT/'work'/'concat-wav.txt';concat.write_text(''.join(f"file '../wav/{t['stem']}.wav'\n" for t in tracks))
    chapters=[';FFMETADATA1'];cursor=0
    for t in tracks:
        chapters+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(cursor*1000)}',f'END={round((cursor+t["seconds"])*1000)}','title='+t['title']];cursor+=t['seconds']
    cp=ROOT/'work'/'chapters.ffmeta';cp.write_text('\n'.join(chapters)+'\n')
    full=ROOT/f'{NAME}-full-album.mp3'
    print('Assembling the complete album...',flush=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',concat,'-i',ROOT/'art'/'cover.png','-i',cp,
         '-map','0:a:0','-map','1:v:0','-map_chapters','2','-c:a','libmp3lame','-b:a','320k','-c:v','png','-disposition:v','attached_pic','-id3v2_version','3',
         '-metadata',f'title={TITLE} - Complete Album','-metadata','artist=Cairn','-metadata',f'album={TITLE}','-metadata','date=2026','-metadata','genre=Trance',full])
    for t in tracks:t['sha256']={fmt:sha(ROOT/t[fmt]) for fmt in ['mp3','wav','midi']}
    album=dict(title=TITLE,artist='Cairn',date='2026-09-13',genre='Trance',brief='Original trance inspired by the 1998-2002 era',totalSeconds=total,displayDuration=fmt(total),tracks=tracks,completeAlbum=full.name,completeAlbumSha256=sha(full),masterFormat='44.1 kHz / 24-bit PCM stereo',mp3Format='320 kb/s stereo',localOnly=True)
    (ROOT/'album.json').write_text(json.dumps(album,indent=2)+'\n')
    (ROOT/'album.m3u8').write_text('#EXTM3U\n'+''.join(f'#EXTINF:{t["seconds"]:.3f},Cairn - {t["title"]}\n{t["mp3"]}\n' for t in tracks))
    (ROOT/'tracklist.txt').write_text(TITLE+' - Cairn\n\n'+''.join(f'{t["number"]:02d}  {fmt(t["seconds"])}  {t["title"]}  /  {t["bpm"]} BPM  /  {t["key"]}\n' for t in tracks)+f'\nTotal: {fmt(total)}\n')
    (ROOT/'index.html').write_text(player(tracks,total))
    (ROOT/'checks'/'sha256.txt').write_text(''.join(f'{t["sha256"][kind]}  {t[kind]}\n' for t in tracks for kind in ['mp3','wav','midi'])+f'{album["completeAlbumSha256"]}  {full.name}\n')
    print(json.dumps(dict(album=TITLE,total=fmt(total),tracks=len(tracks),completeAlbum=str(full))),flush=True)

if __name__=='__main__':
    if '--player-only' in sys.argv:
        album=json.loads((ROOT/'album.json').read_text())
        (ROOT/'index.html').write_text(player(album['tracks'],album['totalSeconds']))
    else:main()
