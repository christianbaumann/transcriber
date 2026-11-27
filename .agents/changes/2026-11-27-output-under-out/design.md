---
datetime: 2026-11-27T14:05:00+01:00
author: Christian Baumann
tags: [transcribing-talks, output-layout, evals]
---

# All run output under `out/`

## Problem

A run of `transcribing-talks` writes outside the repository's `out/` folder:

```
today                                            after this change
-----------------------------------------------  ------------------------------
YouTube  out/youtube/<T>-[id].mp4 + .info.json   unchanged
OUT      <video>-article/   next to the video    out/<name>/article/
SLICES   <video>-slices/    next to the video    out/<name>/slices/
WORK     mktemp -d (/var/folders/...)            out/<name>/work/
```

- A local video `~/Videos/talk.mp4` writes into `~/Videos/`
- The reference talks write into `testdata/talks/<talk>/video-{article,slices}/` (hidden by the gitignore rule `testdata/talks/*/video-*/`)
- All three reference videos are named `video.mp4`, so a flat `out/video-article/` would collide

`out/` is gitignored already.

## Target layout

```
out/
  youtube/                     downloads (unchanged)
    <Title>-[<id>].mp4
    <Title>-[<id>].info.json
  <name>/                      one folder per run
    article/                   was <video>-article/  (OUT)
    slices/                    was <video>-slices/   (SLICES)
    work/                      was mktemp            (WORK)
```

Choosing `<name>`:

```
video stem, kebab-case ──► generic ("video") or out/<name>/ taken?
                              │ no                 │ yes
                              ▼                    ▼
                           <name>        parent folder name, kebab-case
                                                   │ taken too?
                                                   ▼ yes
                                         ask the user
```

`out/<name>/` exists after this (a re-run): ask the user whether to overwrite or to use `<name>-2`.

## Key Decisions

### One folder per run

- **Decision:** `out/<name>/{article,slices,work}/`. YouTube downloads stay in `out/youtube/`.
- **Reason:** all files of one run stay together, and you remove a run by deleting one folder. No output leaves the repository.
- **Trade-offs:** paths in docs and `grade.py` change. Rejected: flat `out/<video>-article/` + `out/<video>-slices/` (same-named videos collide, WORK stays outside `out/`), and mirroring the source path (`out/testdata/talks/...`: long paths, and no clean mapping for videos outside the repo).

### Run name from the stem, then the parent folder

- **Decision:** `<name>` is the video file stem in kebab-case. If the stem is generic (`video`) or `out/<name>/` exists, use the parent folder name. If that is taken too, ask the user.
- **Reason:** readable names, and the reference talks get `out/dragons-agiletd/` etc. without extra input.
- **Trade-offs:** "generic" needs a short fixed list in SKILL.md (start with `video`). Rejected: stem only, which asks on every reference talk; stem plus timestamp, which is hard to read.

### Re-run asks before overwriting

- **Decision:** if `out/<name>/` exists, ask the user: overwrite or `<name>-2`.
- **Reason:** the folder holds review answers and edited images that are expensive to produce. Silent overwrite loses them, and silent new names pile up.
- **Trade-offs:** one more user prompt on re-runs. Rejected: always a new name, always overwrite.

### WORK is kept under the run folder

- **Decision:** `WORK = out/<name>/work/`, kept after the run.
- **Reason:** slide notes, outline and review answers help with debugging and evals. `out/` is gitignored, so this costs nothing in git.
- **Trade-offs:** disk use grows per run. Rejected: delete after success (loses debug data), keep mktemp (violates "everything under `out/`").

### Vendored skills stay unchanged

- **Decision:** the orchestrator passes the slicer's output path (`export.py --output "$SLICES"`) in its brief. `.claude/skills/video-slicer/` and `.claude/skills/downloading-youtube-video/` are not edited.
- **Reason:** the provenance comments stay true, and future re-vendoring stays a plain copy.
- **Trade-offs:** the slicer run on its own (without the orchestrator) still writes `<video>-slices/` next to the video. Rejected: patching the vendored default, and changing upstream first.

### Move the existing Dragons run, drop the testdata gitignore rule

- **Decision:** move `testdata/talks/dragons-agiletd/video-{article,slices}/` to `out/dragons-agiletd/{article,slices}/`. Remove `testdata/talks/*/video-*/` from `.gitignore`.
- **Reason:** keeps the existing graded run, and the rule no longer has a purpose.
- **Trade-offs:** this run has no `work/` folder (its WORK was in mktemp). Rejected: leaving it (two layouts at once), deleting it (needs a full re-run to grade again).

### Update every file that names the old paths

- **Decision:** update the non-vendored files below, and add a test for the new `grade.py --slices` default.
- **Reason:** a stale path in a brief or doc sends a subagent or a reader to the wrong place.
- **Trade-offs:** no `paths.py` helper: the orchestrator (the model) sets the paths in SKILL.md, and no script computes `<name>`. Add a helper only if a script needs it later.

## Affected files

| File | Change |
|---|---|
| `.claude/skills/transcribing-talks/SKILL.md` | Paths table (`OUT`, `SLICES`, `WORK`), `<name>` rule, re-run question, step 0 done criteria, slicer brief passes `--output`, final report |
| `.claude/skills/transcribing-talks/references/slicer-review.md`, `slide-processing.md`, `article-writing.md` | Path mentions such as `<video>-slices/` |
| `.claude/skills/transcribing-talks/evals/grade.py` | `--slices` default: `<article dir>/../slices` instead of the `-article` to `-slices` rename; docstring |
| `.claude/skills/transcribing-talks/scripts/tests/test_grade.py` | Test for the new default |
| `.claude/skills/transcribing-talks/evals/README.md`, `evals.json` | `expected_output` and run instructions: `out/<name>/article/` |
| `.claude/skills/transcribing-talks/scripts/review.py`, `scripts/tests/test_build_html.py` | Check their path mentions; change only if they name the old layout |
| `README.md` | Output section |
| `CLAUDE.md` | Path notes (evals, reference talks gitignore line) |
| `.gitignore` | Remove `testdata/talks/*/video-*/` |

The vendored `video-slicer` and `downloading-youtube-video` skills also name `<video>-slices/` and `out/youtube/`. They stay as they are (see above).

## Related documents

- [Talk-to-article design](../2026-11-26-talk-to-article/design.md): original output layout
- [Key slides design](../2026-11-27-key-slides/design.md): open tasks 01, 02, 06 touch SKILL.md as well
- [Evals README](../../../.claude/skills/transcribing-talks/evals/README.md)
