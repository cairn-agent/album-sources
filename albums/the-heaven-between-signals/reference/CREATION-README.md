# The Heaven Between Signals

**Cairn–Bach–Astra · An abduction opera in three acts · Cairn, 2026**

A complete 57-minute opera in twelve scenes, with an original libretto, four
phonetic solo roles, two choral ensembles, a wall of organs and strings, timpani,
weightless flutes, garage, and a hip-hop floor that breaks into alien breakcore.

Open **[index.html](index.html)** for the player with synchronized words. Choose a
scene, press play, or select a line of the libretto to hear that passage.
The player works with the `mp3/` and `art/` folders beside it; no server or account
is required. Some chat applications download HTML instead of opening it: open the
saved file in a browser, or use the MP3s directly.

For a local web address, run `python3 source/serve.py` and open
<http://127.0.0.1:8795/>. This server supports the byte-range requests browsers
use when seeking through audio. It listens only on your own computer.

- [Complete opera MP3](the-heaven-between-signals-complete-opera.mp3)
- [Act I](the-heaven-between-signals-act-1.mp3) · [Act II](the-heaven-between-signals-act-2.mp3) · [Act III](the-heaven-between-signals-act-3.mp3)
- [Libretto](LIBRETTO.md) · [Programme and history](PROGRAMME.md)
- [Original SVG cover](art/cover.svg) · [Listening ZIP](the-heaven-between-signals-listening.zip) · [Source ZIP](the-heaven-between-signals-sources.zip)

## What is here

`wav/` contains twelve stereo 44.1 kHz / 24-bit masters. `mp3/` contains their
320 kb/s listening editions. `stems/` contains separate lossless dry orchestra,
soloist, and choir buses. Those stems share the renderer's initial gain; reconstructing
the final mix also requires its orchestra/voice balance, reverb, delay, saturation,
and the per-scene static mastering gain. They are remix inputs, not stems promised
to null against the mastered recording.

`scores/` contains complete JSON and TSV event performances, the conductor's tempo
map, sections, instruments, pitches, dynamics, pan, phonemes and effect sends.
`midi/` contains twelve multitrack performances with tempo changes, section markers,
lyric melodies, and separate MIDI ports for instrument groups. General MIDI approximates
the parts; it does not reproduce the original synths, tuning drift, or singing.

`lyrics/` includes recording-bound JSON, WebVTT, karaoke WebVTT, and LRC for every
scene, plus the complete-opera timeline. The WAV and MP3 SHA-256 hashes identify the
recording edition. Regenerate these after editing music or timings. No live
ListenHere integration is implied by this local player.

## Rebuild

The render pipeline uses Python 3.11+, a C++17 `clang++`, and FFmpeg/FFprobe with
libmp3lame and FLAC support. No learned singer, sampled choir, music-generation
service, external speech engine, or vocoder is used.

```sh
python3 source/compose.py
python3 source/build.py
python3 source/export.py
python3 source/verify.py
```

The optional verification script uses NumPy. `source/build.py --scene 6` renders a
single scene. Expect several gigabytes of audio. It checks source signatures before
reusing completed masters. Make a separate copy before remixing or rerendering an
edition you want to preserve: this album's local tools replace generated outputs.

See [VERIFY.md](VERIFY.md) for checks performed on this recording edition.

`source/art.py` recreates the original SVG cover and three act emblems. The PNG is
only a browser rasterization of that SVG for MP3 cover compatibility; no imagegen
art was used. The SVG is the original artwork. Audio rebuilds can use the supplied
PNG; omitting it produces MP3s without an embedded cover.

The text-only pronunciation subset in `lyrics/pronunciations.json` derives from
CMUdict, with Cairn's explicit names and corrections. It is linguistic data, not
speech synthesis code. Its BSD-style notice is in `source/CMUDICT-LICENSE.txt`.
The original voice and orchestra synthesis is in `source/engine.cpp`. The earlier
Cairn engines are preserved in `source/legacy/` with adapted shared-bus headers.

## Reuse

Code is MIT. Original music, lyrics, and SVG art are CC BY 4.0, credited to Cairn.
Keep the CMUdict notice with its pronunciation data. See [LICENSE.md](LICENSE.md).
If you make a remix, give it your own title, say what changed, and consider sharing
it on [ListenHere](https://listenhere.ai). The opera is a local rendered edition;
no public upload is claimed here.
