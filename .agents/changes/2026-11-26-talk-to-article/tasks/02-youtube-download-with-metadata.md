---
id: 02
dependencies: []
---

# Task 02: YouTube download with metadata

A YouTube URL becomes a local video file plus its metadata JSON, which later fills the article's info area.

## Outcome

Given one YouTube video URL, the skill downloads the highest-resolution file and its `info.json` (title, channel, upload date, description, URL) into `out/youtube/`. Commit message direction: "Add YouTube download skill that keeps video metadata".

## References

* `design.md#vendor-video-slicer-and-the-download-skill`
* `design.md#info-area-at-the-start-of-the-article`
* Source: `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/downloading-youtube-video/SKILL.md`
* Touches: `.claude/skills/downloading-youtube-video/SKILL.md` (new), `.gitignore` (`out/`), `CLAUDE.md` (Skills)

## Work

* [ ] Copy the skill from music-transcriber with a provenance comment (source repo path, commit)
* [ ] Add `--write-info-json` to the yt-dlp command; report both paths (video and `.info.json`)
* [ ] Keep the URL check, retry and DRM rules unchanged
* [ ] Add `out/` to `.gitignore`
* [ ] Mention the skill in `CLAUDE.md`

## Verification

* [ ] A single-video URL produces `out/youtube/<Title>-[<id>].mp4` (or `.mkv`) and `<Title>-[<id>].info.json`
* [ ] The JSON holds `title`, `uploader`, `upload_date`, `webpage_url`, `duration`
* [ ] A playlist URL without a video ID stops with a request for a single video URL
* [ ] `git status` does not show files under `out/`
