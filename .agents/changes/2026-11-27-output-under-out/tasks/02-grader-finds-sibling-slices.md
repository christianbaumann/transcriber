---
id: 02
dependencies: []
status: done
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

* [x] Test first: CLI test in `test_grade.py` that builds `<tmp>/run/article/` and `<tmp>/run/slices/`, calls `grade.main` without `--slices`, and checks that slide recall uses the sibling slices
  **Note:** `test_cli_defaults_slices_to_folder_next_to_article`; `run` fixture now builds `run/article/` + `run/slices/`; added `test_cli_explicit_slices_override_sibling_folder`
* [x] Change the default in `grade.main`; drop the `re` import if it becomes unused
  **Note:** `re` is still used elsewhere in `grade.py`, so the import stays
* [x] Update the docstring, evals README and `expected_output` texts
  **Note:** docstring, evals README (2 lines), all 3 `expected_output` entries say `out/<name>/article/`

## Verification

* [x] New test fails before the change, passes after
  **Note:** recall 0.00 against `grade.py` from main, 1.0 after
* [x] Existing `test_grade.py` tests pass, including `test_evals_json_expectations_match_grader`
  **Note:** pytest `test_grade.py`
* [x] `grep -nE '<video>-(article|slices)|-article\$' .claude/skills/transcribing-talks/evals` finds nothing
  **Note:** grep exits 1, no output
* [x] Full test suite passes (CLAUDE.md "Commands")
  **Note:** 66 passed
