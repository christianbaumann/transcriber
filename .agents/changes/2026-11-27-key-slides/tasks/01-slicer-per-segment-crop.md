---
id: 01
dependencies: []
---

# Task 01: Slice every camera layout of a recording (upstream video-slicer)

A recording that switches between camera layouts (conference picture-in-picture, zoomed room camera, wide room shot) yields slides from every layout, not only from the main one.

## Outcome

- The slicer accepts one crop box per time segment. Each segment is cropped with its own box; candidates and exported slides carry the right crop.
- `SKILL.md` step 1 no longer only warns about several layouts: it finds the segments (time ranges) and step 2 sets one crop box per segment.
- Recordings with one layout behave exactly as before; score mode (one box per page region) keeps working.
- Commit messages describe this behavior, e.g. "Crop each camera layout segment with its own box".

## References

* `design.md#multi-layout-slicing-fixed-upstream`, `design.md#problem` (lost slides per talk)
* Upstream repo `~/git_repos/_own/video-slicer` (own `CLAUDE.md`, branch convention of that repo)
* Touches: `.claude/skills/video-slicer/scripts/detect.py`, `candidates.py`, `export.py` (and `samples.py` if segment finding needs denser samples), `tests/test_detect.py`, `tests/test_candidates.py`, `tests/test_export.py`, `.claude/skills/video-slicer/SKILL.md` (steps 1, 2, 3, 4), `README.md`, `CLAUDE.md`
* Existing region mechanism: `--crop` repeats, segments carry `region` (score mode, `.agents/changes/2026-11-10-score-page-regions/design.md`)
* Test recordings: `/Users/christian.baumann/Downloads/Unlearning AI - Pradeep Soundararajan.mp4` (layouts 0:00-5:18 PiP, 5:18-7:34 zoom, 7:45-end wide), `/Users/christian.baumann/git_repos/_own/transcriber/testdata/talks/dragons-agiletd/video.mp4` (PiP 9:30-10:07)

## Work

* [ ] Extend the crop option so a box can be bound to a time range (e.g. `--crop W:H:X:Y@START-END`); a box without range keeps covering the whole video
* [ ] `detect.py`: run `freezedetect` per box only inside its range; report segment times in video time
* [ ] `candidates.py` / `export.py`: crop each candidate with the box of its segment
* [ ] `SKILL.md`: step 1 identifies layout segments from the samples, refining each boundary with extra samples; step 2 finds one box per segment; the report lists segments with their boxes instead of a lost-slides warning. Keep step 5 (review) unchanged unless needed; note any change for task 02
* [ ] Tests first: time-bound boxes on a synthetic two-layout video (ffmpeg-generated, as existing tests do)
* [ ] Update `README.md` and `CLAUDE.md` (non-obvious facts)

## Verification

* [ ] New tests for time-bound boxes fail before and pass after the change
* [ ] `uv run pytest` passes in the upstream repo (existing single-box and score-mode tests unchanged)
* [ ] Unlearning AI run exports the PiP-section slides, including "The Last Keynote of Agile Testing Days 2025 - Unlearning A.I." and "Chapter 1 : I"
* [ ] Dragons run exports deck slides 3 and 4 (shown 9:30-10:07)
* [ ] A single-layout recording gives the same slices as before (same count and times)
