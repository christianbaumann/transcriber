# Evals

## Quality evals (`evals.json`)

One entry per reference talk (`testdata/talks/<name>/`, see CLAUDE.md "Reference talks"). Entry fields: `prompt`, `expected_output`, `files` (relative to the skill root), `ground_truth` (repo-relative), `expectations` (must equal `grade.expectation_texts(config)`; a test checks this). The video and deck files are gitignored: restore them with `scripts/restore-testdata.sh`.

Thresholds and required files are named values at the top of `evals.json`, nowhere else.

## Grade a run

```
uv run .claude/skills/transcribing-talks/evals/grade.py <article dir> <ground truth dir> [--slices DIR] [--out grading.json]
```

- `<article dir>`: the run's `<video>-article/`; `--slices` defaults to `<video>-slices/` next to it
- Writes `grading.json` (`expectations` with `text`, `passed`, `evidence`; `metrics`; `summary`) to `--out` (default: `./grading.json`); exit code 1 if a check fails
- Tests: `uv run --with pytest --with numpy --with pillow --with scipy pytest .claude/skills/transcribing-talks/scripts/tests/test_grade.py`

## Checks and thresholds (agreed with the user)

| Check | Threshold |
|---|---|
| Required files present | `article.md`, `article.html`, `transcript.md`, `whisper.json`, `imagemagick.log` |
| Slide recall | >= 0.90 |
| Unspoken-content coverage | >= 0.70 |
| Heading depth | >= 2 (a `###` below a `##` chapter, the `#` title not counted) |

- **Slide recall:** kept slices (`<video>-slices/`) are matched 1:1 to the deck PNGs by pixel agreement of 96x54 grayscale thumbnails (an optimal assignment, so the speaker inset and scaling cost a few percent, not the match). A pair needs >= 0.65 agreement. Deck slides whose text is a proper subset of the next slide's are build steps: they are neither matched nor counted as missed. Recall = matched / counted deck slides.
- **Unspoken-content coverage:** for matched slides only, slide text lines (from `slides.md`, without notes, headings and social-handle footers) with at least 2 words of 3+ letters. A line is unspoken if less than 80% of its words occur in `transcript.md`; it is covered if at least 80% of its words occur in `article.md` or the text of `diagrams/*.drawio`. Coverage = covered / unspoken. Limitation: the word match is over the whole article, not the nearby chapter, so it is lenient for short lines.

## Results

Run date 2026-11-26.

### Extreme learning situations as testers (EclipseCon, 31 slides, 22 min)

Full skill run, `grade.py` on its output:

| Check | Result |
|---|---|
| Required files | pass |
| Slide recall | 0.89, fail (25 of 28 counted slides; build steps 18-20; missed 22 (an image-only slide), 30, 31 (Resources and Images lists, likely never on screen)) |
| Unspoken coverage | 0.50, fail (1 of 2 lines; the missing one is "Thank you! Questions?" on slide 29) |
| Heading depth | 2, pass |

The recall miss is 0.007 short; the coverage sample is two lines, so one line decides it.

### Don't be a fool with a tool (askui, 55 slides, 46 min)

Not graded yet. The run following `SKILL.md` was started and stopped after step 5 began: transcription (English, `whisper.json`), slicing (50 slices kept from 132 candidates, crop `960:540:0:90`, no overlay, no layout warning), transcript and slide excerpts exist; slide notes for slides 1 to 12 were written by subagents. Missing: slides 13 to 50, outline, chapters, edit pass, review gate, info area, final build. Grade it with `grade.py <article dir> testdata/talks/fool-with-a-tool` after a full run.
