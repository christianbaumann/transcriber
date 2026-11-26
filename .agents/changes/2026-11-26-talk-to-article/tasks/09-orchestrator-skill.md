---
id: 09
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

* [ ] `SKILL.md` frontmatter: name `transcribing-talks`, description that triggers on talk/lecture/presentation video to article or transcript
* [ ] Steps with done criteria, absolute paths in all briefs, work dir in a temp dir
* [ ] `references/slicer-review.md`: step-5 override (transcript excerpt per candidate; keep demo frames the speaker refers to; else slicer rules)
* [ ] Language rule: talk in English or German → same; other → ask the user
* [ ] Info area: gather from `info.json`, title slide, introduction, file name; no guessing; confirm on the review page
* [ ] Title from transcript/title slide, fallback file or video name
* [ ] Final step: drop review screenshots, copy them to `reference/`, build HTML, report paths
* [ ] Write `README.md` (purpose, requirements, usage) and update `CLAUDE.md` (status, commands)

## Verification

* [ ] Full run on the EclipseCon video produces every file listed in `design.md#output`
* [ ] `transcript.md` and `article.md` are different documents (article is restructured prose with chapters)
* [ ] The review page opens, and answers change the final article (a "fix" comment is applied)
* [ ] The final article has no review screenshots; `reference/` holds them
* [ ] A run with a YouTube URL downloads first and fills the info area from `info.json`
* [ ] All script tests pass
