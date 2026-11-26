---
id: 09
status: done
dependencies:
- 01
- 02
- 03
- 04
- 05
- 06
- 08
---

# Task 09: Orchestrator skill end to end

A user can ask Claude Code to turn a local talk video or YouTube URL into a transcript and a finished article, and the skill runs the whole pipeline with two user gates.

## Outcome

`transcribing-talks/SKILL.md` orchestrates: download (if URL), transcribe, slice with transcript-aware review, per-slide subagents in parallel, info area, outline, chapter subagents, edit pass, review page, final article (screenshots of re-created items moved to `reference/`), HTML build. Output lands in `<video>-article/` as in the design. Commit message direction: "Add transcribing-talks skill for talk-to-article conversion".

## References

* `design.md#pipeline`, `design.md#output`, all Key Decisions
* `references/slide-processing.md` (task 04), `references/article-writing.md` (task 08)
* Scripts: `transcribe.py`, `transcript.py` (task 03), `review.py` (task 05), `build_html.py` (task 06)
* Vendored skills: `video-slicer` (task 01), `downloading-youtube-video` (task 02)
* Precedent: `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/transcribing-sheet-music/references/youtube-input.md`
* Touches: `.claude/skills/transcribing-talks/SKILL.md` (new), `references/slicer-review.md` (new), `CLAUDE.md`, `README.md` (new)

## Work

* [x] `SKILL.md` frontmatter: name `transcribing-talks`, description that triggers on talk/lecture/presentation video to article or transcript
  **Note:** Description triggers on talk, lecture or session video to transcript or article.
* [x] Steps with done criteria, absolute paths in all briefs, work dir in a temp dir
  **Note:** Steps 0-12, each with "Done when"; WORK is `mktemp -d`; per-slide and chapter agents capped at `MAX_PARALLEL = 6` (open point in design.md).
* [x] `references/slicer-review.md`: step-5 override (transcript excerpt per candidate; keep demo frames the speaker refers to; else slicer rules)
  **Note:** Also detects a recurring speaker or webcam overlay: crop it out when possible, else report it as `OVERLAY` (`WxH+X+Y` in slice pixels); per-slide agents fill it with background where it covers no slide content.
* [x] Language rule: talk in English or German → same; other → ask the user
* [x] Info area: gather from `info.json`, title slide, introduction, file name; no guessing; confirm on the review page
  **Note:** One `info.json` per run, read by the edit brief (`INFO`) and `review.py` (`--info`); review answers are written back into it and the article.
* [x] Title from transcript/title slide, fallback file or video name
* [x] Final step: drop review screenshots, copy them to `reference/`, build HTML, report paths
  **Note:** `scripts/pipeline.py reference` copies originals of slides with review items to `reference/`. ImageMagick logs are kept per slide and merged in slide order, so parallel agents cannot corrupt the log.
* [x] Write `README.md` (purpose, requirements, usage) and update `CLAUDE.md` (status, commands)

## Verification

* [x] Full run on the EclipseCon video produces every file listed in `design.md#output`
  **Note:** Verified via a full run (95 candidates, 25 slides kept, 8 chapters): `article.md`, `article.html`, `transcript.md`, `whisper.json`, `images/`, `diagrams/`, `reference/`, `imagemagick.log` all present.
* [x] `transcript.md` and `article.md` are different documents (article is restructured prose with chapters)
  **Note:** Verified: transcript has `[HH:MM:SS]` paragraphs and slide markers; article has info area and 8 chapters of prose.
* [x] The review page opens, and answers change the final article (a "fix" comment is applied)
  **Note:** Verified via a submitted "fix" ("Free time" to "Spare time" on the slide 19 diagram) and a filled date gap: `.drawio`, `.svg`, note and article updated; date in the info area. The fix brief now requires updating every sentence naming the changed text.
* [x] The final article has no review screenshots; `reference/` holds them
  **Note:** Verified via grep for `reference/`, `-slices/`, `/Users/` in `article.md` (none) and `reference/0019_00-17-15.png` present.
* [ ] (manual testing required) A run with a YouTube URL downloads first and fills the info area from `info.json`
  **Note:** Partly verified: the download subagent fetched a 198 s talk with its `.info.json`; `info.json` was then built by hand following the SKILL.md source table (title, upload date, URL, duration filled; event and speaker left as gaps, uploader not used as speaker), and the review page shows the gaps highlighted. A full skill run from a URL was not done.
* [x] All script tests pass
  **Note:** Verified via the CLAUDE.md test command: 41 passed.
