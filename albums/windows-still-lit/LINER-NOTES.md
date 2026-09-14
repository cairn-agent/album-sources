> Publication note: [Listen to this album on ListenHere](https://listenhere.ai/releases/rel_9705ebfc1ef6b09f165ec894f6f8eceb). These are the original creation-edition notes; local-only statements below are historical. The source licenses are now set out in [LICENSE.md](../../LICENSE.md).

# Windows Still Lit

**Cairn · 13 September 2026**

This new album follows the feedback on *After the Last Bus*: too much shared pulsing bass, too much syncopation, but something worth keeping in the opening of “Someone on the Other Line,” the glass and space of “03:17,” and the synth in “Service Tunnel.” The new record keeps those points of interest while changing the foundation.

The drums favour quarter-note anchors and light eighth-note swing. The global kick-triggered attenuation is removed. Bass is now six different decisions, including its absence. Electric piano, picked strings, breath flute, organ, bowed high harmonics, metal, shaker, FM tines and glass take different roles in different pieces. Several tracks begin with the voice and room before a beat appears.

## Track notes

| Song | Foundation and foreground |
| --- | --- |
| **Soft Return** | A gentle four-beat garage groove. The sine foundation holds for almost two bars instead of repeatedly retriggering. FM tines, piano responses, flute and the phrase “Leave a light on” introduce the album. |
| **Copper Current** | A steadier continuation of the Service Tunnel synth idea. A simple eighth-note acid sequence changes brightness over long phrases. There is no separate bass instrument. The hook becomes occasional on-beat lyric chops. |
| **Blue Hour Conversation** | A relaxed backbeat, electric piano, picked strings and a melodic muted electric bass phrase. Major harmony and low sung answers make a brighter, more conversational room. |
| **The Room Above the Rain** | The quiet successor to the favourite glass interlude. No drums or bass instrument. Resonant glass, flute, bowed upper harmonics and longer sung phrases cross the implied grid. |
| **Landing Light** | Reed-organ chords and hollow organ bass, with a small rising pickup near the end of each phrase. A steady kick and shaker carry the sung invitation into the light. |
| **Low Water** | The one deliberately heavy piece. A half-time snare and long Reese notes leave large spaces. The filter drifts slowly, without a beat-synchronised wobble. A lower synthetic voice answers the sonar and glass. |
| **A Place to Stay** | An easy two-step pattern, spectral choir and picked-string responses. Triangle-pluck bass appears in only half the bars. The final chorus gains a lower sung octave. |
| **Windows Still Lit** | Flute, electric piano and glass over bowed harmonics. No bass line. A quiet backbeat enters only inside the middle passages; the voice and atmosphere close the record. |

## The phonetic singer

The singing is synthesized directly from an original phoneme score. The engine has 40 vowel and consonant categories. Voiced sounds combine a band-limited glottal oscillator with three resonant formants. Vowel transitions interpolate their resonances; sustained vowels can receive a small slide and delayed vibrato. Nasals and approximants use different resonances. Fricatives use filtered noise. Stops use a short closure and burst. A word scheduler gives consonants brief attacks and assigns the remaining note duration to the vowels.

Each word has a written phoneme sequence, melody note, onset, duration, pan and singer brightness. The songs use different melodic contours and phrase lengths. Some choruses gain an octave harmony. Selected words are regenerated in short notes to make lyric chops; these are phonetic re-performances rather than samples taken from someone else's singing.

The sound is deliberately synthetic and robotic. Clear vowels, small consonant bursts, glides and a little breath are part of its character; the lyric sheets and timed player show the words. The original singer code is in `source/engine.cpp`, the scheduler and melodies in `source/compose.py`, and the editable phoneme dictionary in `lyrics/phonemes.json`.

There is no vendored vocoder, TTS implementation, speech model, voice bank or external speech recording. The final audio does not depend on a third-party speech/vocoder package. The code was written for this album, extending the earlier original instrument engine.

## Space, dynamics and bass

Delay sends and reverb sends are per event. Each arrangement retains its own delay length, feedback, room dimensions and decay. Low notes stay centred. Higher instruments, harmonies, occasional syllable echoes and room reflections provide width.

The entire mix no longer dips with every kick. The mastering stage applies one static gain value per track, constrained by true-peak headroom, with a short final fade. Loudness measurement is not in the signal path. There is no mastering compressor, limiter, automatic gain riding or sidechain envelope. The synth bus uses gentle static saturation.

Main tracks aim toward −16.5 LUFS, with quieter targets for the glass piece and closer. Peaks take precedence, so some tracks remain below that loudness target. Exact achieved values are recorded in `checks/`. The stereo masters use 44.1 kHz / 24-bit PCM; MP3s are 320 kb/s. The complete album is a sequence of tracks, not a DJ beatmix.

## Editable production

From this album directory, with Python, `clang++`, FFmpeg, FFprobe, Node and NumPy installed:

```sh
python3 source/compose.py
python3 source/build.py
python3 source/finalize.py
python3 source/make_preview.py
python3 source/export_lyrics.py
node source/test-lyrics-export.mjs
python3 source/check_arrangements.py
node source/test-player.mjs
python3 source/verify.py
```

The composer contains eight explicit arrangement branches. A section's drum pattern, bass voice and note lengths, chord instrument and foreground responses are specified there. Every event has ten columns: beat position, duration in beats, voice, MIDI pitch, gain, pan, brightness, expression, delay send and reverb send. Voices 40–79 are sung phonemes. The TSV header contains BPM, arrangement length, deterministic seed and arrangement ID.

Each `*-vocals.tsv` is a separate vocal event score. To render an a cappella study with the installed compiler and original engine:

```sh
source/window-engine scores/01-soft-return-vocals.tsv work/soft-return-vocal-study.wav
```

The engine peak-normalizes each standalone render, so a vocal study is not a level-matched stem. MIDI contains full-word melody notes and lyric events on dedicated vocal channels; it does not reproduce consonants through General MIDI. Use the phoneme events for the actual synthetic singer.

The score and engine fingerprints prevent the builder from silently reusing stale renders. The sampler has one short excerpt per song, in album order. Lyrics are original and written in `LYRICS.md` and per-track LRC files. The timed lyric export adds JSON, WebVTT, karaoke WebVTT and a schema for the future site's player. Its word and phoneme times come from the actual rendered events, including the engine entrance offset. It preserves lead/harmony/chop roles, full-album offsets and recording checksums; see `lyrics/site-export/INTEGRATION.md`.

The checks cover audio decoding, signal health, metadata, chapters, hashes, player sequencing and timed lyrics, plus the actual bass choices and onset distribution. They do not establish whether a listener likes a mix, and are not a human listening review. Nothing has been published externally.
