---
id: 07
status: done
dependencies: []
---

# Task 07: Reference talks ground truth

Both reference talks have a committed, known-good description of their slides that evals can compare skill output against.

## Outcome

For each talk, `testdata/talks/<name>/` holds the video and decks (gitignored) and committed ground truth: one PNG per slide (final state, from the PDF) and slide text with speaker notes (from the .pptx). Commit message direction: "Add slide ground truth for two reference talks".

## References

* `design.md#reference-talks-for-evals`
* Source files in `~/Downloads`:
  * `Don’t be a fool with a tool ‒ fundamental knowledge for proper test automation (720p_24fps_H264-192kbit_AAC).mp4`, `Don’t be a fool with a tool - askui Hackathon 2023-03.pptx`, `.pdf` (55 slides)
  * `2020 EclipseCon.mp4`, `Extreme learning situations as testers EclipseCon.pptx`, `.pdf` (31 slides)
* Skill `pptx-to-markdown` (slide text and notes)
* Touches: `testdata/talks/` (new), `.gitignore`, `CLAUDE.md` (Reference talks)

## Work

* [x] Copy the files into `testdata/talks/fool-with-a-tool/` and `testdata/talks/extreme-learning-eclipsecon/` with short names (`video.mp4`, `deck.pptx`, `deck.pdf`)
  **Note:** Copied from `~/Downloads` (originals untouched); `scripts/restore-testdata.sh` restores them on a fresh clone (tested on a clone of the branch).
* [x] Gitignore the video and deck files, keep the folders
* [x] Render each PDF page to `slides/NN.png` (final state of animated slides)
  **Note:** `pdftoppm -r 100`, quantized to PNG8 (1000x563); 13.2 MB in total.
* [x] Convert each .pptx to `slides.md` with the `pptx-to-markdown` skill (text + speaker notes per slide)
  **Note:** Image links and alt-text placeholders of the converter output dropped; the PNGs carry the images. Text, footers and speaker notes kept.
* [x] Write `talk.json` per talk: title, speaker, event, date, duration, slide count, animated slides (askui: 7 slides with entrance effects)
  **Note:** Durations from `ffprobe`; title and speaker from the title slides; dates from file name and design (askui `2023-03`, EclipseCon `2020` only). Animated askui slides 2, 16, 17, 22, 23, 39, 42 (20 entrance effects, found via `p:timing`); EclipseCon none.
* [x] Document in `CLAUDE.md` how to restore the gitignored files on a fresh clone

## Verification

* [x] Slide PNG counts: 55 and 31, equal to the PPTX slide counts
  **Note:** Verified via `ls | wc -l`, `pdfinfo` and the slide XML count of each pptx: 55 and 31; no hidden slides.
* [x] `slides.md` has one section per slide, same numbering as the PNGs
  **Note:** Verified via `# Slide N` heading counts (55, 31) and spot checks of 4 slides per talk against the PNGs.
* [x] `git status` shows ground truth files, not video or decks
  **Note:** Verified via `git ls-files testdata` (86 PNGs, 2 `slides.md`, 2 `talk.json`) and `git check-ignore` on video and decks.
* [x] Animated askui slides show their final state in the PNG
  **Note:** Verified by viewing PNGs 2, 16, 17, 22, 23, 39, 42 against the animated shapes in the pptx XML: all shapes visible.
