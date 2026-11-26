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

- **Slide recall:** kept slices (`<video>-slices/`) are matched 1:1 to the deck PNGs by pixel agreement of 96x54 grayscale thumbnails, as an optimal assignment (`scipy`). Recall = matched / counted deck slides. Not counted (listed in `grading.json`):
  - build steps: slides whose text (without title) is a proper subset of the next slide's
  - repeats: slides whose picture equals an earlier counted slide (the slicer keeps only the first)
  - slides never shown: `not_shown` in the deck's `talk.json` (`{"slides": [..], "reason": ".."}`), set only after checking the video
- **Unspoken-content coverage:** for matched slides only, slide text lines (title from `# Slide N: Title` and body of `slides.md`, without notes and footers) of at least 2 words. A line is unspoken if less than 80% of its words occur in `transcript.md`; it is covered if at least 80% of its words occur in `article.md` or the text of `diagrams/*.drawio`. Coverage = covered / unspoken. Footers are lines of only `@handles`, `#hashtags` and numbers, or lines that repeat (ignoring digits) on at least half of the slides. Fewer than 5 unspoken lines, or none: the check is `inconclusive` (`passed: null`), does not fail the run, and `grading.json` reports `unspoken_lines` and `eligible_slides`. Limitation: the word match is over the whole article, not the nearby chapter, so it is lenient for short lines.

## Constants (`grade.py`)

| Constant | Value | Why |
|---|---|---|
| `THUMB_SIZE` | 96x54 | Small enough to ignore antialiasing, scaling and the inset's detail; large enough to tell slides apart |
| `PIXEL_TOLERANCE` | 24 of 255 | Grey-level difference below which two pixels agree (JPEG-like noise, scaling) |
| `MIN_SIMILARITY` | 0.65 | True pairs measured 0.73 to 0.96 (the webcam inset covers a few percent). Wrong pairs with a similar background reach 0.74, so the threshold alone does not separate them: the 1:1 assignment does, because a wrong pair loses against the true pair of the same slice. The threshold only rejects slices that match nothing |
| `REPEAT_MAX_MEAN_DIFF` | 0.5 | Mean grey difference of repeated slides is 0.0; build steps of one slide measure 1.1 or more |
| `MIN_WORD_LENGTH`, `MIN_LINE_WORDS` | 3, 2 | Drops short words and one-word lines, which match by chance |
| `LINE_MATCH_RATIO` | 0.8 | Tolerates transcription errors and rewording of a line, not a missing half |
| `FOOTER_SHARE` | 0.5 | A line on half of the slides is a footer; builds repeat lines on far fewer |
| `MIN_UNSPOKEN_LINES` | 5 | Below it one line decides the ratio |

## Results

Run date 2026-11-26.

### Extreme learning situations as testers (EclipseCon, 31 slides, 22 min)

Full skill run, `grade.py` on its output. `talk.json` lists slides 30 and 31 (Resources, Images) as not shown: the recording is 1343.8 s long and its last frames show slide 29.

| Check | Result |
|---|---|
| Required files | pass |
| Slide recall | 1.00, pass (25 of 25 counted; build steps 18-20, repeat 22 (same picture as 17), not shown 30-31; 25 slices kept) |
| Unspoken coverage | inconclusive: 2 unspoken lines in 25 slides, fewer than 5; 1 of 2 covered, the missing line is "Thank you! Questions?" on slide 29 |
| Heading depth | 2, pass |

The deck has too little slide text that the talk does not speak for the coverage check to say anything about this talk.

### Don't be a fool with a tool (askui, 55 slides, 46 min)

Not graded yet (the orchestrator adds the result).
