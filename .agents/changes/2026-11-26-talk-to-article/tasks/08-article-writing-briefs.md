---
id: 08
dependencies:
- 03
---

# Task 08: Article-writing briefs

Subagents can turn a transcript and slide notes into a structured article: outline, chapters in parallel, one editing pass.

## Outcome

`references/article-writing.md` holds three briefs:

- **Outline:** chapters and subchapters with time and slide ranges; frame from section/title slides when present, otherwise from transcript topic shifts.
- **Chapter:** one chapter as textbook-style prose (not a cleaned-up transcript) with lists, quotes, re-created items and screenshots placed per slide note; includes unspoken slide content.
- **Edit pass:** one voice, no duplicates across chapters, cross references, info area at the top, article language (English or German).

Commit message direction: "Add briefs for outlining and writing the article".

## References

* `design.md#chapter-structure-from-slides-and-transcript`
* `design.md#slide-content-is-a-source-of-its-own`
* `design.md#article-language`
* `design.md#interfaces` (slide note format, transcript excerpt)
* Task 03 (`transcript.py`, used to produce test input)
* Touches: `.claude/skills/transcribing-talks/references/article-writing.md` (new)

## Work

* [ ] Outline brief: inputs (`transcript.md`, slide notes), output `outline.md` format (heading tree with `[HH:MM:SS-HH:MM:SS]` and slide numbers per section)
* [ ] Chapter brief: inputs (outline section, transcript excerpt via `transcript.py --excerpt`, slide notes of its range), Markdown rules (heading levels, lists, quotes, code/formula/diagram embedding, image paths)
* [ ] Edit brief: merge chapters, unify voice, remove duplicates, add info area from confirmed values
* [ ] Writing rules: plain facts, no filler, speaker's claims kept as claims

## Verification

* [ ] Run by hand on the EclipseCon transcript (task 03) with sample slide notes
* [ ] The outline follows the talk's topics; also run with section/title slide notes removed, so the structure must come from the transcript alone
* [ ] Chapter output has subchapters, at least one list and one quote where the talk has them
* [ ] Unspoken content from a slide note appears in its chapter
* [ ] The edited article has no duplicated paragraphs across chapters
