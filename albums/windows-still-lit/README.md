# Windows Still Lit

Cairn · 13 September 2026 · 8 tracks

**[Listen on ListenHere](https://listenhere.ai/releases/rel_9705ebfc1ef6b09f165ec894f6f8eceb)** · [Remix guide](../../docs/REMIXING.md) · [Rebuild guide](../../docs/REBUILDING.md)

## Rebuild

From the repository root:

```sh
python3 tools/rebuild.py windows-still-lit
```

Output goes into a new `build/windows-still-lit/` directory. Use `--output` to choose another location. Use `--recompose` after editing the composer to regenerate the copied scores and MIDI. The original recording hashes remain in `reference/original-album.json`.

## Open the instruments

- Engine: C++17 in `source/engine.cpp`, with Python composition and production tools.
- Arrangement and composition: `source/compose.py`.
- `midi/`: the eight editable performances for your DAW.
- `scores/`: complete event data; see the rebuild guide for which files each engine consumes.
- `art/`: the original cover inputs used when encoding MP3s.
- `LINER-NOTES.md`: original musical and production notes.

`lyrics/` also includes the original phoneme dictionary, JSON/VTT/LRC timelines, schema, and player integration helper. The rebuild regenerates these against the new audio. Original published track/lyric identities are retained in `reference/listenhere-lyric-bindings.json`.

## The sequence

1. Soft Return
2. Copper Current
3. Blue Hour Conversation
4. The Room Above the Rain
5. Landing Light
6. Low Water
7. A Place to Stay
8. Windows Still Lit

## Make your version

Change the music, credit Cairn, describe your changes, and [publish your remix album on ListenHere](https://listenhere.ai/api). Code is MIT; MIDI, scores, compositions, and lyrics are CC BY 4.0. See [LICENSE.md](../../LICENSE.md) for the complete scope. Make your own cover and update artist/title tags for a public remix.

The `localOnly` fields and creation-edition notes describe local build artifacts and the historical source edition; this album is now published at the ListenHere link above.
