---
id: 03
dependencies: []
---

# Task 03: Edited image for every slide

Every slide note points to an edited image, also for text-only slides, so the outline agent and the writers can show any slide (divider, title, key slide) without a second image pass.

## Outcome

- The slide agent writes `$OUT/images/NNNN.png` and `edited_image` for every slide, whatever `kind` and `show_screenshot`.
- `show_screenshot` keeps its meaning (the picture adds what re-creation cannot) for the existing writer rules.
- Image editing follows the existing rules; a live speaker in the frame stays.
- Commit message describes the behavior, e.g. "Provide an edited image for every slide".

## References

* `design.md#every-slide-gets-an-edited-image`, `design.md#image-editing`
* Touches: `.claude/skills/transcribing-talks/references/slide-processing.md` (step 3 wording, step 5 "Do this only when show_screenshot is true" and last rule, step 7 key rule for `edited_image`, step 8 check 3)
* Test input: `/Users/christian.baumann/Downloads/Unlearning AI - Pradeep Soundararajan-slices/` (all `text` slides), `fixtures/unlearning-ai/slides/` (current notes, no `edited_image`)

## Work

* [ ] Step 5 runs for every slide; drop "A slide with `show_screenshot: false` gets no edited image ..."
* [ ] Step 7: `edited_image` is always present (after `assets`); update the example and the key-order rule
* [ ] Step 8 check 3: `LOG` always holds this slide's commands
* [ ] Step 3: state that `show_screenshot` no longer decides whether an image is made

## Verification

* [ ] Running the brief on Unlearning AI slide `0007` (text) gives `images/0007.png`, `edited_image: images/0007.png`, `show_screenshot: false`, and log lines in `LOG`
* [ ] Running it on a Dragons `mixed` slide gives the same note as before (same `show_screenshot`, `edited_image`)
* [ ] `review.py` tests still pass: `uv run --with pytest --with pyyaml --with numpy --with pillow --with scipy pytest .claude/skills/transcribing-talks/scripts/tests`
