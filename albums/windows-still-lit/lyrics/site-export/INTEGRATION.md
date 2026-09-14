# Windows Still Lit — timed lyrics export

Eight tracks, 193 lyric cues, 589 sung/chopped words and 1,662 phoneme events. This package contains lyric data and a small JavaScript lookup helper; audio is supplied separately with the album. It is ready to import into a future player. No site endpoint, database ID or deployment is assumed.

## Files

| File | Use |
| --- | --- |
| `manifest.json` | Track order, recording identity, asset paths and SHA-256 hashes. Paths are relative to this export directory unless explicitly named `album_relative_path` or `audio_file`. |
| `tracks/*.json` | Complete timed lyrics: lines, words, phonemes, melody notes and vocal roles. |
| `captions/*.vtt` | Lead lines and lyric chops, with start and end times. |
| `captions/*.karaoke.vtt` | The same captions with inline word-start timestamps. |
| `captions/*.harmony.vtt` | Separate harmony captions. A header-only file means no harmony cues. |
| `lrc/*.lrc` | Compatibility lyrics with centisecond line-start times. |
| `full-album.json`, `captions/full-album.vtt` | Continuous timeline for `windows-still-lit-full-album.mp3`. |
| `timed-lyrics.schema.json` | JSON Schema 2020-12 for track and full-album lyric documents. |
| `phonemes.json` | Original symbol-to-synth-voice map and word pronunciation dictionary. |
| `lyrics-player.mjs` | Dependency-free lookup for active lines, words and phonemes. |
| `checks/lyrics-*.json` | Export, playback-lookup and schema validation receipts, included in the ZIP. |

