---
id: 03
dependencies: []
status: done
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

* [x] `mkdir -p out/dragons-agiletd` and move both folders; look at the targets first, stop if they exist
  **Note:** `out/` did not exist before; `video-article/` (34 files) and `video-slices/` (28 files) moved
* [x] Check for other `testdata/talks/*/video-*/` folders (`ls -d testdata/talks/*/video-*/`); move any the same way to `out/<talk>/`
* [x] Remove the rule from `.gitignore`

## Verification

* [x] `ls -d testdata/talks/*/video-*/` finds nothing; `out/dragons-agiletd/article/article.md` and `out/dragons-agiletd/slices/*.png` exist, file counts equal those before the move
  **Note:** glob has no matches; counts 34 and 28 before and after
* [x] `git status --porcelain` shows only `.gitignore` changed
  **Note:** worktree diff is the one removed line; main checkout testdata shows no untracked entries
* [x] `uv run .claude/skills/transcribing-talks/evals/grade.py out/dragons-agiletd/article testdata/talks/dragons-agiletd --slices out/dragons-agiletd/slices --out <scratch>/grading.json` gives the same PASS/FAIL lines as `out/dragons-agiletd/article/grading.json` (explicit `--slices`, so this task does not depend on task 02)
  **Note:** same 4 results as the stored `grading.json`: required files, coverage, heading depth PASS; slide recall FAIL 0.85 (28/33, missed 1, 3, 4, 29, 33), as before the move
