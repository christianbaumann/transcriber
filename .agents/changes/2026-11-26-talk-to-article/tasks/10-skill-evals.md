---
id: 10
dependencies:
- 07
- 09
---

# Task 10: Skill evals against reference talks

The skill's output quality is measured against the two reference talks, so changes to briefs or scripts can be checked for regressions.

## Outcome

`evals/` defines one eval per reference talk and a `grade.py` that checks a run's output folder against the ground truth: slide recall, unspoken slide content in the article, structure, required files. Commit message direction: "Add evals for transcribing-talks against reference talks".

## References

* `design.md#reference-talks-for-evals`
* `design.md#open-points` (metrics and thresholds)
* Ground truth: `testdata/talks/*/` (task 07)
* Precedent: `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/transcribing-sheet-music/evals/` (`evals.json`, `trigger_evals.json`, `grade.py`, README)
* Touches: `.claude/skills/transcribing-talks/evals/` (new), `scripts/tests/test_grade.py`, `CLAUDE.md` (Commands)

## Work

* [ ] `evals.json`: one entry per talk (input, expectations); `trigger_evals.json`: prompts that should and should not trigger the skill
* [ ] `grade.py <output dir> <ground truth dir>`: slide recall (kept slices matched 1:1 to deck slides, final state; build steps not counted as missed), unspoken content check (slide text not in transcript but in article), required files present, heading depth ≥ 2, writes `grading.json`
* [ ] Agree thresholds with the user and record them in the evals README
* [ ] Unit tests for `grade.py` on fixture output
* [ ] Run both evals once; record results in `evals/README.md`

## Verification

* [ ] `grade.py` tests pass
* [ ] Both evals ran; `grading.json` shows recall and coverage per talk
* [ ] A deliberately broken output (missing slide, missing file) fails the matching check
* [ ] Results and thresholds are documented
