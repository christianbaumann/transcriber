import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))

import transcript  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "whisper.json"


@pytest.fixture
def words():
    return transcript.load_words(FIXTURE)


def test_words_are_flattened_and_stripped(words):
    assert [w.text for w in words][:3] == ["Welcome", "to", "the"]
    assert len(words) == 14


def test_pause_starts_new_paragraph(words):
    paragraphs = transcript.split_paragraphs(words)
    assert [len(p) for p in paragraphs] == [8, 6]


def test_short_pause_stays_in_paragraph(words):
    assert transcript.split_paragraphs(words)[0][4] == 4


def test_render_without_slides(words):
    assert transcript.render(words, []) == (
        "[00:00:00] Welcome to the talk. Today we cover testing.\n\n"
        "[00:01:05] Now the second part begins here.\n"
    )


def test_marker_goes_before_nearest_word(words):
    slides = [transcript.Slide("0001", 2.4), transcript.Slide("0002", 66.5)]
    text = transcript.render(words, slides)
    assert "Today → slide 0001 we cover" in text
    assert "part → slide 0002 begins" in text


def test_every_slide_has_one_marker_in_time_order(words):
    slides = [transcript.Slide(f"{i:04d}", t) for i, t in enumerate([0, 0.1, 3.0, 66.0, 500.0], 1)]
    text = transcript.render(words, slides)
    found = [line for line in text.replace("\n", " ").split() if line.isdigit() and len(line) == 4]
    assert found == ["0001", "0002", "0003", "0004", "0005"]


def test_slide_in_silence_goes_to_nearest_word(words):
    text = transcript.render(words, [transcript.Slide("0001", 30.0)])
    assert "→ slide 0001 testing." in text


def test_load_slides_ignores_other_files(tmp_path):
    for name in ["0001_00-00-05.png", "0002_01-02-03.png", "notes.png", "0003_00-00-09.txt"]:
        (tmp_path / name).touch()
    slides = transcript.load_slides(tmp_path)
    assert [(s.number, s.time) for s in slides] == [("0001", 5), ("0002", 3723)]


def test_excerpt_holds_only_words_starting_in_range(words):
    assert transcript.excerpt(words, 2, 4) == "Today we cover testing."
    assert transcript.excerpt(words, 0, 1) == "Welcome to the talk."


def test_excerpt_end_is_exclusive(words):
    assert transcript.excerpt(words, 0, 2) == "Welcome to the talk."


def test_excerpt_empty_range(words):
    assert transcript.excerpt(words, 10, 20) == ""


def test_time_roundtrip():
    assert transcript.format_time(3723.9) == "01:02:03"
    assert transcript.parse_time("01:02:03") == 3723


def test_cli_excerpt_and_out(tmp_path):
    script = str(SCRIPTS / "transcript.py")
    result = subprocess.run(
        [sys.executable, script, str(FIXTURE), "--excerpt", "00:01:05-00:01:06"],
        capture_output=True, text=True, check=True,
    )
    assert result.stdout.strip() == "Now the second"
    out = tmp_path / "t.md"
    subprocess.run([sys.executable, script, str(FIXTURE), "--out", str(out)], check=True)
    assert out.read_text().startswith("[00:00:00] Welcome")


def test_words_without_leading_space_attach_to_previous():
    words = [
        transcript.Word(0, 1, "third"),
        transcript.Word(1, 2, "-party", attached=True),
        transcript.Word(2, 3, "40"),
        transcript.Word(3, 4, "%", attached=True),
    ]
    assert transcript.excerpt(words, 0, 10) == "third-party 40%"
    assert transcript.render(words, []) == "[00:00:00] third-party 40%\n"
