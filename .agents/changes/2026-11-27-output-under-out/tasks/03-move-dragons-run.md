---
id: 03
dependencies: []
---

# Task 03: Move the Dragons run to `out/dragons-agiletd/`

The existing graded Dragons run lives at `out/dragons-agiletd/{article,slices}/`, the testdata folder holds only committed ground truth and restored inputs, and the gitignore rule for run output in testdata is gone.

## Intended behavior

- `testdata/talks/dragons-agiletd/video-article/` becomes `out/dragons-agiletd/article/`, `video-slices/` becomes `out/dragons-agiletd/slices/`, content unchanged
- `.gitignore` no longer lists `testdata/talks/*/video-*/`; `git status` stays clean (nothing under testdata is untracked)
- The moved run has no `work/` folder (its WORK was a temp folder): stated, not recreated

Commit subject direction: "Stop ignoring run output under testdata" (the move itself is outside git).

## References

* `design.md#move-the-existing-dragons-run-drop-the-testdata-gitignore-rule`
* Touches:
  * `.gitignore`
  * `testdata/talks/dragons-agiletd/video-article/`, `video-slices/` (gitignored, moved with `mv`)
  * `out/dragons-agiletd/` (new, gitignored)

## Work

* [ ] `mkdir -p out/dragons-agiletd` and move both folders; look at the targets first, stop if they exist
* [ ] Check for other `testdata/talks/*/video-*/` folders (`ls -d testdata/talks/*/video-*/`); move any the same way to `out/<talk>/`
* [ ] Remove the rule from `.gitignore`

## Verification

* [ ] `ls -d testdata/talks/*/video-*/` finds nothing; `out/dragons-agiletd/article/article.md` and `out/dragons-agiletd/slices/*.png` exist, file counts equal those before the move
* [ ] `git status --porcelain` shows only `.gitignore` changed
* [ ] `uv run .claude/skills/transcribing-talks/evals/grade.py out/dragons-agiletd/article testdata/talks/dragons-agiletd --slices out/dragons-agiletd/slices --out <scratch>/grading.json` gives the same PASS/FAIL lines as `out/dragons-agiletd/article/grading.json` (explicit `--slices`, so this task does not depend on task 02)