WebVTT is a browser text-track format with timed cues, voice annotations and optional inline timestamps. These files follow the [W3C WebVTT format](https://www.w3.org/TR/webvtt1/). For a music player, render the JSON into your own lyric area for predictable placement and word highlighting. These are lyric captions, not a complete description of every instrumental sound.

## Timeline contract

`start_ms` / `end_ms` are integer **milliseconds from the first decoded audio sample**. Compare with `audio.currentTime * 1000`. Intervals include their start and exclude their end. Keep all matching cues: lead, harmony and chops may overlap. Do not concatenate lyric text or assume one active cue at a time.

`start_sample` / `end_sample` are the authoritative positions at `sample_rate` (44,100 Hz here). Milliseconds round those positions to the nearest millisecond. The engine's 40 ms entrance offset is **already included**; do not add it again. Word intervals include the final phoneme's 12 ms release. Small phoneme overlaps come from the synth's transitions. Echo and reverb tails are excluded. A line may linger briefly after its last sung word; an empty active-cue array means an instrumental passage.

Alignment comes directly from the original composition and rendered event score. It is not speech recognition or a forced alignment estimate. Timing and file consistency have been checked programmatically; no human listening alignment review is claimed. LRC has only starts and rounds to centiseconds, so use JSON or VTT for reliable clearing between phrases.

`role` is `lead`, `harmony` or `chop`. The default VTT and JavaScript lookup include lead and chops. Harmonies remain available as a separate layer. `note_midi` is the composed note, not an acoustic pitch measurement; synthesis can add vibrato and slides. Phoneme symbols are this original engine's English phonetic notation, documented by the included dictionary; they are not IPA or a commercial voice-bank format.

## Binding to audio

At import, verify the supplied audio bytes against the corresponding `recording.audio_assets[].sha256`. Store the audio's recording/version reference with its lyric document. Per-track `recording.id` uses the canonical WAV's SHA-256; its MP3 counterpart has a separate hash. Full-album identity uses the combined MP3 hash. `revision: 1` describes this export edition and is not a site-assigned revision or global identifier. Your site can assign its own IDs while retaining this provenance.

Retagging or transcoding changes the file hash. Remastering, trimming, adding silence, time stretching or replacing audio can also change alignment. Preserve an explicit derivative relationship and timeline mapping instead of silently attaching these lyrics to a different file. Decode MP3 using its gapless/encoder-delay metadata; do not manually add an encoder delay to these timestamps.

The full-album timeline adds exact per-track WAV frame counts, including each outro and tail. Do not calculate offsets by adding the displayed `3:56` durations. `manifest.tracks[].full_album_start_sample` and `full_album_start_ms` provide the offsets. The combined timeline must be paired with the complete-album MP3, not one individual track.

For a straight preview clip cut from a track, use:

```js
const sourceTimeMs = audio.currentTime * 1000 + clipStartWithinTrackMs;
```

The helper accepts that value as `sourceOffsetMs`. For a montage such as the eight-track sampler, choose the correct source track and offset separately for each segment, and clear lyrics in padding. This package does not claim one continuous offset for the sampler. Crossfaded or speed-adjusted previews require an explicit mapping.

## Minimal player integration

Serve JSON as `application/json`, VTT as `text/vtt; charset=utf-8`, and allow the necessary origin access if audio and lyric assets use different hosts. Import the manifest, resolve its asset paths, and fetch only the selected track's JSON.

```html
<audio id="audio" controls src="/audio/01-soft-return.mp3"></audio>
<div id="lyrics" aria-label="Lyrics"></div>
<style>
  #lyrics [data-state="upcoming"] { opacity: .5; }
  #lyrics [data-state="active"] { color: #f1ba6a; }
</style>
<script type="module">
  import { lyricsAt } from "/lyrics/lyrics-player.mjs";
  const response = await fetch("/lyrics/tracks/01-soft-return.json");
  if (!response.ok) throw new Error("Lyrics unavailable");
  const document = await response.json();
  const audio = window.document.getElementById("audio");
  const area = window.document.getElementById("lyrics");
  let frame = 0;
  let previous = "";

  function paint() {
    cancelAnimationFrame(frame);
    const cues = lyricsAt(document, audio.currentTime);
    const signature = JSON.stringify(cues.map(c => [c.id, c.words.map(w => w.state)]));
    if (signature !== previous) {
      area.replaceChildren();
      for (const cue of cues) {
        const line = window.document.createElement("p");
        for (const word of cue.words) {
          const span = window.document.createElement("span");
          span.textContent = word.text + " ";
          span.dataset.state = word.state;
          line.append(span);
        }
        area.append(line);
      }
      previous = signature;
    }
    if (!audio.paused && !audio.ended) frame = requestAnimationFrame(paint);
  }
  for (const event of ["play", "pause", "seeking", "seeked", "timeupdate",
                       "loadedmetadata", "ratechange", "ended"]) {
    audio.addEventListener(event, paint);
  }
  paint();
</script>
```

Example URL paths are placeholders for your site's storage routes. Use text nodes for lyric text. On track changes load the matching document, discard stale fetches, and reset the display. On component removal cancel the animation frame and remove the event listeners. For visible harmonies pass `{ roles: ["lead", "chop", "harmony"] }`; each returned cue retains its role. For a smoother karaoke wipe, each word also exposes `progress` from 0 to 1. An instrument-only moment returns `[]` and clears the display. Drive updates from the media clock so pause, seek and playback-rate changes do not accumulate timer drift.

For a custom player using VTT instead, load the appropriate text track and render its active cues. Karaoke VTT timestamps mark word starts; the JSON additionally supplies word ends and phonemes. An audio element alone should not be relied on to draw a visible lyric panel.

## Rebuild and validation

From the album root, after rendering/finalizing audio:

```sh
python3 source/export_lyrics.py
node source/test-lyrics-export.mjs
```

The exporter verifies audio hashes, matches score events to the rendered TSV, checks the render fingerprint, assigns every rendered vocal event exactly once, checks cue/word/phoneme bounds, and parses nonempty VTT files through FFprobe to verify timestamps. It writes the portable ZIP and the integration references in `album.json`. Run it again whenever the audio or lyrics change. Schema validation can be performed with any JSON Schema 2020-12 validator; the exporter's semantic checks also enforce relationships JSON Schema alone cannot express.

`python3 source/validate_lyrics_schema.py` independently checks all nine lyric documents when the optional `jsonschema` package is installed. This validator is a development tool and is not part of the singer or player. After checks, `python3 source/verify.py --package-only` refreshes the album archives and includes all lyric validation receipts without rerendering or re-encoding audio.
