---
name: transcribing-talks
description: Turns a video of a talk, lecture or conference session (local file or YouTube URL) into a timestamped transcript and a finished, textbook-style article with chapters, re-created diagrams, code, formulas and tables, as Markdown and a self-contained HTML file. Use when the user wants a transcript, an article, notes or a write-up of a talk, lecture or presentation video.
---

# Transcribing talks

Input: a video file or one YouTube URL. Output: `<video>-article/` next to the video (for a YouTube URL next to the download in `out/youtube/`), as described in the repository's README. Two user gates: the info area and the review page.

Run commands from the repository root. Constants:

- `MAX_PARALLEL = 6`: subagents running at once for per-slide work, chapters and fixes. Start the first 6 in one message, then one more each time one finishes.
- Every subagent: Agent tool, type `general-purpose`, `model: sonnet`. Briefs use absolute paths only. Subagents work on their own task and write only the files named in their brief.

Paths (resolve to absolute paths first):

| Name | Meaning |
|---|---|
| `SKILL` | This skill's folder `.claude/skills/transcribing-talks/` |
| `SCRIPTS` | `$SKILL/scripts` |
| `REFS` | `$SKILL/references` |
| `VIDEO` | The video file |
| `OUT` | `<VIDEO without extension>-article/` (create it) |
| `SLICES` | `<VIDEO without extension>-slices/` (the slicer's default) |
| `WORK` | `mktemp -d`. Holds `slide-excerpts/`, `slides/` (slide notes), `imagemagick/` (per-slide log fragments), `outline.md`, `chapter-excerpts/`, `chapters/`, `info.json`, `review/`. Keep it until the end; report its path |

Scripts need `uv` and are called as `$SCRIPTS/<name>.py` (PEP 723). If transcription cannot download the model because `~/.cache/huggingface/hub` is unavailable, set `HF_HUB_CACHE` to a writable folder; `mlx_whisper` exits 0 on that failure, so check that `whisper.json` exists.

## 0. Check the input

- A local file: it exists and `ffprobe` reads it.
- A URL: it names exactly one video (else ask for a single-video URL).
- The user may name the article language ("auf Deutsch"). Otherwise it is decided in step 2.

Done when `VIDEO` (or the URL) is settled and `OUT` and `WORK` exist.

## 1. Download (URL only)

One subagent. Brief:

> Read `<repo>/.claude/skills/downloading-youtube-video/SKILL.md` and follow it for `<url>`, working in `<repo>`. Add no format or cookie options. Reply with the video path and the `.info.json` path.

Done when both files exist. A failure goes to the user unchanged. `VIDEO` is now the downloaded file; `YT_INFO` is the `.info.json` (yt-dlp's file, not the info area's `info.json` of step 6).

## 2. Transcribe

```bash
$SCRIPTS/transcribe.py "$VIDEO" --out "$OUT" [--initial-prompt '<names and terms>']
```

Takes minutes for a long talk: give it a timeout of at least 30 minutes or run it in the background. Pass `--initial-prompt` only with terms you already know (YouTube title, uploader, event). It prints `language: <code>` and writes `$OUT/whisper.json`.

Article language `LANGUAGE`: the talk's language if it is `en` (English) or `de` (German). Any other language: ask the user which of the two. A language the user named in step 0 wins.

Done when `$OUT/whisper.json` exists and `LANGUAGE` is `English` or `German`.

## 3. Slice

One subagent. Brief:

> Read `<REFS>/slicer-review.md` and follow it. `VIDEO` = `<abs>`, `SLICER` = `<repo>/.claude/skills/video-slicer`, `WHISPER` = `<OUT>/whisper.json`, `TRANSCRIPT_PY` = `<SCRIPTS>/transcript.py`.

Its reply names the crop box and an `overlay` (a speaker or webcam inset it could not crop out, as `WxH+X+Y` in slice pixels, or `none`). Keep it as `OVERLAY` for step 5.

If it reports a layout warning (several slide layouts), pass it to the user and continue with the main layout. If it exports nothing, stop and tell the user why.

Done when `$SLICES/` holds `NNNN_HH-MM-SS.png` files.

## 4. Transcript and excerpts

```bash
$SCRIPTS/transcript.py "$OUT/whisper.json" --slices "$SLICES" --out "$OUT/transcript.md"
$SCRIPTS/pipeline.py slide-excerpts "$OUT/whisper.json" "$SLICES" --out "$WORK/slide-excerpts"
```

Done when `transcript.md` has `→ slide NNNN` markers and `slide-excerpts/` has one `NNNN.txt` per slide.

## 5. Per-slide processing

One subagent per slide, at most `MAX_PARALLEL` at once. Brief:

> Read `<REFS>/slide-processing.md` and follow it. `SLIDE` = `<SLICES>/<file>`, `EXCERPT` = `<WORK>/slide-excerpts/NNNN.txt`, `OUT` = `<OUT>`, `NOTES` = `<WORK>/slides`, `OVERLAY` = `<WxH+X+Y or none>`, `LOG` = `<WORK>/imagemagick/NNNN.log`.

Collect the replies. A slide whose reply lists a failed check or an unreadable item: note it; do not rerun unless the note is missing.

Then merge the log fragments in slide order (zsh; `(N)` makes an empty match legal, so this also works when no slide needed an edit):

```bash
for f in "$WORK"/imagemagick/*.log(N); do cat "$f"; done > "$OUT/imagemagick.log"
```

Done when `$WORK/slides/NNNN.md` exists for every slide in `$SLICES` and `$OUT/imagemagick.log` holds the merged fragments.

## 6. Info area

Write `$WORK/info.json`, one object for the whole run, keys `title`, `event`, `date`, `source`, `duration`, `speaker`. A value you cannot establish is `null`: no guessing, no value from your own knowledge. Sources, in order:

| Key | Sources |
|---|---|
| `title` | title slide (note of slide 1 or the first notes), the speaker's introduction in the first paragraphs of `transcript.md`, then the video's title (`YT_INFO.title`) or file name without extension. Never `null` |
| `event` | title slide, introduction, `YT_INFO.description` when it names it |
| `speaker` | title slide, introduction, `YT_INFO.description`. The uploader is a channel, not necessarily the speaker: do not use it alone |
| `date` | title slide, introduction, `YT_INFO.description`; else `YT_INFO.upload_date` as `YYYY-MM-DD (uploaded)`; local file: `null` |
| `source` | the URL (`YT_INFO.webpage_url`); local file: the file name |
| `duration` | `ffprobe` duration as `HH:MM:SS` |

The user confirms and fills the gaps on the review page (step 10), not here.

Done when `info.json` is valid JSON with the six keys.

## 7. Outline

One subagent. Brief:

> Read `<REFS>/article-writing.md`, section "Outline brief", and follow it. `TRANSCRIPT` = `<OUT>/transcript.md`, `NOTES` = `<WORK>/slides`, `LANGUAGE` = `<English|German>`, `OUTLINE` = `<WORK>/outline.md`. The article's title in `info.json` is `<title>`: use it as the outline's title.

Done when `outline.md` exists and the brief's check printed `ok` (run it yourself if the reply does not say so).

## 8. Chapters

```bash
$SCRIPTS/pipeline.py chapter-excerpts "$OUT/whisper.json" "$WORK/outline.md" --out "$WORK/chapter-excerpts"
mkdir -p "$WORK/chapters"
```

One subagent per chapter, at most `MAX_PARALLEL` at once. Brief:

> Read `<REFS>/article-writing.md`, section "Chapter brief", and follow it. `OUTLINE` = `<WORK>/outline.md`, `CHAPTER` = `<N>`, `EXCERPT` = `<WORK>/chapter-excerpts/NN.txt`, `TRANSCRIPT` = `<OUT>/transcript.md`, `NOTES` = `<WORK>/slides`, `OUT` = `<OUT>`, `LANGUAGE` = `<language>`, `CHAPTER_FILE` = `<WORK>/chapters/NN.md`.

Done when `chapters/NN.md` exists for every chapter of the outline.

## 9. Edit pass

One subagent. Brief:

> Read `<REFS>/article-writing.md`, section "Edit brief", and follow it. `OUTLINE` = `<WORK>/outline.md`, `CHAPTERS` = `<WORK>/chapters`, `INFO` = `<WORK>/info.json`, `OUT` = `<OUT>`, `LANGUAGE` = `<language>`, `ARTICLE` = `<OUT>/article.md`.

`INFO` is the same `info.json` that step 10 shows and updates.

Done when `$OUT/article.md` exists.

## 10. Review gate (user)

```bash
$SCRIPTS/review.py --notes "$WORK/slides" --info "$WORK/info.json" --article "$OUT" --out "$WORK/review"
```

Run it in the background. It prints `Review page: <url>` and opens the browser. Tell the user the URL and what to do: confirm or fill the info values (gaps are highlighted), set each re-created item to ok or fix with a comment, submit. Wait for the process to exit. Exit 0: `$WORK/review/answers.json` exists. Exit 1 (no answer within the timeout): ask the user whether to start the page again.

Done when `answers.json` exists.

## 11. Apply the answers

`answers.json`: `{"info": {...}, "items": {"<slide>/<item>": {"status": "ok"|"fix", "comment": ""}}}`.

1. Info: write `answers.info` to `$WORK/info.json` (keys with `null` stay `null`). If it differs from before, rewrite the article's info area at the top of `article.md` (the `# title` line and the bullet list below it, as the edit brief's step 2.1 defines it, labels in `LANGUAGE`, empty values omitted). Change nothing else there.
2. Fixes: for every slide with at least one item of status `fix`, one subagent, run one after another (they all edit `article.md`). Brief:

   > Read `<REFS>/slide-processing.md`. Redo only the listed items of one slide. `SLIDE` = `<abs>`, `EXCERPT` = `<WORK>/slide-excerpts/NNNN.txt`, `OUT` = `<OUT>`, `NOTES` = `<WORK>/slides`, `OVERLAY` as in step 5, `LOG` = `<WORK>/imagemagick/NNNN.log` (after the redo, replace this slide's lines in `<OUT>/imagemagick.log` with the fragment's). The slide note is `<WORK>/slides/NNNN.md`. Items to fix, each with the user's comment: `<key>: <comment>` ... Apply each comment to the item (step 4 for the re-creation, step 7 and 8 for the note and checks); keep the same file names and leave all other content of the slide as it is. Then edit `<OUT>/article.md` so that the same item (code block, table, formula, diagram image) and every sentence of the article that describes or names it matches the corrected note (search the article for the changed text); change nothing else in the article. Reply with what you changed in the note, the assets and the article.

3. Check one fix: the changed item in `article.md` matches the changed note.

Done when `info.json` and the article's info area agree, and every `fix` comment has been applied in the note and in `article.md`.

## 12. Final article and output

```bash
$SCRIPTS/pipeline.py reference "$WORK/slides" "$OUT"
$SCRIPTS/build_html.py "$OUT/article.md" --out "$OUT/article.html"
```

Checks:

- `article.md` mentions no path under `$SLICES`, `reference/`, and no absolute path (`grep -nE 'reference/|-slices/|/Users/'` finds nothing). Review screenshots live only in `$OUT/reference/`.
- Every image path in `article.md` exists below `$OUT`.
- `transcript.md` and `article.md` differ in structure: the article has the info area and `##` chapters.
- `build_html.py` needs network for KaTeX (see CLAUDE.md); if it fails, report the error and leave `article.md` as the result.

Report to the user: `$OUT` path, the files present (`article.md`, `article.html`, `transcript.md`, `whisper.json`, `images/`, `diagrams/`, `reference/`, `imagemagick.log`), `$SLICES` and `$WORK`, language, slide and chapter counts, slides with unreadable items, fixes applied.

Done when `article.html` exists and the report names every path.
