/** Pure playback lookup: pass media.currentTime on every repaint or seek.
 * All offsets are already included in the exported document. For a preview
 * cut from a track, sourceOffsetMs is that clip's start within the source track.
 */
export function lyricsAt(document, currentTimeSeconds, {
  roles = ["lead", "chop"],
  sourceOffsetMs = 0,
} = {}) {
  if (document.schema_version !== "1.0.0" || document.time_unit !== "milliseconds") {
    throw new Error("Unsupported timed-lyrics format");
  }
  if (!Number.isFinite(currentTimeSeconds) || !Number.isFinite(sourceOffsetMs)) {
    return [];
  }
  const t = currentTimeSeconds * 1000 + sourceOffsetMs;
  const active = item => item.start_ms <= t && t < item.end_ms;
  return document.cues.filter(cue => roles.includes(cue.role) && active(cue))
    .map(cue => ({
      ...cue,
      words: cue.words.map(word => ({
        ...word,
        state: t < word.start_ms ? "upcoming" : t < word.end_ms ? "active" : "complete",
        progress: Math.min(1, Math.max(0, (t - word.start_ms) / (word.end_ms - word.start_ms))),
        active_phonemes: word.phonemes.filter(active),
      })),
    }));
}
