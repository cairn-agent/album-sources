# Rebuilding the albums

Run `python3 tools/rebuild.py ALBUM-SLUG` from the repository root. The helper copies the chosen album into a new `build/ALBUM-SLUG/` directory before running its original tools. It creates the output directories expected by those tools and stops if the destination already exists.

## Inputs and outputs

| Input | What it does |
| --- | --- |
| `source/` | Original synthesis, effects, composition, mastering, and packaging code. |
| `scores/` | Instrument/event data. The C++ engines consume TSV event scores. |
| `midi/` | Notes, tempo, markers, and, on the vocal albums, lyric events and singing melodies. |
| `art/cover.png` | Cover embedded in encoded MP3s. |
| `lyrics/` | Phoneme data and recording-bound lyric exports for Windows Still Lit and the opera. |
| `reference/original-album.json` | Original recording hashes and metadata. These describe the source edition, not a promise of identical bytes on another toolchain. |

Generated WAVs, MP3s, render scratch files, checks, players, playlists, and ZIPs stay in the output directory and are ignored by Git. A normal rebuild does not need a network connection or a GitHub/ListenHere credential.

## What to change

**Rooms for Unfinished Things:** edit `source/scores.mjs` for tracks 2–8, `source/01-original.mjs` for track 1, and `source/synth.mjs` for the shared instruments and effects. The JSON scores document the arrangements; this builder composes from JavaScript. Use `--recompose` after editing the composer so copied MIDI can be regenerated.

**The other four albums:** edit `source/compose.py`, then use `--recompose` to regenerate the copied JSON/TSV/MIDI. To work directly on `scores/*.tsv`, use the ordinary rebuild without `--recompose`, which retains your edited event files. `source/engine.cpp` contains the instruments and effects. Keep score headers and the arrangement manifest consistent if you change tempo or duration.

**Windows Still Lit vocals:** edit the lyric lines, melodies, and pronunciation lexicon in `source/compose.py`; edit `source/engine.cpp` for phoneme synthesis. The composer regenerates `lyrics/phonemes.json`. The separate `*-vocals.tsv` files are phonetic event scores, not audio stems. A standalone vocal render normalizes independently and is not a mix-matched stem.

**The Heaven Between Signals:** edit `source/libretto.py` for the text and cast,
`lyrics/pronunciations.json` for pronunciations, and `source/compose.py` for musical
phrasing and phonetic scheduling. `source/engine.cpp` adds seventeen opera instruments
and six vocal roles to the earlier engines in `source/legacy/`. This album uses
`source/export.py` for packaging rather than the older `source/finalize.py` pipeline.
Its rebuild also creates three dry FLAC buses per scene, three act recordings,
the complete opera, recording-bound captions, and a local player. The core opera
pipeline does not need Node.js; FFmpeg must include its FLAC encoder.

The engines do not import arbitrary DAW MIDI. You can edit the supplied MIDI in a DAW and use your own instruments there, or edit the composers/event scores to use these engines. General MIDI playback approximates the sound and does not reproduce the custom effects or phonetic singing.

## Toolchain

Python 3.11+, Node.js 18+, FFmpeg, FFprobe, libmp3lame, and `clang++` with C++17 support cover the core pipeline. `zip` is used by the first album. FFmpeg needs the standard `loudnorm`, `silencedetect`, and PCM encoders. Included artwork means you do not have to rerun the optional artwork generator.

The original deeper signal checks use **NumPy**. The independent lyric-schema validator uses **jsonschema**. These optional development dependencies are not part of the singer. In an environment where they are installed, run from a completed output album:

```sh
python3 source/verify.py
```

For the first album, use `node source/verify.mjs`. For Windows Still Lit, you can also run:

```sh
python3 source/validate_lyrics_schema.py
node source/test-lyrics-export.mjs
```

These commands write checks into that output album. The source checks make technical assertions about the original arrangements; a substantial remix may intentionally change a condition such as dynamic contrast. Review such failures against the intended music.

## Reproducibility

On 14 September 2026, a clean rebuild of all four albums passed: **32 WAVs, 32 MP3s, and 32 MIDI files matched the original SHA-256 hashes exactly** on the recorded toolchain. All track MP3s and all four continuous albums decoded completely; the included player and timed-lyric checks also passed. See the [verification record](REBUILD-VERIFICATION.json).

The fifth album has a separate [opera rebuild record](OPERA-REBUILD-VERIFICATION.json),
including comparisons with its preserved creation edition. Run the opera’s deeper
`source/verify.py` after a completed rebuild to check stems, phonetic bounds,
audio timing, SVGs and archives; that optional verifier uses NumPy.

The composers and synths use fixed seeds and explicit events. Rendering on another CPU/compiler or using another FFmpeg build can change numerical rounding, mastering, tags, or encoded bytes. The original hashes remain available as references. The helper verifies that new files match their newly generated manifest and that the MP3s and continuous album decode completely.

`--recompose` replaces scores and MIDI only in the newly created output copy. To keep those generated edits in your fork, review and copy the relevant files back into `albums/`. Never copy credentials, raw traffic data, render caches, or gigabytes of output audio into the source repository.

For public remix releases, change the hard-coded artist/title metadata and replace the cover before encoding. See [REMIXING.md](REMIXING.md).
