---
id: 02
status: done
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

* [x] Copy the skill from music-transcriber with a provenance comment (source repo path, commit)
* [x] Add `--write-info-json` to the yt-dlp command; report both paths (video and `.info.json`)
* [x] Keep the URL check, retry and DRM rules unchanged
* [x] Add `out/` to `.gitignore`
* [x] Mention the skill in `CLAUDE.md`

## Verification

* [x] A single-video URL produces `out/youtube/<Title>-[<id>].mp4` (or `.mkv`) and `<Title>-[<id>].info.json`
  **Note:** Verified via a real run of the skill command on `jNQXAC9IVRw`: `Me_at_the_zoo-[jNQXAC9IVRw].mkv` and `.info.json` written; printed path is the `.mkv`.
* [x] The JSON holds `title`, `uploader`, `upload_date`, `webpage_url`, `duration`
  **Note:** Verified via parsing the info.json: all five keys present, plus `description`.
* [x] A playlist URL without a video ID stops with a request for a single video URL
  **Note:** Verified by following step 1 for a `playlist?list=` URL: no video ID, so the skill stops before yt-dlp. Raw yt-dlp with `--no-playlist` would still walk such a playlist, so step 1 is the only guard.
* [x] `git status` does not show files under `out/`
  **Note:** Verified via `git check-ignore` (`.gitignore:1:out/`) and a clean `git status` with files present under `out/youtube/`.
