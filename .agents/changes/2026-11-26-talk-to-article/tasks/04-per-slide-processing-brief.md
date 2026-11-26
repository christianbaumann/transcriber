---
id: 04
dependencies: []
---

# Task 04: Per-slide processing brief

A subagent can take one slide image plus its transcript excerpt and produce a slide note with edited image, re-created content and the content the speaker did not say.

## Outcome

`references/slide-processing.md` is a self-contained brief. Following it, one subagent per slide:

- reads the slide (vision; `tesseract` cross-check for small text)
- edits the image with `magick` where needed (lighting, colors, contrast) and logs each command
- re-creates diagrams (draw.io by default, other format when better), code (fenced blocks), formulas (LaTeX + rendered image), tables (Markdown)
- writes `slides/NNNN.md` in the slide note format

Commit message direction: "Add per-slide processing brief for slide notes".

## References

* `design.md#interfaces` (slide note format)
* `design.md#slide-reading-by-claude-ocr-as-cross-check`
* `design.md#image-editing-with-imagemagick-driven-by-the-agent`
* `design.md#re-create-non-text-content`
* `design.md#screenshots-only-where-they-add-something`
* Sample input: slides of `~/Downloads/Extreme learning situations as testers EclipseCon.pdf`, transcript excerpt by hand
* Touches: `.claude/skills/transcribing-talks/references/slide-processing.md` (new)

## Work

* [ ] Write the brief: inputs (absolute paths: slide PNG, excerpt, output dirs), steps, output format, rules for `kind` and `show_screenshot`
* [ ] ImageMagick section: look first, choose operations, never overwrite the original, append each command to `imagemagick.log`
* [ ] Re-creation rules per kind, incl. draw.io export command (`.drawio` kept next to export) and formula rendering
* [ ] Done criteria per step, as in the vendored skills

## Verification

* [ ] Run by hand with a subagent on 4 EclipseCon slides of different kinds (text only, diagram, photo/screenshot, mixed)
* [ ] Each run writes a valid slide note (frontmatter keys as in the design)
* [ ] Re-created diagrams open in draw.io and match the slide content
* [ ] `imagemagick.log` holds the commands; originals are unchanged
* [ ] A text-only slide gets `show_screenshot: false` and no edited image
