---
id: 03
dependencies: []
---

# Task 03: Transcription and transcript

A video becomes a timestamped transcript of the spoken word, optionally with slide markers, and any time range of it can be extracted as text.

## Outcome

- `transcribe.py` runs `mlx_whisper` large-v3 with word timestamps on a video and writes `whisper.json`.
- `transcript.py` turns `whisper.json` into `transcript.md`: paragraphs with `[HH:MM:SS]`, and `→ slide NNNN` markers at slide times when a slices folder is given.
- `transcript.py --excerpt` prints the spoken text of a time range (input for slicer review and per-slide subagents).

Commit message direction: "Transcribe talks with word timestamps" and "Format transcript with timestamps and slide markers".

## References

* `design.md#interfaces`
* `design.md#transcription-with-mlx_whisper-large-v3`
* `design.md#transcript-and-article-are-separate-deliverables`
* Slice file names: `NNNN_HH-MM-SS.png` (video-slicer step 6)
* Touches: `.claude/skills/transcribing-talks/scripts/transcribe.py`, `scripts/transcript.py`, `scripts/tests/test_transcript.py`, `scripts/tests/fixtures/`, `CLAUDE.md` (Commands)

## Work

* [ ] `transcribe.py <video> --out <dir> [--language en|de|...] [--initial-prompt <text>]`: calls `mlx_whisper` (model large-v3, `--word_timestamps True`), writes `<dir>/whisper.json`, prints detected language
* [ ] `transcript.py <whisper.json> [--slices <dir>] --out transcript.md`: groups segments into paragraphs (pause-based), one `[HH:MM:SS]` per paragraph, slide markers placed at the word nearest to each slice timestamp
* [ ] `transcript.py <whisper.json> --excerpt HH:MM:SS-HH:MM:SS`: prints words in that range
* [ ] Unit tests for paragraphing, marker placement and excerpt with a small `whisper.json` fixture (no model run)
* [ ] Add test and run commands to `CLAUDE.md`

## Verification

* [ ] Unit tests pass without `mlx_whisper` installed
* [ ] On the EclipseCon video, `whisper.json` has word timestamps and `transcript.md` reads as paragraphs with timestamps
* [ ] With the EclipseCon slices, every slice has exactly one marker, in time order
* [ ] An excerpt of a range holds only words whose start lies in that range
* [ ] Detected language is printed and matches the talk's spoken language
