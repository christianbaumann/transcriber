---
id: 02
status: done
dependencies: []
---

# Task 02: Add "Dragons" ground truth

`grade.py` can grade a run of the AgileTD 2025 talk "Dragons, biases, and other things you shouldn't ignore" against committed ground truth, and a fresh clone can restore its video and deck.

## Intended behavior

- `testdata/talks/dragons-agiletd/` holds `slides/NN.png`, `slides.md`, `talk.json` with one numbering (PDF order), so `grade.py` pairs PNG `NN` with `# Slide N`
- `scripts/restore-testdata.sh` copies the three gitignored files from `~/Downloads`
- `evals.json` has a third entry; its expectations equal `grade.expectation_texts`
- Commit message describes this, e.g. "Add AgileTD 2025 talk as reference talk"

## References

* `design.md#the-new-talk-downloads`, `design.md#ground-truth-follows-the-pdf-numbering`, `design.md#slides-not-shown`, `design.md#two-speakers-in-one-string`, `design.md#folder-name`
* Source files: `~/Downloads/Dragons biases and other things you shouldnt ignore AgileTD 2025.mp4`, `~/Downloads/Dragons, biases, and other things you shouldn’t ignore.pptx`, `~/Downloads/Dragons, biases, and other things you shouldn’t ignore.pdf`
* Touches: `testdata/talks/dragons-agiletd/` (new), `scripts/restore-testdata.sh`, `.claude/skills/transcribing-talks/evals/evals.json`, `CLAUDE.md` ("Reference talks"), `.agents/changes/2026-11-26-talk-to-article/design.md` (one pointer line below the talk table, line ~242)
* Conventions: existing `testdata/talks/fool-with-a-tool/` (PNG 100 dpi, PNG8; `slides.md` from `pptx-to-markdown`, image links and alt text dropped; `talk.json` keys), `.claude/skills/transcribing-talks/evals/README.md` ("Checks and thresholds")
* Tests: `.claude/skills/transcribing-talks/scripts/tests/test_grade.py` (`test_evals_json_expectations_match_grader`)

## Work

* [x] Restore files: add `DRAGONS=dragons-agiletd` block to `scripts/restore-testdata.sh` (names above → `video.mp4`, `deck.pptx`, `deck.pdf`), run it
* [x] Check the video: which slides are shown, whether pptx 35-41 (Inattentional Blindness) appear, which of the wrap-up slides 32/33 the PDF holds, whether slide 29 (linked video) plays. If 35-41 are shown, stop and ask the user
  **Note:** Frames sampled every 30 s, every 5 s near the end. Deck first appears at about 6.5 min (before: welcome slide, room shots). Slides 3-32 and "Thank you" appear; pptx 35-41 never appear. Slide 29 shows a black player for about 5 s (about 34:45); the video does not play. Pptx 32 and 33 have identical text and notes, so which one the PDF holds cannot be told and does not matter. Q&A: "Thank you" at about 37:50, room/stage shots from 38:20 to the end (42:58).
* [x] `slides/NN.png` from the PDF (33 pages) as for the other talks
* [x] `slides.md` via `pptx-to-markdown`; drop the wrap-up slide missing from the PDF and slides 35-41; renumber `# Slide N` to the PDF page order
  **Note:** Pptx 33 dropped (text from pptx 32 kept), pptx 34 renumbered to 33.
* [x] `talk.json`: title, `"speaker": "Søren Wassard, Christian Baumann"`, event `Agile Testing Days 2025`, date (as precise as the sources allow), `duration_seconds` (2577.88), `slide_count` 33, `animated_slides`, `not_shown` only if confirmed in the video, plus a note with the pptx-to-PDF slide mapping
  **Note:** `date: "2025"` (no more precise source). `animated_slides: [4, 29]` from pptx timing nodes. No `not_shown`: slides 35-41 are outside the PDF numbering, so the mapping goes in `note`.
* [x] `evals.json`: entry `id: 3`, prompt, `files`, `ground_truth: testdata/talks/dragons-agiletd`, expectations as in the other entries
* [x] CLAUDE.md "Reference talks": add the talk (slide count, two speakers, deck/PDF mismatch, date precision)
* [x] Old design: one line below the talk table pointing to `.agents/changes/2026-11-26-backlog-qa-dragons/design.md` for the third talk

## Verification

* [x] `ls testdata/talks/dragons-agiletd/slides | wc -l` equals `grep -c '^# Slide' slides.md` equals `slide_count`
  **Note:** 33 = 33 = 33, and `pdfinfo deck.pdf` gives 33 pages.
* [x] Spot check: PNG and `# Slide N` text match for N = 1, 29, 30, 32, 33
  **Note:** Checked by viewing the PNGs (also N = 10), and for all 33 pages by matching every word of 4+ letters in the `slides.md` body against `pdftotext` per page. No misses.
* [x] `grade.py` on a dummy article dir with `--slices testdata/talks/dragons-agiletd/slides` gives slide recall 1.00 (deck against itself)
  **Note:** 33/33, run on an empty dummy dir in scratch.
* [x] `git status` shows no video, pptx or pdf (gitignore holds)
  **Note:** `git check-ignore` confirms all three.
* [x] Tests pass: `uv run --with pytest --with pyyaml --with numpy --with pillow --with scipy pytest .claude/skills/transcribing-talks/scripts/tests`
  **Note:** 63 passed.

## Deviations from the design

- The design says "none hidden". In fact the pptx marks slides 35-41 hidden (`show="0"` on `slide35.xml` to `slide41.xml`). This confirms the decision to leave them out; no change to the approach.
