---
id: 06
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

* [ ] Wrap `pandoc --standalone --embed-resources` with math rendering and a small stylesheet; resolve image paths relative to the article
* [ ] Check how pandoc embeds KaTeX (it fetches from a CDN at build time); make the result work offline, or document the network need
* [ ] Clear error when `pandoc` is missing or an image path does not exist
* [ ] Tests on a fixture article with an image, an SVG, a formula, a code block and a table (skip when `pandoc` is missing)

## Verification

* [ ] Tests pass
* [ ] The HTML file contains no references to local files (all embedded)
* [ ] Opened offline in a browser, the formula renders and images show
* [ ] A missing image fails with a message naming the path
