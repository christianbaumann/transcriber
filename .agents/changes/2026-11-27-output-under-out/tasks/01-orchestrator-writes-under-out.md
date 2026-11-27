---
id: 01
dependencies: []
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

* [ ] SKILL.md paths table: define `NAME`, `RUN = out/<NAME>/` (repo root), `OUT`, `SLICES`, `WORK` as above; replace `mktemp -d` for WORK
* [ ] SKILL.md step 0: the `<name>` rule, the generic-stem list, the re-run question; done when `OUT`, `SLICES` parent and `WORK` exist under `out/<NAME>/`
* [ ] SKILL.md step 3: pass `SLICES` in the slicer brief
* [ ] `slicer-review.md`: add `SLICES` to the input table; step 4 exports with `--output "$SLICES"` instead of the default `<video>-slices/`
* [ ] SKILL.md step 12: the article-path check pattern catches the new slices path (e.g. `slices/` instead of `-slices/`); report names `out/<NAME>/`
* [ ] Update the path wording in `slide-processing.md` and `article-writing.md` input tables
* [ ] README Output section and the CLAUDE.md lines describe the new layout

## Verification

* [ ] `grep -rnE 'next to the video|mktemp -d|<video>-(article|slices)/' .claude/skills/transcribing-talks README.md CLAUDE.md` finds nothing outside `evals/` (task 02 owns those)
* [ ] SKILL.md, `slicer-review.md` and README name the same three folders and the same `<name>` rule
* [ ] Dry check of the rule, written in the task report: `testdata/talks/dragons-agiletd/video.mp4` gives `out/dragons-agiletd/`; `out/youtube/Some_Talk-[abc].mp4` gives `out/some-talk-abc/` (or the kebab-case form SKILL.md defines); `~/Videos/talk.mp4` gives `out/talk/`
* [ ] The slicer brief's export command uses `export.py --output` with the passed path (`export.py` accepts any path; check `.claude/skills/video-slicer/scripts/export.py --help`)
* [ ] All repository tests pass (CLAUDE.md "Commands")
* [ ] Manual, not automatable here: the next full pipeline run writes nothing outside `out/` (run cost: tokens and time). Note it as open in the report if no run happens
