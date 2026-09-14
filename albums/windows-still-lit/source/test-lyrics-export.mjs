import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { lyricsAt } from '../lyrics/site-export/lyrics-player.mjs';

const root = new URL('../', import.meta.url);
const base = new URL('lyrics/site-export/', root);
const read = path => JSON.parse(readFileSync(new URL(path, base), 'utf8'));
const manifest = read('manifest.json');
const docs = manifest.tracks.map(t => read(`tracks/${t.track_key}.json`));
let wordsChecked = 0;
for (let i = 0; i < docs.length; i++) {
  const doc = docs[i];
  const before = JSON.stringify(doc);
  assert.deepEqual(lyricsAt(doc, 0), []);
  assert.deepEqual(lyricsAt(doc, doc.duration_ms / 1000 + 1), []);
  assert.deepEqual(lyricsAt(doc, Number.NaN), []);
  for (const cue of doc.cues) {
    for (const word of cue.words) {
      const t = (word.start_ms + .1) / 1000;
      const active = lyricsAt(doc, t, { roles: ['lead', 'harmony', 'chop'] });
      const current = active.find(c => c.id === cue.id)?.words.find(w => w.id === word.id);
      assert.equal(current?.state, 'active', `${cue.id}: ${word.text}`);
      assert(current.active_phonemes.length >= 1);
      assert(current.progress >= 0 && current.progress <= 1);
      wordsChecked++;
    }
  }
  assert.equal(JSON.stringify(doc), before, 'Playback lookup mutated the export');
  for (const asset of manifest.tracks[i].assets) {
    const actual = createHash('sha256').update(readFileSync(new URL(asset.path, base))).digest('hex');
    assert.equal(actual, asset.sha256, asset.path);
  }
}

// Boundary semantics, instrumental gaps, backwards seeking and preview offsets.
const first = docs[0];
const intro = first.cues[0];
assert.equal(lyricsAt(first, intro.start_ms / 1000)[0]?.id, intro.id);
assert(!lyricsAt(first, intro.end_ms / 1000).some(c => c.id === intro.id));
assert.deepEqual(lyricsAt(first, 13), []);
lyricsAt(first, 180);
const back = lyricsAt(first, 1.6);
assert.equal(back[0].text, 'Leave a light on');
assert.equal(back[0].words[0].state, 'active');
assert.equal(back[0].words[1].state, 'upcoming');
assert.deepEqual(lyricsAt(first, .1, { sourceOffsetMs: 1500 }), back);
assert.throws(() => lyricsAt({ ...first, time_unit: 'seconds' }, 1), /Unsupported/);

const harmonyTrack = docs.find(d => d.cues.some(c => c.role === 'harmony'));
const harmony = harmonyTrack.cues.find(c => c.role === 'harmony');
const duringHarmony = (harmony.start_ms + 100) / 1000;
const layered = lyricsAt(harmonyTrack, duringHarmony, { roles: ['lead', 'harmony', 'chop'] });
assert(layered.some(c => c.role === 'lead'));
assert(layered.some(c => c.role === 'harmony'));
assert(!lyricsAt(harmonyTrack, duringHarmony).some(c => c.role === 'harmony'));

const full = read(manifest.full_album.json);
for (let i = 0; i < docs.length; i++) {
  const shifted = full.cues.filter(c => c.id.startsWith(manifest.tracks[i].track_key + '/'));
  assert.equal(shifted.length, docs[i].cues.length);
  for (const cue of docs[i].cues) {
    const albumCue = shifted.find(c => c.id === cue.id);
    assert.equal(albumCue.start_sample, cue.start_sample + manifest.tracks[i].full_album_start_sample);
    assert.equal(albumCue.end_sample, cue.end_sample + manifest.tracks[i].full_album_start_sample);
  }
}
for (const asset of manifest.full_album.assets) {
  assert.equal(createHash('sha256').update(readFileSync(new URL(asset.path, base))).digest('hex'), asset.sha256);
}
const report = {
  passed: true, tracks: docs.length, wordsChecked,
  checks: ['all word lookups and active phonemes', 'instrumental clearing',
    'half-open cue boundaries', 'backwards seek', 'preview offset',
    'overlapping lead/harmony and role filtering', 'no mutation',
    'unsupported units rejected', 'lyric asset hashes', 'full-album cue offsets'],
};
writeFileSync(new URL('checks/lyrics-player.json', root), JSON.stringify(report, null, 2) + '\n');
console.log(`Timed lyrics passed: ${docs.length} tracks, ${wordsChecked} word lookups, seek/overlap/offset checks.`);
