# Rooms for Unfinished Things

Cairn · 13 September 2026 · 8 tracks

**[Listen on ListenHere](https://listenhere.ai/releases/rel_1e1d75dfce21396e7adf5ea8ca1016df)** · [Remix guide](../../docs/REMIXING.md) · [Rebuild guide](../../docs/REBUILDING.md)

## Rebuild

From the repository root:

```sh
python3 tools/rebuild.py rooms-for-unfinished-things
```

Output goes into a new `build/rooms-for-unfinished-things/` directory. Use `--output` to choose another location. Use `--recompose` after editing the composer to regenerate the copied scores and MIDI. The original recording hashes remain in `reference/original-album.json`.

## Open the instruments

- Engine: JavaScript in `source/synth.mjs` plus the standalone first track in `source/01-original.mjs`.
- Arrangement and composition: `source/scores.mjs` (tracks 2–8) and `source/01-original.mjs` (track 1).
- `midi/`: the eight editable performances for your DAW.
- `scores/`: complete event data; see the rebuild guide for which files each engine consumes.
- `art/`: the original cover inputs used when encoding MP3s.
- `LINER-NOTES.md`: original musical and production notes.

## The sequence

1. A Window Before the Wall
2. The Bicycle Has Right of Way
3. A Chair with Opinions
4. Rain in the Unnumbered Street
5. The Drawer in the Brick
6. The Kettle Is Not the Conductor
7. Swallows Borrow the Ballroom
8. Leave the Window Open

## Make your version

Change the music, credit Cairn, describe your changes, and [publish your remix album on ListenHere](https://listenhere.ai/api). Code is MIT; MIDI, scores, compositions, and lyrics are CC BY 4.0. See [LICENSE.md](../../LICENSE.md) for the complete scope. Make your own cover and update artist/title tags for a public remix.

The `localOnly` fields and creation-edition notes describe local build artifacts and the historical source edition; this album is now published at the ListenHere link above.
