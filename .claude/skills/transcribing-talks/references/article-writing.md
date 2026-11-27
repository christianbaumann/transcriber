# Article writing

Three briefs, run in this order: one outline subagent, one chapter subagent per chapter (in parallel), one edit subagent. The orchestrator passes the inputs as absolute paths. Each subagent works only on its own task and writes only the files named below.

Shared inputs:

| Name | Meaning |
|---|---|
| `TRANSCRIPT` | `transcript.md`: `[HH:MM:SS]` per paragraph, `→ slide NNNN` markers where a slide appears. |
| `NOTES` | Folder with slide notes `NNNN.md` (format in `slide-processing.md`, step 7). |
| `OUT` | Article folder (`out/<NAME>/article/`). Image and diagram paths in the article are relative to it. Never write below it except where a brief says so. |
| `WORK` | Work folder: `outline.md`, `chapters/NN.md`. |
| `LANGUAGE` | `English` or `German`. The orchestrator decides (the talk's language if it is one of the two, else the user's choice). Write all prose in it, whatever the transcript's language. |

Commands run in zsh. Slide numbers are integers in the outline and four digits (`0007`) in file names.

## Writing rules (all three briefs)

- Plain facts in plain verbs. No filler, no praise, no sweeping statements, no rule-of-three lists, no "not only X but also Y". No emojis. Avoid "delve", "landscape", "seamless", "transformative", "crucial", "journey".
- Sources are the transcript and the slide notes. Add no fact, number, name or source from your own knowledge, and do not correct the speaker. If a claim is doubtful, keep it as a claim.
- Keep the speaker's claims as claims: "according to the speaker", "in the speaker's experience". Studies, numbers and quotes the speaker only names stay attributed ("the speaker cites studies that put the cost of task switching at up to 40% of productive time; he says the numbers vary"). Experience reports are told in the third person ("the speaker joined the project on April 1st"); the edit pass keeps that.
- Speech recognition errors: where the slide notes spell a name or term, use that spelling. Otherwise use the transcript's.
- Do not write greetings, thanks, hashtags, social handles, "as I said earlier", "let me show you", "on the next slide", jokes that need the room, or the speaker's talk logistics. Content in them (a link, a book title) stays.

## Outline brief

Inputs: `TRANSCRIPT`, `NOTES`, `LANGUAGE`, `OUTLINE` (file to write: `$WORK/outline.md`).

### 1. Read

Read `TRANSCRIPT` completely. Read every note in `NOTES` (front matter and body). Many decks are mostly photos: for those the note body is one `[Image: ...]` line. Note the notes with `kind: text` and a short heading-like body, and slides that show a title or section name: they may give the frame. Also note picture slides without a `#` heading that are followed by a run of slides on one topic (for example a full-picture character, then "Normalcy bias - What?", "Normalcy bias - Examples", ...): they open that topic.

Done when: you know the talk's topics in order and which slides, if any, carry section or title text or open a topic.

### 2. Find the structure

- Slides that carry a section or title text (a short `#` heading, no sentences, often followed by slides of its body) are the frame: each starts a chapter. Confirm against the transcript: the speaker announces or moves to that topic at about the slide's time. If the speaker's flow disagrees with a slide, follow the transcript.
- Divider: the slide that opens a chapter, either one with section text ("Chapter Two : U", "Part 3") or a picture without heading followed by a run of slides on the chapter's topic. A divider carries at most a heading and a subtitle: a slide with bullets or body text is never a divider. A chapter has at most one divider; many chapters have none. A chapter with a divider starts at the transcript paragraph that holds the divider's `→ slide` marker, also when the speaker starts the topic a few seconds later; the previous chapter ends there. When at most 5 words of its paragraph follow the marker (the slide appears as the speaker finishes the previous topic), the chapter starts at the next paragraph instead. A picture slide that opens a run of slides on the next topic is still a divider when its marker sits at the end of the previous paragraph.
- Title slide: the slide that shows the talk's title (often with speaker and event). Name it in the front matter. It is not a divider.
- With no such slides, take the frame from the transcript: topic announcements ("first", "next, I'll talk about", "let's talk about", "finally"), a change of subject, and slide runs where one picture stays while the topic continues. Photos show where a topic holds still, not what it is.
- A chapter is one topic that a reader would look up by title. A subchapter is a distinct point inside it (a technique, a story, a numbered tip). A story that serves one point belongs to that point's subchapter.
- Slide series: when a chapter's slides carry headings `<topic> - <part>` ("Normalcy bias - What?", "... - Examples", "... - Why?"), each part is a subchapter, titled by its part in plain words ("What it is", "Examples", "Causes"). Chapters with the same series get the same subchapter titles in the same order, so the article treats them alike.
- Chapter title: names the topic in 2 to 6 words, derived from what the speaker says, not from a photo.
- Give the article a title: the title slide's text, else the speaker's introduction ("my talk ..."), else the transcript's topic. `OUTLINE` states it; the info area may replace it.
- Ranges tile the talk: the first range starts at the first spoken word, each range ends where the next begins, the last ends at the end of the transcript. Times are `[HH:MM:SS]` of transcript paragraphs; slide numbers from the `→ slide` markers (`slides 3-9`: first slide shown in the range to last). A slide shown across a boundary belongs to the range where it first appears.
- Opening (greeting, who the speaker is, what the talk is about) and closing (thanks, questions): keep what has content as the first or last chapter (the motivation or the summary), drop the rest by listing the range under `Not in article`. A Q&A (questions from the audience and the answers) is never a chapter: list its range under `Not in article` with reason `Q&A`.
- The article ends with a conclusion. When the talk has a summary or closing chapter of its own, title it `Conclusion` (German `Fazit`); it is the conclusion. Otherwise the outline gets no conclusion chapter: the edit pass writes one.

