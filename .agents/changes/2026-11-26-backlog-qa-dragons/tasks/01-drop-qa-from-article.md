---
id: 01
status: done
dependencies: []
---

# Task 01: Leave the Q&A out of the article

The article no longer has a Q&A chapter: the outline lists the Q&A range under `Not in article`, and the conclusion is always the last chapter.

## Intended behavior

- Outline pass: a Q&A (questions from the audience and the answers) is never a chapter; its range goes under `Not in article` with reason `Q&A`, like the greeting
- Edit pass: the last `##` is the conclusion; no rule mentions moving or keeping a Q&A chapter
- `transcript.md` still contains the full Q&A (unchanged)
- Commit message describes this behavior, e.g. "Leave the Q&A out of the article"

## References

* `design.md#qa-is-left-out-of-the-article`
* `.claude/skills/transcribing-talks/references/article-writing.md` (outline brief lines 43-44; edit brief step 2.7 line 180, check 3.1 line 189)
* `README.md` ("What it does", step 5, line 27)
* `backlog.md` (Q&A line)

## Work

* [x] Outline brief: closing rule (line 43) covers the Q&A explicitly as `Not in article`; remove "A Q&A chapter stays a chapter of its own and comes before the conclusion" (line 44)
* [x] Edit brief step 7 (line 180): remove "after any Q&A chapter" and the rule to move a Q&A chapter before the conclusion
* [x] Check step 1 (line 189): remove "after any Q&A chapter"
* [x] `README.md:27`: remove ", after any Q&A"; state that the Q&A is left out
* [x] `backlog.md`: remove the Q&A line
* [x] Check `SKILL.md` and CLAUDE.md for other Q&A mentions; adjust if any
  **Note:** Neither file mentions a Q&A; unchanged.

## Verification

* [x] `grep -rn -i "q&a" .claude/skills/transcribing-talks README.md` shows only the new "leave out" rule (plus eval README result text, which is history)
  **Note:** Verified via grep: hits are `article-writing.md:43` (new rule), `README.md:27`, `evals/README.md:75` (result history).
* [x] The outline example and check script in `article-writing.md` are unchanged and consistent with the new rule
  **Note:** Verified via `git diff`: only lines 43, 44, 180, 189 changed; the check script already accepts `Not in article` ranges.
* [x] Repository tests pass: `uv run --with pytest --with pyyaml --with numpy --with pillow --with scipy pytest .claude/skills/transcribing-talks/scripts/tests`
  **Note:** 63 passed.
* [x] Behavioral check on a real run happens in task 03
  **Note:** Passed on the Dragons run: the outline lists `Not in article: [00:38:06-end] Q&A`, and `article.md` has no Q&A chapter (see task 03).
