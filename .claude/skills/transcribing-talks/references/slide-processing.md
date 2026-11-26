# Per-slide processing

Brief for one subagent per slide. The orchestrator passes the inputs below as absolute paths. Work on this one slide only. Do not read other slides' notes.

Needs `magick` (ImageMagick 7), `tesseract`, `drawio`, `mmdc` (only when a diagram fits Mermaid better), `uv`.

## Inputs

| Name | Meaning |
|---|---|
| `SLIDE` | Slide PNG `<video>-slices/NNNN_HH-MM-SS.png`. Never modify or move it. |
| `EXCERPT` | Text file with the transcript of the time range in which this slide is shown. |
| `OUT` | Article folder (`<video>-article/`). Write only below it. |
| `NOTES` | Folder for slide notes (work files). The note goes to `$NOTES/NNNN.md`. |
| `LOG` | Absolute path of your own log fragment `<WORK>/imagemagick/NNNN.log` (the orchestrator merges the fragments). |
| `OVERLAY` | Speaker or webcam inset on most slides, as `WxH+X+Y` in the pixels of `SLIDE`, or `none`. |

`NNNN` (slide number) and `HH-MM-SS` come from the slide file name. In the note, `slide` is the number as an integer and `time` is `"HH:MM:SS"`.

Create `OUT`, `NOTES` and `$(dirname "$LOG")` (`mkdir -p`) if missing. Take `md5 -r "$SLIDE"` now; step 8 compares against it. Commands run in zsh: do not store a command in a variable and expand it, write it out.

Done when: `SLIDE` and `EXCERPT` exist, `OUT` and `NOTES` exist and are writable, the md5 is noted.

## 1. Read the slide

Read `SLIDE` with the image reader. Then cross-check small text:

```bash
tesseract "$SLIDE" - 2>/dev/null
```

Transcribe all visible text, keeping order and structure (headings, bullets, columns, labels). Where vision and OCR differ, enlarge the region (`magick "$SLIDE" -crop WxH+X+Y +repage -resize 300% region.png` into a temp file) and decide by looking. OCR is the cross-check, not the authority. Ignore the recurring footer strip at the bottom (event hashtag, handle, logo, slide number). Text with the same content in the slide body (for example next to icons) is slide text; keep it, without describing the icons.

Done when: every visible text item is transcribed or knowingly skipped as footer; every vision/OCR conflict is resolved.

## 2. Choose `kind`

Pick the one that describes what carries the meaning of the slide:

| kind | the slide is |
|---|---|
| `text` | only text (title, bullets, quote, list of links) on a plain or decorative background |
| `diagram` | boxes/arrows, flowchart, chart, graph, architecture, timeline, cartoon-like sketch with labels |
| `code` | source code or terminal output as text |
| `formula` | mathematical or chemical notation |
| `table` | a grid of rows and columns |
| `photo` | a photograph or illustration without data content, with or without a caption |
| `screenshot` | a screenshot of a tool, web page or UI |
| `mixed` | two or more of the above with substantial weight each (for example text next to a photo or portrait) |

Done when: `kind` is one value from the list.

## 3. Decide `show_screenshot`

- `false` when everything that carries meaning on the slide is re-created or is plain text: kinds `text`, `diagram`, `code`, `formula`, `table`, and `mixed` where every part is re-created. The slide's design adds nothing.
- `true` when the image adds what re-creation cannot: photos and illustrations that illustrate the talk (`photo`), tool or UI screenshots (`screenshot`), complex visuals that cannot be redrawn faithfully, and the picture part of `mixed`.
- A portrait, stock photo or decorative image counts as `photo`: `true`, because the talk refers to it or sets a mood the writer may use. The writer decides later whether to include it; your job is to provide the edited image.
- `diagram` slides that are fully labelled are `false` even when curves are only approximated. For `photo`, `screenshot` and visuals that cannot be redrawn faithfully, `true` when unsure.

Done when: `show_screenshot` is `true` or `false` and consistent with `kind`, `edited_image` and `assets`.

## 4. Re-create non-text content

Re-create what the slide says so the article does not need the picture. A portrait, photo or decoration is never re-created. Be faithful: same labels, same relations, same numbers. Do not add, fix or "improve" content. If something is unreadable, write `[unreadable]` in the item and report it.

