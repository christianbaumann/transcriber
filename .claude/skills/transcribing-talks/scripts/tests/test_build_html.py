import shutil
import subprocess
from html.parser import HTMLParser
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_html  # noqa: E402

FIXTURE = Path(__file__).parent / "fixtures" / "build_html" / "article.md"
needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc missing")
REFERENCING_ATTRS = {"src", "href"}


class LocalRefs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in REFERENCING_ATTRS and value and not value.startswith(("data:", "http", "#")):
                self.refs.append(value)


@pytest.fixture(scope="module")
def html(tmp_path_factory) -> str:
    out = tmp_path_factory.mktemp("out") / "article.html"
    build_html.build(FIXTURE, out)
    return out.read_text(encoding="utf-8")


def test_page_title_uses_first_heading_else_fallback():
    assert build_html.page_title("text\n# Talk\n", "x") == "Talk"
    assert build_html.page_title("no heading", "x") == "x"


@needs_pandoc
def test_images_embedded(html):
    assert html.count("data:image/png;base64") >= 1
    assert "<svg" in html or "data:image/svg+xml" in html


@needs_pandoc
def test_code_table_and_formula_present(html):
    assert "sourceCode" in html
    assert "<table" in html
    assert "katex" in html.lower() and "mc^2" in html


@needs_pandoc
def test_no_local_file_references(html):
    parser = LocalRefs()
    parser.feed(html)
    assert parser.refs == []
    assert "file://" not in html


@needs_pandoc
def test_missing_image_fails_with_path(tmp_path):
    article = tmp_path / "a.md"
    article.write_text("![x](images/nope.png)\n")
    with pytest.raises(build_html.BuildError, match="nope.png"):
        build_html.build(article, tmp_path / "a.html")


def test_missing_pandoc_reports_clearly(monkeypatch, tmp_path):
    monkeypatch.setattr(build_html.shutil, "which", lambda _: None)
    with pytest.raises(build_html.BuildError, match="pandoc not found"):
        build_html.build(FIXTURE, tmp_path / "a.html")


SVG = (FIXTURE.parent / "images" / "diagram.svg").read_text()


@needs_pandoc
@pytest.mark.parametrize("ref,target", [
    ("<my images/a b.png>", "my images/a b.png"),
    ("my%20images/a%20b.png", "my images/a b.png"),
    ("diagrams/x.svg", "diagrams/x.svg"),
])
def test_valid_image_refs_build(tmp_path, ref, target):
    path = tmp_path / target
    path.parent.mkdir(parents=True)
    path.write_text(SVG) if target.endswith(".svg") else shutil.copy(
        FIXTURE.parent / "images" / "slide.png", path)
    article = tmp_path / "a.md"
    article.write_text(f"![x]({ref})\n")
    build_html.build(article, tmp_path / "a.html")


@needs_pandoc
def test_cli_missing_image_exits_1_naming_path(tmp_path):
    article = tmp_path / "a.md"
    article.write_text("![x](images/nope.png)\n")
    script = Path(build_html.__file__)
    result = subprocess.run([sys.executable, str(script), str(article), "--out", str(tmp_path / "a.html")],
                            capture_output=True, text=True)
    assert result.returncode == 1
    assert "images/nope.png" in result.stderr
