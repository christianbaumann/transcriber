# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Documentation

- [README.md](README.md) is for humans: purpose, status, what the skill does, output, requirements. Read it first; this file does not repeat it
- CLAUDE.md holds only what an agent needs on top: implementation details, conventions, internal paths
- Information relevant to humans goes into README.md and is referenced from here, never duplicated
- Update both files with every commit as necessary

## Status

Design and tasks exist under `.agents/changes/2026-11-26-talk-to-article/`; no code yet. Update this file once structure, commands and tests exist.

## Dependencies on sibling projects

- **Slicing:** https://github.com/christianbaumann/video-slicer (skill `video-slicer`). Output `<video>-slices/NNNN_HH-MM-SS.png`; the timestamp is when the slide appears, which is what aligns images with the transcript.
- **YouTube download:** same approach as `/Users/christian.baumann/git_repos/_own/music-transcriber/.claude/skills/downloading-youtube-video/SKILL.md`. Core command (from repo root, URL single-quoted):
  ```bash
  uvx 'yt-dlp[default]@latest' --no-playlist -S res --merge-output-format mp4/mkv \
    --restrict-filenames -P out/youtube --print after_move:filepath '<url>'
  ```
  URL must name exactly one video; retry once on network error; stop on DRM.
- Precedent in music-transcriber: both skills are vendored into `.claude/skills/` (video-slicer with a provenance comment naming the source commit) and run as one subagent each, the orchestrator briefing them with absolute paths (`music-transcriber/.claude/skills/transcribing-sheet-music/references/youtube-input.md`). Like music-transcriber, the slicer brief overrides the slicer's step 5 (review): each candidate gets the transcript excerpt of its time range, demo frames (IDE, terminal, browser) are kept when the speaker refers to them, otherwise the slicer's own rules apply (drop repeats, earlier build steps). The override must track changes to the slicer's step 5.

## Packaging as a skill

- A skill is a directory with a `SKILL.md` (YAML frontmatter: `name`, `description`; body: instructions) plus optional `scripts/` and `references/`
- Deterministic, mechanical steps (audio extraction, transcription) belong in scripts; judgment steps (chapter boundaries, prose rewriting, choosing which images matter) stay in `SKILL.md` instructions for the model

## Decisions

User-visible behavior (output layout and formats, article language, info area, review pass, when screenshots are shown) is in [README.md](README.md). Implementation details:

- **video-slicer:** vendored into `.claude/skills/video-slicer/` with a provenance comment naming the source commit; runs as a subagent
- **YouTube download:** vendored copy of music-transcriber's `downloading-youtube-video` skill; runs as a subagent; needs `--write-info-json` added for the info area
- **Transcription:** `mlx_whisper` with model large-v3, word-level timestamps (used to align slides with text)
- **HTML:** built with `pandoc`, KaTeX for formulas
- **Diagrams:** `.drawio` kept next to its exported SVG; decide per diagram whether another format (e.g. Mermaid) works better
- **Formulas:** LaTeX (`$…$`/`$$…$$`) and a rendered image
- **Slide reading:** Claude reads each slide image; `tesseract` OCR as cross-check for small text
- **Image editing:** article uses the edited images; originals stay in `<video>-slices/`; every ImageMagick command is logged
- **Review pass:** after approval, the original screenshots of re-created items stay in a reference folder
- **Info area / title:** fallback order for the title is title slide or speaker's introduction, then file or video name

## Conventions

- Trunk is `main` (no `development` branch in this repo)