### Diagram (default draw.io)

Write `$OUT/diagrams/NNNN-<short-name>.drawio` (lowercase, hyphens) as native mxGraphModel XML (cells `0` and `1`, all elements `parent="1"`, edges with `source`/`target`, `edgeStyle=orthogonalEdgeStyle` and arrowheads where the slide has arrows). Charts with curves: draw boxes, axes (edges with arrows), labels and approximate the curves with `curved=1` edges or polylines through `mxPoint`s in `<Array as="points">`. Keep the `.drawio` file. Include every label, quote and title that is part of the slide's picture. Add no elements the slide lacks. Default font is fine; do not imitate hand-drawn fonts.

Export next to it:

```bash
drawio -x -f svg -e -b 10 -o "$OUT/diagrams/NNNN-<short-name>.svg" "$OUT/diagrams/NNNN-<short-name>.drawio"
```

To compare, export a PNG into a temp dir (`TMP=$(mktemp -d)`) and read it (the SVG uses `light-dark()` colors that ImageMagick and the image reader do not render; keep the SVG as the article asset):

```bash
drawio -x -f png -b 10 -o "$TMP/NNNN-check.png" "$OUT/diagrams/NNNN-<short-name>.drawio"
```

Compare it with the slide. Fix the `.drawio` and re-export until labels, groups and arrows match.

Use another format only when it fits clearly better, for example Mermaid for sequence diagrams, simple flowcharts and Gantt. Then keep the source as `NNNN-<short-name>.mmd` and export with `mmdc -i <src> -o <name>.svg`.

### Code

Fenced block with language, content exactly as on the slide (indentation, comments). No asset file.

### Formula

LaTeX in the note body (`$…$` inline, `$$…$$` display) and a rendered image `$OUT/diagrams/NNNN-<short-name>.png` (black text on opaque white, legible on any viewer):

```bash
uv run --with matplotlib python -c 'import sys,matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as p; f=p.figure(figsize=(0.1,0.1),facecolor="white"); f.text(0,0,"$"+sys.argv[1]+"$",fontsize=28); f.savefig(sys.argv[2],dpi=200,bbox_inches="tight",pad_inches=0.1,facecolor="white")' '<latex without dollars>' "$OUT/diagrams/NNNN-<short-name>.png"
```

matplotlib supports a LaTeX subset. If it fails on a construct, keep the LaTeX in the note, skip the image and say so in your report.

### Table

Markdown table in the note body, header row as on the slide.

Done when: every re-created item exists, was compared with the slide by looking at it (diagrams: at the export), and each asset file is listed in `assets`.

## 5. Look at the image and fix it with ImageMagick

Do this only when `show_screenshot` is `true` (step 3). The article shows only the edited image; the original stays untouched.

Look first: read the image and name the defects (too dark or bright, color cast, low contrast, washed-out, skew, noisy, soft, a speaker or webcam inset at `OVERLAY` or visible elsewhere). Choose the smallest set of operations that fixes exactly those. Typical operations:

- exposure/contrast: `-auto-level`, `-level 5%,95%`, `-brightness-contrast B,C`, `-contrast-stretch 1%x1%`
- color cast: `-auto-gamma`, `-modulate B,S,H`, `-normalize`
- noise/softness: `-despeckle`, `-unsharp 0x1`
- geometry: `-crop WxH+X+Y +repage`, `-deskew 40%` (only if visibly skewed)

Rules:

