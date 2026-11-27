---
id: 02
dependencies: []
---

# Task 02: Grader finds the slices next to the article folder

`grade.py out/<name>/article <truth>` grades a run in the new layout without `--slices`: the default slices folder is `slices/`, a sibling of the article folder.

## Intended behavior

- `--slices` default: `<article dir>/../slices` (was the `-article` to `-slices` rename of the folder name)
- An explicit `--slices DIR` still wins
- Eval docs and `evals.json` describe the run folder as `out/<name>/article/`

Commit subject direction: "Default grader slices to the run's slices folder".

## References

* `design.md#one-folder-per-run`
* `design.md#affected-files`
* Touches:
  * `.claude/skills/transcribing-talks/evals/grade.py` (`main`, module docstring)
  * `.claude/skills/transcribing-talks/scripts/tests/test_grade.py`
  * `.claude/skills/transcribing-talks/evals/README.md` ("Grade a run", slide recall line)
  * `.claude/skills/transcribing-talks/evals/evals.json` (`expected_output` of all three entries)

## Work

* [ ] Test first: CLI test in `test_grade.py` that builds `<tmp>/run/article/` and `<tmp>/run/slices/`, calls `grade.main` without `--slices`, and checks that slide recall uses the sibling slices
* [ ] Change the default in `grade.main`; drop the `re` import if it becomes unused
* [ ] Update the docstring, evals README and `expected_output` texts

## Verification

* [ ] New test fails before the change, passes after
* [ ] Existing `test_grade.py` tests pass, including `test_evals_json_expectations_match_grader`
* [ ] `grep -nE '<video>-(article|slices)|-article\$' .claude/skills/transcribing-talks/evals` finds nothing
* [ ] Full test suite passes (CLAUDE.md "Commands")
