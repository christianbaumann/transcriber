---
id: 05
dependencies: []
---

# Task 05: Show title slide, dividers and key slides in the article

The article shows the talk's visual structure and strongest moments: the title slide below the info area, each chapter's divider below its heading, and about one key slide per subchapter, without repeating a picture.

## Outcome

- Chapter writers place the `Divider: N` slide's `edited_image` directly below the `##` heading, always (like a meme).
- The edit pass places the `title_slide` image below the info area (exception to edit brief 2.1).
- Writers show a key slide (states a key message of the (sub)chapter, a punchline or joke, or a visually memorable picture), about 1 per subchapter; dividers and memes do not count. A text-only key slide's caption is the slide's text.
- A picture already shown in the chapter is not shown again unless the slide adds a new scene or a joke.
- Edit check 4a never removes divider, title slide or meme.
- README states the new behavior.
- Commit message describes the behavior, e.g. "Show title, divider and key slides in articles".

## References

* `design.md#which-slides-appear-in-the-article`, `design.md#placement`, `design.md#text-only-key-slides-are-shown-as-images`, `design.md#no-repeated-pictures`; outline format in `design.md#the-outline-agent-names-title-and-dividers`
* Touches: `.claude/skills/transcribing-talks/references/article-writing.md` (section "Chapter brief": Read step and Images rule; section "Edit brief": 2.1, 3 Duplicates, 4a, check 2), `README.md` (what-it-does list line 28, screenshot paragraph line 43)
* Test input: `fixtures/dragons-agiletd/` (notes with `edited_image`; images in `testdata/talks/dragons-agiletd/video-article/images/`), hand-annotated copy of its outline with `title_slide`/`Divider:` lines

## Work

* [ ] Chapter brief: read `Divider:` and `title_slide`; Images rule: dividers always, key-slide criteria and cap, caption for text-only slides, no repeated picture; any note with `edited_image` may be shown
* [ ] Edit brief 2.1: title slide image allowed between info area and chapter 1; 3 Duplicates and 4a: keep divider, title slide, meme
* [ ] README lines 28 and 43

## Verification

* [ ] With a hand-annotated Dragons outline (`Divider: 1/7/13/19`), chapters 2 to 5 each start with the divider image directly below `##`
* [ ] The Dragons article shows at least one wizard slide (26 to 28) and no character picture twice within a chapter
* [ ] Every image path exists below `OUT`; `build_html.py` builds the article
* [ ] With the unannotated Dragons fixture outline (no `Divider:`, no `title_slide`), no divider or title image is placed and the key-slide rule still applies
