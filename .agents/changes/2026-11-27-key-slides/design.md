---
datetime: 2026-11-27T08:57:03+01:00
author: Christian Baumann
tags: [transcribing-talks, video-slicer, images, outline, article-writing]
---

# Key slides in the article and multi-layout slicing

## Problem

Two runs produced articles without a single slide image:

| Talk | Slices | Images made | Images in article | Cause |
|---|---|---|---|---|
| Unlearning AI (Pradeep Soundararajan, AgileTD 2025, local file) | 28, all `text` | 0 | 0 | `text` ⇒ `show_screenshot: false` ([slide-processing.md](../../../.claude/skills/transcribing-talks/references/slide-processing.md) step 3) |
| Dragons ([testdata/talks/dragons-agiletd](../../../testdata/talks/dragons-agiletd/)) | 28, `photo`/`mixed` | 28 | 0 | "earns its place" rule ([article-writing.md](../../../.claude/skills/transcribing-talks/references/article-writing.md) chapter brief, Images; edit brief 4a): speakers read Discworld quotes and never point at the illustrations |

Both behaved as designed (README: "Screenshots appear only where a re-created version cannot replace them"). The result is still wrong: the article loses the talk's visual structure, its key messages and its memorable pictures.

Two related defects:

1. **Divider slides land in the previous chapter.** A divider appears 5 to 10 s before the speaker starts the chapter, so the outline puts it in the chapter before:

   | Talk | Divider | Shown | Outline chapter start | Placed in |
   |---|---|---|---|---|
   | Dragons | 7 (townsfolk) | 16:15 | ch. 3 at 16:24 | ch. 2 |
   | Dragons | 13 (Vetinari) | 22:40 | ch. 4 at 22:45 | ch. 3 |
   | Dragons | 19 (Vimes) | 29:22 | ch. 5 at 29:30 | ch. 4 |
   | Unlearning AI | 19 ("Chapter Four : U.A.I.") | 30:29 | ch. 4 at 30:35 | ch. 3 |

2. **The slicer loses slides in a second layout.** It uses one crop box per video. Unlearning AI has three layouts (0:00-5:18 conference PiP, 5:18-7:34 zoomed room camera, 7:45-end wide room shot) and lost its title slide ("The Last Keynote of Agile Testing Days 2025 - Unlearning A.I."), "Chapter 1 : I" and four more. Dragons lost slides 3 and 4 (9:30-10:07, PiP layout). Listed in [backlog.md](../../../backlog.md).

Dividers come in two forms, which decides who can detect them:

| Form | Example | Detectable from one slide? |
|---|---|---|
| Text | Unlearning AI 7 "Chapter Two : U", 13, 19 | yes |
| Picture without heading, followed by a run of slides on the chapter's topic | Dragons 1, 7, 13, 19 (full-picture character, then "Normalcy bias - What? / Examples / ...") | no, needs the sequence |

## Target flow

```
slicer (per-segment crop) ─► slices incl. title + all dividers
        │
slide agent ─► note + edited_image for EVERY slide
        │
outline agent ─► `title_slide: N`, `Divider: N` per ##, chapter starts at divider paragraph
        │
chapter writer ─► divider under ##, title slide under info area,
                  key slides (~1 per subchapter), no repeated picture
        │
edit pass 4a ─► never removes divider, title slide, meme
```

Expected result:

| Talk | Images |
|---|---|
| Unlearning AI | title slide below info area; "Chapter 1 : I", 7, 13, 19 below chapters 1 to 4; a few key statement slides |
| Dragons | 1, 7, 13, 19 below chapters 2 to 5; the wizards; a few key slides; each character at most once per chapter unless a new scene or joke |

## Key Decisions

### Which slides appear in the article

- **Decision:** Title slide, chapter dividers (text or picture), and key slides: a slide that states a key message of the (sub)chapter, a punchline, joke or meme, or a visually memorable picture. Key slides: about 1 per subchapter; dividers and memes do not count.
- **Reason:** The article should keep the talk's structure and its strongest visual moments, also when the speaker never points at a slide.
- **Trade-offs:** "Key" is a judgment and varies between runs. Rejected: only title and dividers (drops the Dragons wizards and the strongest statements); every slide of an all-text deck (28 images repeating the prose); agenda slides as a separate class.

### Every slide gets an edited image

- **Decision:** The slide agent writes `edited_image` for every slide, including heading-only `text` slides. `show_screenshot` keeps its meaning for the existing rules; the writer may use any `edited_image`.
- **Reason:** The slide agent sees one slide and cannot know whether it is a divider or a key slide. Providing the image always lets later agents choose without a second edit pass.
- **Trade-offs:** More ImageMagick work and files in `images/`, most of them unused. Rejected: `role:` set by the slide agent (misses picture dividers); a second image pass after the outline.

### The outline agent names title and dividers