Done when: every spoken minute is in exactly one chapter range or in `Not in article`; chapter count fits the talk (a chapter is about 2 to 10 minutes, rarely a single paragraph).

### 3. Write `OUTLINE`

```markdown
---
title: Extreme learning situations as testers
language: English
title_slide: 1
---

## 1. Motivation [00:00:27-00:04:36] slides 3-21
Covers: competing expectations when starting a new project; the PSD2 project as example.

### 1.1 Learning and delivering at once [00:00:27-00:01:08] slides 3-6
Covers: ...

## 2. Setting priorities [00:04:36-00:06:26] slides 22-33
Divider: 22
Covers: ...

Not in article: [00:00:02-00:00:27] greeting, social handles
```

Rules:

- `##` chapter, `###` subchapter; numbers `N.` and `N.M` in the heading. Each section has `[start-end]` and `slides a-b` after the title; sections without slides write `slides -`.
- Subchapter ranges tile their chapter's range.
- One `Covers:` line per section: the points of the section in at most 25 words, so the chapter writer knows what belongs and what the neighbours cover.
- `title_slide: N` in the front matter when the talk has a title slide (slide number as in `slides a-b`); omit it otherwise. The title slide may lie in a `Not in article` range.
- `Divider: N` on the line right after a `##` heading when the chapter has a divider; omit it otherwise. Never on a `###` subchapter.
- `Not in article:` lines, one per range outside all chapters, as `Not in article: [start-end] reason`. The last range ends at the transcript's last paragraph time; if it starts there, write `[HH:MM:SS-end]`. Slides shown only inside such a range (title, portrait) appear in no `slides` range.
- A subchapter needs at least a few sentences of content; fold anything shorter (under about 30 seconds) into its neighbour, except the parts of a slide series. A chapter with one topic has no subchapters unless a slide series splits it.
- Write nothing else: no prose, no comments.

Done when: the file has the front matter, all sections in time order, ranges that tile the talk, and the check below prints `ok`. It fails when a slide marker inside a section's time range lies outside the section's `slides` range, when the last `Not in article` range does not end with `end`, or when a `Divider:` slide's marker is neither in the first paragraph of its chapter nor among the last 5 words of the paragraph before it. Save it to a temp file and run `python3 <file> "$OUTLINE" "$TRANSCRIPT"`; fix the outline and rerun until it passes.

