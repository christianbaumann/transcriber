---
id: 08
status: done
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

* [x] Outline brief: inputs (`transcript.md`, slide notes), output `outline.md` format (heading tree with `[HH:MM:SS-HH:MM:SS]` and slide numbers per section)
  **Note:** Output `outline.md`: front matter (title, language), `##` chapters / `###` subchapters with `[HH:MM:SS-HH:MM:SS] slides a-b`, `Covers:` lines, `Not in article:` ranges; an embedded script checks ranges against the transcript's slide markers.
* [x] Chapter brief: inputs (outline section, transcript excerpt via `transcript.py --excerpt`, slide notes of its range), Markdown rules (heading levels, lists, quotes, code/formula/diagram embedding, image paths)
  **Note:** Takes `EXCERPT` and the full `TRANSCRIPT` (`--excerpt` output has no slide markers). Formulas enter the article as LaTeX; the rendered image serves the review page only. An embedded script flags runs of 8+ words copied from the excerpt.
* [x] Edit brief: merge chapters, unify voice, remove duplicates, add info area from confirmed values
  **Note:** Info area from the orchestrator's `INFO` JSON (missing keys omitted).
* [x] Writing rules: plain facts, no filler, speaker's claims kept as claims

## Verification

* [x] Run by hand on the EclipseCon transcript (task 03) with sample slide notes
  **Note:** Verified via subagent runs following only the briefs: outline twice, chapters 3-6 in parallel, one edit pass, on the EclipseCon transcript with 95 hand-made notes. Chapters 1, 2, 7, 8 not written; formula, code and table rules not exercised (the talk has none).
* [x] The outline follows the talk's topics; also run with section/title slide notes removed, so the structure must come from the transcript alone
  **Note:** Both outlines find the same 8 chapters. The deck has no section slides, so six synthetic section-slide notes were used for the "with" run; the "without" run derived the frame from the transcript alone.
* [x] Chapter output has subchapters, at least one list and one quote where the talk has them
  **Note:** Chapters 3-6 have 3-5 subchapters each, bullet and numbered lists, and one blockquote (the xkcd caption); the talk has few true quotes.
* [x] Unspoken content from a slide note appears in its chapter
  **Note:** Verified via grep in `article.md`: CSSF full name (5.1), comic text (4.4), xkcd phase labels (5.4).
* [x] The edited article has no duplicated paragraphs across chapters
  **Note:** Verified via a script: 0 duplicate paragraphs and 0 duplicate sentences of 8+ words across chapters; the article builds with `build_html.py`.
