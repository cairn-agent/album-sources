"""Check the rendered opera, lyric edition, MIDI, SVG and download archives.

Requires NumPy and FFmpeg. This measures files and playback timing; it does not
claim a human listening review or measure the intelligibility of the singer.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, re, struct, subprocess, wave, zipfile
import xml.etree.ElementTree as ET
import numpy as np
from libretto import SCENES

ROOT = Path(__file__).resolve().parent.parent

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def command(args):
    return subprocess.run(list(map(str, args)), check=True, capture_output=True)

def pcm(path, rate=11025):
    return np.frombuffer(command(['ffmpeg', '-v', 'error', '-i', path,
        '-map', '0:a:0', '-ar', rate, '-ac', 2, '-f', 'f32le', '-']).stdout,
        dtype='<f4').reshape(-1, 2)

def midi_check(path):
    data = path.read_bytes()
    assert data[:4] == b'MThd' and len(data) > 14
    header_length = struct.unpack('>I', data[4:8])[0]
    fmt, tracks, division = struct.unpack('>HHH', data[8:14])
    assert fmt == 1 and division == 960
    pos = 8 + header_length
    for _ in range(tracks):
        assert data[pos:pos+4] == b'MTrk'
        length = struct.unpack('>I', data[pos+4:pos+8])[0]
        chunk = data[pos+8:pos+8+length]
        assert len(chunk) == length and chunk.endswith(b'\xff\x2f\x00')
        pos += 8 + length
    assert pos == len(data) and b'\xff\x51\x03' in data and b'\xff\x05' in data
    return tracks

def check_track(t):
    name = t['stem']
    for kind in ['wav', 'mp3', 'midi']:
        assert sha(ROOT / t[kind]) == t['sha256'][kind], (name, kind, 'hash')
    with wave.open(str(ROOT / t['wav']), 'rb') as w:
        assert (w.getnchannels(), w.getframerate(), w.getsampwidth()) == (2, 44100, 3)
        frames = w.getnframes()
        assert abs(frames/44100 - t['duration']) < 1/44100
    score = json.loads((ROOT / t['score']).read_text())
    lyrics = json.loads((ROOT / t['lyrics']['json']).read_text())
    assert lyrics['cues'] == score['cues'] and lyrics['words'] == score['vocalWords']
    assert lyrics['recordings']['mp3']['sha256'] == t['sha256']['mp3']
    assert lyrics['recordings']['wav']['sha256'] == t['sha256']['wav']
    original = [(line.split('|', 1)[0], line.split('|', 1)[1])
        for line in SCENES[t['number']-1]['lines'].strip().splitlines() if line.strip()]
    assert original == [(c['role'], c['text']) for c in lyrics['cues']], name
    assert len(lyrics['cues']) == t['cues']
    assert len(lyrics['all_phonetic_events']) == t['phonetic_events']
    for i, c in enumerate(lyrics['cues']):
        assert 0 <= c['start'] < c['end'] <= t['duration']
        if i: assert c['start'] >= lyrics['cues'][i-1]['end']
        words = [w for w in lyrics['words'] if w['role'] == c['role']
            and c['start']-.15 <= w['start'] < c['end']]
        assert len(words) == len(c['text'].split()), (name, c['text'], len(words))
        for w in words:
            assert c['start']-.15 <= w['start'] < w['end'] <= c['end']+.15
            assert abs(w['phonemes'][0]['start']-w['start']) < .001
            assert abs(w['phonemes'][-1]['end']-w['end']) < .001
            for p in w['phonemes']:
                assert w['start']-.001 <= p['start'] < p['end'] <= w['end']+.001
    for p in lyrics['all_phonetic_events']:
        assert 0 <= p['start'] < p['end'] <= t['duration']
    for kind in ['vtt', 'karaoke', 'lrc']:
        assert (ROOT / t['lyrics'][kind]).is_file()
    a, b = pcm(ROOT/t['wav']), pcm(ROOT/t['mp3'])
    assert np.isfinite(a).all() and np.isfinite(b).all()
    assert abs(len(a)-len(b)) <= 1, (name, 'gapless length', len(a), len(b))
    assert np.max(np.abs(b)) < 1, (name, 'decoded sample clipping')
    rms = float(np.sqrt(np.mean(a*a)))
    assert rms > .0001
    center = min(len(a)//2, len(b)//2)
    window = 11025*10
    x = a[center-window:center+window].mean(axis=1).astype('float64')
    x -= x.mean()
    correlations = []
    for lag in range(-8, 9):
        y = b[center-window+lag:center+window+lag].mean(axis=1).astype('float64')
        y -= y.mean()
        correlations.append(float(np.dot(x, y) / np.sqrt(np.dot(x,x)*np.dot(y,y))))
    lag = int(np.argmax(correlations))-8
    assert abs(lag) <= 1 and max(correlations) > .98, (name, 'codec alignment', lag, max(correlations))
    measured = command(['ffmpeg', '-hide_banner', '-nostats', '-i', ROOT/t['mp3'],
        '-map', '0:a:0', '-af', 'loudnorm=I=-18:TP=-1:LRA=20:print_format=json', '-f', 'null', '-'])
    log = measured.stderr.decode()
    levels = json.JSONDecoder().raw_decode(log[log.rfind('{'):])[0]
    assert float(levels['input_tp']) < 0, (name, 'true peak', levels['input_tp'])
    stem_frames = []
    for stem in t['stems']:
        probe = json.loads(command(['ffprobe', '-v', 'error', '-show_streams', '-of', 'json', ROOT/stem]).stdout)
        s = probe['streams'][0]
        assert s['codec_name'] == 'flac' and s['channels'] == 2 and s['sample_rate'] == '44100'
        assert int(s['duration_ts']) == frames
        command(['ffmpeg', '-v', 'error', '-i', ROOT/stem, '-f', 'null', '-'])
        stem_frames.append(int(s['duration_ts']))
    answer = {'scene': t['number'], 'title': t['title'], 'duration': t['duration'],
        'master_frames': frames, 'mp3_decoded_frames_11025': len(b),
        'mp3_alignment_lag_seconds': lag/11025, 'mp3_pcm_correlation': max(correlations),
        'mp3_lufs': float(levels['input_i']), 'mp3_true_peak_db': float(levels['input_tp']),
        'mp3_loudness_range_lu': float(levels['input_lra']),
        'midi_tracks': midi_check(ROOT/t['midi']), 'cues': len(lyrics['cues']),
        'words': len(lyrics['words']), 'phonetic_events': len(lyrics['all_phonetic_events']),
        'dry_stems_verified': len(stem_frames), 'hashes_match': True}
    print(f"Verified {t['number']:02}: {t['title']}", flush=True)
    return answer

def main():
    album = json.loads((ROOT/'album.json').read_text())
    assert len(album['tracks']) == 12
    assert len({t['sha256']['wav'] for t in album['tracks']}) == 12
    used = {k for t in album['tracks'] for k in t['instruments']}
    assert used == set(json.loads((ROOT/'scores/instruments.json').read_text())) and len(used) == 99
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(check_track, album['tracks']))
    full = json.loads((ROOT/'lyrics/complete-opera.json').read_text())
    assert sha(ROOT/album['completeOpera']) == album['completeOperaSha256'] == full['recording']['sha256']
    offset, allcues = 0, []
    for t in album['tracks']:
        assert abs(t['full_opera_offset']-offset) < 1e-6
        l = json.loads((ROOT/t['lyrics']['json']).read_text())
        allcues += [{**c, 'start': c['start']+offset, 'end': c['end']+offset, 'scene': t['number']} for c in l['cues']]
        offset += t['duration']
    assert allcues == full['cues'] and abs(full['duration']-offset) < 1e-6
    for label, tracks in [('complete-opera', album['tracks'])] + [
            (f'act-{act}', [t for t in album['tracks'] if t['act'] == act]) for act in [1,2,3]]:
        path = ROOT/f'the-heaven-between-signals-{label}.mp3'
        decoded = pcm(path, rate=1000)
        assert abs(len(decoded)/1000 - sum(t['duration'] for t in tracks)) < .002
        assert np.isfinite(decoded).all()
    for svg in (ROOT/'art').glob('*.svg'):
        tree = ET.parse(svg)
        assert tree.getroot().tag == '{http://www.w3.org/2000/svg}svg'
        assert '<image' not in svg.read_text(), 'Original art must remain vector geometry'
    page = (ROOT/'index.html').read_text()
    for target in re.findall(r'(?:href|src)="([^"]+)"', page):
        if ':' not in target and not target.startswith('#'):
            assert (ROOT/target).is_file(), target
    archives = {}
    for kind in ['sources', 'listening']:
        path = ROOT/f'the-heaven-between-signals-{kind}.zip'
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            names = z.namelist()
            assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
            assert not any(n.endswith(('.env', '.pyc')) or '/work/' in n for n in names)
            if kind == 'sources':
                assert 'source/verify.py' in names and 'source/engine.cpp' in names
                assert len([n for n in names if n.startswith('midi/') and n.endswith('.mid')]) == 12
            else:
                assert 'index.html' in names and album['completeOpera'] in names
                assert all(t['mp3'] in names for t in album['tracks'])
                # The archive link is omitted from its own extracted player.
                extracted = z.read('index.html').decode()
                assert 'href="the-heaven-between-signals-listening.zip"' not in extracted
            archives[kind] = {'files': len(names), 'bytes': path.stat().st_size, 'sha256': sha(path)}
    report = {'passed': True, 'method': 'File, signal, alignment and structure verification; no subjective listening claim.',
        'scenes': 12, 'duration_seconds': offset, 'instrument_recipes': len(used),
        'lyric_lines': sum(t['cues'] for t in results), 'lyric_words': sum(t['words'] for t in results),
        'phonetic_events': sum(t['phonetic_events'] for t in results), 'tracks': results, 'archives': archives}
    (ROOT/'checks/verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['tracks', 'archives']}, indent=2))

if __name__ == '__main__':
    main()