- **Decision:** The outline names the title slide in its front matter (`title_slide: N`) and each chapter's divider on its own line below the `##` heading (`Divider: N`), both optional, slide numbers as in `slides a-b`. A divider is a slide with chapter text, or a picture without heading followed by a run of slides on the chapter's topic.
- **Reason:** Only the outline agent sees all notes in sequence, which picture dividers need. A separate line keeps the heading format, so `pipeline.py` (`CHAPTER_HEADING`) and the outline check (matches `slides a-b$`) stay unchanged.
- **Trade-offs:** The outline brief grows. Rejected: a `divider:` suffix on the `##` line (breaks the check's line-end match).

Outline format (interface between outline agent and chapter writers):

```markdown
---
title: Unlearning AI
language: English
title_slide: 1
---

## 4. Experiments With AI [00:30:05-00:45:08] slides 19-27
Divider: 19
Covers: ...
```

### Chapters start at their divider

- **Decision:** A chapter's time range starts at the transcript paragraph that holds its divider's `→ slide` marker.
- **Reason:** Fixes all four misplaced dividers above; the divider then belongs to the chapter it opens.
- **Trade-offs:** The first seconds of a chapter range may hold the end of the previous sentence. Rejected: only text dividers; the writer moving images across chapters.

### Placement

- **Decision:** Divider directly below its `##` heading, always kept (like a meme). Title slide below the info area (exception to edit brief 2.1). Key slides after the paragraph where the slide appears. Edit brief check 4a never removes divider, title slide or meme.
- **Reason:** Dividers and the title slide frame the text; key slides belong to their point in the prose.
- **Trade-offs:** The info area is no longer followed directly by chapter 1.

### Key slides are chosen once, by the edit pass

- **Decision:** Chapter writers place only dividers, memes and referenced pictures. The edit pass chooses key slides for the whole article in one go: at most one per subchapter, a concrete repeat test (same main character or scene with only text beside it = repeat), and parallel chapters (same subchapter titles from a slide series such as "X - What? / Examples / Why?") get a key slide at a subchapter title in all of them or in none. The outline turns such a series into the same subchapters in every chapter; a slide with bullets is never a divider.
- **Reason:** The first Dragons run with per-writer choice gave 1, 1, 0 and 2 key slides in four chapters of identical structure: the outline had no subchapters (each writer invented its own), and seven agents judged "key" and "repeat" in isolation.
- **Trade-offs:** The edit pass does more work and must place images into prose it did not write. Rejected: keeping the choice with the writers and only aligning afterwards.

### Text-only key slides are shown as images

- **Decision:** A text-only key slide is shown as the edited image, caption = the slide's text.
- **Reason:** Keeps the slide's look; one rule for all images.
- **Trade-offs:** Text inside an image is not searchable; the caption repeats it. Rejected: styled callout or blockquote; image without caption.

### No repeated pictures

- **Decision:** A character or picture already shown in the chapter is not shown again unless the slide adds something new (another scene, a joke).
- **Reason:** Dragons puts the chapter's character next to every bullet slide; without the rule the article repeats it.
- **Trade-offs:** The writer must compare pictures by their `[Image: ...]` lines. Rejected: no limit; strictly one image per chapter besides the divider.

### Image editing

- **Decision:** Existing edit rules (lighting, contrast, insets). A live speaker in the room frame stays.
- **Reason:** No reliable way to remove a person in front of a projection.
- **Trade-offs:** Some images show the speaker's head (Unlearning AI slide 1). Rejected: picking the candidate with least speaker overlap in the slicer; inpainting.

### Multi-layout slicing, fixed upstream

- **Decision:** `video-slicer` detects layout changes from its samples and uses one crop box per time segment. Fixed in the upstream repo (`~/git_repos/_own/video-slicer`), then re-vendored into `.claude/skills/video-slicer/` with a new provenance commit; the two test path constants in `test_detect.py` and `test_score_pipeline.py` are applied again (see [CLAUDE.md](../../../CLAUDE.md), Commands).
- **Reason:** Without it the title slide and early dividers are lost, so the key-slide rules have nothing to place. Upstream keeps one source of truth.
- **Trade-offs:** Two repos and a re-vendor step. Rejected: patching the vendored copy only (lost on next re-vendor); running the slicer once per segment from the orchestrator (needs trimming or `--start/--end` and a merge).

### Two changes, slicer first

- **Decision:** Commit 1 (video-slicer upstream + re-vendor), then commit 2 (key-slide rules here, one commit on `main`).
- **Reason:** Each change is checked on its own; a slicer regression does not mix with brief changes.
- **Trade-offs:** The key-slide check waits for the slicer fix.

### Docs and evals

- **Decision:** Update README (what-it-does list and the screenshot paragraph), add one CLAUDE.md line on `title`/`divider` and key slides, remove the multi-layout entry from `backlog.md` once fixed. No new eval metric.
- **Reason:** The reference talks have no ground truth for dividers or key slides.
- **Trade-offs:** The new behavior is checked by re-running, not by `grade.py`.

## Verification

| Step | Talk | Expect |
|---|---|---|
| Slicer | Unlearning AI | title slide and "Chapter 1 : I" among the slices; layout warning lists segments, not lost slides |
| Slicer | Dragons | slides 3 and 4 among the slices; `grade.py` slide recall up from 0.85 |
| Steps 5-12 | Unlearning AI | images below chapters 1-4 headings, title slide below info area, chapter 4 starts at "Chapter Four" slide, a few key slides |
| Steps 5-12 | Dragons | 1, 7, 13, 19 below chapters 2-5 headings, the wizards, no character repeated within a chapter |

## References

- Briefs: [slide-processing.md](../../../.claude/skills/transcribing-talks/references/slide-processing.md), [article-writing.md](../../../.claude/skills/transcribing-talks/references/article-writing.md), [SKILL.md](../../../.claude/skills/transcribing-talks/SKILL.md)
- Slicer: [vendored SKILL.md](../../../.claude/skills/video-slicer/SKILL.md) (step 1 layout warning, step 2 crop box), upstream https://github.com/christianbaumann/video-slicer
- Evals: [evals README](../../../.claude/skills/transcribing-talks/evals/README.md) (Dragons results, missed slides 3 and 4)
- Earlier designs: [talk-to-article](../2026-11-26-talk-to-article/design.md), [backlog-qa-dragons](../2026-11-26-backlog-qa-dragons/design.md)