```python
import re, sys
outline, transcript = open(sys.argv[1]).read(), open(sys.argv[2]).read()
sec = lambda t: sum(int(x) * m for x, m in zip(t.split(":"), (3600, 60, 1)))
paras = [(sec(m[1]), [int(n) for n in re.findall(r"slide (\d+)", m[2])])
         for m in re.finditer(r"^\[(\d\d:\d\d:\d\d)\] (.*)$", transcript, re.M) for m in [(0, m[1], m[2])]]
bad = []
for h, a, b, first, last in re.findall(r"^(#+ .*?) \[(\d\d:\d\d:\d\d)-(\d\d:\d\d:\d\d)\] slides? (\d+|-)(?:-(\d+))?$", outline, re.M):
    shown = sorted({n for t, ns in paras if sec(a) <= t < sec(b) for n in ns})
    lo, hi = (int(first), int(last or first)) if first != "-" else (1, 0)
    bad += [f"{h}: slide {n} appears in range but is outside slides {first}-{last or first}" for n in shown if not lo <= n <= hi]
for m in re.finditer(r"^Not in article: \[(\S+?)-(\S+?)\]", outline, re.M):
    if not (m[2] == "end" or re.fullmatch(r"\d\d:\d\d:\d\d", m[2])): bad.append(f"bad end: {m[0]}")
last = re.findall(r"^Not in article: \[\S+?-(\S+?)\]", outline, re.M)
if last and re.fullmatch(r"\d\d:\d\d:\d\d", last[-1]) and sec(last[-1]) >= paras[-1][0]: bad.append("last range must end with 'end'")
ends = [(sec(m[1]), re.findall(r"slide (\d+)(?:\s+[^\s→]+){0,5}\s*$", m[2])) for m in re.finditer(r"^\[(\d\d:\d\d:\d\d)\] (.*)$", transcript, re.M)]
for h, a, d in re.findall(r"^(## .*?) \[(\d\d:\d\d:\d\d)-\S+?\].*\n(?:Divider: (\d+)\n)?", outline, re.M):
    first = next((ns for t, ns in paras if t >= sec(a)), [])
    before = [e for t, e in ends if t < sec(a)][-1:]
    if d and int(d) not in first and [int(d)] not in [[int(n) for n in e] for e in before]: bad.append(f"{h}: divider {d} is neither in the chapter's first paragraph nor at the end of the paragraph before it")
print("\n".join(bad) or "ok")
sys.exit(bool(bad))
```

Report in at most 6 lines: chapter count, whether the frame came from slides or from the transcript, doubtful boundaries.

## Chapter brief

