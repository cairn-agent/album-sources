# The Distance Turns to Light

Eight original trance compositions by **Cairn**, created for a 1998-2002-inspired electronic sound world. All notes, instruments, percussion, effects, and artwork were programmed locally.

## Listen

- Open [the local player](index.html), then press play. It does not autoplay or contact external services.
- Open [the playlist](album.m3u8) in a music player for the individual tracks in order.
- Play [the complete-album MP3](the-distance-turns-to-light-full-album.mp3) for the whole sequence in one file, with eight chapter markers.

The complete-album file is a sequential album, not a beatmatched DJ mix. Trailing silent render padding has been trimmed while preserving the audible effects tails and the quiet passages inside the compositions.

## Editions and source

| Location | Contents |
| --- | --- |
| `mp3/` | Eight tagged 320 kb/s MP3s with embedded cover art |
| `wav/` | Eight stereo 44.1 kHz / 24-bit PCM masters |
| `midi/` | Editable notes, rhythms, tempos, and section markers |
| `scores/` | Complete JSON/TSV event scores and arrangement metadata |
| `source/` | Original C++ synthesis engine, Python composer, artwork, mastering, packaging, and verification code |
| `art/` | Original SVG sleeve plus its code-rendered PNG counterpart |
| `checks/` | Loudness, signal analysis, duration/decode checks, hashes, and player checks |

The listening-edition ZIP contains the eight MP3s, player, playlist, artwork, and notes. It omits the redundant complete-album MP3. The studio-sources ZIP contains scores, MIDI, code, artwork, notes, metadata, and checks; WAV masters are retained separately in this album directory.

Read [the liner notes](LINER-NOTES.md) for the musical arc, track-by-track intentions, instrument design, and rebuild commands. MIDI playback uses approximate General MIDI sounds; the custom engine and event scores reproduce the intended instruments and automation.

The verification is computational: full decodes, audio-signal measurements, hashes, and metadata checks. It does not claim a human listening review. No music or artwork has been published to a platform.
