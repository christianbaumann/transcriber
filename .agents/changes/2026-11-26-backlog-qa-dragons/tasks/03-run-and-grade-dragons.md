---
id: 03
status: done
dependencies:
- 01
- 02
---

# Task 03: Run and grade "Dragons"

The evals README records how the skill performs on the AgileTD 2025 talk, the Q&A drop is confirmed on a real run, and defects found are in the backlog.

## Intended behavior

- Evals README has a results section for the Dragons talk with the four checks and their evidence
- A real outline shows the Q&A range under `Not in article` and no Q&A chapter
- Run output under `testdata/talks/*/` stays out of git
- Commit message describes the recorded results, e.g. "Record eval results for the AgileTD talk"

## References

* `design.md#scope-add-the-talk-as-eval-reference-do-not-fix-the-skill-here`, `design.md#verifying-the-qa-drop`, `design.md#backlog-and-docs`
* `.claude/skills/transcribing-talks/SKILL.md` (full run), `.claude/skills/transcribing-talks/evals/grade.py`
* Touches: `.claude/skills/transcribing-talks/evals/README.md` ("Results"), `backlog.md` (Dragons line, new findings), `.gitignore`

## Work

* [x] `.gitignore`: add `testdata/talks/*/video-*/` (slices and article folders of eval runs)
* [x] Full skill run on `testdata/talks/dragons-agiletd/video.mp4` per `SKILL.md`, review gate answered as in earlier eval runs
  **Note:** Subagents ran on sonnet, at most 4 at once instead of `MAX_PARALLEL` 6. Whisper auto-detected `de` from the German pre-talk chat, so the transcription was rerun with `--language en`. The review gate had 0 items. The info values were answered with the `talk.json` facts, because the title slide was not sliced and the title and speaker came from the spoken introduction with ASR errors.
* [x] `grade.py testdata/talks/dragons-agiletd/video-article testdata/talks/dragons-agiletd`
* [x] If misses point to slides never on screen, check the video and set `not_shown` in `talk.json` (record before/after recall, as for askui)
  **Note:** Missed slides 1, 3, 4, 29 and 33 were all on screen at some point, so `not_shown` is not set and recall stays 0.85. Reasons per slide are in the evals README.
* [x] Q&A check: if the Dragons transcript has a Q&A, confirm its outline lists it under `Not in article` and `article.md` has no Q&A chapter. Else restore fool-with-a-tool, transcribe and slice it, run only the outline pass, confirm 33:15 to the end is under `Not in article`
* [x] Evals README: results section (run date, setup, table, explanations), same form as the other talks
* [x] `backlog.md`: remove the Dragons line; add each skill defect the run uncovered as one line (no fixes here)
  **Note:** 8 lines: language detection; second slicer layout; embedded-video frame; dropped last slide; title and speaker ASR errors; edit-pass checks; page-widget handling; grader pairing of dark images.

## Verification

* [x] `grading.json` exists; each check reported pass, fail or inconclusive with evidence in the README
  **Note:** Files pass. Recall 0.85 FAIL. Coverage 0.81 pass. Depth 2 pass. A rerun of `grade.py` gave identical metrics.
* [x] Q&A check passed on the chosen talk (outline excerpt quoted in the README or task notes)
  **Note:** The outline has `Not in article: [00:38:06-end] Q&A`. `article.md` has 7 chapters and the last is `## 7. Conclusion`. `transcript.md` keeps the Q&A from `[00:38:06] So, questions?`.
* [x] `git status` shows no run output under `testdata/talks/`
  **Note:** `git status --short --ignored` shows `video-article/` and `video-slices/` as ignored.
* [x] Tests pass: `uv run --with pytest --with pyyaml --with numpy --with pillow --with scipy pytest .claude/skills/transcribing-talks/scripts/tests`
  **Note:** 63 passed.

## Deviations from the design

- The design expected the talk might fail a threshold. It does: slide recall is 0.85 against 0.90. Per the design's scope decision the causes go to the backlog and are not fixed here.
