---
id: 06
status: done
dependencies: []
---

# Task 06: Self-contained HTML build

The finished Markdown article becomes one HTML file that opens offline with images, diagrams and formulas in place.

## Outcome

`build_html.py article.md --out article.html` calls `pandoc` and produces a standalone HTML file: images and SVGs embedded, formulas rendered (KaTeX), code highlighted, readable typography. Commit message direction: "Build self-contained HTML version of the article".

## References

* `design.md#interfaces`
* `design.md#output-formats`
* `design.md#output`
* Touches: `.claude/skills/transcribing-talks/scripts/build_html.py`, `scripts/article.css` (if needed), `scripts/tests/test_build_html.py`, `scripts/tests/fixtures/` (sample article), `CLAUDE.md` (Commands)

## Work

* [x] Wrap `pandoc --standalone --embed-resources` with math rendering and a small stylesheet; resolve image paths relative to the article
  **Note:** `--standalone --embed-resources --math-method=katex --css article.css --resource-path <article dir>` (`--katex` is deprecated in pandoc 3.13).
* [x] Check how pandoc embeds KaTeX (it fetches from a CDN at build time); make the result work offline, or document the network need
  **Note:** pandoc fetches KaTeX JS, CSS and fonts from its CDN at build time and inlines them (about 1.7 MB). The build and its tests need network; the output renders offline. Documented in CLAUDE.md.
* [x] Clear error when `pandoc` is missing or an image path does not exist
  **Note:** Missing pandoc, article or image exits 1 with a message. Missing resources are detected from pandoc's `Could not fetch resource` warning, so spaced (`<a b.png>`), URL-encoded, reference-style and raw `<img>` paths are handled the way pandoc resolves them.
* [x] Tests on a fixture article with an image, an SVG, a formula, a code block and a table (skip when `pandoc` is missing)
  **Note:** Fixture `tests/fixtures/build_html/` covers all five; pandoc tests skip when pandoc is missing.

## Verification

* [x] Tests pass
  **Note:** Verified via the CLAUDE.md test command: 10 passed.
* [x] The HTML file contains no references to local files (all embedded)
  **Note:** Verified via `test_no_local_file_references` (every `src`/`href` is a data URI, http(s) or `#`).
* [x] Opened offline in a browser, the formula renders and images show
  **Note:** Verified via headless Chrome with all hosts unresolvable and a screenshot: inline and display formulas, PNG, SVG, highlighted code and table render.
* [x] A missing image fails with a message naming the path
  **Note:** Verified via `test_missing_image_fails_with_path`, a CLI test, and ad hoc runs for markdown, reference-style, raw `<img>`, `diagrams/*.svg` and spaced paths.
