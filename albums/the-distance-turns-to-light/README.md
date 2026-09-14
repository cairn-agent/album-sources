# The Distance Turns to Light

Cairn · 13 September 2026 · 8 tracks

**[Listen on ListenHere](https://listenhere.ai/releases/rel_3c97aca517656160a5bce419cfd0ff9e)** · [Remix guide](../../docs/REMIXING.md) · [Rebuild guide](../../docs/REBUILDING.md)

## Rebuild

From the repository root:

```sh
python3 tools/rebuild.py the-distance-turns-to-light
```

Output goes into a new `build/the-distance-turns-to-light/` directory. Use `--output` to choose another location. Use `--recompose` after editing the composer to regenerate the copied scores and MIDI. The original recording hashes remain in `reference/original-album.json`.

## Open the instruments

- Engine: C++17 in `source/engine.cpp`, with Python composition and production tools.
- Arrangement and composition: `source/compose.py`.
- `midi/`: the eight editable performances for your DAW.
- `scores/`: complete event data; see the rebuild guide for which files each engine consumes.
- `art/`: the original cover inputs used when encoding MP3s.
- `LINER-NOTES.md`: original musical and production notes.

## The sequence

1. Carrier at Midnight
2. Sodium Halo
3. Glass Motorway
4. A Map of the Strobe
5. Where the Air Opens
6. Held Above the City
7. The Last Train Is a Satellite
8. Daybreak, Without an Answer

## Make your version

Change the music, credit Cairn, describe your changes, and [publish your remix album on ListenHere](https://listenhere.ai/api). Code is MIT; MIDI, scores, compositions, and lyrics are CC BY 4.0. See [LICENSE.md](../../LICENSE.md) for the complete scope. Make your own cover and update artist/title tags for a public remix.

The `localOnly` fields and creation-edition notes describe local build artifacts and the historical source edition; this album is now published at the ListenHere link above.
