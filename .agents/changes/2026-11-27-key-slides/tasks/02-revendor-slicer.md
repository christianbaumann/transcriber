---
id: 02
dependencies:
- 01
---

# Task 02: Use the multi-layout slicer in the transcriber

The transcriber's vendored slicer gets the per-segment crop boxes, so talk articles start from a complete slide set, including title slides and early chapter dividers.

## Outcome

- `.claude/skills/video-slicer/` equals upstream at the new commit (except the two test path constants), with the provenance comment naming that commit.
- The slicer brief (`slicer-review.md`) still matches the slicer's step 5 and reports segments instead of lost layouts.
- The multi-layout entry is gone from `backlog.md`.
- Commit message describes the behavior, e.g. "Slice talks with several camera layouts".

## References

* `design.md#multi-layout-slicing-fixed-upstream`, `design.md#two-changes-slicer-first`
* Touches: `.claude/skills/video-slicer/` (all files; provenance comment in `SKILL.md` line 6), `.claude/skills/video-slicer/tests/test_detect.py`, `test_score_pipeline.py` (keep the transcriber path constants), `.claude/skills/transcribing-talks/references/slicer-review.md`, `.claude/skills/transcribing-talks/SKILL.md` (step 3 wording on layout warnings), `backlog.md`, `CLAUDE.md` (Dependencies, Commands)
* Upstream: `~/git_repos/_own/video-slicer` at the commit from task 01

## Work

* [ ] Diff upstream `.claude/skills/video-slicer/` and `tests/` against the vendored copy; copy the changes; re-apply the two path constants
* [ ] Update the provenance comment to the new commit
* [ ] Align `slicer-review.md` with any change to the slicer's step 5 and with the new segment report
* [ ] `transcribing-talks/SKILL.md` step 3: replace "continue with the main layout" with handling of the segment report
* [ ] Remove the multi-layout line from `backlog.md`; update `CLAUDE.md`

## Verification

* [ ] Slicer tests pass: `uv run --with pytest pytest -o pythonpath=.claude/skills/video-slicer/scripts .claude/skills/video-slicer/tests`
* [ ] Step 3 of the skill on Unlearning AI exports the title slide and "Chapter 1 : I"
* [ ] Step 3 on Dragons exports slides 3 and 4; `grade.py` slide recall rises above 0.85
