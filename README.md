# transcriber

A Claude Code skill (`transcribing-talks`) that turns a video recording of a talk, lecture or conference session into a transcript and a readable, textbook-style article.

## Status

Usable. Ask Claude Code to turn a talk video or a YouTube URL into an article; the skill `transcribing-talks` (`.claude/skills/transcribing-talks/SKILL.md`) runs the pipeline. Verified on a 22 min talk with 25 slides.

- [Design](.agents/changes/2026-11-26-talk-to-article/design.md): pipeline, output layout, decisions
- [Tasks](.agents/changes/2026-11-26-talk-to-article/tasks/): implementation slices and their dependencies

## Usage

Say, for example: "Turn `~/Videos/talk.mp4` into an article" or "Write an article from this talk: `<YouTube URL>`". The skill works in subagents (at most 6 at once), so a talk with 50 slides takes a while and many tokens. It asks you when:

- the talk is in a language other than English or German (which article language?)
- the review page is ready (info area and re-created items, see above)

## What it does

Input is a local video file or a YouTube URL. The skill:

1. Downloads the video (YouTube only), including its metadata
2. Transcribes the spoken word locally with timestamps
3. Extracts one image per slide
4. Reads every slide: fixes the screenshot (lighting, colors, contrast), re-creates diagrams, code, formulas and tables, and notes what is on the slide but not said in the talk
5. Writes the article: rewritten prose with chapters, lists and quotes, slide content merged in, images at the matching position; decorative photos the speaker never refers to are left out; the article ends with a short conclusion (the talk's own closing chapter, else a summary of the chapters with no new facts), after any Q&A

You are asked twice along the way:

- **Info area**: the article starts with details about the session (title, event, date, source, duration, speaker). The skill gathers them from the video metadata, title slide, the speaker's introduction and the file name, without guessing. You confirm the values and fill the gaps.
- **Review**: a local web page shows each re-created item (diagram, code, formula, table) next to the original slide. You approve or request fixes. The final article then drops the original screenshots.

## Output

A folder `<video>-article/` next to the video; for a YouTube URL next to the download under `out/youtube/`. It holds:

- `transcript.md`: the spoken word, a `[HH:MM:SS]` timestamp per paragraph, markers where a slide appears; plus the raw `whisper.json`
- `article.md` and `article.html` (a single self-contained file, images embedded)
- the edited images, re-created diagrams with their draw.io sources, the original screenshots for reference, and a log of every image edit

Diagrams are redrawn with draw.io by default (Mermaid where it fits better). Code becomes code blocks, formulas LaTeX, tables Markdown tables. Speaker webcam insets are removed from screenshots where they cover no slide content. Screenshots appear only where a re-created version cannot replace them, such as photos or tool screenshots; decorative photos the speaker does not refer to are left out.

The article is written in English or German: the talk's language if it is one of the two, otherwise you choose. You can override it.

## Requirements

- macOS on Apple Silicon (transcription uses `mlx_whisper`)
- Claude Code
- `ffmpeg`, `ffprobe`, `python3` >= 3.10, `uv`, `deno`, `pandoc`, `tesseract`, ImageMagick 7 (`magick`), draw.io (app with CLI), Mermaid CLI (`mmdc`)

## Built on

- [video-slicer](https://github.com/christianbaumann/video-slicer): extracts one cropped image per slide from a talk recording. Slides shown for less than 2 seconds are not extracted.
- The `downloading-youtube-video` skill from the music-transcriber project, based on [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper) with the Whisper large-v3 model

Both skills are copied into this repository, so the versions change only on purpose.
