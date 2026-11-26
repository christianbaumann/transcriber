---
id: 03
status: done
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

* [x] `transcribe.py <video> --out <dir> [--language en|de|...] [--initial-prompt <text>]`: calls `mlx_whisper` (model large-v3, `--word_timestamps True`), writes `<dir>/whisper.json`, prints detected language
* [x] `transcript.py <whisper.json> [--slices <dir>] --out transcript.md`: groups segments into paragraphs (pause-based), one `[HH:MM:SS]` per paragraph, slide markers placed at the word nearest to each slice timestamp
* [x] `transcript.py <whisper.json> --excerpt HH:MM:SS-HH:MM:SS`: prints words in that range
* [x] Unit tests for paragraphing, marker placement and excerpt with a small `whisper.json` fixture (no model run)
* [x] Add test and run commands to `CLAUDE.md`

## Verification

* [x] Unit tests pass without `mlx_whisper` installed
  **Note:** Verified via the CLAUDE.md test command with `PATH` stripped of `mlx_whisper`: 16 passed (tests use `build_command` and `transcript` only).
* [x] On the EclipseCon video, `whisper.json` has word timestamps and `transcript.md` reads as paragraphs with timestamps
  **Note:** Verified via a full run on the EclipseCon video: 3567 words with start/end times, 84 paragraphs with `[HH:MM:SS]`, readable text. A first run looped on repeated sentences; fixed with `--condition-on-previous-text False`.
* [x] With the EclipseCon slices, every slice has exactly one marker, in time order
  **Note:** Verified with the 95 real video-slicer slices of the EclipseCon video: 95 unique markers, 0001 to 0095 in order. Unit tests cover duplicates, slices in silence and after the last word.
* [x] An excerpt of a range holds only words whose start lies in that range
  **Note:** Verified via unit tests (range, exclusive end, empty) and the CLI on the real `whisper.json`: word counts match the words with start in `[start, end)`.
* [x] Detected language is printed and matches the talk's spoken language
  **Note:** Verified via the full run and a 30 s clip run: `language: en`, talk is English.
