---
id: 06
dependencies:
- 02
- 03
- 04
- 05
---

# Task 06: Both talks show their key slides end to end

A full skill run on Unlearning AI and Dragons produces articles with title slide, dividers and key slides in the right chapters, and the Dragons eval result is recorded.

## Outcome

- Both articles match the expected images in `design.md#verification`.
- The evals README records the new Dragons run (slide recall, unspoken coverage, images placed).
- Any rule gap found is fixed in the brief that owns it (02 to 05 scope) or added to `backlog.md`.
- Commit message describes the recorded result, e.g. "Record eval results with key slides for the AgileTD talk".

## References

* `design.md#verification`
* `.claude/skills/transcribing-talks/SKILL.md` (steps 0 to 12)
* Touches: `.claude/skills/transcribing-talks/evals/README.md`, `backlog.md` (if gaps remain)
* Inputs: `/Users/christian.baumann/Downloads/Unlearning AI - Pradeep Soundararajan.mp4`, `testdata/talks/dragons-agiletd/video.mp4`; `grade.py` with `testdata/talks/dragons-agiletd/`

## Work

* [ ] Run the skill on both talks
* [ ] Run `grade.py` on the Dragons output
* [ ] Compare both articles against the expected images; fix or log gaps
* [ ] Record results in the evals README

## Verification

* [ ] Unlearning AI: title slide below the info area; "Chapter 1 : I", 7, 13, 19 below the headings of chapters 1 to 4; chapter 4 starts at the "Chapter Four" slide; a few key statement slides
* [ ] Dragons: slides 1, 7, 13, 19 below the headings of chapters 2 to 5; a wizard slide; no character twice within a chapter; slide recall above 0.85
* [ ] `article.html` builds for both; image paths exist; no slice or `reference/` paths
* [ ] All repository tests pass