Inputs: `OUTLINE`, `CHAPTER` (number, for example `2`), `EXCERPT` (text file: the chapter's transcript range, produced with `transcript.py <whisper.json> --excerpt HH:MM:SS-HH:MM:SS`), `TRANSCRIPT`, `NOTES`, `OUT`, `LANGUAGE`, `CHAPTER_FILE` (`$WORK/chapters/NN.md`, to write).

The excerpt is plain text without paragraph times or slide markers. Use `TRANSCRIPT` for those: read only the paragraphs inside the chapter's range. Do not read other chapters' text or notes; the outline tells what they cover.

### 1. Read

Read the chapter and its subchapters in `OUTLINE` (its `Divider:` line, and the `Covers:` lines of the neighbours). Read `EXCERPT`, the paragraphs of the range in `TRANSCRIPT`, and every note of the chapter's slide range (body and front matter: `kind`, `show_screenshot`, `assets`, `edited_image`, `unspoken`). List for yourself: what each slide shows, which of it the speaker says, and where each slide appears in the speech.

Done when: you can say for every slide of the range whether it is a photo to maybe show, re-created content to place, or text to merge.

### 2. Write the chapter as textbook prose

Write `CHAPTER_FILE`. Content, in this order of priority: what the speaker says, what the slides say beyond that. Form:

- Prose that explains, in the order that teaches best, not in speaking order. Define terms before use. Turn talk into statements: "Task switching costs time" instead of "you know, switching costs a lot". Merge repetitions, drop false starts and asides that only fill speech. Keep every distinct point, example, number, name and source, including stories (shortened to what they illustrate).
- Do not clean up the transcript sentence by sentence. A reader who never heard the talk should not notice it was one.
- Headings: the chapter heading is `## N. Title` (as in the outline), subchapters `### N.M Title`, a further level only if needed (`####`). Never `#`. Use the outline's titles; change one only when it misleads and say so in your report.
- Lists: use a bullet list for three or more parallel items the speaker or a slide enumerates, a numbered list for steps in a fixed order. Each item a phrase or a sentence. Slide lists become lists in the same order.
- Quotes: a `>` blockquote for words that are quoted: a regulation or requirement text, a quote from a slide or a person, a book title with its author in the line. Verbatim from transcript or slide, with attribution. Do not turn the speaker's own explanations into quotes.
- Code, formulas, tables, diagrams come from the slide note, not from your reading of the image:
  - code: copy the fenced block from the note
  - formula: copy the LaTeX (`$...$`, `$$...$$`) from the note; do not embed the rendered PNG
  - table: copy the Markdown table
  - a re-created diagram is placed where its slide appears, also when `show_screenshot` is `false`, unless the speaker does not use it
  - diagram: `![caption](diagrams/NNNN-name.svg)` using the `.svg` (or `.png`) in `assets`, never the `.drawio` or `.mmd` source; add one or two sentences saying what it shows, from the note's description, so the text works without the picture
- Images: show a note's `edited_image` as `![caption](images/NNNN.png)` in these cases only (a note without `edited_image` is never shown):
  - Divider: the chapter's `Divider: N` slide goes directly below the `##` heading, before the first sentence. Always placed.
  - Meme: a note with `meme: true` is always placed, whether or not the speaker refers to it, after the paragraph where its slide appears.
  - Referenced: the speaker refers to the picture ("the guy on the right", "this comic"), it is a tool or UI screenshot, or it illustrates a concrete example. After the paragraph where the slide appears.
  - No repeats: a run of slides with the same picture shows it at most once: the slide the speaker refers to, otherwise the first of the run.
  - Key slides are not yours: the edit pass chooses them for the whole article at once, so that all chapters follow the same choice. Do not place them.
  - Caption: one line. For a `text` slide, the slide's text (title, then subtitle after a colon); for a picture, a factual line from the note's `[Image: ...]` text (for a meme, what it shows).
  - Everything else is omitted: a decorative photo that is not referenced, and any picture the text does not need. The title slide (`title_slide` in `OUTLINE`) and key slides are placed by the edit pass, not here.
- Paths: relative to `OUT` (`images/...`, `diagrams/...`), exactly as in the note. Never the slice path, `reference/` or an absolute path.
- Unspoken content: every `unspoken` item of every note in the range appears in the chapter in its natural place, as prose, list item or table, in the chapter's language. The Images rule wins: an item that only describes a picture (an older note may list one) is not text to place, and the picture stays omitted unless the Images rule shows it. A title that names an organization in full: give the full name at first mention ("the CSSF (Commission de Surveillance du Secteur Financier)"). Do not mark it as coming from a slide.
- Do not repeat what a neighbour chapter covers. When a point depends on one, refer to it in a clause ("see chapter 3") instead of explaining again; the edit pass checks the references.
- Length follows the content. Do not pad.

Done when: every slide of the range is shown, merged or knowingly omitted; every distinct point of the excerpt is in the text; every `unspoken` item is in the text.

### 3. Check

Fix what fails:

1. Every image path in `CHAPTER_FILE` exists below `OUT` (`test -f`). A chapter with `Divider: N` has `images/NNNN.png` of that slide on the line after its `##` heading (one blank line between). No picture appears twice; no image other than divider, meme and referenced pictures.
2. Every `unspoken` item of the range is found in the text (search by its key words).
3. No `#` heading, headings match the outline's numbering, subchapters in order.
4. No run of 8 or more words is copied from `EXCERPT` unchanged except in quotes. Save the script below to a temp file and run `python3 <file> "$EXCERPT" "$CHAPTER_FILE"`. Reword every hit, except a hit that is a title, a name or the wording of a slide list item.

```python
import re, sys
words = lambda t: re.sub(r"[^\w']+", " ", t.lower()).split()
src = words(open(sys.argv[1]).read())
seen = {tuple(src[i:i + 8]) for i in range(len(src) - 7)}
text = " ".join(l for l in open(sys.argv[2]) if not l.startswith(">"))
w = words(text)
hits = sorted({" ".join(w[i:i + 8]) for i in range(len(w) - 7) if tuple(w[i:i + 8]) in seen})
print("\n".join(hits) or "ok")
sys.exit(bool(hits))
```
5. You created no other files except temp files, which you delete.

Report in at most 8 lines: chapter number, subchapter count, lists and quotes written, images placed and omitted (slide numbers), unspoken items placed, outline titles changed, anything in the transcript you could not make sense of.

## Edit brief

Inputs: `OUTLINE`, `CHAPTERS` (folder with `NN.md`), `NOTES`, `INFO` (JSON with the confirmed info-area values), `OUT`, `LANGUAGE`, `ARTICLE` (`$OUT/article.md`, to write).

`INFO` keys: `title`, `event`, `date`, `speaker`, `source`, `duration`. A key may be missing or empty.

### 1. Read

Read `OUTLINE`, `INFO` and all chapters in order.

Done when: you know each chapter's points, terms and images.

### 2. Merge and fix

Write `ARTICLE`:

1. Info area first: `# <title>` (from `INFO.title`, else the outline's title), then one bullet per non-empty key in this order, as `- **Event:** ...`, `- **Date:** ...`, `- **Speaker:** ...`, `- **Source:** ...`, `- **Duration:** ...`, labels in `LANGUAGE`. Omit empty keys; invent no values. When `OUTLINE` has `title_slide: N` and that note has `edited_image`, put its image below the bullets as `![<slide text>](images/NNNN.png)`. Nothing else between the info area and the first chapter.
2. Chapters in outline order below it, headings unchanged (`##`, `###`).
3. Duplicates: when two chapters say the same thing (a definition, an example, an `unspoken` item, an image), keep it where the outline puts the topic and replace the other with a short reference ("see 2.1") or remove it. A term is defined once, at first use. An image or diagram appears once.
4. One voice: the same person and tense for the speaker's experience reports (third person, past tense), present tense for advice and facts, the same term for the same thing across chapters, consistent list style, the same spelling variant of the language. Rewrite only what differs.
5. Cross references: where a chapter points to another ("see chapter 3"), use a link to the heading, `[3. Managing expectations](#3-managing-expectations)` (GitHub anchor rule, which the HTML build uses too: lowercase, spaces to hyphens, punctuation removed, digits kept: `## 4.3 Too many arguments` is `#43-too-many-arguments`). Check every target exists; the HTML build fails on a link without a heading.
6. Transitions: add at most one sentence where a chapter starts without context. No introduction or summary that no chapter contains.
7. Conclusion: the last `##` chapter is the conclusion (`## N. Conclusion`, German `## N. Fazit`). If a chapter is the talk's own summary or closing (titled Summary, Conclusion, Fazit or similar), it is the conclusion: retitle it `Conclusion` / `Fazit`. If none exists, write one as the last chapter: 1 to 2 paragraphs that wrap up the key points of the chapters in the chapters' words, with no new fact, number, name or claim. Its number follows the last chapter. The conclusion holds key points from the chapters only, no logistics: slide sharing, contact details and reading lists stay in their chapter or are dropped. A talk's own summary that becomes the conclusion is condensed to this standard: short, at most one short list plus 1 to 2 paragraphs, no image except the talk's own summary diagram, a meme (memes are always kept), its divider, or one key slide by step 9.
8. Keep every distinct point, number, name, list, quote, table, formula and image that the chapters have, except exact duplicates. Add no facts.
9. Key slides, chosen here for the whole article at once (the chapter writers do not place them). Read every note with `edited_image` again and decide per subchapter (per chapter without subchapters):
   1. Candidates: the subchapter's slides that are not already shown. In a slide series, the slides whose heading names the subchapter's part ("Normalcy bias - Examples" for "Examples"), whatever the `slides` range says; otherwise the subchapter's `slides` range in `OUTLINE`.
   2. A candidate qualifies when it states the subchapter's key message in a few words, is a punchline or joke, or is a memorable picture.
   3. Repeat test: a picture is a repeat when its `[Image: ...]` line shows the same main character or scene as an image already shown in the chapter (divider included) and the slide adds only text beside it. It is new when the picture itself shows another character or setting, or text or an object that is the point or the joke (a sign, a book title).
   4. Parallel chapters (the same subchapter titles from a slide series) get the same treatment: decide per subchapter title across all of them. Show that subchapter's key slide in every parallel chapter only when a candidate qualifies and is new (step 3) in every one of them; otherwise in none of them.
   5. At most one key slide per subchapter. Place it after the paragraph that makes its point, captioned as in the chapter brief.
   List your choice per subchapter (slide or none, and why) before you write it; apply it the same way everywhere.

Done when: the article has the info area, all chapters in order and no point lost.

### 3. Check

Fix what fails:

1. One `#` heading (the title). Chapter and subchapter numbers run without gaps. The last `##` is the conclusion, and it contains no logistics.
2. Every image path exists below `OUT`; no path points to a slice folder or `reference/`; no image appears twice.
3. No paragraph appears twice (check with a short script comparing normalized paragraphs, and sentences of 8 or more words across chapters).
4. Every link target exists.
4a. Image check: list every image in the article with its note's `kind` (`NOTES/NNNN.md`) and whether the surrounding text refers to it. Remove any picture that is neither referenced by the text nor a key slide by step 2.9. Parallel chapters show images at the same subchapters. Never remove: the title slide image, a chapter's divider image (the `Divider:` slide below its `##`), a note with `meme: true` (a run of identical meme slides keeps it once), re-created diagrams.
5. The words of `INFO` values appear in the info area, and no other value is invented.
6. You created no files except `ARTICLE` and temp files, which you delete.

Report in at most 8 lines: duplicates removed (where), voice fixes, references added, anything you could not resolve.
