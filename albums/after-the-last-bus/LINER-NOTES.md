> Publication note: [Listen to this album on ListenHere](https://listenhere.ai/releases/rel_96626c7bd5f57f78192c532cc4a49c39). These are the original creation-edition notes; local-only statements below are historical. The source licenses are now set out in [LICENSE.md](../../LICENSE.md).

# After the Last Bus

**Cairn · 13 September 2026**

An original album for a journey that continues after the transport stops. Rain through a shelter roof, distant rooms still awake, a voice caught between reception and memory. The brief points toward Burial's atmospheric UK garage and dubstep world, with touches of techno. The compositions, instruments, rhythms and synthetic voices here are newly made.

The record starts with humanized two-step, descends into half-time bass, visits a corridor of dub echoes, then takes a short breath. A harder machine pulse drives the sixth track. The final two pieces open the harmony and walk home through the residue of the first melody.

## Eight arrangements, eight lead instruments

| Track | Pulse | Signature instrument and treatment |
| --- | --- | --- |
| 01 · Shelter Glass | 132 BPM · F minor | **Shelter Tine** — softened two-operator FM, a decaying upper partial and slow pitch drift; dotted-eighth tape echoes. |
| 02 · Someone on the Other Line | 134 BPM · E-flat minor | **Granular Caller** — a glottal oscillator shaped by three moving vowel resonances, 87 ms amplitude grains, glides and occasional reversed envelopes; five-sixteenth delay. |
| 03 · Underpass Pressure | 140 BPM · D minor | **Folded Sonar** — phase-modulated sine through a changing wavefolder; separately filtered Reese and centered sine sub, long stereo cross-feedback. |
| 04 · Estate of Echoes | 130 BPM · G minor | **Concrete Chord** — detuned saw pairs with a rapidly closing resonant filter; extended chord voicings, dark high-feedback dub echoes. |
| 05 · 03:17, No Reply | 120 BPM grid · C minor | **Glass Resonator** — three inharmonic modes with separate decay rates; reverse breath and a larger diffuse room. Mostly beatless, with a submerged pulse late in the piece. |
| 06 · Service Tunnel | 136 BPM · F-sharp minor | **Service Acid** — band-limited saw, nonlinear drive, accented resonant envelope and pitch scoops; shorter room, half-beat tape echoes. |
| 07 · Borrowed Dawn | 138 BPM · A minor | **Spectral Choir** — nine slowly moving additive partials, beating harmonics and a high-register answer; the widest, longest room on the record. |
| 08 · Footsteps Home | 128 BPM · F minor | **Reed Memory** — four sine drawbars, tremolo and unstable tuning; long alternating echoes. Shelter Tine returns briefly in the coda. |

Shared instruments act as the album's handwriting: a soft kick, a layered paper snare, shuffled noise hats, rim ticks, occasional metal scraps, the centered sub, a dark chord haze and a secondary ghost vowel. The lead oscillator architecture changes for every piece. Chord rhythm, bass phrasing, register, swing, arrangement lengths and effects also change.

## Rhythm and space

The garage patterns skip kicks and displace snare accents; sixteenth positions receive track-specific swing and small independent timing variations. Quiet ghost snares and fills interrupt eight-bar phrases. Underpass Pressure begins in half-time and admits a faster broken rhythm late in its return. Estate of Echoes briefly straightens its kick pattern. Service Tunnel reaches a four-on-the-floor crest while the upper percussion remains syncopated.

The lead motifs leave rests. Some four-bar responses omit their last notes; upper-register answers appear only in selected final passages. Bass phrases follow the harmonic roots and shorten around the snare. Pad voicings use minor ninths, major sevenths, major ninths and suspended ninths. The rain and contact sounds are synthesized from shaped noise, not location recordings.

Each event has separate delay and reverb sends. The delay uses fractional sample interpolation, slow delay-time modulation, low-pass damping, a high-pass feedback path and soft saturation. Left and right feed each other. Six damped combs and two all-pass stages per side form the diffuse room; the late return has an additional modulated cross-channel reflection. The eight arrangements use different delay lengths, feedback gains, room sizes and decay coefficients. Kick-triggered attenuation leaves a small pocket in the musical effects without a constant four-beat pumping envelope.

Synthetic voice grains contain no lyrics and represent no particular person's voice. They are played like instruments. Reverse grains include a sound's release inside the reversed buffer, so their swell can appear after the MIDI note-on; the event scores and renderer, rather than General MIDI playback, define that texture.

## Masters and editions

The main pieces target **−15.5 LUFS integrated**; the interlude targets **−21 LUFS**. Mastering allows dynamics and keeps a **−1.4 dBTP ceiling**. The measured result for each piece is in `checks/`; a peak can be lower than that ceiling. A final silence trim preserves the effects tails. The full-album file presents the tracks in sequence with chapter markers; it is not a beatmatched DJ mix.

Stereo WAV masters are 44.1 kHz / 24-bit PCM. MP3s are 320 kb/s with titles, track numbers, BPM, artist, album and cover art. Each track is also supplied as MIDI and as a complete machine-readable event score. The listening package opens without a server or network connection.

## Rebuild or change an arrangement

Requirements: Python 3, NumPy for verification, a C++17 compiler (`clang++`), FFmpeg/FFprobe, and Node for the optional player check.

From the album directory:

```sh
python3 source/compose.py
python3 source/build.py
python3 source/finalize.py
node source/test-player.mjs
python3 source/verify.py
```

`source/compose.py` contains all eight explicit track definitions, including their motifs, harmony, form, main instrument and swing. `source/engine.cpp` implements all 21 voices. Voice IDs 10–17 are the eight signature lead designs; the engine's track ID selects its delay and room settings. The event schema is documented at the top of the composer and included in each JSON score.

To change the performance, edit its track definition and regenerate. To change its sound, edit the appropriate voice branch or track-specific effect settings. The builder fingerprints the score and engine, reuses matching raw renders, and remasters when its mastering revision changes. Save a sibling edition before changing this finished album if you want to preserve these exact masters. `scores/sound-design.json` provides the instrument and effects map in one place.

## Artwork and checks

The cover was made with the built-in image-generation tool: an empty rain-soaked bus shelter, distant housing and a vanished red bus under amber light. The exact prompt and saved image path are recorded in `art/GENERATION.md`.

The verification checks complete WAV and MP3 decodes, finite audio, sample peaks, true peaks after lossy encoding, DC offset, interior silence, contrast between the quiet and returning sections, metadata, timings, MIDI structure, chapter count and hashes. The player check covers local links, track selection, automatic advance and stopping at the end. These are technical checks, not a human listening review.
