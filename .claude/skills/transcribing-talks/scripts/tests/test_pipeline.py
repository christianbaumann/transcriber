import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS))

import pipeline  # noqa: E402

FIXTURES = Path(__file__).parent / "fixtures"
WHISPER = FIXTURES / "whisper.json"


@pytest.fixture
def slices(tmp_path):
    d = tmp_path / "talk-slices"
    d.mkdir()
    for name in ("0001_00-00-00.png", "0002_00-01-00.png"):
        (d / name).write_bytes(b"png")
    return d


def test_slide_excerpts_split_the_transcript_at_slide_times(tmp_path, slices):
    files = pipeline.slide_excerpts(WHISPER, slices, tmp_path / "ex")
    assert [f.name for f in files] == ["0001.txt", "0002.txt"]
    first, second = (f.read_text() for f in files)
    assert first.strip() == "Welcome to the talk. Today we cover testing."
    assert second.strip() == "Now the second part begins here."


def test_chapter_excerpts_follow_outline_ranges(tmp_path):
    outline = tmp_path / "outline.md"
    outline.write_text("---\ntitle: T\n---\n\n## 1. One [00:00:00-00:01:00] slides 1-1\n"
                       "### 1.1 Sub [00:00:00-00:01:00] slides 1-1\n\n"
                       "## 2. Two [00:01:00-end] slides 2-2\n")
    files = pipeline.chapter_excerpts(WHISPER, outline, tmp_path / "ch")
    assert [f.name for f in files] == ["01.txt", "02.txt"]
    assert files[0].read_text().strip() == "Welcome to the talk. Today we cover testing."
    assert files[1].read_text().strip() == "Now the second part begins here."


def test_reference_copies_originals_of_slides_with_review_items(tmp_path):
    article = tmp_path / "review"
    shutil.copytree(FIXTURES / "review", article)
    copied = pipeline.copy_reference(article / "notes", article)
    assert copied
    assert {p.parent for p in copied} == {article / "reference"}
    assert all(p.is_file() for p in copied)


def test_cli_writes_slide_excerpts(tmp_path, slices):
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "pipeline.py"), "slide-excerpts",
         str(WHISPER), str(slices), "--out", str(tmp_path / "ex")],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "2 files"
    assert (tmp_path / "ex" / "0001.txt").is_file()
