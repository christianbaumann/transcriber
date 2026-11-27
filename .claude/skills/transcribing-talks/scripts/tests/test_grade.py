import json
import sys
from pathlib import Path

import pytest
from PIL import Image, ImageDraw

EVALS = Path(__file__).parents[2] / "evals"
sys.path.insert(0, str(EVALS))

import grade  # noqa: E402

CONFIG = grade.load_config()
SLIDES_MD = """# Slide 1: Intro talk

Rare quantum entanglement phrase
Spoken words here
**@someone #SomeEvent**

### Notes
Some note text that is not slide text

---

# Slide 2: Build

Alpha beta gamma
**@someone #SomeEvent**

---

# Slide 3: Build final

Alpha beta gamma
Delta epsilon zeta
**@someone #SomeEvent**

---

# Slide 4: Filler

Filler words four
**@someone #SomeEvent**

---

# Slide 5: Filler

Filler words five
**@someone #SomeEvent**
"""
TRANSCRIPT = "intro talk spoken words here and also build final alpha beta gamma delta epsilon zeta"
ARTICLE = "# Title\n\n## 1. One\n\n### 1.1 Sub\n\nRare quantum entanglement phrase appears.\n"


def picture(path, shape, inset=False, size=(400, 225)):
    img = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 120, 80], fill="black") if shape == 0 else None
    d.ellipse([200, 100, 330, 200], fill="black") if shape == 1 else None
    d.polygon([(50, 200), (150, 120), (250, 200)], fill="black") if shape == 2 else None
    if inset:
        d.rectangle([size[0] - 60, 0, size[0], 40], fill="red")
    img.save(path)


@pytest.fixture
def truth(tmp_path):
    t = tmp_path / "truth"
    (t / "slides").mkdir(parents=True)
    for i, shape in enumerate((0, 1, 2, 0, 0)):
        picture(t / "slides" / f"{i + 1:02d}.png", shape, size=(1000, 563))
    (t / "slides.md").write_text(SLIDES_MD)
    return t


@pytest.fixture
def run(tmp_path):
    """Article folder plus slices for deck slides 1 and 3 (webcam inset, other size)."""
    article = tmp_path / "run" / "article"
    article.mkdir(parents=True)
    for name, text in (("article.md", ARTICLE), ("article.html", "<html/>"), ("transcript.md", TRANSCRIPT),
                       ("whisper.json", "{}"), ("imagemagick.log", "")):
        (article / name).write_text(text)
    slices = tmp_path / "run" / "slices"
    slices.mkdir()
    picture(slices / "0001_00-00-00.png", 0, inset=True, size=(1920, 1050))
    picture(slices / "0002_00-01-00.png", 2, inset=True, size=(1920, 1050))
    return article, slices


DEFAULT_MIN_UNSPOKEN_LINES = grade.MIN_UNSPOKEN_LINES


@pytest.fixture(autouse=True)
def small_sample_guard(monkeypatch):
    monkeypatch.setattr(grade, "MIN_UNSPOKEN_LINES", 1)


@pytest.fixture
def default_guard(monkeypatch):
    monkeypatch.setattr(grade, "MIN_UNSPOKEN_LINES", DEFAULT_MIN_UNSPOKEN_LINES)


def grade_run(article, truth, slices):
    return grade.grade(article, truth, slices, CONFIG)


def failed(result):
    return [e["text"] for e in result["expectations"] if e["passed"] is False]


def test_matching_run_passes(run, truth):
    article, slices = run
    result = grade_run(article, truth, slices)
    assert failed(result) == []
    assert result["metrics"]["slide_recall"] == 1.0
    assert result["metrics"]["unspoken_coverage"] == 1.0
    assert result["metrics"]["unspoken_lines"] == 1


def test_build_steps_are_not_missed(truth):
    assert grade.build_steps(grade.slide_texts(SLIDES_MD, with_title=False)) == {2}


def test_social_footer_is_not_slide_text():
    assert grade.slide_texts(SLIDES_MD)[1] == ["Intro talk", "Rare quantum entanglement phrase", "Spoken words here"]


def test_slide_title_is_slide_text():
    assert grade.slide_texts("# Slide 1: Quantum title words\n\nbody\n")[1][0] == "Quantum title words"


def test_footer_is_found_by_repetition_not_by_name():
    md = "".join(f"# Slide {n}\n\nUnique line {n} here\n**@anyone #AnyEvent {n % 2 or 2}**\n\n---\n\n" for n in range(1, 5))
    md = md.replace("Unique line 1", "First thing").replace("Unique line 2", "Second thing").replace("Unique line 3", "Third thing").replace("Unique line 4", "Fourth thing")
    texts = grade.slide_texts(md)
    assert all(len(lines) == 1 for lines in texts.values())


def test_handle_line_on_one_slide_is_kept():
    md = "# Slide 1\n\nonly here @handle thing\n\n---\n\n# Slide 2\n\nother words\n"
    assert grade.slide_texts(md)[1] == ["only here @handle thing"]


def test_missing_slide_fails_recall(run, truth):
    article, slices = run
    (slices / "0002_00-01-00.png").unlink()
    result = grade_run(article, truth, slices)
    assert any(t.startswith("Slide recall") for t in failed(result))
    assert result["metrics"]["missed_slides"] == [3]


def test_missing_file_fails_required_files(run, truth):
    article, slices = run
    (article / "article.html").unlink()
    result = grade_run(article, truth, slices)
    assert failed(result) == [grade.expectation_texts(CONFIG)[0]]
    assert "article.html" in result["expectations"][0]["evidence"]


