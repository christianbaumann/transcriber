---
id: 07
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

* [ ] Copy the files into `testdata/talks/fool-with-a-tool/` and `testdata/talks/extreme-learning-eclipsecon/` with short names (`video.mp4`, `deck.pptx`, `deck.pdf`)
* [ ] Gitignore the video and deck files, keep the folders
* [ ] Render each PDF page to `slides/NN.png` (final state of animated slides)
* [ ] Convert each .pptx to `slides.md` with the `pptx-to-markdown` skill (text + speaker notes per slide)
* [ ] Write `talk.json` per talk: title, speaker, event, date, duration, slide count, animated slides (askui: 7 slides with entrance effects)
* [ ] Document in `CLAUDE.md` how to restore the gitignored files on a fresh clone

## Verification

* [ ] Slide PNG counts: 55 and 31, equal to the PPTX slide counts
* [ ] `slides.md` has one section per slide, same numbering as the PNGs
* [ ] `git status` shows ground truth files, not video or decks
* [ ] Animated askui slides show their final state in the PNG
