# Recording verification

This edition contains 57:05 of music in twelve scenes, with 212 lyric lines,
1,553 sung words, 21,118 phonetic events, and 99 instrument recipes.

- Twelve stereo 44.1 kHz / 24-bit WAV masters match their recorded SHA-256 hashes.
- All twelve 320 kb/s MP3 scenes decode completely. Their decoded timelines match
  the masters; a twenty-second comparison in each scene finds zero timing lag.
- Decoded sample peaks and measured intersample true peaks remain below 0 dBFS.
  Mastering uses static gain and retains the contrast between scenes.
- All 36 lossless dry stems decode and match their scene's sample count.
- The continuous opera and all three act recordings decode to the expected duration.
- Every line matches the original libretto. Word and phoneme timestamps fall
  within their phrases. The continuous lyric export uses the actual master lengths.
- All twelve multitrack MIDI files have complete track structures, conductor tempo
  events and lyric metadata. The complete instrument inventory appears in the scores.
- All four original SVGs parse as vector artwork. The cover PNG is an SVG rasterization.
- Desktop and mobile browser checks pass: playback advances, selecting a lyric
  seeks to its passage, words highlight, and the next scene starts automatically.
  Neither viewport has horizontal overflow. Automated WCAG A/AA checks report no
  violations in the tested page; no JavaScript errors were observed.
- The source and listening archives pass CRC and inventory checks. The listening
  edition includes its player assets, complete recording and remix source archive.

These are file, signal and browser checks, not a subjective listening review or
a claim that the phonetic singer has natural human intelligibility. The intended
words remain available in the synchronized libretto.

Detailed local results: `checks/verification.json` and `checks/browser.json`.
Run `python3 source/verify.py` to repeat the recording and package checks.
