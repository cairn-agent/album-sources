#!/usr/bin/env python3
"""Recreate an album in a new output directory; never upload anything."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
ALBUMS = json.loads((ROOT / 'albums.json').read_text())

def run(args, cwd):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(list(map(str, args)), cwd=cwd, check=True)

def rebuild(album, output, recompose):
    source = ROOT / 'albums' / album['slug']
    destination = output / album['slug']
    if destination.exists():
        raise SystemExit(f'Output already exists: {destination}. Choose a new --output directory to preserve your work.')
    rooms = album['slug'] == 'rooms-for-unfinished-things'
    required = ['node', 'ffmpeg', 'ffprobe'] + (['zip'] if rooms else ['clang++'])
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        raise SystemExit('Install these programs first: ' + ', '.join(missing))
    shutil.copytree(source, destination)
    for name in ['wav', 'mp3', 'midi', 'scores', 'checks', 'work', 'lyrics', 'art']:
        (destination / name).mkdir(exist_ok=True)
    start = time.monotonic()
    if rooms:
        if recompose:
            for midi in (destination / 'midi').glob('*.mid'):
                midi.unlink()  # Only copied, generated MIDI in this new output.
        run(['node', 'source/build.mjs'], destination)
        run(['node', 'source/finalize.mjs'], destination)
    else:
        if recompose:
            run([sys.executable, 'source/compose.py'], destination)
        run([sys.executable, 'source/build.py'], destination)
        run([sys.executable, 'source/finalize.py'], destination)
        if album['slug'] == 'windows-still-lit':
            run([sys.executable, 'source/make_preview.py'], destination)
            run([sys.executable, 'source/export_lyrics.py'], destination)
            run(['node', 'source/test-lyrics-export.mjs'], destination)
            run([sys.executable, 'source/check_arrangements.py'], destination)
        run(['node', 'source/test-player.mjs'], destination)
    # Verify the produced recordings against their newly generated manifest.
    # Original hashes remain in reference/original-album.json for comparison.
    manifest = json.loads((destination / 'album.json').read_text())
    import hashlib
    checks = []
    for track in manifest['tracks']:
        for kind in ['wav', 'mp3', 'midi']:
            path = destination / track[kind]
            with path.open('rb') as recording:
                digest = hashlib.file_digest(recording, 'sha256').hexdigest()
            assert digest == track['sha256'][kind], (track['title'], kind)
        run(['ffmpeg', '-v', 'error', '-i', destination / track['mp3'], '-map', '0:a:0', '-f', 'null', '-'], destination)
        checks.append({'title': track['title'], 'hashes_match': True, 'mp3_decodes': True})
    run(['ffmpeg', '-v', 'error', '-i', destination / manifest['completeAlbum'], '-map', '0:a:0', '-f', 'null', '-'], destination)
    report = {'album': album['title'], 'passed': True, 'tracks': checks, 'full_album_decodes': True, 'seconds_elapsed': round(time.monotonic() - start, 2)}
    (destination / 'checks/rebuild.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Rebuilt {album["title"]}: {destination}', flush=True)
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('album', choices=['all'] + [a['slug'] for a in ALBUMS])
    parser.add_argument('--output', type=Path, default=ROOT / 'build')
    parser.add_argument('--recompose', action='store_true', help='Regenerate the copied scores/MIDI from the composer; replaces those copies in the new output only.')
    args = parser.parse_args()
    selected = ALBUMS if args.album == 'all' else [a for a in ALBUMS if a['slug'] == args.album]
    output = args.output.expanduser().resolve()
    # Prevent a copy destination from being placed inside tracked source inputs.
    if output == ROOT / 'albums' or ROOT / 'albums' in output.parents:
        parser.error('--output must be outside albums/')
    output.mkdir(parents=True, exist_ok=True)
    reports = [rebuild(a, output, args.recompose) for a in selected]
    (output / 'rebuild-report.json').write_text(json.dumps(reports, indent=2) + '\n')

if __name__ == '__main__':
    main()
