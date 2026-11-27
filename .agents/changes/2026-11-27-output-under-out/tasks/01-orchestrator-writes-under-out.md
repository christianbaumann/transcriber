---
id: 01
dependencies: []
status: done
---

# Task 01: Orchestrator writes every run to `out/<name>/`

A pipeline run, started on a local video or a YouTube URL, writes its article, slices and work files only to `out/<name>/{article,slices,work}/`. It never writes next to the video or to a system temp folder.

## Intended behavior

- `OUT = out/<name>/article/`, `SLICES = out/<name>/slices/`, `WORK = out/<name>/work/` (kept after the run), all absolute
- `<name>`: the video file stem in kebab-case. If the stem is generic (fixed list in SKILL.md, starting with `video`) or `out/<name>/` exists, the parent folder name in kebab-case. If that is taken too, ask the user
- If the chosen `out/<name>/` exists (a re-run): ask the user whether to overwrite it or use `<name>-2`
- The slicer subagent exports to the `SLICES` path that the orchestrator passes. The vendored `video-slicer` stays unchanged
- YouTube downloads stay in `out/youtube/`

Commit subject direction: "Write pipeline output to out/<name>/".

## References

* `design.md#target-layout`
* `design.md#one-folder-per-run`, `#run-name-from-the-stem-then-the-parent-folder`, `#re-run-asks-before-overwriting`, `#work-is-kept-under-the-run-folder`, `#vendored-skills-stay-unchanged`
* Touches:
  * `.claude/skills/transcribing-talks/SKILL.md` (intro line, paths table, step 0, step 3 brief, step 12 checks and report)
  * `.claude/skills/transcribing-talks/references/slicer-review.md` (new input `SLICES`, step 4 export)
  * `.claude/skills/transcribing-talks/references/slide-processing.md`, `references/article-writing.md` (`<video>-slices/`, `<video>-article/` in the input tables)
  * `README.md` (Output section)
  * `CLAUDE.md` (Slicing dependency line, Image editing line)
* Not touched: `.claude/skills/video-slicer/`, `.claude/skills/downloading-youtube-video/`
* Open key-slides tasks 01, 02, 06 (`.agents/changes/2026-11-27-key-slides/tasks/`) also edit SKILL.md: rebase on whichever lands first

## Work

* [x] SKILL.md paths table: define `NAME`, `RUN = out/<NAME>/` (repo root), `OUT`, `SLICES`, `WORK` as above; replace `mktemp -d` for WORK
  **Note:** `NAME`, `RUN = out/<NAME>/`; WORK also holds `tmp/NNNN/` (per-slide scratch, replaces the slide brief's `mktemp -d`)
* [x] SKILL.md step 0: the `<name>` rule, the generic-stem list, the re-run question; done when `OUT`, `SLICES` parent and `WORK` exist under `out/<NAME>/`
  **Note:** generic stems: `video`, `recording`, `export`. **Design deviation:** the parent-folder fallback applies only to generic (or empty) stems, not to taken names; any existing `out/<NAME>/` gets the question overwrite / `<NAME>-2` / other name. Reason: with the design's "generic or taken" fallback, a re-run of `talk.mp4` silently became `out/videos/` and the re-run question never came up
* [x] SKILL.md step 3: pass `SLICES` in the slicer brief
  **Note:** read back in the diff
* [x] `slicer-review.md`: add `SLICES` to the input table; step 4 exports with `--output "$SLICES"` instead of the default `<video>-slices/`
  **Note:** `export.py --help` shows `--output`; `export.py` creates the folder
* [x] SKILL.md step 12: the article-path check pattern catches the new slices path (e.g. `slices/` instead of `-slices/`); report names `out/<NAME>/`
  **Note:** pattern `slices/` does not match `images/` or `diagrams/`
* [x] Update the path wording in `slide-processing.md` and `article-writing.md` input tables
  **Note:** read back in the diff
* [x] README Output section and the CLAUDE.md lines describe the new layout
  **Note:** README says "no run output outside `out/`": the vendored slicer's own temp dir and model/uv caches stay outside

## Verification

* [x] `grep -rnE 'next to the video|mktemp -d|<video>-(article|slices)/' .claude/skills/transcribing-talks README.md CLAUDE.md` finds nothing outside `evals/` (task 02 owns those)
  **Note:** remaining hits are intended: `slicer-review.md` names the slicer's default to say it is not used; CLAUDE.md documents the slicer's default and the yt-dlp `.info.json` location
* [x] SKILL.md, `slicer-review.md` and README name the same three folders and the same `<name>` rule
  **Note:** verifier compared all three; README states the rule in short form
* [x] Dry check of the rule, written in the task report: `testdata/talks/dragons-agiletd/video.mp4` gives `out/dragons-agiletd/`; `out/youtube/Some_Talk-[abc].mp4` gives `out/some-talk-abc/` (or the kebab-case form SKILL.md defines); `~/Videos/talk.mp4` gives `out/talk/`
  **Note:** `out/dragons-agiletd/`, `out/some-talk-abc/`, `out/talk/`; re-run with `out/talk/` present asks overwrite / `talk-2` / other name
* [x] The slicer brief's export command uses `export.py --output` with the passed path (`export.py` accepts any path; check `.claude/skills/video-slicer/scripts/export.py --help`)
  **Note:** `slicer-review.md` step 4 uses `--output "$SLICES"`
* [x] All repository tests pass (CLAUDE.md "Commands")
  **Note:** 66 passed after rebase onto main
* [ ] (manual testing required) Manual, not automatable here: the next full pipeline run writes nothing outside `out/` (run cost: tokens and time). Note it as open in the report if no run happens
