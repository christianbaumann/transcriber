---
datetime: 2026-11-26T20:14:34+01:00
author: Christian Baumann
tags: [skill, article, evals, testdata]
---

# Backlog: drop Q&A, add "Dragons" reference talk

Implements the two items in [backlog.md](../../../backlog.md):

1. Do not include the Q&A in the final article
2. Add "Dragons, biases, and other things you shouldn't ignore" (AgileTD 2025) as a third reference talk

Related: [talk-to-article design](../2026-11-26-talk-to-article/design.md#reference-talks-for-evals), [evals README](../../../.claude/skills/transcribing-talks/evals/README.md), [article briefs](../../../.claude/skills/transcribing-talks/references/article-writing.md).

## Context

### Q&A today

The outline brief and the edit brief keep the Q&A as its own chapter, before the conclusion:

```
today:  ... | N-1. Q&A | N. Conclusion
new:    ... | N. Conclusion          Q&A range -> "Not in article"
```

Affected lines: `article-writing.md:43-44` (outline), `:180`, `:189` (edit pass), `README.md:27`. The fool-with-a-tool recording has about 13 min of Q&A (33:15 to 46:21).

### The new talk (`~/Downloads`)

| File | Facts |
|---|---|
| `Dragons biases and other things you shouldnt ignore AgileTD 2025.mp4` | 43 min (2577.9 s), 1920x1080 |
| `Dragons, biases, and other things you shouldn’t ignore.pptx` | 41 slides, none hidden, 2 with animations |
| `Dragons, biases, and other things you shouldn’t ignore.pdf` | 33 pages, 720x405 pt |

Two speakers: Søren Wassard, Christian Baumann. Slide 29 links a video (Google Drive). Slide 1 is image-only.

The deck and the PDF do not match:

```
pptx  1 ..... 28 29 30 31 32 33 34 | 35 ............ 41
                 vid      Wrap Wrap Thank  Inattentional Blindness
pdf   1 ..... 28 29 30 31 32 -- 33 |  (absent)
```

- PDF pages 1-32 equal pptx slides 1-32; PDF page 33 is "Thank you" (pptx 34). One of the two "Wrap up" slides (32/33, probably a build) is missing.
- pptx 35-41 is a whole section after "Thank you", absent from the PDF.

`grade.py` pairs `slides/NN.png` with `# Slide N` in `slides.md` by number (`grade.py:187-191`), so images and text need one numbering.

## Key Decisions

### Q&A is left out of the article

- **Decision:** The outline lists the Q&A range under `Not in article`, like the greeting. No Q&A chapter; the conclusion is the last chapter. `transcript.md` keeps the full Q&A.
- **Reason:** Literal backlog item; simplest change; the briefs get shorter (`article-writing.md:43-44,180,189`, `README.md:27`).
- **Trade-offs:** Facts given only in answers are lost from the article. Rejected: merging useful answers into the matching chapters (chapter writers need the Q&A range, the outline needs an answer-to-chapter mapping); a `grade.py` check for Q&A headings (fragile name match).

### Scope: add the talk as eval reference, do not fix the skill here

- **Decision:** Ground truth, `evals.json` entry, one full skill run, grading, results in the evals README. Skill defects found by the run go into `backlog.md`.
- **Reason:** Keeps the change focused; fixes get their own discussion.
- **Trade-offs:** The new talk may fail a threshold until a follow-up change. Rejected: fixing in the same change; ground truth without a run.

### Ground truth follows the PDF numbering

- **Decision:** Check the video first for which slides were shown. `slides/NN.png` from the PDF (33 pages, 100 dpi, as for the other talks). `slides.md` from the pptx (`pptx-to-markdown`), without the wrap-up slide missing from the PDF and without slides 35-41, renumbered to the PDF. `talk.json` records the pptx-to-PDF mapping. If the video shows slides 35-41, stop and ask the user.
- **Reason:** Existing convention (PNGs from the PDF, text and notes from the pptx); the PDF matches the 34-slide talk; slides 35-41 come after "Thank you" and are probably unused.
- **Trade-offs:** Manual renumbering of `slides.md`. Rejected: rendering all 41 slides from the pptx with LibreOffice and marking 35-41 `not_shown` (rendering differs from the other talks); PDF text only (loses speaker notes).

### Slides not shown

- **Decision:** `not_shown` in `talk.json`, set only after checking the video.
- **Reason:** Existing rule ([evals README](../../../.claude/skills/transcribing-talks/evals/README.md#checks-and-thresholds-agreed-with-the-user)).
- **Trade-offs:** None.

### Two speakers in one string

- **Decision:** `"speaker": "Søren Wassard, Christian Baumann"` in `talk.json` and `info.json`.
- **Reason:** `review.py` (`INFO_FIELDS`) and `info.json` expect a string; no code change.
- **Trade-offs:** No structured speaker list. Rejected: a list (changes `review.py`); first speaker only (wrong).

### Folder name

- **Decision:** `testdata/talks/dragons-agiletd/`
- **Reason:** Same pattern as `extreme-learning-eclipsecon`.
- **Trade-offs:** None.

### Commit order

- **Decision:**

  | Commit | Content |
  |---|---|
  | 1 | Q&A drop: `article-writing.md`, `README.md`, backlog item removed |
  | 2 | Dragons ground truth, `scripts/restore-testdata.sh`, `evals.json` entry (`test_grade.py` green), CLAUDE.md "Reference talks", pointer note in the talk-to-article design |
  | 3 | Skill run, `grade.py`, results in the evals README, backlog item removed, new findings added to the backlog |

- **Reason:** The eval run already uses the new Q&A rule.
- **Trade-offs:** Rejected: Dragons first; one commit for all.

### Verifying the Q&A drop

- **Decision:** If the Dragons talk has a Q&A, its run is the check. Else transcribe and slice fool-with-a-tool (no earlier run output exists), run only the outline pass, and confirm that 33:15 to the end is under `Not in article`.
- **Reason:** The outline decides what becomes a chapter; a full 46 min run costs much for that.
- **Trade-offs:** In the fallback the edit-pass rule is checked by the brief text only. Rejected: full rerun of fool-with-a-tool; diff review only.

### Backlog and docs

- **Decision:** Each commit removes its backlog item and adds new findings. Update CLAUDE.md "Reference talks" (the living list of reference talks), the evals README results, `README.md:27`. In the [talk-to-article design](../2026-11-26-talk-to-article/design.md#reference-talks-for-evals), leave the talk table unchanged and add one line below it pointing to this change for the third talk.
- **Reason:** Documentation rules (`.claude/rules/documentation.md`); backlog stays current; a reader of the old design finds the third talk without the completed design being rewritten.
- **Trade-offs:** A small edit to a completed change design, against the changes-folder convention. Rejected: updating the old table; no pointer at all.