def test_unspoken_text_missing_from_article_fails_coverage(run, truth):
    article, slices = run
    (article / "article.md").write_text("# Title\n\n## 1. One\n\n### 1.1 Sub\n\nNothing relevant.\n")
    result = grade_run(article, truth, slices)
    assert any(t.startswith("Unspoken") for t in failed(result))
    assert result["metrics"]["uncovered_lines"] == ["slide 1: Rare quantum entanglement phrase"]


def test_unspoken_text_in_diagram_counts(run, truth):
    article, slices = run
    (article / "article.md").write_text("# Title\n\n## 1. One\n\n### 1.1 Sub\n")
    (article / "diagrams").mkdir()
    (article / "diagrams" / "d.drawio").write_text('<mxCell value="Rare quantum entanglement phrase"/>')
    assert grade_run(article, truth, slices)["metrics"]["unspoken_coverage"] == 1.0


def test_flat_headings_fail_depth(run, truth):
    article, slices = run
    (article / "article.md").write_text(ARTICLE.replace("### 1.1 Sub", "Sub"))
    assert grade.heading_depth((article / "article.md").read_text()) == 1
    assert any(t.startswith("The article has headings") for t in failed(grade_run(article, truth, slices)))


def test_headings_in_code_fences_are_ignored():
    assert grade.heading_depth("# T\n\n```\n### not a heading\n```\n") == 0


def test_missing_slices_dir_gives_zero_recall(run, truth, tmp_path):
    article, _ = run
    result = grade_run(article, truth, tmp_path / "nope")
    assert result["metrics"]["slide_recall"] == 0.0


def test_evals_json_expectations_match_grader():
    for entry in CONFIG["evals"]:
        assert entry["expectations"] == grade.expectation_texts(CONFIG)


def test_cli_writes_grading_json_and_exits_1_on_failure(run, truth, tmp_path):
    article, slices = run
    out = tmp_path / "grading.json"
    assert grade.main(["grade.py", str(article), str(truth), "--out", str(out)]) == 0
    assert json.loads(out.read_text())["summary"]["failed"] == 0
    (article / "whisper.json").unlink()
    assert grade.main(["grade.py", str(article), str(truth), "--out", str(out)]) == 1


def test_cli_defaults_slices_to_folder_next_to_article(run, truth, tmp_path):
    article, _ = run
    out = tmp_path / "grading.json"
    grade.main(["grade.py", str(article), str(truth), "--out", str(out)])
    assert json.loads(out.read_text())["metrics"]["slide_recall"] == 1.0


def test_cli_explicit_slices_override_sibling_folder(run, truth, tmp_path):
    article, slices = run
    elsewhere = tmp_path / "elsewhere"
    slices.rename(elsewhere)
    (article.parent / "slices").mkdir()
    out = tmp_path / "grading.json"
    grade.main(["grade.py", str(article), str(truth), "--slices", str(elsewhere), "--out", str(out)])
    assert json.loads(out.read_text())["metrics"]["slide_recall"] == 1.0


def test_repeat_of_earlier_slide_is_not_missed(run, truth):
    article, slices = run
    picture(truth / "slides" / "03.png", 0, size=(1000, 563))
    (slices / "0002_00-01-00.png").unlink()
    result = grade_run(article, truth, slices)
    assert result["metrics"]["repeated_slides"] == [3, 4, 5]
    assert result["metrics"]["missed_slides"] == []
    assert result["metrics"]["slide_recall"] == 1.0


def test_not_shown_slides_are_not_missed(run, truth):
    article, slices = run
    (slices / "0002_00-01-00.png").unlink()
    (truth / "talk.json").write_text(json.dumps({"not_shown": {"slides": [3], "reason": "video ends earlier"}}))
    result = grade_run(article, truth, slices)
    assert result["metrics"]["not_shown_slides"] == [3]
    assert result["metrics"]["repeated_slides"] == [4, 5]
    assert result["metrics"]["missed_slides"] == []


def test_small_sample_makes_coverage_inconclusive(run, truth, default_guard):
    article, slices = run
    (article / "article.md").write_text("# Title\n\n## 1. One\n\n### 1.1 Sub\n\nNothing relevant.\n")
    result = grade_run(article, truth, slices)
    coverage = result["expectations"][2]
    assert coverage["passed"] is None
    assert "inconclusive" in coverage["evidence"]
    assert result["metrics"]["unspoken_lines"] == 1
    assert result["metrics"]["eligible_slides"] == 2
    assert result["summary"]["inconclusive"] == 1
    assert result["summary"]["failed"] == 0


def test_zero_unspoken_lines_is_not_a_pass(run, truth, default_guard):
    article, slices = run
    (truth / "slides.md").write_text("# Slide 1\n\nintro talk\n\n---\n\n# Slide 2\n\nbuild\n\n---\n\n# Slide 3\n\nx\n")
    result = grade_run(article, truth, slices)
    assert result["expectations"][2]["passed"] is None
    assert result["metrics"]["unspoken_lines"] == 0


def test_line_of_only_handles_and_hashtags_is_a_footer_even_when_it_varies():
    md = "# Slide 1\n\nReal content words\n**@a_b #Event 2020**\n\n---\n\n# Slide 2\n\nOther content words\n**@a_b #Evnt**\n"
    assert grade.slide_texts(md) == {1: ["Real content words"], 2: ["Other content words"]}
