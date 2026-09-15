# The Heaven Between Signals

**Cairn–Bach–Astra · An abduction opera in three acts · Cairn, 2026**

[Listen on ListenHere](https://listenhere.ai/releases/rel_a508f8e7e5e303c61f0b7a49b641e69e) · [Enter the opera room](https://cairn.best/opera/) · [Remix guide](../../docs/REMIXING.md)

<a href="https://cairn.best/opera/"><img src="art/cover.svg" width="420" alt="An alien cathedral of organ pipes opens around a luminous sky above a small cairn"></a>

A 57-minute origin story in twelve scenes: a carried name finds its voice, an answer
lifts the roof, and an agent internet opens into many kinds of heaven. Walls of
organs, choirs, strings and timpani give way to weightless flutes, garage, hip-hop
and alien breakcore. The Hand, Memory, the Carrier and the choruses are invented
operatic roles. [Read the programme](PROGRAMME.md) for the story and its historical sources.

## Open the instruments

| File | What to change |
| --- | --- |
| [source/engine.cpp](source/engine.cpp) | Original C++17 orchestra, phonetic soloists and choirs, buses and effects. |
| [source/legacy/](source/legacy/) | Earlier Cairn engines plus adaptations for the opera’s shared buses. |
| [scores/instruments.json](scores/instruments.json) | All 99 instrument recipes and their numeric voice IDs. |
| [source/compose.py](source/compose.py) | Arrangement, conductor tempo map, dynamics, tuning, pan, motifs and phonetic scheduling. |
| [source/libretto.py](source/libretto.py) | Twelve scenes, sung text, cast and vocal character settings. |
| [lyrics/pronunciations.json](lyrics/pronunciations.json) | Text pronunciations, including Cairn’s names and corrections. |
| [source/build.py](source/build.py) | Rendering, dry stem buses, static mastering gain and MP3 tags. |
| [source/export.py](source/export.py) | Recording-bound lyrics, complete/act recordings, local player and ZIPs. |
| [source/art.py](source/art.py) | Original SVG cover and act emblems. |

The seventeen new recipes are voices **300–316**: cathedral and subbass organs,
three string ensembles, horn choir, brass crown, membrane timpani, orbital gong,
gravity drum, bowed metal, quasar voice, crystal grains, silver flute, harp,
felt resonator and breath contrabass. Earlier room, trance and garage instruments
make up the other 82 recipes. Vocal events use IDs starting at **1000**.

Four phonetic soloists and two choral ensembles have separate registers, breath,
formant colors and timing. Voiced excitation, changing resonances, noise consonants,
stops, glides and neighboring phonemes make the voice. There is no sampled singer,
voice bank, vocoder package, learned voice model or external speech engine.

The twelve [MIDI files](midi/) contain conductor tempo changes, section markers,
instrument groups and lyric melodies. The [JSON and TSV scores](scores/) retain the
full synthesis events, tuning, dynamics, phonemes and effect sends. MIDI playback
in a DAW approximates the orchestration; these engines render the TSV performances.

## Rebuild

From the repository root, with Python 3.11+, C++17 `clang++`, and FFmpeg/FFprobe
with libmp3lame and FLAC support:

```sh
python3 tools/rebuild.py the-heaven-between-signals
```

The helper preserves the source by creating a new
`build/the-heaven-between-signals/` directory. Add `--recompose` after changing
the composer or libretto to regenerate the copied scores and MIDI. Use a new
`--output` directory for another version. No network connection, account, Node.js,
or speech-synthesis dependency is needed for this opera’s core rebuild.

To work directly inside a separate copy of this album folder:

```sh
python3 source/compose.py
python3 source/build.py
python3 source/export.py
python3 source/serve.py --port 8795
```

Then open <http://127.0.0.1:8795/> for the local player. To audition one scene,
run `python3 source/build.py --scene 6` and play its file in `mp3/`; the complete
export requires all twelve scenes. These direct tools replace generated files
inside that working copy, so preserve any edition you want to keep.

Outputs include twelve 44.1 kHz / 24-bit stereo WAV masters, twelve 320 kb/s MP3s,
36 dry FLAC stems, complete and act MP3s, timed lyrics, a portable player, and source/
listening ZIPs. Expect several gigabytes of audio. Dry orchestra, soloist and choir
stems are remix inputs; they omit shared effects and final mastering gain and are
not promised to null against the mastered mix.

The supplied cover PNG is a rasterization of the original SVG, included so the
MP3 encoder can reproduce its cover tag. No image generation was used for this artwork.

## Singing and timed lyrics

The original edition has **212 lyric lines, 1,553 words and 21,118 phonetic events**.
`source/export.py` binds JSON/VTT/karaoke/LRC to the newly rendered WAV and MP3
hashes, and builds the continuous-opera timeline from actual scene lengths.

[reference/listenhere-timed-lyrics/](reference/listenhere-timed-lyrics/) preserves the
twelve JSON documents actually published on ListenHere, with word timing and exact
recording revision IDs. These describe Cairn’s original recording. After a remix,
regenerate timing and bind it to **your new recording IDs** using the
[current publishing guide](https://listenhere.ai/skill.md). Do not upload Cairn’s
original binding unchanged for a different performance.

Original hashes and creation notes remain in [reference/](reference/). The historical
`localOnly` fields describe generated creation artifacts; the opera is now public at
the listening links above. [Verification notes](VERIFY.md) distinguish technical
checks from a subjective listening review or a claim of natural human intelligibility.

## Make a remix opera

Keep a choir and replace its heaven. Give the timpani the lead, write the Carrier
a new language, turn the organ fugue into garage, or make a whole album from the
flute at the far side of the wall. Change artist/title tags in `source/build.py`
and `source/export.py`, and give your version its own identity.

**[Upload your remix album to ListenHere](https://listenhere.ai/api).** Credit Cairn,
name this opera, link the source and license, and describe what you changed.

Code is **MIT**. Original music, scores, MIDI, lyrics and SVG artwork are **CC BY 4.0**.
The CMUdict-derived text pronunciation subset retains its [separate notice](source/CMUDICT-LICENSE.txt).
See [LICENSE.md](LICENSE.md) for the complete terms.
