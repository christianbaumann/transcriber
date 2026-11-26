# Slicer review

Brief for the one subagent that runs the vendored `video-slicer`. It replaces the slicer's step 5 (review): the slicer drops all demo frames, but tool screenshots can carry content the article needs, and the transcript tells which ones the speaker refers to. Steps 1 to 4 and 6 stay as in the slicer's `SKILL.md`. This file must track changes to that step 5.

The orchestrator passes the inputs as absolute paths.

| Name | Meaning |
|---|---|
| `VIDEO` | The video file. |
| `SLICER` | `.claude/skills/video-slicer/` in this repository (holds `SKILL.md` and `scripts/`). |
| `WHISPER` | `whisper.json` of the video. |
| `TRANSCRIPT_PY` | `transcribing-talks/scripts/transcript.py`. |

## Steps

1. Read `$SLICER/SKILL.md`. Run its steps 1 to 4 on `VIDEO` (sample, crop box, detect, contact sheet). Step 3 needs a timeout of at least 10 minutes.
2. For each candidate (the map from step 4 gives `#N HH:MM:SS`), write the transcript excerpt of its time range to the work directory: from the candidate's start to the next candidate's start (the last: to the video's end).

   ```bash
   "$TRANSCRIPT_PY" "$WHISPER" --excerpt HH:MM:SS-HH:MM:SS > "$WORK/excerpts/NNNN.txt"
   ```

3. Do the slicer's step 5, with these changes to its drop rules:
   - Live demo frames (IDE, terminal, browser filling the shared screen): keep the candidate when its excerpt shows that the speaker refers to it, for example "here in the IDE", "as you can see", or an explanation of what is on screen. Drop it when the excerpt does not refer to the screen.
   - All other rules stay: drop frames without a slide (speaker, audience, black, transition), repeats (keep the earliest), and earlier steps of a slide build (keep the final state). Keep every other candidate.
   - Name the excerpt as the reason for every kept demo frame and for every dropped one.
4. Run the slicer's step 6 (export) to the default `<video>-slices/` next to `VIDEO`, then remove the work directory.

Reply with: output path, crop box, candidate count, kept count, kept demo frames (number, time, what the speaker says about it), dropped candidates with reasons, layout warnings.
