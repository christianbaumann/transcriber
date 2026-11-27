---
id: 04
dependencies: []
---

# Task 04: Outline names title slide and dividers; chapters start at their divider

The outline marks which slide is the title slide and which slide opens each chapter, and each chapter's range starts where its divider appears, so divider images belong to the chapter they open.

## Outcome

- The outline brief writes `title_slide: N` in the front matter and `Divider: N` below a `##` heading, both optional, in the format fixed in `design.md#the-outline-agent-names-title-and-dividers`.
- A divider is a slide with chapter text ("Chapter Two : U") or a picture without heading followed by a run of slides on the chapter's topic (Dragons 1, 7, 13, 19).
- A chapter with a divider starts at the transcript paragraph holding the divider's `→ slide` marker.
- `pipeline.py chapter-excerpts` and the outline check keep working on the new format.
- Commit message describes the behavior, e.g. "Start chapters at their divider slide".

## References

* `design.md#the-outline-agent-names-title-and-dividers`, `design.md#chapters-start-at-their-divider`, `design.md#problem` (misplaced dividers table)
* Touches: `.claude/skills/transcribing-talks/references/article-writing.md` (section "Outline brief": steps 1 to 3, the format example, the check script), `CLAUDE.md` (one line under Decisions)
* Read only: `.claude/skills/transcribing-talks/scripts/pipeline.py` (`CHAPTER_HEADING`), `scripts/tests/test_pipeline.py`
* Test input: `fixtures/dragons-agiletd/` and `fixtures/unlearning-ai/` (notes, old outlines); transcripts `testdata/talks/dragons-agiletd/video-article/transcript.md`, `/Users/christian.baumann/Downloads/Unlearning AI - Pradeep Soundararajan-article/transcript.md`

## Work

* [ ] Step 2: define divider and title slide; chapter start at the divider's paragraph
* [ ] Step 3: add `title_slide` and `Divider:` to the format example and the rules
* [ ] Extend the check script: a `Divider: N` slide lies in its chapter's `slides` range and its marker paragraph is the chapter's first paragraph
* [ ] Add a `pipeline.py` test that `chapter-excerpts` parses an outline with `Divider:` lines and `title_slide` (test only; no code change expected)
* [ ] CLAUDE.md: one line on `title_slide` / `Divider:`

## Verification

* [ ] Outline brief on the Dragons fixtures: `Divider: 7`, `13`, `19` on chapters 3, 4, 5 (plus 1 on chapter 2); chapter 3 starts at or before 16:15, chapter 4 at or before 22:40, chapter 5 at or before 29:22; check prints `ok`
* [ ] Outline brief on the Unlearning AI fixtures: `Divider: 7`, `13`, `19`; chapter 4 starts at the 00:30:05 paragraph; check prints `ok`
* [ ] The extended check fails on the old fixture outline after adding `Divider: 19` to its chapter 4 (slide 19 lies in chapter 3)
* [ ] `chapter-excerpts` test passes; full script tests pass
