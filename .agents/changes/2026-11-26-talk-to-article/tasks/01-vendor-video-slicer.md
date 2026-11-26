---
id: 01
status: done
dependencies: []
---

# Task 01: Vendor video-slicer

The repo contains a pinned copy of video-slicer, so slide extraction works in this repo without a separate install.

## Outcome

`video-slicer` is available as a project skill at a known source commit, and its own tests pass in this repo. Commit message direction: "Vendor video-slicer skill at commit 9887d2e".

## References

* `design.md#vendor-video-slicer-and-the-download-skill`
* https://github.com/christianbaumann/video-slicer (`.claude/skills/video-slicer/`, `tests/`, `pyproject.toml`)
* Precedent: `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/video-slicer/SKILL.md` (provenance comment)
* Touches: `.claude/skills/video-slicer/` (new), `CLAUDE.md` (Commands)

## Work

* [x] Copy `.claude/skills/video-slicer/` (SKILL.md, `scripts/`, tests) from the source repo at commit `9887d2e`
* [x] Add the provenance comment below the frontmatter of `SKILL.md`: source URL, commit, how to update
* [x] Make the slicer tests runnable from this repo root (separate `uv run --with pytest pytest <path>` command; no shared `conftest.py` clash with later skill tests)
  **Note:** Tests live in `.claude/skills/video-slicer/tests/`; `-o pythonpath=...` replaces the source repo's `pyproject.toml` setting.
* [x] Add the test command to `CLAUDE.md`

## Verification

* [x] `SKILL.md` names the source commit `9887d2e`
  **Note:** Verified via the provenance comment on line 6 of `SKILL.md`.
* [x] `diff -r` against the source repo at that commit shows only the provenance comment
  **Note:** Verified via `diff -r` against a clone at 9887d2e: skill dir differs only by the comment; `tests/` additionally differs in two path constants (`DETECT`, `SCRIPTS`) because the tests moved under the skill dir.
* [x] Slicer tests pass from the repo root
  **Note:** Verified via the CLAUDE.md test command from the repo root: 50 passed.
* [x] The skill runs on the EclipseCon video (`~/Downloads/2020 EclipseCon.mp4`) and writes `<video>-slices/NNNN_HH-MM-SS.png`
  **Note:** Verified via a run on a symlinked copy of the video in a temp dir: 95 files `0001_00-00-00.png` to `0095_00-22-12.png`, 1920x1050. Step 5 review was skipped (the transcript-aware review override comes with the orchestrator skill).
