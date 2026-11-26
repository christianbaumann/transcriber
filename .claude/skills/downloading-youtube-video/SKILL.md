---
name: downloading-youtube-video
description: Downloads a YouTube video as a local file at the highest resolution, together with its metadata JSON, given its URL.
---

<!-- Vendored from /Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/downloading-youtube-video (commit 49a08b1). Local change: --write-info-json. -->

STARTER_CHARACTER = 📥

Use only for videos the user may download. Requirements on the machine: `uv`, `ffmpeg`, `deno`.

## 1. Check the URL

The URL must contain a video ID (`watch?v=<id>`, `youtu.be/<id>`, `/shorts/<id>`). A playlist, channel or search URL without one: stop and ask for a single video URL.

Done when the URL names exactly one video.

## 2. Download

Run from the repo root, with the URL in single quotes:

```bash
uvx 'yt-dlp[default]@latest' --no-playlist -S res --merge-output-format mp4/mkv \
  --restrict-filenames --write-info-json -P out/youtube --print after_move:filepath '<url>'
```

Add `--cookies-from-browser <browser>` only when the user asks for it for this download.

The printed path is the video. The metadata is written next to it as `<Title>-[<id>].info.json` (`title`, `uploader`, `upload_date`, `webpage_url`, `duration`, `description`).

Done when yt-dlp exits 0 and the printed path and its `.info.json` exist.

## 3. Handle failure

- Network error on the first run: run the command once more.
- Any other error, or a second network error: stop and show the yt-dlp message.
- DRM-protected video: stop, no workaround.

Done when step 2's criterion holds after at most one retry, or the run has stopped with the yt-dlp message shown to the user.

## 4. Report

Tell the user both paths: the video (`out/youtube/<Title>-[<id>].mp4` or `.mkv`) and the metadata (`out/youtube/<Title>-[<id>].info.json`).

Done when the reply names both paths and both files exist.
