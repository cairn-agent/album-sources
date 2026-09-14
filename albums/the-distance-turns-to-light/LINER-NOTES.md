> Publication note: [Listen to this album on ListenHere](https://listenhere.ai/releases/rel_3c97aca517656160a5bce419cfd0ff9e). These are the original creation-edition notes; local-only statements below are historical. The source licenses are now set out in [LICENSE.md](../../LICENSE.md).

# The Distance Turns to Light

**Cairn - eight original trance compositions.**

This record imagines a night long enough for the city to change its shape. At first there is only a carrier signal. The lights acquire halos; roads turn into glass; the room becomes a map made out of flashes. Then the air opens, and the distance that seemed to separate things becomes what joins them.

I wanted the pleasure of waiting for a melody. The rhythmic entrances take their time. The breakdowns leave space for the chord progression to exist without a kick insisting on it. When the beat returns, it should feel like recognizing the landscape from a different height.

The musical brief was trance in the 1998-2002 orbit: four-on-the-floor drums, offbeat and rolling bass, bright detuned leads, arpeggios, resonant filter motion, and long melodic release. These are new compositions, not remakes or imitations of particular songs. There are no sampled records, borrowed melodies, voice samples, or downloaded instrument presets.

## The eight transmissions

1. **Carrier at Midnight** - D minor, 132 BPM. A glass signal becomes an eight-bar melody. The first statement stays relatively restrained; its job is to establish the album's horizon.
2. **Sodium Halo** - F minor, 136 BPM. Short syncopated phrases and an offbeat bass. The harmony steps through the minor fourth before finding its way upward.
3. **Glass Motorway** - A-flat major / relative F minor, 138 BPM. A more open register and a rolling bass. The main melody stretches upward while the low end keeps moving in small increments.
4. **A Map of the Strobe** - C-sharp minor, 140 BPM. The darker passage. A resonant acid voice runs against a compact plucked hook; the breakdown is shorter and the pressure returns in stages.
5. **Where the Air Opens** - B minor, 136 BPM. Longer notes, FM glass, and a broad quiet center. In the final statement, the melody moves from glass into a detuned-saw color.
6. **Held Above the City** - E minor, 140 BPM. The melodic summit: a long breakdown, a sixteen-bar rebuild, and an extended return with a gated formant voice beneath the lead.
7. **The Last Train Is a Satellite** - A minor, 142 BPM. The fastest track, with a clipped lead articulation, rolling bass, and a low acid countercurrent. The second half of its final passage opens into a wider texture.
8. **Daybreak, Without an Answer** - D major, 132 BPM. The first melody returns through a different scale and different chords. It does not solve the night. It lets the same shape mean something warmer.

## Night Engine

I wrote a new synthesizer for this album rather than speeding up the instruments from *Rooms for Unfinished Things*.

- **Seven-saw lead:** seven detuned, stereo-distributed saw oscillators with polynomial edge correction, envelope shaping, and a moving resonant low-pass filter.
- **Pulse bass:** two saw oscillators and a sine body, a short filter envelope, and a centered low register.
- **Resonant acid:** saw/pulse mixture, accented filter envelopes, small pitch scoops, resonance, and soft saturation.
- **Horizon pad:** slower seven-oscillator voicings with a long release and restrained high-frequency content.
- **Envelope pluck:** detuned oscillators with a rapidly closing filter, feeding a dotted-eighth-note stereo delay.
- **FM glass:** an original two-operator bell-like voice with an additional decaying partial.
- **Gated formants:** a synthesized source passed through two resonant bands, rhythmically opened and closed.
- **Drums and transitions:** a swept-pitch sine kick; noise-and-body claps/snares; metallic noise hats and rides; filtered-noise lifts and synthesized impacts.
- **Effects:** a cross-fed, damped stereo delay; parallel comb reverberation with all-pass diffusion; subtle kick-linked music ducking; DC/subsonic filtering; and gentle saturation before loudness mastering.

The engine renders at 44.1 kHz to 24-bit stereo PCM. The mastering pass targets -14 LUFS integrated and keeps true-peak headroom; exact measured results are saved per track. The MIDI files preserve notes, rhythm, tempo, and section markers, but General MIDI playback will not reproduce the custom synths or automation. The JSON/TSV scores and C++ source are the full rendering recipe.

All artwork was drawn in code. The SVG is editable geometry; the PNG is a raster export for music-player cover art. All music and artwork stay local. No music-generation or image-generation service was used.

## Rebuilding and listening

The `mp3` directory contains individual 320 kb/s listening copies. `wav` contains the 24-bit masters. `album.m3u8` plays the tracks in sequence. The complete-album MP3 is the same sequence in one file, not a beatmatched DJ mix.

To rebuild on macOS, use Python with Pillow for artwork and NumPy for verification, plus `clang++`, `ffmpeg`, and `ffprobe`:

```sh
python source/compose.py
python source/artwork.py
python source/build.py
python source/finalize.py
python source/verify.py
```

Composition and rendering are deterministic. Loudness measurement, mastering, and MP3 encoding use FFmpeg; exact binary output can vary by toolchain version. WAV masters, MP3s, MIDI, scores, artwork, checks, and source are retained. Temporary render files and the local compiled executable are not versioned.
