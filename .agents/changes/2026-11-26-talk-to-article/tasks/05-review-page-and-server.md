---
id: 05
status: done
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

* [x] Parse slide notes (`slides/*.md` frontmatter + body); list items with `assets`
  **Note:** Items come from `assets` (images, except `.drawio`) and from the note body (fenced code, Markdown tables, `$$…$$` formulas), because the per-slide brief writes code, tables and LaTeX into the body. Verified via unit tests and real notes of slides 2, 3, 21, 23, 30.
* [x] Render the page: info fields first, then one block per item (original image, re-created asset rendered: SVG/PNG image, code block, LaTeX via KaTeX or rendered image, table)
  **Note:** Formulas typeset by KaTeX from a CDN (offline: LaTeX source shown). Verified via page-layout tests and headless Chrome screenshots.
* [x] Serve with the standard library `http.server` on a free localhost port; POST writes `answers.json`, page shows "saved"; script exits after saving (with a timeout)
  **Note:** Binds 127.0.0.1 only; images served by server-built id, no path traversal (checked).
* [x] Answer format: `{"info": {field: value}, "items": {"<slide>/<asset>": {"status": "ok"|"fix", "comment": "..."}}}`
  **Note:** Keys are `<slide>/<asset>` or `<slide>/code-N|table-N|formula-N`. Verified via test and a browser click-through.
* [x] Unit tests for note parsing, page rendering and answer writing (server tested on a random port)
  **Note:** 11 tests in `tests/test_review.py`, fixtures in `tests/fixtures/review/` shaped like brief output.

**Design deviation:** `review.py` takes an optional `--article <dir>` (default: parent of `--notes`) because note `assets` are relative to the article folder while notes live in a separate work folder.

## Verification

* [x] Tests pass
  **Note:** Verified via the CLAUDE.md test command: all script tests pass (37).
* [x] With fixture notes, the page shows each re-created item next to its original
  **Note:** Verified via a test (original before re-created per block) and headless Chrome screenshots on fixture and real notes.
* [x] Submitting writes `answers.json` in the documented format and the script exits 0
  **Note:** Verified via a server test, a CLI subprocess test, and a Playwright click-through (fix + comment + info gap) that produced the expected `answers.json` and exit 0.
* [x] Missing info fields are marked as gaps on the page
  **Note:** Verified via a test with null, empty and missing fields.
* [x] Timeout without submission: script exits non-zero with a message and no `answers.json`
  **Note:** Verified via a CLI test with a 1 s timeout: exit 1, message, no `answers.json`.
