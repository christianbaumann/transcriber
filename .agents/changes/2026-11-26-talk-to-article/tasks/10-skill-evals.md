---
id: 10
status: done
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

* [x] `evals.json`: one entry per talk (input, expectations); `trigger_evals.json`: prompts that should and should not trigger the skill
  **Note:** Thresholds and required files sit at the top of `evals.json`; `trigger_evals.json` has 6 positive and 8 negative prompts.
* [x] `grade.py <output dir> <ground truth dir>`: slide recall (kept slices matched 1:1 to deck slides, final state; build steps not counted as missed), unspoken content check (slide text not in transcript but in article), required files present, heading depth ≥ 2, writes `grading.json`
  **Note:** CLI is `grade.py <article dir> <ground truth dir> [--slices DIR] [--out FILE]`. Matching uses grey thumbnails and an optimal 1:1 assignment (robust to the webcam inset). Besides build steps, repeats of an earlier deck slide and slides listed as `not_shown` in `talk.json` are not counted as missed. Coverage is inconclusive (not gating) below 5 unspoken lines; footers are detected generically.
* [x] Agree thresholds with the user and record them in the evals README
  **Note:** Agreed with the user: recall >= 0.90, unspoken coverage >= 0.70; plus all required files and heading depth >= 2.
* [x] Unit tests for `grade.py` on fixture output
  **Note:** 20 tests in `scripts/tests/test_grade.py`.
* [x] Run both evals once; record results in `evals/README.md`
  **Note:** EclipseCon: run from the orchestrator task graded. askui: full run (50 slices kept, 8 chapters, all review items ok). Results in `evals/README.md`.

## Verification

* [x] `grade.py` tests pass
  **Note:** Verified via the CLAUDE.md test command: 61 passed.
* [x] Both evals ran; `grading.json` shows recall and coverage per talk
  **Note:** EclipseCon: files pass, recall 1.00 (25/25; build steps 18-20, repeat 22, not shown 30-31), coverage inconclusive (2 lines), depth 2. askui: files pass, recall 1.00 (50/50; repeat 18, not shown 52-55; 0.93 without `not_shown`), coverage 1.00 (6 lines), depth 2. `not_shown` verified from video frames.
* [x] A deliberately broken output (missing slide, missing file) fails the matching check
  **Note:** Verified via unit tests: a deleted slice fails recall, a deleted `article.html` fails required files, flat headings fail depth, missing slide text fails coverage; the CLI exits 1.
* [x] Results and thresholds are documented
  **Note:** `evals/README.md` lists thresholds, a justified constants table and both results.
