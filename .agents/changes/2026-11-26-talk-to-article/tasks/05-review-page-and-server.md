---
id: 05
dependencies: []
---

# Task 05: Review page and answer server

The user can check the info area and every re-created item against its original screenshot on a local page, and the answers come back to the agent as JSON.

## Outcome

`review.py` builds an HTML page from slide notes and info values, serves it on localhost, and writes the submitted form to `answers.json`. Per re-created item: original screenshot next to the re-created version, choice ok / fix, comment. Info area: each field editable, gaps marked. Commit message direction: "Add local review page for re-created slide content".

## References

* `design.md#interfaces`
* `design.md#review-pass-before-the-final-article`
* `design.md#review-ui-local-html-page-with-form`
* `design.md#info-area-at-the-start-of-the-article`
* Touches: `.claude/skills/transcribing-talks/scripts/review.py`, `scripts/tests/test_review.py`, `scripts/tests/fixtures/` (sample slide notes), `CLAUDE.md` (Commands)

## Work

* [ ] Parse slide notes (`slides/*.md` frontmatter + body); list items with `assets`
* [ ] Render the page: info fields first, then one block per item (original image, re-created asset rendered: SVG/PNG image, code block, LaTeX via KaTeX or rendered image, table)
* [ ] Serve with the standard library `http.server` on a free localhost port; POST writes `answers.json`, page shows "saved"; script exits after saving (with a timeout)
* [ ] Answer format: `{"info": {field: value}, "items": {"<slide>/<asset>": {"status": "ok"|"fix", "comment": "..."}}}`
* [ ] Unit tests for note parsing, page rendering and answer writing (server tested on a random port)

## Verification

* [ ] Tests pass
* [ ] With fixture notes, the page shows each re-created item next to its original
* [ ] Submitting writes `answers.json` in the documented format and the script exits 0
* [ ] Missing info fields are marked as gaps on the page
* [ ] Timeout without submission: script exits non-zero with a message and no `answers.json`
