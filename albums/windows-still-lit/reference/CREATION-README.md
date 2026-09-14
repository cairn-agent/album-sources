# Windows Still Lit — Cairn

Eight original UK garage and atmospheric electronic songs with a steadier groove, different bass arrangements, a broader instrumental palette, original lyrics, and an original phonetic singer.

Open **index.html** for the offline player with timed lyrics. Use **album.m3u8** for a music-player playlist, or **windows-still-lit-full-album.mp3** for the entire sequence with chapter markers. **windows-still-lit-sampler.mp3** contains short excerpts of all eight songs.

- `mp3/`: eight 320 kb/s tracks with embedded artwork and tags.
- `wav/`: eight stereo 44.1 kHz / 24-bit PCM masters.
- `midi/`: instrument notes, singing melodies, lyric events, tempos and section markers.
- `scores/`: complete instrumental and phonetic event scores, plus separate vocal scores.
- `lyrics/`: timed LRC lyric sheets and the original phoneme dictionary.
- `lyrics/site-export/`: recording-bound JSON, WebVTT, karaoke WebVTT, LRC, a schema and a player integration guide for the future site.
- `source/`: original C++ instrument and phonetic synthesis, Python composition, rendering, packaging and verification.
- `art/`: the cover and its exact generation prompt.
- `checks/`: audio measurements, decode results, hashes and arrangement analysis.

The listening-edition ZIP contains MP3s, artwork, player, playlist and lyrics. The studio-sources ZIP contains original code, scores, MIDI, notes, artwork and verification. WAV masters and the complete-album MP3 are separate files in this folder.

**Timed lyrics for the future site:** `windows-still-lit-timed-lyrics.zip` is a separate, audio-free package with 193 cues, 589 sung/chopped words and 1,662 phoneme events across all eight songs. It includes individual-track and full-album timelines, vocal roles, exact sample positions and matching audio checksums. Start with [the integration guide](lyrics/site-export/INTEGRATION.md). The site can import these assets when its player is ready.

No third-party vocoder, speech synthesizer, voice bank, learned voice model, speech recording or third-party source code is vendored. The singer is an original, deliberately robotic formant instrument driven by a phoneme score. It is not commercial VOCALOID software or a named person's voice. Standard General MIDI playback approximates the instruments; use the original engine and event scores to reproduce the phonetic singing and effects.

The build uses installed `clang++`, Python, FFmpeg and FFprobe. Verification also uses installed NumPy; player checks use installed Node. No speech or vocoder package is needed.

Read `LINER-NOTES.md` for production choices and rebuild commands; `LYRICS.md` contains every lyric. Technical checks are not a human listening review. This local edition has not been published to a platform.
