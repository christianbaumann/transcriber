# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Repository is empty (no commits, no code yet). Update this file once structure, commands and tests exist.

## Purpose

Build a Claude Code skill that turns a video recording of a talk, lecture or conference session into an article / textbook-style document:

- Input: a local video file path or a YouTube URL
- **Transcript** of the spoken word, timestamped; a deliverable of its own and the basis for choosing which slides/screenshots to use
- **Slides/screenshots** exported, then edited with ImageMagick (`magick`), the agent choosing per image what to fix after looking at it (lighting, colors, contrast, etc.)
- **Slide content** transcribed and used as a source: information on a slide that the speaker does not say goes into the article
- **Non-text slide content** re-created instead of embedded as a screenshot: diagrams redrawn, source code as code blocks, math formulas as formulas, etc.
- **Article**: transcript and slide content rewritten as readable prose (not a verbatim dump), properly structured (chapters, subchapters, lists, quotes, etc.), images placed at the matching position

## Dependencies on sibling projects

- **Slicing:** https://github.com/christianbaumann/video-slicer (skill `video-slicer`). Turns a talk recording into one cropped PNG per slide, output `<video>-slices/NNNN_HH-MM-SS.png`; the timestamp is when the slide appears, which is what aligns images with the transcript. Needs `ffmpeg`, `ffprobe`, `python3` >= 3.10. Slides shown under 2 s get no candidate.
- **YouTube download:** same approach as `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/downloading-youtube-video/SKILL.md`. Core command (from repo root, URL single-quoted; needs `uv`, `ffmpeg`, `deno`):
  ```bash
  uvx 'yt-dlp[default]@latest' --no-playlist -S res --merge-output-format mp4/mkv \
    --restrict-filenames -P out/youtube --print after_move:filepath '<url>'
  ```
  URL must name exactly one video; retry once on network error; stop on DRM.
- Precedent in music-transcriber: both skills are vendored into `.claude/skills/` (video-slicer with a provenance comment naming the source commit) and run as one subagent each, the orchestrator briefing them with absolute paths (`music-transcriber/.claude/skills/transcribing-sheet-music/references/youtube-input.md`). The slicer's default review rules (drop demo frames, repeats, earlier build steps) fit talks, so unlike music-transcriber no rule override is needed.

## Packaging as a skill

- A skill is a directory with a `SKILL.md` (YAML frontmatter: `name`, `description`; body: instructions) plus optional `scripts/` and `references/`
- Deterministic, mechanical steps (audio extraction, transcription) belong in scripts; judgment steps (chapter boundaries, prose rewriting, choosing which images matter) stay in `SKILL.md` instructions for the model

## Decisions

- **video-slicer:** vendored into `.claude/skills/video-slicer/` with a provenance comment naming the source commit; runs as a subagent
- **YouTube download:** vendored copy of music-transcriber's `downloading-youtube-video` skill; runs as a subagent
- **Transcription:** `mlx_whisper` with model large-v3, word-level timestamps (used to align slides with text)
- **Output format:** Markdown (`<slug>.md` + `images/`), plus a self-contained HTML page with images embedded (via `pandoc`)
- **Article language:** English or German, the talk's language if it is one of the two (the user can override); for a talk in any other language, ask the user which of the two
- **Output location:** `<video>-article/` next to the video; for a YouTube URL next to the downloaded file under `out/youtube/`
- **Transcript vs. article:** two separate deliverables. Transcript = spoken word in Markdown, `[HH:MM:SS]` per paragraph, slide markers (`→ slide 0007`), plus the raw whisper JSON. Article = the rewritten, structured document
- **Diagrams:** draw.io by default (`.drawio` kept next to its exported SVG); decide per diagram whether another format (e.g. Mermaid) works better
- **Formulas, code, tables:** formulas as LaTeX (`$…$`/`$$…$$`, KaTeX in HTML) and as rendered image; code as fenced blocks with language; tables as Markdown tables. Two passes: a review version shows the original slide screenshot next to each re-created item (formula, code, diagram, table) for the user to verify; after approval, the final article drops those screenshots and they stay in a reference folder
- **Slide reading:** Claude reads each slide image; `tesseract` OCR as cross-check for small text
- **Image editing:** article uses the edited images; originals stay in `<video>-slices/`; every ImageMagick command is logged so edits are reproducible
- **Screenshots in the article:** only where they add what a redrawn/text version cannot (photos, tool screenshots, complex visuals); fully re-created slides are not shown as images
- **Info area** at the start of the article: details about the session (title, event, date, source/URL, duration) and the original speaker/author. Filled from all available sources: YouTube metadata (yt-dlp `--write-info-json`, which the vendored download skill does not do yet), title slide, speaker's introduction in the transcript, file name; no guessing. The agent then shows the gathered values and asks the user to confirm them and fill in the gaps
- **Title** of the talk/lecture: taken from the transcript (speaker's introduction, title slide), falling back to the file or video name

## Tools available on the dev machine

Verified present (macOS, Apple Silicon): `ffmpeg`, `ffprobe`, `whisper` (openai-whisper), `mlx_whisper`, `yt-dlp`, `python3`, `uv`, `deno`, `pandoc`, `tesseract`, `magick` (ImageMagick 7), `mmdc` (Mermaid CLI), `drawio` (CLI + app).

## Conventions

- Trunk is `main` (no `development` branch in this repo)