- Write to `$OUT/images/NNNN.png`; never overwrite `SLIDE`. Create `$OUT/images/` if missing.
- If no defect needs fixing, copy the file (`cp`) and log the `cp` line with a `# slide NNNN: no defect, copied` line.
- Run each command exactly as logged (absolute paths) and write it to `LOG`, the fragment of this slide only: never touch `$OUT/imagemagick.log` or another slide's fragment. Format: a `# slide NNNN: <defect and reason>` line, then the command line. Log only commands that succeeded and produced a file.
- A speaker or webcam inset is a recording defect. Remove it when it covers no slide content: fill the region with the color of the surrounding slide background (sample a pixel next to it, `magick ... -fill '<color>' -draw 'rectangle x0,y0 x1,y1'`) or, for a plain edge strip, crop it. When it hides slide content (a photo or picture runs under it), keep it, add `inset kept` to the image note's `[Image: ...]` line and name it in your report. Look at the result: nothing else may change.
  - Extend the fill 5 to 10 px beyond the inset on its inner edges (the inset's border and scaling leave a line otherwise), staying inside the image.
  - On a textured or photographic background, copy a patch from directly below or beside the inset instead of a flat fill: `magick SLIDE \( +clone -crop WxH+X+Y +repage \) -geometry +X0+Y0 -composite OUT`. A flat fill shows as a lighter block.
- Fix defects of the recording (exposure, cast, haze), not the slide's design: a deliberately dark or colored slide stays that way. Aim for a natural look, no extreme values.
- Look at the result. If it got worse, redo from the original and log the new command (the fragment keeps the failed attempt, marked `# slide NNNN: discarded`, and you may rewrite your own fragment).
- A slide with `show_screenshot: false` gets no edited image, no log lines and no `images/` file.

Done when: `$OUT/images/NNNN.png` exists, was looked at and is better than the original (or a copy when it had no defect), and every command that produced it is in `LOG`.

## 6. Find what the speaker did not say

Compare the slide content with `EXCERPT`. List in `unspoken` each piece of slide content that the excerpt does not mention or that goes beyond it: list items, numbers, names, references, labels, table cells. One line each, naming the item and its form, for example `Latency numbers per region (table)`. Paraphrase in the speaker's tolerance: a bullet worded differently but said counts as spoken. Titles and headings count as content: list one that the excerpt never says (for example an organization's full name). Group many small items of one diagram or table in one line. Skip the footer strip and decoration. `unspoken` lists content only: never the picture itself or a description of it (the `[Image: ...]` line in the body covers that). A slide whose only unspoken part is a photo has `unspoken: []`.

If everything is spoken, write `unspoken: []`.

Done when: each slide item is either in `EXCERPT` or in `unspoken`.

## 7. Write the slide note

Write `$NOTES/NNNN.md`:

```markdown
---
slide: 7
time: "00:12:34"
image: <absolute path of SLIDE>
kind: diagram
show_screenshot: false
assets:
  - diagrams/0007-architecture.drawio
  - diagrams/0007-architecture.svg
edited_image: images/0007.png
unspoken:
  - Latency numbers per region (table, not mentioned in the talk)
---

<slide text as read from the image>
```

Rules:

- The seven keys `slide`, `time`, `image`, `kind`, `show_screenshot`, `assets`, `unspoken` appear in the order shown; `edited_image` goes after `assets` and appears only when `show_screenshot` is `true`. `assets: []` when nothing was re-created.
- `image` is `SLIDE` as passed to you. `assets` and `edited_image` paths are relative to `OUT`. List only files that stay (no temp files). Every listed file exists.
- Body: the slide text as read in step 1, in reading order, as Markdown. The slide title is a `#` heading. Re-created code, formulas and tables stand in place of their original. For a diagram, add after the text a short description of nodes and relations (`A -> B: label`; for charts: what each curve does) so a reader without the image can follow it. For a non-text picture (photo, portrait, illustration), add one neutral line `[Image: <what is visible>]`; a slide with only pictures has only these lines. No other commentary, no interpretation.
- Quote YAML strings that contain `:` or start with a special character.

Done when: the note parses (check with `uv run --with pyyaml python -c` loading the part between the `---` lines), has the keys above, and every path in it exists.

## 8. Check and report

Verify, then fix what fails:

1. `SLIDE` unchanged: `md5 -r "$SLIDE"` equals the value from the start.
2. Every `assets` and `edited_image` file exists; `.drawio` files have a matching export.
3. `LOG` holds the commands of this slide's edit (or does not exist when `show_screenshot` is false).
4. You created no files outside `$OUT`, `$NOTES` and `LOG` except temp files, which you delete.

Report in at most 8 lines (add notes on unclear parts of this brief only when the caller asks for them): slide number, kind, show_screenshot, files written, defects fixed in the image, items you could not read or re-create faithfully, and which check failed (if any).
