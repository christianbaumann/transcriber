---
id: 01
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

* [ ] Copy `.claude/skills/video-slicer/` (SKILL.md, `scripts/`, tests) from the source repo at commit `9887d2e`
* [ ] Add the provenance comment below the frontmatter of `SKILL.md`: source URL, commit, how to update
* [ ] Make the slicer tests runnable from this repo root (separate `uv run --with pytest pytest <path>` command; no shared `conftest.py` clash with later skill tests)
* [ ] Add the test command to `CLAUDE.md`

## Verification

* [ ] `SKILL.md` names the source commit `9887d2e`
* [ ] `diff -r` against the source repo at that commit shows only the provenance comment
* [ ] Slicer tests pass from the repo root
* [ ] The skill runs on the EclipseCon video (`~/Downloads/2020 EclipseCon.mp4`) and writes `<video>-slices/NNNN_HH-MM-SS.png`
