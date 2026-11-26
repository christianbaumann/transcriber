# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Design and tasks exist under `.agents/changes/2026-11-26-talk-to-article/`; implementation in progress (task `status` in `tasks/`).

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

## Skills

- `.claude/skills/downloading-youtube-video/`: vendored from music-transcriber (commit named in the provenance comment); only change is `--write-info-json`, so the download yields `out/youtube/<Title>-[<id>].info.json` (`title`, `uploader`, `upload_date`, `webpage_url`, `duration`, `description`) next to the video

## Decisions

User-visible behavior (output layout and formats, article language, info area, review pass, when screenshots are shown) is in [README.md](README.md). Implementation details:

- **video-slicer:** vendored into `.claude/skills/video-slicer/` with a provenance comment naming the source commit; runs as a subagent
- **YouTube download:** vendored copy of music-transcriber's `downloading-youtube-video` skill; runs as a subagent; needs `--write-info-json` added for the info area
- **Transcription:** `mlx_whisper` with model large-v3, word-level timestamps (used to align slides with text)
- **HTML:** built with `pandoc`, KaTeX for formulas; `build_html.py` uses `--embed-resources --math-method=katex`, which fetches KaTeX (JS, CSS, fonts) from pandoc's default CDN at build time and inlines it (~1.7 MB), so the build needs network but the output renders offline
- **Diagrams:** `.drawio` kept next to its exported SVG; decide per diagram whether another format (e.g. Mermaid) works better
- **Formulas:** LaTeX (`$…$`/`$$…$$`) and a rendered image
- **Slide reading:** Claude reads each slide image; `tesseract` OCR as cross-check for small text
- **Per-slide brief:** `.claude/skills/transcribing-talks/references/slide-processing.md`; the orchestrator passes `SLIDE`, `EXCERPT`, `OUT` (article folder), `NOTES` as absolute paths; one subagent per slide writes `$NOTES/NNNN.md`
- **Image editing:** article uses the edited images; originals stay in `<video>-slices/`; every ImageMagick command is logged
- **Review pass:** after approval, the original screenshots of re-created items stay in a reference folder
- **Info area / title:** fallback order for the title is title slide or speaker's introduction, then file or video name

## Commands

- Slicer tests (needs `ffmpeg`, `ffprobe`; ~30 s), from the repo root:
  ```bash
  uv run --with pytest pytest -o pythonpath=.claude/skills/video-slicer/scripts .claude/skills/video-slicer/tests
  ```
  The tests live under the vendored skill (not a root `tests/`) so they do not clash with later skill tests; the `-o pythonpath` replaces the source repo's `pyproject.toml` setting. Two path constants in `test_detect.py` and `test_score_pipeline.py` differ from upstream for that layout.
- HTML build (needs `pandoc` and network for KaTeX, also for its tests; tests skip without pandoc), from the repo root:
  ```bash
  .claude/skills/transcribing-talks/scripts/build_html.py article.md --out article.html
  uv run --with pytest pytest .claude/skills/transcribing-talks/scripts/tests/test_build_html.py
  ```

Scripts live in `.claude/skills/transcribing-talks/scripts/` (PEP 723, run with `uv`):

```bash
# tests (no model needed)
uv run --with pytest pytest .claude/skills/transcribing-talks/scripts/tests
# transcription: writes <dir>/whisper.json, prints language
.claude/skills/transcribing-talks/scripts/transcribe.py <video> --out <dir> [--language de] [--initial-prompt '<terms>']
# transcript with slide markers / excerpt of a range
.claude/skills/transcribing-talks/scripts/transcript.py <dir>/whisper.json --slices <video>-slices --out <dir>/transcript.md
.claude/skills/transcribing-talks/scripts/transcript.py <dir>/whisper.json --excerpt 00:12:00-00:13:30
```

- `transcribe.py` uses `mlx_whisper` from PATH, else `uvx --from mlx-whisper`; model `mlx-community/whisper-large-v3-mlx`
- `mlx_whisper` exits 0 when the model download fails (e.g. `~/.cache/huggingface/hub` symlink to an unmounted drive); set `HF_HUB_CACHE` to override
- `transcribe.py` passes `--condition-on-previous-text False`: with it on, whisper repeated sentences in loops on a 22 min talk; `--initial-prompt` keeps names and terms consistent
- Excerpt range is `[start, end)` on word start times

## Reference talks

- `testdata/talks/<name>/` for `fool-with-a-tool` (askui, 55 slides) and `extreme-learning-eclipsecon` (31 slides); design: `.agents/changes/2026-11-26-talk-to-article/design.md#reference-talks-for-evals`
- Gitignored: `video.mp4`, `deck.pptx`, `deck.pdf`. Restore on a fresh clone with `scripts/restore-testdata.sh [source-dir]` (copies from `~/Downloads` by original file name)
- Committed ground truth: `slides/NN.png` (100 dpi, 1000x563, PNG8, from the PDF, final state of animated slides), `slides.md` (pptx-to-markdown text and speaker notes, `# Slide N` per slide; image links and alt text dropped, the PNGs carry the images), `talk.json` (title, speaker, event, date, duration, slide count, animated slides). Date is month precision for askui and year only for EclipseCon (not in the decks)
- `slides.md` keeps the social-handle footer of each slide (e.g. `@chrissbaumann #EclipseCon`); unspoken-content checks must ignore it

## Conventions

- Trunk is `main` (no `development` branch in this repo)
